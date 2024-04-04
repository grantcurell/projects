#!/bin/bash

echo "Gathering system information for HPL configuration..."

# Memory Information
echo "Memory Information:"
free -h
echo ""

# CPU Information: number of processors, cores per processor, threads per core
echo "CPU Information:"
lscpu
echo ""

# NUMA Nodes Information
echo "NUMA Nodes Information:"
numactl --hardware
echo ""

# Checking for Hyper-Threading
echo "Hyper-Threading Check:"
if [ $(lscpu | grep -i "Thread(s) per core:" | awk '{print $4}') -gt 1 ]; then
    echo "Hyper-Threading is Enabled"
else
    echo "Hyper-Threading is Disabled"
fi
echo ""

# Displaying total number of MPI processes possible (total logical cores)
echo "Total Possible MPI Processes (Logical Cores):"
lscpu | grep -i "^CPU(s):"
echo ""

# Additional information: System Architecture, Model Name
echo "System Architecture:"
lscpu | grep "Architecture"
echo "CPU Model:"
lscpu | grep "Model name"
echo ""

echo "System information gathering complete."
