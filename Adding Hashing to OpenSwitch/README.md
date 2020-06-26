This is the first problem: https://github.com/open-switch/opx-tools/issues/27

He says the code should be somewhere here: https://github.com/open-switch/opx-base-model/blob/master/yang-models/dell-base-hash.yang

![https://github.com/open-switch/opx-docs/wiki/NAS-L2](images/nas_l2.png)

![https://github.com/open-switch/opx-docs/raw/master/images/opx_architecture.png](images/opx_architecture.png)

[Helpful docs on how yang is processed](https://github.com/open-switch/opx-base-model)

## Installing header files for OPX base

Run `apt install -y libopx-base-model-dev`. The headers will be in `/usr/include/opx`. The metadata files are in `ls /usr/lib/x86_64-linux-gnu/`

## Adding Space / Remote Desktop

I wanted more space on my installation so I added a usb drive. Do the following
to clear the USB driver and then add space:

### Configure USB

    fdisk /dev/sdb
    d
    d
    d
    w

### Extend Partition

    pvcreate /deb/sdb
    vgextend OPX /dev/sdb
    lvextend -l +100%FREE /dev/OPX/SYSROOT1
    resize2fs /dev/mapper/OPX-SYSROOT1

### Remote Desktop

    sudo apt update
    sudo apt install xfce4 xfce4-goodies xorg dbus-x11 x11-xserver-utils
    sudo apt install xrdp
    sudo adduser xrdp ssl-cert 
    xfce4-session-logout --halt

## Investigation

- cps_get_oid.py -qua target base-switch/switching-entities/switching-entity
- The question to ask is - what is the server application for the CPS object?
- The problem is that in `opx-config-global-switch` the value `lag-hash-fields` isn't present in target_attrs  on line 214 of opx-config-global-switch
  - The question is what would populate that?
- I don't think any of what I care about is in NAS L2.
  - NAS L2 handles This repository contains the Layer 2 (L2) component of the network abstraction service (NAS). This handles media access control (MAC) learning, programming spanning-tree protocol (STP) state, mirroring, sFlow, and other switch configurations.
- I think what I care about is in opx-nas-interface because the operating system is handling the LAG. Description is
  - This repository contains the interface portion of the network abstraction service (NAS). This creates interfaces in the Linux kernel corresponding to the network processor unit (NPU) front panel ports, manages VLAN and LAG configurations, statistics management and control packet handling.
- Logically there are three components including the LAG: LAG DS, NAS LAG, NDI LAG. See picture.
- NAS Daemon: The NAS daemon integrates standard Linux network APIs with NPU hardware functionality, and registers and listens to networking (netlink) events.
- What enum values in the model of dell-base-hash align with what's in opx-config-global-switch in hash fields map.
  - What are all these actions in opx-config-global-switch?
  - Ok - so now we know the thing I want is in base-traffic-hash/entry, but `opx-config-global-switch` is looking at `base-switch/switching-entities/switching-entity`. The next question is what populates that? Why are the hashes not in it?
    - The definition for switching-entity is at: https://github.com/open-switch/opx-base-model/blob/abdf66f813b48a3c8e7682361cdacccd0271866d/yang-models/dell-base-switch-element.yang
    - Say what? `hash-fields` is also defined in `base-switch/switching-entities/switching-entity`
- The next question to ask is who has ownership of base-traffic-hash? What about base-switch/switching-entities/switching-entity? The problem seems like it should be there? Why? 
  - base-traffic-hash is owned by opx_nas_daemon
  - base-switch/switching-entities/switching-entity is also owned by opx_nas_daemon
- CPS has a REST service according to: https://github.com/open-switch/opx-cps
- The connection between YANG and the applications seems to be the CPS API? 
  - Applications define objects through (optionally YANG-based) object models. These object models are converted into binary (C accessible) object keys and object attributes that can be used in conjunction with the C-based CPS APIs.
- Description of cps_model_info: This tool is useful to get all information about CPS objects on the target. It is used to get the attributes of a specific CPS object, or first-level contents of a given YANG path of the CPS object (as defined in the YANG model).
  - IT GIVES THE PROCESS OWNER!
- Investigating ops-nas-daemon
  - There is a file called base_nas_default_init which defines the mirror port and the flow behaviors. I haven't found anything about other stuff yet.
    - `opx-config-global-switch --lag-hash-alg crc` works and is owned by opx_nas_daemon - there must be other things it owns beside this.
    - There is a file called `hald_init.c`. I think what is happening is all the other services fall under the NAS daemon. The code I'm looking for is somewhere else.
      - After following that around for a while it looks like the file I'm really interested in is here `https://github.com/open-switch/opx-nas-l2/blob/7e80d3952786f219b8072f1666ff1f16ba353d86/src/switch/nas_hash_cps.cpp`. This bubbles up to the L2 init function, which bubbles back up to `hald_init.c`.

## Descriptions

### NAS

The NAS manages the high-level NPU abstraction and adaptation, and abstracts and aggregates the core functionality required for networking access at Layer 1 (physical), Layer 2 (VLAN, link aggregation), Layer 3 (routing), ACL, QoS, and network monitoring.

The NAS provides adaptation of the low-level switch abstraction provided by the SAI for standard Linux networking APIs and interfaces, and CPS API functionality. The NAS is also responsible for providing packet I/O services using the Linux kernel IP stack (see Network adaptation service for complete information).