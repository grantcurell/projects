#!/usr/bin/env python3
"""
Create Large Packet Size PCAP

This script creates a synthetic PCAP file with larger average packet sizes
to test if GPU performance improves with fewer, larger packets.
"""

import os
import sys
import time
import random
import multiprocessing
from pathlib import Path
from scapy.all import *
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import Ether
import argparse

def generate_large_packet_flow(flow_id: int, num_packets: int, target_size_mb: float) -> List[Packet]:
    """Generate a single TCP flow with large packet sizes"""
    packets = []
    
    # Source and destination IPs
    src_ip = f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}"
    dst_ip = f"10.0.{random.randint(1, 254)}.{random.randint(1, 254)}"
    
    # Ports
    src_port = random.randint(1024, 65535)
    dst_port = random.choice([80, 443, 8080, 8443])
    
    # Calculate packet size to reach target
    avg_packet_size = int((target_size_mb * 1024 * 1024) / num_packets)
    min_packet_size = max(1000, avg_packet_size - 500)  # Minimum 1KB
    max_packet_size = avg_packet_size + 1000
    
    # TCP sequence numbers
    seq_num = random.randint(1000, 100000)
    ack_num = random.randint(1000, 100000)
    
    # Generate packets
    for i in range(num_packets):
        # Create large payload
        payload_size = random.randint(min_packet_size, max_packet_size)
        
        # Create realistic HTTP-like payload
        if dst_port in [80, 8080]:
            # HTTP payload
            if i == 0:
                payload = f"GET /large_file_{flow_id}.bin HTTP/1.1\r\nHost: example.com\r\nUser-Agent: Mozilla/5.0\r\nAccept: */*\r\n\r\n".encode()
                payload += b"X" * (payload_size - len(payload))
            else:
                payload = b"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: " + str(payload_size).encode() + b"\r\n\r\n"
                payload += b"DATA_CHUNK_" + str(i).encode() + b"_" + b"X" * (payload_size - len(payload) - 20)
        else:
            # Generic large payload
            payload = b"LARGE_DATA_CHUNK_" + str(i).encode() + b"_" + b"X" * (payload_size - 30)
        
        # Ensure payload is correct size
        if len(payload) > payload_size:
            payload = payload[:payload_size]
        elif len(payload) < payload_size:
            payload += b"X" * (payload_size - len(payload))
        
        # Create packet
        packet = Ether() / IP(src=src_ip, dst=dst_ip) / TCP(
            sport=src_port,
            dport=dst_port,
            seq=seq_num,
            ack=ack_num,
            flags="PA"  # PSH + ACK
        ) / Raw(payload)
        
        packets.append(packet)
        
        # Update sequence numbers
        seq_num += len(payload)
        if i % 10 == 0:  # Occasional ACK updates
            ack_num += random.randint(1000, 5000)
    
    return packets

def generate_worker(args):
    """Worker function for multiprocessing"""
    flow_id, num_flows_per_worker, packets_per_flow, target_size_mb = args
    
    all_packets = []
    for flow in range(num_flows_per_worker):
        packets = generate_large_packet_flow(
            flow_id * num_flows_per_worker + flow,
            packets_per_flow,
            target_size_mb
        )
        all_packets.extend(packets)
    
    return all_packets

def create_large_packet_pcap(output_file: str, target_size_mb: float = 500, 
                           num_flows: int = 1000, packets_per_flow: int = 50):
    """Create a PCAP file with large packet sizes"""
    
    print(f"Creating large packet PCAP: {output_file}")
    print(f"Target size: {target_size_mb} MB")
    print(f"Flows: {num_flows}")
    print(f"Packets per flow: {packets_per_flow}")
    
    # Calculate target size per flow
    target_size_per_flow = target_size_mb / num_flows
    
    # Use multiprocessing
    num_workers = multiprocessing.cpu_count()
    flows_per_worker = num_flows // num_workers
    
    print(f"Using {num_workers} workers, {flows_per_worker} flows per worker")
    
    # Prepare arguments for workers
    worker_args = [
        (i, flows_per_worker, packets_per_flow, target_size_per_flow)
        for i in range(num_workers)
    ]
    
    # Generate packets in parallel
    print("Generating packets...")
    start_time = time.time()
    
    with multiprocessing.Pool(num_workers) as pool:
        results = pool.map(generate_worker, worker_args)
    
    # Flatten results
    all_packets = []
    for packets in results:
        all_packets.extend(packets)
    
    generation_time = time.time() - start_time
    print(f"Generated {len(all_packets):,} packets in {generation_time:.2f}s")
    
    # Add timestamps
    print("Adding timestamps...")
    base_time = time.time()
    for i, packet in enumerate(all_packets):
        packet.time = base_time + (i * 0.001)  # 1ms between packets
    
    # Write to file
    print(f"Writing to {output_file}...")
    start_time = time.time()
    
    wrpcap(output_file, all_packets)
    
    write_time = time.time() - start_time
    file_size = Path(output_file).stat().st_size / 1024 / 1024
    
    print(f"✅ Created {output_file}")
    print(f"   Size: {file_size:.1f} MB")
    print(f"   Packets: {len(all_packets):,}")
    print(f"   Avg packet size: {file_size * 1024 * 1024 / len(all_packets):.0f} bytes")
    print(f"   Generation time: {generation_time:.2f}s")
    print(f"   Write time: {write_time:.2f}s")

def main():
    parser = argparse.ArgumentParser(description="Create PCAP with large packet sizes")
    parser.add_argument("--output", "-o", default="PCAP Files/synthetic_large_packets.pcapng",
                       help="Output PCAP file")
    parser.add_argument("--size", "-s", type=float, default=500,
                       help="Target file size in MB")
    parser.add_argument("--flows", "-f", type=int, default=1000,
                       help="Number of flows")
    parser.add_argument("--packets-per-flow", "-p", type=int, default=50,
                       help="Packets per flow")
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    create_large_packet_pcap(
        args.output,
        args.size,
        args.flows,
        args.packets_per_flow
    )

if __name__ == "__main__":
    main()

