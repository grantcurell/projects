
# MTU Change Bug

- [MTU Change Bug](#mtu-change-bug)
  - [Version](#version)
  - [Reproduction](#reproduction)
  - [Post Mortem](#post-mortem)
  - [Files](#files)
    - [control-plane-interface.bu](#control-plane-interfacebu)
    - [worker-interface.bu](#worker-interfacebu)
    - [control-plane-interface.yaml](#control-plane-interfaceyaml)
    - [worker-interface.yaml](#worker-interfaceyaml)

## Version

- I tested on 4.16 and my work colleague tested on 4.12 with the same results, different networks/hardware.

## Reproduction

- Follow [these instructions](https://docs.openshift.com/container-platform/4.16/networking/changing-cluster-network-mtu.html) to step 9.

## Post Mortem

- I ran [this procedure](https://docs.openshift.com/container-platform/4.16/networking/changing-cluster-network-mtu.html)
- After step 9 the cluster crashes.

```bash
oc patch Network.operator.openshift.io cluster --type=merge --patch '{"spec": { "migration": null, "defaultNetwork":{ "ovnKubernetesConfig": { "mtu": <mtu> }}}}'
```

- In my case I see two nodes offline:

```bash
[grant@rockydesktop tmp]$ oc get nodes
NAME                STATUS     ROLES                  AGE     VERSION
00-50-56-8a-39-a0   Ready      control-plane,master   5h48m   v1.29.6+aba1e8d
00-50-56-8a-44-52   NotReady   control-plane,master   5h48m   v1.29.6+aba1e8d
00-50-56-8a-5c-ec   Ready      control-plane,master   5h30m   v1.29.6+aba1e8d
00-50-56-8a-e1-e7   Ready      worker                 5h37m   v1.29.6+aba1e8d
00-50-56-8a-f2-5d   Ready      worker                 5h37m   v1.29.6+aba1e8d
00-50-56-8a-fb-ea   NotReady   worker                 5h37m   v1.29.6+aba1e8d
```

- First I checked the machine configs to make sure that the MTU change is there as expected. In both you see the same thing
  - [rendered-master-a356caab2b4cda902ccf3872c9f8ef77](./rendered-master-a356caab2b4cda902ccf3872c9f8ef77.md)
  - [rendered-worker-eba2ed8ad0934e9833c26ff044f7e210](./rendered-worker-eba2ed8ad0934e9833c26ff044f7e210.md)

```bash
# Need oneshot to delay kubelet
Type=oneshot
Environment=NETWORK_TYPE=OVNKubernetes
Environment=TARGET_MTU=9000
Environment=CNI_TARGET_MTU=8900
ExecStart=/usr/local/bin/mtu-migration.sh
StandardOutput=journal+console
StandardError=journal+console
```

- I confirmed that the network operator took the MTU change as well:

```bash
[grant@rockydesktop tmp]$ oc get network.operator.openshift.io cluster -o jsonpath='{.spec.defaultNetwork.ovnKubernetesConfig.mtu}'
8900
```

- Next I checked ovn-k8s status:

```bash
[grant@rockydesktop tmp]$ oc get pods -n openshift-ovn-kubernetes
NAME                                     READY   STATUS             RESTARTS        AGE
ovnkube-control-plane-58975cd9fd-7wmvb   2/2     Running            0               120m
ovnkube-control-plane-58975cd9fd-mz4pv   2/2     Running            0               166m
ovnkube-node-568wp                       7/8     CrashLoopBackOff   64 (104s ago)   5h53m
ovnkube-node-5bqnj                       8/8     Running            16              5h53m
ovnkube-node-62ccc                       8/8     Running            16              5h44m
ovnkube-node-7pmvf                       8/8     Running            16              5h44m
ovnkube-node-9h9qr                       7/8     CrashLoopBackOff   64 (88s ago)    5h44m
ovnkube-node-mqh7r                       8/8     Running            16              5h37m
```

- I drilled down into [one of the failed pods](./network_pod_description.md) where I saw that ovnkube-controller had failed:

```bash
Warning  BackOff       22s (x124 over 24m)   kubelet            Back-off restarting failed container ovnkube-controller in pod ovnkube-node-9h9qr_openshift-ovn-kubernetes(5ade0811-dd08-4a17-bac7-fd66e33604a2)
```

- I then pulled [ovnkube-controller's logs](./ovn_kube_controller_logs.md). What caught my attention was the last line:

```bash
F0719 01:46:01.927062   37437 ovnkube.go:136] failed to run ovnkube: failed to start node network controller: failed to start default node network controller: interface MTU (8900) is too small for specified overlay MTU (8958)
```

My hardware MTU is 9000 so I, as the directions specified, set my cluster MTU 100 below to 8900. I don't know why the overlay is looking for 8958 or where that number is coming from. This looks like a bug to me unless I went wrong somewhere along the line.

- To ensure I wasn't facing [this bug](https://access.redhat.com/solutions/5736191) I checked the MTU's on the host:

```bash
[grant@rockydesktop testing]$ oc debug node/00-50-56-8a-fb-ea -- chroot /host ip a sh | grep mtu
Starting pod/00-50-56-8a-fb-ea-debug ...
To use host binaries, run `chroot /host`
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
2: ens192: <BROADCAST,MULTICAST,ALLMULTI,UP,LOWER_UP> mtu 8900 qdisc mq master ovs-system state UP group default qlen 1000
3: ovs-system: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
5: genev_sys_6081: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 65000 qdisc noqueue master ovs-system state UNKNOWN group default qlen 1000
6: ovn-k8s-mp0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 8900 qdisc noqueue state UNKNOWN group default qlen 1000
7: br-int: <BROADCAST,MULTICAST> mtu 8900 qdisc noop state DOWN group default qlen 1000
8: br-ex: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 8900 qdisc noqueue state UNKNOWN group default qlen 1000
```

## Files

Note: I had to make the version 4.15.0 because 4.16.0 was not supported by butane.

### control-plane-interface.bu

```
variant: openshift
version: 4.15.0
metadata:
  name: 01-control-plane-interface
  labels:
    machineconfiguration.openshift.io/role: master
storage:
  files:
    - path: /etc/NetworkManager/conf.d/99-ens192-mtu.conf
      contents:
        local: ens192-mtu.conf
      mode: 0600
```

### worker-interface.bu

```
variant: openshift
version: 4.15.0
metadata:
  name: 01-worker-interface
  labels:
    machineconfiguration.openshift.io/role: worker
storage:
  files:
    - path: /etc/NetworkManager/conf.d/99-ens192-mtu.conf
      contents:
        local: ens192-mtu.conf
      mode: 0600
```

### control-plane-interface.yaml

```
# Generated by Butane; do not edit
apiVersion: machineconfiguration.openshift.io/v1
kind: MachineConfig
metadata:
  labels:
    machineconfiguration.openshift.io/role: master
  name: 01-control-plane-interface
spec:
  config:
    ignition:
      version: 3.4.0
    storage:
      files:
        - contents:
            compression: ""
            source: data:,%5Bconnection-ens192-mtu%5D%0Amatch-device%3Dinterface-name%3Aens192%0Aethernet.mtu%3D8900%0A
          mode: 384
          path: /etc/NetworkManager/conf.d/99-ens192-mtu.conf
```

### worker-interface.yaml

```
# Generated by Butane; do not edit
apiVersion: machineconfiguration.openshift.io/v1
kind: MachineConfig
metadata:
  labels:
    machineconfiguration.openshift.io/role: worker
  name: 01-worker-interface
spec:
  config:
    ignition:
      version: 3.4.0
    storage:
      files:
        - contents:
            compression: ""
            source: data:,%5Bconnection-ens192-mtu%5D%0Amatch-device%3Dinterface-name%3Aens192%0Aethernet.mtu%3D8900%0A
          mode: 384
          path: /etc/NetworkManager/conf.d/99-ens192-mtu.conf
```