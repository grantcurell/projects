#!/usr/bin/env python3
"""
Direct GPU performance test bypassing TCP reassembly
"""

import time
import os
from scapy.all import rdpcap
from gpu_kernels import AdvancedGPUKernels

def test_direct_gpu_performance():
    print("🚀 Direct GPU Performance Test")
    print("=" * 50)
    
    # Load PCAP file
    pcap_file = "PCAP Files/synthetic_100mb.pcapng"
    print(f"Loading: {pcap_file}")
    
    start_time = time.time()
    packets = rdpcap(pcap_file)
    load_time = time.time() - start_time
    
    print(f"Loaded {len(packets)} packets in {load_time:.2f}s")
    
    # Extract all payloads directly (bypass TCP reassembly)
    payloads = []
    total_bytes = 0
    
    extract_start = time.time()
    for packet in packets:
        if packet.haslayer('Raw'):
            payload = bytes(packet['Raw'])
            payloads.append(payload)
            total_bytes += len(payload)
    extract_time = time.time() - extract_start
    
    print(f"Extracted {len(payloads)} payloads ({total_bytes:,} bytes) in {extract_time:.2f}s")
    print(f"Average payload size: {total_bytes/len(payloads):.1f} bytes")
    
    # Test GPU kernels directly
    patterns = [b"HTTP", b"GET", b"POST"]
    kernels = AdvancedGPUKernels()
    
    print(f"\n🔍 Testing GPU kernels with {len(patterns)} patterns...")
    
    # Test with different batch sizes
    batch_sizes = [1, 10, 100, 1000]
    
    for batch_size in batch_sizes:
        print(f"\nBatch size: {batch_size}")
        
        # Process in batches
        total_matches = 0
        gpu_start = time.time()
        
        for i in range(0, len(payloads), batch_size):
            batch = payloads[i:i+batch_size]
            
            for payload in batch:
                # Use vectorized search for multiple patterns
                matches = kernels.vectorized_multi_search(payload, patterns)
                total_matches += sum(len(m) for m in matches)
        
        gpu_time = time.time() - gpu_start
        
        # Calculate metrics
        throughput_mbps = (total_bytes / 1024 / 1024) / gpu_time if gpu_time > 0 else 0
        payloads_per_sec = len(payloads) / gpu_time if gpu_time > 0 else 0
        
        print(f"  GPU Time: {gpu_time:.2f}s")
        print(f"  Throughput: {throughput_mbps:.2f} MB/s")
        print(f"  Payloads/sec: {payloads_per_sec:,.0f}")
        print(f"  Matches found: {total_matches}")
    
    # Test single large payload
    print(f"\n🔍 Testing with single large payload...")
    
    # Concatenate all payloads into one large payload
    large_payload = b''.join(payloads[:1000])  # Use first 1000 payloads
    print(f"Large payload size: {len(large_payload):,} bytes ({len(large_payload)/1024/1024:.2f} MB)")
    
    gpu_start = time.time()
    matches = kernels.vectorized_multi_search(large_payload, patterns)
    gpu_time = time.time() - gpu_start
    
    total_matches = sum(len(m) for m in matches)
    throughput_mbps = (len(large_payload) / 1024 / 1024) / gpu_time if gpu_time > 0 else 0
    
    print(f"  GPU Time: {gpu_time:.2f}s")
    print(f"  Throughput: {throughput_mbps:.2f} MB/s")
    print(f"  Matches found: {total_matches}")
    
    print(f"\n🎯 Summary:")
    print(f"Total data processed: {total_bytes:,} bytes ({total_bytes/1024/1024:.2f} MB)")
    print(f"Total payloads: {len(payloads):,}")
    print(f"Pattern matches: {total_matches}")

if __name__ == "__main__":
    test_direct_gpu_performance()
