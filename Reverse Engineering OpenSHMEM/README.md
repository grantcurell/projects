# Reverse Engineering OpenSHMEM

- [Reverse Engineering OpenSHMEM](#reverse-engineering-openshmem)
  - [libfabric](#libfabric)
  - [Tracing the Implementation of shmem\_put](#tracing-the-implementation-of-shmem_put)
    - [**Breakdown of `shmem_internal_put_nb`**](#breakdown-of-shmem_internal_put_nb)
    - [**Function Parameters**](#function-parameters)
    - [**Implementation Analysis**](#implementation-analysis)
    - [**Related Functions**](#related-functions)
    - [**Where is it Used?**](#where-is-it-used)
    - [**Key Points**](#key-points)
  - [**Where is it Used?**](#where-is-it-used-1)


## libfabric

- Abstracts the network communication aspect of things for the application. Below is an example of a high level SHMEM program that leverages it.

```c
#include <shmem.h>
#include <stdio.h>

int main() {
    shmem_init();  // Uses libfabric internally

    int my_pe = shmem_my_pe();
    int num_pes = shmem_n_pes();

    static int shared_var = 0;  // Symmetric memory

    shmem_barrier_all();  // Ensure all PEs reach this point

    if (my_pe == 0) {
        shared_var = 42;
        shmem_put(&shared_var, &shared_var, 1, 1);  // Uses libfabric to send data
    }

    shmem_barrier_all();  // Wait for transfer

    printf("PE %d sees shared_var = %d\n", my_pe, shared_var);

    shmem_finalize();  // Uses libfabric internally
    return 0;
}
```

## Tracing the Implementation of shmem_put

I used [Sandia's Source Code](https://github.com/Sandia-OpenSHMEM/SOS)

Definition for `shmem_put`

```
src\data_c.c4:69:`#pragma weak shmem_put$1 = pshmem_put$1
src\data_c.c4:70:#define shmem_put$1 pshmem_put$1')dnl
src\data_c.c4:91:`#pragma weak shmem_put$1_nbi = pshmem_put$1_nbi
src\data_c.c4:92:#define shmem_put$1_nbi pshmem_put$1_nbi')dnl
src\data_c.c4:238:`#pragma weak shmem_put$1_signal = pshmem_put$1_signal
src\data_c.c4:239:#define shmem_put$1_signal pshmem_put$1_signal')dnl
src\data_c.c4:261:`#pragma weak shmem_put$1_signal_nbi = pshmem_put$1_signal_nbi
src\data_c.c4:262:#define shmem_put$1_signal_nbi pshmem_put$1_signal_nbi')dnl
src\data_f.c4:57:`SHMEM_DEF_FC_PUT(FC_FUNC_(SH_DOWNCASE(shmem_put$1), SH_UPCASE(SHMEM_PUT$1)), $2)')dnl
src\data_f.c4:83:`SHMEM_DEF_FC_PUT_NBI(FC_FUNC_(SH_DOWNCASE(shmem_put$1_nbi), SH_UPCASE(SHMEM_PUT$1_NBI)), $2)')dnl
```

So I went and looked at `data_c`

1. **`shmem_put` is mapped via `#pragma weak` to `pshmem_put`**:
    
    ```c
    #pragma weak shmem_put = pshmem_put
    #define shmem_put pshmem_put
    ```
    
    This means `shmem_put` is an alias for `pshmem_put` when profiling is enabled.
    
2. **The actual implementation of `shmem_put` is in this macro**:
    
    ```c
    #define SHMEM_DEF_PUT(STYPE, TYPE)                                \
    void SHMEM_FUNCTION_ATTRIBUTES                                 \
    SHMEM_FUNC_PROTOTYPE(STYPE##_put, TYPE *target,                \
                         const TYPE *source, size_t nelems, int pe)\
    long completion = 0;                                         \
    SHMEM_ERR_CHECK_INITIALIZED();                               \
    SHMEM_ERR_CHECK_PE(pe);                                      \
    SHMEM_ERR_CHECK_CTX(ctx);                                    \
    SHMEM_ERR_CHECK_SYMMETRIC(target, sizeof(TYPE) * nelems);    \
    SHMEM_ERR_CHECK_NULL(source, nelems);                        \
    SHMEM_ERR_CHECK_OVERLAP(target, source, sizeof(TYPE) *       \
                            nelems, sizeof(TYPE) * nelems, 0,    \
                            (shmem_internal_my_pe == pe));       \
    shmem_internal_put_nb(ctx, target, source,                   \
                          sizeof(TYPE) * nelems, pe,             \
                          &completion);                          \
    shmem_internal_put_wait(ctx, &completion);                   \
    }
    ```
    
    This tells us:
    
    - **Validation checks** are performed (initialization, PE check, context check, symmetry check, overlap check).
    - The actual **non-blocking put operation** is done using `shmem_internal_put_nb`.
    - The function **waits for completion** using `shmem_internal_put_wait`.

---

If we look at `shmem_comm.h` we find the implementation for `shmem_internal_put_nb`.

```c
static inline
void
shmem_internal_put_nb(shmem_ctx_t ctx, void *target, const void *source, size_t len, int pe,
                      long *completion)
{
    if (len == 0)
        return;

    if (shmem_shr_transport_use_write(ctx, target, source, len, pe)) {
        shmem_shr_transport_put(ctx, target, source, len, pe);
    } else {
        shmem_transport_put_nb((shmem_transport_ctx_t *)ctx, target, source, len, pe, completion);
    }
}
```

### **Breakdown of `shmem_internal_put_nb`**

1. **Check for Zero-Length Transfers**
    
    - If `len == 0`, it just returns immediately.
2. **Choose the Transport Mechanism**
    
    - If `shmem_shr_transport_use_write(...)` is `true`, it calls:
        
        ```c
        shmem_shr_transport_put(ctx, target, source, len, pe);
        ```
        
        This is an alternative transport layer (Shared Transport).
    - Otherwise, it calls:
        
        ```c
        shmem_transport_put_nb((shmem_transport_ctx_t *)ctx, target, source, len, pe, completion);
        ```
        
        This is the **main transport function**, which is where the actual network communication happens.

---

We see that it is defined in multiple different places and depends on the specific type of network in use ex: Unified Communications X (UCX), portals, or openfabrics interconnect (OFI).

```
PS C:\Users\grant\Downloads\SOS-main> Get-ChildItem -Path . -Recurse -Include *.c,*.h | Select-String -Pattern 'shmem_transport_put_nb'

...SNIP...
src\transport_none.h:122:shmem_transport_put_nb(shmem_transport_ctx_t* ctx, void *target, const void *source, size_t
len,
src\transport_none.h:145:shmem_transport_put_nbi(shmem_transport_ctx_t* ctx, void *target, const void *source, size_t
len,
src\transport_ofi.h:680:void shmem_transport_put_nb(shmem_transport_ctx_t* ctx, void *target, const void *source,
size_t len,
src\transport_ofi.h:884:void shmem_transport_put_nbi(shmem_transport_ctx_t* ctx, void *target, const void *source,
size_t len,
src\transport_portals4.h:574:shmem_transport_put_nbi(shmem_transport_ctx_t* ctx, void *target, const void *source,
size_t len, int pe)
src\transport_portals4.h:590:shmem_transport_put_nb(shmem_transport_ctx_t* ctx, void *target, const void *source,
size_t len,
src\transport_portals4.h:606:        shmem_transport_put_nbi(ctx, target, source, len, pe);
src\transport_portals4.h:1110:    shmem_transport_put_nbi(ctx, target, source, len, pe);
src\transport_ucx.h:254:shmem_transport_put_nb(shmem_transport_ctx_t* ctx, void *target, const void *source, size_t
len,
src\transport_ucx.h:286:shmem_transport_put_nbi(shmem_transport_ctx_t* ctx, void *target, const void *source, size_t
len,
src\transport_ucx.h:725:    shmem_transport_put_nbi(ctx, target, source, len, pe);
```

We're interested in the OpenFabrics Interconnect implementation so I went and looked at transport_ofi.h:

```c
static inline
void shmem_transport_put_nb(shmem_transport_ctx_t* ctx, void *target, const void *source, size_t len,
                            int pe, long *completion)
{
    int ret = 0;
    uint64_t dst = (uint64_t) pe;
    uint64_t polled = 0;
    uint64_t key;
    uint8_t *addr;

    shmem_internal_assert(completion != NULL);

    if (len <= shmem_transport_ofi_max_buffered_send) {

        shmem_transport_put_scalar(ctx, target, source, len, pe);

    } else if (len <= shmem_transport_ofi_bounce_buffer_size && ctx->bounce_buffers) {

        SHMEM_TRANSPORT_OFI_CTX_LOCK(ctx);
        SHMEM_TRANSPORT_OFI_CNTR_INC(&ctx->pending_put_cntr);
        shmem_transport_ofi_get_mr(target, pe, &addr, &key);

        shmem_transport_ofi_bounce_buffer_t *buff =
            create_bounce_buffer(ctx, source, len);
        polled = 0;

        const struct iovec      msg_iov = { .iov_base = buff->data, .iov_len = len };
        const struct fi_rma_iov rma_iov = { .addr = (uint64_t) addr, .len = len, .key = key };
        const struct fi_msg_rma msg     = {
                                            .msg_iov       = &msg_iov,
                                            .desc          = GET_MR_DESC_ADDR(shmem_transport_ofi_get_mr_desc_index(source)),
                                            .iov_count     = 1,
                                            .addr          = GET_DEST(dst),
                                            .rma_iov       = &rma_iov,
                                            .rma_iov_count = 1,
                                            .context       = buff,
                                            .data          = 0
                                          };
        do {
            ret = fi_writemsg(ctx->ep, &msg, FI_COMPLETION | FI_DELIVERY_COMPLETE);
        } while (try_again(ctx, ret, &polled));
        SHMEM_TRANSPORT_OFI_CTX_UNLOCK(ctx);

    } else {
        shmem_transport_ofi_put_large(ctx, target, source,len, pe);
        (*completion)++;
    }
}
```

### **Function Parameters**

- `shmem_transport_ctx_t* ctx` → The SHMEM transport context.
- `void *target` → Remote memory location where data is to be written.
- `const void *source` → Local memory buffer containing the data to be written.
- `size_t len` → Length of the data transfer in bytes.
- `int pe` → The processing element (PE) ID of the target node.
- `long *completion` → A pointer to a counter tracking completion status.

---

### **Implementation Analysis**

1. **Handles Non-Blocking Puts (`NB`)**
    
    - This function issues a **non-blocking** put operation.
    - The completion status is tracked via `completion`, which is incremented if needed.
2. **Uses Multiple Strategies for Data Transfer**
    
    - **Small transfers (`<= shmem_transport_ofi_max_buffered_send`)**
        - Calls `shmem_transport_put_scalar()`, which likely performs an `fi_inject_write()`.
    - **Medium-sized transfers (`<= shmem_transport_ofi_bounce_buffer_size`)**
        - Uses a **bounce buffer** and `fi_writemsg()`.
    - **Large transfers**
        - Calls `shmem_transport_ofi_put_large()`, which likely **splits data** into chunks.
3. **Uses `libfabric` API**
    
    - The function interacts with **libfabric** (`fi_writemsg()`).
    - It leverages **Remote Memory Access (RMA)** with **FI_COMPLETION** and **FI_DELIVERY_COMPLETE**.
4. **Ensures Ordering**
    
    - `SHMEM_TRANSPORT_OFI_CTX_LOCK(ctx)` and `SHMEM_TRANSPORT_OFI_CTX_UNLOCK(ctx)` protect shared state.

---

### **Related Functions**

- **`shmem_transport_put_scalar()`**: Used for small transfers (`<= shmem_transport_ofi_max_buffered_send`).
- **`shmem_transport_ofi_put_large()`**: Used for large transfers.
- **`shmem_transport_put_wait()`**: Ensures completion.

---

### **Where is it Used?**

- **`shmem_internal_put_nb()`** in `shmem_comm.h` calls `shmem_transport_put_nb()` when shared memory writes are not possible:
    
    ```c
    shmem_transport_put_nb((shmem_transport_ctx_t *)ctx, target, source, len, pe, completion);
    ```
    
- Other files (`transport_none.h`, `transport_portals4.h`, etc.) contain different transport implementations.

---

If we go look at `shmem_transport_put_scalar` we see

```c
static inline
void shmem_transport_put_scalar(shmem_transport_ctx_t* ctx, void *target, const
                               void *source, size_t len, int pe)
{
    int ret = 0;
    uint64_t dst = (uint64_t) pe;
    uint64_t polled = 0;
    uint64_t key;
    uint8_t *addr;

    shmem_transport_ofi_get_mr(target, pe, &addr, &key);

    shmem_internal_assert(len <= shmem_transport_ofi_max_buffered_send);

    SHMEM_TRANSPORT_OFI_CTX_LOCK(ctx);
    SHMEM_TRANSPORT_OFI_CNTR_INC(&ctx->pending_put_cntr);

    do {

        ret = fi_inject_write(ctx->ep,
                              source,
                              len,
                              GET_DEST(dst),
                              (uint64_t) addr,
                              key);

    } while (try_again(ctx, ret, &polled));
    SHMEM_TRANSPORT_OFI_CTX_UNLOCK(ctx);
}
```

### **Key Points**

1. **Handles Small Transfers**
    
    - This function is called when `len <= shmem_transport_ofi_max_buffered_send`.
    - It ensures that small messages are handled **efficiently** without needing extra buffering.
2. **Uses `fi_inject_write()`**
    
    - `fi_inject_write()` is a **one-sided, RDMA write** in **libfabric** that:
        - Does **not** require completion tracking.
        - Is optimized for **small messages**.
3. **Memory Registration**
    
    - Calls `shmem_transport_ofi_get_mr(target, pe, &addr, &key);`
    - This function retrieves:
        - `addr`: the remote memory address.
        - `key`: the remote memory region key.
4. **Ensures Ordering**
    
    - Uses:
        
        ```c
        SHMEM_TRANSPORT_OFI_CTX_LOCK(ctx);
        SHMEM_TRANSPORT_OFI_CTX_UNLOCK(ctx);
        ```
        
    - This ensures **atomicity** when accessing shared structures.
5. **Retries on Resource Exhaustion**
    
    - Uses:
        
        ```c
        do {
            ret = fi_inject_write(...);
        } while (try_again(ctx, ret, &polled));
        ```
        
    - If `fi_inject_write()` fails due to a temporary resource issue (e.g., lack of completion queue entries), it **retries**.
6. **Incrementing the Counter**
    
    - Uses:
        
        ```c
        SHMEM_TRANSPORT_OFI_CNTR_INC(&ctx->pending_put_cntr);
        ```
        
    - This ensures the operation is **tracked** in the transport layer.

---

## **Where is it Used?**

- **`shmem_transport_put_nb()`** (Non-Blocking Put)
    
    ```c
    if (len <= shmem_transport_ofi_max_buffered_send) {
        shmem_transport_put_scalar(ctx, target, source, len, pe);
    }
    ```
    
- **`shmem_transport_put_nbi()`** (Non-Blocking Immediate Put)
    
    ```c
    if (len <= shmem_transport_ofi_max_buffered_send) {
        shmem_transport_put_scalar(ctx, target, source, len, pe);
    }
    ```
    
- It is also indirectly used by `shmem_internal_put_nb()` and similar SHMEM API functions.
