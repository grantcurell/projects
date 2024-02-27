# How Drive Overprovisioning Works

- [How Drive Overprovisioning Works](#how-drive-overprovisioning-works)
  - [What is Drive Overprovisioning](#what-is-drive-overprovisioning)
  - [How Does Overprovisioning Work](#how-does-overprovisioning-work)
  - [Forcing the Drive to Write all NAND](#forcing-the-drive-to-write-all-nand)
  - [Tips for Increasing Performance](#tips-for-increasing-performance)
    - [Write Amplification](#write-amplification)
  - [Multiuse vs Read Intensive Drives](#multiuse-vs-read-intensive-drives)


When I first encountered overprovisioning, the high level concept seemed quite clear, but the implications and math behind it I found confusing. This paper is for anyone who needs to have an understanding of the mechanics of overprovisioning but it isn't something they look at every day.

## What is Drive Overprovisioning

NVMe drive overprovisioning is a technique used to enhance the performance and extend the lifespan of solid-state drives (SSDs). The drive manufacturer sets aside a portion of the drive's storage capacity and that capacity is not shown as available to the user. This extra space is used by the drive's controller to efficiently manage and rearrange data, which helps in speeding up write operations and reducing wear on the memory cells.

The reason we overprovision is that as the drive is used, NAND dies, but you wouldn't want a situation where the user could use every bit of NAND actually on the drive because that would effectively mean any single NAND failure would immediately cause corruption. Instead, writes to the drive are spread around the entire drive and as parts of the drive die over time spare space is used to replace it. That is in addition to the above where spare space also gives the drive room to do all of its necessary functions - garbage collection, for example.

The next section explains how overprovisioning and drive sizes work.

## How Does Overprovisioning Work

In order to understand overprovisioning you have to understand some (light) math and the difference between how drives are advertised and how they really work.

- In base 10, 1TB is the same as saying $10^{12}=1,000,000,000,000\text{ bytes}$.
- In base 2, 1TB is actually what we call 1TiB. The math is a bit different: $2^{40}=1,099,511,627,776\text{ bytes}$

Ok, but why does that matter? Well, in the real world, each cell of NAND can only be 0 or 1 and the real world measurement should be in base 2. However, most consumers don't understand what base 2 is nor do they want to so marketing decided to advertise things in terms of base 10. For example, if a drive is advertised as being 1TB, that's in base 10 where this number means $10^{12}=1,000,000,000,000\text{ bytes}$, the drive really has 1TiB or $2^{40}=1,099,511,627,776\text{ bytes}$. That's a difference of $99,511,627,776 \text{bytes}=92.677 \text{Gigabytes}$ that the consumer effectively doesn't know is there.

This delta is the overprovisioning. It is the wiggle room that allows the drive to continue to function. To convert it to a percentage, the algorithm is:

$$
\frac{\text{Actual Capacity} - \text{Advertised Capacity}}{\text{Advertised Capacity}}= \text{Percentage Overprovisioned}
$$

Said in plain English, you use $\text{Actual Capacity} - \text{Advertised Capacity}$ to get how many bytes are left over after marketing's base 10 number is removed from the real world's base 2 number. Then you want to make that a percentage so you divide again by marketing's base 10 number. So in the case of our 1TB advertised drive, 1TiB real world, you get:

$$
\frac{1,099,511,627,776 (\text{1TiB}) - 1,000,000,000,000\text{(1TB)}}{1,000,000,000,000\text{(1TB)}}= .09.95\% \text{ Overprovisioned}
$$

That's not a lot, which is why you may notice most manufacturers advertise drives for sizes like 960GBs. The drive **really** is a full 1TiB ($2^{40}$), but the manufacturer advertises it as 960GB ($10^9*960$) A 960GB drive's overprovisioning would be calculated as:

$$
\frac{1,099,511,627,776 (\text{1TiB}) - 960,000,000,000\text{(960GB)}}{960,000,000,000\text{(960GB)}}= 14.5\% \text{ Overprovisioned}
$$

It's worth mentioning these are rough estimations though because this doesn't account for space used by the NVMe drive's internal parallelization mechanisms or proprietary variations.

## Forcing the Drive to Write all NAND

Let's say you want to test the worst-case scenario; it's necessary to completely fill the drive. The objective is to guarantee that all Logical Block Addresses (LBAs) have been written to and every NAND flash cell has been utilized at least once. Below is how you do that:

1. **Sequentially Write 2x the SSD's Capacity**: This step ensures that all NAND blocks have been utilized, regardless of Read Intensive (RI) or Multi-Use (MU) drive type.
2. **Randomly Write 1x the SSD's Capacity**: This step randomizes the LBAs, ensuring a thorough distribution of data across the drive.

After completing these steps, the drive is prepared for Write Amplification (WA) or random performance testing.

## Tips for Increasing Performance
 
1. **Use only the capacity you need**: This helps reduce the problem of write amplification [(explained below)](#write-amplification).
2. **Enhanced Random Write Performance**: SSDs perform best when they have ample unused space to distribute write and erase cycles evenly across the NAND cells, a process known as wear leveling. Keeping a portion of the SSD's capacity unused or 'over-provisioned' ensures that the controller has more flexibility in managing data, which can significantly improve random write performance.
3. **Reduced Power Consumption**: Less used capacity means fewer active write and erase cycles, and less work for the SSD's controller. This efficiency translates into lower power consumption, which is beneficial for both operational costs and, in the case of battery-powered devices, extended device usage between charges.
4. **Use the deallocate Command**: The DEALLOCATE command marks blocks as available for garbage collection and wear leveling.

### Write Amplification

Write Amplification (WA) is an inefficiency in SSDs where the amount of data physically written to the flash memory is significantly higher than the logical data intended to be written by the host system. This discrepancy arises because SSDs cannot overwrite existing data directly; they must first erase the existing data before writing new data. This process often involves copying and erasing more data than what is actually being replaced, leading to WA.

**Why Limiting Used Capacity Reduces WA**:

1. **Increased Over-Provisioning**: By not using the full capacity of the SSD, you effectively increase the amount of over-provisioned (OP) space. Having more OP space allows the controller to more efficiently manage where and how data is written, reducing the need to move and rewrite data as frequently.
2. **Enhanced Wear Leveling**: Wear leveling is a technique used to distribute write and erase cycles evenly across the SSD's memory cells to prolong the device's lifespan. With more free space available, the SSD's controller can spread out the write operations more evenly across a larger pool of memory cells. This reduces the number of erase and rewrite cycles on any given cell, directly decreasing WA.
3. **Optimized Garbage Collection**: Garbage collection is the process by which SSDs reclaim blocks that contain data no longer considered in use. When the SSD has more free space, the garbage collection process can be more selective and efficient, combining partial blocks of valid data into fewer blocks and erasing the now-empty blocks. This efficiency reduces the total number of write operations required for maintenance tasks, lowering WA.
4. **Reduced Frequency of Write and Erase Cycles**: Every write operation on an SSD involves erasing and rewriting entire blocks of data, even if only a small amount of data needs to be changed. By using less of the SSD's capacity, there's less data being shuffled around during garbage collection and wear leveling, which means fewer write and erase cycles are needed. This direct reduction in write and erase cycles leads to a lower Write Amplification Factor (WAF).

## Multiuse vs Read Intensive Drives

In modern NVMe drives, generally the only difference between mixed use and read intensive drives is generally the amount of spare space allocated to them. It depends on manufacturer, but this is generally the case.

Again, generally, a read intensive drive has around 14% spare space and a mixed use drive will have around 37% spare space. That is **after** you account for the delta between advertised being in base 10 and reality being base 2. If you don't account for that delta you will see lower numbers for percentage spare space.

Here's the thing though, modern drives use uncommitted space as spare space. So if you artificially cap the amount of space you use on an RI drive you can effectively turn it into an MU drive. It is only if you completely fill the RI drive that you will see degraded performance due to WA.
