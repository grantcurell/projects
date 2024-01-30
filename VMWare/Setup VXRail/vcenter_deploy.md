# vCenter Deploy

It looks like deploying vCenter is controlled by the file `vc_deploy.py`:

    vxrailmanager:~ # find / -iname vc_deploy.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vcdeploy/vc_deploy.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vcdeploy/vc_deploy.py

Run `docker inspect $(docker ps -qa) |  jq -r 'map([.Name, .GraphDriver.Data.MergedDir]) | .[] | "\(.[0])\t\(.[1])"'` to figure out which container owns that overlay.

Based on that it looks like there is a container called nano-service which owns that file:

    vxrailmanager:~ # docker inspect $(docker ps -qa) |  jq -r 'map([.Name, .GraphDriver.Data.MergedDir]) | .[] | "\(.[0])\t\(.[1])"' | grep 5c284f1529c19ad
    /func_nano-service.1.dqo23zdkgmwbqf9ru6yn0t99r  /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged
    vxrailmanager:~ # docker inspect $(docker ps -qa) |  jq -r 'map([.Name, .GraphDriver.Data.MergedDir]) | .[] | "\(.[0])\t\(.[1])"' | grep 6e4546b5beb8a

Drop to container command line: `docker exec -it 23e0ac7d3f92 /bin/bash`

Browse around and take a look at `vc_deploy.py`:

```python

logger = logging.getLogger(__name__)
ns = api.namespace('', description='Operations related to internal vc case')

host_info_model = get_host_conn_info_model(api)
storage_info_model = get_storage_info_model(api)
sync_call_result = build_api_model_sync_call_result(api)

vc_deploy_model = api.model('VCDeploy', {
    'host_conn_info': fields.Nested(host_info_model),
    'storage_info': fields.Nested(storage_info_model),
    'cluster_type': fields.String(required=True, description='vxrail cluster type')
})

VC_VM_NAME = 'VMware vCenter Server Appliance'

do_vm = DoCaller(do_host='do-vm', do_prefix='do-vm')

def perform(self, request_body):
    logger.info("start to perform VCDeploy, cluster type: {}".format(self.cluster_type))

    src_datastore = self._get_source_datastore_name()
    dst_datastore = self.storage_info.get('datastore') if self.cluster_type == ClusterType.COMPUTE.value else 'vsanDatastore'

    body = {
        'host_conn_info': self.host_conn_info,
        'src_datastore_name': src_datastore,
        'dst_datastore_name': dst_datastore,
        'vm_name': VC_VM_NAME
    }

    result = None
    try:
        result = do_vm.sync_call_do(do_vm.build_call_do_service_task_url(HOST_VM_OVA_DEPLOY_URL), body)
    except Exception as e:
        self.logger.info(e)
        self.raise_error('E3100_Cluster_24', params=(), message='Failed to deploy vCenter.')
    return result

```

Doing a search on `grep -rli 'external vc' / 2> /dev/null` gets 

    ...
    /var/lib/docker/overlay2/19f438b6cef2857e6067e49802d04d61de2afb7275bc6fb1323a41bac03fec1c/diff/home/app/worker/task/cluster.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/common/conf/config-messages.properties
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vcmgmtaccountpermissiongrant/vc_mgmt_account_permission_grant.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/externalvclicensevalidator/external_vc_license_validator.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/externalvcaccesslivevalidator/external_vc_access_live_validator.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/externalvccapacitylimitlivevalidator/external_vc_capacity_limit_live_validator.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hostaddtovds/host_add_to_vds.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hosttimesync/host_time_sync.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/timeconfigurationlivevalidator/time_configuration_live_validator.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hostunusedsystemvmsremove/host_unused_system_vms_remove.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/externalvcversioncompatibilitylivevalidator/external_vc_version_compatibility_live_validator.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vxmtimesync/vxm_time_sync.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/timesyncconfigurationvalidator/time_sync_configuration_validator.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vcsyslogconfig/vc_syslog_config.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/dnshostnameslivevalidator/dns_hostnames_live_validator.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/cursoryvalidator/hostname_configuration_validator.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/cursoryvalidator/tests/test_hostname_configuration_validator.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/cursoryvalidator/tests/test_none_value_validator.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/cursoryvalidator/tests/test_vcenter_configuration_validator.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/cursoryvalidator/tests/test_dns_servers_configuration_validator.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/cursoryvalidator/vcenter_configuration_validator.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/cursoryvalidator/none_value_validator.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/cursoryvalidator/dns_servers_configuration_validator.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/cursoryvalidator/passwords_configuration_validator.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/cursoryvalidator/netmask_configuration_validator.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vcuserpermissionlivevalidator/vc_user_permission_live_validator.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/createvmfolder/create_vm_folder.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/externalvcentitieslivevalidator/external_vc_entities_live_validator.py
    /var/lib/docker/overlay2/6df33189ca552a920f2d6c3259a034fac3ec47f8065634a6ba17ff7c74299377/merged/home/app/messages/messages_en_US.properties
    /var/lib/docker/overlay2/6df33189ca552a920f2d6c3259a034fac3ec47f8065634a6ba17ff7c74299377/merged/home/app/dayone/dayone_processor.py
    /var/lib/docker/overlay2/6df33189ca552a920f2d6c3259a034fac3ec47f8065634a6ba17ff7c74299377/merged/home/app/dayone/api.py
    /var/lib/docker/overlay2/1bc6389a4238217d15b1f5d931c6049e53891a92cef4255f6b402138e130d4d9/merged/home/app/lockbox_app/dao/postgres_dao.py
    /var/lib/docker/overlay2/1bc6389a4238217d15b1f5d931c6049e53891a92cef4255f6b402138e130d4d9/merged/home/app/lockbox_app/resources/verify_error_messages.json
    ...

Remove the cursory checks:

    (base) grant@DESKTOP-2SV1E9O:~$ grep -v cursory test.txt
        /var/lib/docker/overlay2/19f438b6cef2857e6067e49802d04d61de2afb7275bc6fb1323a41bac03fec1c/diff/home/app/worker/task/cluster.py
        /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/common/conf/config-messages.properties
        /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vcmgmtaccountpermissiongrant/vc_mgmt_account_permission_grant.py
        /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/externalvclicensevalidator/external_vc_license_validator.py
        /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/externalvcaccesslivevalidator/external_vc_access_live_validator.py
        /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/externalvccapacitylimitlivevalidator/external_vc_capacity_limit_live_validator.py
        /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hostaddtovds/host_add_to_vds.py
        /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hosttimesync/host_time_sync.py
        /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/timeconfigurationlivevalidator/time_configuration_live_validator.py
        /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hostunusedsystemvmsremove/host_unused_system_vms_remove.py
        /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/externalvcversioncompatibilitylivevalidator/external_vc_version_compatibility_live_validator.py
        /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vxmtimesync/vxm_time_sync.py
        /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/timesyncconfigurationvalidator/time_sync_configuration_validator.py
        /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vcsyslogconfig/vc_syslog_config.py
        /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/dnshostnameslivevalidator/dns_hostnames_live_validator.py
        /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vcuserpermissionlivevalidator/vc_user_permission_live_validator.py
        /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/createvmfolder/create_vm_folder.py
        /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/externalvcentitieslivevalidator/external_vc_entities_live_validator.py
        /var/lib/docker/overlay2/6df33189ca552a920f2d6c3259a034fac3ec47f8065634a6ba17ff7c74299377/merged/home/app/messages/messages_en_US.properties
        /var/lib/docker/overlay2/6df33189ca552a920f2d6c3259a034fac3ec47f8065634a6ba17ff7c74299377/merged/home/app/dayone/dayone_processor.py
        /var/lib/docker/overlay2/6df33189ca552a920f2d6c3259a034fac3ec47f8065634a6ba17ff7c74299377/merged/home/app/dayone/api.py
        /var/lib/docker/overlay2/1bc6389a4238217d15b1f5d931c6049e53891a92cef4255f6b402138e130d4d9/merged/home/app/lockbox_app/dao/postgres_dao.py
        /var/lib/docker/overlay2/1bc6389a4238217d15b1f5d931c6049e53891a92cef4255f6b402138e130d4d9/merged/home/app/lockbox_app/resources/verify_error_messages.json


Looking for the call `build_call_do_service_task_url`

    vxrailmanager:/var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vcdeploy # grep -rli 'build_call_do_service_task_url' /var/lib/docker/ 2> /dev/null
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/common/do.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/common/validation/ip_live_check_utils.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/common/network_prepare_aware_validator.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vxmconfigurationdatapopulate/vxm_configuration_data_populate.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hostaddintocluster/host_add_into_cluster.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/clusterconverttostretchedcluster/cluster_convert_to_stretched_cluster.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hostpsipupdate/host_ps_ip_update.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/multidiskgroupconfigurationvalidator/multi_disk_group_configuration_validator.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vcinitialboot/vc_initial_boot.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/clusterdasconfig/cluster_das_config.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hostnetworkmanagementipchange/host_network_management_ip_change.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vcmgmtaccountpermissiongrant/vc_mgmt_account_permission_grant.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vxrailkgsbaselineload/vxm_kgs_baseline_load.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vcretreatmodeconfigure/vc_retreat_mode_configure.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/enableteaming/enableteaming.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/externalvcaccesslivevalidator/external_vc_access_live_validator.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hosthostnamechange/host_hostname_change.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vxmupdatecertification/vxm_update_certification.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hoststorageleavevsan/host_storage_leave_vsan.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vxmconfigureslaacip/vxm_configure_slaacip.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vxmsystemservicesstop/vxm_system_services_stop.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/removedisconnecthostfromcluster/remove_disconnect_host_from_cluster.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hostaddtovds/host_add_to_vds.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hostassignactivepnictovds/host_assign_active_pnic_to_vds.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hostassignvmktovds/host_assign_vmk_to_vds.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/clusterhighavailabilityenable/cluster_high_availability_enable.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/switchcreatenetworks/switch_create_networks.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vxmruntimepropertiesgenerate/vxm_runtime_properties_generate.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hostvsanstorageenable/host_vsan_storage_enable.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hosttimesync/host_time_sync.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vcguestopsalias/vc_guest_ops_alias.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hostwitnesstrafficconnectivity/host_witness_traffic_connectivity.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hostvsandiskgroupscreate/host_vsan_diskgroups_create.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/createvds/createvds.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/switchconfiguplinks/switch_configure_uplinks.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/createportgroup/createportgroup.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vcpluginregister/vc_plugin_register.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vcdatacentercreate/vc_datacenter_create.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hoststoragevsandiskremove/host_storage_vsan_disk_remove.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hostptagentipchange/host_ptagent_ip_change.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/customersuppliedvdsvlanlivevalidator/customer_supplied_vds_vlan_live_validator.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hostversioncompatibilitylivevalidator/host_version_compatibility_live_validator.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/esxihostaccountvalidator/esxi_host_account_validator.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hostvsanstoragepolicyconfiguration/host_vsan_storage_policy_configuration.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hostunusedsystemvmsremove/host_unused_system_vms_remove.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/switchconfigjumpbox/switch_configure_jumpbox.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vccertsgenerate/vc_certs_generate.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/clusterdrsenable/cluster_drs_enable.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vclicensing/vc_licensing.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hostelectionservicedisable/host_election_service_disable.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/clusteraddexceptionaccounts/cluster_add_exception_accounts.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vcpasswordexpirationdisable/vc_password_expiration_disable.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vxmnetworkvnicremove/vxm_network_vnic_remove.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/externalvcversioncompatibilitylivevalidator/external_vc_version_compatibility_live_validator.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/omeintegration/ome_integration.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hostmarkpnicworkingmode/host_mark_pnic_working_mode.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/switchcreatedownlinks/switch_create_downlinks.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vxmevopassword/vxm_evo_password.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/movevxmvnictovds/vxm_network_vnic_add_to_vds.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hostloudmouthrestart/host_loudmouth_restart.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hoststorageaddtovsan/host_storage_add_to_vsan.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hostloggingsystemconfigure/host_logging_system_configure.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/clusteradvanceparamssetting/cluster_advance_params_setting.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/resetvspherealarms/reset_vsphere_alarms.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/networkcompatibilitylivevalidator/network_compatibility_live_validator.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/switchauthentication/switch_authentication.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vxmtimesync/vxm_time_sync.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hostsecurityservicedisable/host_security_service_disable.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/timesyncconfigurationvalidator/time_sync_configuration_validator.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vxmstaticipchange/vxm_static_ipchange.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/createstoragepolicy/create_storage_policy.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vxmclustercleanup/vxm_cluster_clean_up.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/switchchangepassword/switch_change_password.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hostplatformservicerestart/host_platform_service_restart.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hostdnschange/host_dns_change.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vxmautostartenable/vxm_auto_start_enable.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vlanlivevalidator/vlan_live_validator.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vxmserviceaccountvalidator/vxm_service_account_validator_task.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vxmhostnameset/vxm_hostname_set.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vcautostartenable/vc_auto_start_enable.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vcdeploy/vc_deploy.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hostwitnessnetworking/host_witness_networking.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hostmanagementaccountcreate/host_management_account_create.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/enablenioc/enablenioc.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vcsyslogconfig/vc_syslog_config.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vxmsystemservicesrestart/vxm_system_services_restart.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/checknodestatus/check_node_status.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vxmmovetostorage/vxm_move_to_storage.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hostassignpnictovss/host_assign_pnic_to_vss.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vcmgmntaccountcreate/vc_mgmnt_account_create.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/clusterevcenable/cluster_evc_enable.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vxmsetdns/vxm_set_dns.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/cursoryvalidator/cursory_validator.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hostvssremove/host_vss_remove.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/clustercreate/clustercreate.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hostaccountpasswordchange/host_account_password_change.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vxmrootaccountvalidator/vxm_root_account_validator_task.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hostproxyservicedisable/host_proxy_service_disable.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/clustersystemvmstoragepolicyapply/cluster_system_vm_storage_policy_apply.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hostassignstandbypnictovds/host_assign_standby_pnic_to_vds.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/createvmfolder/create_vm_folder.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/postdayoneconfiguration/post_dayone_configuration.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/hostnetworkmanagementvlanchange/host_network_management_vlan_change.py
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vxmupdateinternaldns/vxm_update_internal_dns.py
    /var/lib/docker/overlay2/6df33189ca552a920f2d6c3259a034fac3ec47f8065634a6ba17ff7c74299377/merged/home/app/dayone/do.py
    /var/lib/docker/overlay2/6df33189ca552a920f2d6c3259a034fac3ec47f8065634a6ba17ff7c74299377/merged/home/app/dayone/transfer_handler.py
    /var/lib/docker/overlay2/6df33189ca552a920f2d6c3259a034fac3ec47f8065634a6ba17ff7c74299377/merged/home/app/dayone/storage_discovery_callback.py
    /var/lib/docker/overlay2/6df33189ca552a920f2d6c3259a034fac3ec47f8065634a6ba17ff7c74299377/merged/home/app/vxm_ip_change_scheduler.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vxmconfigurationdatapopulate/vxm_configuration_data_populate.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hostaddintocluster/host_add_into_cluster.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/clusterconverttostretchedcluster/cluster_convert_to_stretched_cluster.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hostpsipupdate/host_ps_ip_update.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/multidiskgroupconfigurationvalidator/multi_disk_group_configuration_validator.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vcinitialboot/vc_initial_boot.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/clusterdasconfig/cluster_das_config.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hostnetworkmanagementipchange/host_network_management_ip_change.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vcmgmtaccountpermissiongrant/vc_mgmt_account_permission_grant.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vxrailkgsbaselineload/vxm_kgs_baseline_load.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vcretreatmodeconfigure/vc_retreat_mode_configure.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/enableteaming/enableteaming.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/externalvcaccesslivevalidator/external_vc_access_live_validator.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hosthostnamechange/host_hostname_change.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vxmupdatecertification/vxm_update_certification.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hoststorageleavevsan/host_storage_leave_vsan.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vxmconfigureslaacip/vxm_configure_slaacip.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vxmsystemservicesstop/vxm_system_services_stop.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/removedisconnecthostfromcluster/remove_disconnect_host_from_cluster.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hostaddtovds/host_add_to_vds.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hostassignactivepnictovds/host_assign_active_pnic_to_vds.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hostassignvmktovds/host_assign_vmk_to_vds.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/clusterhighavailabilityenable/cluster_high_availability_enable.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/switchcreatenetworks/switch_create_networks.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vxmruntimepropertiesgenerate/vxm_runtime_properties_generate.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hostvsanstorageenable/host_vsan_storage_enable.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hosttimesync/host_time_sync.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vcguestopsalias/vc_guest_ops_alias.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hostwitnesstrafficconnectivity/host_witness_traffic_connectivity.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hostvsandiskgroupscreate/host_vsan_diskgroups_create.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/createvds/createvds.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/switchconfiguplinks/switch_configure_uplinks.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/createportgroup/createportgroup.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vcpluginregister/vc_plugin_register.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vcdatacentercreate/vc_datacenter_create.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hoststoragevsandiskremove/host_storage_vsan_disk_remove.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hostptagentipchange/host_ptagent_ip_change.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/customersuppliedvdsvlanlivevalidator/customer_supplied_vds_vlan_live_validator.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hostversioncompatibilitylivevalidator/host_version_compatibility_live_validator.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/esxihostaccountvalidator/esxi_host_account_validator.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hostvsanstoragepolicyconfiguration/host_vsan_storage_policy_configuration.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hostunusedsystemvmsremove/host_unused_system_vms_remove.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/switchconfigjumpbox/switch_configure_jumpbox.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vccertsgenerate/vc_certs_generate.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/clusterdrsenable/cluster_drs_enable.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vclicensing/vc_licensing.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hostelectionservicedisable/host_election_service_disable.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/clusteraddexceptionaccounts/cluster_add_exception_accounts.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vcpasswordexpirationdisable/vc_password_expiration_disable.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vxmnetworkvnicremove/vxm_network_vnic_remove.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/externalvcversioncompatibilitylivevalidator/external_vc_version_compatibility_live_validator.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/omeintegration/ome_integration.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hostmarkpnicworkingmode/host_mark_pnic_working_mode.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/switchcreatedownlinks/switch_create_downlinks.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vxmevopassword/vxm_evo_password.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/movevxmvnictovds/vxm_network_vnic_add_to_vds.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hostloudmouthrestart/host_loudmouth_restart.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hoststorageaddtovsan/host_storage_add_to_vsan.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hostloggingsystemconfigure/host_logging_system_configure.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/clusteradvanceparamssetting/cluster_advance_params_setting.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/resetvspherealarms/reset_vsphere_alarms.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/networkcompatibilitylivevalidator/network_compatibility_live_validator.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/switchauthentication/switch_authentication.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vxmtimesync/vxm_time_sync.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hostsecurityservicedisable/host_security_service_disable.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/timesyncconfigurationvalidator/time_sync_configuration_validator.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vxmstaticipchange/vxm_static_ipchange.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/createstoragepolicy/create_storage_policy.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vxmclustercleanup/vxm_cluster_clean_up.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/common/do.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/common/validation/ip_live_check_utils.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/common/network_prepare_aware_validator.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/switchchangepassword/switch_change_password.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hostplatformservicerestart/host_platform_service_restart.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hostdnschange/host_dns_change.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vxmautostartenable/vxm_auto_start_enable.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vlanlivevalidator/vlan_live_validator.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vxmserviceaccountvalidator/vxm_service_account_validator_task.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vxmhostnameset/vxm_hostname_set.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vcautostartenable/vc_auto_start_enable.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vcdeploy/vc_deploy.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hostwitnessnetworking/host_witness_networking.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hostmanagementaccountcreate/host_management_account_create.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/enablenioc/enablenioc.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vcsyslogconfig/vc_syslog_config.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vxmsystemservicesrestart/vxm_system_services_restart.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/checknodestatus/check_node_status.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vxmmovetostorage/vxm_move_to_storage.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hostassignpnictovss/host_assign_pnic_to_vss.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vcmgmntaccountcreate/vc_mgmnt_account_create.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/clusterevcenable/cluster_evc_enable.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vxmsetdns/vxm_set_dns.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/cursoryvalidator/cursory_validator.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hostvssremove/host_vss_remove.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/clustercreate/clustercreate.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hostaccountpasswordchange/host_account_password_change.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vxmrootaccountvalidator/vxm_root_account_validator_task.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hostproxyservicedisable/host_proxy_service_disable.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/clustersystemvmstoragepolicyapply/cluster_system_vm_storage_policy_apply.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hostassignstandbypnictovds/host_assign_standby_pnic_to_vds.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/createvmfolder/create_vm_folder.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/postdayoneconfiguration/post_dayone_configuration.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/hostnetworkmanagementvlanchange/host_network_management_vlan_change.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/vxmupdateinternaldns/vxm_update_internal_dns.py
    /var/lib/docker/overlay2/0d8ac81dbb9015f2f3526cd468c2c4e7e433661e38008b04f70539deee19272a/diff/home/app/dayone/do.py
    /var/lib/docker/overlay2/0d8ac81dbb9015f2f3526cd468c2c4e7e433661e38008b04f70539deee19272a/diff/home/app/dayone/transfer_handler.py
    /var/lib/docker/overlay2/0d8ac81dbb9015f2f3526cd468c2c4e7e433661e38008b04f70539deee19272a/diff/home/app/dayone/storage_discovery_callback.py
    /var/lib/docker/overlay2/02a3e09ef808a5f704f821bbf2fcc89ece02f262e0a20b1c5a599fbf949a8c9b/diff/home/app/vxm_ip_change_scheduler.py

Finding the definition:

    vxrailmanager:/var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vcdeploy # grep -rli 'def build_call_do_service_task_url' /var/lib/docker/ 2> /dev/null                                            /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/common/do.py
    /var/lib/docker/overlay2/6df33189ca552a920f2d6c3259a034fac3ec47f8065634a6ba17ff7c74299377/merged/home/app/dayone/do.py
    /var/lib/docker/overlay2/6df33189ca552a920f2d6c3259a034fac3ec47f8065634a6ba17ff7c74299377/merged/home/app/vxm_ip_change_scheduler.py
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/common/do.py
    /var/lib/docker/overlay2/0d8ac81dbb9015f2f3526cd468c2c4e7e433661e38008b04f70539deee19272a/diff/home/app/dayone/do.py
    /var/lib/docker/overlay2/02a3e09ef808a5f704f821bbf2fcc89ece02f262e0a20b1c5a599fbf949a8c9b/diff/home/app/vxm_ip_change_scheduler.py

    There seems to be a file for licensing:


Find embedded license:

    vxrailmanager:/var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vcdeploy # find / -iname license-vc-700-e1-marvin-c1-201909
    \/usr/lib/vmware-marvin/marvind/webapps/lcm/WEB-INF/classes/licensing/7.0/license-vc-700-e1-marvin-c1-201909
    /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/common/conf/license-vc-700-e1-marvin-c1-201909
    /var/lib/docker/overlay2/eabf8f9430b1c90892414b04cd2934b09bbbadf357b3e97a6e4546b5beb8a192/diff/home/app/common/conf/license-vc-700-e1-marvin-c1-201909
    vxrailmanager:/var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/vcdeploy # cat /var/lib/docker/overlay2/de1ff478dd295cc17b5a7f2da36c356a893a18f10ed215c284f1529c19adf5da/merged/home/app/common/conf/license-vc-700-e1-marvin-c1-201909
    # VMware software license
    StartFields = "Cpt, ProductID, LicenseVersion, LicenseType, LicenseEdition, Option, Epoch"
    Cpt = "COPYRIGHT (c) VMware, Inc."
    ProductID = "VMware VirtualCenter Server"
    LicenseVersion = "7.0"
    LicenseType = "Site"
    Epoch = "2019-9-1"
    LicenseEdition = "vc.standard.instance.marvin"
    Option = "7"
    Data = "FileVersion=7.0.0.2;capacityType=server;enable=linkedvc,woe,xvp,vcha,backuprestore,appliancemigration;addon=vsa;disallowedHostEditions=esx.hypervisor.cpuPackage,esx.hypervisorEmbeddedOem.cpuPackage,esx.essentials.cpuPackage,esx.essentialsPlus.cpuPackage,esx.hypervisor.cpuPackageCoreLimited,esx.hypervisorEmbeddedOem.cpuPackageCoreLimited,esx.essentials.cpuPackageCoreLimited,esx.essentialsPlus.cpuPackageCoreLimited;desc=vCenter Server 7 Standard"
    DataHash = "60aebea4-31a0050c-c4e49494-27690fad-5a8a5258"
    Hash = "441d0833-d2f3bed9-0bea3fec-7d13664b-e222d862"

