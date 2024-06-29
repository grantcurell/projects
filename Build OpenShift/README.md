
## Helpful Links

- [Offline Install for VMWare](https://docs.openshift.com/container-platform/4.15/installing/installing_vsphere/upi/installing-restricted-networks-vsphere.html#installing-restricted-networks-vsphere)

## Deploy Dell CSI Operator on OpenShift

- I first followed the instructions I wrote for Rancher [here](../PowerScale%20-%20Configure%20with%20Kubernetes/README.md#install_the_csi_driver) to set up the PowerScale side of things.
  - Stop when you get to the settings for K8s.
  - **Make sure you change the path to /ifs/data/csi**. You could change the openshift files, but I found it easier to roll with the default.

![](images/2024-06-25-11-09-48.png)

- Click on the Dell Container Storage Modules and install it with all the defaults
- After you have it installed, browse to the installed operator and click "Create Instance" on the Container Storage Module

![](images/2024-06-25-11-13-05.png)

- Go to YAML view and set `X_CSI_ISI_IGNORE_UNRESOLVABLE_HOSTS` to true.

![](images/2024-06-25-12-16-33.png)

- Create the below secret with the name `empty-secret.yaml` and then create it using `oc`

```bash
[grant@rockydesktop files]$ oc create -f empty-secret.yaml
secret/isilon-certs-0 created
[grant@rockydesktop files]$ cat empty-secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: isilon-certs-0
  namespace: openshift-operators
type: Opaque
data:
  cert-0: ""
```

- Update the below `secret.yaml` with your data and create it in OpenShift using OC

```yaml
isilonClusters:
    # logical name of PowerScale Cluster
  - clusterName: "powerscale"

    # username for connecting to PowerScale OneFS API server
    # if authorization is enabled, username will be ignored
    # Default value: None
    username: "grant"

    # password for connecting to PowerScale OneFS API server
    # if authorization is enabled, password will be ignored
    password: "password"

    # HTTPS endpoint of the PowerScale OneFS API server
    # if authorization is enabled, the endpont should be the localhost address of the csm-authorization-sidecar
    # Default value: None
    # Examples: "1.2.3.4", "https://1.2.3.4", "https://abc.myonefs.com"
    endpoint: "10.10.25.80"

    # endpointPort: Specify the HTTPs port number of the PowerScale OneFS API server
    # Formerly this attribute was named as "isiPort"
    # If authorization is enabled, endpointPort must match the port specified in the endpoint parameter of the karavi-authorization-config secret
    # Allowed value: valid port number
    # Default value: 8080
    endpointPort: 8080

    # Is this a default cluster (would be used by storage classes without ClusterName parameter)
    # Allowed values:
    #   true: mark this cluster config as default
    #   false: mark this cluster config as not default
    # Default value: false
    isDefault: true

    # Specify whether the PowerScale OneFS API server's certificate chain and host name should be verified.
    # Allowed values:
    #   true: skip OneFS API server's certificate verification
    #   false: verify OneFS API server's certificates
    # Default value: default value specified in values.yaml
    skipCertificateValidation: true

    # The base path for the volumes to be created on PowerScale cluster
    # This will be used if a storage class does not have the IsiPath parameter specified.
    # Ensure that this path exists on PowerScale cluster.
    # Allowed values: unix absolute path
    # Default value: default value specified in values.yaml
    # Examples: "/ifs/data/csi", "/ifs/engineering"
    isiPath: "/ifs/data/csi"

    # The permissions for isi volume directory path
    # This will be used if a storage class does not have the IsiVolumePathPermissions parameter specified.
    # Allowed values: valid octal mode number
    # Default value: "0777"
    # Examples: "0777", "777", "0755"
    # isiVolumePathPermissions: "0777"

    # ignoreUnresolvableHosts: Ignore unresolvable hosts on the OneFS
    # When set to true, OneFS allows new host to add to existing export list though any of the existing hosts from the
    # same exports are unresolvable/doesn't exist anymore.
    # Allowed values:
    #   true: ignore existing unresolvable hosts and append new host to the existing export
    #   false: exhibits OneFS default behavior i.e. if any of existing hosts are unresolvable while adding new one it fails
    # Default value: false
    #ignoreUnresolvableHosts: false

    # Unique ID if the certificate is used to encrypt replication policy
    # This will be used if a replication encrypted is enabled, leave empty in case you use unecrypted replication
    # Allowed values: string, unique id of the certificate
    # Default value: ""
    # Examples: "dd9c736cc17e6dd5f7d85fe13528cfc20f3b4b0af4f26595d22328c8d1f461af"
```

- Create with `oc`. `oc create secret generic isilon-creds -n openshift-operators --from-file=config=secret.yaml`
  - **TODO: I had to use admin because I could not for the life of me figure out how to add the privileges to the grant user**

- On the PowerScale cluster run `isi_gconfig -t web-config auth_basic=true` unless you want to set up a real authentication mechanism.
- For the storage class I went into StorageClasses on OpenShift, created one, edited the YAML, and used:

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: isilon
provisioner: csi-isilon.dellemc.com
reclaimPolicy: Delete
allowVolumeExpansion: true
parameters:
  # The name of the access zone a volume can be created in
  # Optional: true
  # Default value: default value specified in values.yaml
  # Examples: System, zone1
  AccessZone: System

  # The base path for the volumes to be created on PowerScale cluster.
  # Ensure that this path exists on PowerScale cluster.
  # Allowed values: unix absolute path
  # Optional: true
  # Default value: value specified in values.yaml for isiPath
  # Examples: /ifs/data/csi, /ifs/engineering
  IsiPath: /ifs/data/csi

  #Parameter to set Advisory Limit to quota
  #Optional: true
  #Default Behaviour : Limit not set
  #AdvisoryLimit: "50"

  #Parameter to set soft limit to quota
  #Optional: true
  #Default Behaviour: Limit not set
  #SoftLimit: "80"

  #Parameter which must be mentioned along with Soft Limit
  #Soft Limit can be exceeded until the grace period
  #Optional: true
  #Default Behaviour : Limit not set
  #SoftGracePrd: "86400"

  # The permissions for isi volume directory path
  # This value overrides the isiVolumePathPermissions attribute of corresponding cluster config in secret, if present
  # Allowed values: valid octal mode number
  # Default value: "0777"
  # Examples: "0777", "777", "0755"
  #IsiVolumePathPermissions: "0777"

  # AccessZone groupnet service IP. Update AzServiceIP if different than endpoint.
  # Optional: true
  # Default value: endpoint of the cluster ClusterName
  #AzServiceIP : 192.168.2.1

  # When a PVC is being created, this parameter determines, when a node mounts the PVC,
  # whether to add the k8s node to the "Root clients" field or "Clients" field of the NFS export
  # Allowed values:
  #   "true": adds k8s node to the "Root clients" field of the NFS export
  #   "false": adds k8s node to the "Clients" field of the NFS export
  # Optional: true
  # Default value: "false"
  RootClientEnabled: "false"

  # Name of PowerScale cluster, where pv will be provisioned.
  # This name should match with name of one of the cluster configs in isilon-creds secret.
  # If this parameter is not specified, then default cluster config in isilon-creds secret
  # will be considered if available.
  # Optional: true
  #ClusterName: <cluster_name>

  # Sets the filesystem type which will be used to format the new volume
  # Optional: true
  # Default value: None
  #csi.storage.k8s.io/fstype: "nfs"

# volumeBindingMode controls when volume binding and dynamic provisioning should occur.
# Allowed values:
#   Immediate: indicates that volume binding and dynamic provisioning occurs once the
#   PersistentVolumeClaim is created
#   WaitForFirstConsumer: will delay the binding and provisioning of a PersistentVolume
#   until a Pod using the PersistentVolumeClaim is created
# Default value: Immediate
volumeBindingMode: Immediate

# allowedTopologies helps scheduling pods on worker nodes which match all of below expressions.
# If enableCustomTopology is set to true in helm values.yaml, then do not specify allowedTopologies
# Change all instances of <ISILON_IP> to the IP of the PowerScale OneFS API server
#allowedTopologies:
#  - matchLabelExpressions:
#      - key: csi-isilon.dellemc.com/<ISILON_IP>
#        values:
#          - csi-isilon.dellemc.com

# specify additional mount options for when a Persistent Volume is being mounted on a node.
# To mount volume with NFSv4, specify mount option vers=4. Make sure NFSv4 is enabled on the Isilon Cluster
#mountOptions: ["<mountOption1>", "<mountOption2>", ..., "<mountOptionN>"]

```


## Old Stuff -----------------

## Common to All Installs

This is all done on some Linux desktop of your choosing

- First you have to go through [Preparing to install a cluster using user-provisioned infrastructure](https://docs.openshift.com/container-platform/4.15/installing/installing_vsphere/upi/upi-vsphere-preparing-to-install.html#upi-vsphere-preparing-to-install)
- Pull the installer from [here](https://console.redhat.com/openshift/install/vsphere)
- Run `tar -xvf openshift-install-linux.tar.gz`
- Get your pull secret from [here](https://console.redhat.com/openshift/install/pull-secret) and save it somewhere
- Download the Linux client from [here](https://access.redhat.com/downloads/content/290/ver=4.15/rhel---9/4.15.16/x86_64/product-software)
  - I just put it in `/usr/local/bin` because it needs to be in path
- Next you need to generate keys for OpenShift. Run `ssh-keygen -t ed25519 -N '' -f <path>/<file_name>` to do this.
- You will need to add the key to your SSH agent. You can do this with `eval "$(ssh-agent -s)"` (this starts the SSH agent). Next run `ssh-add <private_key_name>`
- Before continuing, you will need to set up your DNS server with forward and reverse records for everything in the [User-provisioned DNS Requirements](https://docs.openshift.com/container-platform/4.15/installing/installing_bare_metal/installing-bare-metal-network-customizations.html#installation-dns-user-infra_installing-bare-metal-network-customizations)

I used the following configs.

**dnsmasq config**

```bash
# Configuration file for dnsmasq.

# Never forward plain names (without a dot or domain part)
domain-needed

# Never forward addresses in the non-routed address spaces.
bogus-priv

# Specify the domain for dnsmasq
local=/lan/
local=/openshift.lan/

# Add local DNS records from this file
addn-hosts=/etc/dnsmasq.hosts

# Add wildcard DNS entry for *.apps.openshift.lan
address=/apps.openshift.lan/10.10.25.158

# Specify interfaces to listen on
interface=lo
interface=ens192

# Bind only to the interfaces it is listening on
bind-interfaces

# Set the domain for dnsmasq
domain=openshift.lan
domain=lan

# Include all the files in a directory except those ending in .bak
conf-dir=/etc/dnsmasq.d,.rpmnew,.rpmsave,.rpmorig
```

**/etc/hosts**

```bash
10.10.25.156 api.openshift.lan
10.10.25.157 api-int.openshift.lan
10.10.25.159 bootstrap.openshift.lan
10.10.25.160 controlplane1.openshift.lan
10.10.25.161 compute1.openshift.lan
10.10.25.162 compute2.openshift.lan
10.10.25.163 compute3.openshift.lan
10.10.25.164 quay-server.openshift.lan
```

Then run a quick test against all your DNS entries:

```bash
[grant@rockydesktop openshift_keys]$ dig +noall +answer @10.10.25.120 api.openshift.lan
api.openshift.lan.      0       IN      A       10.10.25.156
[grant@rockydesktop openshift_keys]$ dig +noall +answer @10.10.25.120 api-int.openshift.lan
api-int.openshift.lan.  0       IN      A       10.10.25.157
[grant@rockydesktop openshift_keys]$ dig +noall +answer @10.10.25.120 random.apps.openshift.lan
random.apps.openshift.lan. 0    IN      A       10.10.25.158
[grant@rockydesktop openshift_keys]$ dig +noall +answer @10.10.25.120 bootstrap.openshift.lan
bootstrap.openshift.lan. 0      IN      A       10.10.25.159
[grant@rockydesktop openshift_keys]$ dig +noall +answer @10.10.25.120 -x 10.10.25.156
156.25.10.10.in-addr.arpa. 0    IN      PTR     api.openshift.lan.
```

### Build a Container Registry - Quay

To run OpenShift you also need an offline repo of all your container images. Since everything else I'm running is RHEL, I went with Quay.

First you need to create a config file that corresponds to the DNS entry that you set up earlier for Quay.

```bash
BUILDLOGS_REDIS:
    host: quay-server.openshift.lan
    password: strongpassword
    port: 6379
CREATE_NAMESPACE_ON_PUSH: true
DATABASE_SECRET_KEY: a8c2744b-7004-4af2-bcee-e417e7bdd235
DB_URI: postgresql://quayuser:quaypass@quay-server.openshift.lan:5432/quay
DISTRIBUTED_STORAGE_CONFIG:
    default:
        - LocalStorage
        - storage_path: /datastorage/registry
DISTRIBUTED_STORAGE_DEFAULT_LOCATIONS: []
DISTRIBUTED_STORAGE_PREFERENCE:
    - default
FEATURE_MAILING: false
SECRET_KEY: e9bd34f4-900c-436a-979e-7530e5d74ac8
SERVER_HOSTNAME: quay-server.openshift.lan
SETUP_COMPLETE: true
USER_EVENTS_REDIS:
    host: quay-server.openshift.lan
    password: strongpassword
    port: 6379
```

- Create some Quay directory and put the config file in `<your_quay_directory>/config/config.yml`
- Make the directory `<your_quay_directory>/storage`
- Run `setfacl -m u:1001:-wx <your_quary_directory>/storage`
- Take the pull secret you [got from RedHat](https://console.redhat.com/openshift/install/pull-secret) and use it in the command:

```bash
sudo podman run --authfile ~/pull_secret -d --rm -p 80:8080 -p 443:8443  \
   --name=quay \
   -v $QUAY/config:/conf/stack:Z \
   -v $QUAY/storage:/datastorage:Z \
   registry.redhat.io/quay/quay-rhel8:v3.11.1
```

## Online Assisted Install


## Offline Install on VMWare

## This is for online install (wrong one)

- I went with the VMWare installer since that's what I had to test on

![](images/2024-06-10-11-15-43.png)

![](images/2024-06-10-11-18-53.png)

![](images/2024-06-10-11-25-07.png)

- Question - I'm doing this in a webgui. How does this work offline?