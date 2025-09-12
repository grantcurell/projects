# gpupcapgrep_cupy.py
# Windows-friendly GPU grep for PCAP/PCAPNG using CuPy (CUDA 13.x).
# Adaptive algorithms:
#  - <=16 patterns: BMH on GPU (one pass per pattern; fast for few patterns)
#  - >=17 patterns: PFAC (failureless Aho–Corasick) on GPU (fast for many patterns)
#
# Requires: Python 3.9+, numpy, cupy-cuda13x, NVIDIA GPU with CUDA 13.x runtime.

import argparse, mmap, os, struct, sys, csv, time
from typing import Tuple, List, Dict
import numpy as np
import cupy as cp
from datetime import datetime

# ============================== Capture loaders ==============================

PCAP_GLOBAL_HDR = struct.Struct("<IHHIIII")   # magic, vmaj, vmin, thiszone, sigfigs, snaplen, linktype
PCAP_REC_HDR    = struct.Struct("<IIII")      # ts_sec, ts_usec, incl_len, orig_len

def _load_pcap(mm: mmap.mmap) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    fsize = mm.size()
    if fsize < PCAP_GLOBAL_HDR.size:
        raise ValueError("PCAP too small")
    magic = struct.unpack_from("<I", mm, 0)[0]
    if magic == 0xa1b2c3d4:
        fmt = "<IIII"
    elif magic == 0xd4c3b2a1:
        fmt = ">IIII"
    else:
        raise ValueError("Not a classic PCAP (magic mismatch)")

    pos = PCAP_GLOBAL_HDR.size
    chunks, offsets, lengths = [], [], []
    total = 0
    while pos + PCAP_REC_HDR.size <= fsize:
        ts_sec, ts_usec, incl_len, orig_len = struct.unpack_from(fmt, mm, pos)
        pos += PCAP_REC_HDR.size
        if incl_len == 0 or pos + incl_len > fsize: break
        offsets.append(total)
        lengths.append(incl_len)
        chunks.append(mm[pos:pos+incl_len])
        total += incl_len
        pos += incl_len
    if not lengths:
        raise ValueError("No packets in PCAP")
    return (np.frombuffer(b"".join(chunks), dtype=np.uint8).copy(),
            np.asarray(offsets, dtype=np.uint32),
            np.asarray(lengths, dtype=np.uint32))

def _u32(mem, off, le=True):
    return struct.unpack_from("<I" if le else ">I", mem, off)[0]

def _load_pcapng(mm: mmap.mmap) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    fsize = mm.size()
    if fsize < 12:
        raise ValueError("PCAPNG too small")

    pos = 0
    chunks, offsets, lengths = [], [], []
    total = 0
    le = True

    while pos + 12 <= fsize:
        raw_btype = _u32(mm, pos, le=True)
        raw_blen  = _u32(mm, pos+4, le=True)
        if raw_blen < 12 or pos + raw_blen > fsize:
            break

        if raw_btype == 0x0A0D0D0A:  # SHB
            bom = struct.unpack_from("<I", mm, pos+12)[0]
            le = (bom == 0x1A2B3C4D) or (bom not in (0x1A2B3C4D, 0x4D3C2B1A))
            pos += raw_blen
            continue

        btype = _u32(mm, pos, le)
        blen  = _u32(mm, pos+4, le)
        if blen < 12 or pos + blen > fsize:
            break

        if btype == 0x00000001:  # IDB
            pos += blen
            continue
        elif btype == 0x00000006:  # EPB
            captured_len = _u32(mm, pos+20, le)
            data_off = pos + 28
            data_end = data_off + captured_len
            if data_end <= pos + blen - 4:
                chunks.append(mm[data_off:data_end])
                offsets.append(total)
                lengths.append(captured_len)
                total += captured_len
            pos += blen
            continue
        elif btype == 0x00000003:  # SPB
            body_len = blen - 16
            if body_len > 0 and (pos + 12 + 4 + body_len) <= pos + blen - 4:
                data_off = pos + 12 + 4
                data_end = data_off + body_len
                chunks.append(mm[data_off:data_end])
                offsets.append(total)
                lengths.append(body_len)
                total += body_len
            pos += blen
            continue
        else:
            pos += blen

    if not lengths:
        raise ValueError("No packets in PCAPNG")
    return (np.frombuffer(b"".join(chunks), dtype=np.uint8).copy(),
            np.asarray(offsets, dtype=np.uint32),
            np.asarray(lengths, dtype=np.uint32))

def load_capture_concatenate(path: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    size = os.path.getsize(path)
    if size < 12:
        raise ValueError("File too small")
    with open(path, "rb") as f:
        mm = mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_READ)
        try:
            magic = mm[:4]
            if magic == b"\x0a\x0d\x0d\x0a":
                return _load_pcapng(mm)
            if magic in (b"\xd4\xc3\xb2\xa1", b"\xa1\xb2\xc3\xd4"):
                return _load_pcap(mm)
            if struct.unpack_from("<I", mm, 0)[0] == 0x0A0D0D0A:
                return _load_pcapng(mm)
            raise ValueError("Unknown capture format")
        finally:
            mm.close()

# ============================== Pattern prep ==============================

MAX_PAT_LEN = 512
BMH_MAX_PATTERNS = 16
DEFAULT_LARGE_PKT_THRESHOLD = 2048
DEFAULT_TILE_BYTES = 8192
BLOCK_SIZE = 256

def unescape(s: str) -> bytes:
    out = bytearray(); i = 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s):
            n = s[i+1]
            if n == "x" and i + 3 < len(s):
                out.append(int(s[i+2:i+4], 16)); i += 4
            elif n == "n": out.append(0x0A); i += 2
            elif n == "r": out.append(0x0D); i += 2
            elif n == "t": out.append(0x09); i += 2
            else: out.append(ord(n)); i += 2
        else:
            out.append(ord(s[i])); i += 1
    return bytes(out)

def make_badchar_table(pat: bytes) -> np.ndarray:
    m = len(pat)
    tbl = np.full(256, m, dtype=np.uint8)
    for i in range(m-1):
        tbl[pat[i]] = (m - 1 - i) & 0xFF
    return tbl

# ============================== CuPy RawKernels ==============================

_bmh_small_src = r'''
extern "C" __global__
void bmh_small(const unsigned char* __restrict__ bigbuf,
               const unsigned int* __restrict__ offsets,
               const unsigned int* __restrict__ lengths,
               const int num_packets,
               const unsigned char* __restrict__ pat,
               const int m,
               const unsigned char* __restrict__ badchar, // 256 bytes
               const unsigned int pat_id,
               unsigned int* __restrict__ out_entries, // shape (N,3) flattened
               unsigned long long* __restrict__ out_count,
               const unsigned int out_cap)
{
    int pkt = blockIdx.x;
    if (pkt >= num_packets) return;
    unsigned int start = offsets[pkt];
    unsigned int n = lengths[pkt];
    if (m == 0 || n < (unsigned)m) return;

    // Each thread owns a moving window with BMH skips
    unsigned int i = threadIdx.x;
    while (i <= n - (unsigned)m) {
        unsigned char last = bigbuf[start + i + m - 1];
        int j = m - 1;
        // compare backward
        while (j >= 0 && pat[j] == bigbuf[start + i + j]) { --j; }
        if (j < 0) {
            unsigned long long idx = atomicAdd(out_count, 1ULL);
            if (idx < (unsigned long long)out_cap) {
                unsigned long long base = idx * 3ULL;
                out_entries[base + 0] = (unsigned int)pkt;
                out_entries[base + 1] = i;
                out_entries[base + 2] = pat_id;
            }
            i += m;
        } else {
            unsigned int shift = badchar[last];
            if (shift < 1) shift = 1;
            i += shift;
        }
    }
}
'''.strip()

_bmh_large_src = r'''
extern "C" __global__
void bmh_large(const unsigned char* __restrict__ bigbuf,
               const unsigned int* __restrict__ offsets,
               const unsigned int* __restrict__ lengths,
               const int* __restrict__ large_indices,
               const int num_large,
               const unsigned char* __restrict__ pat,
               const int m,
               const unsigned char* __restrict__ badchar,
               const unsigned int pat_id,
               unsigned int* __restrict__ out_entries,
               unsigned long long* __restrict__ out_count,
               const unsigned int out_cap)
{
    extern __shared__ unsigned char smem[];
    int li = blockIdx.x;
    if (li >= num_large) return;
    int pkt = large_indices[li];
    unsigned int start = offsets[pkt];
    unsigned int n = lengths[pkt];
    if (m == 0 || n < (unsigned)m) return;

    const int TILE_BYTES = %(TILE_BYTES)s;
    unsigned int base = 0;
    while (base < n) {
        unsigned int tl = (n - base > TILE_BYTES) ? TILE_BYTES : (n - base);
        unsigned int overlap = (m > 0) ? (unsigned)(m - 1) : 0;
        unsigned int copy_len = tl + overlap;
        if (base + copy_len > n) copy_len = n - base;

        // cooperative load
        for (unsigned int t = threadIdx.x; t < copy_len; t += blockDim.x) {
            smem[t] = bigbuf[start + base + t];
        }
        __syncthreads();

        int max_start = (int)tl - m;
        if (max_start >= 0) {
            unsigned int i = threadIdx.x;
            while ((int)i <= max_start) {
                unsigned char last = smem[i + m - 1];
                int j = m - 1;
                while (j >= 0 && pat[j] == smem[i + j]) { --j; }
                if (j < 0) {
                    unsigned long long idx = atomicAdd(out_count, 1ULL);
                    if (idx < (unsigned long long)out_cap) {
                        unsigned long long base3 = idx * 3ULL;
                        out_entries[base3 + 0] = (unsigned int)pkt;
                        out_entries[base3 + 1] = base + i;
                        out_entries[base3 + 2] = pat_id;
                    }
                    i += m;
                } else {
                    unsigned int shift = badchar[last];
                    if (shift < 1) shift = 1;
                    i += shift;
                }
            }
        }
        __syncthreads();
        base += tl;
    }
}
'''.strip()

_pfac_small_src = r'''
extern "C" __global__
void pfac_small(const unsigned char* __restrict__ bigbuf,
                const unsigned int* __restrict__ offsets,
                const unsigned int* __restrict__ lengths,
                const int num_packets,
                const int* __restrict__ goto_tbl, // [states*256]
                const int num_states,
                const int* __restrict__ out_index,
                const int* __restrict__ out_counts,
                const int* __restrict__ flat_out,
                const int max_steps,
                unsigned int* __restrict__ out_entries, // (N,3) flattened: pkt, end_off(1-based), pat_id
                unsigned long long* __restrict__ out_count,
                const unsigned int out_cap)
{
    int pkt = blockIdx.x;
    if (pkt >= num_packets) return;
    unsigned int start = offsets[pkt];
    unsigned int n = lengths[pkt];

    for (unsigned int s = threadIdx.x; s < n; s += blockDim.x) {
        int state = 0;
        int steps = 0;
        unsigned int i = s;
        while (i < n && steps < max_steps) {
            unsigned char c = bigbuf[start + i];
            int nxt = goto_tbl[state * 256 + c];
            if (nxt < 0) break;
            state = nxt;
            int cnt = out_counts[state];
            if (cnt > 0) {
                int base = out_index[state];
                for (int t = 0; t < cnt; ++t) {
                    int pat_id = flat_out[base + t];
                    unsigned long long idx = atomicAdd(out_count, 1ULL);
                    if (idx < (unsigned long long)out_cap) {
                        unsigned long long base3 = idx * 3ULL;
                        out_entries[base3 + 0] = (unsigned int)pkt;
                        out_entries[base3 + 1] = (unsigned int)(i + 1);
                        out_entries[base3 + 2] = (unsigned int)pat_id;
                    }
                }
            }
            ++i; ++steps;
        }
    }
}
'''.strip()

_pfac_large_src = r'''
extern "C" __global__
void pfac_large(const unsigned char* __restrict__ bigbuf,
                const unsigned int* __restrict__ offsets,
                const unsigned int* __restrict__ lengths,
                const int* __restrict__ large_indices,
                const int num_large,
                const int* __restrict__ goto_tbl,
                const int num_states,
                const int* __restrict__ out_index,
                const int* __restrict__ out_counts,
                const int* __restrict__ flat_out,
                const int max_steps,
                unsigned int* __restrict__ out_entries,
                unsigned long long* __restrict__ out_count,
                const unsigned int out_cap)
{
    extern __shared__ unsigned char smem[];
    const int TILE_BYTES = %(TILE_BYTES)s;

    int li = blockIdx.x;
    if (li >= num_large) return;
    int pkt = large_indices[li];
    unsigned int start = offsets[pkt];
    unsigned int n = lengths[pkt];

    unsigned int base = 0;
    while (base < n) {
        unsigned int tl = (n - base > TILE_BYTES) ? TILE_BYTES : (n - base);

        for (unsigned int t = threadIdx.x; t < tl; t += blockDim.x) {
            smem[t] = bigbuf[start + base + t];
        }
        __syncthreads();

        for (unsigned int s = threadIdx.x; s < tl; s += blockDim.x) {
            int state = 0;
            int steps = 0;
            unsigned int i = s;
            while (i < tl && steps < max_steps) {
                unsigned char c = smem[i];
                int nxt = goto_tbl[state * 256 + c];
                if (nxt < 0) break;
                state = nxt;
                int cnt = out_counts[state];
                if (cnt > 0) {
                    int base_out = out_index[state];
                    for (int t2 = 0; t2 < cnt; ++t2) {
                        int pat_id = flat_out[base_out + t2];
                        unsigned long long idx = atomicAdd(out_count, 1ULL);
                        if (idx < (unsigned long long)out_cap) {
                            unsigned long long base3 = idx * 3ULL;
                            out_entries[base3 + 0] = (unsigned int)pkt;
                            out_entries[base3 + 1] = base + i + 1;
                            out_entries[base3 + 2] = (unsigned int)pat_id;
                        }
                    }
                }
                ++i; ++steps;
            }
        }
        __syncthreads();
        base += tl;
    }
}
'''.strip()

# Compile kernels once
def build_kernels(tile_bytes: int):
    bmh_small = cp.RawKernel(_bmh_small_src, "bmh_small", options=("--std=c++14",))
    bmh_large = cp.RawKernel(_bmh_large_src % {"TILE_BYTES": str(tile_bytes)}, "bmh_large", options=("--std=c++14",))
    pfac_small = cp.RawKernel(_pfac_small_src, "pfac_small", options=("--std=c++14",))
    pfac_large = cp.RawKernel(_pfac_large_src % {"TILE_BYTES": str(tile_bytes)}, "pfac_large", options=("--std=c++14",))
    return bmh_small, bmh_large, pfac_small, pfac_large

# ============================== PFAC builder (host) ==============================

class PFAC:
    def __init__(self, patterns: List[bytes]):
        self.patterns = patterns
        self.next: List[Dict[int,int]] = [dict()]
        self.out: List[List[int]] = [[]]
        for pid, pat in enumerate(patterns):
            node = 0
            for b in pat:
                node = self.next[node].setdefault(b, len(self.next))
                if node == len(self.out):
                    self.next.append(dict())
                    self.out.append([])
            self.out[node].append(pid)

        # failure links
        fail = [0]*len(self.next)
        from collections import deque
        q = deque()
        for b, v in self.next[0].items():
            fail[v] = 0
            q.append(v)
        while q:
            r = q.popleft()
            for b, s in self.next[r].items():
                q.append(s)
                f = fail[r]
                while f and (b not in self.next[f]):
                    f = fail[f]
                fail[s] = self.next[f].get(b, 0)
                if self.out[fail[s]]:
                    self.out[s].extend(self.out[fail[s]])

        num_states = len(self.next)
        self.max_pat_len = max((len(p) for p in patterns), default=0)

        goto = np.full((num_states, 256), -1, dtype=np.int32)
        for state, trans in enumerate(self.next):
            for b, s in trans.items():
                goto[state, b] = s

        out_counts = np.array([len(lst) for lst in self.out], dtype=np.int32)
        out_index = np.zeros(len(self.out), dtype=np.int32)
        total_out = int(out_counts.sum())
        flat = np.zeros(total_out, dtype=np.int32)
        k = 0
        for i, lst in enumerate(self.out):
            out_index[i] = k
            if lst:
                flat[k:k+len(lst)] = np.array(lst, dtype=np.int32)
                k += len(lst)

        self.goto = goto
        self.out_index = out_index
        self.out_counts = out_counts
        self.flat_out = flat

# ============================== Driver ==============================

def main():
    ap = argparse.ArgumentParser(description="GPU-accelerated PCAP/PCAPNG grep (CuPy; adaptive BMH/PFAC).")
    ap.add_argument("capture", help="Path to .pcap or .pcapng")
    ap.add_argument("-s", "--string", action="append", required=True, help="Search string; supports \\xNN escapes")
    ap.add_argument("--large-threshold", type=int, default=DEFAULT_LARGE_PKT_THRESHOLD, help="Bytes to treat as 'large'")
    ap.add_argument("--tile-bytes", type=int, default=DEFAULT_TILE_BYTES, help="Shared-memory tile size")
    ap.add_argument("--max-matches", type=int, default=2_000_000, help="Cap total reported matches")
    ap.add_argument("--csv-output", help="Output results to CSV file")
    ap.add_argument("--comprehensive-test", action="store_true", help="Run comprehensive test across all PCAP files")
    args = ap.parse_args()

    # Ensure CUDA runtime is present via CuPy
    try:
        _ = cp.cuda.runtime.getDevice()
    except cp.cuda.runtime.CUDARuntimeError as e:
        print("CuPy cannot access CUDA. Ensure CUDA 13.x is installed and install CuPy built for CUDA 13: pip install cupy-cuda13x")
        raise

    patterns = [unescape(s) for s in args.string]
    patterns = [p for p in patterns if p]
    if not patterns:
        print("No non-empty patterns.")
        sys.exit(1)
    if any(len(p) > MAX_PAT_LEN for p in patterns):
        print(f"One or more patterns exceed MAX_PAT_LEN={MAX_PAT_LEN}. Reduce length or adjust constant.")
        sys.exit(1)

    # Start timing
    load_start = time.time()
    bigbuf_h, offsets_h, lengths_h = load_capture_concatenate(args.capture)
    load_time = time.time() - load_start
    num_packets = len(lengths_h)
    total_bytes = len(bigbuf_h)

    # Move capture to GPU
    bigbuf_d = cp.asarray(bigbuf_h, dtype=cp.uint8)
    offsets_d = cp.asarray(offsets_h, dtype=cp.uint32)
    lengths_d = cp.asarray(lengths_h, dtype=cp.uint32)

    # Large index list
    large_idx = np.where(lengths_h >= args.large_threshold)[0].astype(np.int32)
    large_idx_d = cp.asarray(large_idx, dtype=cp.int32) if len(large_idx) else None

    # Output buffers
    out_cap = int(args.max_matches)
    out_entries_d = cp.empty((out_cap, 3), dtype=cp.uint32)  # packet, offset/end, pattern
    out_count_d = cp.zeros((1,), dtype=cp.uint64)

    # Kernels
    bmh_small, bmh_large, pfac_small, pfac_large = build_kernels(args.tile_bytes)

    threads = BLOCK_SIZE
    blocks_small = max(1, num_packets)
    blocks_large = max(1, len(large_idx))

    # Start search timing
    search_start = time.time()
    total_matches = 0

    if len(patterns) <= BMH_MAX_PATTERNS:
        # Few-patterns: BMH per needle
        for pid, p in enumerate(patterns):
            pat_d = cp.asarray(np.frombuffer(p, dtype=np.uint8))
            m = np.int32(len(p))
            badchar_d = cp.asarray(make_badchar_table(p).astype(np.uint8))
            out_count_d.fill(0)

            # small packets path
            bmh_small((blocks_small,), (threads,),
                      (bigbuf_d, offsets_d, lengths_d, np.int32(num_packets),
                       pat_d, m, badchar_d, np.uint32(pid),
                       out_entries_d.ravel(), out_count_d, np.uint32(out_cap)))

            # large packets path
            if len(large_idx):
                shared_mem = args.tile_bytes + (len(p) - 1)
                bmh_large((blocks_large,), (threads,),
                          (bigbuf_d, offsets_d, lengths_d,
                    large_idx_d, np.int32(len(large_idx)),
                           pat_d, m, badchar_d, np.uint32(pid),
                           out_entries_d.ravel(), out_count_d, np.uint32(out_cap)),
                          shared_mem=shared_mem)

            cp.cuda.Device().synchronize()

            count = int(out_count_d.get()[0])
            count = min(count, out_cap)
            total_matches += count
            # Remove individual match printing
            # if count:
            #     entries = out_entries_d.get()[:count]
            #     order = np.lexsort((entries[:,2], entries[:,1], entries[:,0]))
            #     for row in entries[order]:
            #         print(f"packet={int(row[0])} offset={int(row[1])} pattern={int(row[2])}")

    else:
        # Many-patterns: PFAC
        pf = PFAC(patterns)
        goto_d = cp.asarray(pf.goto, dtype=cp.int32).ravel()
        out_index_d = cp.asarray(pf.out_index, dtype=cp.int32)
        out_counts_d = cp.asarray(pf.out_counts, dtype=cp.int32)
        flat_out_d = cp.asarray(pf.flat_out, dtype=cp.int32)
        max_steps = np.int32(pf.max_pat_len)
        out_count_d.fill(0)

        # small packets
        pfac_small((blocks_small,), (threads,),
                   (bigbuf_d, offsets_d, lengths_d, np.int32(num_packets),
                    goto_d, np.int32(pf.goto.shape[0]),
                    out_index_d, out_counts_d, flat_out_d,
                max_steps,
                    out_entries_d.ravel(), out_count_d, np.uint32(out_cap)))

        # large packets
        if len(large_idx):
            pfac_large((blocks_large,), (threads,),
                       (bigbuf_d, offsets_d, lengths_d,
                large_idx_d, np.int32(len(large_idx)),
                        goto_d, np.int32(pf.goto.shape[0]),
                        out_index_d, out_counts_d, flat_out_d,
                max_steps,
                        out_entries_d.ravel(), out_count_d, np.uint32(out_cap)),
                       shared_mem=args.tile_bytes)

        cp.cuda.Device().synchronize()

        count = int(out_count_d.get()[0])
        total_matches = min(count, out_cap)
        # Remove individual match printing
        # if count:
        #     entries = out_entries_d.get()[:count]
        #     # Convert PFAC end offsets (1-based) to start offsets using pattern lengths
        #     pat_lens = np.array([len(p) for p in patterns], dtype=np.int32)
        #     start_offsets = entries[:,1] - pat_lens[entries[:,2]]
        #     order = np.lexsort((entries[:,2], start_offsets, entries[:,0]))
        #     for row in entries[order]:
        #         pid = int(row[2])
        #         end_off = int(row[1])
        #         start_off = end_off - int(pat_lens[pid])
        #         print(f"packet={int(row[0])} offset={start_off} pattern={pid}")

    # End search timing
    search_time = time.time() - search_start
    
    # Calculate throughput (excluding load time)
    file_size_mb = total_bytes / (1024 * 1024)
    throughput = file_size_mb / search_time if search_time > 0 else 0
    
    # Prepare results
    results = {
        'pcap_file': os.path.basename(args.capture),
        'file_size_mb': file_size_mb,
        'num_patterns': len(patterns),
        'load_time': load_time,
        'search_time': search_time,
        'total_time': load_time + search_time,
        'throughput_mbps': throughput,
        'num_matches': total_matches,
        'num_packets': num_packets
    }
    
    # Output results
    if args.csv_output:
        # Write to CSV
        file_exists = os.path.exists(args.csv_output)
        with open(args.csv_output, 'a', newline='') as csvfile:
            fieldnames = ['pcap_file', 'file_size_mb', 'num_patterns', 'load_time', 
                         'search_time', 'total_time', 'throughput_mbps', 'num_matches', 'num_packets']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(results)
        print(f"Results written to {args.csv_output}")
    else:
        # Print summary
        print(f"File: {results['pcap_file']}")
        print(f"Size: {results['file_size_mb']:.2f} MB")
        print(f"Patterns: {results['num_patterns']}")
        print(f"Load time: {results['load_time']:.3f}s")
        print(f"Search time: {results['search_time']:.3f}s")
        print(f"Throughput: {results['throughput_mbps']:.2f} MB/s")
        print(f"Matches: {results['num_matches']:,}")

if __name__ == "__main__":
    main()
