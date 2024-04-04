
# Understand and Run LINPACK

- [Understand and Run LINPACK](#understand-and-run-linpack)
  - [Running Intel Math Kernel Library (MKL) LINPACK Benchmark](#running-intel-math-kernel-library-mkl-linpack-benchmark)
    - [Install](#install)
    - [Running](#running)
  - [Additional Info](#additional-info)
  - [LINPACK Parameters](#linpack-parameters)
  - [How MPI Processes Work](#how-mpi-processes-work)
    - [What are MPI Processes?](#what-are-mpi-processes)
    - [How MPI Processes Communicate](#how-mpi-processes-communicate)
    - [Creating MPI Processes](#creating-mpi-processes)
    - [Distribution of Work](#distribution-of-work)
    - [Running MPI Programs](#running-mpi-programs)
    - [MPI Ranks](#mpi-ranks)
      - [MPI Ranks as Related to LU Decomposition](#mpi-ranks-as-related-to-lu-decomposition)
    - [MPI Arguments](#mpi-arguments)
    - [-np (Number of Processes)](#-np-number-of-processes)
    - [-ppn (Processes Per Node) aka perhost](#-ppn-processes-per-node-aka-perhost)
    - [Relation to Threads](#relation-to-threads)
    - [Practical Example](#practical-example)
      - [A Note About MPI Implementations](#a-note-about-mpi-implementations)
  - [Run Against a Single Node](#run-against-a-single-node)
    - [Install](#install-1)
    - [Running the Code](#running-the-code)
  - [Run on a Cluster w/SLURM](#run-on-a-cluster-wslurm)
    - [Configure runme\_intel64\_dynamic](#configure-runme_intel64_dynamic)
    - [Gain Access to Cluster](#gain-access-to-cluster)
    - [Running Job](#running-job)
  - [Useful Commands](#useful-commands)
  - [Useful Links](#useful-links)
  - [TODO NOTES](#todo-notes)
  - [Run a Job in SLURM that Gives You Node Access](#run-a-job-in-slurm-that-gives-you-node-access)
  - [How does `-pernode / -ppn` work?](#how-does--pernode---ppn-work)
    - [I\_MPI\_PERHOST](#i_mpi_perhost)
      - [Syntax](#syntax)
      - [Argument](#argument)
      - [Description](#description)
    - [I\_MPI\_JOB\_RESPECT\_PROCESS\_PLACEMENT](#i_mpi_job_respect_process_placement)
      - [Syntax](#syntax-1)
      - [Argument](#argument-1)
      - [Description](#description-1)
    - [Understanding What Rank and Node Mean in Output](#understanding-what-rank-and-node-mean-in-output)


The LINPACK Benchmarkfocuses on solving a dense system of linear equations. The core of the LINPACK Benchmark involves measuring the performance of a system when solving the equation $Ax = b$, where $A$ is a dense $n \times n$ matrix, $x$ is a vector of unknowns, and $b$ is a vector of knowns. The benchmark assesses the system's floating-point computation capabilities, primarily through the execution speed of Double Precision General Matrix Multiply (DGEMM) operations and the LU decomposition of the matrix $A$.

The following is a description of what it does.



## Running Intel Math Kernel Library (MKL) LINPACK Benchmark

Intel's version of LINPACK is unsurprisingly highly tuned for Intel. It provides routines that are specifically tuned to leverage the capabilities of Intel processors, such as utilizing vectorization, advanced instruction sets (e.g., AVX, AVX2, AVX-512), and multi-threading efficiently.

### Install

```bash
dnf update -y && dnf install -y wget tar
wget https://registrationcenter-download.intel.com/akdlm/IRC_NAS/86d6a4c1-c998-4c6b-9fff-ca004e9f7455/l_onemkl_p_2024.0.0.49673.sh
sudo bash ./l_onemkl_p_2024.0.0.49673.sh --eula accept
```


### Running

```bash
cd /opt/intel/oneapi/mkl/2024.0/share/mkl/benchmarks/linpack/
bash runme_xeon64
```


## Additional Info



## LINPACK Parameters

I originally found this [here](https://www.netlib.org/benchmark/hpl/tuning.html) and updated it with additional explanation.

**Line 1:** (unused) 
- Typically used for comments. By default, it reads:
```
HPL Linpack benchmark input file
```

**Line 2:** (unused)
- Similar to line 1, often used for additional comments. By default, it reads:
```
Innovative Computing Laboratory, University of Tennessee
```

**Line 3:** 
- Specifies where to redirect the output. By default:
```
HPL.out  output file name (if any)
```
- This indicates that the output will be written to "HPL.out" unless otherwise specified.

**Line 4:** 
- Indicates where the output should be directed. The options are:
  - `6`: Standard output
  - `7`: Standard error
  - Any other integer: Redirect to a file specified in the previous line. Default:
```
6        device out (6=stdout,7=stderr,file)
```

**Line 5:** 
- Specifies the number of problem sizes (N) to be executed. Example:
```
3        # of problems sizes (N)
```

**Line 6:** 
- Lists the actual problem sizes to run. Example:
```
3000 6000 10000    Ns
```

**Line 7:** 
- Indicates the number of block sizes to be used. Example:
```
5        # of NBs
```

**Line 8:** 
- Specifies the block sizes. Example:
```
80 100 120 140 160 NBs
```

**Line 9:** 
- Details how MPI processes are mapped onto the nodes. Recommended mapping is row-major.
- You could change this to column-major but this is use case specific. Ex: a simulation of fluid dynamics where columns represent vertical slices through a fluid medium. If the physical interactions are primarily vertical, such as in atmospheric simulations where air movements and properties change significantly with altitude but less so horizontally, then column-major mapping would ensure that processes handling adjacent vertical slices are closer together, reducing the communication time for vertically adjacent data points and potentially improving overall computational efficiency.

**Line 10:** 
- Specifies the number of process grids (P x Q) to be tested. Example:
```
2        # of process grids (P x Q)
```

**Line 11-12:** 
- Define the dimensions of each process grid (P rows x Q columns). Example:
```
1 2          Ps
6 8          Qs
```

**Line 13:** 
- Sets the threshold for residuals comparison. A typical value might be:
```
16.0         threshold
```
- The "threshold for residuals comparison" refers to the accuracy of the numerical calculations performed. Residuals are the differences between the results obtained from computational operations and the expected theoretical values. A threshold, such as 16.0, acts as a cut-off point for these residuals. If the computed residual is above this threshold, it might indicate a problem with the numerical accuracy or stability of the calculation. For instance, in solving linear equations, if the solution's accuracy is paramount, the residuals (differences between the left and right-hand sides of the equations) should ideally be small. A large residual compared to the threshold could signal inaccuracies, prompting a need to investigate the computation's precision or to adjust algorithm parameters.

**Lines 14-21:** 
- Configure various algorithmic parameters like panel factorization, recursive stopping criterion, etc. Examples from the provided text illustrate different settings for these algorithmic features.

**Lines 22-23:** 
- Define the broadcast topology used in the algorithm. Examples provided indicate using different broadcast options.

**Lines 24-25:** 
- Specify the lookahead depth used by HPL. Depth of 1 is usually recommended, but examples show how to set different depths.

**Lines 26-27:** 
- Determine the swapping algorithm and threshold. The examples indicate how to choose and configure the swapping algorithm.

**Line 28:** 
- Configures the storage form (transposed or no-transposed) for the upper triangle of the panel of columns.

**Line 29:** 
- Sets the storage form for the panel of rows U.

**Line 30:** 
- Enables or disables the equilibration phase.

**Line 31:** 
- Specifies the memory alignment for allocations done by HPL. Common values are 4, 8, or 16, influencing how memory is aligned.

## How MPI Processes Work

Helpful Presentation: https://www.uio.no/studier/emner/matnat/ifi/INF3380/v11/undervisningsmateriale/inf3380-week06.pdf

MPI (Message Passing Interface) processes are at the core of parallel computing in systems that use the MPI standard for communication.

### What are MPI Processes?

- **Independent Processes**: Each MPI process is an independent unit of computation that executes concurrently with other MPI processes. They can be thought of as separate instances of the program, often running on different cores or different nodes in a cluster.
- **Separate Memory Spaces**: Each process has its own private memory space. This means variables and data in one process are not directly accessible to another process. Any data sharing or communication must be done explicitly using MPI's communication mechanisms.

### How MPI Processes Communicate

- **Message Passing**: The fundamental concept of MPI is that processes communicate by sending and receiving messages. These messages can contain any type of data, and the communication can occur between any two processes.
- **Collective Communications**: Besides point-to-point communication, MPI provides collective communication operations (like broadcast, reduce, scatter, gather) that involve a group of processes. These operations are optimized for efficient communication patterns commonly found in parallel applications.

### Creating MPI Processes

- **MPI_Init and MPI_Finalize**: An MPI program starts with MPI_Init and ends with MPI_Finalize. Between these two calls, the MPI environment is active, and the program can utilize MPI functions.
- **Parallel Region**: The code between MPI_Init and MPI_Finalize is executed by all processes in parallel, but each process can follow different execution paths based on their [rank](#mpi-ranks) or other conditional logic.
- **Rank and Size**: Each process is assigned a unique identifier called its rank. The total number of processes is called the size. These are often used to divide work among processes or to determine the role of each process in communication patterns.

### Distribution of Work

- **Dividing the Problem**: In typical MPI applications, the large problem is divided into smaller parts, and each MPI process works on a portion of the problem. This division can be based on data (data parallelism) or tasks (task parallelism).
- **Synchronization**: Processes can synchronize their execution, for example, by using barriers (MPI_Barrier), ensuring that all processes reach a certain point of execution before continuing.

### Running MPI Programs

- **MPI Executors**: MPI programs are usually executed with a command like `mpirun` or `mpiexec`, followed by options that specify the number of processes to launch and other execution parameters.
- **Scalability**: The scalability of an MPI program depends on its ability to efficiently partition the workload among the available processes and the effectiveness of the communication between the processes.

In the context of the LINPACK benchmark, the MPI processes would each handle a portion of the LINPACK workload, collaborating by exchanging messages to solve the large linear algebra problem in parallel.

### MPI Ranks

An MPI rank is a unique identifier assigned to each process in a parallel program that uses the Message Passing Interface (MPI) for communication. MPI is a standardized and portable message-passing system designed to function on a wide variety of parallel computing architectures. In an MPI program, multiple processes can run simultaneously, potentially on different physical machines or cores within a machine.

Ranks are used for the following:

- **Identification:** The rank allows each process to be uniquely identified within an MPI communicator. A communicator is a group of MPI processes that can communicate with each other. The most common communicator used is `MPI_COMM_WORLD`, which includes all the MPI processes in a program.
- **Coordination and Communication:** By knowing its rank, a process can determine how to coordinate its actions with other processes, such as dividing data among processes for parallel computation or determining the order of operations in a parallel algorithm.
- **Scalability:** Using ranks, MPI programs can be designed to scale efficiently with the number of processes, allowing for parallel execution on systems ranging from a single computer to a large-scale supercomputer.

Ranks are typically represented as integers starting from 0. So, in a program with `N` processes, the ranks are numbered from 0 to `N-1`. This numbering is used in various MPI operations, such as sending and receiving messages, where you specify the rank of the target process.

Here's a simple example to illustrate the use of ranks in MPI:

```c
#include <mpi.h>
#include <stdio.h>

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

    printf("Hello world from rank %d out of %d processes\n", world_rank, world_size);

    MPI_Finalize();
    return 0;
}
```

In this example, each process finds out its rank within `MPI_COMM_WORLD` (with `MPI_Comm_rank`) and the total number of processes (with `MPI_Comm_size`) and prints a message including its rank and the total number of processes. When this program is run with MPI across multiple processes, each process will print its unique rank.

#### MPI Ranks as Related to LU Decomposition

LU decomposition involves breaking down a matrix $A$ into the product of a lower triangular matrix $L$ and an upper triangular matrix $U$. See [LU Decomposition](#lu-decomposition-factorization) for an explanation of LU decomposition.

Recall that given a matrix $A$, the goal is to decompose it into:

$$ A = LU $$

where $L$ is a lower triangular matrix and $U$ is an upper triangular matrix. This decomposition is used to solve $Ax = b$ for $x$ by solving two simpler systems:

1. $Ly = b$
2. $Ux = y$

When MPI is applied to matrices there are two main strategies used:

- **2D Block Decomposition:** The matrix is divided into [blocks](#how-block-size-works) and distributed among the ranks. Each rank works on its block(s) performing necessary operations for the decomposition. This method requires communication between ranks to exchange bordering row and column information during the elimination steps.
- **1D Block Decomposition:** The matrix is divided into horizontal or vertical strips. Each rank works on its strip, and operations are coordinated to ensure the matrix is correctly modified across all ranks. This can be simpler but might not balance load and communication as effectively as 2D blocking.

### MPI Arguments

### -np (Number of Processes)

- **Usage:** `-np X`
- **Description:** Specifies the total number of MPI processes to launch for the entire job. This is a global setting, affecting the total count of processes across all nodes involved in the MPI job.
- **Relation to MPI:** Each MPI process is assigned a unique rank within the MPI communicator (usually `MPI_COMM_WORLD`), starting from 0 up to `X-1` if `-np X` is used. There's a one-to-one correspondence between an MPI process and its rank; thus, `-np` directly dictates the total number of unique ranks in your MPI job.

### -ppn (Processes Per Node) aka perhost

- **Usage:** `-ppn Y`
- **Description:** Specifies the number of MPI processes to launch per node. This is used to control the distribution of the total MPI processes across the available nodes.
- **Relation to MPI:** This option does not directly influence the assignment of ranks but rather how those ranks are distributed across nodes. If you have a total of `X` MPI processes (as specified by `-np`) and you want `Y` of those processes on each node, `-ppn` helps achieve that distribution. 

### Relation to Threads

Threads are typically managed by APIs like OpenMP or the threading facilities within the programming language being used (e.g., C++11 threads). 

- **MPI Processes vs. Threads:** Each MPI process can independently execute its code path and has its memory space. Within each MPI process, you might employ threads to further parallelize computation, especially to leverage multicore processors effectively. The use of threads is completely independent of the distribution of MPI processes managed by `-np` and `-ppn`.
- **OpenMP and MPI:** For hybrid MPI/OpenMP applications, the number of threads per MPI process is usually controlled by setting environment variables like `OMP_NUM_THREADS`.

### Practical Example

Let's say you have a cluster with 4 nodes, and you intend to run a total of 8 MPI processes.

- Using `-np 8` tells MPI to start a total of 8 processes.
- If you also specify `-ppn 2`, it instructs MPI to distribute these processes so that each of the 4 nodes runs 2 processes.

In this setup, each MPI process operates independently (with its rank), and you could further parallelize each process internally using threads, e.g., via OpenMP, by setting `OMP_NUM_THREADS` appropriately for each process.

#### A Note About MPI Implementations

Intel has [its own MPI implementation](https://www.intel.com/content/www/us/en/docs/onemkl/developer-guide-windows/2023-0/overview-intel-distribution-for-linpack-benchmark.html). You can use [OpenMP with it](https://www.intel.com/content/www/us/en/developer/articles/technical/hybrid-applications-mpi-openmp.html).

## Run Against a Single Node

### Install

1. Download from [here](https://downloadmirror.intel.com/793598/l_onemklbench_p_2024.0.0_49515.tgz)
2. Download MPI from [here](https://registrationcenter-download.intel.com/akdlm/IRC_NAS/2c45ede0-623c-4c8e-9e09-bed27d70fa33/l_mpi_oneapi_p_2021.11.0.49513.sh)
Intel has prepackaged binaries for different architectures. For example, below is the file for running against Xeon:

```bash
#!/bin/sh
#===============================================================================
# Copyright 2001-2022 Intel Corporation.
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

echo "This is a SAMPLE run script for running a shared-memory version of"
echo "Intel(R) Distribution for LINPACK* Benchmark. Change it to reflect"
echo "the correct number of CPUs/threads, problem input files, etc.."
echo "*Other names and brands may be claimed as the property of others."

# Setting up affinity for better threading performance
export KMP_AFFINITY=nowarnings,compact,1,0,granularity=fine

# Use numactl for better performance on multi-socket machines.
nnodes=`numactl -H 2>&1 | awk '/available:/ {print $2}'`
cpucores=`cat /proc/cpuinfo | awk '/cpu cores/ {print $4; exit}'`

if [  $nnodes -gt 1 -a $cpucores -gt 8 ]
then
    numacmd="numactl --interleave=all"
else
    numacmd=
fi

arch=xeon64
{
  date
  $numacmd ./xlinpack_$arch lininput_$arch
  echo -n "Done: "
  date
} | tee lin_$arch.txt
```

It takes care of NUMA-alignment, selecting the amount of memory, and memory alignment all as part of the xlinpack binary. Ex: the `numactl --interleave=all` command automatically interleaves memory across all numa nodes for you.

### Running the Code

```bash
cd /home/grant/Downloads/benchmarks_2024.0/linux/share/mkl/benchmarks/linpack
./runme_xeon64
```

## Run on a Cluster w/SLURM

### Configure runme_intel64_dynamic



### Gain Access to Cluster

```bash
[grant@mlogin01 current]$ pwd
/cm/shared/docs/slurm/current
[grant@mlogin01 current]$ ls
AUTHORS  COPYING  DISCLAIMER  NEWS  README.rst  RELEASE_NOTES
[grant@mlogin01 current]$ salloc -p 74F3 -t 0:30:00 -N 1
salloc: Pending job allocation 18688
salloc: job 18688 queued and waiting for resources
salloc: job 18688 has been allocated resources
salloc: Granted job allocation 18688
salloc: Waiting for resource configuration
salloc: Nodes m1-04 are ready for job
[grant@m1-04 current]$ ls /cm/shared/docs/slurm/current/
AUTHORS  COPYING  DISCLAIMER  NEWS  README.rst  RELEASE_NOTES
```

### Running Job

```bash
#!/bin/bash
#SBATCH --job-name=linpack
#SBATCH --output=linpack_%j.out
#SBATCH --partition=8480         # Specify the partition
#SBATCH --nodes=2               # Adjust based on how many nodes you want to use
#SBATCH --ntasks-per-node=8     # Assuming you want to utilize all cores
#SBATCH --time=0:30:00          # Set the time limit; adjust as necessary
#SBATCH --exclusive              # Optional: Request exclusive access to the nodes

# Load the Intel MPI module
module load intel/mpi/2019u12

# Navigate to the directory containing the LINPACK files
cd /home/grant/benchmarks_2024.0/linux/share/mkl/benchmarks/mp_linpack

# Run the LINPACK benchmark
bash runme_intel64_dynamic
```

## Useful Commands

- **Check Module Availability**: `module avail`
- **List partitions and node availability**: `sinfo`
- **Allocate a node interactively**: `srun --partition 8480 --nodes=1 --ntasks=1 --time=01:00:00 --pty $SHELL`
- **Check the job queue**: `squeue`
- **Get Information on a Job**: `sacct --job=249580`

## Useful Links

- [How to use MPI with OpenMP or multi-threaded Intel MKL](https://researchcomputing.princeton.edu/faq/how-to-use-openmpi-with-o)
- [HPL.dat Parameters](https://www.netlib.org/benchmark/hpl/tuning.html)
- [MPI Explained PPT](https://www.uio.no/studier/emner/matnat/ifi/INF3380/v11/undervisningsmateriale/inf3380-week06.pdf)
- [Intel MKL Download](https://downloadmirror.intel.com/793598/l_onemklbench_p_2024.0.0_49515.tgz)

## TODO NOTES

- mpirun ONLY RUNS ONCE ON THE CLUSTER - SLURM basically doesn't matter
- They use a custom threading thing. Not OpenMP.
- Spawned processes is controlled by the number of Ps and Qs NOT -np. -np must match but it is not the driving factor 
- SLURM gives MPIRUN the list of hosts

## Run a Job in SLURM that Gives You Node Access

```bash
!/bin/bash
#SBATCH --time=1:00:00
#SBATCH --nodes=3
#SBATCH --exclusive
#SBATCH --job-name=my_lightweight_job
#SBATCH --ntasks-per-node=1
#SBATCH --partition=8480
#SBATCH --output=my_job_output_%j.txt
#SBATCH --error=my_job_error_%j.txt

# Run a minimal bash loop
while true; do
    echo "Timestamp: $(date)" >> /tmp/keepalive_${SLURM_JOB_ID}.txt
    sleep 300 # Sleep for 5 minutes
done
```

## How does `-pernode / -ppn` work?

When you first look at this, it is very confusing. [`mpirun`](./binary/mpirun) is launched by either by runme_intel_dynamic or directly, and `mpirun` then launches mpiexec.hydra, which then launches multiple instances of runme_intel64_prv, which then launches xhpl_intel64_dynamic. Hydra's options are defined [here](https://www.intel.com/content/www/us/en/docs/mpi-library/developer-reference-linux/2021-8/global-hydra-options.html). I_MPI_PERHOST is defined as:

### I_MPI_PERHOST

Define the default behavior for the `-perhost` option of the `mpiexec.hydra` command.

#### Syntax

`I_MPI_PERHOST=<value>`

#### Argument

| `<value>`     | Description                                     |
|---------------|-------------------------------------------------|
| `<value>`     | Define a value used for `-perhost` by default   |
| `integer > 0` | Exact value for the option                      |
| `all`         | All logical CPUs on the node                    |
| `allcores`    | All cores (physical CPUs) on the node. This is the default value. |

#### Description

Set this environment variable to define the default behavior for the `-perhost` option. Unless specified explicitly, the `-perhost` option is implied with the value set in `I_MPI_PERHOST`.

> **NOTE:** When running under a job scheduler, this environment variable is ignored by default. To control process placement with `I_MPI_PERHOST`, disable the [`I_MPI_JOB_RESPECT_PROCESS_PLACEMENT`](#I_MPI_JOB_RESPECT_PROCESS_PLACEMENT) variable.

### I_MPI_JOB_RESPECT_PROCESS_PLACEMENT

Specify whether to use the process-per-node placement provided by the job scheduler, or set explicitly.

#### Syntax

`I_MPI_JOB_RESPECT_PROCESS_PLACEMENT=<arg>`

#### Argument

| `<value>`                  | Description                                                        |
|----------------------------|--------------------------------------------------------------------|
| `<value>`                  | Binary indicator                                                   |
| `enable | yes | on | 1`    | Use the process placement provided by job scheduler. This is the default value |
| `disable | no | off | 0`   | Do not use the process placement provided by job scheduler        |

#### Description

If the variable is set, the Hydra process manager uses the process placement provided by job scheduler (default). In this case, the `-ppn` option and its equivalents are ignored. If you disable the variable, the Hydra process manager uses the process placement set with `-ppn` or its equivalents.

### Understanding What Rank and Node Mean in Output

In your output you will see things like:

```
RANK=5, NODE=5-5
RANK=3, NODE=3-3
RANK=0, NODE=0-0
RANK=1, NODE=1-1
RANK=6, NODE=6-6
RANK=2, NODE=2-2
RANK=7, NODE=7-7
RANK=4, NODE=4-4
```

But what does that mean? In Intel's scheme, this is printed by this line in [runme_intel64_prv](./binary/runme_intel64_prv):

```bash
echo RANK=${PMI_RANK}, NODE=${HPL_HOST_NODE}, HPL_DEVICE=${HPL_DEVICE}
```

Let's break down what is going on here. 

