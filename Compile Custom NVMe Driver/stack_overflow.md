I ultmiately want to compile a modified NVMe driver on Rocky, but currently am working on compiling the existing NVMe driver as is to test. I am able to successfully compile the driver. I'm trying to make the version magic match between the original driver and my current driver but haven't been successful.

## How I'm Compiling

Get the correct source:

```bash
dnf install -y kernel-headers ncurses-devel
dnf download --source kernel
rpm2cpio kernel-5.14.0-362.18.1.el9_3.src.rpm | cpio -idmv
tar -xf linux-5.14.0-362.18.1.el9_3.tar.xz
```

Get `Module.symvers` file from the kernel headers directory

`cp /usr/src/kernels/5.14.0-362.18.1.el9_3.x86_64/Module.symvers <current_dir>`

Make it. In the menuconfig I have simplified it to just this:

[![enter image description here][1]][1]

```bash
make menuconfig
make clean
make -j$(nproc --all) modules_prepare
make -j$(nproc --all) oldconfig && make -j$(nproc --all) prepare
make ARCH=x86_64 -j$(nproc --all) M=drivers/nvme
```

## Version Magic Strings

But when I check version magic they're still different and I don't understand why:

```
[root@nvmetest linux-5.14.0-362.18.1.el9_3]# !mod
modinfo ./drivers/nvme/host/nvme-core.ko
filename:       /root/new_driver/linux-5.14.0-362.18.1.el9_3/./drivers/nvme/host/nvme-core.ko
version:        1.0
license:        GPL
rhelversion:    9.3
srcversion:     A869617A5E58420845515F4
depends:        t10-pi
retpoline:      Y
name:           nvme_core
vermagic:       5.14.0 SMP preempt mod_unload modversions
parm:           multipath:turn on native support for multiple controllers per subsystem (bool)
parm:           iopolicy:Default multipath I/O policy; 'numa' (default) or 'round-robin'
parm:           admin_timeout:timeout in seconds for admin commands (uint)
parm:           io_timeout:timeout in seconds for I/O (uint)
parm:           shutdown_timeout:timeout in seconds for controller shutdown (byte)
parm:           max_retries:max number of retries a command may have (byte)
parm:           default_ps_max_latency_us:max power saving latency for new devices; use PM QOS to change per device (ulong)
parm:           force_apst:allow APST for newly enumerated devices even if quirked off (bool)
parm:           apst_primary_timeout_ms:primary APST timeout in ms (ulong)
parm:           apst_secondary_timeout_ms:secondary APST timeout in ms (ulong)
parm:           apst_primary_latency_tol_us:primary APST latency tolerance in us (ulong)
parm:           apst_secondary_latency_tol_us:secondary APST latency tolerance in us (ulong)
[root@nvmetest linux-5.14.0-362.18.1.el9_3]# modinfo /lib/modules/5.14.0-362.18.1.el9_3.x86_64/kernel/drivers/nvme/host/nvme-core.ko.xz
filename:       /lib/modules/5.14.0-362.18.1.el9_3.x86_64/kernel/drivers/nvme/host/nvme-core.ko.xz
version:        1.0
license:        GPL
rhelversion:    9.3
srcversion:     ADFE53FFFB5D30ECFF130B0
depends:        nvme-common,t10-pi
retpoline:      Y
intree:         Y
name:           nvme_core
vermagic:       5.14.0-362.18.1.el9_3.x86_64 SMP preempt mod_unload modversions
sig_id:         PKCS#7
signer:         Rocky kernel signing key
sig_key:        37:B0:46:2C:D4:62:CB:E7:6C:CA:AE:9F:2A:A2:BE:E1:36:3A:8A:AF
sig_hashalgo:   sha256
signature:      60:89:BA:1D:1C:71:38:82:DF:09:73:B4:23:3E:C8:FE:7B:E4:9F:0D:
                62:6E:28:D7:3E:5A:5E:11:CD:7B:D2:52:E2:C6:ED:5E:B6:A7:19:54:
                8A:FB:BB:E8:2D:A5:77:3F:A1:C1:7E:EB:45:74:30:E9:18:1C:3D:9A:
                53:4A:2B:B0:1E:F0:35:D3:D1:E5:B6:A5:D0:47:6C:2F:B7:C6:6F:00:
                30:0E:82:BA:FD:4F:9D:0E:3B:4A:17:A4:1B:E8:31:FC:FB:BC:C2:93:
                1C:6D:5E:94:FD:DE:65:3B:3E:0B:F4:B4:B0:82:67:87:8C:90:C9:74:
                44:BB:14:D9:F9:43:33:CC:CC:77:29:11:2C:3D:79:30:EA:B3:63:74:
                F3:02:F0:DA:68:40:BA:65:B0:E5:D8:90:FF:B0:CA:8D:D7:31:00:47:
                FE:9C:B9:17:8F:81:1D:7F:45:F6:98:E8:14:1F:73:99:00:51:18:48:
                1F:29:98:F4:37:FA:62:46:FF:1B:64:B5:1F:03:C3:5C:87:2E:13:9E:
                EE:8C:32:DE:D8:B6:3F:1D:C2:69:45:46:E2:8B:E4:BD:C2:7C:00:14:
                3F:7B:76:C8:43:4E:ED:24:BE:C8:9D:85:16:C6:9B:55:1F:BA:7B:39:
                07:57:A7:46:1A:E4:98:D5:29:C9:27:07:0B:3A:FE:6D:49:4B:DD:24:
                E0:4C:99:C1:C4:88:4D:E1:D9:78:EC:46:4F:D6:94:D6:93:B0:D4:24:
                23:08:40:35:F9:41:0D:1E:4A:78:3C:B2:A9:DB:51:C9:D0:96:F5:64:
                43:7E:FF:69:71:09:06:9D:79:B0:56:A0:49:71:69:64:3D:50:B6:0B:
                DE:A0:FA:36:D7:86:AD:B9:2A:8C:11:B5:73:F3:C5:2B:C5:2F:C2:A6:
                AB:7F:01:B1:E6:60:8F:6A:F0:A1:AE:A9:32:E1:30:DA:4D:7A:98:F5:
                89:F7:7B:4D:FF:23:4B:77:29:BA:62:1B:54:09:1F:33:57:8F:44:A3:
                FE:19:D6:43
parm:           multipath:turn on native support for multiple controllers per subsystem (bool)
parm:           iopolicy:Default multipath I/O policy; 'numa' (default) or 'round-robin'
parm:           admin_timeout:timeout in seconds for admin commands (uint)
parm:           io_timeout:timeout in seconds for I/O (uint)
parm:           shutdown_timeout:timeout in seconds for controller shutdown (byte)
parm:           max_retries:max number of retries a command may have (byte)
parm:           default_ps_max_latency_us:max power saving latency for new devices; use PM QOS to change per device (ulong)
parm:           force_apst:allow APST for newly enumerated devices even if quirked off (bool)
parm:           apst_primary_timeout_ms:primary APST timeout in ms (ulong)
parm:           apst_secondary_timeout_ms:secondary APST timeout in ms (ulong)
parm:           apst_primary_latency_tol_us:primary APST latency tolerance in us (ulong)
parm:           apst_secondary_latency_tol_us:secondary APST latency tolerance in us (ulong)
[root@nvmetest linux-5.14.0-362.18.1.el9_3]#
```

## Using .config From Boot

I have also tried using the config from /boot with `cp /boot/config-$(uname -r) .config` but the results are the same.

It's not clear to me what I need to change to get that to match.

  [1]: https://i.stack.imgur.com/xXfMb.png