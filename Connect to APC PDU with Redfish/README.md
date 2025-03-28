# Connect to APC PDU with Redfish (IN PROGRESS)

## Problems

- If Redfish is not enabled you get auth failed rather than Redfish not enabled. This should return something sensible rather than outright misleading.

```bash
python apc_test.py
[!] Auth failed: 400
```

