#!/usr/bin/env python3
"""
Test Script for GPU-Accelerated PCAP Scanner

This script provides various test scenarios and examples for testing the
GPU-accelerated PCAP scanner with different patterns and data sizes.
"""

import os
import sys
import time
import random
import subprocess
from pathlib import Path
import numpy as np
from scapy.all import wrpcap, IP, TCP, UDP, Raw

from pcap_gpu_scanner import PCAPScanner
from gpu_kernels import AdvancedGPUKernels, GPUBenchmark


def create_test_pcap(filename: str, size_mb: int = 10):
    """Create a test PCAP file with random network traffic"""
    print(f"Creating test PCAP file: {filename} ({size_mb} MB)")
    
    packets = []
    target_size = size_mb * 1024 * 1024  # Convert to bytes
    current_size = 0
    
    # Generate random IP addresses
    def random_ip():
        return f"{random.randint(1, 254)}.{random.randint(1, 254)}." \
               f"{random.randint(1, 254)}.{random.randint(1, 254)}"
    
    while current_size < target_size:
        # Create random packet
        if random.choice([True, False]):
            # TCP packet
            payload = os.urandom(random.randint(64, 1500))
            packet = IP(src=random_ip(), dst=random_ip()) / \
                    TCP(sport=random.randint(1024, 65535), 
                        dport=random.randint(1024, 65535)) / \
                    Raw(load=payload)
        else:
            # UDP packet
            payload = os.urandom(random.randint(64, 1500))
            packet = IP(src=random_ip(), dst=random_ip()) / \
                    UDP(sport=random.randint(1024, 65535), 
                        dport=random.randint(1024, 65535)) / \
                    Raw(load=payload)
        
        packets.append(packet)
        current_size += len(packet)
    
    # Write PCAP file
    wrpcap(filename, packets)
    print(f"Created PCAP file with {len(packets)} packets, {current_size/1024/1024:.2f} MB")


def create_pcap_with_patterns(filename: str, patterns: list, size_mb: int = 10):
    """Create a test PCAP file with embedded patterns"""
    print(f"Creating PCAP file with embedded patterns: {filename}")
    
    packets = []
    target_size = size_mb * 1024 * 1024
    current_size = 0
    
    def random_ip():
        return f"{random.randint(1, 254)}.{random.randint(1, 254)}." \
               f"{random.randint(1, 254)}.{random.randint(1, 254)}"
    
    while current_size < target_size:
        # Randomly decide whether to embed a pattern
        if random.random() < 0.1:  # 10% chance to embed pattern
            pattern = random.choice(patterns)
            # Create payload with pattern embedded
            before = os.urandom(random.randint(10, 100))
            after = os.urandom(random.randint(10, 100))
            payload = before + pattern.encode() + after
        else:
            payload = os.urandom(random.randint(64, 1500))
        
        # Create packet
        packet = IP(src=random_ip(), dst=random_ip()) / \
                TCP(sport=random.randint(1024, 65535), 
                    dport=random.randint(1024, 65535)) / \
                Raw(load=payload)
        
        packets.append(packet)
        current_size += len(packet)
    
    wrpcap(filename, packets)
    print(f"Created PCAP file with embedded patterns: {len(packets)} packets")


def test_gpu_kernels():
    """Test the GPU kernels with various inputs"""
    print("Testing GPU kernels...")
    
    # Test data
    test_text = b"This is a test text for pattern matching. It contains multiple patterns to find including test, pattern, matching, and multiple."
    test_patterns = [b"test", b"pattern", b"matching", b"multiple", b"notfound"]
    
    kernels = AdvancedGPUKernels()
    
    # Test Boyer-Moore
    print("\n--- Boyer-Moore Search ---")
    for pattern in test_patterns:
        matches = kernels.boyer_moore_search(test_text, pattern)
        print(f"Pattern '{pattern.decode()}': {len(matches)} matches at positions {matches}")
    
    # Test vectorized search
    print("\n--- Vectorized Multi-Pattern Search ---")
    vectorized_matches = kernels.vectorized_multi_search(test_text, test_patterns)
    for i, pattern in enumerate(test_patterns):
        print(f"Pattern '{pattern.decode()}': {len(vectorized_matches[i])} matches at positions {vectorized_matches[i]}")
    
    # Test Aho-Corasick
    print("\n--- Aho-Corasick Search ---")
    aho_matches = kernels.aho_corasick_search(test_text, test_patterns)
    for i, pattern in enumerate(test_patterns):
        print(f"Pattern '{pattern.decode()}': {len(aho_matches[i])} matches at positions {aho_matches[i]}")


def benchmark_gpu_performance():
    """Run GPU performance benchmarks"""
    print("Running GPU performance benchmarks...")
    
    # Test different text sizes and pattern counts
    text_sizes = [1024*1024, 10*1024*1024, 50*1024*1024]  # 1MB, 10MB, 50MB
    pattern_counts = [1, 5, 10, 20]
    
    results = GPUBenchmark.benchmark_kernels(text_sizes, pattern_counts)
    
    # Print results
    print("\nBenchmark Results:")
    for key, data in results.items():
        print(f"\n{key}:")
        print(f"  Text Size: {data['text_size_mb']:.1f} MB")
        print(f"  Pattern Count: {data['pattern_count']}")
        print(f"  Boyer-Moore: {data['boyer_moore']:.2f} ms")
        print(f"  Vectorized: {data['vectorized']:.2f} ms")
        print(f"  Aho-Corasick: {data['aho_corasick']:.2f} ms")
    
    # Plot results
    GPUBenchmark.plot_benchmark_results(results)


def test_pcap_scanner():
    """Test the PCAP scanner with various scenarios"""
    print("Testing PCAP scanner...")
    
    # Test patterns
    test_patterns = [
        "HTTP",
        "GET",
        "POST",
        "malware",
        "suspicious",
        "password",
        "admin",
        "login",
        "cookie",
        "session"
    ]
    
    # Create test PCAP files
    test_files = []
    
    # Small test file
    create_test_pcap("test_small.pcap", 1)
    test_files.append("test_small.pcap")
    
    # Medium test file with patterns
    create_pcap_with_patterns("test_medium.pcap", test_patterns, 10)
    test_files.append("test_medium.pcap")
    
    # Large test file
    create_test_pcap("test_large.pcap", 50)
    test_files.append("test_large.pcap")
    
    # Test scanner on each file
    for pcap_file in test_files:
        print(f"\n--- Testing {pcap_file} ---")
        
        scanner = PCAPScanner(test_patterns, use_regex=False)
        
        try:
            matches = scanner.scan_pcap(pcap_file)
            scanner.print_stats()
            
            if matches:
                print(f"Found {len(matches)} matches:")
                for match in matches[:5]:  # Show first 5 matches
                    print(f"  Flow: {match.flow_id}, Pattern: {match.pattern}, Offset: {match.offset}")
                if len(matches) > 5:
                    print(f"  ... and {len(matches) - 5} more matches")
            else:
                print("No matches found")
                
        except Exception as e:
            print(f"Error scanning {pcap_file}: {e}")
    
    # Clean up test files
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)


def test_regex_patterns():
    """Test regex pattern matching"""
    print("Testing regex pattern matching...")
    
    # Create test PCAP with specific content
    test_content = [
        b"GET /admin/login.php HTTP/1.1",
        b"POST /api/user/12345 HTTP/1.1",
        b"Cookie: session=abc123; user=admin",
        b"Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
        b"malware_signature_12345",
        b"suspicious_activity_detected",
        b"password=secret123",
        b"admin=true&role=superuser"
    ]
    
    packets = []
    for content in test_content:
        payload = content + os.urandom(random.randint(50, 200))
        packet = IP(src="192.168.1.1", dst="10.0.0.1") / \
                TCP(sport=random.randint(1024, 65535), dport=80) / \
                Raw(load=payload)
        packets.append(packet)
    
    wrpcap("test_regex.pcap", packets)
    
    # Test regex patterns
    regex_patterns = [
        r"admin.*login",
        r"password=.*",
        r"Bearer [A-Za-z0-9\-._~+/]+=*",
        r"session=[a-zA-Z0-9]+",
        r"malware_signature_\d+",
        r"suspicious_activity"
    ]
    
    scanner = PCAPScanner(regex_patterns, use_regex=True)
    
    try:
        matches = scanner.scan_pcap("test_regex.pcap")
        scanner.print_stats()
        
        if matches:
            print(f"Found {len(matches)} regex matches:")
            for match in matches:
                print(f"  Flow: {match.flow_id}, Pattern: {match.pattern}, Offset: {match.offset}")
        else:
            print("No regex matches found")
            
    except Exception as e:
        print(f"Error with regex scanning: {e}")
    
    # Clean up
    if os.path.exists("test_regex.pcap"):
        os.remove("test_regex.pcap")


def main():
    """Main test function"""
    print("GPU-Accelerated PCAP Scanner Test Suite")
    print("=" * 50)
    
    # Check if GPU is available
    try:
        import cupy as cp
        print("✓ GPU acceleration available")
        gpu_available = True
    except ImportError:
        print("⚠ GPU acceleration not available, some tests will be skipped")
        gpu_available = False
    
    # Run tests
    if gpu_available:
        test_gpu_kernels()
        benchmark_gpu_performance()
    
    test_pcap_scanner()
    test_regex_patterns()
    
    print("\n" + "=" * 50)
    print("All tests completed!")


if __name__ == "__main__":
    main()
