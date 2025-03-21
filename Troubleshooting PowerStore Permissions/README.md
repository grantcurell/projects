# Troubleshooting PowerStore Permissions (IN PROGRESS)

## Problem Summary

In mixed-protocol environments using both NFS and SMB access to a PowerStore share, users may encounter inconsistent file ownership and permission behavior across the two protocols. This typically occurs when:

- Files are created from the Linux (NFS) side using an AD-authenticated user with `uidNumber`/`gidNumber` attributes.
- Those files are then accessed from the Windows (SMB) side, which uses SIDs instead of UID/GID.
- Or vice versa: files created on the Windows side show up with incorrect or dynamic UIDs on the Linux side, resulting in permission mismatches or access denial.

This usually stems from a missing or misconfigured identity mapping between Active Directory and PowerStore’s internal mapping between UNIX-style and Windows-style users.

## Steps to Replicate

1. Ensure AD User is Configured for UNIX  
   Use Active Directory Users and Computers (ADUC) or ADSI Edit to assign the following attributes to the test user (e.g. `jeet.ad`):
   - `uidNumber` (e.g., 12345)
   - `gidNumber` (e.g., 12345)

   Confirm this works on the Linux client:
   ```bash
   getent passwd jeet.ad
   ```

2. Prepare the Share on PowerStore  
   - Create a dual-protocol NAS share (exported via both NFS and SMB).
   - Ensure the share is joined to the same AD domain and is visible via both protocols.
   - Share paths (example):
     - SMB: `\\powerstore\PSTestShare`
     - NFS: `powerstore:/PSTestShare`

3. Mount NFS on Linux  
   ```bash
   sudo mount -t nfs powerstore:/PSTestShare /mnt/nfs
   ```

4. Create File from Linux as AD User  
   ```bash
   sudo -u jeet.ad touch /mnt/nfs/test_from_unix.txt
   ```
   Confirm:
   ```bash
   ls -ln /mnt/nfs/test_from_unix.txt
   ```
   It should show `uid=12345`

5. Check File from Windows via SMB  
   - Navigate to `\\powerstore\PSTestShare`
   - Right-click the `test_from_unix.txt` file → Properties → Security
   - Expected result:
     - Owner resolves to domain user `jeet.ad`
   - Problem result:
     - Owner shows as unknown SID

6. Create File from Windows as Same User  
   - Create `test_from_windows.txt` in the SMB share as `jeet.ad`

7. Inspect File on Linux via NFS  
   ```bash
   ls -ln /mnt/nfs/test_from_windows.txt
   ```
   - Expected: `uid=12345` (matching AD `uidNumber`)
   - Problem: UID appears as a large synthetic number like `3000001`, indicating PowerStore could not map the Windows SID to a UID

8. (Optional) Confirm Dynamic UID is Not in AD  
   ```bash
   getent passwd 3000001
   ```
   This should return nothing, confirming it's a dynamically assigned UID from PowerStore
