#!/usr/bin/env python3
"""
Simple Pattern Matching Benchmark - Isolated Performance Test

This benchmark focuses ONLY on pattern matching performance by:
1. Reading the 1GB PCAP file once
2. Extracting payloads using identical TCP reassembly
3. Running simple pattern matching (CPU vs GPU)
4. Setting a 3-minute time limit
5. Providing clear performance metrics

No complex test cases, no multiple files - just pure pattern matching performance.
"""

import os
import sys
import time
import threading
import logging
from pathlib import Path
from typing import List, Tuple, Optional
from dataclasses import dataclass
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('simple_benchmark.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our modules
from pcap_gpu_scanner import PCAPScanner, TCPReassembler, FlowKey
from scapy.all import rdpcap, IP, TCP, UDP

# Global timeout flag
timeout_reached = False

def timeout_handler():
    """Handle timeout"""
    global timeout_reached
    time.sleep(180)  # 3 minutes
    timeout_reached = True
    print(f"\n{Fore.RED}⏰ TIMEOUT REACHED (3 minutes) - Stopping benchmark{Style.RESET_ALL}")
    os._exit(1)

@dataclass
class SimpleBenchmarkResult:
    """Results from simple benchmark test"""
    test_name: str
    pcap_file: str
    file_size_mb: float
    payload_count: int
    total_bytes: int
    cpu_time: float
    gpu_time: float
    cpu_matches: int
    gpu_matches: int
    cpu_throughput_mbps: float
    gpu_throughput_mbps: float
    speedup: float
    validation_passed: bool
    timeout_reached: bool

class SimplePatternBenchmark:
    """Simple benchmark focused only on pattern matching performance"""
    
    def __init__(self, pcap_file: str, patterns: List[str]):
        self.pcap_file = pcap_file
        self.patterns = patterns
        self.results: List[SimpleBenchmarkResult] = []
        
        # Set up timeout
        timeout_thread = threading.Thread(target=timeout_handler, daemon=True)
        timeout_thread.start()
        
        print(f"{Fore.CYAN}{Style.BRIGHT}🔬 Simple Pattern Matching Benchmark{Style.RESET_ALL}")
        print("=" * 60)
        print(f"{Fore.YELLOW}📁 PCAP File: {Path(pcap_file).name}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}🔍 Patterns: {', '.join(patterns)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}⏰ Time Limit: 3 minutes{Style.RESET_ALL}")
        print()
    
    def _extract_payloads_unified(self) -> Tuple[List[bytes], List[str], int, int]:
        """Extract payloads using unified TCP reassembly (same for both CPU and GPU)"""
        print(f"{Fore.BLUE}📖 Reading PCAP file...{Style.RESET_ALL}")
        start_time = time.time()
        
        try:
            packets = rdpcap(self.pcap_file)
            read_time = time.time() - start_time
            
            print(f"{Fore.BLUE}🔧 Performing TCP reassembly...{Style.RESET_ALL}")
            reassembly_start = time.time()
            
            # Use unified TCP reassembly logic
            reassembler = TCPReassembler()
            payloads = []
            flow_ids = []
            total_bytes = 0
            
            for packet in packets:
                if packet.haslayer(IP) and packet.haslayer(TCP):
                    ip_layer = packet[IP]
                    tcp_layer = packet[TCP]
                    
                    # Add packet to reassembler
                    result = reassembler.add_packet(packet)
                    if result:
                        flow_key, reassembled_payload, timestamp = result
                        payloads.append(reassembled_payload)
                        flow_ids.append(f"{flow_key.src_ip}:{flow_key.src_port}-{flow_key.dst_ip}:{flow_key.dst_port}")
                        total_bytes += len(reassembled_payload)
            
            reassembly_time = time.time() - reassembly_start
            
            print(f"✓ Extracted {len(payloads):,} payloads ({total_bytes:,} bytes)")
            print(f"✓ Read time: {read_time:.3f}s, Reassembly time: {reassembly_time:.3f}s")
            
            return payloads, flow_ids, total_bytes, len(payloads)
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error reading PCAP: {e}{Style.RESET_ALL}")
            return [], [], 0, 0
    
    def _run_cpu_benchmark(self, payloads: List[bytes], flow_ids: List[str]) -> Tuple[int, float]:
        """Run CPU-only pattern matching benchmark"""
        print(f"{Fore.GREEN}🖥️  Running CPU benchmark...{Style.RESET_ALL}")
        
        start_time = time.time()
        
        # Simple CPU pattern matching
        matches = 0
        pattern_bytes = [p.encode() if isinstance(p, str) else p for p in self.patterns]
        
        for payload in payloads:
            for pattern in pattern_bytes:
                if pattern in payload:
                    matches += 1
        
        cpu_time = time.time() - start_time
        print(f"✓ CPU: {cpu_time:.3f}s, {matches:,} matches")
        
        return matches, cpu_time
    
    def _run_gpu_benchmark(self, payloads: List[bytes], flow_ids: List[str]) -> Tuple[int, float]:
        """Run GPU-accelerated pattern matching benchmark"""
        print(f"{Fore.MAGENTA}🚀 Running GPU benchmark...{Style.RESET_ALL}")
        
        start_time = time.time()
        
        try:
            # Create GPU scanner
            gpu_scanner = PCAPScanner(self.patterns, use_regex=False)
            gpu_matches = gpu_scanner.gpu_scanner.scan_payloads(payloads, flow_ids)
            
            gpu_time = time.time() - start_time
            print(f"✓ GPU: {gpu_time:.3f}s, {len(gpu_matches):,} matches")
            
            return len(gpu_matches), gpu_time
            
        except Exception as e:
            print(f"{Fore.RED}❌ GPU Error: {e}{Style.RESET_ALL}")
            return 0, time.time() - start_time
    
    def run_benchmark(self) -> bool:
        """Run the complete benchmark"""
        global timeout_reached
        
        try:
            # Extract payloads once
            payloads, flow_ids, total_bytes, payload_count = self._extract_payloads_unified()
            
            if not payloads:
                print(f"{Fore.RED}❌ No payloads extracted{Style.RESET_ALL}")
                return False
            
            file_size_mb = Path(self.pcap_file).stat().st_size / 1024 / 1024
            
            # Run CPU benchmark
            cpu_matches, cpu_time = self._run_cpu_benchmark(payloads, flow_ids)
            
            if timeout_reached:
                return False
            
            # Run GPU benchmark
            gpu_matches, gpu_time = self._run_gpu_benchmark(payloads, flow_ids)
            
            if timeout_reached:
                return False
            
            # Calculate metrics
            cpu_throughput_mbps = (total_bytes / 1024 / 1024) / cpu_time if cpu_time > 0 else 0
            gpu_throughput_mbps = (total_bytes / 1024 / 1024) / gpu_time if gpu_time > 0 else 0
            speedup = cpu_time / gpu_time if gpu_time > 0 else 0
            validation_passed = cpu_matches == gpu_matches
            
            # Store results
            result = SimpleBenchmarkResult(
                test_name="simple_pattern_match",
                pcap_file=Path(self.pcap_file).name,
                file_size_mb=file_size_mb,
                payload_count=payload_count,
                total_bytes=total_bytes,
                cpu_time=cpu_time,
                gpu_time=gpu_time,
                cpu_matches=cpu_matches,
                gpu_matches=gpu_matches,
                cpu_throughput_mbps=cpu_throughput_mbps,
                gpu_throughput_mbps=gpu_throughput_mbps,
                speedup=speedup,
                validation_passed=validation_passed,
                timeout_reached=timeout_reached
            )
            
            self.results.append(result)
            
            # Print summary
            self._print_summary(result)
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ Benchmark failed: {e}{Style.RESET_ALL}")
            return False
        finally:
            # Timeout handled by daemon thread
            pass
    
    def _print_summary(self, result: SimpleBenchmarkResult):
        """Print benchmark summary"""
        print(f"\n{Fore.CYAN}📊 BENCHMARK SUMMARY{Style.RESET_ALL}")
        print("=" * 60)
        
        print(f"File: {result.pcap_file}")
        print(f"Size: {result.file_size_mb:.1f} MB")
        print(f"Payloads: {result.payload_count:,}")
        print(f"Total Data: {result.total_bytes:,} bytes")
        print()
        
        print(f"CPU Performance:")
        print(f"  Time: {result.cpu_time:.3f}s")
        print(f"  Throughput: {result.cpu_throughput_mbps:.2f} MB/s")
        print(f"  Matches: {result.cpu_matches:,}")
        print()
        
        print(f"GPU Performance:")
        print(f"  Time: {result.gpu_time:.3f}s")
        print(f"  Throughput: {result.gpu_throughput_mbps:.2f} MB/s")
        print(f"  Matches: {result.gpu_matches:,}")
        print()
        
        print(f"Comparison:")
        print(f"  Speedup: {result.speedup:.2f}x")
        print(f"  Validation: {'✅ PASSED' if result.validation_passed else '❌ FAILED'}")
        
        if result.timeout_reached:
            print(f"  Status: {Fore.RED}⏰ TIMEOUT REACHED{Style.RESET_ALL}")
        
        # Performance assessment
        if result.speedup > 1.0:
            print(f"\n{Fore.GREEN}✅ GPU is {result.speedup:.2f}x faster than CPU{Style.RESET_ALL}")
        elif result.speedup < 0.5:
            print(f"\n{Fore.RED}❌ GPU is significantly slower ({result.speedup:.2f}x){Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}⚠️  GPU performance is similar to CPU ({result.speedup:.2f}x){Style.RESET_ALL}")

def main():
    """Main benchmark execution"""
    if len(sys.argv) < 2:
        print(f"{Fore.RED}Usage: python simple_pattern_benchmark.py <pcap_file> [pattern1] [pattern2] ...{Style.RESET_ALL}")
        return 1
    
    pcap_file = sys.argv[1]
    patterns = sys.argv[2:] if len(sys.argv) > 2 else ["HTTP", "GET", "POST"]
    
    if not Path(pcap_file).exists():
        print(f"{Fore.RED}❌ File not found: {pcap_file}{Style.RESET_ALL}")
        return 1
    
    benchmark = SimplePatternBenchmark(pcap_file, patterns)
    
    success = benchmark.run_benchmark()
    
    if success:
        print(f"\n{Fore.GREEN}✅ Benchmark completed successfully!{Style.RESET_ALL}")
        return 0
    else:
        print(f"\n{Fore.RED}❌ Benchmark failed or timed out{Style.RESET_ALL}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
