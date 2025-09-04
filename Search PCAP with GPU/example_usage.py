#!/usr/bin/env python3
"""
Example usage of the GPU-Accelerated PCAP Scanner

This script demonstrates how to use the scanner with different types of patterns
and provides examples for common use cases.
"""

import os
import sys
from pathlib import Path

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pcap_gpu_scanner import PCAPScanner


def example_basic_scanning():
    """Example of basic pattern scanning"""
    print("=== Basic Pattern Scanning Example ===")
    
    # Example patterns for web traffic
    patterns = [
        "HTTP/1.1",
        "GET",
        "POST",
        "User-Agent",
        "Cookie",
        "admin",
        "password"
    ]
    
    print(f"Patterns to search for: {patterns}")
    
    # Initialize scanner
    scanner = PCAPScanner(patterns, use_regex=False)
    
    # Note: You would need an actual PCAP file here
    # pcap_file = "your_capture.pcap"
    # matches = scanner.scan_pcap(pcap_file)
    
    print("Scanner initialized successfully!")
    print("To use: scanner.scan_pcap('your_file.pcap')")


def example_regex_scanning():
    """Example of regex pattern scanning"""
    print("\n=== Regex Pattern Scanning Example ===")
    
    # Example regex patterns
    regex_patterns = [
        r"admin.*login",
        r"password=.*",
        r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}",  # IP addresses
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",  # Email addresses
        r"Bearer [A-Za-z0-9\-._~+/]+=*"  # JWT tokens
    ]
    
    print(f"Regex patterns to search for: {regex_patterns}")
    
    # Initialize scanner with regex
    scanner = PCAPScanner(regex_patterns, use_regex=True)
    
    print("Regex scanner initialized successfully!")
    print("To use: scanner.scan_pcap('your_file.pcap')")


def example_security_scanning():
    """Example of security-focused scanning"""
    print("\n=== Security Scanning Example ===")
    
    # Security-related patterns
    security_patterns = [
        # Malware indicators
        "malware",
        "virus",
        "trojan",
        "backdoor",
        "keylogger",
        "ransomware",
        
        # Network scanning
        "nmap",
        "port scan",
        "reconnaissance",
        
        # Authentication bypass attempts
        "admin",
        "root",
        "password",
        "login",
        
        # Suspicious commands
        "cmd",
        "exec",
        "system",
        "shell"
    ]
    
    print(f"Security patterns to search for: {security_patterns}")
    
    # Initialize scanner
    scanner = PCAPScanner(security_patterns, use_regex=False)
    
    print("Security scanner initialized successfully!")
    print("To use: scanner.scan_pcap('your_file.pcap')")


def example_protocol_scanning():
    """Example of protocol-specific scanning"""
    print("\n=== Protocol Scanning Example ===")
    
    # Protocol-specific patterns
    protocol_patterns = {
        "HTTP/HTTPS": [
            "HTTP/1.1",
            "HTTPS",
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "Host:",
            "User-Agent:",
            "Accept:",
            "Content-Type:"
        ],
        "FTP": [
            "FTP",
            "USER",
            "PASS",
            "RETR",
            "STOR",
            "LIST"
        ],
        "SMTP": [
            "SMTP",
            "MAIL FROM:",
            "RCPT TO:",
            "DATA",
            "QUIT"
        ],
        "SSH": [
            "SSH",
            "SSH-2.0",
            "key exchange",
            "authentication"
        ]
    }
    
    for protocol, patterns in protocol_patterns.items():
        print(f"\n{protocol} patterns:")
        for pattern in patterns:
            print(f"  - {pattern}")
    
    # You can scan for specific protocols
    http_patterns = protocol_patterns["HTTP/HTTPS"]
    scanner = PCAPScanner(http_patterns, use_regex=False)
    
    print("\nHTTP scanner initialized successfully!")


def example_performance_monitoring():
    """Example of performance monitoring"""
    print("\n=== Performance Monitoring Example ===")
    
    patterns = ["HTTP", "GET", "POST", "admin", "password"]
    scanner = PCAPScanner(patterns, use_regex=False)
    
    print("Performance monitoring enabled!")
    print("After scanning, call scanner.print_stats() to see:")
    print("  - Total packets processed")
    print("  - Total bytes scanned")
    print("  - TCP reassembly time")
    print("  - GPU processing time")
    print("  - Total processing time")
    print("  - Throughput (MB/s)")
    print("  - Memory usage")
    print("  - Pattern matches found")


def example_pattern_file_usage():
    """Example of using pattern files"""
    print("\n=== Pattern File Usage Example ===")
    
    # Check if pattern files exist
    if os.path.exists("example_patterns.txt"):
        print("Found example_patterns.txt")
        with open("example_patterns.txt", "r") as f:
            patterns = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        
        print(f"Loaded {len(patterns)} patterns from file")
        print("First 10 patterns:")
        for pattern in patterns[:10]:
            print(f"  - {pattern}")
    
    if os.path.exists("regex_patterns.txt"):
        print("\nFound regex_patterns.txt")
        with open("regex_patterns.txt", "r") as f:
            regex_patterns = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        
        print(f"Loaded {len(regex_patterns)} regex patterns from file")
        print("First 5 regex patterns:")
        for pattern in regex_patterns[:5]:
            print(f"  - {pattern}")


def main():
    """Main example function"""
    print("GPU-Accelerated PCAP Scanner Examples")
    print("=" * 50)
    
    # Check if GPU is available
    try:
        import cupy as cp
        print("✓ GPU acceleration available")
        gpu_available = True
    except ImportError:
        print("⚠ GPU acceleration not available - will use CPU fallback")
        gpu_available = False
    
    # Run examples
    example_basic_scanning()
    example_regex_scanning()
    example_security_scanning()
    example_protocol_scanning()
    example_performance_monitoring()
    example_pattern_file_usage()
    
    print("\n" + "=" * 50)
    print("Examples completed!")
    print("\nTo run the scanner on your PCAP file:")
    print("python pcap_gpu_scanner.py your_file.pcap --patterns 'pattern1' 'pattern2'")
    print("\nFor help:")
    print("python pcap_gpu_scanner.py --help")


if __name__ == "__main__":
    main()
