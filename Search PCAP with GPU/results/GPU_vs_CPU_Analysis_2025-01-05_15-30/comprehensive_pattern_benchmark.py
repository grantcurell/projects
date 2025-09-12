#!/usr/bin/env python3
"""
Comprehensive PCAP Pattern Matching Benchmark

This benchmark tests CPU vs GPU performance across multiple scenarios:
- Different PCAP file sizes (50MB, 100MB, 200MB, 500MB, 1000MB)
- Different packet characteristics (small vs large packets)
- Different pattern counts (1, 7, 14 patterns)
- Multiple algorithms (Boyer-Moore-Horspool, Aho-Corasick, etc.)

Results are stored in CSV format for analysis and report generation.
"""

import os
import sys
import time
import threading
import logging
import csv
import json
import argparse
import signal
import ctypes
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass, asdict
from colorama import init, Fore, Style
import pandas as pd

# Initialize colorama
init(autoreset=True)

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our modules
from pcap_gpu_scanner import PCAPScanner, TCPReassembler, FlowKey
from scapy.all import rdpcap, IP, TCP, UDP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('comprehensive_benchmark.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Global timeout flag
timeout_reached = False

def run_gpu_with_timeout(gpu_scanner, payloads, flow_ids, timeout_seconds=180):
    """Run GPU processing with a timeout using threading"""
    global timeout_reached
    
    result_container = {'matches': [], 'error': None, 'completed': False}
    
    def gpu_worker():
        try:
            matches = gpu_scanner.gpu_scanner.scan_payloads(payloads, flow_ids)
            result_container['matches'] = matches
            result_container['completed'] = True
        except Exception as e:
            result_container['error'] = str(e)
            result_container['completed'] = True
    
    # Start GPU processing in a thread
    gpu_thread = threading.Thread(target=gpu_worker, daemon=True)
    start_time = time.time()
    gpu_thread.start()
    
    # Wait for completion or timeout
    gpu_thread.join(timeout=timeout_seconds)
    
    gpu_time = time.time() - start_time
    
    if gpu_thread.is_alive():
        # Thread is still running - timeout occurred
        timeout_reached = True
        print(f"{Fore.RED}⏰ GPU processing timed out after {timeout_seconds}s{Style.RESET_ALL}")
        return [], gpu_time, "Timeout"
    
    # Thread completed
    if result_container['error']:
        return [], gpu_time, f"Error: {result_container['error']}"
    else:
        return result_container['matches'], gpu_time, "Success"

@dataclass
class ComprehensiveBenchmarkResult:
    """Results from comprehensive benchmark test"""
    test_id: str
    pcap_file: str
    pcap_size_mb: float
    packet_type: str  # "small" or "large"
    packet_count: int
    avg_packet_size: int
    total_payload_bytes: int
    pattern_count: int
    patterns: str  # JSON string of patterns used
    
    # Timing (excluding I/O)
    cpu_pattern_time: float
    gpu_pattern_time: float
    
    # Results
    cpu_matches: int
    gpu_matches: int
    
    # Performance metrics
    cpu_throughput_mbps: float
    gpu_throughput_mbps: float
    speedup: float
    
    # Validation
    validation_passed: bool
    timeout_reached: bool
    
    # Algorithm information
    cpu_algorithm: str
    gpu_algorithm: str
    gpu_batch_count: int
    gpu_kernel_launches: int

class ComprehensivePatternBenchmark:
    """Comprehensive benchmark for CPU vs GPU pattern matching"""
    
    def __init__(self, specific_file: Optional[str] = None):
        self.results: List[ComprehensiveBenchmarkResult] = []
        
        # Define test scenarios
        self.test_scenarios = self._define_test_scenarios(specific_file)
        
        print(f"{Fore.CYAN}{Style.BRIGHT}🔬 Comprehensive PCAP Pattern Matching Benchmark{Style.RESET_ALL}")
        print("=" * 80)
        print(f"{Fore.YELLOW}📋 Test Scenarios: {len(self.test_scenarios)}{Style.RESET_ALL}")
        print()
    
    def _define_test_scenarios(self, specific_file: Optional[str] = None) -> List[Dict[str, Any]]:
        """Define all test scenarios"""
        scenarios = []
        
        # PCAP files to test
        if specific_file:
            # If specific file provided, only test that file
            pcap_files = [(specific_file, "mixed")]
        else:
            pcap_files = [
                ("PCAP Files/synthetic_50mb.pcapng", "small"),
                ("PCAP Files/synthetic_large_50mb.pcapng", "large"),
                ("PCAP Files/synthetic_100mb.pcapng", "small"),
                ("PCAP Files/synthetic_large_100mb.pcapng", "large"),
                ("PCAP Files/synthetic_200mb.pcapng", "small"),
                ("PCAP Files/synthetic_large_200mb.pcapng", "large"),
                ("PCAP Files/synthetic_500mb.pcapng", "small"),
                ("PCAP Files/synthetic_large_500mb.pcapng", "large"),
                ("PCAP Files/synthetic_1000mb.pcapng", "small"),
                ("PCAP Files/synthetic_large_packets.pcapng", "large"),
            ]
        
        # Pattern sets
        pattern_sets = {
            1: ["HTTP"],
            7: ["HTTP", "GET", "POST", "Content-Type", "User-Agent", "Accept", "Host"],
            14: ["HTTP", "GET", "POST", "Content-Type", "User-Agent", "Accept", "Host", "Cookie", "Server", "Date", "Cache-Control", "Connection", "Keep-Alive", "Transfer-Encoding"]
        }
        
        # Generate all combinations
        test_id = 1
        for pcap_file, packet_type in pcap_files:
            if not Path(pcap_file).exists():
                print(f"{Fore.YELLOW}⚠️  Skipping {pcap_file} (not found){Style.RESET_ALL}")
                continue
                
            for pattern_count, patterns in pattern_sets.items():
                scenarios.append({
                    'test_id': f"test_{test_id:03d}",
                    'pcap_file': pcap_file,
                    'packet_type': packet_type,
                    'pattern_count': pattern_count,
                    'patterns': patterns
                })
                test_id += 1
        
        return scenarios
    
    def _extract_payloads_unified(self, pcap_file: str) -> Tuple[List[bytes], List[str], int, int, int]:
        """Extract payloads using unified TCP reassembly (same for both CPU and GPU)"""
        print(f"{Fore.BLUE}📖 Reading PCAP file: {Path(pcap_file).name}{Style.RESET_ALL}")
        start_time = time.time()
        
        try:
            packets = rdpcap(pcap_file)
            read_time = time.time() - start_time
            
            print(f"{Fore.BLUE}🔧 Performing TCP reassembly...{Style.RESET_ALL}")
            reassembly_start = time.time()
            
            # Use unified TCP reassembly logic
            reassembler = TCPReassembler()
            payloads = []
            flow_ids = []
            total_bytes = 0
            packet_count = 0
            
            for packet in packets:
                if packet.haslayer(IP) and packet.haslayer(TCP):
                    packet_count += 1
                    
                    # Add packet to reassembler
                    result = reassembler.add_packet(packet)
                    if result:
                        flow_key, reassembled_payload, timestamp = result
                        payloads.append(reassembled_payload)
                        flow_ids.append(f"{flow_key.src_ip}:{flow_key.src_port}-{flow_key.dst_ip}:{flow_key.dst_port}")
                        total_bytes += len(reassembled_payload)
            
            reassembly_time = time.time() - reassembly_start
            
            # Calculate average packet size
            avg_packet_size = total_bytes // len(payloads) if payloads else 0
            
            print(f"✓ Extracted {len(payloads):,} payloads ({total_bytes:,} bytes)")
            print(f"✓ Packet count: {packet_count:,}, Avg packet size: {avg_packet_size:,} bytes")
            print(f"✓ Read time: {read_time:.3f}s, Reassembly time: {reassembly_time:.3f}s")
            
            return payloads, flow_ids, total_bytes, len(payloads), avg_packet_size
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error reading PCAP: {e}{Style.RESET_ALL}")
            return [], [], 0, 0, 0
    
    def _run_cpu_benchmark(self, payloads: List[bytes], patterns: List[str]) -> Tuple[int, float, str]:
        """Run CPU-only pattern matching benchmark"""
        print(f"{Fore.GREEN}🖥️  Running CPU benchmark...{Style.RESET_ALL}")
        
        start_time = time.time()
        pattern_bytes = [p.encode() if isinstance(p, str) else p for p in patterns]
        
        # Choose optimal algorithm based on pattern count
        if len(patterns) == 1:
            # Single pattern: Use Boyer-Moore-Horspool
            matches = 0
            pattern = pattern_bytes[0]
            bad_char_table = self._build_bad_char_table(pattern)
            
            for payload in payloads:
                if self._boyer_moore_horspool_search(payload, pattern, bad_char_table):
                    matches += 1
            
            algorithm = "Boyer-Moore-Horspool"
        else:
            # Multiple patterns: Use Aho-Corasick
            matches = 0
            aho_corasick = self._build_aho_corasick_automaton(pattern_bytes)
            
            for payload in payloads:
                payload_matches = self._aho_corasick_search(payload, aho_corasick)
                matches += len(payload_matches)
            
            algorithm = "Aho-Corasick"
        
        cpu_time = time.time() - start_time
        print(f"✓ CPU: {cpu_time:.3f}s, {matches:,} matches ({algorithm})")
        
        return matches, cpu_time, algorithm
    
    def _build_bad_char_table(self, pattern: bytes) -> Dict[int, int]:
        """Build Boyer-Moore bad character table"""
        table = {}
        pattern_len = len(pattern)
        
        for i in range(pattern_len - 1):
            table[pattern[i]] = pattern_len - 1 - i
        
        return table
    
    def _boyer_moore_horspool_search(self, text: bytes, pattern: bytes, bad_char_table: Dict[int, int]) -> bool:
        """Boyer-Moore-Horspool string search"""
        text_len = len(text)
        pattern_len = len(pattern)
        
        if pattern_len == 0:
            return True
        if pattern_len > text_len:
            return False
        
        i = 0
        while i <= text_len - pattern_len:
            j = pattern_len - 1
            
            # Check from right to left
            while j >= 0 and text[i + j] == pattern[j]:
                j -= 1
            
            if j < 0:
                return True  # Found match
            
            # Shift using bad character rule
            char = text[i + pattern_len - 1]
            shift = bad_char_table.get(char, pattern_len)
            i += shift
        
        return False
    
    def _build_aho_corasick_automaton(self, patterns: List[bytes]) -> Tuple[Dict[int, Dict[int, int]], Dict[int, List[int]], Dict[int, int]]:
        """Build Aho-Corasick automaton"""
        # Build trie
        trie = {0: {}}  # state -> {char -> next_state}
        output = {0: []}  # state -> [pattern_indices]
        state_count = 1
        
        # Add patterns to trie
        for pattern_idx, pattern in enumerate(patterns):
            current_state = 0
            for char in pattern:
                if char not in trie[current_state]:
                    trie[current_state][char] = state_count
                    trie[state_count] = {}
                    output[state_count] = []
                    state_count += 1
                current_state = trie[current_state][char]
            output[current_state].append(pattern_idx)
        
        # Build failure links using BFS
        failure = {0: 0}  # state -> failure_state
        queue = []
        
        # Initialize queue with children of root
        for char, next_state in trie[0].items():
            failure[next_state] = 0
            queue.append(next_state)
        
        # Process queue
        while queue:
            current_state = queue.pop(0)
            for char, next_state in trie[current_state].items():
                queue.append(next_state)
                
                # Find failure state
                fail_state = failure[current_state]
                while fail_state != 0 and char not in trie[fail_state]:
                    fail_state = failure[fail_state]
                
                failure[next_state] = trie[fail_state].get(char, 0) if fail_state != 0 else 0
                
                # Merge outputs
                output[next_state].extend(output[failure[next_state]])
        
        return trie, output, failure
    
    def _aho_corasick_search(self, text: bytes, automaton: Tuple[Dict[int, Dict[int, int]], Dict[int, List[int]], Dict[int, int]]) -> List[int]:
        """Search using Aho-Corasick automaton"""
        trie, output, failure = automaton
        matches = []
        current_state = 0
        
        for i, char in enumerate(text):
            # Follow failure links until we find a valid transition
            while current_state != 0 and char not in trie[current_state]:
                current_state = failure[current_state]
            
            # Move to next state
            if char in trie[current_state]:
                current_state = trie[current_state][char]
            else:
                current_state = 0
            
            # Collect matches
            for pattern_idx in output[current_state]:
                matches.append(i)
        
        return matches
    
    def _run_gpu_benchmark(self, payloads: List[bytes], flow_ids: List[str], patterns: List[str]) -> Tuple[int, float, str, int, int]:
        """Run GPU-accelerated pattern matching benchmark"""
        print(f"{Fore.MAGENTA}🚀 Running GPU benchmark...{Style.RESET_ALL}")
        
        try:
            # Create GPU scanner
            gpu_scanner = PCAPScanner(patterns, use_regex=False)
            
            # Run GPU processing with timeout using multiprocessing
            gpu_matches, gpu_time, status = run_gpu_with_timeout(gpu_scanner, payloads, flow_ids, timeout_seconds=180)
            
            # Determine algorithm used based on pattern count
            if len(patterns) == 1:
                algorithm = "Boyer-Moore-Horspool"
            elif len(patterns) <= 10:
                algorithm = "Vectorized Multi-Pattern"
            else:
                algorithm = "Aho-Corasick (PFAC)"
            
            # Calculate batch information based on actual GPU scanner logic
            if len(payloads) < 1000:
                batch_size = 100
            elif len(payloads) < 10000:
                batch_size = 1000
            elif len(payloads) < 100000:
                batch_size = 5000
            else:
                batch_size = 10000
                
            batch_count = (len(payloads) + batch_size - 1) // batch_size
            kernel_launches = batch_count
            
            if status == "Timeout":
                print(f"{Fore.RED}⏰ GPU: TIMEOUT after {gpu_time:.3f}s{Style.RESET_ALL}")
                return 0, gpu_time, f"{algorithm} (Timeout)", batch_count, kernel_launches
            elif status.startswith("Error"):
                print(f"{Fore.RED}❌ GPU Error: {status}{Style.RESET_ALL}")
                return 0, gpu_time, f"{algorithm} (Error)", batch_count, kernel_launches
            else:
                print(f"✓ GPU: {gpu_time:.3f}s, {len(gpu_matches):,} matches ({algorithm})")
                print(f"✓ GPU batches: {batch_count:,}, kernel launches: {kernel_launches:,}")
                
                return len(gpu_matches), gpu_time, algorithm, batch_count, kernel_launches
                
        except Exception as e:
            print(f"{Fore.RED}❌ GPU Error: {e}{Style.RESET_ALL}")
            return 0, 0.0, "Error", 0, 0
    
    def run_single_test(self, scenario: Dict[str, Any]) -> Optional[ComprehensiveBenchmarkResult]:
        """Run a single test scenario"""
        try:
            print(f"\n{Fore.CYAN}🧪 Test: {scenario['test_id']}{Style.RESET_ALL}")
            print(f"   File: {Path(scenario['pcap_file']).name}")
            print(f"   Type: {scenario['packet_type']} packets")
            print(f"   Patterns: {scenario['pattern_count']} ({', '.join(scenario['patterns'])})")
            
            # Extract payloads once
            payloads, flow_ids, total_bytes, payload_count, avg_packet_size = self._extract_payloads_unified(scenario['pcap_file'])
            
            if not payloads:
                print(f"{Fore.RED}❌ No payloads extracted{Style.RESET_ALL}")
                return None
            
            file_size_mb = Path(scenario['pcap_file']).stat().st_size / 1024 / 1024
            
            # Run CPU benchmark
            cpu_matches, cpu_time, cpu_algorithm = self._run_cpu_benchmark(payloads, scenario['patterns'])
            
            # Run GPU benchmark
            gpu_matches, gpu_time, gpu_algorithm, batch_count, kernel_launches = self._run_gpu_benchmark(
                payloads, flow_ids, scenario['patterns']
            )
            
            # Calculate metrics
            cpu_throughput_mbps = (total_bytes / 1024 / 1024) / cpu_time if cpu_time > 0 else 0
            gpu_throughput_mbps = (total_bytes / 1024 / 1024) / gpu_time if gpu_time > 0 else 0
            speedup = cpu_time / gpu_time if gpu_time > 0 else 0
            validation_passed = cpu_matches == gpu_matches
            
            # Store results
            # Determine if timeout was reached
            timeout_reached = "Timeout" in gpu_algorithm
            
            result = ComprehensiveBenchmarkResult(
                test_id=scenario['test_id'],
                pcap_file=Path(scenario['pcap_file']).name,
                pcap_size_mb=file_size_mb,
                packet_type=scenario['packet_type'],
                packet_count=payload_count,
                avg_packet_size=avg_packet_size,
                total_payload_bytes=total_bytes,
                pattern_count=scenario['pattern_count'],
                patterns=json.dumps(scenario['patterns']),
                cpu_pattern_time=cpu_time,
                gpu_pattern_time=gpu_time,
                cpu_matches=cpu_matches,
                gpu_matches=gpu_matches,
                cpu_throughput_mbps=cpu_throughput_mbps,
                gpu_throughput_mbps=gpu_throughput_mbps,
                speedup=speedup,
                validation_passed=validation_passed,
                timeout_reached=timeout_reached,
                cpu_algorithm=cpu_algorithm,
                gpu_algorithm=gpu_algorithm,
                gpu_batch_count=batch_count,
                gpu_kernel_launches=kernel_launches
            )
            
            self.results.append(result)
            
            # Print summary
            self._print_test_summary(result)
            
            return result
            
        except Exception as e:
            print(f"{Fore.RED}❌ Test failed: {e}{Style.RESET_ALL}")
            return None
        finally:
            # Timeout handled by daemon thread
            pass
    
    def _print_test_summary(self, result: ComprehensiveBenchmarkResult):
        """Print test summary"""
        print(f"\n{Fore.CYAN}📊 Test Summary{Style.RESET_ALL}")
        print("-" * 40)
        
        print(f"CPU: {result.cpu_pattern_time:.3f}s ({result.cpu_throughput_mbps:.1f} MB/s)")
        print(f"GPU: {result.gpu_pattern_time:.3f}s ({result.gpu_throughput_mbps:.1f} MB/s)")
        print(f"Speedup: {result.speedup:.2f}x")
        print(f"Validation: {'✅ PASSED' if result.validation_passed else '❌ FAILED'}")
        
        if result.timeout_reached:
            print(f"Status: {Fore.RED}⏰ TIMEOUT REACHED{Style.RESET_ALL}")
    
    def run_all_tests(self, resume_from: Optional[str] = None) -> bool:
        """Run all test scenarios, optionally resuming from a specific test"""
        if resume_from:
            print(f"{Fore.YELLOW}🔄 Resuming benchmark from {resume_from}...{Style.RESET_ALL}")
            # Load existing results when resuming
            self._load_existing_results("comprehensive_benchmark_progress.csv")
        else:
            print(f"{Fore.YELLOW}🚀 Starting comprehensive benchmark...{Style.RESET_ALL}")
        
        print(f"Total tests: {len(self.test_scenarios)}")
        print()
        
        # Find the starting index if resuming
        start_index = 0
        if resume_from:
            for i, scenario in enumerate(self.test_scenarios):
                if scenario['test_id'] == resume_from:
                    start_index = i
                    print(f"{Fore.GREEN}✓ Found resume point: {resume_from} (test {i+1}/{len(self.test_scenarios)}){Style.RESET_ALL}")
                    break
            else:
                print(f"{Fore.RED}❌ Resume test '{resume_from}' not found!{Style.RESET_ALL}")
                return False
        
        successful_tests = 0
        failed_tests = 0
        
        for i, scenario in enumerate(self.test_scenarios[start_index:], start_index + 1):
            print(f"\n{Fore.YELLOW}Progress: {i}/{len(self.test_scenarios)} tests{Style.RESET_ALL}")
            
            result = self.run_single_test(scenario)
            
            if result:
                successful_tests += 1
            else:
                failed_tests += 1
            
            # Save intermediate results
            self.save_results_to_csv(f"comprehensive_benchmark_progress.csv")
        
        print(f"\n{Fore.CYAN}📊 BENCHMARK COMPLETE{Style.RESET_ALL}")
        print("=" * 50)
        print(f"Successful tests: {successful_tests}")
        print(f"Failed tests: {failed_tests}")
        print(f"Total tests: {len(self.test_scenarios)}")
        
        return successful_tests > 0
    
    def list_tests(self):
        """List all available tests"""
        print(f"{Fore.CYAN}📋 Available Tests:{Style.RESET_ALL}")
        print("=" * 50)
        
        for i, scenario in enumerate(self.test_scenarios, 1):
            test_id = f"test_{i:03d}"
            print(f"{test_id}: {scenario['pcap_file']} ({scenario['packet_type']}) - {len(scenario['patterns'])} patterns")
        
        print(f"\nTotal: {len(self.test_scenarios)} tests")
    
    def run_specific_test(self, test_id: str):
        """Run a specific test by ID"""
        # Parse test ID (e.g., "test_001" -> 1)
        try:
            test_num = int(test_id.split('_')[1])
            if test_num < 1 or test_num > len(self.test_scenarios):
                print(f"{Fore.RED}❌ Invalid test ID: {test_id}{Style.RESET_ALL}")
                print(f"Valid range: test_001 to test_{len(self.test_scenarios):03d}")
                return
            
            scenario = self.test_scenarios[test_num - 1]
            print(f"{Fore.YELLOW}🎯 Running {test_id}: {scenario['pcap_file']}{Style.RESET_ALL}")
            
            result = self.run_single_test(scenario)
            if result:
                print(f"{Fore.GREEN}✅ Test completed successfully{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Test failed{Style.RESET_ALL}")
                
        except (ValueError, IndexError):
            print(f"{Fore.RED}❌ Invalid test ID format: {test_id}{Style.RESET_ALL}")
            print("Expected format: test_001, test_002, etc.")
    
    def run_quick_test(self):
        """Run first 3 tests for quick validation"""
        print(f"{Fore.YELLOW}⚡ Running quick validation (first 3 tests){Style.RESET_ALL}")
        
        successful_tests = 0
        for i in range(min(3, len(self.test_scenarios))):
            scenario = self.test_scenarios[i]
            test_id = f"test_{i+1:03d}"
            print(f"\n{Fore.YELLOW}🎯 Running {test_id}: {scenario['pcap_file']}{Style.RESET_ALL}")
            
            result = self.run_single_test(scenario)
            if result:
                successful_tests += 1
                print(f"{Fore.GREEN}✅ {test_id} completed successfully{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ {test_id} failed{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}📊 Quick Test Results:{Style.RESET_ALL}")
        print(f"Successful: {successful_tests}/3")
        print(f"Failed: {3 - successful_tests}/3")
    
    def _load_existing_results(self, filename: str):
        """Load existing results from CSV file when resuming"""
        if not os.path.exists(filename):
            print(f"{Fore.YELLOW}⚠️  No existing results file found: {filename}{Style.RESET_ALL}")
            return
        
        try:
            df = pd.read_csv(filename)
            print(f"{Fore.GREEN}✓ Loaded {len(df)} existing results from {filename}{Style.RESET_ALL}")
            
            # Convert DataFrame back to ComprehensiveBenchmarkResult objects
            for _, row in df.iterrows():
                # Convert string representations back to proper types
                patterns = eval(row['patterns']) if isinstance(row['patterns'], str) else row['patterns']
                
                result = ComprehensiveBenchmarkResult(
                    test_id=row['test_id'],
                    pcap_file=row['pcap_file'],
                    pcap_size_mb=float(row['pcap_size_mb']),
                    packet_type=row['packet_type'],
                    packet_count=int(row['packet_count']),
                    avg_packet_size=float(row['avg_packet_size']),
                    total_payload_bytes=int(row['total_payload_bytes']),
                    pattern_count=int(row['pattern_count']),
                    patterns=patterns,
                    cpu_pattern_time=float(row['cpu_pattern_time']),
                    gpu_pattern_time=float(row['gpu_pattern_time']),
                    cpu_matches=int(row['cpu_matches']),
                    gpu_matches=int(row['gpu_matches']),
                    cpu_throughput_mbps=float(row['cpu_throughput_mbps']),
                    gpu_throughput_mbps=float(row['gpu_throughput_mbps']),
                    speedup=float(row['speedup']),
                    validation_passed=bool(row['validation_passed']),
                    timeout_reached=bool(row['timeout_reached']),
                    cpu_algorithm=row['cpu_algorithm'],
                    gpu_algorithm=row['gpu_algorithm'],
                    gpu_batch_count=int(row['gpu_batch_count']),
                    gpu_kernel_launches=int(row['gpu_kernel_launches'])
                )
                self.results.append(result)
                
        except Exception as e:
            print(f"{Fore.RED}❌ Error loading existing results: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}⚠️  Starting fresh benchmark{Style.RESET_ALL}")

    def save_results_to_csv(self, filename: str):
        """Save results to CSV file"""
        if not self.results:
            return
        
        # Convert dataclass to dict for CSV
        results_data = []
        for result in self.results:
            result_dict = asdict(result)
            results_data.append(result_dict)
        
        # Create DataFrame and save
        df = pd.DataFrame(results_data)
        df.to_csv(filename, index=False)
        
        print(f"✓ Results saved to {filename}")
    
    def print_final_summary(self):
        """Print final summary statistics"""
        if not self.results:
            print(f"{Fore.RED}❌ No results to summarize{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}📈 FINAL SUMMARY{Style.RESET_ALL}")
        print("=" * 60)
        
        # Overall statistics
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if not r.timeout_reached)
        validation_passed = sum(1 for r in self.results if r.validation_passed)
        
        print(f"Total tests: {total_tests}")
        print(f"Successful tests: {successful_tests}")
        print(f"Validation passed: {validation_passed}")
        print()
        
        # Performance statistics
        cpu_wins = sum(1 for r in self.results if r.speedup > 1.0 and not r.timeout_reached)
        gpu_wins = sum(1 for r in self.results if r.speedup < 1.0 and not r.timeout_reached)
        
        print(f"CPU wins: {cpu_wins}")
        print(f"GPU wins: {gpu_wins}")
        print()
        
        # Average performance
        avg_cpu_throughput = sum(r.cpu_throughput_mbps for r in self.results if not r.timeout_reached) / successful_tests
        avg_gpu_throughput = sum(r.gpu_throughput_mbps for r in self.results if not r.timeout_reached) / successful_tests
        avg_speedup = sum(r.speedup for r in self.results if not r.timeout_reached) / successful_tests
        
        print(f"Average CPU throughput: {avg_cpu_throughput:.1f} MB/s")
        print(f"Average GPU throughput: {avg_gpu_throughput:.1f} MB/s")
        print(f"Average speedup: {avg_speedup:.2f}x")

def main():
    """Main benchmark execution"""
    parser = argparse.ArgumentParser(description='Comprehensive PCAP Pattern Matching Benchmark')
    parser.add_argument('--file', '-f', help='Specific PCAP file to test')
    parser.add_argument('--test-id', '-t', help='Specific test ID to run (e.g., test_001)')
    parser.add_argument('--quick', '-q', action='store_true', help='Run only first 3 tests for quick validation')
    parser.add_argument('--resume-from', '-r', help='Resume benchmark from specific test ID (e.g., test_019)')
    parser.add_argument('--list-tests', '-l', action='store_true', help='List all available tests')
    
    args = parser.parse_args()
    
    print(f"{Fore.CYAN}🧪 Comprehensive PCAP Pattern Matching Benchmark{Style.RESET_ALL}")
    print(f"{Fore.CYAN}=" * 60 + Style.RESET_ALL)
    
    benchmark = ComprehensivePatternBenchmark(args.file)
    
    if args.list_tests:
        benchmark.list_tests()
        return 0
    
    if args.test_id:
        print(f"{Fore.YELLOW}🎯 Running specific test: {args.test_id}{Style.RESET_ALL}")
        benchmark.run_specific_test(args.test_id)
        return 0
    elif args.quick:
        print(f"{Fore.YELLOW}⚡ Running quick validation (first 3 tests){Style.RESET_ALL}")
        benchmark.run_quick_test()
        return 0
    elif args.resume_from:
        print(f"{Fore.YELLOW}🔄 Resuming benchmark from: {args.resume_from}{Style.RESET_ALL}")
        success = benchmark.run_all_tests(resume_from=args.resume_from)
        
        if success:
            # Save final results
            benchmark.save_results_to_csv("comprehensive_benchmark_results.csv")
            
            # Print final summary
            benchmark.print_final_summary()
            
            print(f"\n{Fore.GREEN}✅ Comprehensive benchmark completed successfully!{Style.RESET_ALL}")
            print(f"📄 Results saved to: comprehensive_benchmark_results.csv")
            return 0
        else:
            print(f"\n{Fore.RED}❌ Comprehensive benchmark failed{Style.RESET_ALL}")
            return 1
    else:
        success = benchmark.run_all_tests()
        
        if success:
            # Save final results
            benchmark.save_results_to_csv("comprehensive_benchmark_results.csv")
            
            # Print final summary
            benchmark.print_final_summary()
            
            print(f"\n{Fore.GREEN}✅ Comprehensive benchmark completed successfully!{Style.RESET_ALL}")
            print(f"📄 Results saved to: comprehensive_benchmark_results.csv")
            return 0
        else:
            print(f"\n{Fore.RED}❌ Comprehensive benchmark failed{Style.RESET_ALL}")
            return 1

if __name__ == "__main__":
    sys.exit(main())