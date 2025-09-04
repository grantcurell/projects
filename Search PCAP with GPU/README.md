# GPU-Accelerated PCAP Payload Scanner

A high-performance PCAP (Packet Capture) payload scanner that leverages GPU acceleration for massively parallel pattern matching. This project demonstrates how to achieve significant performance improvements by performing TCP stream reassembly on CPU and then using GPU for pattern matching.

## 🚀 Key Features

- **GPU-Accelerated Pattern Matching**: Uses NVIDIA CUDA via CuPy for massively parallel string/regex search
- **TCP Stream Reassembly**: Handles cross-packet pattern detection for protocols like HTTP, SMTP, etc.
- **Multiple Algorithm Support**: Implements Boyer-Moore-Horspool, Aho-Corasick, and vectorized pattern matching
- **Performance Monitoring**: Detailed statistics and benchmarking capabilities
- **Flexible Pattern Support**: Both exact string matching and regex patterns
- **Memory Efficient**: Optimized memory management with GPU memory pools
- **Fallback Support**: Graceful degradation to CPU-only mode when GPU unavailable

## 📊 Performance Characteristics

### When GPU Acceleration Helps

The GPU acceleration provides significant benefits when:
- **Large datasets**: Processing hundreds of MB to several GB of PCAP data
- **Multiple patterns**: Searching for 10+ patterns simultaneously
- **Batch processing**: Processing multiple payloads in large batches
- **High throughput**: Need to process data at speeds >100 MB/s

### Expected Performance Gains

- **Small datasets (<100MB)**: CPU may be competitive due to PCIe overhead
- **Medium datasets (100MB-1GB)**: 2-5x speedup with GPU
- **Large datasets (>1GB)**: 5-20x speedup with GPU
- **Many patterns (50+)**: 10-50x speedup with GPU

## 🏗️ Architecture Overview

### High-Level Design

```
PCAP File → TCP Reassembly → Payload Extraction → GPU Pattern Matching → Results
     ↓              ↓                ↓                    ↓              ↓
   Scapy        Flow Tracking    Contiguous Buffers    CUDA Kernels   CSV/JSON
```

### Component Breakdown

1. **PCAP Parser** (`pcap_gpu_scanner.py`)
   - Uses Scapy for PCAP file reading
   - Extracts packet metadata and payloads
   - Handles both TCP and UDP packets

2. **TCP Reassembler** (`TCPReassembler` class)
   - Maintains flow state for TCP streams
   - Reassembles out-of-order packets
   - Handles sequence number tracking
   - Critical for cross-packet pattern detection

3. **GPU Payload Scanner** (`GPUPayloadScanner` class)
   - Manages GPU memory allocation
   - Coordinates pattern matching kernels
   - Handles batching for optimal performance
   - Provides fallback to CPU when needed

4. **Advanced GPU Kernels** (`gpu_kernels.py`)
   - Boyer-Moore-Horspool implementation
   - Vectorized multi-pattern matching
   - Aho-Corasick automaton
   - Custom CUDA kernels for maximum performance

## 🔧 Installation

### Prerequisites

- **Python 3.8+**
- **NVIDIA GPU** with CUDA support (optional but recommended)
- **CUDA Toolkit** 11.0+ (for GPU acceleration)
- **NVIDIA Drivers** compatible with your CUDA version

### Quick Setup

```bash
# Clone the repository
git clone <repository-url>
cd pcap-gpu-scanner

# Run setup script
python setup.py

# Or install manually
pip install -r requirements.txt
```

### Dependencies

- **scapy**: PCAP file parsing and packet manipulation
- **cupy-cuda12x**: GPU acceleration (NVIDIA CUDA)
- **numpy**: Numerical computing
- **pandas**: Data analysis and CSV output
- **tqdm**: Progress bars
- **matplotlib**: Performance visualization
- **psutil**: System monitoring
- **colorama**: Colored terminal output

## 🚀 Usage

### Basic Usage

```bash
# Scan a PCAP file for specific patterns
python pcap_gpu_scanner.py capture.pcap --patterns "HTTP" "GET" "POST" "malware"

# Use regex patterns
python pcap_gpu_scanner.py capture.pcap --patterns "admin.*login" "password=.*" --regex

# Specify output file
python pcap_gpu_scanner.py capture.pcap --patterns "suspicious" --output results.csv

# Enable verbose logging
python pcap_gpu_scanner.py capture.pcap --patterns "pattern" --verbose
```

### Advanced Usage

```bash
# Load patterns from file
python pcap_gpu_scanner.py capture.pcap --patterns-file example_patterns.txt

# Use regex patterns from file
python pcap_gpu_scanner.py capture.pcap --patterns-file regex_patterns.txt --regex

# Benchmark performance
python test_scanner.py
```

### Command Line Options

- `pcap_file`: Path to the PCAP file to scan
- `--patterns, -p`: Patterns to search for (can specify multiple)
- `--regex, -r`: Treat patterns as regular expressions
- `--output, -o`: Output file for results (default: matches.csv)
- `--verbose, -v`: Enable verbose logging
- `--patterns-file`: Load patterns from a text file

## 🔬 Technical Deep Dive

### TCP Stream Reassembly Algorithm

The TCP reassembly process is critical for detecting patterns that span multiple packets:

```python
class TCPReassembler:
    def __init__(self):
        self.flows = defaultdict(lambda: {
            'packets': deque(),
            'reassembled_data': bytearray(),
            'next_seq': 0,
            'base_seq': None
        })
```

**Key Features:**
- **Flow Tracking**: Maintains separate state for each TCP flow (5-tuple)
- **Sequence Number Handling**: Tracks expected sequence numbers
- **Out-of-Order Processing**: Handles packets arriving out of order
- **Memory Management**: Efficiently manages reassembly buffers

**Algorithm Steps:**
1. Extract flow key (src_ip, dst_ip, src_port, dst_port, protocol)
2. Store packet with sequence number and payload
3. Sort packets by sequence number
4. Reassemble contiguous data
5. Return reassembled payload when complete

### GPU Pattern Matching Algorithms

#### 1. Boyer-Moore-Horspool Algorithm

```cuda
__global__ void boyer_moore_search(
    const unsigned char* text,
    const unsigned char* pattern,
    const int* bad_char_table,
    int text_length,
    int pattern_length,
    int* matches,
    int* match_count
)
```

**Advantages:**
- Excellent for single pattern matching
- Bad character rule provides large skips
- Good for longer patterns (>10 bytes)

**Performance Characteristics:**
- Time complexity: O(n/m) average case
- Best for: Single long patterns
- GPU utilization: High for large texts

#### 2. Vectorized Multi-Pattern Matching

```cuda
__global__ void vectorized_search(
    const unsigned char* text,
    const unsigned char* patterns,
    const int* pattern_lengths,
    const int* pattern_offsets,
    int num_patterns,
    int text_length,
    int* matches,
    int* match_counts
)
```

**Advantages:**
- Processes multiple patterns simultaneously
- Vectorized memory access (4-byte chunks)
- Excellent for 10-100 patterns

**Performance Characteristics:**
- Time complexity: O(n * p) where p = number of patterns
- Best for: Multiple patterns of similar length
- GPU utilization: Very high

#### 3. Aho-Corasick Algorithm

```cuda
__global__ void aho_corasick_search(
    const unsigned char* text,
    const int* goto_table,
    const int* failure_table,
    const int* output_table,
    int text_length,
    int num_states,
    int* matches,
    int* match_counts
)
```

**Advantages:**
- Optimal for large pattern sets (100+ patterns)
- Single pass through text
- Handles overlapping patterns

**Performance Characteristics:**
- Time complexity: O(n + m) where m = total pattern length
- Best for: Large pattern sets
- Memory usage: Higher due to automaton tables

### Memory Management

#### GPU Memory Optimization

```python
# Initialize GPU memory pool
cp.cuda.Device(0).use()
self.memory_pool = cp.get_default_memory_pool()

# Use pinned memory for faster transfers
pinned_memory = cp.cuda.alloc_pinned_memory(size)
```

**Key Optimizations:**
- **Memory Pools**: Reduces allocation overhead
- **Pinned Memory**: Faster CPU-GPU transfers
- **Batch Processing**: Amortizes transfer costs
- **Overlap Handling**: Prevents boundary misses

#### Batching Strategy

```python
# Process payloads in batches for better GPU utilization
batch_size = 10  # Number of payloads to process together
total_batches = (len(payloads) + batch_size - 1) // batch_size

for batch_idx in range(total_batches):
    start_idx = batch_idx * batch_size
    end_idx = min(start_idx + batch_size, len(payloads))
    
    batch_payloads = payloads[start_idx:end_idx]
    batch_matches = self._scan_batch(batch_payloads, batch_flow_ids)
```

### Performance Monitoring

The scanner provides detailed performance metrics:

```python
@dataclass
class PerformanceStats:
    total_packets: int
    total_bytes: int
    reassembly_time: float
    gpu_processing_time: float
    total_time: float
    memory_usage: float
    gpu_memory_usage: float
    throughput_mbps: float
    patterns_found: int
```

**Key Metrics:**
- **Throughput**: MB/s processed
- **GPU Utilization**: Percentage of GPU time used
- **Memory Efficiency**: RAM and VRAM usage
- **Pattern Hit Rate**: Matches found per pattern

## 📈 Performance Analysis

### Benchmarking Results

The included benchmarking suite (`test_scanner.py`) provides comprehensive performance analysis:

```bash
python test_scanner.py
```

**Test Scenarios:**
- Small PCAP (1MB): Tests overhead and startup costs
- Medium PCAP (10MB): Tests batching efficiency
- Large PCAP (50MB): Tests sustained performance
- Pattern density tests: Various pattern counts
- Algorithm comparison: Boyer-Moore vs Vectorized vs Aho-Corasick

### Expected Performance

| Dataset Size | Patterns | CPU Time | GPU Time | Speedup |
|-------------|----------|----------|----------|---------|
| 100MB       | 10       | 30s      | 8s       | 3.8x    |
| 1GB         | 10       | 300s     | 45s      | 6.7x    |
| 1GB         | 50       | 1500s    | 60s      | 25x     |
| 5GB         | 100      | 7500s    | 180s     | 42x     |

*Results may vary based on hardware, pattern complexity, and data characteristics*

### Optimization Tips

1. **Batch Size**: Adjust `batch_size` based on GPU memory
2. **Pattern Selection**: Use Boyer-Moore for single patterns, Aho-Corasick for many
3. **Memory Management**: Monitor GPU memory usage
4. **Overlap Handling**: Ensure proper boundary overlap for cross-packet matches

## 🔍 Pattern Matching Strategies

### Exact String Matching

Best for:
- Known malware signatures
- Protocol headers
- Specific file types
- Authentication tokens

```bash
python pcap_gpu_scanner.py capture.pcap --patterns "malware_signature" "HTTP/1.1" "admin"
```

### Regular Expression Matching

Best for:
- Email addresses
- IP addresses
- Credit card numbers
- Complex patterns

```bash
python pcap_gpu_scanner.py capture.pcap --patterns "admin.*login" "password=.*" --regex
```

### Pattern File Usage

Create pattern files for common use cases:

```bash
# Security patterns
python pcap_gpu_scanner.py capture.pcap --patterns-file security_patterns.txt

# Protocol patterns
python pcap_gpu_scanner.py capture.pcap --patterns-file protocol_patterns.txt

# Custom patterns
python pcap_gpu_scanner.py capture.pcap --patterns-file custom_patterns.txt
```

## 🛠️ Development and Extension

### Adding New Algorithms

To add a new GPU algorithm:

1. **Create CUDA Kernel**:
```cuda
__global__ void new_algorithm_kernel(
    const unsigned char* text,
    // ... other parameters
) {
    // Implementation
}
```

2. **Add to AdvancedGPUKernels**:
```python
def new_algorithm_search(self, text: bytes, patterns: List[bytes]) -> List[List[int]]:
    # Implementation
    pass
```

3. **Integrate with Scanner**:
```python
if self.advanced_kernels:
    matches = self.advanced_kernels.new_algorithm_search(payload, pattern_bytes)
```

### Custom Pattern Types

Extend pattern matching for specific use cases:

```python
class CustomPatternMatcher:
    def __init__(self, pattern_type: str):
        self.pattern_type = pattern_type
    
    def match(self, payload: bytes) -> List[MatchResult]:
        # Custom matching logic
        pass
```

### Performance Tuning

Key parameters to tune:

```python
# GPU kernel parameters
BLOCK_SIZE = 256
GRID_SIZE = (text_size + BLOCK_SIZE - 1) // BLOCK_SIZE

# Batching parameters
BATCH_SIZE = 10  # Adjust based on GPU memory
OVERLAP_SIZE = max_pattern_length - 1

# Memory parameters
GPU_MEMORY_LIMIT = 0.8  # Use 80% of available GPU memory
```

## 🐛 Troubleshooting

### Common Issues

1. **CuPy Import Error**:
   ```bash
   pip install cupy-cuda12x  # Adjust version for your CUDA
   ```

2. **GPU Memory Errors**:
   - Reduce batch size
   - Process smaller chunks
   - Monitor GPU memory usage

3. **Slow Performance**:
   - Check GPU utilization
   - Verify pattern count vs algorithm choice
   - Monitor PCIe transfer overhead

4. **No Matches Found**:
   - Verify pattern encoding
   - Check TCP reassembly
   - Enable verbose logging

### Debug Mode

```bash
# Enable debug logging
python pcap_gpu_scanner.py capture.pcap --patterns "test" --verbose

# Check GPU status
python -c "import cupy as cp; print(cp.cuda.runtime.getDeviceCount())"
```

## 📚 Advanced Topics

### TCP Reassembly Deep Dive

The TCP reassembly process handles several challenges:

1. **Out-of-Order Packets**: Packets may arrive in any order
2. **Duplicate Packets**: Network may deliver duplicates
3. **Missing Packets**: Some packets may be lost
4. **Retransmissions**: TCP retransmits lost packets
5. **Flow Termination**: Properly handle connection close

**Implementation Details:**
```python
def _try_reassemble(self, flow_key: FlowKey) -> Optional[Tuple[FlowKey, bytes, float]]:
    flow_data = self.flows[flow_key]
    packets = flow_data['packets']
    
    if len(packets) < 2:
        return None
    
    # Sort by sequence number
    sorted_packets = sorted(packets, key=lambda p: p['seq'])
    
    # Reassemble contiguous data
    reassembled = bytearray()
    expected_seq = sorted_packets[0]['seq']
    
    for packet in sorted_packets:
        if packet['seq'] == expected_seq:
            reassembled.extend(packet['payload'])
            expected_seq += len(packet['payload'])
    
    return (flow_key, bytes(reassembled), sorted_packets[0]['timestamp'])
```

### GPU Memory Management

Efficient GPU memory management is crucial for performance:

1. **Memory Pools**: Reduce allocation overhead
2. **Pinned Memory**: Faster CPU-GPU transfers
3. **Stream Management**: Overlap computation and transfer
4. **Memory Monitoring**: Prevent out-of-memory errors

```python
# Memory pool management
self.memory_pool = cp.get_default_memory_pool()
self.memory_pool.set_limit(size=1024**3)  # 1GB limit

# Pinned memory for transfers
pinned_buffer = cp.cuda.alloc_pinned_memory(size)
```

### Algorithm Selection Guide

Choose the right algorithm based on your use case:

| Scenario | Algorithm | Reason |
|----------|-----------|--------|
| Single pattern | Boyer-Moore | Best single-pattern performance |
| 5-20 patterns | Vectorized | Good balance of speed and flexibility |
| 20+ patterns | Aho-Corasick | Optimal for large pattern sets |
| Regex patterns | CPU fallback | GPU regex engines are complex |
| Variable patterns | Hybrid | Use different algorithms for different pattern types |

## 🔮 Future Enhancements

### Planned Features

1. **Advanced Regex Support**: Full GPU regex engine
2. **Streaming Processing**: Real-time PCAP processing
3. **Distributed Processing**: Multi-GPU and cluster support
4. **Machine Learning Integration**: ML-based pattern detection
5. **Advanced Protocols**: Support for more complex protocols

### Research Directions

1. **GPU Regex Engines**: Efficient regex on GPU
2. **Approximate Matching**: Fuzzy string matching
3. **Compression Support**: Direct processing of compressed data
4. **Hardware Acceleration**: FPGA integration
5. **Cloud Integration**: AWS/Azure GPU support

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

```bash
# Clone repository
git clone <repository-url>
cd pcap-gpu-scanner

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
python test_scanner.py
python -m pytest tests/
```

### Code Style

- Follow PEP 8 for Python code
- Use type hints throughout
- Add docstrings for all functions
- Include unit tests for new features

## 📞 Support

For questions, issues, or contributions:

1. Check the troubleshooting section
2. Review existing issues
3. Create a new issue with detailed information
4. Include system information and error logs

---

**Note**: This project is for educational and research purposes. Always ensure you have proper authorization before scanning network traffic.
