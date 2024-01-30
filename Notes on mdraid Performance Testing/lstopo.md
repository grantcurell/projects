[root@r8402 ~]# lstopo
Machine (187GB total)
  Package L#0
    NUMANode L#0 (P#0 45GB)
    L3 L#0 (14MB)
      L2 L#0 (1024KB) + L1d L#0 (32KB) + L1i L#0 (32KB) + Core L#0
        PU L#0 (P#0)
        PU L#1 (P#40)
      L2 L#1 (1024KB) + L1d L#1 (32KB) + L1i L#1 (32KB) + Core L#1
        PU L#2 (P#4)
        PU L#3 (P#44)
      L2 L#2 (1024KB) + L1d L#2 (32KB) + L1i L#2 (32KB) + Core L#2
        PU L#4 (P#8)
        PU L#5 (P#48)
      L2 L#3 (1024KB) + L1d L#3 (32KB) + L1i L#3 (32KB) + Core L#3
        PU L#6 (P#12)
        PU L#7 (P#52)
      L2 L#4 (1024KB) + L1d L#4 (32KB) + L1i L#4 (32KB) + Core L#4
        PU L#8 (P#16)
        PU L#9 (P#56)
      L2 L#5 (1024KB) + L1d L#5 (32KB) + L1i L#5 (32KB) + Core L#5
        PU L#10 (P#20)
        PU L#11 (P#60)
      L2 L#6 (1024KB) + L1d L#6 (32KB) + L1i L#6 (32KB) + Core L#6
        PU L#12 (P#24)
        PU L#13 (P#64)
      L2 L#7 (1024KB) + L1d L#7 (32KB) + L1i L#7 (32KB) + Core L#7
        PU L#14 (P#28)
        PU L#15 (P#68)
      L2 L#8 (1024KB) + L1d L#8 (32KB) + L1i L#8 (32KB) + Core L#8
        PU L#16 (P#32)
        PU L#17 (P#72)
      L2 L#9 (1024KB) + L1d L#9 (32KB) + L1i L#9 (32KB) + Core L#9
        PU L#18 (P#36)
        PU L#19 (P#76)
    HostBridge
      PCI 00:11.5 (RAID)
      PCI 00:17.0 (RAID)
      PCIBridge
        PCI 01:00.0 (Ethernet)
          Net "eno99"
        PCI 01:00.1 (Ethernet)
          Net "eno100"
      PCIBridge
        PCIBridge
          PCI 03:00.0 (VGA)
    HostBridge
      PCIBridge
        PCI 17:00.0 (Ethernet)
          Net "eno145"
        PCI 17:00.1 (Ethernet)
          Net "eno146"
    HostBridge
      PCIBridge
        PCI 25:00.0 (SATA)
          Block(Disk) "sda"
  Package L#1
    NUMANode L#1 (P#1 47GB)
    L3 L#1 (14MB)
      L2 L#10 (1024KB) + L1d L#10 (32KB) + L1i L#10 (32KB) + Core L#10
        PU L#20 (P#1)
        PU L#21 (P#41)
      L2 L#11 (1024KB) + L1d L#11 (32KB) + L1i L#11 (32KB) + Core L#11
        PU L#22 (P#5)
        PU L#23 (P#45)
      L2 L#12 (1024KB) + L1d L#12 (32KB) + L1i L#12 (32KB) + Core L#12
        PU L#24 (P#9)
        PU L#25 (P#49)
      L2 L#13 (1024KB) + L1d L#13 (32KB) + L1i L#13 (32KB) + Core L#13
        PU L#26 (P#13)
        PU L#27 (P#53)
      L2 L#14 (1024KB) + L1d L#14 (32KB) + L1i L#14 (32KB) + Core L#14
        PU L#28 (P#17)
        PU L#29 (P#57)
      L2 L#15 (1024KB) + L1d L#15 (32KB) + L1i L#15 (32KB) + Core L#15
        PU L#30 (P#21)
        PU L#31 (P#61)
      L2 L#16 (1024KB) + L1d L#16 (32KB) + L1i L#16 (32KB) + Core L#16
        PU L#32 (P#25)
        PU L#33 (P#65)
      L2 L#17 (1024KB) + L1d L#17 (32KB) + L1i L#17 (32KB) + Core L#17
        PU L#34 (P#29)
        PU L#35 (P#69)
      L2 L#18 (1024KB) + L1d L#18 (32KB) + L1i L#18 (32KB) + Core L#18
        PU L#36 (P#33)
        PU L#37 (P#73)
      L2 L#19 (1024KB) + L1d L#19 (32KB) + L1i L#19 (32KB) + Core L#19
        PU L#38 (P#37)
        PU L#39 (P#77)
    HostBridge
      PCIBridge
        PCI 48:00.0 (RAID)
  Package L#2
    NUMANode L#2 (P#2 47GB)
    L3 L#2 (14MB)
      L2 L#20 (1024KB) + L1d L#20 (32KB) + L1i L#20 (32KB) + Core L#20
        PU L#40 (P#2)
        PU L#41 (P#42)
      L2 L#21 (1024KB) + L1d L#21 (32KB) + L1i L#21 (32KB) + Core L#21
        PU L#42 (P#6)
        PU L#43 (P#46)
      L2 L#22 (1024KB) + L1d L#22 (32KB) + L1i L#22 (32KB) + Core L#22
        PU L#44 (P#10)
        PU L#45 (P#50)
      L2 L#23 (1024KB) + L1d L#23 (32KB) + L1i L#23 (32KB) + Core L#23
        PU L#46 (P#14)
        PU L#47 (P#54)
      L2 L#24 (1024KB) + L1d L#24 (32KB) + L1i L#24 (32KB) + Core L#24
        PU L#48 (P#18)
        PU L#49 (P#58)
      L2 L#25 (1024KB) + L1d L#25 (32KB) + L1i L#25 (32KB) + Core L#25
        PU L#50 (P#22)
        PU L#51 (P#62)
      L2 L#26 (1024KB) + L1d L#26 (32KB) + L1i L#26 (32KB) + Core L#26
        PU L#52 (P#26)
        PU L#53 (P#66)
      L2 L#27 (1024KB) + L1d L#27 (32KB) + L1i L#27 (32KB) + Core L#27
        PU L#54 (P#30)
        PU L#55 (P#70)
      L2 L#28 (1024KB) + L1d L#28 (32KB) + L1i L#28 (32KB) + Core L#28
        PU L#56 (P#34)
        PU L#57 (P#74)
      L2 L#29 (1024KB) + L1d L#29 (32KB) + L1i L#29 (32KB) + Core L#29
        PU L#58 (P#38)
        PU L#59 (P#78)
    HostBridge
      PCIBridge
        PCI 88:00.0 (NVMExp)
          Block(Disk) "nvme0n1"
      PCIBridge
        PCI 89:00.0 (NVMExp)
          Block(Disk) "nvme1n1"
    HostBridge
      PCIBridge
        PCI 9b:00.0 (NVMExp)
          Block(Disk) "nvme2n1"
      PCIBridge
        PCI 9c:00.0 (NVMExp)
          Block(Disk) "nvme3n1"
      PCIBridge
        PCI 9d:00.0 (NVMExp)
          Block(Disk) "nvme4n1"
      PCIBridge
        PCI 9e:00.0 (NVMExp)
          Block(Disk) "nvme5n1"
  Package L#3
    NUMANode L#3 (P#3 47GB)
    L3 L#3 (14MB)
      L2 L#30 (1024KB) + L1d L#30 (32KB) + L1i L#30 (32KB) + Core L#30
        PU L#60 (P#3)
        PU L#61 (P#43)
      L2 L#31 (1024KB) + L1d L#31 (32KB) + L1i L#31 (32KB) + Core L#31
        PU L#62 (P#7)
        PU L#63 (P#47)
      L2 L#32 (1024KB) + L1d L#32 (32KB) + L1i L#32 (32KB) + Core L#32
        PU L#64 (P#11)
        PU L#65 (P#51)
      L2 L#33 (1024KB) + L1d L#33 (32KB) + L1i L#33 (32KB) + Core L#33
        PU L#66 (P#15)
        PU L#67 (P#55)
      L2 L#34 (1024KB) + L1d L#34 (32KB) + L1i L#34 (32KB) + Core L#34
        PU L#68 (P#19)
        PU L#69 (P#59)
      L2 L#35 (1024KB) + L1d L#35 (32KB) + L1i L#35 (32KB) + Core L#35
        PU L#70 (P#23)
        PU L#71 (P#63)
      L2 L#36 (1024KB) + L1d L#36 (32KB) + L1i L#36 (32KB) + Core L#36
        PU L#72 (P#27)
        PU L#73 (P#67)
      L2 L#37 (1024KB) + L1d L#37 (32KB) + L1i L#37 (32KB) + Core L#37
        PU L#74 (P#31)
        PU L#75 (P#71)
      L2 L#38 (1024KB) + L1d L#38 (32KB) + L1i L#38 (32KB) + Core L#38
        PU L#76 (P#35)
        PU L#77 (P#75)
      L2 L#39 (1024KB) + L1d L#39 (32KB) + L1i L#39 (32KB) + Core L#39
        PU L#78 (P#39)
        PU L#79 (P#79)
    HostBridge
      PCIBridge
        PCI c8:00.0 (NVMExp)
          Block(Disk) "nvme6n1"
      PCIBridge
        PCI c9:00.0 (NVMExp)
          Block(Disk) "nvme7n1"
      PCIBridge
        PCI ca:00.0 (NVMExp)
          Block(Disk) "nvme8n1"
      PCIBridge
        PCI cb:00.0 (NVMExp)
          Block(Disk) "nvme9n1"
    HostBridge
      PCIBridge
        PCI db:00.0 (NVMExp)
          Block(Disk) "nvme10n1"
      PCIBridge
        PCI dc:00.0 (NVMExp)
          Block(Disk) "nvme11n1"
  Misc(MemoryModule)
  Misc(MemoryModule)
  Misc(MemoryModule)
  Misc(MemoryModule)
  Misc(MemoryModule)
  Misc(MemoryModule)
  Misc(MemoryModule)
  Misc(MemoryModule)
  Misc(MemoryModule)
  Misc(MemoryModule)
  Misc(MemoryModule)
  Misc(MemoryModule)
  Misc(MemoryModule)
  Misc(MemoryModule)
  Misc(MemoryModule)
  Misc(MemoryModule)
  Misc(MemoryModule)
  Misc(MemoryModule)
  Misc(MemoryModule)
  Misc(MemoryModule)
  Misc(MemoryModule)
  Misc(MemoryModule)
  Misc(MemoryModule)
  Misc(MemoryModule)