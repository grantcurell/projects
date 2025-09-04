#!/usr/bin/env python3
"""
Create a proper TCP PCAP file with realistic flows for testing
"""

from scapy.all import wrpcap, IP, TCP, Raw
import time
import random

def create_realistic_tcp_pcap():
    print("🔧 Creating realistic TCP PCAP file...")
    
    packets = []
    base_time = time.time()
    
    # Create realistic TCP flows
    flows = [
        ("192.168.1.100", "10.0.0.1", 80),   # HTTP server
        ("192.168.1.101", "10.0.0.2", 443),  # HTTPS server  
        ("192.168.1.102", "10.0.0.3", 22),   # SSH server
        ("192.168.1.103", "10.0.0.4", 25),   # SMTP server
    ]
    
    # HTTP patterns that will form proper TCP streams
    http_patterns = [
        b"GET /index.html HTTP/1.1\r\nHost: example.com\r\nUser-Agent: Mozilla/5.0\r\n\r\n",
        b"POST /login HTTP/1.1\r\nHost: example.com\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 25\r\n\r\nusername=admin&password=secret",
        b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: 1024\r\n\r\n<html><body>Welcome to our site</body></html>",
        b"GET /api/users HTTP/1.1\r\nHost: api.example.com\r\nAuthorization: Bearer token123\r\n\r\n",
        b"POST /upload HTTP/1.1\r\nHost: files.example.com\r\nContent-Type: multipart/form-data\r\n\r\n--boundary\r\nContent-Disposition: form-data; name=\"file\"; filename=\"document.pdf\"\r\n\r\nPDF content here...",
    ]
    
    packet_count = 0
    target_packets = 10000  # 10K packets for ~50MB file
    
    for flow_idx, (src_ip, dst_ip, dst_port) in enumerate(flows):
        src_port = 50000 + flow_idx * 1000
        
        # Create a TCP flow with multiple packets
        seq_num = random.randint(1000, 10000)
        
        for packet_in_flow in range(target_packets // len(flows)):
            # Choose a pattern
            pattern = random.choice(http_patterns)
            
            # Split pattern into multiple packets to simulate real TCP behavior
            packet_size = random.randint(100, 1500)
            if len(pattern) > packet_size:
                # Split large patterns across multiple packets
                chunks = [pattern[i:i+packet_size] for i in range(0, len(pattern), packet_size)]
            else:
                chunks = [pattern]
            
            for chunk in chunks:
                packet = IP(src=src_ip, dst=dst_ip) / \
                         TCP(sport=src_port, dport=dst_port, seq=seq_num) / \
                         Raw(load=chunk)
                
                packet.time = base_time + packet_count * 0.001
                packets.append(packet)
                
                seq_num += len(chunk)
                packet_count += 1
                
                if packet_count >= target_packets:
                    break
            
            if packet_count >= target_packets:
                break
        
        if packet_count >= target_packets:
            break
    
    # Save the PCAP file
    filename = "PCAP Files/realistic_tcp_flows.pcapng"
    wrpcap(filename, packets)
    
    print(f"✓ Created: {filename}")
    print(f"  Packets: {len(packets)}")
    print(f"  File size: {os.path.getsize(filename)/1024/1024:.1f} MB")
    
    return filename

if __name__ == "__main__":
    create_realistic_tcp_pcap()
