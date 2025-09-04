#!/usr/bin/env python3
"""
Large PCAP File Downloader for Performance Testing

This script downloads large PCAP files from various sources for comprehensive
performance testing of our GPU-accelerated PCAP scanner.
"""

import os
import sys
import requests
import argparse
from pathlib import Path
from tqdm import tqdm
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Large PCAP file sources
PCAP_SOURCES = {
    "caida": {
        "name": "CAIDA Anonymized Internet Traces",
        "url": "https://data.caida.org/datasets/passive-2016/equinix-chicago/20160121-130000.UTC/",
        "files": [
            "20160121-130000.UTC.anon.pcap.gz",
            "20160121-130100.UTC.anon.pcap.gz",
            "20160121-130200.UTC.anon.pcap.gz"
        ],
        "description": "Real internet traffic traces (large files, 1-10GB each)"
    },
    "wireshark_samples": {
        "name": "Wireshark Sample Captures",
        "url": "https://wiki.wireshark.org/SampleCaptures",
        "files": [
            "http.cap",
            "ftp.pcap",
            "dns.cap",
            "tcp.pcap"
        ],
        "description": "Small to medium sample captures for testing"
    },
    "netresec": {
        "name": "Netresec Sample Captures",
        "url": "https://www.netresec.com/?page=PCAP4SICS",
        "files": [
            "4SICS-GeekLounge-151020.pcap",
            "4SICS-GeekLounge-151021.pcap"
        ],
        "description": "Security-focused captures with known threats"
    },
    "synthetic": {
        "name": "Generate Synthetic PCAP",
        "description": "Generate large synthetic PCAP files for testing"
    }
}


def download_file(url: str, filepath: str, chunk_size: int = 8192) -> bool:
    """Download a file with progress bar"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(filepath, 'wb') as f:
            with tqdm(total=total_size, unit='B', unit_scale=True, 
                     desc=f"Downloading {os.path.basename(filepath)}") as pbar:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
        
        return True
        
    except Exception as e:
        print(f"{Fore.RED}❌ Download failed: {e}{Style.RESET_ALL}")
        return False


def generate_synthetic_pcap(size_mb: int, filename: str = None) -> str:
    """Generate a synthetic PCAP file for testing"""
    if not filename:
        filename = f"synthetic_{size_mb}mb.pcapng"
    
    filepath = f"PCAP Files/{filename}"
    
    if os.path.exists(filepath):
        print(f"{Fore.GREEN}✓ Synthetic PCAP already exists: {filepath}{Style.RESET_ALL}")
        return filepath
    
    print(f"{Fore.YELLOW}🔧 Generating synthetic PCAP: {size_mb}MB{Style.RESET_ALL}")
    
    try:
        from scapy.all import wrpcap, IP, TCP, UDP, Raw
        import time
        import random
        
        # Create directory if it doesn't exist
        os.makedirs("PCAP Files", exist_ok=True)
        
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
            b"ZIP archive",
            b"SQL injection",
            b"XSS attack",
            b"buffer overflow",
            b"rootkit detection",
            b"phishing attempt"
        ]
        
        # Calculate number of packets needed
        avg_packet_size = 1500  # bytes
        num_packets = (size_mb * 1024 * 1024) // avg_packet_size
        
        for i in tqdm(range(num_packets), desc="Generating packets"):
            # Create packet with random pattern
            pattern = random.choice(patterns)
            payload = pattern + b" " + os.urandom(random.randint(50, 200))
            
            # Randomize source/destination
            src_ip = f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}"
            dst_ip = f"10.0.{random.randint(1, 254)}.{random.randint(1, 254)}"
            
            packet = IP(src=src_ip, dst=dst_ip) / \
                     TCP(sport=random.randint(1000, 65535), 
                         dport=random.choice([80, 443, 22, 21, 25, 53])) / \
                     Raw(load=payload)
            
            packet.time = base_time + i * 0.001
            packets.append(packet)
        
        wrpcap(filepath, packets)
        print(f"{Fore.GREEN}✓ Generated: {filepath} ({len(packets)} packets, {os.path.getsize(filepath)/1024/1024:.1f}MB){Style.RESET_ALL}")
        return filepath
        
    except Exception as e:
        print(f"{Fore.RED}❌ Generation failed: {e}{Style.RESET_ALL}")
        return None


def list_available_sources():
    """List available PCAP sources"""
    print(f"{Fore.CYAN}📚 Available PCAP Sources:{Style.RESET_ALL}")
    print()
    
    for key, source in PCAP_SOURCES.items():
        print(f"{Fore.YELLOW}{key.upper()}:{Style.RESET_ALL}")
        print(f"  Name: {source['name']}")
        print(f"  Description: {source['description']}")
        if 'url' in source:
            print(f"  URL: {source['url']}")
        if 'files' in source:
            print(f"  Files: {', '.join(source['files'])}")
        print()


def download_from_source(source_key: str, target_dir: str = "PCAP Files"):
    """Download PCAP files from a specific source"""
    if source_key not in PCAP_SOURCES:
        print(f"{Fore.RED}❌ Unknown source: {source_key}{Style.RESET_ALL}")
        return False
    
    source = PCAP_SOURCES[source_key]
    
    if source_key == "synthetic":
        # Generate synthetic files
        sizes = [10, 50, 100, 500]  # MB
        for size in sizes:
            generate_synthetic_pcap(size)
        return True
    
    # Create target directory
    os.makedirs(target_dir, exist_ok=True)
    
    print(f"{Fore.CYAN}📥 Downloading from {source['name']}{Style.RESET_ALL}")
    
    if 'files' not in source:
        print(f"{Fore.YELLOW}💡 Manual download required for {source['name']}{Style.RESET_ALL}")
        print(f"   Visit: {source['url']}")
        return False
    
    success_count = 0
    for filename in source['files']:
        url = f"{source['url']}/{filename}"
        filepath = os.path.join(target_dir, filename)
        
        print(f"\n{Fore.BLUE}Downloading: {filename}{Style.RESET_ALL}")
        if download_file(url, filepath):
            success_count += 1
            print(f"{Fore.GREEN}✓ Successfully downloaded: {filepath}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ Failed to download: {filename}{Style.RESET_ALL}")
    
    print(f"\n{Fore.GREEN}🎉 Download completed: {success_count}/{len(source['files'])} files{Style.RESET_ALL}")
    return success_count > 0


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Download Large PCAP Files for Performance Testing")
    parser.add_argument("--list", action="store_true", help="List available sources")
    parser.add_argument("--source", choices=list(PCAP_SOURCES.keys()), 
                       help="Source to download from")
    parser.add_argument("--synthetic", type=int, nargs="+", 
                       help="Generate synthetic PCAP files with specified sizes (MB)")
    parser.add_argument("--output-dir", default="PCAP Files",
                       help="Output directory for downloaded files")
    
    args = parser.parse_args()
    
    if args.list:
        list_available_sources()
        return
    
    if args.synthetic:
        print(f"{Fore.CYAN}🔧 Generating synthetic PCAP files...{Style.RESET_ALL}")
        for size in args.synthetic:
            generate_synthetic_pcap(size)
        return
    
    if args.source:
        download_from_source(args.source, args.output_dir)
        return
    
    # Default: show help
    parser.print_help()
    print(f"\n{Fore.YELLOW}💡 Quick start examples:{Style.RESET_ALL}")
    print(f"  python {sys.argv[0]} --list")
    print(f"  python {sys.argv[0]} --synthetic 100 500")
    print(f"  python {sys.argv[0]} --source wireshark_samples")


if __name__ == "__main__":
    main()
