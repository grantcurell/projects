Name:                 ovnkube-node-9h9qr
Namespace:            openshift-ovn-kubernetes
Priority:             2000001000
Priority Class Name:  system-node-critical
Node:                 00-50-56-8a-fb-ea/10.10.25.235
Start Time:           Thu, 18 Jul 2024 15:58:21 -0400
Labels:               app=ovnkube-node
                      component=network
                      controller-revision-hash=5ffcfbd6cd
                      kubernetes.io/os=linux
                      openshift.io/component=network
                      ovn-db-pod=true
                      pod-template-generation=2
                      type=infra
Annotations:          network.operator.openshift.io/ovnkube-script-lib-hash: 663c3a02e150fe737e3198bcbd4b9054e311852f
                      networkoperator.openshift.io/cluster-network-cidr: 10.128.0.0/14
                      networkoperator.openshift.io/hybrid-overlay-status: disabled
                      networkoperator.openshift.io/ip-family-mode: single-stack
Status:               Running
IP:                   10.10.25.235
IPs:
  IP:           10.10.25.235
Controlled By:  DaemonSet/ovnkube-node
Init Containers:
  kubecfg-setup:
    Container ID:  cri-o://86d1421710d88dc5a35bf7b2b906b2c63e0a03af34c3623fd82ccb531d364d31
    Image:         quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85
    Image ID:      quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85
    Port:          <none>
    Host Port:     <none>
    Command:
      /bin/bash
      -c
      cat << EOF > /etc/ovn/kubeconfig
      apiVersion: v1
      clusters:
        - cluster:
            certificate-authority: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
            server: https://api-int.vmware-cluster.openshift.lan:6443
          name: default-cluster
      contexts:
        - context:
            cluster: default-cluster
            namespace: default
            user: default-auth
          name: default-context
      current-context: default-context
      kind: Config
      preferences: {}
      users:
        - name: default-auth
          user:
            client-certificate: /etc/ovn/ovnkube-node-certs/ovnkube-client-current.pem
            client-key: /etc/ovn/ovnkube-node-certs/ovnkube-client-current.pem
      EOF

    State:          Terminated
      Reason:       Completed
      Exit Code:    0
      Started:      Thu, 18 Jul 2024 21:19:36 -0400
      Finished:     Thu, 18 Jul 2024 21:19:36 -0400
    Ready:          True
    Restart Count:  4
    Environment:    <none>
    Mounts:
      /etc/ovn/ from etc-openvswitch (rw)
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-t4qsw (ro)
Containers:
  ovn-controller:
    Container ID:  cri-o://1d22558b72511867c3c781f4148b76a06678be11428a8812c6a89f9746608c41
    Image:         quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85
    Image ID:      quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85
    Port:          <none>
    Host Port:     <none>
    Command:
      /bin/bash
      -c
      set -e
      . /ovnkube-lib/ovnkube-lib.sh || exit 1
      start-ovn-controller ${OVN_LOG_LEVEL}

    State:          Running
      Started:      Thu, 18 Jul 2024 21:19:37 -0400
    Ready:          True
    Restart Count:  4
    Requests:
      cpu:     10m
      memory:  300Mi
    Environment:
      OVN_LOG_LEVEL:  info
      K8S_NODE:        (v1:spec.nodeName)
    Mounts:
      /dev/log from log-socket (rw)
      /env from env-overrides (rw)
      /etc/openvswitch from etc-openvswitch (rw)
      /etc/ovn/ from etc-openvswitch (rw)
      /ovnkube-lib from ovnkube-script-lib (rw)
      /run/openvswitch from run-openvswitch (rw)
      /run/ovn/ from run-ovn (rw)
      /var/lib/openvswitch from var-lib-openvswitch (rw)
      /var/log/ovn/ from node-log (rw)
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-t4qsw (ro)
  ovn-acl-logging:
    Container ID:  cri-o://e03313771074e5f2faa7128b24e8a6e097be550e4627a687d3e3d17df6b703a1
    Image:         quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85
    Image ID:      quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85
    Port:          <none>
    Host Port:     <none>
    Command:
      /bin/bash
      -c
      set -euo pipefail
      . /ovnkube-lib/ovnkube-lib.sh || exit 1
      start-audit-log-rotation

    State:          Running
      Started:      Thu, 18 Jul 2024 21:19:37 -0400
    Ready:          True
    Restart Count:  4
    Requests:
      cpu:        10m
      memory:     20Mi
    Environment:  <none>
    Mounts:
      /ovnkube-lib from ovnkube-script-lib (rw)
      /run/ovn/ from run-ovn (rw)
      /var/log/ovn/ from node-log (rw)
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-t4qsw (ro)
  kube-rbac-proxy-node:
    Container ID:  cri-o://8f21eeaa76f5b1a52f7126e32a589972fdcbd80ae4e7e7dc575f0c394aa5b2c6
    Image:         quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:f6a8f8e5b0c9b186512e95cfd740947bdd66584b86150b63ac7bc29b295c94bd
    Image ID:      quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:f6a8f8e5b0c9b186512e95cfd740947bdd66584b86150b63ac7bc29b295c94bd
    Port:          9103/TCP
    Host Port:     9103/TCP
    Command:
      /bin/bash
      -c
      #!/bin/bash
      set -euo pipefail
      . /ovnkube-lib/ovnkube-lib.sh || exit 1
      start-rbac-proxy-node ovn-node-metrics 9103 29103 /etc/pki/tls/metrics-cert/tls.key /etc/pki/tls/metrics-cert/tls.crt

    State:          Running
      Started:      Thu, 18 Jul 2024 21:19:37 -0400
    Ready:          True
    Restart Count:  4
    Requests:
      cpu:        10m
      memory:     20Mi
    Environment:  <none>
    Mounts:
      /etc/pki/tls/metrics-cert from ovn-node-metrics-cert (ro)
      /ovnkube-lib from ovnkube-script-lib (rw)
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-t4qsw (ro)
  kube-rbac-proxy-ovn-metrics:
    Container ID:  cri-o://2e8e75fef4c5c29c48ef2de198beff1d1a8d2cf82d772c21a5214b405456b864
    Image:         quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:f6a8f8e5b0c9b186512e95cfd740947bdd66584b86150b63ac7bc29b295c94bd
    Image ID:      quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:f6a8f8e5b0c9b186512e95cfd740947bdd66584b86150b63ac7bc29b295c94bd
    Port:          9105/TCP
    Host Port:     9105/TCP
    Command:
      /bin/bash
      -c
      #!/bin/bash
      set -euo pipefail
      . /ovnkube-lib/ovnkube-lib.sh || exit 1
      start-rbac-proxy-node ovn-metrics 9105 29105 /etc/pki/tls/metrics-cert/tls.key /etc/pki/tls/metrics-cert/tls.crt

    State:          Running
      Started:      Thu, 18 Jul 2024 21:19:37 -0400
    Ready:          True
    Restart Count:  4
    Requests:
      cpu:        10m
      memory:     20Mi
    Environment:  <none>
    Mounts:
      /etc/pki/tls/metrics-cert from ovn-node-metrics-cert (ro)
      /ovnkube-lib from ovnkube-script-lib (rw)
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-t4qsw (ro)
  northd:
    Container ID:  cri-o://2fad50e5d4aecccd782f4697e5445f826078a402f5267cc60e3cd9ce3101ecb5
    Image:         quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85
    Image ID:      quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85
    Port:          <none>
    Host Port:     <none>
    Command:
      /bin/bash
      -c
      set -xem
      if [[ -f /env/_master ]]; then
        set -o allexport
        source /env/_master
        set +o allexport
      fi
      . /ovnkube-lib/ovnkube-lib.sh || exit 1

      trap quit-ovn-northd TERM INT
      start-ovn-northd "${OVN_LOG_LEVEL}"

    State:          Running
      Started:      Thu, 18 Jul 2024 21:19:37 -0400
    Ready:          True
    Restart Count:  4
    Requests:
      cpu:     10m
      memory:  70Mi
    Environment:
      OVN_LOG_LEVEL:  info
    Mounts:
      /env from env-overrides (rw)
      /etc/ovn from etc-openvswitch (rw)
      /ovnkube-lib from ovnkube-script-lib (rw)
      /run/ovn/ from run-ovn (rw)
      /var/log/ovn from node-log (rw)
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-t4qsw (ro)
  nbdb:
    Container ID:  cri-o://cb6e22a681696d999db1ec967df6ef523f88afbc2860b965db928947ad3f93dd
    Image:         quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85
    Image ID:      quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85
    Port:          <none>
    Host Port:     <none>
    Command:
      /bin/bash
      -c
      set -xem
      if [[ -f /env/_master ]]; then
        set -o allexport
        source /env/_master
        set +o allexport
      fi
      . /ovnkube-lib/ovnkube-lib.sh || exit 1

      trap quit-nbdb TERM INT
      start-nbdb ${OVN_LOG_LEVEL}

    State:          Running
      Started:      Thu, 18 Jul 2024 21:19:37 -0400
    Ready:          True
    Restart Count:  4
    Requests:
      cpu:      10m
      memory:   300Mi
    Readiness:  exec [/bin/bash -c set -xeo pipefail
. /ovnkube-lib/ovnkube-lib.sh || exit 1
ovndb-readiness-probe "nb"
] delay=10s timeout=5s period=10s #success=1 #failure=3
    Environment:
      OVN_LOG_LEVEL:  info
      K8S_NODE:        (v1:spec.nodeName)
    Mounts:
      /env from env-overrides (rw)
      /etc/ovn/ from etc-openvswitch (rw)
      /ovnkube-lib from ovnkube-script-lib (rw)
      /run/ovn/ from run-ovn (rw)
      /var/log/ovn from node-log (rw)
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-t4qsw (ro)
  sbdb:
    Container ID:  cri-o://43336c1654c81d435dc83e3310feece4c024d9de409d5cd3c61a90c0ddd0cb24
    Image:         quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85
    Image ID:      quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85
    Port:          <none>
    Host Port:     <none>
    Command:
      /bin/bash
      -c
      set -xem
      if [[ -f /env/_master ]]; then
        set -o allexport
        source /env/_master
        set +o allexport
      fi
      . /ovnkube-lib/ovnkube-lib.sh || exit 1

      trap quit-sbdb TERM INT
      start-sbdb ${OVN_LOG_LEVEL}

    State:          Running
      Started:      Thu, 18 Jul 2024 21:19:40 -0400
    Ready:          True
    Restart Count:  4
    Requests:
      cpu:      10m
      memory:   300Mi
    Readiness:  exec [/bin/bash -c set -xeo pipefail
. /ovnkube-lib/ovnkube-lib.sh || exit 1
ovndb-readiness-probe "sb"
] delay=10s timeout=5s period=10s #success=1 #failure=3
    Environment:
      OVN_LOG_LEVEL:  info
    Mounts:
      /env from env-overrides (rw)
      /etc/ovn/ from etc-openvswitch (rw)
      /ovnkube-lib from ovnkube-script-lib (rw)
      /run/ovn/ from run-ovn (rw)
      /var/log/ovn from node-log (rw)
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-t4qsw (ro)
  ovnkube-controller:
    Container ID:  cri-o://dce7e6bf4da07d1a996eda3768ff680c7fc94b0a60c902a2194d9438df83e6c8
    Image:         quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85
    Image ID:      quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85
    Port:          29105/TCP
    Host Port:     29105/TCP
    Command:
      /bin/bash
      -c
      set -xe
      . /ovnkube-lib/ovnkube-lib.sh || exit 1
      start-ovnkube-node ${OVN_KUBE_LOG_LEVEL} 29103 29105

    State:       Waiting
      Reason:    CrashLoopBackOff
    Last State:  Terminated
      Reason:    Error
      Message:   r ovn-lb-controller
I0719 01:40:54.006431   31935 egressservice_zone.go:261] Shutting down Egress Services controller
E0719 01:40:54.006439   31935 ovn.go:458] Error running OVN Kubernetes Services controller: error syncing service and endpoint handlers
I0719 01:40:54.006439   31935 admin_network_policy_controller.go:299] Shutting down controller default-network-controller
I0719 01:40:54.006446   31935 obj_retry.go:432] Stop channel got triggered: will stop retrying failed objects of type *v1.EgressFirewall
I0719 01:40:54.006455   31935 obj_retry.go:432] Stop channel got triggered: will stop retrying failed objects of type *factory.egressIPPod
I0719 01:40:54.006456   31935 obj_retry.go:432] Stop channel got triggered: will stop retrying failed objects of type *v1.Pod
I0719 01:40:54.006459   31935 obj_retry.go:432] Stop channel got triggered: will stop retrying failed objects of type *v1.EgressIP
I0719 01:40:54.006482   31935 obj_retry.go:432] Stop channel got triggered: will stop retrying failed objects of type *factory.egressNode
I0719 01:40:54.006476   31935 obj_retry.go:432] Stop channel got triggered: will stop retrying failed objects of type *v1.Node
I0719 01:40:54.006488   31935 obj_retry.go:432] Stop channel got triggered: will stop retrying failed objects of type *v1.Namespace
I0719 01:40:54.006521   31935 network_attach_def_controller
      Exit Code:    1
      Started:      Thu, 18 Jul 2024 21:40:53 -0400
      Finished:     Thu, 18 Jul 2024 21:40:54 -0400
    Ready:          False
    Restart Count:  36
    Requests:
      cpu:      10m
      memory:   600Mi
    Readiness:  exec [/bin/bash -c #!/bin/bash
test -f /etc/cni/net.d/10-ovn-kubernetes.conf
] delay=5s timeout=1s period=30s #success=1 #failure=3
    Environment:
      KUBERNETES_SERVICE_PORT:          6443
      KUBERNETES_SERVICE_HOST:          api-int.vmware-cluster.openshift.lan
      OVN_CONTROLLER_INACTIVITY_PROBE:  180000
      OVN_KUBE_LOG_LEVEL:               4
      K8S_NODE:                          (v1:spec.nodeName)
      POD_NAME:                         ovnkube-node-9h9qr (v1:metadata.name)
    Mounts:
      /cni-bin-dir from host-cni-bin (rw)
      /env from env-overrides (rw)
      /etc/cni/net.d from host-cni-netd (rw)
      /etc/openvswitch from etc-openvswitch (rw)
      /etc/ovn/ from etc-openvswitch (rw)
      /etc/systemd/system from systemd-units (ro)
      /host from host-slash (ro)
      /ovnkube-lib from ovnkube-script-lib (rw)
      /run/netns from host-run-netns (ro)
      /run/openvswitch from run-openvswitch (rw)
      /run/ovn-kubernetes/ from host-run-ovn-kubernetes (rw)
      /run/ovn/ from run-ovn (rw)
      /run/ovnkube-config/ from ovnkube-config (rw)
      /var/lib/cni/networks/ovn-k8s-cni-overlay from host-var-lib-cni-networks-ovn-kubernetes (rw)
      /var/lib/kubelet from host-kubelet (ro)
      /var/lib/openvswitch from var-lib-openvswitch (rw)
      /var/log/ovnkube/ from etc-openvswitch (rw)
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-t4qsw (ro)
Conditions:
  Type                        Status
  PodReadyToStartContainers   True
  Initialized                 True
  Ready                       False
  ContainersReady             False
  PodScheduled                True
Volumes:
  host-kubelet:
    Type:          HostPath (bare host directory volume)
    Path:          /var/lib/kubelet
    HostPathType:
  systemd-units:
    Type:          HostPath (bare host directory volume)
    Path:          /etc/systemd/system
    HostPathType:
  host-slash:
    Type:          HostPath (bare host directory volume)
    Path:          /
    HostPathType:
  host-run-netns:
    Type:          HostPath (bare host directory volume)
    Path:          /run/netns
    HostPathType:
  var-lib-openvswitch:
    Type:          HostPath (bare host directory volume)
    Path:          /var/lib/openvswitch/data
    HostPathType:
  etc-openvswitch:
    Type:          HostPath (bare host directory volume)
    Path:          /var/lib/ovn-ic/etc
    HostPathType:
  run-openvswitch:
    Type:          HostPath (bare host directory volume)
    Path:          /var/run/openvswitch
    HostPathType:
  run-ovn:
    Type:          HostPath (bare host directory volume)
    Path:          /var/run/ovn-ic
    HostPathType:
  node-log:
    Type:          HostPath (bare host directory volume)
    Path:          /var/log/ovn
    HostPathType:
  log-socket:
    Type:          HostPath (bare host directory volume)
    Path:          /dev/log
    HostPathType:
  host-run-ovn-kubernetes:
    Type:          HostPath (bare host directory volume)
    Path:          /run/ovn-kubernetes
    HostPathType:
  host-cni-bin:
    Type:          HostPath (bare host directory volume)
    Path:          /var/lib/cni/bin
    HostPathType:
  host-cni-netd:
    Type:          HostPath (bare host directory volume)
    Path:          /var/run/multus/cni/net.d
    HostPathType:
  host-var-lib-cni-networks-ovn-kubernetes:
    Type:          HostPath (bare host directory volume)
    Path:          /var/lib/cni/networks/ovn-k8s-cni-overlay
    HostPathType:
  ovnkube-config:
    Type:      ConfigMap (a volume populated by a ConfigMap)
    Name:      ovnkube-config
    Optional:  false
  env-overrides:
    Type:      ConfigMap (a volume populated by a ConfigMap)
    Name:      env-overrides
    Optional:  true
  ovn-node-metrics-cert:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  ovn-node-metrics-cert
    Optional:    true
  ovnkube-script-lib:
    Type:      ConfigMap (a volume populated by a ConfigMap)
    Name:      ovnkube-script-lib
    Optional:  false
  kube-api-access-t4qsw:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
    ConfigMapName:           openshift-service-ca.crt
    ConfigMapOptional:       <nil>
QoS Class:                   Burstable
Node-Selectors:              kubernetes.io/os=linux
Tolerations:                 op=Exists
Events:
  Type     Reason        Age                    From               Message
  ----     ------        ----                   ----               -------
  Normal   Scheduled     5h45m                  default-scheduler  Successfully assigned openshift-ovn-kubernetes/ovnkube-node-9h9qr to 00-50-56-8a-fb-ea
  Normal   Pulling       5h45m                  kubelet            Pulling image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85"
  Normal   Pulled        5h44m                  kubelet            Successfully pulled image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" in 22.33s (22.33s including waiting)
  Normal   Created       5h44m                  kubelet            Created container kubecfg-setup
  Normal   Started       5h44m                  kubelet            Started container kubecfg-setup
  Normal   Started       5h44m                  kubelet            Started container ovn-acl-logging
  Normal   Created       5h44m                  kubelet            Created container ovn-controller
  Normal   Started       5h44m                  kubelet            Started container ovn-controller
  Normal   Pulled        5h44m                  kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" already present on machine
  Normal   Created       5h44m                  kubelet            Created container ovn-acl-logging
  Normal   Created       5h44m                  kubelet            Created container northd
  Normal   Pulled        5h44m                  kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:f6a8f8e5b0c9b186512e95cfd740947bdd66584b86150b63ac7bc29b295c94bd" already present on machine
  Normal   Created       5h44m                  kubelet            Created container kube-rbac-proxy-node
  Normal   Started       5h44m                  kubelet            Started container kube-rbac-proxy-node
  Normal   Pulled        5h44m                  kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:f6a8f8e5b0c9b186512e95cfd740947bdd66584b86150b63ac7bc29b295c94bd" already present on machine
  Normal   Created       5h44m                  kubelet            Created container kube-rbac-proxy-ovn-metrics
  Normal   Pulled        5h44m                  kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" already present on machine
  Normal   Pulled        5h44m                  kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" already present on machine
  Normal   Started       5h44m                  kubelet            Started container kube-rbac-proxy-ovn-metrics
  Normal   Started       5h44m                  kubelet            Started container northd
  Normal   Pulled        5h44m                  kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" already present on machine
  Normal   Created       5h44m                  kubelet            Created container nbdb
  Normal   Started       5h44m                  kubelet            Started container nbdb
  Normal   Started       5h44m                  kubelet            Started container sbdb
  Normal   Created       5h44m                  kubelet            Created container sbdb
  Normal   Pulled        5h44m                  kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" already present on machine
  Warning  NodeNotReady  3h9m                   node-controller    Node is not ready
  Normal   Pulled        3h9m                   kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" already present on machine
  Normal   Created       3h9m                   kubelet            Created container kubecfg-setup
  Normal   Started       3h9m                   kubelet            Started container kubecfg-setup
  Normal   Pulled        3h9m                   kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" already present on machine
  Normal   Created       3h9m                   kubelet            Created container nbdb
  Normal   Started       3h9m                   kubelet            Started container ovn-controller
  Normal   Pulled        3h9m                   kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" already present on machine
  Normal   Created       3h9m                   kubelet            Created container ovn-acl-logging
  Normal   Started       3h9m                   kubelet            Started container ovn-acl-logging
  Normal   Created       3h9m                   kubelet            Created container ovn-controller
  Normal   Created       3h9m                   kubelet            Created container kube-rbac-proxy-node
  Normal   Started       3h9m                   kubelet            Started container kube-rbac-proxy-node
  Normal   Pulled        3h9m                   kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:f6a8f8e5b0c9b186512e95cfd740947bdd66584b86150b63ac7bc29b295c94bd" already present on machine
  Normal   Created       3h9m                   kubelet            Created container kube-rbac-proxy-ovn-metrics
  Normal   Started       3h9m                   kubelet            Started container nbdb
  Normal   Pulled        3h9m                   kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" already present on machine
  Normal   Created       3h9m                   kubelet            Created container northd
  Normal   Started       3h9m                   kubelet            Started container northd
  Normal   Pulled        3h9m                   kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" already present on machine
  Normal   Started       3h9m                   kubelet            Started container kube-rbac-proxy-ovn-metrics
  Normal   Pulled        3h9m                   kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:f6a8f8e5b0c9b186512e95cfd740947bdd66584b86150b63ac7bc29b295c94bd" already present on machine
  Normal   Created       3h9m                   kubelet            Created container sbdb
  Normal   Pulled        3h9m                   kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" already present on machine
  Normal   Started       3h9m                   kubelet            Started container sbdb
  Normal   Pulled        3h9m                   kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" already present on machine
  Normal   Created       169m                   kubelet            Created container kubecfg-setup
  Normal   Pulled        169m                   kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" already present on machine
  Normal   Started       169m                   kubelet            Started container kubecfg-setup
  Normal   Pulled        169m                   kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" already present on machine
  Normal   Created       169m                   kubelet            Created container ovn-controller
  Normal   Started       169m                   kubelet            Started container ovn-controller
  Normal   Pulled        169m                   kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" already present on machine
  Normal   Created       169m                   kubelet            Created container ovn-acl-logging
  Normal   Pulled        169m                   kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:f6a8f8e5b0c9b186512e95cfd740947bdd66584b86150b63ac7bc29b295c94bd" already present on machine
  Normal   Pulled        169m                   kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:f6a8f8e5b0c9b186512e95cfd740947bdd66584b86150b63ac7bc29b295c94bd" already present on machine
  Normal   Started       169m                   kubelet            Started container kube-rbac-proxy-node
  Normal   Started       169m                   kubelet            Started container ovn-acl-logging
  Normal   Created       169m                   kubelet            Created container kube-rbac-proxy-node
  Normal   Created       169m                   kubelet            Created container nbdb
  Normal   Started       169m                   kubelet            Started container kube-rbac-proxy-ovn-metrics
  Normal   Pulled        169m                   kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" already present on machine
  Normal   Created       169m                   kubelet            Created container northd
  Normal   Started       169m                   kubelet            Started container northd
  Normal   Pulled        169m                   kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" already present on machine
  Normal   Started       169m                   kubelet            Started container nbdb
  Normal   Created       169m                   kubelet            Created container kube-rbac-proxy-ovn-metrics
  Normal   Created       169m                   kubelet            Created container sbdb
  Normal   Started       169m                   kubelet            Started container sbdb
  Normal   Pulled        169m                   kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" already present on machine
  Normal   Pulled        169m                   kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" already present on machine
  Warning  NodeNotReady  119m                   node-controller    Node is not ready
  Normal   Started       119m                   kubelet            Started container kubecfg-setup
  Normal   Pulled        119m                   kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" already present on machine
  Normal   Created       119m                   kubelet            Created container kubecfg-setup
  Normal   Pulled        119m                   kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:f6a8f8e5b0c9b186512e95cfd740947bdd66584b86150b63ac7bc29b295c94bd" already present on machine
  Normal   Created       119m                   kubelet            Created container ovn-controller
  Normal   Started       119m                   kubelet            Started container ovn-controller
  Normal   Pulled        119m                   kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" already present on machine
  Normal   Created       119m                   kubelet            Created container ovn-acl-logging
  Normal   Started       119m                   kubelet            Started container ovn-acl-logging
  Normal   Pulled        119m                   kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" already present on machine
  Normal   Created       119m                   kubelet            Created container kube-rbac-proxy-node
  Normal   Started       119m                   kubelet            Started container kube-rbac-proxy-node
  Normal   Pulled        119m                   kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:f6a8f8e5b0c9b186512e95cfd740947bdd66584b86150b63ac7bc29b295c94bd" already present on machine
  Normal   Created       119m                   kubelet            Created container kube-rbac-proxy-ovn-metrics
  Normal   Started       119m                   kubelet            Started container kube-rbac-proxy-ovn-metrics
  Normal   Pulled        119m                   kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" already present on machine
  Normal   Created       119m                   kubelet            Created container northd
  Normal   Started       119m                   kubelet            Started container northd
  Normal   Pulled        119m                   kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" already present on machine
  Normal   Created       119m                   kubelet            Created container nbdb
  Normal   Started       119m                   kubelet            Started container nbdb
  Normal   Pulled        119m                   kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" already present on machine
  Normal   Created       119m                   kubelet            Created container sbdb
  Normal   Started       119m                   kubelet            Started container sbdb
  Normal   Pulled        119m                   kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" already present on machine
  Warning  BackOff       29m (x436 over 119m)   kubelet            Back-off restarting failed container ovnkube-controller in pod ovnkube-node-9h9qr_openshift-ovn-kubernetes(5ade0811-dd08-4a17-bac7-fd66e33604a2)
  Normal   Pulling       24m                    kubelet            Pulling image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85"
  Normal   Pulled        23m                    kubelet            Successfully pulled image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" in 26.642s (26.642s including waiting)
  Normal   Created       23m                    kubelet            Created container kubecfg-setup
  Normal   Started       23m                    kubelet            Started container kubecfg-setup
  Normal   Started       23m                    kubelet            Started container kube-rbac-proxy-node
  Normal   Created       23m                    kubelet            Created container ovn-controller
  Normal   Started       23m                    kubelet            Started container ovn-controller
  Normal   Pulled        23m                    kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" already present on machine
  Normal   Created       23m                    kubelet            Created container ovn-acl-logging
  Normal   Started       23m                    kubelet            Started container nbdb
  Normal   Pulled        23m                    kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:f6a8f8e5b0c9b186512e95cfd740947bdd66584b86150b63ac7bc29b295c94bd" already present on machine
  Normal   Created       23m                    kubelet            Created container kube-rbac-proxy-node
  Normal   Pulled        23m                    kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" already present on machine
  Normal   Pulled        23m                    kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:f6a8f8e5b0c9b186512e95cfd740947bdd66584b86150b63ac7bc29b295c94bd" already present on machine
  Normal   Created       23m                    kubelet            Created container kube-rbac-proxy-ovn-metrics
  Normal   Started       23m                    kubelet            Started container kube-rbac-proxy-ovn-metrics
  Normal   Pulled        23m                    kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" already present on machine
  Normal   Created       23m                    kubelet            Created container northd
  Normal   Started       23m                    kubelet            Started container northd
  Normal   Pulled        23m                    kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" already present on machine
  Normal   Created       23m                    kubelet            Created container nbdb
  Normal   Started       23m                    kubelet            Started container ovn-acl-logging
  Normal   Pulled        23m                    kubelet            Container image "quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:23395965032acaad15638e79257b8439395640c8bf73b8c0bb702759840f3b85" already present on machine
  Normal   Created       23m                    kubelet            Created container sbdb
  Normal   Started       23m                    kubelet            Started container sbdb
  Warning  BackOff       4m14s (x100 over 23m)  kubelet            Back-off restarting failed container ovnkube-controller in pod ovnkube-node-9h9qr_openshift-ovn-kubernetes(5ade0811-dd08-4a17-bac7-fd66e33604a2)
