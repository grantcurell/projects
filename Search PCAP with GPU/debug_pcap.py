#!/usr/bin/env python3
"""
Debug PCAP file contents and performance issues
"""

from scapy.all import rdpcap
import time

def debug_pcap_file(filepath):
    print(f"Debugging PCAP file: {filepath}")
    
    # Read PCAP file
    start_time = time.time()
    packets = rdpcap(filepath)
    read_time = time.time() - start_time
    
    print(f"Total packets: {len(packets)}")
    print(f"Read time: {read_time:.2f}s")
    
    # Check payloads
    payload_count = 0
    total_payload_bytes = 0
    
    for i, packet in enumerate(packets[:20]):  # Check first 20 packets
        if packet.haslayer('Raw'):
            payload = bytes(packet['Raw'])
            payload_count += 1
            total_payload_bytes += len(payload)
            print(f"Packet {i}: {len(payload)} bytes payload")
            if i < 5:  # Show first 5 payloads
                print(f"  Sample: {payload[:50]}...")
        else:
            print(f"Packet {i}: No Raw layer")
    
    print(f"\nFirst 20 packets with payload: {payload_count}/20")
    print(f"Total payload bytes in first 20: {total_payload_bytes}")
    
    # Check for our test patterns
    patterns = [b"HTTP", b"GET", b"POST"]
    pattern_found = {p: 0 for p in patterns}
    
    for packet in packets[:100]:  # Check first 100 packets
        if packet.haslayer('Raw'):
            payload = bytes(packet['Raw'])
            for pattern in patterns:
                if pattern in payload:
                    pattern_found[pattern] += 1
    
    print(f"\nPattern matches in first 100 packets:")
    for pattern, count in pattern_found.items():
        print(f"  {pattern}: {count} matches")

if __name__ == "__main__":
    debug_pcap_file("PCAP Files/synthetic_100mb.pcapng")
