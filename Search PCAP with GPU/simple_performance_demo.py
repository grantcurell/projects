#!/usr/bin/env python3
"""
Simple Performance Metrics Demo

This script provides focused performance metrics to demonstrate the efficiency
and speed of our GPU-accelerated PCAP scanner.
"""

import os
import sys
import time
import psutil
from pathlib import Path
from colorama import init, Fore, Style
import pandas as pd

# Initialize colorama
init(autoreset=True)

def get_file_size_mb(filepath: str) -> float:
    """Get file size in MB"""
    return os.path.getsize(filepath) / 1024 / 1024

def format_time(seconds: float) -> str:
    """Format time in human readable format"""
    if seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m {seconds % 60:.0f}s"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h {(seconds % 3600) / 60:.0f}m"

def run_performance_test(pcap_file: str, patterns: list):
    """Run a single performance test"""
    print(f"{Fore.CYAN}🚀 Running Performance Test{Style.RESET_ALL}")
    print(f"File: {pcap_file}")
    print(f"Size: {get_file_size_mb(pcap_file):.1f} MB")
    print(f"Patterns: {len(patterns)} patterns")
    print()
    
    # Import GPU scanner
    try:
        from pcap_gpu_scanner import PCAPScanner
    except Exception as e:
        print(f"{Fore.RED}❌ Failed to import GPU scanner: {e}{Style.RESET_ALL}")
        return None
    
    # Monitor system resources
    process = psutil.Process()
    memory_before = process.memory_info().rss / 1024 / 1024
    cpu_percent_before = psutil.cpu_percent()
    
    print(f"{Fore.BLUE}🔍 Starting GPU scan...{Style.RESET_ALL}")
    
    # Run the scan
    start_time = time.time()
    try:
        scanner = PCAPScanner(patterns, use_regex=False)
        matches = scanner.scan_pcap(pcap_file)
        end_time = time.time()
        
        # Get final metrics
        memory_after = process.memory_info().rss / 1024 / 1024
        cpu_percent_after = psutil.cpu_percent()
        
        processing_time = end_time - start_time
        file_size_mb = get_file_size_mb(pcap_file)
        throughput_mbps = file_size_mb / processing_time if processing_time > 0 else 0
        memory_usage = memory_after - memory_before
        
        # Get GPU memory usage
        try:
            import cupy as cp
            gpu_memory = cp.cuda.runtime.memGetInfo()[0] / 1024 / 1024
        except:
            gpu_memory = 0
        
        return {
            'processing_time': processing_time,
            'file_size_mb': file_size_mb,
            'throughput_mbps': throughput_mbps,
            'memory_usage_mb': memory_usage,
            'gpu_memory_mb': gpu_memory,
            'matches_found': len(matches),
            'pattern_count': len(patterns),
            'packets_per_second': scanner.stats.total_packets / processing_time if processing_time > 0 else 0
        }
        
    except Exception as e:
        print(f"{Fore.RED}❌ Scan failed: {e}{Style.RESET_ALL}")
        return None

def main():
    """Main performance demonstration"""
    print(f"{Fore.CYAN}🎯 GPU-Accelerated PCAP Scanner Performance Demo{Style.RESET_ALL}")
    print("=" * 60)
    
    # Find available PCAP files
    pcap_files = list(Path("PCAP Files").glob("*.pcap*"))
    
    if not pcap_files:
        print(f"{Fore.RED}❌ No PCAP files found in PCAP Files directory{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 Run: python download_pcaps.py --synthetic 50 100 200{Style.RESET_ALL}")
        return
    
    # Test patterns
    test_patterns = [
        ["HTTP", "GET", "POST"],  # Web traffic
        ["password", "admin", "login", "session", "token"],  # Security
        ["malware", "virus", "trojan", "backdoor", "exploit"],  # Threats
        ["PDF", "EXE", "DLL", "ZIP", "RAR"],  # File types
        ["HTTP", "GET", "POST", "password", "admin", "login", "session", "token", "malware", "virus", "trojan", "PDF", "EXE", "DLL", "ZIP", "RAR"]  # All patterns
    ]
    
    pattern_names = ["Web Traffic", "Security", "Threats", "File Types", "All Patterns"]
    
    results = []
    
    # Test each PCAP file
    for pcap_file in pcap_files:
        file_size_mb = get_file_size_mb(str(pcap_file))
        print(f"\n{Fore.YELLOW}📁 Testing: {pcap_file.name} ({file_size_mb:.1f} MB){Style.RESET_ALL}")
        
        # Test with different pattern sets
        for i, (patterns, name) in enumerate(zip(test_patterns, pattern_names)):
            print(f"\n{Fore.BLUE}🔍 Pattern Set: {name} ({len(patterns)} patterns){Style.RESET_ALL}")
            
            result = run_performance_test(str(pcap_file), patterns)
            if result:
                result['file_name'] = pcap_file.name
                result['pattern_set'] = name
                results.append(result)
                
                # Print immediate results
                print(f"{Fore.GREEN}✓ Completed in {format_time(result['processing_time'])}")
                print(f"   Throughput: {result['throughput_mbps']:.2f} MB/s")
                print(f"   Matches: {result['matches_found']:,}")
                print(f"   Memory: {result['memory_usage_mb']:.1f} MB")
                print(f"   GPU Memory: {result['gpu_memory_mb']:.1f} MB")
                print(f"   Packets/sec: {result['packets_per_second']:,.0f}{Style.RESET_ALL}")
    
    # Generate summary report
    if results:
        print(f"\n{Fore.CYAN}📊 Performance Summary{Style.RESET_ALL}")
        print("=" * 60)
        
        # Create DataFrame
        df = pd.DataFrame(results)
        
        # Best performance metrics
        best_throughput = df['throughput_mbps'].max()
        fastest_time = df['processing_time'].min()
        largest_file = df['file_size_mb'].max()
        most_patterns = df['pattern_count'].max()
        
        print(f"🚀 Best Throughput: {best_throughput:.2f} MB/s")
        print(f"⚡ Fastest Processing: {format_time(fastest_time)}")
        print(f"📁 Largest File Processed: {largest_file:.1f} MB")
        print(f"🔍 Most Patterns Tested: {most_patterns}")
        
        # Average metrics
        avg_throughput = df['throughput_mbps'].mean()
        avg_memory = df['memory_usage_mb'].mean()
        avg_gpu_memory = df['gpu_memory_mb'].mean()
        
        print(f"\n📈 Average Performance:")
        print(f"   Throughput: {avg_throughput:.2f} MB/s")
        print(f"   Memory Usage: {avg_memory:.1f} MB")
        print(f"   GPU Memory: {avg_gpu_memory:.1f} MB")
        
        # Save detailed results
        output_file = "performance_results.csv"
        df.to_csv(output_file, index=False)
        print(f"\n{Fore.GREEN}📄 Detailed results saved to: {output_file}{Style.RESET_ALL}")
        
        # Show top performers
        print(f"\n🏆 Top Performers:")
        top_throughput = df.nlargest(3, 'throughput_mbps')
        for _, row in top_throughput.iterrows():
            print(f"   {row['file_name']} - {row['throughput_mbps']:.2f} MB/s ({row['pattern_set']})")
    
    print(f"\n{Fore.GREEN}🎉 Performance demo completed!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
