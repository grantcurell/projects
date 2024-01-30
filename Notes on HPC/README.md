# Notes on HPC

**KEY TAKEAWAY** Economics will drive the pooling of main memory, and whether or not customers choose the CXL way or the Gen-Z way. Considering that memory can account for half of the cost of a server at a hyperscaler, anything that allows a machine to have a minimal amount of capacity on the node and then share the rest in the rack  with all of it being transparent to the operating system and all of it looking local  will be adopted. There is just no question about that. Memory area networks, in one fashion or another, are going to be common in datacenters before too long, and this will be driven by economics.

## Load Store Architecture

A load–store architecture is an instruction set architecture that divides instructions into two categories: memory access (load and store between memory and registers) and ALU operations (which only occur between registers).

For instance, in a load–store approach both operands and destination for an ADD operation must be in registers. This differs from a register-memory architecture (for example, a CISC instruction set architecture such as x86) in which one of the operands for the ADD operation may be in memory, while the other is in a register.

https://www.sciencedirect.com/topics/computer-science/load-store-architecture
https://en.wikipedia.org/wiki/Load%E2%80%93store_architecture

## Fabric Attached Memory

See [Fabric Attached Memory](./fabric_attached_memory.md)

## CXL

See [Compute Express Link](./cxl.md)

## Radix

https://github.com/HewlettPackard/meadowlark
https://ieeexplore.ieee.org/document/6307777

## Things to investigate

https://www.techpowerup.com/292256/amd-details-its-3d-v-cache-design-at-isscc