// gpupcapgrep.cu
// CUDA-accelerated PCAP string search using Boyer–Moore–Horspool.
// Searches entire frames; handles many small packets and large packets efficiently.
// Build: nvcc -O3 -std=c++17 -Xcompiler -fopenmp -lpcap -o gpupcapgrep gpupcapgrep.cu

#include <pcap/pcap.h>
#include <cuda_runtime.h>
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <string>
#include <vector>
#include <iostream>
#include <stdexcept>
#include <algorithm>

#define CUDA_CHECK(call) do { cudaError_t e = (call); if (e != cudaSuccess) { \
  fprintf(stderr, "CUDA error %s:%d: %s\n", __FILE__, __LINE__, cudaGetErrorString(e)); exit(1);} } while(0)

struct Pattern {
  std::string bytes;
  uint8_t badchar[256]; // BMH bad-character shift table
};

struct Match {
  uint32_t packet_id;
  uint32_t offset;
  uint16_t pattern_id;
};

static void make_bmh(const std::string &pat, uint8_t table[256]) {
  const int m = (int)pat.size();
  for (int i=0;i<256;i++) table[i] = (uint8_t)m; // default shift = m
  for (int i=0;i<m-1;i++) table[(uint8_t)pat[i]] = (uint8_t)(m-1-i);
}

// Device constant memory for one pattern at a time (fast access)
__constant__ uint8_t d_pat[512];        // up to 512-byte pattern (tune as needed)
__constant__ int d_pat_len;
__constant__ uint8_t d_badchar[256];

struct PacketView { const uint8_t* base; uint32_t len; };

// Global match buffer bookkeeping
struct GMatches {
  Match* entries;
  unsigned long long* counter;
  unsigned long long capacity;
};

__device__ __forceinline__ bool bmh_find_once(const uint8_t* buf, int n) {
  // Returns true if at least one match exists (used for early-exit variants if needed)
  int m = d_pat_len;
  if (m==0 || n<m) return false;
  int i = 0;
  while (i <= n - m) {
    uint8_t last = buf[i + m - 1];
    int j = m - 1;
    // Compare backwards
    while (j >= 0 && d_pat[j] == buf[i + j]) { --j; }
    if (j < 0) return true;
    i += d_badchar[last];
  }
  return false;
}

__device__ __forceinline__ void bmh_scan_emit(const uint8_t* buf, int n, uint32_t pkt_id, uint16_t pat_id, GMatches g) {
  int m = d_pat_len;
  if (m==0 || n<m) return;
  // stride by blockDim.x * gridDim.x (but we'll use per-block stride below)
  int start = threadIdx.x;
  int step  = blockDim.x;
  // We implement BMH per-thread by scanning candidate windows at positions that this thread owns
  // To preserve correctness, we can't just skip by d_badchar because that's per window; implement a hybrid:
  // Each thread advances 'i' locally with BMH skip logic, starting at its thread-local i.
  for (int i = start; i <= n - m; ) {
    const uint8_t last = buf[i + m - 1];
    int j = m - 1;
    while (j >= 0 && d_pat[j] == buf[i + j]) { --j; }
    if (j < 0) {
      // Emit match
      unsigned long long idx = atomicAdd(g.counter, 1ULL);
      if (idx < g.capacity) {
        g.entries[idx] = Match{pkt_id, (uint32_t)i, pat_id};
      }
      i += m; // on match, advance by m (standard BMH choice)
    } else {
      int shift = d_badchar[last];
      if (shift < 1) shift = 1;
      i += shift;
    }
    // Ensure each thread doesn't starve others; no sync needed
  }
}

// Tunables
constexpr int BLOCK_SIZE = 256;
constexpr int LARGE_PKT_THRESHOLD = 2048;   // bytes
constexpr int TILE_BYTES = 8192;            // shared-memory tile size (<= 48-96KB SMEM budgets across GPUs)
constexpr int OVERLAP_MAX = 511;            // must be >= max pattern length-1 (we set pattern <=512)

__global__ void kernel_small_packets(const uint8_t* __restrict__ bigbuf,
                                     const uint32_t* __restrict__ offsets,
                                     const uint32_t* __restrict__ lengths,
                                     int num_packets,
                                     uint16_t pattern_id,
                                     GMatches g)
{
  int pkt = blockIdx.x;
  if (pkt >= num_packets) return;
  int m = d_pat_len;
  if (m <= 0) return;

  const uint8_t* pkt_ptr = bigbuf + offsets[pkt];
  int n = (int)lengths[pkt];
  if (n < m) return;
  bmh_scan_emit(pkt_ptr, n, pkt, pattern_id, g);
}

__global__ void kernel_large_packets(const uint8_t* __restrict__ bigbuf,
                                     const uint32_t* __restrict__ offsets,
                                     const uint32_t* __restrict__ lengths,
                                     const int* __restrict__ large_indices,
                                     int num_large,
                                     uint16_t pattern_id,
                                     GMatches g)
{
  extern __shared__ uint8_t smem[]; // TILE_BYTES + OVERLAP_MAX
  int list_idx = blockIdx.x;
  if (list_idx >= num_large) return;

  int pkt = large_indices[list_idx];
  int m = d_pat_len;
  if (m <= 0) return;

  const uint8_t* pkt_ptr = bigbuf + offsets[pkt];
  int n = (int)lengths[pkt];
  if (n < m) return;

  // Process packet in tiles with m-1 overlap
  for (int base = 0; base < n; base += TILE_BYTES) {
    int tile_len = min(TILE_BYTES, n - base);
    int overlap = (m > 0) ? (m - 1) : 0;
    int copy_len = tile_len + overlap;
    if (base + copy_len > n) copy_len = n - base;

    // Cooperative load into shared memory
    for (int i = threadIdx.x; i < copy_len; i += blockDim.x) {
      smem[i] = pkt_ptr[base + i];
    }
    __syncthreads();

    // Each thread scans the tile (excluding the final overlap-only region)
    int scan_len = tile_len; // valid starts within [0, tile_len - m]
    const uint8_t* buf = smem;
    int max_start = scan_len - m;
    if (max_start >= 0) {
      int i = threadIdx.x;
      while (i <= max_start) {
        uint8_t last = buf[i + m - 1];
        int j = m - 1;
        while (j >= 0 && d_pat[j] == buf[i + j]) { --j; }
        if (j < 0) {
          unsigned long long idx = atomicAdd(g.counter, 1ULL);
          if (idx < g.capacity) {
            g.entries[idx] = Match{(uint32_t)pkt, (uint32_t)(base + i), pattern_id};
          }
          i += m;
        } else {
          int shift = d_badchar[last];
          if (shift < 1) shift = 1;
          i += shift;
        }
      }
    }
    __syncthreads();
  }
}

// Simple host-side PCAP loader: concatenates all packet bytes into one big buffer
struct PcapData {
  std::vector<uint8_t> bigbuf;
  std::vector<uint32_t> offsets;
  std::vector<uint32_t> lengths;
};

static PcapData load_pcap(const char* path) {
  char errbuf[PCAP_ERRBUF_SIZE];
  pcap_t* p = pcap_open_offline(path, errbuf);
  if (!p) throw std::runtime_error(std::string("pcap_open_offline: ") + errbuf);

  PcapData out;
  out.bigbuf.reserve(1<<26); // pre-reserve 64MB
  const u_char* pkt;
  struct pcap_pkthdr hdr;

  uint64_t total = 0;
  while ((pkt = pcap_next(p, &hdr)) != nullptr) {
    out.offsets.push_back((uint32_t)out.bigbuf.size());
    out.lengths.push_back((uint32_t)hdr.caplen);
    out.bigbuf.insert(out.bigbuf.end(), pkt, pkt + hdr.caplen);
    total += hdr.caplen;
  }
  pcap_close(p);
  // Ensure at least one packet
  if (out.offsets.empty()) throw std::runtime_error("No packets in PCAP.");
  return out;
}

static void usage(const char* argv0) {
  std::cerr << "Usage: " << argv0 << " file.pcap -s <string> [-s <string> ...]\n"
            << "Strings can include C-style hex escapes like \\x00.\n";
}

static std::string unescape(const std::string &in) {
  std::string out;
  out.reserve(in.size());
  for (size_t i=0;i<in.size();) {
    if (in[i]=='\\' && i+1<in.size()) {
      if (in[i+1]=='x' && i+3<in.size()) {
        auto hex = in.substr(i+2,2);
        uint8_t v = (uint8_t)strtoul(hex.c_str(), nullptr, 16);
        out.push_back((char)v);
        i+=4;
      } else {
        char c = in[i+1];
        if (c=='n') out.push_back('\n');
        else if (c=='r') out.push_back('\r');
        else if (c=='t') out.push_back('\t');
        else out.push_back(c);
        i+=2;
      }
    } else {
      out.push_back(in[i++]);
    }
  }
  return out;
}

int main(int argc, char** argv) {
  if (argc < 3) { usage(argv[0]); return 1; }
  const char* pcap_path = argv[1];
  std::vector<Pattern> patterns;

  for (int i=2;i<argc;i++) {
    if (std::string(argv[i]) == "-s") {
      if (i+1>=argc) { usage(argv[0]); return 1; }
      std::string raw = argv[++i];
      std::string un = unescape(raw);
      Pattern p; p.bytes = std::move(un);
      if (p.bytes.empty()) { std::cerr << "Empty pattern ignored\n"; continue; }
      if (p.bytes.size() > 512) { std::cerr << "Pattern too long (max 512 bytes)\n"; return 1; }
      make_bmh(p.bytes, p.badchar);
      patterns.push_back(std::move(p));
    } else {
      std::cerr << "Unknown arg: " << argv[i] << "\n";
      usage(argv[0]);
      return 1;
    }
  }
  if (patterns.empty()) { std::cerr << "No patterns provided.\n"; return 1; }

  // Load PCAP
  PcapData pd;
  try {
    pd = load_pcap(pcap_path);
  } catch (const std::exception &e) {
    std::cerr << "Error: " << e.what() << "\n";
    return 1;
  }

  const int num_packets = (int)pd.offsets.size();

  // Host-side: compute list of large packets indices for the large-kernel path
  std::vector<int> large_indices;
  large_indices.reserve(num_packets/4);
  for (int i=0;i<num_packets;i++) {
    if (pd.lengths[i] >= LARGE_PKT_THRESHOLD) large_indices.push_back(i);
  }

  // Device buffers
  uint8_t* d_bigbuf = nullptr;
  uint32_t *d_offsets=nullptr, *d_lengths=nullptr;
  int* d_large_indices = nullptr;

  CUDA_CHECK(cudaMalloc((void**)&d_bigbuf, pd.bigbuf.size()));
  CUDA_CHECK(cudaMemcpy(d_bigbuf, pd.bigbuf.data(), pd.bigbuf.size(), cudaMemcpyHostToDevice));
  CUDA_CHECK(cudaMalloc((void**)&d_offsets, num_packets*sizeof(uint32_t)));
  CUDA_CHECK(cudaMalloc((void**)&d_lengths, num_packets*sizeof(uint32_t)));
  CUDA_CHECK(cudaMemcpy(d_offsets, pd.offsets.data(), num_packets*sizeof(uint32_t), cudaMemcpyHostToDevice));
  CUDA_CHECK(cudaMemcpy(d_lengths, pd.lengths.data(), num_packets*sizeof(uint32_t), cudaMemcpyHostToDevice));

  if (!large_indices.empty()) {
    CUDA_CHECK(cudaMalloc((void**)&d_large_indices, large_indices.size()*sizeof(int)));
    CUDA_CHECK(cudaMemcpy(d_large_indices, large_indices.data(), large_indices.size()*sizeof(int), cudaMemcpyHostToDevice));
  }

  // Global matches buffer (pre-allocate generous capacity)
  const unsigned long long max_matches = std::max<unsigned long long>(num_packets * 8ULL, 1ULL << 20); // heuristic
  Match* d_matches = nullptr;
  unsigned long long* d_count = nullptr;
  CUDA_CHECK(cudaMalloc((void**)&d_matches, max_matches * sizeof(Match)));
  CUDA_CHECK(cudaMalloc((void**)&d_count, sizeof(unsigned long long)));

  // For each pattern: upload to constant memory and launch kernels
  std::vector<Match> h_matches; h_matches.reserve(1024);
  for (size_t pidx=0; pidx<patterns.size(); ++pidx) {
    const Pattern &pat = patterns[pidx];

    CUDA_CHECK(cudaMemcpyToSymbol(d_pat, pat.bytes.data(), pat.bytes.size(), 0, cudaMemcpyHostToDevice));
    int h_m = (int)pat.bytes.size();
    CUDA_CHECK(cudaMemcpyToSymbol(d_pat_len, &h_m, sizeof(int), 0, cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpyToSymbol(d_badchar, pat.badchar, 256, 0, cudaMemcpyHostToDevice));

    CUDA_CHECK(cudaMemset(d_count, 0, sizeof(unsigned long long)));

    // Launch small packets kernel
    int small_packets = num_packets - (int)large_indices.size();
    if (num_packets > 0) {
      dim3 blocks_small(num_packets); // one block per packet; small packets exit quickly
      kernel_small_packets<<<blocks_small, BLOCK_SIZE>>>(
        d_bigbuf, d_offsets, d_lengths, num_packets,
        (uint16_t)pidx,
        GMatches{d_matches, d_count, max_matches});
    }

    // Launch large packets kernel with shared-memory tiling
    if (!large_indices.empty()) {
      dim3 blocks_large((int)large_indices.size());
      size_t smem_bytes = TILE_BYTES + OVERLAP_MAX;
      kernel_large_packets<<<blocks_large, BLOCK_SIZE, smem_bytes>>>(
        d_bigbuf, d_offsets, d_lengths, d_large_indices, (int)large_indices.size(),
        (uint16_t)pidx,
        GMatches{d_matches, d_count, max_matches});
    }

    CUDA_CHECK(cudaDeviceSynchronize());

    // Copy matches back
    unsigned long long count = 0;
    CUDA_CHECK(cudaMemcpy(&count, d_count, sizeof(unsigned long long), cudaMemcpyDeviceToHost));
    if (count > max_matches) count = max_matches;

    std::vector<Match> temp(count);
    if (count) {
      CUDA_CHECK(cudaMemcpy(temp.data(), d_matches, count*sizeof(Match), cudaMemcpyDeviceToHost));
      // Accumulate
      h_matches.insert(h_matches.end(), temp.begin(), temp.end());
    }
  }

  // Cleanup device
  cudaFree(d_bigbuf); cudaFree(d_offsets); cudaFree(d_lengths);
  if (d_large_indices) cudaFree(d_large_indices);
  cudaFree(d_matches); cudaFree(d_count);

  // Sort matches for stable output: by packet, then offset, then pattern
  std::sort(h_matches.begin(), h_matches.end(), [](const Match&a, const Match&b){
    if (a.packet_id != b.packet_id) return a.packet_id < b.packet_id;
    if (a.offset != b.offset) return a.offset < b.offset;
    return a.pattern_id < b.pattern_id;
  });

  // Print results
  for (const auto &m : h_matches) {
    std::cout << "packet=" << m.packet_id
              << " offset=" << m.offset
              << " pattern=" << m.pattern_id
              << "\n";
  }

  return 0;
}
