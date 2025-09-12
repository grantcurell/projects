# Test 3: GPU-Accelerated PCAP Scanner

## Overview

This folder contains the successful GPU-accelerated PCAP scanner implementation that achieved **2,741 MB/s peak throughput** - a 45x improvement over CPU implementation. The scanner uses CuPy (CUDA) for GPU acceleration with adaptive algorithms.

## Files Explained

### `newtest.py` - Main GPU Scanner
- **Purpose**: The actual GPU-accelerated PCAP scanner implementation
- **Technology**: Uses CuPy (CUDA) for GPU acceleration
- **Algorithms**: 
  - **≤16 patterns**: Boyer-Moore-Horspool on GPU (one pass per pattern)
  - **≥17 patterns**: PFAC (Parallel Finite Automaton for Content) on GPU
- **Features**: 
  - Loads PCAP files using memory mapping
  - Processes patterns on GPU using CUDA kernels
  - Outputs results to CSV with timing and throughput metrics
  - Handles both small and large packet files efficiently

### `run_comprehensive_test.py` - Test Automation Script
- **Purpose**: Automates running `newtest.py` across all test combinations
- **Function**: 
  - Defines 3 pattern sets (1, 7, 14 patterns)
  - Defines 10 PCAP files (5 small packet + 5 large packet)
  - Runs 30 total test combinations (10 files × 3 pattern counts)
  - Executes `python newtest.py` commands with different parameters
  - Saves results to timestamped CSV file
- **Output**: Generates `gpu_test_results_2025-09-12_12-47-35.csv`

### `gpu_test_results_2025-09-12_12-47-35.csv` - Test Results Data
- **Purpose**: Contains the actual performance results from all 30 test runs
- **Columns**: 
  - `pcap_file`, `file_size_mb`, `num_patterns`
  - `load_time`, `search_time`, `total_time`
  - `throughput_mbps`, `num_matches`, `num_packets`
- **Data**: Shows the 2,741 MB/s peak performance and all other results
- **Usage**: Raw data for analysis and reporting

### `GPU_PCAP_Performance_Report_2025-09-12.md` - Analysis Report
- **Purpose**: Human-readable analysis of the test results
- **Content**: 
  - Executive summary with key findings
  - Performance analysis by file type and pattern count
  - Technical insights and recommendations
  - Detailed breakdown of results
- **Value**: Explains what the numbers mean and why performance varies

## How They Work Together

1. **`run_comprehensive_test.py`** orchestrates the testing
2. **`newtest.py`** does the actual GPU-accelerated scanning
3. **`gpu_test_results_*.csv`** stores the raw performance data
4. **`GPU_PCAP_Performance_Report_*.md`** provides human-readable analysis

## Key Achievements

- **Peak throughput**: 2,741 MB/s (500MB large packets, single pattern)
- **45x improvement** over CPU implementation (61 MB/s)
- **Scalability**: Handles files up to 1GB efficiently
- **Adaptive algorithms**: BMH for ≤7 patterns, PFAC for ≥14 patterns
- **Match accuracy**: Over 21 million matches found across all tests

## Usage

```bash
# Run comprehensive test
python run_comprehensive_test.py

# Run single test
python newtest.py "PCAP Files/synthetic_200mb.pcapng" -s password --csv-output results.csv
```

## Requirements

- Python 3.9+
- CuPy (CUDA 13.x)
- NVIDIA GPU with CUDA support
- PCAP/PCAPNG files for testing

This is a complete testing and analysis pipeline that demonstrates the GPU scanner's capabilities across different workloads and provides both raw data and interpreted results.
