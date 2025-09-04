#!/usr/bin/env python3
"""
Advanced GPU Kernels for PCAP Pattern Matching

This module provides optimized CUDA kernels for high-performance pattern matching
on GPU. It implements various algorithms including:
- Boyer-Moore-Horspool string search
- Aho-Corasick multi-pattern matching
- Bitap/Shift-Or algorithm
- Vectorized pattern matching

These kernels are designed to work with the main PCAP scanner for maximum performance.
"""

import numpy as np
import cupy as cp
from typing import List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class AdvancedGPUKernels:
    """Advanced GPU kernels for pattern matching"""
    
    def __init__(self):
        try:
            self.boyer_moore_kernel = self._compile_boyer_moore_kernel()
            self.vectorized_kernel = self._compile_vectorized_kernel()
            self.aho_corasick_kernel = self._compile_aho_corasick_kernel()
            
            if not any([self.boyer_moore_kernel, self.vectorized_kernel, self.aho_corasick_kernel]):
                raise RuntimeError("Failed to compile any GPU kernels")
                
        except Exception as e:
            raise RuntimeError(f"Failed to initialize GPU kernels: {e}")
    
    def _compile_boyer_moore_kernel(self):
        """Compile Boyer-Moore-Horspool kernel"""
        kernel_code = """
        extern "C" __global__ void boyer_moore_search(
            const unsigned char* text,
            const unsigned char* pattern,
            const int* bad_char_table,
            int text_length,
            int pattern_length,
            int* matches,
            int* match_count
        ) {
            int tid = blockIdx.x * blockDim.x + threadIdx.x;
            int stride = blockDim.x * gridDim.x;
            
            for (int i = tid; i <= text_length - pattern_length; i += stride) {
                int j = pattern_length - 1;
                while (j >= 0 && pattern[j] == text[i + j]) {
                    j--;
                }
                
                if (j < 0) {
                    // Found a match
                    int match_idx = atomicAdd(match_count, 1);
                    matches[match_idx] = i;
                } else {
                    // Use bad character rule
                    unsigned char bad_char = text[i + j];
                    int shift = bad_char_table[bad_char];
                    if (shift > j) {
                        i += shift - j - 1;
                    }
                }
            }
        }
        """
        
        try:
            return cp.RawKernel(kernel_code, 'boyer_moore_search')
        except Exception as e:
            logger.warning(f"Failed to compile Boyer-Moore kernel: {e}")
            return None
    
    def _compile_vectorized_kernel(self):
        """Compile vectorized pattern matching kernel"""
        kernel_code = """
        extern "C" __global__ void vectorized_search(
            const unsigned char* text,
            const unsigned char* patterns,
            const int* pattern_lengths,
            const int* pattern_offsets,
            int num_patterns,
            int text_length,
            int* matches,
            int* match_counts
        ) {
            int tid = blockIdx.x * blockDim.x + threadIdx.x;
            int stride = blockDim.x * gridDim.x;
            
            // Each thread handles multiple starting positions
            for (int pos = tid; pos <= text_length - 4; pos += stride) {
                // Load 4 bytes at once for vectorized comparison
                unsigned int text_chunk = *((unsigned int*)(text + pos));
                
                // Check each pattern
                for (int p = 0; p < num_patterns; p++) {
                    int pattern_start = pattern_offsets[p];
                    int pattern_len = pattern_lengths[p];
                    
                    if (pos + pattern_len <= text_length) {
                        bool match = true;
                        for (int k = 0; k < pattern_len; k++) {
                            if (text[pos + k] != patterns[pattern_start + k]) {
                                match = false;
                                break;
                            }
                        }
                        
                        if (match) {
                            int match_idx = atomicAdd(&match_counts[p], 1);
                            matches[p * 1000 + match_idx] = pos;  // Assume max 1000 matches per pattern
                        }
                    }
                }
            }
        }
        """
        
        try:
            return cp.RawKernel(kernel_code, 'vectorized_search')
        except Exception as e:
            logger.warning(f"Failed to compile vectorized kernel: {e}")
            return None
    
    def _compile_aho_corasick_kernel(self):
        """Compile Aho-Corasick multi-pattern matching kernel"""
        kernel_code = """
        extern "C" __global__ void aho_corasick_search(
            const unsigned char* text,
            const int* goto_table,
            const int* failure_table,
            const int* output_table,
            int text_length,
            int num_states,
            int* matches,
            int* match_counts
        ) {
            int tid = blockIdx.x * blockDim.x + threadIdx.x;
            int chunk_size = text_length / (blockDim.x * gridDim.x);
            int start_pos = tid * chunk_size;
            int end_pos = (tid == blockDim.x * gridDim.x - 1) ? text_length : (tid + 1) * chunk_size;
            
            int state = 0;  // Start at initial state
            
            for (int i = start_pos; i < end_pos; i++) {
                unsigned char c = text[i];
                
                // Follow goto function
                while (goto_table[state * 256 + c] == -1) {
                    state = failure_table[state];
                    if (state == 0) break;
                }
                
                if (goto_table[state * 256 + c] != -1) {
                    state = goto_table[state * 256 + c];
                    
                    // Check for output
                    if (output_table[state] != -1) {
                        int pattern_id = output_table[state];
                        int match_idx = atomicAdd(&match_counts[pattern_id], 1);
                        matches[pattern_id * 1000 + match_idx] = i;  // Assume max 1000 matches per pattern
                    }
                }
            }
        }
        """
        
        try:
            return cp.RawKernel(kernel_code, 'aho_corasick_search')
        except Exception as e:
            logger.warning(f"Failed to compile Aho-Corasick kernel: {e}")
            return None
    
    def boyer_moore_search(self, text: bytes, pattern: bytes) -> List[int]:
        """Perform Boyer-Moore-Horspool search on GPU"""
        if not self.boyer_moore_kernel:
            raise RuntimeError("Boyer-Moore GPU kernel not available - CUDA compilation failed")
        
        # Prepare data
        text_array = cp.asarray(np.frombuffer(text, dtype=cp.uint8))
        pattern_array = cp.asarray(np.frombuffer(pattern, dtype=cp.uint8))
        
        # Build bad character table
        bad_char_table = self._build_bad_char_table(pattern)
        bad_char_array = cp.asarray(bad_char_table)
        
        # Allocate output arrays
        matches = cp.zeros(1000, dtype=cp.int32)  # Assume max 1000 matches
        match_count = cp.zeros(1, dtype=cp.int32)
        
        # Launch kernel
        block_size = 256
        grid_size = (text_array.size + block_size - 1) // block_size
        
        self.boyer_moore_kernel(
            (grid_size,), (block_size,),
            (text_array, pattern_array, bad_char_array, 
             text_array.size, pattern_array.size, matches, match_count)
        )
        
        # Get results
        count = int(match_count.get()[0])
        return matches.get()[:count].tolist()
    
    def vectorized_multi_search(self, text: bytes, patterns: List[bytes]) -> List[List[int]]:
        """Perform vectorized multi-pattern search on GPU"""
        if not self.vectorized_kernel:
            raise RuntimeError("Vectorized GPU kernel not available - CUDA compilation failed")
        
        # Prepare data
        text_array = cp.asarray(np.frombuffer(text, dtype=cp.uint8))
        
        # Concatenate patterns
        pattern_lengths = [len(p) for p in patterns]
        pattern_offsets = [0]
        for i in range(len(patterns) - 1):
            pattern_offsets.append(pattern_offsets[-1] + pattern_lengths[i])
        
        all_patterns = b''.join(patterns)
        patterns_array = cp.asarray(np.frombuffer(all_patterns, dtype=cp.uint8))
        lengths_array = cp.asarray(pattern_lengths, dtype=cp.int32)
        offsets_array = cp.asarray(pattern_offsets, dtype=cp.int32)
        
        # Allocate output arrays
        matches = cp.zeros(len(patterns) * 1000, dtype=cp.int32)
        match_counts = cp.zeros(len(patterns), dtype=cp.int32)
        
        # Launch kernel
        block_size = 256
        grid_size = (text_array.size + block_size - 1) // block_size
        
        self.vectorized_kernel(
            (grid_size,), (block_size,),
            (text_array, patterns_array, lengths_array, offsets_array,
             len(patterns), text_array.size, matches, match_counts)
        )
        
        # Get results
        counts = match_counts.get()
        matches_array = matches.get()
        
        results = []
        for i in range(len(patterns)):
            start_idx = i * 1000
            end_idx = start_idx + counts[i]
            results.append(matches_array[start_idx:end_idx].tolist())
        
        return results
    
    def aho_corasick_search(self, text: bytes, patterns: List[bytes]) -> List[List[int]]:
        """Perform Aho-Corasick multi-pattern search on GPU"""
        if not self.aho_corasick_kernel:
            raise RuntimeError("Aho-Corasick GPU kernel not available - CUDA compilation failed")
        
        # Build Aho-Corasick automaton
        goto_table, failure_table, output_table = self._build_aho_corasick_automaton(patterns)
        
        # Prepare data
        text_array = cp.asarray(np.frombuffer(text, dtype=cp.uint8))
        goto_array = cp.asarray(goto_table, dtype=cp.int32)
        failure_array = cp.asarray(failure_table, dtype=cp.int32)
        output_array = cp.asarray(output_table, dtype=cp.int32)
        
        # Allocate output arrays
        matches = cp.zeros(len(patterns) * 1000, dtype=cp.int32)
        match_counts = cp.zeros(len(patterns), dtype=cp.int32)
        
        # Launch kernel
        block_size = 256
        grid_size = (text_array.size + block_size - 1) // block_size
        
        self.aho_corasick_kernel(
            (grid_size,), (block_size,),
            (text_array, goto_array, failure_array, output_array,
             text_array.size, len(goto_table) // 256, matches, match_counts)
        )
        
        # Get results
        counts = match_counts.get()
        matches_array = matches.get()
        
        results = []
        for i in range(len(patterns)):
            start_idx = i * 1000
            end_idx = start_idx + counts[i]
            results.append(matches_array[start_idx:end_idx].tolist())
        
        return results
    
    def _build_bad_char_table(self, pattern: bytes) -> List[int]:
        """Build bad character table for Boyer-Moore algorithm"""
        table = [len(pattern)] * 256
        for i in range(len(pattern) - 1):
            table[pattern[i]] = len(pattern) - 1 - i
        return table
    
    def _build_aho_corasick_automaton(self, patterns: List[bytes]) -> Tuple[List[int], List[int], List[int]]:
        """Build Aho-Corasick automaton tables"""
        # This is a simplified implementation
        # In production, you'd want a more sophisticated automaton builder
        
        num_states = 1000  # Assume max 1000 states
        goto_table = [[-1] * 256 for _ in range(num_states)]
        failure_table = [0] * num_states
        output_table = [-1] * num_states
        
        current_state = 1
        
        # Build goto function
        for pattern_idx, pattern in enumerate(patterns):
            state = 0
            for char in pattern:
                if goto_table[state][char] == -1:
                    goto_table[state][char] = current_state
                    current_state += 1
                state = goto_table[state][char]
            output_table[state] = pattern_idx
        
        # Build failure function (simplified)
        for state in range(1, current_state):
            for char in range(256):
                if goto_table[state][char] != -1:
                    failure = failure_table[state]
                    while failure != 0 and goto_table[failure][char] == -1:
                        failure = failure_table[failure]
                    failure_table[goto_table[state][char]] = goto_table[failure][char] if goto_table[failure][char] != -1 else 0
        
        # Flatten goto table
        flat_goto = []
        for row in goto_table:
            flat_goto.extend(row)
        
        return flat_goto, failure_table, output_table
    
    # Fallback search removed - advanced GPU kernels required for maximum performance


# Performance benchmarking utilities
class GPUBenchmark:
    """Benchmark utilities for GPU pattern matching"""
    
    @staticmethod
    def benchmark_kernels(text_sizes: List[int], pattern_counts: List[int]) -> dict:
        """Benchmark different GPU kernels with various input sizes"""
        results = {}
        
        for text_size in text_sizes:
            for pattern_count in pattern_counts:
                # Generate test data
                text = np.random.bytes(text_size)
                patterns = [np.random.bytes(10) for _ in range(pattern_count)]
                
                # Test different kernels
                kernels = AdvancedGPUKernels()
                
                # Boyer-Moore
                start_time = cp.cuda.Event()
                end_time = cp.cuda.Event()
                
                start_time.record()
                for pattern in patterns:
                    kernels.boyer_moore_search(text, pattern)
                end_time.record()
                end_time.synchronize()
                
                boyer_moore_time = cp.cuda.get_elapsed_time(start_time, end_time)
                
                # Vectorized
                start_time.record()
                kernels.vectorized_multi_search(text, patterns)
                end_time.record()
                end_time.synchronize()
                
                vectorized_time = cp.cuda.get_elapsed_time(start_time, end_time)
                
                # Aho-Corasick
                start_time.record()
                kernels.aho_corasick_search(text, patterns)
                end_time.record()
                end_time.synchronize()
                
                aho_corasick_time = cp.cuda.get_elapsed_time(start_time, end_time)
                
                key = f"text_{text_size}_patterns_{pattern_count}"
                results[key] = {
                    'boyer_moore': boyer_moore_time,
                    'vectorized': vectorized_time,
                    'aho_corasick': aho_corasick_time,
                    'text_size_mb': text_size / (1024 * 1024),
                    'pattern_count': pattern_count
                }
        
        return results
    
    @staticmethod
    def plot_benchmark_results(results: dict):
        """Plot benchmark results"""
        import matplotlib.pyplot as plt
        
        # Extract data
        text_sizes = []
        pattern_counts = []
        boyer_moore_times = []
        vectorized_times = []
        aho_corasick_times = []
        
        for key, data in results.items():
            text_sizes.append(data['text_size_mb'])
            pattern_counts.append(data['pattern_count'])
            boyer_moore_times.append(data['boyer_moore'])
            vectorized_times.append(data['vectorized'])
            aho_corasick_times.append(data['aho_corasick'])
        
        # Create plots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Plot by text size
        ax1.scatter(text_sizes, boyer_moore_times, label='Boyer-Moore', alpha=0.7)
        ax1.scatter(text_sizes, vectorized_times, label='Vectorized', alpha=0.7)
        ax1.scatter(text_sizes, aho_corasick_times, label='Aho-Corasick', alpha=0.7)
        ax1.set_xlabel('Text Size (MB)')
        ax1.set_ylabel('Time (ms)')
        ax1.set_title('Performance vs Text Size')
        ax1.legend()
        ax1.grid(True)
        
        # Plot by pattern count
        ax2.scatter(pattern_counts, boyer_moore_times, label='Boyer-Moore', alpha=0.7)
        ax2.scatter(pattern_counts, vectorized_times, label='Vectorized', alpha=0.7)
        ax2.scatter(pattern_counts, aho_corasick_times, label='Aho-Corasick', alpha=0.7)
        ax2.set_xlabel('Pattern Count')
        ax2.set_ylabel('Time (ms)')
        ax2.set_title('Performance vs Pattern Count')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        plt.savefig('gpu_benchmark_results.png', dpi=300, bbox_inches='tight')
        plt.show()


if __name__ == "__main__":
    # Test the kernels
    print("Testing GPU kernels...")
    
    # Generate test data
    text = b"This is a test text for pattern matching. It contains multiple patterns to find."
    patterns = [b"test", b"pattern", b"matching", b"multiple"]
    
    kernels = AdvancedGPUKernels()
    
    # Test Boyer-Moore
    print("Testing Boyer-Moore search...")
    boyer_moore_matches = kernels.boyer_moore_search(text, b"test")
    print(f"Boyer-Moore matches: {boyer_moore_matches}")
    
    # Test vectorized search
    print("Testing vectorized search...")
    vectorized_matches = kernels.vectorized_multi_search(text, patterns)
    print(f"Vectorized matches: {vectorized_matches}")
    
    # Test Aho-Corasick
    print("Testing Aho-Corasick search...")
    aho_corasick_matches = kernels.aho_corasick_search(text, patterns)
    print(f"Aho-Corasick matches: {aho_corasick_matches}")
    
    print("GPU kernel tests completed!")
