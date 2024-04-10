# Results

- [Results](#results)
  - [Host Info](#host-info)
  - [Run 1: Thu Mar 21 09:16:12 CDT 2024](#run-1-thu-mar-21-091612-cdt-2024)
    - [Versions](#versions)
    - [Notes](#notes)
    - [SLURM Job](#slurm-job)
    - [runme](#runme)
    - [HPL.dat](#hpldat)
    - [Results](#results-1)
  - [Run 2: Thu Mar 21 10:02:20 CDT 2024](#run-2-thu-mar-21-100220-cdt-2024)
    - [Versions](#versions-1)
    - [Notes](#notes-1)
    - [SLURM Job](#slurm-job-1)
    - [runme](#runme-1)
    - [HPL.dat](#hpldat-1)
    - [Results](#results-2)
  - [Run 3: Thu Mar 21 10:10:32 CDT 2024](#run-3-thu-mar-21-101032-cdt-2024)
    - [Versions](#versions-2)
    - [Notes](#notes-2)
    - [SLURM Job](#slurm-job-2)
    - [runme](#runme-2)
    - [HPL.dat](#hpldat-2)
    - [Results](#results-3)
  - [Run 4: Thu Mar 21 16:43:18 CDT 2024](#run-4-thu-mar-21-164318-cdt-2024)
    - [Versions](#versions-3)
    - [Notes](#notes-3)
    - [SLURM Job](#slurm-job-3)
    - [runme](#runme-3)
    - [HPL.dat](#hpldat-3)
    - [Results](#results-4)
  - [Run 5: Thu Mar 21 17:00:17 CDT 2024](#run-5-thu-mar-21-170017-cdt-2024)
    - [Versions](#versions-4)
    - [Notes](#notes-4)
    - [SLURM Job](#slurm-job-4)
    - [runme](#runme-4)
    - [HPL.dat](#hpldat-4)
    - [Results](#results-5)
  - [Run 6: Fri Mar 22 10:35:12 CDT 2024](#run-6-fri-mar-22-103512-cdt-2024)
    - [Versions](#versions-5)
    - [Notes](#notes-5)
    - [SLURM Job](#slurm-job-5)
    - [runme](#runme-5)
    - [HPL.dat](#hpldat-5)
    - [Results](#results-6)
  - [Run 7: Tue Mar 26 15:01:59 2024](#run-7-tue-mar-26-150159-2024)
    - [Versions](#versions-6)
    - [Notes](#notes-6)
    - [SLURM Job](#slurm-job-6)
    - [runme](#runme-6)
    - [HPL.dat](#hpldat-6)
    - [Results](#results-7)
  - [Removed SLURM](#removed-slurm)
    - [Run 1](#run-1)
      - [Notes](#notes-7)
      - [Results](#results-8)
    - [Run 2 Fri Apr  5 11:15:50 CDT 2024](#run-2-fri-apr--5-111550-cdt-2024)
      - [Notes](#notes-8)
      - [Results](#results-9)


## Host Info

```bash
Gathering system information for HPL configuration...
Memory Information:
              total        used        free      shared  buff/cache   available
Mem:          503Gi       2.9Gi       498Gi       1.8Gi       2.2Gi       496Gi
Swap:          11Gi          0B        11Gi

CPU Information:
Architecture:        x86_64
CPU op-mode(s):      32-bit, 64-bit
Byte Order:          Little Endian
CPU(s):              112
On-line CPU(s) list: 0-111
Thread(s) per core:  1
Core(s) per socket:  56
Socket(s):           2
NUMA node(s):        8
Vendor ID:           GenuineIntel
CPU family:          6
Model:               143
Model name:          Intel(R) Xeon(R) Platinum 8480+
Stepping:            6
CPU MHz:             2000.000
BogoMIPS:            4000.00
L1d cache:           48K
L1i cache:           32K
L2 cache:            2048K
L3 cache:            107520K
NUMA node0 CPU(s):   0-13
NUMA node1 CPU(s):   14-27
NUMA node2 CPU(s):   28-41
NUMA node3 CPU(s):   42-55
NUMA node4 CPU(s):   56-69
NUMA node5 CPU(s):   70-83
NUMA node6 CPU(s):   84-97
NUMA node7 CPU(s):   98-111
Flags:               fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pd
pe1gb rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc cpuid aperfmperf tsc_known_freq pni pclmulqdq dtes64 monitor ds
_cpl smx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm 3dnowpr
efetch cpuid_fault epb cat_l3 cat_l2 cdp_l3 invpcid_single cdp_l2 ssbd mba ibrs ibpb stibp ibrs_enhanced fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invp
cid cqm rdt_a avx512f avx512dq rdseed adx smap avx512ifma clflushopt clwb intel_pt avx512cd sha_ni avx512bw avx512vl xsaveopt xsavec xgetbv1 xsaves cqm_ll
c cqm_occup_llc cqm_mbm_total cqm_mbm_local split_lock_detect avx_vnni avx512_bf16 wbnoinvd dtherm ida arat pln pts avx512vbmi umip pku ospke waitpkg avx5
12_vbmi2 gfni vaes vpclmulqdq avx512_vnni avx512_bitalg tme avx512_vpopcntdq la57 rdpid bus_lock_detect cldemote movdiri movdir64b enqcmd fsrm md_clear se
rialize tsxldtrk pconfig arch_lbr amx_bf16 avx512_fp16 amx_tile amx_int8 flush_l1d arch_capabilities

NUMA Nodes Information:
available: 8 nodes (0-7)
node 0 cpus: 0 1 2 3 4 5 6 7 8 9 10 11 12 13
node 0 size: 63920 MB
node 0 free: 63082 MB
node 1 cpus: 14 15 16 17 18 19 20 21 22 23 24 25 26 27
node 1 size: 64508 MB
node 1 free: 64118 MB
node 2 cpus: 28 29 30 31 32 33 34 35 36 37 38 39 40 41
node 2 size: 64508 MB
node 2 free: 64272 MB
node 3 cpus: 42 43 44 45 46 47 48 49 50 51 52 53 54 55
node 3 size: 64508 MB
node 3 free: 63319 MB
node 4 cpus: 56 57 58 59 60 61 62 63 64 65 66 67 68 69
node 4 size: 64508 MB
node 4 free: 64133 MB
node 5 cpus: 70 71 72 73 74 75 76 77 78 79 80 81 82 83
node 5 size: 64508 MB
node 5 free: 64139 MB
node 6 cpus: 84 85 86 87 88 89 90 91 92 93 94 95 96 97
node 6 size: 64508 MB
node 6 free: 63784 MB
node 7 cpus: 98 99 100 101 102 103 104 105 106 107 108 109 110 111
node 7 size: 64505 MB
node 7 free: 63377 MB
node distances:
node   0   1   2   3   4   5   6   7 
  0:  10  12  12  12  21  21  21  21 
  1:  12  10  12  12  21  21  21  21 
  2:  12  12  10  12  21  21  21  21 
  3:  12  12  12  10  21  21  21  21 
  4:  21  21  21  21  10  12  12  12 
  5:  21  21  21  21  12  10  12  12 
  6:  21  21  21  21  12  12  10  12 
  7:  21  21  21  21  12  12  12  10 

Hyper-Threading Check:
Hyper-Threading is Disabled

Total Possible MPI Processes (Logical Cores):
CPU(s):              112

System Architecture:
Architecture:        x86_64
CPU Model:
Model name:          Intel(R) Xeon(R) Platinum 8480+

System information gathering complete.
```

## Run 1: Thu Mar 21 09:16:12 CDT 2024

### Versions

- Intel MKL version: benchmarks_2024.0
- Intel MPI version: intel/mpi/2019u12
  - This was the most recent version available

### Notes

- This was the first controlled run. Performance was terrible. Not sure why. Starting to investigate.

### SLURM Job

```
#SBATCH --job-name=linpack
#SBATCH --output=linpack_%j.out
#SBATCH --partition=8480         # Specify the partition
#SBATCH --nodes=2               # Adjust based on how many nodes you want to use
#SBATCH --ntasks-per-node=8     # Assuming you want to utilize all cores
#SBATCH --time=0:05:00          # Set the time limit; adjust as necessary
#SBATCH --exclusive              # Optional: Request exclusive access to the nodes

# Load the Intel MPI module
module load intel/mpi/2019u12

# Navigate to the directory containing the LINPACK files
cd /home/grant/benchmarks_2024.0/linux/share/mkl/benchmarks/mp_linpack

# Run the LINPACK benchmark
bash runme_intel64_dynamic
```

### runme

```bash
#!/bin/bash

# Set the total number of MPI processes to run.
# Assuming you have 16 cores and you want to utilize all of them with one process per core.
export MPI_PROC_NUM=16

export OUT=xhpl_intel64_dynamic_outputs.txt

# Specify the executable to use.
export HPL_EXE=xhpl_intel64_dynamic

# Log the start time and system state before running the benchmark.
echo -n "This run was done on: " && date
echo -n "This run was done on: " >> $OUT
date >> $OUT
echo "HPL.dat: " >> $OUT
cat HPL.dat >> $OUT
echo "Binary name: " >> $OUT
ls -l ${HPL_EXE} >> $OUT
echo "This script: " >> $OUT
cat $0 >> $OUT  # $0 represents the script itself.
echo "Environment variables: " >> $OUT
env >> $OUT
echo "Actual run: " >> $OUT

# Execute the LINPACK benchmark with the specified number of MPI processes.
mpirun -np ${MPI_PROC_NUM} ./${HPL_EXE} "$@" | tee -a $OUT

# Log the completion time.
echo -n "Done: " >> $OUT
date >> $OUT
echo -n "Done: " && date
```

### HPL.dat

```
HPLinpack benchmark input file
Innovative Computing Laboratory, University of Tennessee
HPL.out      output file name (if any)
6            device out (6=stdout,7=stderr,file)
1            # of problems sizes (N)
1000         Ns (this is an example; adjust based on the calculation above)
1            # of NBs
192          NBs (a common choice, but you might experiment with this)
1            PMAP process mapping (0=Row-,1=Column-major)
1            # of process grids (P x Q)
4            Ps (you could also try 8 for a different P x Q configuration)
4            Qs (correspondingly, this would be 4 if you chose P as 8)
1.0          threshold
1            # of panel fact
2 1 0        PFACTs (0=left, 1=Crout, 2=Right)
1            # of recursive stopping criterium
2            NBMINs (>= 1)
1            # of panels in recursion
2            NDIVs
1            # of recursive panel fact.
1 0 2        RFACTs (0=left, 1=Crout, 2=Right)
1            # of broadcast
0            BCASTs (0=1rg,1=1rM,2=2rg,3=2rM,4=Lng,5=LnM)
1            # of lookahead depth
0            DEPTHs (>=0)
0            SWAP (0=bin-exch,1=long,2=mix)
1            swapping threshold
1            L1 in (0=transposed,1=no-transposed) form
1            U  in (0=transposed,1=no-transposed) form
0            Equilibration (0=no,1=yes)
8            memory alignment in double (> 0)
```

### Results

```
This run was done on: Thu Mar 21 09:16:12 CDT 2024
================================================================================
HPLinpack 2.3  --  High-Performance Linpack benchmark  --   December 2, 2018
Written by A. Petitet and R. Clint Whaley,  Innovative Computing Laboratory, UTK
Modified by Piotr Luszczek, Innovative Computing Laboratory, UTK
Modified by Julien Langou, University of Colorado Denver
================================================================================

An explanation of the input/output parameters follows:
T/V    : Wall time / encoded variant.
N      : The order of the coefficient matrix A.
NB     : The partitioning blocking factor.
P      : The number of process rows.
Q      : The number of process columns.
Time   : Time in seconds to solve the linear system.
Gflops : Rate of execution for solving the linear system.

The following parameter values will be used:

N        :    1000 
NB       :     192 
PMAP     : Column-major process mapping
P        :       4 
Q        :       4 
PFACT    :   Right 
NBMIN    :       2 
NDIV     :       2 
RFACT    :   Crout 
BCAST    :   1ring 
DEPTH    :       0 
SWAP     : Binary-exchange
L1       : no-transposed form
U        : no-transposed form
EQUIL    : no
ALIGN    :    8 double precision words

--------------------------------------------------------------------------------

- The matrix A is randomly generated for each test.
- The following scaled residual check will be computed:
      ||Ax-b||_oo / ( eps * ( || x ||_oo * || A ||_oo + || b ||_oo ) * N )
- The relative machine precision (eps) is taken to be               1.110223e-16
- Computational tests pass if scaled residuals are less than                 1.0

z1-34           : Column=000192 Fraction=0.005 Kernel=    0.00 Mflops=    7.52
z1-34           : Column=000384 Fraction=0.195 Kernel=    4.50 Mflops=    5.98
z1-34           : Column=000576 Fraction=0.385 Kernel=    2.55 Mflops=    4.88
z1-35           : Column=000768 Fraction=0.595 Kernel=    1.13 Mflops=    4.04
z1-35           : Column=000960 Fraction=0.795 Kernel=    0.19 Mflops=    3.22
================================================================================
T/V                N    NB     P     Q               Time                 Gflops
--------------------------------------------------------------------------------
WC00C2R2        1000   192     4     4             218.53            3.05759e-03
HPL_pdgesv() start time Thu Mar 21 09:16:19 2024

HPL_pdgesv() end time   Thu Mar 21 09:19:57 2024

--------------------------------------------------------------------------------
||Ax-b||_oo/(eps*(||A||_oo*||x||_oo+||b||_oo)*N)=   5.58840572e-03 ...... PASSED
================================================================================

Finished      1 tests with the following results:
              1 tests completed and passed residual checks,
              0 tests completed and failed residual checks,
              0 tests skipped because of illegal input values.
--------------------------------------------------------------------------------

End of Tests.
================================================================================
Done: Thu Mar 21 09:20:01 CDT 2024
```

## Run 2: Thu Mar 21 10:02:20 CDT 2024

### Versions

- Intel MKL version: benchmarks_2024.0
- Intel MPI version: intel/mpi/2019u12
  - This was the most recent version available

### Notes

- In this run I set `MPI_PER_NODE`, `NUMA_PER_MPI`, and `I_MPI_DAPL_DIRECT_COPY_THRESHOLD` on run. Performance was still terrible.
- It also seems the `I_MPI_DAPL_DIRECT_COPY_THRESHOLD` value doesn't matter: `[0] MPI startup(): I_MPI_DAPL_DIRECT_COPY_THRESHOLD variable has been removed from the product, its value is ignored`

### SLURM Job

```
#SBATCH --job-name=linpack
#SBATCH --output=linpack_%j.out
#SBATCH --partition=8480         # Specify the partition
#SBATCH --nodes=2               # Adjust based on how many nodes you want to use
#SBATCH --ntasks-per-node=8     # Assuming you want to utilize all cores
#SBATCH --time=0:05:00          # Set the time limit; adjust as necessary
#SBATCH --exclusive              # Optional: Request exclusive access to the nodes

# Load the Intel MPI module
module load intel/mpi/2019u12

# Navigate to the directory containing the LINPACK files
cd /home/grant/benchmarks_2024.0/linux/share/mkl/benchmarks/mp_linpack

# Run the LINPACK benchmark
bash runme_intel64_dynamic
```

### runme

```bash
#!/bin/bash

# Set the total number of MPI processes to run.
# Assuming you have 16 cores and you want to utilize all of them with one process per core.
export MPI_PROC_NUM=16

# Set the MPI per node to each node.
# MPI_PER_NODE should be equal to 1 or number of sockets in the system. Otherwise,
# the HPL performance will be low. 
# MPI_PER_NODE is same as -perhost or -ppn paramaters in mpirun/mpiexec
export MPI_PER_NODE=1

# Set the number of NUMA nodes per MPI.
# NUMA_PER_MPI should be equal to 1 or number of NUMA nodes in the system.
export NUMA_PER_MPI=2

# You can find description of all Intel(R) MPI Library parameters in the
# Intel(R) MPI Library Reference Manual.
export I_MPI_DAPL_DIRECT_COPY_THRESHOLD=655360

export OUT=xhpl_intel64_dynamic_outputs.txt

# Specify the executable to use.
export HPL_EXE=xhpl_intel64_dynamic

# Log the start time and system state before running the benchmark.
echo -n "This run was done on: " && date
echo -n "This run was done on: " >> $OUT
date >> $OUT
echo "HPL.dat: " >> $OUT
cat HPL.dat >> $OUT
echo "Binary name: " >> $OUT
ls -l ${HPL_EXE} >> $OUT
echo "This script: " >> $OUT
cat $0 >> $OUT  # $0 represents the script itself.
echo "Environment variables: " >> $OUT
env >> $OUT
echo "Actual run: " >> $OUT

# Execute the LINPACK benchmark with the specified number of MPI processes.
mpirun -np ${MPI_PROC_NUM} ./${HPL_EXE} "$@" | tee -a $OUT

# Log the completion time.
echo -n "Done: " >> $OUT
date >> $OUT
echo -n "Done: " && date
```

### HPL.dat

```
HPLinpack benchmark input file
Innovative Computing Laboratory, University of Tennessee
HPL.out      output file name (if any)
6            device out (6=stdout,7=stderr,file)
1            # of problems sizes (N)
1000         Ns (this is an example; adjust based on the calculation above)
1            # of NBs
192          NBs (a common choice, but you might experiment with this)
1            PMAP process mapping (0=Row-,1=Column-major)
1            # of process grids (P x Q)
4            Ps (you could also try 8 for a different P x Q configuration)
4            Qs (correspondingly, this would be 4 if you chose P as 8)
1.0          threshold
1            # of panel fact
2 1 0        PFACTs (0=left, 1=Crout, 2=Right)
1            # of recursive stopping criterium
2            NBMINs (>= 1)
1            # of panels in recursion
2            NDIVs
1            # of recursive panel fact.
1 0 2        RFACTs (0=left, 1=Crout, 2=Right)
1            # of broadcast
0            BCASTs (0=1rg,1=1rM,2=2rg,3=2rM,4=Lng,5=LnM)
1            # of lookahead depth
0            DEPTHs (>=0)
0            SWAP (0=bin-exch,1=long,2=mix)
1            swapping threshold
1            L1 in (0=transposed,1=no-transposed) form
1            U  in (0=transposed,1=no-transposed) form
0            Equilibration (0=no,1=yes)
8            memory alignment in double (> 0)
```

### Results

```
This run was done on: Thu Mar 21 10:02:20 CDT 2024
[0] MPI startup(): I_MPI_DAPL_DIRECT_COPY_THRESHOLD variable has been removed from the product, its value is ignored

================================================================================
HPLinpack 2.3  --  High-Performance Linpack benchmark  --   December 2, 2018
Written by A. Petitet and R. Clint Whaley,  Innovative Computing Laboratory, UTK
Modified by Piotr Luszczek, Innovative Computing Laboratory, UTK
Modified by Julien Langou, University of Colorado Denver
================================================================================

An explanation of the input/output parameters follows:
T/V    : Wall time / encoded variant.
N      : The order of the coefficient matrix A.
NB     : The partitioning blocking factor.
P      : The number of process rows.
Q      : The number of process columns.
Time   : Time in seconds to solve the linear system.
Gflops : Rate of execution for solving the linear system.

The following parameter values will be used:

N        :    1000 
NB       :     192 
PMAP     : Column-major process mapping
P        :       4 
Q        :       4 
PFACT    :   Right 
NBMIN    :       2 
NDIV     :       2 
RFACT    :   Crout 
BCAST    :   1ring 
DEPTH    :       0 
SWAP     : Binary-exchange
L1       : no-transposed form
U        : no-transposed form
EQUIL    : no
ALIGN    :    8 double precision words

--------------------------------------------------------------------------------

- The matrix A is randomly generated for each test.
- The following scaled residual check will be computed:
      ||Ax-b||_oo / ( eps * ( || x ||_oo * || A ||_oo + || b ||_oo ) * N )
- The relative machine precision (eps) is taken to be               1.110223e-16
- Computational tests pass if scaled residuals are less than                 1.0

z1-34           : Column=000192 Fraction=0.005 Kernel=    0.00 Mflops=    7.70
z1-34           : Column=000384 Fraction=0.195 Kernel=    4.59 Mflops=    6.11
z1-34           : Column=000576 Fraction=0.385 Kernel=    2.50 Mflops=    4.91
z1-35           : Column=000768 Fraction=0.595 Kernel=    1.11 Mflops=    4.03
z1-35           : Column=000960 Fraction=0.795 Kernel=    0.20 Mflops=    3.25
================================================================================
T/V                N    NB     P     Q               Time                 Gflops
--------------------------------------------------------------------------------
WC00C2R2        1000   192     4     4             216.77            3.08243e-03
HPL_pdgesv() start time Thu Mar 21 10:02:27 2024

HPL_pdgesv() end time   Thu Mar 21 10:06:04 2024

--------------------------------------------------------------------------------
||Ax-b||_oo/(eps*(||A||_oo*||x||_oo+||b||_oo)*N)=   5.58840572e-03 ...... PASSED
================================================================================

Finished      1 tests with the following results:
              1 tests completed and passed residual checks,
              0 tests completed and failed residual checks,
              0 tests skipped because of illegal input values.
--------------------------------------------------------------------------------

End of Tests.
================================================================================
Done: Thu Mar 21 10:06:09 CDT 2024
```

## Run 3: Thu Mar 21 10:10:32 CDT 2024

### Versions

- Intel MKL version: benchmarks_2024.0
- Intel MPI version: intel/mpi/2019u12
  - This was the most recent version available

### Notes

- On this run I tried increasing N to 2000 and that did dramatically increase performance, but still well short of expected.

### SLURM Job

```
#SBATCH --job-name=linpack
#SBATCH --output=linpack_%j.out
#SBATCH --partition=8480         # Specify the partition
#SBATCH --nodes=2               # Adjust based on how many nodes you want to use
#SBATCH --ntasks-per-node=8     # Assuming you want to utilize all cores
#SBATCH --time=0:05:00          # Set the time limit; adjust as necessary
#SBATCH --exclusive              # Optional: Request exclusive access to the nodes

# Load the Intel MPI module
module load intel/mpi/2019u12

# Navigate to the directory containing the LINPACK files
cd /home/grant/benchmarks_2024.0/linux/share/mkl/benchmarks/mp_linpack

# Run the LINPACK benchmark
bash runme_intel64_dynamic
```

### runme

```bash
#!/bin/bash

# Set the total number of MPI processes to run.
# Assuming you have 16 cores and you want to utilize all of them with one process per core.
export MPI_PROC_NUM=16

# Set the MPI per node to each node.
# MPI_PER_NODE should be equal to 1 or number of sockets in the system. Otherwise,
# the HPL performance will be low. 
# MPI_PER_NODE is same as -perhost or -ppn paramaters in mpirun/mpiexec
export MPI_PER_NODE=1

# Set the number of NUMA nodes per MPI.
# NUMA_PER_MPI should be equal to 1 or number of NUMA nodes in the system.
export NUMA_PER_MPI=2

# You can find description of all Intel(R) MPI Library parameters in the
# Intel(R) MPI Library Reference Manual.
export I_MPI_DAPL_DIRECT_COPY_THRESHOLD=655360

export OUT=xhpl_intel64_dynamic_outputs.txt

# Specify the executable to use.
export HPL_EXE=xhpl_intel64_dynamic

# Log the start time and system state before running the benchmark.
echo -n "This run was done on: " && date
echo -n "This run was done on: " >> $OUT
date >> $OUT
echo "HPL.dat: " >> $OUT
cat HPL.dat >> $OUT
echo "Binary name: " >> $OUT
ls -l ${HPL_EXE} >> $OUT
echo "This script: " >> $OUT
cat $0 >> $OUT  # $0 represents the script itself.
echo "Environment variables: " >> $OUT
env >> $OUT
echo "Actual run: " >> $OUT

# Execute the LINPACK benchmark with the specified number of MPI processes.
mpirun -np ${MPI_PROC_NUM} ./${HPL_EXE} "$@" | tee -a $OUT

# Log the completion time.
echo -n "Done: " >> $OUT
date >> $OUT
echo -n "Done: " && date
```

### HPL.dat

```
HPLinpack benchmark input file
Innovative Computing Laboratory, University of Tennessee
HPL.out      output file name (if any)
6            device out (6=stdout,7=stderr,file)
1            # of problems sizes (N)
2000         Ns (this is an example; adjust based on the calculation above)
1            # of NBs
192          NBs (a common choice, but you might experiment with this)
1            PMAP process mapping (0=Row-,1=Column-major)
1            # of process grids (P x Q)
4            Ps (you could also try 8 for a different P x Q configuration)
4            Qs (correspondingly, this would be 4 if you chose P as 8)
1.0          threshold
1            # of panel fact
2 1 0        PFACTs (0=left, 1=Crout, 2=Right)
1            # of recursive stopping criterium
2            NBMINs (>= 1)
1            # of panels in recursion
2            NDIVs
1            # of recursive panel fact.
1 0 2        RFACTs (0=left, 1=Crout, 2=Right)
1            # of broadcast
0            BCASTs (0=1rg,1=1rM,2=2rg,3=2rM,4=Lng,5=LnM)
1            # of lookahead depth
0            DEPTHs (>=0)
0            SWAP (0=bin-exch,1=long,2=mix)
1            swapping threshold
1            L1 in (0=transposed,1=no-transposed) form
1            U  in (0=transposed,1=no-transposed) form
0            Equilibration (0=no,1=yes)
8            memory alignment in double (> 0)
```

### Results

```
This run was done on: Thu Mar 21 10:10:32 CDT 2024
[0] MPI startup(): I_MPI_DAPL_DIRECT_COPY_THRESHOLD variable has been removed from the product, its value is ignored

================================================================================
HPLinpack 2.3  --  High-Performance Linpack benchmark  --   December 2, 2018
Written by A. Petitet and R. Clint Whaley,  Innovative Computing Laboratory, UTK
Modified by Piotr Luszczek, Innovative Computing Laboratory, UTK
Modified by Julien Langou, University of Colorado Denver
================================================================================

An explanation of the input/output parameters follows:
T/V    : Wall time / encoded variant.
N      : The order of the coefficient matrix A.
NB     : The partitioning blocking factor.
P      : The number of process rows.
Q      : The number of process columns.
Time   : Time in seconds to solve the linear system.
Gflops : Rate of execution for solving the linear system.

The following parameter values will be used:

N        :    2000 
NB       :     192 
PMAP     : Column-major process mapping
P        :       4 
Q        :       4 
PFACT    :   Right 
NBMIN    :       2 
NDIV     :       2 
RFACT    :   Crout 
BCAST    :   1ring 
DEPTH    :       0 
SWAP     : Binary-exchange
L1       : no-transposed form
U        : no-transposed form
EQUIL    : no
ALIGN    :    8 double precision words

--------------------------------------------------------------------------------

- The matrix A is randomly generated for each test.
- The following scaled residual check will be computed:
      ||Ax-b||_oo / ( eps * ( || x ||_oo * || A ||_oo + || b ||_oo ) * N )
- The relative machine precision (eps) is taken to be               1.110223e-16
- Computational tests pass if scaled residuals are less than                 1.0

z1-34           : Column=000192 Fraction=0.005 Kernel=    0.00 Mflops=   32.34
z1-34           : Column=000384 Fraction=0.100 Kernel=   26.35 Mflops=   29.35
z1-34           : Column=000576 Fraction=0.195 Kernel=   21.09 Mflops=   26.63
z1-35           : Column=000768 Fraction=0.290 Kernel=   15.67 Mflops=   23.91
z1-35           : Column=000960 Fraction=0.385 Kernel=   11.86 Mflops=   21.60
z1-34           : Column=001152 Fraction=0.480 Kernel=    8.30 Mflops=   19.43
z1-34           : Column=001344 Fraction=0.595 Kernel=    5.12 Mflops=   17.38
srun: Job step aborted: Waiting up to 32 seconds for job step to finish.
slurmstepd: error: *** JOB 249634 ON z1-34 CANCELLED AT 2024-03-21T10:15:59 DUE TO TIME LIMIT ***
slurmstepd: error: *** STEP 249634.0 ON z1-34 CANCELLED AT 2024-03-21T10:15:59 DUE TO TIME LIMIT ***
```

## Run 4: Thu Mar 21 16:43:18 CDT 2024

### Versions

- Intel MKL version: benchmarks_2024.0
- Intel MPI version: intel/mpi/2019u12
  - This was the most recent version available

### Notes

- Realized I had the wrong values for the two nodes. See [host info](#host-info)
- Changed slurm job `ntasks-per-node` to 112
- Updated `MPI_PROC_NUM` to 112
- Updated `MPI_PER_NODE` to 56
- Updated `NUMA_PER_MPI` to 2

### SLURM Job

```
#SBATCH --job-name=linpack
#SBATCH --output=linpack_%j.out
#SBATCH --partition=8480             # Specify the partition
#SBATCH --nodes=2                    # Number of nodes to use
#SBATCH --ntasks-per-node=112        # Use all 112 cores on each node
#SBATCH --time=0:05:00               # Time limit; adjust as needed
#SBATCH --exclusive                  # Request exclusive access to the nodes

# Load the Intel MPI module
module load intel/mpi/2019u12

# Navigate to the directory containing the LINPACK files
cd /home/grant/benchmarks_2024.0/linux/share/mkl/benchmarks/mp_linpack

# Run the LINPACK benchmark
bash runme_intel64_dynamic
```

### runme

```bash
#!/bin/bash

# Set the total number of MPI processes to run.
# Assuming you have 16 cores and you want to utilize all of them with one process per core.
export MPI_PROC_NUM=112

# Set the MPI per node to each node.
# MPI_PER_NODE should be equal to 1 or number of sockets in the system. Otherwise,
# the HPL performance will be low. 
# MPI_PER_NODE is same as -perhost or -ppn paramaters in mpirun/mpiexec
export MPI_PER_NODE=56

# Set the number of NUMA nodes per MPI.
# NUMA_PER_MPI should be equal to 1 or number of NUMA nodes in the system.
export NUMA_PER_MPI=2

export OUT=xhpl_intel64_dynamic_outputs.txt

# Specify the executable to use.
export HPL_EXE=xhpl_intel64_dynamic

# Log the start time and system state before running the benchmark.
echo -n "This run was done on: " && date
echo -n "This run was done on: " >> $OUT
date >> $OUT
echo "HPL.dat: " >> $OUT
cat HPL.dat >> $OUT
echo "Binary name: " >> $OUT
ls -l ${HPL_EXE} >> $OUT
echo "This script: " >> $OUT
cat $0 >> $OUT  # $0 represents the script itself.
echo "Environment variables: " >> $OUT
env >> $OUT
echo "Actual run: " >> $OUT

# Execute the LINPACK benchmark with the specified number of MPI processes.
mpirun -np ${MPI_PROC_NUM} ./${HPL_EXE} "$@" | tee -a $OUT

# Log the completion time.
echo -n "Done: " >> $OUT
date >> $OUT
echo -n "Done: " && date
```

### HPL.dat

```
HPLinpack benchmark input file
Innovative Computing Laboratory, University of Tennessee
HPL.out      output file name (if any)
6            device out (6=stdout,7=stderr,file)
1            # of problems sizes (N)
2000         Ns (this is an example; adjust based on the calculation above)
1            # of NBs
192          NBs (a common choice, but you might experiment with this)
1            PMAP process mapping (0=Row-,1=Column-major)
1            # of process grids (P x Q)
4            Ps (you could also try 8 for a different P x Q configuration)
4            Qs (correspondingly, this would be 4 if you chose P as 8)
1.0          threshold
1            # of panel fact
2 1 0        PFACTs (0=left, 1=Crout, 2=Right)
1            # of recursive stopping criterium
2            NBMINs (>= 1)
1            # of panels in recursion
2            NDIVs
1            # of recursive panel fact.
1 0 2        RFACTs (0=left, 1=Crout, 2=Right)
1            # of broadcast
0            BCASTs (0=1rg,1=1rM,2=2rg,3=2rM,4=Lng,5=LnM)
1            # of lookahead depth
0            DEPTHs (>=0)
0            SWAP (0=bin-exch,1=long,2=mix)
1            swapping threshold
1            L1 in (0=transposed,1=no-transposed) form
1            U  in (0=transposed,1=no-transposed) form
0            Equilibration (0=no,1=yes)
8            memory alignment in double (> 0)
```

### Results

```
tail -f -n 100 linpack_249643.out 
This run was done on: Thu Mar 21 16:43:18 CDT 2024
================================================================================
HPLinpack 2.3  --  High-Performance Linpack benchmark  --   December 2, 2018
Written by A. Petitet and R. Clint Whaley,  Innovative Computing Laboratory, UTK
Modified by Piotr Luszczek, Innovative Computing Laboratory, UTK
Modified by Julien Langou, University of Colorado Denver
================================================================================

An explanation of the input/output parameters follows:
T/V    : Wall time / encoded variant.
N      : The order of the coefficient matrix A.
NB     : The partitioning blocking factor.
P      : The number of process rows.
Q      : The number of process columns.
Time   : Time in seconds to solve the linear system.
Gflops : Rate of execution for solving the linear system.

The following parameter values will be used:

N        :    2000 
NB       :     192 
PMAP     : Column-major process mapping
P        :       4 
Q        :       4 
PFACT    :   Right 
NBMIN    :       2 
NDIV     :       2 
RFACT    :   Crout 
BCAST    :   1ring 
DEPTH    :       0 
SWAP     : Binary-exchange
L1       : no-transposed form
U        : no-transposed form
EQUIL    : no
ALIGN    :    8 double precision words

--------------------------------------------------------------------------------

- The matrix A is randomly generated for each test.
- The following scaled residual check will be computed:
      ||Ax-b||_oo / ( eps * ( || x ||_oo * || A ||_oo + || b ||_oo ) * N )
- The relative machine precision (eps) is taken to be               1.110223e-16
- Computational tests pass if scaled residuals are less than                 1.0

srun: Job step aborted: Waiting up to 32 seconds for job step to finish.
slurmstepd: error: *** JOB 249643 ON z1-33 CANCELLED AT 2024-03-21T16:48:29 DUE TO TIME LIMIT ***
slurmstepd: error: *** STEP 249643.0 ON z1-33 CANCELLED AT 2024-03-21T16:48:29 DUE TO TIME LIMIT ***
```

## Run 5: Thu Mar 21 17:00:17 CDT 2024

### Versions

- Intel MKL version: benchmarks_2024.0
- Intel MPI version: intel/mpi/2019u12
  - This was the most recent version available

### Notes

- Updated `MPI_PROC_NUM` to 224

### SLURM Job

```
#SBATCH --job-name=linpack
#SBATCH --output=linpack_%j.out
#SBATCH --partition=8480             # Specify the partition
#SBATCH --nodes=2                    # Number of nodes to use
#SBATCH --ntasks-per-node=112        # Use all 112 cores on each node
#SBATCH --time=0:05:00               # Time limit; adjust as needed
#SBATCH --exclusive                  # Request exclusive access to the nodes

# Load the Intel MPI module
module load intel/mpi/2019u12

# Navigate to the directory containing the LINPACK files
cd /home/grant/benchmarks_2024.0/linux/share/mkl/benchmarks/mp_linpack

# Run the LINPACK benchmark
bash runme_intel64_dynamic
```

### runme

```bash
#!/bin/bash

# Set the total number of MPI processes to run.
# Assuming you have 16 cores and you want to utilize all of them with one process per core.
export MPI_PROC_NUM=224

# Set the MPI per node to each node.
# MPI_PER_NODE should be equal to 1 or number of sockets in the system. Otherwise,
# the HPL performance will be low. 
# MPI_PER_NODE is same as -perhost or -ppn paramaters in mpirun/mpiexec
export MPI_PER_NODE=56

# Set the number of NUMA nodes per MPI.
# NUMA_PER_MPI should be equal to 1 or number of NUMA nodes in the system.
export NUMA_PER_MPI=1

export OUT=xhpl_intel64_dynamic_outputs.txt

# Specify the executable to use.
export HPL_EXE=xhpl_intel64_dynamic

# Log the start time and system state before running the benchmark.
echo -n "This run was done on: " && date
echo -n "This run was done on: " >> $OUT
date >> $OUT
echo "HPL.dat: " >> $OUT
cat HPL.dat >> $OUT
echo "Binary name: " >> $OUT
ls -l ${HPL_EXE} >> $OUT
echo "This script: " >> $OUT
cat $0 >> $OUT  # $0 represents the script itself.
echo "Environment variables: " >> $OUT
env >> $OUT
echo "Actual run: " >> $OUT

# Execute the LINPACK benchmark with the specified number of MPI processes.
mpirun -np ${MPI_PROC_NUM} ./${HPL_EXE} "$@" | tee -a $OUT

# Log the completion time.
echo -n "Done: " >> $OUT
date >> $OUT
echo -n "Done: " && date
```

### HPL.dat

```
HPLinpack benchmark input file
Innovative Computing Laboratory, University of Tennessee
HPL.out      output file name (if any)
6            device out (6=stdout,7=stderr,file)
1            # of problems sizes (N)
2000         Ns (this is an example; adjust based on the calculation above)
1            # of NBs
192          NBs (a common choice, but you might experiment with this)
1            PMAP process mapping (0=Row-,1=Column-major)
1            # of process grids (P x Q)
4            Ps (you could also try 8 for a different P x Q configuration)
4            Qs (correspondingly, this would be 4 if you chose P as 8)
1.0          threshold
1            # of panel fact
2 1 0        PFACTs (0=left, 1=Crout, 2=Right)
1            # of recursive stopping criterium
2            NBMINs (>= 1)
1            # of panels in recursion
2            NDIVs
1            # of recursive panel fact.
1 0 2        RFACTs (0=left, 1=Crout, 2=Right)
1            # of broadcast
0            BCASTs (0=1rg,1=1rM,2=2rg,3=2rM,4=Lng,5=LnM)
1            # of lookahead depth
0            DEPTHs (>=0)
0            SWAP (0=bin-exch,1=long,2=mix)
1            swapping threshold
1            L1 in (0=transposed,1=no-transposed) form
1            U  in (0=transposed,1=no-transposed) form
0            Equilibration (0=no,1=yes)
8            memory alignment in double (> 0)
```

### Results

```
This run was done on: Thu Mar 21 17:00:17 CDT 2024
================================================================================
HPLinpack 2.3  --  High-Performance Linpack benchmark  --   December 2, 2018
Written by A. Petitet and R. Clint Whaley,  Innovative Computing Laboratory, UTK
Modified by Piotr Luszczek, Innovative Computing Laboratory, UTK
Modified by Julien Langou, University of Colorado Denver
================================================================================

An explanation of the input/output parameters follows:
T/V    : Wall time / encoded variant.
N      : The order of the coefficient matrix A.
NB     : The partitioning blocking factor.
P      : The number of process rows.
Q      : The number of process columns.
Time   : Time in seconds to solve the linear system.
Gflops : Rate of execution for solving the linear system.

The following parameter values will be used:

N        :    2000 
NB       :     192 
PMAP     : Column-major process mapping
P        :      14 
Q        :      16 
PFACT    :   Right 
NBMIN    :       2 
NDIV     :       2 
RFACT    :   Crout 
BCAST    :   1ring 
DEPTH    :       0 
SWAP     : Binary-exchange
L1       : no-transposed form
U        : no-transposed form
EQUIL    : no
ALIGN    :    8 double precision words

--------------------------------------------------------------------------------

- The matrix A is randomly generated for each test.
- The following scaled residual check will be computed:
      ||Ax-b||_oo / ( eps * ( || x ||_oo * || A ||_oo + || b ||_oo ) * N )
- The relative machine precision (eps) is taken to be               1.110223e-16
- Computational tests pass if scaled residuals are less than                 1.0

srun: Job step aborted: Waiting up to 32 seconds for job step to finish.
slurmstepd: error: *** JOB 249647 ON z1-33 CANCELLED AT 2024-03-21T17:05:29 DUE TO TIME LIMIT ***
slurmstepd: error: *** STEP 249647.0 ON z1-33 CANCELLED AT 2024-03-21T17:05:29 DUE TO TIME LIMIT ***
```

## Run 6: Fri Mar 22 10:35:12 CDT 2024

### Versions

- Intel MKL version: 2023.0.0
- Intel MPI version: intel/mpi/2019u12
  - This was the most recent version available

### Notes

- Swapped everything to use colleague's config. Changed all options. See below.

### SLURM Job

```
#!/bin/bash
#SBATCH --job-name=linpack
#SBATCH --output=linpack_%j.out
#SBATCH --partition=8480    # Specify your partition
#SBATCH --nodes=2                     # Number of nodes
#SBATCH --ntasks-per-node=8           # Number of tasks (MPI processes) per node
#SBATCH --time=0:30:00                # Time limit in the format hours:minutes:seconds

# Load the required modules
module load intel/oneAPI/2023.0.0
module load compiler-rt/2023.0.0 mkl/2023.0.0 mpi/2021.8.0

# Navigate to the directory containing your HPL files
cd /home/grant/mp_linpack

# Run the HPL benchmark
bash runme_intel64_dynamic
```

### runme

```bash
#!/bin/bash
#===============================================================================
# Copyright 2001-2021 Intel Corporation.
#
# This software and the related documents are Intel copyrighted  materials,  and
# your use of  them is  governed by the  express license  under which  they were
# provided to you (License).  Unless the License provides otherwise, you may not
# use, modify, copy, publish, distribute,  disclose or transmit this software or
# the related documents without Intel's prior written permission.
#
# This software and the related documents  are provided as  is,  with no express
# or implied  warranties,  other  than those  that are  expressly stated  in the
# License.
#===============================================================================
#SBATCH -p 8480
#SBATCH -N 1
#SBATCH -t 06:00:00
#SBATCH -J HPL_8480
#SBATCH -o HPL_8480x1.%N.o%j

# Set total number of MPI processes for the HPL (should be equal to PxQ).
export MPI_PROC_NUM=8

# Set the MPI per node to each node.
# MPI_PER_NODE should be equal to 1 or number of sockets in the system. Otherwise,
# the HPL performance will be low.
# MPI_PER_NODE is same as -perhost or -ppn paramaters in mpirun/mpiexec
export MPI_PER_NODE=2

# Set the number of NUMA nodes per MPI.
# NUMA_PER_MPI should be equal to 1 or number of NUMA nodes in the system.
export NUMA_PER_MPI=1

#
# You can find description of all Intel(R) MPI Library parameters in the
# Intel(R) MPI Library Reference Manual.
export I_MPI_DAPL_DIRECT_COPY_THRESHOLD=655360

#         "export I_MPI_PIN_CELL=core"
#         You can use this variable (beginning Intel(R) MPI Library 4.0.1) for cases
#         if HT is enabled.
#         The variable forces to pin MPI processes and threads to real cores,
#         so logical processors will not be involved.
#         It can be used together with the variable below, when Hydra Process Manager:
#         "export I_MPI_PIN_DOMAIN=auto" This allows uniform distribution of
#             the processes and thread domains

# export I_MPI_EAGER_THRESHOLD=128000
#          This setting may give 1-2% of performance increase over the
#          default value of 262000 for large problems and high number of cores

export I_MPI_THREAD_MAX=56
export OUT=xhpl_intel64_dynamic_outputs.txt
export HPL_EXE=xhpl_intel64_dynamic

echo -n "This run was done on: "
date

# Capture some meaningful data for future reference:
echo -n "This run was done on: " >> $OUT
date >> $OUT
echo "HPL.dat: " >> $OUT
cat HPL.dat >> $OUT
echo "Binary name: " >> $OUT
ls -l xhpl_intel64_dynamic >> $OUT
echo "This script: " >> $OUT
cat runme_intel64_dynamic_8480 >> $OUT
echo "Environment variables: " >> $OUT
env >> $OUT
echo "Actual run: " >> $OUT

# Load power tracking module
module load sysinfo
power-reset
power-report

date

# Environment variables can also be also be set on the Intel(R) MPI Library command
# line using the -genv option (to appear before the -np 1):

# mpirun -np ${MPI_PROC_NUM} ./runme_intel64_prv "$@" | tee -a $OUT

# In case of multiple nodes involved, please set the number of MPI processes
# per node (ppn=1,2 typically) through the -perhost option (because the
# default is all cores):

#mpirun -perhost ${MPI_PER_NODE} -np ${MPI_PROC_NUM} ./runme_intel64_prv "$@" | tee -a $OUT
#mpirun -perhost ${MPI_PER_NODE} -np ${MPI_PROC_NUM} ./xhpl_intel64_dynamic -n 234240 -b 384 -p 1 -q 1
mpirun -perhost ${MPI_PER_NODE} -np ${MPI_PROC_NUM} ./runme_intel64_prv -n 117120 -b 384 -p 2 -q 4

#Show power usage after completion
date
power-report

echo -n "Done: " >> $OUT
date >> $OUT

echo -n "Done: "
date
```

### HPL.dat

Parameters provided via the run file.

### Results

```
Loading compiler-rt version 2023.0.0
Loading mkl version 2023.0.0
Loading tbb version 2021.8.0
Loading mpi version 2021.8.0
This run was done on: Fri Mar 22 10:35:05 CDT 2024
cat: runme_intel64_dynamic_8480: No such file or directory
[Key=system.Embedded.1#ServerPwrMon.1]
Object value modified successfully

#Avg.LastDay=602 W | 2055 Btu/hr
#Avg.LastHour=631 W | 2154 Btu/hr
#Avg.LastWeek=642 W | 2191 Btu/hr
#Cap.ActivePolicy.BtuHr=111834 Btu/hr
#Cap.ActivePolicy.Name=
#Cap.ActivePolicy.Watts=32767 W
Cap.BtuHr=111834 btu/hr
Cap.Enable=Disabled
#Cap.MaxThreshold=1220 W | 4165 Btu/hr
#Cap.MinThreshold=516 W | 1762 Btu/hr
Cap.Percent=100
Cap.Watts=32767 W
#EnergyConsumption=2702.191 KWh | 9222578 Btu
#EnergyConsumption.Clear=******** (Write-Only)
#EnergyConsumption.StarttimeStamp=Thu Nov 03 10:14:05 2022
#Max.Amps=6.3 Amps
#Max.Amps.Timestamp=Mon Feb 12 18:35:01 2024
#Max.Headroom=0 W | 0 Btu/hr
#Max.LastDay=1207 W | 4119 Btu/hr
#Max.LastDay.Timestamp=Fri Mar 22 15:57:39 2024
#Max.LastHour=1207 W | 4119 Btu/hr
#Max.LastHour.Timestamp=Fri Mar 22 15:57:39 2024
#Max.LastWeek=1278 W | 4362 Btu/hr
#Max.LastWeek.Timestamp=Tue Mar 19 15:01:01 2024
#Max.Power=1306 W | 4457 Btu/hr
#Max.Power.Timestamp=Mon Feb 12 18:35:00 2024
#Max.PowerClear=******** (Write-Only)
#Min.LastDay=598 W | 2041 Btu/hr
#Min.LastDay.Timestamp=Fri Mar 22 01:28:19 2024
#Min.LastHour=599 W | 2044 Btu/hr
#Min.LastHour.Timestamp=Fri Mar 22 15:36:53 2024
#Min.LastWeek=593 W | 2024 Btu/hr
#Min.LastWeek.Timestamp=Tue Mar 19 19:23:55 2024
#PCIeAllocation=0
#Realtime.Amps=2.9 Amps
#Realtime.Power=605 W | 2065 Btu/hr
RedundancyPolicy=Not Redundant
#SCViewSledPwr=615
#ServerAllocation=658 W | 2246 Btu/hr
#Status=1

#ActivePolicyName=
#ActivePowerCapVal=32767
ChassisCurrentCapLimit=0
ChassisCurrentCapSetting=Disabled
GridACurrentCapLimit=1000000
GridACurrentCapSetting=Disabled
GridBCurrentCapLimit=1000000
GridBCurrentCapSetting=Disabled
GridCurrentCapLimit=0
GridCurrentCapSetting=Disabled
#GridCurrentLimitLowerBound=0
#GridCurrentLimitUpperBound=1000000
#PowerCapMaxThres=1220
#PowerCapMinThres=516
PowerCapSetting=Disabled
PowerCapValue=32767
Poweredbyparent=PoweredByChassis
PSRedPolicy=Not Redundant
#SCViewSledPwr=615
SystemCurrentCapLimit=1000000
SystemCurrentCapSetting=Disabled
#SystemCurrentLimitLowerBound=0
#SystemCurrentLimitUpperBound=1000000

[Key=system.Embedded.1#ServerPwrMon.1]
#AccumulativePower=0
#CumulativePowerStartTime=1711143252
#CumulativePowerStartTimeStr=2024-03-22T21:34:12Z
#MinPowerTime=1711143254
#MinPowerTimeStr=2024-03-22T21:34:14Z
#MinPowerWatts=601
#PeakCurrentTime=0
#PeakCurrentTimeStr=2024-03-22T21:34:12Z
#PeakPowerStartTime=1711143252
#PeakPowerStartTimeStr=2024-03-22T21:34:12Z
#PeakPowerTime=1711143254
#PeakPowerTimeStr=2024-03-22T21:34:14Z
#PeakPowerWatts=604
PowerConfigReset=None

PS1 Status                      Present                  AC             1082.000Watts  
PS2 Status                      Present                  AC             1068.000Watts  
PS1 Voltage 1                   Ok          204.00V             NA          NA          
PS2 Voltage 2                   Ok          204.00V             NA          NA          
PS1 Current 1                 Ok      5.4Amps  NA   NA       0Amps [N]      0Amps [N]
PS2 Current 2                 Ok      5.4Amps  NA   NA       0Amps [N]      0Amps [N]

Duration Above Warning Threshold as Percentage = 0.0%
Duration Above Critical Threshold as Percentage = 0.0%

Average Temperatures
Last Hour  = 20C ( 68.0F )
Last Day   = 20C ( 68.0F )
Last Week  = 20C ( 68.0F )
Last Month = 20C ( 68.0F )
Last Year  = 20C ( 68.0F )

Peak Temperatures
Last Hour  = 21C ( 69.8F ) [At Fri, 22 Mar 2024 15:57:41]
Last Day   = 22C ( 71.6F ) [At Thu, 21 Mar 2024 20:16:51]
Last Week  = 22C ( 71.6F ) [At Thu, 21 Mar 2024 20:16:51]
Last Month = 23C ( 73.4F ) [At Tue, 12 Mar 2024 15:33:35]
Last Year  = 34C ( 93.2F ) [At Wed, 06 Dec 2023 13:46:21]

Fri Mar 22 10:35:12 CDT 2024
RANK=5, NODE=5-5
RANK=3, NODE=3-3
RANK=0, NODE=0-0
RANK=1, NODE=1-1
RANK=6, NODE=6-6
RANK=2, NODE=2-2
RANK=7, NODE=7-7
RANK=4, NODE=4-4
MPI startup(): I_MPI_DAPL_DIRECT_COPY_THRESHOLD variable has been removed from the product, its value is ignored

================================================================================
HPLinpack 2.3  --  High-Performance Linpack benchmark  --   December 2, 2018
Written by A. Petitet and R. Clint Whaley,  Innovative Computing Laboratory, UTK
Modified by Piotr Luszczek, Innovative Computing Laboratory, UTK
Modified by Julien Langou, University of Colorado Denver
================================================================================

An explanation of the input/output parameters follows:
T/V    : Wall time / encoded variant.
N      : The order of the coefficient matrix A.
NB     : The partitioning blocking factor.
P      : The number of process rows.
Q      : The number of process columns.
Time   : Time in seconds to solve the linear system.
Gflops : Rate of execution for solving the linear system.

The following parameter values will be used:

N        :  117120 
NB       :     384 
PMAP     : Column-major process mapping
P        :       2 
Q        :       4 
PFACT    :   Right 
NBMIN    :       2 
NDIV     :       2 
RFACT    :   Crout 
BCAST    :   1ring 
DEPTH    :       0 
SWAP     : Binary-exchange
L1       : no-transposed form
U        : no-transposed form
EQUIL    : no
ALIGN    :    8 double precision words

--------------------------------------------------------------------------------

- The matrix A is randomly generated for each test.
- The following scaled residual check will be computed:
      ||Ax-b||_oo / ( eps * ( || x ||_oo * || A ||_oo + || b ||_oo ) * N )
- The relative machine precision (eps) is taken to be               1.110223e-16
- Computational tests pass if scaled residuals are less than                16.0

z5-01           : Column=000768 Fraction=0.005 Kernel=    0.61 Mflops=11987977.79
z5-01           : Column=001536 Fraction=0.010 Kernel=7545020.78 Mflops=9230173.45
z5-02           : Column=001920 Fraction=0.015 Kernel=7488359.30 Mflops=8824061.02
z5-02           : Column=002688 Fraction=0.020 Kernel=7397213.04 Mflops=8385114.11
z5-01           : Column=003072 Fraction=0.025 Kernel=7446258.78 Mflops=8196286.65
z5-01           : Column=003840 Fraction=0.030 Kernel=7399457.17 Mflops=8019276.88
z5-02           : Column=004224 Fraction=0.035 Kernel=7471440.93 Mflops=8001270.50
z5-02           : Column=004992 Fraction=0.040 Kernel=7457425.04 Mflops=7890440.78
z5-01           : Column=005376 Fraction=0.045 Kernel=7306451.47 Mflops=7814816.95
z5-01           : Column=006144 Fraction=0.050 Kernel=7240127.10 Mflops=7778470.50
z5-02           : Column=006528 Fraction=0.055 Kernel=7344247.60 Mflops=7754625.15
z5-02           : Column=007296 Fraction=0.060 Kernel=7393439.49 Mflops=7733418.78
z5-01           : Column=007680 Fraction=0.065 Kernel=7647997.96 Mflops=7717903.98
z5-01           : Column=008448 Fraction=0.070 Kernel=7354742.68 Mflops=7666918.02
z5-02           : Column=008832 Fraction=0.075 Kernel=7196567.01 Mflops=7669991.08
z5-02           : Column=009600 Fraction=0.080 Kernel=7379873.95 Mflops=7645544.15
z5-01           : Column=009984 Fraction=0.085 Kernel=7634805.68 Mflops=7624709.64
z5-01           : Column=010752 Fraction=0.090 Kernel=7627455.11 Mflops=7624049.93
z5-02           : Column=011136 Fraction=0.095 Kernel=6938889.52 Mflops=7599516.69
z5-02           : Column=011904 Fraction=0.100 Kernel=7432040.48 Mflops=7603752.33
z5-02           : Column=012672 Fraction=0.105 Kernel=7361379.27 Mflops=7583218.05
z5-01           : Column=013056 Fraction=0.110 Kernel=7465710.92 Mflops=7569460.06
z5-01           : Column=013824 Fraction=0.115 Kernel=7548266.67 Mflops=7567271.65
z5-02           : Column=014208 Fraction=0.120 Kernel=7359735.23 Mflops=7555452.03
z5-02           : Column=014976 Fraction=0.125 Kernel=7379175.87 Mflops=7555304.14
z5-01           : Column=015360 Fraction=0.130 Kernel=7318291.41 Mflops=7549161.53
z5-01           : Column=016128 Fraction=0.135 Kernel=7253666.34 Mflops=7528579.82
z5-02           : Column=016512 Fraction=0.140 Kernel=7349104.64 Mflops=7539401.68
z5-02           : Column=017280 Fraction=0.145 Kernel=7338704.06 Mflops=7521538.32
z5-01           : Column=017664 Fraction=0.150 Kernel=7155014.33 Mflops=7514863.81
z5-01           : Column=018432 Fraction=0.155 Kernel=7477300.48 Mflops=7523635.82
z5-02           : Column=018816 Fraction=0.160 Kernel=7559612.35 Mflops=7512996.43
z5-02           : Column=019584 Fraction=0.165 Kernel=7365942.08 Mflops=7511485.33
z5-01           : Column=019968 Fraction=0.170 Kernel=6995457.65 Mflops=7503012.25
z5-01           : Column=020736 Fraction=0.175 Kernel=7310397.21 Mflops=7495634.49
z5-02           : Column=021120 Fraction=0.180 Kernel=7131068.42 Mflops=7498380.37
z5-02           : Column=021888 Fraction=0.185 Kernel=7219801.45 Mflops=7488524.52
z5-01           : Column=022272 Fraction=0.190 Kernel=7550313.90 Mflops=7489564.61
z5-01           : Column=023040 Fraction=0.195 Kernel=7493624.09 Mflops=7490032.57
z5-01           : Column=023808 Fraction=0.200 Kernel=7431285.00 Mflops=7477955.97
z5-02           : Column=024192 Fraction=0.205 Kernel=7365733.18 Mflops=7483290.31
z5-02           : Column=024960 Fraction=0.210 Kernel=7333889.76 Mflops=7473058.57
z5-01           : Column=025344 Fraction=0.215 Kernel=7320082.13 Mflops=7471482.91
z5-01           : Column=026112 Fraction=0.220 Kernel=7511626.45 Mflops=7472959.36
z5-02           : Column=026496 Fraction=0.225 Kernel=7424954.45 Mflops=7469053.55
z5-02           : Column=027264 Fraction=0.230 Kernel=7440171.89 Mflops=7469228.61
z5-01           : Column=027648 Fraction=0.235 Kernel=7150456.72 Mflops=7462710.33
z5-01           : Column=028416 Fraction=0.240 Kernel=7397453.02 Mflops=7457491.57
z5-02           : Column=028800 Fraction=0.245 Kernel=7202612.14 Mflops=7460784.02
z5-02           : Column=029568 Fraction=0.250 Kernel=7382221.24 Mflops=7456223.52
z5-01           : Column=029952 Fraction=0.255 Kernel=7069241.49 Mflops=7451035.50
z5-01           : Column=030720 Fraction=0.260 Kernel=7588703.38 Mflops=7454468.70
z5-02           : Column=031104 Fraction=0.265 Kernel=7480895.15 Mflops=7448777.44
z5-02           : Column=031872 Fraction=0.270 Kernel=7184295.96 Mflops=7447157.20
z5-01           : Column=032256 Fraction=0.275 Kernel=7583990.16 Mflops=7447330.81
z5-01           : Column=033024 Fraction=0.280 Kernel=7516801.76 Mflops=7440618.67
z5-02           : Column=033408 Fraction=0.285 Kernel=7444719.39 Mflops=7442437.86
z5-02           : Column=034176 Fraction=0.290 Kernel=7227329.87 Mflops=7437599.24
z5-01           : Column=034560 Fraction=0.295 Kernel=7397675.78 Mflops=7433386.64
z5-01           : Column=035328 Fraction=0.300 Kernel=7327943.78 Mflops=7432727.26
z5-01           : Column=036096 Fraction=0.305 Kernel=7259895.86 Mflops=7429266.18
z5-02           : Column=036480 Fraction=0.310 Kernel=7144532.78 Mflops=7431947.88
z5-02           : Column=037248 Fraction=0.315 Kernel=7447001.38 Mflops=7430187.14
z5-01           : Column=037632 Fraction=0.320 Kernel=7633500.68 Mflops=7425184.34
z5-01           : Column=038400 Fraction=0.325 Kernel=7506550.66 Mflops=7423687.77
z5-02           : Column=038784 Fraction=0.330 Kernel=6995591.62 Mflops=7420296.50
z5-02           : Column=039552 Fraction=0.335 Kernel=7223283.02 Mflops=7421704.15
z5-01           : Column=039936 Fraction=0.340 Kernel=6943770.41 Mflops=7417475.87
z5-01           : Column=040704 Fraction=0.345 Kernel=7238291.61 Mflops=7414468.13
z5-02           : Column=041088 Fraction=0.350 Kernel=7220214.10 Mflops=7416843.60
z5-02           : Column=041856 Fraction=0.355 Kernel=7216516.68 Mflops=7413459.50
z5-01           : Column=042240 Fraction=0.360 Kernel=7421079.53 Mflops=7409985.79
z5-01           : Column=043008 Fraction=0.365 Kernel=7549820.06 Mflops=7412351.03
z5-02           : Column=043392 Fraction=0.370 Kernel=7366151.02 Mflops=7407036.14
z5-02           : Column=044160 Fraction=0.375 Kernel=7176290.27 Mflops=7407577.08
z5-01           : Column=044544 Fraction=0.380 Kernel=7146086.02 Mflops=7406628.19
z5-01           : Column=045312 Fraction=0.385 Kernel=7332819.11 Mflops=7401562.93
z5-02           : Column=045696 Fraction=0.390 Kernel=7242854.58 Mflops=7403724.03
z5-02           : Column=046464 Fraction=0.395 Kernel=7226363.09 Mflops=7399578.97
z5-02           : Column=047232 Fraction=0.400 Kernel=7274222.34 Mflops=7400716.21
z5-01           : Column=047616 Fraction=0.405 Kernel=7644082.97 Mflops=7398856.43
z5-01           : Column=048384 Fraction=0.410 Kernel=7047806.95 Mflops=7392503.77
z5-02           : Column=048768 Fraction=0.415 Kernel=7112535.16 Mflops=7396704.35
z5-02           : Column=049536 Fraction=0.420 Kernel=6931611.91 Mflops=7391121.87
z5-01           : Column=049920 Fraction=0.425 Kernel=6924165.61 Mflops=7388668.09
z5-01           : Column=050688 Fraction=0.430 Kernel=7310821.04 Mflops=7388826.55
z5-02           : Column=051072 Fraction=0.435 Kernel=7685832.97 Mflops=7389420.09
z5-02           : Column=051840 Fraction=0.440 Kernel=7219502.64 Mflops=7389091.35
z5-01           : Column=052224 Fraction=0.445 Kernel=6724635.99 Mflops=7385661.28
z5-01           : Column=052992 Fraction=0.450 Kernel=7065953.93 Mflops=7382441.14
z5-02           : Column=053376 Fraction=0.455 Kernel=6872925.72 Mflops=7384465.72
z5-02           : Column=054144 Fraction=0.460 Kernel=7015032.01 Mflops=7380001.46
z5-01           : Column=054528 Fraction=0.465 Kernel=7439010.33 Mflops=7379932.74
z5-01           : Column=055296 Fraction=0.470 Kernel=7130450.15 Mflops=7379023.02
z5-02           : Column=055680 Fraction=0.475 Kernel=6541440.45 Mflops=7375897.92
z5-02           : Column=056448 Fraction=0.480 Kernel=7210253.19 Mflops=7378083.31
z5-01           : Column=056832 Fraction=0.485 Kernel=7185541.53 Mflops=7374896.52
z5-01           : Column=057600 Fraction=0.490 Kernel=7096126.79 Mflops=7372386.74
z5-02           : Column=057984 Fraction=0.495 Kernel=7074301.87 Mflops=7374260.27
z5-01           : Column=060672 Fraction=0.515 Kernel=7146680.42 Mflops=7366893.43
z5-01           : Column=062976 Fraction=0.535 Kernel=6938790.51 Mflops=7361531.73
z5-01           : Column=065280 Fraction=0.555 Kernel=7037648.06 Mflops=7356222.33
z5-01           : Column=067584 Fraction=0.575 Kernel=6952790.97 Mflops=7351952.29
z5-01           : Column=069888 Fraction=0.595 Kernel=6864673.56 Mflops=7345476.69
z5-01           : Column=072192 Fraction=0.615 Kernel=6976839.69 Mflops=7342441.30
z5-01           : Column=074496 Fraction=0.635 Kernel=6871015.06 Mflops=7337243.72
z5-01           : Column=076800 Fraction=0.655 Kernel=6860187.18 Mflops=7334129.19
z5-01           : Column=079104 Fraction=0.675 Kernel=6881044.89 Mflops=7329170.88
z5-01           : Column=081408 Fraction=0.695 Kernel=6772858.30 Mflops=7326351.88
z5-02           : Column=093312 Fraction=0.795 Kernel=6399710.25 Mflops=7305261.06
z5-02           : Column=104832 Fraction=0.895 Kernel=4660063.63 Mflops=7274269.34
z5-01           : Column=116736 Fraction=0.995 Kernel=1701126.50 Mflops=7246860.83
================================================================================
T/V                N    NB     P     Q               Time                 Gflops
--------------------------------------------------------------------------------
WC00C2R2      117120   384     2     4             147.94            7.23977e+03
HPL_pdgesv() start time Fri Mar 22 10:35:22 2024

HPL_pdgesv() end time   Fri Mar 22 10:37:50 2024

--------------------------------------------------------------------------------
||Ax-b||_oo/(eps*(||A||_oo*||x||_oo+||b||_oo)*N)=   2.58015925e-03 ...... PASSED
================================================================================

Finished      1 tests with the following results:
              1 tests completed and passed residual checks,
              0 tests completed and failed residual checks,
              0 tests skipped because of illegal input values.
--------------------------------------------------------------------------------

End of Tests.
================================================================================
Fri Mar 22 10:37:55 CDT 2024
#Avg.LastDay=602 W | 2055 Btu/hr
#Avg.LastHour=641 W | 2188 Btu/hr
#Avg.LastWeek=642 W | 2191 Btu/hr
#Cap.ActivePolicy.BtuHr=111834 Btu/hr
#Cap.ActivePolicy.Name=
#Cap.ActivePolicy.Watts=32767 W
Cap.BtuHr=111834 btu/hr
Cap.Enable=Disabled
#Cap.MaxThreshold=1220 W | 4165 Btu/hr
#Cap.MinThreshold=516 W | 1762 Btu/hr
Cap.Percent=100
Cap.Watts=32767 W
#EnergyConsumption=0.035 KWh | 119 Btu
#EnergyConsumption.Clear=******** (Write-Only)
#EnergyConsumption.StarttimeStamp=Fri Mar 22 16:34:12 2024
#Max.Amps=4.8 Amps
#Max.Amps.Timestamp=Fri Mar 22 16:36:09 2024
#Max.Headroom=41 W | 140 Btu/hr
#Max.LastDay=1207 W | 4119 Btu/hr
#Max.LastDay.Timestamp=Fri Mar 22 15:57:39 2024
#Max.LastHour=1207 W | 4119 Btu/hr
#Max.LastHour.Timestamp=Fri Mar 22 15:57:39 2024
#Max.LastWeek=1278 W | 4362 Btu/hr
#Max.LastWeek.Timestamp=Tue Mar 19 15:01:01 2024
#Max.Power=996 W | 3399 Btu/hr
#Max.Power.Timestamp=Fri Mar 22 16:36:09 2024
#Max.PowerClear=******** (Write-Only)
#Min.LastDay=598 W | 2041 Btu/hr
#Min.LastDay.Timestamp=Fri Mar 22 01:28:19 2024
#Min.LastHour=599 W | 2044 Btu/hr
#Min.LastHour.Timestamp=Fri Mar 22 15:36:53 2024
#Min.LastWeek=593 W | 2024 Btu/hr
#Min.LastWeek.Timestamp=Tue Mar 19 19:23:55 2024
#PCIeAllocation=0
#Realtime.Amps=4.7 Amps
#Realtime.Power=981 W | 3348 Btu/hr
RedundancyPolicy=Not Redundant
#SCViewSledPwr=902
#ServerAllocation=658 W | 2246 Btu/hr
#Status=1

#ActivePolicyName=
#ActivePowerCapVal=32767
ChassisCurrentCapLimit=0
ChassisCurrentCapSetting=Disabled
GridACurrentCapLimit=1000000
GridACurrentCapSetting=Disabled
GridBCurrentCapLimit=1000000
GridBCurrentCapSetting=Disabled
GridCurrentCapLimit=0
GridCurrentCapSetting=Disabled
#GridCurrentLimitLowerBound=0
#GridCurrentLimitUpperBound=1000000
#PowerCapMaxThres=1220
#PowerCapMinThres=516
PowerCapSetting=Disabled
PowerCapValue=32767
Poweredbyparent=PoweredByChassis
PSRedPolicy=Not Redundant
#SCViewSledPwr=902
SystemCurrentCapLimit=1000000
SystemCurrentCapSetting=Disabled
#SystemCurrentLimitLowerBound=0
#SystemCurrentLimitUpperBound=1000000

[Key=system.Embedded.1#ServerPwrMon.1]
#AccumulativePower=1
#CumulativePowerStartTime=1711143252
#CumulativePowerStartTimeStr=2024-03-22T21:34:12Z
#MinPowerTime=1711143260
#MinPowerTimeStr=2024-03-22T21:34:20Z
#MinPowerWatts=600
#PeakCurrentTime=1711143369
#PeakCurrentTimeStr=2024-03-22T21:36:09Z
#PeakPowerStartTime=1711143252
#PeakPowerStartTimeStr=2024-03-22T21:34:12Z
#PeakPowerTime=1711143369
#PeakPowerTimeStr=2024-03-22T21:36:09Z
#PeakPowerWatts=996
PowerConfigReset=None

PS1 Status                      Present                  AC             1424.000Watts  
PS2 Status                      Present                  AC             1410.000Watts  
PS1 Voltage 1                   Ok          204.00V             NA          NA          
PS2 Voltage 2                   Ok          204.00V             NA          NA          
PS1 Current 1                 Ok      7.0Amps  NA   NA       0Amps [N]      0Amps [N]
PS2 Current 2                 Ok      7.0Amps  NA   NA       0Amps [N]      0Amps [N]

Duration Above Warning Threshold as Percentage = 0.0%
Duration Above Critical Threshold as Percentage = 0.0%

Average Temperatures
Last Hour  = 20C ( 68.0F )
Last Day   = 20C ( 68.0F )
Last Week  = 20C ( 68.0F )
Last Month = 20C ( 68.0F )
Last Year  = 20C ( 68.0F )

Peak Temperatures
Last Hour  = 21C ( 69.8F ) [At Fri, 22 Mar 2024 15:57:41]
Last Day   = 22C ( 71.6F ) [At Thu, 21 Mar 2024 20:16:51]
Last Week  = 22C ( 71.6F ) [At Thu, 21 Mar 2024 20:16:51]
Last Month = 23C ( 73.4F ) [At Tue, 12 Mar 2024 15:33:35]
Last Year  = 34C ( 93.2F ) [At Wed, 06 Dec 2023 13:46:21]

Done: Fri Mar 22 10:38:00 CDT 2024
```

## Run 7: Tue Mar 26 15:01:59 2024

### Versions

- Intel MKL version: 2023.0.0
- Intel MPI version: intel/mpi/2019u12
  - This was the most recent version available

### Notes

- Changed MPI_PROC_NUM, MPI_PER_NODE, and NUMA_PER_MPI
- Changed P and Q to 1/2
  - I tried 2 and 2 in a separate test - that causes a memory error

### SLURM Job

```
#!/bin/bash
#SBATCH --job-name=linpack
#SBATCH --output=linpack_%j.out
#SBATCH --partition=8480    # Specify your partition
#SBATCH --nodes=2                     # Number of nodes
#SBATCH --ntasks-per-node=1           # Number of tasks (MPI processes) per node
#SBATCH --time=0:30:00                # Time limit in the format hours:minutes:seconds

# Load the required modules
module load intel/oneAPI/2023.0.0
module load compiler-rt/2023.0.0 mkl/2023.0.0 mpi/2021.8.0

# Navigate to the directory containing your HPL files
cd /home/grant/mp_linpack

# Run the HPL benchmark
bash runme_intel64_dynamic
```

### runme

```bash
#!/bin/bash
#===============================================================================
# Copyright 2001-2021 Intel Corporation.
#
# This software and the related documents are Intel copyrighted  materials,  and
# your use of  them is  governed by the  express license  under which  they were
# provided to you (License).  Unless the License provides otherwise, you may not
# use, modify, copy, publish, distribute,  disclose or transmit this software or
# the related documents without Intel's prior written permission.
#
# This software and the related documents  are provided as  is,  with no express
# or implied  warranties,  other  than those  that are  expressly stated  in the
# License.
#===============================================================================
#SBATCH -p 8480
#SBATCH -N 1
#SBATCH -t 06:00:00
#SBATCH -J HPL_8480
#SBATCH -o HPL_8480x1.%N.o%j

# Set total number of MPI processes for the HPL (should be equal to PxQ).
export MPI_PROC_NUM=4

# Set the MPI per node to each node.
# MPI_PER_NODE should be equal to 1 or number of sockets in the system. Otherwise,
# the HPL performance will be low.
# MPI_PER_NODE is same as -perhost or -ppn paramaters in mpirun/mpiexec
export MPI_PER_NODE=2

# Set the number of NUMA nodes per MPI.
# NUMA_PER_MPI should be equal to 1 or number of NUMA nodes in the system.
export NUMA_PER_MPI=4

#
# You can find description of all Intel(R) MPI Library parameters in the
# Intel(R) MPI Library Reference Manual.
export I_MPI_DAPL_DIRECT_COPY_THRESHOLD=655360

#         "export I_MPI_PIN_CELL=core"
#         You can use this variable (beginning Intel(R) MPI Library 4.0.1) for cases
#         if HT is enabled.
#         The variable forces to pin MPI processes and threads to real cores,
#         so logical processors will not be involved.
#         It can be used together with the variable below, when Hydra Process Manager:
#         "export I_MPI_PIN_DOMAIN=auto" This allows uniform distribution of
#             the processes and thread domains

# export I_MPI_EAGER_THRESHOLD=128000
#          This setting may give 1-2% of performance increase over the
#          default value of 262000 for large problems and high number of cores

export I_MPI_THREAD_MAX=56
export OUT=xhpl_intel64_dynamic_outputs.txt
export HPL_EXE=xhpl_intel64_dynamic

echo -n "This run was done on: "
date

# Capture some meaningful data for future reference:
echo -n "This run was done on: " >> $OUT
date >> $OUT
echo "HPL.dat: " >> $OUT
cat HPL.dat >> $OUT
echo "Binary name: " >> $OUT
ls -l xhpl_intel64_dynamic >> $OUT
echo "This script: " >> $OUT
cat runme_intel64_dynamic_8480 >> $OUT
echo "Environment variables: " >> $OUT
env >> $OUT
echo "Actual run: " >> $OUT

# Load power tracking module
module load sysinfo
power-reset
power-report

date

# Environment variables can also be also be set on the Intel(R) MPI Library command
# line using the -genv option (to appear before the -np 1):

# mpirun -np ${MPI_PROC_NUM} ./runme_intel64_prv "$@" | tee -a $OUT

# In case of multiple nodes involved, please set the number of MPI processes
# per node (ppn=1,2 typically) through the -perhost option (because the
# default is all cores):

#mpirun -perhost ${MPI_PER_NODE} -np ${MPI_PROC_NUM} ./runme_intel64_prv "$@" | tee -a $OUT
#mpirun -perhost ${MPI_PER_NODE} -np ${MPI_PROC_NUM} ./xhpl_intel64_dynamic -n 234240 -b 384 -p 1 -q 1
mpirun -perhost ${MPI_PER_NODE} -np ${MPI_PROC_NUM} ./runme_intel64_prv -n 117120 -b 384 -p 1 -q 2

#Show power usage after completion
date
power-report

echo -n "Done: " >> $OUT
date >> $OUT

echo -n "Done: "
date
```

### HPL.dat

Parameters provided via the run file.

### Results

```
Loading compiler-rt version 2023.0.0
Loading mkl version 2023.0.0
Loading tbb version 2021.8.0
Loading mpi version 2021.8.0
This run was done on: Tue Mar 26 15:01:59 CDT 2024
cat: runme_intel64_dynamic_8480: No such file or directory
[Key=system.Embedded.1#ServerPwrMon.1]
Object value modified successfully

#Avg.LastDay=533 W | 1819 Btu/hr
#Avg.LastHour=647 W | 2208 Btu/hr
#Avg.LastWeek=533 W | 1819 Btu/hr
#Cap.ActivePolicy.BtuHr=111834 Btu/hr
#Cap.ActivePolicy.Name=
#Cap.ActivePolicy.Watts=32767 W
Cap.BtuHr=111834 btu/hr
Cap.Enable=Disabled
#Cap.MaxThreshold=1220 W | 4165 Btu/hr
#Cap.MinThreshold=516 W | 1762 Btu/hr
Cap.Percent=100
Cap.Watts=32767 W
#EnergyConsumption=0 KWh | 0 Btu
#EnergyConsumption.Clear=******** (Write-Only)
#EnergyConsumption.StarttimeStamp=Tue Mar 26 15:01:59 2024
#Max.Amps=0.0 Amps
#Max.Amps.Timestamp=Tue Mar 26 15:01:59 2024
#Max.Headroom=291 W | 993 Btu/hr
#Max.LastDay=1259 W | 4297 Btu/hr
#Max.LastDay.Timestamp=Tue Mar 26 14:53:15 2024
#Max.LastHour=1259 W | 4297 Btu/hr
#Max.LastHour.Timestamp=Tue Mar 26 14:53:15 2024
#Max.LastWeek=1259 W | 4297 Btu/hr
#Max.LastWeek.Timestamp=Tue Mar 26 14:53:15 2024
#Max.Power=0 W | 0 Btu/hr
#Max.Power.Timestamp=Tue Mar 26 15:01:59 2024
#Max.PowerClear=******** (Write-Only)
#Min.LastDay=19 W | 65 Btu/hr
#Min.LastDay.Timestamp=Mon Mar 25 16:27:19 2024
#Min.LastHour=518 W | 1768 Btu/hr
#Min.LastHour.Timestamp=Tue Mar 26 14:54:57 2024
#Min.LastWeek=19 W | 65 Btu/hr
#Min.LastWeek.Timestamp=Mon Mar 25 16:27:19 2024
#PCIeAllocation=0
#Realtime.Amps=2.6 Amps
#Realtime.Power=540 W | 1843 Btu/hr
RedundancyPolicy=Not Redundant
#SCViewSledPwr=548
#ServerAllocation=658 W | 2246 Btu/hr
#Status=1

#ActivePolicyName=
#ActivePowerCapVal=32767
ChassisCurrentCapLimit=0
ChassisCurrentCapSetting=Disabled
GridACurrentCapLimit=1000000
GridACurrentCapSetting=Disabled
GridBCurrentCapLimit=1000000
GridBCurrentCapSetting=Disabled
GridCurrentCapLimit=0
GridCurrentCapSetting=Disabled
#GridCurrentLimitLowerBound=0
#GridCurrentLimitUpperBound=1000000
#PowerCapMaxThres=1220
#PowerCapMinThres=516
PowerCapSetting=Disabled
PowerCapValue=32767
Poweredbyparent=PoweredByChassis
PSRedPolicy=Not Redundant
#SCViewSledPwr=548
SystemCurrentCapLimit=1000000
SystemCurrentCapSetting=Disabled
#SystemCurrentLimitLowerBound=0
#SystemCurrentLimitUpperBound=1000000

[Key=system.Embedded.1#ServerPwrMon.1]
#AccumulativePower=0
#CumulativePowerStartTime=1711483319
#CumulativePowerStartTimeStr=2024-03-26T20:01:59Z
#MinPowerTime=1711483321
#MinPowerTimeStr=2024-03-26T20:02:01Z
#MinPowerWatts=523
#PeakCurrentTime=1711483322
#PeakCurrentTimeStr=2024-03-26T20:02:02Z
#PeakPowerStartTime=1711483319
#PeakPowerStartTimeStr=2024-03-26T20:01:59Z
#PeakPowerTime=1711483321
#PeakPowerTimeStr=2024-03-26T20:02:01Z
#PeakPowerWatts=528
PowerConfigReset=None

PS1 Status                      Present                  AC             946.000Watts
PS2 Status                      Present                  AC             1002.000Watts
PS1 Voltage 1                   Ok          204.00V             NA          NA
PS2 Voltage 2                   Ok          204.00V             NA          NA
PS1 Current 1                 Ok      4.8Amps  NA   NA       0Amps [N]      0Amps [N]
PS2 Current 2                 Ok      5.2Amps  NA   NA       0Amps [N]      0Amps [N]

Duration Above Warning Threshold as Percentage = 0.0%
Duration Above Critical Threshold as Percentage = 0.0%

Average Temperatures
Last Hour  = 22C ( 71.6F )
Last Day   = 20C ( 68.0F )
Last Week  = 19C ( 68.0F )
Last Month = 20C ( 68.0F )
Last Year  = 20C ( 68.0F )

Peak Temperatures
Last Hour  = 22C ( 71.6F ) [At Tue, 26 Mar 2024 14:57:44]
Last Day   = 23C ( 73.4F ) [At Mon, 25 Mar 2024 21:29:12]
Last Week  = 23C ( 73.4F ) [At Mon, 25 Mar 2024 21:29:12]
Last Month = 23C ( 73.4F ) [At Mon, 25 Mar 2024 21:29:12]
Last Year  = 34C ( 93.2F ) [At Wed, 06 Dec 2023 13:46:21]

Tue Mar 26 15:02:06 CDT 2024
RANK=0, NODE=0-3
RANK=1, NODE=4-7
RANK=2, NODE=8-11
RANK=3, NODE=12-15
MPI startup(): I_MPI_DAPL_DIRECT_COPY_THRESHOLD variable has been removed from the product, its value is ignored

HPL[z5-02] : Affinity (0) is out of range.
HPL[z5-02] : Affinity (0) is out of range.
================================================================================
HPLinpack 2.3  --  High-Performance Linpack benchmark  --   December 2, 2018
Written by A. Petitet and R. Clint Whaley,  Innovative Computing Laboratory, UTK
Modified by Piotr Luszczek, Innovative Computing Laboratory, UTK
Modified by Julien Langou, University of Colorado Denver
================================================================================

An explanation of the input/output parameters follows:
T/V    : Wall time / encoded variant.
N      : The order of the coefficient matrix A.
NB     : The partitioning blocking factor.
P      : The number of process rows.
Q      : The number of process columns.
Time   : Time in seconds to solve the linear system.
Gflops : Rate of execution for solving the linear system.

The following parameter values will be used:

N        :  117120
NB       :     384
PMAP     : Row-major process mapping
P        :       1
Q        :       2
PFACT    :   Right     Left     Left
NBMIN    :       4
NDIV     :       2
RFACT    :   Right
BCAST    :  1ringM
DEPTH    :       1
SWAP     : Mix (threshold = 64)
L1       : transposed form
U        : transposed form
EQUIL    : yes
ALIGN    :   16 double precision words

--------------------------------------------------------------------------------

- The matrix A is randomly generated for each test.
- The following scaled residual check will be computed:
      ||Ax-b||_oo / ( eps * ( || x ||_oo * || A ||_oo + || b ||_oo ) * N )
- The relative machine precision (eps) is taken to be               1.110223e-16
- Computational tests pass if scaled residuals are less than                16.0

z5-01           : Column=000768 Fraction=0.005 Kernel=    0.61 Mflops=11354271.64
z5-01           : Column=001536 Fraction=0.010 Kernel=7121481.37 Mflops=8766267.16
z5-01           : Column=001920 Fraction=0.015 Kernel=6569268.49 Mflops=8176330.03
z5-01           : Column=002688 Fraction=0.020 Kernel=7658104.36 Mflops=8023764.09
z5-01           : Column=003072 Fraction=0.025 Kernel=7609015.52 Mflops=7806403.50
z5-01           : Column=003840 Fraction=0.030 Kernel=6966626.85 Mflops=7627404.59
z5-01           : Column=004224 Fraction=0.035 Kernel=7590871.62 Mflops=7625796.50
z5-01           : Column=004992 Fraction=0.040 Kernel=6936584.27 Mflops=7515131.53
z5-01           : Column=005376 Fraction=0.045 Kernel=7494266.28 Mflops=7504962.76
z5-01           : Column=006144 Fraction=0.050 Kernel=6845870.36 Mflops=7419848.47
z5-01           : Column=006528 Fraction=0.055 Kernel=7458286.44 Mflops=7432322.29
z5-01           : Column=007296 Fraction=0.060 Kernel=7297694.14 Mflops=7418737.36
z5-01           : Column=007680 Fraction=0.065 Kernel=7356681.17 Mflops=7351225.43
z5-01           : Column=008448 Fraction=0.070 Kernel=7318688.77 Mflops=7348455.40
z5-01           : Column=008832 Fraction=0.075 Kernel=7321241.26 Mflops=7360635.61
z5-01           : Column=009600 Fraction=0.080 Kernel=7024521.29 Mflops=7334738.98
z5-01           : Column=009984 Fraction=0.085 Kernel=7226197.63 Mflops=7288573.89
z5-01           : Column=010752 Fraction=0.090 Kernel=7189259.32 Mflops=7282021.15
z5-01           : Column=011136 Fraction=0.095 Kernel=7185301.72 Mflops=7293190.78
z5-01           : Column=011904 Fraction=0.100 Kernel=7136628.62 Mflops=7283897.24
z5-01           : Column=012672 Fraction=0.105 Kernel=7092482.41 Mflops=7273256.19
z5-01           : Column=013056 Fraction=0.110 Kernel=7055695.68 Mflops=7252810.52
z5-01           : Column=013824 Fraction=0.115 Kernel=7018165.81 Mflops=7240922.62
z5-01           : Column=014208 Fraction=0.120 Kernel=7010759.65 Mflops=7249082.85
z5-01           : Column=014976 Fraction=0.125 Kernel=7541914.68 Mflops=7261709.21
z5-01           : Column=015360 Fraction=0.130 Kernel=6916327.39 Mflops=7214096.27
z5-01           : Column=016128 Fraction=0.135 Kernel=7550542.12 Mflops=7227323.77
z5-01           : Column=016512 Fraction=0.140 Kernel=6882332.66 Mflops=7234418.29
z5-01           : Column=017280 Fraction=0.145 Kernel=7474629.34 Mflops=7243230.44
z5-01           : Column=017664 Fraction=0.150 Kernel=8222364.59 Mflops=7219665.87
z5-01           : Column=018432 Fraction=0.155 Kernel=6750967.87 Mflops=7202145.15
z5-01           : Column=018816 Fraction=0.160 Kernel=7674758.97 Mflops=7230419.49
z5-01           : Column=019584 Fraction=0.165 Kernel=6687356.04 Mflops=7211356.61
z5-01           : Column=019968 Fraction=0.170 Kernel=6944531.38 Mflops=7193364.51
z5-01           : Column=020736 Fraction=0.175 Kernel=7107588.12 Mflops=7190731.79
z5-01           : Column=021120 Fraction=0.180 Kernel=7498965.83 Mflops=7213880.80
z5-01           : Column=021888 Fraction=0.185 Kernel=7147174.21 Mflops=7211972.18
z5-01           : Column=022272 Fraction=0.190 Kernel=6530117.08 Mflops=7190495.96
z5-01           : Column=023040 Fraction=0.195 Kernel=7103078.02 Mflops=7188145.59
z5-01           : Column=023808 Fraction=0.200 Kernel=7065911.15 Mflops=7184979.51
z5-01           : Column=024192 Fraction=0.205 Kernel=7689495.86 Mflops=7200564.10
z5-01           : Column=024960 Fraction=0.210 Kernel=7005188.83 Mflops=7195756.90
z5-01           : Column=025344 Fraction=0.215 Kernel=6350688.91 Mflops=7175773.29
z5-01           : Column=026112 Fraction=0.220 Kernel=7658655.94 Mflops=7185997.79
z5-01           : Column=026496 Fraction=0.225 Kernel=6323577.08 Mflops=7181908.28
z5-01           : Column=027264 Fraction=0.230 Kernel=7508388.77 Mflops=7188564.69
z5-01           : Column=027648 Fraction=0.235 Kernel=6205038.46 Mflops=7170658.59
z5-01           : Column=028416 Fraction=0.240 Kernel=7484879.31 Mflops=7176722.22
z5-01           : Column=028800 Fraction=0.245 Kernel=7222357.40 Mflops=7183219.54
z5-01           : Column=029568 Fraction=0.250 Kernel=6758826.71 Mflops=7174639.20
z5-01           : Column=029952 Fraction=0.255 Kernel=7367065.18 Mflops=7170816.74
z5-01           : Column=030720 Fraction=0.260 Kernel=7325287.83 Mflops=7173546.59
z5-01           : Column=031104 Fraction=0.265 Kernel=7078882.38 Mflops=7176944.16
z5-01           : Column=031872 Fraction=0.270 Kernel=6631944.55 Mflops=7166862.97
z5-01           : Column=032256 Fraction=0.275 Kernel=7202341.74 Mflops=7162690.03
z5-01           : Column=033024 Fraction=0.280 Kernel=7148334.72 Mflops=7162456.28
z5-01           : Column=033408 Fraction=0.285 Kernel=7133576.81 Mflops=7166323.59
z5-01           : Column=034176 Fraction=0.290 Kernel=7064674.99 Mflops=7164731.56
z5-01           : Column=034560 Fraction=0.295 Kernel=7055918.08 Mflops=7159710.91
z5-01           : Column=035328 Fraction=0.300 Kernel=6983702.31 Mflops=7157061.72
z5-01           : Column=036096 Fraction=0.305 Kernel=6928427.56 Mflops=7153707.45
z5-01           : Column=036480 Fraction=0.310 Kernel=6427265.22 Mflops=7161281.22
z5-01           : Column=037248 Fraction=0.315 Kernel=7146358.16 Mflops=7161078.93
z5-01           : Column=037632 Fraction=0.320 Kernel=7308026.54 Mflops=7155895.67
z5-01           : Column=038400 Fraction=0.325 Kernel=6757574.03 Mflops=7150463.99
z5-01           : Column=038784 Fraction=0.330 Kernel=6636688.48 Mflops=7155618.36
z5-01           : Column=039552 Fraction=0.335 Kernel=7199047.94 Mflops=7156148.62
z5-01           : Column=039936 Fraction=0.340 Kernel=6659397.80 Mflops=7148396.02
z5-01           : Column=040704 Fraction=0.345 Kernel=7385754.01 Mflops=7151087.63
z5-01           : Column=041088 Fraction=0.350 Kernel=6811778.88 Mflops=7153835.38
z5-01           : Column=041856 Fraction=0.355 Kernel=7192900.02 Mflops=7154269.47
z5-01           : Column=042240 Fraction=0.360 Kernel=6507919.63 Mflops=7145107.68
z5-01           : Column=043008 Fraction=0.365 Kernel=7197426.35 Mflops=7145661.39
z5-01           : Column=043392 Fraction=0.370 Kernel=6348466.38 Mflops=7147682.02
z5-01           : Column=044160 Fraction=0.375 Kernel=7109645.73 Mflops=7147292.97
z5-01           : Column=044544 Fraction=0.380 Kernel=6836667.69 Mflops=7144911.26
z5-01           : Column=045312 Fraction=0.385 Kernel=7011608.16 Mflops=7143592.13
z5-01           : Column=045696 Fraction=0.390 Kernel=6248778.43 Mflops=7145141.38
z5-01           : Column=046464 Fraction=0.395 Kernel=6911122.86 Mflops=7142898.35
z5-01           : Column=047232 Fraction=0.400 Kernel=6991966.21 Mflops=7141512.01
z5-01           : Column=047616 Fraction=0.405 Kernel=6117120.96 Mflops=7136798.75
z5-01           : Column=048384 Fraction=0.410 Kernel=7473103.37 Mflops=7139557.93
z5-01           : Column=048768 Fraction=0.415 Kernel=6976650.05 Mflops=7139726.79
z5-01           : Column=049536 Fraction=0.420 Kernel=6715637.03 Mflops=7136031.07
z5-01           : Column=049920 Fraction=0.425 Kernel=6451365.78 Mflops=7135076.49
z5-01           : Column=050688 Fraction=0.430 Kernel=6943409.54 Mflops=7133534.29
z5-01           : Column=051072 Fraction=0.435 Kernel=6423399.08 Mflops=7132409.98
z5-01           : Column=051840 Fraction=0.440 Kernel=6862461.05 Mflops=7130312.31
z5-01           : Column=052224 Fraction=0.445 Kernel=6486522.71 Mflops=7128933.73
z5-01           : Column=052992 Fraction=0.450 Kernel=6833093.11 Mflops=7126730.40
z5-01           : Column=053376 Fraction=0.455 Kernel=6519767.07 Mflops=7125665.88
z5-01           : Column=054144 Fraction=0.460 Kernel=6740477.67 Mflops=7122890.99
z5-01           : Column=054528 Fraction=0.465 Kernel=6392648.81 Mflops=7121451.03
z5-01           : Column=055296 Fraction=0.470 Kernel=6724904.35 Mflops=7118719.58
z5-01           : Column=055680 Fraction=0.475 Kernel=5433069.49 Mflops=7117130.50
z5-01           : Column=056448 Fraction=0.480 Kernel=6732673.37 Mflops=7114607.78
z5-01           : Column=056832 Fraction=0.485 Kernel=5639334.87 Mflops=7113806.47
z5-01           : Column=057600 Fraction=0.490 Kernel=6589542.74 Mflops=7110455.25
z5-01           : Column=057984 Fraction=0.495 Kernel=5455107.48 Mflops=7109116.99
z5-01           : Column=060672 Fraction=0.515 Kernel=6373756.86 Mflops=7097811.57
z5-01           : Column=062976 Fraction=0.535 Kernel=6358842.97 Mflops=7085789.60
z5-01           : Column=065280 Fraction=0.555 Kernel=6160596.27 Mflops=7071737.86
z5-01           : Column=067584 Fraction=0.575 Kernel=5993311.86 Mflops=7056550.58
z5-01           : Column=069888 Fraction=0.595 Kernel=5804917.58 Mflops=7040185.35
z5-01           : Column=072192 Fraction=0.615 Kernel=5641856.22 Mflops=7023327.93
z5-01           : Column=074496 Fraction=0.635 Kernel=5381445.98 Mflops=7004810.63
z5-01           : Column=076800 Fraction=0.655 Kernel=5144264.76 Mflops=6985315.49
z5-01           : Column=079104 Fraction=0.675 Kernel=4906005.26 Mflops=6965135.01
z5-01           : Column=081408 Fraction=0.695 Kernel=4698503.48 Mflops=6944968.14
z5-01           : Column=093312 Fraction=0.795 Kernel=3988441.66 Mflops=6845423.75
z5-01           : Column=104832 Fraction=0.895 Kernel=2647079.53 Mflops=6767569.07
z5-01           : Column=116736 Fraction=0.995 Kernel=1133332.06 Mflops=6729866.87
================================================================================
T/V                N    NB     P     Q               Time                 Gflops
--------------------------------------------------------------------------------
WR11R2R4      117120   384     1     2             159.30            6.72361e+03
HPL_pdgesv() start time Tue Mar 26 15:02:17 2024

HPL_pdgesv() end time   Tue Mar 26 15:04:57 2024

--------------------------------------------------------------------------------
||Ax-b||_oo/(eps*(||A||_oo*||x||_oo+||b||_oo)*N)=   3.24787514e-03 ...... PASSED
z5-01           : Column=000768 Fraction=0.005 Kernel=    0.61 Mflops=11281867.90
z5-01           : Column=001536 Fraction=0.010 Kernel=7120526.80 Mflops=8743745.27
z5-01           : Column=001920 Fraction=0.015 Kernel=6563088.53 Mflops=8238893.12
z5-01           : Column=002688 Fraction=0.020 Kernel=7610507.98 Mflops=8052082.19
z5-01           : Column=003072 Fraction=0.025 Kernel=7620922.17 Mflops=7801693.05
z5-01           : Column=003840 Fraction=0.030 Kernel=6979109.54 Mflops=7626688.89
z5-01           : Column=004224 Fraction=0.035 Kernel=7587370.85 Mflops=7647249.08
z5-01           : Column=004992 Fraction=0.040 Kernel=6931168.90 Mflops=7531923.06
z5-01           : Column=005376 Fraction=0.045 Kernel=7512467.25 Mflops=7507970.52
z5-01           : Column=006144 Fraction=0.050 Kernel=6858488.58 Mflops=7424202.49
z5-01           : Column=006528 Fraction=0.055 Kernel=7447532.58 Mflops=7442635.39
z5-01           : Column=007296 Fraction=0.060 Kernel=7216251.13 Mflops=7419531.33
z5-01           : Column=007680 Fraction=0.065 Kernel=7374423.72 Mflops=7357933.00
z5-01           : Column=008448 Fraction=0.070 Kernel=7339167.56 Mflops=7356338.14
z5-01           : Column=008832 Fraction=0.075 Kernel=7325525.35 Mflops=7369417.06
z5-01           : Column=009600 Fraction=0.080 Kernel=6693984.02 Mflops=7314954.55
z5-01           : Column=009984 Fraction=0.085 Kernel=7250645.23 Mflops=7297359.98
z5-01           : Column=010752 Fraction=0.090 Kernel=7203884.73 Mflops=7291197.27
z5-01           : Column=011136 Fraction=0.095 Kernel=7187921.50 Mflops=7301088.39
z5-01           : Column=011904 Fraction=0.100 Kernel=7141716.72 Mflops=7291624.79
z5-01           : Column=012672 Fraction=0.105 Kernel=7101899.60 Mflops=7281080.32
z5-01           : Column=013056 Fraction=0.110 Kernel=7071295.16 Mflops=7262599.21
z5-01           : Column=013824 Fraction=0.115 Kernel=7033565.44 Mflops=7251004.86
z5-01           : Column=014208 Fraction=0.120 Kernel=7006408.94 Mflops=7256603.83
z5-01           : Column=014976 Fraction=0.125 Kernel=7404047.17 Mflops=7263080.92
z5-01           : Column=015360 Fraction=0.130 Kernel=6925501.74 Mflops=7224268.42
z5-01           : Column=016128 Fraction=0.135 Kernel=7452372.69 Mflops=7233362.16
z5-01           : Column=016512 Fraction=0.140 Kernel=6864411.01 Mflops=7240392.98
z5-01           : Column=017280 Fraction=0.145 Kernel=7379670.67 Mflops=7245569.81
z5-01           : Column=017664 Fraction=0.150 Kernel=6788856.02 Mflops=7204059.27
z5-01           : Column=018432 Fraction=0.155 Kernel=7403797.28 Mflops=7210875.70
z5-01           : Column=018816 Fraction=0.160 Kernel=8144373.25 Mflops=7235394.36
z5-01           : Column=019584 Fraction=0.165 Kernel=6700481.02 Mflops=7216640.62
z5-01           : Column=019968 Fraction=0.170 Kernel=6657242.51 Mflops=7196495.97
z5-01           : Column=020736 Fraction=0.175 Kernel=7263200.55 Mflops=7198501.62
z5-01           : Column=021120 Fraction=0.180 Kernel=8009157.58 Mflops=7219437.15
z5-01           : Column=021888 Fraction=0.185 Kernel=7087531.82 Mflops=7215629.37
z5-01           : Column=022272 Fraction=0.190 Kernel=7920341.12 Mflops=7197282.32
z5-01           : Column=023040 Fraction=0.195 Kernel=7099836.69 Mflops=7194658.77
z5-01           : Column=023808 Fraction=0.200 Kernel=7055662.23 Mflops=7191050.25
z5-01           : Column=024192 Fraction=0.205 Kernel=7540131.09 Mflops=7205229.54
z5-01           : Column=024960 Fraction=0.210 Kernel=7069720.16 Mflops=7201922.95
z5-01           : Column=025344 Fraction=0.215 Kernel=7692921.77 Mflops=7180612.46
z5-01           : Column=026112 Fraction=0.220 Kernel=6917703.69 Mflops=7174459.29
z5-01           : Column=026496 Fraction=0.225 Kernel=6337072.37 Mflops=7188390.82
z5-01           : Column=027264 Fraction=0.230 Kernel=7417273.03 Mflops=7193117.68
z5-01           : Column=027648 Fraction=0.235 Kernel=7528785.80 Mflops=7174599.07
z5-01           : Column=028416 Fraction=0.240 Kernel=6766488.11 Mflops=7165900.61
z5-01           : Column=028800 Fraction=0.245 Kernel=6717407.28 Mflops=7183924.24
z5-01           : Column=029568 Fraction=0.250 Kernel=7014132.62 Mflops=7180613.60
z5-01           : Column=029952 Fraction=0.255 Kernel=7373072.83 Mflops=7174504.63
z5-01           : Column=030720 Fraction=0.260 Kernel=6604786.28 Mflops=7163353.98
z5-01           : Column=031104 Fraction=0.265 Kernel=6623290.43 Mflops=7176431.71
z5-01           : Column=031872 Fraction=0.270 Kernel=6910459.65 Mflops=7171706.96
z5-01           : Column=032256 Fraction=0.275 Kernel=7203628.57 Mflops=7165565.43
z5-01           : Column=033024 Fraction=0.280 Kernel=7137965.40 Mflops=7165115.18
z5-01           : Column=033408 Fraction=0.285 Kernel=7105349.18 Mflops=7170148.96
z5-01           : Column=034176 Fraction=0.290 Kernel=7041232.92 Mflops=7168122.18
z5-01           : Column=034560 Fraction=0.295 Kernel=7047266.40 Mflops=7162031.30
z5-01           : Column=035328 Fraction=0.300 Kernel=6976811.26 Mflops=7159239.86
z5-01           : Column=036096 Fraction=0.305 Kernel=6924501.49 Mflops=7155793.08
z5-01           : Column=036480 Fraction=0.310 Kernel=7326144.64 Mflops=7165399.37
z5-01           : Column=037248 Fraction=0.315 Kernel=6829710.09 Mflops=7160638.12
z5-01           : Column=037632 Fraction=0.320 Kernel=6838595.78 Mflops=7147274.67
z5-01           : Column=038400 Fraction=0.325 Kernel=7552409.74 Mflops=7152219.06
z5-01           : Column=038784 Fraction=0.330 Kernel=7204916.33 Mflops=7160331.98
z5-01           : Column=039552 Fraction=0.335 Kernel=6668687.30 Mflops=7153853.86
z5-01           : Column=039936 Fraction=0.340 Kernel=6657671.32 Mflops=7149663.69
z5-01           : Column=040704 Fraction=0.345 Kernel=6596327.69 Mflops=7142646.30
z5-01           : Column=041088 Fraction=0.350 Kernel=6680426.51 Mflops=7149839.19
z5-01           : Column=041856 Fraction=0.355 Kernel=7271444.95 Mflops=7151175.28
z5-01           : Column=042240 Fraction=0.360 Kernel=8245746.16 Mflops=7145933.51
z5-01           : Column=043008 Fraction=0.365 Kernel=7187226.19 Mflops=7146371.19
z5-01           : Column=043392 Fraction=0.370 Kernel=7763543.95 Mflops=7150980.83
z5-01           : Column=044160 Fraction=0.375 Kernel=6829403.91 Mflops=7147556.56
z5-01           : Column=044544 Fraction=0.380 Kernel=6360752.94 Mflops=7137194.07
z5-01           : Column=045312 Fraction=0.385 Kernel=7029464.10 Mflops=7136131.82
z5-01           : Column=045696 Fraction=0.390 Kernel=6268019.33 Mflops=7141388.19
z5-01           : Column=046464 Fraction=0.395 Kernel=7217865.47 Mflops=7142089.98
z5-01           : Column=047232 Fraction=0.400 Kernel=7127279.79 Mflops=7141956.52
z5-01           : Column=047616 Fraction=0.405 Kernel=7716735.01 Mflops=7137179.45
z5-01           : Column=048384 Fraction=0.410 Kernel=6727759.06 Mflops=7133451.46
z5-01           : Column=048768 Fraction=0.415 Kernel=6192084.13 Mflops=7136513.19
z5-01           : Column=049536 Fraction=0.420 Kernel=6880389.82 Mflops=7134335.17
z5-01           : Column=049920 Fraction=0.425 Kernel=6861263.93 Mflops=7129768.23
z5-01           : Column=050688 Fraction=0.430 Kernel=6880982.22 Mflops=7127749.91
z5-01           : Column=051072 Fraction=0.435 Kernel=6361028.46 Mflops=7130732.58
z5-01           : Column=051840 Fraction=0.440 Kernel=6826259.82 Mflops=7128354.74
z5-01           : Column=052224 Fraction=0.445 Kernel=6495352.62 Mflops=7123638.81
z5-01           : Column=052992 Fraction=0.450 Kernel=6848458.83 Mflops=7121595.42
z5-01           : Column=053376 Fraction=0.455 Kernel=6385783.09 Mflops=7123561.75
z5-01           : Column=054144 Fraction=0.460 Kernel=6747064.66 Mflops=7120852.90
z5-01           : Column=054528 Fraction=0.465 Kernel=6447159.66 Mflops=7116121.49
z5-01           : Column=055296 Fraction=0.470 Kernel=6629418.84 Mflops=7112723.62
z5-01           : Column=055680 Fraction=0.475 Kernel=5400493.08 Mflops=7114384.35
z5-01           : Column=056448 Fraction=0.480 Kernel=6749759.75 Mflops=7111998.70
z5-01           : Column=056832 Fraction=0.485 Kernel=5581153.55 Mflops=7106827.95
z5-01           : Column=057600 Fraction=0.490 Kernel=6725291.29 Mflops=7104440.32
z5-01           : Column=057984 Fraction=0.495 Kernel=5242404.35 Mflops=7105242.54
z5-01           : Column=060672 Fraction=0.515 Kernel=6316674.48 Mflops=7089571.65
z5-01           : Column=062976 Fraction=0.535 Kernel=6298471.83 Mflops=7076595.08
z5-01           : Column=065280 Fraction=0.555 Kernel=6089535.23 Mflops=7061450.84
z5-01           : Column=067584 Fraction=0.575 Kernel=5920873.45 Mflops=7045217.89
z5-01           : Column=069888 Fraction=0.595 Kernel=5757572.36 Mflops=7028272.07
z5-01           : Column=072192 Fraction=0.615 Kernel=5570281.03 Mflops=7010502.06
z5-01           : Column=074496 Fraction=0.635 Kernel=5316013.57 Mflops=6991193.84
z5-01           : Column=076800 Fraction=0.655 Kernel=5071860.87 Mflops=6970837.90
z5-01           : Column=079104 Fraction=0.675 Kernel=4850313.52 Mflops=6950066.15
z5-01           : Column=081408 Fraction=0.695 Kernel=4634296.73 Mflops=6929223.98
z5-01           : Column=093312 Fraction=0.795 Kernel=3931475.16 Mflops=6829731.21
z5-01           : Column=104832 Fraction=0.895 Kernel=2602552.62 Mflops=6750205.23
z5-01           : Column=116736 Fraction=0.995 Kernel=1120624.54 Mflops=6709606.37
================================================================================
T/V                N    NB     P     Q               Time                 Gflops
--------------------------------------------------------------------------------
WR11R2L4      117120   384     1     2             159.77            6.70365e+03
HPL_pdgesv() start time Tue Mar 26 15:05:15 2024

HPL_pdgesv() end time   Tue Mar 26 15:07:55 2024

--------------------------------------------------------------------------------
||Ax-b||_oo/(eps*(||A||_oo*||x||_oo+||b||_oo)*N)=   3.28451406e-03 ...... PASSED
z5-01           : Column=000768 Fraction=0.005 Kernel=    0.61 Mflops=11278682.20
z5-01           : Column=001536 Fraction=0.010 Kernel=7123257.16 Mflops=8744826.22
z5-01           : Column=001920 Fraction=0.015 Kernel=6552351.56 Mflops=8154815.54
z5-01           : Column=002688 Fraction=0.020 Kernel=7639145.85 Mflops=8003018.80
z5-01           : Column=003072 Fraction=0.025 Kernel=7621461.00 Mflops=7798698.40
z5-01           : Column=003840 Fraction=0.030 Kernel=6977855.69 Mflops=7624092.67
z5-01           : Column=004224 Fraction=0.035 Kernel=7589094.27 Mflops=7613704.66
z5-01           : Column=004992 Fraction=0.040 Kernel=6925345.01 Mflops=7503173.37
z5-01           : Column=005376 Fraction=0.045 Kernel=7524210.42 Mflops=7507026.76
z5-01           : Column=006144 Fraction=0.050 Kernel=6858965.51 Mflops=7423456.18
z5-01           : Column=006528 Fraction=0.055 Kernel=7449192.67 Mflops=7420937.75
z5-01           : Column=007296 Fraction=0.060 Kernel=7377003.68 Mflops=7416553.44
z5-01           : Column=007680 Fraction=0.065 Kernel=7371197.31 Mflops=7358128.22
z5-01           : Column=008448 Fraction=0.070 Kernel=7343560.99 Mflops=7356890.81
z5-01           : Column=008832 Fraction=0.075 Kernel=7290677.17 Mflops=7349544.32
z5-01           : Column=009600 Fraction=0.080 Kernel=7107657.07 Mflops=7331134.64
z5-01           : Column=009984 Fraction=0.085 Kernel=7249190.48 Mflops=7298977.92
z5-01           : Column=010752 Fraction=0.090 Kernel=7206259.82 Mflops=7292865.75
z5-01           : Column=011136 Fraction=0.095 Kernel=7191437.44 Mflops=7284827.33
z5-01           : Column=011904 Fraction=0.100 Kernel=7136184.86 Mflops=7276012.90
z5-01           : Column=012672 Fraction=0.105 Kernel=7102676.89 Mflops=7266399.78
z5-01           : Column=013056 Fraction=0.110 Kernel=7074225.51 Mflops=7264801.19
z5-01           : Column=013824 Fraction=0.115 Kernel=7028562.16 Mflops=7252830.56
z5-01           : Column=014208 Fraction=0.120 Kernel=7548707.73 Mflops=7256086.16
z5-01           : Column=014976 Fraction=0.125 Kernel=7352103.84 Mflops=7260332.35
z5-01           : Column=015360 Fraction=0.130 Kernel=6928668.97 Mflops=7226048.35
z5-01           : Column=016128 Fraction=0.135 Kernel=7551549.70 Mflops=7238864.28
z5-01           : Column=016512 Fraction=0.140 Kernel=6878238.07 Mflops=7229537.85
z5-01           : Column=017280 Fraction=0.145 Kernel=7482775.20 Mflops=7238812.10
z5-01           : Column=017664 Fraction=0.150 Kernel=6813310.88 Mflops=7206482.58
z5-01           : Column=018432 Fraction=0.155 Kernel=7404470.90 Mflops=7213240.90
z5-01           : Column=018816 Fraction=0.160 Kernel=6879857.06 Mflops=7226490.01
z5-01           : Column=019584 Fraction=0.165 Kernel=6848071.56 Mflops=7213514.44
z5-01           : Column=019968 Fraction=0.170 Kernel=6674901.26 Mflops=7199021.45
z5-01           : Column=020736 Fraction=0.175 Kernel=7268710.32 Mflops=7201116.01
z5-01           : Column=021120 Fraction=0.180 Kernel=6599795.56 Mflops=7210807.55
z5-01           : Column=021888 Fraction=0.185 Kernel=7182681.43 Mflops=7210007.00
z5-01           : Column=022272 Fraction=0.190 Kernel=7926505.67 Mflops=7200393.36
z5-01           : Column=023040 Fraction=0.195 Kernel=7104425.42 Mflops=7197810.12
z5-01           : Column=023808 Fraction=0.200 Kernel=7064463.73 Mflops=7194351.02
z5-01           : Column=024192 Fraction=0.205 Kernel=7799799.96 Mflops=7200353.02
z5-01           : Column=024960 Fraction=0.210 Kernel=7002471.04 Mflops=7195482.44
z5-01           : Column=025344 Fraction=0.215 Kernel=6553068.41 Mflops=7184556.61
z5-01           : Column=026112 Fraction=0.220 Kernel=6928358.91 Mflops=7178566.31
z5-01           : Column=026496 Fraction=0.225 Kernel=6534917.81 Mflops=7186558.53
z5-01           : Column=027264 Fraction=0.230 Kernel=7431842.38 Mflops=7191613.13
z5-01           : Column=027648 Fraction=0.235 Kernel=7538492.17 Mflops=7179031.07
z5-01           : Column=028416 Fraction=0.240 Kernel=6788701.34 Mflops=7170733.22
z5-01           : Column=028800 Fraction=0.245 Kernel=7102773.62 Mflops=7185106.44
z5-01           : Column=029568 Fraction=0.250 Kernel=6884295.57 Mflops=7179131.78
z5-01           : Column=029952 Fraction=0.255 Kernel=7380944.65 Mflops=7179354.41
z5-01           : Column=030720 Fraction=0.260 Kernel=6616409.86 Mflops=7168348.03
z5-01           : Column=031104 Fraction=0.265 Kernel=6592101.38 Mflops=7177392.07
z5-01           : Column=031872 Fraction=0.270 Kernel=6861880.35 Mflops=7171747.59
z5-01           : Column=032256 Fraction=0.275 Kernel=7221276.36 Mflops=7170974.80
z5-01           : Column=033024 Fraction=0.280 Kernel=7159358.43 Mflops=7170785.72
z5-01           : Column=033408 Fraction=0.285 Kernel=7099705.54 Mflops=7170171.57
z5-01           : Column=034176 Fraction=0.290 Kernel=7039620.70 Mflops=7168118.61
z5-01           : Column=034560 Fraction=0.295 Kernel=7054593.48 Mflops=7167883.66
z5-01           : Column=035328 Fraction=0.300 Kernel=6986378.17 Mflops=7165149.69
z5-01           : Column=036096 Fraction=0.305 Kernel=6937223.96 Mflops=7161806.28
z5-01           : Column=036480 Fraction=0.310 Kernel=7466428.78 Mflops=7166639.82
z5-01           : Column=037248 Fraction=0.315 Kernel=6841474.65 Mflops=7162034.87
z5-01           : Column=037632 Fraction=0.320 Kernel=6854371.60 Mflops=7153480.01
z5-01           : Column=038400 Fraction=0.325 Kernel=7580299.19 Mflops=7158674.55
z5-01           : Column=038784 Fraction=0.330 Kernel=7382468.26 Mflops=7160771.64
z5-01           : Column=039552 Fraction=0.335 Kernel=6727201.80 Mflops=7155107.44
z5-01           : Column=039936 Fraction=0.340 Kernel=6665245.99 Mflops=7156365.32
z5-01           : Column=040704 Fraction=0.345 Kernel=6616226.80 Mflops=7149529.32
z5-01           : Column=041088 Fraction=0.350 Kernel=6832526.04 Mflops=7151716.58
z5-01           : Column=041856 Fraction=0.355 Kernel=7086725.21 Mflops=7150983.92
z5-01           : Column=042240 Fraction=0.360 Kernel=8189470.84 Mflops=7152389.12
z5-01           : Column=043008 Fraction=0.365 Kernel=7079949.91 Mflops=7151609.10
z5-01           : Column=043392 Fraction=0.370 Kernel=7545118.95 Mflops=7150304.46
z5-01           : Column=044160 Fraction=0.375 Kernel=6671467.51 Mflops=7145086.72
z5-01           : Column=044544 Fraction=0.380 Kernel=6305464.96 Mflops=7143213.12
z5-01           : Column=045312 Fraction=0.385 Kernel=7004657.15 Mflops=7141840.98
z5-01           : Column=045696 Fraction=0.390 Kernel=6387893.65 Mflops=7142105.89
z5-01           : Column=046464 Fraction=0.395 Kernel=6929596.91 Mflops=7140075.25
z5-01           : Column=047232 Fraction=0.400 Kernel=7180378.44 Mflops=7140435.67
z5-01           : Column=047616 Fraction=0.405 Kernel=7153514.33 Mflops=7140169.04
z5-01           : Column=048384 Fraction=0.410 Kernel=6926588.55 Mflops=7138278.82
z5-01           : Column=048768 Fraction=0.415 Kernel=6561014.17 Mflops=7137179.32
z5-01           : Column=049536 Fraction=0.420 Kernel=6758216.59 Mflops=7133898.64
z5-01           : Column=049920 Fraction=0.425 Kernel=6422534.30 Mflops=7133007.47
z5-01           : Column=050688 Fraction=0.430 Kernel=6926115.67 Mflops=7131339.12
z5-01           : Column=051072 Fraction=0.435 Kernel=6400935.69 Mflops=7130409.65
z5-01           : Column=051840 Fraction=0.440 Kernel=6814574.47 Mflops=7127938.99
z5-01           : Column=052224 Fraction=0.445 Kernel=6464062.66 Mflops=7126670.35
z5-01           : Column=052992 Fraction=0.450 Kernel=6788322.80 Mflops=7124134.74
z5-01           : Column=053376 Fraction=0.455 Kernel=6418134.44 Mflops=7123265.27
z5-01           : Column=054144 Fraction=0.460 Kernel=6708133.15 Mflops=7120261.35
z5-01           : Column=054528 Fraction=0.465 Kernel=6552716.08 Mflops=7118875.95
z5-01           : Column=055296 Fraction=0.470 Kernel=6663058.87 Mflops=7115708.44
z5-01           : Column=055680 Fraction=0.475 Kernel=5416206.01 Mflops=7113836.72
z5-01           : Column=056448 Fraction=0.480 Kernel=6742469.94 Mflops=7111404.53
z5-01           : Column=056832 Fraction=0.485 Kernel=5594735.16 Mflops=7109729.98
z5-01           : Column=057600 Fraction=0.490 Kernel=6706192.71 Mflops=7107196.50
z5-01           : Column=057984 Fraction=0.495 Kernel=5249997.37 Mflops=7104745.65
z5-01           : Column=060672 Fraction=0.515 Kernel=6314706.67 Mflops=7092277.50
z5-01           : Column=062976 Fraction=0.535 Kernel=6279039.84 Mflops=7078892.17
z5-01           : Column=065280 Fraction=0.555 Kernel=6086762.28 Mflops=7063658.45
z5-01           : Column=067584 Fraction=0.575 Kernel=5931174.20 Mflops=7047563.32
z5-01           : Column=069888 Fraction=0.595 Kernel=5736288.05 Mflops=7030237.65
z5-01           : Column=072192 Fraction=0.615 Kernel=5572920.38 Mflops=7012479.26
z5-01           : Column=074496 Fraction=0.635 Kernel=5314241.35 Mflops=6993116.54
z5-01           : Column=076800 Fraction=0.655 Kernel=5071617.96 Mflops=6972731.11
z5-01           : Column=079104 Fraction=0.675 Kernel=4852267.15 Mflops=6951962.65
z5-01           : Column=081408 Fraction=0.695 Kernel=4634454.49 Mflops=6931099.90
z5-01           : Column=093312 Fraction=0.795 Kernel=3926486.47 Mflops=6828509.15
z5-01           : Column=104832 Fraction=0.895 Kernel=2596820.75 Mflops=6748739.93
z5-01           : Column=116736 Fraction=0.995 Kernel=1113984.74 Mflops=6710475.73
================================================================================
T/V                N    NB     P     Q               Time                 Gflops
--------------------------------------------------------------------------------
WR11R2L4      117120   384     1     2             159.75            6.70468e+03
HPL_pdgesv() start time Tue Mar 26 15:08:13 2024

HPL_pdgesv() end time   Tue Mar 26 15:10:52 2024

--------------------------------------------------------------------------------
||Ax-b||_oo/(eps*(||A||_oo*||x||_oo+||b||_oo)*N)=   3.28451406e-03 ...... PASSED
================================================================================

Finished      3 tests with the following results:
              3 tests completed and passed residual checks,
              0 tests completed and failed residual checks,
              0 tests skipped because of illegal input values.
--------------------------------------------------------------------------------

End of Tests.
================================================================================
Tue Mar 26 15:11:00 CDT 2024
#Avg.LastDay=536 W | 1829 Btu/hr
#Avg.LastHour=716 W | 2444 Btu/hr
#Avg.LastWeek=536 W | 1829 Btu/hr
#Cap.ActivePolicy.BtuHr=111834 Btu/hr
#Cap.ActivePolicy.Name=
#Cap.ActivePolicy.Watts=32767 W
Cap.BtuHr=111834 btu/hr
Cap.Enable=Disabled
#Cap.MaxThreshold=1220 W | 4165 Btu/hr
#Cap.MinThreshold=516 W | 1762 Btu/hr
Cap.Percent=100
Cap.Watts=32767 W
#EnergyConsumption=0.139 KWh | 474 Btu
#EnergyConsumption.Clear=******** (Write-Only)
#EnergyConsumption.StarttimeStamp=Tue Mar 26 15:01:59 2024
#Max.Amps=6.1 Amps
#Max.Amps.Timestamp=Tue Mar 26 15:10:36 2024
#Max.Headroom=0 W | 0 Btu/hr
#Max.LastDay=1268 W | 4328 Btu/hr
#Max.LastDay.Timestamp=Tue Mar 26 15:18:37 2024
#Max.LastHour=1268 W | 4328 Btu/hr
#Max.LastHour.Timestamp=Tue Mar 26 15:18:37 2024
#Max.LastWeek=1268 W | 4328 Btu/hr
#Max.LastWeek.Timestamp=Tue Mar 26 15:18:37 2024
#Max.Power=1272 W | 4341 Btu/hr
#Max.Power.Timestamp=Tue Mar 26 15:10:36 2024
#Max.PowerClear=******** (Write-Only)
#Min.LastDay=19 W | 65 Btu/hr
#Min.LastDay.Timestamp=Mon Mar 25 16:27:19 2024
#Min.LastHour=518 W | 1768 Btu/hr
#Min.LastHour.Timestamp=Tue Mar 26 14:54:57 2024
#Min.LastWeek=19 W | 65 Btu/hr
#Min.LastWeek.Timestamp=Mon Mar 25 16:27:19 2024
#PCIeAllocation=0
#Realtime.Amps=4.5 Amps
#Realtime.Power=933 W | 3184 Btu/hr
RedundancyPolicy=Not Redundant
#SCViewSledPwr=610
#ServerAllocation=658 W | 2246 Btu/hr
#Status=1

#ActivePolicyName=
#ActivePowerCapVal=32767
ChassisCurrentCapLimit=0
ChassisCurrentCapSetting=Disabled
GridACurrentCapLimit=1000000
GridACurrentCapSetting=Disabled
GridBCurrentCapLimit=1000000
GridBCurrentCapSetting=Disabled
GridCurrentCapLimit=0
GridCurrentCapSetting=Disabled
#GridCurrentLimitLowerBound=0
#GridCurrentLimitUpperBound=1000000
#PowerCapMaxThres=1220
#PowerCapMinThres=516
PowerCapSetting=Disabled
PowerCapValue=32767
Poweredbyparent=PoweredByChassis
PSRedPolicy=Not Redundant
#SCViewSledPwr=535
SystemCurrentCapLimit=1000000
SystemCurrentCapSetting=Disabled
#SystemCurrentLimitLowerBound=0
#SystemCurrentLimitUpperBound=1000000

[Key=system.Embedded.1#ServerPwrMon.1]
#AccumulativePower=1
#CumulativePowerStartTime=1711483319
#CumulativePowerStartTimeStr=2024-03-26T20:01:59Z
#MinPowerTime=1711483321
#MinPowerTimeStr=2024-03-26T20:02:01Z
#MinPowerWatts=523
#PeakCurrentTime=1711483836
#PeakCurrentTimeStr=2024-03-26T20:10:36Z
#PeakPowerStartTime=1711483319
#PeakPowerStartTimeStr=2024-03-26T20:01:59Z
#PeakPowerTime=1711483836
#PeakPowerTimeStr=2024-03-26T20:10:36Z
#PeakPowerWatts=1272
PowerConfigReset=None

PS1 Status                      Present                  AC             1270.000Watts
PS2 Status                      Present                  AC             1256.000Watts
PS1 Voltage 1                   Ok          204.00V             NA          NA
PS2 Voltage 2                   Ok          204.00V             NA          NA
PS1 Current 1                 Ok      6.2Amps  NA   NA       0Amps [N]      0Amps [N]
PS2 Current 2                 Ok      6.2Amps  NA   NA       0Amps [N]      0Amps [N]

Duration Above Warning Threshold as Percentage = 0.0%
Duration Above Critical Threshold as Percentage = 0.0%

Average Temperatures
Last Hour  = 22C ( 71.6F )
Last Day   = 20C ( 68.0F )
Last Week  = 19C ( 68.0F )
Last Month = 20C ( 68.0F )
Last Year  = 20C ( 68.0F )

Peak Temperatures
Last Hour  = 22C ( 71.6F ) [At Tue, 26 Mar 2024 14:57:44]
Last Day   = 23C ( 73.4F ) [At Mon, 25 Mar 2024 21:29:12]
Last Week  = 23C ( 73.4F ) [At Mon, 25 Mar 2024 21:29:12]
Last Month = 23C ( 73.4F ) [At Mon, 25 Mar 2024 21:29:12]
Last Year  = 34C ( 93.2F ) [At Wed, 06 Dec 2023 13:46:21]

Done: Tue Mar 26 15:11:05 CDT 2024
```

## Removed SLURM

### Run 1

#### Notes

- Suggestion from Intel support

#### Results

```bash
Binary name: 
-rwxr-xr-x 1 grant internal 7810144 Feb 20 11:48 xhpl_intel64_dynamic
This script: 
#!/bin/bash
#===============================================================================
# Copyright 2001-2023 Intel Corporation.
#
# This software and the related documents are Intel copyrighted  materials,  and
# your use of  them is  governed by the  express license  under which  they were
# provided to you (License).  Unless the License provides otherwise, you may not
# use, modify, copy, publish, distribute,  disclose or transmit this software or
# the related documents without Intel's prior written permission.
#
# This software and the related documents  are provided as  is,  with no express
# or implied  warranties,  other  than those  that are  expressly stated  in the
# License.
#===============================================================================

echo "This is a SAMPLE run script.  Change it to reflect the correct number"
echo "of CPUs/threads, number of nodes, MPI processes per node, etc.."

# Set total number of MPI processes for the HPL (should be equal to PxQ).
export MPI_PROC_NUM=8

# Set the MPI per node for each node.
# MPI_PER_NODE should be equal to 1 or number of sockets on the system.
# It will be same as -perhost or -ppn paramaters in mpirun/mpiexec.
export MPI_PER_NODE=8

# Set the number of NUMA nodes per MPI. (MPI_PER_NODE * NUMA_PER_MPI)
# should be equal to number of NUMA nodes on the system.
export NUMA_PER_MPI=1

#====================================================================
# Following option is for Intel(R) Optimized HPL-AI Benchmark
#====================================================================

# Comment in to enable Intel(R) Optimized HPL-AI Benchmark
# export USE_HPL_AI=1

#====================================================================
# Following option is for Intel(R) Optimized HPL-AI Benchmark for GPU
#====================================================================

# By default, Intel(R) Optimized HPL-AI Benchmark for GPU will use
# Bfloat16 matrix. If you prefer less iterations, you could choose
# float based matrix. But it will reduce maximum problem size. 
# export USE_BF16MAT=0

#====================================================================
# Following options are for Intel(R) Distribution for LINPACK
# Benchmark for GPU and Intel(R) Optimized HPL-AI Benchmark for GPU
#====================================================================

# Comment in to enable GPUs
# export USE_HPL_GPU=1

# Select backend driver for GPU (OpenCL ... 0, Level Zero ... 1)
# export HPL_DRIVER=0

# Number of stacks on each GPU
# export HPL_NUMSTACK=2

# Total number of GPUs on each node
# export HPL_NUMDEV=2

#====================================================================

export OUT=xhpl_intel64_dynamic_outputs.txt

if [ -z ${USE_HPL_AI} ]; then
if [ -z ${USE_HPL_GPU} ]; then
export HPL_EXE=xhpl_intel64_dynamic
else
export HPL_EXE=xhpl_intel64_dynamic_gpu
fi
else
if [ -z ${USE_HPL_GPU} ]; then
export HPL_EXE=xhpl-ai_intel64_dynamic
else
export HPL_EXE=xhpl-ai_intel64_dynamic_gpu
fi
fi

# Unset this variable to avoid initialization failure
unset I_MPI_OFFLOAD

echo -n "This run was done on: "
date

# Capture some meaningful data for future reference:
echo -n "This run was done on: " >> $OUT
date >> $OUT
echo "HPL.dat: " >> $OUT
cat HPL.dat >> $OUT
echo "Binary name: " >> $OUT
ls -l ${HPL_EXE} >> $OUT
echo "This script: " >> $OUT
cat runme_intel64_dynamic >> $OUT
echo "Environment variables: " >> $OUT
env >> $OUT
echo "Actual run: " >> $OUT

# Environment variables can also be also be set on the Intel(R) MPI Library command
# line using the -genv option (to appear before the -np 1):

mpirun -hostfile hosts -perhost ${MPI_PER_NODE} -np ${MPI_PROC_NUM} ./runme_intel64_prv "$@" | tee -a $OUT
#mpirun -hostfile hosts -np ${MPI_PROC_NUM} ./runme_intel64_prv "$@" | tee -a $OUT

echo -n "Done: " >> $OUT
date >> $OUT

echo -n "Done: "
date
Environment variables: 
LS_COLORS=rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=01;05;37;41:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.zst=01;31:*.tzst=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.wim=01;31:*.swm=01;31:*.dwm=01;31:*.esd=01;31:*.jpg=01;35:*.jpeg=01;35:*.mjpg=01;35:*.mjpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=01;36:*.au=01;36:*.flac=01;36:*.m4a=01;36:*.mid=01;36:*.midi=01;36:*.mka=01;36:*.mp3=01;36:*.mpc=01;36:*.ogg=01;36:*.ra=01;36:*.wav=01;36:*.oga=01;36:*.opus=01;36:*.spx=01;36:*.xspf=01;36:
LD_LIBRARY_PATH=/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/opt/mpi/libfabric/lib:/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/lib:/cm/shared/apps/slurm/current/lib64/slurm:/cm/shared/apps/slurm/current/lib64
__LMOD_REF_COUNT_PATH=/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/opt/mpi/libfabric/bin:1;/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/bin:1;/cm/shared/apps/slurm/current/sbin:1;/cm/shared/apps/slurm/current/bin:1;/usr/local/bin:1;/usr/bin:1;/usr/local/sbin:1;/usr/sbin:1;/opt/dell/srvadmin/bin:1;/home/grant/.local/bin:1;/home/grant/bin:1
_ModuleTable002_=WyJzdGFja0RlcHRoIl09MCxbInN0YXR1cyJdPSJhY3RpdmUiLFsidXNlck5hbWUiXT0iY29yZSIsfSxbImludGVsL29uZUFQSSJdPXtbImZuIl09Ii9ob21lL21vZHVsZXMvY29yZS9tb2R1bGVmaWxlcy9pbnRlbC9vbmVBUEkvMjAyNC4xLjAubHVhIixbImZ1bGxOYW1lIl09ImludGVsL29uZUFQSS8yMDI0LjEuMCIsWyJsb2FkT3JkZXIiXT01LHByb3BUPXt9LFsic3RhY2tEZXB0aCJdPTAsWyJzdGF0dXMiXT0iYWN0aXZlIixbInVzZXJOYW1lIl09ImludGVsL29uZUFQSS8yMDI0LjEuMCIsfSxtcGk9e1siZm4iXT0iL2hvbWUvbW9kdWxlcy9jb3JlL2NvbXBpbGVyL21vZHVsZWZpbGVzL29uZUFQSS0yMDI0LjEuMC9tcGkvMjAyMS4xMiIsWyJmdWxsTmFtZSJdPSJtcGkvMjAy
SSH_CONNECTION=10.140.50.2 44338 10.140.52.33 22
LANG=en_US.UTF-8
HISTCONTROL=ignoredups
HOSTNAME=z1-33
LMOD_SYSTEM_DEFAULT_MODULES=DefaultModules
OLDPWD=/home/grant/benchmarks_2024.1/linux/share/mkl/benchmarks
__LMOD_REF_COUNT__LMFILES_=/cm/local/modulefiles/shared:1;/usr/share/modulefiles/DefaultModules.lua:1;/cm/local/modulefiles/slurm/zenith/20.02.7:1;/cm/shared/modulefiles/core.lua:1;/home/modules/core/modulefiles/intel/oneAPI/2024.1.0.lua:1;/home/modules/core/compiler/modulefiles/oneAPI-2024.1.0/mpi/2021.12:1
OUT=xhpl_intel64_dynamic_outputs.txt
__LMOD_REF_COUNT_LD_LIBRARY_PATH=/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/opt/mpi/libfabric/lib:1;/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/lib:1;/cm/shared/apps/slurm/current/lib64/slurm:1;/cm/shared/apps/slurm/current/lib64:1
FI_PROVIDER_PATH=/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/opt/mpi/libfabric/lib/prov:/usr/lib64/libfabric
_ModuleTable004_=XT0xLFsic3RhdHVzIl09ImFjdGl2ZSIsWyJ1c2VyTmFtZSJdPSJzbHVybS96ZW5pdGgiLH0sfSxtcGF0aEE9eyIvaG9tZS9tb2R1bGVzL2NvcmUvY29tcGlsZXIvbW9kdWxlZmlsZXMvb25lQVBJLTIwMjQuMS4wIiwiL2hvbWUvbW9kdWxlcy9jb3JlL21vZHVsZWZpbGVzIiwiL2NtL2xvY2FsL21vZHVsZWZpbGVzIiwiL2V0Yy9tb2R1bGVmaWxlcyIsIi91c3Ivc2hhcmUvbW9kdWxlZmlsZXMiLCIvdXNyL3NoYXJlL01vZHVsZXMvbW9kdWxlZmlsZXMiLCIvY20vc2hhcmVkL21vZHVsZWZpbGVzIix9LFsic3lzdGVtQmFzZU1QQVRIIl09Ii9jbS9sb2NhbC9tb2R1bGVmaWxlczovY20vc2hhcmVkL21vZHVsZWZpbGVzOi9ldGMvbW9kdWxlZmlsZXM6L3Vzci9zaGFyZS9tb2R1bGVm
S_COLORS=auto
which_declare=declare -f
CLASSPATH=/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/share/java/mpi.jar
XDG_SESSION_ID=15518
USER=grant
__LMOD_REF_COUNT_MODULEPATH=/home/modules/core/compiler/modulefiles/oneAPI-2024.1.0:1;/home/modules/core/modulefiles:1;/cm/local/modulefiles:1;/etc/modulefiles:1;/usr/share/modulefiles:1;/usr/share/Modules/modulefiles:1;/cm/shared/modulefiles:2
__LMOD_REF_COUNT_LOADEDMODULES=shared:1;DefaultModules:1;slurm/zenith/20.02.7:1;core:1;intel/oneAPI/2024.1.0:1;mpi/2021.12:1
PWD=/home/grant/benchmarks_2024.1/linux/share/mkl/benchmarks/mp_linpack
ENABLE_LMOD=1
HOME=/home/grant
LMOD_COLORIZE=yes
SSH_CLIENT=10.140.50.2 44338 22
LMOD_VERSION=8.2.4
CPATH=/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/include:/cm/shared/apps/slurm/current/include
NUMA_PER_MPI=1
LMOD_SETTARG_CMD=:
BASH_ENV=/usr/share/lmod/lmod/init/bash
MPI_PROC_NUM=8
__LMOD_REF_COUNT_LIBRARY_PATH=/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/opt/mpi/libfabric/lib:1;/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/lib:1;/cm/shared/apps/slurm/current/lib64/slurm:1;/cm/shared/apps/slurm/current/lib64:1
LIBRARY_PATH=/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/opt/mpi/libfabric/lib:/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/lib:/cm/shared/apps/slurm/current/lib64/slurm:/cm/shared/apps/slurm/current/lib64
LMOD_sys=Linux
MPI_PER_NODE=8
_ModuleTable001_=X01vZHVsZVRhYmxlXz17WyJNVHZlcnNpb24iXT0zLFsiY19yZWJ1aWxkVGltZSJdPTg2NDAwLFsiY19zaG9ydFRpbWUiXT1mYWxzZSxkZXB0aFQ9e30sZmFtaWx5PXt9LG1UPXtEZWZhdWx0TW9kdWxlcz17WyJmbiJdPSIvdXNyL3NoYXJlL21vZHVsZWZpbGVzL0RlZmF1bHRNb2R1bGVzLmx1YSIsWyJmdWxsTmFtZSJdPSJEZWZhdWx0TW9kdWxlcyIsWyJsb2FkT3JkZXIiXT0yLHByb3BUPXt9LFsic3RhY2tEZXB0aCJdPTAsWyJzdGF0dXMiXT0iYWN0aXZlIixbInVzZXJOYW1lIl09IkRlZmF1bHRNb2R1bGVzIix9LGNvcmU9e1siZm4iXT0iL2NtL3NoYXJlZC9tb2R1bGVmaWxlcy9jb3JlLmx1YSIsWyJmdWxsTmFtZSJdPSJjb3JlIixbImxvYWRPcmRlciJdPTQscHJvcFQ9e30s
SLURM_CONF=/cm/shared/apps/slurm/var/etc/zenith/slurm.conf
LOADEDMODULES=shared:DefaultModules:slurm/zenith/20.02.7:core:intel/oneAPI/2024.1.0:mpi/2021.12
__LMOD_REF_COUNT_MANPATH=/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/share/man:1;/cm/shared/apps/slurm/current/man:1;/usr/share/lmod/lmod/share/man:1;/usr/local/share/man:1;/usr/share/man:1;/cm/local/apps/environment-modules/current/share/man:1
_ModuleTable003_=MS4xMiIsWyJsb2FkT3JkZXIiXT02LHByb3BUPXt9LFsic3RhY2tEZXB0aCJdPTAsWyJzdGF0dXMiXT0iYWN0aXZlIixbInVzZXJOYW1lIl09Im1waS8yMDIxLjEyIix9LHNoYXJlZD17WyJmbiJdPSIvY20vbG9jYWwvbW9kdWxlZmlsZXMvc2hhcmVkIixbImZ1bGxOYW1lIl09InNoYXJlZCIsWyJsb2FkT3JkZXIiXT0xLHByb3BUPXt9LFsic3RhY2tEZXB0aCJdPTEsWyJzdGF0dXMiXT0iYWN0aXZlIixbInVzZXJOYW1lIl09InNoYXJlZCIsfSxzbHVybT17WyJmbiJdPSIvY20vbG9jYWwvbW9kdWxlZmlsZXMvc2x1cm0vemVuaXRoLzIwLjAyLjciLFsiZnVsbE5hbWUiXT0ic2x1cm0vemVuaXRoLzIwLjAyLjciLFsibG9hZE9yZGVyIl09Myxwcm9wVD17fSxbInN0YWNrRGVwdGgi
LMOD_ROOT=/usr/share/lmod
SSH_TTY=/dev/pts/1
MAIL=/var/spool/mail/grant
LMOD_arch=x86_64
__Init_Default_Modules=1
CMD_WLM_CLUSTER_NAME=zenith
SHELL=/bin/bash
TERM=screen
HPL_EXE=xhpl_intel64_dynamic
_ModuleTable_Sz_=5
__LMOD_REF_COUNT_CPATH=/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/include:1;/cm/shared/apps/slurm/current/include:1
SPACK_SYSTEM_CONFIG=/home/modules/core/spack/etc
SHLVL=2
MANPATH=/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/share/man:/cm/shared/apps/slurm/current/man:/usr/share/lmod/lmod/share/man:/usr/local/share/man:/usr/share/man:/cm/local/apps/environment-modules/current/share/man
__LMOD_REF_COUNT_CLASSPATH=/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/share/java/mpi.jar:1
LMOD_PREPEND_BLOCK=normal
MODULEPATH=/home/modules/core/compiler/modulefiles/oneAPI-2024.1.0:/home/modules/core/modulefiles:/cm/local/modulefiles:/etc/modulefiles:/usr/share/modulefiles:/usr/share/Modules/modulefiles:/cm/shared/modulefiles
LOGNAME=grant
DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/11208/bus
CLUSTER=zenith
XDG_RUNTIME_DIR=/run/user/11208
MODULEPATH_ROOT=/usr/share/modulefiles
PATH=/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/opt/mpi/libfabric/bin:/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/bin:/cm/shared/apps/slurm/current/sbin:/cm/shared/apps/slurm/current/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/opt/dell/srvadmin/bin:/home/grant/.local/bin:/home/grant/bin
_LMFILES_=/cm/local/modulefiles/shared:/usr/share/modulefiles/DefaultModules.lua:/cm/local/modulefiles/slurm/zenith/20.02.7:/cm/shared/modulefiles/core.lua:/home/modules/core/modulefiles/intel/oneAPI/2024.1.0.lua:/home/modules/core/compiler/modulefiles/oneAPI-2024.1.0/mpi/2021.12
MODULESHOME=/usr/share/lmod/lmod
LMOD_SETTARG_FULL_SUPPORT=no
I_MPI_ROOT=/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12
HISTSIZE=1000
LMOD_PKG=/usr/share/lmod/lmod
LMOD_CMD=/usr/share/lmod/lmod/libexec/lmod
_ModuleTable005_=aWxlczovdXNyL3NoYXJlL01vZHVsZXMvbW9kdWxlZmlsZXMiLH0=
LESSOPEN=||/usr/bin/lesspipe.sh %s
LMOD_FULL_SETTARG_SUPPORT=no
LMOD_DIR=/usr/share/lmod/lmod/libexec
BASH_FUNC_which%%=() {  ( alias;
 eval ${which_declare} ) | /usr/bin/which --tty-only --read-alias --read-functions --show-tilde --show-dot $@
}
BASH_FUNC_module%%=() {  eval $($LMOD_CMD bash "$@") && eval $(${LMOD_SETTARG_CMD:-:} -s sh)
}
BASH_FUNC_ml%%=() {  eval $($LMOD_DIR/ml_cmd "$@")
}
_=/usr/bin/env
Actual run: 
RANK=0, NODE=0-0
RANK=6, NODE=6-6
RANK=7, NODE=7-7
RANK=5, NODE=5-5
RANK=1, NODE=1-1
RANK=2, NODE=2-2
RANK=3, NODE=3-3
RANK=4, NODE=4-4
================================================================================
HPLinpack 2.3  --  High-Performance Linpack benchmark  --   December 2, 2018
Written by A. Petitet and R. Clint Whaley,  Innovative Computing Laboratory, UTK
Modified by Piotr Luszczek, Innovative Computing Laboratory, UTK
Modified by Julien Langou, University of Colorado Denver
================================================================================

An explanation of the input/output parameters follows:
T/V    : Wall time / encoded variant.
N      : The order of the coefficient matrix A.
NB     : The partitioning blocking factor.
P      : The number of process rows.
Q      : The number of process columns.
Time   : Time in seconds to solve the linear system.
Gflops : Rate of execution for solving the linear system.

The following parameter values will be used:

N        :   80000 
NB       :     384 
PMAP     : Column-major process mapping
P        :       4 
Q        :       2 
PFACT    :   Right 
NBMIN    :       2 
NDIV     :       2 
RFACT    :   Crout 
BCAST    :   1ring 
DEPTH    :       0 
SWAP     : Binary-exchange
L1       : no-transposed form
U        : no-transposed form
EQUIL    : no
ALIGN    :    8 double precision words

--------------------------------------------------------------------------------

- The matrix A is randomly generated for each test.
- The following scaled residual check will be computed:
      ||Ax-b||_oo / ( eps * ( || x ||_oo * || A ||_oo + || b ||_oo ) * N )
- The relative machine precision (eps) is taken to be               1.110223e-16
- Computational tests pass if scaled residuals are less than                 1.0

z1-33           : Column=000768 Fraction=0.005 Kernel=    0.19 Mflops=11716921.90
z1-33           : Column=001152 Fraction=0.010 Kernel=7363621.65 Mflops=9759666.47
z1-33           : Column=001536 Fraction=0.015 Kernel=6612879.10 Mflops=8731528.63
z1-33           : Column=001920 Fraction=0.020 Kernel=6950926.49 Mflops=8351479.45
z1-33           : Column=002304 Fraction=0.025 Kernel=6924126.78 Mflops=8059259.53
z1-33           : Column=002688 Fraction=0.030 Kernel=6765311.76 Mflops=7874392.60
z1-33           : Column=003072 Fraction=0.035 Kernel=6873783.94 Mflops=7686750.05
z1-33           : Column=003456 Fraction=0.040 Kernel=7024359.34 Mflops=7625245.21
z1-33           : Column=003840 Fraction=0.045 Kernel=6893523.56 Mflops=7501441.99
z1-33           : Column=004224 Fraction=0.050 Kernel=6926701.78 Mflops=7482072.71
z1-33           : Column=004608 Fraction=0.055 Kernel=6718662.00 Mflops=7359253.03
z1-33           : Column=004992 Fraction=0.060 Kernel=6764161.65 Mflops=7382277.10
z1-33           : Column=005376 Fraction=0.065 Kernel=6662615.33 Mflops=7274460.46
z1-33           : Column=005760 Fraction=0.070 Kernel=6636785.32 Mflops=7295180.05
z1-33           : Column=006144 Fraction=0.075 Kernel=6851588.78 Mflops=7216028.17
z1-33           : Column=006528 Fraction=0.080 Kernel=6850487.39 Mflops=7251642.27
z1-33           : Column=006912 Fraction=0.085 Kernel=6782708.16 Mflops=7174633.41
z1-33           : Column=007296 Fraction=0.090 Kernel=6784437.15 Mflops=7200357.88
z1-33           : Column=007680 Fraction=0.095 Kernel=6727920.97 Mflops=7122304.82
z1-33           : Column=008064 Fraction=0.100 Kernel=6652066.69 Mflops=7160605.40
z1-33           : Column=008448 Fraction=0.105 Kernel=6895779.47 Mflops=7096245.40
z1-33           : Column=008832 Fraction=0.110 Kernel=6861647.32 Mflops=7136957.32
z1-33           : Column=009216 Fraction=0.115 Kernel=6791848.53 Mflops=7064777.92
z1-33           : Column=009984 Fraction=0.120 Kernel=6793690.41 Mflops=7045771.43
z1-33           : Column=010368 Fraction=0.125 Kernel=6749388.09 Mflops=7084333.14
z1-33           : Column=010752 Fraction=0.130 Kernel=6856061.64 Mflops=7028699.91
z1-33           : Column=011136 Fraction=0.135 Kernel=6961522.36 Mflops=7065222.47
z1-33           : Column=011520 Fraction=0.140 Kernel=6876839.39 Mflops=7013362.57
z1-33           : Column=011904 Fraction=0.145 Kernel=6969524.12 Mflops=7051004.31
z1-33           : Column=012288 Fraction=0.150 Kernel=6774538.80 Mflops=6993509.61
z1-33           : Column=012672 Fraction=0.155 Kernel=6979493.10 Mflops=7035167.25
z1-33           : Column=013056 Fraction=0.160 Kernel=6786957.72 Mflops=6983105.79
z1-33           : Column=013440 Fraction=0.165 Kernel=7073116.94 Mflops=7020960.90
z1-33           : Column=013824 Fraction=0.170 Kernel=6816478.09 Mflops=6971082.61
z1-33           : Column=014208 Fraction=0.175 Kernel=6557207.01 Mflops=7005285.23
z1-33           : Column=014592 Fraction=0.180 Kernel=7154202.20 Mflops=6966675.88
z1-33           : Column=014976 Fraction=0.185 Kernel=6849070.75 Mflops=6997789.73
z1-33           : Column=015360 Fraction=0.190 Kernel=6752580.10 Mflops=6953314.50
z1-33           : Column=015744 Fraction=0.195 Kernel=6966117.68 Mflops=6985288.95
z1-33           : Column=016128 Fraction=0.200 Kernel=6956871.18 Mflops=6948461.52
z1-33           : Column=016512 Fraction=0.205 Kernel=6675480.85 Mflops=6973188.78
z1-33           : Column=016896 Fraction=0.210 Kernel=6876869.44 Mflops=6940900.05
z1-33           : Column=017280 Fraction=0.215 Kernel=6585150.57 Mflops=6968534.48
z1-33           : Column=017664 Fraction=0.220 Kernel=6813042.03 Mflops=6932521.51
z1-33           : Column=018048 Fraction=0.225 Kernel=6536704.44 Mflops=6961467.67
z1-33           : Column=018432 Fraction=0.230 Kernel=6649074.79 Mflops=6925063.42
z1-33           : Column=018816 Fraction=0.235 Kernel=6601383.67 Mflops=6950548.91
z1-33           : Column=019584 Fraction=0.240 Kernel=6623583.93 Mflops=6940546.93
z1-33           : Column=019968 Fraction=0.245 Kernel=6802508.47 Mflops=6915730.38
z1-33           : Column=020352 Fraction=0.250 Kernel=7000766.08 Mflops=6938240.41
z1-33           : Column=020736 Fraction=0.255 Kernel=6798505.60 Mflops=6910594.47
z1-33           : Column=021120 Fraction=0.260 Kernel=6642918.92 Mflops=6929815.79
z1-33           : Column=021504 Fraction=0.265 Kernel=6821280.22 Mflops=6906166.51
z1-33           : Column=021888 Fraction=0.270 Kernel=6667880.30 Mflops=6923757.15
z1-33           : Column=022272 Fraction=0.275 Kernel=6785333.55 Mflops=6901454.39
z1-33           : Column=022656 Fraction=0.280 Kernel=6579022.72 Mflops=6916404.63
z1-33           : Column=023040 Fraction=0.285 Kernel=6687156.85 Mflops=6897139.71
z1-33           : Column=023424 Fraction=0.290 Kernel=6498323.61 Mflops=6911070.48
z1-33           : Column=023808 Fraction=0.295 Kernel=6686128.97 Mflops=6892180.96
z1-33           : Column=024192 Fraction=0.300 Kernel=6263821.45 Mflops=6905904.15
z1-33           : Column=024576 Fraction=0.305 Kernel=6850082.25 Mflops=6889335.51
z1-33           : Column=024960 Fraction=0.310 Kernel=6890655.28 Mflops=6904143.63
z1-33           : Column=025344 Fraction=0.315 Kernel=6473159.49 Mflops=6881478.56
z1-33           : Column=025728 Fraction=0.320 Kernel=6555840.26 Mflops=6897980.25
z1-33           : Column=026112 Fraction=0.325 Kernel=6756174.27 Mflops=6877624.69
z1-33           : Column=026496 Fraction=0.330 Kernel=6411799.76 Mflops=6893025.86
z1-33           : Column=026880 Fraction=0.335 Kernel=6593691.64 Mflops=6874181.95
z1-33           : Column=027264 Fraction=0.340 Kernel=6573387.84 Mflops=6887976.33
z1-33           : Column=027648 Fraction=0.345 Kernel=6500760.63 Mflops=6867231.24
z1-33           : Column=028032 Fraction=0.350 Kernel=6783632.21 Mflops=6882431.46
z1-33           : Column=028416 Fraction=0.355 Kernel=6912695.64 Mflops=6867181.91
z1-33           : Column=029184 Fraction=0.360 Kernel=6473290.63 Mflops=6860569.57
z1-33           : Column=029568 Fraction=0.365 Kernel=6829939.89 Mflops=6875906.26
z1-33           : Column=029952 Fraction=0.370 Kernel=6874113.40 Mflops=6858682.15
z1-33           : Column=030336 Fraction=0.375 Kernel=6284538.15 Mflops=6869121.28
z1-33           : Column=030720 Fraction=0.380 Kernel=6723997.41 Mflops=6855053.48
z1-33           : Column=031104 Fraction=0.385 Kernel=6950924.24 Mflops=6867698.78
z1-33           : Column=031488 Fraction=0.390 Kernel=6295696.57 Mflops=6851010.76
z1-33           : Column=031872 Fraction=0.395 Kernel=6533696.03 Mflops=6862301.28
z1-33           : Column=032256 Fraction=0.400 Kernel=6591764.67 Mflops=6848292.84
z1-33           : Column=032640 Fraction=0.405 Kernel=6641674.27 Mflops=6857273.70
z1-33           : Column=033024 Fraction=0.410 Kernel=6619450.56 Mflops=6846316.53
z1-33           : Column=033408 Fraction=0.415 Kernel=6524645.47 Mflops=6856317.84
z1-33           : Column=033792 Fraction=0.420 Kernel=6391703.45 Mflops=6843535.61
z1-33           : Column=034176 Fraction=0.425 Kernel=6677345.57 Mflops=6852521.31
z1-33           : Column=034560 Fraction=0.430 Kernel=6736423.62 Mflops=6842071.36
z1-33           : Column=034944 Fraction=0.435 Kernel=6133771.54 Mflops=6847441.02
z1-33           : Column=035328 Fraction=0.440 Kernel=6978257.91 Mflops=6839812.58
z1-33           : Column=035712 Fraction=0.445 Kernel=6657006.92 Mflops=6845187.92
z1-33           : Column=036096 Fraction=0.450 Kernel=6434124.02 Mflops=6836435.96
z1-33           : Column=036480 Fraction=0.455 Kernel=6691061.79 Mflops=6842612.55
z1-33           : Column=036864 Fraction=0.460 Kernel=6339396.74 Mflops=6833410.05
z1-33           : Column=037248 Fraction=0.465 Kernel=6682575.22 Mflops=6839242.67
z1-33           : Column=037632 Fraction=0.470 Kernel=6306002.44 Mflops=6832465.77
z1-33           : Column=038016 Fraction=0.475 Kernel=6526839.41 Mflops=6836852.84
z1-33           : Column=038784 Fraction=0.480 Kernel=6665549.44 Mflops=6835280.94
z1-33           : Column=039168 Fraction=0.485 Kernel=7019548.95 Mflops=6829552.56
z1-33           : Column=039552 Fraction=0.490 Kernel=6810299.07 Mflops=6832005.64
z1-33           : Column=039936 Fraction=0.495 Kernel=6503878.70 Mflops=6826189.68
z1-33           : Column=041472 Fraction=0.515 Kernel=6561172.42 Mflops=6821878.14
z1-33           : Column=043008 Fraction=0.535 Kernel=6627478.01 Mflops=6819029.43
z1-33           : Column=044544 Fraction=0.555 Kernel=6458021.97 Mflops=6814101.30
z1-33           : Column=046080 Fraction=0.575 Kernel=6521245.08 Mflops=6810515.31
z1-33           : Column=047616 Fraction=0.595 Kernel=6497878.41 Mflops=6807044.95
z1-33           : Column=049536 Fraction=0.615 Kernel=6436600.49 Mflops=6803282.93
z1-33           : Column=051072 Fraction=0.635 Kernel=6326327.85 Mflops=6799011.81
z1-33           : Column=052608 Fraction=0.655 Kernel=6274765.76 Mflops=6794789.77
z1-33           : Column=054144 Fraction=0.675 Kernel=6381389.50 Mflops=6791883.93
z1-33           : Column=055680 Fraction=0.695 Kernel=6110595.79 Mflops=6787471.87
z1-33           : Column=063744 Fraction=0.795 Kernel=5810908.08 Mflops=6765762.19
z1-33           : Column=071808 Fraction=0.895 Kernel=4042951.52 Mflops=6732907.06
z1-33           : Column=079872 Fraction=0.995 Kernel=1283946.41 Mflops=6702622.18
================================================================================
T/V                N    NB     P     Q               Time                 Gflops
--------------------------------------------------------------------------------
WC00C2R2       80000   384     4     2              51.05            6.68634e+03
HPL_pdgesv() start time Fri Apr  5 10:48:20 2024

HPL_pdgesv() end time   Fri Apr  5 10:49:11 2024

--------------------------------------------------------------------------------
||Ax-b||_oo/(eps*(||A||_oo*||x||_oo+||b||_oo)*N)=   3.99007393e-03 ...... PASSED
================================================================================

Finished      1 tests with the following results:
              1 tests completed and passed residual checks,
              0 tests completed and failed residual checks,
              0 tests skipped because of illegal input values.
--------------------------------------------------------------------------------

End of Tests.
```

### Run 2 Fri Apr  5 11:15:50 CDT 2024

#### Notes

- P and Q no longer work when just matching np it looks like. This performance was terrible.

#### Results

```bash
Binary name: 
-rwxr-xr-x 1 grant internal 7810144 Feb 20 11:48 xhpl_intel64_dynamic
This script: 
#!/bin/bash
#===============================================================================
# Copyright 2001-2023 Intel Corporation.
#
# This software and the related documents are Intel copyrighted  materials,  and
# your use of  them is  governed by the  express license  under which  they were
# provided to you (License).  Unless the License provides otherwise, you may not
# use, modify, copy, publish, distribute,  disclose or transmit this software or
# the related documents without Intel's prior written permission.
#
# This software and the related documents  are provided as  is,  with no express
# or implied  warranties,  other  than those  that are  expressly stated  in the
# License.
#===============================================================================

echo "This is a SAMPLE run script.  Change it to reflect the correct number"
echo "of CPUs/threads, number of nodes, MPI processes per node, etc.."

# Set total number of MPI processes for the HPL (should be equal to PxQ).
export MPI_PROC_NUM=8

# Set the MPI per node for each node.
# MPI_PER_NODE should be equal to 1 or number of sockets on the system.
# It will be same as -perhost or -ppn paramaters in mpirun/mpiexec.
export MPI_PER_NODE=2

# Set the number of NUMA nodes per MPI. (MPI_PER_NODE * NUMA_PER_MPI)
# should be equal to number of NUMA nodes on the system.
export NUMA_PER_MPI=1

#====================================================================
# Following option is for Intel(R) Optimized HPL-AI Benchmark
#====================================================================

# Comment in to enable Intel(R) Optimized HPL-AI Benchmark
# export USE_HPL_AI=1

#====================================================================
# Following option is for Intel(R) Optimized HPL-AI Benchmark for GPU
#====================================================================

# By default, Intel(R) Optimized HPL-AI Benchmark for GPU will use
# Bfloat16 matrix. If you prefer less iterations, you could choose
# float based matrix. But it will reduce maximum problem size. 
# export USE_BF16MAT=0

#====================================================================
# Following options are for Intel(R) Distribution for LINPACK
# Benchmark for GPU and Intel(R) Optimized HPL-AI Benchmark for GPU
#====================================================================

# Comment in to enable GPUs
# export USE_HPL_GPU=1

# Select backend driver for GPU (OpenCL ... 0, Level Zero ... 1)
# export HPL_DRIVER=0

# Number of stacks on each GPU
# export HPL_NUMSTACK=2

# Total number of GPUs on each node
# export HPL_NUMDEV=2

#====================================================================

export OUT=xhpl_intel64_dynamic_outputs.txt

if [ -z ${USE_HPL_AI} ]; then
if [ -z ${USE_HPL_GPU} ]; then
export HPL_EXE=xhpl_intel64_dynamic
else
export HPL_EXE=xhpl_intel64_dynamic_gpu
fi
else
if [ -z ${USE_HPL_GPU} ]; then
export HPL_EXE=xhpl-ai_intel64_dynamic
else
export HPL_EXE=xhpl-ai_intel64_dynamic_gpu
fi
fi

# Unset this variable to avoid initialization failure
unset I_MPI_OFFLOAD

echo -n "This run was done on: "
date

# Capture some meaningful data for future reference:
echo -n "This run was done on: " >> $OUT
date >> $OUT
echo "HPL.dat: " >> $OUT
cat HPL.dat >> $OUT
echo "Binary name: " >> $OUT
ls -l ${HPL_EXE} >> $OUT
echo "This script: " >> $OUT
cat runme_intel64_dynamic >> $OUT
echo "Environment variables: " >> $OUT
env >> $OUT
echo "Actual run: " >> $OUT

# Environment variables can also be also be set on the Intel(R) MPI Library command
# line using the -genv option (to appear before the -np 1):

#mpirun -hostfile hosts -perhost ${MPI_PER_NODE} -np ${MPI_PROC_NUM} ./runme_intel64_prv "$@" | tee -a $OUT
mpirun -hostfile hosts -np ${MPI_PROC_NUM} ./runme_intel64_prv "$@" | tee -a $OUT

echo -n "Done: " >> $OUT
date >> $OUT

echo -n "Done: "
date
Environment variables: 
LS_COLORS=rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=01;05;37;41:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.zst=01;31:*.tzst=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.wim=01;31:*.swm=01;31:*.dwm=01;31:*.esd=01;31:*.jpg=01;35:*.jpeg=01;35:*.mjpg=01;35:*.mjpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=01;36:*.au=01;36:*.flac=01;36:*.m4a=01;36:*.mid=01;36:*.midi=01;36:*.mka=01;36:*.mp3=01;36:*.mpc=01;36:*.ogg=01;36:*.ra=01;36:*.wav=01;36:*.oga=01;36:*.opus=01;36:*.spx=01;36:*.xspf=01;36:
LD_LIBRARY_PATH=/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/opt/mpi/libfabric/lib:/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/lib:/cm/shared/apps/slurm/current/lib64/slurm:/cm/shared/apps/slurm/current/lib64
__LMOD_REF_COUNT_PATH=/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/opt/mpi/libfabric/bin:1;/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/bin:1;/cm/shared/apps/slurm/current/sbin:1;/cm/shared/apps/slurm/current/bin:1;/usr/local/bin:1;/usr/bin:1;/usr/local/sbin:1;/usr/sbin:1;/opt/dell/srvadmin/bin:1;/home/grant/.local/bin:1;/home/grant/bin:1
_ModuleTable002_=WyJzdGFja0RlcHRoIl09MCxbInN0YXR1cyJdPSJhY3RpdmUiLFsidXNlck5hbWUiXT0iY29yZSIsfSxbImludGVsL29uZUFQSSJdPXtbImZuIl09Ii9ob21lL21vZHVsZXMvY29yZS9tb2R1bGVmaWxlcy9pbnRlbC9vbmVBUEkvMjAyNC4xLjAubHVhIixbImZ1bGxOYW1lIl09ImludGVsL29uZUFQSS8yMDI0LjEuMCIsWyJsb2FkT3JkZXIiXT01LHByb3BUPXt9LFsic3RhY2tEZXB0aCJdPTAsWyJzdGF0dXMiXT0iYWN0aXZlIixbInVzZXJOYW1lIl09ImludGVsL29uZUFQSS8yMDI0LjEuMCIsfSxtcGk9e1siZm4iXT0iL2hvbWUvbW9kdWxlcy9jb3JlL2NvbXBpbGVyL21vZHVsZWZpbGVzL29uZUFQSS0yMDI0LjEuMC9tcGkvMjAyMS4xMiIsWyJmdWxsTmFtZSJdPSJtcGkvMjAy
SSH_CONNECTION=10.140.50.2 44338 10.140.52.33 22
LANG=en_US.UTF-8
HISTCONTROL=ignoredups
HOSTNAME=z1-33
LMOD_SYSTEM_DEFAULT_MODULES=DefaultModules
OLDPWD=/home/grant/benchmarks_2024.1/linux/share/mkl/benchmarks
__LMOD_REF_COUNT__LMFILES_=/cm/local/modulefiles/shared:1;/usr/share/modulefiles/DefaultModules.lua:1;/cm/local/modulefiles/slurm/zenith/20.02.7:1;/cm/shared/modulefiles/core.lua:1;/home/modules/core/modulefiles/intel/oneAPI/2024.1.0.lua:1;/home/modules/core/compiler/modulefiles/oneAPI-2024.1.0/mpi/2021.12:1
OUT=xhpl_intel64_dynamic_outputs.txt
__LMOD_REF_COUNT_LD_LIBRARY_PATH=/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/opt/mpi/libfabric/lib:1;/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/lib:1;/cm/shared/apps/slurm/current/lib64/slurm:1;/cm/shared/apps/slurm/current/lib64:1
FI_PROVIDER_PATH=/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/opt/mpi/libfabric/lib/prov:/usr/lib64/libfabric
_ModuleTable004_=XT0xLFsic3RhdHVzIl09ImFjdGl2ZSIsWyJ1c2VyTmFtZSJdPSJzbHVybS96ZW5pdGgiLH0sfSxtcGF0aEE9eyIvaG9tZS9tb2R1bGVzL2NvcmUvY29tcGlsZXIvbW9kdWxlZmlsZXMvb25lQVBJLTIwMjQuMS4wIiwiL2hvbWUvbW9kdWxlcy9jb3JlL21vZHVsZWZpbGVzIiwiL2NtL2xvY2FsL21vZHVsZWZpbGVzIiwiL2V0Yy9tb2R1bGVmaWxlcyIsIi91c3Ivc2hhcmUvbW9kdWxlZmlsZXMiLCIvdXNyL3NoYXJlL01vZHVsZXMvbW9kdWxlZmlsZXMiLCIvY20vc2hhcmVkL21vZHVsZWZpbGVzIix9LFsic3lzdGVtQmFzZU1QQVRIIl09Ii9jbS9sb2NhbC9tb2R1bGVmaWxlczovY20vc2hhcmVkL21vZHVsZWZpbGVzOi9ldGMvbW9kdWxlZmlsZXM6L3Vzci9zaGFyZS9tb2R1bGVm
S_COLORS=auto
which_declare=declare -f
CLASSPATH=/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/share/java/mpi.jar
XDG_SESSION_ID=15518
USER=grant
__LMOD_REF_COUNT_MODULEPATH=/home/modules/core/compiler/modulefiles/oneAPI-2024.1.0:1;/home/modules/core/modulefiles:1;/cm/local/modulefiles:1;/etc/modulefiles:1;/usr/share/modulefiles:1;/usr/share/Modules/modulefiles:1;/cm/shared/modulefiles:2
__LMOD_REF_COUNT_LOADEDMODULES=shared:1;DefaultModules:1;slurm/zenith/20.02.7:1;core:1;intel/oneAPI/2024.1.0:1;mpi/2021.12:1
PWD=/home/grant/benchmarks_2024.1/linux/share/mkl/benchmarks/mp_linpack
ENABLE_LMOD=1
HOME=/home/grant
LMOD_COLORIZE=yes
SSH_CLIENT=10.140.50.2 44338 22
LMOD_VERSION=8.2.4
CPATH=/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/include:/cm/shared/apps/slurm/current/include
NUMA_PER_MPI=1
LMOD_SETTARG_CMD=:
BASH_ENV=/usr/share/lmod/lmod/init/bash
MPI_PROC_NUM=8
__LMOD_REF_COUNT_LIBRARY_PATH=/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/opt/mpi/libfabric/lib:1;/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/lib:1;/cm/shared/apps/slurm/current/lib64/slurm:1;/cm/shared/apps/slurm/current/lib64:1
LIBRARY_PATH=/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/opt/mpi/libfabric/lib:/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/lib:/cm/shared/apps/slurm/current/lib64/slurm:/cm/shared/apps/slurm/current/lib64
LMOD_sys=Linux
MPI_PER_NODE=2
_ModuleTable001_=X01vZHVsZVRhYmxlXz17WyJNVHZlcnNpb24iXT0zLFsiY19yZWJ1aWxkVGltZSJdPTg2NDAwLFsiY19zaG9ydFRpbWUiXT1mYWxzZSxkZXB0aFQ9e30sZmFtaWx5PXt9LG1UPXtEZWZhdWx0TW9kdWxlcz17WyJmbiJdPSIvdXNyL3NoYXJlL21vZHVsZWZpbGVzL0RlZmF1bHRNb2R1bGVzLmx1YSIsWyJmdWxsTmFtZSJdPSJEZWZhdWx0TW9kdWxlcyIsWyJsb2FkT3JkZXIiXT0yLHByb3BUPXt9LFsic3RhY2tEZXB0aCJdPTAsWyJzdGF0dXMiXT0iYWN0aXZlIixbInVzZXJOYW1lIl09IkRlZmF1bHRNb2R1bGVzIix9LGNvcmU9e1siZm4iXT0iL2NtL3NoYXJlZC9tb2R1bGVmaWxlcy9jb3JlLmx1YSIsWyJmdWxsTmFtZSJdPSJjb3JlIixbImxvYWRPcmRlciJdPTQscHJvcFQ9e30s
SLURM_CONF=/cm/shared/apps/slurm/var/etc/zenith/slurm.conf
LOADEDMODULES=shared:DefaultModules:slurm/zenith/20.02.7:core:intel/oneAPI/2024.1.0:mpi/2021.12
__LMOD_REF_COUNT_MANPATH=/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/share/man:1;/cm/shared/apps/slurm/current/man:1;/usr/share/lmod/lmod/share/man:1;/usr/local/share/man:1;/usr/share/man:1;/cm/local/apps/environment-modules/current/share/man:1
_ModuleTable003_=MS4xMiIsWyJsb2FkT3JkZXIiXT02LHByb3BUPXt9LFsic3RhY2tEZXB0aCJdPTAsWyJzdGF0dXMiXT0iYWN0aXZlIixbInVzZXJOYW1lIl09Im1waS8yMDIxLjEyIix9LHNoYXJlZD17WyJmbiJdPSIvY20vbG9jYWwvbW9kdWxlZmlsZXMvc2hhcmVkIixbImZ1bGxOYW1lIl09InNoYXJlZCIsWyJsb2FkT3JkZXIiXT0xLHByb3BUPXt9LFsic3RhY2tEZXB0aCJdPTEsWyJzdGF0dXMiXT0iYWN0aXZlIixbInVzZXJOYW1lIl09InNoYXJlZCIsfSxzbHVybT17WyJmbiJdPSIvY20vbG9jYWwvbW9kdWxlZmlsZXMvc2x1cm0vemVuaXRoLzIwLjAyLjciLFsiZnVsbE5hbWUiXT0ic2x1cm0vemVuaXRoLzIwLjAyLjciLFsibG9hZE9yZGVyIl09Myxwcm9wVD17fSxbInN0YWNrRGVwdGgi
LMOD_ROOT=/usr/share/lmod
SSH_TTY=/dev/pts/1
MAIL=/var/spool/mail/grant
LMOD_arch=x86_64
__Init_Default_Modules=1
CMD_WLM_CLUSTER_NAME=zenith
SHELL=/bin/bash
TERM=screen
HPL_EXE=xhpl_intel64_dynamic
_ModuleTable_Sz_=5
__LMOD_REF_COUNT_CPATH=/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/include:1;/cm/shared/apps/slurm/current/include:1
SPACK_SYSTEM_CONFIG=/home/modules/core/spack/etc
SHLVL=2
MANPATH=/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/share/man:/cm/shared/apps/slurm/current/man:/usr/share/lmod/lmod/share/man:/usr/local/share/man:/usr/share/man:/cm/local/apps/environment-modules/current/share/man
__LMOD_REF_COUNT_CLASSPATH=/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/share/java/mpi.jar:1
LMOD_PREPEND_BLOCK=normal
MODULEPATH=/home/modules/core/compiler/modulefiles/oneAPI-2024.1.0:/home/modules/core/modulefiles:/cm/local/modulefiles:/etc/modulefiles:/usr/share/modulefiles:/usr/share/Modules/modulefiles:/cm/shared/modulefiles
LOGNAME=grant
DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/11208/bus
CLUSTER=zenith
XDG_RUNTIME_DIR=/run/user/11208
MODULEPATH_ROOT=/usr/share/modulefiles
PATH=/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/opt/mpi/libfabric/bin:/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/bin:/cm/shared/apps/slurm/current/sbin:/cm/shared/apps/slurm/current/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/opt/dell/srvadmin/bin:/home/grant/.local/bin:/home/grant/bin
_LMFILES_=/cm/local/modulefiles/shared:/usr/share/modulefiles/DefaultModules.lua:/cm/local/modulefiles/slurm/zenith/20.02.7:/cm/shared/modulefiles/core.lua:/home/modules/core/modulefiles/intel/oneAPI/2024.1.0.lua:/home/modules/core/compiler/modulefiles/oneAPI-2024.1.0/mpi/2021.12
MODULESHOME=/usr/share/lmod/lmod
LMOD_SETTARG_FULL_SUPPORT=no
I_MPI_ROOT=/home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12
HISTSIZE=1000
LMOD_PKG=/usr/share/lmod/lmod
LMOD_CMD=/usr/share/lmod/lmod/libexec/lmod
_ModuleTable005_=aWxlczovdXNyL3NoYXJlL01vZHVsZXMvbW9kdWxlZmlsZXMiLH0=
LESSOPEN=||/usr/bin/lesspipe.sh %s
LMOD_FULL_SETTARG_SUPPORT=no
LMOD_DIR=/usr/share/lmod/lmod/libexec
BASH_FUNC_which%%=() {  ( alias;
 eval ${which_declare} ) | /usr/bin/which --tty-only --read-alias --read-functions --show-tilde --show-dot $@
}
BASH_FUNC_module%%=() {  eval $($LMOD_CMD bash "$@") && eval $(${LMOD_SETTARG_CMD:-:} -s sh)
}
BASH_FUNC_ml%%=() {  eval $($LMOD_DIR/ml_cmd "$@")
}
_=/usr/bin/env
Actual run: 
RANK=0, NODE=0-0
RANK=1, NODE=1-1
RANK=2, NODE=0-0
RANK=3, NODE=1-1
RANK=4, NODE=0-0
RANK=5, NODE=1-1
RANK=6, NODE=0-0
RANK=7, NODE=1-1
================================================================================
HPLinpack 2.3  --  High-Performance Linpack benchmark  --   December 2, 2018
Written by A. Petitet and R. Clint Whaley,  Innovative Computing Laboratory, UTK
Modified by Piotr Luszczek, Innovative Computing Laboratory, UTK
Modified by Julien Langou, University of Colorado Denver
================================================================================

An explanation of the input/output parameters follows:
T/V    : Wall time / encoded variant.
N      : The order of the coefficient matrix A.
NB     : The partitioning blocking factor.
P      : The number of process rows.
Q      : The number of process columns.
Time   : Time in seconds to solve the linear system.
Gflops : Rate of execution for solving the linear system.

The following parameter values will be used:

N        :  117120 
NB       :     384 
PMAP     : Column-major process mapping
P        :       2 
Q        :       4 
PFACT    :   Right 
NBMIN    :       2 
NDIV     :       2 
RFACT    :   Crout 
BCAST    :   1ring 
DEPTH    :       0 
SWAP     : Binary-exchange
L1       : no-transposed form
U        : no-transposed form
EQUIL    : no
ALIGN    :    8 double precision words

--------------------------------------------------------------------------------

- The matrix A is randomly generated for each test.
- The following scaled residual check will be computed:
      ||Ax-b||_oo / ( eps * ( || x ||_oo * || A ||_oo + || b ||_oo ) * N )
- The relative machine precision (eps) is taken to be               1.110223e-16
- Computational tests pass if scaled residuals are less than                 1.0

z1-33           : Column=000768 Fraction=0.005 Kernel=    0.61 Mflops=160604.34
z1-33           : Column=001536 Fraction=0.010 Kernel=161173.44 Mflops=164478.46
z1-33           : Column=001920 Fraction=0.015 Kernel=85724.20 Mflops=152336.54
Done: Fri Apr  5 11:15:50 CDT 2024
```