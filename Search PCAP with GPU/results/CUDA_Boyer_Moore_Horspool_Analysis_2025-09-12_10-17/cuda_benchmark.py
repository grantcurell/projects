#!/usr/bin/env python3
"""
CUDA PCAP Scanner Benchmark Script
Tests the CUDA-based Boyer-Moore-Horspool scanner against different pattern counts
"""

import subprocess
import time
import os
import sys
import csv
import json
from pathlib import Path
import argparse

class CUDABenchmark:
    def __init__(self, scanner_path="gpupcapgrep.exe", results_dir="results"):
        self.scanner_path = scanner_path
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
        
        # Results storage
        self.results = []
        
    def check_scanner_exists(self):
        """Check if the CUDA scanner executable exists"""
        if not os.path.exists(self.scanner_path):
            print(f"ERROR: Scanner executable '{self.scanner_path}' not found!")
            print("Please run build.bat first to compile the CUDA scanner.")
            return False
        return True
        
    def load_patterns(self, pattern_file):
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
        
    def get_pcap_info(self, pcap_file):
        """Get basic info about PCAP file"""
        try:
            # Use a simple approach to get file size
            size_bytes = os.path.getsize(pcap_file)
            size_mb = size_bytes / (1024 * 1024)
            return {
                'file': pcap_file,
                'size_bytes': size_bytes,
                'size_mb': round(size_mb, 2)
            }
        except FileNotFoundError:
            return None
            
    def run_scanner(self, pcap_file, patterns, timeout=300):
        """Run the CUDA scanner with given patterns"""
        if not patterns:
            return None
            
        # Build command
        cmd = [self.scanner_path, pcap_file]
        for pattern in patterns:
            cmd.extend(["-s", pattern])
            
        print(f"Running: {' '.join(cmd[:3])}... (with {len(patterns)} patterns)")
        
        try:
            start_time = time.time()
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            end_time = time.time()
            
            execution_time = end_time - start_time
            
            # Count matches from output
            match_count = len([line for line in result.stdout.split('\n') if line.strip()])
            
            return {
                'success': result.returncode == 0,
                'execution_time': execution_time,
                'match_count': match_count,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            print(f"TIMEOUT: Scanner took longer than {timeout} seconds")
            return {
                'success': False,
                'execution_time': timeout,
                'match_count': 0,
                'stdout': '',
                'stderr': f'Timeout after {timeout} seconds',
                'returncode': -1
            }
        except Exception as e:
            print(f"ERROR running scanner: {e}")
            return {
                'success': False,
                'execution_time': 0,
                'match_count': 0,
                'stdout': '',
                'stderr': str(e),
                'returncode': -1
            }
            
    def run_benchmark(self):
        """Run complete benchmark suite"""
        print("CUDA PCAP Scanner Benchmark")
        print("=" * 50)
        
        if not self.check_scanner_exists():
            return False
            
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
                    
                # Run scanner
                result = self.run_scanner(pcap_file, patterns)
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
                    'throughput_mbps': pcap_info['size_mb'] / result['execution_time'] if result['execution_time'] > 0 else 0,
                    'matches_per_second': result['match_count'] / result['execution_time'] if result['execution_time'] > 0 else 0,
                    'returncode': result['returncode'],
                    'stderr': result['stderr']
                }
                
                self.results.append(test_result)
                
                # Print summary
                if result['success']:
                    print(f"  ✓ Success: {result['execution_time']:.2f}s, {result['match_count']} matches")
                    print(f"  ✓ Throughput: {test_result['throughput_mbps']:.2f} MB/s")
                else:
                    print(f"  ✗ Failed: {result['stderr']}")
                    
        return True
        
    def save_results(self):
        """Save benchmark results to files"""
        if not self.results:
            print("No results to save")
            return
            
        # Save CSV
        csv_file = self.results_dir / "cuda_scanner_benchmark.csv"
        with open(csv_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'timestamp', 'pcap_file', 'pcap_size_mb', 'pattern_count', 
                'pattern_file', 'success', 'execution_time', 'match_count',
                'throughput_mbps', 'matches_per_second', 'returncode'
            ])
            writer.writeheader()
            for result in self.results:
                writer.writerow({k: v for k, v in result.items() if k in writer.fieldnames})
                
        # Save JSON
        json_file = self.results_dir / "cuda_scanner_benchmark.json"
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
        print("CUDA SCANNER BENCHMARK SUMMARY")
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
                
                print(f"  Avg Time: {avg_time:.2f}s")
                print(f"  Avg Throughput: {avg_throughput:.2f} MB/s")
                print(f"  Total Matches: {total_matches}")
                
                # Show per-file results
                for result in results:
                    print(f"    {os.path.basename(result['pcap_file'])}: "
                          f"{result['execution_time']:.2f}s, "
                          f"{result['throughput_mbps']:.2f} MB/s, "
                          f"{result['match_count']} matches")

def main():
    parser = argparse.ArgumentParser(description='CUDA PCAP Scanner Benchmark')
    parser.add_argument('--scanner', default='gpupcapgrep.exe', 
                       help='Path to CUDA scanner executable')
    parser.add_argument('--results-dir', default='results',
                       help='Directory to save results')
    parser.add_argument('--timeout', type=int, default=300,
                       help='Timeout for each test in seconds')
    
    args = parser.parse_args()
    
    benchmark = CUDABenchmark(args.scanner, args.results_dir)
    
    print("Starting CUDA PCAP Scanner Benchmark...")
    print(f"Scanner: {args.scanner}")
    print(f"Results: {args.results_dir}")
    print(f"Timeout: {args.timeout}s")
    
    success = benchmark.run_benchmark()
    
    if success:
        benchmark.save_results()
        benchmark.print_summary()
        print("\nBenchmark completed successfully!")
    else:
        print("\nBenchmark failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
