#!/usr/bin/env python3
"""
CPU PCAP Scanner Implementation
This script implements CPU-based PCAP pattern matching using Python
to test the Boyer-Moore-Horspool algorithm approach
"""

import os
import sys
import time
import argparse
import csv
import json
from pathlib import Path
from typing import List, Dict, Tuple, Any
import numpy as np
import pandas as pd
from scapy.all import rdpcap, IP, TCP, UDP
from collections import defaultdict, deque
from dataclasses import dataclass

# Try to import CuPy for GPU acceleration (not used in this implementation)
try:
    import cupy as cp
    GPU_AVAILABLE = True
    print("✓ CuPy available - but using CPU implementation")
except ImportError:
    GPU_AVAILABLE = False
    print("⚠ CuPy not available - using CPU implementation")

@dataclass
class Match:
    packet_id: int
    offset: int
    pattern_id: int

class BoyerMooreHorspool:
    """Boyer-Moore-Horspool string matching algorithm"""
    
    def __init__(self, pattern: str):
        self.pattern = pattern.encode('utf-8') if isinstance(pattern, str) else pattern
        self.pattern_len = len(self.pattern)
        self.bad_char_table = self._build_bad_char_table()
    
    def _build_bad_char_table(self) -> Dict[int, int]:
        """Build the bad character shift table"""
        table = {}
        pattern_len = self.pattern_len
        
        # Initialize with pattern length
        for i in range(256):
            table[i] = pattern_len
            
        # Set shift values for characters in pattern
        for i in range(pattern_len - 1):
            table[self.pattern[i]] = pattern_len - 1 - i
            
        return table
    
    def find_all_matches(self, text: bytes, packet_id: int, pattern_id: int) -> List[Match]:
        """Find all occurrences of pattern in text"""
        matches = []
        text_len = len(text)
        pattern_len = self.pattern_len
        
        if pattern_len == 0 or text_len < pattern_len:
            return matches
            
        i = 0
        while i <= text_len - pattern_len:
            # Check if pattern matches at position i
            j = pattern_len - 1
            while j >= 0 and self.pattern[j] == text[i + j]:
                j -= 1
                
            if j < 0:
                # Match found
                matches.append(Match(packet_id, i, pattern_id))
                i += pattern_len  # Skip by pattern length
            else:
                # Use bad character rule to skip
                bad_char = text[i + pattern_len - 1]
                shift = self.bad_char_table.get(bad_char, pattern_len)
                i += max(1, shift)
                
        return matches

class CPUScannerImplementation:
    """CPU-based PCAP pattern matching implementation"""
    
    def __init__(self):
        self.patterns = []
        self.bmh_matchers = []
        
    def add_pattern(self, pattern: str):
        """Add a pattern to search for"""
        self.patterns.append(pattern)
        self.bmh_matchers.append(BoyerMooreHorspool(pattern))
        
    def scan_packets(self, packets_data: List[bytes]) -> List[Match]:
        """Scan packets for all patterns"""
        all_matches = []
        
        for packet_id, packet_data in enumerate(packets_data):
            for pattern_id, matcher in enumerate(self.bmh_matchers):
                matches = matcher.find_all_matches(packet_data, packet_id, pattern_id)
                all_matches.extend(matches)
                
        return all_matches

class PCAPLoader:
    """Loads PCAP files and extracts packet data"""
    
    @staticmethod
    def load_pcap(pcap_file: str) -> Tuple[List[bytes], List[int], List[int]]:
        """Load PCAP file and return packet data, offsets, and lengths"""
        try:
            packets = rdpcap(pcap_file)
            
            packet_data = []
            offsets = []
            lengths = []
            
            current_offset = 0
            
            for packet in packets:
                # Get raw packet bytes
                raw_bytes = bytes(packet)
                
                packet_data.append(raw_bytes)
                offsets.append(current_offset)
                lengths.append(len(raw_bytes))
                
                current_offset += len(raw_bytes)
                
            return packet_data, offsets, lengths
            
        except Exception as e:
            print(f"Error loading PCAP file {pcap_file}: {e}")
            return [], [], []

class CPUBenchmarkImplementation:
    """Benchmark implementation for CPU scanner approach"""
    
    def __init__(self, results_dir="results"):
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(exist_ok=True)
        
        # Test PCAP files
        self.pcap_files = [
            "PCAP Files/synthetic_50mb.pcapng",
            "PCAP Files/synthetic_100mb.pcapng", 
            "PCAP Files/synthetic_200mb.pcapng",
            "PCAP Files/synthetic_500mb.pcapng"
        ]
        
        # Pattern files
        self.pattern_files = {
            1: "test_patterns_1.txt",
            7: "test_patterns_7.txt", 
            14: "test_patterns_14.txt"
        }
        
        self.results = []
        
    def load_patterns(self, pattern_file: str) -> List[str]:
        """Load patterns from file"""
        patterns = []
        try:
            with open(pattern_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        patterns.append(line)
        except FileNotFoundError:
            print(f"ERROR: Pattern file '{pattern_file}' not found!")
            return []
        return patterns
        
    def get_pcap_info(self, pcap_file: str) -> Dict[str, Any]:
        """Get basic info about PCAP file"""
        try:
            size_bytes = os.path.getsize(pcap_file)
            size_mb = size_bytes / (1024 * 1024)
            return {
                'file': pcap_file,
                'size_bytes': size_bytes,
                'size_mb': round(size_mb, 2)
            }
        except FileNotFoundError:
            return None
            
    def run_scanner_simulation(self, pcap_file: str, patterns: List[str]) -> Dict[str, Any]:
        """Run scanner simulation with given patterns"""
        if not patterns:
            return None
            
        print(f"Running CPU scanner on {pcap_file} with {len(patterns)} patterns...")
        
        # Load PCAP data
        packet_data, offsets, lengths = PCAPLoader.load_pcap(pcap_file)
        if not packet_data:
            return {
                'success': False,
                'execution_time': 0,
                'match_count': 0,
                'error': 'Failed to load PCAP file'
            }
            
        # Initialize scanner
        scanner = CPUScannerImplementation()
        for pattern in patterns:
            scanner.add_pattern(pattern)
            
        # Run simulation
        start_time = time.time()
        matches = scanner.scan_packets(packet_data)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        return {
            'success': True,
            'execution_time': execution_time,
            'match_count': len(matches),
            'matches': matches,
            'packet_count': len(packet_data),
            'total_bytes': sum(lengths)
        }
        
    def run_benchmark(self):
        """Run complete benchmark suite"""
        print("CPU PCAP Scanner Implementation Benchmark")
        print("=" * 50)
        
        total_tests = len(self.pcap_files) * len(self.pattern_files)
        current_test = 0
        
        for pcap_file in self.pcap_files:
            pcap_info = self.get_pcap_info(pcap_file)
            if not pcap_info:
                print(f"WARNING: Skipping {pcap_file} - file not found")
                continue
                
            print(f"\nTesting PCAP: {pcap_file} ({pcap_info['size_mb']} MB)")
            
            for pattern_count, pattern_file in self.pattern_files.items():
                current_test += 1
                print(f"\n[{current_test}/{total_tests}] Testing {pattern_count} patterns...")
                
                # Load patterns
                patterns = self.load_patterns(pattern_file)
                if not patterns:
                    continue
                    
                # Run scanner simulation
                result = self.run_scanner_simulation(pcap_file, patterns)
                if not result:
                    continue
                    
                # Store results
                test_result = {
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'pcap_file': pcap_file,
                    'pcap_size_mb': pcap_info['size_mb'],
                    'pattern_count': pattern_count,
                    'pattern_file': pattern_file,
                    'patterns': patterns,
                    'success': result['success'],
                    'execution_time': result['execution_time'],
                    'match_count': result['match_count'],
                    'packet_count': result.get('packet_count', 0),
                    'total_bytes': result.get('total_bytes', 0),
                    'throughput_mbps': pcap_info['size_mb'] / result['execution_time'] if result['execution_time'] > 0 else 0,
                    'matches_per_second': result['match_count'] / result['execution_time'] if result['execution_time'] > 0 else 0,
                    'error': result.get('error', '')
                }
                
                self.results.append(test_result)
                
                # Print summary
                if result['success']:
                    print(f"  ✓ Success: {result['execution_time']:.2f}s, {result['match_count']} matches")
                    print(f"  ✓ Throughput: {test_result['throughput_mbps']:.2f} MB/s")
                    print(f"  ✓ Packets: {result.get('packet_count', 0):,}")
                else:
                    print(f"  ✗ Failed: {result.get('error', 'Unknown error')}")
                    
        return True
        
    def save_results(self):
        """Save benchmark results to files"""
        if not self.results:
            print("No results to save")
            return
            
        # Save CSV
        csv_file = self.results_dir / "cpu_scanner_results.csv"
        with open(csv_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'timestamp', 'pcap_file', 'pcap_size_mb', 'pattern_count', 
                'pattern_file', 'success', 'execution_time', 'match_count',
                'packet_count', 'total_bytes', 'throughput_mbps', 'matches_per_second', 'error'
            ])
            writer.writeheader()
            for result in self.results:
                writer.writerow({k: v for k, v in result.items() if k in writer.fieldnames})
                
        # Save JSON
        json_file = self.results_dir / "cpu_scanner_results.json"
        with open(json_file, 'w') as f:
            json.dump(self.results, f, indent=2)
            
        print(f"\nResults saved to:")
        print(f"  CSV: {csv_file}")
        print(f"  JSON: {json_file}")
        
    def print_summary(self):
        """Print benchmark summary"""
        if not self.results:
            print("No results to summarize")
            return
            
        print("\n" + "=" * 60)
        print("CPU SCANNER IMPLEMENTATION SUMMARY")
        print("=" * 60)
        
        # Group by pattern count
        by_patterns = {}
        for result in self.results:
            if result['success']:
                pattern_count = result['pattern_count']
                if pattern_count not in by_patterns:
                    by_patterns[pattern_count] = []
                by_patterns[pattern_count].append(result)
                
        for pattern_count in sorted(by_patterns.keys()):
            results = by_patterns[pattern_count]
            print(f"\n{pattern_count} Pattern(s):")
            print(f"  Tests: {len(results)}")
            
            if results:
                avg_time = sum(r['execution_time'] for r in results) / len(results)
                avg_throughput = sum(r['throughput_mbps'] for r in results) / len(results)
                total_matches = sum(r['match_count'] for r in results)
                total_packets = sum(r['packet_count'] for r in results)
                
                print(f"  Avg Time: {avg_time:.2f}s")
                print(f"  Avg Throughput: {avg_throughput:.2f} MB/s")
                print(f"  Total Matches: {total_matches}")
                print(f"  Total Packets: {total_packets:,}")
                
                # Show per-file results
                for result in results:
                    print(f"    {os.path.basename(result['pcap_file'])}: "
                          f"{result['execution_time']:.2f}s, "
                          f"{result['throughput_mbps']:.2f} MB/s, "
                          f"{result['match_count']} matches, "
                          f"{result['packet_count']:,} packets")

def main():
    parser = argparse.ArgumentParser(description='CPU PCAP Scanner Implementation Benchmark')
    parser.add_argument('--results-dir', default='results',
                       help='Directory to save results')
    
    args = parser.parse_args()
    
    benchmark = CPUBenchmarkImplementation(args.results_dir)
    
    print("Starting CPU PCAP Scanner Implementation...")
    print(f"GPU Available: {GPU_AVAILABLE} (not used)")
    print(f"Results: {args.results_dir}")
    
    success = benchmark.run_benchmark()
    
    if success:
        benchmark.save_results()
        benchmark.print_summary()
        print("\nSimulation completed successfully!")
        print("\nNote: This is a CPU implementation of the Boyer-Moore-Horspool algorithm.")
        print("The implementation processes patterns sequentially on CPU.")
    else:
        print("\nSimulation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
