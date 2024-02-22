# Swap Kernel on Rocky 9

- [Swap Kernel on Rocky 9](#swap-kernel-on-rocky-9)
  - [Build the Kernel](#build-the-kernel)
  - [Create RPM Package for It](#create-rpm-package-for-it)
  - [Research](#research)
    - [What is vmlinuz](#what-is-vmlinuz)
      - [Where to Find `vmlinuz`](#where-to-find-vmlinuz)
    - [What is the System Map](#what-is-the-system-map)
      - [Purpose and Usage](#purpose-and-usage)
      - [Location](#location)
      - [Security Considerations](#security-considerations)
      - [Updating and Managing](#updating-and-managing)


## Build the Kernel

Pull the Linux kernel from [here](https://www.kernel.org/)

```bash
# Pull in Rocky's existing config
cp -f /boot/config-$(uname -r) .config

# This accepts all the defaults for the new kernel options
yes "" | make -j$(nproc --all) oldconfig
make -j$(nproc)
make -j$(nproc) modules
make -j$(nproc) modules_install
grub2-mkconfig -o /boot/efi/EFI/rocky/grub.cfg
# sudo dnf reinstall grub2-efi-x64 shim-x64
```

**CERTIFICATE ERROR** If you get a certificate error you need to get `rhel.pem` from the kernel source. [Follow these instructions](https://unix.stackexchange.com/a/769359/240147)

**RANDOM ERRORS** I also had some random errors I think were due to race conditions. I just dropped it down to `make -j 10` and it worked.

## Create RPM Package for It

```
sudo dnf install rpm-build redhat-rpm-config make gcc
mkdir -p ~/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
mkdir -p custom-kernel-nvme-6.6.16/
cd custom-kernel-nvme-6.6.16/
cp /boot/vmlinuz-$(uname -r) .
cp /boot/System.map-$(uname -r) .
cp ~/linux-6.6.16/.config config-$(uname -r)
cp -R /lib/modules/$(uname -r) modules
cd ..
mv custom-kernel-distro/ custom-kernel-nvme-6.6.16
tar --use-compress-program=pigz -cvf custom-kernel-nvme-6.6.16.tar.gz custom-kernel-nvme-6.6.16/
mv custom-kernel-nvme-6.6.16.tar.gz rpmbuild/SOURCES/
vim ~/rpmbuild/SPECS/custom-kernel-nvme-6.6.16.spec
```

Paste the following content:

```
Summary: Custom Kernel Package with NVMe Debug Driver
Name: custom-kernel-nvme
Version: 6.6.16
Release: 1
License: GPL
Group: System Environment/Kernel
Source: custom-kernel-nvme-6.6.16.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
This package provides a custom Linux kernel version 6.6.16, specifically built for debugging NVMe.

%prep
%setup -q

%build
# Since we're packaging a precompiled kernel, no build commands are necessary

%install
%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/boot
mkdir -p $RPM_BUILD_ROOT/lib/modules/6.6.16
cp vmlinuz-6.6.16 $RPM_BUILD_ROOT/boot/
cp System.map-6.6.16 $RPM_BUILD_ROOT/boot/
cp config-6.6.16 $RPM_BUILD_ROOT/boot/
cp -a modules/* $RPM_BUILD_ROOT/lib/modules/6.6.16/


%files
/boot/vmlinuz-6.6.16
/boot/System.map-6.6.16
/boot/config-6.6.16
/lib/modules/*

%clean
rm -rf $RPM_BUILD_ROOT

```

## Research

### What is vmlinuz

`vmlinuz` is the name of the Linux kernel executable. It's a compressed, bootable image of the kernel. When the system boots, this is the file loaded by the bootloader (GRUB) into memory to start the Linux operating system. The "vm" in `vmlinuz` stands for Virtual Memory, highlighting the kernel's capability to manage hardware virtual memory. The "linuz" part is a play on Linux, with "z" indicating it's compressed (historically, `z` stood for zlib compression, but modern kernels might use other compression methods like LZMA).

#### Where to Find `vmlinuz`

On Rocky Linux, `vmlinuz` is located in the `/boot` directory. The full path is typically `/boot/vmlinuz-$(uname -r)`, where `$(uname -r)` is replaced with the version of the kernel currently running. For instance, if you're running kernel version 5.11.0, the path would likely be `/boot/vmlinuz-5.11.0`.

When you compile a new kernel from source, the `vmlinuz` file for your new kernel needs to be manually placed in the `/boot` directory (or wherever your distribution expects kernel images) and then referenced in your bootloader's configuration so that it can be loaded at boot time.

### What is the System Map

The System Map, often referred to as `System.map`, is a file generated during the compilation of the Linux kernel. This file maps the memory addresses to the symbol names within the kernel. It's essentially a lookup table that contains the addresses of various functions, variables, and data structures used by the kernel.

#### Purpose and Usage

- **Debugging and Diagnostic Tools**: The System Map is crucial for kernel developers and system administrators for debugging purposes. Tools like `kdump`, `kprobe`, and `SystemTap`, as well as many others, use the System Map to translate memory addresses into human-readable symbol names when analyzing kernel crashes or behavior.
- **Security**: The addresses of kernel symbols can vary between different builds of the kernel due to features like Kernel Address Space Layout Randomization (KASLR), which enhances system security by randomizing the memory address at which kernel code is loaded. However, the System Map can be used to map these addresses to specific functions or variables, making it a sensitive file in terms of system security.
- **Kernel Module Development**: Developers working on kernel modules may refer to the System Map to understand kernel internals, such as function addresses they wish to hook or modify.

#### Location

The System Map file is typically located in the `/boot` directory alongside the kernel it corresponds to. For example, if you're running a kernel version `5.11.0`, you might find it at `/boot/System.map-5.11.0`. The exact path can vary depending on your distribution's configuration.

When installing a new kernel, the corresponding System Map file is also installed to ensure that tools and operations requiring symbol resolution can function correctly with the new kernel.

#### Security Considerations

Given its detailed insight into the kernel's memory layout, the System Map file is considered sensitive. Unauthorized access to this file could potentially help an attacker understand the kernel's structure, making it easier to exploit vulnerabilities. Therefore, access to the System Map is usually restricted to root or users with specific permissions.

#### Updating and Managing

When you compile and install a new kernel, a new System Map file is generated and should be installed in the appropriate location (`/boot`, for most systems). Managing multiple kernels involves keeping the corresponding System Map files organized and correctly named, ensuring that diagnostic tools can automatically find and use the correct System Map file for the currently running kernel.