# Setting Up Proxmox on R6515

- [Setting Up Proxmox on R6515](#setting-up-proxmox-on-r6515)
  - [Configure Ceph](#configure-ceph)
    - [Sanity checks and tiny troubleshooting](#sanity-checks-and-tiny-troubleshooting)


## Configure Ceph

On my setup I only had the one R6515 so I had to do some things to configure Ceph so that it would be "ok" with running on one node.

1. Create OSDs (Ceph will wipe the disks it needs; they must be empty)

```bash
# replace with your actual raw devices
pveceph osd create /dev/nvme1n1
pveceph osd create /dev/nvme0n1
pveceph osd create /dev/nvme2n1
pveceph osd create /dev/nvme3n1
pveceph osd create /dev/nvme4n1
```

2. Tell Ceph it's a single host: place replicas on different OSDs of the same node

```bash
ceph osd crush rule create-replicated onehost_osd default osd
```

3. Fix the internal pool and create your data pool

```bash
# internal manager pool: keep 2 copies across different OSDs on this host
ceph osd pool set .mgr crush_rule onehost_osd
ceph osd pool set .mgr size 2
ceph osd pool set .mgr min_size 1
ceph osd pool set .mgr pg_autoscale_mode on

# VM/data pool (RBD) with the same policy
ceph osd pool create rbd
ceph osd pool set rbd crush_rule onehost_osd
ceph osd pool set rbd size 2
ceph osd pool set rbd min_size 1
ceph osd pool set rbd pg_autoscale_mode on
rbd pool init rbd
```

So what are all these commands doing?

`ceph osd pool create rbd`
Creates a new logical "bucket" (pool) named rbd. A pool is where objects (your VM disk data, in this case) will live. Initially it has a tiny number of placement groups (PGs); we let the autoscaler fix that next.

`ceph osd pool set rbd crush_rule onehost_osd`
Binds the rbd pool to the CRUSH rule called onehost\_osd. That rule tells Ceph how to place replicas: in your single-node setup, it means "spread copies across different OSDs (disks) within this one host," instead of trying (and failing) to place them on different hosts.

`ceph osd pool set rbd size 2`
Sets the replication factor (number of copies) for every object in the rbd pool to 2. With 5 OSDs on one box, this gives you resilience to one-disk failure.

`ceph osd pool set rbd min_size 1`
Sets the minimum number of copies required to keep the pool writable to 1. If one of the two copies is temporarily missing (e.g., an OSD died and recovery is in progress), Ceph will still serve I/O so you don't stall.

`ceph osd pool set rbd pg_autoscale_mode on`
Enables the PG autoscaler for this pool. Instead of you picking `pg_num manually`, Ceph will grow/shrink the number of placement groups as the pool's size and cluster capacity change, aiming for balanced data distribution without you tuning PG math.

`rbd pool init rbd`
Initializes the pool for RBD (Ceph's block device layer). Under the hood it does two key things:

- Marks the pool as an RBD "application" so Ceph understands what's stored there (this removes warnings about an unbound application).
- Creates the minimal metadata needed for RBD images (so you can start creating VM disks immediately).


4. Verify health

```bash
ceph -s
ceph osd pool ls detail
ceph osd crush rule dump | grep -A5 onehost_osd
```

You want to see `HEALTH_OK` (or briefly "peering/remapped" that settles to "active+clean").

5. (Optional) Add the pool to Proxmox storage via CLI (you can also click it in the UI)

```bash
# uses /etc/pve/ceph.conf and the local Ceph keyrings
pvesm add rbd cephrbd -pool rbd -content images,rootdir
```

### Sanity checks and tiny troubleshooting

* After creating OSDs or changing rules, a brief "peering/remapped" is normal. It should converge to "active+clean".
* If you ever see "undersized" again on `.mgr` or `rbd`, confirm both pools are using `onehost_osd` and `size 2`.

  ```bash
  ceph osd pool get .mgr crush_rule
  ceph osd pool get rbd crush_rule
  ceph osd pool get rbd size
  ```
* If a disk dies, Ceph will mark that OSD down/out and re-replicate the missing copies onto the remaining disks automatically.


