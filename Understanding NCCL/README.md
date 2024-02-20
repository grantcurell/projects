

- [Intro](#intro)
- [NVIDIA Collective Communications Library (NCCL)](#nvidia-collective-communications-library-nccl)
  - [Understanding All Reduce](#understanding-all-reduce)
  - [Why Distribute Gradient Descent](#why-distribute-gradient-descent)
  - [Distributed Gradient Descent Using Allreduce](#distributed-gradient-descent-using-allreduce)
  - [Understanding point-to-point and scatter, gather, and all-to-all](#understanding-point-to-point-and-scatter-gather-and-all-to-all)
  - [Why is NCCL faster than the traditional CUDA implementation?](#why-is-nccl-faster-than-the-traditional-cuda-implementation)
    - [NCCL Optimizations](#nccl-optimizations)
      - [Memory Optimizations](#memory-optimizations)
      - [Warp and Thread Block Optimization](#warp-and-thread-block-optimization)
      - [Exploiting Communication Capabilities](#exploiting-communication-capabilities)
      - [Synchronization Techniques](#synchronization-techniques)
      - [Computation and Communication Overlap](#computation-and-communication-overlap)
  - [Custom Algorithms for Collective Operations](#custom-algorithms-for-collective-operations)
- [Rail Fabric](#rail-fabric)
  - [Fat Tree](#fat-tree)


## Intro

This explanation for NCCL assumes the reader has some passing familiarity with how AI/ML training functions at a high level.

## NVIDIA Collective Communications Library (NCCL)

From [the docs](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/overview.html#:~:text=The%20NVIDIA%20Collective%20Communications%20Library,be%20easily%20integrated%20into%20applications.)

> The NVIDIA Collective Communications Library (NCCL, pronounced “Nickel”) is a library providing inter-GPU communication primitives that are topology-aware and can be easily integrated into applications. NCCL implements both collective communication and point-to-point send/receive primitives. It is not a full-blown parallel programming framework; rather, it is a library focused on accelerating inter-GPU communication.

To understand NCCL you have to understand at least one of its "communication primitives" which it defines as:

- AllReduce
- Broadcast
- Reduce
- AllGather
- ReduceScatter

One of the things that may not be immediately obvious is what it means for this to be a primitive. When they say primitive here what they mean is that these five algorithms are the most basic building blocks this library offers and you are meant to build other things on top of them. For example, batch gradient descent, which I will briefly describe below, leverages AllReduce under the hood. Here is some pseudo code that gives you a rough idea of what that looks like in practice:

```c
/*******************************************************
 * Initialize NCCL
 ******************************************************/
ncclComm_t comms[numberOfGPUs];
int myRank, numberOfGPUs;

// Assume a function to determine the rank (ID) and number of GPUs
getMyRankAndNumberOfGPUs(&myRank, &numberOfGPUs);

// Creating NCCL communicators
ncclCommInitRank(&comms[myRank], numberOfGPUs, ncclUniqueId, myRank);

/*******************************************************
 * Allocate Memory for Your Job
 ******************************************************/
// Example allocations on the GPU
float *localGradients;
cudaMalloc(&localGradients, sizeof(float) * gradientSize);
// Initialize your gradients here or within your computation

/*******************************************************
 * Compute whatever gradients are local to just this node
 ******************************************************/
void computeGradients(float *localGradients) {
  // Your model's forward and backward pass to fill localGradients
  // A forward pass is having your model predict the parameters
  // The backward pass is when your fix the guess based on the training data
}

/*******************************************************
 * Aggregate Gradients Across GPUs with NCCL
 * Use ncclAllReduce to aggregate gradients across all 
 * GPUs. Each GPU calls this function with its local 
 * gradients, and ncclAllReduce aggregates these 
 * gradients, distributing the result back to each GPU.
 ******************************************************/
// Assuming single precision (float) gradients
ncclAllReduce(localGradients, // Input buffer
              localGradients, // Output buffer (in-place operation)
              gradientSize,   // Number of elements
              ncclFloat,      // Data type
              ncclSum,        // Operation (sum of gradients)
              comms[myRank],  // NCCL communicator
              0);             // CUDA stream (0 for default stream)

/*******************************************************
 * Update Model Parameters Locally
 ******************************************************/
void updateModelParameters(float *localGradients) {
  // Update your model parameters using the aggregated gradients
}
```

### Understanding All Reduce

I decided to use gradient descent as the example here since that shows up in a lot of AI problems.

The purpose of Gradient Descent is to optimize some loss function. Specifically, we want to find the model parameters (weights) $w$ that minimize the loss function $L(w)$.

Given a dataset with $N$ samples, the update rule for the model's weights in gradient descent is given by:

$$
w_{\text{new}} = w_{\text{old}} - \eta \nabla L(w_{\text{old}})
$$

where:
- $w_{\text{old}}$ are the model weights before the update,
- $\eta$ is the learning rate, a small positive scalar determining the step size,
- $\nabla L(w_{\text{old}})$ is the gradient of the loss function with respect to the weights $w$.

What's important to understand here is that you have $N$ gradients that have to be computed. The details of gradient descent aren't particularly important here but I talk about how it works in [LLMs Explained in the section on loss functions](../LLMs%20Explained/README.md#loss-function-and-back-propagation). The high level is that during training, at the very end of the algorithm after you have estimated the model's parameters, you need a way to move those model parameters towards being more correct. Gradient descent is how that gets done. You take what your model guessed and what the training data says is correct and compute the difference and then use that to update the parameters. In most cases you use what is called batch gradient descent where instead of individually updating each parameter based on the delta between what your model guessed and correct, you compute all the deltas, then you average them into a single number, and then you apply that to every parameter. The reason you do this is that mathematically it works out that just using the average tends to better highlight the correct signal while ignoring the noise.

We express this mathematically as: $\nabla L(w)$ with the equation below. It is just a fancy way of saying calculate the average gradient across all samples:

$$
\nabla L(w) = \frac{1}{N} \sum_{i=1}^{N} \nabla l_i(w)
$$

where $l_i(w)$ is the loss for the $i$-th sample (parameter).

### Why Distribute Gradient Descent

For very large datasets (i.e., when $N$ is very large), computing $\nabla L(w)$ is computationally expensive and time-consuming because it involves processing every single sample in the dataset. Distributing this computation across multiple nodes allows for parallel processing, significantly speeding up the computation.

### Distributed Gradient Descent Using Allreduce

Assume we have $M$ nodes, and the dataset is evenly distributed among these nodes. Each node $m$ has a subset of the data, containing $N_m$ samples, such that $\sum_{m=1}^{M} N_m = N$. In plain English, the samples are evenly distributed across all the nodes.

1. **Local Gradient Computation**: Each node computes the gradient based on its subset of the data:
   1. The equation given is simply saying, "For each piece of data I (the node) have, I calculate how wrong the model's predictions are (that's the gradient of the loss for each sample, $\nabla l_i(w)$), and then I average these to get an overall direction and magnitude for how to adjust the model's parameters based on my data."

$$
\nabla L_m(w) = \frac{1}{N_m} \sum_{i=1}^{N_m} \nabla l_i(w)
$$

2. **Allreduce Operation**: The local gradients $\nabla L_m(w)$ from each node are aggregated across all nodes using the Allreduce algorithm to compute the average gradient:
   1. This is saying, "Add up all the average adjustments suggested by each node (the sum of $\nabla L_m(w)$) and then divide by the total number of nodes to get an average adjustment that takes into account the insights from the whole dataset." The note about the sum and division by $N$ is just a technical detail to ensure that what we're working with is indeed an average over all samples in the dataset.

$$
\nabla L(w) = \frac{1}{M} \sum_{m=1}^{M} \nabla L_m(w)
$$

Note: The actual operation performed by Allreduce is a sum, so each node first computes the sum of its gradients and then divides by $N$ (total number of samples) after the aggregation to get the average.

3. **Model Update**: Each node updates its model weights using the aggregated gradient:
   1. This step says, "Take the model's current parameters (the knowledge it has now), and adjust them by subtracting a small, scaled version of the agreed-upon adjustments (the average gradient, $\nabla L(w)$, scaled by the learning rate, $\eta$." This subtraction is how the model learns from the data, improving its predictions by reducing the errors highlighted by the combined insights from all nodes.

$$
w_{\text{new}} = w_{\text{old}} - \eta \nabla L(w)
$$

### Understanding point-to-point and scatter, gather, and all-to-all

The docs say:

> Additionally, it allows for point-to-point send/receive communication which allows for scatter, gather, or all-to-all operations.

- **point-to-point**: This is GPU on one node to GPU on another node
- **Scatter**: This operation takes data from one source GPU and distributes it among multiple destination GPUs, with each destination receiving a unique portion of the data. 
- **Gather**: The opposite of scatter. Here, data from multiple source GPUs is collected and combined into a single destination GPU.
- **All-to-All**: In this operation, every GPU sends data to every other GPU, with potentially each exchange involving different data.

### Why is NCCL faster than the traditional CUDA implementation?

[On the docs page](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/overview.html#:~:text=The%20NVIDIA%20Collective%20Communications%20Library,be%20easily%20integrated%20into%20applications.) the below paragraph casually mentions why NCCL is faster but there is a lot to unpack there.

> Tight synchronization between communicating processors is a key aspect of collective communication. CUDA based collectives would traditionally be realized through a combination of CUDA memory copy operations and CUDA kernels for local reductions. NCCL, on the other hand, implements each collective in a single kernel handling both communication and computation operations. This allows for fast synchronization and minimizes the resources needed to reach peak bandwidth.

What do they mean by:

> CUDA based collectives would traditionally be realized through a combination of CUDA memory copy operations and CUDA kernels for local reductions.

What they're talking about here is that previously if you wanted to do something like sum values across GPUs or any other collective operation, you would have to run a bunch of CUDA commands to copy data in and out of GPU and application memory which is slow. We don't want to do that. A CUDA kernel here is just a fancy way to say a block of code executed on the GPU.

NCCL simplifies this process by implementing collective operations within a single kernel per operation. This means that for any collective task (e.g., aggregating data across GPUs), NCCL uses one piece of code that runs on the GPUs, handling both the movement of data between GPUs and any necessary calculations on that data. No more copying and then executing, it's done all in one go.

Here is what our AllReduce example might look like between the two:

- **Traditional Approach**
    1. **Local Reduction**: Each GPU performs a local reduction operation on its data subset. This is one or more kernel launch(s).
    2. **Communication**: Data is communicated between GPUs, potentially requiring additional kernel launches for memory copying, or using CUDA's peer-to-peer communication capabilities.
    3. **Final Reduction and Distribution**: The results from different GPUs are combined (reduced) and then distributed back. This might require further kernel launches for the reduction and for distributing the data.

- **NCCL's Single Kernel Approach**
    1. **Integrated Computation and Communication**: The kernel handles both the local computation (ex, reduction) and the necessary communication between GPUs to share and aggregate data.
    2. **Optimized for GPU Architecture**: These kernels are designed to take advantage of the GPU's architecture, such as its memory hierarchy and communication capabilities, to perform these operations as efficiently as possible.

#### NCCL Optimizations

##### Memory Optimizations

GPUs have a complex memory hierarchy, including global memory, shared memory, constant memory, and registers, each with different scopes, latencies, and bandwidths. NCCL is written to optimize how memory accesses occur against these.

- **Global Memory**: The largest and slowest form of memory accessible by all threads. Optimizations may involve minimizing global memory accesses and maximizing coalesced accesses where possible to improve bandwidth utilization.
- **Shared Memory**: A faster, but limited pool of memory that is shared among threads in the same block. NCCL kernels can use shared memory to efficiently share data between threads, reducing the need for slower global memory accesses.
- **Registers**: The fastest form of memory available to threads. Efficient use of registers can significantly speed up computations but requires careful management to avoid register spilling, where excess data spills over into slower global memory.
- **Constant Memory**: Cached and optimized for broadcast access, constant memory is used for data that does not change and is accessed by all threads.

##### Warp and Thread Block Optimization

- **Warp-Level Primitives**: Modern GPUs have warp-level primitives (e.g., warp shuffle functions) that allow threads within the same warp (a group of 32 threads) to share data without using shared or global memory. NCCL kernels can use these for efficient intra-warp communication.
- **Thread Block Configuration**: Choosing the optimal size and configuration of thread blocks (groups of threads that execute the same kernel and can share data through shared memory) is crucial for maximizing the occupancy of the GPU and ensuring that as many threads as possible are running concurrently.

##### Exploiting Communication Capabilities

- **NVLink and PCIe**: NCCL leverages NVLink
- **GPUDirect RDMA**: For inter-node communication (between servers), NCCL leverages GPUDirect RDMA to allow direct memory access between GPU memory and the network, bypassing the CPU and reducing latency and CPU overhead.

##### Synchronization Techniques

- **Efficient Synchronization**: Kernels must often synchronize between different stages of computation, especially in collective operations where data from multiple threads or thread blocks needs to be combined. NCCL kernels are optimized to use efficient synchronization techniques to minimize waiting times between threads and thread blocks.

##### Computation and Communication Overlap

- **Overlap**: Where possible, NCCL kernels are designed to overlap computation with communication, such that while data is being transferred over the network or between GPUs, computation on available data can proceed concurrently. This requires careful scheduling and partitioning of tasks within the kernel.

### Custom Algorithms for Collective Operations

For each operation Nvidia has written in optimizations for specific GPU architectures.

## Rail Fabric

When I first started reading I was a bit confused as to what a rail fabric is. On investigation, I found that this is just a high level term. "Rail Fabric" doesn't directly correspond to a specific technical standard or component but is just a metaphorical term for HPC networking interconnect. Usually with some implication of something like RDMA.

### Fat Tree

This is the same as a folded 5 stage CLOS. See [Fat-Trees as special case of Clos Network](https://packetpushers.net/blog/demystifying-dcn-topologies-clos-fat-trees-part2/)