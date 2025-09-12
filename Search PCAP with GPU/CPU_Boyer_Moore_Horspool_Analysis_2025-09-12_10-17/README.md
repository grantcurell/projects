# CPU Boyer-Moore-Horspool PCAP Scanner Analysis

## Overview

This analysis implements and evaluates a CPU-based PCAP scanner using the Boyer-Moore-Horspool algorithm. The implementation uses pure Python with sequential processing to test pattern matching performance across 1, 7, and 14 patterns.

## Key Findings

- **Single Pattern Performance**: Excellent performance (~61 MB/s) for single patterns
- **Multi-Pattern Scaling**: Significant performance degradation with multiple patterns
- **Sequential Processing**: Each pattern requires full dataset scan
- **CPU Implementation**: Pure Python implementation provides baseline performance metrics

## Files

- `cpu_scanner.py`: Main CPU implementation
- `cpu_benchmark.py`: Benchmark runner
- `cpu_scanner_results.csv`: Detailed results in CSV format
- `cpu_scanner_results.json`: Structured results in JSON format
- `CPU_Boyer_Moore_Horspool_Analysis_2025-09-12_10-17.md`: Detailed analysis report

## Usage

```bash
# Run CPU benchmark
python cpu_scanner.py

# Run comprehensive benchmark
python cpu_benchmark.py
```

## Results Summary

| Pattern Count | Average Throughput | Performance |
|---------------|-------------------|-------------|
| 1 Pattern     | 61.40 MB/s        | Excellent   |
| 7 Patterns    | 6.12 MB/s         | 10x slower  |
| 14 Patterns   | 3.07 MB/s         | 20x slower  |

## Technical Details

- **Algorithm**: Boyer-Moore-Horspool with bad character rule
- **Implementation**: Pure Python, sequential processing
- **Memory**: System RAM
- **Processing**: CPU-only, no GPU acceleration

## Conclusions

The Boyer-Moore-Horspool algorithm excels at single-pattern matching but suffers from linear scaling issues with multiple patterns due to sequential processing requirements. This implementation provides a baseline for comparing against GPU-accelerated alternatives.