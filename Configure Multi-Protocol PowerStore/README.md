# Configure Multi-Protocol PowerStore

- [Configure Multi-Protocol PowerStore](#configure-multi-protocol-powerstore)
  - [Overview](#overview)
  - [Configure Your Active Directory User](#configure-your-active-directory-user)
  - [Configure a NAS Server](#configure-a-nas-server)
  - [Problem Summary](#problem-summary)
  - [Steps to Replicate](#steps-to-replicate)
  - [My Replication](#my-replication)
  - [Bug/Problem/Stuck](#bugproblemstuck)
  - [Output](#output)
  - [Notes](#notes)
  - [Things He Did](#things-he-did)
    - [Logs](#logs)

## Overview

This article describes how to configure multi-protocol PowerStore for both SMB and NFS.

## Configure Your Active Directory User

Here I demo on Microsoft Active Directory but the same logic will apply for OpenLDAP. It will just be harder to setup because it is OpenLDAP and OpenLDAP's purpose is to cause pain and suffering.



## Configure a NAS Server

The first thing you will have to do is configure the NAS server itself. This part is fairly straightforward so below I simply show the screenshots without much explanation.

![](images/2025-03-25-10-35-32.png)

![](images/2025-03-25-10-35-57.png)

![](images/2025-03-25-10-39-21.png)

![](images/2025-03-25-10-40-06.png)

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

## My Replication

I set up a user called `gcurell-adm` and then assigned UID/GID 10001

![](images/2025-03-21-15-52-27.png)

![](images/2025-03-21-15-52-52.png)

After that, I had a Rocky test box from which I wanted to test all the creds.

```bash
sudo dnf install -y openldap-clients
```

We can confirm from our Rocky box that the UID/GID are correct:

```bash
[root@rocky ~]# ldapsearch -x -H ldap://domaincontroller.grantlab.local \
  -D "gcurell_adm@grantlab.local" -W \
  -b "dc=grantlab,dc=local" \
  "(sAMAccountName=gcurell_adm)" \
  uidNumber gidNumber unixHomeDirectory loginShell
Enter LDAP Password:
# extended LDIF
#
# LDAPv3
# base <dc=grantlab,dc=local> with scope subtree
# filter: (sAMAccountName=gcurell_adm)
# requesting: uidNumber gidNumber unixHomeDirectory loginShell
#

# Grant Curell -- Admin, Grant_Sales_Team, grantlab.local
dn: CN=Grant Curell -- Admin,OU=Grant_Sales_Team,DC=grantlab,DC=local
uidNumber: 10001
gidNumber: 10001
unixHomeDirectory: /home/grant_adm
loginShell: /bin/bash

# search reference
ref: ldap://DomainDnsZones.grantlab.local/DC=DomainDnsZones,DC=grantlab,DC=local

# search reference
ref: ldap://ForestDnsZones.grantlab.local/DC=ForestDnsZones,DC=grantlab,DC=local

# search reference
ref: ldap://grantlab.local/CN=Configuration,DC=grantlab,DC=local

# search result
search: 2
result: 0 Success

# numResponses: 5
# numEntries: 1
# numReferences: 3
```

Now we want to set up a user on our Rocky box that matches that:

```bash
sudo groupadd -g 10001 gcurell_adm
sudo useradd -u 10001 -g 10001 -d /home/gcurell_adm -s /bin/bash gcurell_adm
sudo mkdir -p /mnt/nfs_test
sudo mount -t nfs 192.168.0.62:/PSNFS01 /mnt/nfs_test
```

Now that we have the mount setup, run the test:

```bash
# Try to create a file as gcurell_adm
[root@rocky ~]# sudo -u gcurell_adm touch /mnt/nfs_test/from_nfs.txt
touch: cannot touch '/mnt/nfs_test/from_nfs.txt': Permission denied

# Try to create a file as root
[gcurell_adm@rocky nfs_test]$ touch ultra_test
touch: cannot touch 'ultra_test': Permission denied
```

We're getting this permission denied error because I am currently using the windows security policy for my share:

![](images/2025-03-24-09-57-03.png)

This means that PowerStore must map Linux usernames to UIDs which then get mapped to SIDs. This is explained in detail [here](https://infohub.delltechnologies.com/nl-nl/l/dell-powerstore-file-capabilities-1/user-mapping-13/#:~:text=NFS%20users%20have%20a%20UID,enforced%20(Windows%20Access%20Policy).). However, we haven't configured a UNIX Directory Service (UDS) so right now PowerStore has no way to perform this mapping.

We need to [configure our NAS server to use LDAP](https://www.dell.com/support/manuals/en-us/powerstore-9000t/pwrstr-cfg-nfs/configure-a-nas-server-unix-directory-service-using-ldap?guid=guid-3525a724-af93-4df4-9ba5-1fcedcf0f82e&lang=en-us).

![](images/2025-03-24-10-06-18.png)



## Bug/Problem/Stuck

Note from Grant - even after doing all that, I still get:

```
[root@rocky nfs_test]# sudo -u gcurell_adm touch /mnt/nfs_test/test_fallback.txt                                                               touch: cannot touch '/mnt/nfs_test/test_fallback.txt': Permission denied
[root@rocky nfs_test]# cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
---SNIP---
gcurell_adm:x:10001:10001::/home/gcurell_adm:/bin/bash
```



## Output

```
[SVC:root@4XZBTZ3-A user]$ svc_nas_cifssupport --server NAS01 --args="-checkup -full"

NAS01 :

------------------------------------Checks--------------------------------------


Component SMB :

ACL       : Checking the number of ACLs per file system. ........................ Pass
Connection: Checking the load of SMB TCP connections. ........................... Pass
Credential: Checking the validity of credentials. ............................... Pass
DC        : Checking the connectivity and configuration of Domain Controllers. .. Pass
DFS       : DFS check in svc_nas service script is deprecated. .................. Pass
DNS       : Checking the DNS configuration and connectivity to DNS servers. ..... Pass
EventLog  : Checking the configuration of Windows Event Logs. ................... FAILURE
GPO       : Checking the GPO configuration. ..................................... Pass
HomeDir   : Checking the configuration of home directory shares. ................ Pass
I18N      : Checking the I18N mode and the Unicode/UTF8 translation tables. ..... Pass
Kerberos  : Checking password updates and AES for Kerberos. ..................... Pass
LDAP      : Checking the LDAP configuration. .................................... Pass
LocalGrp  : Checking the database configuration of local groups. ................ Pass
NIS       : Checking the connectivity to the NIS servers. ....................... Pass
Ntxmap    : Checking the ntxmap configuration file. ............................. Pass
Secmap    : Checking the SECMAP database. ....................................... Pass
Security  : Checking the SMB security settings. ................................. Pass
Server    : Checking the SMB file servers configuration. ........................ Pass
Share     : Checking the network shares database. ............................... Pass
SmbList   : Checking the range availability of SMB IDs. ......................... Pass
Threads   : Checking for SMB blocked threads. ................................... Pass
UnsupOS   : Checking for unsupported client network operating systems. .......... Pass
UnsupProto: Checking for unsupported client network protocols. .................. Pass
VC        : Checking the configuration of Virus Checker servers. ................ Pass
VDM       : Checking the NAS server configuration. .............................. Pass
WINS      : Checking the connectivity to WINS servers. .......................... FAILURE
--------------------------------------------------------------------------------

-----------------------------SMB : EventLog Warnings----------------------------

Warning 17456169068: NAS01 :  A new value for the maximum size of the 'application' event log of the NAS server has been defined. This value is not yet effective.
--> On the Windows host, start the Microsoft event viewer. Connect to a SMB server of this NAS server and clear the corresponding event logs.

-------------------------------SMB : WINS Warnings------------------------------

Warning 17451974758: NAS01 :  The NetBIOS server 'AJPS01' does not have any WINS server in its configuration. The SMB clients might not be able to access the SMB server.
--> WINS not supported by NAS.

--------------------------------------------------------------------------------

Total :   2 warnings
*** WARNING *** service shell activated! *** WARNING ***
[SVC:root@4XZBTZ3-A user]$
*** WARNING *** service shell activated! *** WARNING ***
[SVC:root@4XZBTZ3-A user]$
```

## Notes

There are two physically separate controller nodes

SVDM node A and node 2 are the controller VMs. Node 1 is on controller A and node 2 is on controller 2. SVDM is a witness. You can use the IPv6 address to figure what VDM (Virtual Data Mover). NAS01 is running the NAS

![](images/2025-03-24-13-07-07.png)

## Things He Did

`svc_cifssupport NAS01 -secmap -list`

- Why can we do standalone SMB if it won't work without domain joined on the SMB side.
- What is the point of UDS if I have to set up SMB?
- How are you supposed to know that you have to add `nss_map_attribute uid SamAccountName`
- Why does it clear my input on the UDS screen
- DNS wasn't configured so this just stays grayed out, but makes no mention of why.

![](images/2025-03-24-17-25-53.png)

it does show it here:

![](images/2025-03-24-17-26-42.png)

but no one looks there

- When you have automatic UID/GID creation enabled even after you update the uid/gid, it doesn't update secmap. You have to go in and manually delete the secmap mappings.
- 

### Logs

`svc_nas NAS01

![](images/2025-03-24-13-10-14.png)

`svc_nas -ldap`

![](images/2025-03-24-17-35-59.png)

![](images/2025-03-24-17-36-13.png)

![](images/2025-03-24-17-37-20.png)

![](images/2025-03-24-17-37-34.png)