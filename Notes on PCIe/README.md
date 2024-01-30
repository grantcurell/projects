# Notes on PCIe

- [Notes on PCIe](#notes-on-pcie)
  - [PCIe Basics and Background](#pcie-basics-and-background)
  - [How multiple root complexes are handled](#how-multiple-root-complexes-are-handled)
  - [Interpreting PCIe Device to CPU Locality Information](#interpreting-pcie-device-to-cpu-locality-information)
  - [What is the PCIe PHY](#what-is-the-pcie-phy)
  - [Human readable overview of how PCIe works](#human-readable-overview-of-how-pcie-works)
  - [How does ID-based Ordering (IDO) Work?](#how-does-id-based-ordering-ido-work)
  - [How does transaction ordering work?](#how-does-transaction-ordering-work)
  - [What is a PCIe Root Complex?](#what-is-a-pcie-root-complex)
  - [How does PCIe Enumeration Work?](#how-does-pcie-enumeration-work)
  - [NVMe over PCIe vs Other Protocols](#nvme-over-pcie-vs-other-protocols)
  - [What is a PCIe Function?](#what-is-a-pcie-function)
  - [PCIe-Bus and NUMA Node Correlation](#pcie-bus-and-numa-node-correlation)
  - [How does the root complex work?](#how-does-the-root-complex-work)
  - [What is PCIe P2P?](#what-is-pcie-p2p)
  - [What is Relaxed Ordering](#what-is-relaxed-ordering)
  - [What is a traffic class (TC)?](#what-is-a-traffic-class-tc)
  - [PCIe BAR Register](#pcie-bar-register)
  - [How NVMe Drive Opcodes Work](#how-nvme-drive-opcodes-work)
  - [How does SR-IOV work?](#how-does-sr-iov-work)
  - [PCIe Bridge vs Switch](#pcie-bridge-vs-switch)
  - [PCIe Configuration Space](#pcie-configuration-space)
  - [PCIe Switches](#pcie-switches)
  - [How to Check CPU Affinity](#how-to-check-cpu-affinity)


## PCIe Basics and Background

https://pcisig.com/sites/default/files/files/PCI_Express_Basics_Background.pdf#page=26

## How multiple root complexes are handled

https://codywu2010.wordpress.com/2015/11/29/how-modern-multi-processor-multi-root-complex-system-assigns-pci-bus-number/

## Interpreting PCIe Device to CPU Locality Information

https://dshcherb.github.io/2019/02/02/interpreting-pcie-device-to-cpu-locality-information.html

## What is the PCIe PHY

https://www.linkedin.com/pulse/pci-express-depth-physical-layer-luigi-c-filho-/

## Human readable overview of how PCIe works

http://xillybus.com/tutorials/pci-express-tlp-pcie-primer-tutorial-guide-1/
http://xillybus.com/tutorials/pci-express-tlp-pcie-primer-tutorial-guide-2

## How does ID-based Ordering (IDO) Work?

https://blog.csdn.net/weixin_48180416/article/details/115790068

## How does transaction ordering work?

https://blog.csdn.net/weixin_40357487/article/details/120162461?spm=1001.2101.3001.6661.1&utm_medium=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1.no_search_link&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1.no_search_link&utm_relevant_index=1

## What is a PCIe Root Complex?

https://www.quora.com/What-is-a-PCIe-root-complex?share=1

## How does PCIe Enumeration Work?

https://www.quora.com/What-is-PCIE-enumeration/answer/Satish-Kumar-525?ch=15&oid=31389493&share=44585235&target_type=answer

## NVMe over PCIe vs Other Protocols

https://www.quora.com/Is-NVMe-faster-than-PCIe/answer/Mike-Jones-169?ch=15&oid=193548046&share=a587ff45&target_type=answer

## What is a PCIe Function?

https://www.quora.com/What-is-a-PCIe-function/answer/Udit-Khanna-2?ch=15&oid=58319695&share=c7f066e5&target_type=answer

## PCIe-Bus and NUMA Node Correlation

https://social.msdn.microsoft.com/Forums/en-US/fabb05b7-eb3f-4a7c-91c5-1ced90af3d0c/pciebus-and-numanode-correlation

## How does the root complex work?

https://codywu2010.wordpress.com/2015/11/29/how-modern-multi-processor-multi-root-complex-system-assigns-pci-bus-number/

## What is PCIe P2P?

https://xilinx.github.io/XRT/master/html/p2p.html

## What is Relaxed Ordering

https://qr.ae/pG6SWe

## What is a traffic class (TC)?

https://www.oreilly.com/library/view/pci-express-system/0321156307/0321156307_ch06lev1sec6.html

## PCIe BAR Register

https://github.com/cirosantilli/linux-kernel-module-cheat/blob/366b1c1af269f56d6a7e6464f2862ba2bc368062/kernel_module/pci.c

## How NVMe Drive Opcodes Work

https://stackoverflow.com/questions/30190050/what-is-the-base-address-register-bar-in-pcie
https://stackoverflow.com/questions/19006632/how-is-a-pci-pcie-bar-size-determined

- BIOS/OS discovers whether PCIe device exists
- Places the addresses for mmio or I/O port addresses in NVMe drive​'s BAR registers (which it figures out from the configuration registers)
- It seems from the documentation I found NVMe does this through 64bit mmio
- Driver establishes the admin queue via BAR0. The admin queue's base addresses are in ASQ and ACQ respectively
- I submit commands to the admin submission queue to establish I/O queues.
- Send/receive data via I/O queues.

## How does SR-IOV work?

https://docs.microsoft.com/en-us/windows-hardware/drivers/network/overview-of-single-root-i-o-virtualization--sr-iov-

Architecture: https://docs.microsoft.com/en-us/windows-hardware/drivers/network/sr-iov-architecture

## PCIe Bridge vs Switch
wke...@gmail.com wrote:
> I would appreciate of someone can explain the difference between
> a PCI bridge and a PCI switch.

With good ol' PCI, a single bus can have many devices. A PCI bridge
is a device that connects multiple buses together, which is something
that was very seldom needed.

PCI Express looks, for software, very similar to PCI, but is electrically
a point-to-point connection, i.e., a PCIe bus has exactly two devices.

To connect PCIe with PCI, you need a PCI/PCIe or PCIe/PCI bridge.

If you have a single PCIe connector and multiple PCIe devices, you need
a PCIe switch. A single PCIe connection still is between exactly two
devices, so a PCIe switch consists of a (virtual) PCI bridge for the
upstream PCIe connection, and one (virtual) PCI bridge for each
downstream PCIe connection.


Regards,
Clemens

## PCIe Configuration Space

https://docs.oracle.com/cd/E19683-01/806-5222/hwovr-22/#:~:text=The%20PCI%20host%20bridge%20provides,of%20other%20PCI%20bus%20masters.

https://bitwiseanne.wordpress.com/2020/05/15/pcie-101-the-root-complex-and-the-endpoint/

## PCIe Switches

https://linuxhint.com/pcie-switch/#:~:text=PCIe%20switches%20are%20devices%20that,the%20CPU%20alone%20can%20handle.

## How to Check CPU Affinity

```
[root@r7525 ~]# cat /sys/class/pci_bus/0000\:00/cpulistaffinity
24-31,88-95
[root@r7525 ~]# lscpu | grep -i numa
NUMA node(s):        8
NUMA node0 CPU(s):   0-7,64-71
NUMA node1 CPU(s):   8-15,72-79
NUMA node2 CPU(s):   16-23,80-87
NUMA node3 CPU(s):   24-31,88-95
NUMA node4 CPU(s):   32-39,96-103
NUMA node5 CPU(s):   40-47,104-111
NUMA node6 CPU(s):   48-55,112-119
NUMA node7 CPU(s):   56-63,120-127
```
You can check the CPU affinity of a PCIe bus and then see what processor it is aligned to by referencing the processor ranges.