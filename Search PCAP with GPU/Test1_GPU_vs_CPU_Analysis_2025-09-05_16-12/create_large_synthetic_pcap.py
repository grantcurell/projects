#!/usr/bin/env python3
"""
Multi-threaded Synthetic PCAP Generator

A high-performance tool for generating realistic PCAP files with diverse network traffic
patterns. Uses multi-threading to leverage all available CPU cores for fast generation.

Features:
- Multi-threaded packet generation using all CPU cores
- Realistic network traffic patterns (HTTP, HTTPS, SSH, FTP, DNS, etc.)
- Configurable file sizes and output locations
- Diverse payload patterns for comprehensive testing
- Chronologically ordered packets
- Progress tracking and performance metrics

Usage:
    python create_large_synthetic_pcap.py --size 500 --output large_test.pcapng
    python create_large_synthetic_pcap.py --size 1000 --patterns web,security
    python create_large_synthetic_pcap.py --help
"""

import argparse
import os
import sys
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import cpu_count
from pathlib import Path
import math
from typing import List, Tuple, Dict

from scapy.all import wrpcap, IP, TCP, Raw
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)


class PatternLibrary:
    """Library of realistic network traffic patterns for PCAP generation"""
    
    def __init__(self):
        self.patterns = self._initialize_patterns()
    
    def _initialize_patterns(self) -> Dict[str, List[bytes]]:
        """Initialize all available pattern categories"""
        return {
            'web': [
                b"GET /index.html HTTP/1.1\r\nHost: example.com\r\nUser-Agent: Mozilla/5.0\r\n\r\n",
                b"POST /login HTTP/1.1\r\nHost: example.com\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 25\r\n\r\nusername=admin&password=secret",
                b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: 1024\r\n\r\n<html><body>Welcome to our site</body></html>",
                b"GET /api/users HTTP/1.1\r\nHost: api.example.com\r\nAuthorization: Bearer token123\r\n\r\n",
                b"POST /upload HTTP/1.1\r\nHost: files.example.com\r\nContent-Type: multipart/form-data\r\n\r\n--boundary\r\nContent-Disposition: form-data; name=\"file\"; filename=\"document.pdf\"\r\n\r\nPDF content here...",
                b"GET /css/style.css HTTP/1.1\r\nHost: static.example.com\r\nAccept: text/css\r\n\r\n",
                b"GET /js/app.js HTTP/1.1\r\nHost: static.example.com\r\nAccept: application/javascript\r\n\r\n",
                b"GET /images/logo.png HTTP/1.1\r\nHost: cdn.example.com\r\nAccept: image/png\r\n\r\n",
            ],
            
            'security': [
                b"password=admin123&login=user",
                b"session_id=abc123def456",
                b"auth_token=xyz789",
                b"admin_login=true",
                b"user_authentication=success",
                b"security_check=passed",
                b"malware_detected=false",
                b"virus_scan=clean",
                b"trojan_horse=not_found",
                b"backdoor_access=denied",
                b"exploit_found=none",
                b"firewall_rule=allow",
                b"intrusion_detection=alert",
                b"vulnerability_scan=complete",
            ],
            
            'files': [
                b"%PDF-1.4 document content here...",
                b"PK\x03\x04 ZIP archive content...",
                b"MZ executable file content...",
                b"\xff\xd8\xff JPEG image data...",
                b"\x89PNG\r\n\x1a\n PNG image data...",
                b"GIF87a animated image data...",
                b"ID3 MP3 audio data...",
                b"ftypisom MP4 video data...",
                b"DOCX Microsoft Word document...",
                b"XLSX Microsoft Excel spreadsheet...",
                b"PPTX Microsoft PowerPoint presentation...",
            ],
            
            'ssh': [
                b"SSH-2.0-OpenSSH_8.0",
                b"SSH-2.0-OpenSSH_7.4",
                b"SSH-2.0-OpenSSH_7.9",
                b"password authentication",
                b"publickey authentication",
                b"keyboard-interactive authentication",
                b"SSH connection established",
                b"remote command execution",
                b"file transfer via SCP",
                b"tunnel establishment",
            ],
            
            'ftp': [
                b"USER anonymous",
                b"PASS guest",
                b"LIST",
                b"RETR file.txt",
                b"STOR upload.txt",
                b"QUIT",
                b"PASV",
                b"PORT 192,168,1,100,20,4",
                b"PWD",
                b"CWD /uploads",
                b"MKD new_directory",
                b"RMD old_directory",
                b"DELE file_to_delete",
            ],
            
            'dns': [
                b"www.google.com",
                b"www.facebook.com",
                b"www.amazon.com",
                b"www.microsoft.com",
                b"mail.example.com",
                b"ftp.example.com",
                b"api.example.com",
                b"cdn.example.com",
                b"static.example.com",
                b"admin.example.com",
            ],
            
            'email': [
                b"HELO mail.example.com",
                b"MAIL FROM: sender@example.com",
                b"RCPT TO: recipient@example.com",
                b"DATA",
                b"Subject: Test Email",
                b"From: sender@example.com",
                b"To: recipient@example.com",
                b"Date: Mon, 01 Jan 2024 12:00:00 +0000",
                b"Message-ID: <unique-id@example.com>",
                b"QUIT",
            ],
            
            'database': [
                b"SELECT * FROM users WHERE id = 1",
                b"INSERT INTO logs (message) VALUES ('test')",
                b"UPDATE users SET last_login = NOW()",
                b"DELETE FROM temp_data WHERE created < DATE_SUB(NOW(), INTERVAL 1 DAY)",
                b"CREATE TABLE new_table (id INT PRIMARY KEY)",
                b"DROP TABLE old_table",
                b"GRANT SELECT ON database.* TO 'user'@'localhost'",
                b"REVOKE INSERT ON database.* FROM 'user'@'localhost'",
            ]
        }
    
    def get_patterns(self, categories: List[str]) -> List[bytes]:
        """Get patterns from specified categories"""
        if not categories:
            # Return all patterns if no categories specified
            all_patterns = []
            for category_patterns in self.patterns.values():
                all_patterns.extend(category_patterns)
            return all_patterns
        
        patterns = []
        for category in categories:
            if category in self.patterns:
                patterns.extend(self.patterns[category])
            else:
                print(f"{Fore.YELLOW}⚠️  Warning: Unknown pattern category '{category}'{Style.RESET_ALL}")
        
        return patterns
    
    def list_categories(self) -> List[str]:
        """List all available pattern categories"""
        return list(self.patterns.keys())


class FlowGenerator:
    """Generates realistic network flows for PCAP files"""
    
    def __init__(self):
        self.flows = [
            ("192.168.1.100", "10.0.0.1", 80),   # HTTP server
            ("192.168.1.101", "10.0.0.2", 443),  # HTTPS server  
            ("192.168.1.102", "10.0.0.3", 22),   # SSH server
            ("192.168.1.103", "10.0.0.4", 25),   # SMTP server
            ("192.168.1.104", "10.0.0.5", 21),   # FTP server
            ("192.168.1.105", "10.0.0.6", 53),   # DNS server
            ("192.168.1.106", "10.0.0.7", 8080), # HTTP alt
            ("192.168.1.107", "10.0.0.8", 8443), # HTTPS alt
            ("192.168.1.108", "10.0.0.9", 3306), # MySQL
            ("192.168.1.109", "10.0.0.10", 5432), # PostgreSQL
            ("192.168.1.110", "10.0.0.11", 1433), # SQL Server
            ("192.168.1.111", "10.0.0.12", 1521), # Oracle
        ]
    
    def get_random_flow(self) -> Tuple[str, str, int]:
        """Get a random network flow"""
        return random.choice(self.flows)


def generate_packet_batch(batch_id: int, batch_size: int, patterns: List[bytes], 
                         flow_generator: FlowGenerator, base_time: float, 
                         start_packet_id: int) -> Tuple[int, List]:
    """
    Generate a batch of packets in parallel
    
    Args:
        batch_id: Unique identifier for this batch
        batch_size: Number of packets to generate in this batch
        patterns: List of payload patterns to use
        flow_generator: Flow generator instance
        base_time: Base timestamp for packet timing
        start_packet_id: Starting packet ID for this batch
    
    Returns:
        Tuple of (batch_id, list_of_packets)
    """
    packets = []
    
    for i in range(batch_size):
        # Select random flow
        src_ip, dst_ip, dst_port = flow_generator.get_random_flow()
        src_port = random.randint(50000, 60000)
        
        # Choose a pattern
        pattern = random.choice(patterns)
        
        # Split pattern into packets to simulate real TCP behavior
        packet_size = random.randint(100, 1500)
        if len(pattern) > packet_size:
            chunks = [pattern[i:i+packet_size] for i in range(0, len(pattern), packet_size)]
        else:
            chunks = [pattern]
        
        seq_num = random.randint(1000, 10000)
        
        for chunk in chunks:
            packet = IP(src=src_ip, dst=dst_ip) / \
                     TCP(sport=src_port, dport=dst_port, seq=seq_num) / \
                     Raw(load=chunk)
            
            packet.time = base_time + (start_packet_id + i) * 0.001
            packets.append(packet)
            
            seq_num += len(chunk)
    
    return batch_id, packets


class SyntheticPCAPGenerator:
    """Main class for generating synthetic PCAP files"""
    
    def __init__(self, size_mb: int, output_file: str, pattern_categories: List[str], 
                 num_threads: int = None):
        """
        Initialize the PCAP generator
        
        Args:
            size_mb: Target file size in MB
            output_file: Output file path
            pattern_categories: List of pattern categories to use
            num_threads: Number of threads to use (default: all CPU cores)
        """
        self.size_mb = size_mb
        self.output_file = output_file
        self.pattern_categories = pattern_categories
        self.num_threads = num_threads or cpu_count()
        
        self.pattern_library = PatternLibrary()
        self.flow_generator = FlowGenerator()
        
        # Get patterns for specified categories
        self.patterns = self.pattern_library.get_patterns(pattern_categories)
        
        if not self.patterns:
            raise ValueError("No patterns available for the specified categories")
    
    def generate(self) -> str:
        """
        Generate the synthetic PCAP file
        
        Returns:
            Path to the generated file
        """
        print(f"{Fore.CYAN}🔧 Creating {self.size_mb}MB synthetic PCAP file{Style.RESET_ALL}")
        print(f"   Output: {self.output_file}")
        print(f"   Patterns: {', '.join(self.pattern_categories) if self.pattern_categories else 'all'}")
        print(f"   Threads: {self.num_threads}")
        print("=" * 60)
        
        base_time = time.time()
        target_bytes = self.size_mb * 1024 * 1024
        estimated_packets = target_bytes // 1000  # Rough estimate: 1KB per packet
        
        # Calculate batch size for parallel processing
        batch_size = max(1000, estimated_packets // (self.num_threads * 10))
        num_batches = math.ceil(estimated_packets / batch_size)
        
        print(f"Target size: {self.size_mb} MB ({target_bytes:,} bytes)")
        print(f"Estimated packets: {estimated_packets:,}")
        print(f"Batch size: {batch_size:,} packets")
        print(f"Number of batches: {num_batches}")
        print(f"Generating packets in parallel...")
        
        all_packets = []
        completed_batches = 0
        
        # Use ThreadPoolExecutor for parallel packet generation
        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            # Submit all batch generation tasks
            futures = []
            for batch_id in range(num_batches):
                start_packet_id = batch_id * batch_size
                future = executor.submit(
                    generate_packet_batch, 
                    batch_id, 
                    batch_size, 
                    self.patterns, 
                    self.flow_generator, 
                    base_time, 
                    start_packet_id
                )
                futures.append(future)
            
            # Collect results as they complete
            for future in as_completed(futures):
                batch_id, packets = future.result()
                all_packets.extend(packets)
                completed_batches += 1
                
                # Progress update
                progress = (completed_batches / num_batches) * 100
                print(f"   Completed batch {completed_batches}/{num_batches} ({progress:.1f}%) - {len(all_packets):,} packets")
        
        # Sort packets by timestamp to maintain chronological order
        print(f"\n📊 Sorting packets by timestamp...")
        all_packets.sort(key=lambda p: p.time)
        
        # Ensure output directory exists
        output_path = Path(self.output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save the PCAP file
        print(f"\n💾 Writing PCAP file...")
        write_start = time.time()
        wrpcap(str(output_path), all_packets)
        write_time = time.time() - write_start
        
        # Get final file size
        final_size = output_path.stat().st_size
        final_size_mb = final_size / 1024 / 1024
        
        print(f"\n{Fore.GREEN}✅ PCAP file created successfully!{Style.RESET_ALL}")
        print(f"   File: {output_path}")
        print(f"   Packets: {len(all_packets):,}")
        print(f"   File size: {final_size_mb:.1f} MB")
        print(f"   Write time: {write_time:.2f}s")
        print(f"   Average packet size: {final_size / len(all_packets):.0f} bytes")
        
        return str(output_path)


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Multi-threaded Synthetic PCAP Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate 500MB PCAP with all patterns
  python create_large_synthetic_pcap.py --size 500
  
  # Generate 1GB PCAP with only web and security patterns
  python create_large_synthetic_pcap.py --size 1000 --patterns web,security
  
  # Generate 2GB PCAP with custom output location
  python create_large_synthetic_pcap.py --size 2000 --output /path/to/large_test.pcapng
  
  # List available pattern categories
  python create_large_synthetic_pcap.py --list-patterns
        """
    )
    
    parser.add_argument(
        '--size', '-s',
        type=int,
        default=1000,
        help='Target file size in MB (default: 1000)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='PCAP Files/synthetic_{size}mb.pcapng',
        help='Output file path (default: PCAP Files/synthetic_{size}mb.pcapng)'
    )
    
    parser.add_argument(
        '--patterns', '-p',
        type=str,
        default='',
        help='Comma-separated list of pattern categories (web,security,files,ssh,ftp,dns,email,database). Default: all patterns'
    )
    
    parser.add_argument(
        '--threads', '-t',
        type=int,
        default=None,
        help='Number of threads to use (default: all CPU cores)'
    )
    
    parser.add_argument(
        '--list-patterns',
        action='store_true',
        help='List available pattern categories and exit'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    return parser.parse_args()


def main():
    """Main function"""
    args = parse_arguments()
    
    # Initialize colorama
    init(autoreset=True)
    
    print(f"{Fore.CYAN}🔧 Multi-threaded Synthetic PCAP Generator{Style.RESET_ALL}")
    print("=" * 60)
    
    try:
        # Handle list patterns request
        if args.list_patterns:
            pattern_lib = PatternLibrary()
            categories = pattern_lib.list_categories()
            print(f"{Fore.YELLOW}Available pattern categories:{Style.RESET_ALL}")
            for category in categories:
                print(f"  - {category}")
            return 0
        
        # Process pattern categories
        pattern_categories = []
        if args.patterns:
            pattern_categories = [cat.strip() for cat in args.patterns.split(',')]
        
        # Process output file path
        output_file = args.output
        if '{size}' in output_file:
            output_file = output_file.format(size=args.size)
        
        # Create generator and generate PCAP
        generator = SyntheticPCAPGenerator(
            size_mb=args.size,
            output_file=output_file,
            pattern_categories=pattern_categories,
            num_threads=args.threads
        )
        
        output_path = generator.generate()
        
        print(f"\n{Fore.GREEN}🎉 Success! PCAP file ready for testing.{Style.RESET_ALL}")
        print(f"   Use this file to test GPU performance scaling with larger datasets.")
        
        return 0
        
    except Exception as e:
        print(f"\n{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())