# BIOS Settings

- [BIOS Settings](#bios-settings)
  - [Equipment Used](#equipment-used)
  - [Memory Settings](#memory-settings)
    - [Helpful Resources](#helpful-resources)
    - [Dram Refresh Delay](#dram-refresh-delay)
      - [How DRAM is Organized](#how-dram-is-organized)
      - [What is a DRAM Refresh](#what-is-a-dram-refresh)
      - [tRFC and recovery time](#trfc-and-recovery-time)
      - [Refresh Penalty](#refresh-penalty)
      - [Setting Explanation](#setting-explanation)
      - [Performance Tuning Recommendation](#performance-tuning-recommendation)
    - [Memory Operating Mode](#memory-operating-mode)
    - [Memory Interleaving](#memory-interleaving)
      - [What is Memory Interleaving](#what-is-memory-interleaving)
      - [Interleaving on AMD vs Intel](#interleaving-on-amd-vs-intel)
      - [Optimizing AMD](#optimizing-amd)
      - [When would one value of Memory Interleave Size be chosen versus another?](#when-would-one-value-of-memory-interleave-size-be-chosen-versus-another)
    - [Correctable Memory ECC SMI](#correctable-memory-ecc-smi)
      - [Performance Tuning Recommendation](#performance-tuning-recommendation-1)
    - [Correctable Error Logging](#correctable-error-logging)
      - [Performance Tuning Recommendation](#performance-tuning-recommendation-2)
    - [Opportunistic Self Refresh](#opportunistic-self-refresh)
    - [DIMM Self Healing (Post Package Repair) on Uncorrectable Memory Error](#dimm-self-healing-post-package-repair-on-uncorrectable-memory-error)
      - [Performance Tuning Recommendation](#performance-tuning-recommendation-3)
  - [Processor Settings](#processor-settings)
    - [Logical Processor](#logical-processor)
    - [IOMMU Support](#iommu-support)
    - [Kernel DMA Protection](#kernel-dma-protection)
    - [Prefetching](#prefetching)
      - [Understanding Prefetching Performance Implications](#understanding-prefetching-performance-implications)
    - [MADT Core Enumeration](#madt-core-enumeration)


## Equipment Used

This guide was written for an R7525 with a Milan processor.

## Memory Settings

### Helpful Resources

- A useful explanation of the different types of memory supported on PowerEdge is available [here](https://www.dell.com/support/kbdoc/en-us/000135681/supported-memory-configuration-guide-for-poweredge-servers)
- For each PowerEdge server, you can find a description of the memory layout in the System Memory section of the service manual. For example, [this is the R7525's layout](https://www.dell.com/support/manuals/en-us/poweredge-r7525/r7525_ism_pub/system-memory-guidelines?guid=guid-8665c17a-2613-45b2-9204-c02a89225024&lang=en-us).
- [This paper on error correction](resources/pdfs/common_dellemc_poweredge_yx4x_memoryras_v1_0.pdf) by Jordan Chin, Co-Chair of the CXL Memory Systems Workgroup and memory engineering specialist at Dell

### Dram Refresh Delay

This setting exists due to the [Row Hammer](https://en.wikipedia.org/wiki/Row_hammer) attack. To fully understand the explanation, it is important to first understand some memory concepts.

#### How DRAM is Organized

[This Stack Exchange post](https://electronics.stackexchange.com/a/454717/279031) does a good job explaining the difference between a DRAM rank and channel. [Page 3 of this lecture](https://my.eng.utah.edu/~cs7810/pres/11-7810-12.pdf) from the University of Utah provides a visual of DRAM organization.

#### What is a DRAM Refresh

Source: https://utaharch.blogspot.com/2013/11/a-dram-refresh-tutorial.html

> The charge on a DRAM cell weakens over time.  The DDR standard requires every cell to be refreshed within a 64 ms interval, referred to as the retention time.  At temperatures higher than 85° C (referred to as extended temperature range), the retention time is halved to 32 ms to account for the higher leakage rate.  The refresh of a memory rank is partitioned into 8,192 smaller refresh operations.  One such refresh operation has to be issued every 7.8 µs (64 ms/8192).  This 7.8 µs interval is referred to as the refresh interval, tREFI.  The DDR3 standard requires that eight refresh operations be issued within a time window equal to 8 x tREFI, giving the memory controller some flexibility when scheduling these refresh operations.  Refresh operations are issued at rank granularity in DDR3 and DDR4.  Before issuing a refresh operation, the memory controller precharges all banks in the rank.  It then issues a single refresh command to the rank.  DRAM chips maintain a row counter to keep track of the last row that was refreshed -- this row counter is used to determine the rows that must be refreshed next.

#### tRFC and recovery time

Source: https://utaharch.blogspot.com/2013/11/a-dram-refresh-tutorial.html

> Upon receiving a refresh command, the DRAM chips enter a refresh mode that has been carefully designed to perform the maximum amount of cell refresh in as little time as possible.  During this time, the current carrying capabilities of the power delivery network and the charge pumps are stretched to the limit.  The operation lasts for a time referred to as the refresh cycle time, tRFC.  Towards the end of this period, the refresh process starts to wind down and some recovery time is provisioned so that the banks can be precharged and charge is restored to the charge pumps.  Providing this recovery time at the end allows the memory controller to resume normal operation at the end of tRFC.  Without this recovery time, the memory controller would require a new set of timing constraints that allow it to gradually ramp up its operations in parallel with charge pump restoration.  Since such complexity can't be expected of every memory controller, the DDR standards include the recovery time in the tRFC specification.  As soon as the tRFC time elapses, the memory controller can issue four consecutive Activate commands to different banks in the rank.

#### Refresh Penalty

Source: https://utaharch.blogspot.com/2013/11/a-dram-refresh-tutorial.html

> On average, in every tREFI window, the rank is unavailable for a time equal to tRFC.  So for a memory-bound application on a 1-rank memory system, the percentage of execution time that can be attributed to refresh (the refresh penalty) is tRFC/tREFI.  In reality, the refresh penalty can be a little higher because directly prior to the refresh operation, the memory controller wastes some time precharging all the banks.  Also, right after the refresh operation, since all rows are closed, the memory controller has to issue a few Activates to re-populate the row buffers.  These added delays can grow the refresh penalty from (say) 8% in a 32 Gb chip to 9%.  The refresh penalty can also be lower than the tRFC/tREFI ratio if the processors can continue to execute independent instructions in their reorder buffers while the memory system is unavailable.  In a multi-rank memory system, the refresh penalty depends on whether ranks are refreshed together or in a staggered manner.  If ranks are refreshed together, the refresh penalty, as above, is in the neighborhood of tRFC/tREFI.  If ranks are refreshed in a staggered manner, the refresh penalty can be greater.  Staggered refresh is frequently employed because it reduces the memory's peak power requirement.

#### Setting Explanation

Every time a row in DRAM is refreshed, it ‘wipes the slate clean’ in terms of Rowhammer induced electrical disturbances. However, when a DRAM row is being refreshed, it cannot be accessed to read/write data – so it is momentarily offline. The JEDEC specification for DDR4 and DDR5 allows the CPU memory controller to postpone sending DRAM refreshes. The memory controller is required to ‘catch up’ in refreshes at a later time. The theory is that some workloads may see additional performance benefits by ‘squeezing in’ read/write transactions during the window where refreshes is not occurring.

In this timing diagram below, you can see there is a window where refresh is postponed (and later caught-up by sending a burst of refreshes). The theory on RH mitigation is that the window you see below allows a ‘window of opportunity’ for Row Hammer attackers to induce bitflips. ‘Performance mode’ of the Dram Refresh Delay setting allows the memory controller to do this postponing.

![](images/2022-12-01-06-00-44.png)
 
By changing the BIOS setting mentioned, it forces the memory controller to send refreshes at regular intervals. Therefore, the ‘window of opportunity’ closes.

![](images/2022-12-01-06-01-28.png)

Dell's testing has showed that there is <1% performance benefit to allowing refresh postponed. Subsequently, starting in 15G, Dell started disabling refresh postponing/delay by default.

#### Performance Tuning Recommendation

From a performance tuning standpoint, our experience shows us that this setting is not significant and can be left at the "Minimum" setting.

### Memory Operating Mode

> This field selects the memory operating mode. This feature is active only if a valid memory configuration is detected. When Optimizer Mode is enabled, the DRAM controllers operate independently in 64-bit mode and provide optimized memory performance.

On AMD platforms this memory setting is not applicable. On Intel platforms the memory operating mode field allows you to enable memory mirroring, fault resilient memory (FRM) mode, or use memory sparing. These features aren't currently on AMD platform but the setting is still present in the BIOS (though locked).

### Memory Interleaving

#### What is Memory Interleaving

The memory interleave size is the amount of data written/read to a single memory channel before the CPU moves to the next channel.  This is done through memory addressing, so that addresses are mapped to certain channels based on the setting.  If you wrote a 1K byte block with the interleave size set to 256 bytes, that data would be spread across 4 difference memory channels/DIMMs.  If you had the setting at 2K bytes, that data would all end up on a single DIMM.

#### Interleaving on AMD vs Intel

In current gen processors, at time of writing Dell 15G Milan (AMD)/Icelake (Intel), there is a significant difference between AMD and Intel. AMD includes a setting called [NUMAs Per Core (NPS)](resources/pdfs/56338_1.00_pub.pdf) which affects interleaving. When NPS is anything more than 1 instead of distributing each increment of the interleave size across different channels it will move between each of the NUMA nodes and channels.

NPS is not a consideration on Intel servers.

#### Optimizing AMD

[AMD's Guidelines on Memory Population](resources/pdfs/56873_0.80_PUB.pdf)

If you are looking to maximize performance, first it is key to populate all 16 DIMMs. AMD processors each have 8 channels and each channel may contain two DIMMs. You can think of interleaving as a sort of load balancing and as with most load balancing scenarios the more you spread the load the faster it goes. Subsequently, if you're looking for maximum performance here having 16 DIMMs is optimum. Equally important is making sure that all memory is the same size.

An exhaustive list of the memory configurations are available in [the guidelines](resources/pdfs/56873_0.80_PUB.pdf). 

#### When would one value of Memory Interleave Size be chosen versus another? 

In general, you should leave the memory interleave size at 256 bytes.  We don’t know of any real-world workloads where it makes a significant difference.

TODO: If you knew that the data read woud be consistently large is this worth exploring?

You could see a difference in synthetic workloads that only use a small address range for their testing. For example, if only 1K of data is accessed you would be MUCH better off with the 256 byte interleaving than the 2K setting in the example above.

### Correctable Memory ECC SMI

Allows the system to log ECC corrected DRAM errors into the System Event Log (SEL) log. Logging these rare errors can help identify marginal components; however the system will pause for a few milliseconds after an error while the log entry is created. Latency conscious customers may wish to disable the feature. Spare Mode, and Mirror mode require this feature to be enabled.

#### Performance Tuning Recommendation

This is a judgement call: if strictly improving performance is your only aim we suggest disabling it though the performance improvements are not substantial. Keeping it enabled will, as the description mentions, allow you to notice if a DIMM is going bad.

### Correctable Error Logging

Some correctable errors in modern RAM are unavoidable. See [page 3 of this paper](./resources/pdfs/common_dellemc_poweredge_yx4x_memoryras_v1_0.pdf). 

> Correctable errors are errors that can be detected and corrected by the server platform. These are typically single-bit errors, though based on CPU and memory configuration, may also be some types of multi-bit errors (corrected by Advanced ECC). Correctable errors can be caused by both soft and hard errors and will not disrupt operation of PowerEdge servers.
> As DRAM based memory shrinks in geometry to grow in capacity, an increasing number of correctable errors are expected to occur as a natural part of uniform scaling. Additionally, due to various other DRAM scaling factors (e.g. decreasing cell capacitance) there is an expected increase in the number of error generating phenomenon such as Variable Retention Time (VRT) [1] and Random Telegraph Noise (RTN) [2].
> Within the server industry, it is an increasingly accepted understanding shared by Dell that some correctable errors per DIMM is unavoidable and does not inherently warrant  4 Memory Errors and Dell PowerEdge YX4X Server Memory RAS Features a memory module replacement. However, some server competitors will go as far as to say that an indefinite number of correctable errors are acceptable – a belief that is not shared by Dell Engineering. Instead, PowerEdge server firmware will intelligently monitor the health of memory and recommend self-healing action or module replacement based on a variety of factors including DIMM capacity, rates of correctable errors, and effectiveness of available self-healing. The intent behind Dell’s proprietary predictive failure algorithms is to proactively identify DIMMs that are most likely to continue to degrade and potentially generate uncorrectable errors. 

In previous generation servers we would log any and all errors generated by the RAM which would lead to a ["self-healing" event](https://www.dell.com/support/kbdoc/en-us/000053203/what-is-ddr4-self-healing-on-dell-poweredge-servers-with-intel-xeon-scalable-processors). These events would trigger memory retraining on reboot, often unnecessarily. This setting allows you to force enable logging for these errors.

#### Performance Tuning Recommendation

Leave this to disabled.

### Opportunistic Self Refresh

Only applies to Intel. Can be ignored on AMD servers and on newer servers should not be present at all.

### DIMM Self Healing (Post Package Repair) on Uncorrectable Memory Error

This description was taken from [page 12 of this paper](./resources/pdfs/common_dellemc_poweredge_yx4x_memoryras_v1_0.pdf).

Post Package Repair (PPR) is an industry-standard capability, defined by JEDEC, where a memory module is capable of swapping out degraded rows of memory with spare ones being held in reserve. While JEDEC requires that all DDR4 memory be built with at least one spare row per DRAM bank group, Dell requires all memory suppliers manufacture genuine Dell DIMMs with a significantly larger number of available spare rows. This is done to ensure that PowerEdge servers have a robust self-healing memory ecosystem.

When the server platform determines that a DRAM row has one or more faulty cells, it can instruct the DRAM to electrically swap out the old row and replace it with a new one. This happens through electrical fusing and is a permanent process. Additionally, the PPR process can only occur at the beginning of a boot process – before memory training and test can occur. Similar to Memory Page Retirement, deeming which DRAM require Post Package Repair is determined by a proprietary Dell algorithm that takes into account correctable error rates and error patterns.

![](images/2022-12-01-08-15-05.png)

PPR is always available on PowerEdge server platforms that support it and will automatically execute after a system reboot if BIOS deems it necessary. Note that BIOS may automatically promote a warm reset to a cold reset during this process. In order for PPR to successfully execute, it is recommended that
users do not swap or replace DIMMs between boots when receiving memory error event messages, unless instructed to do so by Dell technical support personnel.
In addition to PPR, the PowerEdge server memory self-healing process also includes memory re-training. Memory training is the process by which the CPU initializes, calibrates, and tunes the link between itself and the memory modules. [Grant's note: the memory signaling can change for a variety of reasons: ambient temperature, humidity, or in this case - a change in the memory.] While performing full memory training can help to ensure that the memory
bus operates at the highest level of signaling integrity, it is also a time-consuming process that directly impacts server boot times. Therefore, PowerEdge servers only perform this step when necessary, such as during the memory self-healing process.

#### Performance Tuning Recommendation

Leave this enabled. It will only run when an uncorrectable memory error occurs which is rare.

## Processor Settings

### Logical Processor

This controls hyper threading/simultaneous multithreading (SMT). Many years ago there was wisdom saying that you should turn off SMT because the performance benefits were minimal and operating systems would schedule tasks on logical cores instead of available physical cores. With time all major operating systems rewrote their schedulers to be aware of SMT and performance has significantly increased. In the vast majority of workloads, SMT is beneficial. However, it works by sharing the resources of one physical CPU core between two logical CPUs. Those two logical CPUs share resources and the idea is that whenever one thread or another is briefly idle the other can take advantage of the CPU resources. However, in some instances, ex: databases, threads stay busy resulting in competition and a degradation of performance. [Oracle is an example of this](https://docs.oracle.com/cd/E95618_01/html/sbc_scz810_installation/GUID-F2C27A7A-D173-4655-99C5-D1E367DDF2A8.htm). If you think you may be in this scenario it is worth benchmarking with and without SMT to see which performs better.

### IOMMU Support

The IOMMU is required to support Direct Memory Access (DMA). Unless you have a use-case specific reason, this is best left on. On AMD systems, it enables the [IVRS ACPI table](https://www.amd.com/system/files/TechDocs/48882_3.07_PUB.pdf) used to support DMA for VMs.

### Kernel DMA Protection

This is there to protect against [DMA Attacks](https://en.wikipedia.org/wiki/DMA_attack). Originally, PCIe devices were entirely external and usually required a reboot to enable. However, in modern computers you often have things like Thunderbolt. An attacker can plug in a Thunderbolt device and then use DMA to read arbitrary memory. [Kernel DMA Protection](https://learn.microsoft.com/en-us/windows/security/information-protection/kernel-dma-protection-for-thunderbolt) protects against this by rejecting any devices which don't support memory access protection. This is done by the IOMMU and it effectively forces the device to honor memory access protection in order to function. With memory access protection the device is only allowed to access its own memory space.

### Prefetching

There are two prefetch settings you can control L1 and L2. The merits of prefetching or not prefetching are a deep and complicated subject. [This paper](https://faculty.cc.gatech.edu/~hyesoon/lee_taco12.pdf) does a good job of getting into the weeds on when it is worth it and when it isn't. In general, whether prefetching is valuable is extremely workload dependent. Well optimized workloads will be compiled with prefetch instructions specific to it.

In general, there are two types of prefetching - hardware and software. [This book](http://www.nic.uoregon.edu/~khuck/ts/acumem-report/manual_html/ch_intro_prefetch.html) has a good deep dive and there is also a [Wikipedia Article](https://en.wikipedia.org/wiki/Cache_prefetching#Hardware_vs._software_cache_prefetching).

**Software Prefetching**

Software prefetching is when the programmer or compiler adds instructions to the program. These instructions then load the cache line into cache, but will not stall the thread while waiting for it to load. In this way, the programmer directly controls what is and isn't prefetched. The goal is to prefetch the data long enough before its usage such that it is available at the time of execution, but not so longe before that the data is evicted and then must be reloaded. An intuitive example of where this is helpful is in loops where the compiler can see that something will imminently be loaded.

**Hardware Prefetching**

Hardware prefetches are, as the name implies, implemented in hardware. There are many different [types of hardware prefetching](https://en.wikipedia.org/wiki/Cache_prefetching#Methods_of_hardware_prefetching).

- Stream buffer: If there is a cache miss, fetch the missed block *and* several of the surrounding blocks under the assumption that data you want is typically close together in memory.
- Strided prefetching: Watch for patterns in memory accesses and fetch based on those patterns. Ex: If A is fetched, immediately followed by B, starting prefetching B with A.
- Temporal prefetching: Watch for memory access patterns over time

#### Understanding Prefetching Performance Implications

I found [page 2 of this study to be particularly helpful](https://faculty.cc.gatech.edu/~hyesoon/lee_taco12.pdf#page=2). The graph is a bit confusing at first but it illustrates testing different workloads with and without hardware prefetch enabled. Here are some notes on how to interpret it:

- SW refers to software prefetch but only in the context of a programmer manually interceding and creating prefetch rules specific to the workload
- Base also refers to software prefetch but only the default compiler optimizations (the study used `icc` compiler)
- GHB is an acornym for Global History Buffer
- The right axis only applies to the black tickmark
- The black tickmark describes the ratio of the best performing combination of SW, SW+GHB, SW+STR vs the best performing hardware prefetch scheme **alone** or compiler optimizations only.
- Positive means that the performance of SW/SW+GHB/SW+STR outperformed base/GHB/STR by the ratio indicate on the right axis. Neutral means it was a tie. Negative means that SW/SW+GHB/SW+STR was worse than base/GHB/STR.

[Section 3](https://faculty.cc.gatech.edu/~hyesoon/lee_taco12.pdf#page=5) of the paper discusses the positive and negative impacts of prefetching. It is worth exploring these to get some notion of how your workload may perform. However, nothing beats benchmarking.

From an options perspective, you can both enable and disable L1 and L2 prefetching. The options simply let you turn hardware caching at both levels on and off.

### MADT Core Enumeration

https://learn.microsoft.com/en-us/windows-hardware/drivers/bringup/acpi-system-description-tables

