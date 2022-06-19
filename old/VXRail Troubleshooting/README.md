grep -rin <UID> ./*
apigw.log
dataservice.loglocalhost log

/var/lib/vmware-marvin - set to

## Disappearing Browse Button

1. Take a snapshot of VxM
2. psql -U postgres vxrail -c "DELETE FROM system.operation_status WHERE state='IN_PROGRESS';"
3. enable advanced mode by change it in /var/lib/vmware-marvin/lcm_advanced_mode.properties
4. Change the contents of /var/lib/vmware-mariv to {"state":"NONE","vc_plugin_updated":false,"deployed_for_public_api":false}
5. Result `system restart vmware-marvin`

## Log Info

lcm-web.log - Shows upgrade related info
web.log - combined web output

## Fixing Half Upgrade

Roll back to previous VxRail manager, then use it to complete the upgrade.

Uses ESXi management account for updates
Uses PSC log

## vCenter Logs

## Altbootbank

You can load the old version with shift+r

## Add nodes NIC config page

When you hit https://<host>/ui/vxrail/rest/vxm/private/system/cluster-hosts?$$objectID=urn:vmomi:ClusterComputeResource:domain<ID>&lang=en-us you should get back the existing hosts in the cluster with their hostname, model, serial_number, and vmnics

https://<HOST>/ui/vxrail/rest/vxm/private/system/available-hosts?$filter=serial_number%20in%20(SERIAL,SERIAL)&$$objectId=urn:vmomi:ClusterComputeResource:domain-<ID>&lang=en-us should get you the two hosts you are going to add

# Add Node Error

"Could not find NSX-T network information"
Http failure response for https://<address>/ui/vxrail/rest/vxm/private/cluster/network/nsxt???objectId=urn:vmomi:ClusterComputeResource:domain-ID=en-US: 404 OK

## Error Node

Validation Errors

Disk Grouping Error (JKSLH63)
Error occurs when validating disk group on host JKSLH63

web.log: ERROR [tomcat-http--48] com.emc.mystic.manager.commons.emc.webutil.LocaleUtil LocaleUtil.getBundleMessage:198 - No en_US resource bundle for ExpansionValidation with key JKSLH63

## General Error

web.log: [WARN] com.vce.commons.config.ConfigServiceImpl$NotFoundHandler ConfigServiceImpl$NotFoundHandler.handleNotFound:114 - provided key is not present: [404, {"message":"404 Not Found: bandwidth_throttling_level does not exist"}]

## Redeploying VxRail Manager

If VxRail Manager was previously deployed but something happened to it you can rebuild it. If you have the old VxRail manager, but the cluster has changed on ESXi, you will have to do:

- Update `/var/lib/vmware-marvin/runtime.properties` with the new cluster UUID
- Connect to the postgresql database on the manager, go to the settings table and update it with the new settings.

If you are redeploying VxRail manager in its totality then you can follow this procedure: [reloading-vxrail-plugin.docx](./reloading-vxrail-plugin.docx)