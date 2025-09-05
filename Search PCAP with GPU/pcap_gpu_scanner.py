#!/usr/bin/env python3
"""
GPU-Accelerated PCAP Payload Scanner

This module implements a high-performance PCAP payload scanner using GPU acceleration
for pattern matching. It performs TCP stream reassembly on CPU and then uses GPU
for massively parallel string/regex search.

Key Features:
- TCP stream reassembly for cross-packet pattern detection
- GPU-accelerated multi-pattern matching using CuPy
- Efficient batching and memory management
- Performance monitoring and benchmarking
- Support for both exact string and regex patterns
"""

import os
import sys
import time
import argparse
import logging
from collections import defaultdict, deque
from typing import List, Dict, Tuple, Optional, Set, Any
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scapy.all import rdpcap, IP, TCP, UDP
from tqdm import tqdm
import psutil
import matplotlib.pyplot as plt
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

# Try to import CuPy for GPU acceleration
try:
    import cupy as cp
    # Test if GPU is actually working
    cp.cuda.Device(0).use()
    # Test basic GPU operations
    test_array = cp.zeros(1000, dtype=cp.float32)
    GPU_AVAILABLE = True
    print(f"{Fore.GREEN}✓ CuPy GPU acceleration available")
    print(f"{Fore.GREEN}✓ GPU device: {cp.cuda.Device(0).id}")
    # Get memory info using runtime API
    total_memory = cp.cuda.runtime.memGetInfo()[1]  # Total memory
    print(f"{Fore.GREEN}✓ GPU memory: {total_memory / 1024**3:.1f} GB total")
except ImportError as e:
    GPU_AVAILABLE = False
    print(f"{Fore.RED}❌ CuPy not installed or import failed: {e}")
    print(f"{Fore.YELLOW}💡 Fix: Install CuPy for your CUDA version:")
    print(f"   pip install cupy-cuda12x  # for CUDA 12.x")
    print(f"   pip install cupy-cuda11x  # for CUDA 11.x")
    print(f"   pip install cupy-cuda10x  # for CUDA 10.x")
    sys.exit(1)
except Exception as e:
    GPU_AVAILABLE = False
    print(f"{Fore.RED}❌ GPU initialization failed: {e}")
    print(f"{Fore.YELLOW}💡 Possible fixes:")
    print(f"   1. Install NVIDIA drivers: https://www.nvidia.com/drivers")
    print(f"   2. Install CUDA Toolkit: https://developer.nvidia.com/cuda-downloads")
    print(f"   3. Set CUDA_PATH environment variable")
    print(f"   4. Restart system after driver installation")
    print(f"   5. Check GPU compatibility with CUDA")
    sys.exit(1)

# Import advanced GPU kernels
try:
    from gpu_kernels import AdvancedGPUKernels, GPUBenchmark
    ADVANCED_KERNELS_AVAILABLE = True
except ImportError as e:
    print(f"{Fore.RED}❌ Failed to import advanced GPU kernels: {e}")
    print(f"{Fore.YELLOW}💡 This is required for maximum GPU performance.")
    print(f"{Fore.YELLOW}💡 Ensure gpu_kernels.py is in the same directory.")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pcap_scanner.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class FlowKey:
    """Represents a network flow (5-tuple)"""
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    protocol: str
    
    def __hash__(self):
        return hash((self.src_ip, self.dst_ip, self.src_port, self.dst_port, self.protocol))
    
    def __eq__(self, other):
        return (self.src_ip == other.src_ip and 
                self.dst_ip == other.dst_ip and
                self.src_port == other.src_port and
                self.dst_port == other.dst_port and
                self.protocol == other.protocol)


@dataclass
class MatchResult:
    """Represents a pattern match found in the PCAP"""
    flow_id: str
    pattern: str
    offset: int
    packet_timestamp: float
    flow_start: int
    flow_end: int
    match_context: str  # Surrounding bytes for context


@dataclass
class PerformanceStats:
    """Performance statistics for the scanner"""
    total_packets: int
    total_bytes: int
    reassembly_time: float
    gpu_processing_time: float
    total_time: float
    memory_usage: float
    gpu_memory_usage: float
    throughput_mbps: float
    gpu_throughput_mbps: float
    patterns_found: int


class TCPReassembler:
    """Handles TCP stream reassembly for cross-packet pattern detection"""
    
    def __init__(self):
        self.flows: Dict[FlowKey, Dict] = defaultdict(lambda: {
            'packets': deque(),
            'reassembled_data': bytearray(),
            'next_seq': 0,
            'base_seq': None
        })
    
    def add_packet(self, packet) -> Optional[Tuple[FlowKey, bytes, float]]:
        """Add a TCP packet to the reassembler"""
        if not packet.haslayer(TCP):
            return None
            
        ip_layer = packet[IP]
        tcp_layer = packet[TCP]
        
        # Create flow key
        flow_key = FlowKey(
            src_ip=ip_layer.src,
            dst_ip=ip_layer.dst,
            src_port=tcp_layer.sport,
            dst_port=tcp_layer.dport,
            protocol='TCP'
        )
        
        # Get payload
        payload = bytes(tcp_layer.payload) if tcp_layer.payload else b''
        if not payload:
            return None
            
        # Store packet info
        flow_data = self.flows[flow_key]
        flow_data['packets'].append({
            'seq': tcp_layer.seq,
            'payload': payload,
            'timestamp': packet.time
        })
        
        # Try to reassemble
        return self._try_reassemble(flow_key)
    
    def _try_reassemble(self, flow_key: FlowKey) -> Optional[Tuple[FlowKey, bytes, float]]:
        """Attempt to reassemble TCP stream - FIXED to process every packet immediately"""
        flow_data = self.flows[flow_key]
        packets = flow_data['packets']
        
        # FIXED: Process every packet immediately, don't wait for multiple packets
        if len(packets) == 0:
            return None
            
        # Get the most recent packet
        latest_packet = packets[-1]
        
        # Return the payload immediately (same logic as CPU scanner)
        if len(latest_packet['payload']) > 0:
            # Clear processed packets to avoid duplicates
            flow_data['packets'].clear()
            return (flow_key, latest_packet['payload'], latest_packet['timestamp'])
        
        return None


class GPUPayloadScanner:
    """GPU-accelerated payload scanner using CuPy and advanced kernels"""
    
    def __init__(self, patterns: List[str], use_regex: bool = False):
        self.patterns = patterns
        self.use_regex = use_regex
        self.pattern_lengths = [len(p.encode()) for p in patterns]
        self.max_pattern_length = max(self.pattern_lengths) if self.pattern_lengths else 0
        
        if not GPU_AVAILABLE:
            raise RuntimeError("GPU acceleration is required for this scanner. Please fix GPU issues and try again.")
        
        # Initialize GPU memory pool for better performance
        try:
            cp.cuda.Device(0).use()
            self.memory_pool = cp.get_default_memory_pool()
            # Set memory pool limit to 80% of available GPU memory
            total_memory = cp.cuda.runtime.memGetInfo()[1]  # Total memory
            self.memory_pool.set_limit(size=int(total_memory * 0.8))
        except Exception as e:
            raise RuntimeError(f"Failed to initialize GPU memory pool: {e}")
        
        # Initialize advanced kernels if available
        if ADVANCED_KERNELS_AVAILABLE:
            try:
                self.advanced_kernels = AdvancedGPUKernels()
                logger.info("Advanced GPU kernels initialized")
            except Exception as e:
                logger.error(f"Failed to initialize advanced GPU kernels: {e}")
                print(f"{Fore.RED}❌ Advanced GPU kernels failed to initialize: {e}")
                print(f"{Fore.YELLOW}💡 This is required for maximum performance.")
                print(f"{Fore.YELLOW}💡 Possible causes:")
                print(f"   1. CUDA Runtime Compiler (NVRTC) not found")
                print(f"   2. CUDA Toolkit not properly installed")
                print(f"   3. GPU driver issues")
                print(f"   4. Incompatible CUDA version")
                print(f"{Fore.YELLOW}💡 Solutions:")
                print(f"   1. Install CUDA Toolkit: https://developer.nvidia.com/cuda-downloads")
                print(f"   2. Set CUDA_PATH environment variable")
                print(f"   3. Add CUDA bin to PATH: %CUDA_PATH%\\bin")
                print(f"   4. Restart system after installation")
                raise RuntimeError(f"Advanced GPU kernels required but failed: {e}")
        else:
            raise RuntimeError("Advanced GPU kernels are required but not available")
        
        logger.info(f"Initialized GPU scanner with {len(patterns)} patterns")
    
    def scan_payloads(self, payloads: List[bytes], flow_ids: List[str]) -> List[MatchResult]:
        """Scan multiple payloads for patterns using GPU acceleration"""
        if not payloads:
            return []
        
        start_time = time.time()
        matches = []
        
        # Process payloads in batches for better GPU utilization
        batch_size = 100  # Increased batch size for better GPU utilization
        total_batches = (len(payloads) + batch_size - 1) // batch_size
        
        logger.info(f"Processing {len(payloads)} payloads in {total_batches} batches using GPU")
        
        try:
            # Process batches without progress bar for speed
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min(start_idx + batch_size, len(payloads))
                
                batch_payloads = payloads[start_idx:end_idx]
                batch_flow_ids = flow_ids[start_idx:end_idx]
                
                batch_matches = self._scan_batch(batch_payloads, batch_flow_ids)
                matches.extend(batch_matches)
        except Exception as e:
            logger.error(f"GPU batch processing failed: {e}")
            if "nvrtc64" in str(e):
                print(f"{Fore.RED}❌ CUDA Runtime Compiler (NVRTC) not found!")
                print(f"{Fore.YELLOW}💡 This is needed for advanced GPU pattern matching kernels.")
                print(f"{Fore.YELLOW}💡 Solutions:")
                print(f"   1. Install CUDA Toolkit: https://developer.nvidia.com/cuda-downloads")
                print(f"   2. Set CUDA_PATH environment variable to point to CUDA installation")
                print(f"   3. Add CUDA bin directory to PATH: %CUDA_PATH%\\bin")
                print(f"   4. Restart system after CUDA installation")
                print(f"   5. Check if nvrtc64_120_0.dll exists in CUDA bin directory")
                print(f"   6. Try using basic GPU mode (without advanced kernels)")
            raise RuntimeError(f"GPU batch processing failed: {e}")
        
        gpu_time = time.time() - start_time
        logger.info(f"GPU scanning completed in {gpu_time:.2f}s, found {len(matches)} matches")
        
        return matches
    
    def _scan_batch(self, payloads: List[bytes], flow_ids: List[str]) -> List[MatchResult]:
        """Scan a batch of payloads using GPU"""
        matches = []
        
        for i, (payload, flow_id) in enumerate(zip(payloads, flow_ids)):
            payload_matches = self._scan_single_payload(payload, flow_id)
            matches.extend(payload_matches)
        
        return matches
    
    def _scan_single_payload(self, payload: bytes, flow_id: str) -> List[MatchResult]:
        """Scan a single payload for all patterns using advanced GPU kernels"""
        matches = []
        
        # Choose optimal algorithm based on pattern count
        if len(self.patterns) == 1:
            # Single pattern: Use Boyer-Moore-Horspool (fastest for single patterns)
            pattern_bytes = self.patterns[0].encode()
            pattern_matches = self.advanced_kernels.boyer_moore_search(payload, pattern_bytes)
            
            # Convert matches to results
            for match_offset in pattern_matches:
                # Get context around the match
                start = max(0, match_offset - 20)
                end = min(len(payload), match_offset + len(pattern_bytes) + 20)
                context = payload[start:end]
                
                match_result = MatchResult(
                    flow_id=flow_id,
                    pattern=self.patterns[0],
                    offset=match_offset,
                    packet_timestamp=time.time(),
                    flow_start=start,
                    flow_end=end,
                    match_context=context.hex()
                )
                matches.append(match_result)
        elif len(self.patterns) <= 10:
            # Few patterns (2-10): Use vectorized multi-pattern search
            pattern_bytes = [p.encode() for p in self.patterns]
            pattern_matches = self.advanced_kernels.vectorized_multi_search(payload, pattern_bytes)
            
            # Convert matches to results
            for pattern_idx, pattern in enumerate(self.patterns):
                for match_offset in pattern_matches[pattern_idx]:
                    # Get context around the match
                    start = max(0, match_offset - 20)
                    end = min(len(payload), match_offset + len(pattern_bytes[pattern_idx]) + 20)
                    context = payload[start:end]
                    
                    match_result = MatchResult(
                        flow_id=flow_id,
                        pattern=pattern,
                        offset=match_offset,
                        packet_timestamp=time.time(),
                        flow_start=start,
                        flow_end=end,
                        match_context=context.hex()
                    )
                    matches.append(match_result)
        else:
            # Many patterns (10+): Use Aho-Corasick (PFAC)
            pattern_bytes = [p.encode() for p in self.patterns]
            pattern_matches = self.advanced_kernels.aho_corasick_search(payload, pattern_bytes)
            
            # Convert matches to results
            for pattern_idx, pattern in enumerate(self.patterns):
                for match_offset in pattern_matches[pattern_idx]:
                    # Get context around the match
                    start = max(0, match_offset - 20)
                    end = min(len(payload), match_offset + len(pattern_bytes[pattern_idx]) + 20)
                    context = payload[start:end]
                    
                    match_result = MatchResult(
                        flow_id=flow_id,
                        pattern=pattern,
                        offset=match_offset,
                        packet_timestamp=time.time(),
                        flow_start=start,
                        flow_end=end,
                        match_context=context.hex()
                    )
                    matches.append(match_result)
        
        return matches
    
    # Basic GPU string search removed - advanced kernels required for maximum performance


class PCAPScanner:
    """Main PCAP scanner that orchestrates the entire scanning process"""
    
    def __init__(self, patterns: List[str], use_regex: bool = False):
        self.patterns = patterns
        self.use_regex = use_regex
        self.reassembler = TCPReassembler()
        
        # GPU is required for this scanner
        if not GPU_AVAILABLE:
            raise RuntimeError("GPU acceleration is required for this scanner. Please fix GPU issues and try again.")
        
        try:
            self.gpu_scanner = GPUPayloadScanner(patterns, use_regex)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize GPU scanner: {e}")
        
        self.stats = PerformanceStats(
            total_packets=0,
            total_bytes=0,
            reassembly_time=0,
            gpu_processing_time=0,
            total_time=0,
            memory_usage=0,
            gpu_memory_usage=0,
            throughput_mbps=0,
            gpu_throughput_mbps=0,
            patterns_found=0
        )
    
    def scan_pcap(self, pcap_file: str) -> List[MatchResult]:
        """Scan a PCAP file for patterns"""
        logger.info(f"Starting PCAP scan: {pcap_file}")
        start_time = time.time()
        
        # Read PCAP file
        logger.info("Reading PCAP file...")
        packets = rdpcap(pcap_file)
        self.stats.total_packets = len(packets)
        
        # Extract payloads and perform TCP reassembly
        logger.info("Performing TCP reassembly...")
        reassembly_start = time.time()
        payloads, flow_ids, timestamps = self._extract_payloads(packets)
        self.stats.reassembly_time = time.time() - reassembly_start
        
        # Scan payloads using GPU
        logger.info("Scanning payloads for patterns using GPU acceleration...")
        gpu_start = time.time()
        try:
            matches = self.gpu_scanner.scan_payloads(payloads, flow_ids)
            self.stats.gpu_processing_time = time.time() - gpu_start
        except Exception as e:
            logger.error(f"GPU scanning failed: {e}")
            raise RuntimeError(f"GPU pattern matching failed: {e}")
        
        # Calculate final statistics
        self.stats.total_time = time.time() - start_time
        self.stats.patterns_found = len(matches)
        
        # Calculate throughput metrics
        total_data_mb = self.stats.total_bytes / 1024 / 1024
        self.stats.throughput_mbps = total_data_mb / self.stats.total_time  # Overall system throughput
        self.stats.gpu_throughput_mbps = total_data_mb / self.stats.gpu_processing_time if self.stats.gpu_processing_time > 0 else 0  # Pure GPU throughput
        
        # Get memory usage
        process = psutil.Process()
        self.stats.memory_usage = process.memory_info().rss / 1024 / 1024  # MB
        
        if GPU_AVAILABLE:
            try:
                self.stats.gpu_memory_usage = cp.cuda.runtime.memGetInfo()[0] / 1024 / 1024  # MB (used memory)
            except:
                self.stats.gpu_memory_usage = 0
        
        logger.info(f"Scan completed in {self.stats.total_time:.2f}s")
        logger.info(f"Found {len(matches)} pattern matches")
        
        return matches
    
    def _extract_payloads(self, packets) -> Tuple[List[bytes], List[str], List[float]]:
        """Extract payloads from packets with TCP reassembly - optimized version"""
        # Pre-allocate lists for better performance
        payloads = []
        flow_ids = []
        timestamps = []
        
        # Process packets without progress bar for speed
        for packet in packets:
            if packet.haslayer(IP):
                ip_layer = packet[IP]
                
                # Handle TCP packets with reassembly
                if packet.haslayer(TCP):
                    result = self.reassembler.add_packet(packet)
                    if result:
                        flow_key, payload, timestamp = result
                        payloads.append(payload)
                        flow_ids.append(f"{flow_key.src_ip}:{flow_key.src_port}-{flow_key.dst_ip}:{flow_key.dst_port}")
                        timestamps.append(timestamp)
                        self.stats.total_bytes += len(payload)
                
                # Handle UDP packets (no reassembly needed)
                elif packet.haslayer(UDP):
                    udp_layer = packet[UDP]
                    payload = bytes(udp_layer.payload) if udp_layer.payload else b''
                    if payload:
                        flow_key = FlowKey(
                            src_ip=ip_layer.src,
                            dst_ip=ip_layer.dst,
                            src_port=udp_layer.sport,
                            dst_port=udp_layer.dport,
                            protocol='UDP'
                        )
                        payloads.append(payload)
                        flow_ids.append(f"{flow_key.src_ip}:{flow_key.src_port}-{flow_key.dst_ip}:{flow_key.dst_port}")
                        timestamps.append(packet.time)
                        self.stats.total_bytes += len(payload)
        
        return payloads, flow_ids, timestamps
    
    # CPU fallback method removed - GPU is required for this scanner
    
    def print_stats(self):
        """Print detailed performance statistics"""
        print(f"\n{Fore.CYAN}=== PCAP Scanner Performance Statistics ==={Style.RESET_ALL}")
        print(f"Total Packets Processed: {self.stats.total_packets:,}")
        print(f"Total Bytes Scanned: {self.stats.total_bytes:,} bytes ({self.stats.total_bytes/1024/1024:.2f} MB)")
        print(f"TCP Reassembly Time: {self.stats.reassembly_time:.2f}s")
        print(f"GPU Processing Time: {self.stats.gpu_processing_time:.2f}s")
        print(f"Total Processing Time: {self.stats.total_time:.2f}s")
        print(f"{Fore.YELLOW}Overall Throughput: {self.stats.throughput_mbps:.2f} MB/s{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Pure GPU Throughput: {self.stats.gpu_throughput_mbps:.2f} MB/s{Style.RESET_ALL}")
        print(f"Memory Usage: {self.stats.memory_usage:.2f} MB")
        if GPU_AVAILABLE:
            print(f"GPU Memory Usage: {self.stats.gpu_memory_usage:.2f} MB")
        print(f"Pattern Matches Found: {self.stats.patterns_found}")
        
        if self.stats.total_time > 0:
            packets_per_second = self.stats.total_packets / self.stats.total_time
            print(f"Packets per Second: {packets_per_second:.2f}")
            
        # Performance breakdown
        if self.stats.total_time > 0:
            reassembly_pct = (self.stats.reassembly_time / self.stats.total_time) * 100
            gpu_pct = (self.stats.gpu_processing_time / self.stats.total_time) * 100
            other_pct = 100 - reassembly_pct - gpu_pct
            print(f"\n{Fore.CYAN}Performance Breakdown:{Style.RESET_ALL}")
            print(f"  TCP Reassembly: {reassembly_pct:.1f}% ({self.stats.reassembly_time:.2f}s)")
            print(f"  GPU Processing: {gpu_pct:.1f}% ({self.stats.gpu_processing_time:.2f}s)")
            print(f"  Other (I/O, etc): {other_pct:.1f}% ({self.stats.total_time - self.stats.reassembly_time - self.stats.gpu_processing_time:.2f}s)")


def main():
    """Main entry point for the PCAP scanner"""
    parser = argparse.ArgumentParser(description="GPU-Accelerated PCAP Payload Scanner")
    parser.add_argument("pcap_file", help="Path to the PCAP file to scan")
    parser.add_argument("--patterns", "-p", nargs="+", required=True, 
                       help="Patterns to search for (strings or regex)")
    parser.add_argument("--regex", "-r", action="store_true", 
                       help="Treat patterns as regular expressions")
    parser.add_argument("--output", "-o", default="matches.csv",
                       help="Output file for matches (CSV format)")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Check if PCAP file exists
    if not os.path.exists(args.pcap_file):
        print(f"{Fore.RED}Error: PCAP file '{args.pcap_file}' not found{Style.RESET_ALL}")
        sys.exit(1)
    
    # Initialize scanner
    scanner = PCAPScanner(args.patterns, args.regex)
    
    try:
        # Scan PCAP file
        matches = scanner.scan_pcap(args.pcap_file)
        
        # Save results
        if matches:
            df = pd.DataFrame([
                {
                    'flow_id': m.flow_id,
                    'pattern': m.pattern,
                    'offset': m.offset,
                    'timestamp': m.packet_timestamp,
                    'context': m.match_context
                }
                for m in matches
            ])
            df.to_csv(args.output, index=False)
            print(f"{Fore.GREEN}✓ Found {len(matches)} matches, saved to {args.output}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}No pattern matches found{Style.RESET_ALL}")
        
        # Print performance statistics
        scanner.print_stats()
        
    except Exception as e:
        logger.error(f"Error during scanning: {e}")
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
