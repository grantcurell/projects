#!/usr/bin/env python3
"""
Comprehensive GPU PCAP Test Runner
Runs newtest.py across all PCAP files and pattern combinations
"""

import subprocess
import os
import sys
from datetime import datetime

def run_comprehensive_test():
    """Run comprehensive test across all PCAP files and pattern counts"""
    
    # Define test patterns
    patterns_1 = ["password"]
    patterns_7 = ["password", "GET", "POST", "HTTP", "HTTPS", "User-Agent", "Authorization"]
    patterns_14 = ["password", "GET", "POST", "HTTP", "HTTPS", "User-Agent", "Authorization", 
                   "admin", "login", "session", "token", "malware", "virus", "exploit", "vulnerability"]
    
    # Define PCAP files to test
    pcap_files = [
        "PCAP Files/synthetic_50mb.pcapng",
        "PCAP Files/synthetic_100mb.pcapng", 
        "PCAP Files/synthetic_200mb.pcapng",
        "PCAP Files/synthetic_500mb.pcapng",
        "PCAP Files/synthetic_1000mb.pcapng",
        "PCAP Files/synthetic_large_50mb.pcapng",
        "PCAP Files/synthetic_large_100mb.pcapng",
        "PCAP Files/synthetic_large_200mb.pcapng", 
        "PCAP Files/synthetic_large_500mb.pcapng",
        "PCAP Files/synthetic_large_1000mb.pcapng"
    ]
    
    # Check which files actually exist
    existing_files = []
    for pcap_file in pcap_files:
        if os.path.exists(pcap_file):
            existing_files.append(pcap_file)
        else:
            print(f"Warning: {pcap_file} not found, skipping...")
    
    if not existing_files:
        print("No PCAP files found!")
        return
    
    # Create results CSV
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_filename = f"gpu_test_results_{timestamp}.csv"
    
    print(f"Starting comprehensive GPU PCAP tests...")
    print(f"Results will be saved to: {csv_filename}")
    print(f"Testing {len(existing_files)} PCAP files with 1, 7, and 14 patterns each")
    print("=" * 80)
    
    total_tests = len(existing_files) * 3
    current_test = 0
    
    for pcap_file in existing_files:
        for patterns, pattern_count in [(patterns_1, 1), (patterns_7, 7), (patterns_14, 14)]:
            current_test += 1
            print(f"[{current_test}/{total_tests}] Testing {os.path.basename(pcap_file)} with {pattern_count} patterns...")
            
            # Build command
            cmd = ["python", "newtest.py", pcap_file, "--csv-output", csv_filename]
            for pattern in patterns:
                cmd.extend(["-s", pattern])
            
            try:
                # Run the test
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0:
                    print(f"  ✓ Success")
                else:
                    print(f"  ✗ Error: {result.stderr}")
                    
            except subprocess.TimeoutExpired:
                print(f"  ✗ Timeout after 5 minutes")
            except Exception as e:
                print(f"  ✗ Exception: {e}")
    
    print("=" * 80)
    print(f"Testing completed! Results saved to {csv_filename}")
    
    # Show summary
    if os.path.exists(csv_filename):
        import pandas as pd
        try:
            df = pd.read_csv(csv_filename)
            successful_tests = df[df['throughput_mbps'] > 0]
            if len(successful_tests) > 0:
                avg_throughput = successful_tests['throughput_mbps'].mean()
                max_throughput = successful_tests['throughput_mbps'].max()
                total_matches = successful_tests['num_matches'].sum()
                
                print(f"Average throughput: {avg_throughput:.2f} MB/s")
                print(f"Maximum throughput: {max_throughput:.2f} MB/s")
                print(f"Total matches found: {total_matches:,}")
        except ImportError:
            print("Install pandas to see summary statistics: pip install pandas")

if __name__ == "__main__":
    run_comprehensive_test()
