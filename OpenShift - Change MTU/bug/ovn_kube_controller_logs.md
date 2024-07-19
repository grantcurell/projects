+ . /ovnkube-lib/ovnkube-lib.sh
++ set -x
++ K8S_NODE=00-50-56-8a-fb-ea
++ [[ -n 00-50-56-8a-fb-ea ]]
++ [[ -f /env/00-50-56-8a-fb-ea ]]
++ northd_pidfile=/var/run/ovn/ovn-northd.pid
++ controller_pidfile=/var/run/ovn/ovn-controller.pid
++ controller_logfile=/var/log/ovn/acl-audit-log.log
++ vswitch_dbsock=/var/run/openvswitch/db.sock
++ nbdb_pidfile=/var/run/ovn/ovnnb_db.pid
++ nbdb_sock=/var/run/ovn/ovnnb_db.sock
++ nbdb_ctl=/var/run/ovn/ovnnb_db.ctl
++ sbdb_pidfile=/var/run/ovn/ovnsb_db.pid
++ sbdb_sock=/var/run/ovn/ovnsb_db.sock
++ sbdb_ctl=/var/run/ovn/ovnsb_db.ctl
+ start-ovnkube-node 4 29103 29105
+ local log_level=4
+ local metrics_port=29103
+ local ovn_metrics_port=29105
+ [[ 3 -ne 3 ]]
+ cni-bin-copy
+ . /host/etc/os-release
++ NAME='Red Hat Enterprise Linux CoreOS'
++ ID=rhcos
++ ID_LIKE='rhel fedora'
++ VERSION=416.94.202407030122-0
++ VERSION_ID=4.16
++ VARIANT=CoreOS
++ VARIANT_ID=coreos
++ PLATFORM_ID=platform:el9
++ PRETTY_NAME='Red Hat Enterprise Linux CoreOS 416.94.202407030122-0'
++ ANSI_COLOR='0;31'
++ CPE_NAME=cpe:/o:redhat:enterprise_linux:9::baseos::coreos
++ HOME_URL=https://www.redhat.com/
++ DOCUMENTATION_URL=https://docs.okd.io/latest/welcome/index.html
++ BUG_REPORT_URL=https://access.redhat.com/labs/rhir/
++ REDHAT_BUGZILLA_PRODUCT='OpenShift Container Platform'
++ REDHAT_BUGZILLA_PRODUCT_VERSION=4.16
++ REDHAT_SUPPORT_PRODUCT='OpenShift Container Platform'
++ REDHAT_SUPPORT_PRODUCT_VERSION=4.16
++ OPENSHIFT_VERSION=4.16
++ RHEL_VERSION=9.4
++ OSTREE_VERSION=416.94.202407030122-0
+ rhelmajor=
+ case "${ID}" in
++ echo cpe:/o:redhat:enterprise_linux:9::baseos::coreos
++ cut -f 5 -d :
+ RHEL_VERSION=9
++ echo 9
++ sed -E 's/([0-9]+)\.{1}[0-9]+(\.[0-9]+)?/\1/'
+ rhelmajor=9
+ sourcedir=/usr/libexec/cni/
+ case "${rhelmajor}" in
+ sourcedir=/usr/libexec/cni/rhel9
+ cp -f /usr/libexec/cni/rhel9/ovn-k8s-cni-overlay /cni-bin-dir/
++ date '+%m%d %H:%M:%S.%N'
+ echo 'I0719 01:46:01.203131904 - disable conntrack on geneve port'
I0719 01:46:01.203131904 - disable conntrack on geneve port
+ iptables -t raw -A PREROUTING -p udp --dport 6081 -j NOTRACK
+ iptables -t raw -A OUTPUT -p udp --dport 6081 -j NOTRACK
+ ip6tables -t raw -A PREROUTING -p udp --dport 6081 -j NOTRACK
+ ip6tables -t raw -A OUTPUT -p udp --dport 6081 -j NOTRACK
++ date '+%m%d %H:%M:%S.%N'
I0719 01:46:01.216767060 - starting ovnkube-node
+ echo 'I0719 01:46:01.216767060 - starting ovnkube-node'
+ '[' shared == shared ']'
+ gateway_mode_flags='--gateway-mode shared --gateway-interface br-ex'
+ export_network_flows_flags=
+ [[ -n '' ]]
+ [[ -n '' ]]
+ [[ -n '' ]]
+ [[ -n '' ]]
+ [[ -n '' ]]
+ [[ -n '' ]]
+ gw_interface_flag=
+ '[' -d /sys/class/net/br-ex1 ']'
+ node_mgmt_port_netdev_flags=
+ [[ -n '' ]]
+ [[ -n '' ]]
+ multi_network_enabled_flag=
+ [[ true == \t\r\u\e ]]
+ multi_network_enabled_flag=--enable-multi-network
+ multi_network_policy_enabled_flag=
+ [[ false == \t\r\u\e ]]
+ admin_network_policy_enabled_flag=
+ [[ true == \t\r\u\e ]]
+ admin_network_policy_enabled_flag=--enable-admin-network-policy
+ dns_name_resolver_enabled_flag=
+ [[ false == \t\r\u\e ]]
+ ip_forwarding_flag=
+ '[' '' == Global ']'
+ ip_forwarding_flag=--disable-forwarding
+ NETWORK_NODE_IDENTITY_ENABLE=
+ [[ true == \t\r\u\e ]]
+ NETWORK_NODE_IDENTITY_ENABLE='
      --bootstrap-kubeconfig=/var/lib/kubelet/kubeconfig
      --cert-dir=/etc/ovn/ovnkube-node-certs
      --cert-duration=24h
    '
+ ovn_v4_join_subnet_opt=
+ [[ '' != '' ]]
+ ovn_v6_join_subnet_opt=
+ [[ '' != '' ]]
+ exec /usr/bin/ovnkube --init-ovnkube-controller 00-50-56-8a-fb-ea --init-node 00-50-56-8a-fb-ea --config-file=/run/ovnkube-config/ovnkube.conf --ovn-empty-lb-events --loglevel 4 --inactivity-probe=180000 --gateway-mode shared --gateway-interface br-ex --metrics-bind-address 127.0.0.1:29103 --ovn-metrics-bind-address 127.0.0.1:29105 --metrics-enable-pprof --metrics-enable-config-duration --export-ovs-metrics --disable-snat-multiple-gws --enable-multi-network --enable-admin-network-policy --enable-multicast --zone 00-50-56-8a-fb-ea --enable-interconnect --acl-logging-rate-limit 20 --disable-forwarding --bootstrap-kubeconfig=/var/lib/kubelet/kubeconfig --cert-dir=/etc/ovn/ovnkube-node-certs --cert-duration=24h
I0719 01:46:01.245857   37437 config.go:2178] Parsed config file /run/ovnkube-config/ovnkube.conf
I0719 01:46:01.245996   37437 config.go:2179] Parsed config: {Default:{MTU:8900 RoutableMTU:0 ConntrackZone:64000 HostMasqConntrackZone:0 OVNMasqConntrackZone:0 HostNodePortConntrackZone:0 ReassemblyConntrackZone:0 EncapType:geneve EncapIP: EncapPort:6081 InactivityProbe:100000 OpenFlowProbe:180 OfctrlWaitBeforeClear:0 MonitorAll:true LFlowCacheEnable:true LFlowCacheLimit:0 LFlowCacheLimitKb:1048576 RawClusterSubnets:10.128.0.0/14/23 ClusterSubnets:[] EnableUDPAggregation:true Zone:global} Logging:{File: CNIFile: LibovsdbFile:/var/log/ovnkube/libovsdb.log Level:4 LogFileMaxSize:100 LogFileMaxBackups:5 LogFileMaxAge:0 ACLLoggingRateLimit:20} Monitoring:{RawNetFlowTargets: RawSFlowTargets: RawIPFIXTargets: NetFlowTargets:[] SFlowTargets:[] IPFIXTargets:[]} IPFIX:{Sampling:400 CacheActiveTimeout:60 CacheMaxFlows:0} CNI:{ConfDir:/etc/cni/net.d Plugin:ovn-k8s-cni-overlay} OVNKubernetesFeature:{EnableAdminNetworkPolicy:true EnableEgressIP:true EgressIPReachabiltyTotalTimeout:1 EnableEgressFirewall:true EnableEgressQoS:true EnableEgressService:true EgressIPNodeHealthCheckPort:9107 EnableMultiNetwork:true EnableMultiNetworkPolicy:false EnableStatelessNetPol:false EnableInterconnect:false EnableMultiExternalGateway:true EnablePersistentIPs:false EnableDNSNameResolver:false EnableServiceTemplateSupport:false} Kubernetes:{BootstrapKubeconfig: CertDir: CertDuration:10m0s Kubeconfig: CACert: CAData:[] APIServer:https://api-int.vmware-cluster.openshift.lan:6443 Token: TokenFile: CompatServiceCIDR: RawServiceCIDRs:172.30.0.0/16 ServiceCIDRs:[] OVNConfigNamespace:openshift-ovn-kubernetes OVNEmptyLbEvents:false PodIP: RawNoHostSubnetNodes: NoHostSubnetNodes:<nil> HostNetworkNamespace:openshift-host-network PlatformType:BareMetal HealthzBindAddress:0.0.0.0:10256 CompatMetricsBindAddress: CompatOVNMetricsBindAddress: CompatMetricsEnablePprof:false DNSServiceNamespace:openshift-dns DNSServiceName:dns-default} Metrics:{BindAddress: OVNMetricsBindAddress: ExportOVSMetrics:false EnablePprof:false NodeServerPrivKey: NodeServerCert: EnableConfigDuration:false EnableScaleMetrics:false} OvnNorth:{Address: PrivKey: Cert: CACert: CertCommonName: Scheme: ElectionTimer:0 northbound:false exec:<nil>} OvnSouth:{Address: PrivKey: Cert: CACert: CertCommonName: Scheme: ElectionTimer:0 northbound:false exec:<nil>} Gateway:{Mode:shared Interface: EgressGWInterface: NextHop: VLANID:0 NodeportEnable:true DisableSNATMultipleGWs:false V4JoinSubnet:100.64.0.0/16 V6JoinSubnet:fd98::/64 V4MasqueradeSubnet:169.254.169.0/29 V6MasqueradeSubnet:fd69::/125 MasqueradeIPs:{V4OVNMasqueradeIP:169.254.169.1 V6OVNMasqueradeIP:fd69::1 V4HostMasqueradeIP:169.254.169.2 V6HostMasqueradeIP:fd69::2 V4HostETPLocalMasqueradeIP:169.254.169.3 V6HostETPLocalMasqueradeIP:fd69::3 V4DummyNextHopMasqueradeIP:169.254.169.4 V6DummyNextHopMasqueradeIP:fd69::4 V4OVNServiceHairpinMasqueradeIP:169.254.169.5 V6OVNServiceHairpinMasqueradeIP:fd69::5} DisablePacketMTUCheck:false RouterSubnet: SingleNode:false DisableForwarding:false AllowNoUplink:false} MasterHA:{ElectionLeaseDuration:137 ElectionRenewDeadline:107 ElectionRetryPeriod:26} ClusterMgrHA:{ElectionLeaseDuration:137 ElectionRenewDeadline:107 ElectionRetryPeriod:26} HybridOverlay:{Enabled:false RawClusterSubnets: ClusterSubnets:[] VXLANPort:4789} OvnKubeNode:{Mode:full DPResourceDeviceIdsMap:map[] MgmtPortNetdev: MgmtPortDPResourceName:} ClusterManager:{V4TransitSwitchSubnet:100.88.0.0/16 V6TransitSwitchSubnet:fd97::/64}}
I0719 01:46:01.248002   37437 certificate_store.go:130] Loading cert/key pair from "/etc/ovn/ovnkube-node-certs/ovnkube-client-current.pem".
I0719 01:46:01.248239   37437 certificate_store.go:130] Loading cert/key pair from "/etc/ovn/ovnkube-node-certs/ovnkube-client-current.pem".
I0719 01:46:01.248369   37437 certificate_manager.go:356] kubernetes.io/kube-apiserver-client: Certificate rotation is enabled
I0719 01:46:01.248397   37437 kube.go:358] Waiting for certificate
I0719 01:46:01.248424   37437 kube.go:365] Certificate found
I0719 01:46:01.248474   37437 certificate_manager.go:356] kubernetes.io/kube-apiserver-client: Certificate expiration is 2024-07-19 19:40:48 +0000 UTC, rotation deadline is 2024-07-19 16:33:25.110778537 +0000 UTC
I0719 01:46:01.248537   37437 certificate_manager.go:356] kubernetes.io/kube-apiserver-client: Waiting 14h47m23.862244798s for next certificate rotation
I0719 01:46:01.249056   37437 cert_rotation.go:137] Starting client certificate rotation controller
I0719 01:46:01.250282   37437 metrics.go:532] Starting metrics server at address "127.0.0.1:29103"
I0719 01:46:01.251318   37437 libovsdb.go:62] Client for OVN_Northbound using log verbosity 4 with lumberjack &lumberjack.Logger{Filename:"/var/log/ovnkube/libovsdb.log", MaxSize:100, MaxAge:0, MaxBackups:5, LocalTime:false, Compress:true, size:0, file:(*os.File)(nil), mu:sync.Mutex{state:0, sema:0x0}, millCh:(chan bool)(nil), startMill:sync.Once{done:0x0, m:sync.Mutex{state:0, sema:0x0}}}
I0719 01:46:01.252147   37437 node_network_controller_manager.go:98] Starting the node network controller manager, Mode: full
I0719 01:46:01.252222   37437 factory.go:405] Starting watch factory
I0719 01:46:01.253057   37437 reflector.go:289] Starting reflector *v1.Service (0s) from k8s.io/client-go/informers/factory.go:159
I0719 01:46:01.253111   37437 reflector.go:325] Listing and watching *v1.Service from k8s.io/client-go/informers/factory.go:159
I0719 01:46:01.253664   37437 reflector.go:289] Starting reflector *v1.Node (0s) from k8s.io/client-go/informers/factory.go:159
I0719 01:46:01.253680   37437 reflector.go:325] Listing and watching *v1.Node from k8s.io/client-go/informers/factory.go:159
I0719 01:46:01.253725   37437 reflector.go:289] Starting reflector *v1.Namespace (0s) from k8s.io/client-go/informers/factory.go:159
I0719 01:46:01.253781   37437 reflector.go:325] Listing and watching *v1.Namespace from k8s.io/client-go/informers/factory.go:159
I0719 01:46:01.253998   37437 reflector.go:289] Starting reflector *v1.EndpointSlice (0s) from k8s.io/client-go/informers/factory.go:159
I0719 01:46:01.254017   37437 reflector.go:325] Listing and watching *v1.EndpointSlice from k8s.io/client-go/informers/factory.go:159
I0719 01:46:01.254352   37437 reflector.go:289] Starting reflector *v1.NetworkPolicy (0s) from k8s.io/client-go/informers/factory.go:159
I0719 01:46:01.255028   37437 reflector.go:325] Listing and watching *v1.NetworkPolicy from k8s.io/client-go/informers/factory.go:159
I0719 01:46:01.254998   37437 reflector.go:289] Starting reflector *v1.Pod (0s) from k8s.io/client-go/informers/factory.go:159
I0719 01:46:01.255117   37437 reflector.go:325] Listing and watching *v1.Pod from k8s.io/client-go/informers/factory.go:159
I0719 01:46:01.257915   37437 metrics.go:532] Starting metrics server at address "127.0.0.1:29105"
I0719 01:46:01.268650   37437 reflector.go:351] Caches populated for *v1.Node from k8s.io/client-go/informers/factory.go:159
I0719 01:46:01.269645   37437 reflector.go:351] Caches populated for *v1.NetworkPolicy from k8s.io/client-go/informers/factory.go:159
I0719 01:46:01.272700   37437 reflector.go:351] Caches populated for *v1.Namespace from k8s.io/client-go/informers/factory.go:159
I0719 01:46:01.272799   37437 reflector.go:351] Caches populated for *v1.EndpointSlice from k8s.io/client-go/informers/factory.go:159
I0719 01:46:01.274951   37437 ovn_db.go:374] Found OVN DB Pod running on this node. Registering OVN DB Metrics
I0719 01:46:01.275262   37437 reflector.go:351] Caches populated for *v1.Service from k8s.io/client-go/informers/factory.go:159
I0719 01:46:01.279660   37437 ovn_db.go:329] /var/run/openvswitch/ovnnb_db.sock getting info failed: stat /var/run/openvswitch/ovnnb_db.sock: no such file or directory
I0719 01:46:01.279703   37437 ovn_db.go:326] ovnnb_db.sock found at /var/run/ovn/
I0719 01:46:01.297215   37437 libovsdb.go:62] Client for OVN_Southbound using log verbosity 4 with lumberjack &lumberjack.Logger{Filename:"/var/log/ovnkube/libovsdb.log", MaxSize:100, MaxAge:0, MaxBackups:5, LocalTime:false, Compress:true, size:0, file:(*os.File)(nil), mu:sync.Mutex{state:0, sema:0x0}, millCh:(chan bool)(nil), startMill:sync.Once{done:0x0, m:sync.Mutex{state:0, sema:0x0}}}
I0719 01:46:01.304075   37437 ovn_db.go:421] Found db is standalone, don't register db_cluster metrics
I0719 01:46:01.307470   37437 network_controller_manager.go:300] Starting the ovnkube controller
I0719 01:46:01.307492   37437 network_controller_manager.go:305] Waiting up to 5m0s for NBDB zone to match: 00-50-56-8a-fb-ea
I0719 01:46:01.307570   37437 network_controller_manager.go:325] NBDB zone sync took: 68.05µs
I0719 01:46:01.307581   37437 factory.go:405] Starting watch factory
I0719 01:46:01.333597   37437 reflector.go:351] Caches populated for *v1.Pod from k8s.io/client-go/informers/factory.go:159
I0719 01:46:01.353476   37437 reflector.go:289] Starting reflector *v1alpha1.BaselineAdminNetworkPolicy (0s) from sigs.k8s.io/network-policy-api/pkg/client/informers/externalversions/factory.go:141
I0719 01:46:01.353506   37437 reflector.go:325] Listing and watching *v1alpha1.BaselineAdminNetworkPolicy from sigs.k8s.io/network-policy-api/pkg/client/informers/externalversions/factory.go:141
I0719 01:46:01.353481   37437 reflector.go:289] Starting reflector *v1alpha1.AdminNetworkPolicy (0s) from sigs.k8s.io/network-policy-api/pkg/client/informers/externalversions/factory.go:141
I0719 01:46:01.353555   37437 reflector.go:325] Listing and watching *v1alpha1.AdminNetworkPolicy from sigs.k8s.io/network-policy-api/pkg/client/informers/externalversions/factory.go:141
I0719 01:46:01.355961   37437 reflector.go:351] Caches populated for *v1alpha1.BaselineAdminNetworkPolicy from sigs.k8s.io/network-policy-api/pkg/client/informers/externalversions/factory.go:141
I0719 01:46:01.356459   37437 reflector.go:351] Caches populated for *v1alpha1.AdminNetworkPolicy from sigs.k8s.io/network-policy-api/pkg/client/informers/externalversions/factory.go:141
I0719 01:46:01.408004   37437 reflector.go:289] Starting reflector *v1.EgressIP (0s) from github.com/openshift/ovn-kubernetes/go-controller/pkg/crd/egressip/v1/apis/informers/externalversions/factory.go:140
I0719 01:46:01.408029   37437 reflector.go:325] Listing and watching *v1.EgressIP from github.com/openshift/ovn-kubernetes/go-controller/pkg/crd/egressip/v1/apis/informers/externalversions/factory.go:140
I0719 01:46:01.410007   37437 reflector.go:351] Caches populated for *v1.EgressIP from github.com/openshift/ovn-kubernetes/go-controller/pkg/crd/egressip/v1/apis/informers/externalversions/factory.go:140
I0719 01:46:01.453636   37437 reflector.go:289] Starting reflector *v1.EgressFirewall (0s) from github.com/openshift/ovn-kubernetes/go-controller/pkg/crd/egressfirewall/v1/apis/informers/externalversions/factory.go:140
I0719 01:46:01.453667   37437 reflector.go:325] Listing and watching *v1.EgressFirewall from github.com/openshift/ovn-kubernetes/go-controller/pkg/crd/egressfirewall/v1/apis/informers/externalversions/factory.go:140
I0719 01:46:01.456262   37437 reflector.go:351] Caches populated for *v1.EgressFirewall from github.com/openshift/ovn-kubernetes/go-controller/pkg/crd/egressfirewall/v1/apis/informers/externalversions/factory.go:140
I0719 01:46:01.509127   37437 reflector.go:289] Starting reflector *v1.EgressQoS (0s) from github.com/openshift/ovn-kubernetes/go-controller/pkg/crd/egressqos/v1/apis/informers/externalversions/factory.go:140
I0719 01:46:01.509151   37437 reflector.go:325] Listing and watching *v1.EgressQoS from github.com/openshift/ovn-kubernetes/go-controller/pkg/crd/egressqos/v1/apis/informers/externalversions/factory.go:140
I0719 01:46:01.511292   37437 reflector.go:351] Caches populated for *v1.EgressQoS from github.com/openshift/ovn-kubernetes/go-controller/pkg/crd/egressqos/v1/apis/informers/externalversions/factory.go:140
I0719 01:46:01.553871   37437 reflector.go:289] Starting reflector *v1.EgressService (0s) from github.com/openshift/ovn-kubernetes/go-controller/pkg/crd/egressservice/v1/apis/informers/externalversions/factory.go:140
I0719 01:46:01.553897   37437 reflector.go:325] Listing and watching *v1.EgressService from github.com/openshift/ovn-kubernetes/go-controller/pkg/crd/egressservice/v1/apis/informers/externalversions/factory.go:140
I0719 01:46:01.556151   37437 reflector.go:351] Caches populated for *v1.EgressService from github.com/openshift/ovn-kubernetes/go-controller/pkg/crd/egressservice/v1/apis/informers/externalversions/factory.go:140
I0719 01:46:01.609887   37437 reflector.go:289] Starting reflector *v1.AdminPolicyBasedExternalRoute (0s) from github.com/openshift/ovn-kubernetes/go-controller/pkg/crd/adminpolicybasedroute/v1/apis/informers/externalversions/factory.go:140
I0719 01:46:01.609910   37437 reflector.go:325] Listing and watching *v1.AdminPolicyBasedExternalRoute from github.com/openshift/ovn-kubernetes/go-controller/pkg/crd/adminpolicybasedroute/v1/apis/informers/externalversions/factory.go:140
I0719 01:46:01.611941   37437 reflector.go:351] Caches populated for *v1.AdminPolicyBasedExternalRoute from github.com/openshift/ovn-kubernetes/go-controller/pkg/crd/adminpolicybasedroute/v1/apis/informers/externalversions/factory.go:140
I0719 01:46:01.654519   37437 default_node_network_controller.go:133] Enable node proxy healthz server on 0.0.0.0:10256
I0719 01:46:01.654678   37437 default_node_network_controller.go:684] Starting the default node network controller
I0719 01:46:01.654700   37437 ovs.go:159] Exec(9): /usr/bin/ovs-vsctl --timeout=15 --no-heading --data=bare --format=csv --columns name list interface
I0719 01:46:01.660924   37437 ovs.go:162] Exec(9): stdout: "ovn-48ef73-0\nens192\nbr-ex\novn-0a949b-0\novn-k8s-mp0\novn-0af759-0\novn-58c4d9-0\npatch-br-int-to-br-ex_00-50-56-8a-fb-ea\novn-9733f6-0\npatch-br-ex_00-50-56-8a-fb-ea-to-br-int\nbr-int\n"
I0719 01:46:01.660964   37437 ovs.go:163] Exec(9): stderr: ""
I0719 01:46:01.660949   37437 ovs.go:162] Exec(8): stdout: ""
I0719 01:46:01.661007   37437 ovs.go:163] Exec(8): stderr: ""
I0719 01:46:01.661027   37437 node_network_controller_manager.go:251] CheckForStaleOVSInternalPorts took 6.39155ms
I0719 01:46:01.661045   37437 ovs.go:159] Exec(10): /usr/bin/ovs-vsctl --timeout=15 --columns=name,external_ids --data=bare --no-headings --format=csv find Interface external_ids:sandbox!="" external_ids:vf-netdev-name!=""
I0719 01:46:01.661062   37437 ovs.go:159] Exec(11): /usr/bin/ovs-ofctl dump-flows br-ex
I0719 01:46:01.666716   37437 ovs.go:162] Exec(11): stdout: "NXST_FLOW reply (xid=0x4):\n cookie=0xdeff105, duration=1576.553s, table=0, n_packets=5, n_bytes=210, idle_age=1561, priority=10,in_port=2,dl_src=00:50:56:8a:fb:ea actions=NORMAL\n cookie=0xdeff105, duration=1576.553s, table=0, n_packets=0, n_bytes=0, idle_age=1576, priority=9,in_port=2 actions=drop\n cookie=0x0, duration=1652.758s, table=0, n_packets=9821789, n_bytes=11909192667, idle_age=0, priority=0 actions=NORMAL\n"
I0719 01:46:01.666748   37437 ovs.go:163] Exec(11): stderr: ""
I0719 01:46:01.666977   37437 ovs.go:162] Exec(10): stdout: ""
I0719 01:46:01.667004   37437 ovs.go:163] Exec(10): stderr: ""
I0719 01:46:01.671088   37437 ovs.go:159] Exec(12): /usr/bin/ovn-sbctl --timeout=15 --no-leader-only get SB_Global . options:name
I0719 01:46:01.677972   37437 ovs.go:162] Exec(12): stdout: "\"00-50-56-8a-fb-ea\"\n"
I0719 01:46:01.678011   37437 ovs.go:163] Exec(12): stderr: ""
I0719 01:46:01.678069   37437 config.go:1590] Exec: /usr/bin/ovs-vsctl --timeout=15 set Open_vSwitch . external_ids:ovn-remote="unix:/var/run/ovn/ovnsb_db.sock"
I0719 01:46:01.685785   37437 ovs.go:159] Exec(13): /usr/bin/ovs-vsctl --timeout=15 set Open_vSwitch . external_ids:ovn-encap-type=geneve external_ids:ovn-encap-ip=10.10.25.235 external_ids:ovn-remote-probe-interval=180000 external_ids:ovn-openflow-probe-interval=180 other_config:bundle-idle-timeout=180 external_ids:hostname="00-50-56-8a-fb-ea" external_ids:ovn-is-interconn=true external_ids:ovn-monitor-all=true external_ids:ovn-ofctrl-wait-before-clear=0 external_ids:ovn-enable-lflow-cache=true external_ids:ovn-set-local-ip="true" external_ids:ovn-memlimit-lflow-cache-kb=1048576
I0719 01:46:01.694256   37437 ovs.go:162] Exec(13): stdout: ""
I0719 01:46:01.694287   37437 ovs.go:163] Exec(13): stderr: ""
I0719 01:46:01.694306   37437 ovs.go:159] Exec(14): /usr/bin/ovs-vsctl --timeout=15 -- clear bridge br-int netflow -- clear bridge br-int sflow -- clear bridge br-int ipfix
I0719 01:46:01.700567   37437 ovs.go:162] Exec(14): stdout: ""
I0719 01:46:01.700589   37437 ovs.go:163] Exec(14): stderr: ""
I0719 01:46:01.704625   37437 default_node_network_controller.go:778] Node 00-50-56-8a-fb-ea ready for ovn initialization with subnet 10.130.0.0/23
I0719 01:46:01.704719   37437 ovs.go:159] Exec(15): /usr/bin/ovs-vsctl --timeout=15 --no-headings --data bare --format csv --columns type,name find Interface name=ovn-k8s-mp0
I0719 01:46:01.709910   37437 network_controller_manager.go:336] Waiting up to 5m0s for a node to have "00-50-56-8a-fb-ea" zone
I0719 01:46:01.709967   37437 network_controller_manager.go:359] Waiting for node in zone sync took: 34.095µs
I0719 01:46:01.710188   37437 ovs.go:159] Exec(16): /usr/bin/ovsdb-client list-columns unix:/var/run/ovn/ovnnb_db.sock --data=bare --no-heading --format=json OVN_Northbound Load_Balancer
I0719 01:46:01.711928   37437 ovs.go:162] Exec(15): stdout: "internal,ovn-k8s-mp0\n"
I0719 01:46:01.711946   37437 ovs.go:163] Exec(15): stderr: ""
I0719 01:46:01.711959   37437 ovs.go:159] Exec(17): /usr/bin/ovs-vsctl --timeout=15 --no-headings --data bare --format csv --columns type,name find Interface name=ovn-k8s-mp0_0
I0719 01:46:01.717588   37437 ovs.go:162] Exec(17): stdout: ""
I0719 01:46:01.717603   37437 ovs.go:163] Exec(17): stderr: ""
I0719 01:46:01.717678   37437 ovs.go:162] Exec(16): stdout: "{\"data\":[[\"health_check\",{\"key\":{\"refTable\":\"Load_Balancer_Health_Check\",\"type\":\"uuid\"},\"max\":\"unlimited\",\"min\":0}],[\"external_ids\",{\"key\":\"string\",\"max\":\"unlimited\",\"min\":0,\"value\":\"string\"}],[\"_uuid\",\"uuid\"],[\"selection_fields\",{\"key\":{\"enum\":[\"set\",[\"eth_dst\",\"eth_src\",\"ip_dst\",\"ip_src\",\"tp_dst\",\"tp_src\"]],\"type\":\"string\"},\"max\":\"unlimited\",\"min\":0}],[\"vips\",{\"key\":\"string\",\"max\":\"unlimited\",\"min\":0,\"value\":\"string\"}],[\"_version\",\"uuid\"],[\"ip_port_mappings\",{\"key\":\"string\",\"max\":\"unlimited\",\"min\":0,\"value\":\"string\"}],[\"name\",\"string\"],[\"options\",{\"key\":\"string\",\"max\":\"unlimited\",\"min\":0,\"value\":\"string\"}],[\"protocol\",{\"key\":{\"enum\":[\"set\",[\"sctp\",\"tcp\",\"udp\"]],\"type\":\"string\"},\"min\":0}]],\"headings\":[\"Column\",\"Type\"]}\n"
I0719 01:46:01.717745   37437 ovs.go:163] Exec(16): stderr: ""
I0719 01:46:01.717719   37437 ovs.go:159] Exec(18): /usr/bin/ovs-vsctl --timeout=15 -- --if-exists del-port br-int k8s-00-50-56-8a -- --may-exist add-port br-int ovn-k8s-mp0 -- set interface ovn-k8s-mp0 type=internal mtu_request=8900 external-ids:iface-id=k8s-00-50-56-8a-fb-ea
I0719 01:46:01.717916   37437 network_controller_manager.go:220] SCTP support detected in OVN
I0719 01:46:01.718050   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Meter Row:map[bands:{GoSet:[{GoUUID:f8c9e699-aa60-4aba-98cf-487d6327250d}]} fair:{GoSet:[true]} unit:pktps] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {b85643a3-9b0c-4fd2-ad09-494aa6dabd96}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.718175   37437 transact.go:42] Configuring OVN: [{Op:update Table:Meter Row:map[bands:{GoSet:[{GoUUID:f8c9e699-aa60-4aba-98cf-487d6327250d}]} fair:{GoSet:[true]} unit:pktps] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {b85643a3-9b0c-4fd2-ad09-494aa6dabd96}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.722063   37437 ovnkube_controller.go:1230] Config duration recorder: updated measurement rate to approx 1 in every 60 requests
I0719 01:46:01.722238   37437 services_controller.go:60] Creating event broadcaster
I0719 01:46:01.722474   37437 default_network_controller.go:328] Starting the default network controller
I0719 01:46:01.722611   37437 address_set_sync.go:394] SyncAddressSets found 0 stale address sets, 0 of them were ignored
I0719 01:46:01.725042   37437 ovs.go:162] Exec(18): stdout: ""
I0719 01:46:01.725058   37437 ovs.go:163] Exec(18): stderr: ""
I0719 01:46:01.725069   37437 ovs.go:159] Exec(19): /usr/bin/ovs-vsctl --timeout=15 --if-exists get interface ovn-k8s-mp0 mac_in_use
I0719 01:46:01.725589   37437 acl_sync.go:167] Updating Tier of existing ACLs...
I0719 01:46:01.725658   37437 acl_sync.go:192] Updating tier's of all ACLs in cluster took 14.057µs
I0719 01:46:01.725890   37437 port_group_sync.go:309] SyncPortGroups found 0 stale port groups
I0719 01:46:01.729059   37437 default_network_controller.go:364] Existing number of nodes: 6
I0719 01:46:01.729085   37437 ovs.go:159] Exec(20): /usr/bin/ovn-nbctl --timeout=15 --columns=_uuid list Load_Balancer_Group
I0719 01:46:01.731718   37437 ovs.go:162] Exec(19): stdout: "\"be:6d:32:1d:e9:29\"\n"
I0719 01:46:01.731786   37437 ovs.go:163] Exec(19): stderr: ""
I0719 01:46:01.731807   37437 ovs.go:159] Exec(21): /usr/bin/ovs-vsctl --timeout=15 set interface ovn-k8s-mp0 mac=be\:6d\:32\:1d\:e9\:29
I0719 01:46:01.733961   37437 ovs.go:162] Exec(20): stdout: "_uuid               : aea29a04-5376-45bc-b303-62d4a3f5c7bb\n\n_uuid               : 2400c21d-35b5-4059-bdc0-cfe46ebce829\n\n_uuid               : e2fd0a53-3438-47ef-bc25-2dcb5c7ffe1c\n"
I0719 01:46:01.733997   37437 ovs.go:163] Exec(20): stderr: ""
I0719 01:46:01.734055   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Load_Balancer_Group Row:map[name:clusterLBGroup] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {2400c21d-35b5-4059-bdc0-cfe46ebce829}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.734087   37437 transact.go:42] Configuring OVN: [{Op:update Table:Load_Balancer_Group Row:map[name:clusterLBGroup] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {2400c21d-35b5-4059-bdc0-cfe46ebce829}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.734444   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Load_Balancer_Group Row:map[name:clusterSwitchLBGroup] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {aea29a04-5376-45bc-b303-62d4a3f5c7bb}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.734475   37437 transact.go:42] Configuring OVN: [{Op:update Table:Load_Balancer_Group Row:map[name:clusterSwitchLBGroup] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {aea29a04-5376-45bc-b303-62d4a3f5c7bb}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.734694   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Load_Balancer_Group Row:map[name:clusterRouterLBGroup] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {e2fd0a53-3438-47ef-bc25-2dcb5c7ffe1c}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.734717   37437 transact.go:42] Configuring OVN: [{Op:update Table:Load_Balancer_Group Row:map[name:clusterRouterLBGroup] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {e2fd0a53-3438-47ef-bc25-2dcb5c7ffe1c}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.734960   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Meter Row:map[bands:{GoSet:[{GoUUID:49e6966c-b80b-4b72-a946-9a65c1ce976f}]} fair:{GoSet:[true]} unit:pktps] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {44185e9e-b008-45d9-aab7-226f48bb3403}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.735022   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Meter Row:map[bands:{GoSet:[{GoUUID:49e6966c-b80b-4b72-a946-9a65c1ce976f}]} fair:{GoSet:[true]} unit:pktps] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {b5f8f447-56bd-4d16-8389-790cd663d183}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.735064   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Meter Row:map[bands:{GoSet:[{GoUUID:49e6966c-b80b-4b72-a946-9a65c1ce976f}]} fair:{GoSet:[true]} unit:pktps] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {57c3ff71-55ca-4ac1-8405-a5698e581dd7}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.735108   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Meter Row:map[bands:{GoSet:[{GoUUID:49e6966c-b80b-4b72-a946-9a65c1ce976f}]} fair:{GoSet:[true]} unit:pktps] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {aeaa2650-8602-42c8-bb11-d8d11a3ce4da}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.735148   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Meter Row:map[bands:{GoSet:[{GoUUID:49e6966c-b80b-4b72-a946-9a65c1ce976f}]} fair:{GoSet:[true]} unit:pktps] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {231e4847-b8a3-4bea-9408-796fdc6a183e}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.735190   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Meter Row:map[bands:{GoSet:[{GoUUID:49e6966c-b80b-4b72-a946-9a65c1ce976f}]} fair:{GoSet:[true]} unit:pktps] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {9c52aaa8-c41e-4efd-b464-6fb15cde39fc}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.735229   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Meter Row:map[bands:{GoSet:[{GoUUID:49e6966c-b80b-4b72-a946-9a65c1ce976f}]} fair:{GoSet:[true]} unit:pktps] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {adcb66ce-820c-4142-942c-5425432423a9}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.735267   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Meter Row:map[bands:{GoSet:[{GoUUID:49e6966c-b80b-4b72-a946-9a65c1ce976f}]} fair:{GoSet:[true]} unit:pktps] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {afce96a8-658b-4f0f-9acd-a2ee997616f7}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.735306   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Meter Row:map[bands:{GoSet:[{GoUUID:49e6966c-b80b-4b72-a946-9a65c1ce976f}]} fair:{GoSet:[true]} unit:pktps] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {50f3e512-b7e8-4eb3-8fea-eccc03adc9bf}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.735351   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Copp Row:map[meters:{GoMap:map[arp:arp-rate-limiter arp-resolve:arp-resolve-rate-limiter bfd:bfd-rate-limiter event-elb:event-elb-rate-limiter icmp4-error:icmp4-error-rate-limiter icmp6-error:icmp6-error-rate-limiter reject:reject-rate-limiter svc-monitor:svc-monitor-rate-limiter tcp-reset:tcp-reset-rate-limiter]} name:ovnkube-default] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {993b87a7-28f5-463c-84ba-4cb0178f4f2a}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.735392   37437 transact.go:42] Configuring OVN: [{Op:update Table:Meter Row:map[bands:{GoSet:[{GoUUID:49e6966c-b80b-4b72-a946-9a65c1ce976f}]} fair:{GoSet:[true]} unit:pktps] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {44185e9e-b008-45d9-aab7-226f48bb3403}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:update Table:Meter Row:map[bands:{GoSet:[{GoUUID:49e6966c-b80b-4b72-a946-9a65c1ce976f}]} fair:{GoSet:[true]} unit:pktps] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {b5f8f447-56bd-4d16-8389-790cd663d183}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:update Table:Meter Row:map[bands:{GoSet:[{GoUUID:49e6966c-b80b-4b72-a946-9a65c1ce976f}]} fair:{GoSet:[true]} unit:pktps] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {57c3ff71-55ca-4ac1-8405-a5698e581dd7}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:update Table:Meter Row:map[bands:{GoSet:[{GoUUID:49e6966c-b80b-4b72-a946-9a65c1ce976f}]} fair:{GoSet:[true]} unit:pktps] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {aeaa2650-8602-42c8-bb11-d8d11a3ce4da}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:update Table:Meter Row:map[bands:{GoSet:[{GoUUID:49e6966c-b80b-4b72-a946-9a65c1ce976f}]} fair:{GoSet:[true]} unit:pktps] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {231e4847-b8a3-4bea-9408-796fdc6a183e}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:update Table:Meter Row:map[bands:{GoSet:[{GoUUID:49e6966c-b80b-4b72-a946-9a65c1ce976f}]} fair:{GoSet:[true]} unit:pktps] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {9c52aaa8-c41e-4efd-b464-6fb15cde39fc}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:update Table:Meter Row:map[bands:{GoSet:[{GoUUID:49e6966c-b80b-4b72-a946-9a65c1ce976f}]} fair:{GoSet:[true]} unit:pktps] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {adcb66ce-820c-4142-942c-5425432423a9}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:update Table:Meter Row:map[bands:{GoSet:[{GoUUID:49e6966c-b80b-4b72-a946-9a65c1ce976f}]} fair:{GoSet:[true]} unit:pktps] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {afce96a8-658b-4f0f-9acd-a2ee997616f7}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:update Table:Meter Row:map[bands:{GoSet:[{GoUUID:49e6966c-b80b-4b72-a946-9a65c1ce976f}]} fair:{GoSet:[true]} unit:pktps] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {50f3e512-b7e8-4eb3-8fea-eccc03adc9bf}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:update Table:Copp Row:map[meters:{GoMap:map[arp:arp-rate-limiter arp-resolve:arp-resolve-rate-limiter bfd:bfd-rate-limiter event-elb:event-elb-rate-limiter icmp4-error:icmp4-error-rate-limiter icmp6-error:icmp6-error-rate-limiter reject:reject-rate-limiter svc-monitor:svc-monitor-rate-limiter tcp-reset:tcp-reset-rate-limiter]} name:ovnkube-default] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {993b87a7-28f5-463c-84ba-4cb0178f4f2a}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.736128   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Router Row:map[copp:{GoSet:[{GoUUID:993b87a7-28f5-463c-84ba-4cb0178f4f2a}]} external_ids:{GoMap:map[k8s-cluster-router:yes]} options:{GoMap:map[mcast_relay:true]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.736161   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Router Row:map[copp:{GoSet:[{GoUUID:993b87a7-28f5-463c-84ba-4cb0178f4f2a}]} external_ids:{GoMap:map[k8s-cluster-router:yes]} options:{GoMap:map[mcast_relay:true]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.736516   37437 model_client.go:381] Update operations generated as: [{Op:update Table:ACL Row:map[action:drop direction:from-lport external_ids:{GoMap:map[direction:Egress k8s.ovn.org/id:default-network-controller:MulticastCluster:DefaultDeny:Egress k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:MulticastCluster type:DefaultDeny]} log:false match:(ip4.mcast || mldv1 || mldv2 || (ip6.dst[120..127] == 0xff && ip6.dst[116] == 1)) meter:{GoSet:[acl-logging]} name:{GoSet:[]} options:{GoMap:map[apply-after-lb:true]} priority:1011 severity:{GoSet:[]} tier:2] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {9c1239ee-0d4c-497f-b8e3-2a51192fc316}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.736661   37437 model_client.go:381] Update operations generated as: [{Op:update Table:ACL Row:map[action:drop direction:to-lport external_ids:{GoMap:map[direction:Ingress k8s.ovn.org/id:default-network-controller:MulticastCluster:DefaultDeny:Ingress k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:MulticastCluster type:DefaultDeny]} log:false match:(ip4.mcast || mldv1 || mldv2 || (ip6.dst[120..127] == 0xff && ip6.dst[116] == 1)) meter:{GoSet:[acl-logging]} name:{GoSet:[]} options:{GoMap:map[]} priority:1011 severity:{GoSet:[]} tier:2] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {90594073-e263-47d9-813f-aa8fa67423f9}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.736714   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Port_Group Row:map[] Rows:[] Columns:[] Mutations:[{Column:acls Mutator:insert Value:{GoSet:[{GoUUID:9c1239ee-0d4c-497f-b8e3-2a51192fc316} {GoUUID:90594073-e263-47d9-813f-aa8fa67423f9}]}}] Timeout:<nil> Where:[where column _uuid == {cfdb2406-27d3-4869-bb58-7f65e5a726d7}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.736751   37437 transact.go:42] Configuring OVN: [{Op:update Table:ACL Row:map[action:drop direction:from-lport external_ids:{GoMap:map[direction:Egress k8s.ovn.org/id:default-network-controller:MulticastCluster:DefaultDeny:Egress k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:MulticastCluster type:DefaultDeny]} log:false match:(ip4.mcast || mldv1 || mldv2 || (ip6.dst[120..127] == 0xff && ip6.dst[116] == 1)) meter:{GoSet:[acl-logging]} name:{GoSet:[]} options:{GoMap:map[apply-after-lb:true]} priority:1011 severity:{GoSet:[]} tier:2] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {9c1239ee-0d4c-497f-b8e3-2a51192fc316}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:update Table:ACL Row:map[action:drop direction:to-lport external_ids:{GoMap:map[direction:Ingress k8s.ovn.org/id:default-network-controller:MulticastCluster:DefaultDeny:Ingress k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:MulticastCluster type:DefaultDeny]} log:false match:(ip4.mcast || mldv1 || mldv2 || (ip6.dst[120..127] == 0xff && ip6.dst[116] == 1)) meter:{GoSet:[acl-logging]} name:{GoSet:[]} options:{GoMap:map[]} priority:1011 severity:{GoSet:[]} tier:2] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {90594073-e263-47d9-813f-aa8fa67423f9}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Port_Group Row:map[] Rows:[] Columns:[] Mutations:[{Column:acls Mutator:insert Value:{GoSet:[{GoUUID:9c1239ee-0d4c-497f-b8e3-2a51192fc316} {GoUUID:90594073-e263-47d9-813f-aa8fa67423f9}]}}] Timeout:<nil> Where:[where column _uuid == {cfdb2406-27d3-4869-bb58-7f65e5a726d7}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.737284   37437 model_client.go:381] Update operations generated as: [{Op:update Table:ACL Row:map[action:allow direction:from-lport external_ids:{GoMap:map[direction:Egress k8s.ovn.org/id:default-network-controller:MulticastCluster:AllowInterNode:Egress k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:MulticastCluster type:AllowInterNode]} log:false match:inport == @a4743249366342378346 && (ip4.mcast || mldv1 || mldv2 || (ip6.dst[120..127] == 0xff && ip6.dst[116] == 1)) meter:{GoSet:[acl-logging]} name:{GoSet:[]} options:{GoMap:map[apply-after-lb:true]} priority:1012 severity:{GoSet:[]} tier:2] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {a5f03c75-c196-40ee-9264-5a964ad2ff0b}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.737401   37437 model_client.go:381] Update operations generated as: [{Op:update Table:ACL Row:map[action:allow direction:to-lport external_ids:{GoMap:map[direction:Ingress k8s.ovn.org/id:default-network-controller:MulticastCluster:AllowInterNode:Ingress k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:MulticastCluster type:AllowInterNode]} log:false match:outport == @a4743249366342378346 && (ip4.mcast || mldv1 || mldv2 || (ip6.dst[120..127] == 0xff && ip6.dst[116] == 1)) meter:{GoSet:[acl-logging]} name:{GoSet:[]} options:{GoMap:map[]} priority:1012 severity:{GoSet:[]} tier:2] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {604fdc1f-b6a4-4a94-a762-eda1f53c077f}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.737454   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Port_Group Row:map[] Rows:[] Columns:[] Mutations:[{Column:acls Mutator:insert Value:{GoSet:[{GoUUID:a5f03c75-c196-40ee-9264-5a964ad2ff0b} {GoUUID:604fdc1f-b6a4-4a94-a762-eda1f53c077f}]}}] Timeout:<nil> Where:[where column _uuid == {620dbd54-29f5-47b2-949a-b9f74c1cd372}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.737473   37437 transact.go:42] Configuring OVN: [{Op:update Table:ACL Row:map[action:allow direction:from-lport external_ids:{GoMap:map[direction:Egress k8s.ovn.org/id:default-network-controller:MulticastCluster:AllowInterNode:Egress k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:MulticastCluster type:AllowInterNode]} log:false match:inport == @a4743249366342378346 && (ip4.mcast || mldv1 || mldv2 || (ip6.dst[120..127] == 0xff && ip6.dst[116] == 1)) meter:{GoSet:[acl-logging]} name:{GoSet:[]} options:{GoMap:map[apply-after-lb:true]} priority:1012 severity:{GoSet:[]} tier:2] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {a5f03c75-c196-40ee-9264-5a964ad2ff0b}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:update Table:ACL Row:map[action:allow direction:to-lport external_ids:{GoMap:map[direction:Ingress k8s.ovn.org/id:default-network-controller:MulticastCluster:AllowInterNode:Ingress k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:MulticastCluster type:AllowInterNode]} log:false match:outport == @a4743249366342378346 && (ip4.mcast || mldv1 || mldv2 || (ip6.dst[120..127] == 0xff && ip6.dst[116] == 1)) meter:{GoSet:[acl-logging]} name:{GoSet:[]} options:{GoMap:map[]} priority:1012 severity:{GoSet:[]} tier:2] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {604fdc1f-b6a4-4a94-a762-eda1f53c077f}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Port_Group Row:map[] Rows:[] Columns:[] Mutations:[{Column:acls Mutator:insert Value:{GoSet:[{GoUUID:a5f03c75-c196-40ee-9264-5a964ad2ff0b} {GoUUID:604fdc1f-b6a4-4a94-a762-eda1f53c077f}]}}] Timeout:<nil> Where:[where column _uuid == {620dbd54-29f5-47b2-949a-b9f74c1cd372}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.737868   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Switch Row:map[name:join] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {8a07c5b0-3092-44c2-aad5-3b39da1e7f5f}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.737888   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Switch Row:map[name:join] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {8a07c5b0-3092-44c2-aad5-3b39da1e7f5f}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.738095   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Router_Port Row:map[mac:0a:58:64:40:00:01 networks:{GoSet:[100.64.0.1/16]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {b7292467-a44d-4f0f-acba-cd094769a8c1}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.738139   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:b7292467-a44d-4f0f-acba-cd094769a8c1}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.738159   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Router_Port Row:map[mac:0a:58:64:40:00:01 networks:{GoSet:[100.64.0.1/16]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {b7292467-a44d-4f0f-acba-cd094769a8c1}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:b7292467-a44d-4f0f-acba-cd094769a8c1}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.738547   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[router]} options:{GoMap:map[router-port:rtoj-ovn_cluster_router]} port_security:{GoSet:[]} tag_request:{GoSet:[]} type:router] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {a390690c-bcf3-44d5-ac76-c485c0923984}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.738595   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:a390690c-bcf3-44d5-ac76-c485c0923984}]}}] Timeout:<nil> Where:[where column _uuid == {8a07c5b0-3092-44c2-aad5-3b39da1e7f5f}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.738614   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[router]} options:{GoMap:map[router-port:rtoj-ovn_cluster_router]} port_security:{GoSet:[]} tag_request:{GoSet:[]} type:router] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {a390690c-bcf3-44d5-ac76-c485c0923984}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:a390690c-bcf3-44d5-ac76-c485c0923984}]}}] Timeout:<nil> Where:[where column _uuid == {8a07c5b0-3092-44c2-aad5-3b39da1e7f5f}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.738697   37437 ovs.go:162] Exec(21): stdout: ""
I0719 01:46:01.738720   37437 ovs.go:163] Exec(21): stderr: ""
I0719 01:46:01.738895   37437 default_network_controller.go:419] Cleaning External Gateway ECMP routes
I0719 01:46:01.739310   37437 repair.go:33] Syncing exgw routes took 390.482µs
I0719 01:46:01.739344   37437 default_network_controller.go:430] Starting all the Watchers...
I0719 01:46:01.740286   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-nutanix-infra
I0719 01:46:01.740342   37437 namespace.go:100] [openshift-nutanix-infra] adding namespace
I0719 01:46:01.740357   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-kube-scheduler-operator
I0719 01:46:01.740384   37437 namespace.go:100] [openshift-kube-scheduler-operator] adding namespace
I0719 01:46:01.740394   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-kni-infra
I0719 01:46:01.740390   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-storage
I0719 01:46:01.740406   37437 namespace.go:100] [openshift-kni-infra] adding namespace
I0719 01:46:01.740414   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-cluster-samples-operator
I0719 01:46:01.740418   37437 namespace.go:100] [openshift-storage] adding namespace
I0719 01:46:01.740426   37437 namespace.go:100] [openshift-cluster-samples-operator] adding namespace
I0719 01:46:01.740417   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-cloud-controller-manager
I0719 01:46:01.740434   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-cluster-version
I0719 01:46:01.740437   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-dns-operator
I0719 01:46:01.740445   37437 namespace.go:100] [openshift-cluster-version] adding namespace
I0719 01:46:01.740441   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-kube-controller-manager-operator
I0719 01:46:01.740458   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-cloud-platform-infra
I0719 01:46:01.740460   37437 obj_retry.go:502] Add event received for *v1.Namespace kube-system
I0719 01:46:01.740463   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-authentication-operator
I0719 01:46:01.740451   37437 namespace.go:100] [openshift-cloud-controller-manager] adding namespace
I0719 01:46:01.740451   37437 namespace.go:100] [openshift-dns-operator] adding namespace
I0719 01:46:01.740430   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-config-operator
I0719 01:46:01.740488   37437 namespace.go:100] [openshift-kube-controller-manager-operator] adding namespace
I0719 01:46:01.740529   37437 namespace.go:100] [openshift-config-operator] adding namespace
I0719 01:46:01.740434   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-nutanix-infra:v4 k8s.ovn.org/name:openshift-nutanix-infra k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {8af8ba94-fa5b-41b8-8030-1bf3b7b9c19a}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.740563   37437 address_set.go:304] New(8af8ba94-fa5b-41b8-8030-1bf3b7b9c19a/default-network-controller:Namespace:openshift-nutanix-infra:v4/a10781256116209244644) with []
I0719 01:46:01.740574   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-nutanix-infra:v4 k8s.ovn.org/name:openshift-nutanix-infra k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {8af8ba94-fa5b-41b8-8030-1bf3b7b9c19a}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.740454   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-cluster-csi-drivers
I0719 01:46:01.740646   37437 namespace.go:100] [openshift-cluster-csi-drivers] adding namespace
I0719 01:46:01.740469   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-cluster-machine-approver
I0719 01:46:01.740662   37437 namespace.go:100] [openshift-cluster-machine-approver] adding namespace
I0719 01:46:01.740477   37437 namespace.go:100] [kube-system] adding namespace
I0719 01:46:01.740478   37437 namespace.go:100] [openshift-authentication-operator] adding namespace
I0719 01:46:01.740480   37437 namespace.go:100] [openshift-cloud-platform-infra] adding namespace
I0719 01:46:01.740904   37437 namespace.go:104] [openshift-nutanix-infra] adding namespace took 556.192µs
I0719 01:46:01.740917   37437 obj_retry.go:541] Creating *v1.Namespace openshift-nutanix-infra took: 589.841µs
I0719 01:46:01.740925   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-kube-apiserver
I0719 01:46:01.740930   37437 namespace.go:100] [openshift-kube-apiserver] adding namespace
I0719 01:46:01.741071   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.10 10.129.0.8 10.129.0.11 10.128.0.13]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-kube-apiserver:v4 k8s.ovn.org/name:openshift-kube-apiserver k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {9269757a-340c-45bf-828d-361c80cb0226}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.741108   37437 address_set.go:304] New(9269757a-340c-45bf-828d-361c80cb0226/default-network-controller:Namespace:openshift-kube-apiserver:v4/a4531626005796422843) with [10.129.0.11 10.128.0.13 10.129.2.10 10.129.0.8]
I0719 01:46:01.741115   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.10 10.129.0.8 10.129.0.11 10.128.0.13]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-kube-apiserver:v4 k8s.ovn.org/name:openshift-kube-apiserver k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {9269757a-340c-45bf-828d-361c80cb0226}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.741340   37437 route_manager.go:155] Route Manager: netlink route deletion event: "{Ifindex: 6 Dst: 10.130.0.0/23 Src: 10.130.0.2 Gw: <nil> Flags: [] Table: 254 Realm: 0}"
I0719 01:46:01.741365   37437 route_manager.go:155] Route Manager: netlink route deletion event: "{Ifindex: 6 Dst: 10.130.1.255/32 Src: 10.130.0.2 Gw: <nil> Flags: [] Table: 255 Realm: 0}"
I0719 01:46:01.741381   37437 route_manager.go:155] Route Manager: netlink route deletion event: "{Ifindex: 6 Dst: 10.130.0.2/32 Src: 10.130.0.2 Gw: <nil> Flags: [] Table: 255 Realm: 0}"
I0719 01:46:01.742265   37437 namespace.go:104] [openshift-kube-apiserver] adding namespace took 1.329105ms
I0719 01:46:01.742282   37437 obj_retry.go:541] Creating *v1.Namespace openshift-kube-apiserver took: 1.349814ms
I0719 01:46:01.742294   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-monitoring
I0719 01:46:01.742302   37437 namespace.go:100] [openshift-monitoring] adding namespace
I0719 01:46:01.742400   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.131.0.28 10.128.2.20 10.128.2.26 10.131.0.27 10.128.2.18 10.131.0.25 10.131.0.14 10.128.0.40 10.128.2.33 10.129.2.61 10.131.0.12 10.131.0.15 10.128.2.15 10.128.2.19 10.128.2.17 10.128.2.16 10.131.0.16]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-monitoring:v4 k8s.ovn.org/name:openshift-monitoring k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {f493566b-d155-438d-898b-1fd72c886f9a}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.742478   37437 address_set.go:304] New(f493566b-d155-438d-898b-1fd72c886f9a/default-network-controller:Namespace:openshift-monitoring:v4/a5151710470485437164) with [10.128.2.16 10.131.0.16 10.131.0.15 10.129.2.61 10.128.2.15 10.131.0.14 10.131.0.28 10.128.0.40 10.128.2.19 10.128.2.26 10.131.0.27 10.128.2.17 10.131.0.12 10.128.2.18 10.128.2.20 10.131.0.25 10.128.2.33]
I0719 01:46:01.742491   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.131.0.28 10.128.2.20 10.128.2.26 10.131.0.27 10.128.2.18 10.131.0.25 10.131.0.14 10.128.0.40 10.128.2.33 10.129.2.61 10.131.0.12 10.131.0.15 10.128.2.15 10.128.2.19 10.128.2.17 10.128.2.16 10.131.0.16]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-monitoring:v4 k8s.ovn.org/name:openshift-monitoring k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {f493566b-d155-438d-898b-1fd72c886f9a}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.742854   37437 namespace.go:104] [openshift-monitoring] adding namespace took 545.374µs
I0719 01:46:01.742865   37437 obj_retry.go:541] Creating *v1.Namespace openshift-monitoring took: 561.793µs
I0719 01:46:01.742874   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-authentication
I0719 01:46:01.742880   37437 namespace.go:100] [openshift-authentication] adding namespace
I0719 01:46:01.742996   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.67]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-kube-scheduler-operator:v4 k8s.ovn.org/name:openshift-kube-scheduler-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {530d19c4-871e-451d-9c65-7da36524146d}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.743063   37437 address_set.go:304] New(530d19c4-871e-451d-9c65-7da36524146d/default-network-controller:Namespace:openshift-kube-scheduler-operator:v4/a8446891589965341694) with [10.129.2.67]
I0719 01:46:01.743091   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.67]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-kube-scheduler-operator:v4 k8s.ovn.org/name:openshift-kube-scheduler-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {530d19c4-871e-451d-9c65-7da36524146d}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.743425   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-kni-infra:v4 k8s.ovn.org/name:openshift-kni-infra k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {5c4c21dc-c8a6-49bf-9fed-d43f18b7854f}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.743452   37437 address_set.go:304] New(5c4c21dc-c8a6-49bf-9fed-d43f18b7854f/default-network-controller:Namespace:openshift-kni-infra:v4/a12641306622762432907) with []
I0719 01:46:01.743452   37437 namespace.go:104] [openshift-kube-scheduler-operator] adding namespace took 3.057369ms
I0719 01:46:01.743466   37437 obj_retry.go:541] Creating *v1.Namespace openshift-kube-scheduler-operator took: 3.092813ms
I0719 01:46:01.743459   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-kni-infra:v4 k8s.ovn.org/name:openshift-kni-infra k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {5c4c21dc-c8a6-49bf-9fed-d43f18b7854f}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.743480   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-etcd-operator
I0719 01:46:01.743490   37437 namespace.go:100] [openshift-etcd-operator] adding namespace
I0719 01:46:01.743790   37437 namespace.go:104] [openshift-kni-infra] adding namespace took 3.377529ms
I0719 01:46:01.743807   37437 obj_retry.go:541] Creating *v1.Namespace openshift-kni-infra took: 3.406181ms
I0719 01:46:01.743818   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-insights
I0719 01:46:01.743825   37437 namespace.go:100] [openshift-insights] adding namespace
I0719 01:46:01.743860   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.128.2.7 10.128.2.23 10.131.0.5 10.131.0.20 10.131.0.29 10.131.0.19 10.131.0.21 10.128.2.13 10.131.0.22 10.128.2.25 10.128.2.30 10.128.2.41 10.128.2.28 10.128.2.21 10.131.0.6 10.128.2.34 10.128.2.29 10.131.0.26 10.128.2.6 10.128.2.35 10.131.0.10 10.131.0.18 10.131.0.24 10.131.0.17 10.128.2.12 10.128.2.24 10.131.0.9 10.131.0.23 10.128.2.32 10.128.2.31]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-storage:v4 k8s.ovn.org/name:openshift-storage k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {21ebc082-0159-4676-a683-86fbd995314a}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.743909   37437 address_set.go:304] New(21ebc082-0159-4676-a683-86fbd995314a/default-network-controller:Namespace:openshift-storage:v4/a14013983289553355313) with [10.131.0.18 10.131.0.24 10.128.2.24 10.128.2.34 10.128.2.7 10.131.0.22 10.131.0.29 10.131.0.17 10.128.2.25 10.128.2.29 10.128.2.30 10.131.0.23 10.128.2.12 10.131.0.19 10.131.0.26 10.128.2.35 10.128.2.41 10.128.2.6 10.131.0.10 10.131.0.9 10.128.2.28 10.128.2.23 10.128.2.32 10.131.0.5 10.128.2.21 10.131.0.20 10.131.0.21 10.128.2.31 10.128.2.13 10.131.0.6]
I0719 01:46:01.743920   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.128.2.7 10.128.2.23 10.131.0.5 10.131.0.20 10.131.0.29 10.131.0.19 10.131.0.21 10.128.2.13 10.131.0.22 10.128.2.25 10.128.2.30 10.128.2.41 10.128.2.28 10.128.2.21 10.131.0.6 10.128.2.34 10.128.2.29 10.131.0.26 10.128.2.6 10.128.2.35 10.131.0.10 10.131.0.18 10.131.0.24 10.131.0.17 10.128.2.12 10.128.2.24 10.131.0.9 10.131.0.23 10.128.2.32 10.128.2.31]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-storage:v4 k8s.ovn.org/name:openshift-storage k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {21ebc082-0159-4676-a683-86fbd995314a}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.744561   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.78]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-cluster-samples-operator:v4 k8s.ovn.org/name:openshift-cluster-samples-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {28465e81-248a-4bdb-9dac-799aedc78aff}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.744604   37437 address_set.go:304] New(28465e81-248a-4bdb-9dac-799aedc78aff/default-network-controller:Namespace:openshift-cluster-samples-operator:v4/a3083655245828550199) with [10.129.2.78]
I0719 01:46:01.744613   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.78]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-cluster-samples-operator:v4 k8s.ovn.org/name:openshift-cluster-samples-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {28465e81-248a-4bdb-9dac-799aedc78aff}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.744626   37437 namespace.go:104] [openshift-storage] adding namespace took 4.197923ms
I0719 01:46:01.744642   37437 obj_retry.go:541] Creating *v1.Namespace openshift-storage took: 4.231382ms
I0719 01:46:01.744655   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-console-user-settings
I0719 01:46:01.744662   37437 namespace.go:100] [openshift-console-user-settings] adding namespace
I0719 01:46:01.744971   37437 namespace.go:104] [openshift-cluster-samples-operator] adding namespace took 4.537087ms
I0719 01:46:01.745002   37437 obj_retry.go:541] Creating *v1.Namespace openshift-cluster-samples-operator took: 4.58075ms
I0719 01:46:01.745011   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-cloud-network-config-controller
I0719 01:46:01.745021   37437 namespace.go:100] [openshift-cloud-network-config-controller] adding namespace
I0719 01:46:01.744962   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-cluster-version:v4 k8s.ovn.org/name:openshift-cluster-version k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {9163231c-ca8b-460b-9642-c50d32a5f55e}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.745039   37437 address_set.go:304] New(9163231c-ca8b-460b-9642-c50d32a5f55e/default-network-controller:Namespace:openshift-cluster-version:v4/a8029920972938375443) with []
I0719 01:46:01.745047   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-cluster-version:v4 k8s.ovn.org/name:openshift-cluster-version k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {9163231c-ca8b-460b-9642-c50d32a5f55e}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.745351   37437 namespace.go:104] [openshift-cluster-version] adding namespace took 4.898486ms
I0719 01:46:01.745365   37437 obj_retry.go:541] Creating *v1.Namespace openshift-cluster-version took: 4.923885ms
I0719 01:46:01.745354   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-cloud-controller-manager:v4 k8s.ovn.org/name:openshift-cloud-controller-manager k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {187e9af2-63a2-4e64-af75-0d92ffec3c52}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.745381   37437 address_set.go:304] New(187e9af2-63a2-4e64-af75-0d92ffec3c52/default-network-controller:Namespace:openshift-cloud-controller-manager:v4/a545707041332338296) with []
I0719 01:46:01.745387   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-cloud-controller-manager:v4 k8s.ovn.org/name:openshift-cloud-controller-manager k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {187e9af2-63a2-4e64-af75-0d92ffec3c52}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.745373   37437 obj_retry.go:502] Add event received for *v1.Namespace kube-public
I0719 01:46:01.745456   37437 namespace.go:100] [kube-public] adding namespace
I0719 01:46:01.745673   37437 namespace.go:104] [openshift-cloud-controller-manager] adding namespace took 5.19387ms
I0719 01:46:01.745685   37437 obj_retry.go:541] Creating *v1.Namespace openshift-cloud-controller-manager took: 5.244779ms
I0719 01:46:01.745694   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-ingress-canary
I0719 01:46:01.745699   37437 namespace.go:100] [openshift-ingress-canary] adding namespace
I0719 01:46:01.745688   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.128.0.34]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-dns-operator:v4 k8s.ovn.org/name:openshift-dns-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {197daab0-3834-4ec8-ba82-a12678a67adf}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.745714   37437 address_set.go:304] New(197daab0-3834-4ec8-ba82-a12678a67adf/default-network-controller:Namespace:openshift-dns-operator:v4/a12081638711291249560) with [10.128.0.34]
I0719 01:46:01.745720   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.128.0.34]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-dns-operator:v4 k8s.ovn.org/name:openshift-dns-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {197daab0-3834-4ec8-ba82-a12678a67adf}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.746039   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.66]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-kube-controller-manager-operator:v4 k8s.ovn.org/name:openshift-kube-controller-manager-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {c421804e-dfc2-4199-9585-f0967996d395}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.746086   37437 address_set.go:304] New(c421804e-dfc2-4199-9585-f0967996d395/default-network-controller:Namespace:openshift-kube-controller-manager-operator:v4/a13990978431870169537) with [10.129.2.66]
I0719 01:46:01.746099   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.66]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-kube-controller-manager-operator:v4 k8s.ovn.org/name:openshift-kube-controller-manager-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {c421804e-dfc2-4199-9585-f0967996d395}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.746134   37437 namespace.go:104] [openshift-dns-operator] adding namespace took 5.645817ms
I0719 01:46:01.746144   37437 obj_retry.go:541] Creating *v1.Namespace openshift-dns-operator took: 5.698723ms
I0719 01:46:01.746154   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-host-network
I0719 01:46:01.746160   37437 namespace.go:100] [openshift-host-network] adding namespace
I0719 01:46:01.746156   37437 route_manager.go:149] Route Manager: netlink route addition event: "{Ifindex: 6 Dst: 10.130.0.2/32 Src: 10.130.0.2 Gw: <nil> Flags: [] Table: 255 Realm: 0}"
I0719 01:46:01.746203   37437 route_manager.go:149] Route Manager: netlink route addition event: "{Ifindex: 6 Dst: 10.130.1.255/32 Src: 10.130.0.2 Gw: <nil> Flags: [] Table: 255 Realm: 0}"
I0719 01:46:01.746213   37437 route_manager.go:93] Route Manager: attempting to add route: {Ifindex: 6 Dst: 10.128.0.0/14 Src: <nil> Gw: 10.130.0.1 Flags: [] Table: 0 Realm: 0}
I0719 01:46:01.746378   37437 ovs.go:159] Exec(22): /usr/sbin/sysctl -w net.ipv4.conf.ovn-k8s-mp0.forwarding=1
I0719 01:46:01.746455   37437 route_manager.go:110] Route Manager: completed adding route: {Ifindex: 6 Dst: 10.128.0.0/14 Src: <nil> Gw: 10.130.0.1 Flags: [] Table: 254 Realm: 0}
I0719 01:46:01.746475   37437 route_manager.go:93] Route Manager: attempting to add route: {Ifindex: 6 Dst: 169.254.169.3/32 Src: <nil> Gw: 10.130.0.1 Flags: [] Table: 0 Realm: 0}
I0719 01:46:01.746633   37437 route_manager.go:110] Route Manager: completed adding route: {Ifindex: 6 Dst: 169.254.169.3/32 Src: <nil> Gw: 10.130.0.1 Flags: [] Table: 254 Realm: 0}
I0719 01:46:01.746659   37437 route_manager.go:149] Route Manager: netlink route addition event: "{Ifindex: 6 Dst: 10.130.0.0/23 Src: 10.130.0.2 Gw: <nil> Flags: [] Table: 254 Realm: 0}"
I0719 01:46:01.746676   37437 route_manager.go:149] Route Manager: netlink route addition event: "{Ifindex: 6 Dst: 10.128.0.0/14 Src: <nil> Gw: 10.130.0.1 Flags: [] Table: 254 Realm: 0}"
I0719 01:46:01.746691   37437 route_manager.go:149] Route Manager: netlink route addition event: "{Ifindex: 6 Dst: 169.254.169.3/32 Src: <nil> Gw: 10.130.0.1 Flags: [] Table: 254 Realm: 0}"
I0719 01:46:01.746713   37437 namespace.go:104] [openshift-kube-controller-manager-operator] adding namespace took 6.214786ms
I0719 01:46:01.746730   37437 obj_retry.go:541] Creating *v1.Namespace openshift-kube-controller-manager-operator took: 6.246294ms
I0719 01:46:01.746743   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-infra
I0719 01:46:01.746751   37437 namespace.go:100] [openshift-infra] adding namespace
I0719 01:46:01.746808   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.81]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-config-operator:v4 k8s.ovn.org/name:openshift-config-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {f0357032-311a-4144-af3b-fc6469256866}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.746854   37437 address_set.go:304] New(f0357032-311a-4144-af3b-fc6469256866/default-network-controller:Namespace:openshift-config-operator:v4/a15513656991472936797) with [10.129.2.81]
I0719 01:46:01.746864   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.81]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-config-operator:v4 k8s.ovn.org/name:openshift-config-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {f0357032-311a-4144-af3b-fc6469256866}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.747275   37437 namespace.go:104] [openshift-config-operator] adding namespace took 6.727433ms
I0719 01:46:01.747295   37437 obj_retry.go:541] Creating *v1.Namespace openshift-config-operator took: 6.795926ms
I0719 01:46:01.747306   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-oauth-apiserver
I0719 01:46:01.747312   37437 namespace.go:100] [openshift-oauth-apiserver] adding namespace
I0719 01:46:01.747288   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-cluster-csi-drivers:v4 k8s.ovn.org/name:openshift-cluster-csi-drivers k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {cdb57dda-1359-4cce-b823-478c565f1a3a}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.747386   37437 address_set.go:304] New(cdb57dda-1359-4cce-b823-478c565f1a3a/default-network-controller:Namespace:openshift-cluster-csi-drivers:v4/a12187954455470212926) with []
I0719 01:46:01.747396   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-cluster-csi-drivers:v4 k8s.ovn.org/name:openshift-cluster-csi-drivers k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {cdb57dda-1359-4cce-b823-478c565f1a3a}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.747427   37437 ovs.go:162] Exec(22): stdout: "net.ipv4.conf.ovn-k8s-mp0.forwarding = 1\n"
I0719 01:46:01.747526   37437 ovs.go:163] Exec(22): stderr: ""
I0719 01:46:01.747794   37437 namespace.go:104] [openshift-cluster-csi-drivers] adding namespace took 7.139674ms
I0719 01:46:01.747812   37437 obj_retry.go:541] Creating *v1.Namespace openshift-cluster-csi-drivers took: 7.167754ms
I0719 01:46:01.747822   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-vsphere-infra
I0719 01:46:01.747828   37437 namespace.go:100] [openshift-vsphere-infra] adding namespace
I0719 01:46:01.747816   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-cluster-machine-approver:v4 k8s.ovn.org/name:openshift-cluster-machine-approver k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {ab48b7f3-4c9e-4671-bc45-8a1a7c247aa8}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.747844   37437 address_set.go:304] New(ab48b7f3-4c9e-4671-bc45-8a1a7c247aa8/default-network-controller:Namespace:openshift-cluster-machine-approver:v4/a8065968527448962190) with []
I0719 01:46:01.747855   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-cluster-machine-approver:v4 k8s.ovn.org/name:openshift-cluster-machine-approver k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {ab48b7f3-4c9e-4671-bc45-8a1a7c247aa8}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.748180   37437 namespace.go:104] [openshift-cluster-machine-approver] adding namespace took 7.512352ms
I0719 01:46:01.748190   37437 obj_retry.go:541] Creating *v1.Namespace openshift-cluster-machine-approver took: 7.535955ms
I0719 01:46:01.748197   37437 obj_retry.go:502] Add event received for *v1.Namespace kube-node-lease
I0719 01:46:01.748204   37437 namespace.go:100] [kube-node-lease] adding namespace
I0719 01:46:01.748193   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:kube-system:v4 k8s.ovn.org/name:kube-system k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {2c53b4d8-e0c7-4c78-89d8-7138c58a28fd}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.748230   37437 address_set.go:304] New(2c53b4d8-e0c7-4c78-89d8-7138c58a28fd/default-network-controller:Namespace:kube-system:v4/a8746611765617041202) with []
I0719 01:46:01.748236   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:kube-system:v4 k8s.ovn.org/name:kube-system k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {2c53b4d8-e0c7-4c78-89d8-7138c58a28fd}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.748527   37437 namespace.go:104] [kube-system] adding namespace took 7.856708ms
I0719 01:46:01.748540   37437 obj_retry.go:541] Creating *v1.Namespace kube-system took: 8.069162ms
I0719 01:46:01.748548   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-node
I0719 01:46:01.748554   37437 namespace.go:100] [openshift-node] adding namespace
I0719 01:46:01.748563   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.64]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-authentication-operator:v4 k8s.ovn.org/name:openshift-authentication-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {9f97cf2b-2d2e-4546-b141-b36f041a2936}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.748585   37437 address_set.go:304] New(9f97cf2b-2d2e-4546-b141-b36f041a2936/default-network-controller:Namespace:openshift-authentication-operator:v4/a11592754075545683359) with [10.129.2.64]
I0719 01:46:01.748591   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.64]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-authentication-operator:v4 k8s.ovn.org/name:openshift-authentication-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {9f97cf2b-2d2e-4546-b141-b36f041a2936}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.748849   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-cloud-platform-infra:v4 k8s.ovn.org/name:openshift-cloud-platform-infra k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {a737c5f6-8359-420a-a2b1-373e3689fbf0}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.748875   37437 address_set.go:304] New(a737c5f6-8359-420a-a2b1-373e3689fbf0/default-network-controller:Namespace:openshift-cloud-platform-infra:v4/a755693067844839690) with []
I0719 01:46:01.748876   37437 namespace.go:104] [openshift-authentication-operator] adding namespace took 8.20109ms
I0719 01:46:01.748886   37437 obj_retry.go:541] Creating *v1.Namespace openshift-authentication-operator took: 8.413094ms
I0719 01:46:01.748881   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-cloud-platform-infra:v4 k8s.ovn.org/name:openshift-cloud-platform-infra k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {a737c5f6-8359-420a-a2b1-373e3689fbf0}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.748894   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-ovirt-infra
I0719 01:46:01.748901   37437 namespace.go:100] [openshift-ovirt-infra] adding namespace
I0719 01:46:01.749166   37437 namespace.go:104] [openshift-cloud-platform-infra] adding namespace took 8.489941ms
I0719 01:46:01.749178   37437 obj_retry.go:541] Creating *v1.Namespace openshift-cloud-platform-infra took: 8.706845ms
I0719 01:46:01.749187   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-machine-config-operator
I0719 01:46:01.749193   37437 namespace.go:100] [openshift-machine-config-operator] adding namespace
I0719 01:46:01.749187   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.128.0.16 10.129.2.16]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-authentication:v4 k8s.ovn.org/name:openshift-authentication k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {5cd80617-8ea6-490e-9aab-5f3c44ca3297}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.749237   37437 address_set.go:304] New(5cd80617-8ea6-490e-9aab-5f3c44ca3297/default-network-controller:Namespace:openshift-authentication:v4/a5821095395710037482) with [10.128.0.16 10.129.2.16]
I0719 01:46:01.749248   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.128.0.16 10.129.2.16]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-authentication:v4 k8s.ovn.org/name:openshift-authentication k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {5cd80617-8ea6-490e-9aab-5f3c44ca3297}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.749558   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.83]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-etcd-operator:v4 k8s.ovn.org/name:openshift-etcd-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {38b2191b-77d6-43bc-a21a-ad27789b8053}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.749587   37437 address_set.go:304] New(38b2191b-77d6-43bc-a21a-ad27789b8053/default-network-controller:Namespace:openshift-etcd-operator:v4/a14710618839743769589) with [10.129.2.83]
I0719 01:46:01.749593   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.83]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-etcd-operator:v4 k8s.ovn.org/name:openshift-etcd-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {38b2191b-77d6-43bc-a21a-ad27789b8053}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.749605   37437 namespace.go:104] [openshift-authentication] adding namespace took 6.717248ms
I0719 01:46:01.749619   37437 obj_retry.go:541] Creating *v1.Namespace openshift-authentication took: 6.735271ms
I0719 01:46:01.749634   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-ingress
I0719 01:46:01.749644   37437 namespace.go:100] [openshift-ingress] adding namespace
I0719 01:46:01.749845   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.84]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-insights:v4 k8s.ovn.org/name:openshift-insights k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {c59702c8-ace4-4494-888e-9e8c89992172}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.749874   37437 address_set.go:304] New(c59702c8-ace4-4494-888e-9e8c89992172/default-network-controller:Namespace:openshift-insights:v4/a17978228596290493481) with [10.129.2.84]
I0719 01:46:01.749880   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.84]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-insights:v4 k8s.ovn.org/name:openshift-insights k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {c59702c8-ace4-4494-888e-9e8c89992172}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.749895   37437 namespace.go:104] [openshift-etcd-operator] adding namespace took 6.398234ms
I0719 01:46:01.749902   37437 obj_retry.go:541] Creating *v1.Namespace openshift-etcd-operator took: 6.412497ms
I0719 01:46:01.749910   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-marketplace
I0719 01:46:01.749916   37437 namespace.go:100] [openshift-marketplace] adding namespace
I0719 01:46:01.750115   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-console-user-settings:v4 k8s.ovn.org/name:openshift-console-user-settings k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {261be235-9433-4e1e-8052-aab728fdbb24}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.750141   37437 address_set.go:304] New(261be235-9433-4e1e-8052-aab728fdbb24/default-network-controller:Namespace:openshift-console-user-settings:v4/a17174782576849527835) with []
I0719 01:46:01.750149   37437 namespace.go:104] [openshift-insights] adding namespace took 6.317698ms
I0719 01:46:01.750148   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-console-user-settings:v4 k8s.ovn.org/name:openshift-console-user-settings k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {261be235-9433-4e1e-8052-aab728fdbb24}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.750158   37437 obj_retry.go:541] Creating *v1.Namespace openshift-insights took: 6.332454ms
I0719 01:46:01.750169   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-kube-apiserver-operator
I0719 01:46:01.750177   37437 namespace.go:100] [openshift-kube-apiserver-operator] adding namespace
I0719 01:46:01.750475   37437 namespace.go:104] [openshift-console-user-settings] adding namespace took 5.807416ms
I0719 01:46:01.750488   37437 obj_retry.go:541] Creating *v1.Namespace openshift-console-user-settings took: 5.82485ms
I0719 01:46:01.750497   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-kube-controller-manager
I0719 01:46:01.750503   37437 namespace.go:100] [openshift-kube-controller-manager] adding namespace
I0719 01:46:01.750482   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-cloud-network-config-controller:v4 k8s.ovn.org/name:openshift-cloud-network-config-controller k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {203c3c22-1c15-448e-a12e-e02a92d3b669}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.750524   37437 address_set.go:304] New(203c3c22-1c15-448e-a12e-e02a92d3b669/default-network-controller:Namespace:openshift-cloud-network-config-controller:v4/a6429873968864053860) with []
I0719 01:46:01.750533   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-cloud-network-config-controller:v4 k8s.ovn.org/name:openshift-cloud-network-config-controller k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {203c3c22-1c15-448e-a12e-e02a92d3b669}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.750843   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:kube-public:v4 k8s.ovn.org/name:kube-public k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {e72c197c-77d2-4774-a069-1da13485f896}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.750879   37437 address_set.go:304] New(e72c197c-77d2-4774-a069-1da13485f896/default-network-controller:Namespace:kube-public:v4/a8590749387396730558) with []
I0719 01:46:01.750884   37437 namespace.go:104] [openshift-cloud-network-config-controller] adding namespace took 5.853916ms
I0719 01:46:01.750885   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:kube-public:v4 k8s.ovn.org/name:kube-public k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {e72c197c-77d2-4774-a069-1da13485f896}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.750898   37437 obj_retry.go:541] Creating *v1.Namespace openshift-cloud-network-config-controller took: 5.875412ms
I0719 01:46:01.750912   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-apiserver
I0719 01:46:01.750925   37437 namespace.go:100] [openshift-apiserver] adding namespace
I0719 01:46:01.751178   37437 namespace.go:104] [kube-public] adding namespace took 5.716684ms
I0719 01:46:01.751191   37437 obj_retry.go:541] Creating *v1.Namespace kube-public took: 5.73429ms
I0719 01:46:01.751199   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-ingress-operator
I0719 01:46:01.751205   37437 namespace.go:100] [openshift-ingress-operator] adding namespace
I0719 01:46:01.751203   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.131.0.30 10.130.0.10 10.128.2.22]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-ingress-canary:v4 k8s.ovn.org/name:openshift-ingress-canary k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {466df127-0d1d-4973-af87-c1c2f24dc3be}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.751230   37437 address_set.go:304] New(466df127-0d1d-4973-af87-c1c2f24dc3be/default-network-controller:Namespace:openshift-ingress-canary:v4/a17074529903361539284) with [10.131.0.30 10.130.0.10 10.128.2.22]
I0719 01:46:01.751237   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.131.0.30 10.130.0.10 10.128.2.22]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-ingress-canary:v4 k8s.ovn.org/name:openshift-ingress-canary k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {466df127-0d1d-4973-af87-c1c2f24dc3be}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.751523   37437 namespace.go:104] [openshift-ingress-canary] adding namespace took 5.819062ms
I0719 01:46:01.751536   37437 obj_retry.go:541] Creating *v1.Namespace openshift-ingress-canary took: 5.835499ms
I0719 01:46:01.751545   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-local-storage
I0719 01:46:01.751551   37437 namespace.go:100] [openshift-local-storage] adding namespace
I0719 01:46:01.751632   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.130.0.2 10.128.0.2 100.64.0.2 100.64.0.3 10.129.2.2 100.64.0.7 100.64.0.5 10.128.2.2 100.64.0.4 10.129.0.2 10.131.0.2 100.64.0.6]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-host-network:v4 k8s.ovn.org/name:openshift-host-network k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {13c7748f-9ab4-428d-b5b9-cfcfb5c0298b}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.751683   37437 address_set.go:304] New(13c7748f-9ab4-428d-b5b9-cfcfb5c0298b/default-network-controller:Namespace:openshift-host-network:v4/a6910206611978007605) with [10.131.0.2 100.64.0.5 10.128.2.2 100.64.0.6 10.130.0.2 100.64.0.4 10.128.0.2 100.64.0.2 10.129.0.2 100.64.0.3 10.129.2.2 100.64.0.7]
I0719 01:46:01.751695   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.130.0.2 10.128.0.2 100.64.0.2 100.64.0.3 10.129.2.2 100.64.0.7 100.64.0.5 10.128.2.2 100.64.0.4 10.129.0.2 10.131.0.2 100.64.0.6]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-host-network:v4 k8s.ovn.org/name:openshift-host-network k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {13c7748f-9ab4-428d-b5b9-cfcfb5c0298b}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.752021   37437 namespace.go:104] [openshift-host-network] adding namespace took 5.853819ms
I0719 01:46:01.752039   37437 obj_retry.go:541] Creating *v1.Namespace openshift-host-network took: 5.876209ms
I0719 01:46:01.752052   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-console
I0719 01:46:01.752060   37437 namespace.go:100] [openshift-console] adding namespace
I0719 01:46:01.752055   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-infra:v4 k8s.ovn.org/name:openshift-infra k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {58211017-0695-4d22-a54a-56b2d7a51152}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.752092   37437 address_set.go:304] New(58211017-0695-4d22-a54a-56b2d7a51152/default-network-controller:Namespace:openshift-infra:v4/a4190772658089390776) with []
I0719 01:46:01.752099   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-infra:v4 k8s.ovn.org/name:openshift-infra k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {58211017-0695-4d22-a54a-56b2d7a51152}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.752358   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.128.0.15 10.129.2.13]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-oauth-apiserver:v4 k8s.ovn.org/name:openshift-oauth-apiserver k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {fa6db537-270f-4791-a1f5-5143d52b5d5b}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.752385   37437 address_set.go:304] New(fa6db537-270f-4791-a1f5-5143d52b5d5b/default-network-controller:Namespace:openshift-oauth-apiserver:v4/a18232515746603522929) with [10.128.0.15 10.129.2.13]
I0719 01:46:01.752377   37437 namespace.go:104] [openshift-infra] adding namespace took 5.619837ms
I0719 01:46:01.752392   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.128.0.15 10.129.2.13]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-oauth-apiserver:v4 k8s.ovn.org/name:openshift-oauth-apiserver k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {fa6db537-270f-4791-a1f5-5143d52b5d5b}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.752401   37437 obj_retry.go:541] Creating *v1.Namespace openshift-infra took: 5.64701ms
I0719 01:46:01.752415   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-cloud-credential-operator
I0719 01:46:01.752425   37437 namespace.go:100] [openshift-cloud-credential-operator] adding namespace
I0719 01:46:01.752638   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-vsphere-infra:v4 k8s.ovn.org/name:openshift-vsphere-infra k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {e02e246b-bad8-483c-95b7-67f0f5e7ae32}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.752669   37437 namespace.go:104] [openshift-oauth-apiserver] adding namespace took 5.350461ms
I0719 01:46:01.752678   37437 address_set.go:304] New(e02e246b-bad8-483c-95b7-67f0f5e7ae32/default-network-controller:Namespace:openshift-vsphere-infra:v4/a15940016096332404286) with []
I0719 01:46:01.752682   37437 obj_retry.go:541] Creating *v1.Namespace openshift-oauth-apiserver took: 5.367924ms
I0719 01:46:01.752694   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-cluster-storage-operator
I0719 01:46:01.752706   37437 namespace.go:100] [openshift-cluster-storage-operator] adding namespace
I0719 01:46:01.752685   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-vsphere-infra:v4 k8s.ovn.org/name:openshift-vsphere-infra k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {e02e246b-bad8-483c-95b7-67f0f5e7ae32}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.753020   37437 namespace.go:104] [openshift-vsphere-infra] adding namespace took 5.184261ms
I0719 01:46:01.753040   37437 obj_retry.go:541] Creating *v1.Namespace openshift-vsphere-infra took: 5.208768ms
I0719 01:46:01.753052   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-kube-storage-version-migrator
I0719 01:46:01.753060   37437 namespace.go:100] [openshift-kube-storage-version-migrator] adding namespace
I0719 01:46:01.753043   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:kube-node-lease:v4 k8s.ovn.org/name:kube-node-lease k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {1c7df195-5e2f-48f0-85ba-e185bb8b4f2f}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.753072   37437 address_set.go:304] New(1c7df195-5e2f-48f0-85ba-e185bb8b4f2f/default-network-controller:Namespace:kube-node-lease:v4/a8945957557890443212) with []
I0719 01:46:01.753080   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:kube-node-lease:v4 k8s.ovn.org/name:kube-node-lease k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {1c7df195-5e2f-48f0-85ba-e185bb8b4f2f}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.753325   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-node:v4 k8s.ovn.org/name:openshift-node k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {fe14606d-2a09-43a7-ad12-82fb21365448}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.753353   37437 address_set.go:304] New(fe14606d-2a09-43a7-ad12-82fb21365448/default-network-controller:Namespace:openshift-node:v4/a10320713570038180226) with []
I0719 01:46:01.753359   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-node:v4 k8s.ovn.org/name:openshift-node k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {fe14606d-2a09-43a7-ad12-82fb21365448}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.753375   37437 namespace.go:104] [kube-node-lease] adding namespace took 5.165003ms
I0719 01:46:01.753384   37437 obj_retry.go:541] Creating *v1.Namespace kube-node-lease took: 5.180626ms
I0719 01:46:01.753393   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-user-workload-monitoring
I0719 01:46:01.753399   37437 namespace.go:100] [openshift-user-workload-monitoring] adding namespace
I0719 01:46:01.753629   37437 namespace.go:104] [openshift-node] adding namespace took 5.068798ms
I0719 01:46:01.753622   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-ovirt-infra:v4 k8s.ovn.org/name:openshift-ovirt-infra k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {8f014840-9bbe-4d89-a526-1d8af7ba3551}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.753648   37437 obj_retry.go:541] Creating *v1.Namespace openshift-node took: 5.088489ms
I0719 01:46:01.753651   37437 address_set.go:304] New(8f014840-9bbe-4d89-a526-1d8af7ba3551/default-network-controller:Namespace:openshift-ovirt-infra:v4/a5172224344187132617) with []
I0719 01:46:01.753660   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-openstack-infra
I0719 01:46:01.753657   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-ovirt-infra:v4 k8s.ovn.org/name:openshift-ovirt-infra k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {8f014840-9bbe-4d89-a526-1d8af7ba3551}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.753669   37437 namespace.go:100] [openshift-openstack-infra] adding namespace
I0719 01:46:01.753964   37437 namespace.go:104] [openshift-ovirt-infra] adding namespace took 5.056884ms
I0719 01:46:01.753989   37437 obj_retry.go:541] Creating *v1.Namespace openshift-ovirt-infra took: 5.079914ms
I0719 01:46:01.753999   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-console-operator
I0719 01:46:01.754005   37437 namespace.go:100] [openshift-console-operator] adding namespace
I0719 01:46:01.753948   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.128.0.41 10.128.0.22]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-machine-config-operator:v4 k8s.ovn.org/name:openshift-machine-config-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {24856fe8-bae3-4b5f-ba4c-8b650f414ed0}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.754015   37437 address_set.go:304] New(24856fe8-bae3-4b5f-ba4c-8b650f414ed0/default-network-controller:Namespace:openshift-machine-config-operator:v4/a1512537150246498877) with [10.128.0.41 10.128.0.22]
I0719 01:46:01.754022   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.128.0.41 10.128.0.22]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-machine-config-operator:v4 k8s.ovn.org/name:openshift-machine-config-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {24856fe8-bae3-4b5f-ba4c-8b650f414ed0}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.754345   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-ingress:v4 k8s.ovn.org/name:openshift-ingress k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {580e707c-d652-43ce-8b86-7a58fc0b5243}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.754384   37437 address_set.go:304] New(580e707c-d652-43ce-8b86-7a58fc0b5243/default-network-controller:Namespace:openshift-ingress:v4/a9185810757115582127) with []
I0719 01:46:01.754390   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-ingress:v4 k8s.ovn.org/name:openshift-ingress k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {580e707c-d652-43ce-8b86-7a58fc0b5243}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.754369   37437 namespace.go:104] [openshift-machine-config-operator] adding namespace took 5.170879ms
I0719 01:46:01.754466   37437 obj_retry.go:541] Creating *v1.Namespace openshift-machine-config-operator took: 5.27129ms
I0719 01:46:01.754475   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-operators
I0719 01:46:01.754480   37437 namespace.go:100] [openshift-operators] adding namespace
I0719 01:46:01.754646   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.128.0.20 10.128.0.45 10.128.0.46 10.128.0.47 10.128.0.43]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-marketplace:v4 k8s.ovn.org/name:openshift-marketplace k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {b3549e25-5f72-44b3-a15e-31d5c16522b8}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.754671   37437 namespace.go:104] [openshift-ingress] adding namespace took 5.020453ms
I0719 01:46:01.754676   37437 address_set.go:304] New(b3549e25-5f72-44b3-a15e-31d5c16522b8/default-network-controller:Namespace:openshift-marketplace:v4/a13245376580307887587) with [10.128.0.47 10.128.0.43 10.128.0.20 10.128.0.45 10.128.0.46]
I0719 01:46:01.754679   37437 obj_retry.go:541] Creating *v1.Namespace openshift-ingress took: 5.036743ms
I0719 01:46:01.754684   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.128.0.20 10.128.0.45 10.128.0.46 10.128.0.47 10.128.0.43]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-marketplace:v4 k8s.ovn.org/name:openshift-marketplace k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {b3549e25-5f72-44b3-a15e-31d5c16522b8}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.755116   37437 namespace.go:104] [openshift-marketplace] adding namespace took 5.194051ms
I0719 01:46:01.755128   37437 obj_retry.go:541] Creating *v1.Namespace openshift-marketplace took: 5.210771ms
I0719 01:46:01.755137   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-route-controller-manager
I0719 01:46:01.755143   37437 namespace.go:100] [openshift-route-controller-manager] adding namespace
I0719 01:46:01.755104   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.65]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-kube-apiserver-operator:v4 k8s.ovn.org/name:openshift-kube-apiserver-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {618b7c4f-ee58-47fb-a0d7-ecfaaf326b1d}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.755152   37437 address_set.go:304] New(618b7c4f-ee58-47fb-a0d7-ecfaaf326b1d/default-network-controller:Namespace:openshift-kube-apiserver-operator:v4/a11465645704438275080) with [10.129.2.65]
I0719 01:46:01.755160   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.65]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-kube-apiserver-operator:v4 k8s.ovn.org/name:openshift-kube-apiserver-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {618b7c4f-ee58-47fb-a0d7-ecfaaf326b1d}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.755512   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.0.10 10.129.2.8 10.128.0.12]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-kube-controller-manager:v4 k8s.ovn.org/name:openshift-kube-controller-manager k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {6c98b9db-4936-4b02-8b5f-1773dfda4f56}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.755846   37437 namespace.go:104] [openshift-kube-apiserver-operator] adding namespace took 5.660937ms
I0719 01:46:01.755861   37437 obj_retry.go:541] Creating *v1.Namespace openshift-kube-apiserver-operator took: 5.685051ms
I0719 01:46:01.755553   37437 address_set.go:304] New(6c98b9db-4936-4b02-8b5f-1773dfda4f56/default-network-controller:Namespace:openshift-kube-controller-manager:v4/a4663622633901538608) with [10.129.0.10 10.129.2.8 10.128.0.12]
I0719 01:46:01.755886   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.0.10 10.129.2.8 10.128.0.12]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-kube-controller-manager:v4 k8s.ovn.org/name:openshift-kube-controller-manager k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {6c98b9db-4936-4b02-8b5f-1773dfda4f56}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.755872   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-cloud-controller-manager-operator
I0719 01:46:01.755970   37437 namespace.go:100] [openshift-cloud-controller-manager-operator] adding namespace
I0719 01:46:01.756207   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.17 10.128.0.18]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-apiserver:v4 k8s.ovn.org/name:openshift-apiserver k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {48914cd5-324d-49c2-a8f8-fed171c04411}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.756247   37437 address_set.go:304] New(48914cd5-324d-49c2-a8f8-fed171c04411/default-network-controller:Namespace:openshift-apiserver:v4/a12374569603079029239) with [10.129.2.17 10.128.0.18]
I0719 01:46:01.756251   37437 namespace.go:104] [openshift-kube-controller-manager] adding namespace took 5.741488ms
I0719 01:46:01.756261   37437 obj_retry.go:541] Creating *v1.Namespace openshift-kube-controller-manager took: 5.757039ms
I0719 01:46:01.756254   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.17 10.128.0.18]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-apiserver:v4 k8s.ovn.org/name:openshift-apiserver k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {48914cd5-324d-49c2-a8f8-fed171c04411}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.756271   37437 obj_retry.go:502] Add event received for *v1.Namespace default
I0719 01:46:01.756277   37437 namespace.go:100] [default] adding namespace
I0719 01:46:01.756537   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.82]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-ingress-operator:v4 k8s.ovn.org/name:openshift-ingress-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {f4d40fd6-924c-4c1f-9267-8ba6db2dc0d1}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.756574   37437 address_set.go:304] New(f4d40fd6-924c-4c1f-9267-8ba6db2dc0d1/default-network-controller:Namespace:openshift-ingress-operator:v4/a12824364980436020060) with [10.129.2.82]
I0719 01:46:01.756582   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.82]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-ingress-operator:v4 k8s.ovn.org/name:openshift-ingress-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {f4d40fd6-924c-4c1f-9267-8ba6db2dc0d1}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.756553   37437 namespace.go:104] [openshift-apiserver] adding namespace took 5.621881ms
I0719 01:46:01.756655   37437 obj_retry.go:541] Creating *v1.Namespace openshift-apiserver took: 5.731573ms
I0719 01:46:01.756664   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-ovn-kubernetes
I0719 01:46:01.756670   37437 namespace.go:100] [openshift-ovn-kubernetes] adding namespace
I0719 01:46:01.756889   37437 namespace.go:104] [openshift-ingress-operator] adding namespace took 5.678664ms
I0719 01:46:01.756901   37437 obj_retry.go:541] Creating *v1.Namespace openshift-ingress-operator took: 5.694322ms
I0719 01:46:01.756891   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.128.2.14 10.130.0.17 10.131.0.39 10.128.2.27]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-local-storage:v4 k8s.ovn.org/name:openshift-local-storage k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {51d17a64-7bd0-4e5b-91a1-c619a1a5b24b}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.756910   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-network-node-identity
I0719 01:46:01.756913   37437 address_set.go:304] New(51d17a64-7bd0-4e5b-91a1-c619a1a5b24b/default-network-controller:Namespace:openshift-local-storage:v4/a12699375267713376219) with [10.128.2.14 10.130.0.17 10.131.0.39 10.128.2.27]
I0719 01:46:01.756916   37437 namespace.go:100] [openshift-network-node-identity] adding namespace
I0719 01:46:01.756920   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.128.2.14 10.130.0.17 10.131.0.39 10.128.2.27]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-local-storage:v4 k8s.ovn.org/name:openshift-local-storage k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {51d17a64-7bd0-4e5b-91a1-c619a1a5b24b}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.757175   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.222 10.129.2.86 10.128.0.38 10.128.0.177]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-console:v4 k8s.ovn.org/name:openshift-console k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {af2707d4-eb95-495e-81e2-104f52221a64}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.757198   37437 namespace.go:104] [openshift-local-storage] adding namespace took 5.642312ms
I0719 01:46:01.757202   37437 address_set.go:304] New(af2707d4-eb95-495e-81e2-104f52221a64/default-network-controller:Namespace:openshift-console:v4/a11622011068173273797) with [10.128.0.177 10.129.2.222 10.129.2.86 10.128.0.38]
I0719 01:46:01.757206   37437 obj_retry.go:541] Creating *v1.Namespace openshift-local-storage took: 5.653862ms
I0719 01:46:01.757213   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-cluster-node-tuning-operator
I0719 01:46:01.757208   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.222 10.129.2.86 10.128.0.38 10.128.0.177]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-console:v4 k8s.ovn.org/name:openshift-console k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {af2707d4-eb95-495e-81e2-104f52221a64}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.757219   37437 namespace.go:100] [openshift-cluster-node-tuning-operator] adding namespace
I0719 01:46:01.757577   37437 gateway_init.go:324] Initializing Gateway Functionality
I0719 01:46:01.757657   37437 namespace.go:104] [openshift-console] adding namespace took 5.591289ms
I0719 01:46:01.757647   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.73]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-cloud-credential-operator:v4 k8s.ovn.org/name:openshift-cloud-credential-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {54b15d23-ae85-48f3-aa65-d76f68d2e548}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.757665   37437 obj_retry.go:541] Creating *v1.Namespace openshift-console took: 5.605998ms
I0719 01:46:01.757672   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-config-managed
I0719 01:46:01.757671   37437 address_set.go:304] New(54b15d23-ae85-48f3-aa65-d76f68d2e548/default-network-controller:Namespace:openshift-cloud-credential-operator:v4/a7815234012393910246) with [10.129.2.73]
I0719 01:46:01.757677   37437 namespace.go:100] [openshift-config-managed] adding namespace
I0719 01:46:01.757679   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.73]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-cloud-credential-operator:v4 k8s.ovn.org/name:openshift-cloud-credential-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {54b15d23-ae85-48f3-aa65-d76f68d2e548}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.757868   37437 gateway_localnet.go:181] Node local addresses initialized to: map[10.10.25.235:{10.10.25.0 ffffff00} 10.130.0.2:{10.130.0.0 fffffe00} 127.0.0.1:{127.0.0.0 ff000000} ::1:{::1 ffffffffffffffffffffffffffffffff} fe80::194b:ee14:ac95:140f:{fe80:: ffffffffffffffff0000000000000000} fe80::80c7:22ff:fe80:b7f6:{fe80:: ffffffffffffffff0000000000000000} fe80::bc6d:32ff:fe1d:e929:{fe80:: ffffffffffffffff0000000000000000}]
I0719 01:46:01.757907   37437 ovs.go:159] Exec(23): /usr/bin/ovs-vsctl --timeout=15 port-to-br br-ex
I0719 01:46:01.758272   37437 namespace.go:104] [openshift-cloud-credential-operator] adding namespace took 5.841582ms
I0719 01:46:01.758285   37437 obj_retry.go:541] Creating *v1.Namespace openshift-cloud-credential-operator took: 5.860732ms
I0719 01:46:01.758293   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-network-operator
I0719 01:46:01.758299   37437 namespace.go:100] [openshift-network-operator] adding namespace
I0719 01:46:01.758282   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.76 10.129.2.79 10.128.0.21 10.129.2.77 10.128.0.23 10.129.2.75]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-cluster-storage-operator:v4 k8s.ovn.org/name:openshift-cluster-storage-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {d9405cb9-74e0-462c-a689-f8b2b1f2a279}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.758310   37437 address_set.go:304] New(d9405cb9-74e0-462c-a689-f8b2b1f2a279/default-network-controller:Namespace:openshift-cluster-storage-operator:v4/a13337366700695359377) with [10.129.2.77 10.128.0.23 10.129.2.75 10.129.2.76 10.129.2.79 10.128.0.21]
I0719 01:46:01.758317   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.76 10.129.2.79 10.128.0.21 10.129.2.77 10.128.0.23 10.129.2.75]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-cluster-storage-operator:v4 k8s.ovn.org/name:openshift-cluster-storage-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {d9405cb9-74e0-462c-a689-f8b2b1f2a279}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.758585   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.87]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-kube-storage-version-migrator:v4 k8s.ovn.org/name:openshift-kube-storage-version-migrator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {9b1deeb2-f4cf-4e73-ba5e-d65079b7e9ee}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.758632   37437 address_set.go:304] New(9b1deeb2-f4cf-4e73-ba5e-d65079b7e9ee/default-network-controller:Namespace:openshift-kube-storage-version-migrator:v4/a16978912863426934758) with [10.129.2.87]
I0719 01:46:01.758640   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.87]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-kube-storage-version-migrator:v4 k8s.ovn.org/name:openshift-kube-storage-version-migrator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {9b1deeb2-f4cf-4e73-ba5e-d65079b7e9ee}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.758606   37437 namespace.go:104] [openshift-cluster-storage-operator] adding namespace took 5.894529ms
I0719 01:46:01.758710   37437 obj_retry.go:541] Creating *v1.Namespace openshift-cluster-storage-operator took: 6.004298ms
I0719 01:46:01.758717   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-kube-scheduler
I0719 01:46:01.758722   37437 namespace.go:100] [openshift-kube-scheduler] adding namespace
I0719 01:46:01.758882   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-user-workload-monitoring:v4 k8s.ovn.org/name:openshift-user-workload-monitoring k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {f48faae5-0cb3-4e47-b785-270ce30b4d6f}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.758909   37437 address_set.go:304] New(f48faae5-0cb3-4e47-b785-270ce30b4d6f/default-network-controller:Namespace:openshift-user-workload-monitoring:v4/a17884403498503024866) with []
I0719 01:46:01.758913   37437 namespace.go:104] [openshift-kube-storage-version-migrator] adding namespace took 5.846766ms
I0719 01:46:01.758919   37437 obj_retry.go:541] Creating *v1.Namespace openshift-kube-storage-version-migrator took: 5.859809ms
I0719 01:46:01.758924   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-kube-storage-version-migrator-operator
I0719 01:46:01.758916   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-user-workload-monitoring:v4 k8s.ovn.org/name:openshift-user-workload-monitoring k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {f48faae5-0cb3-4e47-b785-270ce30b4d6f}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.758930   37437 namespace.go:100] [openshift-kube-storage-version-migrator-operator] adding namespace
I0719 01:46:01.759201   37437 namespace.go:104] [openshift-user-workload-monitoring] adding namespace took 5.796136ms
I0719 01:46:01.759215   37437 obj_retry.go:541] Creating *v1.Namespace openshift-user-workload-monitoring took: 5.814899ms
I0719 01:46:01.759224   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-multus
I0719 01:46:01.759230   37437 namespace.go:100] [openshift-multus] adding namespace
I0719 01:46:01.759189   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-openstack-infra:v4 k8s.ovn.org/name:openshift-openstack-infra k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {180c5fc0-b52d-455b-9056-adf6d8c8f08b}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.759239   37437 address_set.go:304] New(180c5fc0-b52d-455b-9056-adf6d8c8f08b/default-network-controller:Namespace:openshift-openstack-infra:v4/a16831300222096547883) with []
I0719 01:46:01.759244   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-openstack-infra:v4 k8s.ovn.org/name:openshift-openstack-infra k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {180c5fc0-b52d-455b-9056-adf6d8c8f08b}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.759486   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.128.0.35 10.128.0.37]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-console-operator:v4 k8s.ovn.org/name:openshift-console-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {2b61070b-e3b0-4008-84f0-719cf4aa1e82}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.759507   37437 namespace.go:104] [openshift-openstack-infra] adding namespace took 5.746947ms
I0719 01:46:01.759513   37437 address_set.go:304] New(2b61070b-e3b0-4008-84f0-719cf4aa1e82/default-network-controller:Namespace:openshift-console-operator:v4/a16211398687523592942) with [10.128.0.35 10.128.0.37]
I0719 01:46:01.759521   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.128.0.35 10.128.0.37]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-console-operator:v4 k8s.ovn.org/name:openshift-console-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {2b61070b-e3b0-4008-84f0-719cf4aa1e82}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.759515   37437 obj_retry.go:541] Creating *v1.Namespace openshift-openstack-infra took: 5.847545ms
I0719 01:46:01.759601   37437 obj_retry.go:502] Add event received for *v1.Namespace assisted-installer
I0719 01:46:01.759607   37437 namespace.go:100] [assisted-installer] adding namespace
I0719 01:46:01.759804   37437 namespace.go:104] [openshift-console-operator] adding namespace took 5.794724ms
I0719 01:46:01.759814   37437 obj_retry.go:541] Creating *v1.Namespace openshift-console-operator took: 5.809489ms
I0719 01:46:01.759800   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-operators:v4 k8s.ovn.org/name:openshift-operators k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {e1c2a39f-b5cb-4f8b-8b4c-7da4a8a96b6a}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.759820   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-etcd
I0719 01:46:01.759825   37437 namespace.go:100] [openshift-etcd] adding namespace
I0719 01:46:01.759825   37437 address_set.go:304] New(e1c2a39f-b5cb-4f8b-8b4c-7da4a8a96b6a/default-network-controller:Namespace:openshift-operators:v4/a17780485792851514981) with []
I0719 01:46:01.759833   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-operators:v4 k8s.ovn.org/name:openshift-operators k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {e1c2a39f-b5cb-4f8b-8b4c-7da4a8a96b6a}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.760090   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.128.0.17 10.129.2.18]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-route-controller-manager:v4 k8s.ovn.org/name:openshift-route-controller-manager k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {084efe9f-e10d-471a-bd02-b921c1bf43b3}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.760115   37437 address_set.go:304] New(084efe9f-e10d-471a-bd02-b921c1bf43b3/default-network-controller:Namespace:openshift-route-controller-manager:v4/a5513313330862551964) with [10.128.0.17 10.129.2.18]
I0719 01:46:01.760121   37437 namespace.go:104] [openshift-operators] adding namespace took 5.636091ms
I0719 01:46:01.760129   37437 obj_retry.go:541] Creating *v1.Namespace openshift-operators took: 5.647576ms
I0719 01:46:01.760123   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.128.0.17 10.129.2.18]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-route-controller-manager:v4 k8s.ovn.org/name:openshift-route-controller-manager k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {084efe9f-e10d-471a-bd02-b921c1bf43b3}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.760138   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-service-ca-operator
I0719 01:46:01.760144   37437 namespace.go:100] [openshift-service-ca-operator] adding namespace
I0719 01:46:01.760350   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-cloud-controller-manager-operator:v4 k8s.ovn.org/name:openshift-cloud-controller-manager-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {6113e2ff-605a-4511-a07f-a3b6c4abce0c}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.760375   37437 address_set.go:304] New(6113e2ff-605a-4511-a07f-a3b6c4abce0c/default-network-controller:Namespace:openshift-cloud-controller-manager-operator:v4/a5078242225911085769) with []
I0719 01:46:01.760382   37437 namespace.go:104] [openshift-route-controller-manager] adding namespace took 5.234463ms
I0719 01:46:01.760389   37437 obj_retry.go:541] Creating *v1.Namespace openshift-route-controller-manager took: 5.245606ms
I0719 01:46:01.760382   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-cloud-controller-manager-operator:v4 k8s.ovn.org/name:openshift-cloud-controller-manager-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {6113e2ff-605a-4511-a07f-a3b6c4abce0c}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.760614   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:default:v4 k8s.ovn.org/name:default k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {2b16a9c4-01dd-4e43-a331-53418bf6abaf}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.760636   37437 namespace.go:104] [openshift-cloud-controller-manager-operator] adding namespace took 4.660336ms
I0719 01:46:01.760640   37437 address_set.go:304] New(2b16a9c4-01dd-4e43-a331-53418bf6abaf/default-network-controller:Namespace:default:v4/a4322231855293774466) with []
I0719 01:46:01.760642   37437 obj_retry.go:541] Creating *v1.Namespace openshift-cloud-controller-manager-operator took: 4.67187ms
I0719 01:46:01.760647   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:default:v4 k8s.ovn.org/name:default k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {2b16a9c4-01dd-4e43-a331-53418bf6abaf}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.760878   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-ovn-kubernetes:v4 k8s.ovn.org/name:openshift-ovn-kubernetes k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {869e7b08-898a-49ab-bf7e-5e21cce13b2d}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.760901   37437 namespace.go:104] [default] adding namespace took 4.618214ms
I0719 01:46:01.760903   37437 address_set.go:304] New(869e7b08-898a-49ab-bf7e-5e21cce13b2d/default-network-controller:Namespace:openshift-ovn-kubernetes:v4/a1398255725986493602) with []
I0719 01:46:01.760908   37437 obj_retry.go:541] Creating *v1.Namespace default took: 4.630666ms
I0719 01:46:01.760909   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-ovn-kubernetes:v4 k8s.ovn.org/name:openshift-ovn-kubernetes k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {869e7b08-898a-49ab-bf7e-5e21cce13b2d}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.761233   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-network-node-identity:v4 k8s.ovn.org/name:openshift-network-node-identity k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {f349f4b8-04b6-43d0-9455-5a6e033e2b10}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.761259   37437 namespace.go:104] [openshift-ovn-kubernetes] adding namespace took 4.583692ms
I0719 01:46:01.761267   37437 obj_retry.go:541] Creating *v1.Namespace openshift-ovn-kubernetes took: 4.596094ms
I0719 01:46:01.761275   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-image-registry
I0719 01:46:01.761280   37437 namespace.go:100] [openshift-image-registry] adding namespace
I0719 01:46:01.761259   37437 address_set.go:304] New(f349f4b8-04b6-43d0-9455-5a6e033e2b10/default-network-controller:Namespace:openshift-network-node-identity:v4/a6647208685787594228) with []
I0719 01:46:01.761289   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-network-node-identity:v4 k8s.ovn.org/name:openshift-network-node-identity k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {f349f4b8-04b6-43d0-9455-5a6e033e2b10}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.761536   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.74]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-cluster-node-tuning-operator:v4 k8s.ovn.org/name:openshift-cluster-node-tuning-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {4aed24a2-44de-42c1-9788-791ce23d4f3a}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.761558   37437 namespace.go:104] [openshift-network-node-identity] adding namespace took 4.637347ms
I0719 01:46:01.761562   37437 address_set.go:304] New(4aed24a2-44de-42c1-9788-791ce23d4f3a/default-network-controller:Namespace:openshift-cluster-node-tuning-operator:v4/a10032735054068291610) with [10.129.2.74]
I0719 01:46:01.761566   37437 obj_retry.go:541] Creating *v1.Namespace openshift-network-node-identity took: 4.64987ms
I0719 01:46:01.761572   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-config
I0719 01:46:01.761568   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.74]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-cluster-node-tuning-operator:v4 k8s.ovn.org/name:openshift-cluster-node-tuning-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {4aed24a2-44de-42c1-9788-791ce23d4f3a}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.761579   37437 namespace.go:100] [openshift-config] adding namespace
I0719 01:46:01.761819   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-config-managed:v4 k8s.ovn.org/name:openshift-config-managed k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {fdb4dd7d-9ba7-4e32-93eb-be0ef90cb400}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.761844   37437 address_set.go:304] New(fdb4dd7d-9ba7-4e32-93eb-be0ef90cb400/default-network-controller:Namespace:openshift-config-managed:v4/a6117206921658593480) with []
I0719 01:46:01.761850   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-config-managed:v4 k8s.ovn.org/name:openshift-config-managed k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {fdb4dd7d-9ba7-4e32-93eb-be0ef90cb400}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.761863   37437 namespace.go:104] [openshift-cluster-node-tuning-operator] adding namespace took 4.563159ms
I0719 01:46:01.761874   37437 obj_retry.go:541] Creating *v1.Namespace openshift-cluster-node-tuning-operator took: 4.653346ms
I0719 01:46:01.761884   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-controller-manager
I0719 01:46:01.761889   37437 namespace.go:100] [openshift-controller-manager] adding namespace
I0719 01:46:01.762097   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-network-operator:v4 k8s.ovn.org/name:openshift-network-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {6bce5f87-2ecd-4345-a951-8e262d249c25}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.762121   37437 address_set.go:304] New(6bce5f87-2ecd-4345-a951-8e262d249c25/default-network-controller:Namespace:openshift-network-operator:v4/a17843891307737330665) with []
I0719 01:46:01.762128   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-network-operator:v4 k8s.ovn.org/name:openshift-network-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {6bce5f87-2ecd-4345-a951-8e262d249c25}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.762121   37437 namespace.go:104] [openshift-config-managed] adding namespace took 4.439036ms
I0719 01:46:01.762206   37437 obj_retry.go:541] Creating *v1.Namespace openshift-config-managed took: 4.528024ms
I0719 01:46:01.762215   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-apiserver-operator
I0719 01:46:01.762221   37437 namespace.go:100] [openshift-apiserver-operator] adding namespace
I0719 01:46:01.762416   37437 namespace.go:104] [openshift-network-operator] adding namespace took 4.111479ms
I0719 01:46:01.762426   37437 obj_retry.go:541] Creating *v1.Namespace openshift-network-operator took: 4.126796ms
I0719 01:46:01.762432   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-network-diagnostics
I0719 01:46:01.762436   37437 namespace.go:100] [openshift-network-diagnostics] adding namespace
I0719 01:46:01.762492   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.128.0.9 10.129.0.7 10.129.2.7 10.129.0.6]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-kube-scheduler:v4 k8s.ovn.org/name:openshift-kube-scheduler k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {ae1e6050-3670-4f5e-978c-ca1e35ef7b65}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.762539   37437 address_set.go:304] New(ae1e6050-3670-4f5e-978c-ca1e35ef7b65/default-network-controller:Namespace:openshift-kube-scheduler:v4/a15634036902741400949) with [10.128.0.9 10.129.0.7 10.129.2.7 10.129.0.6]
I0719 01:46:01.762549   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.128.0.9 10.129.0.7 10.129.2.7 10.129.0.6]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-kube-scheduler:v4 k8s.ovn.org/name:openshift-kube-scheduler k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {ae1e6050-3670-4f5e-978c-ca1e35ef7b65}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.762873   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.71]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-kube-storage-version-migrator-operator:v4 k8s.ovn.org/name:openshift-kube-storage-version-migrator-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {4f6d67f0-ce40-4f4b-b89e-a25d937e59d5}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.762899   37437 address_set.go:304] New(4f6d67f0-ce40-4f4b-b89e-a25d937e59d5/default-network-controller:Namespace:openshift-kube-storage-version-migrator-operator:v4/a11291866915865594395) with [10.129.2.71]
I0719 01:46:01.762905   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.71]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-kube-storage-version-migrator-operator:v4 k8s.ovn.org/name:openshift-kube-storage-version-migrator-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {4f6d67f0-ce40-4f4b-b89e-a25d937e59d5}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.762915   37437 namespace.go:104] [openshift-kube-scheduler] adding namespace took 4.18578ms
I0719 01:46:01.762929   37437 obj_retry.go:541] Creating *v1.Namespace openshift-kube-scheduler took: 4.203326ms
I0719 01:46:01.762940   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-machine-api
I0719 01:46:01.762949   37437 namespace.go:100] [openshift-machine-api] adding namespace
I0719 01:46:01.763182   37437 namespace.go:104] [openshift-kube-storage-version-migrator-operator] adding namespace took 4.245802ms
I0719 01:46:01.763198   37437 obj_retry.go:541] Creating *v1.Namespace openshift-kube-storage-version-migrator-operator took: 4.264322ms
I0719 01:46:01.763211   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift
I0719 01:46:01.763219   37437 namespace.go:100] [openshift] adding namespace
I0719 01:46:01.763216   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.128.2.4 10.128.0.27 10.130.0.4 10.129.0.4 10.131.0.4 10.128.0.4 10.129.2.70 10.129.2.4]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-multus:v4 k8s.ovn.org/name:openshift-multus k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {f5cff015-5950-4b85-a441-83b9162315b4}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.763263   37437 address_set.go:304] New(f5cff015-5950-4b85-a441-83b9162315b4/default-network-controller:Namespace:openshift-multus:v4/a13687770890520536676) with [10.131.0.4 10.128.0.4 10.129.2.70 10.129.2.4 10.128.2.4 10.128.0.27 10.130.0.4 10.129.0.4]
I0719 01:46:01.763273   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.128.2.4 10.128.0.27 10.130.0.4 10.129.0.4 10.131.0.4 10.128.0.4 10.129.2.70 10.129.2.4]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-multus:v4 k8s.ovn.org/name:openshift-multus k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {f5cff015-5950-4b85-a441-83b9162315b4}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.763635   37437 namespace.go:104] [openshift-multus] adding namespace took 4.398454ms
I0719 01:46:01.763627   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:assisted-installer:v4 k8s.ovn.org/name:assisted-installer k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {6ab91f56-9a69-4dbf-8d6e-2ee5cf5c8d8e}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.763667   37437 address_set.go:304] New(6ab91f56-9a69-4dbf-8d6e-2ee5cf5c8d8e/default-network-controller:Namespace:assisted-installer:v4/a3061684233240860130) with []
I0719 01:46:01.763676   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:assisted-installer:v4 k8s.ovn.org/name:assisted-installer k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {6ab91f56-9a69-4dbf-8d6e-2ee5cf5c8d8e}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.763650   37437 obj_retry.go:541] Creating *v1.Namespace openshift-multus took: 4.41665ms
I0719 01:46:01.763747   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-operator-lifecycle-manager
I0719 01:46:01.763753   37437 namespace.go:100] [openshift-operator-lifecycle-manager] adding namespace
I0719 01:46:01.764020   37437 namespace.go:104] [assisted-installer] adding namespace took 4.407295ms
I0719 01:46:01.764035   37437 obj_retry.go:541] Creating *v1.Namespace assisted-installer took: 4.426423ms
I0719 01:46:01.764045   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-dns
I0719 01:46:01.764051   37437 namespace.go:100] [openshift-dns] adding namespace
I0719 01:46:01.764026   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.0.9 10.129.2.11 10.129.0.5 10.128.0.8]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-etcd:v4 k8s.ovn.org/name:openshift-etcd k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {d75a7453-719e-42f4-9198-95782be1eecd}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.764064   37437 address_set.go:304] New(d75a7453-719e-42f4-9198-95782be1eecd/default-network-controller:Namespace:openshift-etcd:v4/a1263951348256964356) with [10.129.0.9 10.129.2.11 10.129.0.5 10.128.0.8]
I0719 01:46:01.764075   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.0.9 10.129.2.11 10.129.0.5 10.128.0.8]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-etcd:v4 k8s.ovn.org/name:openshift-etcd k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {d75a7453-719e-42f4-9198-95782be1eecd}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.764417   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.128.0.28]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-service-ca-operator:v4 k8s.ovn.org/name:openshift-service-ca-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {c9260bfe-40d4-47d1-bcdf-12e8f2f36a6e}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.764445   37437 address_set.go:304] New(c9260bfe-40d4-47d1-bcdf-12e8f2f36a6e/default-network-controller:Namespace:openshift-service-ca-operator:v4/a9531058592630863333) with [10.128.0.28]
I0719 01:46:01.764455   37437 namespace.go:104] [openshift-etcd] adding namespace took 4.623651ms
I0719 01:46:01.764451   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.128.0.28]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-service-ca-operator:v4 k8s.ovn.org/name:openshift-service-ca-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {c9260bfe-40d4-47d1-bcdf-12e8f2f36a6e}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.764466   37437 obj_retry.go:541] Creating *v1.Namespace openshift-etcd took: 4.638338ms
I0719 01:46:01.764478   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-controller-manager-operator
I0719 01:46:01.764485   37437 namespace.go:100] [openshift-controller-manager-operator] adding namespace
I0719 01:46:01.765027   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.80]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-image-registry:v4 k8s.ovn.org/name:openshift-image-registry k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {468f827d-e692-4f8a-8b7e-c261e6905f5a}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.765128   37437 address_set.go:304] New(468f827d-e692-4f8a-8b7e-c261e6905f5a/default-network-controller:Namespace:openshift-image-registry:v4/a65811733811199347) with [10.129.2.80]
I0719 01:46:01.765131   37437 ovs.go:162] Exec(23): stdout: ""
I0719 01:46:01.765149   37437 ovs.go:163] Exec(23): stderr: "ovs-vsctl: no port named br-ex\n"
I0719 01:46:01.765161   37437 ovs.go:165] Exec(23): err: exit status 1
I0719 01:46:01.765138   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.80]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-image-registry:v4 k8s.ovn.org/name:openshift-image-registry k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {468f827d-e692-4f8a-8b7e-c261e6905f5a}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.765109   37437 namespace.go:104] [openshift-service-ca-operator] adding namespace took 4.955878ms
I0719 01:46:01.765201   37437 obj_retry.go:541] Creating *v1.Namespace openshift-service-ca-operator took: 5.053791ms
I0719 01:46:01.765214   37437 obj_retry.go:502] Add event received for *v1.Namespace openshift-service-ca
I0719 01:46:01.765225   37437 namespace.go:100] [openshift-service-ca] adding namespace
I0719 01:46:01.765303   37437 helper_linux.go:92] Provided gateway interface "br-ex", found as index: 8
I0719 01:46:01.765453   37437 helper_linux.go:117] Found default gateway interface br-ex 10.10.25.1
I0719 01:46:01.765600   37437 gateway_init.go:374] Preparing Shared Gateway
I0719 01:46:01.765615   37437 gateway_shared_intf.go:1721] Creating new shared gateway
I0719 01:46:01.765632   37437 ovs.go:159] Exec(24): /usr/bin/ovs-vsctl --timeout=15 port-to-br br-ex
I0719 01:46:01.766241   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-config:v4 k8s.ovn.org/name:openshift-config k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {9d9fbf98-1565-47cb-b7cc-b48e5425b530}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.766304   37437 address_set.go:304] New(9d9fbf98-1565-47cb-b7cc-b48e5425b530/default-network-controller:Namespace:openshift-config:v4/a14322580666718461836) with []
I0719 01:46:01.766315   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-config:v4 k8s.ovn.org/name:openshift-config k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {9d9fbf98-1565-47cb-b7cc-b48e5425b530}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.766556   37437 namespace.go:104] [openshift-image-registry] adding namespace took 5.266354ms
I0719 01:46:01.766577   37437 obj_retry.go:541] Creating *v1.Namespace openshift-image-registry took: 5.291956ms
I0719 01:46:01.766896   37437 namespace.go:104] [openshift-config] adding namespace took 5.233949ms
I0719 01:46:01.766921   37437 obj_retry.go:541] Creating *v1.Namespace openshift-config took: 5.336465ms
I0719 01:46:01.766979   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.12 10.128.0.14]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-controller-manager:v4 k8s.ovn.org/name:openshift-controller-manager k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {afdc9c37-65ce-46f5-b49d-d5479a81b654}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.767038   37437 address_set.go:304] New(afdc9c37-65ce-46f5-b49d-d5479a81b654/default-network-controller:Namespace:openshift-controller-manager:v4/a10467312518402121836) with [10.129.2.12 10.128.0.14]
I0719 01:46:01.767045   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.12 10.128.0.14]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-controller-manager:v4 k8s.ovn.org/name:openshift-controller-manager k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {afdc9c37-65ce-46f5-b49d-d5479a81b654}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.768023   37437 namespace.go:104] [openshift-controller-manager] adding namespace took 6.127286ms
I0719 01:46:01.768039   37437 obj_retry.go:541] Creating *v1.Namespace openshift-controller-manager took: 6.148398ms
I0719 01:46:01.768075   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.62]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-apiserver-operator:v4 k8s.ovn.org/name:openshift-apiserver-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {2fa532ab-3219-4cc8-8029-9f88da28c3a6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.768103   37437 address_set.go:304] New(2fa532ab-3219-4cc8-8029-9f88da28c3a6/default-network-controller:Namespace:openshift-apiserver-operator:v4/a17733727332347776420) with [10.129.2.62]
I0719 01:46:01.768110   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.62]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-apiserver-operator:v4 k8s.ovn.org/name:openshift-apiserver-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {2fa532ab-3219-4cc8-8029-9f88da28c3a6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.768432   37437 namespace.go:104] [openshift-apiserver-operator] adding namespace took 6.2067ms
I0719 01:46:01.768442   37437 obj_retry.go:541] Creating *v1.Namespace openshift-apiserver-operator took: 6.220689ms
I0719 01:46:01.768503   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.131.0.11 10.129.2.9 10.130.0.3 10.129.0.3 10.128.2.3 10.131.0.3 10.128.0.3]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-network-diagnostics:v4 k8s.ovn.org/name:openshift-network-diagnostics k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {41ec6041-61e5-4831-9116-03810e7667bd}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.768545   37437 address_set.go:304] New(41ec6041-61e5-4831-9116-03810e7667bd/default-network-controller:Namespace:openshift-network-diagnostics:v4/a1966919964212966539) with [10.128.0.3 10.131.0.11 10.129.2.9 10.130.0.3 10.129.0.3 10.128.2.3 10.131.0.3]
I0719 01:46:01.768552   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.131.0.11 10.129.2.9 10.130.0.3 10.129.0.3 10.128.2.3 10.131.0.3 10.128.0.3]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-network-diagnostics:v4 k8s.ovn.org/name:openshift-network-diagnostics k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {41ec6041-61e5-4831-9116-03810e7667bd}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.768887   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.128.0.29 10.128.0.42 10.128.0.36 10.128.0.39 10.129.2.72 10.128.0.24 10.128.0.19]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-machine-api:v4 k8s.ovn.org/name:openshift-machine-api k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {9e74cef1-586b-4bed-b81e-e30d139bfbb8}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.768930   37437 address_set.go:304] New(9e74cef1-586b-4bed-b81e-e30d139bfbb8/default-network-controller:Namespace:openshift-machine-api:v4/a8146979490545162082) with [10.128.0.39 10.129.2.72 10.128.0.24 10.128.0.19 10.128.0.29 10.128.0.42 10.128.0.36]
I0719 01:46:01.768937   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.128.0.29 10.128.0.42 10.128.0.36 10.128.0.39 10.129.2.72 10.128.0.24 10.128.0.19]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-machine-api:v4 k8s.ovn.org/name:openshift-machine-api k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {9e74cef1-586b-4bed-b81e-e30d139bfbb8}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.768898   37437 namespace.go:104] [openshift-network-diagnostics] adding namespace took 6.454512ms
I0719 01:46:01.769022   37437 obj_retry.go:541] Creating *v1.Namespace openshift-network-diagnostics took: 6.582228ms
I0719 01:46:01.769295   37437 namespace.go:104] [openshift-machine-api] adding namespace took 6.335745ms
I0719 01:46:01.769314   37437 obj_retry.go:541] Creating *v1.Namespace openshift-machine-api took: 6.363007ms
I0719 01:46:01.769357   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift:v4 k8s.ovn.org/name:openshift k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {4ea61001-4ee8-4a2e-844c-b7ae4b1394a6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.769432   37437 address_set.go:304] New(4ea61001-4ee8-4a2e-844c-b7ae4b1394a6/default-network-controller:Namespace:openshift:v4/a8611152139381270309) with []
I0719 01:46:01.769463   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift:v4 k8s.ovn.org/name:openshift k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {4ea61001-4ee8-4a2e-844c-b7ae4b1394a6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.769993   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.68 10.128.0.44 10.128.0.26 10.129.2.69 10.129.2.63]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-operator-lifecycle-manager:v4 k8s.ovn.org/name:openshift-operator-lifecycle-manager k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {575fa52c-db50-4745-88b9-948435e2dbe8}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.770019   37437 address_set.go:304] New(575fa52c-db50-4745-88b9-948435e2dbe8/default-network-controller:Namespace:openshift-operator-lifecycle-manager:v4/a1482332553631220387) with [10.128.0.44 10.128.0.26 10.129.2.69 10.129.2.63 10.129.2.68]
I0719 01:46:01.770027   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.68 10.128.0.44 10.128.0.26 10.129.2.69 10.129.2.63]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-operator-lifecycle-manager:v4 k8s.ovn.org/name:openshift-operator-lifecycle-manager k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {575fa52c-db50-4745-88b9-948435e2dbe8}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.770090   37437 namespace.go:104] [openshift] adding namespace took 6.861538ms
I0719 01:46:01.770136   37437 obj_retry.go:541] Creating *v1.Namespace openshift took: 6.91261ms
I0719 01:46:01.770375   37437 namespace.go:104] [openshift-operator-lifecycle-manager] adding namespace took 6.614016ms
I0719 01:46:01.770388   37437 obj_retry.go:541] Creating *v1.Namespace openshift-operator-lifecycle-manager took: 6.633888ms
I0719 01:46:01.770470   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.0.39 10.130.0.5 10.129.2.14 10.128.0.11 10.128.2.5 10.131.0.13]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-dns:v4 k8s.ovn.org/name:openshift-dns k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {35a9889d-4873-4857-ac47-d7249158d652}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.770542   37437 address_set.go:304] New(35a9889d-4873-4857-ac47-d7249158d652/default-network-controller:Namespace:openshift-dns:v4/a11732331429224425771) with [10.131.0.13 10.129.0.39 10.130.0.5 10.129.2.14 10.128.0.11 10.128.2.5]
I0719 01:46:01.770553   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.0.39 10.130.0.5 10.129.2.14 10.128.0.11 10.128.2.5 10.131.0.13]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-dns:v4 k8s.ovn.org/name:openshift-dns k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {35a9889d-4873-4857-ac47-d7249158d652}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.770957   37437 namespace.go:104] [openshift-dns] adding namespace took 6.900522ms
I0719 01:46:01.770968   37437 obj_retry.go:541] Creating *v1.Namespace openshift-dns took: 6.916037ms
I0719 01:46:01.771063   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.85]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-controller-manager-operator:v4 k8s.ovn.org/name:openshift-controller-manager-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {f3205854-3013-4942-93f2-fe168ab9c838}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.771140   37437 address_set.go:304] New(f3205854-3013-4942-93f2-fe168ab9c838/default-network-controller:Namespace:openshift-controller-manager-operator:v4/a14938231737766799037) with [10.129.2.85]
I0719 01:46:01.771180   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.129.2.85]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-controller-manager-operator:v4 k8s.ovn.org/name:openshift-controller-manager-operator k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {f3205854-3013-4942-93f2-fe168ab9c838}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.771579   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.128.0.25]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-service-ca:v4 k8s.ovn.org/name:openshift-service-ca k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {3fdde7ff-788f-453a-bb7d-a035d1a41ed1}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.771603   37437 address_set.go:304] New(3fdde7ff-788f-453a-bb7d-a035d1a41ed1/default-network-controller:Namespace:openshift-service-ca:v4/a15543462790031426324) with [10.128.0.25]
I0719 01:46:01.771609   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.128.0.25]} external_ids:{GoMap:map[ip-family:v4 k8s.ovn.org/id:default-network-controller:Namespace:openshift-service-ca:v4 k8s.ovn.org/name:openshift-service-ca k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:Namespace]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {3fdde7ff-788f-453a-bb7d-a035d1a41ed1}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.771658   37437 namespace.go:104] [openshift-controller-manager-operator] adding namespace took 7.104583ms
I0719 01:46:01.771688   37437 obj_retry.go:541] Creating *v1.Namespace openshift-controller-manager-operator took: 7.200177ms
I0719 01:46:01.771853   37437 namespace.go:104] [openshift-service-ca] adding namespace took 6.620947ms
I0719 01:46:01.771865   37437 obj_retry.go:541] Creating *v1.Namespace openshift-service-ca took: 6.641926ms
I0719 01:46:01.771880   37437 factory.go:988] Added *v1.Namespace event handler 1
I0719 01:46:01.772125   37437 obj_retry.go:502] Add event received for *v1.Node 00-50-56-8a-5c-ec
I0719 01:46:01.772136   37437 obj_retry.go:502] Add event received for *v1.Node 00-50-56-8a-39-a0
I0719 01:46:01.772280   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Encap Row:map[chassis_name:48ef73f0-c449-4501-b68d-9d975ad26497 ip:10.10.25.192 options:{GoMap:map[csum:true]} type:geneve] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {ea6bcded-6365-45f0-91f5-9ba39a05081b}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.772325   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Encap Row:map[chassis_name:0af75963-cff9-4195-8768-b3c765dda596 ip:10.10.25.190 options:{GoMap:map[csum:true]} type:geneve] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {6736770e-592e-45e6-bd21-5df255431f19}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.772377   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Chassis Row:map[encaps:{GoSet:[{GoUUID:6736770e-592e-45e6-bd21-5df255431f19}]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {f6049807-ed8b-4ad4-a307-3fc16579e45a}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.772406   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Chassis Row:map[] Rows:[] Columns:[] Mutations:[{Column:other_config Mutator:delete Value:{GoSet:[is-remote]}} {Column:other_config Mutator:insert Value:{GoMap:map[is-remote:true]}}] Timeout:<nil> Where:[where column _uuid == {f6049807-ed8b-4ad4-a307-3fc16579e45a}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.772389   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Chassis Row:map[encaps:{GoSet:[{GoUUID:ea6bcded-6365-45f0-91f5-9ba39a05081b}]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {5ae55940-179a-4276-ad3f-41554f63ecab}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.772488   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Chassis Row:map[] Rows:[] Columns:[] Mutations:[{Column:other_config Mutator:delete Value:{GoSet:[is-remote]}} {Column:other_config Mutator:insert Value:{GoMap:map[is-remote:true]}}] Timeout:<nil> Where:[where column _uuid == {5ae55940-179a-4276-ad3f-41554f63ecab}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.772536   37437 transact.go:42] Configuring OVN: [{Op:update Table:Encap Row:map[chassis_name:48ef73f0-c449-4501-b68d-9d975ad26497 ip:10.10.25.192 options:{GoMap:map[csum:true]} type:geneve] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {ea6bcded-6365-45f0-91f5-9ba39a05081b}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:update Table:Chassis Row:map[encaps:{GoSet:[{GoUUID:ea6bcded-6365-45f0-91f5-9ba39a05081b}]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {5ae55940-179a-4276-ad3f-41554f63ecab}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Chassis Row:map[] Rows:[] Columns:[] Mutations:[{Column:other_config Mutator:delete Value:{GoSet:[is-remote]}} {Column:other_config Mutator:insert Value:{GoMap:map[is-remote:true]}}] Timeout:<nil> Where:[where column _uuid == {5ae55940-179a-4276-ad3f-41554f63ecab}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.772426   37437 transact.go:42] Configuring OVN: [{Op:update Table:Encap Row:map[chassis_name:0af75963-cff9-4195-8768-b3c765dda596 ip:10.10.25.190 options:{GoMap:map[csum:true]} type:geneve] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {6736770e-592e-45e6-bd21-5df255431f19}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:update Table:Chassis Row:map[encaps:{GoSet:[{GoUUID:6736770e-592e-45e6-bd21-5df255431f19}]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {f6049807-ed8b-4ad4-a307-3fc16579e45a}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Chassis Row:map[] Rows:[] Columns:[] Mutations:[{Column:other_config Mutator:delete Value:{GoSet:[is-remote]}} {Column:other_config Mutator:insert Value:{GoMap:map[is-remote:true]}}] Timeout:<nil> Where:[where column _uuid == {f6049807-ed8b-4ad4-a307-3fc16579e45a}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.772148   37437 obj_retry.go:502] Add event received for *v1.Node 00-50-56-8a-f2-5d
I0719 01:46:01.772887   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Encap Row:map[chassis_name:0a949bf0-1b14-4733-a246-3125b962a9fb ip:10.10.25.191 options:{GoMap:map[csum:true]} type:geneve] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {a6b26320-099a-4990-bf48-0414ed78ea9d}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.772929   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Chassis Row:map[encaps:{GoSet:[{GoUUID:a6b26320-099a-4990-bf48-0414ed78ea9d}]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {46e73ec6-ce08-4a58-9fa0-2b7da4a632da}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.772154   37437 obj_retry.go:502] Add event received for *v1.Node 00-50-56-8a-fb-ea
I0719 01:46:01.772954   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Chassis Row:map[] Rows:[] Columns:[] Mutations:[{Column:other_config Mutator:delete Value:{GoSet:[is-remote]}} {Column:other_config Mutator:insert Value:{GoMap:map[is-remote:true]}}] Timeout:<nil> Where:[where column _uuid == {46e73ec6-ce08-4a58-9fa0-2b7da4a632da}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.772154   37437 obj_retry.go:502] Add event received for *v1.Node 00-50-56-8a-44-52
I0719 01:46:01.772998   37437 master.go:627] Adding or Updating Node "00-50-56-8a-fb-ea"
I0719 01:46:01.772969   37437 transact.go:42] Configuring OVN: [{Op:update Table:Encap Row:map[chassis_name:0a949bf0-1b14-4733-a246-3125b962a9fb ip:10.10.25.191 options:{GoMap:map[csum:true]} type:geneve] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {a6b26320-099a-4990-bf48-0414ed78ea9d}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:update Table:Chassis Row:map[encaps:{GoSet:[{GoUUID:a6b26320-099a-4990-bf48-0414ed78ea9d}]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {46e73ec6-ce08-4a58-9fa0-2b7da4a632da}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Chassis Row:map[] Rows:[] Columns:[] Mutations:[{Column:other_config Mutator:delete Value:{GoSet:[is-remote]}} {Column:other_config Mutator:insert Value:{GoMap:map[is-remote:true]}}] Timeout:<nil> Where:[where column _uuid == {46e73ec6-ce08-4a58-9fa0-2b7da4a632da}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.773066   37437 zone_ic_handler.go:238] Creating interconnect resources for remote zone node 00-50-56-8a-39-a0 for the network default
I0719 01:46:01.773090   37437 zone_ic_handler.go:238] Creating interconnect resources for remote zone node 00-50-56-8a-5c-ec for the network default
I0719 01:46:01.773058   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Encap Row:map[chassis_name:58c4d980-bdb4-4f4c-9ae1-1f15f1e86529 ip:10.10.25.203 options:{GoMap:map[csum:true]} type:geneve] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {adc6796f-5705-42af-99b7-956032e99c53}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.773188   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Switch Row:map[load_balancer_group:{GoSet:[{GoUUID:2400c21d-35b5-4059-bdc0-cfe46ebce829} {GoUUID:aea29a04-5376-45bc-b303-62d4a3f5c7bb}]} other_config:{GoMap:map[exclude_ips:10.130.0.2 mcast_eth_src:0a:58:0a:82:00:01 mcast_ip4_src:10.130.0.1 mcast_querier:true mcast_snoop:true subnet:10.130.0.0/23]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {bc57259c-2feb-4fdd-95c3-dc98eb57f6e4}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.773211   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[0a:58:64:58:00:07 100.88.0.7/16]} options:{GoMap:map[requested-tnl-key:7]} port_security:{GoSet:[]} tag_request:{GoSet:[]} type:remote] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {9b8bedd6-4f43-4c3d-9f7f-faa77e069023}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.773225   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Switch Row:map[load_balancer_group:{GoSet:[{GoUUID:2400c21d-35b5-4059-bdc0-cfe46ebce829} {GoUUID:aea29a04-5376-45bc-b303-62d4a3f5c7bb}]} other_config:{GoMap:map[exclude_ips:10.130.0.2 mcast_eth_src:0a:58:0a:82:00:01 mcast_ip4_src:10.130.0.1 mcast_querier:true mcast_snoop:true subnet:10.130.0.0/23]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {bc57259c-2feb-4fdd-95c3-dc98eb57f6e4}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.773267   37437 zone_ic_handler.go:238] Creating interconnect resources for remote zone node 00-50-56-8a-f2-5d for the network default
I0719 01:46:01.773223   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Chassis Row:map[encaps:{GoSet:[{GoUUID:adc6796f-5705-42af-99b7-956032e99c53}]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {ed7c5a76-537d-4c67-b2a7-082476117b57}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.773296   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Chassis Row:map[] Rows:[] Columns:[] Mutations:[{Column:other_config Mutator:delete Value:{GoSet:[is-remote]}} {Column:other_config Mutator:insert Value:{GoMap:map[is-remote:true]}}] Timeout:<nil> Where:[where column _uuid == {ed7c5a76-537d-4c67-b2a7-082476117b57}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.772146   37437 obj_retry.go:502] Add event received for *v1.Node 00-50-56-8a-e1-e7
I0719 01:46:01.773391   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[0a:58:64:58:00:06 100.88.0.6/16]} options:{GoMap:map[requested-tnl-key:6]} port_security:{GoSet:[]} tag_request:{GoSet:[]} type:remote] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {91fddfb4-6c6f-40df-a73d-479d50748793}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.773429   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:91fddfb4-6c6f-40df-a73d-479d50748793}]}}] Timeout:<nil> Where:[where column _uuid == {86ba2710-ebc4-4689-adf6-f6f48ae98fa3}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.773263   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:9b8bedd6-4f43-4c3d-9f7f-faa77e069023}]}}] Timeout:<nil> Where:[where column _uuid == {86ba2710-ebc4-4689-adf6-f6f48ae98fa3}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.773444   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[0a:58:64:58:00:06 100.88.0.6/16]} options:{GoMap:map[requested-tnl-key:6]} port_security:{GoSet:[]} tag_request:{GoSet:[]} type:remote] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {91fddfb4-6c6f-40df-a73d-479d50748793}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:91fddfb4-6c6f-40df-a73d-479d50748793}]}}] Timeout:<nil> Where:[where column _uuid == {86ba2710-ebc4-4689-adf6-f6f48ae98fa3}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.773478   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[0a:58:64:58:00:07 100.88.0.7/16]} options:{GoMap:map[requested-tnl-key:7]} port_security:{GoSet:[]} tag_request:{GoSet:[]} type:remote] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {9b8bedd6-4f43-4c3d-9f7f-faa77e069023}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:9b8bedd6-4f43-4c3d-9f7f-faa77e069023}]}}] Timeout:<nil> Where:[where column _uuid == {86ba2710-ebc4-4689-adf6-f6f48ae98fa3}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.773326   37437 transact.go:42] Configuring OVN: [{Op:update Table:Encap Row:map[chassis_name:58c4d980-bdb4-4f4c-9ae1-1f15f1e86529 ip:10.10.25.203 options:{GoMap:map[csum:true]} type:geneve] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {adc6796f-5705-42af-99b7-956032e99c53}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:update Table:Chassis Row:map[encaps:{GoSet:[{GoUUID:adc6796f-5705-42af-99b7-956032e99c53}]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {ed7c5a76-537d-4c67-b2a7-082476117b57}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Chassis Row:map[] Rows:[] Columns:[] Mutations:[{Column:other_config Mutator:delete Value:{GoSet:[is-remote]}} {Column:other_config Mutator:insert Value:{GoMap:map[is-remote:true]}}] Timeout:<nil> Where:[where column _uuid == {ed7c5a76-537d-4c67-b2a7-082476117b57}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.773591   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[0a:58:64:58:00:02 100.88.0.2/16]} options:{GoMap:map[requested-tnl-key:2]} port_security:{GoSet:[]} tag_request:{GoSet:[]} type:remote] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {bd410cba-27b4-4607-aa9f-c5fa343a2958}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.773439   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Encap Row:map[chassis_name:9733f6f5-f080-4d63-badb-da12dc045b62 ip:10.10.25.250 options:{GoMap:map[csum:true]} type:geneve] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {04f7dc82-8524-44f9-aa31-14bb397c09fb}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.773689   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:bd410cba-27b4-4607-aa9f-c5fa343a2958}]}}] Timeout:<nil> Where:[where column _uuid == {86ba2710-ebc4-4689-adf6-f6f48ae98fa3}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.773727   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[0a:58:64:58:00:02 100.88.0.2/16]} options:{GoMap:map[requested-tnl-key:2]} port_security:{GoSet:[]} tag_request:{GoSet:[]} type:remote] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {bd410cba-27b4-4607-aa9f-c5fa343a2958}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:bd410cba-27b4-4607-aa9f-c5fa343a2958}]}}] Timeout:<nil> Where:[where column _uuid == {86ba2710-ebc4-4689-adf6-f6f48ae98fa3}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.773694   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Chassis Row:map[encaps:{GoSet:[{GoUUID:04f7dc82-8524-44f9-aa31-14bb397c09fb}]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {1c109b05-688a-4408-9ade-f6db51c258ec}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.773896   37437 ovs.go:162] Exec(24): stdout: ""
I0719 01:46:01.773907   37437 ovs.go:163] Exec(24): stderr: "ovs-vsctl: no port named br-ex\n"
I0719 01:46:01.773911   37437 zone_ic_handler.go:238] Creating interconnect resources for remote zone node 00-50-56-8a-44-52 for the network default
I0719 01:46:01.773914   37437 ovs.go:165] Exec(24): err: exit status 1
I0719 01:46:01.773962   37437 ovs.go:159] Exec(25): /usr/bin/ovs-vsctl --timeout=15 br-exists br-ex
I0719 01:46:01.773903   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Chassis Row:map[] Rows:[] Columns:[] Mutations:[{Column:other_config Mutator:delete Value:{GoSet:[is-remote]}} {Column:other_config Mutator:insert Value:{GoMap:map[is-remote:true]}}] Timeout:<nil> Where:[where column _uuid == {1c109b05-688a-4408-9ade-f6db51c258ec}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.774018   37437 transact.go:42] Configuring OVN: [{Op:update Table:Encap Row:map[chassis_name:9733f6f5-f080-4d63-badb-da12dc045b62 ip:10.10.25.250 options:{GoMap:map[csum:true]} type:geneve] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {04f7dc82-8524-44f9-aa31-14bb397c09fb}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:update Table:Chassis Row:map[encaps:{GoSet:[{GoUUID:04f7dc82-8524-44f9-aa31-14bb397c09fb}]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {1c109b05-688a-4408-9ade-f6db51c258ec}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Chassis Row:map[] Rows:[] Columns:[] Mutations:[{Column:other_config Mutator:delete Value:{GoSet:[is-remote]}} {Column:other_config Mutator:insert Value:{GoMap:map[is-remote:true]}}] Timeout:<nil> Where:[where column _uuid == {1c109b05-688a-4408-9ade-f6db51c258ec}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.774091   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[0a:58:64:58:00:03 100.88.0.3/16]} options:{GoMap:map[requested-tnl-key:3]} port_security:{GoSet:[]} tag_request:{GoSet:[]} type:remote] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {245ec315-e8a5-4ae9-974a-eeac89c369c6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.774143   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:245ec315-e8a5-4ae9-974a-eeac89c369c6}]}}] Timeout:<nil> Where:[where column _uuid == {86ba2710-ebc4-4689-adf6-f6f48ae98fa3}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.774166   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[0a:58:64:58:00:03 100.88.0.3/16]} options:{GoMap:map[requested-tnl-key:3]} port_security:{GoSet:[]} tag_request:{GoSet:[]} type:remote] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {245ec315-e8a5-4ae9-974a-eeac89c369c6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:245ec315-e8a5-4ae9-974a-eeac89c369c6}]}}] Timeout:<nil> Where:[where column _uuid == {86ba2710-ebc4-4689-adf6-f6f48ae98fa3}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.774194   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Port_Binding Row:map[chassis:{GoSet:[{GoUUID:46e73ec6-ce08-4a58-9fa0-2b7da4a632da}]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {7b6bc6bc-7f9f-4aaf-8c3e-d46a6491f9f8}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.774222   37437 transact.go:42] Configuring OVN: [{Op:update Table:Port_Binding Row:map[chassis:{GoSet:[{GoUUID:46e73ec6-ce08-4a58-9fa0-2b7da4a632da}]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {7b6bc6bc-7f9f-4aaf-8c3e-d46a6491f9f8}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.774220   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Port_Binding Row:map[chassis:{GoSet:[{GoUUID:5ae55940-179a-4276-ad3f-41554f63ecab}]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {dcf80149-e895-48c6-80e8-a2d73cedda2a}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.774244   37437 transact.go:42] Configuring OVN: [{Op:update Table:Port_Binding Row:map[chassis:{GoSet:[{GoUUID:5ae55940-179a-4276-ad3f-41554f63ecab}]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {dcf80149-e895-48c6-80e8-a2d73cedda2a}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.774216   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[router]} options:{GoMap:map[arp_proxy:0a:58:a9:fe:01:01 169.254.1.1 fe80::1 10.128.0.0/14 router-port:rtos-00-50-56-8a-fb-ea]} port_security:{GoSet:[]} tag_request:{GoSet:[]} type:router] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {b5c6a263-62bc-417a-9ffc-d748b02eebf4}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.774204   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Port_Binding Row:map[chassis:{GoSet:[{GoUUID:f6049807-ed8b-4ad4-a307-3fc16579e45a}]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {69841ee9-ab3a-450f-8438-30c6c2796143}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.774279   37437 transact.go:42] Configuring OVN: [{Op:update Table:Port_Binding Row:map[chassis:{GoSet:[{GoUUID:f6049807-ed8b-4ad4-a307-3fc16579e45a}]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {69841ee9-ab3a-450f-8438-30c6c2796143}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.774303   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:b5c6a263-62bc-417a-9ffc-d748b02eebf4}]}}] Timeout:<nil> Where:[where column _uuid == {bc57259c-2feb-4fdd-95c3-dc98eb57f6e4}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.774327   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[router]} options:{GoMap:map[arp_proxy:0a:58:a9:fe:01:01 169.254.1.1 fe80::1 10.128.0.0/14 router-port:rtos-00-50-56-8a-fb-ea]} port_security:{GoSet:[]} tag_request:{GoSet:[]} type:router] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {b5c6a263-62bc-417a-9ffc-d748b02eebf4}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:b5c6a263-62bc-417a-9ffc-d748b02eebf4}]}}] Timeout:<nil> Where:[where column _uuid == {bc57259c-2feb-4fdd-95c3-dc98eb57f6e4}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.774543   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Port_Binding Row:map[chassis:{GoSet:[{GoUUID:ed7c5a76-537d-4c67-b2a7-082476117b57}]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {c66163aa-ff89-4ce6-ad10-dd08424fb7d0}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.774569   37437 transact.go:42] Configuring OVN: [{Op:update Table:Port_Binding Row:map[chassis:{GoSet:[{GoUUID:ed7c5a76-537d-4c67-b2a7-082476117b57}]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {c66163aa-ff89-4ce6-ad10-dd08424fb7d0}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.774656   37437 zone_ic_handler.go:238] Creating interconnect resources for remote zone node 00-50-56-8a-e1-e7 for the network default
I0719 01:46:01.774662   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Port_Group Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:b5c6a263-62bc-417a-9ffc-d748b02eebf4}]}}] Timeout:<nil> Where:[where column _uuid == {620dbd54-29f5-47b2-949a-b9f74c1cd372}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.774687   37437 transact.go:42] Configuring OVN: [{Op:mutate Table:Port_Group Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:b5c6a263-62bc-417a-9ffc-d748b02eebf4}]}}] Timeout:<nil> Where:[where column _uuid == {620dbd54-29f5-47b2-949a-b9f74c1cd372}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.774805   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[0a:58:64:58:00:05 100.88.0.5/16]} options:{GoMap:map[requested-tnl-key:5]} port_security:{GoSet:[]} tag_request:{GoSet:[]} type:remote] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {574ecbdb-f54b-4316-ba9d-c1dd8e5e8c29}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.774849   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:574ecbdb-f54b-4316-ba9d-c1dd8e5e8c29}]}}] Timeout:<nil> Where:[where column _uuid == {86ba2710-ebc4-4689-adf6-f6f48ae98fa3}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.774864   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[0a:58:64:58:00:05 100.88.0.5/16]} options:{GoMap:map[requested-tnl-key:5]} port_security:{GoSet:[]} tag_request:{GoSet:[]} type:remote] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {574ecbdb-f54b-4316-ba9d-c1dd8e5e8c29}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:574ecbdb-f54b-4316-ba9d-c1dd8e5e8c29}]}}] Timeout:<nil> Where:[where column _uuid == {86ba2710-ebc4-4689-adf6-f6f48ae98fa3}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.774889   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Router_Static_Route Row:map[external_ids:{GoMap:map[ic-node:00-50-56-8a-5c-ec]} ip_prefix:10.129.2.0/23 nexthop:100.88.0.7] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {fc05709f-f0d4-4734-b3fd-fd5e3c374117}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.774925   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:insert Value:{GoSet:[{GoUUID:fc05709f-f0d4-4734-b3fd-fd5e3c374117}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.774947   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Router_Static_Route Row:map[external_ids:{GoMap:map[ic-node:00-50-56-8a-5c-ec]} ip_prefix:10.129.2.0/23 nexthop:100.88.0.7] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {fc05709f-f0d4-4734-b3fd-fd5e3c374117}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:insert Value:{GoSet:[{GoUUID:fc05709f-f0d4-4734-b3fd-fd5e3c374117}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.774997   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Router_Static_Route Row:map[external_ids:{GoMap:map[ic-node:00-50-56-8a-f2-5d]} ip_prefix:10.128.2.0/23 nexthop:100.88.0.6] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {46505a33-8960-4e2d-aceb-3de4dcbc5013}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.775058   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:insert Value:{GoSet:[{GoUUID:46505a33-8960-4e2d-aceb-3de4dcbc5013}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.775077   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Router_Static_Route Row:map[external_ids:{GoMap:map[ic-node:00-50-56-8a-44-52]} ip_prefix:10.129.0.0/23 nexthop:100.88.0.3] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {efcb70a3-a107-4e35-b570-9ca05d71289a}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.775087   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Router_Static_Route Row:map[external_ids:{GoMap:map[ic-node:00-50-56-8a-f2-5d]} ip_prefix:10.128.2.0/23 nexthop:100.88.0.6] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {46505a33-8960-4e2d-aceb-3de4dcbc5013}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:insert Value:{GoSet:[{GoUUID:46505a33-8960-4e2d-aceb-3de4dcbc5013}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.775137   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:insert Value:{GoSet:[{GoUUID:efcb70a3-a107-4e35-b570-9ca05d71289a}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.775171   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Router_Static_Route Row:map[external_ids:{GoMap:map[ic-node:00-50-56-8a-44-52]} ip_prefix:10.129.0.0/23 nexthop:100.88.0.3] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {efcb70a3-a107-4e35-b570-9ca05d71289a}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:insert Value:{GoSet:[{GoUUID:efcb70a3-a107-4e35-b570-9ca05d71289a}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.775211   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Router_Static_Route Row:map[external_ids:{GoMap:map[ic-node:00-50-56-8a-39-a0]} ip_prefix:10.128.0.0/23 nexthop:100.88.0.2] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {f9e7d6ce-92bd-4dba-a27f-dd70de98e6a9}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.775247   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:insert Value:{GoSet:[{GoUUID:f9e7d6ce-92bd-4dba-a27f-dd70de98e6a9}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.775265   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Router_Static_Route Row:map[external_ids:{GoMap:map[ic-node:00-50-56-8a-39-a0]} ip_prefix:10.128.0.0/23 nexthop:100.88.0.2] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {f9e7d6ce-92bd-4dba-a27f-dd70de98e6a9}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:insert Value:{GoSet:[{GoUUID:f9e7d6ce-92bd-4dba-a27f-dd70de98e6a9}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.775352   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Router_Static_Route Row:map[external_ids:{GoMap:map[ic-node:00-50-56-8a-5c-ec]} ip_prefix:100.64.0.7/32 nexthop:100.88.0.7] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {2e937692-a448-4b2f-ba22-0d2a5d5c0d13}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.775415   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:insert Value:{GoSet:[{GoUUID:2e937692-a448-4b2f-ba22-0d2a5d5c0d13}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.775452   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Router_Static_Route Row:map[external_ids:{GoMap:map[ic-node:00-50-56-8a-44-52]} ip_prefix:100.64.0.3/32 nexthop:100.88.0.3] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {bcb9515f-fe63-46ea-83f8-660eb7724a43}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.775444   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Router_Static_Route Row:map[external_ids:{GoMap:map[ic-node:00-50-56-8a-5c-ec]} ip_prefix:100.64.0.7/32 nexthop:100.88.0.7] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {2e937692-a448-4b2f-ba22-0d2a5d5c0d13}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:insert Value:{GoSet:[{GoUUID:2e937692-a448-4b2f-ba22-0d2a5d5c0d13}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.775487   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:insert Value:{GoSet:[{GoUUID:bcb9515f-fe63-46ea-83f8-660eb7724a43}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.775506   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Router_Static_Route Row:map[external_ids:{GoMap:map[ic-node:00-50-56-8a-44-52]} ip_prefix:100.64.0.3/32 nexthop:100.88.0.3] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {bcb9515f-fe63-46ea-83f8-660eb7724a43}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:insert Value:{GoSet:[{GoUUID:bcb9515f-fe63-46ea-83f8-660eb7724a43}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.775591   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Router_Static_Route Row:map[external_ids:{GoMap:map[ic-node:00-50-56-8a-f2-5d]} ip_prefix:100.64.0.6/32 nexthop:100.88.0.6] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {956840d7-3800-4cd0-8c7e-2017a157b1ae}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.775626   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Gateway_Chassis Row:map[chassis_name:ec7a39e5-89ad-4e47-a317-9fefe94160bf name:rtos-00-50-56-8a-fb-ea-ec7a39e5-89ad-4e47-a317-9fefe94160bf priority:1] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {9f1c445e-e3a3-4fd7-adfe-f9c69f421ec7}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.775643   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:insert Value:{GoSet:[{GoUUID:956840d7-3800-4cd0-8c7e-2017a157b1ae}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.775659   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Router_Static_Route Row:map[external_ids:{GoMap:map[ic-node:00-50-56-8a-f2-5d]} ip_prefix:100.64.0.6/32 nexthop:100.88.0.6] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {956840d7-3800-4cd0-8c7e-2017a157b1ae}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:insert Value:{GoSet:[{GoUUID:956840d7-3800-4cd0-8c7e-2017a157b1ae}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.775711   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Router_Port Row:map[gateway_chassis:{GoSet:[{GoUUID:9f1c445e-e3a3-4fd7-adfe-f9c69f421ec7}]} mac:0a:58:0a:82:00:01 networks:{GoSet:[10.130.0.1/23]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {171ebe0f-ec93-4a54-99a8-bbb6acd3c1af}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.775636   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Router_Static_Route Row:map[external_ids:{GoMap:map[ic-node:00-50-56-8a-39-a0]} ip_prefix:100.64.0.2/32 nexthop:100.88.0.2] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {0576c7f9-68e1-49e2-9555-91cdc0d30c6a}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.775748   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:171ebe0f-ec93-4a54-99a8-bbb6acd3c1af}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.775758   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:insert Value:{GoSet:[{GoUUID:0576c7f9-68e1-49e2-9555-91cdc0d30c6a}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.775765   37437 transact.go:42] Configuring OVN: [{Op:update Table:Gateway_Chassis Row:map[chassis_name:ec7a39e5-89ad-4e47-a317-9fefe94160bf name:rtos-00-50-56-8a-fb-ea-ec7a39e5-89ad-4e47-a317-9fefe94160bf priority:1] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {9f1c445e-e3a3-4fd7-adfe-f9c69f421ec7}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:update Table:Logical_Router_Port Row:map[gateway_chassis:{GoSet:[{GoUUID:9f1c445e-e3a3-4fd7-adfe-f9c69f421ec7}]} mac:0a:58:0a:82:00:01 networks:{GoSet:[10.130.0.1/23]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {171ebe0f-ec93-4a54-99a8-bbb6acd3c1af}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:171ebe0f-ec93-4a54-99a8-bbb6acd3c1af}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.775773   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Router_Static_Route Row:map[external_ids:{GoMap:map[ic-node:00-50-56-8a-39-a0]} ip_prefix:100.64.0.2/32 nexthop:100.88.0.2] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {0576c7f9-68e1-49e2-9555-91cdc0d30c6a}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:insert Value:{GoSet:[{GoUUID:0576c7f9-68e1-49e2-9555-91cdc0d30c6a}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.775465   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Port_Binding Row:map[chassis:{GoSet:[{GoUUID:1c109b05-688a-4408-9ade-f6db51c258ec}]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {fbe36f6b-15f8-41b3-9487-b4c7b311a379}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.775938   37437 transact.go:42] Configuring OVN: [{Op:update Table:Port_Binding Row:map[chassis:{GoSet:[{GoUUID:1c109b05-688a-4408-9ade-f6db51c258ec}]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {fbe36f6b-15f8-41b3-9487-b4c7b311a379}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.776164   37437 zone_ic_handler.go:255] Creating Interconnect resources for node 00-50-56-8a-44-52 took: 2.253137ms
I0719 01:46:01.776181   37437 master.go:780] Creating Interconnect resources for node 00-50-56-8a-44-52 took: 3.172104ms
I0719 01:46:01.776221   37437 obj_retry.go:541] Creating *v1.Node 00-50-56-8a-44-52 took: 3.213677ms
I0719 01:46:01.776245   37437 zone_ic_handler.go:255] Creating Interconnect resources for node 00-50-56-8a-5c-ec took: 3.155852ms
I0719 01:46:01.776250   37437 master.go:780] Creating Interconnect resources for node 00-50-56-8a-5c-ec took: 4.081422ms
I0719 01:46:01.776272   37437 obj_retry.go:541] Creating *v1.Node 00-50-56-8a-5c-ec took: 4.103645ms
I0719 01:46:01.776311   37437 zone_ic_handler.go:255] Creating Interconnect resources for node 00-50-56-8a-f2-5d took: 3.044827ms
I0719 01:46:01.776320   37437 master.go:780] Creating Interconnect resources for node 00-50-56-8a-f2-5d took: 3.487901ms
I0719 01:46:01.776341   37437 obj_retry.go:541] Creating *v1.Node 00-50-56-8a-f2-5d took: 3.509226ms
I0719 01:46:01.776397   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Router_Static_Route Row:map[external_ids:{GoMap:map[ic-node:00-50-56-8a-e1-e7]} ip_prefix:10.131.0.0/23 nexthop:100.88.0.5] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {7a843c5f-a6b2-4184-850f-b131a7d16a3f}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.776440   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:insert Value:{GoSet:[{GoUUID:7a843c5f-a6b2-4184-850f-b131a7d16a3f}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.776457   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Router_Static_Route Row:map[external_ids:{GoMap:map[ic-node:00-50-56-8a-e1-e7]} ip_prefix:10.131.0.0/23 nexthop:100.88.0.5] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {7a843c5f-a6b2-4184-850f-b131a7d16a3f}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:insert Value:{GoSet:[{GoUUID:7a843c5f-a6b2-4184-850f-b131a7d16a3f}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.776478   37437 model_client.go:381] Update operations generated as: [{Op:update Table:ACL Row:map[action:allow-related direction:to-lport external_ids:{GoMap:map[ip:10.130.0.2 k8s.ovn.org/id:default-network-controller:NetpolNode:00-50-56-8a-fb-ea:10.130.0.2 k8s.ovn.org/name:00-50-56-8a-fb-ea k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:NetpolNode]} log:false match:ip4.src==10.130.0.2 meter:{GoSet:[acl-logging]} name:{GoSet:[]} options:{GoMap:map[]} priority:1001 severity:{GoSet:[]} tier:2] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {b963f1bb-69f0-4455-b441-6bd4382161f6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.776537   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:acls Mutator:insert Value:{GoSet:[{GoUUID:b963f1bb-69f0-4455-b441-6bd4382161f6}]}}] Timeout:<nil> Where:[where column _uuid == {bc57259c-2feb-4fdd-95c3-dc98eb57f6e4}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.776559   37437 transact.go:42] Configuring OVN: [{Op:update Table:ACL Row:map[action:allow-related direction:to-lport external_ids:{GoMap:map[ip:10.130.0.2 k8s.ovn.org/id:default-network-controller:NetpolNode:00-50-56-8a-fb-ea:10.130.0.2 k8s.ovn.org/name:00-50-56-8a-fb-ea k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:NetpolNode]} log:false match:ip4.src==10.130.0.2 meter:{GoSet:[acl-logging]} name:{GoSet:[]} options:{GoMap:map[]} priority:1001 severity:{GoSet:[]} tier:2] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {b963f1bb-69f0-4455-b441-6bd4382161f6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:acls Mutator:insert Value:{GoSet:[{GoUUID:b963f1bb-69f0-4455-b441-6bd4382161f6}]}}] Timeout:<nil> Where:[where column _uuid == {bc57259c-2feb-4fdd-95c3-dc98eb57f6e4}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.776654   37437 zone_ic_handler.go:255] Creating Interconnect resources for node 00-50-56-8a-39-a0 took: 3.588229ms
I0719 01:46:01.776692   37437 master.go:780] Creating Interconnect resources for node 00-50-56-8a-39-a0 took: 4.445182ms
I0719 01:46:01.776757   37437 obj_retry.go:541] Creating *v1.Node 00-50-56-8a-39-a0 took: 4.510123ms
I0719 01:46:01.776808   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Router_Static_Route Row:map[external_ids:{GoMap:map[ic-node:00-50-56-8a-e1-e7]} ip_prefix:100.64.0.5/32 nexthop:100.88.0.5] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {1c94a8fe-c442-4248-8d23-0d886af68e47}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.776849   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:insert Value:{GoSet:[{GoUUID:1c94a8fe-c442-4248-8d23-0d886af68e47}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.776891   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Router_Static_Route Row:map[external_ids:{GoMap:map[ic-node:00-50-56-8a-e1-e7]} ip_prefix:100.64.0.5/32 nexthop:100.88.0.5] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {1c94a8fe-c442-4248-8d23-0d886af68e47}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:insert Value:{GoSet:[{GoUUID:1c94a8fe-c442-4248-8d23-0d886af68e47}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.777130   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[be:6d:32:1d:e9:29 10.130.0.2]} options:{GoMap:map[]} port_security:{GoSet:[]} tag_request:{GoSet:[]} type:] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {9bcc9b6b-d31a-4d64-8d2b-5fa4aae32b40}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.777202   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:9bcc9b6b-d31a-4d64-8d2b-5fa4aae32b40}]}}] Timeout:<nil> Where:[where column _uuid == {bc57259c-2feb-4fdd-95c3-dc98eb57f6e4}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.777225   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[be:6d:32:1d:e9:29 10.130.0.2]} options:{GoMap:map[]} port_security:{GoSet:[]} tag_request:{GoSet:[]} type:] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {9bcc9b6b-d31a-4d64-8d2b-5fa4aae32b40}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:9bcc9b6b-d31a-4d64-8d2b-5fa4aae32b40}]}}] Timeout:<nil> Where:[where column _uuid == {bc57259c-2feb-4fdd-95c3-dc98eb57f6e4}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.777280   37437 zone_ic_handler.go:255] Creating Interconnect resources for node 00-50-56-8a-e1-e7 took: 2.603882ms
I0719 01:46:01.777330   37437 master.go:780] Creating Interconnect resources for node 00-50-56-8a-e1-e7 took: 3.964771ms
I0719 01:46:01.777390   37437 obj_retry.go:541] Creating *v1.Node 00-50-56-8a-e1-e7 took: 4.024453ms
I0719 01:46:01.777632   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Port_Group Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:9bcc9b6b-d31a-4d64-8d2b-5fa4aae32b40}]}}] Timeout:<nil> Where:[where column _uuid == {cfdb2406-27d3-4869-bb58-7f65e5a726d7}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.777656   37437 transact.go:42] Configuring OVN: [{Op:mutate Table:Port_Group Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:9bcc9b6b-d31a-4d64-8d2b-5fa4aae32b40}]}}] Timeout:<nil> Where:[where column _uuid == {cfdb2406-27d3-4869-bb58-7f65e5a726d7}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.777896   37437 switch.go:50] Hybridoverlay port does not exist for node 00-50-56-8a-fb-ea
I0719 01:46:01.777931   37437 switch.go:59] haveMP true haveHO false ManagementPortAddress 10.130.0.2/23 HybridOverlayAddressOA 10.130.0.3/23
I0719 01:46:01.778017   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Switch Row:map[other_config:{GoMap:map[mcast_eth_src:0a:58:0a:82:00:01 mcast_ip4_src:10.130.0.1 mcast_querier:true mcast_snoop:true subnet:10.130.0.0/23]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {bc57259c-2feb-4fdd-95c3-dc98eb57f6e4}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.778063   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Switch Row:map[other_config:{GoMap:map[mcast_eth_src:0a:58:0a:82:00:01 mcast_ip4_src:10.130.0.1 mcast_querier:true mcast_snoop:true subnet:10.130.0.0/23]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {bc57259c-2feb-4fdd-95c3-dc98eb57f6e4}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.778480   37437 hybrid.go:140] Removing node 00-50-56-8a-fb-ea hybrid overlay port
I0719 01:46:01.778708   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Router Row:map[copp:{GoSet:[{GoUUID:993b87a7-28f5-463c-84ba-4cb0178f4f2a}]} external_ids:{GoMap:map[physical_ip:10.10.25.235 physical_ips:10.10.25.235]} load_balancer_group:{GoSet:[{GoUUID:2400c21d-35b5-4059-bdc0-cfe46ebce829} {GoUUID:e2fd0a53-3438-47ef-bc25-2dcb5c7ffe1c}]} options:{GoMap:map[always_learn_from_arp_request:false chassis:ec7a39e5-89ad-4e47-a317-9fefe94160bf dynamic_neigh_routers:true lb_force_snat_ip:router_ip mac_binding_age_threshold:300 snat-ct-zone:0]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {26b6d604-e9d3-4544-a4f0-f760e4ff11b6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.778741   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Router Row:map[copp:{GoSet:[{GoUUID:993b87a7-28f5-463c-84ba-4cb0178f4f2a}]} external_ids:{GoMap:map[physical_ip:10.10.25.235 physical_ips:10.10.25.235]} load_balancer_group:{GoSet:[{GoUUID:2400c21d-35b5-4059-bdc0-cfe46ebce829} {GoUUID:e2fd0a53-3438-47ef-bc25-2dcb5c7ffe1c}]} options:{GoMap:map[always_learn_from_arp_request:false chassis:ec7a39e5-89ad-4e47-a317-9fefe94160bf dynamic_neigh_routers:true lb_force_snat_ip:router_ip mac_binding_age_threshold:300 snat-ct-zone:0]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {26b6d604-e9d3-4544-a4f0-f760e4ff11b6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.779159   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[router]} options:{GoMap:map[router-port:rtoj-GR_00-50-56-8a-fb-ea]} port_security:{GoSet:[]} tag_request:{GoSet:[]} type:router] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {dce76c36-eed0-434a-aa7c-3d7f85e40bf7}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.779199   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:dce76c36-eed0-434a-aa7c-3d7f85e40bf7}]}}] Timeout:<nil> Where:[where column _uuid == {8a07c5b0-3092-44c2-aad5-3b39da1e7f5f}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.779214   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[router]} options:{GoMap:map[router-port:rtoj-GR_00-50-56-8a-fb-ea]} port_security:{GoSet:[]} tag_request:{GoSet:[]} type:router] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {dce76c36-eed0-434a-aa7c-3d7f85e40bf7}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:dce76c36-eed0-434a-aa7c-3d7f85e40bf7}]}}] Timeout:<nil> Where:[where column _uuid == {8a07c5b0-3092-44c2-aad5-3b39da1e7f5f}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.779517   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Router_Port Row:map[mac:0a:58:64:40:00:04 networks:{GoSet:[100.64.0.4/16]} options:{GoMap:map[gateway_mtu:8900]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {df57f58e-1d7e-4aab-8ed6-ec565b25da28}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.779563   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:df57f58e-1d7e-4aab-8ed6-ec565b25da28}]}}] Timeout:<nil> Where:[where column _uuid == {26b6d604-e9d3-4544-a4f0-f760e4ff11b6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.779580   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Router_Port Row:map[mac:0a:58:64:40:00:04 networks:{GoSet:[100.64.0.4/16]} options:{GoMap:map[gateway_mtu:8900]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {df57f58e-1d7e-4aab-8ed6-ec565b25da28}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:df57f58e-1d7e-4aab-8ed6-ec565b25da28}]}}] Timeout:<nil> Where:[where column _uuid == {26b6d604-e9d3-4544-a4f0-f760e4ff11b6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.779845   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Router_Static_Route Row:map[nexthop:100.64.0.1] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {c40f5d7a-bd8e-485c-aafc-078cea5d0d15}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.779880   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:insert Value:{GoSet:[{GoUUID:c40f5d7a-bd8e-485c-aafc-078cea5d0d15}]}}] Timeout:<nil> Where:[where column _uuid == {26b6d604-e9d3-4544-a4f0-f760e4ff11b6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.779900   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Router_Static_Route Row:map[nexthop:100.64.0.1] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {c40f5d7a-bd8e-485c-aafc-078cea5d0d15}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:insert Value:{GoSet:[{GoUUID:c40f5d7a-bd8e-485c-aafc-078cea5d0d15}]}}] Timeout:<nil> Where:[where column _uuid == {26b6d604-e9d3-4544-a4f0-f760e4ff11b6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.780162   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Router_Port Row:map[external_ids:{GoMap:map[gateway-physical-ip:yes]} mac:00:50:56:8a:fb:ea networks:{GoSet:[10.10.25.235/24]} options:{GoMap:map[]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {c99e05db-7949-4038-b973-cc0b8ab94d77}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.780205   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:c99e05db-7949-4038-b973-cc0b8ab94d77}]}}] Timeout:<nil> Where:[where column _uuid == {26b6d604-e9d3-4544-a4f0-f760e4ff11b6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.780221   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Router_Port Row:map[external_ids:{GoMap:map[gateway-physical-ip:yes]} mac:00:50:56:8a:fb:ea networks:{GoSet:[10.10.25.235/24]} options:{GoMap:map[]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {c99e05db-7949-4038-b973-cc0b8ab94d77}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:c99e05db-7949-4038-b973-cc0b8ab94d77}]}}] Timeout:<nil> Where:[where column _uuid == {26b6d604-e9d3-4544-a4f0-f760e4ff11b6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.780243   37437 ovs.go:162] Exec(25): stdout: ""
I0719 01:46:01.780253   37437 ovs.go:163] Exec(25): stderr: ""
I0719 01:46:01.780265   37437 ovs.go:159] Exec(26): /usr/bin/ovs-vsctl --timeout=15 list-ports br-ex
I0719 01:46:01.780525   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[unknown]} options:{GoMap:map[network_name:physnet]} port_security:{GoSet:[]} tag_request:{GoSet:[]} type:localnet] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {3caf28e2-776c-432b-b0a5-13f09f95dd0a}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.780634   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[00:50:56:8a:fb:ea]} options:{GoMap:map[exclude-lb-vips-from-garp:true nat-addresses:router router-port:rtoe-GR_00-50-56-8a-fb-ea]} port_security:{GoSet:[]} tag_request:{GoSet:[]} type:router] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {ebb1a1d9-f2ac-42a4-9590-ab0ca5c2b460}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.780669   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:3caf28e2-776c-432b-b0a5-13f09f95dd0a} {GoUUID:ebb1a1d9-f2ac-42a4-9590-ab0ca5c2b460}]}}] Timeout:<nil> Where:[where column _uuid == {5811cdea-30a4-47c9-a62a-0596f31b4388}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.780681   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[unknown]} options:{GoMap:map[network_name:physnet]} port_security:{GoSet:[]} tag_request:{GoSet:[]} type:localnet] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {3caf28e2-776c-432b-b0a5-13f09f95dd0a}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[00:50:56:8a:fb:ea]} options:{GoMap:map[exclude-lb-vips-from-garp:true nat-addresses:router router-port:rtoe-GR_00-50-56-8a-fb-ea]} port_security:{GoSet:[]} tag_request:{GoSet:[]} type:router] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {ebb1a1d9-f2ac-42a4-9590-ab0ca5c2b460}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:3caf28e2-776c-432b-b0a5-13f09f95dd0a} {GoUUID:ebb1a1d9-f2ac-42a4-9590-ab0ca5c2b460}]}}] Timeout:<nil> Where:[where column _uuid == {5811cdea-30a4-47c9-a62a-0596f31b4388}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.780980   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Static_MAC_Binding Row:map[ip:169.254.169.4 logical_port:rtoe-GR_00-50-56-8a-fb-ea mac:0a:58:a9:fe:a9:04 override_dynamic_mac:true] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {dffcf1f3-7d90-48c6-bc31-21ad220e88ae}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.781010   37437 transact.go:42] Configuring OVN: [{Op:update Table:Static_MAC_Binding Row:map[ip:169.254.169.4 logical_port:rtoe-GR_00-50-56-8a-fb-ea mac:0a:58:a9:fe:a9:04 override_dynamic_mac:true] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {dffcf1f3-7d90-48c6-bc31-21ad220e88ae}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.781214   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Router_Static_Route Row:map[nexthop:169.254.169.4] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {c2cad6f7-40d8-48cf-842f-2a44c99535bb}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.781248   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:insert Value:{GoSet:[{GoUUID:c2cad6f7-40d8-48cf-842f-2a44c99535bb}]}}] Timeout:<nil> Where:[where column _uuid == {26b6d604-e9d3-4544-a4f0-f760e4ff11b6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.781265   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Router_Static_Route Row:map[nexthop:169.254.169.4] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {c2cad6f7-40d8-48cf-842f-2a44c99535bb}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:insert Value:{GoSet:[{GoUUID:c2cad6f7-40d8-48cf-842f-2a44c99535bb}]}}] Timeout:<nil> Where:[where column _uuid == {26b6d604-e9d3-4544-a4f0-f760e4ff11b6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.781492   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Router_Static_Route Row:map[nexthop:10.10.25.1] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {8def044c-50f2-47b2-84d5-4780112c893f}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.781531   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:insert Value:{GoSet:[{GoUUID:8def044c-50f2-47b2-84d5-4780112c893f}]}}] Timeout:<nil> Where:[where column _uuid == {26b6d604-e9d3-4544-a4f0-f760e4ff11b6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.781551   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Router_Static_Route Row:map[nexthop:10.10.25.1] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {8def044c-50f2-47b2-84d5-4780112c893f}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:insert Value:{GoSet:[{GoUUID:8def044c-50f2-47b2-84d5-4780112c893f}]}}] Timeout:<nil> Where:[where column _uuid == {26b6d604-e9d3-4544-a4f0-f760e4ff11b6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.781774   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Router_Static_Route Row:map[nexthop:100.64.0.4] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {f3bf04a4-4a9c-4887-b4bc-49d41b65de84}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.781810   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:insert Value:{GoSet:[{GoUUID:f3bf04a4-4a9c-4887-b4bc-49d41b65de84}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.781826   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Router_Static_Route Row:map[nexthop:100.64.0.4] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {f3bf04a4-4a9c-4887-b4bc-49d41b65de84}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:insert Value:{GoSet:[{GoUUID:f3bf04a4-4a9c-4887-b4bc-49d41b65de84}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.782079   37437 model_client.go:372] Create operations generated as: [{Op:insert Table:Logical_Router_Static_Route Row:map[ip_prefix:10.130.0.0/23 nexthop:100.64.0.4 policy:{GoSet:[src-ip]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:u4265923265}]
I0719 01:46:01.782116   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:insert Value:{GoSet:[{GoUUID:u4265923265}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.782132   37437 transact.go:42] Configuring OVN: [{Op:insert Table:Logical_Router_Static_Route Row:map[ip_prefix:10.130.0.0/23 nexthop:100.64.0.4 policy:{GoSet:[src-ip]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:u4265923265} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:insert Value:{GoSet:[{GoUUID:u4265923265}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.782595   37437 model_client.go:381] Update operations generated as: [{Op:update Table:NAT Row:map[external_ip:10.10.25.235 logical_ip:100.64.0.4 options:{GoMap:map[stateless:false]} type:snat] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {051833d2-bdaf-4396-8a4b-2843beb3803e}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.782634   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:nat Mutator:insert Value:{GoSet:[{GoUUID:051833d2-bdaf-4396-8a4b-2843beb3803e}]}}] Timeout:<nil> Where:[where column _uuid == {26b6d604-e9d3-4544-a4f0-f760e4ff11b6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.782647   37437 transact.go:42] Configuring OVN: [{Op:update Table:NAT Row:map[external_ip:10.10.25.235 logical_ip:100.64.0.4 options:{GoMap:map[stateless:false]} type:snat] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {051833d2-bdaf-4396-8a4b-2843beb3803e}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:nat Mutator:insert Value:{GoSet:[{GoUUID:051833d2-bdaf-4396-8a4b-2843beb3803e}]}}] Timeout:<nil> Where:[where column _uuid == {26b6d604-e9d3-4544-a4f0-f760e4ff11b6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.787113   37437 ovs.go:162] Exec(26): stdout: "ens192\npatch-br-ex_00-50-56-8a-fb-ea-to-br-int\n"
I0719 01:46:01.787129   37437 ovs.go:163] Exec(26): stderr: ""
I0719 01:46:01.787142   37437 ovs.go:159] Exec(27): /usr/bin/ovs-vsctl --timeout=15 get Port ens192 Interfaces
I0719 01:46:01.793327   37437 ovs.go:162] Exec(27): stdout: "[16af03e8-0b22-4405-97ef-670f17d9e493]\n"
I0719 01:46:01.793345   37437 ovs.go:163] Exec(27): stderr: ""
I0719 01:46:01.793358   37437 ovs.go:159] Exec(28): /usr/bin/ovs-vsctl --timeout=15 get Port patch-br-ex_00-50-56-8a-fb-ea-to-br-int Interfaces
I0719 01:46:01.795382   37437 base_network_controller.go:458] When adding node 00-50-56-8a-fb-ea for network default, found 19 pods to add to retryPods
I0719 01:46:01.795401   37437 base_network_controller.go:464] Adding pod openshift-cluster-node-tuning-operator/tuned-9mzgb to retryPods for network default
I0719 01:46:01.795413   37437 base_network_controller.go:464] Adding pod openshift-dns/dns-default-qzrlq to retryPods for network default
I0719 01:46:01.795419   37437 base_network_controller.go:464] Adding pod openshift-dns/node-resolver-nsvs6 to retryPods for network default
I0719 01:46:01.795425   37437 base_network_controller.go:464] Adding pod openshift-image-registry/node-ca-lfxb8 to retryPods for network default
I0719 01:46:01.795432   37437 base_network_controller.go:464] Adding pod openshift-ingress-canary/ingress-canary-lsx7x to retryPods for network default
I0719 01:46:01.795437   37437 base_network_controller.go:464] Adding pod openshift-kni-infra/coredns-00-50-56-8a-fb-ea to retryPods for network default
I0719 01:46:01.795443   37437 base_network_controller.go:464] Adding pod openshift-kni-infra/keepalived-00-50-56-8a-fb-ea to retryPods for network default
I0719 01:46:01.795458   37437 base_network_controller.go:464] Adding pod openshift-local-storage/diskmaker-manager-2zrc6 to retryPods for network default
I0719 01:46:01.795466   37437 base_network_controller.go:464] Adding pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-fb-ea to retryPods for network default
I0719 01:46:01.795479   37437 base_network_controller.go:464] Adding pod openshift-machine-config-operator/machine-config-daemon-vllgq to retryPods for network default
I0719 01:46:01.795484   37437 base_network_controller.go:464] Adding pod openshift-monitoring/node-exporter-9mlmj to retryPods for network default
I0719 01:46:01.795490   37437 base_network_controller.go:464] Adding pod openshift-multus/multus-additional-cni-plugins-b5t42 to retryPods for network default
I0719 01:46:01.795495   37437 base_network_controller.go:464] Adding pod openshift-multus/multus-sv782 to retryPods for network default
I0719 01:46:01.795502   37437 base_network_controller.go:464] Adding pod openshift-multus/network-metrics-daemon-7ttpg to retryPods for network default
I0719 01:46:01.795506   37437 base_network_controller.go:464] Adding pod openshift-network-diagnostics/network-check-target-dj4vt to retryPods for network default
I0719 01:46:01.795513   37437 base_network_controller.go:464] Adding pod openshift-network-operator/iptables-alerter-nh7z8 to retryPods for network default
I0719 01:46:01.795518   37437 base_network_controller.go:464] Adding pod openshift-ovn-kubernetes/ovnkube-node-9h9qr to retryPods for network default
I0719 01:46:01.795533   37437 base_network_controller.go:464] Adding pod openshift-storage/csi-cephfsplugin-5fvh4 to retryPods for network default
I0719 01:46:01.795540   37437 base_network_controller.go:464] Adding pod openshift-storage/csi-rbdplugin-xkw8r to retryPods for network default
I0719 01:46:01.795546   37437 obj_retry.go:233] Iterate retry objects requested (resource *v1.Pod)
I0719 01:46:01.795618   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Encap Row:map[chassis_name:ec7a39e5-89ad-4e47-a317-9fefe94160bf ip:10.10.25.235 options:{GoMap:map[csum:true]} type:geneve] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {01241142-dc7b-4585-b250-4d074990b548}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.795691   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Chassis Row:map[encaps:{GoSet:[{GoUUID:01241142-dc7b-4585-b250-4d074990b548}]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {e6841250-5ca4-4a65-8660-f04c844f451e}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.795724   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Chassis Row:map[] Rows:[] Columns:[] Mutations:[{Column:other_config Mutator:delete Value:{GoSet:[is-remote]}} {Column:other_config Mutator:insert Value:{GoMap:map[is-remote:false]}}] Timeout:<nil> Where:[where column _uuid == {e6841250-5ca4-4a65-8660-f04c844f451e}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.795744   37437 transact.go:42] Configuring OVN: [{Op:update Table:Encap Row:map[chassis_name:ec7a39e5-89ad-4e47-a317-9fefe94160bf ip:10.10.25.235 options:{GoMap:map[csum:true]} type:geneve] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {01241142-dc7b-4585-b250-4d074990b548}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:update Table:Chassis Row:map[encaps:{GoSet:[{GoUUID:01241142-dc7b-4585-b250-4d074990b548}]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {e6841250-5ca4-4a65-8660-f04c844f451e}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Chassis Row:map[] Rows:[] Columns:[] Mutations:[{Column:other_config Mutator:delete Value:{GoSet:[is-remote]}} {Column:other_config Mutator:insert Value:{GoMap:map[is-remote:false]}}] Timeout:<nil> Where:[where column _uuid == {e6841250-5ca4-4a65-8660-f04c844f451e}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.796171   37437 zone_ic_handler.go:220] Creating interconnect resources for local zone node 00-50-56-8a-fb-ea for the network default
I0719 01:46:01.796240   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Router_Port Row:map[mac:0a:58:64:58:00:04 name:rtots-00-50-56-8a-fb-ea networks:{GoSet:[100.88.0.4/16]} options:{GoMap:map[mcast_flood:true]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {21b207e1-ed5b-4759-ac82-0c66b102fd0e}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.796296   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:21b207e1-ed5b-4759-ac82-0c66b102fd0e}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.796317   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Router_Port Row:map[mac:0a:58:64:58:00:04 name:rtots-00-50-56-8a-fb-ea networks:{GoSet:[100.88.0.4/16]} options:{GoMap:map[mcast_flood:true]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {21b207e1-ed5b-4759-ac82-0c66b102fd0e}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:21b207e1-ed5b-4759-ac82-0c66b102fd0e}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.796781   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[router]} options:{GoMap:map[requested-tnl-key:4 router-port:rtots-00-50-56-8a-fb-ea]} port_security:{GoSet:[]} tag_request:{GoSet:[]} type:router] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {bacbb205-77f3-41ac-867b-3ad5f82d8e23}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.796825   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:bacbb205-77f3-41ac-867b-3ad5f82d8e23}]}}] Timeout:<nil> Where:[where column _uuid == {86ba2710-ebc4-4689-adf6-f6f48ae98fa3}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.796846   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[router]} options:{GoMap:map[requested-tnl-key:4 router-port:rtots-00-50-56-8a-fb-ea]} port_security:{GoSet:[]} tag_request:{GoSet:[]} type:router] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {bacbb205-77f3-41ac-867b-3ad5f82d8e23}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:bacbb205-77f3-41ac-867b-3ad5f82d8e23}]}}] Timeout:<nil> Where:[where column _uuid == {86ba2710-ebc4-4689-adf6-f6f48ae98fa3}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.797196   37437 obj_retry.go:541] Creating *v1.Node 00-50-56-8a-fb-ea took: 24.226177ms
I0719 01:46:01.797228   37437 factory.go:988] Added *v1.Node event handler 2
I0719 01:46:01.797244   37437 ovn.go:449] Starting OVN Service Controller: Using Endpoint Slices
I0719 01:46:01.797350   37437 services_controller.go:168] Starting controller ovn-lb-controller
I0719 01:46:01.797412   37437 services_controller.go:176] Waiting for node tracker handler to sync
I0719 01:46:01.797471   37437 shared_informer.go:311] Waiting for caches to sync for node-tracker-controller
I0719 01:46:01.797453   37437 node_tracker.go:204] Processing possible switch / router updates for node 00-50-56-8a-e1-e7
I0719 01:46:01.797592   37437 node_tracker.go:165] Node 00-50-56-8a-e1-e7 switch + router changed, syncing services
I0719 01:46:01.797619   37437 services_controller.go:519] Full service sync requested
I0719 01:46:01.797643   37437 node_tracker.go:204] Processing possible switch / router updates for node 00-50-56-8a-f2-5d
I0719 01:46:01.797696   37437 node_tracker.go:165] Node 00-50-56-8a-f2-5d switch + router changed, syncing services
I0719 01:46:01.797731   37437 services_controller.go:519] Full service sync requested
I0719 01:46:01.797754   37437 node_tracker.go:204] Processing possible switch / router updates for node 00-50-56-8a-fb-ea
I0719 01:46:01.797772   37437 default_network_controller.go:655] Recording add event on pod openshift-dns/dns-default-rj9px
I0719 01:46:01.797792   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-dns/dns-default-rj9px
I0719 01:46:01.797805   37437 ovn.go:138] Ensuring zone remote for Pod openshift-dns/dns-default-rj9px in node 00-50-56-8a-f2-5d
I0719 01:46:01.797840   37437 default_network_controller.go:655] Recording add event on pod openshift-cluster-node-tuning-operator/tuned-9mzgb
I0719 01:46:01.797892   37437 default_network_controller.go:655] Recording add event on pod openshift-cluster-node-tuning-operator/tuned-x2svx
I0719 01:46:01.797905   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-cluster-node-tuning-operator/tuned-x2svx
I0719 01:46:01.797912   37437 ovn.go:138] Ensuring zone remote for Pod openshift-cluster-node-tuning-operator/tuned-x2svx in node 00-50-56-8a-44-52
I0719 01:46:01.797917   37437 obj_retry.go:541] Creating *v1.Pod openshift-cluster-node-tuning-operator/tuned-x2svx took: 6.72µs
I0719 01:46:01.797915   37437 default_network_controller.go:655] Recording add event on pod openshift-machine-config-operator/machine-config-server-zwkfw
I0719 01:46:01.797931   37437 default_network_controller.go:655] Recording add event on pod openshift-machine-config-operator/machine-config-daemon-vllgq
I0719 01:46:01.797935   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-machine-config-operator/machine-config-server-zwkfw
I0719 01:46:01.797940   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-machine-config-operator/machine-config-daemon-vllgq
I0719 01:46:01.797948   37437 ovn.go:134] Ensuring zone local for Pod openshift-machine-config-operator/machine-config-daemon-vllgq in node 00-50-56-8a-fb-ea
I0719 01:46:01.797953   37437 obj_retry.go:541] Creating *v1.Pod openshift-machine-config-operator/machine-config-daemon-vllgq took: 6.709µs
I0719 01:46:01.797957   37437 default_network_controller.go:699] Recording success event on pod openshift-machine-config-operator/machine-config-daemon-vllgq
I0719 01:46:01.797954   37437 default_network_controller.go:655] Recording add event on pod openshift-monitoring/alertmanager-main-1
I0719 01:46:01.797962   37437 default_network_controller.go:655] Recording add event on pod openshift-marketplace/certified-operators-j5jtq
I0719 01:46:01.797922   37437 default_network_controller.go:699] Recording success event on pod openshift-cluster-node-tuning-operator/tuned-x2svx
I0719 01:46:01.797972   37437 default_network_controller.go:655] Recording add event on pod openshift-cluster-node-tuning-operator/tuned-hpvxx
I0719 01:46:01.797975   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/csi-cephfsplugin-b549v
I0719 01:46:01.797748   37437 default_network_controller.go:655] Recording add event on pod openshift-kni-infra/coredns-00-50-56-8a-e1-e7
I0719 01:46:01.797992   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-marketplace/certified-operators-j5jtq
I0719 01:46:01.797863   37437 obj_retry.go:541] Creating *v1.Pod openshift-dns/dns-default-rj9px took: 60.09µs
I0719 01:46:01.798003   37437 default_network_controller.go:699] Recording success event on pod openshift-dns/dns-default-rj9px
I0719 01:46:01.798004   37437 ovn.go:138] Ensuring zone remote for Pod openshift-marketplace/certified-operators-j5jtq in node 00-50-56-8a-39-a0
I0719 01:46:01.798010   37437 default_network_controller.go:655] Recording add event on pod openshift-machine-api/machine-api-controllers-59cdf7bd97-7l7pt
I0719 01:46:01.798009   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/csi-cephfsplugin-b549v
I0719 01:46:01.798017   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-machine-api/machine-api-controllers-59cdf7bd97-7l7pt
I0719 01:46:01.798025   37437 ovn.go:138] Ensuring zone remote for Pod openshift-machine-api/machine-api-controllers-59cdf7bd97-7l7pt in node 00-50-56-8a-39-a0
I0719 01:46:01.798019   37437 default_network_controller.go:655] Recording add event on pod openshift-network-node-identity/network-node-identity-xlk9z
I0719 01:46:01.798040   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-network-node-identity/network-node-identity-xlk9z
I0719 01:46:01.798049   37437 obj_retry.go:541] Creating *v1.Pod openshift-marketplace/certified-operators-j5jtq took: 47.17µs
I0719 01:46:01.798054   37437 ovn.go:138] Ensuring zone remote for Pod openshift-network-node-identity/network-node-identity-xlk9z in node 00-50-56-8a-39-a0
I0719 01:46:01.797962   37437 ovn.go:138] Ensuring zone remote for Pod openshift-machine-config-operator/machine-config-server-zwkfw in node 00-50-56-8a-5c-ec
I0719 01:46:01.798060   37437 obj_retry.go:541] Creating *v1.Pod openshift-network-node-identity/network-node-identity-xlk9z took: 9.029µs
I0719 01:46:01.797976   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-monitoring/alertmanager-main-1
I0719 01:46:01.798066   37437 default_network_controller.go:699] Recording success event on pod openshift-network-node-identity/network-node-identity-xlk9z
I0719 01:46:01.798071   37437 ovn.go:138] Ensuring zone remote for Pod openshift-monitoring/alertmanager-main-1 in node 00-50-56-8a-e1-e7
I0719 01:46:01.798062   37437 obj_retry.go:541] Creating *v1.Pod openshift-machine-config-operator/machine-config-server-zwkfw took: 117.747µs
I0719 01:46:01.798078   37437 default_network_controller.go:699] Recording success event on pod openshift-machine-config-operator/machine-config-server-zwkfw
I0719 01:46:01.798022   37437 default_network_controller.go:655] Recording add event on pod openshift-ovn-kubernetes/ovnkube-control-plane-58975cd9fd-7wmvb
I0719 01:46:01.798084   37437 default_network_controller.go:655] Recording add event on pod openshift-authentication/oauth-openshift-7c9d9dfc8c-lxcsb
I0719 01:46:01.798090   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-ovn-kubernetes/ovnkube-control-plane-58975cd9fd-7wmvb
I0719 01:46:01.798094   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-authentication/oauth-openshift-7c9d9dfc8c-lxcsb
I0719 01:46:01.798098   37437 ovn.go:138] Ensuring zone remote for Pod openshift-ovn-kubernetes/ovnkube-control-plane-58975cd9fd-7wmvb in node 00-50-56-8a-5c-ec
I0719 01:46:01.798072   37437 default_network_controller.go:655] Recording add event on pod openshift-operator-lifecycle-manager/catalog-operator-7d75668bc4-sjfjn
I0719 01:46:01.797993   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kni-infra/coredns-00-50-56-8a-e1-e7
I0719 01:46:01.798098   37437 obj_retry.go:541] Creating *v1.Pod openshift-monitoring/alertmanager-main-1 took: 28.091µs
I0719 01:46:01.798109   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kni-infra/coredns-00-50-56-8a-e1-e7 in node 00-50-56-8a-e1-e7
I0719 01:46:01.798114   37437 obj_retry.go:541] Creating *v1.Pod openshift-kni-infra/coredns-00-50-56-8a-e1-e7 took: 6.652µs
I0719 01:46:01.798113   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-operator-lifecycle-manager/catalog-operator-7d75668bc4-sjfjn
I0719 01:46:01.798025   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/csi-cephfsplugin-b549v in node 00-50-56-8a-f2-5d
I0719 01:46:01.798124   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/csi-cephfsplugin-b549v took: 102.917µs
I0719 01:46:01.798125   37437 ovn.go:138] Ensuring zone remote for Pod openshift-operator-lifecycle-manager/catalog-operator-7d75668bc4-sjfjn in node 00-50-56-8a-5c-ec
I0719 01:46:01.798129   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/csi-cephfsplugin-b549v
I0719 01:46:01.798134   37437 default_network_controller.go:655] Recording add event on pod openshift-local-storage/local-storage-operator-6486fccd57-h47kh
I0719 01:46:01.798139   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-local-storage/local-storage-operator-6486fccd57-h47kh
I0719 01:46:01.798146   37437 ovn.go:138] Ensuring zone remote for Pod openshift-local-storage/local-storage-operator-6486fccd57-h47kh in node 00-50-56-8a-f2-5d
I0719 01:46:01.798118   37437 default_network_controller.go:699] Recording success event on pod openshift-kni-infra/coredns-00-50-56-8a-e1-e7
I0719 01:46:01.798169   37437 obj_retry.go:541] Creating *v1.Pod openshift-operator-lifecycle-manager/catalog-operator-7d75668bc4-sjfjn took: 45.015µs
I0719 01:46:01.797761   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/noobaa-endpoint-6ddf6bb6b-jmx4r
I0719 01:46:01.798176   37437 default_network_controller.go:699] Recording success event on pod openshift-operator-lifecycle-manager/catalog-operator-7d75668bc4-sjfjn
I0719 01:46:01.797757   37437 default_network_controller.go:655] Recording add event on pod openshift-multus/multus-admission-controller-5cc499c6f4-jtjqw
I0719 01:46:01.798181   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/noobaa-endpoint-6ddf6bb6b-jmx4r
I0719 01:46:01.798183   37437 default_network_controller.go:655] Recording add event on pod openshift-ingress/router-default-54fb8ffc6b-kgb2v
I0719 01:46:01.798189   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/noobaa-endpoint-6ddf6bb6b-jmx4r in node 00-50-56-8a-e1-e7
I0719 01:46:01.798191   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-ingress/router-default-54fb8ffc6b-kgb2v
I0719 01:46:01.798198   37437 ovn.go:138] Ensuring zone remote for Pod openshift-ingress/router-default-54fb8ffc6b-kgb2v in node 00-50-56-8a-e1-e7
I0719 01:46:01.798199   37437 obj_retry.go:541] Creating *v1.Pod openshift-local-storage/local-storage-operator-6486fccd57-h47kh took: 53.565µs
I0719 01:46:01.798203   37437 obj_retry.go:541] Creating *v1.Pod openshift-ingress/router-default-54fb8ffc6b-kgb2v took: 5.929µs
I0719 01:46:01.798053   37437 obj_retry.go:541] Creating *v1.Pod openshift-machine-api/machine-api-controllers-59cdf7bd97-7l7pt took: 29.316µs
I0719 01:46:01.798208   37437 default_network_controller.go:699] Recording success event on pod openshift-ingress/router-default-54fb8ffc6b-kgb2v
I0719 01:46:01.798109   37437 default_network_controller.go:699] Recording success event on pod openshift-monitoring/alertmanager-main-1
I0719 01:46:01.798220   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/noobaa-endpoint-6ddf6bb6b-jmx4r took: 32.384µs
I0719 01:46:01.798226   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/noobaa-endpoint-6ddf6bb6b-jmx4r
I0719 01:46:01.798189   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-multus/multus-admission-controller-5cc499c6f4-jtjqw
I0719 01:46:01.798203   37437 default_network_controller.go:699] Recording success event on pod openshift-local-storage/local-storage-operator-6486fccd57-h47kh
I0719 01:46:01.798246   37437 ovn.go:138] Ensuring zone remote for Pod openshift-multus/multus-admission-controller-5cc499c6f4-jtjqw in node 00-50-56-8a-39-a0
I0719 01:46:01.798224   37437 default_network_controller.go:655] Recording add event on pod openshift-route-controller-manager/route-controller-manager-676cdfdbc8-t6rhq
I0719 01:46:01.798256   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-route-controller-manager/route-controller-manager-676cdfdbc8-t6rhq
I0719 01:46:01.797740   37437 default_network_controller.go:655] Recording add event on pod openshift-kube-apiserver/kube-apiserver-00-50-56-8a-44-52
I0719 01:46:01.798263   37437 ovn.go:138] Ensuring zone remote for Pod openshift-route-controller-manager/route-controller-manager-676cdfdbc8-t6rhq in node 00-50-56-8a-5c-ec
I0719 01:46:01.798268   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kube-apiserver/kube-apiserver-00-50-56-8a-44-52
I0719 01:46:01.798246   37437 default_network_controller.go:655] Recording add event on pod openshift-machine-api/cluster-autoscaler-operator-56cd7bcc4-8t6ns
I0719 01:46:01.798276   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kube-apiserver/kube-apiserver-00-50-56-8a-44-52 in node 00-50-56-8a-44-52
I0719 01:46:01.798277   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-machine-api/cluster-autoscaler-operator-56cd7bcc4-8t6ns
I0719 01:46:01.798055   37437 default_network_controller.go:699] Recording success event on pod openshift-marketplace/certified-operators-j5jtq
I0719 01:46:01.797977   37437 default_network_controller.go:655] Recording add event on pod openshift-kni-infra/haproxy-00-50-56-8a-44-52
I0719 01:46:01.798291   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kni-infra/haproxy-00-50-56-8a-44-52
I0719 01:46:01.798103   37437 obj_retry.go:541] Creating *v1.Pod openshift-ovn-kubernetes/ovnkube-control-plane-58975cd9fd-7wmvb took: 6.539µs
I0719 01:46:01.798299   37437 obj_retry.go:541] Creating *v1.Pod openshift-multus/multus-admission-controller-5cc499c6f4-jtjqw took: 56.521µs
I0719 01:46:01.798308   37437 default_network_controller.go:699] Recording success event on pod openshift-multus/multus-admission-controller-5cc499c6f4-jtjqw
I0719 01:46:01.798315   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/rook-ceph-osd-2-9c5dbbd88-crlql
I0719 01:46:01.798321   37437 obj_retry.go:541] Creating *v1.Pod openshift-route-controller-manager/route-controller-manager-676cdfdbc8-t6rhq took: 58.374µs
I0719 01:46:01.798292   37437 default_network_controller.go:655] Recording add event on pod openshift-cluster-storage-operator/cluster-storage-operator-6c5864c5b-kgzzc
I0719 01:46:01.798322   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/rook-ceph-osd-2-9c5dbbd88-crlql
I0719 01:46:01.798332   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-cluster-storage-operator/cluster-storage-operator-6c5864c5b-kgzzc
I0719 01:46:01.798334   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/rook-ceph-osd-2-9c5dbbd88-crlql took: 183ns
I0719 01:46:01.798338   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/rook-ceph-osd-2-9c5dbbd88-crlql
I0719 01:46:01.798341   37437 ovn.go:138] Ensuring zone remote for Pod openshift-cluster-storage-operator/cluster-storage-operator-6c5864c5b-kgzzc in node 00-50-56-8a-5c-ec
I0719 01:46:01.798343   37437 default_network_controller.go:655] Recording add event on pod openshift-monitoring/openshift-state-metrics-6bb8db76bd-2wlhc
I0719 01:46:01.798348   37437 node_tracker.go:165] Node 00-50-56-8a-fb-ea switch + router changed, syncing services
I0719 01:46:01.798358   37437 services_controller.go:519] Full service sync requested
I0719 01:46:01.798365   37437 node_tracker.go:204] Processing possible switch / router updates for node 00-50-56-8a-39-a0
I0719 01:46:01.798301   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kni-infra/haproxy-00-50-56-8a-44-52 in node 00-50-56-8a-44-52
I0719 01:46:01.798375   37437 obj_retry.go:541] Creating *v1.Pod openshift-kni-infra/haproxy-00-50-56-8a-44-52 took: 73.473µs
I0719 01:46:01.798381   37437 default_network_controller.go:699] Recording success event on pod openshift-kni-infra/haproxy-00-50-56-8a-44-52
I0719 01:46:01.798359   37437 obj_retry.go:541] Creating *v1.Pod openshift-cluster-storage-operator/cluster-storage-operator-6c5864c5b-kgzzc took: 18.975µs
I0719 01:46:01.798387   37437 default_network_controller.go:655] Recording add event on pod openshift-kni-infra/coredns-00-50-56-8a-44-52
I0719 01:46:01.798388   37437 node_tracker.go:165] Node 00-50-56-8a-39-a0 switch + router changed, syncing services
I0719 01:46:01.798390   37437 default_network_controller.go:699] Recording success event on pod openshift-cluster-storage-operator/cluster-storage-operator-6c5864c5b-kgzzc
I0719 01:46:01.798393   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kni-infra/coredns-00-50-56-8a-44-52
I0719 01:46:01.798349   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-monitoring/openshift-state-metrics-6bb8db76bd-2wlhc
I0719 01:46:01.798400   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kni-infra/coredns-00-50-56-8a-44-52 in node 00-50-56-8a-44-52
I0719 01:46:01.798394   37437 services_controller.go:519] Full service sync requested
I0719 01:46:01.798233   37437 default_network_controller.go:655] Recording add event on pod openshift-image-registry/node-ca-kqt8n
I0719 01:46:01.797977   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-cluster-node-tuning-operator/tuned-hpvxx
I0719 01:46:01.798410   37437 node_tracker.go:204] Processing possible switch / router updates for node 00-50-56-8a-44-52
I0719 01:46:01.798412   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-image-registry/node-ca-kqt8n
I0719 01:46:01.798285   37437 ovn.go:138] Ensuring zone remote for Pod openshift-machine-api/cluster-autoscaler-operator-56cd7bcc4-8t6ns in node 00-50-56-8a-39-a0
I0719 01:46:01.798420   37437 ovn.go:138] Ensuring zone remote for Pod openshift-image-registry/node-ca-kqt8n in node 00-50-56-8a-44-52
I0719 01:46:01.798425   37437 obj_retry.go:541] Creating *v1.Pod openshift-image-registry/node-ca-kqt8n took: 6.123µs
I0719 01:46:01.798429   37437 default_network_controller.go:699] Recording success event on pod openshift-image-registry/node-ca-kqt8n
I0719 01:46:01.798435   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/noobaa-core-0
I0719 01:46:01.798438   37437 obj_retry.go:541] Creating *v1.Pod openshift-machine-api/cluster-autoscaler-operator-56cd7bcc4-8t6ns took: 154.525µs
I0719 01:46:01.798440   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/noobaa-core-0
I0719 01:46:01.798443   37437 default_network_controller.go:699] Recording success event on pod openshift-machine-api/cluster-autoscaler-operator-56cd7bcc4-8t6ns
I0719 01:46:01.798444   37437 node_tracker.go:165] Node 00-50-56-8a-44-52 switch + router changed, syncing services
I0719 01:46:01.798448   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/noobaa-core-0 in node 00-50-56-8a-f2-5d
I0719 01:46:01.798451   37437 services_controller.go:519] Full service sync requested
I0719 01:46:01.798283   37437 obj_retry.go:541] Creating *v1.Pod openshift-kube-apiserver/kube-apiserver-00-50-56-8a-44-52 took: 7.397µs
I0719 01:46:01.798457   37437 node_tracker.go:204] Processing possible switch / router updates for node 00-50-56-8a-5c-ec
I0719 01:46:01.798459   37437 default_network_controller.go:699] Recording success event on pod openshift-kube-apiserver/kube-apiserver-00-50-56-8a-44-52
I0719 01:46:01.798465   37437 default_network_controller.go:655] Recording add event on pod openshift-cluster-node-tuning-operator/cluster-node-tuning-operator-68cc9c9cf9-6brm7
I0719 01:46:01.798469   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/noobaa-core-0 took: 23.796µs
I0719 01:46:01.798302   37437 default_network_controller.go:699] Recording success event on pod openshift-ovn-kubernetes/ovnkube-control-plane-58975cd9fd-7wmvb
I0719 01:46:01.798475   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/noobaa-core-0
I0719 01:46:01.798448   37437 default_network_controller.go:655] Recording add event on pod openshift-etcd/revision-pruner-9-00-50-56-8a-5c-ec
I0719 01:46:01.798480   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/odf-operator-controller-manager-78d57f457c-tbwjf
I0719 01:46:01.798485   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-etcd/revision-pruner-9-00-50-56-8a-5c-ec
I0719 01:46:01.798471   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-cluster-node-tuning-operator/cluster-node-tuning-operator-68cc9c9cf9-6brm7
I0719 01:46:01.798494   37437 ovn.go:138] Ensuring zone remote for Pod openshift-cluster-node-tuning-operator/cluster-node-tuning-operator-68cc9c9cf9-6brm7 in node 00-50-56-8a-5c-ec
I0719 01:46:01.798517   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-cluster-node-tuning-operator/tuned-9mzgb
I0719 01:46:01.798550   37437 ovn.go:134] Ensuring zone local for Pod openshift-cluster-node-tuning-operator/tuned-9mzgb in node 00-50-56-8a-fb-ea
I0719 01:46:01.798576   37437 obj_retry.go:541] Creating *v1.Pod openshift-cluster-node-tuning-operator/tuned-9mzgb took: 28.733µs
I0719 01:46:01.798599   37437 default_network_controller.go:699] Recording success event on pod openshift-cluster-node-tuning-operator/tuned-9mzgb
I0719 01:46:01.798634   37437 default_network_controller.go:655] Recording add event on pod openshift-network-diagnostics/network-check-target-8gshd
I0719 01:46:01.798662   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-network-diagnostics/network-check-target-8gshd
I0719 01:46:01.798686   37437 ovn.go:138] Ensuring zone remote for Pod openshift-network-diagnostics/network-check-target-8gshd in node 00-50-56-8a-5c-ec
I0719 01:46:01.798740   37437 obj_retry.go:541] Creating *v1.Pod openshift-network-diagnostics/network-check-target-8gshd took: 55.732µs
I0719 01:46:01.798765   37437 default_network_controller.go:699] Recording success event on pod openshift-network-diagnostics/network-check-target-8gshd
I0719 01:46:01.798794   37437 default_network_controller.go:655] Recording add event on pod openshift-dns/dns-default-zwbjg
I0719 01:46:01.798826   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-dns/dns-default-zwbjg
I0719 01:46:01.798856   37437 ovn.go:138] Ensuring zone remote for Pod openshift-dns/dns-default-zwbjg in node 00-50-56-8a-39-a0
I0719 01:46:01.798892   37437 obj_retry.go:541] Creating *v1.Pod openshift-dns/dns-default-zwbjg took: 36.635µs
I0719 01:46:01.798914   37437 default_network_controller.go:699] Recording success event on pod openshift-dns/dns-default-zwbjg
I0719 01:46:01.798944   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/rook-ceph-operator-cf758864f-c6zl8
I0719 01:46:01.798975   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/rook-ceph-operator-cf758864f-c6zl8
I0719 01:46:01.799024   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/rook-ceph-operator-cf758864f-c6zl8 in node 00-50-56-8a-f2-5d
I0719 01:46:01.799066   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/rook-ceph-operator-cf758864f-c6zl8 took: 43.775µs
I0719 01:46:01.799089   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/rook-ceph-operator-cf758864f-c6zl8
I0719 01:46:01.799116   37437 default_network_controller.go:655] Recording add event on pod openshift-apiserver/apiserver-7d9bbd465d-6cgbw
I0719 01:46:01.799140   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-apiserver/apiserver-7d9bbd465d-6cgbw
I0719 01:46:01.799163   37437 ovn.go:138] Ensuring zone remote for Pod openshift-apiserver/apiserver-7d9bbd465d-6cgbw in node 00-50-56-8a-5c-ec
I0719 01:46:01.799207   37437 obj_retry.go:541] Creating *v1.Pod openshift-apiserver/apiserver-7d9bbd465d-6cgbw took: 42.976µs
I0719 01:46:01.799240   37437 default_network_controller.go:699] Recording success event on pod openshift-apiserver/apiserver-7d9bbd465d-6cgbw
I0719 01:46:01.799274   37437 default_network_controller.go:655] Recording add event on pod openshift-ovn-kubernetes/ovnkube-node-5bqnj
I0719 01:46:01.799306   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-ovn-kubernetes/ovnkube-node-5bqnj
I0719 01:46:01.799340   37437 ovn.go:138] Ensuring zone remote for Pod openshift-ovn-kubernetes/ovnkube-node-5bqnj in node 00-50-56-8a-39-a0
I0719 01:46:01.799381   37437 obj_retry.go:541] Creating *v1.Pod openshift-ovn-kubernetes/ovnkube-node-5bqnj took: 42.807µs
I0719 01:46:01.799411   37437 default_network_controller.go:699] Recording success event on pod openshift-ovn-kubernetes/ovnkube-node-5bqnj
I0719 01:46:01.799441   37437 default_network_controller.go:655] Recording add event on pod openshift-monitoring/monitoring-plugin-6f457fd4b8-pqp4m
I0719 01:46:01.798486   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/odf-operator-controller-manager-78d57f457c-tbwjf
I0719 01:46:01.799500   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/odf-operator-controller-manager-78d57f457c-tbwjf in node 00-50-56-8a-f2-5d
I0719 01:46:01.799526   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/odf-operator-controller-manager-78d57f457c-tbwjf took: 29.781µs
I0719 01:46:01.799534   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/odf-operator-controller-manager-78d57f457c-tbwjf
I0719 01:46:01.799541   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/rook-ceph-mgr-a-6fddb5fd95-mr2cn
I0719 01:46:01.799549   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/rook-ceph-mgr-a-6fddb5fd95-mr2cn
I0719 01:46:01.799564   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/rook-ceph-mgr-a-6fddb5fd95-mr2cn in node 00-50-56-8a-f2-5d
I0719 01:46:01.798492   37437 obj_retry.go:459] Detected object openshift-etcd/revision-pruner-9-00-50-56-8a-5c-ec of type *v1.Pod in terminal state (e.g. completed) during add event: will remove it
I0719 01:46:01.798211   37437 default_network_controller.go:699] Recording success event on pod openshift-machine-api/machine-api-controllers-59cdf7bd97-7l7pt
I0719 01:46:01.798397   37437 default_network_controller.go:655] Recording add event on pod openshift-network-diagnostics/network-check-target-dj4vt
I0719 01:46:01.798213   37437 default_network_controller.go:655] Recording add event on pod openshift-monitoring/thanos-querier-68bf686489-qbcjs
I0719 01:46:01.798404   37437 ovn.go:138] Ensuring zone remote for Pod openshift-monitoring/openshift-state-metrics-6bb8db76bd-2wlhc in node 00-50-56-8a-e1-e7
I0719 01:46:01.798405   37437 obj_retry.go:541] Creating *v1.Pod openshift-kni-infra/coredns-00-50-56-8a-44-52 took: 5.929µs
I0719 01:46:01.798414   37437 ovn.go:138] Ensuring zone remote for Pod openshift-cluster-node-tuning-operator/tuned-hpvxx in node 00-50-56-8a-5c-ec
I0719 01:46:01.798101   37437 ovn.go:138] Ensuring zone remote for Pod openshift-authentication/oauth-openshift-7c9d9dfc8c-lxcsb in node 00-50-56-8a-5c-ec
I0719 01:46:01.798478   37437 node_tracker.go:165] Node 00-50-56-8a-5c-ec switch + router changed, syncing services
I0719 01:46:01.798479   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/ux-backend-server-6444f844bf-whf8g
I0719 01:46:01.797886   37437 default_network_controller.go:655] Recording add event on pod openshift-kni-infra/keepalived-00-50-56-8a-fb-ea
I0719 01:46:01.798173   37437 default_network_controller.go:655] Recording add event on pod openshift-monitoring/monitoring-plugin-6f457fd4b8-6wb4z
I0719 01:46:01.798523   37437 obj_retry.go:541] Creating *v1.Pod openshift-cluster-node-tuning-operator/cluster-node-tuning-operator-68cc9c9cf9-6brm7 took: 29.51µs
I0719 01:46:01.798327   37437 default_network_controller.go:699] Recording success event on pod openshift-route-controller-manager/route-controller-manager-676cdfdbc8-t6rhq
I0719 01:46:01.799482   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-monitoring/monitoring-plugin-6f457fd4b8-pqp4m
I0719 01:46:01.799600   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/rook-ceph-mgr-a-6fddb5fd95-mr2cn took: 42.771µs
I0719 01:46:01.799612   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/rook-ceph-mgr-a-6fddb5fd95-mr2cn
I0719 01:46:01.799620   37437 default_network_controller.go:655] Recording add event on pod openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-44-52
I0719 01:46:01.799627   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-44-52
I0719 01:46:01.799635   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-44-52 in node 00-50-56-8a-44-52
I0719 01:46:01.799640   37437 obj_retry.go:541] Creating *v1.Pod openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-44-52 took: 7.395µs
I0719 01:46:01.799645   37437 default_network_controller.go:699] Recording success event on pod openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-44-52
I0719 01:46:01.799650   37437 default_network_controller.go:655] Recording add event on pod openshift-machine-config-operator/machine-config-daemon-4kr96
I0719 01:46:01.799655   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-machine-config-operator/machine-config-daemon-4kr96
I0719 01:46:01.799661   37437 ovn.go:138] Ensuring zone remote for Pod openshift-machine-config-operator/machine-config-daemon-4kr96 in node 00-50-56-8a-5c-ec
I0719 01:46:01.799665   37437 obj_retry.go:541] Creating *v1.Pod openshift-machine-config-operator/machine-config-daemon-4kr96 took: 5.317µs
I0719 01:46:01.799669   37437 default_network_controller.go:699] Recording success event on pod openshift-machine-config-operator/machine-config-daemon-4kr96
I0719 01:46:01.799673   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/rook-ceph-exporter-00-50-56-8a-e1-e7-558dfbd955-jzh65
I0719 01:46:01.799678   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/rook-ceph-exporter-00-50-56-8a-e1-e7-558dfbd955-jzh65
I0719 01:46:01.799683   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/rook-ceph-exporter-00-50-56-8a-e1-e7-558dfbd955-jzh65 in node 00-50-56-8a-e1-e7
I0719 01:46:01.799689   37437 address_set.go:613] (d75a7453-719e-42f4-9198-95782be1eecd/default-network-controller:Namespace:openshift-etcd:v4/a1263951348256964356) deleting addresses [10.129.2.3] from address set
I0719 01:46:01.799699   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/rook-ceph-exporter-00-50-56-8a-e1-e7-558dfbd955-jzh65 took: 15.849µs
I0719 01:46:01.799703   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/rook-ceph-exporter-00-50-56-8a-e1-e7-558dfbd955-jzh65
I0719 01:46:01.799708   37437 default_network_controller.go:655] Recording add event on pod openshift-dns/node-resolver-nsvs6
I0719 01:46:01.799714   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-dns/node-resolver-nsvs6
I0719 01:46:01.799724   37437 ovn.go:134] Ensuring zone local for Pod openshift-dns/node-resolver-nsvs6 in node 00-50-56-8a-fb-ea
I0719 01:46:01.799731   37437 obj_retry.go:541] Creating *v1.Pod openshift-dns/node-resolver-nsvs6 took: 12.251µs
I0719 01:46:01.799735   37437 default_network_controller.go:699] Recording success event on pod openshift-dns/node-resolver-nsvs6
I0719 01:46:01.799739   37437 default_network_controller.go:655] Recording add event on pod openshift-monitoring/node-exporter-9mlmj
I0719 01:46:01.799745   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-monitoring/node-exporter-9mlmj
I0719 01:46:01.799737   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Address_Set Row:map[] Rows:[] Columns:[] Mutations:[{Column:addresses Mutator:delete Value:{GoSet:[10.129.2.3]}}] Timeout:<nil> Where:[where column _uuid == {d75a7453-719e-42f4-9198-95782be1eecd}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.799607   37437 ovn.go:138] Ensuring zone remote for Pod openshift-monitoring/monitoring-plugin-6f457fd4b8-pqp4m in node 00-50-56-8a-f2-5d
I0719 01:46:01.799755   37437 transact.go:42] Configuring OVN: [{Op:mutate Table:Address_Set Row:map[] Rows:[] Columns:[] Mutations:[{Column:addresses Mutator:delete Value:{GoSet:[10.129.2.3]}}] Timeout:<nil> Where:[where column _uuid == {d75a7453-719e-42f4-9198-95782be1eecd}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.799771   37437 obj_retry.go:541] Creating *v1.Pod openshift-monitoring/monitoring-plugin-6f457fd4b8-pqp4m took: 166.163µs
I0719 01:46:01.799775   37437 default_network_controller.go:699] Recording success event on pod openshift-monitoring/monitoring-plugin-6f457fd4b8-pqp4m
I0719 01:46:01.799780   37437 default_network_controller.go:655] Recording add event on pod openshift-console/console-c675c654b-rw8cg
I0719 01:46:01.799784   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-console/console-c675c654b-rw8cg
I0719 01:46:01.799790   37437 ovn.go:138] Ensuring zone remote for Pod openshift-console/console-c675c654b-rw8cg in node 00-50-56-8a-39-a0
I0719 01:46:01.799807   37437 obj_retry.go:541] Creating *v1.Pod openshift-console/console-c675c654b-rw8cg took: 17.782µs
I0719 01:46:01.799813   37437 default_network_controller.go:699] Recording success event on pod openshift-console/console-c675c654b-rw8cg
I0719 01:46:01.799818   37437 default_network_controller.go:655] Recording add event on pod openshift-multus/multus-ltqfr
I0719 01:46:01.799823   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-multus/multus-ltqfr
I0719 01:46:01.799829   37437 ovn.go:138] Ensuring zone remote for Pod openshift-multus/multus-ltqfr in node 00-50-56-8a-39-a0
I0719 01:46:01.799833   37437 obj_retry.go:541] Creating *v1.Pod openshift-multus/multus-ltqfr took: 4.953µs
I0719 01:46:01.799837   37437 default_network_controller.go:699] Recording success event on pod openshift-multus/multus-ltqfr
I0719 01:46:01.799844   37437 default_network_controller.go:655] Recording add event on pod openshift-monitoring/prometheus-operator-admission-webhook-67db68b49d-w8jqx
I0719 01:46:01.799844   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-monitoring/monitoring-plugin-6f457fd4b8-6wb4z
I0719 01:46:01.799850   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-monitoring/prometheus-operator-admission-webhook-67db68b49d-w8jqx
I0719 01:46:01.799851   37437 services_controller.go:519] Full service sync requested
I0719 01:46:01.799855   37437 ovn.go:138] Ensuring zone remote for Pod openshift-monitoring/prometheus-operator-admission-webhook-67db68b49d-w8jqx in node 00-50-56-8a-e1-e7
I0719 01:46:01.799857   37437 default_network_controller.go:699] Recording success event on pod openshift-cluster-node-tuning-operator/cluster-node-tuning-operator-68cc9c9cf9-6brm7
I0719 01:46:01.799861   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/ux-backend-server-6444f844bf-whf8g
I0719 01:46:01.799750   37437 ovn.go:134] Ensuring zone local for Pod openshift-monitoring/node-exporter-9mlmj in node 00-50-56-8a-fb-ea
I0719 01:46:01.799868   37437 default_network_controller.go:655] Recording add event on pod openshift-local-storage/diskmaker-manager-2zrc6
I0719 01:46:01.799853   37437 ovn.go:138] Ensuring zone remote for Pod openshift-monitoring/monitoring-plugin-6f457fd4b8-6wb4z in node 00-50-56-8a-e1-e7
I0719 01:46:01.799875   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-local-storage/diskmaker-manager-2zrc6
I0719 01:46:01.799843   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kni-infra/keepalived-00-50-56-8a-fb-ea
I0719 01:46:01.799879   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-network-diagnostics/network-check-target-dj4vt
I0719 01:46:01.799882   37437 ovn.go:134] Ensuring zone local for Pod openshift-local-storage/diskmaker-manager-2zrc6 in node 00-50-56-8a-fb-ea
I0719 01:46:01.799882   37437 default_network_controller.go:655] Recording add event on pod openshift-machine-api/metal3-baremetal-operator-6fd5ccf9-9p448
I0719 01:46:01.799886   37437 ovn.go:134] Ensuring zone local for Pod openshift-network-diagnostics/network-check-target-dj4vt in node 00-50-56-8a-fb-ea
I0719 01:46:01.799891   37437 ovn.go:134] Ensuring zone local for Pod openshift-kni-infra/keepalived-00-50-56-8a-fb-ea in node 00-50-56-8a-fb-ea
I0719 01:46:01.799894   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-machine-api/metal3-baremetal-operator-6fd5ccf9-9p448
I0719 01:46:01.799896   37437 obj_retry.go:541] Creating *v1.Pod openshift-monitoring/monitoring-plugin-6f457fd4b8-6wb4z took: 44.355µs
I0719 01:46:01.799901   37437 default_network_controller.go:699] Recording success event on pod openshift-monitoring/monitoring-plugin-6f457fd4b8-6wb4z
I0719 01:46:01.799873   37437 obj_retry.go:541] Creating *v1.Pod openshift-monitoring/node-exporter-9mlmj took: 121.501µs
I0719 01:46:01.799906   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/csi-rbdplugin-b6gdm
I0719 01:46:01.799909   37437 default_network_controller.go:699] Recording success event on pod openshift-monitoring/node-exporter-9mlmj
I0719 01:46:01.799913   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/csi-rbdplugin-b6gdm
I0719 01:46:01.799915   37437 default_network_controller.go:655] Recording add event on pod openshift-operator-lifecycle-manager/olm-operator-59f98dcc4-xqd8j
I0719 01:46:01.799868   37437 obj_retry.go:541] Creating *v1.Pod openshift-monitoring/prometheus-operator-admission-webhook-67db68b49d-w8jqx took: 13.563µs
I0719 01:46:01.799919   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/csi-rbdplugin-b6gdm in node 00-50-56-8a-f2-5d
I0719 01:46:01.799922   37437 default_network_controller.go:699] Recording success event on pod openshift-monitoring/prometheus-operator-admission-webhook-67db68b49d-w8jqx
I0719 01:46:01.799924   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-operator-lifecycle-manager/olm-operator-59f98dcc4-xqd8j
I0719 01:46:01.799925   37437 obj_retry.go:541] Creating *v1.Pod openshift-monitoring/openshift-state-metrics-6bb8db76bd-2wlhc took: 1.522371ms
I0719 01:46:01.799901   37437 base_network_controller_pods.go:476] [default/openshift-network-diagnostics/network-check-target-dj4vt] creating logical port openshift-network-diagnostics_network-check-target-dj4vt for pod on switch 00-50-56-8a-fb-ea
I0719 01:46:01.799931   37437 default_network_controller.go:699] Recording success event on pod openshift-monitoring/openshift-state-metrics-6bb8db76bd-2wlhc
I0719 01:46:01.799895   37437 base_network_controller_pods.go:476] [default/openshift-local-storage/diskmaker-manager-2zrc6] creating logical port openshift-local-storage_diskmaker-manager-2zrc6 for pod on switch 00-50-56-8a-fb-ea
I0719 01:46:01.799937   37437 default_network_controller.go:655] Recording add event on pod openshift-network-operator/iptables-alerter-wxl7s
I0719 01:46:01.799943   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-network-operator/iptables-alerter-wxl7s
I0719 01:46:01.799949   37437 ovn.go:138] Ensuring zone remote for Pod openshift-network-operator/iptables-alerter-wxl7s in node 00-50-56-8a-e1-e7
I0719 01:46:01.799953   37437 obj_retry.go:541] Creating *v1.Pod openshift-network-operator/iptables-alerter-wxl7s took: 5.1µs
I0719 01:46:01.799957   37437 default_network_controller.go:699] Recording success event on pod openshift-network-operator/iptables-alerter-wxl7s
I0719 01:46:01.799961   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/rook-ceph-mgr-b-779b65ccb6-29sz4
I0719 01:46:01.799966   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/rook-ceph-mgr-b-779b65ccb6-29sz4
I0719 01:46:01.799971   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/rook-ceph-mgr-b-779b65ccb6-29sz4 in node 00-50-56-8a-e1-e7
I0719 01:46:01.800001   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/rook-ceph-mgr-b-779b65ccb6-29sz4 took: 30.408µs
I0719 01:46:01.799931   37437 ovn.go:138] Ensuring zone remote for Pod openshift-operator-lifecycle-manager/olm-operator-59f98dcc4-xqd8j in node 00-50-56-8a-5c-ec
I0719 01:46:01.800015   37437 default_network_controller.go:655] Recording add event on pod openshift-cluster-storage-operator/csi-snapshot-controller-794ff44f88-7cksj
I0719 01:46:01.800025   37437 obj_retry.go:541] Creating *v1.Pod openshift-operator-lifecycle-manager/olm-operator-59f98dcc4-xqd8j took: 95.165µs
I0719 01:46:01.800030   37437 default_network_controller.go:699] Recording success event on pod openshift-operator-lifecycle-manager/olm-operator-59f98dcc4-xqd8j
I0719 01:46:01.800036   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/noobaa-db-pg-0
I0719 01:46:01.800040   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/rook-ceph-mgr-b-779b65ccb6-29sz4
I0719 01:46:01.799873   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/ux-backend-server-6444f844bf-whf8g in node 00-50-56-8a-e1-e7
I0719 01:46:01.800048   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/noobaa-operator-bf7774fd8-zskvp
I0719 01:46:01.800055   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/noobaa-operator-bf7774fd8-zskvp
I0719 01:46:01.800029   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-cluster-storage-operator/csi-snapshot-controller-794ff44f88-7cksj
I0719 01:46:01.799925   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/csi-rbdplugin-b6gdm took: 6.169µs
I0719 01:46:01.800042   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/noobaa-db-pg-0
I0719 01:46:01.800082   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/csi-rbdplugin-b6gdm
I0719 01:46:01.799903   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-monitoring/thanos-querier-68bf686489-qbcjs
I0719 01:46:01.800092   37437 default_network_controller.go:655] Recording add event on pod openshift-multus/network-metrics-daemon-7ttpg
I0719 01:46:01.800095   37437 ovn.go:138] Ensuring zone remote for Pod openshift-monitoring/thanos-querier-68bf686489-qbcjs in node 00-50-56-8a-e1-e7
I0719 01:46:01.800101   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-multus/network-metrics-daemon-7ttpg
I0719 01:46:01.800109   37437 ovn.go:134] Ensuring zone local for Pod openshift-multus/network-metrics-daemon-7ttpg in node 00-50-56-8a-fb-ea
I0719 01:46:01.800127   37437 base_network_controller_pods.go:476] [default/openshift-multus/network-metrics-daemon-7ttpg] creating logical port openshift-multus_network-metrics-daemon-7ttpg for pod on switch 00-50-56-8a-fb-ea
I0719 01:46:01.800117   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[0a:58:0a:82:00:03 10.130.0.3]} options:{GoMap:map[iface-id-ver:df7bf111-6cb1-4687-9496-e5b90d4ec650 requested-chassis:00-50-56-8a-fb-ea]} port_security:{GoSet:[0a:58:0a:82:00:03 10.130.0.3]} tag_request:{GoSet:[]} type:] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {3d36b4a1-7390-4f3d-92a8-cf79b788e3c6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.799911   37437 obj_retry.go:541] Creating *v1.Pod openshift-cluster-node-tuning-operator/tuned-hpvxx took: 1.498042ms
I0719 01:46:01.800147   37437 default_network_controller.go:699] Recording success event on pod openshift-cluster-node-tuning-operator/tuned-hpvxx
I0719 01:46:01.800152   37437 default_network_controller.go:655] Recording add event on pod openshift-kube-apiserver/kube-apiserver-guard-00-50-56-8a-5c-ec
I0719 01:46:01.800120   37437 obj_retry.go:541] Creating *v1.Pod openshift-monitoring/thanos-querier-68bf686489-qbcjs took: 26.769µs
I0719 01:46:01.800158   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kube-apiserver/kube-apiserver-guard-00-50-56-8a-5c-ec
I0719 01:46:01.800162   37437 default_network_controller.go:699] Recording success event on pod openshift-monitoring/thanos-querier-68bf686489-qbcjs
I0719 01:46:01.800157   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:3d36b4a1-7390-4f3d-92a8-cf79b788e3c6}]}}] Timeout:<nil> Where:[where column _uuid == {bc57259c-2feb-4fdd-95c3-dc98eb57f6e4}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.800084   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/noobaa-db-pg-0 in node 00-50-56-8a-e1-e7
I0719 01:46:01.800171   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/rook-ceph-crashcollector-00-50-56-8a-f2-5d-5bfb656d8f-tvtpr
I0719 01:46:01.800165   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kube-apiserver/kube-apiserver-guard-00-50-56-8a-5c-ec in node 00-50-56-8a-5c-ec
I0719 01:46:01.800180   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/rook-ceph-crashcollector-00-50-56-8a-f2-5d-5bfb656d8f-tvtpr
I0719 01:46:01.800187   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/rook-ceph-crashcollector-00-50-56-8a-f2-5d-5bfb656d8f-tvtpr in node 00-50-56-8a-f2-5d
I0719 01:46:01.799896   37437 obj_retry.go:541] Creating *v1.Pod openshift-kni-infra/keepalived-00-50-56-8a-fb-ea took: 12.217µs
I0719 01:46:01.800063   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/noobaa-operator-bf7774fd8-zskvp in node 00-50-56-8a-e1-e7
I0719 01:46:01.800072   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/ux-backend-server-6444f844bf-whf8g took: 205.525µs
I0719 01:46:01.800205   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/ux-backend-server-6444f844bf-whf8g
I0719 01:46:01.800200   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Port_Group Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:3d36b4a1-7390-4f3d-92a8-cf79b788e3c6}]}}] Timeout:<nil> Where:[where column _uuid == {6bf9bdd3-8780-4e09-b7c5-dc4c1b97c060}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.800210   37437 default_network_controller.go:655] Recording add event on pod openshift-etcd/etcd-guard-00-50-56-8a-44-52
I0719 01:46:01.800217   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-etcd/etcd-guard-00-50-56-8a-44-52
I0719 01:46:01.800220   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/noobaa-operator-bf7774fd8-zskvp took: 158.648µs
I0719 01:46:01.800223   37437 ovn.go:138] Ensuring zone remote for Pod openshift-etcd/etcd-guard-00-50-56-8a-44-52 in node 00-50-56-8a-44-52
I0719 01:46:01.800226   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/noobaa-operator-bf7774fd8-zskvp
I0719 01:46:01.800226   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/rook-ceph-crashcollector-00-50-56-8a-f2-5d-5bfb656d8f-tvtpr took: 40.536µs
I0719 01:46:01.800232   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/rook-ceph-crashcollector-00-50-56-8a-f2-5d-5bfb656d8f-tvtpr
I0719 01:46:01.800234   37437 default_network_controller.go:655] Recording add event on pod openshift-machine-api/control-plane-machine-set-operator-77bcc698b6-wvkdb
I0719 01:46:01.799928   37437 default_network_controller.go:655] Recording add event on pod openshift-etcd/etcd-00-50-56-8a-5c-ec
I0719 01:46:01.799863   37437 default_network_controller.go:655] Recording add event on pod openshift-controller-manager/controller-manager-5c7f9f9d47-thph4
I0719 01:46:01.800248   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-controller-manager/controller-manager-5c7f9f9d47-thph4
I0719 01:46:01.799905   37437 ovn.go:138] Ensuring zone remote for Pod openshift-machine-api/metal3-baremetal-operator-6fd5ccf9-9p448 in node 00-50-56-8a-39-a0
I0719 01:46:01.800256   37437 ovn.go:138] Ensuring zone remote for Pod openshift-controller-manager/controller-manager-5c7f9f9d47-thph4 in node 00-50-56-8a-39-a0
I0719 01:46:01.800606   37437 model_client.go:381] Update operations generated as: [{Op:update Table:NAT Row:map[external_ip:10.10.25.235 logical_ip:10.130.0.3 options:{GoMap:map[stateless:false]} type:snat] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {c74772bc-1ecf-4c29-a440-a7b82ef7063b}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.800668   37437 obj_retry.go:541] Creating *v1.Pod openshift-controller-manager/controller-manager-5c7f9f9d47-thph4 took: 383.799µs
I0719 01:46:01.800693   37437 default_network_controller.go:699] Recording success event on pod openshift-controller-manager/controller-manager-5c7f9f9d47-thph4
I0719 01:46:01.800718   37437 default_network_controller.go:655] Recording add event on pod openshift-kni-infra/keepalived-00-50-56-8a-e1-e7
I0719 01:46:01.800742   37437 obj_retry.go:541] Creating *v1.Pod openshift-etcd/etcd-guard-00-50-56-8a-44-52 took: 518.852µs
I0719 01:46:01.800753   37437 default_network_controller.go:699] Recording success event on pod openshift-etcd/etcd-guard-00-50-56-8a-44-52
I0719 01:46:01.800767   37437 default_network_controller.go:655] Recording add event on pod openshift-console/console-57f455cd77-h96cj
I0719 01:46:01.800775   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-console/console-57f455cd77-h96cj
I0719 01:46:01.800781   37437 obj_retry.go:541] Creating *v1.Pod openshift-console/console-57f455cd77-h96cj took: 214ns
I0719 01:46:01.800785   37437 default_network_controller.go:699] Recording success event on pod openshift-console/console-57f455cd77-h96cj
I0719 01:46:01.800791   37437 default_network_controller.go:655] Recording add event on pod openshift-kube-scheduler-operator/openshift-kube-scheduler-operator-555f7bb8bc-4vw77
I0719 01:46:01.800798   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-machine-api/control-plane-machine-set-operator-77bcc698b6-wvkdb
I0719 01:46:01.800812   37437 ovn.go:138] Ensuring zone remote for Pod openshift-machine-api/control-plane-machine-set-operator-77bcc698b6-wvkdb in node 00-50-56-8a-5c-ec
I0719 01:46:01.800827   37437 obj_retry.go:541] Creating *v1.Pod openshift-machine-api/control-plane-machine-set-operator-77bcc698b6-wvkdb took: 17.273µs
I0719 01:46:01.800834   37437 default_network_controller.go:699] Recording success event on pod openshift-machine-api/control-plane-machine-set-operator-77bcc698b6-wvkdb
I0719 01:46:01.800844   37437 default_network_controller.go:655] Recording add event on pod openshift-monitoring/node-exporter-7m7sg
I0719 01:46:01.800850   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-monitoring/node-exporter-7m7sg
I0719 01:46:01.800856   37437 ovn.go:138] Ensuring zone remote for Pod openshift-monitoring/node-exporter-7m7sg in node 00-50-56-8a-e1-e7
I0719 01:46:01.800861   37437 obj_retry.go:541] Creating *v1.Pod openshift-monitoring/node-exporter-7m7sg took: 5.825µs
I0719 01:46:01.800865   37437 default_network_controller.go:699] Recording success event on pod openshift-monitoring/node-exporter-7m7sg
I0719 01:46:01.800444   37437 default_network_controller.go:655] Recording add event on pod openshift-dns-operator/dns-operator-5fc6bf9796-jgj7s
I0719 01:46:01.800873   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-etcd/etcd-00-50-56-8a-5c-ec
I0719 01:46:01.800171   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[0a:58:0a:82:00:11 10.130.0.17]} options:{GoMap:map[iface-id-ver:b68a6803-6a94-4650-9d45-997245e04fe1 requested-chassis:00-50-56-8a-fb-ea]} port_security:{GoSet:[0a:58:0a:82:00:11 10.130.0.17]} tag_request:{GoSet:[]} type:] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {8105b57b-09e5-4f84-bac3-f79cdbc3d9ae}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.800887   37437 ovn.go:138] Ensuring zone remote for Pod openshift-etcd/etcd-00-50-56-8a-5c-ec in node 00-50-56-8a-5c-ec
I0719 01:46:01.800896   37437 obj_retry.go:541] Creating *v1.Pod openshift-etcd/etcd-00-50-56-8a-5c-ec took: 9.874µs
I0719 01:46:01.800900   37437 default_network_controller.go:699] Recording success event on pod openshift-etcd/etcd-00-50-56-8a-5c-ec
I0719 01:46:01.800907   37437 default_network_controller.go:655] Recording add event on pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-44-52
I0719 01:46:01.800913   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-44-52
I0719 01:46:01.800919   37437 ovn.go:138] Ensuring zone remote for Pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-44-52 in node 00-50-56-8a-44-52
I0719 01:46:01.800916   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/noobaa-db-pg-0 took: 829.34µs
I0719 01:46:01.800924   37437 obj_retry.go:541] Creating *v1.Pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-44-52 took: 5.591µs
I0719 01:46:01.800928   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/noobaa-db-pg-0
I0719 01:46:01.800929   37437 default_network_controller.go:699] Recording success event on pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-44-52
I0719 01:46:01.800938   37437 default_network_controller.go:655] Recording add event on pod openshift-kube-controller-manager-operator/kube-controller-manager-operator-85c67fcb8d-fg9j7
I0719 01:46:01.800943   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kube-scheduler-operator/openshift-kube-scheduler-operator-555f7bb8bc-4vw77
I0719 01:46:01.800948   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kube-controller-manager-operator/kube-controller-manager-operator-85c67fcb8d-fg9j7
I0719 01:46:01.800951   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kube-scheduler-operator/openshift-kube-scheduler-operator-555f7bb8bc-4vw77 in node 00-50-56-8a-5c-ec
I0719 01:46:01.800199   37437 default_network_controller.go:699] Recording success event on pod openshift-kni-infra/keepalived-00-50-56-8a-fb-ea
I0719 01:46:01.800957   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kube-controller-manager-operator/kube-controller-manager-operator-85c67fcb8d-fg9j7 in node 00-50-56-8a-5c-ec
I0719 01:46:01.800964   37437 default_network_controller.go:655] Recording add event on pod openshift-network-operator/iptables-alerter-m6v49
I0719 01:46:01.800971   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-network-operator/iptables-alerter-m6v49
I0719 01:46:01.800974   37437 obj_retry.go:541] Creating *v1.Pod openshift-kube-scheduler-operator/openshift-kube-scheduler-operator-555f7bb8bc-4vw77 took: 24.126µs
I0719 01:46:01.800980   37437 default_network_controller.go:699] Recording success event on pod openshift-kube-scheduler-operator/openshift-kube-scheduler-operator-555f7bb8bc-4vw77
I0719 01:46:01.800997   37437 default_network_controller.go:655] Recording add event on pod openshift-ovn-kubernetes/ovnkube-node-9h9qr
I0719 01:46:01.801003   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-ovn-kubernetes/ovnkube-node-9h9qr
I0719 01:46:01.801005   37437 ovn.go:138] Ensuring zone remote for Pod openshift-network-operator/iptables-alerter-m6v49 in node 00-50-56-8a-f2-5d
I0719 01:46:01.801010   37437 ovn.go:134] Ensuring zone local for Pod openshift-ovn-kubernetes/ovnkube-node-9h9qr in node 00-50-56-8a-fb-ea
I0719 01:46:01.800939   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/csi-addons-controller-manager-6d78957fdf-gs4tk
I0719 01:46:01.801015   37437 obj_retry.go:541] Creating *v1.Pod openshift-ovn-kubernetes/ovnkube-node-9h9qr took: 6.723µs
I0719 01:46:01.801025   37437 default_network_controller.go:699] Recording success event on pod openshift-ovn-kubernetes/ovnkube-node-9h9qr
I0719 01:46:01.801034   37437 default_network_controller.go:655] Recording add event on pod openshift-machine-api/cluster-baremetal-operator-5fb6f8f7d4-ltc5l
I0719 01:46:01.801034   37437 ovnkube_controller.go:1292] Config duration recorder: kind/namespace/name pod/openshift-etcd/etcd-00-50-56-8a-5c-ec. OVN-Kubernetes controller took 0.000659977 seconds. No OVN measurement.
I0719 01:46:01.801040   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-machine-api/cluster-baremetal-operator-5fb6f8f7d4-ltc5l
I0719 01:46:01.801047   37437 ovn.go:138] Ensuring zone remote for Pod openshift-machine-api/cluster-baremetal-operator-5fb6f8f7d4-ltc5l in node 00-50-56-8a-39-a0
I0719 01:46:01.800669   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:nat Mutator:insert Value:{GoSet:[{GoUUID:c74772bc-1ecf-4c29-a440-a7b82ef7063b}]}}] Timeout:<nil> Where:[where column _uuid == {26b6d604-e9d3-4544-a4f0-f760e4ff11b6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.801064   37437 default_network_controller.go:655] Recording add event on pod openshift-multus/network-metrics-daemon-bqt8s
I0719 01:46:01.801074   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-multus/network-metrics-daemon-bqt8s
I0719 01:46:01.801092   37437 ovn.go:138] Ensuring zone remote for Pod openshift-multus/network-metrics-daemon-bqt8s in node 00-50-56-8a-44-52
I0719 01:46:01.801065   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[0a:58:0a:82:00:03 10.130.0.3]} options:{GoMap:map[iface-id-ver:df7bf111-6cb1-4687-9496-e5b90d4ec650 requested-chassis:00-50-56-8a-fb-ea]} port_security:{GoSet:[0a:58:0a:82:00:03 10.130.0.3]} tag_request:{GoSet:[]} type:] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {3d36b4a1-7390-4f3d-92a8-cf79b788e3c6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:3d36b4a1-7390-4f3d-92a8-cf79b788e3c6}]}}] Timeout:<nil> Where:[where column _uuid == {bc57259c-2feb-4fdd-95c3-dc98eb57f6e4}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Port_Group Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:3d36b4a1-7390-4f3d-92a8-cf79b788e3c6}]}}] Timeout:<nil> Where:[where column _uuid == {6bf9bdd3-8780-4e09-b7c5-dc4c1b97c060}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:update Table:NAT Row:map[external_ip:10.10.25.235 logical_ip:10.130.0.3 options:{GoMap:map[stateless:false]} type:snat] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {c74772bc-1ecf-4c29-a440-a7b82ef7063b}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:nat Mutator:insert Value:{GoSet:[{GoUUID:c74772bc-1ecf-4c29-a440-a7b82ef7063b}]}}] Timeout:<nil> Where:[where column _uuid == {26b6d604-e9d3-4544-a4f0-f760e4ff11b6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.801020   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/csi-addons-controller-manager-6d78957fdf-gs4tk
I0719 01:46:01.801150   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/csi-addons-controller-manager-6d78957fdf-gs4tk in node 00-50-56-8a-f2-5d
I0719 01:46:01.800209   37437 obj_retry.go:541] Creating *v1.Pod openshift-kube-apiserver/kube-apiserver-guard-00-50-56-8a-5c-ec took: 45.33µs
I0719 01:46:01.801194   37437 default_network_controller.go:699] Recording success event on pod openshift-kube-apiserver/kube-apiserver-guard-00-50-56-8a-5c-ec
I0719 01:46:01.801212   37437 ovs.go:162] Exec(28): stdout: "[b05109fd-71da-455e-8873-6ea210676041]\n"
I0719 01:46:01.801223   37437 ovs.go:163] Exec(28): stderr: ""
I0719 01:46:01.801239   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/csi-cephfsplugin-5fvh4
I0719 01:46:01.801010   37437 obj_retry.go:541] Creating *v1.Pod openshift-kube-controller-manager-operator/kube-controller-manager-operator-85c67fcb8d-fg9j7 took: 54.225µs
I0719 01:46:01.801282   37437 default_network_controller.go:699] Recording success event on pod openshift-kube-controller-manager-operator/kube-controller-manager-operator-85c67fcb8d-fg9j7
I0719 01:46:01.800072   37437 ovn.go:138] Ensuring zone remote for Pod openshift-cluster-storage-operator/csi-snapshot-controller-794ff44f88-7cksj in node 00-50-56-8a-5c-ec
I0719 01:46:01.800935   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:8105b57b-09e5-4f84-bac3-f79cdbc3d9ae}]}}] Timeout:<nil> Where:[where column _uuid == {bc57259c-2feb-4fdd-95c3-dc98eb57f6e4}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.801355   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kni-infra/keepalived-00-50-56-8a-e1-e7
I0719 01:46:01.801366   37437 obj_retry.go:541] Creating *v1.Pod openshift-cluster-storage-operator/csi-snapshot-controller-794ff44f88-7cksj took: 1.295283ms
I0719 01:46:01.801369   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kni-infra/keepalived-00-50-56-8a-e1-e7 in node 00-50-56-8a-e1-e7
I0719 01:46:01.801373   37437 default_network_controller.go:699] Recording success event on pod openshift-cluster-storage-operator/csi-snapshot-controller-794ff44f88-7cksj
I0719 01:46:01.801376   37437 obj_retry.go:541] Creating *v1.Pod openshift-kni-infra/keepalived-00-50-56-8a-e1-e7 took: 9.023µs
I0719 01:46:01.801382   37437 default_network_controller.go:699] Recording success event on pod openshift-kni-infra/keepalived-00-50-56-8a-e1-e7
I0719 01:46:01.801380   37437 default_network_controller.go:655] Recording add event on pod openshift-multus/multus-additional-cni-plugins-tpn87
I0719 01:46:01.801389   37437 default_network_controller.go:655] Recording add event on pod openshift-service-ca/service-ca-6dbc4646f9-6q769
I0719 01:46:01.801392   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-multus/multus-additional-cni-plugins-tpn87
I0719 01:46:01.801400   37437 ovn.go:138] Ensuring zone remote for Pod openshift-multus/multus-additional-cni-plugins-tpn87 in node 00-50-56-8a-e1-e7
I0719 01:46:01.801402   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-service-ca/service-ca-6dbc4646f9-6q769
I0719 01:46:01.801405   37437 obj_retry.go:541] Creating *v1.Pod openshift-multus/multus-additional-cni-plugins-tpn87 took: 6.673µs
I0719 01:46:01.801409   37437 ovn.go:138] Ensuring zone remote for Pod openshift-service-ca/service-ca-6dbc4646f9-6q769 in node 00-50-56-8a-39-a0
I0719 01:46:01.801437   37437 obj_retry.go:541] Creating *v1.Pod openshift-service-ca/service-ca-6dbc4646f9-6q769 took: 28.825µs
I0719 01:46:01.801444   37437 default_network_controller.go:699] Recording success event on pod openshift-service-ca/service-ca-6dbc4646f9-6q769
I0719 01:46:01.801449   37437 default_network_controller.go:655] Recording add event on pod openshift-ovn-kubernetes/ovnkube-node-mqh7r
I0719 01:46:01.801455   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-ovn-kubernetes/ovnkube-node-mqh7r
I0719 01:46:01.801461   37437 ovn.go:138] Ensuring zone remote for Pod openshift-ovn-kubernetes/ovnkube-node-mqh7r in node 00-50-56-8a-5c-ec
I0719 01:46:01.801046   37437 ovnkube_controller.go:1292] Config duration recorder: kind/namespace/name pod/openshift-kube-scheduler-operator/openshift-kube-scheduler-operator-555f7bb8bc-4vw77. OVN-Kubernetes controller took 0.000198589 seconds. No OVN measurement.
I0719 01:46:01.801410   37437 default_network_controller.go:699] Recording success event on pod openshift-multus/multus-additional-cni-plugins-tpn87
I0719 01:46:01.801066   37437 obj_retry.go:541] Creating *v1.Pod openshift-machine-api/cluster-baremetal-operator-5fb6f8f7d4-ltc5l took: 19.921µs
I0719 01:46:01.801479   37437 default_network_controller.go:655] Recording add event on pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-f2-5d
I0719 01:46:01.801481   37437 default_network_controller.go:699] Recording success event on pod openshift-machine-api/cluster-baremetal-operator-5fb6f8f7d4-ltc5l
I0719 01:46:01.800497   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[0a:58:0a:82:00:04 10.130.0.4]} options:{GoMap:map[iface-id-ver:37298806-1fb0-40f5-85e9-8ec04e23a29b requested-chassis:00-50-56-8a-fb-ea]} port_security:{GoSet:[0a:58:0a:82:00:04 10.130.0.4]} tag_request:{GoSet:[]} type:] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {08abcee6-d3a4-4fc0-a550-dbee0406324c}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.801489   37437 default_network_controller.go:655] Recording add event on pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-e1-e7
I0719 01:46:01.800552   37437 obj_retry.go:541] Creating *v1.Pod openshift-machine-api/metal3-baremetal-operator-6fd5ccf9-9p448 took: 647.431µs
I0719 01:46:01.801496   37437 default_network_controller.go:699] Recording success event on pod openshift-machine-api/metal3-baremetal-operator-6fd5ccf9-9p448
I0719 01:46:01.801498   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-e1-e7
I0719 01:46:01.801502   37437 default_network_controller.go:655] Recording add event on pod openshift-kni-infra/haproxy-00-50-56-8a-5c-ec
I0719 01:46:01.801507   37437 ovn.go:138] Ensuring zone remote for Pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-e1-e7 in node 00-50-56-8a-e1-e7
I0719 01:46:01.799905   37437 default_network_controller.go:699] Recording success event on pod openshift-kni-infra/coredns-00-50-56-8a-44-52
I0719 01:46:01.801523   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/rook-ceph-mon-b-59759dbb89-7jlvw
I0719 01:46:01.801527   37437 obj_retry.go:541] Creating *v1.Pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-e1-e7 took: 21.671µs
I0719 01:46:01.801533   37437 default_network_controller.go:699] Recording success event on pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-e1-e7
I0719 01:46:01.801174   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/csi-addons-controller-manager-6d78957fdf-gs4tk took: 25.162µs
I0719 01:46:01.801540   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/csi-addons-controller-manager-6d78957fdf-gs4tk
I0719 01:46:01.801543   37437 default_network_controller.go:655] Recording add event on pod openshift-kni-infra/keepalived-00-50-56-8a-39-a0
I0719 01:46:01.801545   37437 default_network_controller.go:655] Recording add event on pod openshift-image-registry/node-ca-tvhtl
I0719 01:46:01.801550   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kni-infra/keepalived-00-50-56-8a-39-a0
I0719 01:46:01.801537   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:08abcee6-d3a4-4fc0-a550-dbee0406324c}]}}] Timeout:<nil> Where:[where column _uuid == {bc57259c-2feb-4fdd-95c3-dc98eb57f6e4}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.801556   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kni-infra/keepalived-00-50-56-8a-39-a0 in node 00-50-56-8a-39-a0
I0719 01:46:01.801561   37437 obj_retry.go:541] Creating *v1.Pod openshift-kni-infra/keepalived-00-50-56-8a-39-a0 took: 6.09µs
I0719 01:46:01.801565   37437 default_network_controller.go:699] Recording success event on pod openshift-kni-infra/keepalived-00-50-56-8a-39-a0
I0719 01:46:01.801572   37437 default_network_controller.go:655] Recording add event on pod openshift-network-operator/iptables-alerter-6s78n
I0719 01:46:01.801578   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-network-operator/iptables-alerter-6s78n
I0719 01:46:01.801588   37437 ovn.go:138] Ensuring zone remote for Pod openshift-network-operator/iptables-alerter-6s78n in node 00-50-56-8a-5c-ec
I0719 01:46:01.801592   37437 obj_retry.go:541] Creating *v1.Pod openshift-network-operator/iptables-alerter-6s78n took: 5.543µs
I0719 01:46:01.801596   37437 default_network_controller.go:699] Recording success event on pod openshift-network-operator/iptables-alerter-6s78n
I0719 01:46:01.801601   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/csi-rbdplugin-xgkn6
I0719 01:46:01.801607   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/csi-rbdplugin-xgkn6
I0719 01:46:01.801600   37437 port_cache.go:96] port-cache(openshift-network-diagnostics_network-check-target-dj4vt): added port &{name:openshift-network-diagnostics_network-check-target-dj4vt uuid:3d36b4a1-7390-4f3d-92a8-cf79b788e3c6 logicalSwitch:00-50-56-8a-fb-ea ips:[0xc0015b68a0] mac:[10 88 10 130 0 3] expires:{wall:0 ext:0 loc:<nil>}} with IP: [10.130.0.3/23] and MAC: 0a:58:0a:82:00:03
I0719 01:46:01.801619   37437 pods.go:220] [openshift-network-diagnostics/network-check-target-dj4vt] addLogicalPort took 1.724944ms, libovsdb time 525.957µs
I0719 01:46:01.801608   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Port_Group Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:08abcee6-d3a4-4fc0-a550-dbee0406324c}]}}] Timeout:<nil> Where:[where column _uuid == {dd05a1c4-32f5-4f3f-937e-1e74633a1101}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.801627   37437 obj_retry.go:541] Creating *v1.Pod openshift-network-diagnostics/network-check-target-dj4vt took: 1.740589ms
I0719 01:46:01.801613   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/csi-rbdplugin-xgkn6 in node 00-50-56-8a-e1-e7
I0719 01:46:01.801636   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/csi-rbdplugin-xgkn6 took: 23.318µs
I0719 01:46:01.801555   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-image-registry/node-ca-tvhtl
I0719 01:46:01.801641   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/csi-rbdplugin-xgkn6
I0719 01:46:01.801646   37437 ovn.go:138] Ensuring zone remote for Pod openshift-image-registry/node-ca-tvhtl in node 00-50-56-8a-e1-e7
I0719 01:46:01.801633   37437 default_network_controller.go:699] Recording success event on pod openshift-network-diagnostics/network-check-target-dj4vt
I0719 01:46:01.801652   37437 obj_retry.go:541] Creating *v1.Pod openshift-image-registry/node-ca-tvhtl took: 6.515µs
I0719 01:46:01.801657   37437 default_network_controller.go:699] Recording success event on pod openshift-image-registry/node-ca-tvhtl
I0719 01:46:01.801656   37437 default_network_controller.go:655] Recording add event on pod openshift-console/console-57f455cd77-77wrt
I0719 01:46:01.801662   37437 default_network_controller.go:655] Recording add event on pod openshift-multus/multus-47wxd
I0719 01:46:01.801666   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-console/console-57f455cd77-77wrt
I0719 01:46:01.801669   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-multus/multus-47wxd
I0719 01:46:01.801672   37437 obj_retry.go:541] Creating *v1.Pod openshift-console/console-57f455cd77-77wrt took: 137ns
I0719 01:46:01.801676   37437 default_network_controller.go:699] Recording success event on pod openshift-console/console-57f455cd77-77wrt
I0719 01:46:01.801678   37437 ovn.go:138] Ensuring zone remote for Pod openshift-multus/multus-47wxd in node 00-50-56-8a-44-52
I0719 01:46:01.801681   37437 default_network_controller.go:655] Recording add event on pod openshift-kni-infra/haproxy-00-50-56-8a-39-a0
I0719 01:46:01.801683   37437 obj_retry.go:541] Creating *v1.Pod openshift-multus/multus-47wxd took: 8.983µs
I0719 01:46:01.801688   37437 default_network_controller.go:699] Recording success event on pod openshift-multus/multus-47wxd
I0719 01:46:01.801647   37437 default_network_controller.go:655] Recording add event on pod openshift-marketplace/redhat-operators-mm6k4
I0719 01:46:01.801688   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kni-infra/haproxy-00-50-56-8a-39-a0
I0719 01:46:01.801508   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kni-infra/haproxy-00-50-56-8a-5c-ec
I0719 01:46:01.801722   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kni-infra/haproxy-00-50-56-8a-5c-ec in node 00-50-56-8a-5c-ec
I0719 01:46:01.801732   37437 obj_retry.go:541] Creating *v1.Pod openshift-kni-infra/haproxy-00-50-56-8a-5c-ec took: 16.172µs
I0719 01:46:01.801738   37437 default_network_controller.go:699] Recording success event on pod openshift-kni-infra/haproxy-00-50-56-8a-5c-ec
I0719 01:46:01.801745   37437 default_network_controller.go:655] Recording add event on pod openshift-machine-api/metal3-image-customization-5f9d4c754c-5v2p8
I0719 01:46:01.801760   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-machine-api/metal3-image-customization-5f9d4c754c-5v2p8
I0719 01:46:01.801768   37437 ovn.go:138] Ensuring zone remote for Pod openshift-machine-api/metal3-image-customization-5f9d4c754c-5v2p8 in node 00-50-56-8a-39-a0
I0719 01:46:01.801759   37437 model_client.go:381] Update operations generated as: [{Op:update Table:NAT Row:map[external_ip:10.10.25.235 logical_ip:10.130.0.4 options:{GoMap:map[stateless:false]} type:snat] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {8f0033f4-1487-4c43-8c06-196e155647ed}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.801529   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/rook-ceph-mon-b-59759dbb89-7jlvw
I0719 01:46:01.801785   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/rook-ceph-mon-b-59759dbb89-7jlvw took: 184ns
I0719 01:46:01.801790   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/rook-ceph-mon-b-59759dbb89-7jlvw
I0719 01:46:01.801797   37437 default_network_controller.go:655] Recording add event on pod openshift-monitoring/node-exporter-gbsmf
I0719 01:46:01.801805   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-monitoring/node-exporter-gbsmf
I0719 01:46:01.801797   37437 obj_retry.go:541] Creating *v1.Pod openshift-machine-api/metal3-image-customization-5f9d4c754c-5v2p8 took: 29.464µs
I0719 01:46:01.801817   37437 default_network_controller.go:699] Recording success event on pod openshift-machine-api/metal3-image-customization-5f9d4c754c-5v2p8
I0719 01:46:01.801272   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/csi-cephfsplugin-5fvh4
I0719 01:46:01.801807   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:nat Mutator:insert Value:{GoSet:[{GoUUID:8f0033f4-1487-4c43-8c06-196e155647ed}]}}] Timeout:<nil> Where:[where column _uuid == {26b6d604-e9d3-4544-a4f0-f760e4ff11b6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.801827   37437 ovn.go:134] Ensuring zone local for Pod openshift-storage/csi-cephfsplugin-5fvh4 in node 00-50-56-8a-fb-ea
I0719 01:46:01.801830   37437 default_network_controller.go:655] Recording add event on pod openshift-image-registry/node-ca-986d7
I0719 01:46:01.801834   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/csi-cephfsplugin-5fvh4 took: 7.564µs
I0719 01:46:01.801838   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/csi-cephfsplugin-5fvh4
I0719 01:46:01.801843   37437 default_network_controller.go:655] Recording add event on pod openshift-dns/node-resolver-bf5zv
I0719 01:46:01.801849   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-dns/node-resolver-bf5zv
I0719 01:46:01.801861   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-image-registry/node-ca-986d7
I0719 01:46:01.801867   37437 ovn.go:138] Ensuring zone remote for Pod openshift-dns/node-resolver-bf5zv in node 00-50-56-8a-5c-ec
I0719 01:46:01.801260   37437 ovs.go:159] Exec(29): /usr/bin/ovs-vsctl --timeout=15 get Interface 16af03e8-0b22-4405-97ef-670f17d9e493 Type
I0719 01:46:01.801872   37437 obj_retry.go:541] Creating *v1.Pod openshift-dns/node-resolver-bf5zv took: 8.796µs
I0719 01:46:01.801877   37437 default_network_controller.go:699] Recording success event on pod openshift-dns/node-resolver-bf5zv
I0719 01:46:01.801882   37437 default_network_controller.go:655] Recording add event on pod openshift-kni-infra/coredns-00-50-56-8a-f2-5d
I0719 01:46:01.801888   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kni-infra/coredns-00-50-56-8a-f2-5d
I0719 01:46:01.801894   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kni-infra/coredns-00-50-56-8a-f2-5d in node 00-50-56-8a-f2-5d
I0719 01:46:01.801898   37437 obj_retry.go:541] Creating *v1.Pod openshift-kni-infra/coredns-00-50-56-8a-f2-5d took: 5.836µs
I0719 01:46:01.801321   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-dns-operator/dns-operator-5fc6bf9796-jgj7s
I0719 01:46:01.801868   37437 ovn.go:138] Ensuring zone remote for Pod openshift-image-registry/node-ca-986d7 in node 00-50-56-8a-f2-5d
I0719 01:46:01.801914   37437 obj_retry.go:541] Creating *v1.Pod openshift-image-registry/node-ca-986d7 took: 45.645µs
I0719 01:46:01.801919   37437 default_network_controller.go:699] Recording success event on pod openshift-image-registry/node-ca-986d7
I0719 01:46:01.801831   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[0a:58:0a:82:00:04 10.130.0.4]} options:{GoMap:map[iface-id-ver:37298806-1fb0-40f5-85e9-8ec04e23a29b requested-chassis:00-50-56-8a-fb-ea]} port_security:{GoSet:[0a:58:0a:82:00:04 10.130.0.4]} tag_request:{GoSet:[]} type:] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {08abcee6-d3a4-4fc0-a550-dbee0406324c}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:08abcee6-d3a4-4fc0-a550-dbee0406324c}]}}] Timeout:<nil> Where:[where column _uuid == {bc57259c-2feb-4fdd-95c3-dc98eb57f6e4}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Port_Group Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:08abcee6-d3a4-4fc0-a550-dbee0406324c}]}}] Timeout:<nil> Where:[where column _uuid == {dd05a1c4-32f5-4f3f-937e-1e74633a1101}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:update Table:NAT Row:map[external_ip:10.10.25.235 logical_ip:10.130.0.4 options:{GoMap:map[stateless:false]} type:snat] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {8f0033f4-1487-4c43-8c06-196e155647ed}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:nat Mutator:insert Value:{GoSet:[{GoUUID:8f0033f4-1487-4c43-8c06-196e155647ed}]}}] Timeout:<nil> Where:[where column _uuid == {26b6d604-e9d3-4544-a4f0-f760e4ff11b6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.801926   37437 default_network_controller.go:655] Recording add event on pod openshift-kube-controller-manager/kube-controller-manager-guard-00-50-56-8a-39-a0
I0719 01:46:01.801919   37437 ovn.go:138] Ensuring zone remote for Pod openshift-dns-operator/dns-operator-5fc6bf9796-jgj7s in node 00-50-56-8a-39-a0
I0719 01:46:01.801939   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kube-controller-manager/kube-controller-manager-guard-00-50-56-8a-39-a0
I0719 01:46:01.801946   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kube-controller-manager/kube-controller-manager-guard-00-50-56-8a-39-a0 in node 00-50-56-8a-39-a0
I0719 01:46:01.801972   37437 obj_retry.go:541] Creating *v1.Pod openshift-dns-operator/dns-operator-5fc6bf9796-jgj7s took: 60.546µs
I0719 01:46:01.801979   37437 obj_retry.go:541] Creating *v1.Pod openshift-kube-controller-manager/kube-controller-manager-guard-00-50-56-8a-39-a0 took: 32.956µs
I0719 01:46:01.801992   37437 default_network_controller.go:699] Recording success event on pod openshift-kube-controller-manager/kube-controller-manager-guard-00-50-56-8a-39-a0
I0719 01:46:01.802004   37437 default_network_controller.go:655] Recording add event on pod openshift-kube-scheduler/revision-pruner-6-00-50-56-8a-44-52
I0719 01:46:01.802010   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kube-scheduler/revision-pruner-6-00-50-56-8a-44-52
I0719 01:46:01.802016   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kube-scheduler/revision-pruner-6-00-50-56-8a-44-52 in node 00-50-56-8a-44-52
I0719 01:46:01.801980   37437 default_network_controller.go:699] Recording success event on pod openshift-dns-operator/dns-operator-5fc6bf9796-jgj7s
I0719 01:46:01.802078   37437 obj_retry.go:541] Creating *v1.Pod openshift-kube-scheduler/revision-pruner-6-00-50-56-8a-44-52 took: 62.572µs
I0719 01:46:01.802084   37437 default_network_controller.go:699] Recording success event on pod openshift-kube-scheduler/revision-pruner-6-00-50-56-8a-44-52
I0719 01:46:01.802095   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/rook-ceph-osd-0-6d5dbb5f-24hfr
I0719 01:46:01.802101   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/rook-ceph-osd-0-6d5dbb5f-24hfr
I0719 01:46:01.802106   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/rook-ceph-osd-0-6d5dbb5f-24hfr in node 00-50-56-8a-e1-e7
I0719 01:46:01.802143   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/rook-ceph-osd-0-6d5dbb5f-24hfr took: 37.488µs
I0719 01:46:01.802080   37437 default_network_controller.go:655] Recording add event on pod openshift-multus/multus-additional-cni-plugins-rtmj7
I0719 01:46:01.802194   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/rook-ceph-osd-0-6d5dbb5f-24hfr
I0719 01:46:01.802201   37437 default_network_controller.go:655] Recording add event on pod openshift-image-registry/image-pruner-28689120-2bnxj
I0719 01:46:01.802204   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-multus/multus-additional-cni-plugins-rtmj7
I0719 01:46:01.802208   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-image-registry/image-pruner-28689120-2bnxj
I0719 01:46:01.802212   37437 ovn.go:138] Ensuring zone remote for Pod openshift-multus/multus-additional-cni-plugins-rtmj7 in node 00-50-56-8a-39-a0
I0719 01:46:01.802214   37437 obj_retry.go:459] Detected object openshift-image-registry/image-pruner-28689120-2bnxj of type *v1.Pod in terminal state (e.g. completed) during add event: will remove it
I0719 01:46:01.801817   37437 ovn.go:138] Ensuring zone remote for Pod openshift-monitoring/node-exporter-gbsmf in node 00-50-56-8a-39-a0
I0719 01:46:01.802217   37437 obj_retry.go:541] Creating *v1.Pod openshift-multus/multus-additional-cni-plugins-rtmj7 took: 6.399µs
I0719 01:46:01.802227   37437 default_network_controller.go:699] Recording success event on pod openshift-multus/multus-additional-cni-plugins-rtmj7
I0719 01:46:01.802232   37437 default_network_controller.go:655] Recording add event on pod openshift-monitoring/thanos-querier-68bf686489-9cctf
I0719 01:46:01.802234   37437 obj_retry.go:541] Creating *v1.Pod openshift-monitoring/node-exporter-gbsmf took: 415.524µs
I0719 01:46:01.802245   37437 default_network_controller.go:699] Recording success event on pod openshift-monitoring/node-exporter-gbsmf
I0719 01:46:01.801705   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kni-infra/haproxy-00-50-56-8a-39-a0 in node 00-50-56-8a-39-a0
I0719 01:46:01.802239   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-monitoring/thanos-querier-68bf686489-9cctf
I0719 01:46:01.802261   37437 obj_retry.go:541] Creating *v1.Pod openshift-kni-infra/haproxy-00-50-56-8a-39-a0 took: 556.684µs
I0719 01:46:01.802266   37437 default_network_controller.go:699] Recording success event on pod openshift-kni-infra/haproxy-00-50-56-8a-39-a0
I0719 01:46:01.802271   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/rook-ceph-mds-ocs-storagecluster-cephfilesystem-a-8679ddf7kqp98
I0719 01:46:01.801011   37437 obj_retry.go:541] Creating *v1.Pod openshift-network-operator/iptables-alerter-m6v49 took: 33.153µs
I0719 01:46:01.802281   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/rook-ceph-mds-ocs-storagecluster-cephfilesystem-a-8679ddf7kqp98
I0719 01:46:01.802271   37437 ovn.go:138] Ensuring zone remote for Pod openshift-monitoring/thanos-querier-68bf686489-9cctf in node 00-50-56-8a-f2-5d
I0719 01:46:01.802293   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/rook-ceph-mds-ocs-storagecluster-cephfilesystem-a-8679ddf7kqp98 in node 00-50-56-8a-e1-e7
I0719 01:46:01.801906   37437 default_network_controller.go:699] Recording success event on pod openshift-kni-infra/coredns-00-50-56-8a-f2-5d
I0719 01:46:01.802309   37437 default_network_controller.go:655] Recording add event on pod openshift-machine-api/ironic-proxy-k9xzh
I0719 01:46:01.802320   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-machine-api/ironic-proxy-k9xzh
I0719 01:46:01.802322   37437 address_set.go:613] (468f827d-e692-4f8a-8b7e-c261e6905f5a/default-network-controller:Namespace:openshift-image-registry:v4/a65811733811199347) deleting addresses [10.128.2.44] from address set
I0719 01:46:01.802329   37437 ovn.go:138] Ensuring zone remote for Pod openshift-machine-api/ironic-proxy-k9xzh in node 00-50-56-8a-5c-ec
I0719 01:46:01.802339   37437 obj_retry.go:541] Creating *v1.Pod openshift-machine-api/ironic-proxy-k9xzh took: 10.636µs
I0719 01:46:01.802345   37437 default_network_controller.go:699] Recording success event on pod openshift-machine-api/ironic-proxy-k9xzh
I0719 01:46:01.802282   37437 default_network_controller.go:699] Recording success event on pod openshift-network-operator/iptables-alerter-m6v49
I0719 01:46:01.802359   37437 default_network_controller.go:655] Recording add event on pod openshift-kni-infra/keepalived-00-50-56-8a-f2-5d
I0719 01:46:01.802363   37437 default_network_controller.go:655] Recording add event on pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-fb-ea
I0719 01:46:01.802368   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kni-infra/keepalived-00-50-56-8a-f2-5d
I0719 01:46:01.802357   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Address_Set Row:map[] Rows:[] Columns:[] Mutations:[{Column:addresses Mutator:delete Value:{GoSet:[10.128.2.44]}}] Timeout:<nil> Where:[where column _uuid == {468f827d-e692-4f8a-8b7e-c261e6905f5a}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.802381   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kni-infra/keepalived-00-50-56-8a-f2-5d in node 00-50-56-8a-f2-5d
I0719 01:46:01.802071   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Port_Group Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:8105b57b-09e5-4f84-bac3-f79cdbc3d9ae}]}}] Timeout:<nil> Where:[where column _uuid == {dc5706a1-bba4-466c-a511-94f4646e1880}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.802388   37437 obj_retry.go:541] Creating *v1.Pod openshift-kni-infra/keepalived-00-50-56-8a-f2-5d took: 10.685µs
I0719 01:46:01.802395   37437 default_network_controller.go:699] Recording success event on pod openshift-kni-infra/keepalived-00-50-56-8a-f2-5d
I0719 01:46:01.802324   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/rook-ceph-mds-ocs-storagecluster-cephfilesystem-a-8679ddf7kqp98 took: 33.964µs
I0719 01:46:01.802401   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/odf-console-b7ccd85c5-84cnv
I0719 01:46:01.802404   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/rook-ceph-mds-ocs-storagecluster-cephfilesystem-a-8679ddf7kqp98
I0719 01:46:01.802410   37437 default_network_controller.go:655] Recording add event on pod openshift-etcd/etcd-00-50-56-8a-39-a0
I0719 01:46:01.802382   37437 transact.go:42] Configuring OVN: [{Op:mutate Table:Address_Set Row:map[] Rows:[] Columns:[] Mutations:[{Column:addresses Mutator:delete Value:{GoSet:[10.128.2.44]}}] Timeout:<nil> Where:[where column _uuid == {468f827d-e692-4f8a-8b7e-c261e6905f5a}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.802419   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-etcd/etcd-00-50-56-8a-39-a0
I0719 01:46:01.802414   37437 port_cache.go:96] port-cache(openshift-multus_network-metrics-daemon-7ttpg): added port &{name:openshift-multus_network-metrics-daemon-7ttpg uuid:08abcee6-d3a4-4fc0-a550-dbee0406324c logicalSwitch:00-50-56-8a-fb-ea ips:[0xc00170f020] mac:[10 88 10 130 0 4] expires:{wall:0 ext:0 loc:<nil>}} with IP: [10.130.0.4/23] and MAC: 0a:58:0a:82:00:04
I0719 01:46:01.802426   37437 ovn.go:138] Ensuring zone remote for Pod openshift-etcd/etcd-00-50-56-8a-39-a0 in node 00-50-56-8a-39-a0
I0719 01:46:01.802436   37437 obj_retry.go:541] Creating *v1.Pod openshift-etcd/etcd-00-50-56-8a-39-a0 took: 6.688µs
I0719 01:46:01.802441   37437 default_network_controller.go:699] Recording success event on pod openshift-etcd/etcd-00-50-56-8a-39-a0
I0719 01:46:01.801333   37437 default_network_controller.go:655] Recording add event on pod openshift-network-node-identity/network-node-identity-z7b9j
I0719 01:46:01.802447   37437 default_network_controller.go:655] Recording add event on pod openshift-multus/network-metrics-daemon-fslb2
I0719 01:46:01.802449   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-network-node-identity/network-node-identity-z7b9j
I0719 01:46:01.802453   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-multus/network-metrics-daemon-fslb2
I0719 01:46:01.802456   37437 ovn.go:138] Ensuring zone remote for Pod openshift-network-node-identity/network-node-identity-z7b9j in node 00-50-56-8a-5c-ec
I0719 01:46:01.802460   37437 ovn.go:138] Ensuring zone remote for Pod openshift-multus/network-metrics-daemon-fslb2 in node 00-50-56-8a-f2-5d
I0719 01:46:01.802461   37437 obj_retry.go:541] Creating *v1.Pod openshift-network-node-identity/network-node-identity-z7b9j took: 6.052µs
I0719 01:46:01.802466   37437 default_network_controller.go:699] Recording success event on pod openshift-network-node-identity/network-node-identity-z7b9j
I0719 01:46:01.802475   37437 default_network_controller.go:655] Recording add event on pod openshift-console/downloads-6967878986-76phj
I0719 01:46:01.802481   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-console/downloads-6967878986-76phj
I0719 01:46:01.802345   37437 obj_retry.go:541] Creating *v1.Pod openshift-monitoring/thanos-querier-68bf686489-9cctf took: 79.765µs
I0719 01:46:01.802488   37437 default_network_controller.go:699] Recording success event on pod openshift-monitoring/thanos-querier-68bf686489-9cctf
I0719 01:46:01.802497   37437 ovn.go:138] Ensuring zone remote for Pod openshift-console/downloads-6967878986-76phj in node 00-50-56-8a-5c-ec
I0719 01:46:01.802369   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-fb-ea
I0719 01:46:01.801706   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-marketplace/redhat-operators-mm6k4
I0719 01:46:01.802510   37437 ovn.go:138] Ensuring zone remote for Pod openshift-marketplace/redhat-operators-mm6k4 in node 00-50-56-8a-39-a0
I0719 01:46:01.802518   37437 ovn.go:134] Ensuring zone local for Pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-fb-ea in node 00-50-56-8a-fb-ea
I0719 01:46:01.802430   37437 pods.go:220] [openshift-multus/network-metrics-daemon-7ttpg] addLogicalPort took 2.31443ms, libovsdb time 579.175µs
I0719 01:46:01.802527   37437 obj_retry.go:541] Creating *v1.Pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-fb-ea took: 10.915µs
I0719 01:46:01.802530   37437 obj_retry.go:541] Creating *v1.Pod openshift-marketplace/redhat-operators-mm6k4 took: 20.953µs
I0719 01:46:01.802407   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/odf-console-b7ccd85c5-84cnv
I0719 01:46:01.802535   37437 default_network_controller.go:699] Recording success event on pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-fb-ea
I0719 01:46:01.802520   37437 obj_retry.go:541] Creating *v1.Pod openshift-console/downloads-6967878986-76phj took: 31.692µs
I0719 01:46:01.802541   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/odf-console-b7ccd85c5-84cnv in node 00-50-56-8a-f2-5d
I0719 01:46:01.802543   37437 default_network_controller.go:655] Recording add event on pod openshift-operator-lifecycle-manager/collect-profiles-28689195-w9664
I0719 01:46:01.802481   37437 obj_retry.go:541] Creating *v1.Pod openshift-multus/network-metrics-daemon-fslb2 took: 22.917µs
I0719 01:46:01.802550   37437 default_network_controller.go:699] Recording success event on pod openshift-multus/network-metrics-daemon-fslb2
I0719 01:46:01.802544   37437 default_network_controller.go:699] Recording success event on pod openshift-console/downloads-6967878986-76phj
I0719 01:46:01.802559   37437 default_network_controller.go:655] Recording add event on pod openshift-cluster-node-tuning-operator/tuned-5pn2c
I0719 01:46:01.802564   37437 default_network_controller.go:655] Recording add event on pod openshift-route-controller-manager/route-controller-manager-676cdfdbc8-gt4t6
I0719 01:46:01.802566   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-cluster-node-tuning-operator/tuned-5pn2c
I0719 01:46:01.802570   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-route-controller-manager/route-controller-manager-676cdfdbc8-gt4t6
I0719 01:46:01.802572   37437 ovn.go:138] Ensuring zone remote for Pod openshift-cluster-node-tuning-operator/tuned-5pn2c in node 00-50-56-8a-f2-5d
I0719 01:46:01.802494   37437 default_network_controller.go:655] Recording add event on pod openshift-network-diagnostics/network-check-target-h9cbr
I0719 01:46:01.802577   37437 obj_retry.go:541] Creating *v1.Pod openshift-cluster-node-tuning-operator/tuned-5pn2c took: 5.837µs
I0719 01:46:01.802550   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-operator-lifecycle-manager/collect-profiles-28689195-w9664
I0719 01:46:01.802528   37437 obj_retry.go:541] Creating *v1.Pod openshift-multus/network-metrics-daemon-7ttpg took: 2.421112ms
I0719 01:46:01.802588   37437 default_network_controller.go:699] Recording success event on pod openshift-multus/network-metrics-daemon-7ttpg
I0719 01:46:01.802589   37437 obj_retry.go:459] Detected object openshift-operator-lifecycle-manager/collect-profiles-28689195-w9664 of type *v1.Pod in terminal state (e.g. completed) during add event: will remove it
I0719 01:46:01.802586   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-network-diagnostics/network-check-target-h9cbr
I0719 01:46:01.802597   37437 default_network_controller.go:655] Recording add event on pod openshift-machine-config-operator/machine-config-daemon-r8bgv
I0719 01:46:01.802603   37437 ovn.go:138] Ensuring zone remote for Pod openshift-network-diagnostics/network-check-target-h9cbr in node 00-50-56-8a-f2-5d
I0719 01:46:01.800594   37437 obj_retry.go:541] Creating *v1.Pod openshift-authentication/oauth-openshift-7c9d9dfc8c-lxcsb took: 2.494309ms
I0719 01:46:01.802611   37437 default_network_controller.go:699] Recording success event on pod openshift-authentication/oauth-openshift-7c9d9dfc8c-lxcsb
I0719 01:46:01.802616   37437 default_network_controller.go:655] Recording add event on pod openshift-dns/dns-default-qzrlq
I0719 01:46:01.802623   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-dns/dns-default-qzrlq
I0719 01:46:01.802623   37437 obj_retry.go:541] Creating *v1.Pod openshift-network-diagnostics/network-check-target-h9cbr took: 19.907µs
I0719 01:46:01.802632   37437 default_network_controller.go:699] Recording success event on pod openshift-network-diagnostics/network-check-target-h9cbr
I0719 01:46:01.802256   37437 default_network_controller.go:655] Recording add event on pod openshift-ingress-operator/ingress-operator-5cc96867f4-pdgdd
I0719 01:46:01.802639   37437 default_network_controller.go:655] Recording add event on pod openshift-controller-manager/controller-manager-5c7f9f9d47-kxpdr
I0719 01:46:01.802642   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-ingress-operator/ingress-operator-5cc96867f4-pdgdd
I0719 01:46:01.802645   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-controller-manager/controller-manager-5c7f9f9d47-kxpdr
I0719 01:46:01.802648   37437 ovn.go:138] Ensuring zone remote for Pod openshift-ingress-operator/ingress-operator-5cc96867f4-pdgdd in node 00-50-56-8a-5c-ec
I0719 01:46:01.802650   37437 obj_retry.go:541] Creating *v1.Pod openshift-controller-manager/controller-manager-5c7f9f9d47-kxpdr took: 142ns
I0719 01:46:01.802655   37437 default_network_controller.go:699] Recording success event on pod openshift-controller-manager/controller-manager-5c7f9f9d47-kxpdr
I0719 01:46:01.802660   37437 default_network_controller.go:655] Recording add event on pod openshift-etcd/etcd-guard-00-50-56-8a-39-a0
I0719 01:46:01.802569   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/odf-console-b7ccd85c5-84cnv took: 26.756µs
I0719 01:46:01.802668   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/odf-console-b7ccd85c5-84cnv
I0719 01:46:01.802671   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-etcd/etcd-guard-00-50-56-8a-39-a0
I0719 01:46:01.802678   37437 ovn.go:138] Ensuring zone remote for Pod openshift-etcd/etcd-guard-00-50-56-8a-39-a0 in node 00-50-56-8a-39-a0
I0719 01:46:01.802680   37437 default_network_controller.go:655] Recording add event on pod openshift-kni-infra/coredns-00-50-56-8a-fb-ea
I0719 01:46:01.802681   37437 obj_retry.go:541] Creating *v1.Pod openshift-ingress-operator/ingress-operator-5cc96867f4-pdgdd took: 33.401µs
I0719 01:46:01.802686   37437 default_network_controller.go:699] Recording success event on pod openshift-ingress-operator/ingress-operator-5cc96867f4-pdgdd
I0719 01:46:01.802603   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-machine-config-operator/machine-config-daemon-r8bgv
I0719 01:46:01.802691   37437 default_network_controller.go:655] Recording add event on pod openshift-monitoring/cluster-monitoring-operator-b4b4bcf9f-d4xhg
I0719 01:46:01.802696   37437 ovn.go:138] Ensuring zone remote for Pod openshift-machine-config-operator/machine-config-daemon-r8bgv in node 00-50-56-8a-39-a0
I0719 01:46:01.802629   37437 ovn.go:134] Ensuring zone local for Pod openshift-dns/dns-default-qzrlq in node 00-50-56-8a-fb-ea
I0719 01:46:01.802699   37437 address_set.go:613] (575fa52c-db50-4745-88b9-948435e2dbe8/default-network-controller:Namespace:openshift-operator-lifecycle-manager:v4/a1482332553631220387) deleting addresses [10.128.2.49] from address set
I0719 01:46:01.802702   37437 obj_retry.go:541] Creating *v1.Pod openshift-machine-config-operator/machine-config-daemon-r8bgv took: 7.554µs
I0719 01:46:01.802708   37437 default_network_controller.go:699] Recording success event on pod openshift-machine-config-operator/machine-config-daemon-r8bgv
I0719 01:46:01.802711   37437 base_network_controller_pods.go:476] [default/openshift-dns/dns-default-qzrlq] creating logical port openshift-dns_dns-default-qzrlq for pod on switch 00-50-56-8a-fb-ea
I0719 01:46:01.802713   37437 default_network_controller.go:655] Recording add event on pod openshift-insights/insights-operator-586b65d57b-7rk2w
I0719 01:46:01.802722   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-insights/insights-operator-586b65d57b-7rk2w
I0719 01:46:01.802728   37437 ovn.go:138] Ensuring zone remote for Pod openshift-insights/insights-operator-586b65d57b-7rk2w in node 00-50-56-8a-5c-ec
I0719 01:46:01.802548   37437 model_client.go:381] Update operations generated as: [{Op:update Table:NAT Row:map[external_ip:10.10.25.235 logical_ip:10.130.0.17 options:{GoMap:map[stateless:false]} type:snat] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {d2b8e06f-1a01-4f37-9d33-2ff359aa53e6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.802757   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Address_Set Row:map[] Rows:[] Columns:[] Mutations:[{Column:addresses Mutator:delete Value:{GoSet:[10.128.2.49]}}] Timeout:<nil> Where:[where column _uuid == {575fa52c-db50-4745-88b9-948435e2dbe8}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.802792   37437 transact.go:42] Configuring OVN: [{Op:mutate Table:Address_Set Row:map[] Rows:[] Columns:[] Mutations:[{Column:addresses Mutator:delete Value:{GoSet:[10.128.2.49]}}] Timeout:<nil> Where:[where column _uuid == {575fa52c-db50-4745-88b9-948435e2dbe8}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.802686   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kni-infra/coredns-00-50-56-8a-fb-ea
I0719 01:46:01.802845   37437 ovn.go:134] Ensuring zone local for Pod openshift-kni-infra/coredns-00-50-56-8a-fb-ea in node 00-50-56-8a-fb-ea
I0719 01:46:01.802851   37437 obj_retry.go:541] Creating *v1.Pod openshift-kni-infra/coredns-00-50-56-8a-fb-ea took: 10.603µs
I0719 01:46:01.802857   37437 default_network_controller.go:699] Recording success event on pod openshift-kni-infra/coredns-00-50-56-8a-fb-ea
I0719 01:46:01.802863   37437 default_network_controller.go:655] Recording add event on pod openshift-multus/multus-2nb4x
I0719 01:46:01.802872   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-multus/multus-2nb4x
I0719 01:46:01.802879   37437 ovn.go:138] Ensuring zone remote for Pod openshift-multus/multus-2nb4x in node 00-50-56-8a-5c-ec
I0719 01:46:01.801466   37437 obj_retry.go:541] Creating *v1.Pod openshift-ovn-kubernetes/ovnkube-node-mqh7r took: 5.682µs
I0719 01:46:01.801693   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/csi-rbdplugin-xkw8r
I0719 01:46:01.802582   37437 default_network_controller.go:699] Recording success event on pod openshift-cluster-node-tuning-operator/tuned-5pn2c
I0719 01:46:01.802896   37437 default_network_controller.go:655] Recording add event on pod openshift-cloud-controller-manager-operator/cluster-cloud-controller-manager-operator-7f55545d59-r8j8z
I0719 01:46:01.801486   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-f2-5d
I0719 01:46:01.802904   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-cloud-controller-manager-operator/cluster-cloud-controller-manager-operator-7f55545d59-r8j8z
I0719 01:46:01.802907   37437 default_network_controller.go:699] Recording success event on pod openshift-ovn-kubernetes/ovnkube-node-mqh7r
I0719 01:46:01.802911   37437 ovn.go:138] Ensuring zone remote for Pod openshift-cloud-controller-manager-operator/cluster-cloud-controller-manager-operator-7f55545d59-r8j8z in node 00-50-56-8a-39-a0
I0719 01:46:01.802914   37437 default_network_controller.go:655] Recording add event on pod openshift-kube-scheduler/revision-pruner-6-00-50-56-8a-5c-ec
I0719 01:46:01.802916   37437 obj_retry.go:541] Creating *v1.Pod openshift-cloud-controller-manager-operator/cluster-cloud-controller-manager-operator-7f55545d59-r8j8z took: 5.912µs
I0719 01:46:01.802896   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/csi-rbdplugin-xkw8r
I0719 01:46:01.802921   37437 default_network_controller.go:699] Recording success event on pod openshift-cloud-controller-manager-operator/cluster-cloud-controller-manager-operator-7f55545d59-r8j8z
I0719 01:46:01.802921   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kube-scheduler/revision-pruner-6-00-50-56-8a-5c-ec
I0719 01:46:01.802926   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/rook-ceph-crashcollector-00-50-56-8a-e1-e7-6c5dcb6f44-8z5np
I0719 01:46:01.802693   37437 obj_retry.go:541] Creating *v1.Pod openshift-etcd/etcd-guard-00-50-56-8a-39-a0 took: 16.097µs
I0719 01:46:01.802933   37437 obj_retry.go:459] Detected object openshift-kube-scheduler/revision-pruner-6-00-50-56-8a-5c-ec of type *v1.Pod in terminal state (e.g. completed) during add event: will remove it
I0719 01:46:01.802937   37437 default_network_controller.go:699] Recording success event on pod openshift-etcd/etcd-guard-00-50-56-8a-39-a0
I0719 01:46:01.802910   37437 ovn.go:138] Ensuring zone remote for Pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-f2-5d in node 00-50-56-8a-f2-5d
I0719 01:46:01.802944   37437 default_network_controller.go:655] Recording add event on pod openshift-multus/multus-additional-cni-plugins-qdrk9
I0719 01:46:01.802951   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-multus/multus-additional-cni-plugins-qdrk9
I0719 01:46:01.802948   37437 obj_retry.go:541] Creating *v1.Pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-f2-5d took: 40.563µs
I0719 01:46:01.802958   37437 ovn.go:138] Ensuring zone remote for Pod openshift-multus/multus-additional-cni-plugins-qdrk9 in node 00-50-56-8a-5c-ec
I0719 01:46:01.802536   37437 default_network_controller.go:699] Recording success event on pod openshift-marketplace/redhat-operators-mm6k4
I0719 01:46:01.802963   37437 obj_retry.go:541] Creating *v1.Pod openshift-multus/multus-additional-cni-plugins-qdrk9 took: 5.901µs
I0719 01:46:01.802967   37437 default_network_controller.go:699] Recording success event on pod openshift-multus/multus-additional-cni-plugins-qdrk9
I0719 01:46:01.802926   37437 ovn.go:134] Ensuring zone local for Pod openshift-storage/csi-rbdplugin-xkw8r in node 00-50-56-8a-fb-ea
I0719 01:46:01.802977   37437 default_network_controller.go:655] Recording add event on pod openshift-network-diagnostics/network-check-target-gc5jl
I0719 01:46:01.802990   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-network-diagnostics/network-check-target-gc5jl
I0719 01:46:01.802993   37437 obj_retry.go:541] Creating *v1.Pod openshift-multus/multus-2nb4x took: 113.869µs
I0719 01:46:01.802576   37437 obj_retry.go:541] Creating *v1.Pod openshift-route-controller-manager/route-controller-manager-676cdfdbc8-gt4t6 took: 164ns
I0719 01:46:01.803001   37437 default_network_controller.go:699] Recording success event on pod openshift-multus/multus-2nb4x
I0719 01:46:01.803003   37437 default_network_controller.go:699] Recording success event on pod openshift-route-controller-manager/route-controller-manager-676cdfdbc8-gt4t6
I0719 01:46:01.802938   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/rook-ceph-crashcollector-00-50-56-8a-e1-e7-6c5dcb6f44-8z5np
I0719 01:46:01.803009   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/ocs-client-operator-controller-manager-846f549988-v288f
I0719 01:46:01.803007   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/csi-cephfsplugin-provisioner-585f89d895-2b4wk
I0719 01:46:01.802959   37437 default_network_controller.go:699] Recording success event on pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-f2-5d
I0719 01:46:01.803020   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/ocs-client-operator-controller-manager-846f549988-v288f
I0719 01:46:01.802996   37437 ovn.go:138] Ensuring zone remote for Pod openshift-network-diagnostics/network-check-target-gc5jl in node 00-50-56-8a-44-52
I0719 01:46:01.803032   37437 default_network_controller.go:655] Recording add event on pod openshift-network-diagnostics/network-check-source-b89b7bb96-lpzlv
I0719 01:46:01.803037   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/csi-cephfsplugin-provisioner-585f89d895-2b4wk
I0719 01:46:01.803039   37437 address_set.go:613] (ae1e6050-3670-4f5e-978c-ca1e35ef7b65/default-network-controller:Namespace:openshift-kube-scheduler:v4/a15634036902741400949) deleting addresses [10.129.2.6] from address set
I0719 01:46:01.803054   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/csi-cephfsplugin-provisioner-585f89d895-2b4wk in node 00-50-56-8a-e1-e7
I0719 01:46:01.803098   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/csi-cephfsplugin-provisioner-585f89d895-2b4wk took: 47.193µs
I0719 01:46:01.802751   37437 obj_retry.go:541] Creating *v1.Pod openshift-insights/insights-operator-586b65d57b-7rk2w took: 23.703µs
I0719 01:46:01.803107   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/csi-cephfsplugin-provisioner-585f89d895-2b4wk
I0719 01:46:01.803110   37437 default_network_controller.go:699] Recording success event on pod openshift-insights/insights-operator-586b65d57b-7rk2w
I0719 01:46:01.803115   37437 default_network_controller.go:655] Recording add event on pod openshift-kube-scheduler/openshift-kube-scheduler-guard-00-50-56-8a-39-a0
I0719 01:46:01.802995   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/csi-rbdplugin-xkw8r took: 54.925µs
I0719 01:46:01.803107   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Address_Set Row:map[] Rows:[] Columns:[] Mutations:[{Column:addresses Mutator:delete Value:{GoSet:[10.129.2.6]}}] Timeout:<nil> Where:[where column _uuid == {ae1e6050-3670-4f5e-978c-ca1e35ef7b65}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.803123   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kube-scheduler/openshift-kube-scheduler-guard-00-50-56-8a-39-a0
I0719 01:46:01.803129   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/csi-rbdplugin-xkw8r
I0719 01:46:01.803135   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kube-scheduler/openshift-kube-scheduler-guard-00-50-56-8a-39-a0 in node 00-50-56-8a-39-a0
I0719 01:46:01.803138   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/rook-ceph-osd-1-6db96b64cc-nw82d
I0719 01:46:01.803134   37437 transact.go:42] Configuring OVN: [{Op:mutate Table:Address_Set Row:map[] Rows:[] Columns:[] Mutations:[{Column:addresses Mutator:delete Value:{GoSet:[10.129.2.6]}}] Timeout:<nil> Where:[where column _uuid == {ae1e6050-3670-4f5e-978c-ca1e35ef7b65}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.803152   37437 obj_retry.go:541] Creating *v1.Pod openshift-kube-scheduler/openshift-kube-scheduler-guard-00-50-56-8a-39-a0 took: 18.571µs
I0719 01:46:01.802967   37437 default_network_controller.go:655] Recording add event on pod openshift-kube-controller-manager/kube-controller-manager-guard-00-50-56-8a-44-52
I0719 01:46:01.803101   37437 obj_retry.go:541] Creating *v1.Pod openshift-network-diagnostics/network-check-target-gc5jl took: 104.589µs
I0719 01:46:01.803163   37437 default_network_controller.go:699] Recording success event on pod openshift-kube-scheduler/openshift-kube-scheduler-guard-00-50-56-8a-39-a0
I0719 01:46:01.803165   37437 default_network_controller.go:655] Recording add event on pod openshift-monitoring/metrics-server-7d47f4cbc-dqrxk
I0719 01:46:01.803169   37437 default_network_controller.go:655] Recording add event on pod openshift-multus/multus-sv782
I0719 01:46:01.803168   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kube-controller-manager/kube-controller-manager-guard-00-50-56-8a-44-52
I0719 01:46:01.803178   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-multus/multus-sv782
I0719 01:46:01.803181   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kube-controller-manager/kube-controller-manager-guard-00-50-56-8a-44-52 in node 00-50-56-8a-44-52
I0719 01:46:01.803186   37437 ovn.go:134] Ensuring zone local for Pod openshift-multus/multus-sv782 in node 00-50-56-8a-fb-ea
I0719 01:46:01.803191   37437 obj_retry.go:541] Creating *v1.Pod openshift-multus/multus-sv782 took: 6.61µs
I0719 01:46:01.803166   37437 default_network_controller.go:699] Recording success event on pod openshift-network-diagnostics/network-check-target-gc5jl
I0719 01:46:01.803188   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/rook-ceph-exporter-00-50-56-8a-f2-5d-785d485f5d-v5k84
I0719 01:46:01.803203   37437 default_network_controller.go:655] Recording add event on pod openshift-cluster-version/cluster-version-operator-78b5d9c79d-znx2p
I0719 01:46:01.803210   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-cluster-version/cluster-version-operator-78b5d9c79d-znx2p
I0719 01:46:01.801175   37437 obj_retry.go:541] Creating *v1.Pod openshift-multus/network-metrics-daemon-bqt8s took: 92.796µs
I0719 01:46:01.803217   37437 ovn.go:138] Ensuring zone remote for Pod openshift-cluster-version/cluster-version-operator-78b5d9c79d-znx2p in node 00-50-56-8a-39-a0
I0719 01:46:01.803220   37437 default_network_controller.go:699] Recording success event on pod openshift-multus/network-metrics-daemon-bqt8s
I0719 01:46:01.803222   37437 obj_retry.go:541] Creating *v1.Pod openshift-cluster-version/cluster-version-operator-78b5d9c79d-znx2p took: 6.313µs
I0719 01:46:01.803226   37437 default_network_controller.go:655] Recording add event on pod openshift-machine-config-operator/machine-config-daemon-kgwdc
I0719 01:46:01.803232   37437 default_network_controller.go:699] Recording success event on pod openshift-cluster-version/cluster-version-operator-78b5d9c79d-znx2p
I0719 01:46:01.803026   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/ocs-client-operator-controller-manager-846f549988-v288f in node 00-50-56-8a-e1-e7
I0719 01:46:01.803210   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/rook-ceph-exporter-00-50-56-8a-f2-5d-785d485f5d-v5k84
I0719 01:46:01.803246   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/rook-ceph-exporter-00-50-56-8a-f2-5d-785d485f5d-v5k84 in node 00-50-56-8a-f2-5d
I0719 01:46:01.803257   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/ocs-client-operator-controller-manager-846f549988-v288f took: 231.561µs
I0719 01:46:01.803179   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-monitoring/metrics-server-7d47f4cbc-dqrxk
I0719 01:46:01.803263   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/ocs-client-operator-controller-manager-846f549988-v288f
I0719 01:46:01.803271   37437 ovn.go:138] Ensuring zone remote for Pod openshift-monitoring/metrics-server-7d47f4cbc-dqrxk in node 00-50-56-8a-f2-5d
I0719 01:46:01.803274   37437 default_network_controller.go:655] Recording add event on pod openshift-kni-infra/keepalived-00-50-56-8a-5c-ec
I0719 01:46:01.803276   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/rook-ceph-exporter-00-50-56-8a-f2-5d-785d485f5d-v5k84 took: 30.768µs
I0719 01:46:01.803283   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kni-infra/keepalived-00-50-56-8a-5c-ec
I0719 01:46:01.803285   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/rook-ceph-exporter-00-50-56-8a-f2-5d-785d485f5d-v5k84
I0719 01:46:01.803294   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kni-infra/keepalived-00-50-56-8a-5c-ec in node 00-50-56-8a-5c-ec
I0719 01:46:01.803232   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-machine-config-operator/machine-config-daemon-kgwdc
I0719 01:46:01.803303   37437 obj_retry.go:541] Creating *v1.Pod openshift-kni-infra/keepalived-00-50-56-8a-5c-ec took: 11.479µs
I0719 01:46:01.803306   37437 ovn.go:138] Ensuring zone remote for Pod openshift-machine-config-operator/machine-config-daemon-kgwdc in node 00-50-56-8a-e1-e7
I0719 01:46:01.803116   37437 default_network_controller.go:655] Recording add event on pod openshift-ovn-kubernetes/ovnkube-node-7pmvf
I0719 01:46:01.803312   37437 obj_retry.go:541] Creating *v1.Pod openshift-machine-config-operator/machine-config-daemon-kgwdc took: 8.392µs
I0719 01:46:01.803146   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/rook-ceph-osd-1-6db96b64cc-nw82d
I0719 01:46:01.803317   37437 default_network_controller.go:699] Recording success event on pod openshift-machine-config-operator/machine-config-daemon-kgwdc
I0719 01:46:01.803319   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-ovn-kubernetes/ovnkube-node-7pmvf
I0719 01:46:01.803327   37437 ovn.go:138] Ensuring zone remote for Pod openshift-ovn-kubernetes/ovnkube-node-7pmvf in node 00-50-56-8a-f2-5d
I0719 01:46:01.803296   37437 obj_retry.go:541] Creating *v1.Pod openshift-monitoring/metrics-server-7d47f4cbc-dqrxk took: 27.07µs
I0719 01:46:01.803332   37437 obj_retry.go:541] Creating *v1.Pod openshift-ovn-kubernetes/ovnkube-node-7pmvf took: 6.273µs
I0719 01:46:01.803333   37437 default_network_controller.go:655] Recording add event on pod openshift-multus/network-metrics-daemon-t4g2p
I0719 01:46:01.803335   37437 default_network_controller.go:699] Recording success event on pod openshift-monitoring/metrics-server-7d47f4cbc-dqrxk
I0719 01:46:01.803346   37437 default_network_controller.go:699] Recording success event on pod openshift-ovn-kubernetes/ovnkube-node-7pmvf
I0719 01:46:01.803043   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-network-diagnostics/network-check-source-b89b7bb96-lpzlv
I0719 01:46:01.803352   37437 default_network_controller.go:655] Recording add event on pod openshift-kube-apiserver/revision-pruner-8-00-50-56-8a-5c-ec
I0719 01:46:01.803334   37437 default_network_controller.go:655] Recording add event on pod openshift-dns/node-resolver-djq2g
I0719 01:46:01.803359   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kube-apiserver/revision-pruner-8-00-50-56-8a-5c-ec
I0719 01:46:01.803365   37437 ovn.go:138] Ensuring zone remote for Pod openshift-network-diagnostics/network-check-source-b89b7bb96-lpzlv in node 00-50-56-8a-e1-e7
I0719 01:46:01.803369   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-dns/node-resolver-djq2g
I0719 01:46:01.803196   37437 default_network_controller.go:699] Recording success event on pod openshift-multus/multus-sv782
I0719 01:46:01.803377   37437 ovn.go:138] Ensuring zone remote for Pod openshift-dns/node-resolver-djq2g in node 00-50-56-8a-44-52
I0719 01:46:01.803382   37437 obj_retry.go:541] Creating *v1.Pod openshift-dns/node-resolver-djq2g took: 6.675µs
I0719 01:46:01.803327   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/rook-ceph-osd-1-6db96b64cc-nw82d in node 00-50-56-8a-f2-5d
I0719 01:46:01.803388   37437 default_network_controller.go:699] Recording success event on pod openshift-dns/node-resolver-djq2g
I0719 01:46:01.803394   37437 default_network_controller.go:655] Recording add event on pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-39-a0
I0719 01:46:01.803400   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-39-a0
I0719 01:46:01.803379   37437 default_network_controller.go:655] Recording add event on pod openshift-console-operator/console-conversion-webhook-664b4df6f5-nq9pd
I0719 01:46:01.803365   37437 obj_retry.go:459] Detected object openshift-kube-apiserver/revision-pruner-8-00-50-56-8a-5c-ec of type *v1.Pod in terminal state (e.g. completed) during add event: will remove it
I0719 01:46:01.803407   37437 ovn.go:138] Ensuring zone remote for Pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-39-a0 in node 00-50-56-8a-39-a0
I0719 01:46:01.803416   37437 obj_retry.go:541] Creating *v1.Pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-39-a0 took: 9.804µs
I0719 01:46:01.803417   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-console-operator/console-conversion-webhook-664b4df6f5-nq9pd
I0719 01:46:01.802699   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-monitoring/cluster-monitoring-operator-b4b4bcf9f-d4xhg
I0719 01:46:01.803429   37437 ovn.go:138] Ensuring zone remote for Pod openshift-console-operator/console-conversion-webhook-664b4df6f5-nq9pd in node 00-50-56-8a-39-a0
I0719 01:46:01.803434   37437 ovn.go:138] Ensuring zone remote for Pod openshift-monitoring/cluster-monitoring-operator-b4b4bcf9f-d4xhg in node 00-50-56-8a-5c-ec
I0719 01:46:01.803453   37437 obj_retry.go:541] Creating *v1.Pod openshift-monitoring/cluster-monitoring-operator-b4b4bcf9f-d4xhg took: 19.532µs
I0719 01:46:01.803419   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/rook-ceph-osd-1-6db96b64cc-nw82d took: 92.969µs
I0719 01:46:01.803463   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/rook-ceph-osd-1-6db96b64cc-nw82d
I0719 01:46:01.803456   37437 obj_retry.go:541] Creating *v1.Pod openshift-console-operator/console-conversion-webhook-664b4df6f5-nq9pd took: 28.309µs
I0719 01:46:01.803470   37437 default_network_controller.go:699] Recording success event on pod openshift-console-operator/console-conversion-webhook-664b4df6f5-nq9pd
I0719 01:46:01.803349   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-multus/network-metrics-daemon-t4g2p
I0719 01:46:01.803476   37437 default_network_controller.go:655] Recording add event on pod openshift-operator-lifecycle-manager/collect-profiles-28689210-mbs94
I0719 01:46:01.803483   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-operator-lifecycle-manager/collect-profiles-28689210-mbs94
I0719 01:46:01.803464   37437 default_network_controller.go:699] Recording success event on pod openshift-monitoring/cluster-monitoring-operator-b4b4bcf9f-d4xhg
I0719 01:46:01.803489   37437 obj_retry.go:459] Detected object openshift-operator-lifecycle-manager/collect-profiles-28689210-mbs94 of type *v1.Pod in terminal state (e.g. completed) during add event: will remove it
I0719 01:46:01.803238   37437 default_network_controller.go:655] Recording add event on pod openshift-network-diagnostics/network-check-target-jhhzw
I0719 01:46:01.803470   37437 default_network_controller.go:655] Recording add event on pod openshift-kube-apiserver/kube-apiserver-00-50-56-8a-39-a0
I0719 01:46:01.803260   37437 obj_retry.go:541] Creating *v1.Pod openshift-kube-controller-manager/kube-controller-manager-guard-00-50-56-8a-44-52 took: 81.433µs
I0719 01:46:01.803500   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-network-diagnostics/network-check-target-jhhzw
I0719 01:46:01.803504   37437 default_network_controller.go:699] Recording success event on pod openshift-kube-controller-manager/kube-controller-manager-guard-00-50-56-8a-44-52
I0719 01:46:01.803507   37437 ovn.go:138] Ensuring zone remote for Pod openshift-network-diagnostics/network-check-target-jhhzw in node 00-50-56-8a-e1-e7
I0719 01:46:01.803309   37437 default_network_controller.go:699] Recording success event on pod openshift-kni-infra/keepalived-00-50-56-8a-5c-ec
I0719 01:46:01.803516   37437 default_network_controller.go:655] Recording add event on pod openshift-kube-storage-version-migrator/migrator-7fc5dd675b-tfjhl
I0719 01:46:01.803420   37437 default_network_controller.go:699] Recording success event on pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-39-a0
I0719 01:46:01.803522   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kube-storage-version-migrator/migrator-7fc5dd675b-tfjhl
I0719 01:46:01.803525   37437 default_network_controller.go:655] Recording add event on pod openshift-machine-config-operator/machine-config-daemon-p677g
I0719 01:46:01.803529   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kube-storage-version-migrator/migrator-7fc5dd675b-tfjhl in node 00-50-56-8a-5c-ec
I0719 01:46:01.803509   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kube-apiserver/kube-apiserver-00-50-56-8a-39-a0
I0719 01:46:01.803535   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-machine-config-operator/machine-config-daemon-p677g
I0719 01:46:01.803539   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kube-apiserver/kube-apiserver-00-50-56-8a-39-a0 in node 00-50-56-8a-39-a0
I0719 01:46:01.803543   37437 ovn.go:138] Ensuring zone remote for Pod openshift-machine-config-operator/machine-config-daemon-p677g in node 00-50-56-8a-44-52
I0719 01:46:01.803544   37437 obj_retry.go:541] Creating *v1.Pod openshift-kube-apiserver/kube-apiserver-00-50-56-8a-39-a0 took: 6.759µs
I0719 01:46:01.803548   37437 obj_retry.go:541] Creating *v1.Pod openshift-machine-config-operator/machine-config-daemon-p677g took: 6.788µs
I0719 01:46:01.803553   37437 default_network_controller.go:699] Recording success event on pod openshift-machine-config-operator/machine-config-daemon-p677g
I0719 01:46:01.803554   37437 obj_retry.go:541] Creating *v1.Pod openshift-kube-storage-version-migrator/migrator-7fc5dd675b-tfjhl took: 24.18µs
I0719 01:46:01.803516   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/csi-rbdplugin-provisioner-5dcc45fbf4-v5l2c
I0719 01:46:01.803563   37437 default_network_controller.go:655] Recording add event on pod openshift-operator-lifecycle-manager/package-server-manager-74bbc7c476-4555r
I0719 01:46:01.803549   37437 default_network_controller.go:699] Recording success event on pod openshift-kube-apiserver/kube-apiserver-00-50-56-8a-39-a0
I0719 01:46:01.803573   37437 default_network_controller.go:655] Recording add event on pod openshift-operator-lifecycle-manager/packageserver-6bf7d58455-k8qkk
I0719 01:46:01.803575   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/csi-rbdplugin-provisioner-5dcc45fbf4-v5l2c
I0719 01:46:01.803578   37437 address_set.go:613] (575fa52c-db50-4745-88b9-948435e2dbe8/default-network-controller:Namespace:openshift-operator-lifecycle-manager:v4/a1482332553631220387) deleting addresses [10.128.2.50] from address set
I0719 01:46:01.803348   37437 default_network_controller.go:655] Recording add event on pod openshift-image-registry/node-ca-sq7qk
I0719 01:46:01.803528   37437 obj_retry.go:541] Creating *v1.Pod openshift-network-diagnostics/network-check-target-jhhzw took: 22.119µs
I0719 01:46:01.803589   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-image-registry/node-ca-sq7qk
I0719 01:46:01.803494   37437 default_network_controller.go:655] Recording add event on pod openshift-kube-apiserver/kube-apiserver-guard-00-50-56-8a-44-52
I0719 01:46:01.803599   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kube-apiserver/kube-apiserver-guard-00-50-56-8a-44-52
I0719 01:46:01.803601   37437 ovn.go:138] Ensuring zone remote for Pod openshift-image-registry/node-ca-sq7qk in node 00-50-56-8a-5c-ec
I0719 01:46:01.803605   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kube-apiserver/kube-apiserver-guard-00-50-56-8a-44-52 in node 00-50-56-8a-44-52
I0719 01:46:01.803591   37437 default_network_controller.go:699] Recording success event on pod openshift-network-diagnostics/network-check-target-jhhzw
I0719 01:46:01.803617   37437 default_network_controller.go:655] Recording add event on pod openshift-machine-api/ironic-proxy-sn8n9
I0719 01:46:01.803623   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-machine-api/ironic-proxy-sn8n9
I0719 01:46:01.803492   37437 address_set.go:613] (9269757a-340c-45bf-828d-361c80cb0226/default-network-controller:Namespace:openshift-kube-apiserver:v4/a4531626005796422843) deleting addresses [10.129.2.5] from address set
I0719 01:46:01.803624   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Address_Set Row:map[] Rows:[] Columns:[] Mutations:[{Column:addresses Mutator:delete Value:{GoSet:[10.128.2.50]}}] Timeout:<nil> Where:[where column _uuid == {575fa52c-db50-4745-88b9-948435e2dbe8}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.803402   37437 obj_retry.go:541] Creating *v1.Pod openshift-network-diagnostics/network-check-source-b89b7bb96-lpzlv took: 40.427µs
I0719 01:46:01.803646   37437 default_network_controller.go:699] Recording success event on pod openshift-network-diagnostics/network-check-source-b89b7bb96-lpzlv
I0719 01:46:01.803652   37437 default_network_controller.go:655] Recording add event on pod openshift-marketplace/marketplace-operator-59c7f5b7bd-8pd2c
I0719 01:46:01.803650   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-operator-lifecycle-manager/package-server-manager-74bbc7c476-4555r
I0719 01:46:01.803579   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-operator-lifecycle-manager/packageserver-6bf7d58455-k8qkk
I0719 01:46:01.803660   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-marketplace/marketplace-operator-59c7f5b7bd-8pd2c
I0719 01:46:01.803663   37437 ovn.go:138] Ensuring zone remote for Pod openshift-operator-lifecycle-manager/package-server-manager-74bbc7c476-4555r in node 00-50-56-8a-39-a0
I0719 01:46:01.803668   37437 ovn.go:138] Ensuring zone remote for Pod openshift-marketplace/marketplace-operator-59c7f5b7bd-8pd2c in node 00-50-56-8a-39-a0
I0719 01:46:01.803666   37437 ovn.go:138] Ensuring zone remote for Pod openshift-operator-lifecycle-manager/packageserver-6bf7d58455-k8qkk in node 00-50-56-8a-5c-ec
I0719 01:46:01.803664   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Address_Set Row:map[] Rows:[] Columns:[] Mutations:[{Column:addresses Mutator:delete Value:{GoSet:[10.129.2.5]}}] Timeout:<nil> Where:[where column _uuid == {9269757a-340c-45bf-828d-361c80cb0226}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.803685   37437 obj_retry.go:541] Creating *v1.Pod openshift-operator-lifecycle-manager/package-server-manager-74bbc7c476-4555r took: 23.282µs
I0719 01:46:01.803016   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/rook-ceph-crashcollector-00-50-56-8a-e1-e7-6c5dcb6f44-8z5np in node 00-50-56-8a-e1-e7
I0719 01:46:01.803692   37437 obj_retry.go:541] Creating *v1.Pod openshift-marketplace/marketplace-operator-59c7f5b7bd-8pd2c took: 24.507µs
I0719 01:46:01.803694   37437 default_network_controller.go:699] Recording success event on pod openshift-operator-lifecycle-manager/package-server-manager-74bbc7c476-4555r
I0719 01:46:01.803698   37437 default_network_controller.go:699] Recording success event on pod openshift-marketplace/marketplace-operator-59c7f5b7bd-8pd2c
I0719 01:46:01.803703   37437 default_network_controller.go:655] Recording add event on pod openshift-service-ca-operator/service-ca-operator-86c8d4bbfd-w2qxx
I0719 01:46:01.803298   37437 default_network_controller.go:655] Recording add event on pod openshift-oauth-apiserver/apiserver-86f656c4dd-x7cqj
I0719 01:46:01.803706   37437 default_network_controller.go:655] Recording add event on pod openshift-cluster-storage-operator/csi-snapshot-controller-794ff44f88-5jz8j
I0719 01:46:01.803710   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-service-ca-operator/service-ca-operator-86c8d4bbfd-w2qxx
I0719 01:46:01.803713   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/rook-ceph-crashcollector-00-50-56-8a-e1-e7-6c5dcb6f44-8z5np took: 699.321µs
I0719 01:46:01.803630   37437 ovn.go:138] Ensuring zone remote for Pod openshift-machine-api/ironic-proxy-sn8n9 in node 00-50-56-8a-39-a0
I0719 01:46:01.803721   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/rook-ceph-crashcollector-00-50-56-8a-e1-e7-6c5dcb6f44-8z5np
I0719 01:46:01.803684   37437 obj_retry.go:541] Creating *v1.Pod openshift-kube-apiserver/kube-apiserver-guard-00-50-56-8a-44-52 took: 79.478µs
I0719 01:46:01.803687   37437 obj_retry.go:541] Creating *v1.Pod openshift-operator-lifecycle-manager/packageserver-6bf7d58455-k8qkk took: 21.928µs
I0719 01:46:01.803745   37437 default_network_controller.go:655] Recording add event on pod openshift-kube-scheduler/openshift-kube-scheduler-guard-00-50-56-8a-44-52
I0719 01:46:01.803606   37437 obj_retry.go:541] Creating *v1.Pod openshift-image-registry/node-ca-sq7qk took: 6.164µs
I0719 01:46:01.803812   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kube-scheduler/openshift-kube-scheduler-guard-00-50-56-8a-44-52
I0719 01:46:01.803813   37437 default_network_controller.go:699] Recording success event on pod openshift-image-registry/node-ca-sq7qk
I0719 01:46:01.803715   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-oauth-apiserver/apiserver-86f656c4dd-x7cqj
I0719 01:46:01.803583   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/csi-rbdplugin-provisioner-5dcc45fbf4-v5l2c in node 00-50-56-8a-f2-5d
I0719 01:46:01.803829   37437 obj_retry.go:541] Creating *v1.Pod openshift-oauth-apiserver/apiserver-86f656c4dd-x7cqj took: 231ns
I0719 01:46:01.803835   37437 default_network_controller.go:699] Recording success event on pod openshift-oauth-apiserver/apiserver-86f656c4dd-x7cqj
I0719 01:46:01.803841   37437 default_network_controller.go:655] Recording add event on pod openshift-kube-controller-manager/kube-controller-manager-guard-00-50-56-8a-5c-ec
I0719 01:46:01.803847   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kube-controller-manager/kube-controller-manager-guard-00-50-56-8a-5c-ec
I0719 01:46:01.803854   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kube-controller-manager/kube-controller-manager-guard-00-50-56-8a-5c-ec in node 00-50-56-8a-5c-ec
I0719 01:46:01.803855   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/csi-rbdplugin-provisioner-5dcc45fbf4-v5l2c took: 272.972µs
I0719 01:46:01.803861   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/csi-rbdplugin-provisioner-5dcc45fbf4-v5l2c
I0719 01:46:01.803866   37437 default_network_controller.go:655] Recording add event on pod openshift-authentication/oauth-openshift-7c9d9dfc8c-ddj6k
I0719 01:46:01.803873   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-authentication/oauth-openshift-7c9d9dfc8c-ddj6k
I0719 01:46:01.803878   37437 obj_retry.go:541] Creating *v1.Pod openshift-kube-controller-manager/kube-controller-manager-guard-00-50-56-8a-5c-ec took: 25.407µs
I0719 01:46:01.803560   37437 default_network_controller.go:699] Recording success event on pod openshift-kube-storage-version-migrator/migrator-7fc5dd675b-tfjhl
I0719 01:46:01.803896   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/csi-cephfsplugin-provisioner-585f89d895-ddwtl
I0719 01:46:01.803913   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/csi-cephfsplugin-provisioner-585f89d895-ddwtl
I0719 01:46:01.803748   37437 default_network_controller.go:699] Recording success event on pod openshift-operator-lifecycle-manager/packageserver-6bf7d58455-k8qkk
I0719 01:46:01.803924   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/csi-cephfsplugin-provisioner-585f89d895-ddwtl in node 00-50-56-8a-f2-5d
I0719 01:46:01.803937   37437 default_network_controller.go:655] Recording add event on pod openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-5c-ec
I0719 01:46:01.803275   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[0a:58:0a:82:00:05 10.130.0.5]} options:{GoMap:map[iface-id-ver:581109a4-a009-4938-b731-7e11b88236b0 requested-chassis:00-50-56-8a-fb-ea]} port_security:{GoSet:[0a:58:0a:82:00:05 10.130.0.5]} tag_request:{GoSet:[]} type:] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {4beb4d33-315b-4cb9-a30f-50f639da7d7f}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.803948   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-5c-ec
I0719 01:46:01.803951   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/csi-cephfsplugin-provisioner-585f89d895-ddwtl took: 28.894µs
I0719 01:46:01.803958   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-5c-ec in node 00-50-56-8a-5c-ec
I0719 01:46:01.803961   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/csi-cephfsplugin-provisioner-585f89d895-ddwtl
I0719 01:46:01.803964   37437 obj_retry.go:541] Creating *v1.Pod openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-5c-ec took: 8.454µs
I0719 01:46:01.803967   37437 default_network_controller.go:655] Recording add event on pod openshift-config-operator/openshift-config-operator-59dc875ddb-rnq74
I0719 01:46:01.803970   37437 default_network_controller.go:699] Recording success event on pod openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-5c-ec
I0719 01:46:01.803974   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-config-operator/openshift-config-operator-59dc875ddb-rnq74
I0719 01:46:01.803977   37437 default_network_controller.go:655] Recording add event on pod openshift-multus/multus-additional-cni-plugins-2kgg5
I0719 01:46:01.803988   37437 ovn.go:138] Ensuring zone remote for Pod openshift-config-operator/openshift-config-operator-59dc875ddb-rnq74 in node 00-50-56-8a-5c-ec
I0719 01:46:01.803717   37437 ovn.go:138] Ensuring zone remote for Pod openshift-service-ca-operator/service-ca-operator-86c8d4bbfd-w2qxx in node 00-50-56-8a-39-a0
I0719 01:46:01.803997   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-multus/multus-additional-cni-plugins-2kgg5
I0719 01:46:01.803991   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:4beb4d33-315b-4cb9-a30f-50f639da7d7f}]}}] Timeout:<nil> Where:[where column _uuid == {bc57259c-2feb-4fdd-95c3-dc98eb57f6e4}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.804004   37437 ovn.go:138] Ensuring zone remote for Pod openshift-multus/multus-additional-cni-plugins-2kgg5 in node 00-50-56-8a-f2-5d
I0719 01:46:01.804009   37437 obj_retry.go:541] Creating *v1.Pod openshift-multus/multus-additional-cni-plugins-2kgg5 took: 6.017µs
I0719 01:46:01.804014   37437 default_network_controller.go:699] Recording success event on pod openshift-multus/multus-additional-cni-plugins-2kgg5
I0719 01:46:01.804010   37437 obj_retry.go:541] Creating *v1.Pod openshift-service-ca-operator/service-ca-operator-86c8d4bbfd-w2qxx took: 294.288µs
I0719 01:46:01.804020   37437 default_network_controller.go:655] Recording add event on pod openshift-monitoring/telemeter-client-7b74cd774c-fg6lz
I0719 01:46:01.803481   37437 ovn.go:138] Ensuring zone remote for Pod openshift-multus/network-metrics-daemon-t4g2p in node 00-50-56-8a-39-a0
I0719 01:46:01.804027   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-monitoring/telemeter-client-7b74cd774c-fg6lz
I0719 01:46:01.804034   37437 ovn.go:138] Ensuring zone remote for Pod openshift-monitoring/telemeter-client-7b74cd774c-fg6lz in node 00-50-56-8a-f2-5d
I0719 01:46:01.804038   37437 obj_retry.go:541] Creating *v1.Pod openshift-multus/network-metrics-daemon-t4g2p took: 558.333µs
I0719 01:46:01.804047   37437 default_network_controller.go:699] Recording success event on pod openshift-multus/network-metrics-daemon-t4g2p
I0719 01:46:01.804052   37437 default_network_controller.go:655] Recording add event on pod openshift-multus/network-metrics-daemon-hxzdd
I0719 01:46:01.804059   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-multus/network-metrics-daemon-hxzdd
I0719 01:46:01.804053   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Port_Group Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:4beb4d33-315b-4cb9-a30f-50f639da7d7f}]}}] Timeout:<nil> Where:[where column _uuid == {8b7a4b62-2b45-4ee3-8ae7-c5dd66f13556}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.804009   37437 obj_retry.go:541] Creating *v1.Pod openshift-config-operator/openshift-config-operator-59dc875ddb-rnq74 took: 29.156µs
I0719 01:46:01.804065   37437 obj_retry.go:541] Creating *v1.Pod openshift-monitoring/telemeter-client-7b74cd774c-fg6lz took: 32.369µs
I0719 01:46:01.804073   37437 default_network_controller.go:699] Recording success event on pod openshift-config-operator/openshift-config-operator-59dc875ddb-rnq74
I0719 01:46:01.804075   37437 default_network_controller.go:699] Recording success event on pod openshift-monitoring/telemeter-client-7b74cd774c-fg6lz
I0719 01:46:01.804081   37437 default_network_controller.go:655] Recording add event on pod openshift-console/downloads-6967878986-hpkbw
I0719 01:46:01.804079   37437 default_network_controller.go:655] Recording add event on pod openshift-operator-lifecycle-manager/collect-profiles-28689225-j8wtn
I0719 01:46:01.804088   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-console/downloads-6967878986-hpkbw
I0719 01:46:01.804091   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-operator-lifecycle-manager/collect-profiles-28689225-j8wtn
I0719 01:46:01.804094   37437 ovn.go:138] Ensuring zone remote for Pod openshift-console/downloads-6967878986-hpkbw in node 00-50-56-8a-39-a0
I0719 01:46:01.804097   37437 obj_retry.go:459] Detected object openshift-operator-lifecycle-manager/collect-profiles-28689225-j8wtn of type *v1.Pod in terminal state (e.g. completed) during add event: will remove it
I0719 01:46:01.804115   37437 obj_retry.go:541] Creating *v1.Pod openshift-console/downloads-6967878986-hpkbw took: 20.931µs
I0719 01:46:01.804122   37437 default_network_controller.go:699] Recording success event on pod openshift-console/downloads-6967878986-hpkbw
I0719 01:46:01.804148   37437 default_network_controller.go:655] Recording add event on pod openshift-cluster-storage-operator/csi-snapshot-webhook-85b445968-78v7q
I0719 01:46:01.804160   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-cluster-storage-operator/csi-snapshot-webhook-85b445968-78v7q
I0719 01:46:01.804168   37437 ovn.go:138] Ensuring zone remote for Pod openshift-cluster-storage-operator/csi-snapshot-webhook-85b445968-78v7q in node 00-50-56-8a-5c-ec
I0719 01:46:01.804021   37437 default_network_controller.go:699] Recording success event on pod openshift-service-ca-operator/service-ca-operator-86c8d4bbfd-w2qxx
I0719 01:46:01.804182   37437 default_network_controller.go:655] Recording add event on pod openshift-machine-config-operator/machine-config-daemon-qpmqf
I0719 01:46:01.804189   37437 obj_retry.go:541] Creating *v1.Pod openshift-cluster-storage-operator/csi-snapshot-webhook-85b445968-78v7q took: 21.479µs
I0719 01:46:01.804194   37437 default_network_controller.go:699] Recording success event on pod openshift-cluster-storage-operator/csi-snapshot-webhook-85b445968-78v7q
I0719 01:46:01.804193   37437 address_set.go:613] (575fa52c-db50-4745-88b9-948435e2dbe8/default-network-controller:Namespace:openshift-operator-lifecycle-manager:v4/a1482332553631220387) deleting addresses [10.128.2.51] from address set
I0719 01:46:01.804200   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-machine-config-operator/machine-config-daemon-qpmqf
I0719 01:46:01.804203   37437 default_network_controller.go:655] Recording add event on pod openshift-cluster-samples-operator/cluster-samples-operator-6b95974b98-cxvvt
I0719 01:46:01.804209   37437 ovn.go:138] Ensuring zone remote for Pod openshift-machine-config-operator/machine-config-daemon-qpmqf in node 00-50-56-8a-f2-5d
I0719 01:46:01.803648   37437 transact.go:42] Configuring OVN: [{Op:mutate Table:Address_Set Row:map[] Rows:[] Columns:[] Mutations:[{Column:addresses Mutator:delete Value:{GoSet:[10.128.2.50]}}] Timeout:<nil> Where:[where column _uuid == {575fa52c-db50-4745-88b9-948435e2dbe8}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.804215   37437 obj_retry.go:541] Creating *v1.Pod openshift-machine-config-operator/machine-config-daemon-qpmqf took: 7.694µs
I0719 01:46:01.804198   37437 model_client.go:381] Update operations generated as: [{Op:update Table:NAT Row:map[external_ip:10.10.25.235 logical_ip:10.130.0.5 options:{GoMap:map[stateless:false]} type:snat] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {d59f8392-81cb-4c9f-bdd9-725151331a57}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.804209   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-cluster-samples-operator/cluster-samples-operator-6b95974b98-cxvvt
I0719 01:46:01.804228   37437 ovn.go:138] Ensuring zone remote for Pod openshift-cluster-samples-operator/cluster-samples-operator-6b95974b98-cxvvt in node 00-50-56-8a-5c-ec
I0719 01:46:01.804065   37437 ovn.go:138] Ensuring zone remote for Pod openshift-multus/network-metrics-daemon-hxzdd in node 00-50-56-8a-5c-ec
I0719 01:46:01.803097   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:nat Mutator:insert Value:{GoSet:[{GoUUID:d2b8e06f-1a01-4f37-9d33-2ff359aa53e6}]}}] Timeout:<nil> Where:[where column _uuid == {26b6d604-e9d3-4544-a4f0-f760e4ff11b6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.804312   37437 obj_retry.go:541] Creating *v1.Pod openshift-multus/network-metrics-daemon-hxzdd took: 244.572µs
I0719 01:46:01.804339   37437 default_network_controller.go:699] Recording success event on pod openshift-multus/network-metrics-daemon-hxzdd
I0719 01:46:01.804220   37437 default_network_controller.go:699] Recording success event on pod openshift-machine-config-operator/machine-config-daemon-qpmqf
I0719 01:46:01.804374   37437 default_network_controller.go:655] Recording add event on pod openshift-monitoring/alertmanager-main-0
I0719 01:46:01.804382   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-monitoring/alertmanager-main-0
I0719 01:46:01.804390   37437 ovn.go:138] Ensuring zone remote for Pod openshift-monitoring/alertmanager-main-0 in node 00-50-56-8a-f2-5d
I0719 01:46:01.804416   37437 obj_retry.go:541] Creating *v1.Pod openshift-monitoring/alertmanager-main-0 took: 27.27µs
I0719 01:46:01.804422   37437 default_network_controller.go:699] Recording success event on pod openshift-monitoring/alertmanager-main-0
I0719 01:46:01.804428   37437 default_network_controller.go:655] Recording add event on pod openshift-cluster-node-tuning-operator/tuned-f4pbt
I0719 01:46:01.804434   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-cluster-node-tuning-operator/tuned-f4pbt
I0719 01:46:01.803883   37437 default_network_controller.go:699] Recording success event on pod openshift-kube-controller-manager/kube-controller-manager-guard-00-50-56-8a-5c-ec
I0719 01:46:01.804449   37437 default_network_controller.go:655] Recording add event on pod openshift-apiserver/apiserver-7d9bbd465d-ln8v5
I0719 01:46:01.804456   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-apiserver/apiserver-7d9bbd465d-ln8v5
I0719 01:46:01.804463   37437 obj_retry.go:541] Creating *v1.Pod openshift-apiserver/apiserver-7d9bbd465d-ln8v5 took: 244ns
I0719 01:46:01.804468   37437 default_network_controller.go:699] Recording success event on pod openshift-apiserver/apiserver-7d9bbd465d-ln8v5
I0719 01:46:01.803884   37437 ovn.go:138] Ensuring zone remote for Pod openshift-authentication/oauth-openshift-7c9d9dfc8c-ddj6k in node 00-50-56-8a-39-a0
I0719 01:46:01.804473   37437 default_network_controller.go:655] Recording add event on pod openshift-network-operator/iptables-alerter-m44lf
I0719 01:46:01.803692   37437 transact.go:42] Configuring OVN: [{Op:mutate Table:Address_Set Row:map[] Rows:[] Columns:[] Mutations:[{Column:addresses Mutator:delete Value:{GoSet:[10.129.2.5]}}] Timeout:<nil> Where:[where column _uuid == {9269757a-340c-45bf-828d-361c80cb0226}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.804485   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-network-operator/iptables-alerter-m44lf
I0719 01:46:01.804493   37437 ovn.go:138] Ensuring zone remote for Pod openshift-network-operator/iptables-alerter-m44lf in node 00-50-56-8a-44-52
I0719 01:46:01.804495   37437 obj_retry.go:541] Creating *v1.Pod openshift-authentication/oauth-openshift-7c9d9dfc8c-ddj6k took: 614.926µs
I0719 01:46:01.804498   37437 obj_retry.go:541] Creating *v1.Pod openshift-network-operator/iptables-alerter-m44lf took: 7.047µs
I0719 01:46:01.804502   37437 default_network_controller.go:699] Recording success event on pod openshift-authentication/oauth-openshift-7c9d9dfc8c-ddj6k
I0719 01:46:01.804503   37437 default_network_controller.go:699] Recording success event on pod openshift-network-operator/iptables-alerter-m44lf
I0719 01:46:01.804510   37437 default_network_controller.go:655] Recording add event on pod openshift-kube-apiserver/kube-apiserver-guard-00-50-56-8a-39-a0
I0719 01:46:01.804514   37437 default_network_controller.go:655] Recording add event on pod openshift-etcd/revision-pruner-9-00-50-56-8a-44-52
I0719 01:46:01.804286   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[0a:58:0a:82:00:11 10.130.0.17]} options:{GoMap:map[iface-id-ver:b68a6803-6a94-4650-9d45-997245e04fe1 requested-chassis:00-50-56-8a-fb-ea]} port_security:{GoSet:[0a:58:0a:82:00:11 10.130.0.17]} tag_request:{GoSet:[]} type:] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {8105b57b-09e5-4f84-bac3-f79cdbc3d9ae}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:8105b57b-09e5-4f84-bac3-f79cdbc3d9ae}]}}] Timeout:<nil> Where:[where column _uuid == {bc57259c-2feb-4fdd-95c3-dc98eb57f6e4}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Port_Group Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:8105b57b-09e5-4f84-bac3-f79cdbc3d9ae}]}}] Timeout:<nil> Where:[where column _uuid == {dc5706a1-bba4-466c-a511-94f4646e1880}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:update Table:NAT Row:map[external_ip:10.10.25.235 logical_ip:10.130.0.17 options:{GoMap:map[stateless:false]} type:snat] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {d2b8e06f-1a01-4f37-9d33-2ff359aa53e6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:nat Mutator:insert Value:{GoSet:[{GoUUID:d2b8e06f-1a01-4f37-9d33-2ff359aa53e6}]}}] Timeout:<nil> Where:[where column _uuid == {26b6d604-e9d3-4544-a4f0-f760e4ff11b6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.804253   37437 obj_retry.go:541] Creating *v1.Pod openshift-cluster-samples-operator/cluster-samples-operator-6b95974b98-cxvvt took: 25.813µs
I0719 01:46:01.804523   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-etcd/revision-pruner-9-00-50-56-8a-44-52
I0719 01:46:01.804529   37437 default_network_controller.go:699] Recording success event on pod openshift-cluster-samples-operator/cluster-samples-operator-6b95974b98-cxvvt
I0719 01:46:01.804531   37437 ovn.go:138] Ensuring zone remote for Pod openshift-etcd/revision-pruner-9-00-50-56-8a-44-52 in node 00-50-56-8a-44-52
I0719 01:46:01.804534   37437 default_network_controller.go:655] Recording add event on pod openshift-dns/node-resolver-r7f9m
I0719 01:46:01.804541   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-dns/node-resolver-r7f9m
I0719 01:46:01.804247   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:nat Mutator:insert Value:{GoSet:[{GoUUID:d59f8392-81cb-4c9f-bdd9-725151331a57}]}}] Timeout:<nil> Where:[where column _uuid == {26b6d604-e9d3-4544-a4f0-f760e4ff11b6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.804548   37437 ovn.go:138] Ensuring zone remote for Pod openshift-dns/node-resolver-r7f9m in node 00-50-56-8a-f2-5d
I0719 01:46:01.803820   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kube-scheduler/openshift-kube-scheduler-guard-00-50-56-8a-44-52 in node 00-50-56-8a-44-52
I0719 01:46:01.804553   37437 obj_retry.go:541] Creating *v1.Pod openshift-dns/node-resolver-r7f9m took: 6.319µs
I0719 01:46:01.804558   37437 default_network_controller.go:699] Recording success event on pod openshift-dns/node-resolver-r7f9m
I0719 01:46:01.803754   37437 default_network_controller.go:699] Recording success event on pod openshift-kube-apiserver/kube-apiserver-guard-00-50-56-8a-44-52
I0719 01:46:01.804572   37437 default_network_controller.go:655] Recording add event on pod openshift-image-registry/node-ca-wgn2l
I0719 01:46:01.804573   37437 obj_retry.go:541] Creating *v1.Pod openshift-etcd/revision-pruner-9-00-50-56-8a-44-52 took: 43.575µs
I0719 01:46:01.804577   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-image-registry/node-ca-wgn2l
I0719 01:46:01.804596   37437 ovn.go:138] Ensuring zone remote for Pod openshift-image-registry/node-ca-wgn2l in node 00-50-56-8a-39-a0
I0719 01:46:01.804603   37437 obj_retry.go:541] Creating *v1.Pod openshift-image-registry/node-ca-wgn2l took: 8.264µs
I0719 01:46:01.804607   37437 default_network_controller.go:699] Recording success event on pod openshift-image-registry/node-ca-wgn2l
I0719 01:46:01.804606   37437 obj_retry.go:541] Creating *v1.Pod openshift-kube-scheduler/openshift-kube-scheduler-guard-00-50-56-8a-44-52 took: 783.763µs
I0719 01:46:01.804613   37437 default_network_controller.go:655] Recording add event on pod openshift-monitoring/node-exporter-7xrvj
I0719 01:46:01.803715   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-cluster-storage-operator/csi-snapshot-controller-794ff44f88-5jz8j
I0719 01:46:01.804620   37437 default_network_controller.go:699] Recording success event on pod openshift-kube-scheduler/openshift-kube-scheduler-guard-00-50-56-8a-44-52
I0719 01:46:01.804626   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-monitoring/node-exporter-7xrvj
I0719 01:46:01.803822   37437 default_network_controller.go:655] Recording add event on pod openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-44-52
I0719 01:46:01.804633   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/ocs-metrics-exporter-84f9766477-r8fxs
I0719 01:46:01.804516   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kube-apiserver/kube-apiserver-guard-00-50-56-8a-39-a0
I0719 01:46:01.804642   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-44-52
I0719 01:46:01.804643   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/ocs-metrics-exporter-84f9766477-r8fxs
I0719 01:46:01.804242   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Address_Set Row:map[] Rows:[] Columns:[] Mutations:[{Column:addresses Mutator:delete Value:{GoSet:[10.128.2.51]}}] Timeout:<nil> Where:[where column _uuid == {575fa52c-db50-4745-88b9-948435e2dbe8}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.804440   37437 ovn.go:138] Ensuring zone remote for Pod openshift-cluster-node-tuning-operator/tuned-f4pbt in node 00-50-56-8a-39-a0
I0719 01:46:01.804653   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kube-apiserver/kube-apiserver-guard-00-50-56-8a-39-a0 in node 00-50-56-8a-39-a0
I0719 01:46:01.804658   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/ocs-metrics-exporter-84f9766477-r8fxs in node 00-50-56-8a-e1-e7
I0719 01:46:01.804658   37437 obj_retry.go:541] Creating *v1.Pod openshift-cluster-node-tuning-operator/tuned-f4pbt took: 218.316µs
I0719 01:46:01.804561   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[0a:58:0a:82:00:05 10.130.0.5]} options:{GoMap:map[iface-id-ver:581109a4-a009-4938-b731-7e11b88236b0 requested-chassis:00-50-56-8a-fb-ea]} port_security:{GoSet:[0a:58:0a:82:00:05 10.130.0.5]} tag_request:{GoSet:[]} type:] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {4beb4d33-315b-4cb9-a30f-50f639da7d7f}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:4beb4d33-315b-4cb9-a30f-50f639da7d7f}]}}] Timeout:<nil> Where:[where column _uuid == {bc57259c-2feb-4fdd-95c3-dc98eb57f6e4}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Port_Group Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:4beb4d33-315b-4cb9-a30f-50f639da7d7f}]}}] Timeout:<nil> Where:[where column _uuid == {8b7a4b62-2b45-4ee3-8ae7-c5dd66f13556}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:update Table:NAT Row:map[external_ip:10.10.25.235 logical_ip:10.130.0.5 options:{GoMap:map[stateless:false]} type:snat] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {d59f8392-81cb-4c9f-bdd9-725151331a57}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:nat Mutator:insert Value:{GoSet:[{GoUUID:d59f8392-81cb-4c9f-bdd9-725151331a57}]}}] Timeout:<nil> Where:[where column _uuid == {26b6d604-e9d3-4544-a4f0-f760e4ff11b6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.804664   37437 default_network_controller.go:699] Recording success event on pod openshift-cluster-node-tuning-operator/tuned-f4pbt
I0719 01:46:01.804672   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/ocs-operator-5567c4fdb4-8b9zr
I0719 01:46:01.804676   37437 obj_retry.go:541] Creating *v1.Pod openshift-kube-apiserver/kube-apiserver-guard-00-50-56-8a-39-a0 took: 23.983µs
I0719 01:46:01.804678   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/ocs-metrics-exporter-84f9766477-r8fxs took: 22.057µs
I0719 01:46:01.804680   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/ocs-operator-5567c4fdb4-8b9zr
I0719 01:46:01.804633   37437 ovn.go:138] Ensuring zone remote for Pod openshift-cluster-storage-operator/csi-snapshot-controller-794ff44f88-5jz8j in node 00-50-56-8a-39-a0
I0719 01:46:01.804688   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/ocs-metrics-exporter-84f9766477-r8fxs
I0719 01:46:01.804698   37437 default_network_controller.go:655] Recording add event on pod openshift-monitoring/kube-state-metrics-589b9987d-ck4ch
I0719 01:46:01.804578   37437 default_network_controller.go:699] Recording success event on pod openshift-etcd/revision-pruner-9-00-50-56-8a-44-52
I0719 01:46:01.804659   37437 transact.go:42] Configuring OVN: [{Op:mutate Table:Address_Set Row:map[] Rows:[] Columns:[] Mutations:[{Column:addresses Mutator:delete Value:{GoSet:[10.128.2.51]}}] Timeout:<nil> Where:[where column _uuid == {575fa52c-db50-4745-88b9-948435e2dbe8}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.804714   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-monitoring/kube-state-metrics-589b9987d-ck4ch
I0719 01:46:01.804701   37437 obj_retry.go:541] Creating *v1.Pod openshift-cluster-storage-operator/csi-snapshot-controller-794ff44f88-5jz8j took: 72.394µs
I0719 01:46:01.804722   37437 ovn.go:138] Ensuring zone remote for Pod openshift-monitoring/kube-state-metrics-589b9987d-ck4ch in node 00-50-56-8a-f2-5d
I0719 01:46:01.804734   37437 default_network_controller.go:699] Recording success event on pod openshift-cluster-storage-operator/csi-snapshot-controller-794ff44f88-5jz8j
I0719 01:46:01.804741   37437 default_network_controller.go:655] Recording add event on pod openshift-operator-lifecycle-manager/packageserver-6bf7d58455-gh44f
I0719 01:46:01.804719   37437 default_network_controller.go:655] Recording add event on pod openshift-ingress-canary/ingress-canary-lrjr5
I0719 01:46:01.804756   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-operator-lifecycle-manager/packageserver-6bf7d58455-gh44f
I0719 01:46:01.804809   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-ingress-canary/ingress-canary-lrjr5
I0719 01:46:01.804816   37437 ovn.go:138] Ensuring zone remote for Pod openshift-operator-lifecycle-manager/packageserver-6bf7d58455-gh44f in node 00-50-56-8a-39-a0
I0719 01:46:01.804823   37437 ovn.go:138] Ensuring zone remote for Pod openshift-ingress-canary/ingress-canary-lrjr5 in node 00-50-56-8a-e1-e7
I0719 01:46:01.804822   37437 obj_retry.go:541] Creating *v1.Pod openshift-monitoring/kube-state-metrics-589b9987d-ck4ch took: 99.703µs
I0719 01:46:01.804831   37437 default_network_controller.go:699] Recording success event on pod openshift-monitoring/kube-state-metrics-589b9987d-ck4ch
I0719 01:46:01.804634   37437 ovn.go:138] Ensuring zone remote for Pod openshift-monitoring/node-exporter-7xrvj in node 00-50-56-8a-5c-ec
I0719 01:46:01.804855   37437 obj_retry.go:541] Creating *v1.Pod openshift-monitoring/node-exporter-7xrvj took: 220.478µs
I0719 01:46:01.804858   37437 obj_retry.go:541] Creating *v1.Pod openshift-ingress-canary/ingress-canary-lrjr5 took: 36.839µs
I0719 01:46:01.804864   37437 default_network_controller.go:699] Recording success event on pod openshift-ingress-canary/ingress-canary-lrjr5
I0719 01:46:01.804871   37437 default_network_controller.go:655] Recording add event on pod openshift-dns/dns-default-5hh4c
I0719 01:46:01.804886   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-dns/dns-default-5hh4c
I0719 01:46:01.804893   37437 default_network_controller.go:699] Recording success event on pod openshift-monitoring/node-exporter-7xrvj
I0719 01:46:01.804898   37437 ovn.go:138] Ensuring zone remote for Pod openshift-dns/dns-default-5hh4c in node 00-50-56-8a-44-52
I0719 01:46:01.804901   37437 default_network_controller.go:655] Recording add event on pod openshift-network-operator/iptables-alerter-b72gh
I0719 01:46:01.804681   37437 default_network_controller.go:699] Recording success event on pod openshift-kube-apiserver/kube-apiserver-guard-00-50-56-8a-39-a0
I0719 01:46:01.804917   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-network-operator/iptables-alerter-b72gh
I0719 01:46:01.804925   37437 ovn.go:138] Ensuring zone remote for Pod openshift-network-operator/iptables-alerter-b72gh in node 00-50-56-8a-39-a0
I0719 01:46:01.804926   37437 default_network_controller.go:655] Recording add event on pod openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-39-a0
I0719 01:46:01.804930   37437 obj_retry.go:541] Creating *v1.Pod openshift-network-operator/iptables-alerter-b72gh took: 6.548µs
I0719 01:46:01.804934   37437 default_network_controller.go:699] Recording success event on pod openshift-network-operator/iptables-alerter-b72gh
I0719 01:46:01.804936   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-39-a0
I0719 01:46:01.804939   37437 default_network_controller.go:655] Recording add event on pod openshift-route-controller-manager/route-controller-manager-676cdfdbc8-t227m
I0719 01:46:01.804947   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-39-a0 in node 00-50-56-8a-39-a0
I0719 01:46:01.804956   37437 obj_retry.go:541] Creating *v1.Pod openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-39-a0 took: 10.078µs
I0719 01:46:01.804701   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-44-52 in node 00-50-56-8a-44-52
I0719 01:46:01.804962   37437 default_network_controller.go:699] Recording success event on pod openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-39-a0
I0719 01:46:01.804965   37437 obj_retry.go:541] Creating *v1.Pod openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-44-52 took: 270.096µs
I0719 01:46:01.804707   37437 default_network_controller.go:655] Recording add event on pod openshift-controller-manager/controller-manager-5c7f9f9d47-c74xp
I0719 01:46:01.804970   37437 default_network_controller.go:699] Recording success event on pod openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-44-52
I0719 01:46:01.804970   37437 default_network_controller.go:655] Recording add event on pod openshift-machine-config-operator/machine-config-operator-7fc5c776cc-r6wsl
I0719 01:46:01.804980   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-controller-manager/controller-manager-5c7f9f9d47-c74xp
I0719 01:46:01.804998   37437 default_network_controller.go:655] Recording add event on pod openshift-kube-apiserver/revision-pruner-8-00-50-56-8a-44-52
I0719 01:46:01.805001   37437 ovn.go:138] Ensuring zone remote for Pod openshift-controller-manager/controller-manager-5c7f9f9d47-c74xp in node 00-50-56-8a-5c-ec
I0719 01:46:01.805003   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-machine-config-operator/machine-config-operator-7fc5c776cc-r6wsl
I0719 01:46:01.805006   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kube-apiserver/revision-pruner-8-00-50-56-8a-44-52
I0719 01:46:01.805006   37437 obj_retry.go:541] Creating *v1.Pod openshift-dns/dns-default-5hh4c took: 106.419µs
I0719 01:46:01.805020   37437 default_network_controller.go:699] Recording success event on pod openshift-dns/dns-default-5hh4c
I0719 01:46:01.805023   37437 obj_retry.go:541] Creating *v1.Pod openshift-controller-manager/controller-manager-5c7f9f9d47-c74xp took: 28.904µs
I0719 01:46:01.805029   37437 default_network_controller.go:699] Recording success event on pod openshift-controller-manager/controller-manager-5c7f9f9d47-c74xp
I0719 01:46:01.805031   37437 default_network_controller.go:655] Recording add event on pod openshift-kube-apiserver/kube-apiserver-00-50-56-8a-5c-ec
I0719 01:46:01.805035   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/rook-ceph-mon-c-5b4c4697fb-8w28d
I0719 01:46:01.805040   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kube-apiserver/kube-apiserver-00-50-56-8a-5c-ec
I0719 01:46:01.805046   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/rook-ceph-mon-c-5b4c4697fb-8w28d
I0719 01:46:01.805048   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kube-apiserver/kube-apiserver-00-50-56-8a-5c-ec in node 00-50-56-8a-5c-ec
I0719 01:46:01.805054   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/rook-ceph-mon-c-5b4c4697fb-8w28d in node 00-50-56-8a-e1-e7
I0719 01:46:01.804949   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-route-controller-manager/route-controller-manager-676cdfdbc8-t227m
I0719 01:46:01.805053   37437 obj_retry.go:541] Creating *v1.Pod openshift-kube-apiserver/kube-apiserver-00-50-56-8a-5c-ec took: 7.123µs
I0719 01:46:01.805063   37437 default_network_controller.go:699] Recording success event on pod openshift-kube-apiserver/kube-apiserver-00-50-56-8a-5c-ec
I0719 01:46:01.805065   37437 ovn.go:138] Ensuring zone remote for Pod openshift-route-controller-manager/route-controller-manager-676cdfdbc8-t227m in node 00-50-56-8a-39-a0
I0719 01:46:01.805068   37437 default_network_controller.go:655] Recording add event on pod openshift-kube-apiserver-operator/kube-apiserver-operator-55dc5cdcf9-p4csg
I0719 01:46:01.805070   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/rook-ceph-mon-c-5b4c4697fb-8w28d took: 18.277µs
I0719 01:46:01.805076   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kube-apiserver-operator/kube-apiserver-operator-55dc5cdcf9-p4csg
I0719 01:46:01.805079   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/rook-ceph-mon-c-5b4c4697fb-8w28d
I0719 01:46:01.805083   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kube-apiserver-operator/kube-apiserver-operator-55dc5cdcf9-p4csg in node 00-50-56-8a-5c-ec
I0719 01:46:01.805084   37437 default_network_controller.go:655] Recording add event on pod openshift-cluster-machine-approver/machine-approver-5bf6544664-79krt
I0719 01:46:01.805090   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-cluster-machine-approver/machine-approver-5bf6544664-79krt
I0719 01:46:01.805012   37437 ovn.go:138] Ensuring zone remote for Pod openshift-machine-config-operator/machine-config-operator-7fc5c776cc-r6wsl in node 00-50-56-8a-39-a0
I0719 01:46:01.805110   37437 obj_retry.go:541] Creating *v1.Pod openshift-route-controller-manager/route-controller-manager-676cdfdbc8-t227m took: 40.617µs
I0719 01:46:01.805115   37437 obj_retry.go:541] Creating *v1.Pod openshift-kube-apiserver-operator/kube-apiserver-operator-55dc5cdcf9-p4csg took: 33.805µs
I0719 01:46:01.805118   37437 default_network_controller.go:699] Recording success event on pod openshift-route-controller-manager/route-controller-manager-676cdfdbc8-t227m
I0719 01:46:01.805123   37437 obj_retry.go:541] Creating *v1.Pod openshift-machine-config-operator/machine-config-operator-7fc5c776cc-r6wsl took: 112.733µs
I0719 01:46:01.805127   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/rook-ceph-mon-a-6dc9d78597-7ttc9
I0719 01:46:01.805129   37437 default_network_controller.go:699] Recording success event on pod openshift-machine-config-operator/machine-config-operator-7fc5c776cc-r6wsl
I0719 01:46:01.805129   37437 default_network_controller.go:699] Recording success event on pod openshift-kube-apiserver-operator/kube-apiserver-operator-55dc5cdcf9-p4csg
I0719 01:46:01.805135   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/rook-ceph-mon-a-6dc9d78597-7ttc9
I0719 01:46:01.805142   37437 default_network_controller.go:655] Recording add event on pod openshift-monitoring/node-exporter-s77zj
I0719 01:46:01.805144   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/rook-ceph-mon-a-6dc9d78597-7ttc9 in node 00-50-56-8a-f2-5d
I0719 01:46:01.805152   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-monitoring/node-exporter-s77zj
I0719 01:46:01.804845   37437 obj_retry.go:541] Creating *v1.Pod openshift-operator-lifecycle-manager/packageserver-6bf7d58455-gh44f took: 30.882µs
I0719 01:46:01.805163   37437 ovn.go:138] Ensuring zone remote for Pod openshift-monitoring/node-exporter-s77zj in node 00-50-56-8a-44-52
I0719 01:46:01.805166   37437 default_network_controller.go:699] Recording success event on pod openshift-operator-lifecycle-manager/packageserver-6bf7d58455-gh44f
I0719 01:46:01.805172   37437 default_network_controller.go:655] Recording add event on pod openshift-image-registry/cluster-image-registry-operator-656868857f-f94pq
I0719 01:46:01.804418   37437 default_network_controller.go:655] Recording add event on pod openshift-cluster-node-tuning-operator/tuned-cjc5f
I0719 01:46:01.805181   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-image-registry/cluster-image-registry-operator-656868857f-f94pq
I0719 01:46:01.805172   37437 obj_retry.go:541] Creating *v1.Pod openshift-monitoring/node-exporter-s77zj took: 10.552µs
I0719 01:46:01.804847   37437 default_network_controller.go:655] Recording add event on pod openshift-dns/dns-default-wn5nz
I0719 01:46:01.805136   37437 default_network_controller.go:655] Recording add event on pod openshift-oauth-apiserver/apiserver-86f656c4dd-g82dw
I0719 01:46:01.805177   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/rook-ceph-mon-a-6dc9d78597-7ttc9 took: 34.361µs
I0719 01:46:01.805197   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-dns/dns-default-wn5nz
I0719 01:46:01.804841   37437 default_network_controller.go:655] Recording add event on pod openshift-multus/multus-25bkq
I0719 01:46:01.805206   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-oauth-apiserver/apiserver-86f656c4dd-g82dw
I0719 01:46:01.805097   37437 ovn.go:138] Ensuring zone remote for Pod openshift-cluster-machine-approver/machine-approver-5bf6544664-79krt in node 00-50-56-8a-39-a0
I0719 01:46:01.805219   37437 obj_retry.go:541] Creating *v1.Pod openshift-cluster-machine-approver/machine-approver-5bf6544664-79krt took: 122.775µs
I0719 01:46:01.805224   37437 default_network_controller.go:699] Recording success event on pod openshift-cluster-machine-approver/machine-approver-5bf6544664-79krt
I0719 01:46:01.805231   37437 default_network_controller.go:655] Recording add event on pod openshift-cloud-credential-operator/cloud-credential-operator-6488fd5f9b-jkdg2
I0719 01:46:01.805236   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-multus/multus-25bkq
I0719 01:46:01.805245   37437 ovn.go:138] Ensuring zone remote for Pod openshift-multus/multus-25bkq in node 00-50-56-8a-e1-e7
I0719 01:46:01.805249   37437 default_network_controller.go:655] Recording add event on pod openshift-machine-config-operator/machine-config-server-j8kbc
I0719 01:46:01.805262   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-machine-config-operator/machine-config-server-j8kbc
I0719 01:46:01.805271   37437 ovn.go:138] Ensuring zone remote for Pod openshift-machine-config-operator/machine-config-server-j8kbc in node 00-50-56-8a-44-52
I0719 01:46:01.805013   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kube-apiserver/revision-pruner-8-00-50-56-8a-44-52 in node 00-50-56-8a-44-52
I0719 01:46:01.805287   37437 obj_retry.go:541] Creating *v1.Pod openshift-machine-config-operator/machine-config-server-j8kbc took: 5.955µs
I0719 01:46:01.805368   37437 default_network_controller.go:699] Recording success event on pod openshift-machine-config-operator/machine-config-server-j8kbc
I0719 01:46:01.805377   37437 default_network_controller.go:655] Recording add event on pod openshift-kube-scheduler/revision-pruner-6-00-50-56-8a-39-a0
I0719 01:46:01.805249   37437 obj_retry.go:541] Creating *v1.Pod openshift-multus/multus-25bkq took: 5.922µs
I0719 01:46:01.805386   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kube-scheduler/revision-pruner-6-00-50-56-8a-39-a0
I0719 01:46:01.805387   37437 obj_retry.go:541] Creating *v1.Pod openshift-kube-apiserver/revision-pruner-8-00-50-56-8a-44-52 took: 374.528µs
I0719 01:46:01.805391   37437 default_network_controller.go:699] Recording success event on pod openshift-multus/multus-25bkq
I0719 01:46:01.805394   37437 default_network_controller.go:699] Recording success event on pod openshift-kube-apiserver/revision-pruner-8-00-50-56-8a-44-52
I0719 01:46:01.805398   37437 default_network_controller.go:655] Recording add event on pod openshift-kni-infra/keepalived-00-50-56-8a-44-52
I0719 01:46:01.805401   37437 default_network_controller.go:655] Recording add event on pod openshift-network-operator/network-operator-6967d44d7-4wwpm
I0719 01:46:01.805406   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kni-infra/keepalived-00-50-56-8a-44-52
I0719 01:46:01.805412   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-network-operator/network-operator-6967d44d7-4wwpm
I0719 01:46:01.805414   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kni-infra/keepalived-00-50-56-8a-44-52 in node 00-50-56-8a-44-52
I0719 01:46:01.805419   37437 ovn.go:138] Ensuring zone remote for Pod openshift-network-operator/network-operator-6967d44d7-4wwpm in node 00-50-56-8a-5c-ec
I0719 01:46:01.805214   37437 port_cache.go:96] port-cache(openshift-local-storage_diskmaker-manager-2zrc6): added port &{name:openshift-local-storage_diskmaker-manager-2zrc6 uuid:8105b57b-09e5-4f84-bac3-f79cdbc3d9ae logicalSwitch:00-50-56-8a-fb-ea ips:[0xc000941f50] mac:[10 88 10 130 0 17] expires:{wall:0 ext:0 loc:<nil>}} with IP: [10.130.0.17/23] and MAC: 0a:58:0a:82:00:11
I0719 01:46:01.805237   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-cloud-credential-operator/cloud-credential-operator-6488fd5f9b-jkdg2
I0719 01:46:01.805433   37437 ovn.go:138] Ensuring zone remote for Pod openshift-cloud-credential-operator/cloud-credential-operator-6488fd5f9b-jkdg2 in node 00-50-56-8a-5c-ec
I0719 01:46:01.805436   37437 pods.go:220] [openshift-local-storage/diskmaker-manager-2zrc6] addLogicalPort took 5.54247ms, libovsdb time 923.04µs
I0719 01:46:01.805443   37437 obj_retry.go:541] Creating *v1.Pod openshift-local-storage/diskmaker-manager-2zrc6 took: 5.5623ms
I0719 01:46:01.805447   37437 default_network_controller.go:699] Recording success event on pod openshift-local-storage/diskmaker-manager-2zrc6
I0719 01:46:01.805453   37437 default_network_controller.go:655] Recording add event on pod openshift-dns/node-resolver-tjmrc
I0719 01:46:01.805454   37437 obj_retry.go:541] Creating *v1.Pod openshift-cloud-credential-operator/cloud-credential-operator-6488fd5f9b-jkdg2 took: 21.495µs
I0719 01:46:01.805393   37437 obj_retry.go:459] Detected object openshift-kube-scheduler/revision-pruner-6-00-50-56-8a-39-a0 of type *v1.Pod in terminal state (e.g. completed) during add event: will remove it
I0719 01:46:01.805419   37437 obj_retry.go:541] Creating *v1.Pod openshift-kni-infra/keepalived-00-50-56-8a-44-52 took: 7.079µs
I0719 01:46:01.805465   37437 default_network_controller.go:699] Recording success event on pod openshift-kni-infra/keepalived-00-50-56-8a-44-52
I0719 01:46:01.805189   37437 ovn.go:138] Ensuring zone remote for Pod openshift-image-registry/cluster-image-registry-operator-656868857f-f94pq in node 00-50-56-8a-5c-ec
I0719 01:46:01.805471   37437 default_network_controller.go:655] Recording add event on pod openshift-network-operator/iptables-alerter-nh7z8
I0719 01:46:01.805482   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-network-operator/iptables-alerter-nh7z8
I0719 01:46:01.805184   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-cluster-node-tuning-operator/tuned-cjc5f
I0719 01:46:01.805509   37437 ovn.go:138] Ensuring zone remote for Pod openshift-cluster-node-tuning-operator/tuned-cjc5f in node 00-50-56-8a-e1-e7
I0719 01:46:01.805518   37437 obj_retry.go:541] Creating *v1.Pod openshift-cluster-node-tuning-operator/tuned-cjc5f took: 10.911µs
I0719 01:46:01.805523   37437 default_network_controller.go:699] Recording success event on pod openshift-cluster-node-tuning-operator/tuned-cjc5f
I0719 01:46:01.805529   37437 default_network_controller.go:655] Recording add event on pod openshift-ingress-canary/ingress-canary-lsx7x
I0719 01:46:01.805517   37437 obj_retry.go:541] Creating *v1.Pod openshift-image-registry/cluster-image-registry-operator-656868857f-f94pq took: 327.375µs
I0719 01:46:01.805536   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-ingress-canary/ingress-canary-lsx7x
I0719 01:46:01.805543   37437 default_network_controller.go:699] Recording success event on pod openshift-image-registry/cluster-image-registry-operator-656868857f-f94pq
I0719 01:46:01.805546   37437 ovn.go:134] Ensuring zone local for Pod openshift-ingress-canary/ingress-canary-lsx7x in node 00-50-56-8a-fb-ea
I0719 01:46:01.805199   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/rook-ceph-mon-a-6dc9d78597-7ttc9
I0719 01:46:01.805555   37437 default_network_controller.go:655] Recording add event on pod openshift-monitoring/prometheus-operator-admission-webhook-67db68b49d-wbfqq
I0719 01:46:01.805560   37437 base_network_controller_pods.go:476] [default/openshift-ingress-canary/ingress-canary-lsx7x] creating logical port openshift-ingress-canary_ingress-canary-lsx7x for pod on switch 00-50-56-8a-fb-ea
I0719 01:46:01.805190   37437 default_network_controller.go:699] Recording success event on pod openshift-monitoring/node-exporter-s77zj
I0719 01:46:01.805596   37437 default_network_controller.go:655] Recording add event on pod openshift-apiserver/apiserver-7d9bbd465d-7pbl8
I0719 01:46:01.805603   37437 default_network_controller.go:655] Recording add event on pod openshift-ingress/router-default-54fb8ffc6b-hhdt2
I0719 01:46:01.805607   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-apiserver/apiserver-7d9bbd465d-7pbl8
I0719 01:46:01.805614   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-ingress/router-default-54fb8ffc6b-hhdt2
I0719 01:46:01.805616   37437 ovn.go:138] Ensuring zone remote for Pod openshift-apiserver/apiserver-7d9bbd465d-7pbl8 in node 00-50-56-8a-39-a0
I0719 01:46:01.805626   37437 ovn.go:138] Ensuring zone remote for Pod openshift-ingress/router-default-54fb8ffc6b-hhdt2 in node 00-50-56-8a-f2-5d
I0719 01:46:01.805634   37437 obj_retry.go:541] Creating *v1.Pod openshift-ingress/router-default-54fb8ffc6b-hhdt2 took: 10.978µs
I0719 01:46:01.805642   37437 default_network_controller.go:699] Recording success event on pod openshift-ingress/router-default-54fb8ffc6b-hhdt2
I0719 01:46:01.804709   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/ocs-operator-5567c4fdb4-8b9zr in node 00-50-56-8a-f2-5d
I0719 01:46:01.805648   37437 obj_retry.go:541] Creating *v1.Pod openshift-apiserver/apiserver-7d9bbd465d-7pbl8 took: 33.06µs
I0719 01:46:01.805657   37437 default_network_controller.go:699] Recording success event on pod openshift-apiserver/apiserver-7d9bbd465d-7pbl8
I0719 01:46:01.805568   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-monitoring/prometheus-operator-admission-webhook-67db68b49d-wbfqq
I0719 01:46:01.805665   37437 default_network_controller.go:655] Recording add event on pod openshift-etcd/etcd-00-50-56-8a-44-52
I0719 01:46:01.805671   37437 ovn.go:138] Ensuring zone remote for Pod openshift-monitoring/prometheus-operator-admission-webhook-67db68b49d-wbfqq in node 00-50-56-8a-f2-5d
I0719 01:46:01.805207   37437 ovn.go:138] Ensuring zone remote for Pod openshift-dns/dns-default-wn5nz in node 00-50-56-8a-5c-ec
I0719 01:46:01.805214   37437 ovn.go:138] Ensuring zone remote for Pod openshift-oauth-apiserver/apiserver-86f656c4dd-g82dw in node 00-50-56-8a-5c-ec
I0719 01:46:01.805698   37437 obj_retry.go:541] Creating *v1.Pod openshift-dns/dns-default-wn5nz took: 493.491µs
I0719 01:46:01.805673   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-etcd/etcd-00-50-56-8a-44-52
I0719 01:46:01.806111   37437 default_network_controller.go:699] Recording success event on pod openshift-dns/dns-default-wn5nz
I0719 01:46:01.806125   37437 default_network_controller.go:655] Recording add event on pod openshift-authentication/oauth-openshift-7c9d9dfc8c-qcf89
I0719 01:46:01.806128   37437 ovn.go:138] Ensuring zone remote for Pod openshift-etcd/etcd-00-50-56-8a-44-52 in node 00-50-56-8a-44-52
I0719 01:46:01.806135   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-authentication/oauth-openshift-7c9d9dfc8c-qcf89
I0719 01:46:01.806136   37437 obj_retry.go:541] Creating *v1.Pod openshift-etcd/etcd-00-50-56-8a-44-52 took: 13.661µs
I0719 01:46:01.806144   37437 default_network_controller.go:699] Recording success event on pod openshift-etcd/etcd-00-50-56-8a-44-52
I0719 01:46:01.806145   37437 obj_retry.go:541] Creating *v1.Pod openshift-authentication/oauth-openshift-7c9d9dfc8c-qcf89 took: 422ns
I0719 01:46:01.806150   37437 default_network_controller.go:699] Recording success event on pod openshift-authentication/oauth-openshift-7c9d9dfc8c-qcf89
I0719 01:46:01.805552   37437 address_set.go:613] (ae1e6050-3670-4f5e-978c-ca1e35ef7b65/default-network-controller:Namespace:openshift-kube-scheduler:v4/a15634036902741400949) deleting addresses [10.128.0.5] from address set
I0719 01:46:01.806156   37437 default_network_controller.go:655] Recording add event on pod openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-39-a0
I0719 01:46:01.805459   37437 default_network_controller.go:699] Recording success event on pod openshift-cloud-credential-operator/cloud-credential-operator-6488fd5f9b-jkdg2
I0719 01:46:01.806151   37437 default_network_controller.go:655] Recording add event on pod openshift-monitoring/prometheus-k8s-0
I0719 01:46:01.805685   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/ocs-operator-5567c4fdb4-8b9zr took: 975.448µs
I0719 01:46:01.805424   37437 obj_retry.go:541] Creating *v1.Pod openshift-network-operator/network-operator-6967d44d7-4wwpm took: 6.369µs
I0719 01:46:01.806175   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/ocs-operator-5567c4fdb4-8b9zr
I0719 01:46:01.806053   37437 obj_retry.go:541] Creating *v1.Pod openshift-monitoring/prometheus-operator-admission-webhook-67db68b49d-wbfqq took: 27.788µs
I0719 01:46:01.806181   37437 default_network_controller.go:699] Recording success event on pod openshift-network-operator/network-operator-6967d44d7-4wwpm
I0719 01:46:01.806183   37437 default_network_controller.go:699] Recording success event on pod openshift-monitoring/prometheus-operator-admission-webhook-67db68b49d-wbfqq
I0719 01:46:01.806164   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[0a:58:0a:82:00:0a 10.130.0.10]} options:{GoMap:map[iface-id-ver:f89c28d9-9c2b-4bde-abbc-d06eda08730b requested-chassis:00-50-56-8a-fb-ea]} port_security:{GoSet:[0a:58:0a:82:00:0a 10.130.0.10]} tag_request:{GoSet:[]} type:] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {a89efe1a-8a9e-4458-8f2e-7b5e3036c052}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.806189   37437 default_network_controller.go:655] Recording add event on pod openshift-monitoring/metrics-server-7d47f4cbc-5qp84
I0719 01:46:01.806182   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Address_Set Row:map[] Rows:[] Columns:[] Mutations:[{Column:addresses Mutator:delete Value:{GoSet:[10.128.0.5]}}] Timeout:<nil> Where:[where column _uuid == {ae1e6050-3670-4f5e-978c-ca1e35ef7b65}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.806101   37437 obj_retry.go:541] Creating *v1.Pod openshift-oauth-apiserver/apiserver-86f656c4dd-g82dw took: 886.838µs
I0719 01:46:01.806204   37437 default_network_controller.go:699] Recording success event on pod openshift-oauth-apiserver/apiserver-86f656c4dd-g82dw
I0719 01:46:01.806202   37437 transact.go:42] Configuring OVN: [{Op:mutate Table:Address_Set Row:map[] Rows:[] Columns:[] Mutations:[{Column:addresses Mutator:delete Value:{GoSet:[10.128.0.5]}}] Timeout:<nil> Where:[where column _uuid == {ae1e6050-3670-4f5e-978c-ca1e35ef7b65}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.806214   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:a89efe1a-8a9e-4458-8f2e-7b5e3036c052}]}}] Timeout:<nil> Where:[where column _uuid == {bc57259c-2feb-4fdd-95c3-dc98eb57f6e4}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.803724   37437 obj_retry.go:541] Creating *v1.Pod openshift-machine-api/ironic-proxy-sn8n9 took: 95.629µs
I0719 01:46:01.806245   37437 default_network_controller.go:699] Recording success event on pod openshift-machine-api/ironic-proxy-sn8n9
I0719 01:46:01.806196   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-monitoring/metrics-server-7d47f4cbc-5qp84
I0719 01:46:01.806253   37437 default_network_controller.go:655] Recording add event on pod openshift-machine-api/ironic-proxy-6zm7s
I0719 01:46:01.806259   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-machine-api/ironic-proxy-6zm7s
I0719 01:46:01.806260   37437 ovn.go:138] Ensuring zone remote for Pod openshift-monitoring/metrics-server-7d47f4cbc-5qp84 in node 00-50-56-8a-e1-e7
I0719 01:46:01.806267   37437 ovn.go:138] Ensuring zone remote for Pod openshift-machine-api/ironic-proxy-6zm7s in node 00-50-56-8a-44-52
I0719 01:46:01.806261   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Port_Group Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:a89efe1a-8a9e-4458-8f2e-7b5e3036c052}]}}] Timeout:<nil> Where:[where column _uuid == {ecf197d0-8290-4f21-9e31-9dd9f7c67435}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.806271   37437 obj_retry.go:541] Creating *v1.Pod openshift-machine-api/ironic-proxy-6zm7s took: 6.402µs
I0719 01:46:01.806278   37437 default_network_controller.go:699] Recording success event on pod openshift-machine-api/ironic-proxy-6zm7s
I0719 01:46:01.806189   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/csi-cephfsplugin-s29g7
I0719 01:46:01.806286   37437 default_network_controller.go:655] Recording add event on pod openshift-cluster-storage-operator/csi-snapshot-controller-operator-bb8d9765b-b24f6
I0719 01:46:01.806290   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/csi-cephfsplugin-s29g7
I0719 01:46:01.806163   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-39-a0
I0719 01:46:01.806296   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-cluster-storage-operator/csi-snapshot-controller-operator-bb8d9765b-b24f6
I0719 01:46:01.806300   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/csi-cephfsplugin-s29g7 in node 00-50-56-8a-e1-e7
I0719 01:46:01.806303   37437 ovn.go:138] Ensuring zone remote for Pod openshift-cluster-storage-operator/csi-snapshot-controller-operator-bb8d9765b-b24f6 in node 00-50-56-8a-5c-ec
I0719 01:46:01.806305   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/csi-cephfsplugin-s29g7 took: 8.026µs
I0719 01:46:01.806310   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/csi-cephfsplugin-s29g7
I0719 01:46:01.806209   37437 default_network_controller.go:655] Recording add event on pod openshift-network-diagnostics/network-check-target-vltnw
I0719 01:46:01.806317   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/rook-ceph-mds-ocs-storagecluster-cephfilesystem-b-c4dc5cd7zkffj
I0719 01:46:01.806320   37437 obj_retry.go:541] Creating *v1.Pod openshift-cluster-storage-operator/csi-snapshot-controller-operator-bb8d9765b-b24f6 took: 17.847µs
I0719 01:46:01.806322   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-network-diagnostics/network-check-target-vltnw
I0719 01:46:01.806303   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-39-a0 in node 00-50-56-8a-39-a0
I0719 01:46:01.806331   37437 obj_retry.go:541] Creating *v1.Pod openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-39-a0 took: 30.683µs
I0719 01:46:01.806291   37437 obj_retry.go:541] Creating *v1.Pod openshift-monitoring/metrics-server-7d47f4cbc-5qp84 took: 32.087µs
I0719 01:46:01.806336   37437 default_network_controller.go:699] Recording success event on pod openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-39-a0
I0719 01:46:01.806339   37437 default_network_controller.go:699] Recording success event on pod openshift-monitoring/metrics-server-7d47f4cbc-5qp84
I0719 01:46:01.806332   37437 ovn.go:138] Ensuring zone remote for Pod openshift-network-diagnostics/network-check-target-vltnw in node 00-50-56-8a-39-a0
I0719 01:46:01.806349   37437 default_network_controller.go:655] Recording add event on pod openshift-machine-config-operator/machine-config-controller-b886dd6cb-6kjkp
I0719 01:46:01.805492   37437 ovn.go:134] Ensuring zone local for Pod openshift-network-operator/iptables-alerter-nh7z8 in node 00-50-56-8a-fb-ea
I0719 01:46:01.806357   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-machine-config-operator/machine-config-controller-b886dd6cb-6kjkp
I0719 01:46:01.806365   37437 ovn.go:138] Ensuring zone remote for Pod openshift-machine-config-operator/machine-config-controller-b886dd6cb-6kjkp in node 00-50-56-8a-39-a0
I0719 01:46:01.806367   37437 obj_retry.go:541] Creating *v1.Pod openshift-network-operator/iptables-alerter-nh7z8 took: 873.427µs
I0719 01:46:01.806379   37437 default_network_controller.go:699] Recording success event on pod openshift-network-operator/iptables-alerter-nh7z8
I0719 01:46:01.806387   37437 obj_retry.go:541] Creating *v1.Pod openshift-machine-config-operator/machine-config-controller-b886dd6cb-6kjkp took: 22.123µs
I0719 01:46:01.806381   37437 model_client.go:381] Update operations generated as: [{Op:update Table:NAT Row:map[external_ip:10.10.25.235 logical_ip:10.130.0.10 options:{GoMap:map[stateless:false]} type:snat] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {03d3a700-3f7e-4be2-88cc-9db25e811673}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.806324   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/rook-ceph-mds-ocs-storagecluster-cephfilesystem-b-c4dc5cd7zkffj
I0719 01:46:01.806403   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/rook-ceph-mds-ocs-storagecluster-cephfilesystem-b-c4dc5cd7zkffj in node 00-50-56-8a-f2-5d
I0719 01:46:01.806412   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:nat Mutator:insert Value:{GoSet:[{GoUUID:03d3a700-3f7e-4be2-88cc-9db25e811673}]}}] Timeout:<nil> Where:[where column _uuid == {26b6d604-e9d3-4544-a4f0-f760e4ff11b6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.806425   37437 default_network_controller.go:655] Recording add event on pod openshift-dns/dns-default-24pdt
I0719 01:46:01.806433   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-dns/dns-default-24pdt
I0719 01:46:01.806441   37437 ovn.go:138] Ensuring zone remote for Pod openshift-dns/dns-default-24pdt in node 00-50-56-8a-e1-e7
I0719 01:46:01.806172   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-monitoring/prometheus-k8s-0
I0719 01:46:01.806456   37437 obj_retry.go:541] Creating *v1.Pod openshift-dns/dns-default-24pdt took: 17µs
I0719 01:46:01.806458   37437 ovn.go:138] Ensuring zone remote for Pod openshift-monitoring/prometheus-k8s-0 in node 00-50-56-8a-f2-5d
I0719 01:46:01.806394   37437 port_cache.go:96] port-cache(openshift-dns_dns-default-qzrlq): added port &{name:openshift-dns_dns-default-qzrlq uuid:4beb4d33-315b-4cb9-a30f-50f639da7d7f logicalSwitch:00-50-56-8a-fb-ea ips:[0xc001578cc0] mac:[10 88 10 130 0 5] expires:{wall:0 ext:0 loc:<nil>}} with IP: [10.130.0.5/23] and MAC: 0a:58:0a:82:00:05
I0719 01:46:01.806471   37437 pods.go:220] [openshift-dns/dns-default-qzrlq] addLogicalPort took 3.765628ms, libovsdb time 1.829382ms
I0719 01:46:01.806478   37437 obj_retry.go:541] Creating *v1.Pod openshift-dns/dns-default-qzrlq took: 3.849966ms
I0719 01:46:01.806482   37437 default_network_controller.go:699] Recording success event on pod openshift-dns/dns-default-qzrlq
I0719 01:46:01.806487   37437 default_network_controller.go:655] Recording add event on pod openshift-etcd/revision-pruner-9-00-50-56-8a-39-a0
I0719 01:46:01.806487   37437 obj_retry.go:541] Creating *v1.Pod openshift-monitoring/prometheus-k8s-0 took: 32.885µs
I0719 01:46:01.806493   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-etcd/revision-pruner-9-00-50-56-8a-39-a0
I0719 01:46:01.806494   37437 default_network_controller.go:699] Recording success event on pod openshift-monitoring/prometheus-k8s-0
I0719 01:46:01.806431   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Switch_Port Row:map[addresses:{GoSet:[0a:58:0a:82:00:0a 10.130.0.10]} options:{GoMap:map[iface-id-ver:f89c28d9-9c2b-4bde-abbc-d06eda08730b requested-chassis:00-50-56-8a-fb-ea]} port_security:{GoSet:[0a:58:0a:82:00:0a 10.130.0.10]} tag_request:{GoSet:[]} type:] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {a89efe1a-8a9e-4458-8f2e-7b5e3036c052}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Switch Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:a89efe1a-8a9e-4458-8f2e-7b5e3036c052}]}}] Timeout:<nil> Where:[where column _uuid == {bc57259c-2feb-4fdd-95c3-dc98eb57f6e4}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Port_Group Row:map[] Rows:[] Columns:[] Mutations:[{Column:ports Mutator:insert Value:{GoSet:[{GoUUID:a89efe1a-8a9e-4458-8f2e-7b5e3036c052}]}}] Timeout:<nil> Where:[where column _uuid == {ecf197d0-8290-4f21-9e31-9dd9f7c67435}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:update Table:NAT Row:map[external_ip:10.10.25.235 logical_ip:10.130.0.10 options:{GoMap:map[stateless:false]} type:snat] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {03d3a700-3f7e-4be2-88cc-9db25e811673}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:nat Mutator:insert Value:{GoSet:[{GoUUID:03d3a700-3f7e-4be2-88cc-9db25e811673}]}}] Timeout:<nil> Where:[where column _uuid == {26b6d604-e9d3-4544-a4f0-f760e4ff11b6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.806501   37437 obj_retry.go:459] Detected object openshift-etcd/revision-pruner-9-00-50-56-8a-39-a0 of type *v1.Pod in terminal state (e.g. completed) during add event: will remove it
I0719 01:46:01.806325   37437 default_network_controller.go:699] Recording success event on pod openshift-cluster-storage-operator/csi-snapshot-controller-operator-bb8d9765b-b24f6
I0719 01:46:01.806511   37437 default_network_controller.go:655] Recording add event on pod openshift-monitoring/prometheus-operator-848d66f7-nx2v2
I0719 01:46:01.806519   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-monitoring/prometheus-operator-848d66f7-nx2v2
I0719 01:46:01.806527   37437 ovn.go:138] Ensuring zone remote for Pod openshift-monitoring/prometheus-operator-848d66f7-nx2v2 in node 00-50-56-8a-39-a0
I0719 01:46:01.806341   37437 default_network_controller.go:655] Recording add event on pod openshift-oauth-apiserver/apiserver-86f656c4dd-2pxdq
I0719 01:46:01.806540   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-oauth-apiserver/apiserver-86f656c4dd-2pxdq
I0719 01:46:01.806542   37437 obj_retry.go:541] Creating *v1.Pod openshift-monitoring/prometheus-operator-848d66f7-nx2v2 took: 17.238µs
I0719 01:46:01.806547   37437 default_network_controller.go:699] Recording success event on pod openshift-monitoring/prometheus-operator-848d66f7-nx2v2
I0719 01:46:01.806356   37437 obj_retry.go:541] Creating *v1.Pod openshift-network-diagnostics/network-check-target-vltnw took: 26.113µs
I0719 01:46:01.806552   37437 default_network_controller.go:655] Recording add event on pod openshift-multus/network-metrics-daemon-gqqpq
I0719 01:46:01.806554   37437 default_network_controller.go:699] Recording success event on pod openshift-network-diagnostics/network-check-target-vltnw
I0719 01:46:01.806558   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-multus/network-metrics-daemon-gqqpq
I0719 01:46:01.806560   37437 default_network_controller.go:655] Recording add event on pod openshift-kni-infra/coredns-00-50-56-8a-5c-ec
I0719 01:46:01.806565   37437 ovn.go:138] Ensuring zone remote for Pod openshift-multus/network-metrics-daemon-gqqpq in node 00-50-56-8a-e1-e7
I0719 01:46:01.806566   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kni-infra/coredns-00-50-56-8a-5c-ec
I0719 01:46:01.806573   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kni-infra/coredns-00-50-56-8a-5c-ec in node 00-50-56-8a-5c-ec
I0719 01:46:01.806577   37437 obj_retry.go:541] Creating *v1.Pod openshift-kni-infra/coredns-00-50-56-8a-5c-ec took: 5.596µs
I0719 01:46:01.806578   37437 obj_retry.go:541] Creating *v1.Pod openshift-multus/network-metrics-daemon-gqqpq took: 14.767µs
I0719 01:46:01.806582   37437 default_network_controller.go:699] Recording success event on pod openshift-kni-infra/coredns-00-50-56-8a-5c-ec
I0719 01:46:01.806584   37437 default_network_controller.go:699] Recording success event on pod openshift-multus/network-metrics-daemon-gqqpq
I0719 01:46:01.806420   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/rook-ceph-mds-ocs-storagecluster-cephfilesystem-b-c4dc5cd7zkffj took: 17.546µs
I0719 01:46:01.806590   37437 default_network_controller.go:655] Recording add event on pod openshift-multus/multus-admission-controller-5cc499c6f4-bngv4
I0719 01:46:01.806548   37437 ovn.go:138] Ensuring zone remote for Pod openshift-oauth-apiserver/apiserver-86f656c4dd-2pxdq in node 00-50-56-8a-39-a0
I0719 01:46:01.806503   37437 default_network_controller.go:655] Recording add event on pod openshift-ingress-canary/ingress-canary-zxwrq
I0719 01:46:01.806388   37437 default_network_controller.go:655] Recording add event on pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-5c-ec
I0719 01:46:01.806642   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-5c-ec
I0719 01:46:01.806662   37437 ovn.go:138] Ensuring zone remote for Pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-5c-ec in node 00-50-56-8a-5c-ec
I0719 01:46:01.806668   37437 obj_retry.go:541] Creating *v1.Pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-5c-ec took: 9.518µs
I0719 01:46:01.806460   37437 default_network_controller.go:699] Recording success event on pod openshift-dns/dns-default-24pdt
I0719 01:46:01.806683   37437 default_network_controller.go:655] Recording add event on pod openshift-kube-apiserver/revision-pruner-8-00-50-56-8a-39-a0
I0719 01:46:01.806691   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kube-apiserver/revision-pruner-8-00-50-56-8a-39-a0
I0719 01:46:01.806698   37437 obj_retry.go:459] Detected object openshift-kube-apiserver/revision-pruner-8-00-50-56-8a-39-a0 of type *v1.Pod in terminal state (e.g. completed) during add event: will remove it
I0719 01:46:01.806590   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/rook-ceph-mds-ocs-storagecluster-cephfilesystem-b-c4dc5cd7zkffj
I0719 01:46:01.806747   37437 address_set.go:613] (9269757a-340c-45bf-828d-361c80cb0226/default-network-controller:Namespace:openshift-kube-apiserver:v4/a4531626005796422843) deleting addresses [10.128.0.7] from address set
I0719 01:46:01.806783   37437 default_network_controller.go:655] Recording add event on pod openshift-cluster-storage-operator/csi-snapshot-webhook-85b445968-9dpmd
I0719 01:46:01.806825   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-cluster-storage-operator/csi-snapshot-webhook-85b445968-9dpmd
I0719 01:46:01.806867   37437 ovn.go:138] Ensuring zone remote for Pod openshift-cluster-storage-operator/csi-snapshot-webhook-85b445968-9dpmd in node 00-50-56-8a-39-a0
I0719 01:46:01.806930   37437 obj_retry.go:541] Creating *v1.Pod openshift-cluster-storage-operator/csi-snapshot-webhook-85b445968-9dpmd took: 66.482µs
I0719 01:46:01.806775   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Address_Set Row:map[] Rows:[] Columns:[] Mutations:[{Column:addresses Mutator:delete Value:{GoSet:[10.128.0.7]}}] Timeout:<nil> Where:[where column _uuid == {9269757a-340c-45bf-828d-361c80cb0226}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.806995   37437 transact.go:42] Configuring OVN: [{Op:mutate Table:Address_Set Row:map[] Rows:[] Columns:[] Mutations:[{Column:addresses Mutator:delete Value:{GoSet:[10.128.0.7]}}] Timeout:<nil> Where:[where column _uuid == {9269757a-340c-45bf-828d-361c80cb0226}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.806973   37437 default_network_controller.go:699] Recording success event on pod openshift-cluster-storage-operator/csi-snapshot-webhook-85b445968-9dpmd
I0719 01:46:01.807084   37437 default_network_controller.go:655] Recording add event on pod openshift-local-storage/diskmaker-manager-vrh5h
I0719 01:46:01.807121   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-local-storage/diskmaker-manager-vrh5h
I0719 01:46:01.806827   37437 port_cache.go:96] port-cache(openshift-ingress-canary_ingress-canary-lsx7x): added port &{name:openshift-ingress-canary_ingress-canary-lsx7x uuid:a89efe1a-8a9e-4458-8f2e-7b5e3036c052 logicalSwitch:00-50-56-8a-fb-ea ips:[0xc001825860] mac:[10 88 10 130 0 10] expires:{wall:0 ext:0 loc:<nil>}} with IP: [10.130.0.10/23] and MAC: 0a:58:0a:82:00:0a
I0719 01:46:01.807153   37437 pods.go:220] [openshift-ingress-canary/ingress-canary-lsx7x] addLogicalPort took 1.600019ms, libovsdb time 390.094µs
I0719 01:46:01.807161   37437 obj_retry.go:541] Creating *v1.Pod openshift-ingress-canary/ingress-canary-lsx7x took: 1.616004ms
I0719 01:46:01.807166   37437 default_network_controller.go:699] Recording success event on pod openshift-ingress-canary/ingress-canary-lsx7x
I0719 01:46:01.807174   37437 default_network_controller.go:655] Recording add event on pod openshift-monitoring/node-exporter-nvqsf
I0719 01:46:01.807181   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-monitoring/node-exporter-nvqsf
I0719 01:46:01.807188   37437 ovn.go:138] Ensuring zone remote for Pod openshift-monitoring/node-exporter-nvqsf in node 00-50-56-8a-f2-5d
I0719 01:46:01.807192   37437 obj_retry.go:541] Creating *v1.Pod openshift-monitoring/node-exporter-nvqsf took: 6.133µs
I0719 01:46:01.807197   37437 default_network_controller.go:699] Recording success event on pod openshift-monitoring/node-exporter-nvqsf
I0719 01:46:01.807202   37437 default_network_controller.go:655] Recording add event on pod openshift-machine-api/metal3-599ff8f4b7-vntm7
I0719 01:46:01.807208   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-machine-api/metal3-599ff8f4b7-vntm7
I0719 01:46:01.806579   37437 address_set.go:613] (d75a7453-719e-42f4-9198-95782be1eecd/default-network-controller:Namespace:openshift-etcd:v4/a1263951348256964356) deleting addresses [10.128.0.6] from address set
I0719 01:46:01.807214   37437 ovn.go:138] Ensuring zone remote for Pod openshift-machine-api/metal3-599ff8f4b7-vntm7 in node 00-50-56-8a-39-a0
I0719 01:46:01.807219   37437 obj_retry.go:541] Creating *v1.Pod openshift-machine-api/metal3-599ff8f4b7-vntm7 took: 6.321µs
I0719 01:46:01.807223   37437 default_network_controller.go:699] Recording success event on pod openshift-machine-api/metal3-599ff8f4b7-vntm7
I0719 01:46:01.807227   37437 default_network_controller.go:655] Recording add event on pod openshift-multus/multus-mqkdb
I0719 01:46:01.807233   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-multus/multus-mqkdb
I0719 01:46:01.807238   37437 ovn.go:138] Ensuring zone remote for Pod openshift-multus/multus-mqkdb in node 00-50-56-8a-f2-5d
I0719 01:46:01.807242   37437 obj_retry.go:541] Creating *v1.Pod openshift-multus/multus-mqkdb took: 5.007µs
I0719 01:46:01.807246   37437 default_network_controller.go:699] Recording success event on pod openshift-multus/multus-mqkdb
I0719 01:46:01.807251   37437 default_network_controller.go:655] Recording add event on pod openshift-etcd/etcd-guard-00-50-56-8a-5c-ec
I0719 01:46:01.807243   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Address_Set Row:map[] Rows:[] Columns:[] Mutations:[{Column:addresses Mutator:delete Value:{GoSet:[10.128.0.6]}}] Timeout:<nil> Where:[where column _uuid == {d75a7453-719e-42f4-9198-95782be1eecd}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.807257   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-etcd/etcd-guard-00-50-56-8a-5c-ec
I0719 01:46:01.807262   37437 ovn.go:138] Ensuring zone remote for Pod openshift-etcd/etcd-guard-00-50-56-8a-5c-ec in node 00-50-56-8a-5c-ec
I0719 01:46:01.807260   37437 transact.go:42] Configuring OVN: [{Op:mutate Table:Address_Set Row:map[] Rows:[] Columns:[] Mutations:[{Column:addresses Mutator:delete Value:{GoSet:[10.128.0.6]}}] Timeout:<nil> Where:[where column _uuid == {d75a7453-719e-42f4-9198-95782be1eecd}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.806394   37437 default_network_controller.go:699] Recording success event on pod openshift-machine-config-operator/machine-config-controller-b886dd6cb-6kjkp
I0719 01:46:01.807295   37437 default_network_controller.go:655] Recording add event on pod openshift-console-operator/console-operator-76c8786869-jr6r2
I0719 01:46:01.807302   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-console-operator/console-operator-76c8786869-jr6r2
I0719 01:46:01.806597   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-multus/multus-admission-controller-5cc499c6f4-bngv4
I0719 01:46:01.807309   37437 ovn.go:138] Ensuring zone remote for Pod openshift-console-operator/console-operator-76c8786869-jr6r2 in node 00-50-56-8a-39-a0
I0719 01:46:01.807314   37437 ovn.go:138] Ensuring zone remote for Pod openshift-multus/multus-admission-controller-5cc499c6f4-bngv4 in node 00-50-56-8a-5c-ec
I0719 01:46:01.807326   37437 obj_retry.go:541] Creating *v1.Pod openshift-console-operator/console-operator-76c8786869-jr6r2 took: 18.687µs
I0719 01:46:01.807328   37437 obj_retry.go:541] Creating *v1.Pod openshift-multus/multus-admission-controller-5cc499c6f4-bngv4 took: 16.765µs
I0719 01:46:01.807331   37437 default_network_controller.go:699] Recording success event on pod openshift-console-operator/console-operator-76c8786869-jr6r2
I0719 01:46:01.807333   37437 default_network_controller.go:699] Recording success event on pod openshift-multus/multus-admission-controller-5cc499c6f4-bngv4
I0719 01:46:01.807336   37437 default_network_controller.go:655] Recording add event on pod openshift-kni-infra/coredns-00-50-56-8a-39-a0
I0719 01:46:01.806613   37437 obj_retry.go:541] Creating *v1.Pod openshift-oauth-apiserver/apiserver-86f656c4dd-2pxdq took: 66.909µs
I0719 01:46:01.807342   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kni-infra/coredns-00-50-56-8a-39-a0
I0719 01:46:01.807349   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kni-infra/coredns-00-50-56-8a-39-a0 in node 00-50-56-8a-39-a0
I0719 01:46:01.807343   37437 default_network_controller.go:699] Recording success event on pod openshift-oauth-apiserver/apiserver-86f656c4dd-2pxdq
I0719 01:46:01.807353   37437 obj_retry.go:541] Creating *v1.Pod openshift-kni-infra/coredns-00-50-56-8a-39-a0 took: 5.459µs
I0719 01:46:01.807356   37437 default_network_controller.go:655] Recording add event on pod openshift-console/console-f7dbc9784-cj9wp
I0719 01:46:01.807362   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-console/console-f7dbc9784-cj9wp
I0719 01:46:01.807365   37437 default_network_controller.go:699] Recording success event on pod openshift-kni-infra/coredns-00-50-56-8a-39-a0
I0719 01:46:01.807368   37437 ovn.go:138] Ensuring zone remote for Pod openshift-console/console-f7dbc9784-cj9wp in node 00-50-56-8a-5c-ec
I0719 01:46:01.807370   37437 default_network_controller.go:655] Recording add event on pod openshift-apiserver-operator/openshift-apiserver-operator-84fc88fd69-mqjqx
I0719 01:46:01.807376   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-apiserver-operator/openshift-apiserver-operator-84fc88fd69-mqjqx
I0719 01:46:01.806674   37437 default_network_controller.go:699] Recording success event on pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-5c-ec
I0719 01:46:01.807381   37437 obj_retry.go:541] Creating *v1.Pod openshift-console/console-f7dbc9784-cj9wp took: 14.543µs
I0719 01:46:01.807383   37437 ovn.go:138] Ensuring zone remote for Pod openshift-apiserver-operator/openshift-apiserver-operator-84fc88fd69-mqjqx in node 00-50-56-8a-5c-ec
I0719 01:46:01.807386   37437 default_network_controller.go:699] Recording success event on pod openshift-console/console-f7dbc9784-cj9wp
I0719 01:46:01.807392   37437 default_network_controller.go:655] Recording add event on pod openshift-controller-manager-operator/openshift-controller-manager-operator-cf8f9956c-x6xn5
I0719 01:46:01.807398   37437 obj_retry.go:541] Creating *v1.Pod openshift-apiserver-operator/openshift-apiserver-operator-84fc88fd69-mqjqx took: 15.814µs
I0719 01:46:01.807401   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-controller-manager-operator/openshift-controller-manager-operator-cf8f9956c-x6xn5
I0719 01:46:01.807403   37437 default_network_controller.go:699] Recording success event on pod openshift-apiserver-operator/openshift-apiserver-operator-84fc88fd69-mqjqx
I0719 01:46:01.807282   37437 obj_retry.go:541] Creating *v1.Pod openshift-etcd/etcd-guard-00-50-56-8a-5c-ec took: 19.163µs
I0719 01:46:01.807410   37437 ovn.go:138] Ensuring zone remote for Pod openshift-controller-manager-operator/openshift-controller-manager-operator-cf8f9956c-x6xn5 in node 00-50-56-8a-5c-ec
I0719 01:46:01.807414   37437 default_network_controller.go:699] Recording success event on pod openshift-etcd/etcd-guard-00-50-56-8a-5c-ec
I0719 01:46:01.806614   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-ingress-canary/ingress-canary-zxwrq
I0719 01:46:01.807426   37437 ovn.go:138] Ensuring zone remote for Pod openshift-ingress-canary/ingress-canary-zxwrq in node 00-50-56-8a-f2-5d
I0719 01:46:01.807436   37437 obj_retry.go:541] Creating *v1.Pod openshift-controller-manager-operator/openshift-controller-manager-operator-cf8f9956c-x6xn5 took: 27.745µs
I0719 01:46:01.807445   37437 default_network_controller.go:699] Recording success event on pod openshift-controller-manager-operator/openshift-controller-manager-operator-cf8f9956c-x6xn5
I0719 01:46:01.807450   37437 default_network_controller.go:655] Recording add event on pod openshift-local-storage/diskmaker-manager-wj2h7
I0719 01:46:01.807456   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-local-storage/diskmaker-manager-wj2h7
I0719 01:46:01.807463   37437 ovn.go:138] Ensuring zone remote for Pod openshift-local-storage/diskmaker-manager-wj2h7 in node 00-50-56-8a-f2-5d
I0719 01:46:01.807440   37437 ovn.go:138] Ensuring zone remote for Pod openshift-local-storage/diskmaker-manager-vrh5h in node 00-50-56-8a-e1-e7
I0719 01:46:01.807516   37437 obj_retry.go:541] Creating *v1.Pod openshift-local-storage/diskmaker-manager-vrh5h took: 370.104µs
I0719 01:46:01.807541   37437 default_network_controller.go:699] Recording success event on pod openshift-local-storage/diskmaker-manager-vrh5h
I0719 01:46:01.807414   37437 default_network_controller.go:655] Recording add event on pod openshift-image-registry/node-ca-lfxb8
I0719 01:46:01.807587   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-image-registry/node-ca-lfxb8
I0719 01:46:01.807612   37437 ovn.go:134] Ensuring zone local for Pod openshift-image-registry/node-ca-lfxb8 in node 00-50-56-8a-fb-ea
I0719 01:46:01.807640   37437 obj_retry.go:541] Creating *v1.Pod openshift-image-registry/node-ca-lfxb8 took: 27.792µs
I0719 01:46:01.807477   37437 obj_retry.go:541] Creating *v1.Pod openshift-local-storage/diskmaker-manager-wj2h7 took: 15.048µs
I0719 01:46:01.807680   37437 default_network_controller.go:699] Recording success event on pod openshift-local-storage/diskmaker-manager-wj2h7
I0719 01:46:01.807687   37437 default_network_controller.go:655] Recording add event on pod openshift-monitoring/prometheus-k8s-1
I0719 01:46:01.807694   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-monitoring/prometheus-k8s-1
I0719 01:46:01.807702   37437 ovn.go:138] Ensuring zone remote for Pod openshift-monitoring/prometheus-k8s-1 in node 00-50-56-8a-e1-e7
I0719 01:46:01.807723   37437 obj_retry.go:541] Creating *v1.Pod openshift-monitoring/prometheus-k8s-1 took: 23.139µs
I0719 01:46:01.807728   37437 default_network_controller.go:699] Recording success event on pod openshift-monitoring/prometheus-k8s-1
I0719 01:46:01.807734   37437 default_network_controller.go:655] Recording add event on pod openshift-network-node-identity/network-node-identity-tzcq8
I0719 01:46:01.807739   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-network-node-identity/network-node-identity-tzcq8
I0719 01:46:01.807745   37437 ovn.go:138] Ensuring zone remote for Pod openshift-network-node-identity/network-node-identity-tzcq8 in node 00-50-56-8a-44-52
I0719 01:46:01.807750   37437 obj_retry.go:541] Creating *v1.Pod openshift-network-node-identity/network-node-identity-tzcq8 took: 5.724µs
I0719 01:46:01.807753   37437 default_network_controller.go:699] Recording success event on pod openshift-network-node-identity/network-node-identity-tzcq8
I0719 01:46:01.807673   37437 default_network_controller.go:699] Recording success event on pod openshift-image-registry/node-ca-lfxb8
I0719 01:46:01.807823   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/ocs-client-operator-console-6fdbfcd95-jhcss
I0719 01:46:01.807863   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/ocs-client-operator-console-6fdbfcd95-jhcss
I0719 01:46:01.807894   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/ocs-client-operator-console-6fdbfcd95-jhcss in node 00-50-56-8a-f2-5d
I0719 01:46:01.807936   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/ocs-client-operator-console-6fdbfcd95-jhcss took: 44.047µs
I0719 01:46:01.807965   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/ocs-client-operator-console-6fdbfcd95-jhcss
I0719 01:46:01.808028   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/csi-rbdplugin-provisioner-5dcc45fbf4-9svs4
I0719 01:46:01.808078   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/csi-rbdplugin-provisioner-5dcc45fbf4-9svs4
I0719 01:46:01.808114   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/csi-rbdplugin-provisioner-5dcc45fbf4-9svs4 in node 00-50-56-8a-e1-e7
I0719 01:46:01.808156   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/csi-rbdplugin-provisioner-5dcc45fbf4-9svs4 took: 43.678µs
I0719 01:46:01.808180   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/csi-rbdplugin-provisioner-5dcc45fbf4-9svs4
I0719 01:46:01.808210   37437 default_network_controller.go:655] Recording add event on pod openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-5c-ec
I0719 01:46:01.808242   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-5c-ec
I0719 01:46:01.808271   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-5c-ec in node 00-50-56-8a-5c-ec
I0719 01:46:01.808298   37437 obj_retry.go:541] Creating *v1.Pod openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-5c-ec took: 28.738µs
I0719 01:46:01.808332   37437 default_network_controller.go:699] Recording success event on pod openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-5c-ec
I0719 01:46:01.808362   37437 default_network_controller.go:655] Recording add event on pod openshift-ovn-kubernetes/ovnkube-control-plane-58975cd9fd-mz4pv
I0719 01:46:01.808394   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-ovn-kubernetes/ovnkube-control-plane-58975cd9fd-mz4pv
I0719 01:46:01.808426   37437 ovn.go:138] Ensuring zone remote for Pod openshift-ovn-kubernetes/ovnkube-control-plane-58975cd9fd-mz4pv in node 00-50-56-8a-39-a0
I0719 01:46:01.808456   37437 obj_retry.go:541] Creating *v1.Pod openshift-ovn-kubernetes/ovnkube-control-plane-58975cd9fd-mz4pv took: 30.744µs
I0719 01:46:01.807440   37437 obj_retry.go:541] Creating *v1.Pod openshift-ingress-canary/ingress-canary-zxwrq took: 15.075µs
I0719 01:46:01.805458   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-dns/node-resolver-tjmrc
I0719 01:46:01.807419   37437 default_network_controller.go:655] Recording add event on pod openshift-ovn-kubernetes/ovnkube-node-62ccc
I0719 01:46:01.807629   37437 ovs.go:162] Exec(29): stdout: "system\n"
I0719 01:46:01.808578   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-ovn-kubernetes/ovnkube-node-62ccc
I0719 01:46:01.808596   37437 ovn.go:138] Ensuring zone remote for Pod openshift-ovn-kubernetes/ovnkube-node-62ccc in node 00-50-56-8a-e1-e7
I0719 01:46:01.808604   37437 obj_retry.go:541] Creating *v1.Pod openshift-ovn-kubernetes/ovnkube-node-62ccc took: 10.845µs
I0719 01:46:01.808608   37437 default_network_controller.go:699] Recording success event on pod openshift-ovn-kubernetes/ovnkube-node-62ccc
I0719 01:46:01.808585   37437 ovs.go:163] Exec(29): stderr: ""
I0719 01:46:01.808650   37437 ovs.go:159] Exec(30): /usr/bin/ovs-vsctl --timeout=15 get Interface b05109fd-71da-455e-8873-6ea210676041 Type
I0719 01:46:01.808505   37437 default_network_controller.go:699] Recording success event on pod openshift-ovn-kubernetes/ovnkube-control-plane-58975cd9fd-mz4pv
I0719 01:46:01.808698   37437 default_network_controller.go:655] Recording add event on pod openshift-kube-scheduler/openshift-kube-scheduler-guard-00-50-56-8a-5c-ec
I0719 01:46:01.808705   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kube-scheduler/openshift-kube-scheduler-guard-00-50-56-8a-5c-ec
I0719 01:46:01.808512   37437 default_network_controller.go:699] Recording success event on pod openshift-ingress-canary/ingress-canary-zxwrq
I0719 01:46:01.808553   37437 ovn.go:138] Ensuring zone remote for Pod openshift-dns/node-resolver-tjmrc in node 00-50-56-8a-39-a0
I0719 01:46:01.808726   37437 obj_retry.go:541] Creating *v1.Pod openshift-dns/node-resolver-tjmrc took: 174.484µs
I0719 01:46:01.808731   37437 default_network_controller.go:699] Recording success event on pod openshift-dns/node-resolver-tjmrc
I0719 01:46:01.808737   37437 default_network_controller.go:655] Recording add event on pod openshift-authentication-operator/authentication-operator-68795c8768-8rvtz
I0719 01:46:01.808744   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-authentication-operator/authentication-operator-68795c8768-8rvtz
I0719 01:46:01.808750   37437 ovn.go:138] Ensuring zone remote for Pod openshift-authentication-operator/authentication-operator-68795c8768-8rvtz in node 00-50-56-8a-5c-ec
I0719 01:46:01.808769   37437 obj_retry.go:541] Creating *v1.Pod openshift-authentication-operator/authentication-operator-68795c8768-8rvtz took: 20.538µs
I0719 01:46:01.808774   37437 default_network_controller.go:699] Recording success event on pod openshift-authentication-operator/authentication-operator-68795c8768-8rvtz
I0719 01:46:01.808779   37437 default_network_controller.go:655] Recording add event on pod openshift-marketplace/community-operators-wgnxc
I0719 01:46:01.808712   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kube-scheduler/openshift-kube-scheduler-guard-00-50-56-8a-5c-ec in node 00-50-56-8a-5c-ec
I0719 01:46:01.808784   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-marketplace/community-operators-wgnxc
I0719 01:46:01.808790   37437 ovn.go:138] Ensuring zone remote for Pod openshift-marketplace/community-operators-wgnxc in node 00-50-56-8a-39-a0
I0719 01:46:01.808804   37437 obj_retry.go:541] Creating *v1.Pod openshift-marketplace/community-operators-wgnxc took: 15.102µs
I0719 01:46:01.808808   37437 default_network_controller.go:699] Recording success event on pod openshift-marketplace/community-operators-wgnxc
I0719 01:46:01.808808   37437 obj_retry.go:541] Creating *v1.Pod openshift-kube-scheduler/openshift-kube-scheduler-guard-00-50-56-8a-5c-ec took: 96.824µs
I0719 01:46:01.808813   37437 default_network_controller.go:655] Recording add event on pod openshift-storage/rook-ceph-rgw-ocs-storagecluster-cephobjectstore-a-766774cx8zqw
I0719 01:46:01.808814   37437 default_network_controller.go:699] Recording success event on pod openshift-kube-scheduler/openshift-kube-scheduler-guard-00-50-56-8a-5c-ec
I0719 01:46:01.808820   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-storage/rook-ceph-rgw-ocs-storagecluster-cephobjectstore-a-766774cx8zqw
I0719 01:46:01.808821   37437 default_network_controller.go:655] Recording add event on pod openshift-kube-storage-version-migrator-operator/kube-storage-version-migrator-operator-75d5d9b9f8-lj6w5
I0719 01:46:01.808826   37437 ovn.go:138] Ensuring zone remote for Pod openshift-storage/rook-ceph-rgw-ocs-storagecluster-cephobjectstore-a-766774cx8zqw in node 00-50-56-8a-f2-5d
I0719 01:46:01.808828   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-kube-storage-version-migrator-operator/kube-storage-version-migrator-operator-75d5d9b9f8-lj6w5
I0719 01:46:01.808835   37437 ovn.go:138] Ensuring zone remote for Pod openshift-kube-storage-version-migrator-operator/kube-storage-version-migrator-operator-75d5d9b9f8-lj6w5 in node 00-50-56-8a-5c-ec
I0719 01:46:01.808841   37437 obj_retry.go:541] Creating *v1.Pod openshift-storage/rook-ceph-rgw-ocs-storagecluster-cephobjectstore-a-766774cx8zqw took: 16.151µs
I0719 01:46:01.808845   37437 default_network_controller.go:699] Recording success event on pod openshift-storage/rook-ceph-rgw-ocs-storagecluster-cephobjectstore-a-766774cx8zqw
I0719 01:46:01.808850   37437 default_network_controller.go:655] Recording add event on pod openshift-etcd-operator/etcd-operator-6c7489b895-5tql8
I0719 01:46:01.808850   37437 obj_retry.go:541] Creating *v1.Pod openshift-kube-storage-version-migrator-operator/kube-storage-version-migrator-operator-75d5d9b9f8-lj6w5 took: 16.057µs
I0719 01:46:01.808859   37437 default_network_controller.go:699] Recording success event on pod openshift-kube-storage-version-migrator-operator/kube-storage-version-migrator-operator-75d5d9b9f8-lj6w5
I0719 01:46:01.808865   37437 default_network_controller.go:655] Recording add event on pod openshift-multus/multus-additional-cni-plugins-pjk5m
I0719 01:46:01.808866   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-etcd-operator/etcd-operator-6c7489b895-5tql8
I0719 01:46:01.808871   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-multus/multus-additional-cni-plugins-pjk5m
I0719 01:46:01.808876   37437 ovn.go:138] Ensuring zone remote for Pod openshift-etcd-operator/etcd-operator-6c7489b895-5tql8 in node 00-50-56-8a-5c-ec
I0719 01:46:01.808877   37437 ovn.go:138] Ensuring zone remote for Pod openshift-multus/multus-additional-cni-plugins-pjk5m in node 00-50-56-8a-44-52
I0719 01:46:01.808882   37437 obj_retry.go:541] Creating *v1.Pod openshift-multus/multus-additional-cni-plugins-pjk5m took: 6.434µs
I0719 01:46:01.808886   37437 default_network_controller.go:699] Recording success event on pod openshift-multus/multus-additional-cni-plugins-pjk5m
I0719 01:46:01.808891   37437 default_network_controller.go:655] Recording add event on pod openshift-machine-api/machine-api-operator-5cb7d5868-9p8wr
I0719 01:46:01.808895   37437 obj_retry.go:541] Creating *v1.Pod openshift-etcd-operator/etcd-operator-6c7489b895-5tql8 took: 21.4µs
I0719 01:46:01.808901   37437 default_network_controller.go:699] Recording success event on pod openshift-etcd-operator/etcd-operator-6c7489b895-5tql8
I0719 01:46:01.808906   37437 default_network_controller.go:655] Recording add event on pod openshift-marketplace/redhat-marketplace-hbf7g
I0719 01:46:01.808912   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-marketplace/redhat-marketplace-hbf7g
I0719 01:46:01.808918   37437 ovn.go:138] Ensuring zone remote for Pod openshift-marketplace/redhat-marketplace-hbf7g in node 00-50-56-8a-39-a0
I0719 01:46:01.808933   37437 obj_retry.go:541] Creating *v1.Pod openshift-marketplace/redhat-marketplace-hbf7g took: 15.137µs
I0719 01:46:01.808939   37437 default_network_controller.go:699] Recording success event on pod openshift-marketplace/redhat-marketplace-hbf7g
I0719 01:46:01.808944   37437 default_network_controller.go:655] Recording add event on pod openshift-machine-config-operator/machine-config-server-968nk
I0719 01:46:01.808950   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-machine-config-operator/machine-config-server-968nk
I0719 01:46:01.808956   37437 ovn.go:138] Ensuring zone remote for Pod openshift-machine-config-operator/machine-config-server-968nk in node 00-50-56-8a-39-a0
I0719 01:46:01.808960   37437 obj_retry.go:541] Creating *v1.Pod openshift-machine-config-operator/machine-config-server-968nk took: 5.356µs
I0719 01:46:01.808964   37437 default_network_controller.go:699] Recording success event on pod openshift-machine-config-operator/machine-config-server-968nk
I0719 01:46:01.808896   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-machine-api/machine-api-operator-5cb7d5868-9p8wr
I0719 01:46:01.808969   37437 default_network_controller.go:655] Recording add event on pod openshift-multus/multus-additional-cni-plugins-b5t42
I0719 01:46:01.808973   37437 ovn.go:138] Ensuring zone remote for Pod openshift-machine-api/machine-api-operator-5cb7d5868-9p8wr in node 00-50-56-8a-39-a0
I0719 01:46:01.808975   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-multus/multus-additional-cni-plugins-b5t42
I0719 01:46:01.808988   37437 ovn.go:134] Ensuring zone local for Pod openshift-multus/multus-additional-cni-plugins-b5t42 in node 00-50-56-8a-fb-ea
I0719 01:46:01.808994   37437 obj_retry.go:541] Creating *v1.Pod openshift-multus/multus-additional-cni-plugins-b5t42 took: 13.094µs
I0719 01:46:01.808995   37437 obj_retry.go:541] Creating *v1.Pod openshift-machine-api/machine-api-operator-5cb7d5868-9p8wr took: 23.474µs
I0719 01:46:01.808998   37437 default_network_controller.go:699] Recording success event on pod openshift-multus/multus-additional-cni-plugins-b5t42
I0719 01:46:01.808999   37437 default_network_controller.go:699] Recording success event on pod openshift-machine-api/machine-api-operator-5cb7d5868-9p8wr
I0719 01:46:01.809003   37437 default_network_controller.go:655] Recording add event on pod openshift-dns/node-resolver-dpn9t
I0719 01:46:01.809009   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-dns/node-resolver-dpn9t
I0719 01:46:01.809015   37437 ovn.go:138] Ensuring zone remote for Pod openshift-dns/node-resolver-dpn9t in node 00-50-56-8a-e1-e7
I0719 01:46:01.809019   37437 obj_retry.go:541] Creating *v1.Pod openshift-dns/node-resolver-dpn9t took: 5.169µs
I0719 01:46:01.809023   37437 default_network_controller.go:699] Recording success event on pod openshift-dns/node-resolver-dpn9t
I0719 01:46:01.809027   37437 default_network_controller.go:655] Recording add event on pod openshift-ovn-kubernetes/ovnkube-node-568wp
I0719 01:46:01.809032   37437 obj_retry.go:502] Add event received for *v1.Pod openshift-ovn-kubernetes/ovnkube-node-568wp
I0719 01:46:01.809037   37437 ovn.go:138] Ensuring zone remote for Pod openshift-ovn-kubernetes/ovnkube-node-568wp in node 00-50-56-8a-44-52
I0719 01:46:01.809043   37437 obj_retry.go:541] Creating *v1.Pod openshift-ovn-kubernetes/ovnkube-node-568wp took: 5.138µs
I0719 01:46:01.809046   37437 default_network_controller.go:699] Recording success event on pod openshift-ovn-kubernetes/ovnkube-node-568wp
I0719 01:46:01.809056   37437 factory.go:988] Added *v1.Pod event handler 3
I0719 01:46:01.809088   37437 admin_network_policy_controller.go:124] Setting up event handlers for Admin Network Policy
I0719 01:46:01.809135   37437 admin_network_policy_controller.go:142] Setting up event handlers for Baseline Admin Network Policy
I0719 01:46:01.809141   37437 obj_retry.go:427] periodicallyRetryResources: Retry channel got triggered: retrying failed objects of type *v1.Pod
I0719 01:46:01.809166   37437 admin_network_policy_controller.go:159] Setting up event handlers for Namespaces in Admin Network Policy controller
I0719 01:46:01.809239   37437 admin_network_policy_controller.go:175] Setting up event handlers for Pods in Admin Network Policy controller
I0719 01:46:01.809242   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-apiserver-operator
I0719 01:46:01.809290   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-config
I0719 01:46:01.809303   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-dns
I0719 01:46:01.809309   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-image-registry
I0719 01:46:01.809314   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-ingress
I0719 01:46:01.809309   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/rook-ceph-rgw-ocs-storagecluster-cephobjectstore-a-766774cx8zqw
I0719 01:46:01.809319   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-cluster-samples-operator
I0719 01:46:01.809323   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-kube-apiserver
I0719 01:46:01.809327   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kube-apiserver/kube-apiserver-guard-00-50-56-8a-44-52
I0719 01:46:01.809328   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-nutanix-infra
I0719 01:46:01.809341   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-cloud-controller-manager
I0719 01:46:01.809350   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-config-operator
I0719 01:46:01.809354   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller kube-node-lease
I0719 01:46:01.809358   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-cloud-network-config-controller
I0719 01:46:01.809363   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-cluster-csi-drivers
I0719 01:46:01.809370   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-cluster-machine-approver
I0719 01:46:01.809374   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-kni-infra
I0719 01:46:01.809379   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-kube-controller-manager-operator
I0719 01:46:01.809383   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-dns-operator
I0719 01:46:01.809383   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/csi-rbdplugin-provisioner-5dcc45fbf4-9svs4
I0719 01:46:01.809388   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-insights
I0719 01:46:01.809399   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-kube-scheduler-operator
I0719 01:46:01.809405   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller kube-public
I0719 01:46:01.809405   37437 admin_network_policy_controller.go:191] Setting up event handlers for Nodes in Admin Network Policy controller
I0719 01:46:01.809409   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-cloud-platform-infra
I0719 01:46:01.809414   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-cluster-version
I0719 01:46:01.809418   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-ingress-canary
I0719 01:46:01.809423   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-vsphere-infra
I0719 01:46:01.809427   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-etcd-operator
I0719 01:46:01.809452   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller kube-system
I0719 01:46:01.809460   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-authentication-operator
I0719 01:46:01.809394   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-ovn-kubernetes/ovnkube-node-7pmvf
I0719 01:46:01.809465   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-host-network
I0719 01:46:01.809470   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-infra
I0719 01:46:01.809470   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-44-52
I0719 01:46:01.809476   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-machine-config-operator
I0719 01:46:01.809479   37437 admin_network_policy_controller.go:549] Adding Node in Admin Network Policy controller 00-50-56-8a-39-a0
I0719 01:46:01.809487   37437 admin_network_policy_controller.go:549] Adding Node in Admin Network Policy controller 00-50-56-8a-44-52
I0719 01:46:01.809492   37437 admin_network_policy_controller.go:549] Adding Node in Admin Network Policy controller 00-50-56-8a-5c-ec
I0719 01:46:01.809496   37437 admin_network_policy_controller.go:549] Adding Node in Admin Network Policy controller 00-50-56-8a-e1-e7
I0719 01:46:01.809500   37437 admin_network_policy_controller.go:549] Adding Node in Admin Network Policy controller 00-50-56-8a-f2-5d
I0719 01:46:01.809504   37437 admin_network_policy_controller.go:549] Adding Node in Admin Network Policy controller 00-50-56-8a-fb-ea
I0719 01:46:01.809479   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-monitoring/monitoring-plugin-6f457fd4b8-pqp4m
I0719 01:46:01.809512   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-machine-config-operator/machine-config-daemon-4kr96
I0719 01:46:01.809518   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kube-scheduler/revision-pruner-6-00-50-56-8a-44-52
I0719 01:46:01.809521   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kube-scheduler/revision-pruner-6-00-50-56-8a-5c-ec
I0719 01:46:01.809529   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-machine-api/control-plane-machine-set-operator-77bcc698b6-wvkdb
I0719 01:46:01.809533   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-f2-5d
I0719 01:46:01.809538   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-multus/multus-additional-cni-plugins-rtmj7
I0719 01:46:01.809542   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-multus/network-metrics-daemon-fslb2
I0719 01:46:01.809549   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-console/console-c675c654b-rw8cg
I0719 01:46:01.809554   37437 admin_network_policy_controller.go:218] Starting controller default-network-controller
I0719 01:46:01.809561   37437 admin_network_policy_controller.go:221] Waiting for informer caches to sync
I0719 01:46:01.809571   37437 shared_informer.go:311] Waiting for caches to sync for default-network-controller
I0719 01:46:01.809577   37437 shared_informer.go:318] Caches are synced for default-network-controller
I0719 01:46:01.809581   37437 admin_network_policy_controller.go:228] Repairing Admin Network Policies
I0719 01:46:01.809556   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-etcd-operator/etcd-operator-6c7489b895-5tql8
I0719 01:46:01.809630   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/rook-ceph-osd-0-6d5dbb5f-24hfr
I0719 01:46:01.809636   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-monitoring/node-exporter-7m7sg
I0719 01:46:01.809641   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-network-diagnostics/network-check-source-b89b7bb96-lpzlv
I0719 01:46:01.809646   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/rook-ceph-exporter-00-50-56-8a-e1-e7-558dfbd955-jzh65
I0719 01:46:01.809650   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-monitoring/thanos-querier-68bf686489-9cctf
I0719 01:46:01.809655   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-multus/network-metrics-daemon-t4g2p
I0719 01:46:01.809659   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-image-registry/node-ca-wgn2l
I0719 01:46:01.809663   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-network-diagnostics/network-check-target-h9cbr
I0719 01:46:01.809667   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-5c-ec
I0719 01:46:01.809672   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-e1-e7
I0719 01:46:01.809681   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-ovn-kubernetes/ovnkube-control-plane-58975cd9fd-mz4pv
I0719 01:46:01.809687   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/odf-console-b7ccd85c5-84cnv
I0719 01:46:01.809692   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kube-apiserver/revision-pruner-8-00-50-56-8a-44-52
I0719 01:46:01.809697   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kube-apiserver/revision-pruner-8-00-50-56-8a-5c-ec
I0719 01:46:01.809675   37437 model_client.go:381] Update operations generated as: [{Op:update Table:ACL Row:map[action:allow-related direction:to-lport external_ids:{GoMap:map[direction:Ingress k8s.ovn.org/id:default-network-controller:NetpolDefault:allow-hairpinning:Ingress k8s.ovn.org/name:allow-hairpinning k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:NetpolDefault]} log:false match:ip4.src == 169.254.169.5 meter:{GoSet:[acl-logging]} name:{GoSet:[]} options:{GoMap:map[]} priority:1001 severity:{GoSet:[]} tier:2] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {82d46076-35f0-4356-90c2-727689df8020}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.809701   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kube-scheduler/openshift-kube-scheduler-guard-00-50-56-8a-5c-ec
I0719 01:46:01.809707   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-marketplace/redhat-marketplace-hbf7g
I0719 01:46:01.809711   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-multus/multus-25bkq
I0719 01:46:01.809718   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-multus/multus-ltqfr
I0719 01:46:01.809727   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-network-operator/network-operator-6967d44d7-4wwpm
I0719 01:46:01.809731   37437 repair.go:29] Repairing admin network policies took 145.551µs
I0719 01:46:01.809736   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-cluster-node-tuning-operator/tuned-5pn2c
I0719 01:46:01.809741   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-dns/node-resolver-nsvs6
I0719 01:46:01.809750   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-image-registry/image-pruner-28689120-2bnxj
I0719 01:46:01.809481   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-ingress-operator
I0719 01:46:01.809758   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-multus/network-metrics-daemon-hxzdd
I0719 01:46:01.809769   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-monitoring
I0719 01:46:01.809776   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kni-infra/coredns-00-50-56-8a-fb-ea
I0719 01:46:01.809777   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-node
I0719 01:46:01.809786   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-oauth-apiserver
I0719 01:46:01.809792   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-ovirt-infra
I0719 01:46:01.809797   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-storage
I0719 01:46:01.809801   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-apiserver
I0719 01:46:01.809805   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-console
I0719 01:46:01.809809   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-console-operator
I0719 01:46:01.809813   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-kube-storage-version-migrator
I0719 01:46:01.809818   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-cloud-credential-operator
I0719 01:46:01.809822   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-cluster-storage-operator
I0719 01:46:01.809826   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-console-user-settings
I0719 01:46:01.809830   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-kube-controller-manager
I0719 01:46:01.809833   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-multus/network-metrics-daemon-bqt8s
I0719 01:46:01.809817   37437 model_client.go:381] Update operations generated as: [{Op:update Table:ACL Row:map[action:allow-related direction:from-lport external_ids:{GoMap:map[direction:Egress k8s.ovn.org/id:default-network-controller:NetpolDefault:allow-hairpinning:Egress k8s.ovn.org/name:allow-hairpinning k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:NetpolDefault]} log:false match:ip4.src == 169.254.169.5 meter:{GoSet:[acl-logging]} name:{GoSet:[]} options:{GoMap:map[apply-after-lb:true]} priority:1001 severity:{GoSet:[]} tier:2] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {6dbee1db-5811-4cf0-99d8-c7039e875d90}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.809842   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-marketplace/marketplace-operator-59c7f5b7bd-8pd2c
I0719 01:46:01.809845   37437 repair.go:104] Repairing baseline admin network policies took 107.978µs
I0719 01:46:01.809847   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-monitoring/node-exporter-7xrvj
I0719 01:46:01.809852   37437 admin_network_policy_controller.go:241] Starting Admin Network Policy workers
I0719 01:46:01.809863   37437 admin_network_policy_controller.go:252] Starting Baseline Admin Network Policy workers
I0719 01:46:01.809864   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Port_Group Row:map[] Rows:[] Columns:[] Mutations:[{Column:acls Mutator:insert Value:{GoSet:[{GoUUID:82d46076-35f0-4356-90c2-727689df8020} {GoUUID:6dbee1db-5811-4cf0-99d8-c7039e875d90}]}}] Timeout:<nil> Where:[where column _uuid == {cfdb2406-27d3-4869-bb58-7f65e5a726d7}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.809875   37437 admin_network_policy_controller.go:263] Starting Namespace Admin Network Policy workers
I0719 01:46:01.809883   37437 admin_network_policy_controller.go:274] Starting Pod Admin Network Policy workers
I0719 01:46:01.809892   37437 admin_network_policy_controller.go:285] Starting Node Admin Network Policy workers
I0719 01:46:01.809878   37437 transact.go:42] Configuring OVN: [{Op:update Table:ACL Row:map[action:allow-related direction:to-lport external_ids:{GoMap:map[direction:Ingress k8s.ovn.org/id:default-network-controller:NetpolDefault:allow-hairpinning:Ingress k8s.ovn.org/name:allow-hairpinning k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:NetpolDefault]} log:false match:ip4.src == 169.254.169.5 meter:{GoSet:[acl-logging]} name:{GoSet:[]} options:{GoMap:map[]} priority:1001 severity:{GoSet:[]} tier:2] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {82d46076-35f0-4356-90c2-727689df8020}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:update Table:ACL Row:map[action:allow-related direction:from-lport external_ids:{GoMap:map[direction:Egress k8s.ovn.org/id:default-network-controller:NetpolDefault:allow-hairpinning:Egress k8s.ovn.org/name:allow-hairpinning k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:NetpolDefault]} log:false match:ip4.src == 169.254.169.5 meter:{GoSet:[acl-logging]} name:{GoSet:[]} options:{GoMap:map[apply-after-lb:true]} priority:1001 severity:{GoSet:[]} tier:2] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {6dbee1db-5811-4cf0-99d8-c7039e875d90}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Port_Group Row:map[] Rows:[] Columns:[] Mutations:[{Column:acls Mutator:insert Value:{GoSet:[{GoUUID:82d46076-35f0-4356-90c2-727689df8020} {GoUUID:6dbee1db-5811-4cf0-99d8-c7039e875d90}]}}] Timeout:<nil> Where:[where column _uuid == {cfdb2406-27d3-4869-bb58-7f65e5a726d7}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.809971   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-apiserver-operator in Admin Network Policy controller
I0719 01:46:01.809994   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-apiserver-operator Admin Network Policy controller: took 23.267µs
I0719 01:46:01.810005   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-config in Admin Network Policy controller
I0719 01:46:01.810009   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-config Admin Network Policy controller: took 3.754µs
I0719 01:46:01.809853   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-controller-manager/controller-manager-5c7f9f9d47-kxpdr
I0719 01:46:01.810015   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-dns in Admin Network Policy controller
I0719 01:46:01.810019   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-dns Admin Network Policy controller: took 3.773µs
I0719 01:46:01.810019   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kni-infra/keepalived-00-50-56-8a-39-a0
I0719 01:46:01.810025   37437 admin_network_policy_node.go:55] Processing sync for Node 00-50-56-8a-39-a0 in Admin Network Policy controller
I0719 01:46:01.810034   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/rook-ceph-exporter-00-50-56-8a-f2-5d-785d485f5d-v5k84
I0719 01:46:01.810044   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-cloud-controller-manager-operator/cluster-cloud-controller-manager-operator-7f55545d59-r8j8z
I0719 01:46:01.810055   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-cluster-storage-operator/csi-snapshot-controller-794ff44f88-5jz8j
I0719 01:46:01.810033   37437 admin_network_policy_node.go:58] Finished syncing Node 00-50-56-8a-39-a0 Admin Network Policy controller: took 7.799µs
I0719 01:46:01.809835   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-local-storage
I0719 01:46:01.810071   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-openstack-infra
I0719 01:46:01.810073   37437 admin_network_policy_node.go:55] Processing sync for Node 00-50-56-8a-44-52 in Admin Network Policy controller
I0719 01:46:01.810076   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-user-workload-monitoring
I0719 01:46:01.810081   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-authentication
I0719 01:46:01.810061   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-network-operator/iptables-alerter-6s78n
I0719 01:46:01.810087   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-cloud-controller-manager-operator
I0719 01:46:01.810090   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-network-operator/iptables-alerter-b72gh
I0719 01:46:01.810080   37437 admin_network_policy_node.go:58] Finished syncing Node 00-50-56-8a-44-52 Admin Network Policy controller: took 8.473µs
I0719 01:46:01.810097   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-operator-lifecycle-manager/packageserver-6bf7d58455-gh44f
I0719 01:46:01.810101   37437 admin_network_policy_node.go:55] Processing sync for Node 00-50-56-8a-5c-ec in Admin Network Policy controller
I0719 01:46:01.810092   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-kube-apiserver-operator
I0719 01:46:01.810106   37437 admin_network_policy_node.go:58] Finished syncing Node 00-50-56-8a-5c-ec Admin Network Policy controller: took 4.766µs
I0719 01:46:01.810122   37437 admin_network_policy_node.go:55] Processing sync for Node 00-50-56-8a-e1-e7 in Admin Network Policy controller
I0719 01:46:01.810127   37437 admin_network_policy_node.go:58] Finished syncing Node 00-50-56-8a-e1-e7 Admin Network Policy controller: took 4.315µs
I0719 01:46:01.810109   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kube-storage-version-migrator-operator/kube-storage-version-migrator-operator-75d5d9b9f8-lj6w5
I0719 01:46:01.810140   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-multus/multus-2nb4x
I0719 01:46:01.810149   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kni-infra/keepalived-00-50-56-8a-44-52
I0719 01:46:01.810155   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-machine-config-operator/machine-config-daemon-kgwdc
I0719 01:46:01.810161   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-machine-config-operator/machine-config-server-968nk
I0719 01:46:01.810165   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-monitoring/metrics-server-7d47f4cbc-5qp84
I0719 01:46:01.810169   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-monitoring/node-exporter-9mlmj
I0719 01:46:01.810173   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-monitoring/prometheus-operator-admission-webhook-67db68b49d-w8jqx
I0719 01:46:01.810115   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-marketplace
I0719 01:46:01.810178   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-cluster-node-tuning-operator/tuned-cjc5f
I0719 01:46:01.810132   37437 admin_network_policy_node.go:55] Processing sync for Node 00-50-56-8a-f2-5d in Admin Network Policy controller
I0719 01:46:01.810187   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-operators
I0719 01:46:01.810190   37437 admin_network_policy_node.go:58] Finished syncing Node 00-50-56-8a-f2-5d Admin Network Policy controller: took 56.403µs
I0719 01:46:01.810195   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller assisted-installer
I0719 01:46:01.810183   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-etcd/etcd-guard-00-50-56-8a-39-a0
I0719 01:46:01.810207   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-network-operator/iptables-alerter-nh7z8
I0719 01:46:01.810208   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-kube-scheduler
I0719 01:46:01.810213   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-route-controller-manager/route-controller-manager-676cdfdbc8-t227m
I0719 01:46:01.810217   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-kube-storage-version-migrator-operator
I0719 01:46:01.810223   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-network-node-identity
I0719 01:46:01.810229   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-route-controller-manager
I0719 01:46:01.810234   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-service-ca-operator
I0719 01:46:01.810240   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller default
I0719 01:46:01.810244   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-cluster-node-tuning-operator
I0719 01:46:01.810217   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-machine-config-operator/machine-config-controller-b886dd6cb-6kjkp
I0719 01:46:01.810255   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-oauth-apiserver/apiserver-86f656c4dd-x7cqj
I0719 01:46:01.810261   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-dns/node-resolver-djq2g
I0719 01:46:01.810267   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-etcd/etcd-00-50-56-8a-5c-ec
I0719 01:46:01.810201   37437 admin_network_policy_node.go:55] Processing sync for Node 00-50-56-8a-fb-ea in Admin Network Policy controller
I0719 01:46:01.810272   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-multus/multus-additional-cni-plugins-b5t42
I0719 01:46:01.810274   37437 admin_network_policy_node.go:58] Finished syncing Node 00-50-56-8a-fb-ea Admin Network Policy controller: took 73.127µs
I0719 01:46:01.810276   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-multus/multus-additional-cni-plugins-pjk5m
I0719 01:46:01.810281   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-multus/multus-additional-cni-plugins-qdrk9
I0719 01:46:01.810281   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/rook-ceph-rgw-ocs-storagecluster-cephobjectstore-a-766774cx8zqw in Admin Network Policy controller
I0719 01:46:01.810286   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/csi-rbdplugin-xgkn6
I0719 01:46:01.810291   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/rook-ceph-crashcollector-00-50-56-8a-e1-e7-6c5dcb6f44-8z5np
I0719 01:46:01.810249   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-config-managed
I0719 01:46:01.810295   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-image-registry/cluster-image-registry-operator-656868857f-f94pq
I0719 01:46:01.810300   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-ingress-canary/ingress-canary-lsx7x
I0719 01:46:01.810291   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/rook-ceph-rgw-ocs-storagecluster-cephobjectstore-a-766774cx8zqw Admin Network Policy controller: took 10.871µs
I0719 01:46:01.810305   37437 default_network_controller.go:660] Recording add event on network policy assisted-installer/assisted-installer-network-policy
I0719 01:46:01.810306   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-5c-ec
I0719 01:46:01.810312   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kube-apiserver/kube-apiserver-guard-00-50-56-8a-44-52 in Admin Network Policy controller
I0719 01:46:01.810314   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-network-diagnostics/network-check-target-gc5jl
I0719 01:46:01.810317   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kube-apiserver/kube-apiserver-guard-00-50-56-8a-44-52 Admin Network Policy controller: took 4.958µs
I0719 01:46:01.810320   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-operator-lifecycle-manager/olm-operator-59f98dcc4-xqd8j
I0719 01:46:01.810301   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-etcd
I0719 01:46:01.810323   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-image-registry in Admin Network Policy controller
I0719 01:46:01.810327   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/csi-cephfsplugin-provisioner-585f89d895-2b4wk
I0719 01:46:01.810314   37437 obj_retry.go:502] Add event received for *v1.NetworkPolicy assisted-installer/assisted-installer-network-policy
I0719 01:46:01.810332   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-image-registry Admin Network Policy controller: took 7.826µs
I0719 01:46:01.810336   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/noobaa-db-pg-0
I0719 01:46:01.810339   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-ingress in Admin Network Policy controller
I0719 01:46:01.810341   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-cluster-version/cluster-version-operator-78b5d9c79d-znx2p
I0719 01:46:01.810343   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-ingress Admin Network Policy controller: took 4.417µs
I0719 01:46:01.810327   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-multus
I0719 01:46:01.810348   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-dns/node-resolver-dpn9t
I0719 01:46:01.810350   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-ovn-kubernetes
I0719 01:46:01.810339   37437 base_network_controller_policy.go:1098] Adding network policy assisted-installer/assisted-installer-network-policy for network default
I0719 01:46:01.810355   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-controller-manager
I0719 01:46:01.810361   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-machine-api
I0719 01:46:01.810363   37437 base_network_controller_policy.go:973] Policy assisted-installer/assisted-installer-network-policy added to peer address sets []
I0719 01:46:01.810366   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-network-operator
I0719 01:46:01.810371   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-service-ca
I0719 01:46:01.810376   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift
I0719 01:46:01.810379   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-controller-manager-operator
I0719 01:46:01.810353   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-monitoring/prometheus-operator-admission-webhook-67db68b49d-wbfqq
I0719 01:46:01.810387   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-network-diagnostics
I0719 01:46:01.810394   37437 admin_network_policy_controller.go:443] Adding Namespace in Admin Network Policy controller openshift-operator-lifecycle-manager
I0719 01:46:01.810388   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-controller-manager-operator/openshift-controller-manager-operator-cf8f9956c-x6xn5
I0719 01:46:01.810404   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kube-controller-manager-operator/kube-controller-manager-operator-85c67fcb8d-fg9j7
I0719 01:46:01.810410   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-44-52
I0719 01:46:01.810414   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-network-node-identity/network-node-identity-z7b9j
I0719 01:46:01.810419   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/csi-addons-controller-manager-6d78957fdf-gs4tk
I0719 01:46:01.810349   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-cluster-samples-operator in Admin Network Policy controller
I0719 01:46:01.810429   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-cluster-samples-operator Admin Network Policy controller: took 78.831µs
I0719 01:46:01.810438   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-kube-apiserver in Admin Network Policy controller
I0719 01:46:01.810442   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-kube-apiserver Admin Network Policy controller: took 4.425µs
I0719 01:46:01.810447   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-nutanix-infra in Admin Network Policy controller
I0719 01:46:01.810451   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-nutanix-infra Admin Network Policy controller: took 3.657µs
I0719 01:46:01.810455   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-cloud-controller-manager in Admin Network Policy controller
I0719 01:46:01.810459   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-cloud-controller-manager Admin Network Policy controller: took 4.113µs
I0719 01:46:01.810423   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-console/downloads-6967878986-76phj
I0719 01:46:01.810464   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-config-operator in Admin Network Policy controller
I0719 01:46:01.810467   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-image-registry/node-ca-tvhtl
I0719 01:46:01.810468   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-config-operator Admin Network Policy controller: took 3.578µs
I0719 01:46:01.810474   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-multus/multus-47wxd
I0719 01:46:01.810478   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace kube-node-lease in Admin Network Policy controller
I0719 01:46:01.810481   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-route-controller-manager/route-controller-manager-676cdfdbc8-gt4t6
I0719 01:46:01.810482   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace kube-node-lease Admin Network Policy controller: took 3.804µs
I0719 01:46:01.810489   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/csi-rbdplugin-xkw8r
I0719 01:46:01.810492   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-cloud-network-config-controller in Admin Network Policy controller
I0719 01:46:01.810494   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/ocs-client-operator-controller-manager-846f549988-v288f
I0719 01:46:01.810497   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-cloud-network-config-controller Admin Network Policy controller: took 4.864µs
I0719 01:46:01.810500   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/rook-ceph-osd-1-6db96b64cc-nw82d
I0719 01:46:01.810503   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-cluster-csi-drivers in Admin Network Policy controller
I0719 01:46:01.810507   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-cluster-csi-drivers Admin Network Policy controller: took 4.315µs
I0719 01:46:01.810504   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kni-infra/keepalived-00-50-56-8a-5c-ec
I0719 01:46:01.810512   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-cluster-machine-approver in Admin Network Policy controller
I0719 01:46:01.810517   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-cluster-machine-approver Admin Network Policy controller: took 3.938µs
I0719 01:46:01.810514   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kube-apiserver/kube-apiserver-00-50-56-8a-39-a0
I0719 01:46:01.810522   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-kni-infra in Admin Network Policy controller
I0719 01:46:01.810524   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kube-storage-version-migrator/migrator-7fc5dd675b-tfjhl
I0719 01:46:01.810526   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-kni-infra Admin Network Policy controller: took 3.876µs
I0719 01:46:01.810529   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-operator-lifecycle-manager/packageserver-6bf7d58455-k8qkk
I0719 01:46:01.810531   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-kube-controller-manager-operator in Admin Network Policy controller
I0719 01:46:01.810535   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-39-a0
I0719 01:46:01.810535   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-kube-controller-manager-operator Admin Network Policy controller: took 4.637µs
I0719 01:46:01.810542   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-machine-config-operator/machine-config-daemon-p677g
I0719 01:46:01.810544   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-dns-operator in Admin Network Policy controller
I0719 01:46:01.810508   37437 model_client.go:381] Update operations generated as: [{Op:update Table:ACL Row:map[action:drop direction:to-lport external_ids:{GoMap:map[direction:Ingress k8s.ovn.org/id:default-network-controller:NetpolNamespace:assisted-installer:Ingress:defaultDeny k8s.ovn.org/name:assisted-installer k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:NetpolNamespace type:defaultDeny]} log:false match:outport == @a18306990282168154761 meter:{GoSet:[acl-logging]} name:{GoSet:[NP:assisted-installer:Ingress]} options:{GoMap:map[]} priority:1000 severity:{GoSet:[]} tier:2] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {71a611dd-ddeb-4a5a-b3e6-daa462cbbde3}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.810548   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-monitoring/node-exporter-nvqsf
I0719 01:46:01.810635   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-operator-lifecycle-manager/package-server-manager-74bbc7c476-4555r
I0719 01:46:01.810644   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/csi-cephfsplugin-provisioner-585f89d895-ddwtl
I0719 01:46:01.810649   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-5c-ec
I0719 01:46:01.810548   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-dns-operator Admin Network Policy controller: took 4.128µs
I0719 01:46:01.810657   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kube-scheduler/openshift-kube-scheduler-guard-00-50-56-8a-44-52
I0719 01:46:01.810663   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/csi-cephfsplugin-s29g7
I0719 01:46:01.810665   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-insights in Admin Network Policy controller
I0719 01:46:01.810669   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-config-operator/openshift-config-operator-59dc875ddb-rnq74
I0719 01:46:01.810673   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-insights Admin Network Policy controller: took 8.678µs
I0719 01:46:01.810682   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-kube-scheduler-operator in Admin Network Policy controller
I0719 01:46:01.810688   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-kube-scheduler-operator Admin Network Policy controller: took 5.794µs
I0719 01:46:01.810694   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace kube-public in Admin Network Policy controller
I0719 01:46:01.810674   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-multus/multus-additional-cni-plugins-2kgg5
I0719 01:46:01.810698   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace kube-public Admin Network Policy controller: took 3.759µs
I0719 01:46:01.810704   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-cloud-platform-infra in Admin Network Policy controller
I0719 01:46:01.810708   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-service-ca-operator/service-ca-operator-86c8d4bbfd-w2qxx
I0719 01:46:01.810686   37437 model_client.go:381] Update operations generated as: [{Op:update Table:ACL Row:map[action:allow direction:to-lport external_ids:{GoMap:map[direction:Ingress k8s.ovn.org/id:default-network-controller:NetpolNamespace:assisted-installer:Ingress:arpAllow k8s.ovn.org/name:assisted-installer k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:NetpolNamespace type:arpAllow]} log:false match:outport == @a18306990282168154761 && (arp || nd) meter:{GoSet:[acl-logging]} name:{GoSet:[NP:assisted-installer:Ingress]} options:{GoMap:map[]} priority:1001 severity:{GoSet:[]} tier:2] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {3dd6b68f-c354-4d0f-9f35-198fba10be05}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.810715   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/rook-ceph-mds-ocs-storagecluster-cephfilesystem-b-c4dc5cd7zkffj
I0719 01:46:01.810793   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-operator-lifecycle-manager/collect-profiles-28689225-j8wtn
I0719 01:46:01.810799   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-ovn-kubernetes/ovnkube-node-568wp
I0719 01:46:01.810803   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/ocs-metrics-exporter-84f9766477-r8fxs
I0719 01:46:01.810708   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-cloud-platform-infra Admin Network Policy controller: took 3.773µs
I0719 01:46:01.810808   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/rook-ceph-mon-a-6dc9d78597-7ttc9
I0719 01:46:01.810812   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kube-controller-manager/kube-controller-manager-guard-00-50-56-8a-5c-ec
I0719 01:46:01.810814   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-cluster-version in Admin Network Policy controller
I0719 01:46:01.810817   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-machine-config-operator/machine-config-daemon-qpmqf
I0719 01:46:01.810819   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-cluster-version Admin Network Policy controller: took 5.612µs
I0719 01:46:01.810821   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-machine-api/metal3-599ff8f4b7-vntm7
I0719 01:46:01.810824   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-ingress-canary in Admin Network Policy controller
I0719 01:46:01.810826   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-marketplace/redhat-operators-mm6k4
I0719 01:46:01.810828   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-ingress-canary Admin Network Policy controller: took 3.715µs
I0719 01:46:01.810830   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-monitoring/alertmanager-main-0
I0719 01:46:01.810834   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-vsphere-infra in Admin Network Policy controller
I0719 01:46:01.810838   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-vsphere-infra Admin Network Policy controller: took 5.372µs
I0719 01:46:01.810835   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-network-diagnostics/network-check-target-jhhzw
I0719 01:46:01.810843   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-etcd-operator in Admin Network Policy controller
I0719 01:46:01.810847   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-etcd-operator Admin Network Policy controller: took 3.845µs
I0719 01:46:01.810849   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kube-scheduler/openshift-kube-scheduler-guard-00-50-56-8a-39-a0
I0719 01:46:01.810852   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace kube-system in Admin Network Policy controller
I0719 01:46:01.810855   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-machine-api/ironic-proxy-sn8n9
I0719 01:46:01.810856   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace kube-system Admin Network Policy controller: took 3.987µs
I0719 01:46:01.810861   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kube-controller-manager/kube-controller-manager-guard-00-50-56-8a-44-52
I0719 01:46:01.810842   37437 model_client.go:381] Update operations generated as: [{Op:update Table:ACL Row:map[action:drop direction:from-lport external_ids:{GoMap:map[direction:Egress k8s.ovn.org/id:default-network-controller:NetpolNamespace:assisted-installer:Egress:defaultDeny k8s.ovn.org/name:assisted-installer k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:NetpolNamespace type:defaultDeny]} log:false match:inport == @a14498204875478697137 meter:{GoSet:[acl-logging]} name:{GoSet:[NP:assisted-installer:Egress]} options:{GoMap:map[apply-after-lb:true]} priority:1000 severity:{GoSet:[]} tier:2] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {376d2745-181a-4cbf-8ced-7212363e169f}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.810867   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-local-storage/diskmaker-manager-wj2h7
I0719 01:46:01.810871   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-machine-config-operator/machine-config-server-j8kbc
I0719 01:46:01.810876   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/csi-rbdplugin-provisioner-5dcc45fbf4-v5l2c
I0719 01:46:01.810880   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-authentication/oauth-openshift-7c9d9dfc8c-ddj6k
I0719 01:46:01.810885   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-cluster-node-tuning-operator/tuned-f4pbt
I0719 01:46:01.810892   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-etcd/revision-pruner-9-00-50-56-8a-44-52
I0719 01:46:01.810897   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-monitoring/telemeter-client-7b74cd774c-fg6lz
I0719 01:46:01.810902   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-multus/multus-mqkdb
I0719 01:46:01.810908   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-console-operator/console-operator-76c8786869-jr6r2
I0719 01:46:01.810912   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-console/downloads-6967878986-hpkbw
I0719 01:46:01.810917   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/ocs-operator-5567c4fdb4-8b9zr
I0719 01:46:01.810921   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-ingress-canary/ingress-canary-lrjr5
I0719 01:46:01.810926   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-machine-api/machine-api-operator-5cb7d5868-9p8wr
I0719 01:46:01.810929   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-multus/multus-sv782
I0719 01:46:01.810863   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-authentication-operator in Admin Network Policy controller
I0719 01:46:01.810935   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-apiserver/apiserver-7d9bbd465d-ln8v5
I0719 01:46:01.810936   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-authentication-operator Admin Network Policy controller: took 72.241µs
I0719 01:46:01.810939   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-console-operator/console-conversion-webhook-664b4df6f5-nq9pd
I0719 01:46:01.810941   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-host-network in Admin Network Policy controller
I0719 01:46:01.810944   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-monitoring/kube-state-metrics-589b9987d-ck4ch
I0719 01:46:01.810945   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-host-network Admin Network Policy controller: took 3.826µs
I0719 01:46:01.810948   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-network-operator/iptables-alerter-m44lf
I0719 01:46:01.810950   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-infra in Admin Network Policy controller
I0719 01:46:01.810953   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kube-apiserver/kube-apiserver-guard-00-50-56-8a-39-a0
I0719 01:46:01.810954   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-infra Admin Network Policy controller: took 3.694µs
I0719 01:46:01.810958   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-machine-api/ironic-proxy-6zm7s
I0719 01:46:01.810960   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-machine-config-operator in Admin Network Policy controller
I0719 01:46:01.810963   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-operator-lifecycle-manager/collect-profiles-28689210-mbs94
I0719 01:46:01.810964   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-machine-config-operator Admin Network Policy controller: took 3.69µs
I0719 01:46:01.810968   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-dns/dns-default-5hh4c
I0719 01:46:01.810972   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-ingress-operator in Admin Network Policy controller
I0719 01:46:01.810974   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-dns/dns-default-wn5nz
I0719 01:46:01.810976   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-ingress-operator Admin Network Policy controller: took 3.611µs
I0719 01:46:01.810979   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-controller-manager/controller-manager-5c7f9f9d47-c74xp
I0719 01:46:01.810959   37437 model_client.go:381] Update operations generated as: [{Op:update Table:ACL Row:map[action:allow direction:from-lport external_ids:{GoMap:map[direction:Egress k8s.ovn.org/id:default-network-controller:NetpolNamespace:assisted-installer:Egress:arpAllow k8s.ovn.org/name:assisted-installer k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:NetpolNamespace type:arpAllow]} log:false match:inport == @a14498204875478697137 && (arp || nd) meter:{GoSet:[acl-logging]} name:{GoSet:[NP:assisted-installer:Egress]} options:{GoMap:map[apply-after-lb:true]} priority:1001 severity:{GoSet:[]} tier:2] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {e0b04054-e4b6-494e-9a84-63dbf107c703}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.811001   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-apiserver/apiserver-7d9bbd465d-7pbl8
I0719 01:46:01.810987   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-monitoring in Admin Network Policy controller
I0719 01:46:01.811014   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-monitoring Admin Network Policy controller: took 31.678µs
I0719 01:46:01.811022   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-node in Admin Network Policy controller
I0719 01:46:01.811026   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-node Admin Network Policy controller: took 3.71µs
I0719 01:46:01.811030   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-oauth-apiserver in Admin Network Policy controller
I0719 01:46:01.811007   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-authentication/oauth-openshift-7c9d9dfc8c-qcf89
I0719 01:46:01.811045   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-39-a0
I0719 01:46:01.811037   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Port_Group Row:map[acls:{GoSet:[{GoUUID:71a611dd-ddeb-4a5a-b3e6-daa462cbbde3} {GoUUID:3dd6b68f-c354-4d0f-9f35-198fba10be05}]} external_ids:{GoMap:map[direction:Ingress k8s.ovn.org/id:default-network-controller:NetpolNamespace:assisted-installer:Ingress k8s.ovn.org/name:assisted-installer k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:NetpolNamespace]} ports:{GoSet:[]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {5faec432-502f-48d7-b85b-d59f2c9912a5}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.811057   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-cluster-storage-operator/csi-snapshot-controller-operator-bb8d9765b-b24f6
I0719 01:46:01.811064   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kube-apiserver/kube-apiserver-00-50-56-8a-5c-ec
I0719 01:46:01.811071   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kube-apiserver-operator/kube-apiserver-operator-55dc5cdcf9-p4csg
I0719 01:46:01.811077   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kube-scheduler/revision-pruner-6-00-50-56-8a-39-a0
I0719 01:46:01.811085   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-monitoring/prometheus-operator-848d66f7-nx2v2
I0719 01:46:01.811091   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/rook-ceph-mon-c-5b4c4697fb-8w28d
I0719 01:46:01.811098   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-cluster-storage-operator/csi-snapshot-webhook-85b445968-78v7q
I0719 01:46:01.811034   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-oauth-apiserver Admin Network Policy controller: took 3.58µs
I0719 01:46:01.811092   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Port_Group Row:map[acls:{GoSet:[{GoUUID:376d2745-181a-4cbf-8ced-7212363e169f} {GoUUID:e0b04054-e4b6-494e-9a84-63dbf107c703}]} external_ids:{GoMap:map[direction:Egress k8s.ovn.org/id:default-network-controller:NetpolNamespace:assisted-installer:Egress k8s.ovn.org/name:assisted-installer k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:NetpolNamespace]} ports:{GoSet:[]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {a6d36e2e-5e3b-44dd-adb0-935e60ce9ad4}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.811109   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-ovirt-infra in Admin Network Policy controller
I0719 01:46:01.811113   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-ovirt-infra Admin Network Policy controller: took 4.59µs
I0719 01:46:01.811118   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-storage in Admin Network Policy controller
I0719 01:46:01.811121   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-storage Admin Network Policy controller: took 3.341µs
I0719 01:46:01.811126   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-apiserver in Admin Network Policy controller
I0719 01:46:01.811129   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-apiserver Admin Network Policy controller: took 3.415µs
I0719 01:46:01.811134   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-console in Admin Network Policy controller
I0719 01:46:01.811138   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-console Admin Network Policy controller: took 3.519µs
I0719 01:46:01.811142   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-console-operator in Admin Network Policy controller
I0719 01:46:01.811146   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-console-operator Admin Network Policy controller: took 3.287µs
I0719 01:46:01.811150   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-kube-storage-version-migrator in Admin Network Policy controller
I0719 01:46:01.811153   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-kube-storage-version-migrator Admin Network Policy controller: took 3.238µs
I0719 01:46:01.811158   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-cloud-credential-operator in Admin Network Policy controller
I0719 01:46:01.811161   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-cloud-credential-operator Admin Network Policy controller: took 3.207µs
I0719 01:46:01.811167   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-cluster-storage-operator in Admin Network Policy controller
I0719 01:46:01.811171   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-cluster-storage-operator Admin Network Policy controller: took 4.603µs
I0719 01:46:01.811175   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-console-user-settings in Admin Network Policy controller
I0719 01:46:01.811179   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-console-user-settings Admin Network Policy controller: took 3.322µs
I0719 01:46:01.811104   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-etcd/etcd-00-50-56-8a-44-52
I0719 01:46:01.811186   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/csi-rbdplugin-provisioner-5dcc45fbf4-9svs4 in Admin Network Policy controller
I0719 01:46:01.811196   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/csi-rbdplugin-provisioner-5dcc45fbf4-9svs4 Admin Network Policy controller: took 10.462µs
I0719 01:46:01.811205   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-ovn-kubernetes/ovnkube-node-7pmvf in Admin Network Policy controller
I0719 01:46:01.811211   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-ovn-kubernetes/ovnkube-node-7pmvf Admin Network Policy controller: took 4.646µs
I0719 01:46:01.811216   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-44-52 in Admin Network Policy controller
I0719 01:46:01.811112   37437 transact.go:42] Configuring OVN: [{Op:update Table:ACL Row:map[action:drop direction:to-lport external_ids:{GoMap:map[direction:Ingress k8s.ovn.org/id:default-network-controller:NetpolNamespace:assisted-installer:Ingress:defaultDeny k8s.ovn.org/name:assisted-installer k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:NetpolNamespace type:defaultDeny]} log:false match:outport == @a18306990282168154761 meter:{GoSet:[acl-logging]} name:{GoSet:[NP:assisted-installer:Ingress]} options:{GoMap:map[]} priority:1000 severity:{GoSet:[]} tier:2] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {71a611dd-ddeb-4a5a-b3e6-daa462cbbde3}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:update Table:ACL Row:map[action:allow direction:to-lport external_ids:{GoMap:map[direction:Ingress k8s.ovn.org/id:default-network-controller:NetpolNamespace:assisted-installer:Ingress:arpAllow k8s.ovn.org/name:assisted-installer k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:NetpolNamespace type:arpAllow]} log:false match:outport == @a18306990282168154761 && (arp || nd) meter:{GoSet:[acl-logging]} name:{GoSet:[NP:assisted-installer:Ingress]} options:{GoMap:map[]} priority:1001 severity:{GoSet:[]} tier:2] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {3dd6b68f-c354-4d0f-9f35-198fba10be05}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:update Table:ACL Row:map[action:drop direction:from-lport external_ids:{GoMap:map[direction:Egress k8s.ovn.org/id:default-network-controller:NetpolNamespace:assisted-installer:Egress:defaultDeny k8s.ovn.org/name:assisted-installer k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:NetpolNamespace type:defaultDeny]} log:false match:inport == @a14498204875478697137 meter:{GoSet:[acl-logging]} name:{GoSet:[NP:assisted-installer:Egress]} options:{GoMap:map[apply-after-lb:true]} priority:1000 severity:{GoSet:[]} tier:2] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {376d2745-181a-4cbf-8ced-7212363e169f}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:update Table:ACL Row:map[action:allow direction:from-lport external_ids:{GoMap:map[direction:Egress k8s.ovn.org/id:default-network-controller:NetpolNamespace:assisted-installer:Egress:arpAllow k8s.ovn.org/name:assisted-installer k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:NetpolNamespace type:arpAllow]} log:false match:inport == @a14498204875478697137 && (arp || nd) meter:{GoSet:[acl-logging]} name:{GoSet:[NP:assisted-installer:Egress]} options:{GoMap:map[apply-after-lb:true]} priority:1001 severity:{GoSet:[]} tier:2] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {e0b04054-e4b6-494e-9a84-63dbf107c703}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:update Table:Port_Group Row:map[acls:{GoSet:[{GoUUID:71a611dd-ddeb-4a5a-b3e6-daa462cbbde3} {GoUUID:3dd6b68f-c354-4d0f-9f35-198fba10be05}]} external_ids:{GoMap:map[direction:Ingress k8s.ovn.org/id:default-network-controller:NetpolNamespace:assisted-installer:Ingress k8s.ovn.org/name:assisted-installer k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:NetpolNamespace]} ports:{GoSet:[]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {5faec432-502f-48d7-b85b-d59f2c9912a5}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:update Table:Port_Group Row:map[acls:{GoSet:[{GoUUID:376d2745-181a-4cbf-8ced-7212363e169f} {GoUUID:e0b04054-e4b6-494e-9a84-63dbf107c703}]} external_ids:{GoMap:map[direction:Egress k8s.ovn.org/id:default-network-controller:NetpolNamespace:assisted-installer:Egress k8s.ovn.org/name:assisted-installer k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:NetpolNamespace]} ports:{GoSet:[]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {a6d36e2e-5e3b-44dd-adb0-935e60ce9ad4}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.811220   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-44-52 Admin Network Policy controller: took 4.388µs
I0719 01:46:01.811189   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-39-a0
I0719 01:46:01.811318   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-monitoring/monitoring-plugin-6f457fd4b8-pqp4m in Admin Network Policy controller
I0719 01:46:01.811322   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-machine-config-operator/machine-config-operator-7fc5c776cc-r6wsl
I0719 01:46:01.811326   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-monitoring/monitoring-plugin-6f457fd4b8-pqp4m Admin Network Policy controller: took 9.17µs
I0719 01:46:01.811328   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-monitoring/prometheus-k8s-1
I0719 01:46:01.811332   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-machine-config-operator/machine-config-daemon-4kr96 in Admin Network Policy controller
I0719 01:46:01.811337   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-machine-config-operator/machine-config-daemon-4kr96 Admin Network Policy controller: took 5.113µs
I0719 01:46:01.811343   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kube-scheduler/revision-pruner-6-00-50-56-8a-44-52 in Admin Network Policy controller
I0719 01:46:01.811347   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kube-scheduler/revision-pruner-6-00-50-56-8a-44-52 Admin Network Policy controller: took 4.326µs
I0719 01:46:01.811352   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kube-scheduler/revision-pruner-6-00-50-56-8a-5c-ec in Admin Network Policy controller
I0719 01:46:01.811355   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kube-scheduler/revision-pruner-6-00-50-56-8a-5c-ec Admin Network Policy controller: took 3.875µs
I0719 01:46:01.811360   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-machine-api/control-plane-machine-set-operator-77bcc698b6-wvkdb in Admin Network Policy controller
I0719 01:46:01.811364   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-machine-api/control-plane-machine-set-operator-77bcc698b6-wvkdb Admin Network Policy controller: took 4.313µs
I0719 01:46:01.811369   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-f2-5d in Admin Network Policy controller
I0719 01:46:01.811373   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-f2-5d Admin Network Policy controller: took 3.889µs
I0719 01:46:01.811378   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-multus/multus-additional-cni-plugins-rtmj7 in Admin Network Policy controller
I0719 01:46:01.811382   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-multus/multus-additional-cni-plugins-rtmj7 Admin Network Policy controller: took 4.156µs
I0719 01:46:01.811333   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-oauth-apiserver/apiserver-86f656c4dd-2pxdq
I0719 01:46:01.811386   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-multus/network-metrics-daemon-fslb2 in Admin Network Policy controller
I0719 01:46:01.811391   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-oauth-apiserver/apiserver-86f656c4dd-g82dw
I0719 01:46:01.811395   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-multus/network-metrics-daemon-fslb2 Admin Network Policy controller: took 7.127µs
I0719 01:46:01.811398   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-cluster-storage-operator/csi-snapshot-webhook-85b445968-9dpmd
I0719 01:46:01.811401   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-console/console-c675c654b-rw8cg in Admin Network Policy controller
I0719 01:46:01.811406   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-console/console-c675c654b-rw8cg Admin Network Policy controller: took 4.968µs
I0719 01:46:01.811411   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-etcd-operator/etcd-operator-6c7489b895-5tql8 in Admin Network Policy controller
I0719 01:46:01.811415   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-etcd-operator/etcd-operator-6c7489b895-5tql8 Admin Network Policy controller: took 4.336µs
I0719 01:46:01.811420   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/rook-ceph-osd-0-6d5dbb5f-24hfr in Admin Network Policy controller
I0719 01:46:01.811424   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/rook-ceph-osd-0-6d5dbb5f-24hfr Admin Network Policy controller: took 3.954µs
I0719 01:46:01.811428   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-monitoring/node-exporter-7m7sg in Admin Network Policy controller
I0719 01:46:01.811432   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-monitoring/node-exporter-7m7sg Admin Network Policy controller: took 3.753µs
I0719 01:46:01.811437   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-network-diagnostics/network-check-source-b89b7bb96-lpzlv in Admin Network Policy controller
I0719 01:46:01.811441   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-network-diagnostics/network-check-source-b89b7bb96-lpzlv Admin Network Policy controller: took 3.895µs
I0719 01:46:01.811445   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/rook-ceph-exporter-00-50-56-8a-e1-e7-558dfbd955-jzh65 in Admin Network Policy controller
I0719 01:46:01.811449   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/rook-ceph-exporter-00-50-56-8a-e1-e7-558dfbd955-jzh65 Admin Network Policy controller: took 3.905µs
I0719 01:46:01.811454   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-monitoring/thanos-querier-68bf686489-9cctf in Admin Network Policy controller
I0719 01:46:01.811457   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-monitoring/thanos-querier-68bf686489-9cctf Admin Network Policy controller: took 3.745µs
I0719 01:46:01.811462   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-multus/network-metrics-daemon-t4g2p in Admin Network Policy controller
I0719 01:46:01.811402   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-dns/dns-default-24pdt
I0719 01:46:01.811466   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-multus/network-metrics-daemon-t4g2p Admin Network Policy controller: took 4.267µs
I0719 01:46:01.811472   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-image-registry/node-ca-wgn2l in Admin Network Policy controller
I0719 01:46:01.811476   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-image-registry/node-ca-wgn2l Admin Network Policy controller: took 3.972µs
I0719 01:46:01.811478   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-etcd/etcd-guard-00-50-56-8a-5c-ec
I0719 01:46:01.811481   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-network-diagnostics/network-check-target-h9cbr in Admin Network Policy controller
I0719 01:46:01.811484   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kni-infra/coredns-00-50-56-8a-39-a0
I0719 01:46:01.811486   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-network-diagnostics/network-check-target-h9cbr Admin Network Policy controller: took 5.177µs
I0719 01:46:01.811489   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-cluster-machine-approver/machine-approver-5bf6544664-79krt
I0719 01:46:01.811491   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-5c-ec in Admin Network Policy controller
I0719 01:46:01.811494   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-cluster-samples-operator/cluster-samples-operator-6b95974b98-cxvvt
I0719 01:46:01.811496   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-5c-ec Admin Network Policy controller: took 4.521µs
I0719 01:46:01.811499   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-multus/network-metrics-daemon-gqqpq
I0719 01:46:01.811501   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-e1-e7 in Admin Network Policy controller
I0719 01:46:01.811504   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-monitoring/node-exporter-s77zj
I0719 01:46:01.811505   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-e1-e7 Admin Network Policy controller: took 4.225µs
I0719 01:46:01.811508   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-monitoring/prometheus-k8s-0
I0719 01:46:01.811510   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-ovn-kubernetes/ovnkube-control-plane-58975cd9fd-mz4pv in Admin Network Policy controller
I0719 01:46:01.811514   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-ingress/router-default-54fb8ffc6b-hhdt2
I0719 01:46:01.811515   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-ovn-kubernetes/ovnkube-control-plane-58975cd9fd-mz4pv Admin Network Policy controller: took 4.279µs
I0719 01:46:01.811519   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kube-apiserver/revision-pruner-8-00-50-56-8a-39-a0
I0719 01:46:01.811523   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/odf-console-b7ccd85c5-84cnv in Admin Network Policy controller
I0719 01:46:01.811524   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-network-diagnostics/network-check-target-vltnw
I0719 01:46:01.811527   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/odf-console-b7ccd85c5-84cnv Admin Network Policy controller: took 4.348µs
I0719 01:46:01.811529   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-network-node-identity/network-node-identity-tzcq8
I0719 01:46:01.811532   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kube-apiserver/revision-pruner-8-00-50-56-8a-44-52 in Admin Network Policy controller
I0719 01:46:01.811534   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-console/console-f7dbc9784-cj9wp
I0719 01:46:01.811536   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kube-apiserver/revision-pruner-8-00-50-56-8a-44-52 Admin Network Policy controller: took 4.167µs
I0719 01:46:01.811538   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-ingress-canary/ingress-canary-zxwrq
I0719 01:46:01.811541   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kube-apiserver/revision-pruner-8-00-50-56-8a-5c-ec in Admin Network Policy controller
I0719 01:46:01.811543   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-local-storage/diskmaker-manager-vrh5h
I0719 01:46:01.811545   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kube-apiserver/revision-pruner-8-00-50-56-8a-5c-ec Admin Network Policy controller: took 4.252µs
I0719 01:46:01.811548   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-ovn-kubernetes/ovnkube-node-62ccc
I0719 01:46:01.811550   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kube-scheduler/openshift-kube-scheduler-guard-00-50-56-8a-5c-ec in Admin Network Policy controller
I0719 01:46:01.811552   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-cloud-credential-operator/cloud-credential-operator-6488fd5f9b-jkdg2
I0719 01:46:01.811555   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kube-scheduler/openshift-kube-scheduler-guard-00-50-56-8a-5c-ec Admin Network Policy controller: took 4.499µs
I0719 01:46:01.811557   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-dns/node-resolver-r7f9m
I0719 01:46:01.811560   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-marketplace/redhat-marketplace-hbf7g in Admin Network Policy controller
I0719 01:46:01.811562   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-multus/multus-admission-controller-5cc499c6f4-bngv4
I0719 01:46:01.811566   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-apiserver-operator/openshift-apiserver-operator-84fc88fd69-mqjqx
I0719 01:46:01.811566   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-marketplace/redhat-marketplace-hbf7g Admin Network Policy controller: took 4.293µs
I0719 01:46:01.811576   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-multus/multus-25bkq in Admin Network Policy controller
I0719 01:46:01.811581   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-multus/multus-25bkq Admin Network Policy controller: took 5.29µs
I0719 01:46:01.811586   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-multus/multus-ltqfr in Admin Network Policy controller
I0719 01:46:01.811590   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-multus/multus-ltqfr Admin Network Policy controller: took 4.16µs
I0719 01:46:01.811592   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kni-infra/coredns-00-50-56-8a-5c-ec
I0719 01:46:01.811605   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kube-apiserver/kube-apiserver-00-50-56-8a-44-52
I0719 01:46:01.811610   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-multus/multus-admission-controller-5cc499c6f4-jtjqw
I0719 01:46:01.811615   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/noobaa-endpoint-6ddf6bb6b-jmx4r
I0719 01:46:01.811620   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-cluster-node-tuning-operator/cluster-node-tuning-operator-68cc9c9cf9-6brm7
I0719 01:46:01.811624   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kni-infra/coredns-00-50-56-8a-e1-e7
I0719 01:46:01.811595   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-network-operator/network-operator-6967d44d7-4wwpm in Admin Network Policy controller
I0719 01:46:01.811629   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-image-registry/node-ca-kqt8n
I0719 01:46:01.811637   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-network-operator/network-operator-6967d44d7-4wwpm Admin Network Policy controller: took 40.558µs
I0719 01:46:01.811638   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kni-infra/keepalived-00-50-56-8a-fb-ea
I0719 01:46:01.811646   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-cluster-node-tuning-operator/tuned-5pn2c in Admin Network Policy controller
I0719 01:46:01.811651   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-cluster-node-tuning-operator/tuned-5pn2c Admin Network Policy controller: took 5.181µs
I0719 01:46:01.811656   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-dns/node-resolver-nsvs6 in Admin Network Policy controller
I0719 01:46:01.811662   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-dns/node-resolver-nsvs6 Admin Network Policy controller: took 4.425µs
I0719 01:46:01.811667   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-image-registry/image-pruner-28689120-2bnxj in Admin Network Policy controller
I0719 01:46:01.811671   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-image-registry/image-pruner-28689120-2bnxj Admin Network Policy controller: took 4.346µs
I0719 01:46:01.811676   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-multus/network-metrics-daemon-hxzdd in Admin Network Policy controller
I0719 01:46:01.811680   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-multus/network-metrics-daemon-hxzdd Admin Network Policy controller: took 4.015µs
I0719 01:46:01.811647   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-monitoring/monitoring-plugin-6f457fd4b8-6wb4z
I0719 01:46:01.811693   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/rook-ceph-osd-2-9c5dbbd88-crlql
I0719 01:46:01.811699   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-cluster-node-tuning-operator/tuned-x2svx
I0719 01:46:01.811704   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-dns/dns-default-rj9px
I0719 01:46:01.811709   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kni-infra/haproxy-00-50-56-8a-44-52
I0719 01:46:01.811713   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-machine-config-operator/machine-config-server-zwkfw
I0719 01:46:01.811685   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kni-infra/coredns-00-50-56-8a-fb-ea in Admin Network Policy controller
I0719 01:46:01.811718   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-network-operator/iptables-alerter-m6v49
I0719 01:46:01.811722   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-authentication/oauth-openshift-7c9d9dfc8c-lxcsb
I0719 01:46:01.811725   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kni-infra/coredns-00-50-56-8a-fb-ea Admin Network Policy controller: took 38.527µs
I0719 01:46:01.811727   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-cluster-node-tuning-operator/tuned-hpvxx
I0719 01:46:01.811735   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/csi-cephfsplugin-b549v
I0719 01:46:01.811736   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-kube-controller-manager in Admin Network Policy controller
I0719 01:46:01.811740   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-cluster-node-tuning-operator/tuned-9mzgb
I0719 01:46:01.811741   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-kube-controller-manager Admin Network Policy controller: took 5.881µs
I0719 01:46:01.811745   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-monitoring/alertmanager-main-1
I0719 01:46:01.811751   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-machine-api/machine-api-controllers-59cdf7bd97-7l7pt
I0719 01:46:01.811751   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-local-storage in Admin Network Policy controller
I0719 01:46:01.811756   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-network-diagnostics/network-check-target-8gshd
I0719 01:46:01.811759   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-local-storage Admin Network Policy controller: took 8.409µs
I0719 01:46:01.811761   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-local-storage/local-storage-operator-6486fccd57-h47kh
I0719 01:46:01.811765   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-openstack-infra in Admin Network Policy controller
I0719 01:46:01.811767   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-route-controller-manager/route-controller-manager-676cdfdbc8-t6rhq
I0719 01:46:01.811768   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-openstack-infra Admin Network Policy controller: took 3.671µs
I0719 01:46:01.811771   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-machine-config-operator/machine-config-daemon-vllgq
I0719 01:46:01.811774   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-user-workload-monitoring in Admin Network Policy controller
I0719 01:46:01.811776   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-marketplace/certified-operators-j5jtq
I0719 01:46:01.811781   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-network-node-identity/network-node-identity-xlk9z
I0719 01:46:01.811786   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-operator-lifecycle-manager/catalog-operator-7d75668bc4-sjfjn
I0719 01:46:01.811790   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-ovn-kubernetes/ovnkube-control-plane-58975cd9fd-7wmvb
I0719 01:46:01.811797   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/ux-backend-server-6444f844bf-whf8g
I0719 01:46:01.811801   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kni-infra/coredns-00-50-56-8a-44-52
I0719 01:46:01.811806   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-machine-api/cluster-autoscaler-operator-56cd7bcc4-8t6ns
I0719 01:46:01.811810   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kube-apiserver/kube-apiserver-guard-00-50-56-8a-5c-ec
I0719 01:46:01.811815   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-monitoring/openshift-state-metrics-6bb8db76bd-2wlhc
I0719 01:46:01.811818   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/rook-ceph-mon-b-59759dbb89-7jlvw
I0719 01:46:01.811823   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-dns/dns-default-qzrlq
I0719 01:46:01.811777   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-user-workload-monitoring Admin Network Policy controller: took 3.799µs
I0719 01:46:01.811827   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-dns/dns-default-zwbjg
I0719 01:46:01.811832   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-local-storage/diskmaker-manager-2zrc6
I0719 01:46:01.811834   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-authentication in Admin Network Policy controller
I0719 01:46:01.811837   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-cluster-storage-operator/cluster-storage-operator-6c5864c5b-kgzzc
I0719 01:46:01.811839   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-authentication Admin Network Policy controller: took 6.196µs
I0719 01:46:01.811842   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-etcd/etcd-guard-00-50-56-8a-44-52
I0719 01:46:01.811845   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-cloud-controller-manager-operator in Admin Network Policy controller
I0719 01:46:01.811849   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-cloud-controller-manager-operator Admin Network Policy controller: took 4.236µs
I0719 01:46:01.811854   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-kube-apiserver-operator in Admin Network Policy controller
I0719 01:46:01.811858   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-kube-apiserver-operator Admin Network Policy controller: took 3.382µs
I0719 01:46:01.811862   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-marketplace in Admin Network Policy controller
I0719 01:46:01.811866   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-marketplace Admin Network Policy controller: took 3.459µs
I0719 01:46:01.811870   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-operators in Admin Network Policy controller
I0719 01:46:01.811874   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-operators Admin Network Policy controller: took 3.204µs
I0719 01:46:01.811878   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace assisted-installer in Admin Network Policy controller
I0719 01:46:01.811881   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace assisted-installer Admin Network Policy controller: took 3.189µs
I0719 01:46:01.811886   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-kube-scheduler in Admin Network Policy controller
I0719 01:46:01.811889   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-kube-scheduler Admin Network Policy controller: took 3.413µs
I0719 01:46:01.811894   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-kube-storage-version-migrator-operator in Admin Network Policy controller
I0719 01:46:01.811897   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-kube-storage-version-migrator-operator Admin Network Policy controller: took 3.352µs
I0719 01:46:01.811846   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-machine-api/metal3-baremetal-operator-6fd5ccf9-9p448
I0719 01:46:01.811910   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-fb-ea
I0719 01:46:01.811902   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-network-node-identity in Admin Network Policy controller
I0719 01:46:01.811917   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/csi-rbdplugin-b6gdm
I0719 01:46:01.811923   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/noobaa-core-0
I0719 01:46:01.811922   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-network-node-identity Admin Network Policy controller: took 19.449µs
I0719 01:46:01.811930   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-controller-manager/controller-manager-5c7f9f9d47-thph4
I0719 01:46:01.811934   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-route-controller-manager in Admin Network Policy controller
I0719 01:46:01.811939   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-route-controller-manager Admin Network Policy controller: took 5.394µs
I0719 01:46:01.811945   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-service-ca-operator in Admin Network Policy controller
I0719 01:46:01.811949   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-service-ca-operator Admin Network Policy controller: took 3.76µs
I0719 01:46:01.811954   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace default in Admin Network Policy controller
I0719 01:46:01.811957   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace default Admin Network Policy controller: took 3.519µs
I0719 01:46:01.811962   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-cluster-node-tuning-operator in Admin Network Policy controller
I0719 01:46:01.811966   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-cluster-node-tuning-operator Admin Network Policy controller: took 3.393µs
I0719 01:46:01.811935   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-ingress/router-default-54fb8ffc6b-kgb2v
I0719 01:46:01.811956   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Port_Group Row:map[acls:{GoSet:[]} external_ids:{GoMap:map[k8s.ovn.org/id:default-network-controller:NetworkPolicy:assisted-installer:assisted-installer-network-policy k8s.ovn.org/name:assisted-installer:assisted-installer-network-policy k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:NetworkPolicy]} ports:{GoSet:[]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {5a440f2a-c43f-4eda-971b-a12726dc0adc}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.811978   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-network-operator/iptables-alerter-wxl7s
I0719 01:46:01.811970   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-config-managed in Admin Network Policy controller
I0719 01:46:01.811998   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-config-managed Admin Network Policy controller: took 27.196µs
I0719 01:46:01.811993   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/odf-operator-controller-manager-78d57f457c-tbwjf
I0719 01:46:01.812006   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-etcd in Admin Network Policy controller
I0719 01:46:01.812010   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-etcd Admin Network Policy controller: took 4.031µs
I0719 01:46:01.812015   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-multus in Admin Network Policy controller
I0719 01:46:01.812016   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/csi-cephfsplugin-5fvh4
I0719 01:46:01.812019   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-multus Admin Network Policy controller: took 3.647µs
I0719 01:46:01.812031   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-ovn-kubernetes in Admin Network Policy controller
I0719 01:46:01.812037   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-ovn-kubernetes Admin Network Policy controller: took 6.307µs
I0719 01:46:01.812044   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-controller-manager in Admin Network Policy controller
I0719 01:46:01.812048   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-controller-manager Admin Network Policy controller: took 4.346µs
I0719 01:46:01.812053   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-machine-api in Admin Network Policy controller
I0719 01:46:01.812057   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-machine-api Admin Network Policy controller: took 3.504µs
I0719 01:46:01.811989   37437 transact.go:42] Configuring OVN: [{Op:update Table:Port_Group Row:map[acls:{GoSet:[]} external_ids:{GoMap:map[k8s.ovn.org/id:default-network-controller:NetworkPolicy:assisted-installer:assisted-installer-network-policy k8s.ovn.org/name:assisted-installer:assisted-installer-network-policy k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:NetworkPolicy]} ports:{GoSet:[]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {5a440f2a-c43f-4eda-971b-a12726dc0adc}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.812067   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-dns/node-resolver-tjmrc
I0719 01:46:01.812086   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kni-infra/haproxy-00-50-56-8a-5c-ec
I0719 01:46:01.812097   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-network-diagnostics/network-check-target-dj4vt
I0719 01:46:01.812104   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/rook-ceph-operator-cf758864f-c6zl8
I0719 01:46:01.812112   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-console/console-57f455cd77-h96cj
I0719 01:46:01.812119   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-monitoring/node-exporter-gbsmf
I0719 01:46:01.812125   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-etcd/revision-pruner-9-00-50-56-8a-39-a0
I0719 01:46:01.812130   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-etcd/revision-pruner-9-00-50-56-8a-5c-ec
I0719 01:46:01.812061   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-network-operator in Admin Network Policy controller
I0719 01:46:01.812142   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-network-operator Admin Network Policy controller: took 79.813µs
I0719 01:46:01.812136   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kni-infra/keepalived-00-50-56-8a-e1-e7
I0719 01:46:01.812150   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-service-ca in Admin Network Policy controller
I0719 01:46:01.812154   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-service-ca Admin Network Policy controller: took 3.964µs
I0719 01:46:01.812156   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-monitoring/thanos-querier-68bf686489-qbcjs
I0719 01:46:01.812159   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift in Admin Network Policy controller
I0719 01:46:01.812165   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-multus/network-metrics-daemon-7ttpg
I0719 01:46:01.812171   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-operator-lifecycle-manager/collect-profiles-28689195-w9664
I0719 01:46:01.812177   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-cluster-storage-operator/csi-snapshot-controller-794ff44f88-7cksj
I0719 01:46:01.812183   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-dns/node-resolver-bf5zv
I0719 01:46:01.812165   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift Admin Network Policy controller: took 3.81µs
I0719 01:46:01.812190   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-console/console-57f455cd77-77wrt
I0719 01:46:01.812199   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-controller-manager-operator in Admin Network Policy controller
I0719 01:46:01.812204   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-controller-manager-operator Admin Network Policy controller: took 5.74µs
I0719 01:46:01.812209   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-network-diagnostics in Admin Network Policy controller
I0719 01:46:01.812212   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-network-diagnostics Admin Network Policy controller: took 3.176µs
I0719 01:46:01.812217   37437 admin_network_policy_namespace.go:53] Processing sync for Namespace openshift-operator-lifecycle-manager in Admin Network Policy controller
I0719 01:46:01.812221   37437 admin_network_policy_namespace.go:56] Finished syncing Namespace openshift-operator-lifecycle-manager Admin Network Policy controller: took 3.294µs
I0719 01:46:01.812199   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-image-registry/node-ca-lfxb8
I0719 01:46:01.812232   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-ingress-operator/ingress-operator-5cc96867f4-pdgdd
I0719 01:46:01.812235   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-multus/network-metrics-daemon-bqt8s in Admin Network Policy controller
I0719 01:46:01.812240   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-machine-api/metal3-image-customization-5f9d4c754c-5v2p8
I0719 01:46:01.812243   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-multus/network-metrics-daemon-bqt8s Admin Network Policy controller: took 9.036µs
I0719 01:46:01.812245   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-machine-config-operator/machine-config-daemon-r8bgv
I0719 01:46:01.812256   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-marketplace/marketplace-operator-59c7f5b7bd-8pd2c in Admin Network Policy controller
I0719 01:46:01.812263   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-marketplace/marketplace-operator-59c7f5b7bd-8pd2c Admin Network Policy controller: took 6.96µs
I0719 01:46:01.812269   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-monitoring/node-exporter-7xrvj in Admin Network Policy controller
I0719 01:46:01.812268   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-monitoring/metrics-server-7d47f4cbc-dqrxk
I0719 01:46:01.812273   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-monitoring/node-exporter-7xrvj Admin Network Policy controller: took 4.198µs
I0719 01:46:01.812277   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-apiserver/apiserver-7d9bbd465d-6cgbw
I0719 01:46:01.812280   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-controller-manager/controller-manager-5c7f9f9d47-kxpdr in Admin Network Policy controller
I0719 01:46:01.812283   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-authentication-operator/authentication-operator-68795c8768-8rvtz
I0719 01:46:01.812284   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-controller-manager/controller-manager-5c7f9f9d47-kxpdr Admin Network Policy controller: took 4.44µs
I0719 01:46:01.812288   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/rook-ceph-mgr-a-6fddb5fd95-mr2cn
I0719 01:46:01.812290   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kni-infra/keepalived-00-50-56-8a-39-a0 in Admin Network Policy controller
I0719 01:46:01.812293   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/rook-ceph-mgr-b-779b65ccb6-29sz4
I0719 01:46:01.812294   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kni-infra/keepalived-00-50-56-8a-39-a0 Admin Network Policy controller: took 4.484µs
I0719 01:46:01.812297   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-service-ca/service-ca-6dbc4646f9-6q769
I0719 01:46:01.812300   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/rook-ceph-exporter-00-50-56-8a-f2-5d-785d485f5d-v5k84 in Admin Network Policy controller
I0719 01:46:01.812302   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/rook-ceph-crashcollector-00-50-56-8a-f2-5d-5bfb656d8f-tvtpr
I0719 01:46:01.812304   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/rook-ceph-exporter-00-50-56-8a-f2-5d-785d485f5d-v5k84 Admin Network Policy controller: took 4.229µs
I0719 01:46:01.812306   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kni-infra/haproxy-00-50-56-8a-39-a0
I0719 01:46:01.812309   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-cloud-controller-manager-operator/cluster-cloud-controller-manager-operator-7f55545d59-r8j8z in Admin Network Policy controller
I0719 01:46:01.812311   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kube-scheduler-operator/openshift-kube-scheduler-operator-555f7bb8bc-4vw77
I0719 01:46:01.812314   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-cloud-controller-manager-operator/cluster-cloud-controller-manager-operator-7f55545d59-r8j8z Admin Network Policy controller: took 5.259µs
I0719 01:46:01.812319   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/noobaa-operator-bf7774fd8-zskvp
I0719 01:46:01.812319   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-cluster-storage-operator/csi-snapshot-controller-794ff44f88-5jz8j in Admin Network Policy controller
I0719 01:46:01.812325   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-image-registry/node-ca-986d7
I0719 01:46:01.812329   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-cluster-storage-operator/csi-snapshot-controller-794ff44f88-5jz8j Admin Network Policy controller: took 8.495µs
I0719 01:46:01.812332   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kni-infra/coredns-00-50-56-8a-f2-5d
I0719 01:46:01.812336   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-network-operator/iptables-alerter-6s78n in Admin Network Policy controller
I0719 01:46:01.812341   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-network-operator/iptables-alerter-6s78n Admin Network Policy controller: took 5.427µs
I0719 01:46:01.812346   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-network-operator/iptables-alerter-b72gh in Admin Network Policy controller
I0719 01:46:01.812351   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-network-operator/iptables-alerter-b72gh Admin Network Policy controller: took 4.004µs
I0719 01:46:01.812327   37437 factory.go:988] Added *v1.Pod event handler 5
I0719 01:46:01.812368   37437 base_network_controller_policy.go:1151] Create network policy assisted-installer/assisted-installer-network-policy resources completed, update namespace loglevel
I0719 01:46:01.812337   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-machine-api/ironic-proxy-k9xzh
I0719 01:46:01.812380   37437 obj_retry.go:541] Creating *v1.NetworkPolicy assisted-installer/assisted-installer-network-policy took: 2.04187ms
I0719 01:46:01.812383   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-multus/multus-additional-cni-plugins-tpn87
I0719 01:46:01.812356   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-operator-lifecycle-manager/packageserver-6bf7d58455-gh44f in Admin Network Policy controller
I0719 01:46:01.812397   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-operator-lifecycle-manager/packageserver-6bf7d58455-gh44f Admin Network Policy controller: took 39.513µs
I0719 01:46:01.812387   37437 default_network_controller.go:703] Recording success event on network policy assisted-installer/assisted-installer-network-policy
I0719 01:46:01.812408   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kube-storage-version-migrator-operator/kube-storage-version-migrator-operator-75d5d9b9f8-lj6w5 in Admin Network Policy controller
I0719 01:46:01.812413   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kube-storage-version-migrator-operator/kube-storage-version-migrator-operator-75d5d9b9f8-lj6w5 Admin Network Policy controller: took 5.33µs
I0719 01:46:01.812418   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-multus/multus-2nb4x in Admin Network Policy controller
I0719 01:46:01.812422   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-multus/multus-2nb4x Admin Network Policy controller: took 4.506µs
I0719 01:46:01.812429   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kni-infra/keepalived-00-50-56-8a-44-52 in Admin Network Policy controller
I0719 01:46:01.812433   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kni-infra/keepalived-00-50-56-8a-44-52 Admin Network Policy controller: took 5.836µs
I0719 01:46:01.812438   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-machine-config-operator/machine-config-daemon-kgwdc in Admin Network Policy controller
I0719 01:46:01.812442   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-machine-config-operator/machine-config-daemon-kgwdc Admin Network Policy controller: took 4.269µs
I0719 01:46:01.812447   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-machine-config-operator/machine-config-server-968nk in Admin Network Policy controller
I0719 01:46:01.812451   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-machine-config-operator/machine-config-server-968nk Admin Network Policy controller: took 3.87µs
I0719 01:46:01.812456   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-monitoring/metrics-server-7d47f4cbc-5qp84 in Admin Network Policy controller
I0719 01:46:01.812460   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-monitoring/metrics-server-7d47f4cbc-5qp84 Admin Network Policy controller: took 4.48µs
I0719 01:46:01.812465   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-monitoring/node-exporter-9mlmj in Admin Network Policy controller
I0719 01:46:01.812469   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-monitoring/node-exporter-9mlmj Admin Network Policy controller: took 3.952µs
I0719 01:46:01.812473   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-monitoring/prometheus-operator-admission-webhook-67db68b49d-w8jqx in Admin Network Policy controller
I0719 01:46:01.812478   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-monitoring/prometheus-operator-admission-webhook-67db68b49d-w8jqx Admin Network Policy controller: took 4.074µs
I0719 01:46:01.812413   37437 factory.go:988] Added *v1.NetworkPolicy event handler 4
I0719 01:46:01.812483   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-cluster-node-tuning-operator/tuned-cjc5f in Admin Network Policy controller
I0719 01:46:01.812487   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-cluster-node-tuning-operator/tuned-cjc5f Admin Network Policy controller: took 4.382µs
I0719 01:46:01.812492   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-etcd/etcd-guard-00-50-56-8a-39-a0 in Admin Network Policy controller
I0719 01:46:01.812496   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-etcd/etcd-guard-00-50-56-8a-39-a0 Admin Network Policy controller: took 4.337µs
I0719 01:46:01.812501   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-network-operator/iptables-alerter-nh7z8 in Admin Network Policy controller
I0719 01:46:01.812505   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-network-operator/iptables-alerter-nh7z8 Admin Network Policy controller: took 3.825µs
I0719 01:46:01.812510   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-route-controller-manager/route-controller-manager-676cdfdbc8-t227m in Admin Network Policy controller
I0719 01:46:01.812514   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-route-controller-manager/route-controller-manager-676cdfdbc8-t227m Admin Network Policy controller: took 4.221µs
I0719 01:46:01.812519   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-machine-config-operator/machine-config-controller-b886dd6cb-6kjkp in Admin Network Policy controller
I0719 01:46:01.812389   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-ovn-kubernetes/ovnkube-node-5bqnj
I0719 01:46:01.812523   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-machine-config-operator/machine-config-controller-b886dd6cb-6kjkp Admin Network Policy controller: took 4.013µs
I0719 01:46:01.812542   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-oauth-apiserver/apiserver-86f656c4dd-x7cqj in Admin Network Policy controller
I0719 01:46:01.812530   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-ovn-kubernetes/ovnkube-node-mqh7r
I0719 01:46:01.812555   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-image-registry/node-ca-sq7qk
I0719 01:46:01.812543   37437 egressip.go:1052] syncStaleEgressReroutePolicy will remove stale nexthops: []
I0719 01:46:01.812563   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-44-52
I0719 01:46:01.812569   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-dns-operator/dns-operator-5fc6bf9796-jgj7s
I0719 01:46:01.812574   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-insights/insights-operator-586b65d57b-7rk2w
I0719 01:46:01.812579   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-ovn-kubernetes/ovnkube-node-9h9qr
I0719 01:46:01.812584   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-marketplace/community-operators-wgnxc
I0719 01:46:01.812589   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-monitoring/cluster-monitoring-operator-b4b4bcf9f-d4xhg
I0719 01:46:01.812593   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/ocs-client-operator-console-6fdbfcd95-jhcss
I0719 01:46:01.812596   37437 address_set.go:304] New(56bd379c-e2e9-4708-b784-36bd80cece61/default-network-controller:EgressIP:egressip-served-pods:v4/a4548040316634674295) with []
I0719 01:46:01.812555   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-oauth-apiserver/apiserver-86f656c4dd-x7cqj Admin Network Policy controller: took 11.443µs
I0719 01:46:01.812606   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-dns/node-resolver-djq2g in Admin Network Policy controller
I0719 01:46:01.812610   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-dns/node-resolver-djq2g Admin Network Policy controller: took 4.722µs
I0719 01:46:01.812615   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-etcd/etcd-00-50-56-8a-5c-ec in Admin Network Policy controller
I0719 01:46:01.812619   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-etcd/etcd-00-50-56-8a-5c-ec Admin Network Policy controller: took 3.996µs
I0719 01:46:01.812624   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-multus/multus-additional-cni-plugins-b5t42 in Admin Network Policy controller
I0719 01:46:01.812628   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-multus/multus-additional-cni-plugins-b5t42 Admin Network Policy controller: took 4.079µs
I0719 01:46:01.812620   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {56bd379c-e2e9-4708-b784-36bd80cece61}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.812633   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-multus/multus-additional-cni-plugins-pjk5m in Admin Network Policy controller
I0719 01:46:01.812637   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-multus/multus-additional-cni-plugins-pjk5m Admin Network Policy controller: took 5.293µs
I0719 01:46:01.812634   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {56bd379c-e2e9-4708-b784-36bd80cece61}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.812642   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-multus/multus-additional-cni-plugins-qdrk9 in Admin Network Policy controller
I0719 01:46:01.812647   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-multus/multus-additional-cni-plugins-qdrk9 Admin Network Policy controller: took 5.269µs
I0719 01:46:01.812652   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/csi-rbdplugin-xgkn6 in Admin Network Policy controller
I0719 01:46:01.812656   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/csi-rbdplugin-xgkn6 Admin Network Policy controller: took 4.153µs
I0719 01:46:01.812661   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/rook-ceph-crashcollector-00-50-56-8a-e1-e7-6c5dcb6f44-8z5np in Admin Network Policy controller
I0719 01:46:01.812665   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/rook-ceph-crashcollector-00-50-56-8a-e1-e7-6c5dcb6f44-8z5np Admin Network Policy controller: took 4.261µs
I0719 01:46:01.812670   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-image-registry/cluster-image-registry-operator-656868857f-f94pq in Admin Network Policy controller
I0719 01:46:01.812674   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-image-registry/cluster-image-registry-operator-656868857f-f94pq Admin Network Policy controller: took 4.094µs
I0719 01:46:01.812679   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-ingress-canary/ingress-canary-lsx7x in Admin Network Policy controller
I0719 01:46:01.812683   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-ingress-canary/ingress-canary-lsx7x Admin Network Policy controller: took 4.011µs
I0719 01:46:01.812687   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-5c-ec in Admin Network Policy controller
I0719 01:46:01.812692   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-5c-ec Admin Network Policy controller: took 4.479µs
I0719 01:46:01.812598   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-storage/rook-ceph-mds-ocs-storagecluster-cephfilesystem-a-8679ddf7kqp98
I0719 01:46:01.812696   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-network-diagnostics/network-check-target-gc5jl in Admin Network Policy controller
I0719 01:46:01.812706   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-network-diagnostics/network-check-target-gc5jl Admin Network Policy controller: took 9.227µs
I0719 01:46:01.812711   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-operator-lifecycle-manager/olm-operator-59f98dcc4-xqd8j in Admin Network Policy controller
I0719 01:46:01.812717   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-operator-lifecycle-manager/olm-operator-59f98dcc4-xqd8j Admin Network Policy controller: took 4.206µs
I0719 01:46:01.812706   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kube-controller-manager/kube-controller-manager-guard-00-50-56-8a-39-a0
I0719 01:46:01.812721   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/csi-cephfsplugin-provisioner-585f89d895-2b4wk in Admin Network Policy controller
I0719 01:46:01.812726   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/csi-cephfsplugin-provisioner-585f89d895-2b4wk Admin Network Policy controller: took 4.362µs
I0719 01:46:01.812747   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/noobaa-db-pg-0 in Admin Network Policy controller
I0719 01:46:01.812758   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/noobaa-db-pg-0 Admin Network Policy controller: took 25.556µs
I0719 01:46:01.812764   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-cluster-version/cluster-version-operator-78b5d9c79d-znx2p in Admin Network Policy controller
I0719 01:46:01.812768   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-cluster-version/cluster-version-operator-78b5d9c79d-znx2p Admin Network Policy controller: took 4.319µs
I0719 01:46:01.812773   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-dns/node-resolver-dpn9t in Admin Network Policy controller
I0719 01:46:01.812777   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-dns/node-resolver-dpn9t Admin Network Policy controller: took 3.889µs
I0719 01:46:01.812727   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-machine-api/cluster-baremetal-operator-5fb6f8f7d4-ltc5l
I0719 01:46:01.812781   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-monitoring/prometheus-operator-admission-webhook-67db68b49d-wbfqq in Admin Network Policy controller
I0719 01:46:01.812786   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-monitoring/prometheus-operator-admission-webhook-67db68b49d-wbfqq Admin Network Policy controller: took 4.787µs
I0719 01:46:01.812788   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-etcd/etcd-00-50-56-8a-39-a0
I0719 01:46:01.812791   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-controller-manager-operator/openshift-controller-manager-operator-cf8f9956c-x6xn5 in Admin Network Policy controller
I0719 01:46:01.812794   37437 admin_network_policy_controller.go:489] Adding Pod in Admin Network Policy controller openshift-kni-infra/keepalived-00-50-56-8a-f2-5d
I0719 01:46:01.812795   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-controller-manager-operator/openshift-controller-manager-operator-cf8f9956c-x6xn5 Admin Network Policy controller: took 4.384µs
I0719 01:46:01.812801   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kube-controller-manager-operator/kube-controller-manager-operator-85c67fcb8d-fg9j7 in Admin Network Policy controller
I0719 01:46:01.812805   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kube-controller-manager-operator/kube-controller-manager-operator-85c67fcb8d-fg9j7 Admin Network Policy controller: took 4.191µs
I0719 01:46:01.812810   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-44-52 in Admin Network Policy controller
I0719 01:46:01.812814   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-44-52 Admin Network Policy controller: took 3.954µs
I0719 01:46:01.812819   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-network-node-identity/network-node-identity-z7b9j in Admin Network Policy controller
I0719 01:46:01.812823   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-network-node-identity/network-node-identity-z7b9j Admin Network Policy controller: took 4.246µs
I0719 01:46:01.812827   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/csi-addons-controller-manager-6d78957fdf-gs4tk in Admin Network Policy controller
I0719 01:46:01.812831   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/csi-addons-controller-manager-6d78957fdf-gs4tk Admin Network Policy controller: took 3.895µs
I0719 01:46:01.812836   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-console/downloads-6967878986-76phj in Admin Network Policy controller
I0719 01:46:01.812840   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-console/downloads-6967878986-76phj Admin Network Policy controller: took 3.717µs
I0719 01:46:01.812844   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-image-registry/node-ca-tvhtl in Admin Network Policy controller
I0719 01:46:01.812848   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-image-registry/node-ca-tvhtl Admin Network Policy controller: took 3.886µs
I0719 01:46:01.812853   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-multus/multus-47wxd in Admin Network Policy controller
I0719 01:46:01.812857   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-multus/multus-47wxd Admin Network Policy controller: took 3.868µs
I0719 01:46:01.812862   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-route-controller-manager/route-controller-manager-676cdfdbc8-gt4t6 in Admin Network Policy controller
I0719 01:46:01.812866   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-route-controller-manager/route-controller-manager-676cdfdbc8-gt4t6 Admin Network Policy controller: took 4.185µs
I0719 01:46:01.812871   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/csi-rbdplugin-xkw8r in Admin Network Policy controller
I0719 01:46:01.812875   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/csi-rbdplugin-xkw8r Admin Network Policy controller: took 4.558µs
I0719 01:46:01.812880   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/ocs-client-operator-controller-manager-846f549988-v288f in Admin Network Policy controller
I0719 01:46:01.812884   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/ocs-client-operator-controller-manager-846f549988-v288f Admin Network Policy controller: took 3.968µs
I0719 01:46:01.812889   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/rook-ceph-osd-1-6db96b64cc-nw82d in Admin Network Policy controller
I0719 01:46:01.812892   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/rook-ceph-osd-1-6db96b64cc-nw82d Admin Network Policy controller: took 3.998µs
I0719 01:46:01.812897   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kni-infra/keepalived-00-50-56-8a-5c-ec in Admin Network Policy controller
I0719 01:46:01.812901   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kni-infra/keepalived-00-50-56-8a-5c-ec Admin Network Policy controller: took 3.903µs
I0719 01:46:01.812906   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kube-apiserver/kube-apiserver-00-50-56-8a-39-a0 in Admin Network Policy controller
I0719 01:46:01.812910   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kube-apiserver/kube-apiserver-00-50-56-8a-39-a0 Admin Network Policy controller: took 3.953µs
I0719 01:46:01.812915   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kube-storage-version-migrator/migrator-7fc5dd675b-tfjhl in Admin Network Policy controller
I0719 01:46:01.812920   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kube-storage-version-migrator/migrator-7fc5dd675b-tfjhl Admin Network Policy controller: took 4.399µs
I0719 01:46:01.812924   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-operator-lifecycle-manager/packageserver-6bf7d58455-k8qkk in Admin Network Policy controller
I0719 01:46:01.812929   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-operator-lifecycle-manager/packageserver-6bf7d58455-k8qkk Admin Network Policy controller: took 3.884µs
I0719 01:46:01.812933   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-39-a0 in Admin Network Policy controller
I0719 01:46:01.812937   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-39-a0 Admin Network Policy controller: took 3.903µs
I0719 01:46:01.812942   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-machine-config-operator/machine-config-daemon-p677g in Admin Network Policy controller
I0719 01:46:01.812945   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-machine-config-operator/machine-config-daemon-p677g Admin Network Policy controller: took 3.945µs
I0719 01:46:01.812950   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-monitoring/node-exporter-nvqsf in Admin Network Policy controller
I0719 01:46:01.812954   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-monitoring/node-exporter-nvqsf Admin Network Policy controller: took 3.887µs
I0719 01:46:01.812958   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-operator-lifecycle-manager/package-server-manager-74bbc7c476-4555r in Admin Network Policy controller
I0719 01:46:01.812962   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-operator-lifecycle-manager/package-server-manager-74bbc7c476-4555r Admin Network Policy controller: took 3.898µs
I0719 01:46:01.812967   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/csi-cephfsplugin-provisioner-585f89d895-ddwtl in Admin Network Policy controller
I0719 01:46:01.812970   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/csi-cephfsplugin-provisioner-585f89d895-ddwtl Admin Network Policy controller: took 3.995µs
I0719 01:46:01.812975   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-5c-ec in Admin Network Policy controller
I0719 01:46:01.812979   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-5c-ec Admin Network Policy controller: took 3.884µs
I0719 01:46:01.812992   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kube-scheduler/openshift-kube-scheduler-guard-00-50-56-8a-44-52 in Admin Network Policy controller
I0719 01:46:01.812996   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kube-scheduler/openshift-kube-scheduler-guard-00-50-56-8a-44-52 Admin Network Policy controller: took 4.279µs
I0719 01:46:01.813001   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/csi-cephfsplugin-s29g7 in Admin Network Policy controller
I0719 01:46:01.813005   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/csi-cephfsplugin-s29g7 Admin Network Policy controller: took 3.958µs
I0719 01:46:01.813010   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-config-operator/openshift-config-operator-59dc875ddb-rnq74 in Admin Network Policy controller
I0719 01:46:01.813016   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-config-operator/openshift-config-operator-59dc875ddb-rnq74 Admin Network Policy controller: took 6.16µs
I0719 01:46:01.813016   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-authentication-operator
I0719 01:46:01.813021   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-multus/multus-additional-cni-plugins-2kgg5 in Admin Network Policy controller
I0719 01:46:01.813025   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-multus/multus-additional-cni-plugins-2kgg5 Admin Network Policy controller: took 4.346µs
I0719 01:46:01.813026   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-host-network
I0719 01:46:01.813037   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-vsphere-infra
I0719 01:46:01.813039   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace kube-public
I0719 01:46:01.813048   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-ingress-canary
I0719 01:46:01.813052   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-machine-config-operator
I0719 01:46:01.813059   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-vsphere-infra took: 14.299µs
I0719 01:46:01.813061   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-ingress-canary took: 7.528µs
I0719 01:46:01.813065   37437 obj_retry.go:541] Creating *factory.egressIPNamespace kube-public took: 14.512µs
I0719 01:46:01.813068   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-console
I0719 01:46:01.813069   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-kube-scheduler-operator
I0719 01:46:01.813070   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-etcd-operator
I0719 01:46:01.813075   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-console took: 2.089µs
I0719 01:46:01.813076   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-infra
I0719 01:46:01.813080   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-authentication
I0719 01:46:01.813086   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-dns-operator
I0719 01:46:01.813088   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-kube-scheduler-operator took: 12.255µs
I0719 01:46:01.813091   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-infra took: 7.879µs
I0719 01:46:01.813094   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-node
I0719 01:46:01.813096   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-apiserver
I0719 01:46:01.813100   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-dns-operator took: 7.391µs
I0719 01:46:01.813104   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-apiserver took: 2.528µs
I0719 01:46:01.813106   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-user-workload-monitoring
I0719 01:46:01.813107   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-node took: 7.619µs
I0719 01:46:01.813114   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-ingress-operator
I0719 01:46:01.813114   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-user-workload-monitoring took: 2.147µs
I0719 01:46:01.813121   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-network-operator
I0719 01:46:01.813043   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-authentication-operator took: 17.459µs
I0719 01:46:01.813128   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-monitoring
I0719 01:46:01.813122   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-ingress-operator took: 2.025µs
I0719 01:46:01.813136   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-service-ca
I0719 01:46:01.813061   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-cluster-version
I0719 01:46:01.813143   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-service-ca took: 1.466µs
I0719 01:46:01.813148   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-ingress
I0719 01:46:01.813152   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-cluster-version took: 8.71µs
I0719 01:46:01.813156   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-ingress took: 3.183µs
I0719 01:46:01.813157   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-console-operator
I0719 01:46:01.813129   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-network-operator took: 2.206µs
I0719 01:46:01.813166   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-console-operator took: 1.443µs
I0719 01:46:01.813168   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift
I0719 01:46:01.813171   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-network-node-identity
I0719 01:46:01.813178   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-network-node-identity took: 1.712µs
I0719 01:46:01.813065   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-kube-storage-version-migrator
I0719 01:46:01.813183   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-config
I0719 01:46:01.813188   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-kube-storage-version-migrator took: 2.277µs
I0719 01:46:01.813190   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-config took: 1.801µs
I0719 01:46:01.813178   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift took: 3.415µs
I0719 01:46:01.813198   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-apiserver-operator
I0719 01:46:01.813204   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-apiserver-operator took: 1.52µs
I0719 01:46:01.813208   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-config-operator
I0719 01:46:01.813214   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-config-operator took: 1.697µs
I0719 01:46:01.813218   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-cloud-network-config-controller
I0719 01:46:01.813224   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-cloud-network-config-controller took: 1.28µs
I0719 01:46:01.813137   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-monitoring took: 3.077µs
I0719 01:46:01.813231   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-kube-apiserver-operator
I0719 01:46:01.813095   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-storage
I0719 01:46:01.813240   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-kube-apiserver-operator took: 3.883µs
I0719 01:46:01.813245   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-cloud-controller-manager
I0719 01:46:01.813245   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-storage took: 4.873µs
I0719 01:46:01.813251   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-cloud-controller-manager took: 2.011µs
I0719 01:46:01.813256   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-cluster-machine-approver
I0719 01:46:01.813263   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-cluster-machine-approver took: 2.801µs
I0719 01:46:01.813030   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-service-ca-operator/service-ca-operator-86c8d4bbfd-w2qxx in Admin Network Policy controller
I0719 01:46:01.813274   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-service-ca-operator/service-ca-operator-86c8d4bbfd-w2qxx Admin Network Policy controller: took 243.114µs
I0719 01:46:01.813283   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/rook-ceph-mds-ocs-storagecluster-cephfilesystem-b-c4dc5cd7zkffj in Admin Network Policy controller
I0719 01:46:01.813287   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/rook-ceph-mds-ocs-storagecluster-cephfilesystem-b-c4dc5cd7zkffj Admin Network Policy controller: took 5.219µs
I0719 01:46:01.813292   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-operator-lifecycle-manager/collect-profiles-28689225-j8wtn in Admin Network Policy controller
I0719 01:46:01.813297   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-operator-lifecycle-manager/collect-profiles-28689225-j8wtn Admin Network Policy controller: took 4.395µs
I0719 01:46:01.813302   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-ovn-kubernetes/ovnkube-node-568wp in Admin Network Policy controller
I0719 01:46:01.813306   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-ovn-kubernetes/ovnkube-node-568wp Admin Network Policy controller: took 4.274µs
I0719 01:46:01.813311   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/ocs-metrics-exporter-84f9766477-r8fxs in Admin Network Policy controller
I0719 01:46:01.813315   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/ocs-metrics-exporter-84f9766477-r8fxs Admin Network Policy controller: took 4.062µs
I0719 01:46:01.813320   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/rook-ceph-mon-a-6dc9d78597-7ttc9 in Admin Network Policy controller
I0719 01:46:01.813324   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/rook-ceph-mon-a-6dc9d78597-7ttc9 Admin Network Policy controller: took 3.83µs
I0719 01:46:01.813328   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kube-controller-manager/kube-controller-manager-guard-00-50-56-8a-5c-ec in Admin Network Policy controller
I0719 01:46:01.813332   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kube-controller-manager/kube-controller-manager-guard-00-50-56-8a-5c-ec Admin Network Policy controller: took 4.081µs
I0719 01:46:01.813338   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-machine-config-operator/machine-config-daemon-qpmqf in Admin Network Policy controller
I0719 01:46:01.813342   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-machine-config-operator/machine-config-daemon-qpmqf Admin Network Policy controller: took 4.844µs
I0719 01:46:01.813347   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-machine-api/metal3-599ff8f4b7-vntm7 in Admin Network Policy controller
I0719 01:46:01.813351   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-machine-api/metal3-599ff8f4b7-vntm7 Admin Network Policy controller: took 4.165µs
I0719 01:46:01.813355   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-marketplace/redhat-operators-mm6k4 in Admin Network Policy controller
I0719 01:46:01.813359   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-marketplace/redhat-operators-mm6k4 Admin Network Policy controller: took 3.958µs
I0719 01:46:01.813364   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-monitoring/alertmanager-main-0 in Admin Network Policy controller
I0719 01:46:01.813368   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-monitoring/alertmanager-main-0 Admin Network Policy controller: took 3.961µs
I0719 01:46:01.813252   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-kube-scheduler
I0719 01:46:01.813372   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-network-diagnostics/network-check-target-jhhzw in Admin Network Policy controller
I0719 01:46:01.813376   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-network-diagnostics/network-check-target-jhhzw Admin Network Policy controller: took 4.095µs
I0719 01:46:01.813380   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-kube-scheduler took: 3.932µs
I0719 01:46:01.813087   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-etcd-operator took: 8.93µs
I0719 01:46:01.813386   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-controller-manager
I0719 01:46:01.813389   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-console-user-settings
I0719 01:46:01.813393   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-controller-manager took: 1.493µs
I0719 01:46:01.813396   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-console-user-settings took: 1.301µs
I0719 01:46:01.813080   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-machine-config-operator took: 15.697µs
I0719 01:46:01.813402   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-etcd
I0719 01:46:01.813404   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-local-storage
I0719 01:46:01.813409   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-etcd took: 1.718µs
I0719 01:46:01.813412   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-local-storage took: 2.232µs
I0719 01:46:01.813381   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kube-scheduler/openshift-kube-scheduler-guard-00-50-56-8a-39-a0 in Admin Network Policy controller
I0719 01:46:01.813417   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-operators
I0719 01:46:01.813419   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kube-scheduler/openshift-kube-scheduler-guard-00-50-56-8a-39-a0 Admin Network Policy controller: took 38.502µs
I0719 01:46:01.813424   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-operators took: 1.741µs
I0719 01:46:01.813398   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-kube-controller-manager-operator
I0719 01:46:01.813429   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-cluster-node-tuning-operator
I0719 01:46:01.813434   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-kube-controller-manager-operator took: 1.819µs
I0719 01:46:01.813425   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-machine-api/ironic-proxy-sn8n9 in Admin Network Policy controller
I0719 01:46:01.813414   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-kube-apiserver
I0719 01:46:01.813442   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-machine-api/ironic-proxy-sn8n9 Admin Network Policy controller: took 16.799µs
I0719 01:46:01.813447   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-kube-apiserver took: 2.634µs
I0719 01:46:01.813008   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-insights
I0719 01:46:01.813473   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-insights took: 14.099µs
I0719 01:46:01.813485   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-oauth-apiserver
I0719 01:46:01.813492   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-oauth-apiserver took: 2.675µs
I0719 01:46:01.813497   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-cloud-controller-manager-operator
I0719 01:46:01.813504   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-cloud-controller-manager-operator took: 2.188µs
I0719 01:46:01.813508   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-nutanix-infra
I0719 01:46:01.813515   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-nutanix-infra took: 2.344µs
I0719 01:46:01.813056   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-host-network took: 16.09µs
I0719 01:46:01.813523   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-ovirt-infra
I0719 01:46:01.813529   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-ovirt-infra took: 2.306µs
I0719 01:46:01.813534   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-openstack-infra
I0719 01:46:01.813540   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-openstack-infra took: 2.003µs
I0719 01:46:01.813544   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-operator-lifecycle-manager
I0719 01:46:01.813550   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-operator-lifecycle-manager took: 2.126µs
I0719 01:46:01.813447   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kube-controller-manager/kube-controller-manager-guard-00-50-56-8a-44-52 in Admin Network Policy controller
I0719 01:46:01.813560   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kube-controller-manager/kube-controller-manager-guard-00-50-56-8a-44-52 Admin Network Policy controller: took 111.532µs
I0719 01:46:01.813569   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-local-storage/diskmaker-manager-wj2h7 in Admin Network Policy controller
I0719 01:46:01.813573   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-local-storage/diskmaker-manager-wj2h7 Admin Network Policy controller: took 5.091µs
I0719 01:46:01.813578   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-machine-config-operator/machine-config-server-j8kbc in Admin Network Policy controller
I0719 01:46:01.813584   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-machine-config-operator/machine-config-server-j8kbc Admin Network Policy controller: took 4.172µs
I0719 01:46:01.813589   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/csi-rbdplugin-provisioner-5dcc45fbf4-v5l2c in Admin Network Policy controller
I0719 01:46:01.813593   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/csi-rbdplugin-provisioner-5dcc45fbf4-v5l2c Admin Network Policy controller: took 3.935µs
I0719 01:46:01.813598   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-authentication/oauth-openshift-7c9d9dfc8c-ddj6k in Admin Network Policy controller
I0719 01:46:01.813602   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-authentication/oauth-openshift-7c9d9dfc8c-ddj6k Admin Network Policy controller: took 3.892µs
I0719 01:46:01.813606   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-cluster-node-tuning-operator/tuned-f4pbt in Admin Network Policy controller
I0719 01:46:01.813610   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-cluster-node-tuning-operator/tuned-f4pbt Admin Network Policy controller: took 3.877µs
I0719 01:46:01.813615   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-etcd/revision-pruner-9-00-50-56-8a-44-52 in Admin Network Policy controller
I0719 01:46:01.813619   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-etcd/revision-pruner-9-00-50-56-8a-44-52 Admin Network Policy controller: took 4.03µs
I0719 01:46:01.813624   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-monitoring/telemeter-client-7b74cd774c-fg6lz in Admin Network Policy controller
I0719 01:46:01.813628   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-monitoring/telemeter-client-7b74cd774c-fg6lz Admin Network Policy controller: took 4.259µs
I0719 01:46:01.813633   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-multus/multus-mqkdb in Admin Network Policy controller
I0719 01:46:01.813637   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-multus/multus-mqkdb Admin Network Policy controller: took 3.96µs
I0719 01:46:01.813641   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-console-operator/console-operator-76c8786869-jr6r2 in Admin Network Policy controller
I0719 01:46:01.813645   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-console-operator/console-operator-76c8786869-jr6r2 Admin Network Policy controller: took 3.963µs
I0719 01:46:01.813066   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-cloud-platform-infra
I0719 01:46:01.813650   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-console/downloads-6967878986-hpkbw in Admin Network Policy controller
I0719 01:46:01.813654   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-console/downloads-6967878986-hpkbw Admin Network Policy controller: took 4.057µs
I0719 01:46:01.813659   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/ocs-operator-5567c4fdb4-8b9zr in Admin Network Policy controller
I0719 01:46:01.813662   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/ocs-operator-5567c4fdb4-8b9zr Admin Network Policy controller: took 3.923µs
I0719 01:46:01.813668   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-ingress-canary/ingress-canary-lrjr5 in Admin Network Policy controller
I0719 01:46:01.813672   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-ingress-canary/ingress-canary-lrjr5 Admin Network Policy controller: took 3.981µs
I0719 01:46:01.813676   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-machine-api/machine-api-operator-5cb7d5868-9p8wr in Admin Network Policy controller
I0719 01:46:01.813680   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-machine-api/machine-api-operator-5cb7d5868-9p8wr Admin Network Policy controller: took 4.096µs
I0719 01:46:01.813685   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-multus/multus-sv782 in Admin Network Policy controller
I0719 01:46:01.813689   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-multus/multus-sv782 Admin Network Policy controller: took 3.781µs
I0719 01:46:01.813713   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-apiserver/apiserver-7d9bbd465d-ln8v5 in Admin Network Policy controller
I0719 01:46:01.813717   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-apiserver/apiserver-7d9bbd465d-ln8v5 Admin Network Policy controller: took 5.376µs
I0719 01:46:01.813662   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-cloud-platform-infra took: 8.776µs
I0719 01:46:01.813722   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-console-operator/console-conversion-webhook-664b4df6f5-nq9pd in Admin Network Policy controller
I0719 01:46:01.813726   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-kube-storage-version-migrator-operator
I0719 01:46:01.813728   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-console-operator/console-conversion-webhook-664b4df6f5-nq9pd Admin Network Policy controller: took 5.447µs
I0719 01:46:01.813733   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-monitoring/kube-state-metrics-589b9987d-ck4ch in Admin Network Policy controller
I0719 01:46:01.813735   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-kube-storage-version-migrator-operator took: 3.669µs
I0719 01:46:01.813737   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-monitoring/kube-state-metrics-589b9987d-ck4ch Admin Network Policy controller: took 3.875µs
I0719 01:46:01.813740   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-config-managed
I0719 01:46:01.813742   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-network-operator/iptables-alerter-m44lf in Admin Network Policy controller
I0719 01:46:01.813746   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-network-operator/iptables-alerter-m44lf Admin Network Policy controller: took 4.068µs
I0719 01:46:01.813751   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kube-apiserver/kube-apiserver-guard-00-50-56-8a-39-a0 in Admin Network Policy controller
I0719 01:46:01.813755   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kube-apiserver/kube-apiserver-guard-00-50-56-8a-39-a0 Admin Network Policy controller: took 3.7µs
I0719 01:46:01.813759   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-machine-api/ironic-proxy-6zm7s in Admin Network Policy controller
I0719 01:46:01.813764   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-machine-api/ironic-proxy-6zm7s Admin Network Policy controller: took 3.748µs
I0719 01:46:01.813769   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-operator-lifecycle-manager/collect-profiles-28689210-mbs94 in Admin Network Policy controller
I0719 01:46:01.813773   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-operator-lifecycle-manager/collect-profiles-28689210-mbs94 Admin Network Policy controller: took 4.253µs
I0719 01:46:01.813778   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-dns/dns-default-5hh4c in Admin Network Policy controller
I0719 01:46:01.813782   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-dns/dns-default-5hh4c Admin Network Policy controller: took 3.951µs
I0719 01:46:01.813786   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-dns/dns-default-wn5nz in Admin Network Policy controller
I0719 01:46:01.813790   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-dns/dns-default-wn5nz Admin Network Policy controller: took 3.762µs
I0719 01:46:01.813795   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-controller-manager/controller-manager-5c7f9f9d47-c74xp in Admin Network Policy controller
I0719 01:46:01.813799   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-controller-manager/controller-manager-5c7f9f9d47-c74xp Admin Network Policy controller: took 3.909µs
I0719 01:46:01.813803   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-apiserver/apiserver-7d9bbd465d-7pbl8 in Admin Network Policy controller
I0719 01:46:01.813807   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-apiserver/apiserver-7d9bbd465d-7pbl8 Admin Network Policy controller: took 3.813µs
I0719 01:46:01.813812   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-authentication/oauth-openshift-7c9d9dfc8c-qcf89 in Admin Network Policy controller
I0719 01:46:01.813816   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-authentication/oauth-openshift-7c9d9dfc8c-qcf89 Admin Network Policy controller: took 4.574µs
I0719 01:46:01.813821   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-39-a0 in Admin Network Policy controller
I0719 01:46:01.813826   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-39-a0 Admin Network Policy controller: took 4.339µs
I0719 01:46:01.813831   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-cluster-storage-operator/csi-snapshot-controller-operator-bb8d9765b-b24f6 in Admin Network Policy controller
I0719 01:46:01.813835   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-cluster-storage-operator/csi-snapshot-controller-operator-bb8d9765b-b24f6 Admin Network Policy controller: took 4.434µs
I0719 01:46:01.813839   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kube-apiserver/kube-apiserver-00-50-56-8a-5c-ec in Admin Network Policy controller
I0719 01:46:01.813843   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kube-apiserver/kube-apiserver-00-50-56-8a-5c-ec Admin Network Policy controller: took 3.852µs
I0719 01:46:01.813848   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kube-apiserver-operator/kube-apiserver-operator-55dc5cdcf9-p4csg in Admin Network Policy controller
I0719 01:46:01.813852   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kube-apiserver-operator/kube-apiserver-operator-55dc5cdcf9-p4csg Admin Network Policy controller: took 4.054µs
I0719 01:46:01.813856   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kube-scheduler/revision-pruner-6-00-50-56-8a-39-a0 in Admin Network Policy controller
I0719 01:46:01.813860   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kube-scheduler/revision-pruner-6-00-50-56-8a-39-a0 Admin Network Policy controller: took 3.746µs
I0719 01:46:01.813864   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-monitoring/prometheus-operator-848d66f7-nx2v2 in Admin Network Policy controller
I0719 01:46:01.813868   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-monitoring/prometheus-operator-848d66f7-nx2v2 Admin Network Policy controller: took 4.101µs
I0719 01:46:01.813873   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/rook-ceph-mon-c-5b4c4697fb-8w28d in Admin Network Policy controller
I0719 01:46:01.813746   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-config-managed took: 1.588µs
I0719 01:46:01.813883   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-image-registry
I0719 01:46:01.813892   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-image-registry took: 3.609µs
I0719 01:46:01.813109   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-route-controller-manager
I0719 01:46:01.813902   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-route-controller-manager took: 2.186µs
I0719 01:46:01.813906   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-machine-api
I0719 01:46:01.813914   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-machine-api took: 3.717µs
I0719 01:46:01.813919   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-controller-manager-operator
I0719 01:46:01.813927   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-controller-manager-operator took: 3.711µs
I0719 01:46:01.813931   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-kni-infra
I0719 01:46:01.813938   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-kni-infra took: 2.718µs
I0719 01:46:01.813155   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace kube-system
I0719 01:46:01.813953   37437 obj_retry.go:541] Creating *factory.egressIPNamespace kube-system took: 7.412µs
I0719 01:46:01.813958   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-cluster-storage-operator
I0719 01:46:01.813964   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-cluster-storage-operator took: 1.53µs
I0719 01:46:01.813968   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-cluster-samples-operator
I0719 01:46:01.813974   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-cluster-samples-operator took: 1.582µs
I0719 01:46:01.813162   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-cluster-csi-drivers
I0719 01:46:01.813990   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-cluster-csi-drivers took: 8.637µs
I0719 01:46:01.813995   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace kube-node-lease
I0719 01:46:01.814001   37437 obj_retry.go:541] Creating *factory.egressIPNamespace kube-node-lease took: 1.265µs
I0719 01:46:01.813193   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-marketplace
I0719 01:46:01.814012   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-marketplace took: 4.116µs
I0719 01:46:01.814017   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-service-ca-operator
I0719 01:46:01.814023   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-service-ca-operator took: 1.462µs
I0719 01:46:01.814027   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-network-diagnostics
I0719 01:46:01.814033   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-network-diagnostics took: 1.657µs
I0719 01:46:01.813437   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-cluster-node-tuning-operator took: 3.144µs
I0719 01:46:01.813072   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-kube-controller-manager
I0719 01:46:01.814045   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-kube-controller-manager took: 2.057µs
I0719 01:46:01.814049   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-cloud-credential-operator
I0719 01:46:01.814056   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-cloud-credential-operator took: 2.819µs
I0719 01:46:01.814061   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-multus
I0719 01:46:01.814069   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-multus took: 3.154µs
I0719 01:46:01.814073   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace default
I0719 01:46:01.814079   37437 obj_retry.go:541] Creating *factory.egressIPNamespace default took: 1.7µs
I0719 01:46:01.813087   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-authentication took: 2.186µs
I0719 01:46:01.814086   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace assisted-installer
I0719 01:46:01.814094   37437 obj_retry.go:541] Creating *factory.egressIPNamespace assisted-installer took: 2.431µs
I0719 01:46:01.814098   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-ovn-kubernetes
I0719 01:46:01.814104   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-ovn-kubernetes took: 1.979µs
I0719 01:46:01.814108   37437 obj_retry.go:502] Add event received for *factory.egressIPNamespace openshift-dns
I0719 01:46:01.814115   37437 obj_retry.go:541] Creating *factory.egressIPNamespace openshift-dns took: 2.154µs
I0719 01:46:01.813877   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/rook-ceph-mon-c-5b4c4697fb-8w28d Admin Network Policy controller: took 4.115µs
I0719 01:46:01.814143   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-cluster-storage-operator/csi-snapshot-webhook-85b445968-78v7q in Admin Network Policy controller
I0719 01:46:01.814150   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-cluster-storage-operator/csi-snapshot-webhook-85b445968-78v7q Admin Network Policy controller: took 7.255µs
I0719 01:46:01.814123   37437 factory.go:988] Added *v1.Namespace event handler 6
I0719 01:46:01.814155   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-etcd/etcd-00-50-56-8a-44-52 in Admin Network Policy controller
I0719 01:46:01.814160   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-etcd/etcd-00-50-56-8a-44-52 Admin Network Policy controller: took 4.831µs
I0719 01:46:01.814164   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-39-a0 in Admin Network Policy controller
I0719 01:46:01.814168   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-39-a0 Admin Network Policy controller: took 4.002µs
I0719 01:46:01.814173   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-machine-config-operator/machine-config-operator-7fc5c776cc-r6wsl in Admin Network Policy controller
I0719 01:46:01.814177   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-machine-config-operator/machine-config-operator-7fc5c776cc-r6wsl Admin Network Policy controller: took 4.004µs
I0719 01:46:01.814182   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-monitoring/prometheus-k8s-1 in Admin Network Policy controller
I0719 01:46:01.814187   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-monitoring/prometheus-k8s-1 Admin Network Policy controller: took 3.816µs
I0719 01:46:01.814196   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-oauth-apiserver/apiserver-86f656c4dd-2pxdq in Admin Network Policy controller
I0719 01:46:01.814200   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-oauth-apiserver/apiserver-86f656c4dd-2pxdq Admin Network Policy controller: took 5.166µs
I0719 01:46:01.814205   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-oauth-apiserver/apiserver-86f656c4dd-g82dw in Admin Network Policy controller
I0719 01:46:01.814209   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-oauth-apiserver/apiserver-86f656c4dd-g82dw Admin Network Policy controller: took 3.729µs
I0719 01:46:01.814213   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-cluster-storage-operator/csi-snapshot-webhook-85b445968-9dpmd in Admin Network Policy controller
I0719 01:46:01.814218   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-cluster-storage-operator/csi-snapshot-webhook-85b445968-9dpmd Admin Network Policy controller: took 3.93µs
I0719 01:46:01.814222   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-dns/dns-default-24pdt in Admin Network Policy controller
I0719 01:46:01.814226   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-dns/dns-default-24pdt Admin Network Policy controller: took 4.226µs
I0719 01:46:01.814231   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-etcd/etcd-guard-00-50-56-8a-5c-ec in Admin Network Policy controller
I0719 01:46:01.814235   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-etcd/etcd-guard-00-50-56-8a-5c-ec Admin Network Policy controller: took 3.877µs
I0719 01:46:01.814239   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kni-infra/coredns-00-50-56-8a-39-a0 in Admin Network Policy controller
I0719 01:46:01.814243   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kni-infra/coredns-00-50-56-8a-39-a0 Admin Network Policy controller: took 3.838µs
I0719 01:46:01.814248   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-cluster-machine-approver/machine-approver-5bf6544664-79krt in Admin Network Policy controller
I0719 01:46:01.814252   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-cluster-machine-approver/machine-approver-5bf6544664-79krt Admin Network Policy controller: took 4.162µs
I0719 01:46:01.814256   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-cluster-samples-operator/cluster-samples-operator-6b95974b98-cxvvt in Admin Network Policy controller
I0719 01:46:01.814256   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-multus/multus-sv782
I0719 01:46:01.814278   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-multus/multus-sv782 took: 11.628µs
I0719 01:46:01.814284   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-operator-lifecycle-manager/collect-profiles-28689210-mbs94
I0719 01:46:01.814284   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-apiserver/apiserver-7d9bbd465d-ln8v5
I0719 01:46:01.814293   37437 obj_retry.go:459] Detected object openshift-operator-lifecycle-manager/collect-profiles-28689210-mbs94 of type *factory.egressIPPod in terminal state (e.g. completed) during add event: will remove it
I0719 01:46:01.814294   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-dns/dns-default-5hh4c
I0719 01:46:01.814298   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-monitoring/kube-state-metrics-589b9987d-ck4ch
I0719 01:46:01.814310   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-authentication/oauth-openshift-7c9d9dfc8c-qcf89
I0719 01:46:01.814311   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-apiserver/apiserver-7d9bbd465d-ln8v5 took: 12.445µs
I0719 01:46:01.814315   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-dns/dns-default-5hh4c took: 12.608µs
I0719 01:46:01.814318   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-apiserver/apiserver-7d9bbd465d-7pbl8
I0719 01:46:01.814321   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-dns/dns-default-wn5nz
I0719 01:46:01.814322   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-ingress-canary/ingress-canary-lrjr5
I0719 01:46:01.814330   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-machine-api/ironic-proxy-6zm7s
I0719 01:46:01.814332   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-cluster-storage-operator/csi-snapshot-controller-operator-bb8d9765b-b24f6
I0719 01:46:01.814340   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-39-a0
I0719 01:46:01.814346   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-machine-api/ironic-proxy-6zm7s took: 8.729µs
I0719 01:46:01.814332   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-machine-api/machine-api-operator-5cb7d5868-9p8wr
I0719 01:46:01.814350   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-dns/dns-default-wn5nz took: 22.179µs
I0719 01:46:01.814318   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-authentication/oauth-openshift-7c9d9dfc8c-qcf89 took: 2.182µs
I0719 01:46:01.814356   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kube-apiserver/kube-apiserver-00-50-56-8a-5c-ec
I0719 01:46:01.814357   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-39-a0 took: 11.481µs
I0719 01:46:01.814360   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-dns/dns-default-24pdt
I0719 01:46:01.814363   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-machine-api/machine-api-operator-5cb7d5868-9p8wr took: 8.663µs
I0719 01:46:01.814352   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-controller-manager/controller-manager-5c7f9f9d47-c74xp
I0719 01:46:01.814369   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-monitoring/prometheus-operator-848d66f7-nx2v2
I0719 01:46:01.814316   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-console-operator/console-conversion-webhook-664b4df6f5-nq9pd
I0719 01:46:01.814378   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-monitoring/prometheus-operator-848d66f7-nx2v2 took: 2.023µs
I0719 01:46:01.814380   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-controller-manager/controller-manager-5c7f9f9d47-c74xp took: 8.622µs
I0719 01:46:01.814383   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-cloud-credential-operator/cloud-credential-operator-6488fd5f9b-jkdg2
I0719 01:46:01.814385   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-monitoring/prometheus-k8s-0
I0719 01:46:01.814388   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-console-operator/console-conversion-webhook-664b4df6f5-nq9pd took: 8.616µs
I0719 01:46:01.814390   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-cloud-credential-operator/cloud-credential-operator-6488fd5f9b-jkdg2 took: 1.701µs
I0719 01:46:01.814393   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-monitoring/prometheus-k8s-0 took: 2.377µs
I0719 01:46:01.814349   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-ingress-canary/ingress-canary-lrjr5 took: 12.442µs
I0719 01:46:01.814398   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kube-apiserver/revision-pruner-8-00-50-56-8a-39-a0
I0719 01:46:01.814403   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-cluster-storage-operator/csi-snapshot-webhook-85b445968-9dpmd
I0719 01:46:01.814347   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-cluster-storage-operator/csi-snapshot-controller-operator-bb8d9765b-b24f6 took: 7.966µs
I0719 01:46:01.814410   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-cluster-storage-operator/csi-snapshot-webhook-85b445968-9dpmd took: 1.658µs
I0719 01:46:01.814403   37437 obj_retry.go:459] Detected object openshift-kube-apiserver/revision-pruner-8-00-50-56-8a-39-a0 of type *factory.egressIPPod in terminal state (e.g. completed) during add event: will remove it
I0719 01:46:01.814413   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-cluster-storage-operator/csi-snapshot-webhook-85b445968-78v7q
I0719 01:46:01.814420   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/noobaa-endpoint-6ddf6bb6b-jmx4r
I0719 01:46:01.814429   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/noobaa-endpoint-6ddf6bb6b-jmx4r took: 3.222µs
I0719 01:46:01.814434   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-authentication/oauth-openshift-7c9d9dfc8c-lxcsb
I0719 01:46:01.814370   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-dns/dns-default-24pdt took: 3.744µs
I0719 01:46:01.814446   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-monitoring/node-exporter-s77zj
I0719 01:46:01.814261   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-cluster-samples-operator/cluster-samples-operator-6b95974b98-cxvvt Admin Network Policy controller: took 4.153µs
I0719 01:46:01.814453   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-monitoring/node-exporter-s77zj took: 2.158µs
I0719 01:46:01.814455   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-multus/network-metrics-daemon-gqqpq in Admin Network Policy controller
I0719 01:46:01.814458   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-multus/multus-admission-controller-5cc499c6f4-bngv4
I0719 01:46:01.814460   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-multus/network-metrics-daemon-gqqpq Admin Network Policy controller: took 5.348µs
I0719 01:46:01.814465   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-monitoring/node-exporter-s77zj in Admin Network Policy controller
I0719 01:46:01.814326   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-apiserver/apiserver-7d9bbd465d-7pbl8 took: 1.741µs
I0719 01:46:01.814470   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-monitoring/node-exporter-s77zj Admin Network Policy controller: took 4.592µs
I0719 01:46:01.814477   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-monitoring/prometheus-k8s-0 in Admin Network Policy controller
I0719 01:46:01.814481   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-monitoring/prometheus-k8s-0 Admin Network Policy controller: took 3.846µs
I0719 01:46:01.814466   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-multus/multus-admission-controller-5cc499c6f4-bngv4 took: 1.804µs
I0719 01:46:01.814485   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-ingress/router-default-54fb8ffc6b-hhdt2 in Admin Network Policy controller
I0719 01:46:01.814490   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-ingress/router-default-54fb8ffc6b-hhdt2 Admin Network Policy controller: took 4.221µs
I0719 01:46:01.814491   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kni-infra/haproxy-00-50-56-8a-44-52
I0719 01:46:01.814494   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kube-apiserver/revision-pruner-8-00-50-56-8a-39-a0 in Admin Network Policy controller
I0719 01:46:01.814500   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kni-infra/haproxy-00-50-56-8a-44-52 took: 3.037µs
I0719 01:46:01.814505   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-dns/dns-default-zwbjg
I0719 01:46:01.814510   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kube-apiserver/revision-pruner-8-00-50-56-8a-39-a0 Admin Network Policy controller: took 4.155µs
I0719 01:46:01.814516   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-network-diagnostics/network-check-target-vltnw in Admin Network Policy controller
I0719 01:46:01.814519   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-network-diagnostics/network-check-target-vltnw Admin Network Policy controller: took 3.9µs
I0719 01:46:01.814525   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-network-node-identity/network-node-identity-tzcq8 in Admin Network Policy controller
I0719 01:46:01.814528   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-network-node-identity/network-node-identity-tzcq8 Admin Network Policy controller: took 3.799µs
I0719 01:46:01.814434   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-cluster-storage-operator/csi-snapshot-webhook-85b445968-78v7q took: 10.855µs
I0719 01:46:01.814533   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-console/console-f7dbc9784-cj9wp in Admin Network Policy controller
I0719 01:46:01.814537   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-console/console-f7dbc9784-cj9wp Admin Network Policy controller: took 4.045µs
I0719 01:46:01.814542   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-ingress-canary/ingress-canary-zxwrq in Admin Network Policy controller
I0719 01:46:01.814546   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-ingress-canary/ingress-canary-zxwrq Admin Network Policy controller: took 4.019µs
I0719 01:46:01.814511   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-dns/dns-default-zwbjg took: 1.47µs
I0719 01:46:01.814551   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-local-storage/diskmaker-manager-vrh5h in Admin Network Policy controller
I0719 01:46:01.814554   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-local-storage/diskmaker-manager-2zrc6
I0719 01:46:01.814472   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-machine-config-operator/machine-config-operator-7fc5c776cc-r6wsl
I0719 01:46:01.814579   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-machine-config-operator/machine-config-operator-7fc5c776cc-r6wsl took: 2.974µs
I0719 01:46:01.814585   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-local-storage/diskmaker-manager-vrh5h
I0719 01:46:01.814591   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-local-storage/diskmaker-manager-vrh5h took: 2.001µs
I0719 01:46:01.814596   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-route-controller-manager/route-controller-manager-676cdfdbc8-t6rhq
I0719 01:46:01.814602   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-route-controller-manager/route-controller-manager-676cdfdbc8-t6rhq took: 1.359µs
I0719 01:46:01.814556   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-local-storage/diskmaker-manager-vrh5h Admin Network Policy controller: took 4.404µs
I0719 01:46:01.814606   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/rook-ceph-mon-b-59759dbb89-7jlvw
I0719 01:46:01.814613   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/rook-ceph-mon-b-59759dbb89-7jlvw took: 2.287µs
I0719 01:46:01.814618   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-network-operator/iptables-alerter-wxl7s
I0719 01:46:01.814625   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-network-operator/iptables-alerter-wxl7s took: 1.842µs
I0719 01:46:01.814629   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-network-diagnostics/network-check-target-dj4vt
I0719 01:46:01.814636   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-network-diagnostics/network-check-target-dj4vt took: 1.975µs
I0719 01:46:01.814640   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-service-ca/service-ca-6dbc4646f9-6q769
I0719 01:46:01.814646   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-service-ca/service-ca-6dbc4646f9-6q769 took: 1.134µs
I0719 01:46:01.814650   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-machine-api/ironic-proxy-k9xzh
I0719 01:46:01.814656   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-machine-api/ironic-proxy-k9xzh took: 1.5µs
I0719 01:46:01.814661   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/ocs-client-operator-console-6fdbfcd95-jhcss
I0719 01:46:01.814667   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/ocs-client-operator-console-6fdbfcd95-jhcss took: 1.88µs
I0719 01:46:01.814671   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kube-apiserver/kube-apiserver-guard-00-50-56-8a-44-52
I0719 01:46:01.814677   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kube-apiserver/kube-apiserver-guard-00-50-56-8a-44-52 took: 1.517µs
I0719 01:46:01.814536   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-oauth-apiserver/apiserver-86f656c4dd-g82dw
I0719 01:46:01.814682   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-monitoring/monitoring-plugin-6f457fd4b8-pqp4m
I0719 01:46:01.814688   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-oauth-apiserver/apiserver-86f656c4dd-g82dw took: 2.304µs
I0719 01:46:01.814689   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-monitoring/monitoring-plugin-6f457fd4b8-pqp4m took: 2.012µs
I0719 01:46:01.814694   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-cluster-node-tuning-operator/cluster-node-tuning-operator-68cc9c9cf9-6brm7
I0719 01:46:01.814703   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-cluster-node-tuning-operator/cluster-node-tuning-operator-68cc9c9cf9-6brm7 took: 2.522µs
I0719 01:46:01.814708   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kni-infra/keepalived-00-50-56-8a-fb-ea
I0719 01:46:01.814715   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kni-infra/keepalived-00-50-56-8a-fb-ea took: 2.562µs
I0719 01:46:01.814720   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-machine-config-operator/machine-config-daemon-vllgq
I0719 01:46:01.814726   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-machine-config-operator/machine-config-daemon-vllgq took: 2.007µs
I0719 01:46:01.814731   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-etcd/revision-pruner-9-00-50-56-8a-5c-ec
I0719 01:46:01.814736   37437 obj_retry.go:459] Detected object openshift-etcd/revision-pruner-9-00-50-56-8a-5c-ec of type *factory.egressIPPod in terminal state (e.g. completed) during add event: will remove it
I0719 01:46:01.814613   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-ovn-kubernetes/ovnkube-node-62ccc in Admin Network Policy controller
I0719 01:46:01.814751   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-ovn-kubernetes/ovnkube-node-62ccc Admin Network Policy controller: took 137.607µs
I0719 01:46:01.814762   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-cloud-credential-operator/cloud-credential-operator-6488fd5f9b-jkdg2 in Admin Network Policy controller
I0719 01:46:01.814767   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-cloud-credential-operator/cloud-credential-operator-6488fd5f9b-jkdg2 Admin Network Policy controller: took 5.426µs
I0719 01:46:01.814773   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-dns/node-resolver-r7f9m in Admin Network Policy controller
I0719 01:46:01.814777   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-dns/node-resolver-r7f9m Admin Network Policy controller: took 4.333µs
I0719 01:46:01.814782   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-multus/multus-admission-controller-5cc499c6f4-bngv4 in Admin Network Policy controller
I0719 01:46:01.814786   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-multus/multus-admission-controller-5cc499c6f4-bngv4 Admin Network Policy controller: took 4.031µs
I0719 01:46:01.814791   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-apiserver-operator/openshift-apiserver-operator-84fc88fd69-mqjqx in Admin Network Policy controller
I0719 01:46:01.814795   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-apiserver-operator/openshift-apiserver-operator-84fc88fd69-mqjqx Admin Network Policy controller: took 4.116µs
I0719 01:46:01.814800   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kni-infra/coredns-00-50-56-8a-5c-ec in Admin Network Policy controller
I0719 01:46:01.814804   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kni-infra/coredns-00-50-56-8a-5c-ec Admin Network Policy controller: took 4.044µs
I0719 01:46:01.814809   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kube-apiserver/kube-apiserver-00-50-56-8a-44-52 in Admin Network Policy controller
I0719 01:46:01.814416   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-ingress-canary/ingress-canary-zxwrq
I0719 01:46:01.814812   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kube-apiserver/kube-apiserver-00-50-56-8a-44-52 Admin Network Policy controller: took 3.868µs
I0719 01:46:01.814817   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-multus/multus-admission-controller-5cc499c6f4-jtjqw in Admin Network Policy controller
I0719 01:46:01.814819   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-ingress-canary/ingress-canary-zxwrq took: 2.202µs
I0719 01:46:01.814821   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-multus/multus-admission-controller-5cc499c6f4-jtjqw Admin Network Policy controller: took 3.889µs
I0719 01:46:01.814825   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-cluster-node-tuning-operator/tuned-hpvxx
I0719 01:46:01.814827   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/noobaa-endpoint-6ddf6bb6b-jmx4r in Admin Network Policy controller
I0719 01:46:01.814831   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/noobaa-endpoint-6ddf6bb6b-jmx4r Admin Network Policy controller: took 4.094µs
I0719 01:46:01.814836   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-cluster-node-tuning-operator/cluster-node-tuning-operator-68cc9c9cf9-6brm7 in Admin Network Policy controller
I0719 01:46:01.814840   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-cluster-node-tuning-operator/cluster-node-tuning-operator-68cc9c9cf9-6brm7 Admin Network Policy controller: took 4.391µs
I0719 01:46:01.814845   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kni-infra/coredns-00-50-56-8a-e1-e7 in Admin Network Policy controller
I0719 01:46:01.814849   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kni-infra/coredns-00-50-56-8a-e1-e7 Admin Network Policy controller: took 3.842µs
I0719 01:46:01.814854   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-image-registry/node-ca-kqt8n in Admin Network Policy controller
I0719 01:46:01.814858   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-image-registry/node-ca-kqt8n Admin Network Policy controller: took 4.063µs
I0719 01:46:01.814862   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kni-infra/keepalived-00-50-56-8a-fb-ea in Admin Network Policy controller
I0719 01:46:01.814866   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kni-infra/keepalived-00-50-56-8a-fb-ea Admin Network Policy controller: took 3.964µs
I0719 01:46:01.814871   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-monitoring/monitoring-plugin-6f457fd4b8-6wb4z in Admin Network Policy controller
I0719 01:46:01.814875   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-monitoring/monitoring-plugin-6f457fd4b8-6wb4z Admin Network Policy controller: took 3.975µs
I0719 01:46:01.814879   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/rook-ceph-osd-2-9c5dbbd88-crlql in Admin Network Policy controller
I0719 01:46:01.814883   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/rook-ceph-osd-2-9c5dbbd88-crlql Admin Network Policy controller: took 3.812µs
I0719 01:46:01.814888   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-cluster-node-tuning-operator/tuned-x2svx in Admin Network Policy controller
I0719 01:46:01.814891   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-cluster-node-tuning-operator/tuned-x2svx Admin Network Policy controller: took 3.926µs
I0719 01:46:01.814695   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-machine-config-operator/machine-config-daemon-4kr96
I0719 01:46:01.814896   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-dns/dns-default-rj9px in Admin Network Policy controller
I0719 01:46:01.814901   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-dns/dns-default-rj9px Admin Network Policy controller: took 4.682µs
I0719 01:46:01.814903   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-machine-config-operator/machine-config-daemon-4kr96 took: 2.652µs
I0719 01:46:01.814906   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kni-infra/haproxy-00-50-56-8a-44-52 in Admin Network Policy controller
I0719 01:46:01.814909   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kube-scheduler/revision-pruner-6-00-50-56-8a-5c-ec
I0719 01:46:01.814910   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kni-infra/haproxy-00-50-56-8a-44-52 Admin Network Policy controller: took 4.327µs
I0719 01:46:01.814914   37437 obj_retry.go:459] Detected object openshift-kube-scheduler/revision-pruner-6-00-50-56-8a-5c-ec of type *factory.egressIPPod in terminal state (e.g. completed) during add event: will remove it
I0719 01:46:01.814916   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-machine-config-operator/machine-config-server-zwkfw in Admin Network Policy controller
I0719 01:46:01.814921   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-machine-config-operator/machine-config-server-zwkfw Admin Network Policy controller: took 5.606µs
I0719 01:46:01.814926   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-network-operator/iptables-alerter-m6v49 in Admin Network Policy controller
I0719 01:46:01.814932   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-network-operator/iptables-alerter-m6v49 Admin Network Policy controller: took 4.089µs
I0719 01:46:01.814936   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-authentication/oauth-openshift-7c9d9dfc8c-lxcsb in Admin Network Policy controller
I0719 01:46:01.814940   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-authentication/oauth-openshift-7c9d9dfc8c-lxcsb Admin Network Policy controller: took 3.917µs
I0719 01:46:01.814945   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-cluster-node-tuning-operator/tuned-hpvxx in Admin Network Policy controller
I0719 01:46:01.814949   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-cluster-node-tuning-operator/tuned-hpvxx Admin Network Policy controller: took 4.074µs
I0719 01:46:01.814410   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/rook-ceph-mon-c-5b4c4697fb-8w28d
I0719 01:46:01.814970   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/rook-ceph-mon-c-5b4c4697fb-8w28d took: 7.325µs
I0719 01:46:01.814831   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-cluster-node-tuning-operator/tuned-hpvxx took: 1.433µs
I0719 01:46:01.814998   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-network-operator/iptables-alerter-m6v49
I0719 01:46:01.815005   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-network-operator/iptables-alerter-m6v49 took: 2.188µs
I0719 01:46:01.815010   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-machine-api/machine-api-controllers-59cdf7bd97-7l7pt
I0719 01:46:01.815016   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-machine-api/machine-api-controllers-59cdf7bd97-7l7pt took: 1.717µs
I0719 01:46:01.815020   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kube-apiserver/kube-apiserver-guard-00-50-56-8a-5c-ec
I0719 01:46:01.815027   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kube-apiserver/kube-apiserver-guard-00-50-56-8a-5c-ec took: 1.776µs
I0719 01:46:01.815031   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kni-infra/keepalived-00-50-56-8a-e1-e7
I0719 01:46:01.815038   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kni-infra/keepalived-00-50-56-8a-e1-e7 took: 3µs
I0719 01:46:01.815043   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kube-scheduler-operator/openshift-kube-scheduler-operator-555f7bb8bc-4vw77
I0719 01:46:01.815050   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kube-scheduler-operator/openshift-kube-scheduler-operator-555f7bb8bc-4vw77 took: 1.762µs
I0719 01:46:01.815054   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/rook-ceph-mds-ocs-storagecluster-cephfilesystem-a-8679ddf7kqp98
I0719 01:46:01.814922   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/rook-ceph-osd-0-6d5dbb5f-24hfr
I0719 01:46:01.815062   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/rook-ceph-mds-ocs-storagecluster-cephfilesystem-a-8679ddf7kqp98 took: 2.821µs
I0719 01:46:01.815068   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-multus/multus-additional-cni-plugins-rtmj7
I0719 01:46:01.815070   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/rook-ceph-osd-0-6d5dbb5f-24hfr took: 3.314µs
I0719 01:46:01.815076   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-multus/multus-additional-cni-plugins-rtmj7 took: 3.45µs
I0719 01:46:01.815077   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-network-diagnostics/network-check-source-b89b7bb96-lpzlv
I0719 01:46:01.815081   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/rook-ceph-exporter-00-50-56-8a-e1-e7-558dfbd955-jzh65
I0719 01:46:01.815086   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-network-diagnostics/network-check-source-b89b7bb96-lpzlv took: 1.594µs
I0719 01:46:01.814394   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-39-a0
I0719 01:46:01.815092   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-image-registry/node-ca-wgn2l
I0719 01:46:01.815097   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-39-a0 took: 2.631µs
I0719 01:46:01.815099   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-image-registry/node-ca-wgn2l took: 2.222µs
I0719 01:46:01.815103   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-network-diagnostics/network-check-target-vltnw
I0719 01:46:01.815110   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-network-diagnostics/network-check-target-vltnw took: 1.373µs
I0719 01:46:01.815115   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-cluster-node-tuning-operator/tuned-x2svx
I0719 01:46:01.814364   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kube-apiserver/kube-apiserver-00-50-56-8a-5c-ec took: 2.227µs
I0719 01:46:01.815120   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-cluster-node-tuning-operator/tuned-x2svx took: 1.317µs
I0719 01:46:01.815124   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kni-infra/coredns-00-50-56-8a-39-a0
I0719 01:46:01.815104   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-ovn-kubernetes/ovnkube-control-plane-58975cd9fd-mz4pv
I0719 01:46:01.815133   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kni-infra/coredns-00-50-56-8a-39-a0 took: 2.474µs
I0719 01:46:01.815138   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kni-infra/coredns-00-50-56-8a-e1-e7
I0719 01:46:01.815145   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kni-infra/coredns-00-50-56-8a-e1-e7 took: 1.852µs
I0719 01:46:01.815150   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-image-registry/node-ca-kqt8n
I0719 01:46:01.815156   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-image-registry/node-ca-kqt8n took: 1.579µs
I0719 01:46:01.815160   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/csi-rbdplugin-b6gdm
I0719 01:46:01.815167   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/csi-rbdplugin-b6gdm took: 2.561µs
I0719 01:46:01.815174   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-dns/node-resolver-tjmrc
I0719 01:46:01.815180   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-dns/node-resolver-tjmrc took: 1.729µs
I0719 01:46:01.815184   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-console/console-57f455cd77-77wrt
I0719 01:46:01.815088   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/rook-ceph-exporter-00-50-56-8a-e1-e7-558dfbd955-jzh65 took: 1.943µs
I0719 01:46:01.815202   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-multus/network-metrics-daemon-bqt8s
I0719 01:46:01.815216   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-multus/network-metrics-daemon-bqt8s took: 5.342µs
I0719 01:46:01.815221   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-network-operator/iptables-alerter-nh7z8
I0719 01:46:01.815228   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-network-operator/iptables-alerter-nh7z8 took: 2.052µs
I0719 01:46:01.815232   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-route-controller-manager/route-controller-manager-676cdfdbc8-t227m
I0719 01:46:01.815240   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-route-controller-manager/route-controller-manager-676cdfdbc8-t227m took: 1.479µs
I0719 01:46:01.815244   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-dns/node-resolver-djq2g
I0719 01:46:01.815251   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-dns/node-resolver-djq2g took: 1.929µs
I0719 01:46:01.815255   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-etcd/etcd-00-50-56-8a-5c-ec
I0719 01:46:01.815125   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-monitoring/alertmanager-main-1
I0719 01:46:01.815262   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-etcd/etcd-00-50-56-8a-5c-ec took: 1.724µs
I0719 01:46:01.815268   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-machine-config-operator/machine-config-controller-b886dd6cb-6kjkp
I0719 01:46:01.815275   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-machine-config-operator/machine-config-controller-b886dd6cb-6kjkp took: 2.112µs
I0719 01:46:01.815275   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-monitoring/alertmanager-main-1 took: 5.322µs
I0719 01:46:01.815280   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/csi-rbdplugin-xgkn6
I0719 01:46:01.815284   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-network-node-identity/network-node-identity-xlk9z
I0719 01:46:01.815288   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/csi-rbdplugin-xgkn6 took: 2.854µs
I0719 01:46:01.815291   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-network-node-identity/network-node-identity-xlk9z took: 1.981µs
I0719 01:46:01.815293   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-image-registry/cluster-image-registry-operator-656868857f-f94pq
I0719 01:46:01.815296   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-console/console-57f455cd77-h96cj
I0719 01:46:01.815300   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-image-registry/cluster-image-registry-operator-656868857f-f94pq took: 2.142µs
I0719 01:46:01.815303   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-console/console-57f455cd77-h96cj took: 1.585µs
I0719 01:46:01.815305   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-dns/node-resolver-dpn9t
I0719 01:46:01.815307   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-machine-config-operator/machine-config-daemon-r8bgv
I0719 01:46:01.815312   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-dns/node-resolver-dpn9t took: 1.412µs
I0719 01:46:01.815314   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-machine-config-operator/machine-config-daemon-r8bgv took: 1.981µs
I0719 01:46:01.815316   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-network-diagnostics/network-check-target-gc5jl
I0719 01:46:01.815319   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-monitoring/cluster-monitoring-operator-b4b4bcf9f-d4xhg
I0719 01:46:01.815323   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-network-diagnostics/network-check-target-gc5jl took: 1.525µs
I0719 01:46:01.815326   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-monitoring/cluster-monitoring-operator-b4b4bcf9f-d4xhg took: 2.066µs
I0719 01:46:01.815134   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-ovn-kubernetes/ovnkube-control-plane-58975cd9fd-mz4pv took: 2.281µs
I0719 01:46:01.815331   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kube-scheduler/revision-pruner-6-00-50-56-8a-44-52
I0719 01:46:01.815334   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-dns/node-resolver-nsvs6
I0719 01:46:01.815338   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kube-scheduler/revision-pruner-6-00-50-56-8a-44-52 took: 2.037µs
I0719 01:46:01.815341   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-dns/node-resolver-nsvs6 took: 2.033µs
I0719 01:46:01.815344   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-multus/multus-25bkq
I0719 01:46:01.815346   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-multus/network-metrics-daemon-hxzdd
I0719 01:46:01.815351   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-multus/multus-25bkq took: 1.67µs
I0719 01:46:01.815353   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-multus/network-metrics-daemon-hxzdd took: 2.049µs
I0719 01:46:01.814322   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kube-apiserver-operator/kube-apiserver-operator-55dc5cdcf9-p4csg
I0719 01:46:01.815328   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-console/downloads-6967878986-76phj
I0719 01:46:01.815361   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kni-infra/coredns-00-50-56-8a-fb-ea
I0719 01:46:01.815365   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-console/downloads-6967878986-76phj took: 1.455µs
I0719 01:46:01.815368   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kni-infra/coredns-00-50-56-8a-fb-ea took: 1.813µs
I0719 01:46:01.815371   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-network-node-identity/network-node-identity-z7b9j
I0719 01:46:01.815373   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-marketplace/marketplace-operator-59c7f5b7bd-8pd2c
I0719 01:46:01.815378   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-network-node-identity/network-node-identity-z7b9j took: 1.745µs
I0719 01:46:01.815382   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-marketplace/marketplace-operator-59c7f5b7bd-8pd2c took: 2.634µs
I0719 01:46:01.815384   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/csi-addons-controller-manager-6d78957fdf-gs4tk
I0719 01:46:01.815387   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-monitoring/metrics-server-7d47f4cbc-5qp84
I0719 01:46:01.815392   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/csi-addons-controller-manager-6d78957fdf-gs4tk took: 2.015µs
I0719 01:46:01.815393   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-monitoring/metrics-server-7d47f4cbc-5qp84 took: 1.595µs
I0719 01:46:01.815396   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/ocs-client-operator-controller-manager-846f549988-v288f
I0719 01:46:01.815398   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-oauth-apiserver/apiserver-86f656c4dd-x7cqj
I0719 01:46:01.815404   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/ocs-client-operator-controller-manager-846f549988-v288f took: 2.334µs
I0719 01:46:01.815406   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-oauth-apiserver/apiserver-86f656c4dd-x7cqj took: 1.642µs
I0719 01:46:01.815410   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kni-infra/keepalived-00-50-56-8a-5c-ec
I0719 01:46:01.815411   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/rook-ceph-crashcollector-00-50-56-8a-e1-e7-6c5dcb6f44-8z5np
I0719 01:46:01.815417   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kni-infra/keepalived-00-50-56-8a-5c-ec took: 1.903µs
I0719 01:46:01.815419   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/rook-ceph-crashcollector-00-50-56-8a-e1-e7-6c5dcb6f44-8z5np took: 2.27µs
I0719 01:46:01.815422   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kube-apiserver/kube-apiserver-00-50-56-8a-39-a0
I0719 01:46:01.815424   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-multus/multus-additional-cni-plugins-pjk5m
I0719 01:46:01.815372   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kube-apiserver-operator/kube-apiserver-operator-55dc5cdcf9-p4csg took: 1.971µs
I0719 01:46:01.814326   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-network-operator/iptables-alerter-m44lf
I0719 01:46:01.815437   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-monitoring/prometheus-k8s-1
I0719 01:46:01.815447   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-monitoring/prometheus-k8s-1 took: 3.849µs
I0719 01:46:01.815449   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-network-operator/iptables-alerter-m44lf took: 11.612µs
I0719 01:46:01.815452   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-ingress/router-default-54fb8ffc6b-hhdt2
I0719 01:46:01.815454   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-cluster-machine-approver/machine-approver-5bf6544664-79krt
I0719 01:46:01.815460   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-ingress/router-default-54fb8ffc6b-hhdt2 took: 3.105µs
I0719 01:46:01.815465   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-network-diagnostics/network-check-target-8gshd
I0719 01:46:01.815471   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-network-diagnostics/network-check-target-8gshd took: 1.3µs
I0719 01:46:01.815475   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-monitoring/openshift-state-metrics-6bb8db76bd-2wlhc
I0719 01:46:01.815482   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-monitoring/openshift-state-metrics-6bb8db76bd-2wlhc took: 2.219µs
I0719 01:46:01.815487   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-dns/node-resolver-bf5zv
I0719 01:46:01.815493   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-dns/node-resolver-bf5zv took: 1.852µs
I0719 01:46:01.814312   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-monitoring/kube-state-metrics-589b9987d-ck4ch took: 7.815µs
I0719 01:46:01.815504   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kube-scheduler/revision-pruner-6-00-50-56-8a-39-a0
I0719 01:46:01.815510   37437 obj_retry.go:459] Detected object openshift-kube-scheduler/revision-pruner-6-00-50-56-8a-39-a0 of type *factory.egressIPPod in terminal state (e.g. completed) during add event: will remove it
I0719 01:46:01.815518   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-dns/node-resolver-r7f9m
I0719 01:46:01.815525   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-dns/node-resolver-r7f9m took: 1.477µs
I0719 01:46:01.815530   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-dns/dns-default-rj9px
I0719 01:46:01.815536   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-dns/dns-default-rj9px took: 1.63µs
I0719 01:46:01.815541   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-marketplace/certified-operators-j5jtq
I0719 01:46:01.815547   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-marketplace/certified-operators-j5jtq took: 2.28µs
I0719 01:46:01.815551   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-monitoring/node-exporter-gbsmf
I0719 01:46:01.815558   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-monitoring/node-exporter-gbsmf took: 1.83µs
I0719 01:46:01.815562   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-monitoring/metrics-server-7d47f4cbc-dqrxk
I0719 01:46:01.815461   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-cluster-machine-approver/machine-approver-5bf6544664-79krt took: 1.671µs
I0719 01:46:01.815568   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-monitoring/metrics-server-7d47f4cbc-dqrxk took: 1.732µs
I0719 01:46:01.815573   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-etcd/etcd-guard-00-50-56-8a-5c-ec
I0719 01:46:01.815575   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-dns-operator/dns-operator-5fc6bf9796-jgj7s
I0719 01:46:01.815581   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-etcd/etcd-guard-00-50-56-8a-5c-ec took: 2.359µs
I0719 01:46:01.814396   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kube-apiserver/kube-apiserver-00-50-56-8a-44-52
I0719 01:46:01.815587   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-operator-lifecycle-manager/catalog-operator-7d75668bc4-sjfjn
I0719 01:46:01.814364   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-oauth-apiserver/apiserver-86f656c4dd-2pxdq
I0719 01:46:01.814441   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-authentication/oauth-openshift-7c9d9dfc8c-lxcsb took: 1.874µs
I0719 01:46:01.815598   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-local-storage/local-storage-operator-6486fccd57-h47kh
I0719 01:46:01.814564   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-local-storage/diskmaker-manager-2zrc6 took: 3.395µs
I0719 01:46:01.815606   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-machine-api/metal3-baremetal-operator-6fd5ccf9-9p448
I0719 01:46:01.815614   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-machine-api/metal3-baremetal-operator-6fd5ccf9-9p448 took: 3.167µs
I0719 01:46:01.815619   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kni-infra/haproxy-00-50-56-8a-5c-ec
I0719 01:46:01.815627   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kni-infra/haproxy-00-50-56-8a-5c-ec took: 2.448µs
I0719 01:46:01.815631   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-operator-lifecycle-manager/collect-profiles-28689195-w9664
I0719 01:46:01.815636   37437 obj_retry.go:459] Detected object openshift-operator-lifecycle-manager/collect-profiles-28689195-w9664 of type *factory.egressIPPod in terminal state (e.g. completed) during add event: will remove it
I0719 01:46:01.815643   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-cluster-storage-operator/csi-snapshot-controller-794ff44f88-7cksj
I0719 01:46:01.815650   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-cluster-storage-operator/csi-snapshot-controller-794ff44f88-7cksj took: 1.204µs
I0719 01:46:01.815655   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-apiserver/apiserver-7d9bbd465d-6cgbw
I0719 01:46:01.815582   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-dns-operator/dns-operator-5fc6bf9796-jgj7s took: 1.444µs
I0719 01:46:01.815667   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/rook-ceph-rgw-ocs-storagecluster-cephobjectstore-a-766774cx8zqw
I0719 01:46:01.815675   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/rook-ceph-rgw-ocs-storagecluster-cephobjectstore-a-766774cx8zqw took: 3.035µs
I0719 01:46:01.815680   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-image-registry/image-pruner-28689120-2bnxj
I0719 01:46:01.815684   37437 obj_retry.go:459] Detected object openshift-image-registry/image-pruner-28689120-2bnxj of type *factory.egressIPPod in terminal state (e.g. completed) during add event: will remove it
I0719 01:46:01.815691   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-machine-config-operator/machine-config-daemon-kgwdc
I0719 01:46:01.815699   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-machine-config-operator/machine-config-daemon-kgwdc took: 2.942µs
I0719 01:46:01.815703   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/csi-rbdplugin-provisioner-5dcc45fbf4-v5l2c
I0719 01:46:01.815710   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/csi-rbdplugin-provisioner-5dcc45fbf4-v5l2c took: 2.298µs
I0719 01:46:01.815714   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-cluster-node-tuning-operator/tuned-f4pbt
I0719 01:46:01.815720   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-cluster-node-tuning-operator/tuned-f4pbt took: 1.691µs
I0719 01:46:01.815725   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kube-controller-manager/kube-controller-manager-guard-00-50-56-8a-44-52
I0719 01:46:01.815599   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-oauth-apiserver/apiserver-86f656c4dd-2pxdq took: 2.398µs
I0719 01:46:01.815742   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-console/console-f7dbc9784-cj9wp
I0719 01:46:01.815756   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-console/console-f7dbc9784-cj9wp took: 3.918µs
I0719 01:46:01.815762   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kni-infra/coredns-00-50-56-8a-5c-ec
I0719 01:46:01.815772   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kni-infra/coredns-00-50-56-8a-5c-ec took: 4.865µs
I0719 01:46:01.815777   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-machine-config-operator/machine-config-server-zwkfw
I0719 01:46:01.815785   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-machine-config-operator/machine-config-server-zwkfw took: 2.8µs
I0719 01:46:01.815790   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-controller-manager/controller-manager-5c7f9f9d47-thph4
I0719 01:46:01.815796   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-controller-manager/controller-manager-5c7f9f9d47-thph4 took: 1.494µs
I0719 01:46:01.815800   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-etcd/revision-pruner-9-00-50-56-8a-39-a0
I0719 01:46:01.815805   37437 obj_retry.go:459] Detected object openshift-etcd/revision-pruner-9-00-50-56-8a-39-a0 of type *factory.egressIPPod in terminal state (e.g. completed) during add event: will remove it
I0719 01:46:01.815606   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-local-storage/local-storage-operator-6486fccd57-h47kh took: 2.355µs
I0719 01:46:01.815838   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kni-infra/coredns-00-50-56-8a-44-52
I0719 01:46:01.815850   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kni-infra/coredns-00-50-56-8a-44-52 took: 4.338µs
I0719 01:46:01.815855   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-machine-api/cluster-autoscaler-operator-56cd7bcc4-8t6ns
I0719 01:46:01.815863   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-machine-api/cluster-autoscaler-operator-56cd7bcc4-8t6ns took: 3.558µs
I0719 01:46:01.815868   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-fb-ea
I0719 01:46:01.815874   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-fb-ea took: 1.875µs
I0719 01:46:01.815878   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/csi-cephfsplugin-5fvh4
I0719 01:46:01.815886   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/csi-cephfsplugin-5fvh4 took: 2.601µs
I0719 01:46:01.815890   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-authentication-operator/authentication-operator-68795c8768-8rvtz
I0719 01:46:01.814744   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-ingress-operator/ingress-operator-5cc96867f4-pdgdd
I0719 01:46:01.815898   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-authentication-operator/authentication-operator-68795c8768-8rvtz took: 2.965µs
I0719 01:46:01.815903   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kube-controller-manager/kube-controller-manager-guard-00-50-56-8a-39-a0
I0719 01:46:01.815905   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-ingress-operator/ingress-operator-5cc96867f4-pdgdd took: 3.871µs
I0719 01:46:01.815909   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kube-controller-manager/kube-controller-manager-guard-00-50-56-8a-39-a0 took: 1.954µs
I0719 01:46:01.815911   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kni-infra/coredns-00-50-56-8a-f2-5d
I0719 01:46:01.815915   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-monitoring/thanos-querier-68bf686489-9cctf
I0719 01:46:01.815919   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kni-infra/coredns-00-50-56-8a-f2-5d took: 2.631µs
I0719 01:46:01.815921   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-monitoring/thanos-querier-68bf686489-9cctf took: 1.622µs
I0719 01:46:01.815924   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-ovn-kubernetes/ovnkube-node-9h9qr
I0719 01:46:01.815928   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-e1-e7
I0719 01:46:01.815932   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-ovn-kubernetes/ovnkube-node-9h9qr took: 2.209µs
I0719 01:46:01.815935   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-e1-e7 took: 2.034µs
I0719 01:46:01.814953   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/csi-cephfsplugin-b549v in Admin Network Policy controller
I0719 01:46:01.815941   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-network-operator/iptables-alerter-6s78n
I0719 01:46:01.815945   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/csi-cephfsplugin-b549v Admin Network Policy controller: took 989.885µs
I0719 01:46:01.815948   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-network-operator/iptables-alerter-6s78n took: 1.897µs
I0719 01:46:01.815953   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-multus/multus-mqkdb
I0719 01:46:01.815954   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-cluster-node-tuning-operator/tuned-9mzgb in Admin Network Policy controller
I0719 01:46:01.815959   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-multus/multus-mqkdb took: 1.766µs
I0719 01:46:01.815937   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-multus/network-metrics-daemon-fslb2
I0719 01:46:01.815970   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-multus/network-metrics-daemon-fslb2 took: 2.12µs
I0719 01:46:01.815974   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-cluster-node-tuning-operator/tuned-5pn2c
I0719 01:46:01.815959   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-cluster-node-tuning-operator/tuned-9mzgb Admin Network Policy controller: took 5.461µs
I0719 01:46:01.815988   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-cluster-node-tuning-operator/tuned-5pn2c took: 1.591µs
I0719 01:46:01.815994   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-controller-manager/controller-manager-5c7f9f9d47-kxpdr
I0719 01:46:01.815994   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-monitoring/alertmanager-main-1 in Admin Network Policy controller
I0719 01:46:01.816000   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-controller-manager/controller-manager-5c7f9f9d47-kxpdr took: 1.335µs
I0719 01:46:01.816000   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-monitoring/alertmanager-main-1 Admin Network Policy controller: took 6.75µs
I0719 01:46:01.816005   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kube-storage-version-migrator-operator/kube-storage-version-migrator-operator-75d5d9b9f8-lj6w5
I0719 01:46:01.816009   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-machine-api/machine-api-controllers-59cdf7bd97-7l7pt in Admin Network Policy controller
I0719 01:46:01.816012   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kube-storage-version-migrator-operator/kube-storage-version-migrator-operator-75d5d9b9f8-lj6w5 took: 1.759µs
I0719 01:46:01.816014   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-machine-api/machine-api-controllers-59cdf7bd97-7l7pt Admin Network Policy controller: took 6.297µs
I0719 01:46:01.816017   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-operator-lifecycle-manager/packageserver-6bf7d58455-gh44f
I0719 01:46:01.816019   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-network-diagnostics/network-check-target-8gshd in Admin Network Policy controller
I0719 01:46:01.816024   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-network-diagnostics/network-check-target-8gshd Admin Network Policy controller: took 4.935µs
I0719 01:46:01.815190   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-console/console-57f455cd77-77wrt took: 1.679µs
I0719 01:46:01.816029   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-local-storage/local-storage-operator-6486fccd57-h47kh in Admin Network Policy controller
I0719 01:46:01.816032   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kni-infra/keepalived-00-50-56-8a-f2-5d
I0719 01:46:01.816033   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-local-storage/local-storage-operator-6486fccd57-h47kh Admin Network Policy controller: took 4.504µs
I0719 01:46:01.816039   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-route-controller-manager/route-controller-manager-676cdfdbc8-t6rhq in Admin Network Policy controller
I0719 01:46:01.815356   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kni-infra/keepalived-00-50-56-8a-44-52
I0719 01:46:01.816044   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-route-controller-manager/route-controller-manager-676cdfdbc8-t6rhq Admin Network Policy controller: took 5.391µs
I0719 01:46:01.816049   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kni-infra/keepalived-00-50-56-8a-44-52 took: 1.912µs
I0719 01:46:01.815431   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-multus/multus-additional-cni-plugins-pjk5m took: 1.774µs
I0719 01:46:01.816054   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-ingress-canary/ingress-canary-lsx7x
I0719 01:46:01.816058   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-5c-ec
I0719 01:46:01.816061   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-ingress-canary/ingress-canary-lsx7x took: 1.113µs
I0719 01:46:01.816066   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/csi-cephfsplugin-provisioner-585f89d895-2b4wk
I0719 01:46:01.816024   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-operator-lifecycle-manager/packageserver-6bf7d58455-gh44f took: 1.864µs
I0719 01:46:01.816074   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-cluster-node-tuning-operator/tuned-cjc5f
I0719 01:46:01.816066   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-5c-ec took: 2.581µs
I0719 01:46:01.816081   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-cluster-node-tuning-operator/tuned-cjc5f took: 1.997µs
I0719 01:46:01.816039   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kni-infra/keepalived-00-50-56-8a-f2-5d took: 2.506µs
I0719 01:46:01.816086   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-etcd/etcd-guard-00-50-56-8a-39-a0
I0719 01:46:01.816091   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/csi-rbdplugin-provisioner-5dcc45fbf4-9svs4
I0719 01:46:01.816094   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-etcd/etcd-guard-00-50-56-8a-39-a0 took: 2.399µs
I0719 01:46:01.816098   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/csi-rbdplugin-provisioner-5dcc45fbf4-9svs4 took: 1.965µs
I0719 01:46:01.816074   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/csi-cephfsplugin-provisioner-585f89d895-2b4wk took: 3.116µs
I0719 01:46:01.816103   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kube-apiserver/revision-pruner-8-00-50-56-8a-5c-ec
I0719 01:46:01.816105   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-operator-lifecycle-manager/olm-operator-59f98dcc4-xqd8j
I0719 01:46:01.816110   37437 obj_retry.go:459] Detected object openshift-kube-apiserver/revision-pruner-8-00-50-56-8a-5c-ec of type *factory.egressIPPod in terminal state (e.g. completed) during add event: will remove it
I0719 01:46:01.816113   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-operator-lifecycle-manager/olm-operator-59f98dcc4-xqd8j took: 2.385µs
I0719 01:46:01.816118   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/rook-ceph-exporter-00-50-56-8a-f2-5d-785d485f5d-v5k84
I0719 01:46:01.816082   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-image-registry/node-ca-tvhtl
I0719 01:46:01.816125   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/rook-ceph-exporter-00-50-56-8a-f2-5d-785d485f5d-v5k84 took: 1.939µs
I0719 01:46:01.816129   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-image-registry/node-ca-tvhtl took: 1.863µs
I0719 01:46:01.816131   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-machine-config-operator/machine-config-server-968nk
I0719 01:46:01.816119   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/rook-ceph-osd-1-6db96b64cc-nw82d
I0719 01:46:01.816138   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-machine-config-operator/machine-config-server-968nk took: 1.562µs
I0719 01:46:01.816143   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-multus/multus-additional-cni-plugins-b5t42
I0719 01:46:01.816149   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-multus/multus-additional-cni-plugins-b5t42 took: 1.644µs
I0719 01:46:01.816154   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-multus/multus-additional-cni-plugins-qdrk9
I0719 01:46:01.816160   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-multus/multus-additional-cni-plugins-qdrk9 took: 1.55µs
I0719 01:46:01.816164   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/noobaa-db-pg-0
I0719 01:46:01.816171   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/noobaa-db-pg-0 took: 1.989µs
I0719 01:46:01.816175   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-cluster-version/cluster-version-operator-78b5d9c79d-znx2p
I0719 01:46:01.816181   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-cluster-version/cluster-version-operator-78b5d9c79d-znx2p took: 1.765µs
I0719 01:46:01.816185   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kube-controller-manager-operator/kube-controller-manager-operator-85c67fcb8d-fg9j7
I0719 01:46:01.816191   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kube-controller-manager-operator/kube-controller-manager-operator-85c67fcb8d-fg9j7 took: 1.114µs
I0719 01:46:01.816099   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-monitoring/prometheus-operator-admission-webhook-67db68b49d-wbfqq
I0719 01:46:01.816201   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-monitoring/prometheus-operator-admission-webhook-67db68b49d-wbfqq took: 1.861µs
I0719 01:46:01.816050   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-machine-config-operator/machine-config-daemon-vllgq in Admin Network Policy controller
I0719 01:46:01.816142   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/rook-ceph-osd-1-6db96b64cc-nw82d took: 2.888µs
I0719 01:46:01.816210   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-machine-config-operator/machine-config-daemon-vllgq Admin Network Policy controller: took 160.158µs
I0719 01:46:01.816214   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-route-controller-manager/route-controller-manager-676cdfdbc8-gt4t6
I0719 01:46:01.814351   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-cluster-samples-operator/cluster-samples-operator-6b95974b98-cxvvt
I0719 01:46:01.815594   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-operator-lifecycle-manager/catalog-operator-7d75668bc4-sjfjn took: 2.061µs
I0719 01:46:01.816224   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-ingress/router-default-54fb8ffc6b-kgb2v
I0719 01:46:01.816232   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-ingress/router-default-54fb8ffc6b-kgb2v took: 2.67µs
I0719 01:46:01.816236   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-monitoring/thanos-querier-68bf686489-qbcjs
I0719 01:46:01.816242   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-monitoring/thanos-querier-68bf686489-qbcjs took: 1.726µs
I0719 01:46:01.816247   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/noobaa-operator-bf7774fd8-zskvp
I0719 01:46:01.816253   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/noobaa-operator-bf7774fd8-zskvp took: 2.156µs
I0719 01:46:01.816258   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-image-registry/node-ca-sq7qk
I0719 01:46:01.816263   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-image-registry/node-ca-sq7qk took: 1.432µs
I0719 01:46:01.816268   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-machine-api/control-plane-machine-set-operator-77bcc698b6-wvkdb
I0719 01:46:01.816274   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-machine-api/control-plane-machine-set-operator-77bcc698b6-wvkdb took: 1.865µs
I0719 01:46:01.816280   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-network-diagnostics/network-check-target-h9cbr
I0719 01:46:01.816282   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-cluster-samples-operator/cluster-samples-operator-6b95974b98-cxvvt took: 1.699µs
I0719 01:46:01.816287   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-network-diagnostics/network-check-target-h9cbr took: 1.37µs
I0719 01:46:01.816287   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-network-node-identity/network-node-identity-tzcq8
I0719 01:46:01.816292   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-monitoring/node-exporter-7xrvj
I0719 01:46:01.815661   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-apiserver/apiserver-7d9bbd465d-6cgbw took: 1.599µs
I0719 01:46:01.816299   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-monitoring/node-exporter-7xrvj took: 1.871µs
I0719 01:46:01.816304   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-authentication/oauth-openshift-7c9d9dfc8c-ddj6k
I0719 01:46:01.816305   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-ovn-kubernetes/ovnkube-node-mqh7r
I0719 01:46:01.816312   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-authentication/oauth-openshift-7c9d9dfc8c-ddj6k took: 1.627µs
I0719 01:46:01.816316   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-console/downloads-6967878986-hpkbw
I0719 01:46:01.816321   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-ovn-kubernetes/ovnkube-node-mqh7r took: 4.58µs
I0719 01:46:01.816330   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-insights/insights-operator-586b65d57b-7rk2w
I0719 01:46:01.816337   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-insights/insights-operator-586b65d57b-7rk2w took: 2.263µs
I0719 01:46:01.816342   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-monitoring/node-exporter-7m7sg
I0719 01:46:01.816348   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-monitoring/node-exporter-7m7sg took: 1.926µs
I0719 01:46:01.816352   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-5c-ec
I0719 01:46:01.816359   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-5c-ec took: 1.849µs
I0719 01:46:01.815826   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-image-registry/node-ca-986d7
I0719 01:46:01.816372   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-image-registry/node-ca-986d7 took: 2.5µs
I0719 01:46:01.816378   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-44-52
I0719 01:46:01.816385   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-44-52 took: 1.661µs
I0719 01:46:01.816391   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-multus/network-metrics-daemon-t4g2p
I0719 01:46:01.816398   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-multus/network-metrics-daemon-t4g2p took: 1.905µs
I0719 01:46:01.816402   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-network-operator/network-operator-6967d44d7-4wwpm
I0719 01:46:01.816408   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-network-operator/network-operator-6967d44d7-4wwpm took: 1.634µs
I0719 01:46:01.816412   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-monitoring/node-exporter-9mlmj
I0719 01:46:01.816418   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-monitoring/node-exporter-9mlmj took: 1.439µs
I0719 01:46:01.816274   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-route-controller-manager/route-controller-manager-676cdfdbc8-gt4t6 took: 2.892µs
I0719 01:46:01.816426   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kube-storage-version-migrator/migrator-7fc5dd675b-tfjhl
I0719 01:46:01.816432   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kube-storage-version-migrator/migrator-7fc5dd675b-tfjhl took: 1.482µs
I0719 01:46:01.816436   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-operator-lifecycle-manager/package-server-manager-74bbc7c476-4555r
I0719 01:46:01.816442   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-operator-lifecycle-manager/package-server-manager-74bbc7c476-4555r took: 1.582µs
I0719 01:46:01.816447   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-machine-config-operator/machine-config-daemon-p677g
I0719 01:46:01.816453   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-machine-config-operator/machine-config-daemon-p677g took: 1.765µs
I0719 01:46:01.816458   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-service-ca-operator/service-ca-operator-86c8d4bbfd-w2qxx
I0719 01:46:01.816463   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-service-ca-operator/service-ca-operator-86c8d4bbfd-w2qxx took: 1.123µs
I0719 01:46:01.816468   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kube-controller-manager/kube-controller-manager-guard-00-50-56-8a-5c-ec
I0719 01:46:01.816474   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kube-controller-manager/kube-controller-manager-guard-00-50-56-8a-5c-ec took: 1.309µs
I0719 01:46:01.816323   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-console/downloads-6967878986-hpkbw took: 1.181µs
I0719 01:46:01.816481   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-etcd/revision-pruner-9-00-50-56-8a-44-52
I0719 01:46:01.816488   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-etcd/revision-pruner-9-00-50-56-8a-44-52 took: 1.862µs
I0719 01:46:01.814992   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-multus/network-metrics-daemon-gqqpq
I0719 01:46:01.816501   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-multus/network-metrics-daemon-gqqpq took: 3.042µs
I0719 01:46:01.816506   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-cluster-node-tuning-operator/tuned-9mzgb
I0719 01:46:01.814980   37437 ovs.go:162] Exec(30): stdout: "patch\n"
I0719 01:46:01.816513   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-cluster-node-tuning-operator/tuned-9mzgb took: 1.733µs
I0719 01:46:01.816517   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/ux-backend-server-6444f844bf-whf8g
I0719 01:46:01.816524   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/ux-backend-server-6444f844bf-whf8g took: 2.237µs
I0719 01:46:01.816528   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-cluster-storage-operator/cluster-storage-operator-6c5864c5b-kgzzc
I0719 01:46:01.816534   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-cluster-storage-operator/cluster-storage-operator-6c5864c5b-kgzzc took: 1.112µs
I0719 01:46:01.816538   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/rook-ceph-operator-cf758864f-c6zl8
I0719 01:46:01.816545   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/rook-ceph-operator-cf758864f-c6zl8 took: 2.097µs
I0719 01:46:01.816549   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/rook-ceph-mgr-b-779b65ccb6-29sz4
I0719 01:46:01.816555   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/rook-ceph-mgr-b-779b65ccb6-29sz4 took: 1.858µs
I0719 01:46:01.816560   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-multus/multus-additional-cni-plugins-tpn87
I0719 01:46:01.816566   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-multus/multus-additional-cni-plugins-tpn87 took: 1.588µs
I0719 01:46:01.816570   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-etcd-operator/etcd-operator-6c7489b895-5tql8
I0719 01:46:01.816577   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-etcd-operator/etcd-operator-6c7489b895-5tql8 took: 1.704µs
I0719 01:46:01.816581   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-multus/multus-ltqfr
I0719 01:46:01.816516   37437 ovs.go:163] Exec(30): stderr: ""
I0719 01:46:01.816588   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-multus/multus-ltqfr took: 1.456µs
I0719 01:46:01.816593   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kni-infra/keepalived-00-50-56-8a-39-a0
I0719 01:46:01.816599   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kni-infra/keepalived-00-50-56-8a-39-a0 took: 1.899µs
I0719 01:46:01.816602   37437 ovs.go:159] Exec(31): /usr/bin/ovs-vsctl --timeout=15 get interface ens192 ofport
I0719 01:46:01.816603   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-controller-manager-operator/openshift-controller-manager-operator-cf8f9956c-x6xn5
I0719 01:46:01.816610   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-controller-manager-operator/openshift-controller-manager-operator-cf8f9956c-x6xn5 took: 1.129µs
I0719 01:46:01.814289   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kube-apiserver/kube-apiserver-guard-00-50-56-8a-39-a0
I0719 01:46:01.816621   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kube-apiserver/kube-apiserver-guard-00-50-56-8a-39-a0 took: 2.024µs
I0719 01:46:01.816625   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-etcd/etcd-00-50-56-8a-44-52
I0719 01:46:01.816631   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-etcd/etcd-00-50-56-8a-44-52 took: 1.17µs
I0719 01:46:01.816635   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-ovn-kubernetes/ovnkube-node-62ccc
I0719 01:46:01.816641   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-ovn-kubernetes/ovnkube-node-62ccc took: 1.433µs
I0719 01:46:01.816646   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-ovn-kubernetes/ovnkube-control-plane-58975cd9fd-7wmvb
I0719 01:46:01.816651   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-ovn-kubernetes/ovnkube-control-plane-58975cd9fd-7wmvb took: 1.57µs
I0719 01:46:01.816656   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-etcd/etcd-guard-00-50-56-8a-44-52
I0719 01:46:01.816662   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-etcd/etcd-guard-00-50-56-8a-44-52 took: 1.266µs
I0719 01:46:01.816666   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/odf-operator-controller-manager-78d57f457c-tbwjf
I0719 01:46:01.816134   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-44-52
I0719 01:46:01.816673   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/odf-operator-controller-manager-78d57f457c-tbwjf took: 1.941µs
I0719 01:46:01.816678   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-image-registry/node-ca-lfxb8
I0719 01:46:01.816679   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-44-52 took: 2.895µs
I0719 01:46:01.816684   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-image-registry/node-ca-lfxb8 took: 1.375µs
I0719 01:46:01.816217   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-marketplace/certified-operators-j5jtq in Admin Network Policy controller
I0719 01:46:01.816689   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-ovn-kubernetes/ovnkube-node-5bqnj
I0719 01:46:01.816692   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-marketplace/certified-operators-j5jtq Admin Network Policy controller: took 474.046µs
I0719 01:46:01.816695   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-ovn-kubernetes/ovnkube-node-5bqnj took: 1.545µs
I0719 01:46:01.816700   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-network-node-identity/network-node-identity-xlk9z in Admin Network Policy controller
I0719 01:46:01.816705   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-network-node-identity/network-node-identity-xlk9z Admin Network Policy controller: took 5.424µs
I0719 01:46:01.816710   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-operator-lifecycle-manager/catalog-operator-7d75668bc4-sjfjn in Admin Network Policy controller
I0719 01:46:01.816714   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-operator-lifecycle-manager/catalog-operator-7d75668bc4-sjfjn Admin Network Policy controller: took 4.72µs
I0719 01:46:01.816719   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-ovn-kubernetes/ovnkube-control-plane-58975cd9fd-7wmvb in Admin Network Policy controller
I0719 01:46:01.816742   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-ovn-kubernetes/ovnkube-control-plane-58975cd9fd-7wmvb Admin Network Policy controller: took 4.102µs
I0719 01:46:01.816685   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-5c-ec
I0719 01:46:01.816760   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-5c-ec took: 3.369µs
I0719 01:46:01.816766   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kube-scheduler/openshift-kube-scheduler-guard-00-50-56-8a-44-52
I0719 01:46:01.816772   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kube-scheduler/openshift-kube-scheduler-guard-00-50-56-8a-44-52 took: 1.608µs
I0719 01:46:01.815592   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kube-apiserver/kube-apiserver-00-50-56-8a-44-52 took: 1.952µs
I0719 01:46:01.816777   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-config-operator/openshift-config-operator-59dc875ddb-rnq74
I0719 01:46:01.816782   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-multus/multus-admission-controller-5cc499c6f4-jtjqw
I0719 01:46:01.816783   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-config-operator/openshift-config-operator-59dc875ddb-rnq74 took: 1.319µs
I0719 01:46:01.816790   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/csi-cephfsplugin-s29g7
I0719 01:46:01.816792   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-multus/multus-admission-controller-5cc499c6f4-jtjqw took: 2.972µs
I0719 01:46:01.816796   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/rook-ceph-osd-2-9c5dbbd88-crlql
I0719 01:46:01.816700   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-44-52
I0719 01:46:01.816799   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/ux-backend-server-6444f844bf-whf8g in Admin Network Policy controller
I0719 01:46:01.816804   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/rook-ceph-osd-2-9c5dbbd88-crlql took: 2.361µs
I0719 01:46:01.816806   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-44-52 took: 2.205µs
I0719 01:46:01.816808   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/ux-backend-server-6444f844bf-whf8g Admin Network Policy controller: took 11.107µs
I0719 01:46:01.816812   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kube-scheduler/openshift-kube-scheduler-guard-00-50-56-8a-5c-ec
I0719 01:46:01.815497   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/rook-ceph-mgr-a-6fddb5fd95-mr2cn
I0719 01:46:01.816797   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/csi-cephfsplugin-s29g7 took: 2.385µs
I0719 01:46:01.816809   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/csi-cephfsplugin-b549v
I0719 01:46:01.816829   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/csi-cephfsplugin-b549v took: 2.122µs
I0719 01:46:01.815430   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kube-apiserver/kube-apiserver-00-50-56-8a-39-a0 took: 2.567µs
I0719 01:46:01.816835   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/noobaa-core-0
I0719 01:46:01.816837   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-multus/multus-47wxd
I0719 01:46:01.816296   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-network-node-identity/network-node-identity-tzcq8 took: 1.786µs
I0719 01:46:01.816843   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/noobaa-core-0 took: 2.056µs
I0719 01:46:01.816847   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-multus/multus-47wxd took: 3.63µs
I0719 01:46:01.816815   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kni-infra/coredns-00-50-56-8a-44-52 in Admin Network Policy controller
I0719 01:46:01.816853   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/csi-rbdplugin-xkw8r
I0719 01:46:01.816856   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kni-infra/coredns-00-50-56-8a-44-52 Admin Network Policy controller: took 41.317µs
I0719 01:46:01.816862   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/csi-rbdplugin-xkw8r took: 2.528µs
I0719 01:46:01.816867   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-operator-lifecycle-manager/packageserver-6bf7d58455-k8qkk
I0719 01:46:01.816876   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-operator-lifecycle-manager/packageserver-6bf7d58455-k8qkk took: 2.05µs
I0719 01:46:01.816880   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/csi-cephfsplugin-provisioner-585f89d895-ddwtl
I0719 01:46:01.816887   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/csi-cephfsplugin-provisioner-585f89d895-ddwtl took: 2.2µs
I0719 01:46:01.816892   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-39-a0
I0719 01:46:01.816898   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-39-a0 took: 1.646µs
I0719 01:46:01.816902   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-monitoring/node-exporter-nvqsf
I0719 01:46:01.816909   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-monitoring/node-exporter-nvqsf took: 1.79µs
I0719 01:46:01.816913   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-multus/multus-additional-cni-plugins-2kgg5
I0719 01:46:01.816920   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-multus/multus-additional-cni-plugins-2kgg5 took: 1.853µs
I0719 01:46:01.816924   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/rook-ceph-mds-ocs-storagecluster-cephfilesystem-b-c4dc5cd7zkffj
I0719 01:46:01.816828   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/rook-ceph-mon-a-6dc9d78597-7ttc9
I0719 01:46:01.816940   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/rook-ceph-mon-a-6dc9d78597-7ttc9 took: 2.916µs
I0719 01:46:01.816947   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-operator-lifecycle-manager/collect-profiles-28689225-j8wtn
I0719 01:46:01.816952   37437 obj_retry.go:459] Detected object openshift-operator-lifecycle-manager/collect-profiles-28689225-j8wtn of type *factory.egressIPPod in terminal state (e.g. completed) during add event: will remove it
I0719 01:46:01.816960   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/ocs-metrics-exporter-84f9766477-r8fxs
I0719 01:46:01.816969   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/ocs-metrics-exporter-84f9766477-r8fxs took: 2.935µs
I0719 01:46:01.816848   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-machine-api/metal3-image-customization-5f9d4c754c-5v2p8
I0719 01:46:01.816978   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-machine-api/metal3-image-customization-5f9d4c754c-5v2p8 took: 2.074µs
I0719 01:46:01.816989   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kni-infra/haproxy-00-50-56-8a-39-a0
I0719 01:46:01.816863   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-machine-api/cluster-autoscaler-operator-56cd7bcc4-8t6ns in Admin Network Policy controller
I0719 01:46:01.816996   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kni-infra/haproxy-00-50-56-8a-39-a0 took: 1.818µs
I0719 01:46:01.816997   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-machine-api/cluster-autoscaler-operator-56cd7bcc4-8t6ns Admin Network Policy controller: took 134.398µs
I0719 01:46:01.817001   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-marketplace/community-operators-wgnxc
I0719 01:46:01.817004   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kube-apiserver/kube-apiserver-guard-00-50-56-8a-5c-ec in Admin Network Policy controller
I0719 01:46:01.817007   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-marketplace/community-operators-wgnxc took: 2.036µs
I0719 01:46:01.816819   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kube-scheduler/openshift-kube-scheduler-guard-00-50-56-8a-5c-ec took: 1.403µs
I0719 01:46:01.817012   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-console/console-c675c654b-rw8cg
I0719 01:46:01.817016   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-monitoring/prometheus-operator-admission-webhook-67db68b49d-w8jqx
I0719 01:46:01.817018   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-console/console-c675c654b-rw8cg took: 1.119µs
I0719 01:46:01.817023   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-marketplace/redhat-marketplace-hbf7g
I0719 01:46:01.817026   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-monitoring/prometheus-operator-admission-webhook-67db68b49d-w8jqx took: 3.29µs
I0719 01:46:01.817030   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-marketplace/redhat-marketplace-hbf7g took: 2.371µs
I0719 01:46:01.817009   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kube-apiserver/kube-apiserver-guard-00-50-56-8a-5c-ec Admin Network Policy controller: took 4.562µs
I0719 01:46:01.817035   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-network-operator/iptables-alerter-b72gh
I0719 01:46:01.817038   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-monitoring/openshift-state-metrics-6bb8db76bd-2wlhc in Admin Network Policy controller
I0719 01:46:01.817042   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-network-operator/iptables-alerter-b72gh took: 1.88µs
I0719 01:46:01.817031   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/ocs-operator-5567c4fdb4-8b9zr
I0719 01:46:01.817052   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/ocs-operator-5567c4fdb4-8b9zr took: 2.304µs
I0719 01:46:01.816848   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-apiserver-operator/openshift-apiserver-operator-84fc88fd69-mqjqx
I0719 01:46:01.817062   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-apiserver-operator/openshift-apiserver-operator-84fc88fd69-mqjqx took: 1.891µs
I0719 01:46:01.817067   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-monitoring/monitoring-plugin-6f457fd4b8-6wb4z
I0719 01:46:01.817073   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-monitoring/monitoring-plugin-6f457fd4b8-6wb4z took: 1.987µs
I0719 01:46:01.817077   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-dns/dns-default-qzrlq
I0719 01:46:01.817084   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-dns/dns-default-qzrlq took: 2.585µs
I0719 01:46:01.817089   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-multus/network-metrics-daemon-7ttpg
I0719 01:46:01.817095   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-multus/network-metrics-daemon-7ttpg took: 1.645µs
I0719 01:46:01.817099   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/rook-ceph-crashcollector-00-50-56-8a-f2-5d-5bfb656d8f-tvtpr
I0719 01:46:01.817107   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/rook-ceph-crashcollector-00-50-56-8a-f2-5d-5bfb656d8f-tvtpr took: 2.736µs
I0719 01:46:01.817111   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-etcd/etcd-00-50-56-8a-39-a0
I0719 01:46:01.817117   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-etcd/etcd-00-50-56-8a-39-a0 took: 1.436µs
I0719 01:46:01.817121   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-ovn-kubernetes/ovnkube-node-7pmvf
I0719 01:46:01.815731   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kube-controller-manager/kube-controller-manager-guard-00-50-56-8a-44-52 took: 1.408µs
I0719 01:46:01.817128   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-ovn-kubernetes/ovnkube-node-7pmvf took: 1.408µs
I0719 01:46:01.817130   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-local-storage/diskmaker-manager-wj2h7
I0719 01:46:01.817133   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kube-apiserver/revision-pruner-8-00-50-56-8a-44-52
I0719 01:46:01.817138   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-local-storage/diskmaker-manager-wj2h7 took: 2.392µs
I0719 01:46:01.817140   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kube-apiserver/revision-pruner-8-00-50-56-8a-44-52 took: 1.648µs
I0719 01:46:01.817143   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-machine-config-operator/machine-config-server-j8kbc
I0719 01:46:01.817145   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-cluster-storage-operator/csi-snapshot-controller-794ff44f88-5jz8j
I0719 01:46:01.817151   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-cluster-storage-operator/csi-snapshot-controller-794ff44f88-5jz8j took: 1.239µs
I0719 01:46:01.817152   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-machine-config-operator/machine-config-server-j8kbc took: 3.58µs
I0719 01:46:01.817159   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-console-operator/console-operator-76c8786869-jr6r2
I0719 01:46:01.817165   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-console-operator/console-operator-76c8786869-jr6r2 took: 1.389µs
I0719 01:46:01.817169   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-monitoring/telemeter-client-7b74cd774c-fg6lz
I0719 01:46:01.817175   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-monitoring/telemeter-client-7b74cd774c-fg6lz took: 1.957µs
I0719 01:46:01.816363   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-multus/multus-2nb4x
I0719 01:46:01.817185   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-multus/multus-2nb4x took: 2.157µs
I0719 01:46:01.817044   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-monitoring/openshift-state-metrics-6bb8db76bd-2wlhc Admin Network Policy controller: took 4.67µs
I0719 01:46:01.817195   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/rook-ceph-mon-b-59759dbb89-7jlvw in Admin Network Policy controller
I0719 01:46:01.817199   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/rook-ceph-mon-b-59759dbb89-7jlvw Admin Network Policy controller: took 4.947µs
I0719 01:46:01.817204   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-dns/dns-default-qzrlq in Admin Network Policy controller
I0719 01:46:01.817208   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-dns/dns-default-qzrlq Admin Network Policy controller: took 4.257µs
I0719 01:46:01.817213   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-dns/dns-default-zwbjg in Admin Network Policy controller
I0719 01:46:01.817217   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-dns/dns-default-zwbjg Admin Network Policy controller: took 3.866µs
I0719 01:46:01.817222   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-local-storage/diskmaker-manager-2zrc6 in Admin Network Policy controller
I0719 01:46:01.817225   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-local-storage/diskmaker-manager-2zrc6 Admin Network Policy controller: took 3.868µs
I0719 01:46:01.817230   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-cluster-storage-operator/cluster-storage-operator-6c5864c5b-kgzzc in Admin Network Policy controller
I0719 01:46:01.817234   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-cluster-storage-operator/cluster-storage-operator-6c5864c5b-kgzzc Admin Network Policy controller: took 4.181µs
I0719 01:46:01.817239   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-etcd/etcd-guard-00-50-56-8a-44-52 in Admin Network Policy controller
I0719 01:46:01.817243   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-etcd/etcd-guard-00-50-56-8a-44-52 Admin Network Policy controller: took 4.108µs
I0719 01:46:01.817247   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-machine-api/metal3-baremetal-operator-6fd5ccf9-9p448 in Admin Network Policy controller
I0719 01:46:01.817251   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-machine-api/metal3-baremetal-operator-6fd5ccf9-9p448 Admin Network Policy controller: took 3.974µs
I0719 01:46:01.817256   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-fb-ea in Admin Network Policy controller
I0719 01:46:01.817260   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-fb-ea Admin Network Policy controller: took 4.106µs
I0719 01:46:01.817265   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/csi-rbdplugin-b6gdm in Admin Network Policy controller
I0719 01:46:01.817268   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/csi-rbdplugin-b6gdm Admin Network Policy controller: took 3.893µs
I0719 01:46:01.817273   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/noobaa-core-0 in Admin Network Policy controller
I0719 01:46:01.817277   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/noobaa-core-0 Admin Network Policy controller: took 4.44µs
I0719 01:46:01.816835   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/rook-ceph-mgr-a-6fddb5fd95-mr2cn took: 5.255µs
I0719 01:46:01.817282   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-controller-manager/controller-manager-5c7f9f9d47-thph4 in Admin Network Policy controller
I0719 01:46:01.817286   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-controller-manager/controller-manager-5c7f9f9d47-thph4 Admin Network Policy controller: took 4.249µs
I0719 01:46:01.816932   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/rook-ceph-mds-ocs-storagecluster-cephfilesystem-b-c4dc5cd7zkffj took: 2.419µs
I0719 01:46:01.817291   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-ingress/router-default-54fb8ffc6b-kgb2v in Admin Network Policy controller
I0719 01:46:01.817294   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-machine-config-operator/machine-config-daemon-qpmqf
I0719 01:46:01.817296   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-ingress/router-default-54fb8ffc6b-kgb2v Admin Network Policy controller: took 4.989µs
I0719 01:46:01.817301   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-network-operator/iptables-alerter-wxl7s in Admin Network Policy controller
I0719 01:46:01.817301   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-machine-config-operator/machine-config-daemon-qpmqf took: 2.568µs
I0719 01:46:01.817305   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-network-operator/iptables-alerter-wxl7s Admin Network Policy controller: took 4.404µs
I0719 01:46:01.817307   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-ovn-kubernetes/ovnkube-node-568wp
I0719 01:46:01.817312   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/odf-operator-controller-manager-78d57f457c-tbwjf in Admin Network Policy controller
I0719 01:46:01.817314   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-ovn-kubernetes/ovnkube-node-568wp took: 1.674µs
I0719 01:46:01.817317   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/odf-operator-controller-manager-78d57f457c-tbwjf Admin Network Policy controller: took 6.435µs
I0719 01:46:01.817287   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-machine-api/cluster-baremetal-operator-5fb6f8f7d4-ltc5l
I0719 01:46:01.817322   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/csi-cephfsplugin-5fvh4 in Admin Network Policy controller
I0719 01:46:01.817326   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/csi-cephfsplugin-5fvh4 Admin Network Policy controller: took 4.324µs
I0719 01:46:01.817331   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-dns/node-resolver-tjmrc in Admin Network Policy controller
I0719 01:46:01.817335   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-dns/node-resolver-tjmrc Admin Network Policy controller: took 4.077µs
I0719 01:46:01.817339   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kni-infra/haproxy-00-50-56-8a-5c-ec in Admin Network Policy controller
I0719 01:46:01.817344   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kni-infra/haproxy-00-50-56-8a-5c-ec Admin Network Policy controller: took 5.139µs
I0719 01:46:01.817350   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-network-diagnostics/network-check-target-dj4vt in Admin Network Policy controller
I0719 01:46:01.817354   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-network-diagnostics/network-check-target-dj4vt Admin Network Policy controller: took 4.619µs
I0719 01:46:01.817358   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/rook-ceph-operator-cf758864f-c6zl8 in Admin Network Policy controller
I0719 01:46:01.817362   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/rook-ceph-operator-cf758864f-c6zl8 Admin Network Policy controller: took 4.015µs
I0719 01:46:01.817367   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-console/console-57f455cd77-h96cj in Admin Network Policy controller
I0719 01:46:01.817326   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-machine-api/cluster-baremetal-operator-5fb6f8f7d4-ltc5l took: 2.129µs
I0719 01:46:01.817378   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-f2-5d
I0719 01:46:01.817387   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-f2-5d took: 2.774µs
I0719 01:46:01.817391   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-storage/odf-console-b7ccd85c5-84cnv
I0719 01:46:01.817398   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-storage/odf-console-b7ccd85c5-84cnv took: 2.462µs
I0719 01:46:01.817402   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-cloud-controller-manager-operator/cluster-cloud-controller-manager-operator-7f55545d59-r8j8z
I0719 01:46:01.817409   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-cloud-controller-manager-operator/cluster-cloud-controller-manager-operator-7f55545d59-r8j8z took: 1.984µs
I0719 01:46:01.817413   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-network-diagnostics/network-check-target-jhhzw
I0719 01:46:01.817419   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-network-diagnostics/network-check-target-jhhzw took: 1.362µs
I0719 01:46:01.817423   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-kube-scheduler/openshift-kube-scheduler-guard-00-50-56-8a-39-a0
I0719 01:46:01.817429   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-kube-scheduler/openshift-kube-scheduler-guard-00-50-56-8a-39-a0 took: 1.678µs
I0719 01:46:01.817435   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-machine-api/ironic-proxy-sn8n9
I0719 01:46:01.817371   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-console/console-57f455cd77-h96cj Admin Network Policy controller: took 4.066µs
I0719 01:46:01.817451   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-monitoring/node-exporter-gbsmf in Admin Network Policy controller
I0719 01:46:01.817457   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-monitoring/node-exporter-gbsmf Admin Network Policy controller: took 6.955µs
I0719 01:46:01.817462   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-etcd/revision-pruner-9-00-50-56-8a-39-a0 in Admin Network Policy controller
I0719 01:46:01.817466   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-etcd/revision-pruner-9-00-50-56-8a-39-a0 Admin Network Policy controller: took 4.232µs
I0719 01:46:01.817471   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-etcd/revision-pruner-9-00-50-56-8a-5c-ec in Admin Network Policy controller
I0719 01:46:01.817475   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-etcd/revision-pruner-9-00-50-56-8a-5c-ec Admin Network Policy controller: took 3.967µs
I0719 01:46:01.817480   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kni-infra/keepalived-00-50-56-8a-e1-e7 in Admin Network Policy controller
I0719 01:46:01.817485   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kni-infra/keepalived-00-50-56-8a-e1-e7 Admin Network Policy controller: took 4.035µs
I0719 01:46:01.817490   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-monitoring/thanos-querier-68bf686489-qbcjs in Admin Network Policy controller
I0719 01:46:01.817494   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-monitoring/thanos-querier-68bf686489-qbcjs Admin Network Policy controller: took 4.027µs
I0719 01:46:01.817499   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-multus/network-metrics-daemon-7ttpg in Admin Network Policy controller
I0719 01:46:01.817503   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-multus/network-metrics-daemon-7ttpg Admin Network Policy controller: took 3.778µs
I0719 01:46:01.817507   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-operator-lifecycle-manager/collect-profiles-28689195-w9664 in Admin Network Policy controller
I0719 01:46:01.817512   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-operator-lifecycle-manager/collect-profiles-28689195-w9664 Admin Network Policy controller: took 4.737µs
I0719 01:46:01.817517   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-cluster-storage-operator/csi-snapshot-controller-794ff44f88-7cksj in Admin Network Policy controller
I0719 01:46:01.817441   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-machine-api/ironic-proxy-sn8n9 took: 1.851µs
I0719 01:46:01.817527   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-machine-api/metal3-599ff8f4b7-vntm7
I0719 01:46:01.817536   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-machine-api/metal3-599ff8f4b7-vntm7 took: 3.674µs
I0719 01:46:01.817541   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-marketplace/redhat-operators-mm6k4
I0719 01:46:01.817548   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-marketplace/redhat-operators-mm6k4 took: 2.159µs
I0719 01:46:01.817553   37437 obj_retry.go:502] Add event received for *factory.egressIPPod openshift-monitoring/alertmanager-main-0
I0719 01:46:01.817560   37437 obj_retry.go:541] Creating *factory.egressIPPod openshift-monitoring/alertmanager-main-0 took: 2.254µs
I0719 01:46:01.817567   37437 factory.go:988] Added *v1.Pod event handler 7
I0719 01:46:01.817521   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-cluster-storage-operator/csi-snapshot-controller-794ff44f88-7cksj Admin Network Policy controller: took 4.041µs
I0719 01:46:01.817581   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-dns/node-resolver-bf5zv in Admin Network Policy controller
I0719 01:46:01.817586   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-dns/node-resolver-bf5zv Admin Network Policy controller: took 5.492µs
I0719 01:46:01.817591   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-console/console-57f455cd77-77wrt in Admin Network Policy controller
I0719 01:46:01.817595   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-console/console-57f455cd77-77wrt Admin Network Policy controller: took 4.228µs
I0719 01:46:01.817600   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-image-registry/node-ca-lfxb8 in Admin Network Policy controller
I0719 01:46:01.817604   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-image-registry/node-ca-lfxb8 Admin Network Policy controller: took 4.043µs
I0719 01:46:01.817609   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-ingress-operator/ingress-operator-5cc96867f4-pdgdd in Admin Network Policy controller
I0719 01:46:01.817613   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-ingress-operator/ingress-operator-5cc96867f4-pdgdd Admin Network Policy controller: took 4.09µs
I0719 01:46:01.817617   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-machine-api/metal3-image-customization-5f9d4c754c-5v2p8 in Admin Network Policy controller
I0719 01:46:01.817622   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-machine-api/metal3-image-customization-5f9d4c754c-5v2p8 Admin Network Policy controller: took 4.083µs
I0719 01:46:01.817626   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-machine-config-operator/machine-config-daemon-r8bgv in Admin Network Policy controller
I0719 01:46:01.817630   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-machine-config-operator/machine-config-daemon-r8bgv Admin Network Policy controller: took 3.939µs
I0719 01:46:01.817635   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-monitoring/metrics-server-7d47f4cbc-dqrxk in Admin Network Policy controller
I0719 01:46:01.817639   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-monitoring/metrics-server-7d47f4cbc-dqrxk Admin Network Policy controller: took 4.319µs
I0719 01:46:01.817644   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-apiserver/apiserver-7d9bbd465d-6cgbw in Admin Network Policy controller
I0719 01:46:01.817648   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-apiserver/apiserver-7d9bbd465d-6cgbw Admin Network Policy controller: took 4.006µs
I0719 01:46:01.817653   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-authentication-operator/authentication-operator-68795c8768-8rvtz in Admin Network Policy controller
I0719 01:46:01.817657   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-authentication-operator/authentication-operator-68795c8768-8rvtz Admin Network Policy controller: took 4.377µs
I0719 01:46:01.817662   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/rook-ceph-mgr-a-6fddb5fd95-mr2cn in Admin Network Policy controller
I0719 01:46:01.817666   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/rook-ceph-mgr-a-6fddb5fd95-mr2cn Admin Network Policy controller: took 3.809µs
I0719 01:46:01.817670   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/rook-ceph-mgr-b-779b65ccb6-29sz4 in Admin Network Policy controller
I0719 01:46:01.817674   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/rook-ceph-mgr-b-779b65ccb6-29sz4 Admin Network Policy controller: took 3.739µs
I0719 01:46:01.817679   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-service-ca/service-ca-6dbc4646f9-6q769 in Admin Network Policy controller
I0719 01:46:01.817684   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-service-ca/service-ca-6dbc4646f9-6q769 Admin Network Policy controller: took 3.995µs
I0719 01:46:01.817689   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/rook-ceph-crashcollector-00-50-56-8a-f2-5d-5bfb656d8f-tvtpr in Admin Network Policy controller
I0719 01:46:01.817693   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/rook-ceph-crashcollector-00-50-56-8a-f2-5d-5bfb656d8f-tvtpr Admin Network Policy controller: took 4.11µs
I0719 01:46:01.817698   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kni-infra/haproxy-00-50-56-8a-39-a0 in Admin Network Policy controller
I0719 01:46:01.817701   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kni-infra/haproxy-00-50-56-8a-39-a0 Admin Network Policy controller: took 3.758µs
I0719 01:46:01.817623   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Router_Policy Row:map[action:allow match:ip4.src == 10.128.0.0/14 && ip4.dst == 10.128.0.0/14 priority:102] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {94163063-61a6-4eac-8bfb-2a0609fc22a0}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.817706   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kube-scheduler-operator/openshift-kube-scheduler-operator-555f7bb8bc-4vw77 in Admin Network Policy controller
I0719 01:46:01.817711   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kube-scheduler-operator/openshift-kube-scheduler-operator-555f7bb8bc-4vw77 Admin Network Policy controller: took 4.85µs
I0719 01:46:01.817715   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/noobaa-operator-bf7774fd8-zskvp in Admin Network Policy controller
I0719 01:46:01.817719   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/noobaa-operator-bf7774fd8-zskvp Admin Network Policy controller: took 3.792µs
I0719 01:46:01.817723   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-image-registry/node-ca-986d7 in Admin Network Policy controller
I0719 01:46:01.817727   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-image-registry/node-ca-986d7 Admin Network Policy controller: took 3.902µs
I0719 01:46:01.817732   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kni-infra/coredns-00-50-56-8a-f2-5d in Admin Network Policy controller
I0719 01:46:01.817736   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kni-infra/coredns-00-50-56-8a-f2-5d Admin Network Policy controller: took 3.879µs
I0719 01:46:01.817729   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:policies Mutator:insert Value:{GoSet:[{GoUUID:94163063-61a6-4eac-8bfb-2a0609fc22a0}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.817740   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-machine-api/ironic-proxy-k9xzh in Admin Network Policy controller
I0719 01:46:01.817744   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-machine-api/ironic-proxy-k9xzh Admin Network Policy controller: took 4.087µs
I0719 01:46:01.817749   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-multus/multus-additional-cni-plugins-tpn87 in Admin Network Policy controller
I0719 01:46:01.817753   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-multus/multus-additional-cni-plugins-tpn87 Admin Network Policy controller: took 3.799µs
I0719 01:46:01.817743   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Router_Policy Row:map[action:allow match:ip4.src == 10.128.0.0/14 && ip4.dst == 10.128.0.0/14 priority:102] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {94163063-61a6-4eac-8bfb-2a0609fc22a0}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:policies Mutator:insert Value:{GoSet:[{GoUUID:94163063-61a6-4eac-8bfb-2a0609fc22a0}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.817758   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-ovn-kubernetes/ovnkube-node-5bqnj in Admin Network Policy controller
I0719 01:46:01.817763   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-ovn-kubernetes/ovnkube-node-5bqnj Admin Network Policy controller: took 5.031µs
I0719 01:46:01.817768   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-ovn-kubernetes/ovnkube-node-mqh7r in Admin Network Policy controller
I0719 01:46:01.817772   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-ovn-kubernetes/ovnkube-node-mqh7r Admin Network Policy controller: took 3.981µs
I0719 01:46:01.817776   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-image-registry/node-ca-sq7qk in Admin Network Policy controller
I0719 01:46:01.817780   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-image-registry/node-ca-sq7qk Admin Network Policy controller: took 3.909µs
I0719 01:46:01.817785   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-44-52 in Admin Network Policy controller
I0719 01:46:01.817789   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-44-52 Admin Network Policy controller: took 3.959µs
I0719 01:46:01.817793   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-dns-operator/dns-operator-5fc6bf9796-jgj7s in Admin Network Policy controller
I0719 01:46:01.817797   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-dns-operator/dns-operator-5fc6bf9796-jgj7s Admin Network Policy controller: took 3.957µs
I0719 01:46:01.817801   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-insights/insights-operator-586b65d57b-7rk2w in Admin Network Policy controller
I0719 01:46:01.817805   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-insights/insights-operator-586b65d57b-7rk2w Admin Network Policy controller: took 4.042µs
I0719 01:46:01.817810   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-ovn-kubernetes/ovnkube-node-9h9qr in Admin Network Policy controller
I0719 01:46:01.817814   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-ovn-kubernetes/ovnkube-node-9h9qr Admin Network Policy controller: took 3.76µs
I0719 01:46:01.817818   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-marketplace/community-operators-wgnxc in Admin Network Policy controller
I0719 01:46:01.817822   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-marketplace/community-operators-wgnxc Admin Network Policy controller: took 3.832µs
I0719 01:46:01.817827   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-monitoring/cluster-monitoring-operator-b4b4bcf9f-d4xhg in Admin Network Policy controller
I0719 01:46:01.817831   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-monitoring/cluster-monitoring-operator-b4b4bcf9f-d4xhg Admin Network Policy controller: took 4.078µs
I0719 01:46:01.817835   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/ocs-client-operator-console-6fdbfcd95-jhcss in Admin Network Policy controller
I0719 01:46:01.817840   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/ocs-client-operator-console-6fdbfcd95-jhcss Admin Network Policy controller: took 4.156µs
I0719 01:46:01.817845   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-storage/rook-ceph-mds-ocs-storagecluster-cephfilesystem-a-8679ddf7kqp98 in Admin Network Policy controller
I0719 01:46:01.817849   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-storage/rook-ceph-mds-ocs-storagecluster-cephfilesystem-a-8679ddf7kqp98 Admin Network Policy controller: took 4.227µs
I0719 01:46:01.817854   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kube-controller-manager/kube-controller-manager-guard-00-50-56-8a-39-a0 in Admin Network Policy controller
I0719 01:46:01.817858   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kube-controller-manager/kube-controller-manager-guard-00-50-56-8a-39-a0 Admin Network Policy controller: took 4.032µs
I0719 01:46:01.817862   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-machine-api/cluster-baremetal-operator-5fb6f8f7d4-ltc5l in Admin Network Policy controller
I0719 01:46:01.817867   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-machine-api/cluster-baremetal-operator-5fb6f8f7d4-ltc5l Admin Network Policy controller: took 4.646µs
I0719 01:46:01.817872   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-etcd/etcd-00-50-56-8a-39-a0 in Admin Network Policy controller
I0719 01:46:01.817875   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-etcd/etcd-00-50-56-8a-39-a0 Admin Network Policy controller: took 3.824µs
I0719 01:46:01.817880   37437 admin_network_policy_pod.go:56] Processing sync for Pod openshift-kni-infra/keepalived-00-50-56-8a-f2-5d in Admin Network Policy controller
I0719 01:46:01.817884   37437 admin_network_policy_pod.go:59] Finished syncing Pod openshift-kni-infra/keepalived-00-50-56-8a-f2-5d Admin Network Policy controller: took 3.889µs
I0719 01:46:01.818103   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Router_Policy Row:map[action:allow match:ip4.src == 10.128.0.0/14 && ip4.dst == 100.64.0.0/16 priority:102] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {b07e8c57-f2b1-4ea8-974c-bf5597481445}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.818148   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:policies Mutator:insert Value:{GoSet:[{GoUUID:b07e8c57-f2b1-4ea8-974c-bf5597481445}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.818167   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Router_Policy Row:map[action:allow match:ip4.src == 10.128.0.0/14 && ip4.dst == 100.64.0.0/16 priority:102] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {b07e8c57-f2b1-4ea8-974c-bf5597481445}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:policies Mutator:insert Value:{GoSet:[{GoUUID:b07e8c57-f2b1-4ea8-974c-bf5597481445}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.818414   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Router_Policy Row:map[action:allow external_ids:{GoMap:map[ip-family:ip k8s.ovn.org/id:default-network-controller:EgressIP:102:EIP-No-Reroute-reply-traffic:ip k8s.ovn.org/name:EIP-No-Reroute-reply-traffic k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:EgressIP priority:102]} match:pkt.mark == 42 priority:102] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {597a4aae-2b65-43b8-b2af-a74393734f47}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.818462   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:policies Mutator:insert Value:{GoSet:[{GoUUID:597a4aae-2b65-43b8-b2af-a74393734f47}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.818482   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Router_Policy Row:map[action:allow external_ids:{GoMap:map[ip-family:ip k8s.ovn.org/id:default-network-controller:EgressIP:102:EIP-No-Reroute-reply-traffic:ip k8s.ovn.org/name:EIP-No-Reroute-reply-traffic k8s.ovn.org/owner-controller:default-network-controller k8s.ovn.org/owner-type:EgressIP priority:102]} match:pkt.mark == 42 priority:102] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {597a4aae-2b65-43b8-b2af-a74393734f47}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:policies Mutator:insert Value:{GoSet:[{GoUUID:597a4aae-2b65-43b8-b2af-a74393734f47}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.818731   37437 address_set.go:304] New(7810e501-de3f-425b-bbb6-8472f5cd1e1d/default-network-controller:EgressIP:node-ips:v4/a14918748166599097711) with []
I0719 01:46:01.818753   37437 address_set.go:304] New(56bd379c-e2e9-4708-b784-36bd80cece61/default-network-controller:EgressIP:egressip-served-pods:v4/a4548040316634674295) with []
I0719 01:46:01.818768   37437 address_set.go:304] New(ff451472-f1f3-4db7-bb61-f7f38984d502/default-network-controller:EgressService:egresssvc-served-pods:v4/a13607449821398607916) with []
I0719 01:46:01.818900   37437 obj_retry.go:502] Add event received for *factory.egressNode 00-50-56-8a-39-a0
I0719 01:46:01.818910   37437 obj_retry.go:502] Add event received for *factory.egressNode 00-50-56-8a-fb-ea
I0719 01:46:01.818919   37437 obj_retry.go:502] Add event received for *factory.egressNode 00-50-56-8a-e1-e7
I0719 01:46:01.818924   37437 obj_retry.go:502] Add event received for *factory.egressNode 00-50-56-8a-f2-5d
I0719 01:46:01.818901   37437 obj_retry.go:502] Add event received for *factory.egressNode 00-50-56-8a-5c-ec
I0719 01:46:01.818901   37437 obj_retry.go:502] Add event received for *factory.egressNode 00-50-56-8a-44-52
I0719 01:46:01.819073   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.10.25.179 10.10.25.203 10.10.25.192 10.10.25.250 10.10.25.178 10.10.25.191 10.10.25.235 10.10.25.190]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {7810e501-de3f-425b-bbb6-8472f5cd1e1d}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.819094   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.10.25.179 10.10.25.203 10.10.25.192 10.10.25.250 10.10.25.178 10.10.25.191 10.10.25.235 10.10.25.190]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {7810e501-de3f-425b-bbb6-8472f5cd1e1d}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.819422   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Router_Policy Row:map[action:allow match:(ip4.src == $a4548040316634674295 || ip4.src == $a13607449821398607916) && ip4.dst == $a14918748166599097711 options:{GoMap:map[pkt_mark:1008]} priority:102] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {e2ad1968-9777-481d-b706-76472e04c8d6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.819463   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:policies Mutator:insert Value:{GoSet:[{GoUUID:e2ad1968-9777-481d-b706-76472e04c8d6}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.819478   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Router_Policy Row:map[action:allow match:(ip4.src == $a4548040316634674295 || ip4.src == $a13607449821398607916) && ip4.dst == $a14918748166599097711 options:{GoMap:map[pkt_mark:1008]} priority:102] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {e2ad1968-9777-481d-b706-76472e04c8d6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:policies Mutator:insert Value:{GoSet:[{GoUUID:e2ad1968-9777-481d-b706-76472e04c8d6}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.819686   37437 obj_retry.go:541] Creating *factory.egressNode 00-50-56-8a-39-a0 took: 771.776µs
I0719 01:46:01.819866   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.10.25.190 10.10.25.203 10.10.25.192 10.10.25.178 10.10.25.250 10.10.25.191 10.10.25.235 10.10.25.179]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {7810e501-de3f-425b-bbb6-8472f5cd1e1d}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.819886   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.10.25.190 10.10.25.203 10.10.25.192 10.10.25.178 10.10.25.250 10.10.25.191 10.10.25.235 10.10.25.179]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {7810e501-de3f-425b-bbb6-8472f5cd1e1d}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.820225   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Router_Policy Row:map[action:allow match:(ip4.src == $a4548040316634674295 || ip4.src == $a13607449821398607916) && ip4.dst == $a14918748166599097711 options:{GoMap:map[pkt_mark:1008]} priority:102] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {e2ad1968-9777-481d-b706-76472e04c8d6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.820270   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:policies Mutator:insert Value:{GoSet:[{GoUUID:e2ad1968-9777-481d-b706-76472e04c8d6}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.820285   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Router_Policy Row:map[action:allow match:(ip4.src == $a4548040316634674295 || ip4.src == $a13607449821398607916) && ip4.dst == $a14918748166599097711 options:{GoMap:map[pkt_mark:1008]} priority:102] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {e2ad1968-9777-481d-b706-76472e04c8d6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:policies Mutator:insert Value:{GoSet:[{GoUUID:e2ad1968-9777-481d-b706-76472e04c8d6}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.820532   37437 egressip.go:1280] Egress node: 00-50-56-8a-fb-ea about to be initialized
I0719 01:46:01.820634   37437 model_client.go:406] Delete operations generated as: [{Op:delete Table:Logical_Router_Static_Route Row:map[] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {00f4221b-aba0-497e-bde0-67d1f036dff8}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.820668   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:delete Value:{GoSet:[{GoUUID:00f4221b-aba0-497e-bde0-67d1f036dff8}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.820701   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Router_Static_Route Row:map[ip_prefix:10.128.0.0/14 nexthop:100.64.0.4 policy:{GoSet:[src-ip]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {a90a0017-6c59-4709-bd11-730f103dc482}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.820733   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:insert Value:{GoSet:[{GoUUID:a90a0017-6c59-4709-bd11-730f103dc482}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.820747   37437 transact.go:42] Configuring OVN: [{Op:delete Table:Logical_Router_Static_Route Row:map[] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {00f4221b-aba0-497e-bde0-67d1f036dff8}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:delete Value:{GoSet:[{GoUUID:00f4221b-aba0-497e-bde0-67d1f036dff8}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:update Table:Logical_Router_Static_Route Row:map[ip_prefix:10.128.0.0/14 nexthop:100.64.0.4 policy:{GoSet:[src-ip]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {a90a0017-6c59-4709-bd11-730f103dc482}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:static_routes Mutator:insert Value:{GoSet:[{GoUUID:a90a0017-6c59-4709-bd11-730f103dc482}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.820770   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.10.25.250 10.10.25.191 10.10.25.235 10.10.25.190 10.10.25.179 10.10.25.203 10.10.25.192 10.10.25.178]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {7810e501-de3f-425b-bbb6-8472f5cd1e1d}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.820790   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.10.25.250 10.10.25.191 10.10.25.235 10.10.25.190 10.10.25.179 10.10.25.203 10.10.25.192 10.10.25.178]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {7810e501-de3f-425b-bbb6-8472f5cd1e1d}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.821371   37437 obj_retry.go:541] Creating *factory.egressNode 00-50-56-8a-fb-ea took: 2.448127ms
I0719 01:46:01.821380   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Router_Policy Row:map[action:allow match:(ip4.src == $a4548040316634674295 || ip4.src == $a13607449821398607916) && ip4.dst == $a14918748166599097711 options:{GoMap:map[pkt_mark:1008]} priority:102] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {e2ad1968-9777-481d-b706-76472e04c8d6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.821420   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:policies Mutator:insert Value:{GoSet:[{GoUUID:e2ad1968-9777-481d-b706-76472e04c8d6}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.821441   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Router_Policy Row:map[action:allow match:(ip4.src == $a4548040316634674295 || ip4.src == $a13607449821398607916) && ip4.dst == $a14918748166599097711 options:{GoMap:map[pkt_mark:1008]} priority:102] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {e2ad1968-9777-481d-b706-76472e04c8d6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:policies Mutator:insert Value:{GoSet:[{GoUUID:e2ad1968-9777-481d-b706-76472e04c8d6}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.821723   37437 obj_retry.go:541] Creating *factory.egressNode 00-50-56-8a-e1-e7 took: 2.789349ms
I0719 01:46:01.821875   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.10.25.178 10.10.25.250 10.10.25.191 10.10.25.235 10.10.25.179 10.10.25.190 10.10.25.203 10.10.25.192]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {7810e501-de3f-425b-bbb6-8472f5cd1e1d}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.821902   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.10.25.178 10.10.25.250 10.10.25.191 10.10.25.235 10.10.25.179 10.10.25.190 10.10.25.203 10.10.25.192]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {7810e501-de3f-425b-bbb6-8472f5cd1e1d}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.822229   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Router_Policy Row:map[action:allow match:(ip4.src == $a4548040316634674295 || ip4.src == $a13607449821398607916) && ip4.dst == $a14918748166599097711 options:{GoMap:map[pkt_mark:1008]} priority:102] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {e2ad1968-9777-481d-b706-76472e04c8d6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.822274   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:policies Mutator:insert Value:{GoSet:[{GoUUID:e2ad1968-9777-481d-b706-76472e04c8d6}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.822289   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Router_Policy Row:map[action:allow match:(ip4.src == $a4548040316634674295 || ip4.src == $a13607449821398607916) && ip4.dst == $a14918748166599097711 options:{GoMap:map[pkt_mark:1008]} priority:102] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {e2ad1968-9777-481d-b706-76472e04c8d6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:policies Mutator:insert Value:{GoSet:[{GoUUID:e2ad1968-9777-481d-b706-76472e04c8d6}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.822547   37437 obj_retry.go:541] Creating *factory.egressNode 00-50-56-8a-f2-5d took: 3.592351ms
I0719 01:46:01.822680   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.10.25.235 10.10.25.179 10.10.25.190 10.10.25.203 10.10.25.192 10.10.25.178 10.10.25.250 10.10.25.191]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {7810e501-de3f-425b-bbb6-8472f5cd1e1d}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.822701   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.10.25.235 10.10.25.179 10.10.25.190 10.10.25.203 10.10.25.192 10.10.25.178 10.10.25.250 10.10.25.191]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {7810e501-de3f-425b-bbb6-8472f5cd1e1d}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.823007   37437 ovs.go:162] Exec(31): stdout: "1\n"
I0719 01:46:01.823020   37437 ovs.go:163] Exec(31): stderr: ""
I0719 01:46:01.823032   37437 ovs.go:159] Exec(32): /usr/bin/ovs-vsctl --timeout=15 --if-exists get interface br-ex mac_in_use
I0719 01:46:01.823047   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Router_Policy Row:map[action:allow match:(ip4.src == $a4548040316634674295 || ip4.src == $a13607449821398607916) && ip4.dst == $a14918748166599097711 options:{GoMap:map[pkt_mark:1008]} priority:102] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {e2ad1968-9777-481d-b706-76472e04c8d6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.823095   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:policies Mutator:insert Value:{GoSet:[{GoUUID:e2ad1968-9777-481d-b706-76472e04c8d6}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.823122   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Router_Policy Row:map[action:allow match:(ip4.src == $a4548040316634674295 || ip4.src == $a13607449821398607916) && ip4.dst == $a14918748166599097711 options:{GoMap:map[pkt_mark:1008]} priority:102] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {e2ad1968-9777-481d-b706-76472e04c8d6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:policies Mutator:insert Value:{GoSet:[{GoUUID:e2ad1968-9777-481d-b706-76472e04c8d6}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.823368   37437 obj_retry.go:541] Creating *factory.egressNode 00-50-56-8a-5c-ec took: 4.360133ms
I0719 01:46:01.823574   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.10.25.178 10.10.25.250 10.10.25.191 10.10.25.235 10.10.25.190 10.10.25.179 10.10.25.203 10.10.25.192]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {7810e501-de3f-425b-bbb6-8472f5cd1e1d}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.823607   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[10.10.25.178 10.10.25.250 10.10.25.191 10.10.25.235 10.10.25.190 10.10.25.179 10.10.25.203 10.10.25.192]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {7810e501-de3f-425b-bbb6-8472f5cd1e1d}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.823925   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Logical_Router_Policy Row:map[action:allow match:(ip4.src == $a4548040316634674295 || ip4.src == $a13607449821398607916) && ip4.dst == $a14918748166599097711 options:{GoMap:map[pkt_mark:1008]} priority:102] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {e2ad1968-9777-481d-b706-76472e04c8d6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.823966   37437 model_client.go:397] Mutate operations generated as: [{Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:policies Mutator:insert Value:{GoSet:[{GoUUID:e2ad1968-9777-481d-b706-76472e04c8d6}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.823989   37437 transact.go:42] Configuring OVN: [{Op:update Table:Logical_Router_Policy Row:map[action:allow match:(ip4.src == $a4548040316634674295 || ip4.src == $a13607449821398607916) && ip4.dst == $a14918748166599097711 options:{GoMap:map[pkt_mark:1008]} priority:102] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {e2ad1968-9777-481d-b706-76472e04c8d6}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:} {Op:mutate Table:Logical_Router Row:map[] Rows:[] Columns:[] Mutations:[{Column:policies Mutator:insert Value:{GoSet:[{GoUUID:e2ad1968-9777-481d-b706-76472e04c8d6}]}}] Timeout:<nil> Where:[where column _uuid == {a4c8a135-565b-498d-a63f-15379886b783}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.824218   37437 obj_retry.go:541] Creating *factory.egressNode 00-50-56-8a-44-52 took: 5.206033ms
I0719 01:46:01.824238   37437 factory.go:988] Added *v1.Node event handler 8
I0719 01:46:01.824260   37437 factory.go:988] Added *v1.EgressIP event handler 9
I0719 01:46:01.824434   37437 factory.go:988] Added *v1.EgressFirewall event handler 10
I0719 01:46:01.824513   37437 obj_retry.go:502] Add event received for *factory.egressFwNode 00-50-56-8a-39-a0
I0719 01:46:01.824544   37437 obj_retry.go:502] Add event received for *factory.egressFwNode 00-50-56-8a-e1-e7
I0719 01:46:01.824558   37437 obj_retry.go:541] Creating *factory.egressFwNode 00-50-56-8a-39-a0 took: 27.537µs
I0719 01:46:01.824561   37437 obj_retry.go:502] Add event received for *factory.egressFwNode 00-50-56-8a-f2-5d
I0719 01:46:01.824574   37437 obj_retry.go:502] Add event received for *factory.egressFwNode 00-50-56-8a-fb-ea
I0719 01:46:01.824580   37437 obj_retry.go:541] Creating *factory.egressFwNode 00-50-56-8a-e1-e7 took: 21.964µs
I0719 01:46:01.824590   37437 obj_retry.go:541] Creating *factory.egressFwNode 00-50-56-8a-f2-5d took: 17.717µs
I0719 01:46:01.824591   37437 obj_retry.go:502] Add event received for *factory.egressFwNode 00-50-56-8a-5c-ec
I0719 01:46:01.824598   37437 obj_retry.go:541] Creating *factory.egressFwNode 00-50-56-8a-fb-ea took: 15.69µs
I0719 01:46:01.824615   37437 obj_retry.go:541] Creating *factory.egressFwNode 00-50-56-8a-5c-ec took: 10.674µs
I0719 01:46:01.824590   37437 obj_retry.go:502] Add event received for *factory.egressFwNode 00-50-56-8a-44-52
I0719 01:46:01.824633   37437 obj_retry.go:541] Creating *factory.egressFwNode 00-50-56-8a-44-52 took: 9.104µs
I0719 01:46:01.824642   37437 factory.go:988] Added *v1.Node event handler 11
I0719 01:46:01.824653   37437 egressqos.go:193] Setting up event handlers for EgressQoS
I0719 01:46:01.824968   37437 egressqos.go:245] Starting EgressQoS Controller
I0719 01:46:01.824989   37437 shared_informer.go:311] Waiting for caches to sync for egressqosnodes
I0719 01:46:01.824995   37437 shared_informer.go:318] Caches are synced for egressqosnodes
I0719 01:46:01.825000   37437 shared_informer.go:311] Waiting for caches to sync for egressqospods
I0719 01:46:01.825004   37437 shared_informer.go:318] Caches are synced for egressqospods
I0719 01:46:01.825008   37437 shared_informer.go:311] Waiting for caches to sync for egressqos
I0719 01:46:01.825011   37437 shared_informer.go:318] Caches are synced for egressqos
I0719 01:46:01.825015   37437 egressqos.go:259] Repairing EgressQoSes
I0719 01:46:01.825019   37437 egressqos.go:400] Starting repairing loop for egressqos
I0719 01:46:01.825090   37437 egressqos.go:402] Finished repairing loop for egressqos: 69.736µs
I0719 01:46:01.825109   37437 egressservice_zone.go:129] Setting up event handlers for Egress Services
I0719 01:46:01.825179   37437 egressqos.go:1008] Processing sync for EgressQoS node 00-50-56-8a-fb-ea
I0719 01:46:01.825341   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-service-ca-operator/metrics for endpointslice openshift-service-ca-operator/metrics-q4cb9 as it is not a known egress service
I0719 01:46:01.825363   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-etcd/etcd for endpointslice openshift-etcd/etcd-jqbgq as it is not a known egress service
I0719 01:46:01.825375   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-ingress-operator/metrics for endpointslice openshift-ingress-operator/metrics-whm4p as it is not a known egress service
I0719 01:46:01.825378   37437 egressservice_zone.go:205] Starting Egress Services Controller
I0719 01:46:01.825381   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-storage/ocs-client-operator-controller-manager-metrics-service for endpointslice openshift-storage/ocs-client-operator-controller-manager-metrics-service-b8dnf as it is not a known egress service
I0719 01:46:01.825388   37437 shared_informer.go:311] Waiting for caches to sync for egressservices
I0719 01:46:01.825388   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-storage/odf-console-service for endpointslice openshift-storage/odf-console-service-8q9zr as it is not a known egress service
I0719 01:46:01.825394   37437 shared_informer.go:318] Caches are synced for egressservices
I0719 01:46:01.825396   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-storage/rook-ceph-mgr for endpointslice openshift-storage/rook-ceph-mgr-rx9qr as it is not a known egress service
I0719 01:46:01.825399   37437 shared_informer.go:311] Waiting for caches to sync for egressservices_services
I0719 01:46:01.825401   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-console/console for endpointslice openshift-console/console-czxzd as it is not a known egress service
I0719 01:46:01.825403   37437 shared_informer.go:318] Caches are synced for egressservices_services
I0719 01:46:01.825407   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-operator-lifecycle-manager/olm-operator-metrics for endpointslice openshift-operator-lifecycle-manager/olm-operator-metrics-zc4pl as it is not a known egress service
I0719 01:46:01.825407   37437 shared_informer.go:311] Waiting for caches to sync for egressservices_endpointslices
I0719 01:46:01.825188   37437 egressqos.go:1023] EgressQoS 00-50-56-8a-fb-ea node retrieved from lister: &Node{ObjectMeta:{00-50-56-8a-fb-ea    2488f6b8-3abd-4376-978b-8281d8547579 300997 0 2024-07-18 19:58:16 +0000 UTC <nil> <nil> map[beta.kubernetes.io/arch:amd64 beta.kubernetes.io/os:linux kubernetes.io/arch:amd64 kubernetes.io/hostname:00-50-56-8a-fb-ea kubernetes.io/os:linux node-role.kubernetes.io/worker: node.openshift.io/os_id:rhcos] map[csi.volume.kubernetes.io/nodeid:{"openshift-storage.cephfs.csi.ceph.com":"00-50-56-8a-fb-ea","openshift-storage.rbd.csi.ceph.com":"00-50-56-8a-fb-ea"} k8s.ovn.org/host-cidrs:["10.10.25.235/24"] k8s.ovn.org/l3-gateway-config:{"default":{"mode":"shared","interface-id":"br-ex_00-50-56-8a-fb-ea","mac-address":"00:50:56:8a:fb:ea","ip-addresses":["10.10.25.235/24"],"ip-address":"10.10.25.235/24","next-hops":["10.10.25.1"],"next-hop":"10.10.25.1","node-port-enable":"true","vlan-id":"0"}} k8s.ovn.org/network-ids:{"default":"0"} k8s.ovn.org/node-chassis-id:ec7a39e5-89ad-4e47-a317-9fefe94160bf k8s.ovn.org/node-gateway-router-lrp-ifaddr:{"ipv4":"100.64.0.4/16"} k8s.ovn.org/node-id:4 k8s.ovn.org/node-mgmt-port-mac-address:be:6d:32:1d:e9:29 k8s.ovn.org/node-primary-ifaddr:{"ipv4":"10.10.25.235/24"} k8s.ovn.org/node-subnets:{"default":["10.130.0.0/23"]} k8s.ovn.org/node-transit-switch-port-ifaddr:{"ipv4":"100.88.0.4/16"} k8s.ovn.org/remote-zone-migrated:00-50-56-8a-fb-ea k8s.ovn.org/zone-name:00-50-56-8a-fb-ea machine.openshift.io/machine:openshift-machine-api/vmware-cluster-9ffwp-worker-0-qs6ct machineconfiguration.openshift.io/controlPlaneTopology:HighlyAvailable machineconfiguration.openshift.io/currentConfig:rendered-worker-579b01fcc039e9e8fbe8738fe153d0f4 machineconfiguration.openshift.io/desiredConfig:rendered-worker-579b01fcc039e9e8fbe8738fe153d0f4 machineconfiguration.openshift.io/desiredDrain:uncordon-rendered-worker-579b01fcc039e9e8fbe8738fe153d0f4 machineconfiguration.openshift.io/lastAppliedDrain:uncordon-rendered-worker-579b01fcc039e9e8fbe8738fe153d0f4 machineconfiguration.openshift.io/lastObservedServerCAAnnotation:false machineconfiguration.openshift.io/lastSyncedControllerConfigResourceVersion:207452 machineconfiguration.openshift.io/post-config-action: machineconfiguration.openshift.io/reason: machineconfiguration.openshift.io/state:Done volumes.kubernetes.io/controller-managed-attach-detach:true] [] [] []},Spec:NodeSpec{PodCIDR:,DoNotUseExternalID:,ProviderID:baremetalhost:///openshift-machine-api/00-50-56-8a-fb-ea/d1be48fd-c473-4206-b810-4056e70e3b25,Unschedulable:false,Taints:[]Taint{Taint{Key:node.kubernetes.io/not-ready,Value:,Effect:NoSchedule,TimeAdded:2024-07-19 01:19:00 +0000 UTC,},Taint{Key:node.kubernetes.io/not-ready,Value:,Effect:NoExecute,TimeAdded:2024-07-19 01:19:01 +0000 UTC,},},ConfigSource:nil,PodCIDRs:[],},Status:NodeStatus{Capacity:ResourceList{cpu: {{12 0} {<nil>} 12 DecimalSI},ephemeral-storage: {{106769133568 0} {<nil>} 104266732Ki BinarySI},hugepages-1Gi: {{0 0} {<nil>} 0 DecimalSI},hugepages-2Mi: {{0 0} {<nil>} 0 DecimalSI},memory: {{33653567488 0} {<nil>} 32864812Ki BinarySI},pods: {{250 0} {<nil>} 250 DecimalSI},},Allocatable:ResourceList{cpu: {{11500 -3} {<nil>} 11500m DecimalSI},ephemeral-storage: {{95018478229 0} {<nil>} 95018478229 DecimalSI},hugepages-1Gi: {{0 0} {<nil>} 0 DecimalSI},hugepages-2Mi: {{0 0} {<nil>} 0 DecimalSI},memory: {{32474968064 0} {<nil>} 31713836Ki BinarySI},pods: {{250 0} {<nil>} 250 DecimalSI},},Phase:,Conditions:[]NodeCondition{NodeCondition{Type:MemoryPressure,Status:False,LastHeartbeatTime:2024-07-19 01:41:07 +0000 UTC,LastTransitionTime:2024-07-19 01:19:00 +0000 UTC,Reason:KubeletHasSufficientMemory,Message:kubelet has sufficient memory available,},NodeCondition{Type:DiskPressure,Status:False,LastHeartbeatTime:2024-07-19 01:41:07 +0000 UTC,LastTransitionTime:2024-07-19 01:19:00 +0000 UTC,Reason:KubeletHasNoDiskPressure,Message:kubelet has no disk pressure,},NodeCondition{Type:PIDPressure,Status:False,LastHeartbeatTime:2024-07-19 01:41:07 +0000 UTC,LastTransitionTime:2024-07-19 01:19:00 +0000 UTC,Reason:KubeletHasSufficientPID,Message:kubelet has sufficient PID available,},NodeCondition{Type:Ready,Status:False,LastHeartbeatTime:2024-07-19 01:41:07 +0000 UTC,LastTransitionTime:2024-07-19 01:19:00 +0000 UTC,Reason:KubeletNotReady,Message:container runtime network not ready: NetworkReady=false reason:NetworkPluginNotReady message:Network plugin returns error: No CNI configuration file in /etc/kubernetes/cni/net.d/. Has your network provider started?,},},Addresses:[]NodeAddress{NodeAddress{Type:InternalIP,Address:10.10.25.235,},NodeAddress{Type:Hostname,Address:00-50-56-8a-fb-ea,},},DaemonEndpoints:NodeDaemonEndpoints{KubeletEndpoint:DaemonEndpoint{Port:10250,},},NodeInfo:NodeSystemInfo{MachineID:d3fc109db19247a296df60402ab42cf9,SystemUUID:3e3a0a42-d17b-3623-543f-dc350d4ba17f,BootID:3a898992-b4c5-40aa-9ea3-8ece2a3ba1df,KernelVersion:5.14.0-427.24.1.el9_4.x86_64,OSImage:Red Hat Enterprise Linux CoreOS 416.94.202407030122-0,ContainerRuntimeVersion:cri-o://1.29.6-3.rhaos4.16.gitfd433b7.el9,KubeletVersion:v1.29.6+aba1e8d,KubeProxyVersion:v1.29.6+aba1e8d,OperatingSystem:linux,Architecture:amd64,},Images:[]ContainerImage{ContainerImage{Names:[quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85],SizeBytes:1346706973,},ContainerImage{Names:[registry.redhat.io/odf4/cephcsi-rhel9@sha256:32251200ab1f9a15390236f6cfaeb8f2ef89e32616f3a44fe83254e0a104f71c registry.redhat.io/odf4/cephcsi-rhel9@sha256:ac0c3a8d86539bc4668e1a6de82e1f8439a1fbbb17a3b4102cabf078f021b41f],SizeBytes:1291394311,},ContainerImage{Names:[quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:a8d605d90d80c86b27e93eac023b67a95e72e19913e0b0e4db803737cf0a9ed5],SizeBytes:1222085412,},ContainerImage{Names:[quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:381b102d034f4404550d6392f62a744e45694e1b9a5b4f372b2a2caf9942592a],SizeBytes:826526256,},ContainerImage{Names:[quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:cdcd17ee9ae2152aad570bbee6a5fb66398ca68f1d4a0ed7b7cc807785a73bc1],SizeBytes:775216571,},ContainerImage{Names:[quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:b8068751688e54e209ad17e48b6db681d23a5716921ca42637f3443c4de01b0a],SizeBytes:713264783,},ContainerImage{Names:[quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:de5a5168f5b9a6275d315fa4b6ff46e0510a9c9a006723ab5f1ffb1ad963b3aa],SizeBytes:685300631,},ContainerImage{Names:[quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:598b8f29d07cf77edb243c77f34cd9173752006925534fc0d5fb8f4813a09dd6],SizeBytes:669239131,},ContainerImage{Names:[quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:f692e2703b699f7d23e4085599d80b8db1a57196d9a3b6a5a12bdeec493d2a63],SizeBytes:562105956,},ContainerImage{Names:[quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:e56420014ea17e1196a6a67aca991014137b6383d9acebe5e545206a6c709719],SizeBytes:492232521,},ContainerImage{Names:[quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:29ff7c37702007f0f2bb3104e82cfc0c494adaf314bb46053c46944358b98489],SizeBytes:491822725,},ContainerImage{Names:[quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:c5d7c70e5891265d8ac8c8145c99f950424365d9a2e803aa237acbbe690a2908],SizeBytes:482198618,},ContainerImage{Names:[quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:54d11ee63fe6bf444dcc6108c9e55b0c6992f81db88a6eece85f8fc00be46dce],SizeBytes:474695710,},ContainerImage{Names:[quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:f6a8f8e5b0c9b186512e95cfd740947bdd66584b86150b63ac7bc29b295c94bd],SizeBytes:464093510,},ContainerImage{Names:[quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:9866afa9304e442bf24111b49e6b9fd5f99cf17ead0787c93ae7250c62127cbc],SizeBytes:425311736,},ContainerImage{Names:[registry.redhat.io/openshift4/ose-csi-node-driver-registrar-rhel9@sha256:09a30b59c906ddc4604d70f18210bcebef1f90f8bf965422b0caba363cd88989 registry.redhat.io/openshift4/ose-csi-node-driver-registrar-rhel9@sha256:8921ba74fd32806cb89d558d3222a865908e180f66d5447ec2327e98939b2c3b],SizeBytes:420492495,},ContainerImage{Names:[quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:d333167cb5a71f5eba726d6090f022564a00923b845d0c75ca7d089d78620040],SizeBytes:414207900,},ContainerImage{Names:[quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:ec9d732a8ce4483c3f4dc2fc52cbc1a236746b161a6ea1d99be86bfb3167da6d],SizeBytes:410933600,},ContainerImage{Names:[quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:ed2ce2e2ea5332dada58c681e9a85ed89ad606e9f6619da2c040823cb6fe0e04],SizeBytes:400396983,},ContainerImage{Names:[registry.redhat.io/odf4/odf-csi-addons-sidecar-rhel9@sha256:0e565039b003b02e08f6cd80d0f603a568ae772ce1ba8784a3c54bf178b56164 registry.redhat.io/odf4/odf-csi-addons-sidecar-rhel9@sha256:162f35a85baabd9055c53717463c908247769a9bf617a4b457adf398d2e972be],SizeBytes:298431610,},},VolumesInUse:[],VolumesAttached:[]AttachedVolume{},Config:nil,},}
I0719 01:46:01.825424   37437 shared_informer.go:318] Caches are synced for egressservices_endpointslices
I0719 01:46:01.825433   37437 shared_informer.go:311] Waiting for caches to sync for egressservices_nodes
I0719 01:46:01.825437   37437 shared_informer.go:318] Caches are synced for egressservices_nodes
I0719 01:46:01.825442   37437 egressservice_zone.go:223] Repairing Egress Services
I0719 01:46:01.825413   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-storage/sts for endpointslice openshift-storage/sts-pnxx8 as it is not a known egress service
I0719 01:46:01.825449   37437 egressqos.go:1011] Finished syncing EgressQoS node 00-50-56-8a-fb-ea : 269.188µs
I0719 01:46:01.825455   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-storage/noobaa-db-pg for endpointslice openshift-storage/noobaa-db-pg-vzt5h as it is not a known egress service
I0719 01:46:01.825635   37437 model_client.go:381] Update operations generated as: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {ff451472-f1f3-4db7-bb61-f7f38984d502}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.825659   37437 transact.go:42] Configuring OVN: [{Op:update Table:Address_Set Row:map[addresses:{GoSet:[]}] Rows:[] Columns:[] Mutations:[] Timeout:<nil> Where:[where column _uuid == {ff451472-f1f3-4db7-bb61-f7f38984d502}] Until: Durable:<nil> Comment:<nil> Lock:<nil> UUID: UUIDName:}]
I0719 01:46:01.825868   37437 master_controller.go:86] Starting Admin Policy Based Route Controller
I0719 01:46:01.825879   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-storage/ocs-client-operator-webhook-server for endpointslice openshift-storage/ocs-client-operator-webhook-server-kc7q6 as it is not a known egress service
I0719 01:46:01.825892   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-controller-manager-operator/metrics for endpointslice openshift-controller-manager-operator/metrics-4mwgk as it is not a known egress service
I0719 01:46:01.825885   37437 external_controller.go:276] Starting Admin Policy Based Route Controller
I0719 01:46:01.825899   37437 egressservice_zone_node.go:110] Processing sync for Egress Service node 00-50-56-8a-39-a0
I0719 01:46:01.825907   37437 egressservice_zone_node.go:113] Finished syncing Egress Service node 00-50-56-8a-39-a0: 8.447µs
I0719 01:46:01.825917   37437 egressservice_zone_node.go:110] Processing sync for Egress Service node 00-50-56-8a-44-52
I0719 01:46:01.825921   37437 egressservice_zone_node.go:113] Finished syncing Egress Service node 00-50-56-8a-44-52: 4.813µs
I0719 01:46:01.825927   37437 egressservice_zone_node.go:110] Processing sync for Egress Service node 00-50-56-8a-5c-ec
I0719 01:46:01.825931   37437 egressservice_zone_node.go:113] Finished syncing Egress Service node 00-50-56-8a-5c-ec: 4.113µs
I0719 01:46:01.825935   37437 egressservice_zone_node.go:110] Processing sync for Egress Service node 00-50-56-8a-e1-e7
I0719 01:46:01.825939   37437 egressservice_zone_node.go:113] Finished syncing Egress Service node 00-50-56-8a-e1-e7: 4.048µs
I0719 01:46:01.825943   37437 egressservice_zone_node.go:110] Processing sync for Egress Service node 00-50-56-8a-f2-5d
I0719 01:46:01.825947   37437 egressservice_zone_node.go:113] Finished syncing Egress Service node 00-50-56-8a-f2-5d: 3.821µs
I0719 01:46:01.825952   37437 egressservice_zone_node.go:110] Processing sync for Egress Service node 00-50-56-8a-fb-ea
I0719 01:46:01.825956   37437 egressservice_zone_node.go:113] Finished syncing Egress Service node 00-50-56-8a-fb-ea: 4.418µs
I0719 01:46:01.825964   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-ingress-canary/ingress-canary for endpointslice openshift-ingress-canary/ingress-canary-fbx6f as it is not a known egress service
I0719 01:46:01.825969   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-monitoring/prometheus-k8s for endpointslice openshift-monitoring/prometheus-k8s-ct6b5 as it is not a known egress service
I0719 01:46:01.825976   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-storage/noobaa-syslog for endpointslice openshift-storage/noobaa-syslog-5bs7g as it is not a known egress service
I0719 01:46:01.825990   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-storage/ocs-metrics-exporter for endpointslice openshift-storage/ocs-metrics-exporter-tjh99 as it is not a known egress service
I0719 01:46:01.825996   37437 egressservice_zone_endpointslice.go:80] Ignoring updating default/kubernetes for endpointslice default/kubernetes as it is not a known egress service
I0719 01:46:01.826001   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-cluster-storage-operator/csi-snapshot-webhook for endpointslice openshift-cluster-storage-operator/csi-snapshot-webhook-b49qr as it is not a known egress service
I0719 01:46:01.826007   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-machine-api/control-plane-machine-set-operator for endpointslice openshift-machine-api/control-plane-machine-set-operator-tmtzm as it is not a known egress service
I0719 01:46:01.826013   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-machine-api/machine-api-operator for endpointslice openshift-machine-api/machine-api-operator-7kvp7 as it is not a known egress service
I0719 01:46:01.826021   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-machine-config-operator/machine-config-controller for endpointslice openshift-machine-config-operator/machine-config-controller-sgrzt as it is not a known egress service
I0719 01:46:01.826026   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-storage/rook-ceph-mon-b for endpointslice openshift-storage/rook-ceph-mon-b-w9r7f as it is not a known egress service
I0719 01:46:01.826032   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-console-operator/webhook for endpointslice openshift-console-operator/webhook-z8nzx as it is not a known egress service
I0719 01:46:01.826037   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-kube-scheduler/scheduler for endpointslice openshift-kube-scheduler/scheduler-52mp4 as it is not a known egress service
I0719 01:46:01.826042   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-kube-apiserver-operator/metrics for endpointslice openshift-kube-apiserver-operator/metrics-srmks as it is not a known egress service
I0719 01:46:01.826047   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-machine-api/baremetal-operator-webhook-service for endpointslice openshift-machine-api/baremetal-operator-webhook-service-hckjq as it is not a known egress service
I0719 01:46:01.826053   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-operator-lifecycle-manager/packageserver-service for endpointslice openshift-operator-lifecycle-manager/packageserver-service-hftrm as it is not a known egress service
I0719 01:46:01.826059   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-storage/ocs-client-operator-console for endpointslice openshift-storage/ocs-client-operator-console-2g5gb as it is not a known egress service
I0719 01:46:01.826065   37437 egressservice_zone_endpointslice.go:80] Ignoring updating kube-system/kubelet for endpointslice kube-system/kubelet-kqkgf as it is not a known egress service
I0719 01:46:01.826069   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-config-operator/metrics for endpointslice openshift-config-operator/metrics-wq82z as it is not a known egress service
I0719 01:46:01.826075   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-machine-api/machine-api-controllers for endpointslice openshift-machine-api/machine-api-controllers-n5jp6 as it is not a known egress service
I0719 01:46:01.826079   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-monitoring/prometheus-operator-admission-webhook for endpointslice openshift-monitoring/prometheus-operator-admission-webhook-w7qrg as it is not a known egress service
I0719 01:46:01.826084   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-operator-lifecycle-manager/catalog-operator-metrics for endpointslice openshift-operator-lifecycle-manager/catalog-operator-metrics-5d8px as it is not a known egress service
I0719 01:46:01.826092   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-storage/odf-operator-controller-manager-metrics-service for endpointslice openshift-storage/odf-operator-controller-manager-metrics-service-9jtln as it is not a known egress service
I0719 01:46:01.826097   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-storage/rook-ceph-mon-a for endpointslice openshift-storage/rook-ceph-mon-a-r6jzc as it is not a known egress service
I0719 01:46:01.826104   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-cloud-credential-operator/cco-metrics for endpointslice openshift-cloud-credential-operator/cco-metrics-bmjzk as it is not a known egress service
I0719 01:46:01.826108   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-machine-api/cluster-baremetal-operator-service for endpointslice openshift-machine-api/cluster-baremetal-operator-service-2pgb8 as it is not a known egress service
I0719 01:46:01.826114   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-monitoring/alertmanager-main for endpointslice openshift-monitoring/alertmanager-main-87ghb as it is not a known egress service
I0719 01:46:01.826119   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-dns/dns-default for endpointslice openshift-dns/dns-default-xjl6q as it is not a known egress service
I0719 01:46:01.826125   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-machine-api/metal3-image-customization-service for endpointslice openshift-machine-api/metal3-image-customization-service-wxhvr as it is not a known egress service
I0719 01:46:01.826130   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-insights/metrics for endpointslice openshift-insights/metrics-ndlfb as it is not a known egress service
I0719 01:46:01.826136   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-kube-scheduler-operator/metrics for endpointslice openshift-kube-scheduler-operator/metrics-8lznk as it is not a known egress service
I0719 01:46:01.826141   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-kube-storage-version-migrator-operator/metrics for endpointslice openshift-kube-storage-version-migrator-operator/metrics-w4hgz as it is not a known egress service
I0719 01:46:01.826148   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-machine-api/machine-api-operator-machine-webhook for endpointslice openshift-machine-api/machine-api-operator-machine-webhook-ddss9 as it is not a known egress service
I0719 01:46:01.826156   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-marketplace/community-operators for endpointslice openshift-marketplace/community-operators-xdmqg as it is not a known egress service
I0719 01:46:01.826163   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-monitoring/thanos-querier for endpointslice openshift-monitoring/thanos-querier-mb8rf as it is not a known egress service
I0719 01:46:01.826168   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-cluster-storage-operator/csi-snapshot-controller-operator-metrics for endpointslice openshift-cluster-storage-operator/csi-snapshot-controller-operator-metrics-l9n5w as it is not a known egress service
I0719 01:46:01.826174   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-cluster-version/cluster-version-operator for endpointslice openshift-cluster-version/cluster-version-operator-dppcg as it is not a known egress service
I0719 01:46:01.826179   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-machine-config-operator/machine-config-daemon for endpointslice openshift-machine-config-operator/machine-config-daemon-2ql4m as it is not a known egress service
I0719 01:46:01.826187   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-monitoring/monitoring-plugin for endpointslice openshift-monitoring/monitoring-plugin-5ccpt as it is not a known egress service
I0719 01:46:01.826192   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-multus/multus-admission-controller for endpointslice openshift-multus/multus-admission-controller-8w57k as it is not a known egress service
I0719 01:46:01.826198   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-operator-lifecycle-manager/package-server-manager-metrics for endpointslice openshift-operator-lifecycle-manager/package-server-manager-metrics-5xwsr as it is not a known egress service
I0719 01:46:01.826203   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-storage/noobaa-mgmt for endpointslice openshift-storage/noobaa-mgmt-nzfft as it is not a known egress service
I0719 01:46:01.826210   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-storage/rook-ceph-rgw-ocs-storagecluster-cephobjectstore for endpointslice openshift-storage/rook-ceph-rgw-ocs-storagecluster-cephobjectstore-lwdjm as it is not a known egress service
I0719 01:46:01.826215   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-cluster-node-tuning-operator/performance-addon-operator-service for endpointslice openshift-cluster-node-tuning-operator/performance-addon-operator-service-vqxgq as it is not a known egress service
I0719 01:46:01.826222   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-kube-controller-manager-operator/metrics for endpointslice openshift-kube-controller-manager-operator/metrics-mth4w as it is not a known egress service
I0719 01:46:01.826228   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-storage/ux-backend-proxy for endpointslice openshift-storage/ux-backend-proxy-zfx67 as it is not a known egress service
I0719 01:46:01.826234   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-machine-api/machine-api-operator-webhook for endpointslice openshift-machine-api/machine-api-operator-webhook-24pjb as it is not a known egress service
I0719 01:46:01.826238   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-network-diagnostics/network-check-target for endpointslice openshift-network-diagnostics/network-check-target-hjwlf as it is not a known egress service
I0719 01:46:01.826243   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-kube-apiserver/apiserver for endpointslice openshift-kube-apiserver/apiserver-q98kb as it is not a known egress service
I0719 01:46:01.826248   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-machine-api/cluster-autoscaler-operator for endpointslice openshift-machine-api/cluster-autoscaler-operator-rqwv9 as it is not a known egress service
I0719 01:46:01.826252   37437 default_network_controller.go:572] Completing all the Watchers took 86.893793ms
I0719 01:46:01.826266   37437 default_network_controller.go:576] Starting unidling controllers
I0719 01:46:01.826276   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-monitoring/node-exporter-7m7sg
I0719 01:46:01.826288   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-cloud-controller-manager
I0719 01:46:01.826302   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-config-operator
I0719 01:46:01.826308   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: kube-node-lease
I0719 01:46:01.826312   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-cloud-network-config-controller
I0719 01:46:01.826314   37437 unidle.go:45] Registering OVN SB ControllerEvent handler
I0719 01:46:01.826319   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-cluster-csi-drivers
I0719 01:46:01.826322   37437 unidle.go:62] Populating Initial ContollerEvent events
I0719 01:46:01.826324   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-cluster-machine-approver
I0719 01:46:01.826329   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-kni-infra
I0719 01:46:01.826334   37437 unidle.go:78] Setting up event handlers for services
I0719 01:46:01.826292   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-multus/network-metrics-daemon-t4g2p
I0719 01:46:01.826334   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-kube-controller-manager-operator
I0719 01:46:01.826398   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-network-diagnostics/network-check-source-b89b7bb96-lpzlv
I0719 01:46:01.826403   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-dns-operator
I0719 01:46:01.826408   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/rook-ceph-exporter-00-50-56-8a-e1-e7-558dfbd955-jzh65
I0719 01:46:01.826411   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-insights
I0719 01:46:01.826416   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-monitoring/thanos-querier-68bf686489-9cctf
I0719 01:46:01.826419   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-kube-scheduler-operator
I0719 01:46:01.826254   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-machine-api/cluster-baremetal-webhook-service for endpointslice openshift-machine-api/cluster-baremetal-webhook-service-8l5bq as it is not a known egress service
I0719 01:46:01.826427   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: kube-public
I0719 01:46:01.826432   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-cloud-platform-infra
I0719 01:46:01.826423   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-network-diagnostics/network-check-target-h9cbr
I0719 01:46:01.826438   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-cluster-version
I0719 01:46:01.826443   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-ingress-canary
I0719 01:46:01.826443   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-image-registry/node-ca-wgn2l
I0719 01:46:01.826448   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-vsphere-infra
I0719 01:46:01.826453   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-etcd-operator
I0719 01:46:01.826458   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: kube-system
I0719 01:46:01.826462   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-authentication-operator
I0719 01:46:01.826467   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-host-network
I0719 01:46:01.826471   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-infra
I0719 01:46:01.826473   37437 network_attach_def_controller.go:134] Starting network-controller-manager NAD controller
I0719 01:46:01.826431   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-apiserver-operator/metrics for endpointslice openshift-apiserver-operator/metrics-tf6bm as it is not a known egress service
I0719 01:46:01.826488   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kube-apiserver/revision-pruner-8-00-50-56-8a-5c-ec
I0719 01:46:01.826476   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-machine-config-operator
I0719 01:46:01.826498   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-5c-ec
I0719 01:46:01.826499   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-ingress-operator
I0719 01:46:01.826505   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-e1-e7
I0719 01:46:01.826505   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-monitoring
I0719 01:46:01.826511   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-ovn-kubernetes/ovnkube-control-plane-58975cd9fd-mz4pv
I0719 01:46:01.826512   37437 shared_informer.go:311] Waiting for caches to sync for network-controller-manager
I0719 01:46:01.826517   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/odf-console-b7ccd85c5-84cnv
I0719 01:46:01.826512   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-node
I0719 01:46:01.826525   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-dns/node-resolver-nsvs6
I0719 01:46:01.826531   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kube-scheduler/openshift-kube-scheduler-guard-00-50-56-8a-5c-ec
I0719 01:46:01.826532   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-oauth-apiserver
I0719 01:46:01.826537   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-marketplace/redhat-marketplace-hbf7g
I0719 01:46:01.826540   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-ovirt-infra
I0719 01:46:01.826544   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-multus/multus-25bkq
I0719 01:46:01.826550   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-multus/multus-ltqfr
I0719 01:46:01.826492   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-etcd-operator/metrics for endpointslice openshift-etcd-operator/metrics-4f4kg as it is not a known egress service
I0719 01:46:01.826557   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-network-operator/network-operator-6967d44d7-4wwpm
I0719 01:46:01.826560   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-local-storage/local-storage-diskmaker-metrics for endpointslice openshift-local-storage/local-storage-diskmaker-metrics-lpb6n as it is not a known egress service
I0719 01:46:01.826562   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-cluster-node-tuning-operator/tuned-5pn2c
I0719 01:46:01.826545   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-storage
I0719 01:46:01.826575   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-multus/network-metrics-daemon-hxzdd
I0719 01:46:01.826579   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-machine-config-operator/machine-config-operator for endpointslice openshift-machine-config-operator/machine-config-operator-99xcj as it is not a known egress service
I0719 01:46:01.826586   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-marketplace/certified-operators for endpointslice openshift-marketplace/certified-operators-52cbv as it is not a known egress service
I0719 01:46:01.826586   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-image-registry/image-pruner-28689120-2bnxj
I0719 01:46:01.826577   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-apiserver
I0719 01:46:01.826604   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-console
I0719 01:46:01.826605   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kni-infra/coredns-00-50-56-8a-fb-ea
I0719 01:46:01.826611   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-console-operator
I0719 01:46:01.826616   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-kube-storage-version-migrator
I0719 01:46:01.826619   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-monitoring/node-exporter-7xrvj
I0719 01:46:01.826622   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-user-workload-monitoring
I0719 01:46:01.826627   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-cloud-credential-operator
I0719 01:46:01.826628   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-multus/network-metrics-daemon-bqt8s
I0719 01:46:01.826632   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-cluster-storage-operator
I0719 01:46:01.826637   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-console-user-settings
I0719 01:46:01.826639   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-marketplace/marketplace-operator-59c7f5b7bd-8pd2c
I0719 01:46:01.826642   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-kube-controller-manager
I0719 01:46:01.826642   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-marketplace/marketplace-operator-metrics for endpointslice openshift-marketplace/marketplace-operator-metrics-jvcsw as it is not a known egress service
I0719 01:46:01.826647   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-local-storage
I0719 01:46:01.826648   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-cluster-storage-operator/csi-snapshot-controller-794ff44f88-5jz8j
I0719 01:46:01.826652   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-openstack-infra
I0719 01:46:01.826657   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-authentication
I0719 01:46:01.826662   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-cloud-controller-manager-operator
I0719 01:46:01.826666   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-kube-apiserver-operator
I0719 01:46:01.826666   37437 reflector.go:289] Starting reflector *v1.NetworkAttachmentDefinition (0s) from github.com/k8snetworkplumbingwg/network-attachment-definition-client/pkg/client/informers/externalversions/factory.go:117
I0719 01:46:01.826671   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-marketplace
I0719 01:46:01.826674   37437 reflector.go:325] Listing and watching *v1.NetworkAttachmentDefinition from github.com/k8snetworkplumbingwg/network-attachment-definition-client/pkg/client/informers/externalversions/factory.go:117
I0719 01:46:01.826676   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-operators
I0719 01:46:01.826681   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: assisted-installer
I0719 01:46:01.826685   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-kube-scheduler
I0719 01:46:01.826690   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-kube-storage-version-migrator-operator
I0719 01:46:01.826694   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-network-node-identity
I0719 01:46:01.826698   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-route-controller-manager
I0719 01:46:01.826703   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-service-ca-operator
I0719 01:46:01.826707   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: default
I0719 01:46:01.826650   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-route-controller-manager/route-controller-manager for endpointslice openshift-route-controller-manager/route-controller-manager-cnsjv as it is not a known egress service
I0719 01:46:01.826711   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-cluster-node-tuning-operator
I0719 01:46:01.826717   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-config-managed
I0719 01:46:01.826721   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-etcd
I0719 01:46:01.826657   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kni-infra/keepalived-00-50-56-8a-39-a0
I0719 01:46:01.826726   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-multus
I0719 01:46:01.826731   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-ovn-kubernetes
I0719 01:46:01.826732   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/rook-ceph-exporter-00-50-56-8a-f2-5d-785d485f5d-v5k84
I0719 01:46:01.826736   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-controller-manager
I0719 01:46:01.826741   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-cloud-controller-manager-operator/cluster-cloud-controller-manager-operator-7f55545d59-r8j8z
I0719 01:46:01.826749   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-multus/multus-2nb4x
I0719 01:46:01.826756   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-network-operator/iptables-alerter-6s78n
I0719 01:46:01.826763   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-network-operator/iptables-alerter-b72gh
I0719 01:46:01.826769   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-operator-lifecycle-manager/packageserver-6bf7d58455-gh44f
I0719 01:46:01.826777   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kube-storage-version-migrator-operator/kube-storage-version-migrator-operator-75d5d9b9f8-lj6w5
I0719 01:46:01.826787   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-etcd/etcd-guard-00-50-56-8a-39-a0
I0719 01:46:01.826796   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kni-infra/keepalived-00-50-56-8a-44-52
I0719 01:46:01.826805   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-machine-config-operator/machine-config-daemon-kgwdc
I0719 01:46:01.826815   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-machine-config-operator/machine-config-server-968nk
I0719 01:46:01.826824   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-monitoring/metrics-server-7d47f4cbc-5qp84
I0719 01:46:01.826834   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-monitoring/node-exporter-9mlmj
I0719 01:46:01.826843   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-monitoring/prometheus-operator-admission-webhook-67db68b49d-w8jqx
I0719 01:46:01.826851   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-cluster-node-tuning-operator/tuned-cjc5f
I0719 01:46:01.826719   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-apiserver/api for endpointslice openshift-apiserver/api-tkdf5 as it is not a known egress service
I0719 01:46:01.826872   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-authentication/oauth-openshift for endpointslice openshift-authentication/oauth-openshift-mbrq8 as it is not a known egress service
I0719 01:46:01.826884   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-cluster-storage-operator/cluster-storage-operator-metrics for endpointslice openshift-cluster-storage-operator/cluster-storage-operator-metrics-rl7x6 as it is not a known egress service
I0719 01:46:01.826741   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-machine-api
I0719 01:46:01.826918   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-network-operator
I0719 01:46:01.826935   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-service-ca
I0719 01:46:01.826945   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift
I0719 01:46:01.826954   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-controller-manager-operator
I0719 01:46:01.826963   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-network-diagnostics
I0719 01:46:01.826972   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-operator-lifecycle-manager
I0719 01:46:01.826980   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-apiserver-operator
I0719 01:46:01.827000   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-config
I0719 01:46:01.827007   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-dns
I0719 01:46:01.827014   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-image-registry
I0719 01:46:01.827019   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-ingress
I0719 01:46:01.827024   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-cluster-samples-operator
I0719 01:46:01.827029   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-kube-apiserver
I0719 01:46:01.827034   37437 external_controller_namespace.go:16] APB queuing policies: map[] for namespace: openshift-nutanix-infra
I0719 01:46:01.826859   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-route-controller-manager/route-controller-manager-676cdfdbc8-t227m
I0719 01:46:01.827045   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-network-operator/iptables-alerter-nh7z8
I0719 01:46:01.827050   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-etcd/etcd-00-50-56-8a-5c-ec
I0719 01:46:01.827056   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-machine-config-operator/machine-config-controller-b886dd6cb-6kjkp
I0719 01:46:01.827061   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-dns/node-resolver-djq2g
I0719 01:46:01.827066   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-ingress-canary/ingress-canary-lsx7x
I0719 01:46:01.827071   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-multus/multus-additional-cni-plugins-b5t42
I0719 01:46:01.827075   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-multus/multus-additional-cni-plugins-pjk5m
I0719 01:46:01.827081   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-multus/multus-additional-cni-plugins-qdrk9
I0719 01:46:01.827087   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/csi-rbdplugin-xgkn6
I0719 01:46:01.827092   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/rook-ceph-crashcollector-00-50-56-8a-e1-e7-6c5dcb6f44-8z5np
I0719 01:46:01.827097   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-image-registry/cluster-image-registry-operator-656868857f-f94pq
I0719 01:46:01.827102   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-dns/node-resolver-dpn9t
I0719 01:46:01.827108   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-5c-ec
I0719 01:46:01.827113   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-network-diagnostics/network-check-target-gc5jl
I0719 01:46:01.827119   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-operator-lifecycle-manager/olm-operator-59f98dcc4-xqd8j
I0719 01:46:01.827124   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/csi-cephfsplugin-provisioner-585f89d895-2b4wk
I0719 01:46:01.827129   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/noobaa-db-pg-0
I0719 01:46:01.827134   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-cluster-version/cluster-version-operator-78b5d9c79d-znx2p
I0719 01:46:01.827139   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kube-controller-manager-operator/kube-controller-manager-operator-85c67fcb8d-fg9j7
I0719 01:46:01.827144   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-monitoring/prometheus-operator-admission-webhook-67db68b49d-wbfqq
I0719 01:46:01.827149   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-controller-manager-operator/openshift-controller-manager-operator-cf8f9956c-x6xn5
I0719 01:46:01.827154   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-image-registry/node-ca-tvhtl
I0719 01:46:01.827159   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-44-52
I0719 01:46:01.827164   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-network-node-identity/network-node-identity-z7b9j
I0719 01:46:01.827169   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/csi-addons-controller-manager-6d78957fdf-gs4tk
I0719 01:46:01.827174   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-console/downloads-6967878986-76phj
I0719 01:46:01.827178   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kube-apiserver/kube-apiserver-00-50-56-8a-39-a0
I0719 01:46:01.827183   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-multus/multus-47wxd
I0719 01:46:01.827188   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/csi-rbdplugin-xkw8r
I0719 01:46:01.827193   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/ocs-client-operator-controller-manager-846f549988-v288f
I0719 01:46:01.827198   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/rook-ceph-osd-1-6db96b64cc-nw82d
I0719 01:46:01.827203   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kni-infra/keepalived-00-50-56-8a-5c-ec
I0719 01:46:01.826893   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-console/downloads for endpointslice openshift-console/downloads-2lj5d as it is not a known egress service
I0719 01:46:01.827208   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-operator-lifecycle-manager/packageserver-6bf7d58455-k8qkk
I0719 01:46:01.827214   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kube-storage-version-migrator/migrator-7fc5dd675b-tfjhl
I0719 01:46:01.827219   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-39-a0
I0719 01:46:01.827224   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-machine-config-operator/machine-config-daemon-p677g
I0719 01:46:01.827230   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-monitoring/node-exporter-nvqsf
I0719 01:46:01.827234   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-operator-lifecycle-manager/package-server-manager-74bbc7c476-4555r
I0719 01:46:01.827239   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/csi-cephfsplugin-provisioner-585f89d895-ddwtl
I0719 01:46:01.827244   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-5c-ec
I0719 01:46:01.827248   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-multus/multus-additional-cni-plugins-2kgg5
I0719 01:46:01.827253   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/csi-cephfsplugin-s29g7
I0719 01:46:01.827258   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-config-operator/openshift-config-operator-59dc875ddb-rnq74
I0719 01:46:01.827262   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/rook-ceph-mds-ocs-storagecluster-cephfilesystem-b-c4dc5cd7zkffj
I0719 01:46:01.827267   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-service-ca-operator/service-ca-operator-86c8d4bbfd-w2qxx
I0719 01:46:01.827272   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-machine-config-operator/machine-config-daemon-qpmqf
I0719 01:46:01.827279   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-operator-lifecycle-manager/collect-profiles-28689225-j8wtn
I0719 01:46:01.827219   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-kube-controller-manager/kube-controller-manager for endpointslice openshift-kube-controller-manager/kube-controller-manager-5j6w4 as it is not a known egress service
I0719 01:46:01.827288   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-ovn-kubernetes/ovnkube-node-568wp
I0719 01:46:01.827296   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-monitoring/metrics-server for endpointslice openshift-monitoring/metrics-server-c5g9h as it is not a known egress service
I0719 01:46:01.827298   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/ocs-metrics-exporter-84f9766477-r8fxs
I0719 01:46:01.827312   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-storage/csi-addons-controller-manager-metrics-service for endpointslice openshift-storage/csi-addons-controller-manager-metrics-service-48rpl as it is not a known egress service
I0719 01:46:01.827324   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/rook-ceph-mon-a-6dc9d78597-7ttc9
I0719 01:46:01.827333   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kube-controller-manager/kube-controller-manager-guard-00-50-56-8a-5c-ec
I0719 01:46:01.827338   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-machine-api/ironic-proxy-sn8n9
I0719 01:46:01.827344   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-machine-api/metal3-599ff8f4b7-vntm7
I0719 01:46:01.827351   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-marketplace/redhat-operators-mm6k4
I0719 01:46:01.827356   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-monitoring/alertmanager-main-0
I0719 01:46:01.827361   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-network-diagnostics/network-check-target-jhhzw
I0719 01:46:01.827366   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kube-scheduler/openshift-kube-scheduler-guard-00-50-56-8a-39-a0
I0719 01:46:01.827374   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-cluster-node-tuning-operator/tuned-f4pbt
I0719 01:46:01.827383   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-local-storage/diskmaker-manager-wj2h7
I0719 01:46:01.827393   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-machine-config-operator/machine-config-server-j8kbc
I0719 01:46:01.827325   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-storage/noobaa-operator-service for endpointslice openshift-storage/noobaa-operator-service-cmrbr as it is not a known egress service
I0719 01:46:01.827403   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/csi-rbdplugin-provisioner-5dcc45fbf4-v5l2c
I0719 01:46:01.827410   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-authentication/oauth-openshift-7c9d9dfc8c-ddj6k
I0719 01:46:01.827414   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-apiserver/check-endpoints for endpointslice openshift-apiserver/check-endpoints-8zd7b as it is not a known egress service
I0719 01:46:01.827415   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-console/downloads-6967878986-hpkbw
I0719 01:46:01.827434   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-monitoring/telemeter-client-7b74cd774c-fg6lz
I0719 01:46:01.827441   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-multus/multus-mqkdb
I0719 01:46:01.827446   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-console-operator/console-operator-76c8786869-jr6r2
I0719 01:46:01.827451   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/ocs-operator-5567c4fdb4-8b9zr
I0719 01:46:01.827456   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-console-operator/console-conversion-webhook-664b4df6f5-nq9pd
I0719 01:46:01.827461   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-ingress-canary/ingress-canary-lrjr5
I0719 01:46:01.827466   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-machine-api/machine-api-operator-5cb7d5868-9p8wr
I0719 01:46:01.827472   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-multus/multus-sv782
I0719 01:46:01.827476   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-monitoring/kube-state-metrics-589b9987d-ck4ch
I0719 01:46:01.827482   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-network-operator/iptables-alerter-m44lf
I0719 01:46:01.827485   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-authentication-operator/metrics for endpointslice openshift-authentication-operator/metrics-l845z as it is not a known egress service
I0719 01:46:01.827487   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-dns/dns-default-wn5nz
I0719 01:46:01.827492   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-storage/rook-ceph-mon-c for endpointslice openshift-storage/rook-ceph-mon-c-x5m6v as it is not a known egress service
I0719 01:46:01.827496   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kube-apiserver/kube-apiserver-guard-00-50-56-8a-39-a0
I0719 01:46:01.827502   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-machine-api/metal3-state for endpointslice openshift-machine-api/metal3-state-5mc4x as it is not a known egress service
I0719 01:46:01.827504   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-machine-api/ironic-proxy-6zm7s
I0719 01:46:01.827508   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-marketplace/redhat-marketplace for endpointslice openshift-marketplace/redhat-marketplace-gj9p9 as it is not a known egress service
I0719 01:46:01.827511   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-operator-lifecycle-manager/collect-profiles-28689210-mbs94
I0719 01:46:01.827518   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-marketplace/redhat-operators for endpointslice openshift-marketplace/redhat-operators-68r7h as it is not a known egress service
I0719 01:46:01.827522   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-dns/dns-default-5hh4c
I0719 01:46:01.827526   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-storage/rook-ceph-exporter for endpointslice openshift-storage/rook-ceph-exporter-48bs8 as it is not a known egress service
I0719 01:46:01.827530   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-controller-manager/controller-manager-5c7f9f9d47-c74xp
I0719 01:46:01.827536   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-storage/s3 for endpointslice openshift-storage/s3-nww4d as it is not a known egress service
I0719 01:46:01.827537   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-apiserver/apiserver-7d9bbd465d-7pbl8
I0719 01:46:01.827544   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-console-operator/metrics for endpointslice openshift-console-operator/metrics-qzgbg as it is not a known egress service
I0719 01:46:01.827547   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kube-apiserver/kube-apiserver-00-50-56-8a-5c-ec
I0719 01:46:01.827551   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-dns-operator/metrics for endpointslice openshift-dns-operator/metrics-4scxm as it is not a known egress service
I0719 01:46:01.827556   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-39-a0
I0719 01:46:01.827561   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-cluster-storage-operator/csi-snapshot-controller-operator-bb8d9765b-b24f6
I0719 01:46:01.827567   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-etcd/etcd-00-50-56-8a-44-52
I0719 01:46:01.827572   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kube-apiserver-operator/kube-apiserver-operator-55dc5cdcf9-p4csg
I0719 01:46:01.827577   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kube-scheduler/revision-pruner-6-00-50-56-8a-39-a0
I0719 01:46:01.827582   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-monitoring/prometheus-operator-848d66f7-nx2v2
I0719 01:46:01.827587   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/rook-ceph-mon-c-5b4c4697fb-8w28d
I0719 01:46:01.827592   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-cluster-storage-operator/csi-snapshot-webhook-85b445968-78v7q
I0719 01:46:01.827596   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-dns/dns-default-24pdt
I0719 01:46:01.827601   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-39-a0
I0719 01:46:01.827606   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-machine-config-operator/machine-config-operator-7fc5c776cc-r6wsl
I0719 01:46:01.827611   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-monitoring/prometheus-k8s-1
I0719 01:46:01.827616   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-oauth-apiserver/apiserver-86f656c4dd-2pxdq
I0719 01:46:01.827620   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-oauth-apiserver/apiserver-86f656c4dd-g82dw
I0719 01:46:01.827625   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-cluster-storage-operator/csi-snapshot-webhook-85b445968-9dpmd
I0719 01:46:01.827630   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-cluster-samples-operator/cluster-samples-operator-6b95974b98-cxvvt
I0719 01:46:01.827637   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-etcd/etcd-guard-00-50-56-8a-5c-ec
I0719 01:46:01.827642   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kni-infra/coredns-00-50-56-8a-39-a0
I0719 01:46:01.827647   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-cluster-machine-approver/machine-approver-5bf6544664-79krt
I0719 01:46:01.827653   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-monitoring/prometheus-k8s-0
I0719 01:46:01.827658   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-multus/network-metrics-daemon-gqqpq
I0719 01:46:01.827663   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-monitoring/node-exporter-s77zj
I0719 01:46:01.827668   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-ingress-canary/ingress-canary-zxwrq
I0719 01:46:01.827673   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-ingress/router-default-54fb8ffc6b-hhdt2
I0719 01:46:01.827678   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kube-apiserver/revision-pruner-8-00-50-56-8a-39-a0
I0719 01:46:01.827682   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-network-diagnostics/network-check-target-vltnw
I0719 01:46:01.827687   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-network-node-identity/network-node-identity-tzcq8
I0719 01:46:01.827556   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-oauth-apiserver/api for endpointslice openshift-oauth-apiserver/api-hpbm5 as it is not a known egress service
I0719 01:46:01.827692   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-console/console-f7dbc9784-cj9wp
I0719 01:46:01.827698   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-dns/node-resolver-r7f9m
I0719 01:46:01.827703   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-local-storage/diskmaker-manager-vrh5h
I0719 01:46:01.827708   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-ovn-kubernetes/ovnkube-node-62ccc
I0719 01:46:01.827713   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-cloud-credential-operator/cloud-credential-operator-6488fd5f9b-jkdg2
I0719 01:46:01.827720   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kni-infra/coredns-00-50-56-8a-5c-ec
I0719 01:46:01.827728   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-multus/multus-admission-controller-5cc499c6f4-bngv4
I0719 01:46:01.827735   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-apiserver-operator/openshift-apiserver-operator-84fc88fd69-mqjqx
I0719 01:46:01.827743   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kni-infra/coredns-00-50-56-8a-e1-e7
I0719 01:46:01.827698   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-controller-manager/controller-manager for endpointslice openshift-controller-manager/controller-manager-cncjz as it is not a known egress service
I0719 01:46:01.827773   37437 egressservice_zone_endpointslice.go:80] Ignoring updating openshift-ingress/router-internal-default for endpointslice openshift-ingress/router-internal-default-526gk as it is not a known egress service
I0719 01:46:01.827819   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kube-apiserver/kube-apiserver-00-50-56-8a-44-52
I0719 01:46:01.827909   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-multus/multus-admission-controller-5cc499c6f4-jtjqw
I0719 01:46:01.827923   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/noobaa-endpoint-6ddf6bb6b-jmx4r
I0719 01:46:01.827952   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-cluster-node-tuning-operator/cluster-node-tuning-operator-68cc9c9cf9-6brm7
I0719 01:46:01.827966   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-dns/dns-default-rj9px
I0719 01:46:01.827972   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-image-registry/node-ca-kqt8n
I0719 01:46:01.827977   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kni-infra/keepalived-00-50-56-8a-fb-ea
I0719 01:46:01.827993   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-monitoring/monitoring-plugin-6f457fd4b8-6wb4z
I0719 01:46:01.827999   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-cluster-node-tuning-operator/tuned-x2svx
I0719 01:46:01.828004   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-cluster-node-tuning-operator/tuned-hpvxx
I0719 01:46:01.828009   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kni-infra/haproxy-00-50-56-8a-44-52
I0719 01:46:01.828013   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-machine-config-operator/machine-config-server-zwkfw
I0719 01:46:01.828018   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-network-operator/iptables-alerter-m6v49
I0719 01:46:01.828023   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-authentication/oauth-openshift-7c9d9dfc8c-lxcsb
I0719 01:46:01.828027   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-monitoring/alertmanager-main-1
I0719 01:46:01.828032   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/csi-cephfsplugin-b549v
I0719 01:46:01.828038   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-cluster-node-tuning-operator/tuned-9mzgb
I0719 01:46:01.828043   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-network-diagnostics/network-check-target-8gshd
I0719 01:46:01.828048   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-machine-api/machine-api-controllers-59cdf7bd97-7l7pt
I0719 01:46:01.828053   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-route-controller-manager/route-controller-manager-676cdfdbc8-t6rhq
I0719 01:46:01.828058   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-local-storage/local-storage-operator-6486fccd57-h47kh
I0719 01:46:01.828063   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-machine-api/cluster-autoscaler-operator-56cd7bcc4-8t6ns
I0719 01:46:01.828067   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-machine-config-operator/machine-config-daemon-vllgq
I0719 01:46:01.828073   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-marketplace/certified-operators-j5jtq
I0719 01:46:01.828125   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-network-node-identity/network-node-identity-xlk9z
I0719 01:46:01.828142   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-operator-lifecycle-manager/catalog-operator-7d75668bc4-sjfjn
I0719 01:46:01.828149   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-ovn-kubernetes/ovnkube-control-plane-58975cd9fd-7wmvb
I0719 01:46:01.828155   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/ux-backend-server-6444f844bf-whf8g
I0719 01:46:01.828160   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kni-infra/coredns-00-50-56-8a-44-52
I0719 01:46:01.828165   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-dns/dns-default-zwbjg
I0719 01:46:01.828169   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kube-apiserver/kube-apiserver-guard-00-50-56-8a-5c-ec
I0719 01:46:01.828174   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-monitoring/openshift-state-metrics-6bb8db76bd-2wlhc
I0719 01:46:01.828179   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-dns/dns-default-qzrlq
I0719 01:46:01.828184   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-local-storage/diskmaker-manager-2zrc6
I0719 01:46:01.828190   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-cluster-storage-operator/cluster-storage-operator-6c5864c5b-kgzzc
I0719 01:46:01.828195   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-ingress/router-default-54fb8ffc6b-kgb2v
I0719 01:46:01.828200   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-machine-api/metal3-baremetal-operator-6fd5ccf9-9p448
I0719 01:46:01.828205   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-fb-ea
I0719 01:46:01.828210   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/csi-rbdplugin-b6gdm
I0719 01:46:01.828214   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/noobaa-core-0
I0719 01:46:01.828219   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-controller-manager/controller-manager-5c7f9f9d47-thph4
I0719 01:46:01.828224   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/odf-operator-controller-manager-78d57f457c-tbwjf
I0719 01:46:01.828229   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-network-operator/iptables-alerter-wxl7s
I0719 01:46:01.828234   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kni-infra/haproxy-00-50-56-8a-5c-ec
I0719 01:46:01.828239   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/csi-cephfsplugin-5fvh4
I0719 01:46:01.828243   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-dns/node-resolver-tjmrc
I0719 01:46:01.828248   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-monitoring/node-exporter-gbsmf
I0719 01:46:01.828253   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-network-diagnostics/network-check-target-dj4vt
I0719 01:46:01.828259   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/rook-ceph-operator-cf758864f-c6zl8
I0719 01:46:01.828266   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-dns/node-resolver-bf5zv
I0719 01:46:01.828273   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-etcd/revision-pruner-9-00-50-56-8a-39-a0
I0719 01:46:01.828280   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-etcd/revision-pruner-9-00-50-56-8a-5c-ec
I0719 01:46:01.828288   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kni-infra/keepalived-00-50-56-8a-e1-e7
I0719 01:46:01.828296   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-monitoring/thanos-querier-68bf686489-qbcjs
I0719 01:46:01.828303   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-multus/network-metrics-daemon-7ttpg
I0719 01:46:01.828311   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-operator-lifecycle-manager/collect-profiles-28689195-w9664
I0719 01:46:01.828319   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-cluster-storage-operator/csi-snapshot-controller-794ff44f88-7cksj
I0719 01:46:01.828327   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-authentication-operator/authentication-operator-68795c8768-8rvtz
I0719 01:46:01.828335   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-image-registry/node-ca-lfxb8
I0719 01:46:01.828344   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-ingress-operator/ingress-operator-5cc96867f4-pdgdd
I0719 01:46:01.828356   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-machine-api/metal3-image-customization-5f9d4c754c-5v2p8
I0719 01:46:01.828364   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-machine-config-operator/machine-config-daemon-r8bgv
I0719 01:46:01.828369   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-monitoring/metrics-server-7d47f4cbc-dqrxk
I0719 01:46:01.828374   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-apiserver/apiserver-7d9bbd465d-6cgbw
I0719 01:46:01.828379   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/rook-ceph-crashcollector-00-50-56-8a-f2-5d-5bfb656d8f-tvtpr
I0719 01:46:01.828384   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/rook-ceph-mgr-a-6fddb5fd95-mr2cn
I0719 01:46:01.828388   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/rook-ceph-mgr-b-779b65ccb6-29sz4
I0719 01:46:01.828393   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-service-ca/service-ca-6dbc4646f9-6q769
I0719 01:46:01.828397   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kni-infra/coredns-00-50-56-8a-f2-5d
I0719 01:46:01.828402   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kni-infra/haproxy-00-50-56-8a-39-a0
I0719 01:46:01.828407   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kube-scheduler-operator/openshift-kube-scheduler-operator-555f7bb8bc-4vw77
I0719 01:46:01.828412   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/noobaa-operator-bf7774fd8-zskvp
I0719 01:46:01.828417   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-image-registry/node-ca-986d7
I0719 01:46:01.828422   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kube-controller-manager/kube-controller-manager-00-50-56-8a-44-52
I0719 01:46:01.828427   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-machine-api/ironic-proxy-k9xzh
I0719 01:46:01.828432   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-multus/multus-additional-cni-plugins-tpn87
I0719 01:46:01.828436   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-ovn-kubernetes/ovnkube-node-5bqnj
I0719 01:46:01.828441   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-ovn-kubernetes/ovnkube-node-mqh7r
I0719 01:46:01.828446   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-image-registry/node-ca-sq7qk
I0719 01:46:01.828451   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-insights/insights-operator-586b65d57b-7rk2w
I0719 01:46:01.828456   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-dns-operator/dns-operator-5fc6bf9796-jgj7s
I0719 01:46:01.828461   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-ovn-kubernetes/ovnkube-node-9h9qr
I0719 01:46:01.828466   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-machine-api/cluster-baremetal-operator-5fb6f8f7d4-ltc5l
I0719 01:46:01.828471   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-marketplace/community-operators-wgnxc
I0719 01:46:01.828476   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-monitoring/cluster-monitoring-operator-b4b4bcf9f-d4xhg
I0719 01:46:01.828480   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/ocs-client-operator-console-6fdbfcd95-jhcss
I0719 01:46:01.828485   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/rook-ceph-mds-ocs-storagecluster-cephfilesystem-a-8679ddf7kqp98
I0719 01:46:01.828490   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kube-controller-manager/kube-controller-manager-guard-00-50-56-8a-39-a0
I0719 01:46:01.828495   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kni-infra/keepalived-00-50-56-8a-f2-5d
I0719 01:46:01.828501   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-etcd/etcd-00-50-56-8a-39-a0
I0719 01:46:01.828506   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/csi-rbdplugin-provisioner-5dcc45fbf4-9svs4
I0719 01:46:01.828513   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/rook-ceph-rgw-ocs-storagecluster-cephobjectstore-a-766774cx8zqw
I0719 01:46:01.828520   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-monitoring/monitoring-plugin-6f457fd4b8-pqp4m
I0719 01:46:01.828529   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-ovn-kubernetes/ovnkube-node-7pmvf
I0719 01:46:01.828538   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kube-scheduler/openshift-kube-scheduler-00-50-56-8a-44-52
I0719 01:46:01.828548   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-machine-config-operator/machine-config-daemon-4kr96
I0719 01:46:01.828557   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-etcd-operator/etcd-operator-6c7489b895-5tql8
I0719 01:46:01.828566   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-kube-scheduler/revision-pruner-6-00-50-56-8a-5c-ec
I0719 01:46:01.828576   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-machine-api/control-plane-machine-set-operator-77bcc698b6-wvkdb
I0719 01:46:01.828585   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-machine-config-operator/kube-rbac-proxy-crio-00-50-56-8a-f2-5d
I0719 01:46:01.828594   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-multus/multus-additional-cni-plugins-rtmj7
I0719 01:46:01.828603   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-multus/network-metrics-daemon-fslb2
I0719 01:46:01.828612   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-console/console-c675c654b-rw8cg
I0719 01:46:01.828620   37437 external_controller_pod.go:21] APB queuing policies: map[] for pod: openshift-storage/rook-ceph-osd-0-6d5dbb5f-24hfr
I0719 01:46:01.828791   37437 reflector.go:351] Caches populated for *v1.NetworkAttachmentDefinition from github.com/k8snetworkplumbingwg/network-attachment-definition-client/pkg/client/informers/externalversions/factory.go:117
I0719 01:46:01.830610   37437 ovs.go:162] Exec(32): stdout: "\"00:50:56:8a:fb:ea\"\n"
I0719 01:46:01.830624   37437 ovs.go:163] Exec(32): stderr: ""
I0719 01:46:01.830636   37437 ovs.go:159] Exec(33): /usr/sbin/sysctl -w net.ipv4.conf.br-ex.forwarding=1
I0719 01:46:01.831512   37437 ovs.go:162] Exec(33): stdout: "net.ipv4.conf.br-ex.forwarding = 1\n"
I0719 01:46:01.831525   37437 ovs.go:163] Exec(33): stderr: ""
I0719 01:46:01.831535   37437 ovs.go:159] Exec(34): /usr/bin/ovs-vsctl --timeout=15 --if-exists get Open_vSwitch . external_ids:ovn-bridge-mappings
I0719 01:46:01.837543   37437 ovs.go:162] Exec(34): stdout: "\"physnet:br-ex\"\n"
I0719 01:46:01.837563   37437 ovs.go:163] Exec(34): stderr: ""
I0719 01:46:01.837579   37437 ovs.go:159] Exec(35): /usr/bin/ovs-vsctl --timeout=15 set Open_vSwitch . external_ids:ovn-bridge-mappings=physnet:br-ex
I0719 01:46:01.843270   37437 ovs.go:162] Exec(35): stdout: ""
I0719 01:46:01.843286   37437 ovs.go:163] Exec(35): stderr: ""
I0719 01:46:01.843298   37437 ovs.go:159] Exec(36): /usr/bin/ovs-vsctl --timeout=15 --if-exists get Open_vSwitch . external_ids:system-id
I0719 01:46:01.849149   37437 ovs.go:162] Exec(36): stdout: "\"ec7a39e5-89ad-4e47-a317-9fefe94160bf\"\n"
I0719 01:46:01.849170   37437 ovs.go:163] Exec(36): stderr: ""
I0719 01:46:01.849184   37437 ovs.go:159] Exec(37): /usr/bin/ovs-appctl --timeout=15 dpif/show-dp-features br-ex
I0719 01:46:01.853351   37437 ovs.go:162] Exec(37): stdout: "Masked set action: Yes\nTunnel push pop: No\nUfid: Yes\nTruncate action: Yes\nClone action: Yes\nSample nesting: 10\nConntrack eventmask: Yes\nConntrack clear: Yes\nMax dp_hash algorithm: 1\nCheck pkt length action: Yes\nConntrack timeout policy: Yes\nExplicit Drop action: No\nOptimized Balance TCP mode: No\nConntrack all-zero IP SNAT: Yes\nMPLS Label add: Yes\nMax VLAN headers: 2\nMax MPLS depth: 3\nRecirc: Yes\nCT state: Yes\nCT zone: Yes\nCT mark: Yes\nCT label: Yes\nCT state NAT: Yes\nCT orig tuple: Yes\nCT orig tuple for IPv6: Yes\nIPv6 ND Extension: No\n"
I0719 01:46:01.853378   37437 ovs.go:163] Exec(37): stderr: ""
I0719 01:46:01.853437   37437 ovs.go:159] Exec(38): /usr/bin/ovs-vsctl --timeout=15 --if-exists get Open_vSwitch . other_config:hw-offload
I0719 01:46:01.858808   37437 ovs.go:162] Exec(38): stdout: "\n"
I0719 01:46:01.858825   37437 ovs.go:163] Exec(38): stderr: ""
I0719 01:46:01.859289   37437 iptables.go:146] Deleting rule in table: filter, chain: FORWARD with args: "-p tcp -m tcp --dport 22623 -j REJECT" for protocol: 0
I0719 01:46:01.861554   37437 iptables.go:146] Deleting rule in table: filter, chain: FORWARD with args: "-p tcp -m tcp --dport 22624 -j REJECT" for protocol: 0
I0719 01:46:01.863747   37437 iptables.go:146] Deleting rule in table: filter, chain: OUTPUT with args: "-p tcp -m tcp --dport 22623 -j REJECT" for protocol: 0
I0719 01:46:01.866037   37437 iptables.go:146] Deleting rule in table: filter, chain: OUTPUT with args: "-p tcp -m tcp --dport 22624 -j REJECT" for protocol: 0
I0719 01:46:01.868226   37437 iptables.go:108] Creating table: filter chain: FORWARD
I0719 01:46:01.870145   37437 iptables.go:110] Chain: "FORWARD" in table: "filter" already exists, skipping creation: running [/usr/sbin/iptables -t filter -N FORWARD --wait]: exit status 1: iptables: Chain already exists.
I0719 01:46:01.874506   37437 iptables.go:108] Creating table: filter chain: OUTPUT
I0719 01:46:01.876429   37437 iptables.go:110] Chain: "OUTPUT" in table: "filter" already exists, skipping creation: running [/usr/sbin/iptables -t filter -N OUTPUT --wait]: exit status 1: iptables: Chain already exists.
I0719 01:46:01.880738   37437 gateway_shared_intf.go:1834] Shared Gateway Creation Complete
I0719 01:46:01.880955   37437 metrics.go:552] Stopping metrics server at address "127.0.0.1:29105"
I0719 01:46:01.880970   37437 ovnkube.go:577] Stopping ovnkube...
I0719 01:46:01.881013   37437 handler.go:203] Sending *v1.NetworkPolicy event handler 4 for removal
I0719 01:46:01.881026   37437 handler.go:203] Sending *v1.EgressFirewall event handler 10 for removal
I0719 01:46:01.881031   37437 handler.go:203] Sending *v1.Pod event handler 3 for removal
I0719 01:46:01.881038   37437 handler.go:203] Sending *v1.Pod event handler 5 for removal
I0719 01:46:01.881042   37437 handler.go:203] Sending *v1.Pod event handler 7 for removal
I0719 01:46:01.881049   37437 handler.go:217] Removed *v1.Pod event handler 7
I0719 01:46:01.881098   37437 handler.go:217] Removed *v1.NetworkPolicy event handler 4
I0719 01:46:01.881105   37437 handler.go:217] Removed *v1.EgressFirewall event handler 10
I0719 01:46:01.881109   37437 handler.go:217] Removed *v1.Pod event handler 3
I0719 01:46:01.881113   37437 handler.go:217] Removed *v1.Pod event handler 5
I0719 01:46:01.881138   37437 reflector.go:295] Stopping reflector *v1.AdminPolicyBasedExternalRoute (0s) from github.com/openshift/ovn-kubernetes/go-controller/pkg/crd/adminpolicybasedroute/v1/apis/informers/externalversions/factory.go:140
I0719 01:46:01.881150   37437 handler.go:203] Sending *v1.Namespace event handler 6 for removal
I0719 01:46:01.881155   37437 handler.go:203] Sending *v1.Namespace event handler 1 for removal
I0719 01:46:01.881159   37437 handler.go:203] Sending *v1.Node event handler 2 for removal
I0719 01:46:01.881164   37437 handler.go:203] Sending *v1.Node event handler 11 for removal
I0719 01:46:01.881167   37437 handler.go:203] Sending *v1.Node event handler 8 for removal
I0719 01:46:01.881170   37437 reflector.go:295] Stopping reflector *v1.EgressService (0s) from github.com/openshift/ovn-kubernetes/go-controller/pkg/crd/egressservice/v1/apis/informers/externalversions/factory.go:140
I0719 01:46:01.881177   37437 handler.go:217] Removed *v1.Node event handler 8
I0719 01:46:01.881174   37437 handler.go:203] Sending *v1.EgressIP event handler 9 for removal
I0719 01:46:01.881193   37437 handler.go:217] Removed *v1.Namespace event handler 1
I0719 01:46:01.881191   37437 handler.go:217] Removed *v1.Node event handler 2
I0719 01:46:01.881201   37437 handler.go:217] Removed *v1.EgressIP event handler 9
I0719 01:46:01.881207   37437 handler.go:217] Removed *v1.Node event handler 11
I0719 01:46:01.881205   37437 handler.go:217] Removed *v1.Namespace event handler 6
I0719 01:46:01.881207   37437 reflector.go:295] Stopping reflector *v1.EgressIP (0s) from github.com/openshift/ovn-kubernetes/go-controller/pkg/crd/egressip/v1/apis/informers/externalversions/factory.go:140
I0719 01:46:01.881279   37437 reflector.go:295] Stopping reflector *v1.EgressFirewall (0s) from github.com/openshift/ovn-kubernetes/go-controller/pkg/crd/egressfirewall/v1/apis/informers/externalversions/factory.go:140
I0719 01:46:01.881336   37437 reflector.go:295] Stopping reflector *v1alpha1.AdminNetworkPolicy (0s) from sigs.k8s.io/network-policy-api/pkg/client/informers/externalversions/factory.go:141
I0719 01:46:01.881383   37437 reflector.go:295] Stopping reflector *v1alpha1.BaselineAdminNetworkPolicy (0s) from sigs.k8s.io/network-policy-api/pkg/client/informers/externalversions/factory.go:141
I0719 01:46:01.881439   37437 reflector.go:295] Stopping reflector *v1.Service (0s) from k8s.io/client-go/informers/factory.go:159
I0719 01:46:01.881479   37437 reflector.go:295] Stopping reflector *v1.EndpointSlice (0s) from k8s.io/client-go/informers/factory.go:159
I0719 01:46:01.881525   37437 reflector.go:295] Stopping reflector *v1.Namespace (0s) from k8s.io/client-go/informers/factory.go:159
I0719 01:46:01.881567   37437 reflector.go:295] Stopping reflector *v1.NetworkPolicy (0s) from k8s.io/client-go/informers/factory.go:159
I0719 01:46:01.881600   37437 reflector.go:295] Stopping reflector *v1.Node (0s) from k8s.io/client-go/informers/factory.go:159
I0719 01:46:01.881653   37437 reflector.go:295] Stopping reflector *v1.EgressQoS (0s) from github.com/openshift/ovn-kubernetes/go-controller/pkg/crd/egressqos/v1/apis/informers/externalversions/factory.go:140
I0719 01:46:01.881704   37437 reflector.go:295] Stopping reflector *v1.Pod (0s) from k8s.io/client-go/informers/factory.go:159
I0719 01:46:01.898388   37437 shared_informer.go:318] Caches are synced for node-tracker-controller
I0719 01:46:01.898411   37437 services_controller.go:184] Setting up event handlers for services
I0719 01:46:01.898445   37437 services_controller.go:191] Shutting down controller ovn-lb-controller
E0719 01:46:01.898453   37437 ovn.go:458] Error running OVN Kubernetes Services controller: handler {0x1adac60 0x1ada9e0 0x1ada980} was not added to shared informer because it has stopped already
I0719 01:46:01.926604   37437 shared_informer.go:318] Caches are synced for network-controller-manager
I0719 01:46:01.926657   37437 network_attach_def_controller.go:182] Starting repairing loop for network-controller-manager
I0719 01:46:01.926727   37437 network_attach_def_controller.go:184] Finished repairing loop for network-controller-manager: 71.715µs err: <nil>
I0719 01:46:01.926733   37437 network_attach_def_controller.go:153] Starting workers for network-controller-manager NAD controller
I0719 01:46:01.926759   37437 obj_retry.go:432] Stop channel got triggered: will stop retrying failed objects of type *factory.localPodSelector
I0719 01:46:01.926774   37437 obj_retry.go:432] Stop channel got triggered: will stop retrying failed objects of type *factory.egressFwNode
I0719 01:46:01.926780   37437 obj_retry.go:432] Stop channel got triggered: will stop retrying failed objects of type *v1.EgressFirewall
I0719 01:46:01.926787   37437 obj_retry.go:432] Stop channel got triggered: will stop retrying failed objects of type *v1.Pod
I0719 01:46:01.926794   37437 obj_retry.go:432] Stop channel got triggered: will stop retrying failed objects of type *v1.Node
I0719 01:46:01.926795   37437 egressservice_zone.go:261] Shutting down Egress Services controller
I0719 01:46:01.926814   37437 obj_retry.go:432] Stop channel got triggered: will stop retrying failed objects of type *factory.egressIPPod
I0719 01:46:01.926813   37437 obj_retry.go:432] Stop channel got triggered: will stop retrying failed objects of type *v1.EgressIP
I0719 01:46:01.926822   37437 obj_retry.go:432] Stop channel got triggered: will stop retrying failed objects of type *factory.egressNode
I0719 01:46:01.926825   37437 egressqos.go:302] Shutting down EgressQoS controller
I0719 01:46:01.926829   37437 obj_retry.go:432] Stop channel got triggered: will stop retrying failed objects of type *v1.NetworkPolicy
I0719 01:46:01.926799   37437 admin_network_policy_controller.go:299] Shutting down controller default-network-controller
I0719 01:46:01.926833   37437 obj_retry.go:432] Stop channel got triggered: will stop retrying failed objects of type *factory.egressIPNamespace
I0719 01:46:01.926801   37437 obj_retry.go:432] Stop channel got triggered: will stop retrying failed objects of type *v1.Namespace
I0719 01:46:01.926885   37437 network_attach_def_controller.go:166] Shutting down network-controller-manager NAD controller
I0719 01:46:01.926957   37437 ovnkube.go:581] Stopped ovnkube
I0719 01:46:01.926999   37437 metrics.go:552] Stopping metrics server at address "127.0.0.1:29103"
I0719 01:46:01.927000   37437 reflector.go:295] Stopping reflector *v1.NetworkAttachmentDefinition (0s) from github.com/k8snetworkplumbingwg/network-attachment-definition-client/pkg/client/informers/externalversions/factory.go:117
F0719 01:46:01.927062   37437 ovnkube.go:136] failed to run ovnkube: failed to start node network controller: failed to start default node network controller: interface MTU (8900) is too small for specified overlay MTU (8958)
