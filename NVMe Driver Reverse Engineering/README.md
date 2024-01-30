
## Reverse Engineering

### NVMe ENODATA

- Started by looking for ENODATA and it only appears here:

```c
inline u16 errno_to_nvme_status(struct nvmet_req *req, int errno)
{
	switch (errno) {
	case 0:
		return NVME_SC_SUCCESS;
	case -ENOSPC:
		req->error_loc = offsetof(struct nvme_rw_command, length);
		return NVME_SC_CAP_EXCEEDED | NVME_SC_DNR;
	case -EREMOTEIO:
		req->error_loc = offsetof(struct nvme_rw_command, slba);
		return  NVME_SC_LBA_RANGE | NVME_SC_DNR;
	case -EOPNOTSUPP:
		req->error_loc = offsetof(struct nvme_common_command, opcode);
		switch (req->cmd->common.opcode) {
		case nvme_cmd_dsm:
		case nvme_cmd_write_zeroes:
			return NVME_SC_ONCS_NOT_SUPPORTED | NVME_SC_DNR;
		default:
			return NVME_SC_INVALID_OPCODE | NVME_SC_DNR;
		}
		break;
	case -ENODATA:
		req->error_loc = offsetof(struct nvme_rw_command, nsid);
		return NVME_SC_ACCESS_DENIED;
	case -EIO:
		fallthrough;
	default:
		req->error_loc = offsetof(struct nvme_common_command, opcode);
		return NVME_SC_INTERNAL | NVME_SC_DNR;
	}
}
```

This C function, `errno_to_nvme_status`, converts a given error number (`errno`) to an NVMe status code. It's designed to be used within the context of NVMe (Non-Volatile Memory express) subsystems, particularly for handling error conditions. The function takes two parameters: a pointer to a `struct nvmet_req` (which represents a request in the NVMe target subsystem) and an `int` representing the error number (`errno`). Here's a breakdown of its behavior:

1. **Switch Statement on `errno`**: The function uses a switch-case statement to handle different values of `errno`.

2. **Case 0 (Success)**: If `errno` is 0 (no error), it returns `NVME_SC_SUCCESS`, indicating successful completion.

3. **Case `-ENOSPC` (No Space Left on Device)**: For this error, it sets the `error_loc` field of the request to the offset of the `length` field in the `struct nvme_rw_command`. It then returns `NVME_SC_CAP_EXCEEDED | NVME_SC_DNR`, indicating that the capacity is exceeded and the request should not be retried.

4. **Case `-EREMOTEIO` (Remote I/O Error)**: This sets `error_loc` to the offset of the `slba` field in `struct nvme_rw_command` and returns `NVME_SC_LBA_RANGE | NVME_SC_DNR`, indicating an LBA (Logical Block Addressing) range error and that the request should not be retried.

5. **Case `-EOPNOTSUPP` (Operation Not Supported)**: The function sets `error_loc` to the offset of the `opcode` field in `struct nvme_common_command`. It then checks the opcode of the command: if it's `nvme_cmd_dsm` or `nvme_cmd_write_zeroes`, it returns `NVME_SC_ONCS_NOT_SUPPORTED | NVME_SC_DNR`, indicating that the operation is not supported. For other opcodes, it returns `NVME_SC_INVALID_OPCODE | NVME_SC_DNR`, indicating an invalid opcode.

6. **Case `-ENODATA` (No Data)**: Sets `error_loc` to the offset of the `nsid` field in `struct nvme_rw_command` and returns `NVME_SC_ACCESS_DENIED`, indicating access is denied.

7. **Case `-EIO` (I/O Error) and Default**: For an I/O error or any other unspecified error (`default` case), it sets `error_loc` to the offset of the `opcode` in `struct nvme_common_command` and returns `NVME_SC_INTERNAL | NVME_SC_DNR`, indicating an internal error and that the request should not be retried.

This function is specific to NVMe storage device error handling, translating system errors into NVMe-specific status codes, providing additional information about the location of the error in the command structure.

### NVMe Block Status Codes

```c
static blk_status_t nvme_error_status(u16 status)
{
	switch (status & 0x7ff) {
	case NVME_SC_SUCCESS:
		return BLK_STS_OK;
	case NVME_SC_CAP_EXCEEDED:
		return BLK_STS_NOSPC;
	case NVME_SC_LBA_RANGE:
	case NVME_SC_CMD_INTERRUPTED:
	case NVME_SC_NS_NOT_READY:
		return BLK_STS_TARGET;
	case NVME_SC_BAD_ATTRIBUTES:
	case NVME_SC_ONCS_NOT_SUPPORTED:
	case NVME_SC_INVALID_OPCODE:
	case NVME_SC_INVALID_FIELD:
	case NVME_SC_INVALID_NS:
		return BLK_STS_NOTSUPP;
	case NVME_SC_WRITE_FAULT:
	case NVME_SC_READ_ERROR:
	case NVME_SC_UNWRITTEN_BLOCK:
	case NVME_SC_ACCESS_DENIED:
	case NVME_SC_READ_ONLY:
	case NVME_SC_COMPARE_FAILED:
		return BLK_STS_MEDIUM;
	case NVME_SC_GUARD_CHECK:
	case NVME_SC_APPTAG_CHECK:
	case NVME_SC_REFTAG_CHECK:
	case NVME_SC_INVALID_PI:
		return BLK_STS_PROTECTION;
	case NVME_SC_RESERVATION_CONFLICT:
		return BLK_STS_RESV_CONFLICT;
	case NVME_SC_HOST_PATH_ERROR:
		return BLK_STS_TRANSPORT;
	case NVME_SC_ZONE_TOO_MANY_ACTIVE:
		return BLK_STS_ZONE_ACTIVE_RESOURCE;
	case NVME_SC_ZONE_TOO_MANY_OPEN:
		return BLK_STS_ZONE_OPEN_RESOURCE;
	default:
		return BLK_STS_IOERR;
	}
}
```

### NVMe End Request

```c
static inline void nvme_end_req(struct request *req)
{
	blk_status_t status = nvme_error_status(nvme_req(req)->status);

	if (unlikely(nvme_req(req)->status && !(req->rq_flags & RQF_QUIET)))
		nvme_log_error(req);
	nvme_end_req_zoned(req);
	nvme_trace_bio_complete(req);
	if (req->cmd_flags & REQ_NVME_MPATH)
		nvme_mpath_end_request(req);
	blk_mq_end_request(req, status);
}
```

The function `nvme_end_req` is a part of the NVMe driver in the Linux kernel. It's responsible for finalizing an NVMe I/O request. Here's a step-by-step explanation of what this function is doing:

1. **Convert NVMe Status to Block Layer Status**: 
    - `blk_status_t status = nvme_error_status(nvme_req(req)->status);`
    - This line calls `nvme_error_status` with the NVMe request's status code. The `nvme_error_status` function translates NVMe-specific status codes (like `NVME_SC_WRITE_FAULT`) into generic block layer status codes (`blk_status_t`). This translation is necessary because the block layer of the kernel (which handles block devices like SSDs and HDDs) uses its own set of status codes.

2. **Log Error if Necessary**:
    - `if (unlikely(nvme_req(req)->status && !(req->rq_flags & RQF_QUIET))) nvme_log_error(req);`
    - This line checks if there was an error in the NVMe request (i.e., `status` is non-zero) and if the request is not flagged as `RQF_QUIET` (which suppresses error logging). If these conditions are met, it logs the error using `nvme_log_error`.

3. **Handle Zoned Requests**:
    - `nvme_end_req_zoned(req);`
    - This line calls a function to handle the end of a zoned request. NVMe zoned namespaces (ZNS) are a type of storage architecture on NVMe devices that can improve performance and endurance by dividing the storage space into zones.

4. **Trace Bio Completion**:
    - `nvme_trace_bio_complete(req);`
    - This line is for tracing/block layer accounting purposes. It's used for diagnostic and performance monitoring tools to track the completion of the block I/O (`bio`) request.

5. **Multipath Handling**:
    - `if (req->cmd_flags & REQ_NVME_MPATH) nvme_mpath_end_request(req);`
    - This checks if the request is a multipath I/O request (using NVMe multipathing features). If it is, it calls `nvme_mpath_end_request` to handle the multipath-specific aspects of request completion.

6. **Finalize the Request**:
    - `blk_mq_end_request(req, status);`
    - Finally, it calls `blk_mq_end_request`, which marks the request as completed in the block layer. The `status` parameter is the translated block status code.

In summary, `nvme_end_req` is a comprehensive function that handles the finalization of NVMe I/O requests. It takes care of translating NVMe-specific status codes to generic block layer codes, logs errors if necessary, deals with zoned requests, handles multipathing, and ensures the request is properly completed in the block subsystem of the kernel.

### The Call to NVMe End Request

```c
void nvme_complete_rq(struct request *req)
{
	struct nvme_ctrl *ctrl = nvme_req(req)->ctrl;

	trace_nvme_complete_rq(req);
	nvme_cleanup_cmd(req);

	/*
	 * Completions of long-running commands should not be able to
	 * defer sending of periodic keep alives, since the controller
	 * may have completed processing such commands a long time ago
	 * (arbitrarily close to command submission time).
	 * req->deadline - req->timeout is the command submission time
	 * in jiffies.
	 */
	if (ctrl->kas &&
	    req->deadline - req->timeout >= ctrl->ka_last_check_time)
		ctrl->comp_seen = true;

	switch (nvme_decide_disposition(req)) {
	case COMPLETE:
		nvme_end_req(req);
		return;
	case RETRY:
		nvme_retry_req(req);
		return;
	case FAILOVER:
		nvme_failover_req(req);
		return;
	case AUTHENTICATE:
#ifdef CONFIG_NVME_HOST_AUTH
		queue_work(nvme_wq, &ctrl->dhchap_auth_work);
		nvme_retry_req(req);
#else
		nvme_end_req(req);
#endif
		return;
	}
}
EXPORT_SYMBOL_GPL(nvme_complete_rq);

void nvme_complete_batch_req(struct request *req)
{
	trace_nvme_complete_rq(req);
	nvme_cleanup_cmd(req);
	nvme_end_req_zoned(req);
}
EXPORT_SYMBOL_GPL(nvme_complete_batch_req);
```

The provided code defines two functions, `nvme_complete_rq` and `nvme_complete_batch_req`, which are part of the NVMe (Non-Volatile Memory Express) driver in the Linux kernel. These functions are responsible for handling the completion of NVMe requests. Let's break down what each function does:

### `nvme_complete_rq` Function

This function is called to complete a single NVMe request.

1. **Trace and Cleanup**:
    - `trace_nvme_complete_rq(req);` records a tracepoint for the completion of the request. Tracepoints are used for debugging and performance analysis.
    - `nvme_cleanup_cmd(req);` cleans up the command associated with the request.

2. **Keep Alive Check**:
    - The block checks if the completion of long-running commands should trigger a keep-alive signal. NVMe controllers may drop connections if they don't receive periodic keep-alive messages.
    - `ctrl->kas` checks if keep-alive is enabled. If the command has been running longer than the last keep-alive check, it sets `ctrl->comp_seen` to `true` to ensure a keep-alive message is sent.

3. **Command Disposition**:
    - `switch (nvme_decide_disposition(req))` decides how to handle the request based on its current state, which can be one of `COMPLETE`, `RETRY`, `FAILOVER`, or `AUTHENTICATE`.
    - `COMPLETE`: Calls `nvme_end_req(req)` to finalize the request.
    - `RETRY`: Calls `nvme_retry_req(req)` to retry the request.
    - `FAILOVER`: Calls `nvme_failover_req(req)` to handle failover in case of an error.
    - `AUTHENTICATE`: In systems with host authentication (`CONFIG_NVME_HOST_AUTH`), queues authentication work and retries the request. Otherwise, it ends the request.

### `nvme_complete_batch_req` Function

This function is designed for completing a batch of NVMe requests, particularly for zoned namespaces.

1. **Trace and Cleanup**:
    - Similar to `nvme_complete_rq`, it records a tracepoint and cleans up the command.

2. **Zoned Request Completion**:
    - Calls `nvme_end_req_zoned(req)` to handle the specific requirements for completing a zoned request.

### Summary

- `nvme_complete_rq` is a more comprehensive function handling individual NVMe requests, including various scenarios like retries, failovers, and special handling for long-running commands in the context of keep-alive signals.
- `nvme_complete_batch_req` is a simpler function used for completing a batch of requests, with specific handling for zoned namespaces.

These functions are critical for the NVMe driver's operation in Linux, ensuring that NVMe requests are correctly processed, completed, retried, or failed over as needed. They also handle the specific requirements of zoned namespaces, a feature that optimizes SSD performance and longevity.

#### NVMe Completion Described

The `nvme_end_req` function is typically called at the end of an NVMe I/O request's lifecycle in the Linux kernel's NVMe driver. This function is invoked when an I/O request to an NVMe device has been processed and is ready to be completed. Here's a general overview of when and how it gets called:

1. **Completion of an I/O Operation**: NVMe I/O operations, such as read or write requests, are processed asynchronously. When an NVMe I/O operation completes (successfully or with an error), a completion routine is triggered. `nvme_end_req` is often called within such completion routines.

2. **From NVMe Interrupt Handlers**: NVMe devices use interrupts to signal the completion of I/O operations. The NVMe driver has interrupt handlers to respond to these interrupts. When an interrupt indicates the completion of an I/O request, the interrupt handler will eventually call `nvme_end_req` to finalize the request.

3. **Completion Path in the NVMe Driver**: Within the NVMe driver's code, after processing the response from the NVMe device (like handling the status of the command), the driver will call `nvme_end_req` to clean up the request and perform necessary final steps like error logging, multipath handling, and notifying the block layer of the completion status.

4. **In Response to Errors or Timeouts**: If an error occurs during the processing of an NVMe command, or if a command times out, `nvme_end_req` will be called as part of the error handling or timeout handling code path to properly complete the request with the appropriate error status.

5. **NVMe Queue Processing**: The NVMe driver uses request queues to manage I/O operations. As requests are processed and completed (either by the hardware or due to some error conditions), `nvme_end_req` is called to properly close out these requests.

The exact call chain leading to `nvme_end_req` can be quite complex, as it involves asynchronous I/O processing, interrupt handling, and interactions with the Linux kernel's block layer. The function plays a crucial role in ensuring that each I/O request is correctly finalized, whether it completes successfully or encounters an error.

## Zoned vs Not Zoned

The difference between zoned and non-zoned in the context of NVMe (Non-Volatile Memory Express) and the provided code snippets pertains to a specific type of storage management called Zoned Namespaces (ZNS).

Zoned Namespaces is a relatively new concept in NVMe storage, introduced to optimize the way data is written and managed, particularly for SSDs. Let's break down what each type of namespace means:

1. **Non-Zoned (Regular) NVMe Namespaces**:
    - In regular (non-zoned) NVMe namespaces, data can be written to any location on the drive without any specific restrictions. This is the traditional way SSDs operate.
    - You can perform typical read, write, and erase operations anywhere across the drive's storage space.
    - This approach is straightforward but can lead to inefficiencies in how data is stored and managed, especially as the drive starts to fill up and requires more frequent garbage collection and wear leveling.

2. **Zoned NVMe Namespaces**:
    - In ZNS (Zoned Namespaces), the storage space is divided into zones.
    - Each zone must be written sequentially, meaning new data must be appended to the end of the current data in the zone. This is unlike regular namespaces where data can be written randomly.
    - This sequential write requirement aligns better with the underlying characteristics of NAND flash memory, potentially increasing drive efficiency, lifespan, and performance.
    - ZNS can reduce the overhead of garbage collection and wear leveling, as each zone is written and erased as a unit.

Now, looking at your provided code:

- `nvme_end_req_zoned` function: This function is specifically for handling the completion of requests in a zoned namespace. If the request is a zone append operation (indicated by `REQ_OP_ZONE_APPEND`), it updates the sector number based on the result of the NVMe command. This is specific to ZNS, where the location where data is written might be determined by the drive and needs to be communicated back to the host system.

- `nvme_end_req` function: This is a more general function for handling the completion of any NVMe request (both zoned and non-zoned). It calls `nvme_end_req_zoned` as part of its process, so it correctly handles zoned requests when necessary. For non-zoned requests, or if zoned features are not enabled (`CONFIG_BLK_DEV_ZONED` not set), `nvme_end_req` handles the request completion without the specific considerations needed for ZNS.

In summary, the key difference is in how data is written and managed on the drive: zoned namespaces require sequential writes within zones, while non-zoned namespaces do not have this restriction. The code you provided shows how the NVMe driver in Linux handles these differences during the completion of I/O requests.