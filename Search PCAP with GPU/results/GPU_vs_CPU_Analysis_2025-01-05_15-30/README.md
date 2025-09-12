# GPU vs CPU Performance Analysis - January 5, 2025, 15:30

This folder contains a complete analysis of GPU vs CPU performance for PCAP pattern matching, including all code and data used to generate the results.

## Quick Reproduction Steps

1. **Install Dependencies**:
   ```bash
   pip install cupy-cuda12x scapy pandas colorama
   ```

2. **Run Complete Benchmark**:
   ```bash
   python comprehensive_pattern_benchmark.py
   ```

3. **Run Specific Test**:
   ```bash
   python comprehensive_pattern_benchmark.py --test-id test_001
   ```

4. **Resume Interrupted Benchmark**:
   ```bash
   python comprehensive_pattern_benchmark.py --resume-from test_019
   ```

5. **Quick Validation** (first 3 tests):
   ```bash
   python comprehensive_pattern_benchmark.py --quick
   ```

**Note**: Requires NVIDIA GPU with CUDA support. Results saved to `comprehensive_benchmark_progress.csv`.

## Contents

### Analysis Report
- `GPU_vs_CPU_Performance_Analysis_2025-01-05_15-30.md` - Complete analysis report with findings, methodology, and conclusions

### Benchmark Code
- `comprehensive_pattern_benchmark.py` - Main benchmark script that orchestrates CPU vs GPU comparisons
- `pcap_gpu_scanner.py` - GPU-accelerated PCAP scanner implementation
- `gpu_kernels.py` - CUDA kernel implementations for pattern matching algorithms

### PCAP Generation Scripts
- `create_large_synthetic_pcap.py` - Generates PCAP files with small packets (43-139 bytes average)
- `create_large_packet_pcap.py` - Generates PCAP files with large packets (~26KB average)

### Data Files
- `comprehensive_benchmark_progress.csv` - Complete benchmark results from 25 test scenarios

## Key Findings

- **Packet Size Critical**: GPU performance heavily depends on packet characteristics
- **Small Packets**: GPU is 20-300x slower than CPU and consistently times out
- **Large Packets**: GPU can be competitive (0.19-1.11x speedup) on smaller files
- **Algorithm Selection**: Dynamic algorithm selection based on pattern count
- **Validation Issues**: 40% of tests failed due to GPU timeouts

## Test Coverage

- **25/30 tests completed** (83%)
- **PCAP Sizes**: 50MB, 100MB, 200MB, 500MB, 1000MB
- **Packet Types**: Small packets (43-139 bytes) vs Large packets (~26KB)
- **Pattern Counts**: 1, 7, 14 patterns
- **Algorithms**: Boyer-Moore-Horspool, Aho-Corasick, Vectorized Multi-Pattern, PFAC

## Reproducibility

All code is included to reproduce the analysis. See the methodology section in the main report for detailed execution instructions.

## Generated
- **Date**: January 5, 2025
- **Time**: 15:30
- **Status**: Analysis complete, 5 tests remaining (1GB large packet scenarios)
