# PCIev3 vs v4
## PCIe v3 vs v4

PCIev3 Speed Per lane: 1GB/s unidirectional
PCIev3 Max unidirectional speed: 16GB/s

PCIev4 Speed per lane: 2GB/s unidirectional
PCIev4 Max unidirectional speed: 32GB/s

## Samsung NF1 Drive

According to [this article](https://www.anandtech.com/show/12567/hands-on-samsung-nf1-16-tb-ssds) a single NF1 drive runs at 3,000MB/s sequential read speed and a 1900 MB/s sequential write speed.

## Xeon Second Gen Scalable Procs

According to [this article](https://www.intel.com/content/dam/www/public/us/en/documents/product-briefs/2nd-gen-xeon-scalable-processors-brief-Feb-2020-2.pdf) a second gen xeon proc provides 48 PCIe v3 lanes. Two procs would mean 96.

This means that a 2 proc server with these chips could theoretically run up to 96GB/s unidirectional speed.

96-36 = 60

64

## SuperMicro 1029P-NMR36L

Dual socket Xeon gen 2 procs with space for 32 hot-swap pci-e3 nf1 drives plus 4 SATA 3 M.2 drive bays.

In a scenario where only drives were in the box and under theoretical perfect conditions, you could see a 96GB/s read speed. (Bascially impossible you'd ever actually see that)



