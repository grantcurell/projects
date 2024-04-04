
## Understanding Intel's MKL Process Flow

Assuming you change nothing, Intel's MKL has a fairly complex process flow that isn't immediately obvious. Here is what it looks like visually:

TODO - ADD LINKS

+---------------------+
| runme_intel_dynamic |
+---------------------+
            |
            v
         +-------+
         | mpirun |
         +-------+
            |
            v
      +--------------+
      | mpiexec.hydra|
      +--------------+
            |
            v
   +-------------------+
   | runme_intel64_prv |
   +-------------------+
            |
            v
   +-----------------------+
   | xhpl_intel64_dynamic  |
   +-----------------------+

TODO - figure out exactly how many of each and reword the below.

When you first look at this, it is very confusing. [`mpirun`](./binary/mpirun) is launched by either by runme_intel64_dynamic or directly, and `mpirun` then launches mpiexec.hydra, which then launches multiple instances of runme_intel64_prv, which then launches xhpl_intel64_dynamic. Hydra's options are defined [here](https://www.intel.com/content/www/us/en/docs/mpi-library/developer-reference-linux/2021-8/global-hydra-options.html). I_MPI_PERHOST is defined as:

TODO - get rid of this

### [runme_intel_dynamic](./binary/runme_intel64_dynamic)

In my case I'm not running with GPUs and in this case, [runme_intel_dynamic](./binary/runme_intel64_dynamic) does not do a whole lot. It's main job is to kick off [mpirun](./binary/mpirun) with [runme_intel64_prv](./binary/runme_intel64_prv) as an argument. It does this here:

```bash
mpirun -perhost ${MPI_PER_NODE} -np ${MPI_PROC_NUM} ./runme_intel64_prv "$@" | tee -a $OUT
```

where `MPI_PER_NODE` and `MPI_PROC_NUM` are defined as:

```bash
# Set total number of MPI processes for the HPL (should be equal to PxQ).
export MPI_PROC_NUM=2

# Set the MPI per node for each node.
# MPI_PER_NODE should be equal to 1 or number of sockets on the system.
# It will be same as -perhost or -ppn paramaters in mpirun/mpiexec.
export MPI_PER_NODE=2

# Set the number of NUMA nodes per MPI. (MPI_PER_NODE * NUMA_PER_MPI)
# should be equal to number of NUMA nodes on the system.
export NUMA_PER_MPI=1
```

### [mpirun](./binary/mpirun)

The [mpirun](./binary/mpirun) bash script's job is to set up the MPI environment and then call mpiexec.hydra on a single node in the cluster. mpiexec.hydra will then deploy instances of [runme_intel64_prv](./binary/runme_intel64_prv) across the cluster.

I'll go through the highlights of [mpirun](./binary/mpirun). First it sets up a bunch of environment variables with the main one being `I_MPI_MPIRUN`. This is used internally by Intel's binaries to determine how the process was launched. 

```bash
export I_MPI_MPIRUN="mpirun"
```

In this case, we launched it with the `mpirun` bash script and this environment variable tells the binaries that. Alternatively, we could have launched by calling `mpiexec` directly. The rest of the code is for handling what happens if we are launching with a job scheduler. In our case we are not so I ignore this. If we have no job scheduler, it executes this code:

```bash
# PBS or ordinary job
else
    mpiexec.hydra "$@" <&0
    rc=$?
fi
```

which will launch `mpiexec.hydra` on the current node with whatever command line arguments were passed in from `mpirun` which by default are inhereted from `runme_intel64_dynamic` and are:

```bash
-perhost ${MPI_PER_NODE} -np ${MPI_PROC_NUM} ./runme_intel64_prv "$@" | tee -a $OUT
```

### [mpiexec.hydra](https://www.intel.com/content/www/us/en/docs/mpi-library/developer-reference-linux/2021-8/mpiexec-hydra.html)

[mpiexec.hydra](https://www.intel.com/content/www/us/en/docs/mpi-library/developer-reference-linux/2021-8/mpiexec-hydra.html) is a process manager. In our case we are using Intel's instantiation, but it is an [open source project](https://github.com/pmodels/mpich/blob/main/doc/wiki/how_to/Using_the_Hydra_Process_Manager.md). mpiexec.hydra's job is to spawn our [runme_intel64_prv](./binary/runme_intel64_prv) jobs on the cluster. This is how the command line arguments are interpreted:

**-n <number-of-processes> or -np <number-of-processes>**  
Use this option to set the number of MPI processes to run with the current argument set.

**-perhost <# of processes >, -ppn <# of processes >, or -grr <# of processes>**  
Use this option to place the specified number of consecutive MPI processes on every host in the group using round robin scheduling. See the I_MPI_PERHOST environment variable for more details.

**NOTE:** When running under a job scheduler, these options are ignored by default. To be able to control process placement with these options, disable the I_MPI_JOB_RESPECT_PROCESS_PLACEMENT variable.

TODO - maybe mention how processes work here?


## How to Setup Intel's MKL

Intel's variant of MKL has many parts