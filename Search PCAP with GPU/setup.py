#!/usr/bin/env python3
"""
Setup script for GPU-Accelerated PCAP Scanner

This script sets up the environment and installs dependencies for the
GPU-accelerated PCAP scanner.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def check_cuda_availability():
    """Check if CUDA is available"""
    try:
        import cupy as cp
        print(f"✓ CuPy detected with CUDA {cp.cuda.runtime.driverGetVersion()}")
        return True
    except ImportError:
        print("⚠ CuPy not found - GPU acceleration will not be available")
        return False
    except Exception as e:
        print(f"⚠ CUDA error: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)

def create_directories():
    """Create necessary directories"""
    directories = ["logs", "output", "temp", "results"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Created directory: {directory}")

def test_installation():
    """Test the installation"""
    print("Testing installation...")
    
    try:
        # Test basic imports
        import numpy as np
        import pandas as pd
        from scapy.all import rdpcap
        import psutil
        
        print("✓ Basic dependencies imported successfully")
        
        # Test GPU if available
        if check_cuda_availability():
            import cupy as cp
            print("✓ GPU acceleration available")
            
            # Test GPU memory allocation
            test_array = cp.zeros(1000, dtype=cp.float32)
            print("✓ GPU memory allocation successful")
        else:
            print("⚠ GPU acceleration not available")
        
        print("✓ Installation test completed successfully")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Test error: {e}")
        sys.exit(1)

def main():
    """Main setup function"""
    print("GPU-Accelerated PCAP Scanner Setup")
    print("=" * 40)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Create directories
    create_directories()
    
    # Test installation
    test_installation()
    
    print("\n" + "=" * 40)
    print("Setup completed successfully!")
    print("\nNext steps:")
    print("1. Download a PCAP file for testing")
    print("2. Run: python test_scanner.py")
    print("3. Or run: python pcap_gpu_scanner.py your_file.pcap --patterns pattern1 pattern2")
    print("\nFor help: python pcap_gpu_scanner.py --help")

if __name__ == "__main__":
    main()
