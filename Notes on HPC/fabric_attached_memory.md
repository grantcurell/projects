# Fabric Attached Memory

[Return to README.md](./README.md)

- [Fabric Attached Memory](#fabric-attached-memory)
  - [Resources](#resources)
  - [What is it](#what-is-it)
  - [What Problem is it Solving](#what-problem-is-it-solving)
  - [The Future of FAM](#the-future-of-fam)
  - [Questions:](#questions)

## Resources

Broad overview: https://itigic.com/fabric-attached-memory-is-not-ram-or-cache-in-cpu/

The Machine background information: https://github.com/FabricAttachedMemory/Emulation/wiki

How the emulation for the Machine works: https://github.com/FabricAttachedMemory/Emulation/wiki/Emulation-via-Virtual-Machines

## What is it

FAM is a type of scratchpad memory. Scratchpad memory is memory that resides inside the processor (usually). This brings with it two obvious benefits:

- Programs that run inside scratchpad memory run faster due to the low distance to the processor and with lower power consumption
- Due to its proximity to the processor, a cache system is not needed to access said memory

The difference between regular scratchpad memory and FAM is that FAM uses some network interface to communicate.

## What Problem is it Solving

The main problem with main memory is that the increased wire distance leads to a large increase in power. FAM seeks to solve this by moving it closer to the processor.

It also allows processors to directly share information (or at least not have to write it to main memory and then recover it) by instead writing to FAM which is located between the last level cache and the interface to RAM for each of them.

## The Future of FAM

To understand this part you will need to understand [chiplets](./chiplet_based_systems.md)

The best solution is a chiplet-based system where the Northbridge is disconnected from the rest of the system, as is the case in AMD‘s Ryzen 3000 and Ryzen 5000 CPUs.

FAM, by its nature should have more capacity than the fastest cache but less than RAM. With the northbridge on a separate chip you can integrate FAM into it. However this is difficult to do on 2D chip so instead it would be preferable to use a 3D chip with the northbridge on one level and FAM on the others.

## Questions:

Why is it difficult to integrate FAM onto a 2D chip?