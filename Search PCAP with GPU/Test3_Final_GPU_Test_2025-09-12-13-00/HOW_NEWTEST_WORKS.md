# How newtest Works

This tool scans packet captures on NVIDIA GPUs to find byte strings quickly, even at multi-gigabyte scale. It is written in Python, uses CuPy to launch custom CUDA kernels, and supports both classic PCAP and PCAPNG (Enhanced Packet Blocks and Simple Packet Blocks).

The program automatically chooses the most efficient search algorithm based on how many patterns you pass:

* 1–16 patterns: Boyer–Moore–Horspool (BMH) on the GPU, one pass per pattern
* 17+ patterns: PFAC (failureless Aho–Corasick) on the GPU, one pass over the data

By tiling jumbo packets into shared memory and using one block per packet for small packets, the kernels are efficient across varied traffic mixes.

---

## What this README covers

* What the script does and when to use it
* Supported input formats and pattern encodings
* Installation and environment setup on Windows (CUDA 13.x)
* Command-line usage and examples
* Output formats (stdout summary and optional CSV)
* How it works internally (BMH vs PFAC, kernels, memory layout)
* Performance tuning knobs and guidance
* Troubleshooting common issues
* Implementation notes and limitations
* How to extend or customize

---

## What it does

* Reads a capture file (.pcap or .pcapng) and concatenates all captured packet bytes into one contiguous buffer.
* Builds per-packet offset and length arrays so the GPU can address each packet.
* Accepts N arbitrary byte patterns (including binary via \xNN escape sequences).
* Chooses a GPU algorithm:

  * BMH for up to 16 patterns (fast when the pattern count is small)
  * PFAC for 17+ patterns (scales well when the pattern set is large)
* Splits packets into two execution paths:

  * Small packets: one CUDA block per packet; threads stride candidate positions
  * Large packets: processes in tiles copied to shared memory with m−1 overlap
* Reports summary metrics (load time, search time, throughput, match count, packet count) to stdout, or emits a CSV row if requested.

By default the script prints only a summary, not every individual match. You can enable per-match printing by uncommenting the indicated blocks in the code.

---

## Supported inputs

* Classic PCAP (both little-endian and big-endian headers)
* PCAPNG

  * Enhanced Packet Blocks (EPB)
  * Simple Packet Blocks (SPB)
* Any link type payloads are supported because the search is byte-wise; there’s no protocol parsing unless you add it. The search covers the entire captured frame payload for each packet.

Not supported by default:

* pcapng blocks other than EPB/SPB are skipped; that’s fine for most captures.
* Files that are too small to contain a valid header or are malformed will raise a ValueError.

---

## Pattern syntax

* Pass patterns using `-s`. You can use multiple `-s` flags.
* Strings are interpreted as bytes with C-style escapes:

  * `\xNN` for hex bytes (e.g., `\x16\x03\x01`)
  * `\n`, `\r`, `\t` for newline, carriage return, tab
  * Other characters are taken literally
* Maximum single pattern length is 512 bytes by default (set by `MAX_PAT_LEN`).

Examples:

* `-s "GET /"`
* `-s "\x16\x03\x01"`  (TLS ClientHello start)
* `-s "password"`

---

## Requirements (Windows)

* NVIDIA GPU with CUDA 13.x runtime
* Python 3.9+ (64-bit)
* Packages: numpy, cupy-cuda13x

Install:

```
py -m pip install --upgrade pip
py -m pip install numpy cupy-cuda13x
```

Verify CUDA is available to CuPy:

```
py - << "PY"
import cupy as cp
cp.cuda.runtime.getDevice()
print("GPU OK:", cp.cuda.Device())
PY
```

If that fails, see Troubleshooting.

---

## Quick start

Save your script as `gpupcapgrep_cupy.py` (content at the end of this README is the same code you provided).

Basic run:

```
py gpupcapgrep_cupy.py capture.pcapng -s "password" -s "GET /"
```

Binary pattern:

```
py gpupcapgrep_cupy.py capture.pcap -s "\x16\x03\x01"
```

CSV output (appends a row with performance metrics):

```
py gpupcapgrep_cupy.py capture.pcapng -s "foo" -s "bar" --csv-output results.csv
```

Tuning for very large packets:

```
py gpupcapgrep_cupy.py big.pcapng -s "needle" --large-threshold 4096 --tile-bytes 16384
```

---

## Command-line options

* `capture` (positional): Path to the `.pcap` or `.pcapng` file.
* `-s / --string`: Repeatable; adds one search pattern (supports `\xNN`).
* `--large-threshold` (default 2048): Packet length in bytes at or above which a packet is treated as “large” and processed in shared-memory tiles.
* `--tile-bytes` (default 8192): Tile size (bytes) for the large-packet shared memory path. Increase for fewer global memory reads, decrease to avoid TDR or shared-mem pressure.
* `--max-matches` (default 2,000,000): Upper bound on total matches captured in the device buffer.
* `--csv-output path.csv`: Instead of printing a summary to stdout, append a structured row to the CSV file.
* `--comprehensive-test`: Placeholder switch (no behavior in current code) for running a batch over multiple pcaps; keep for future expansion.

Output summary fields:

* pcap\_file, file\_size\_mb, num\_patterns, load\_time, search\_time,
  total\_time, throughput\_mbps, num\_matches, num\_packets

Note: throughput\_mbps here is MB/s computed as captured bytes / search\_time.

---

## How the program works

### File loading

`load_capture_concatenate` detects file type and dispatches to:

* `_load_pcap`:

  * Validates magic
  * Walks each record header and appends the captured bytes to `chunks`
* `_load_pcapng`:

  * Iterates block by block
  * For EPB: captures `captured_len` bytes starting at the fixed data offset
  * For SPB: uses block length minus headers to find data length
* Finally concatenates `chunks` into one `bigbuf` and builds arrays:

  * `offsets[i]` = starting byte index of packet i within bigbuf
  * `lengths[i]` = length of packet i

These arrays enable packet-aware GPU kernels without copying per-packet buffers.

### Pattern preparation

* Each command-line pattern string is unescaped into raw bytes.
* For BMH: builds a 256-entry bad-character shift table per pattern.

### Algorithm selection

* If `num_patterns <= 16`:

  * Use BMH and scan once per pattern
* Else:

  * Use PFAC (Aho–Corasick without failure transitions in the GPU kernel)

The threshold is chosen to balance two costs:

* BMH per-pattern kernel launch is cheap and often outperforms multi-pattern automata for small pattern sets.
* PFAC amortizes traversal when the pattern set is large.

### Packet scheduling

* Small packets:

  * Grid size = number of packets
  * One block per packet
  * Threads in the block stride candidate start positions
* Large packets:

  * Grid size = number of large packets
  * One block per large packet
  * The block copies a tile (default 8192 bytes) into shared memory
  * A `m−1` overlap is included to catch matches crossing tile boundaries
  * Threads scan the tile concurrently using the chosen algorithm

### GPU kernels (CuPy RawKernel)

The kernels are written in CUDA C++ and compiled at runtime by CuPy:

* `bmh_small` and `bmh_large`:

  * Reverse compare against the pattern
  * Skip ahead by bad-character shift on mismatch
  * Emit matches atomically into a flat `(N,3)` buffer \[packet\_id, start\_offset, pattern\_id]

* `pfac_small` and `pfac_large`:

  * One thread per candidate start position
  * Walk the failureless goto table up to `max_steps` (max pattern length)
  * On reaching a state with outputs, emit each associated pattern id
  * Report end offsets (1-based) in the kernel; host can derive start offset as `end - len(pattern)`

### PFAC automaton construction

On the host:

* Build trie over all patterns
* Compute failure links via BFS
* Merge output lists so every state knows which patterns end there
* Construct a failureless goto table:

  * For missing transitions, set to `-1` so threads terminate early
* Flatten outputs for each state into:

  * `out_index[state]`: start index in `flat_out`
  * `out_counts[state]`: number of pattern ids at that state
  * `flat_out`: contiguous pattern id list

This representation is compact, GPU-friendly, and bounds per-thread work.

---

## Performance tuning

* `--large-threshold`:

  * Lower values push more packets to the shared-memory path, improving cache locality but increasing overhead for very small packets.
  * Higher values keep more packets in the global-memory path which performs fine for tiny frames.

* `--tile-bytes`:

  * Increase if you have headroom in shared memory per SM to reduce the number of global reads.
  * Decrease if you encounter Windows TDR resets or if shared memory becomes a limiting factor.

* Pattern mix:

  * Few patterns: prefer BMH (default behavior); it typically wins on web traffic, short strings, and English-like alphabets.
  * Many patterns: PFAC scales better; consider grouping related patterns to a single run.

* `--max-matches`:

  * If you expect very many matches (e.g., short repetitive patterns), bump this to prevent capping. Keep in mind it controls device memory reserved for results.

* Run-to-run variance:

  * First launch includes JIT compilation of RawKernels; subsequent runs are faster due to kernel caching.

---

## Interpreting the summary

* load\_time: time to memory-map and parse the capture and assemble host arrays.
* search\_time: end-to-end GPU time from copy-in to synchronized completion (not including file load).
* throughput\_mbps: MB of captured data per second of search\_time.
* num\_matches: number of matched windows recorded (capped by `--max-matches`).
* num\_packets: count of frames parsed from the capture.

Note: In the provided script, individual matches are not printed by default. Uncomment the indicated sections if you want per-match reporting. For PFAC, the kernel reports an end offset (1-based) and the host converts that to a start offset using the known pattern length.

---

## Troubleshooting

CuPy cannot access CUDA

* Ensure you installed the CuPy wheel matching your CUDA major version (CUDA 13.x → `cupy-cuda13x`).
* Verify the GPU is available:

  * `nvidia-smi` should list your GPU.
  * `py -c "import cupy as cp; cp.cuda.runtime.getDevice(); print(cp.cuda.Device())"`
* If you installed multiple CUDA versions, ensure CUDA 13.x DLL directories are reachable by the process (usually handled by the CUDA installer; CuPy bundles necessary runtime components with the wheel).

Windows TDR (driver resets during long kernels)

* Reduce `--tile-bytes` so each kernel iteration finishes faster.
* Increase `--large-threshold` to leave more work on the small-packet path.
* If you must, adjust TdrDelay in the registry at your own risk. Prefer keeping kernels short.

Out of memory

* Reduce `--max-matches`.
* Process multiple smaller capture files rather than one extremely large file.
* Ensure other GPU workloads are not consuming memory.

Malformed/unsupported pcapng

* If a capture contains only unsupported blocks (no EPB/SPB), the loader will report “No packets in PCAPNG”.
* Convert using Wireshark/tshark to a standard pcapng with EPB or classic pcap.

No matches reported when you expect some

* Confirm the pattern encoding: binary bytes require `\xNN` escapes.
* Remember the search includes link and network headers; if you want payload-only, add a header parser and pass payload spans to the GPU.

---

## Extending and customizing

Per-match output

* In the code, search for the commented “Remove individual match printing” sections under the BMH and PFAC branches.
* Uncomment to print `packet=<id> offset=<start> pattern=<id>` for each match.

Payload-only search

* Add a lightweight Ethernet/IP/TCP/UDP parser on the host:

  * For each packet, compute payload offset and payload length.
  * Populate `offsets`/`lengths` with payload ranges instead of full frames.
  * No changes needed in the kernels.

Larger patterns

* Increase `MAX_PAT_LEN` and ensure `shared_mem = tile_bytes + (len(pattern) - 1)` remains within the device’s shared memory per block.

Different algorithm threshold

* Adjust `BMH_MAX_PATTERNS` if your workload favors BMH up to a larger count or moves to PFAC earlier.

---

## Security and correctness notes

* This is a byte-wise search. It does not parse protocols and does not attempt reassembly (e.g., TCP streams). It will find signatures that appear within a single captured frame only.
* For compliance or forensic workflows that require precise payload boundaries, add header parsing.
* For encrypted traffic (TLS), searches for cleartext strings will not match post-handshake ciphertext.

---

## Known limitations

* PCAPNG parsing is minimal by design; it handles the common EPB/SPB cases and ignores optional fields.
* PFAC reports every match; for very short patterns with high frequency, you may hit the `--max-matches` cap.
* No multi-GPU support in this script version.
* No streaming of captures in chunks; the file is read and concatenated into a single host buffer, then transferred once to the device. For multi-GB captures and limited VRAM, add chunked processing.

---

## Example sessions

Single pattern:

```
py gpupcapgrep_cupy.py capture.pcap -s "Authorization: Bearer "
```

Binary signature and CSV summary:

```
py gpupcapgrep_cupy.py capture.pcapng -s "\x16\x03\x01" --csv-output bench.csv
type bench.csv
```

Many patterns (PFAC path):

```
py gpupcapgrep_cupy.py capture.pcapng ^
  -s "login" -s "password" -s "GET /" -s "POST /" -s "User-Agent:" -s "Set-Cookie:" ^
  -s "Authorization: Basic" -s "ssh-rsa" -s "ssh-ed25519" -s "Content-Type:" ^
  -s "Host:" -s "Cookie:" -s "HTTP/1.1" -s "HTTP/2" -s "TLS" -s "ClientHello" -s "ServerHello"
```

Tuning tiles for jumbo frames:

```
py gpupcapgrep_cupy.py jumbo.pcapng -s "needle" --tile-bytes 16384 --large-threshold 1024
```

---

## Code structure at a glance

* Capture loaders

  * `_load_pcap`, `_load_pcapng`, `load_capture_concatenate`
* Pattern tools

  * `unescape`, `make_badchar_table`
* Kernels (CuPy RawKernel strings)

  * `_bmh_small_src`, `_bmh_large_src`, `_pfac_small_src`, `_pfac_large_src`
* Kernel compilation

  * `build_kernels`
* PFAC host builder

  * `class PFAC`: builds trie, failure links, goto table, and flattened outputs
* Driver

  * Parses args, loads capture, moves to GPU, chooses algorithm, launches kernels, collects summary (or CSV)

---

## Reproducibility and benchmarking tips

* Include `--csv-output` to log each run with the exact `num_patterns`, `num_packets`, and captured file size.
* Pin your GPU clocks or minimize other GPU activity for stable throughput numbers.
* Warm-up run: the first run includes JIT; ignore it for performance comparisons.
