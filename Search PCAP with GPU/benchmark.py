#!/usr/bin/env python3
"""
Simple GPU Performance Benchmark
"""

import time
import numpy as np
from gpu_kernels import AdvancedGPUKernels

def run_benchmark():
    print("Running GPU Performance Benchmark...")
    
    # Test data sizes
    text_sizes = [1024*1024, 5*1024*1024, 10*1024*1024]  # 1MB, 5MB, 10MB
    pattern_counts = [5, 10, 20]
    
    kernels = AdvancedGPUKernels()
    
    for text_size in text_sizes:
        for pattern_count in pattern_counts:
            print(f"\nTesting: {text_size//1024//1024}MB text, {pattern_count} patterns")
            
            # Generate test data
            text = np.random.bytes(text_size)
            patterns = [np.random.bytes(10) for _ in range(pattern_count)]
            
            # Test Boyer-Moore
            start_time = time.time()
            for pattern in patterns:
                kernels.boyer_moore_search(text, pattern)
            boyer_moore_time = (time.time() - start_time) * 1000  # Convert to ms
            
            # Test Vectorized
            start_time = time.time()
            kernels.vectorized_multi_search(text, patterns)
            vectorized_time = (time.time() - start_time) * 1000  # Convert to ms
            
            # Test Aho-Corasick
            start_time = time.time()
            kernels.aho_corasick_search(text, patterns)
            aho_corasick_time = (time.time() - start_time) * 1000  # Convert to ms
            
            print(f"  Boyer-Moore: {boyer_moore_time:.2f}ms")
            print(f"  Vectorized: {vectorized_time:.2f}ms")
            print(f"  Aho-Corasick: {aho_corasick_time:.2f}ms")
            
            # Calculate throughput
            throughput_mbps = (text_size / 1024 / 1024) / (max(boyer_moore_time, vectorized_time, aho_corasick_time) / 1000)
            print(f"  Throughput: {throughput_mbps:.2f} MB/s")

if __name__ == "__main__":
    run_benchmark()
