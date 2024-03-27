
# Understand and Run LINPACK

- [Understand and Run LINPACK](#understand-and-run-linpack)
  - [Setup](#setup)
  - [LU Decomposition (Factorization)](#lu-decomposition-factorization)
    - [Why LU Decomposition](#why-lu-decomposition)
      - [Solving $Ax=b$ Through Matrix Inversion](#solving-axb-through-matrix-inversion)
      - [Example of Using Matrix Inversion](#example-of-using-matrix-inversion)
      - [Issues with Direct Inversion:](#issues-with-direct-inversion)
      - [Using LU Decomposition for Matrix Inversion](#using-lu-decomposition-for-matrix-inversion)
      - [Example of Using LU Decomposition for Matrix Inversion](#example-of-using-lu-decomposition-for-matrix-inversion)
      - [Advantages of LU Decomposition:](#advantages-of-lu-decomposition)
  - [Performance Measurement - Calculating FLOPS](#performance-measurement---calculating-flops)
  - [Validation](#validation)
  - [Running Intel Math Kernel Library (MKL) LINPACK Benchmark](#running-intel-math-kernel-library-mkl-linpack-benchmark)
    - [Install](#install)
    - [Configuring Parameters](#configuring-parameters)
      - [1. Problem Size (N)](#1-problem-size-n)
    - [2. Block Size (NB)](#2-block-size-nb)
    - [3. Process Grid (P x Q)](#3-process-grid-p-x-q)
    - [Running](#running)
    - [Interpreting Results](#interpreting-results)
  - [Additional Info](#additional-info)
    - [How Block Size Works](#how-block-size-works)
    - [What is Numerical Stability](#what-is-numerical-stability)
    - [Right Looking LU Factorization](#right-looking-lu-factorization)
    - [Row Partial Pivoting](#row-partial-pivoting)
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
    - [Gain Access to Cluster](#gain-access-to-cluster)
    - [Running Job](#running-job)
  - [Useful Commands](#useful-commands)
  - [Useful Links](#useful-links)


The LINPACK Benchmarkfocuses on solving a dense system of linear equations. The core of the LINPACK Benchmark involves measuring the performance of a system when solving the equation $Ax = b$, where $A$ is a dense $n \times n$ matrix, $x$ is a vector of unknowns, and $b$ is a vector of knowns. The benchmark assesses the system's floating-point computation capabilities, primarily through the execution speed of Double Precision General Matrix Multiply (DGEMM) operations and the LU decomposition of the matrix $A$.

The following is a description of what it does.

## Setup

The benchmark will initialize a dense $n\times n$ matrix $A$ and a vector $b$ with specific values that ensure the solution will converge and is known in advance for verification purposes.

## LU Decomposition (Factorization)

- The benchmark performs an LU decomposition of matrix $A$, which is the process of factoring $A$ into the product of a lower triangular matrix $L$ and an upper triangular matrix $U$, such that $A = LU$. This decomposition includes partial pivoting, where rows of the matrix are swapped to enhance numerical stability.

### Why LU Decomposition

We know we are benchmarking, but why LU decomposition specifically? To understand this, you need to understand how we normally solve the equation $Ax=B$.

#### Solving $Ax=b$ Through Matrix Inversion

The direct inversion of a matrix $A$ to find $A^{-1}$ typically involves the use of the adjugate matrix and the determinant:

$$
A^{-1} = \frac{1}{\text{det}(A)} \text{adj}(A)
$$

where $\text{adj}(A)$ is the adjugate (or adjoint) of $A$, and det$(A)$ is the determinant of $A$.

1. **Calculate the determinant** of $A$. If det$(A) = 0$, $A$ is not invertible.
   1. If this value is zero, it means the machine’s design doesn’t allow for reversal, indicating the matrix can't be inverted.
2. **Find the matrix of cofactors** for $A$.
   1. Each cofactor represents the effect of removing the element's row and column from the matrix. In essence, the cofactor reflects how the exclusion of a particular element (and its corresponding row and column) impacts the overall determinant of the matrix.
3. **Transpose the matrix of cofactors** to get the adjugate matrix.
   1. Once you have the cofactors, you transpose them, meaning you flip the grid along its diagonal. This doesn’t change the individual contributions but reorganizes the layout, ensuring the machine's operation can be reversed correctly. This rearrangement produces what’s called the adjugate matrix.
4. **Divide each element** of the adjugate matrix by det$(A)$ to get $A^{-1}$.
   1. The final step involves adjusting the adjugate matrix by the machine's overall scaling factor (the determinant). You scale each component's contribution down or up to ensure that when you apply this reversed operation, it perfectly undoes whatever the original machine did. The result is your inverse matrix, \(A^{-1}\), which can reverse the effects of the original matrix \(A\).

#### Example of Using Matrix Inversion

Below is an example of this in action.

$$
A = \begin{bmatrix} 4 & 7 \\
2 & 6 \end{bmatrix}
$$

**Step 1: Calculate the determinant of $A$**

The determinant of a 2x2 matrix:

$\begin{bmatrix} a & b \\ 
c & d 
\end{bmatrix}$ 

is calculated as $ad - bc$. For our matrix $A$:

$$
\text{det}(A) = (4)(6) - (7)(2) = 24 - 14 = 10
$$

Since $\text{det}(A) \neq 0$, the matrix $A$ is invertible.

**Step 2: Find the matrix of cofactors for $A$**

The cofactor matrix is found by calculating the cofactor for each element of $A$. For a 2x2 matrix, this involves swapping the elements on the main diagonal, changing the signs of the off-diagonal elements, and then taking the determinant of each 1x1 matrix (which is the element itself in this case):

- Cofactor of $4$ (top-left) is $6$ (bottom-right element).
- Cofactor of $7$ (top-right) is $-2$ (bottom-left element, sign changed).
- Cofactor of $2$ (bottom-left) is $-7$ (top-right element, sign changed).
- Cofactor of $6$ (bottom-right) is $4$ (top-left element).

So, the cofactor matrix is:

$$
\text{Cof}(A) = \begin{bmatrix} 6 & -2 \\ 
-7 & 4 \end{bmatrix}
$$

**Step 3: Transpose the matrix of cofactors to get the adjugate matrix**

The adjugate of $A$ is the transpose of the cofactor matrix. For a 2x2 matrix, this simply means swapping the non-diagonal elements:

$$
\text{adj}(A) = \text{Cof}(A)^T = \begin{bmatrix} 6 & -7 \
 -2 & 4 \end{bmatrix}
$$

**Step 4: Divide each element of the adjugate matrix by $\text{det}(A)$ to get $A^{-1}$**

Finally, we divide each element of the adjugate matrix by the determinant of $A$ to find the inverse:

$$
A^{-1} = \frac{1}{\text{det}(A)} \text{adj}(A) = \frac{1}{10} \begin{bmatrix} 6 & -7 \\
 -2 & 4 \end{bmatrix} = \begin{bmatrix} 0.6 & -0.7 \\
 -0.2 & 0.4 \end{bmatrix}
$$

So, the inverse of matrix $A$ is:

$$
A^{-1} = \begin{bmatrix} 0.6 & -0.7 \\
 -0.2 & 0.4 \end{bmatrix}
$$

#### Issues with Direct Inversion:

- **Computational Complexity:** This method involves calculating determinants and cofactors for each element of the matrix, leading to a computational complexity of $O(n^3)$ to $O(n^4)$ for an $n \times n$ matrix, which is highly inefficient for large matrices.
- **Numerical Stability:** The process can be numerically unstable, especially if det$(A)$ is very close to zero, leading to large errors in $A^{-1}$.

#### Using LU Decomposition for Matrix Inversion

LU decomposition expresses matrix $A$ as the product of a lower triangular matrix $L$ and an upper triangular matrix $U$. This decomposition can be leveraged to compute $A^{-1}$ more efficiently and stably.

1. **Decompose $A$ into $L$ and $U$:** $A = LU$.
2. **Solve $LY = I$ for $Y$:** Use forward substitution, where $I$ is the identity matrix.
3. **Solve $UX = Y$ for $X$:** Use backward substitution, where $X$ eventually represents $A^{-1}$.

#### Example of Using LU Decomposition for Matrix Inversion

$$
A = \begin{bmatrix} 4 & 7 \\
 2 & 6 \end{bmatrix}
$$

**Decompose $A$ into $L$ and $U$**

For LU decomposition, we want to break down $A$ into a lower triangular matrix $L$ and an upper triangular matrix $U$.

1. Start with $U$ as $A$ and $L$ as an identity matrix, which will be modified to represent the elimination steps.
2. To eliminate the $2$ in the second row of $U$, subtract $\frac{1}{2}$ times the first row from the second row. The multiplier $\frac{1}{2}$ is stored in $L$.

Now we have:

$$
L = \begin{bmatrix} 1 & 0 \\
 \frac{1}{2} & 1 \end{bmatrix}, \quad U = \begin{bmatrix} 4 & 7 \\
 0 & \frac{5}{2} \end{bmatrix}
$$

**Step 2: Solve $LY = I$ for $Y$**

The goal here is to find a matrix $Y$ such that when $L$ is multiplied by $Y$, the result is the identity matrix $I$. The matrix $L$ is a lower triangular matrix, and $I$ is the $2 \times 2$ identity matrix.

Since $L$ is lower triangular with 1s on the diagonal, we can solve for $Y$ using forward substitution. However, in this context, since we are eventually seeking $A^{-1}$, we don't need to explicitly solve for $Y$ because it will be the identity matrix.

**Step 3: Solve $UX = Y$ for $X$**

Finally, we need to solve $UX = I$ (since $Y = I$ in this context) for $X$, where $X$ represents $A^{-1}$. This is done using backward substitution.

We compute $X$ by directly using backward substitution on the equation $UX = I$, where $I$ is the identity matrix. This process will yield $X$, which is the inverse of $A$.

After solving $UX = I$, we get:

$$
A^{-1} = \begin{bmatrix} 0.6 & -0.7 \\
 -0.2 & 0.4 \end{bmatrix}
$$

You can see the intermediate steps in this program:

```python
import numpy as np
import scipy.linalg

# Define the matrix A
A = np.array([[4, 7], [2, 6]])

# Perform LU decomposition with pivoting
P, L, U = scipy.linalg.lu(A)

# Display the matrices P, L, and U
print("P (Permutation Matrix):")
print(P)
print("\nL (Lower Triangular Matrix):")
print(L)
print("\nU (Upper Triangular Matrix):")
print(U)

# Step 1: Solve LY = P for Y using forward substitution
Y = scipy.linalg.solve_triangular(L, P, lower=True)

# Display the intermediate matrix Y
print("\nY (Intermediate Matrix):")
print(Y)

# Step 2: Solve UX = Y for X using backward substitution, where X is A^(-1)
X = scipy.linalg.solve_triangular(U, Y, lower=False)

# Display the computed inverse of A
print("\nX (Computed Inverse of A):")
print(X)

# Verify by direct inversion
A_inv = np.linalg.inv(A)
print("\nDirectly Calculated Inverse of A (for verification):")
print(A_inv)
```

#### Advantages of LU Decomposition:

- **Computational Efficiency:** LU decomposition reduces the problem to solving triangular matrices, which is computationally cheaper than the direct method. The overall complexity remains $O(n^3)$ but with a significantly lower constant factor.
- **Reusability:** Once $A$ has been decomposed into $L$ and $U$, these matrices can be reused to solve multiple systems or invert other matrices derived from $A$, without the need to perform decomposition again.
- **Numerical Stability:** Partial pivoting (adjusting $L$ and $U$ during decomposition to maintain stability) ensures that LU decomposition is more numerically stable than direct inversion, especially for matrices that are close to singular.

## Performance Measurement - Calculating FLOPS

The benchmark calculates the total number of floating-point operations required to perform the LU decomposition and solves the system. It then measures the time taken to execute these operations, using this to calculate the system's performance in floating-point operations per second (FLOPS). The key metric is the maximum achieved FLOPS rate during the test.

## Validation

After computing the solution vector $x$, the benchmark verifies the accuracy of the solution by comparing it against the expected result, ensuring that the computation has been performed correctly.

## Running Intel Math Kernel Library (MKL) LINPACK Benchmark

Intel's version of LINPACK is unsurprisingly highly tuned for Intel. It provides routines that are specifically tuned to leverage the capabilities of Intel processors, such as utilizing vectorization, advanced instruction sets (e.g., AVX, AVX2, AVX-512), and multi-threading efficiently.

### Install

```bash
dnf update -y && dnf install -y wget tar
wget https://registrationcenter-download.intel.com/akdlm/IRC_NAS/86d6a4c1-c998-4c6b-9fff-ca004e9f7455/l_onemkl_p_2024.0.0.49673.sh
sudo bash ./l_onemkl_p_2024.0.0.49673.sh --eula accept
```

### Configuring Parameters

#### 1. Problem Size (N)

This is the size of the problem that LINPACK will solve. If you set this to 10,000, then LINPACK will solve for a 10,000x10,000 matrix. This subsequently controls the amount of memory the benchmark will use. For the benchmark you want the memory to be ~80%.

$$
N = \sqrt{\frac{{.8\times\text{Memory in Gigabytes}}}{8 \times \text{sizeof(double)}}}
$$

Since each double-precision number uses 8 bytes, we divide the allocated memory in bytes by 8.

### 2. Block Size (NB)

I explain exactly how blocks work [in this section](#how-block-size-works). The high level is that instead of trying to do the matrix multiplication outright, we chunk it up into blocks and the size of these blocks is determined by the block size. Ex: If you were solving a 4x4 matrix and you selected a block size of 2 it would chunk that multiplication into multiplications with 2x2 matrices.

Common values range from 128 to 256. The optimal value often depends on the specifics of your system's memory hierarchy. Many people simply start with 256. Some reasons why this matters:

- **Cache Efficiency:** Smaller matrices fit to CPU cache speeding things up
- **Data Locality:** By working on small contiguous blocks of the matrices at a time, the algorithm improves data locality, leading to better performance.
- **Parallelization:** Each block multiplication can potentially be performed in parallel, offering opportunities for performance optimization in multicore or multiprocessor environments.

### 3. Process Grid (P x Q)

At the highest level, this controls the distribution of processes over a two-dimensional grid. P and Q are the dimensions of the grid.

Generally, what you want is:

$$
P \times Q = \text{Total number of cores or threads}
$$

where we choose $P$ and $Q$ such that their product is equal to the number of physical cores or logical threads (if hyper-threading is enabled). The ideal grid minimizes the difference between $P$ and $Q$. For a system with 12 cores, you might use 3x4 or 2x6. You will probably want to explore different values to see which is best.

Extending [the example for block size](#how-block-size-works), this is effectively assigning a core to each subblock we create. Ideally they match perfectly, but you really just want to get it as close as you can.

### Running

```bash
cd /opt/intel/oneapi/mkl/2024.0/share/mkl/benchmarks/linpack/
bash runme_xeon64
```

### Interpreting Results

```
This is a SAMPLE run script for running a shared-memory version of
Intel(R) Distribution for LINPACK* Benchmark. Change it to reflect
the correct number of CPUs/threads, problem input files, etc..
*Other names and brands may be claimed as the property of others.
runme_xeon64: line 28: [: too many arguments
Wed Mar  6 01:17:25 PM EST 2024
Sample data file lininput_xeon64.

Current date/time: Wed Mar  6 13:17:25 2024

CPU frequency:    2.692 GHz
Number of CPUs: 2
Number of cores: 24
Number of threads: 24

Parameters are set to:

Number of tests: 15
Number of equations to solve (problem size) : 1000  2000  5000  10000 15000 18000 20000 22000 25000 26000 27000 30000 35000 40000 45000
Leading dimension of array                  : 1000  2000  5008  10000 15000 18008 20016 22008 25000 26000 27000 30000 35000 40000 45000
Number of trials to run                     : 8     6     4     4     3     3     3     3     3     3     2     1     1     1     1
Data alignment value (in Kbytes)            : 4     4     4     4     4     4     4     4     4     4     4     1     1     1     1

Maximum memory requested that can be used=16200901024, at the size=45000

=================== Timing linear equation system solver ===================

Size   LDA    Align. Time(s)    GFlops   Residual     Residual(norm) Check
1000   1000   4      0.013      51.4481  1.319833e-12 4.019661e-02   pass
1000   1000   4      0.006      115.4058 1.319833e-12 4.019661e-02   pass
1000   1000   4      0.006      114.9894 1.319833e-12 4.019661e-02   pass
1000   1000   4      0.006      113.9290 1.319833e-12 4.019661e-02   pass
1000   1000   4      0.006      117.8895 1.319833e-12 4.019661e-02   pass
1000   1000   4      0.006      119.3595 1.319833e-12 4.019661e-02   pass
1000   1000   4      0.006      116.9847 1.319833e-12 4.019661e-02   pass
1000   1000   4      0.006      118.7078 1.319833e-12 4.019661e-02   pass
2000   2000   4      0.023      231.5382 5.176637e-12 4.065060e-02   pass
2000   2000   4      0.024      225.9432 5.176637e-12 4.065060e-02   pass
2000   2000   4      0.022      239.2326 5.176637e-12 4.065060e-02   pass
2000   2000   4      0.025      214.1079 5.176637e-12 4.065060e-02   pass
2000   2000   4      0.022      239.7369 5.176637e-12 4.065060e-02   pass
2000   2000   4      0.023      228.6342 5.176637e-12 4.065060e-02   pass
5000   5008   4      0.230      362.3217 2.344738e-11 3.096182e-02   pass
5000   5008   4      0.225      371.2111 2.344738e-11 3.096182e-02   pass
5000   5008   4      0.226      369.3271 2.344738e-11 3.096182e-02   pass
5000   5008   4      0.226      369.2534 2.344738e-11 3.096182e-02   pass
10000  10000  4      1.421      469.3290 8.459977e-11 2.865107e-02   pass
10000  10000  4      1.398      476.9397 8.459977e-11 2.865107e-02   pass
10000  10000  4      1.385      481.4629 8.459977e-11 2.865107e-02   pass
10000  10000  4      1.383      482.1042 8.459977e-11 2.865107e-02   pass
15000  15000  4      4.469      503.5350 2.237140e-10 3.392439e-02   pass
15000  15000  4      4.462      504.3754 2.237140e-10 3.392439e-02   pass
15000  15000  4      4.459      504.7193 2.237140e-10 3.392439e-02   pass
18000  18008  4      7.425      523.7450 3.461987e-10 3.673234e-02   pass
18000  18008  4      7.262      535.4732 3.461987e-10 3.673234e-02   pass
18000  18008  4      7.238      537.2687 3.461987e-10 3.673234e-02   pass
20000  20016  4      10.235     521.1456 3.549664e-10 3.036127e-02   pass
20000  20016  4      10.230     521.4355 3.549664e-10 3.036127e-02   pass
20000  20016  4      10.089     528.7277 3.549664e-10 3.036127e-02   pass
22000  22008  4      13.360     531.4139 4.328670e-10 3.065988e-02   pass
22000  22008  4      13.327     532.7448 4.328670e-10 3.065988e-02   pass
22000  22008  4      13.300     533.8255 4.328670e-10 3.065988e-02   pass
25000  25000  4      19.541     533.1316 5.450296e-10 3.015733e-02   pass
25000  25000  4      19.242     541.4267 5.450296e-10 3.015733e-02   pass
25000  25000  4      19.187     542.9651 5.450296e-10 3.015733e-02   pass
26000  26000  4      21.612     542.2365 6.520824e-10 3.323271e-02   pass
26000  26000  4      21.666     540.8737 6.520824e-10 3.323271e-02   pass
26000  26000  4      21.641     541.5003 6.520824e-10 3.323271e-02   pass
27000  27000  4      24.343     539.1040 6.041370e-10 2.857495e-02   pass
27000  27000  4      24.304     539.9609 6.041370e-10 2.857495e-02   pass
30000  30000  1      33.634     535.2317 9.424864e-10 3.610605e-02   pass
35000  35000  1      53.551     533.8045 1.064996e-09 3.020948e-02   pass
40000  40000  1      79.507     536.6813 1.523135e-09 3.289340e-02   pass
45000  45000  1      110.173    551.4434 2.085267e-09 3.591039e-02   pass

Performance Summary (GFlops)

Size   LDA    Align.  Average  Maximal
1000   1000   4       108.5892 119.3595
2000   2000   4       229.8655 239.7369
5000   5008   4       368.0283 371.2111
10000  10000  4       477.4589 482.1042
15000  15000  4       504.2099 504.7193
18000  18008  4       532.1623 537.2687
20000  20016  4       523.7696 528.7277
22000  22008  4       532.6614 533.8255
25000  25000  4       539.1745 542.9651
26000  26000  4       541.5368 542.2365
27000  27000  4       539.5325 539.9609
30000  30000  1       535.2317 535.2317
35000  35000  1       533.8045 533.8045
40000  40000  1       536.6813 536.6813
45000  45000  1       551.4434 551.4434

Residual checks PASSED

End of tests

Done: Wed Mar  6 01:27:43 PM EST 2024
```

1. **Size and LDA (Leading Dimension Array)**:
   - **Size**: This refers to the problem size, specifically the number of linear equations to solve, which directly corresponds to the size of the matrix involved in the computations. Larger sizes indicate more complex problems that require more computational resources.
   - **LDA**: The Leading Dimension of the Array is a parameter that specifies the physical storage dimensions of the matrix in memory. It's usually equal to or greater than the actual matrix size (problem size) to accommodate efficient memory access and alignment. The choice of LDA can affect the efficiency of the algorithm, especially in terms of memory usage and speed of accessing array elements during computation.
   - The key here is that LDA must be *at least* as large as the size of the matrix being solved.
2. **Align**: This represents the data alignment in kilobytes (Kbytes) and is crucial for optimizing memory access. Proper alignment ensures that data is stored in memory in a way that aligns with the cache lines, thereby minimizing cache misses and improving the efficiency of memory access. When data is well-aligned, the processor can fetch and store data more efficiently, leading to faster computation times and reduced risk of bottlenecks due to memory access delays.
3. **Time(s)**: The time, measured in seconds, indicates how long the system took to solve a set of linear equations of a given size.
4. **GFlops (Giga Floating-Point Operations Per Second)**: GFlops measure the number of billions of floating-point operations the system can perform per second.
5. **Residual and Residual(norm)**:
   - **Residual**: This is a measure of the error in the solutions of the linear equations. It's calculated as the difference between the left-hand side and right-hand side of the equations when using the computed solution. Ideally, the residual should be close to zero, indicating that the computed solution closely approximates the true solution.
   - **Residual(norm)**: The normalized residual provides a scale-independent measure of accuracy, which is particularly useful for comparing the accuracy across different problem sizes or different systems. A small normalized residual suggests that the solution is accurate relative to the size of the input matrix.
6. **Check**: This column indicates whether each individual test passed or failed based on the computed residuals. A "pass" means that the solution meets the predefined accuracy criteria, usually a small residual. This is crucial for verifying the reliability of the computational results, ensuring that they are within acceptable error margins.

## Additional Info

### How Block Size Works

Suppose we have a 4x4 matrix $A$ and we want to multiply it by another 4x4 matrix $B$.

$$
A = \begin{bmatrix}
a_{11} & a_{12} & a_{13} & a_{14} \\
a_{21} & a_{22} & a_{23} & a_{24} \\
a_{31} & a_{32} & a_{33} & a_{34} \\
a_{41} & a_{42} & a_{43} & a_{44}
\end{bmatrix}
B = \begin{bmatrix}
b_{11} & b_{12} & b_{13} & b_{14} \\
b_{21} & b_{22} & b_{23} & b_{24} \\
b_{31} & b_{32} & b_{33} & b_{34} \\
b_{41} & b_{42} & b_{43} & b_{44}
\end{bmatrix}
$$

We will choose a **block size of 2**, meaning we'll partition this matrix into four 2x2 blocks.

$$
A = \left[
\begin{array}{cc}
A_{11} & A_{12} \\
A_{21} & A_{22}
\end{array}
\right] = \left[
\begin{array}{cc}
\begin{bmatrix} a_{11} & a_{12} \\
 a_{21} & a_{22} \end{bmatrix} & \begin{bmatrix} a_{13} & a_{14} \\
 a_{23} & a_{24} \end{bmatrix} \\

\begin{bmatrix} a_{31} & a_{32} \\
 a_{41} & a_{42} \end{bmatrix} & \begin{bmatrix} a_{33} & a_{34} \\
 a_{43} & a_{44} \end{bmatrix}
\end{array}
\right]
$$
$$
B = \left[
\begin{array}{cc}
B_{11} & B_{12} \\
B_{21} & B_{22}
\end{array}
\right] = \left[
\begin{array}{cc}
\begin{bmatrix} b_{11} & b_{12} \\
 b_{21} & b_{22} \end{bmatrix} & \begin{bmatrix} b_{13} & b_{14} \\
 b_{23} & b_{24} \end{bmatrix} \\

\begin{bmatrix} b_{31} & b_{32} \\
 b_{41} & b_{42} \end{bmatrix} & \begin{bmatrix} b_{33} & b_{34} \\
 b_{43} & b_{44} \end{bmatrix}
\end{array}
\right]
$$

Where each block $A_{ij}$ is a 2x2 matrix:

$$
A_{11} = \begin{bmatrix} a_{11} & a_{12} \\
 a_{21} & a_{22} \end{bmatrix}, \quad B_{11} = \begin{bmatrix} b_{11} & b_{12} \\
 b_{21} & b_{22} \end{bmatrix}
$$

$$
A_{12} = \begin{bmatrix} a_{13} & a_{14} \\
 a_{23} & a_{24} \end{bmatrix}, \quad B_{12} = \begin{bmatrix} b_{13} & b_{14} \\
 b_{23} & b_{24} \end{bmatrix}
$$

$$
A_{21} = \begin{bmatrix} a_{31} & a_{32} \\
 a_{41} & a_{42} \end{bmatrix}, \quad B_{21} = \begin{bmatrix} b_{31} & b_{32} \\
 b_{41} & b_{42} \end{bmatrix}
$$

$$
A_{22} = \begin{bmatrix} a_{33} & a_{34} \\
 a_{43} & a_{44} \end{bmatrix}, \quad B_{22} = \begin{bmatrix} b_{33} & b_{34} \\
 b_{43} & b_{44} \end{bmatrix}
$$

Now we multiply them as follows to get $C = AB$:

1. Multiply the corresponding 2x2 blocks of matrices $A$ and $B$ together.
2. Add the resulting 2x2 matrices to form the blocks of the resulting matrix $C$.

**For $C_{11}$**:
   
$$
C_{11} = A_{11}B_{11} + A_{12}B_{21}
$$

Breaking it down, the multiplication and addition are:

$$
C_{11} = \begin{bmatrix} a_{11} & a_{12} \\
 a_{21} & a_{22} \end{bmatrix} \begin{bmatrix} b_{11} & b_{12} \\
 b_{21} & b_{22} \end{bmatrix} + \begin{bmatrix} a_{13} & a_{14} \\
 a_{23} & a_{24} \end{bmatrix} \begin{bmatrix} b_{31} & b_{32} \\
 b_{41} & b_{42} \end{bmatrix}
$$

This results in a new 2x2 matrix for $C_{11}$.

**For $C_{12}$**:

$$
C_{12} = A_{11}B_{12} + A_{12}B_{22}
$$

$$
C_{12} = \begin{bmatrix} a_{11} & a_{12} \\
 a_{21} & a_{22} \end{bmatrix} \begin{bmatrix} b_{13} & b_{14} \\
 b_{23} & b_{24} \end{bmatrix} + \begin{bmatrix} a_{13} & a_{14} \\
 a_{23} & a_{24} \end{bmatrix} \begin{bmatrix} b_{33} & b_{34} \\
 b_{43} & b_{44} \end{bmatrix}
$$

**For $C_{21}$**:

$$
C_{21} = A_{21}B_{11} + A_{22}B_{21}
$$
$$
C_{21} = \begin{bmatrix} a_{31} & a_{32} \\
 a_{41} & a_{42} \end{bmatrix} \begin{bmatrix} b_{11} & b_{12} \\
 b_{21} & b_{22} \end{bmatrix} + \begin{bmatrix} a_{33} & a_{34} \\
 a_{43} & a_{44} \end{bmatrix} \begin{bmatrix} b_{31} & b_{32} \\
 b_{41} & b_{42} \end{bmatrix}
$$

**For $C_{22}$**:

$$
C_{22} = A_{21}B_{12} + A_{22}B_{22}
$$
$$
C_{22} = \begin{bmatrix} a_{31} & a_{32} \\
 a_{41} & a_{42} \end{bmatrix} \begin{bmatrix} b_{13} & b_{14} \\
 b_{23} & b_{24} \end{bmatrix} + \begin{bmatrix} a_{33} & a_{34} \\
 a_{43} & a_{44} \end{bmatrix} \begin{bmatrix} b_{33} & b_{34} \\
 b_{43} & b_{44} \end{bmatrix}
$$

Each $C_{ij}$ block is computed by adding the products of the 2x2 blocks from matrices $A$ and $B$. The summation of these products gives us the respective blocks of the resulting matrix $C$.

### What is Numerical Stability

Numerical stability refers to the ability to produce accurate results even when subjected to small perturbations, such as rounding errors or slight changes in input values. A numerically stable algorithm minimizes the error amplification over its computation, ensuring that the outcome remains close to the true mathematical solution, even in the presence of inherent numerical inaccuracies due to the finite precision of floating-point representation.

Imagine the linear system $Ax = b$, where $A$ is a matrix, $x$ is the vector of unknowns, and $b$ is the result vector. What happens when, due to the nature of base 2, we have a slight inaccuracy in the calculation of $b$?

- **Original System**: $Ax = b$
- **Perturbed System**: $Ax' = b + \delta b$ (where $\delta b$ is a tiny change in $b$)

In the ideal outcome the solution $x'$ should only slightly differ from $x$, reflecting the small change $\delta b$.

A numerically stable algorithm ensures that the small change $\delta b$ leads to a proportionally small change in the solution $x'$.

In a numerically unstable algorithm a tiny change in $\delta b$ could result in a dramatically different solution $x'$, amplifying errors and leading to unreliable results.

### Right Looking LU Factorization

Right-looking LU factorization is a variant of the standard LU factorization. In regular LU factorization, the matrix is decomposed into a lower triangular matrix (L) and an upper triangular matrix (U) generally without specifying the order of operations. In contrast, the right-looking approach specifically refers to the order in which the matrix is processed: it begins with the leftmost column and moves rightward, updating the remainder of the matrix as it progresses. 

### Row Partial Pivoting

Row-partial pivoting in LU factorization is a strategy to enhance numerical stability. It interchanges rows of the matrix as it's decomposed into lower (L) and upper (U) triangular matrices. Before zeroing out below-diagonal elements in a column, the algorithm swaps the current row with a below row that has the largest absolute value in the current column. This step helps prevent small pivot elements, which can lead to significant numerical errors, ensuring the algorithm remains stable even for matrices prone to inducing calculation inaccuracies.

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

