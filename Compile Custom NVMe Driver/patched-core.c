

#define DEBUG_BUF_SIZE 1024 // Adjust based on needed capacity

struct debug_entry {
    char info[256]; // Adjust based on what you need to store, e.g., error messages
    unsigned long jiffies; // Timestamp
    // Extend with more fields if needed
};

static struct debug_entry debug_buf[DEBUG_BUF_SIZE];
static int debug_buf_pos = 0;

// Adds an entry to the circular debug buffer
void add_debug_entry(const char *info) {
    unsigned long flags;

    // Ensure thread safety (if necessary, depending on usage context)
    local_irq_save(flags);

    strncpy(debug_buf[debug_buf_pos].info, info, sizeof(debug_buf[debug_buf_pos].info) - 1);
    debug_buf[debug_buf_pos].jiffies = jiffies;
    // Initialize additional fields here if added

    debug_buf_pos = (debug_buf_pos + 1) % DEBUG_BUF_SIZE;

    local_irq_restore(flags);
}

void add_debug_entry(const char *info) {
    unsigned long flags;

    // Ensure thread safety (if necessary, depending on usage context)
    local_irq_save(flags);

    strncpy(debug_buf[debug_buf_pos].info, info, sizeof(debug_buf[debug_buf_pos].info) - 1);
    debug_buf[debug_buf_pos].info[sizeof(debug_buf[debug_buf_pos].info) - 1] = '\0'; // Ensure null-termination
    debug_buf[debug_buf_pos].jiffies = jiffies;

    debug_buf_pos = (debug_buf_pos + 1) % DEBUG_BUF_SIZE;

    local_irq_restore(flags);
}

void log_specific_nvme_error(u16 status) {
    char error_msg[256]; // Adjust size as necessary

    // Construct an appropriate message based on the NVMe status code
    snprintf(error_msg, sizeof(error_msg), "Specific NVMe error encountered: Status = 0x%x", status);
    
    // Log this occurrence to the circular DRAM buffer
    add_debug_entry(error_msg);
}

static blk_status_t nvme_error_status(u16 status)
{
    blk_status_t blk_status;

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
    // Special handling for specific NVMe errors
    case NVME_SC_WRITE_FAULT:
    case NVME_SC_READ_ERROR:
    case NVME_SC_UNWRITTEN_BLOCK:
    case NVME_SC_ACCESS_DENIED:
    case NVME_SC_READ_ONLY:
    case NVME_SC_COMPARE_FAILED:
        blk_status = BLK_STS_MEDIUM;
        // Call custom function to log specific NVMe errors
        log_specific_nvme_error(status);
        return blk_status;
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

#include <linux/uaccess.h> // For copy_to_user()
#include <linux/proc_fs.h> // For proc file operations
#include <linux/seq_file.h> // For sequential reads

// Prototype for simplicity; ensure it matches your actual setup
static ssize_t circular_buffer_read_proc(struct file *filp, char __user *buffer, size_t length, loff_t *offset);

static const struct file_operations proc_file_fops = {
    .owner = THIS_MODULE,
    .read = circular_buffer_read_proc,
};

ssize_t circular_buffer_read_proc(struct file *filp, char __user *buffer, size_t length, loff_t *offset) {
    static int finished = 0; // Static variable to keep track if we've finished reading the buffer
    int i;
    ssize_t ret = 0;

    if (finished) { // Check if we have finished reading the circular buffer
        finished = 0; // Reset for the next call
        return 0;
    }

    if (*offset >= DEBUG_BUF_SIZE) // Check if the offset is beyond our buffer size
        return 0;

    // Iterate over the circular buffer from the current offset
    for (i = *offset; i < DEBUG_BUF_SIZE; i++) {
        int bytes_not_copied;
        char entry_info[512]; // Buffer to hold the formatted entry for copying
        int entry_len;

        // Format the debug entry into entry_info, including the jiffies timestamp
        entry_len = snprintf(entry_info, sizeof(entry_info), "[%lu] %s\n", debug_buf[i].jiffies, debug_buf[i].info);

        // Ensure we don't copy more than the user buffer can hold
        if (length < entry_len) break;

        // Copy the formatted string to user space
        bytes_not_copied = copy_to_user(buffer + ret, entry_info, entry_len);
        if (bytes_not_copied == 0) {
            ret += entry_len; // Increment return value by the number of bytes successfully copied
            *offset = i + 1;  // Update offset for partial reads
        } else {
            break; // Break the loop if we couldn't copy data to user space
        }

        if (ret >= length) break; // Check if we've filled the user buffer
    }

    finished = 1; // Indicate we've finished reading the circular buffer
    return ret; // Return the number of bytes copied
}

static struct proc_dir_entry *proc_file_entry;

int init_module(void) { // Module initialization function
    proc_file_entry = proc_create("nvme_circular_buffer", 0444, NULL, &proc_fops);
    if (proc_file_entry == NULL) {
        return -ENOMEM; // Return an error if unable to create proc entry
    }
    return 0; // Success
}

static const struct file_operations proc_fops = {
    .owner = THIS_MODULE,
    .read = circular_buffer_read_proc,
};

void cleanup_module(void) { // Module cleanup function
    proc_remove(proc_file_entry);
}