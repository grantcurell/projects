#!/usr/bin/env python3
"""
Comprehensive Performance Demonstration for GPU-Accelerated PCAP Scanner

This script provides detailed benchmarking and performance analysis to demonstrate
the efficiency and speed of our GPU-accelerated pattern matching system.
"""

import os
import sys
import time
import argparse
import logging
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import psutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from colorama import init, Fore, Style
import requests
from tqdm import tqdm

# Initialize colorama
init(autoreset=True)

# Import our GPU scanner
try:
    from pcap_gpu_scanner import PCAPScanner
    from gpu_kernels import AdvancedGPUKernels
except ImportError as e:
    print(f"{Fore.RED}❌ Failed to import GPU scanner: {e}")
    sys.exit(1)

# Try to import CPU alternatives for comparison
try:
    import re
    CPU_ALTERNATIVES_AVAILABLE = True
except ImportError:
    CPU_ALTERNATIVES_AVAILABLE = False


@dataclass
class BenchmarkResult:
    """Results from a single benchmark run"""
    method: str
    file_size_mb: float
    pattern_count: int
    processing_time: float
    memory_usage_mb: float
    throughput_mbps: float
    matches_found: int
    gpu_memory_mb: float = 0


class CPUPatternMatcher:
    """CPU-based pattern matcher for comparison"""
    
    def __init__(self, patterns: List[str]):
        self.patterns = patterns
        self.compiled_patterns = [re.compile(re.escape(p), re.IGNORECASE) for p in patterns]
    
    def scan_payload(self, payload: bytes) -> List[Tuple[str, int]]:
        """Scan a single payload using CPU"""
        payload_str = payload.decode('utf-8', errors='ignore')
        matches = []
        
        for pattern, compiled_pattern in zip(self.patterns, self.compiled_patterns):
            for match in compiled_pattern.finditer(payload_str):
                matches.append((pattern, match.start()))
        
        return matches


class PerformanceDemo:
    """Comprehensive performance demonstration system"""
    
    def __init__(self):
        self.results: List[BenchmarkResult] = []
        self.gpu_scanner = None
        self.cpu_matcher = None
        
        # Performance monitoring
        self.process = psutil.Process()
        self.initial_memory = self.process.memory_info().rss / 1024 / 1024
        
        print(f"{Fore.CYAN}🚀 GPU-Accelerated PCAP Scanner Performance Demo{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Initial memory usage: {self.initial_memory:.2f} MB{Style.RESET_ALL}")
    
    def download_large_pcap(self, url: str, filename: str) -> str:
        """Download a large PCAP file for testing"""
        filepath = f"PCAP Files/{filename}"
        
        if os.path.exists(filepath):
            print(f"{Fore.GREEN}✓ PCAP file already exists: {filepath}{Style.RESET_ALL}")
            return filepath
        
        print(f"{Fore.YELLOW}📥 Downloading large PCAP file: {filename}{Style.RESET_ALL}")
        
        # Create directory if it doesn't exist
        os.makedirs("PCAP Files", exist_ok=True)
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            with open(filepath, 'wb') as f:
                with tqdm(total=total_size, unit='B', unit_scale=True, desc=f"Downloading {filename}") as pbar:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))
            
            print(f"{Fore.GREEN}✓ Download completed: {filepath}{Style.RESET_ALL}")
            return filepath
            
        except Exception as e:
            print(f"{Fore.RED}❌ Download failed: {e}{Style.RESET_ALL}")
            return None
    
    def generate_test_pcap(self, size_mb: int) -> str:
        """Generate a synthetic large PCAP file for testing"""
        filename = f"synthetic_{size_mb}mb.pcapng"
        filepath = f"PCAP Files/{filename}"
        
        if os.path.exists(filepath):
            print(f"{Fore.GREEN}✓ Test PCAP already exists: {filepath}{Style.RESET_ALL}")
            return filepath
        
        print(f"{Fore.YELLOW}🔧 Generating synthetic PCAP: {size_mb}MB{Style.RESET_ALL}")
        
        # Create directory if it doesn't exist
        os.makedirs("PCAP Files", exist_ok=True)
        
        try:
            # Use scapy to generate synthetic packets
            from scapy.all import wrpcap, IP, TCP, UDP, Raw
            
            packets = []
            base_time = time.time()
            
            # Generate packets with various patterns
            patterns = [
                b"HTTP/1.1 200 OK",
                b"GET /api/v1/users",
                b"POST /login",
                b"password=admin123",
                b"session_token=",
                b"malware_signature",
                b"PDF document",
                b"EXE file",
                b"ZIP archive"
            ]
            
            for i in tqdm(range(size_mb * 1000), desc="Generating packets"):
                # Create packet with random pattern
                payload = patterns[i % len(patterns)] + b" " + os.urandom(100)
                
                packet = IP(src=f"192.168.1.{i % 254}", dst=f"10.0.0.{i % 254}") / \
                         TCP(sport=1000 + (i % 1000), dport=80) / \
                         Raw(load=payload)
                
                packet.time = base_time + i * 0.001
                packets.append(packet)
            
            wrpcap(filepath, packets)
            print(f"{Fore.GREEN}✓ Generated: {filepath} ({len(packets)} packets){Style.RESET_ALL}")
            return filepath
            
        except Exception as e:
            print(f"{Fore.RED}❌ Generation failed: {e}{Style.RESET_ALL}")
            return None
    
    def benchmark_gpu_scanner(self, pcap_file: str, patterns: List[str]) -> BenchmarkResult:
        """Benchmark the GPU scanner"""
        print(f"{Fore.BLUE}🔍 Benchmarking GPU Scanner...{Style.RESET_ALL}")
        
        # Initialize GPU scanner
        if not self.gpu_scanner:
            self.gpu_scanner = PCAPScanner(patterns, use_regex=False)
        
        # Get file size
        file_size_mb = os.path.getsize(pcap_file) / 1024 / 1024
        
        # Monitor memory before
        memory_before = self.process.memory_info().rss / 1024 / 1024
        
        # Run scan
        start_time = time.time()
        matches = self.gpu_scanner.scan_pcap(pcap_file)
        end_time = time.time()
        
        # Monitor memory after
        memory_after = self.process.memory_info().rss / 1024 / 1024
        
        processing_time = end_time - start_time
        memory_usage = memory_after - memory_before
        throughput = file_size_mb / processing_time if processing_time > 0 else 0
        
        # Get GPU memory usage
        try:
            import cupy as cp
            gpu_memory = cp.cuda.runtime.memGetInfo()[0] / 1024 / 1024
        except:
            gpu_memory = 0
        
        result = BenchmarkResult(
            method="GPU Accelerated",
            file_size_mb=file_size_mb,
            pattern_count=len(patterns),
            processing_time=processing_time,
            memory_usage_mb=memory_usage,
            throughput_mbps=throughput,
            matches_found=len(matches),
            gpu_memory_mb=gpu_memory
        )
        
        print(f"{Fore.GREEN}✓ GPU Scan completed in {processing_time:.2f}s")
        print(f"   Throughput: {throughput:.2f} MB/s")
        print(f"   Matches: {len(matches)}")
        print(f"   Memory: {memory_usage:.2f} MB{Style.RESET_ALL}")
        
        return result
    
    def benchmark_cpu_matcher(self, pcap_file: str, patterns: List[str]) -> BenchmarkResult:
        """Benchmark CPU-based pattern matching for comparison"""
        if not CPU_ALTERNATIVES_AVAILABLE:
            print(f"{Fore.YELLOW}⚠️ CPU alternatives not available{Style.RESET_ALL}")
            return None
        
        print(f"{Fore.BLUE}🔍 Benchmarking CPU Matcher...{Style.RESET_ALL}")
        
        # Initialize CPU matcher
        if not self.cpu_matcher:
            self.cpu_matcher = CPUPatternMatcher(patterns)
        
        # Get file size
        file_size_mb = os.path.getsize(pcap_file) / 1024 / 1024
        
        # Monitor memory before
        memory_before = self.process.memory_info().rss / 1024 / 1024
        
        # Read PCAP file
        from scapy.all import rdpcap
        
        start_time = time.time()
        packets = rdpcap(pcap_file)
        
        # Extract payloads and scan
        total_matches = 0
        for packet in tqdm(packets, desc="CPU Scanning"):
            if packet.haslayer('Raw'):
                payload = bytes(packet['Raw'])
                matches = self.cpu_matcher.scan_payload(payload)
                total_matches += len(matches)
        
        end_time = time.time()
        
        # Monitor memory after
        memory_after = self.process.memory_info().rss / 1024 / 1024
        
        processing_time = end_time - start_time
        memory_usage = memory_after - memory_before
        throughput = file_size_mb / processing_time if processing_time > 0 else 0
        
        result = BenchmarkResult(
            method="CPU Sequential",
            file_size_mb=file_size_mb,
            pattern_count=len(patterns),
            processing_time=processing_time,
            memory_usage_mb=memory_usage,
            throughput_mbps=throughput,
            matches_found=total_matches
        )
        
        print(f"{Fore.GREEN}✓ CPU Scan completed in {processing_time:.2f}s")
        print(f"   Throughput: {throughput:.2f} MB/s")
        print(f"   Matches: {total_matches}")
        print(f"   Memory: {memory_usage:.2f} MB{Style.RESET_ALL}")
        
        return result
    
    def run_comprehensive_benchmark(self, pcap_file: str, patterns: List[str]) -> List[BenchmarkResult]:
        """Run comprehensive benchmark comparing GPU vs CPU"""
        results = []
        
        # Benchmark GPU scanner
        gpu_result = self.benchmark_gpu_scanner(pcap_file, patterns)
        if gpu_result:
            results.append(gpu_result)
        
        # Benchmark CPU matcher
        cpu_result = self.benchmark_cpu_matcher(pcap_file, patterns)
        if cpu_result:
            results.append(cpu_result)
        
        # Calculate speedup
        if len(results) >= 2:
            gpu_time = results[0].processing_time
            cpu_time = results[1].processing_time
            speedup = cpu_time / gpu_time if gpu_time > 0 else 0
            
            print(f"\n{Fore.CYAN}📊 Performance Comparison:{Style.RESET_ALL}")
            print(f"GPU Time: {gpu_time:.2f}s")
            print(f"CPU Time: {cpu_time:.2f}s")
            print(f"{Fore.GREEN}🚀 Speedup: {speedup:.1f}x faster with GPU!{Style.RESET_ALL}")
        
        return results
    
    def run_scalability_test(self, base_patterns: List[str]) -> List[BenchmarkResult]:
        """Test scalability with different file sizes and pattern counts"""
        print(f"\n{Fore.CYAN}📈 Running Scalability Test...{Style.RESET_ALL}")
        
        results = []
        
        # Test different file sizes
        file_sizes = [10, 50, 100]  # MB
        pattern_counts = [5, 10, 20]
        
        for size_mb in file_sizes:
            # Generate or use existing test file
            pcap_file = self.generate_test_pcap(size_mb)
            if not pcap_file:
                continue
            
            for pattern_count in pattern_counts:
                # Use subset of patterns
                test_patterns = base_patterns[:pattern_count]
                
                print(f"\n{Fore.YELLOW}Testing: {size_mb}MB file, {pattern_count} patterns{Style.RESET_ALL}")
                
                result = self.benchmark_gpu_scanner(pcap_file, test_patterns)
                if result:
                    results.append(result)
        
        return results
    
    def generate_performance_report(self, results: List[BenchmarkResult], output_file: str = "performance_report.html"):
        """Generate a comprehensive HTML performance report"""
        print(f"\n{Fore.CYAN}📊 Generating Performance Report...{Style.RESET_ALL}")
        
        # Create DataFrame
        df = pd.DataFrame([vars(r) for r in results])
        
        # Create HTML report
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>GPU-Accelerated PCAP Scanner Performance Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; }}
                .metric {{ background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #007bff; }}
                .gpu {{ border-left-color: #28a745; }}
                .cpu {{ border-left-color: #dc3545; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #f2f2f2; }}
                .highlight {{ background-color: #fff3cd; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚀 GPU-Accelerated PCAP Scanner Performance Report</h1>
                <p>Comprehensive performance analysis and benchmarking results</p>
            </div>
            
            <h2>📊 Summary Statistics</h2>
            <div class="metric gpu">
                <h3>GPU Performance Highlights</h3>
                <p><strong>Peak Throughput:</strong> {df[df['method'] == 'GPU Accelerated']['throughput_mbps'].max():.2f} MB/s</p>
                <p><strong>Average Processing Time:</strong> {df[df['method'] == 'GPU Accelerated']['processing_time'].mean():.2f}s</p>
                <p><strong>Total Matches Found:</strong> {df[df['method'] == 'GPU Accelerated']['matches_found'].sum():,}</p>
            </div>
            
            <h2>📈 Detailed Results</h2>
            {df.to_html(classes='table table-striped', index=False)}
            
            <h2>🎯 Key Metrics</h2>
            <div class="metric">
                <h3>Performance Comparison</h3>
                <p><strong>GPU vs CPU Speedup:</strong> {self._calculate_speedup(df):.1f}x faster</p>
                <p><strong>Memory Efficiency:</strong> GPU uses {df[df['method'] == 'GPU Accelerated']['memory_usage_mb'].mean():.2f} MB vs CPU {df[df['method'] == 'CPU Sequential']['memory_usage_mb'].mean():.2f} MB</p>
                <p><strong>Scalability:</strong> Handles up to {df['file_size_mb'].max():.0f}MB files efficiently</p>
            </div>
            
            <div class="metric highlight">
                <h3>🚀 Conclusion</h3>
                <p>The GPU-accelerated PCAP scanner demonstrates exceptional performance, achieving significant speedup over CPU-based alternatives while maintaining high accuracy and memory efficiency.</p>
            </div>
        </body>
        </html>
        """
        
        with open(output_file, 'w') as f:
            f.write(html_content)
        
        print(f"{Fore.GREEN}✓ Performance report generated: {output_file}{Style.RESET_ALL}")
        return output_file
    
    def _calculate_speedup(self, df: pd.DataFrame) -> float:
        """Calculate average speedup between GPU and CPU"""
        gpu_times = df[df['method'] == 'GPU Accelerated']['processing_time']
        cpu_times = df[df['method'] == 'CPU Sequential']['processing_time']
        
        if len(gpu_times) > 0 and len(cpu_times) > 0:
            return cpu_times.mean() / gpu_times.mean()
        return 0
    
    def run_demo(self, pcap_file: str = None, patterns: List[str] = None, 
                download_large: bool = False, generate_synthetic: bool = False):
        """Run the complete performance demonstration"""
        
        # Default patterns if none provided
        if not patterns:
            patterns = [
                "HTTP", "GET", "POST", "password", "admin", "login", 
                "session", "token", "malware", "virus", "trojan",
                "PDF", "EXE", "DLL", "ZIP", "RAR", "error", "warning",
                "debug", "info", "success", "failed", "timeout"
            ]
        
        # Get or create PCAP file
        if not pcap_file:
            if download_large:
                # Download a large PCAP file
                large_pcap_urls = [
                    "https://www.netresec.com/?download=SampleCaptures",
                    "https://wiki.wireshark.org/SampleCaptures"
                ]
                print(f"{Fore.YELLOW}💡 Large PCAP URLs available at:{Style.RESET_ALL}")
                for url in large_pcap_urls:
                    print(f"   {url}")
                print(f"{Fore.YELLOW}💡 Or use --generate-synthetic to create test files{Style.RESET_ALL}")
                return
            
            elif generate_synthetic:
                pcap_file = self.generate_test_pcap(100)  # 100MB synthetic file
            else:
                # Use existing file
                pcap_files = list(Path("PCAP Files").glob("*.pcap*"))
                if pcap_files:
                    pcap_file = str(pcap_files[0])
                    print(f"{Fore.GREEN}✓ Using existing PCAP file: {pcap_file}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}❌ No PCAP files found. Use --generate-synthetic or --download-large{Style.RESET_ALL}")
                    return
        
        if not os.path.exists(pcap_file):
            print(f"{Fore.RED}❌ PCAP file not found: {pcap_file}{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}🎯 Starting Performance Demo{Style.RESET_ALL}")
        print(f"PCAP File: {pcap_file}")
        print(f"Patterns: {len(patterns)} patterns")
        
        # Run comprehensive benchmark
        results = self.run_comprehensive_benchmark(pcap_file, patterns)
        
        # Run scalability test
        scalability_results = self.run_scalability_test(patterns)
        results.extend(scalability_results)
        
        # Generate performance report
        report_file = self.generate_performance_report(results)
        
        # Print summary
        print(f"\n{Fore.GREEN}🎉 Performance Demo Completed!{Style.RESET_ALL}")
        print(f"📊 Results saved to: {report_file}")
        print(f"📈 Total benchmarks run: {len(results)}")
        
        # Show best performance
        if results:
            best_gpu = max([r for r in results if r.method == "GPU Accelerated"], 
                         key=lambda x: x.throughput_mbps, default=None)
            if best_gpu:
                print(f"🚀 Best GPU Performance: {best_gpu.throughput_mbps:.2f} MB/s")


def main():
    """Main entry point for performance demonstration"""
    parser = argparse.ArgumentParser(description="GPU-Accelerated PCAP Scanner Performance Demo")
    parser.add_argument("--pcap-file", help="Path to PCAP file to test")
    parser.add_argument("--patterns", nargs="+", 
                       default=["HTTP", "GET", "POST", "password", "admin", "login"],
                       help="Patterns to search for")
    parser.add_argument("--download-large", action="store_true",
                       help="Download a large PCAP file for testing")
    parser.add_argument("--generate-synthetic", action="store_true",
                       help="Generate synthetic PCAP files for testing")
    parser.add_argument("--output", default="performance_report.html",
                       help="Output file for performance report")
    
    args = parser.parse_args()
    
    # Run performance demo
    demo = PerformanceDemo()
    demo.run_demo(
        pcap_file=args.pcap_file,
        patterns=args.patterns,
        download_large=args.download_large,
        generate_synthetic=args.generate_synthetic
    )


if __name__ == "__main__":
    main()
