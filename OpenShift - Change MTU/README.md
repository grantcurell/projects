# OpenShift - Change MTU

- Run `oc describe network.config cluster` and confirm the current MTU

```bash
oc describe network.config cluster
Status:
  Cluster Network:
    Cidr:               10.128.0.0/14
    Host Prefix:        23
  Cluster Network MTU:  1400
  Conditions:
    Last Transition Time:  2024-07-18T20:13:35Z
    Message:
    Reason:                AsExpected
    Status:                True
    Type:                  NetworkDiagnosticsAvailable
  Network Type:            OVNKubernetes
```

- Run the below script to generate the network manager configurations automatically for all nodes in your cluster. Change the MTU if you need to, just don't forget that it needs to be 100 less than the hardware MTU.

```bash
#!/bin/bash

# Variables
MTU=8900
OUTPUT_DIR="mtu_configs"
rm -rf mtu_configs

# Create the output directory if it does not exist
mkdir -p ${OUTPUT_DIR}

# Function to find the primary network interface using OVN-Kubernetes
find_primary_interface() {
    local node=$1
    oc debug node/$node -- chroot /host nmcli -g connection.interface-name c show ovs-if-phys0 | tr -d '\r'
}

# Function to create NetworkManager configuration file
create_nm_config() {
    local node=$1
    local interface=$2
    local mtu=$3
    local output_dir=$4
    cat <<EOF > ${output_dir}/${node}-${interface}-mtu.conf
[connection-${interface}-mtu]
match-device=interface-name:${interface}
ethernet.mtu=${mtu}
EOF
}

# Main script
echo "Retrieving list of nodes..."
nodes=$(oc get nodes -o jsonpath='{.items[*].metadata.name}')

if [ -z "$nodes" ]; then
    echo "Failed to retrieve nodes or no nodes found."
    exit 1
fi

for node in $nodes; do
    echo "Processing node: $node"
    interface=$(find_primary_interface $node)
    if [ -z "$interface" ]; then
        echo "Failed to find the primary network interface on node $node. Skipping."
        continue
    fi
    echo "Primary network interface on node $node is $interface."
    create_nm_config $node $interface $MTU $OUTPUT_DIR
    echo "Configuration file created for node $node with interface $interface."
done

echo "All configuration files have been generated in the ${OUTPUT_DIR} directory."
```

- Next we have to create Butane files to make the actual change. Butane is a tool used to generate Fedora CoreOS (FCOS) configurations. It takes a human-readable YAML configuration file and translates it into an Ignition JSON configuration file. Ignition is a provisioning utility designed to configure Fedora CoreOS machines during the first boot.
- Create the control plane file:
  - Note: You must use 15 or you'll get a translation error. 16 hasn't been loaded into butane.

**control-plane-interface.bu**
```yaml
variant: openshift
version: 4.15.0
metadata:
  name: 01-control-plane-interface
  labels:
    machineconfiguration.openshift.io/role: master
storage:
  files:
    - path: /etc/NetworkManager/conf.d/99-<interface>-mtu.conf 
      contents:
        local: <interface>-mtu.conf 
      mode: 0600
```

- Create the worker:

**worker-interface.bu**
```yaml
variant: openshift
version: 4.16.0
metadata:
  name: 01-worker-interface
  labels:
    machineconfiguration.openshift.io/role: worker
storage:
  files:
    - path: /etc/NetworkManager/conf.d/99-<interface>-mtu.conf 
      contents:
        local: <interface>-mtu.conf 
      mode: 0600
```

Now run:

```bash
for manifest in control-plane-interface worker-interface; do
    butane --files-dir . $manifest.bu > $manifest.yaml
done
```

- Kick off the migration with:

```bash
oc patch Network.operator.openshift.io cluster --type=merge --patch '{"spec": { "migration": { "mtu": { "network": { "from": 1400, "to": 8900 }, "machine": { "to": 9000 } } } } }'
```