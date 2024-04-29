def nvme_error_lookup():
    # Prompt the user for the NVMe status code in hexadecimal
    status_code_hex = input("Enter NVMe status code in hex (e.g., 0x2281): ")

    # Convert hex input to integer
    status_code = int(status_code_hex, 16)

    # Mask the status code
    masked_status = status_code & 0x7ff

    # Define the specific NVMe error codes of interest
    nvme_error_codes = {
        0x280: "NVME_SC_WRITE_FAULT",
        0x281: "NVME_SC_READ_ERROR",
        0x287: "NVME_SC_UNWRITTEN_BLOCK",
        0x286: "NVME_SC_ACCESS_DENIED",
        0x182: "NVME_SC_READ_ONLY",
        0x285: "NVME_SC_COMPARE_FAILED",
    }

    # Lookup the error code
    error_name = nvme_error_codes.get(masked_status, "Unknown Error Code")

    print(f"Error Code: {status_code_hex} (Masked: 0x{masked_status:x}) - {error_name}")


# Call the function to prompt the user and look up the NVMe error
nvme_error_lookup()