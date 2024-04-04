
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

There are a few things going on with `mpirun -perhost ${MPI_PER_NODE} -np ${MPI_PROC_NUM} ./runme_intel64_prv "$@" | tee -a $OUT` that are not at all obvious at first. As I mentioned earlier, first this leads to `mpirun` executing, but none of the arguments are actually destined for `mpirun` What really happens is the arguments `-perhost ${MPI_PER_NODE} -np ${MPI_PROC_NUM}` are fed into [mpiexec.hydra](#mpiexechydra) and then the `$@` part of `./runme_intel64_prv "$@"` is ultimately destined for `xhpl_intel64_dynamic` which accepts the [Ease-of-use Command-line Parameters](https://www.intel.com/content/www/us/en/docs/onemkl/developer-guide-linux/2023-0/ease-of-use-command-line-parameters.html). The ease of use command line parameters are meant to replace `HPL.dat`. So instead of just running `runme_intel64_dynamic` you can do:

```bash
./runme_intel64_dynamic -m <memory size in Mbytes> -b <block size> -p <grid row dimn> -q <grid column dimn>
```

or

```bash
./runme_intel64_dynamic -n 10000 -p 1 -q 3
```

where

- **-n <size of the matrix>**: Determines the size of the problem matrix to be solved
- **-m <memory size in Mbytes>**: If you're familiar with `HPL.dat` this option may confuse you because it isn't present. What this does is allow you to control the size of the problem matrix by specifying the total amount of memory dedicated to matrix storage across all nodes instead of specifying `-n`. When you set `-m` to 50000 Mbytes, you're instructing the application to use matrices that, when combined, fit within 50 GB of memory for their storage. The block size (`-b`) parameter, set to 256 in the example, defines the size of the sub-matrix or "block" used by the HPL algorithm during matrix factorization. TODO - add reference.
- **-b <block size>**: Specifies the block size used by the HPL algorithm
- **-p <grid row dimension>**: Sets the rows dimension of the process grid
- **-q <grid column dimension>**: Sets the columns dimension of the process grid

Finally, we are missing one last thing that is completely absent in the documentation or comments. If you are not running under a job manager you have to specify the nodes for `mpiexec.hydra` using one of the two following options:

**-hostfile <hostfile> or -f <hostfile>**  
Use this option to specify host names on which to run the application. If a host name is repeated, this name is used only once.

See also the I_MPI_HYDRA_HOST_FILE environment variable for more details.

**NOTE:** Use the following options to change the process placement on the cluster nodes:  
Use the -perhost, -ppn, and -grr options to place consecutive MPI processes on every host using the round robin scheduling.

Use the -rr option to place consecutive MPI processes on different hosts using the round robin scheduling.

**-machinefile <machine file> or -machine <machine file>**  
Use this option to control process placement through a machine file. To define the total number of processes to start, use the -n option. For example:

```bash
$ cat ./machinefile
node0:2
node1:2
node0:1
```

The `I_MPI_HYDRA_HOST_FILE` is defined below.

**I_MPI_HYDRA_HOST_FILE**  
Set the host file to run the application.

**Syntax**  
`I_MPI_HYDRA_HOST_FILE=<arg>`

**Argument**  
- `<arg>`: String parameter  
- `<hostsfile>`: The full or relative path to the host file  

**Description**  
Set this environment variable to specify the hosts file.

So basically, it's just a list of hostnames one per line. TODO - CONFIRM

### [mpirun](./binary/mpirun)

TODO - pretty sure we need a hosts file

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

[mpiexec.hydra](https://www.intel.com/content/www/us/en/docs/mpi-library/developer-reference-linux/2021-8/mpiexec-hydra.html) is a process manager. In our case we are using Intel's instantiation, but it is an [open source project](https://github.com/pmodels/mpich/blob/main/doc/wiki/how_to/Using_the_Hydra_Process_Manager.md). mpiexec.hydra's job is to spawn our [runme_intel64_prv](./binary/runme_intel64_prv) jobs on the cluster. `-perhost ${MPI_PER_NODE} -np ${MPI_PROC_NUM}` plus the hostfile or machinefile I mentioned in [runme_intel64_dynamic](#runme_intel_dynamic) are what is interpreted by `mpiexec.hydra`. This is how the command line arguments are interpreted:

**-n <number-of-processes> or -np <number-of-processes>**  
Use this option to set the number of MPI processes to run with the current argument set.

**-perhost <# of processes >, -ppn <# of processes >, or -grr <# of processes>**  
Use this option to place the specified number of consecutive MPI processes on every host in the group using round robin scheduling. See the I_MPI_PERHOST environment variable for more details.

**NOTE:** When running under a job scheduler, these options are ignored by default. To be able to control process placement with these options, disable the I_MPI_JOB_RESPECT_PROCESS_PLACEMENT variable.

TODO - maybe mention how processes work here?

`I_MPI_PERHOST` is defined as

**I_MPI_PERHOST**

Define the default behavior for the `-perhost` option of the `mpiexec.hydra` command.

**Syntax**

`I_MPI_PERHOST=<value>`

**Argument**

| `<value>`     | Description                                     |
|---------------|-------------------------------------------------|
| `<value>`     | Define a value used for `-perhost` by default   |
| `integer > 0` | Exact value for the option                      |
| `all`         | All logical CPUs on the node                    |
| `allcores`    | All cores (physical CPUs) on the node. This is the default value. |

**Description**

Set this environment variable to define the default behavior for the `-perhost` option. Unless specified explicitly, the `-perhost` option is implied with the value set in `I_MPI_PERHOST`.

> **NOTE:** When running under a job scheduler, this environment variable is ignored by default. To control process placement with `I_MPI_PERHOST`, disable the `I_MPI_JOB_RESPECT_PROCESS_PLACEMENT` variable.

### [runme_intel64_prv](./binary/runme_intel64_prv)

### xhpl_intel64_dynamic

TODO - add link

## How to Setup Intel's MKL

Intel's variant of MKL has many parts