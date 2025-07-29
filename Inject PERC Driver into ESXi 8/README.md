# Injecting `dellshar.v00` PERC Driver into ESXi 8.0 Installer ISO for Dell VRTX

This guide explains how to inject the `dellshar.v00` driver—extracted from a working ESXi 7.0.3 system—into the ESXi 8.0 installer ISO. This enables installation on a Dell VRTX system where the default ESXi 8 installer does not recognize the PERC RAID controller.

## Prerequisites

* A Linux system with `7z`, `tar`, and `mkisofs` or `genisoimage` installed
* Official ESXi 8.0 ISO
* Access to a working ESXi 7.0.3 system with Dell’s Addon
* SCP access to both systems (or alternative file transfer mechanism)

## 1. Extract the driver from an ESXi 7.0.3 host

From the working ESXi 7.0.3 host:

```bash
scp root@esxi7-host:/bootbank/dellshar.v00 .
```

This copies the required PERC driver file from the working system.

## 2. Extract the contents of the ESXi 8 ISO

```bash
mkdir -p ~/esxi8-vrtx/iso
cd ~/esxi8-vrtx
7z x /path/to/VMware-VMvisor-Installer-8.x.x-xxxxxx.x86_64.iso -oiso
```

The ISO contents will now be extracted into `~/esxi8-vrtx/iso`.

## 3. Copy the driver into the ISO structure

```bash
cp dellshar.v00 iso/
```

This places the driver module in the root of the installer where it can be loaded at boot time.

## 4. Modify `boot.cfg` to load the driver

Edit the boot configuration file:

```bash
nano iso/boot.cfg
```

Locate the `modules=` line. Insert `--- dellshar.v00` between `s.v00` and `bnxtnet.v00`:

Before:

```
modules=--- s.v00 --- bnxtnet.v00 --- ...
```

After:

```
modules=--- s.v00 --- dellshar.v00 --- bnxtnet.v00 --- ...
```

Save and close the file.

## 5. Rebuild the custom ESXi 8 ISO

```bash
cd iso
mkisofs -relaxed-filenames -J -R -o ../ESXi-8.0-VRTX.iso \
-b isolinux.bin -c boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table .
```

The rebuilt installer ISO will be saved as `~/esxi8-vrtx/ESXi-8.0-VRTX.iso`.

## 6. Install ESXi 8 using the modified ISO

* Write the ISO to a USB drive or mount it using iDRAC
* Boot the Dell VRTX host from the ISO
* Proceed with the installation. The storage should now be detected correctly

## 7. Verify the driver is loaded (optional)

After booting into ESXi, access the shell and run:

```bash
vmkload_mod -l | grep dell
```

You should see the module associated with `dellshar.v00` loaded into the kernel.
