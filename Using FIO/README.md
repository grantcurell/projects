# Using FIO

- [Understanding FIO Test Output](#understanding-fio-test-output)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
    - [Installing Python 3](#installing-python-3)
    - [Installing FIO](#installing-fio)
  - [Using the Script](#using-the-script)
    - [Script Arguments](#script-arguments)
    - [Running the Script](#running-the-script)
    - [Selecting a Device](#selecting-a-device)
    - [Example Usage](#example-usage)
  - [Interpreting Results](#interpreting-results)
  - [Warnings and Recommendations](#warnings-and-recommendations)
  - [Understanding Output](#understanding-output)
    - [Initial Setup Information](#initial-setup-information)
    - [Main Performance Metrics](#main-performance-metrics)
    - [Latency Statistics](#latency-statistics)
    - [Latency Percentiles](#latency-percentiles)
    - [Bandwidth and IOPS Analysis](#bandwidth-and-iops-analysis)
    - [Additional Statistics](#additional-statistics)
    - [IO Depths](#io-depths)
    - [Disk Stats](#disk-stats)
    - [IO Depth](#io-depth)
      - [Context in Real-World Scenarios](#context-in-real-world-scenarios)
      - [Choosing the Right `iodepth`](#choosing-the-right-iodepth)


## Overview

The script uses FIO (Flexible I/O Tester) to perform various I/O operations on a specified storage device.

## Prerequisites

Before using the script, ensure you have Python 3 and FIO installed on your system.

### Installing Python 3

- Linux: Use your native Python instance

- **macOS** (using Homebrew):
  
```bash
brew install python
```

### Installing FIO

- **Ubuntu**:

```bash
sudo apt-get install fio
```

- **RHEL**:

```bash
sudo dnf install fio
```

- **macOS** (using Homebrew):

```bash
brew install fio
```

## Using the Script

### Script Arguments

- `-e, --ioengine`: I/O engine for the test (default: 'libaio').
- `-b, --block_size`: Block size for I/O operations (default: '4k').
- `-t, --io_type`: Type of I/O operation (default: 'rw').
- `-s, --size`: Size of the test data (default: '2G').
- `-d, --iodepth`: I/O depth for operations (default: 64).
- `-j, --numjobs`: Number of jobs to spawn (default: Number of CPU cores).
- `device`: The target device for testing (required).

### Running the Script

1. **Download the Script**:
   Save the provided Python script to your system.

2. **Make the Script Executable** (Linux/macOS):
   
```bash
chmod +x fio_test.py
```

3. **Run the Script**:
   
Use the command line to navigate to the script's directory and run it. Replace `[arguments]` with desired options:
```bash
python3 fio_test.py [arguments] /dev/sda
```

Replace `/dev/sda` with the appropriate device identifier for your system.

### Selecting a Device

- Use commands like `lsblk`, `df`, or `fdisk -l` to identify the correct storage device.
- Be extremely cautious with device selection to avoid accidental data loss.

### Example Usage

Run a test with the default settings on device `/dev/sda`:

```bash
python3 fio_test.py /dev/sda
```

Run a test with a block size of 1M, in read mode, on device `/dev/nvme0n1`:

```bash
python3 fio_test.py -b 1M -t read /dev/nvme0n1
```

## Interpreting Results

The script will output various metrics such as IOPS (Input/Output Operations Per Second), bandwidth (BW), latency, and more. These metrics provide insight into the performance characteristics of the tested storage device.

See [Understanding Output](#understanding-output)

## Warnings and Recommendations

- **Data Loss**: Direct I/O operations can overwrite data. Ensure you have backups and use a non-critical device for testing.
- **Permissions**: Running the script might require appropriate permissions, especially when accessing raw devices.
- **Long-Running Tests**: Some tests, especially with large sizes or high I/O depths, may take a significant amount of time to complete.

## Understanding Output

FIO (Flexible I/O Tester) provides comprehensive details about I/O performance. Here's a breakdown of the output from a typical run:

### Initial Setup Information

- `test: (g=0): rw=write, bs=(R) 4096B-4096B, (W) 4096B-4096B, (T) 4096B-4096B, ioengine=libaio, iodepth=1`
  - **rw**: Read/Write mode (here, it's set to write).
  - **bs**: Block size for read (R), write (W), and trim (T) operations.
  - **ioengine**: I/O engine used (libaio, in this case).
  - [**iodepth**](#io-depth): Number of I/O operations to keep in flight.

### Main Performance Metrics

- `write: IOPS=53.4k, BW=208MiB/s (219MB/s)(2048MiB/9826msec); 0 zone resets`
  - **IOPS (Input/Output Operations Per Second)**: Number of read/write operations per second.
  - **BW (Bandwidth)**: The rate of data transfer, shown in MiB/s (Mebibytes per second) and MB/s (Megabytes per second).
  - **2048MiB/9826msec**: Total data transferred and the total time taken.

### Latency Statistics

- `slat (nsec)`: Submission latency (time from submission to the device until it's queued).
- `clat (usec)`: Completion latency (time from submission until completion).
- `lat (usec)`: Total latency (submission to completion).
  - **min, max, avg, stdev**: Minimum, maximum, average, and standard deviation of latencies.

### Latency Percentiles

- `clat percentiles (nsec)`: Shows various percentiles for completion latency.
  - Percentiles indicate the latency under which a certain percentage of operations completed.

### Bandwidth and IOPS Analysis

- `bw (KiB/s)`: Bandwidth in Kibibytes per second.
- `iops`: Input/output operations per second.
  - **min, max, avg, stdev, samples**: Statistics on IOPS.

### Additional Statistics

- `cpu`: CPU usage statistics, including user (`usr`) and system (`sys`) percentages.
- `ctx`: Number of context switches.
- `majf/minf`: Major and minor faults.

### IO Depths

- Shows the percentage of I/Os that were at each depth.
  - **1=100.0%**: All I/Os had a depth of 1 (synchronous I/O).

### Disk Stats

- `Disk stats (read/write)`: Shows the read and write statistics for the disk.
- `sdb: ios=50/515233, merge=0/0, ticks=3/8010, in_queue=8014, util=99.13%`
  - **ios**: Number of read and write I/Os.
  - **merge**: Number of merged read and write requests.
  - **ticks**: Duration of read and write requests.
  - **in_queue**: Time the device had I/O requests queued.
  - **util**: Utilization percentage of the device.

### IO Depth

`iodepth` refers to the number of I/O operations (I/O requests) that FIO will keep in the queue (or "in flight") before waiting for them to complete. Essentially, it's about how many I/O requests are outstanding at any given moment.

- **Impact on I/O Performance Testing**:
    - **Low `iodepth` (e.g., 1)**: This setting means FIO will wait for an I/O operation to complete before issuing the next one. This simulates a more sequential and synchronous I/O pattern, which is typical for workloads where each operation depends on the completion of the previous one.
    - **High `iodepth`**: A higher value, such as 32 or 64, allows FIO to issue multiple I/O requests simultaneously. This setting is used to simulate asynchronous I/O, where multiple operations are happening at the same time. It's more representative of high-performance environments, like databases or servers handling multiple parallel requests.

#### Context in Real-World Scenarios

- **SSD vs HDD**: Solid State Drives (SSDs) often benefit from higher `iodepth` values because they can handle a large number of simultaneous operations efficiently. In contrast, traditional Hard Disk Drives (HDDs) might not show the same level of performance improvement with high `iodepth` due to their mechanical nature.

- **Testing Different Workloads**: By varying the `iodepth`, you can simulate different types of workloads. For instance, a web server handling multiple concurrent requests might be best simulated with a higher `iodepth`, while an application that does heavy but sequential file writing might be more accurately tested with a lower `iodepth`.

#### Choosing the Right `iodepth`

- **Depends on Your Goals**: The right `iodepth` depends on what aspect of I/O performance you're trying to measure or what kind of workload you want to simulate. 
- **Trial and Error**: Often, finding the optimal `iodepth` for a specific scenario involves some experimentation. You might need to run tests at different `iodepth` levels to see how your storage device or system performs under varying load conditions.
