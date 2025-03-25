# Configure Multi-Protocol PowerStore with LDAP

- [Configure Multi-Protocol PowerStore with LDAP](#configure-multi-protocol-powerstore-with-ldap)
  - [Overview](#overview)
  - [How This Works](#how-this-works)
    - [Some Gotchas](#some-gotchas)
  - [Configure Your Active Directory User](#configure-your-active-directory-user)
  - [Configure a NAS Server](#configure-a-nas-server)
  - [Configure Your Filesystem](#configure-your-filesystem)
  - [Update the LDAP Schema](#update-the-ldap-schema)
  - [Mount the Share and NFS Export](#mount-the-share-and-nfs-export)

## Overview

This article describes how to configure multi-protocol PowerStore for both SMB and NFS using LDAP.

## How This Works

You can skip this if you want, but I found it helpful to get an academic understanding of what to expect is going to happen.

1. PowerStore receives the UID/GID from the NFS client in the request.
2. It checks its Secure Mapping Cache (secmap) to see if it already knows how to map that UID to a Windows SID.
3. If there's no cached mapping, PowerStore attempts to resolve the UID to a username using the configured UDS (Unix Directory Service).
    - UDS is backed by LDAP (e.g., Active Directory with RFC2307 or IDMU schema).
    - It looks for an entry where `uidNumber = <UID>` and `gidNumber = <GID>` in the directory.
4. If it finds a user in LDAP with that UID/GID:
    - It extracts the UNIX username
    - Then matches the UNIX username to a Windows username (same name or using `ntxmap` if they're different)
    - Finally, it maps that to a Windows SID
5. Access is granted or denied based on the resolved user’s permissions.

### Some Gotchas

- You **must** have an LDAP server configured on the SMB filesystem. It is not enough to just configure UDS.
- PowerStore checks the field `uid` for your user and in this case that **must** match the field  samaccountname or the system won't work. I'll explain how to map this later.

## Configure Your Active Directory User

Here I demo on Microsoft Active Directory but the same logic will apply for OpenLDAP. It will just be harder to setup because it is OpenLDAP and OpenLDAP's purpose is to cause pain and suffering.

NFS uses UID / GID to authenticate. The problem is, if you are using Windows users, they natively have neither a UID or a GID. They have a SID. This means if you try to authenticate with a Windows user with NFS, it doesn't actually have a UID or GID for you to use. You can solve this problem in one of three ways:

1. You can enable automatic mapping and PowerStore will just make up a UID/GID for your Windows users
2. You can enable a default account for unmapped users
3. You can do either 1, 2, or neither **and** set a UID or GID for your users. If you don't enable either it will automatically default to enabling a default account. This is what I did. I prefer this because if you do automatic mapping and then change a user's UID/GID later you lose access to all the things they had aside from root because those things will have been created with a random UID/GID.

Whether you use 1 or 2 is controlled under the **Naming Services** tab for your NAS server:

![](images/2025-03-25-13-39-30.png)

I set up a user called `gcurell-adm` and then assigned UID/GID 10001 in active directory:

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

There is one key piece of information you need from this - the **dn**. You will need that later. Notice that my UID and GID number are accurately reflected. If those don't show up you need to fix that first.

## Configure a NAS Server

The first thing you will have to do is configure the NAS server itself. This part is fairly straightforward so below I simply show the screenshots without much explanation.

![](images/2025-03-25-10-35-32.png)

![](images/2025-03-25-10-35-57.png)

![](images/2025-03-25-10-39-21.png)

![](images/2025-03-25-10-40-06.png)

For this next step you will need the **dn** you got at the end of [Configure Your Active Directory User](#configure-your-active-directory-user). In the example I have above it is `CN=Grant Curell -- Admin,OU=Grant_Sales_Team,DC=grantlab,DC=local`. Unix Directory Services (UDS) is the thing that will resolve a UID/GID to a Windows username and subsequently a SID.

![](images/2025-03-25-13-44-05.png)

![](images/2025-03-25-13-46-08.png)

![](images/2025-03-25-13-46-49.png)

The rest I just clicked next to finish. I didn't add a protection policy.

## Configure Your Filesystem

I assume you are already familiar with how to do this. There isn't anything unique for multiprotocol in the initial setup. See [the manual](https://www.dell.com/support/manuals/en-us/powerstore-1000/pwrstr-cfg-smb/create-file-systems-and-smb-shares?guid=guid-de8c3203-3da8-4205-8680-3868acb9f03a&lang=en-us) for details.

After your filesystem is created, there is one special thing you have to do. Under the properties for your filesystem is a setting called access policy:

![](images/2025-03-25-14-03-21.png)

When set to native security, NFS and SMB permissions are completely separated. In my case, I wanted the mapper to rely on the Windows SID so I changed this to Windows Security.

## Update the LDAP Schema

The final step stems from some legacy behavior. Back in the day when unix services were separate in Microsoft, installing them would automatically populate the uid field for a user with the SamAccountName. This no longer happens but the RFC still expects the uid field to be populated. Subsequently, we need to add a mapping in our LDAP configuration to do this automatically. Go to your NAS server, click the naming service tile, and then click UDS.

![](images/2025-03-25-14-17-12.png)

Under the UDS tab, click retrieve current schema and download your LDAP schema. This is what mine looks like by default:

```bash
# -----------------------------------------------------------------------------
# This template was automatically generated by the EMC Nas server
# - Adjustments could be required to fit your specific LDAP configuration.

# - The following setup fits the MS IdMU schema
#   used by Windows Server 2003 R2 or newer (like Windows Server 2008).

# Containers

nss_base_passwd    cn=Users,DC=grantlab,DC=local?one
nss_base_group     cn=Users,DC=grantlab,DC=local?one
nss_base_hosts     cn=Computers,DC=grantlab,DC=local?one
nss_base_netgroup  cn=netgroup,cn=grantlab,cn=DefaultMigrationContainer30,DC=grantlab,DC=local?one
# Objects
nss_map_objectclass  posixAccount    User
nss_map_objectclass  posixGroup      Group
nss_map_objectclass  ipHost          Computer
# Attributes
nss_map_attribute    userPassword    unixUserPassword
nss_map_attribute    homeDirectory   unixHomeDirectory

# The group members are defined in Active Directory by the "member" attribute,
# whose value is a DN, while IDMU expects a "memberUid" attribute whose value
# is an UID (login name).
# If "memberUid" attributes aren't present in the group objects, then you can
# simply remap "memberUid" to "member", and the Data Mover will issue additional
# LDAP queries to get the members UID from the members DN.
# This remapping may impact performances due to the additional LDAP queries it
# involves.

nss_map_attribute memberUid member

# - The parameter fast_search allows fast search encoding to boost performances with big LDAP repositories.
#   The parameter is set to 0 by default on this configuration,#   Some issue could occurs on Microsoft Active Directory server.
#   If you encounter some issue on LDAP lookup, set the value of the parameter to 0
fast_search 0
```

You need to add the line `nss_map_attribute uid SamAccountName` and update `nss_base_passwd` and `nss_base_group` to end with sub instead of one. So the end result is like this:

```bash
# -----------------------------------------------------------------------------
# This template was automatically generated by the EMC Nas server
# - Adjustments could be required to fit your specific LDAP configuration.

# - The following setup fits the MS IdMU schema
#   used by Windows Server 2003 R2 or newer (like Windows Server 2008).

# Containers

nss_base_passwd    DC=grantlab,DC=local?sub
nss_base_group     DC=grantlab,DC=local?sub
nss_base_hosts     cn=Computers,DC=grantlab,DC=local?one
nss_base_netgroup  cn=netgroup,cn=grantlab,cn=DefaultMigrationContainer30,DC=grantlab,DC=local?one

# Objects
nss_map_objectclass  posixAccount    User
nss_map_objectclass  posixGroup      Group
nss_map_objectclass  ipHost          Computer

# Attributes
nss_map_attribute    uid             SamAccountName
nss_map_attribute    userPassword    unixUserPassword
nss_map_attribute    homeDirectory   unixHomeDirectory

# The group members are defined in Active Directory by the "member" attribute,
# whose value is a DN, while IDMU expects a "memberUid" attribute whose value
# is an UID (login name).
# If "memberUid" attributes aren't present in the group objects, then you can
# simply remap "memberUid" to "member", and the Data Mover will issue additional
# LDAP queries to get the members UID from the members DN.
# This remapping may impact performances due to the additional LDAP queries it
# involves.

nss_map_attribute memberUid member

# - The parameter fast_search allows fast search encoding to boost performances with big LDAP repositories.
#   The parameter is set to 0 by default on this configuration.
#   If you encounter some issue on LDAP lookup, set the value of the parameter to 0
fast_search 0
```

**GOTCHA**: PowerStore defaults to assuming your users exist under `cn=Users`. If your users **ARE NOT** under Users, you will need to change this. Notice I also did that for my `nss_base_passwd` and `nss_base_group`. The `sub` keyword makes it so that LDAP will search the entire subdirectory instead of just one level down.

## Mount the Share and NFS Export

Next I hopped back on my Rocky box to test all this out. First we need to create a user that matches what we did in active directory:

```bash
sudo groupadd -g 10001 gcurell_adm
sudo useradd -u 10001 -g 10001 -d /home/gcurell_adm -s /bin/bash gcurell_adm
sudo mkdir -p /mnt/nfs_test
mount -t nfs4 192.168.0.63:/grantexport /mnt/nfs_test
sudo -u gcurell_adm touch /mnt/nfs_test/test.txt
cd nfs_test/
ls -al
total 16
drwxr-xr-x. 5 root        root        8192 Mar 25 14:24 .
drwxr-xr-x. 5 root        root          52 Mar 24 09:33 ..
dr-xr-xr-x. 2 root        bin          152 Mar 25 13:58 .etc
drwxr-xr-x. 2 root        root        8192 Mar 25 13:58 lost+found
-rw-r--r--. 1 gcurell_adm gcurell_adm    0 Mar 25 14:24 test.txt
```

Now you can see that I'm able to write to the share with my active directory user. Moreover, we see that the active directory user correctly owns the files. You can then open that share on SMB and edit or create new files:

![](images/2025-03-25-14-31-58.png)

