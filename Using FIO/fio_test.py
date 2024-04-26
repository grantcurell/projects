import argparse
import subprocess
import sys
import os

def run_fio(block_size, io_type, size, device, ioengine, iodepth, numjobs):
    cmd = [
        'fio',
        '--name=test',
        f'--ioengine={ioengine}',
        f'--iodepth={iodepth}',
        f'--rw={io_type}',
        f'--bs={block_size}',
        '--direct=1',
        f'--size={size}',
        f'--numjobs={numjobs}',
        f'--filename={device}'
    ]

    print("Starting FIO with the following command: {}".format(' '.join(cmd)))
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    # Print live output from FIO
    for line in iter(process.stdout.readline, ''):
        print(line, end='')

    process.stdout.close()
    process.wait()

def print_detailed_instructions():
    print("""
FIO Drive Performance Test Script
---------------------------------

This script uses FIO (Flexible I/O Tester) to test the performance of a storage device using direct I/O operations.

USAGE:
    python3 fio_test.py [-e IOENGINE] [-b BLOCK_SIZE] [-t {read,write}] [-s SIZE] device

ARGUMENTS:
    device           The target device for testing (required), e.g., '/dev/sda'.
                     IMPORTANT: Be extremely careful with the device selection to avoid data loss.
                     Only use dedicated testing devices or partitions.

OPTIONAL ARGUMENTS:
    -e IOENGINE      I/O engine for the test. Default is 'libaio'.
    -b BLOCK_SIZE    Block size for I/O operations. Default is '4k'.
    -t {read,write,rw,randrw}  Type of I/O operation: 'read', 'write', 'rw' (mixed read/write), 
                               or 'randrw' (mixed random read/write). Default is 'rw'.
    -s SIZE          Size of the test data. Default is '2G'.
    -d IODEPTH       I/O depth for operations. Default is 64.
    -j NUMJOBS       Number of jobs to spawn. Default is the number of CPU cores.


Selecting a Device:
    - Ensure the device is not in use and does not contain critical data.
    - Use commands like 'lsblk', 'df', or 'fdisk -l' to identify the correct device.
    - Running this script on the wrong device can result in data loss.

What the Program Does:
    - The script performs read or write operations directly on the specified device.
    - It measures the performance of these operations using the specified parameters.
    - Results include metrics like I/O speed and latency.

WARNING:
    - This script performs direct I/O operations that can overwrite data.
    - Ensure you have backups and use a non-critical device for testing.
    - Running the script requires appropriate permissions (typically root).
""")

def main():
    parser = argparse.ArgumentParser(description="Run FIO to test drive performance with direct I/O.", add_help=False)
    default_numjobs = os.cpu_count()  # Default to the number of CPU cores

    parser.add_argument("-e", "--ioengine", default="libaio", choices=['libaio', 'posixaio', 'mmap', 'sync', 'io_uring'], help="I/O engine for the test (default: 'libaio').")
    parser.add_argument("-b", "--block_size", default="4k", help="Block size for I/O operations (default: '4k').")
    parser.add_argument("-t", "--io_type", default="rw", choices=['read', 'write', 'rw', 'randrw'], help="Type of I/O operation (default: 'rw').")
    parser.add_argument("-s", "--size", default="2G", help="Size of the test data (default: '2G').")
    parser.add_argument("-d", "--iodepth", default="64", help="I/O depth for operations (default: 64).")
    parser.add_argument("-j", "--numjobs", default=default_numjobs, type=int, help=f"Number of jobs to spawn (default: {default_numjobs}).")
    parser.add_argument("device", help="The target device, e.g., '/dev/sda'.")

    if len(sys.argv) == 1:
        print_detailed_instructions()
        sys.exit(1)

    args = parser.parse_args()

    run_fio(args.block_size, args.io_type, args.size, args.device, args.ioengine, args.iodepth, args.numjobs)

if __name__ == "__main__":
    main()