# Bug Report

- [Bug Report](#bug-report)
  - [BMO Version](#bmo-version)
  - [Problem Description](#problem-description)
  - [Command Output](#command-output)
  - [Config file](#config-file)

## BMO Version

```
dell@bmo-manager-1:~$ !b
bmo version
COMPONENT NAME					VERSION
mw-release					v1.3.1
hpe-redfish-sku-pack				v1.3.1
mw-api-proxy					v1.3.1
mw-api-svc					v1.3.1
mw-cli						v1.3.1
mw-common					v1.3.1
mw-dhcp-server					v1.3.1
mw-discovery-manager				v1.3.1
mw-event-router					v1.3.1
mw-gui						v1.3.1
mw-hardware-controller				v1.3.1
mw-install					v1.3.1
mw-iso-builder					v1.3.1
mw-pxe-service					v1.3.1
mw-server-controller				v1.3.1
mw-site-controller				v1.3.1
mw-site-manager					v1.3.1
mw-sku-sdk					v1.3.1
mw-stack-deployer				v1.3.1
mw-stack-sku-pack				v1.3.1
mw-stack-sku-sdk				v1.3.1
mw-switch-controller				v1.3.1
mw-tenant-controller				v1.3.1
nso-sku-pack					v1.3.1
redfish-sku-pack				v1.3.1
samples						v1.3.1
supermicro-redfish-sku-pack			v1.3.1
switch-sku-pack					v1.3.1
wr-stack-sku-pack				v1.3.1
mw-s3-global					v1.3.1
mw-s3						v1.3.1
reloader					v1.3.1
redis						v1.3.1
mw-nginx					v1.3.1
mw-internal-nginx				v1.3.1
mw-opensearch					v1.3.1
mw-opensearch-dashboard				v1.3.1
mw-fluentd					v1.3.1
mw-tftp-server					v1.3.1
mw-dhcp-relay					v1.3.1
storage-version-migration-initializer		v0.0.5
storage-version-migration-trigger		v0.0.5
storage-version-migration-migrator		v0.0.5
```

## Problem Description

- When importing hardware profiles error output errenously reports incorrect fields
  - See below `namespace, reason: HardwareProfile.mw.dell.com "r7525-profile" is invalid: [spec.server.bios.attributes.numLock: Unsupported value: "true": supported values: "On", "Off"` but if you check [the configuration](#config-file) numLock is correctly set to `On` and not `true`. This error repeats for several other fields - ex: `tpmSecurity`
- Running the import multiple times yields different error messages instead of printing the entire error message

It is unclear how to take the values from a server configuration exported from the iDRAC or OME and import it into BMO. In my case, I attempted to export from iDRAC, clean with find/replace regex `^[ \t]+<Attribute Name="(.+)">([A-Za-z]+).*` -> `$1: $2` but while most of these fields directly match, capitalization does not seem to work. I am unsure what else is not working because I can't properly tell which fields aren't being accepted.

## Command Output

```
dell@bmo-manager-1:~$ bmo create hardwareprofile -f hw_pf_bios.yaml 
Failed to create hardware profile in the 'metalweaver' namespace, reason: HardwareProfile.mw.dell.com "r7525-profile" is invalid: [spec.server.bios.attributes.numLock: Unsupported value: "true": supported values: "On", "Off", spec.server.bios.attributes.setBootOrderEn: Invalid value: "AHCI": spec.server.bios.attributes.setBootOrderEn in body should match '^$|^((\w+|\*)\.(\w+|\*)\.(\w+|\*)(\-(\w+|\*))*((\w+|\*))*(\:((\w+|\*)\.(\w+|\*)\.(\w+|\*)(\-(\w+|\*))*((\w+|\*))*))*)(\,(\w+|\*)\.(\w+|\*)\.(\w+|\*)(\-(\w+|\*))*((\w+|\*))*(\:((\w+|\*)\.(\w+|\*)\.(\w+|\*)(\-(\w+|\*))*((\w+|\*))*))*)*$', spec.server.bios.attributes.serialPortAddress: Unsupported value: "Com": supported values: "Com1", "Com2", spec.server.bios.attributes.conTermType: Unsupported value: "Vt": supported values: "Vt100Vt220", "Ansi", spec.server.bios.attributes.tpmSecurity: Unsupported value: "true": supported values: "On", "Off", "OnPbm", "OnNoPbm", spec.server.bios.attributes.usbManagedPort: Unsupported value: "true": supported values: "On", "Off", spec.server.bios.attributes.pxeDev1Interface: Invalid value: "NIC": spec.server.bios.attributes.pxeDev1Interface in body should match '^NIC\.[A-Za-z]+\.[0-9]+\-[0-9]+\-[0-9]+']   
dell@bmo-manager-1:~$ fg
vim hw_pf_bios.yaml

[1]+  Stopped                 vim hw_pf_bios.yaml
dell@bmo-manager-1:~$ !b
bmo create hardwareprofile -f hw_pf_bios.yaml 
Failed to create hardware profile in the 'metalweaver' namespace, reason: HardwareProfile.mw.dell.com "r7525-profile" is invalid: [spec.server.bios.attributes.numLock: Unsupported value: "true": supported values: "On", "Off", spec.server.bios.attributes.setBootOrderEn: Invalid value: "AHCI": spec.server.bios.attributes.setBootOrderEn in body should match '^$|^((\w+|\*)\.(\w+|\*)\.(\w+|\*)(\-(\w+|\*))*((\w+|\*))*(\:((\w+|\*)\.(\w+|\*)\.(\w+|\*)(\-(\w+|\*))*((\w+|\*))*))*)(\,(\w+|\*)\.(\w+|\*)\.(\w+|\*)(\-(\w+|\*))*((\w+|\*))*(\:((\w+|\*)\.(\w+|\*)\.(\w+|\*)(\-(\w+|\*))*((\w+|\*))*))*)*$', spec.server.bios.attributes.serialPortAddress: Unsupported value: "Com": supported values: "Com1", "Com2", spec.server.bios.attributes.conTermType: Unsupported value: "Vt": supported values: "Vt100Vt220", "Ansi", spec.server.bios.attributes.tpmSecurity: Unsupported value: "true": supported values: "On", "Off", "OnPbm", "OnNoPbm", spec.server.bios.attributes.usbManagedPort: Unsupported value: "true": supported values: "On", "Off", spec.server.bios.attributes.pxeDev1Interface: Invalid value: "NIC": spec.server.bios.attributes.pxeDev1Interface in body should match '^NIC\.[A-Za-z]+\.[0-9]+\-[0-9]+\-[0-9]+']   
dell@bmo-manager-1:~$ !b
bmo create hardwareprofile -f hw_pf_bios.yaml 
Failed to create hardware profile in the 'metalweaver' namespace, reason: HardwareProfile.mw.dell.com "r7525-profile" is invalid: [spec.server.bios.attributes.numLock: Unsupported value: "true": supported values: "On", "Off", spec.server.bios.attributes.setBootOrderEn: Invalid value: "AHCI": spec.server.bios.attributes.setBootOrderEn in body should match '^$|^((\w+|\*)\.(\w+|\*)\.(\w+|\*)(\-(\w+|\*))*((\w+|\*))*(\:((\w+|\*)\.(\w+|\*)\.(\w+|\*)(\-(\w+|\*))*((\w+|\*))*))*)(\,(\w+|\*)\.(\w+|\*)\.(\w+|\*)(\-(\w+|\*))*((\w+|\*))*(\:((\w+|\*)\.(\w+|\*)\.(\w+|\*)(\-(\w+|\*))*((\w+|\*))*))*)*$', spec.server.bios.attributes.serialPortAddress: Unsupported value: "Com": supported values: "Com1", "Com2", spec.server.bios.attributes.conTermType: Unsupported value: "Vt": supported values: "Vt100Vt220", "Ansi", spec.server.bios.attributes.tpmSecurity: Unsupported value: "true": supported values: "On", "Off", "OnPbm", "OnNoPbm", spec.server.bios.attributes.usbManagedPort: Unsupported value: "true": supported values: "On", "Off", spec.server.bios.attributes.pxeDev1Interface: Invalid value: "NIC": spec.server.bios.attributes.pxeDev1Interface in body should match '^NIC\.[A-Za-z]+\.[0-9]+\-[0-9]+\-[0-9]+']   
dell@bmo-manager-1:~$ !b
bmo create hardwareprofile -f hw_pf_bios.yaml 
Failed to create hardware profile in the 'metalweaver' namespace, reason: HardwareProfile.mw.dell.com "r7525-profile" is invalid: [spec.server.bios.attributes.setBootOrderEn: Invalid value: "AHCI": spec.server.bios.attributes.setBootOrderEn in body should match '^$|^((\w+|\*)\.(\w+|\*)\.(\w+|\*)(\-(\w+|\*))*((\w+|\*))*(\:((\w+|\*)\.(\w+|\*)\.(\w+|\*)(\-(\w+|\*))*((\w+|\*))*))*)(\,(\w+|\*)\.(\w+|\*)\.(\w+|\*)(\-(\w+|\*))*((\w+|\*))*(\:((\w+|\*)\.(\w+|\*)\.(\w+|\*)(\-(\w+|\*))*((\w+|\*))*))*)*$', spec.server.bios.attributes.serialPortAddress: Unsupported value: "Com": supported values: "Com1", "Com2", spec.server.bios.attributes.conTermType: Unsupported value: "Vt": supported values: "Vt100Vt220", "Ansi", spec.server.bios.attributes.tpmSecurity: Unsupported value: "true": supported values: "On", "Off", "OnPbm", "OnNoPbm", spec.server.bios.attributes.usbManagedPort: Unsupported value: "true": supported values: "On", "Off", spec.server.bios.attributes.pxeDev1Interface: Invalid value: "NIC": spec.server.bios.attributes.pxeDev1Interface in body should match '^NIC\.[A-Za-z]+\.[0-9]+\-[0-9]+\-[0-9]+', spec.server.bios.attributes.numLock: Unsupported value: "true": supported values: "On", "Off"]   
dell@bmo-manager-1:~$ !b
bmo create hardwareprofile -f hw_pf_bios.yaml 
Failed to create hardware profile in the 'metalweaver' namespace, reason: HardwareProfile.mw.dell.com "r7525-profile" is invalid: [spec.server.bios.attributes.numLock: Unsupported value: "true": supported values: "On", "Off", spec.server.bios.attributes.setBootOrderEn: Invalid value: "AHCI": spec.server.bios.attributes.setBootOrderEn in body should match '^$|^((\w+|\*)\.(\w+|\*)\.(\w+|\*)(\-(\w+|\*))*((\w+|\*))*(\:((\w+|\*)\.(\w+|\*)\.(\w+|\*)(\-(\w+|\*))*((\w+|\*))*))*)(\,(\w+|\*)\.(\w+|\*)\.(\w+|\*)(\-(\w+|\*))*((\w+|\*))*(\:((\w+|\*)\.(\w+|\*)\.(\w+|\*)(\-(\w+|\*))*((\w+|\*))*))*)*$', spec.server.bios.attributes.serialPortAddress: Unsupported value: "Com": supported values: "Com1", "Com2", spec.server.bios.attributes.conTermType: Unsupported value: "Vt": supported values: "Vt100Vt220", "Ansi", spec.server.bios.attributes.tpmSecurity: Unsupported value: "true": supported values: "On", "Off", "OnPbm", "OnNoPbm", spec.server.bios.attributes.usbManagedPort: Unsupported value: "true": supported values: "On", "Off", spec.server.bios.attributes.pxeDev1Interface: Invalid value: "NIC": spec.server.bios.attributes.pxeDev1Interface in body should match '^NIC\.[A-Za-z]+\.[0-9]+\-[0-9]+\-[0-9]+']   
dell@bmo-manager-1:~$ !b
bmo create hardwareprofile -f hw_pf_bios.yaml 
Failed to create hardware profile in the 'metalweaver' namespace, reason: HardwareProfile.mw.dell.com "r7525-profile" is invalid: [spec.server.bios.attributes.tpmSecurity: Unsupported value: "true": supported values: "On", "Off", "OnPbm", "OnNoPbm", spec.server.bios.attributes.usbManagedPort: Unsupported value: "true": supported values: "On", "Off", spec.server.bios.attributes.pxeDev1Interface: Invalid value: "NIC": spec.server.bios.attributes.pxeDev1Interface in body should match '^NIC\.[A-Za-z]+\.[0-9]+\-[0-9]+\-[0-9]+', spec.server.bios.attributes.numLock: Unsupported value: "true": supported values: "On", "Off", spec.server.bios.attributes.setBootOrderEn: Invalid value: "AHCI": spec.server.bios.attributes.setBootOrderEn in body should match '^$|^((\w+|\*)\.(\w+|\*)\.(\w+|\*)(\-(\w+|\*))*((\w+|\*))*(\:((\w+|\*)\.(\w+|\*)\.(\w+|\*)(\-(\w+|\*))*((\w+|\*))*))*)(\,(\w+|\*)\.(\w+|\*)\.(\w+|\*)(\-(\w+|\*))*((\w+|\*))*(\:((\w+|\*)\.(\w+|\*)\.(\w+|\*)(\-(\w+|\*))*((\w+|\*))*))*)*$', spec.server.bios.attributes.serialPortAddress: Unsupported value: "Com": supported values: "Com1", "Com2", spec.server.bios.attributes.conTermType: Unsupported value: "Vt": supported values: "Vt100Vt220", "Ansi"]
```

## Config file

```
apiVersion: mw.dell.com/v1
kind: HardwareProfile
metadata:
  name: r7525-profile
  labels:
    site: gc
spec:
  # Add fields here
  apply: false
  preview: true
  server:
    bios:
     attributes:
      LogicalProc: Enabled
      ProcVirtualization: Enabled
      KernelDmaProtection: Disabled
      L1StreamHwPrefetcher: Enabled
      L2StreamHwPrefetcher: Enabled
      MadtCoreEnumeration: Linear
      CcxAsNumaDomain: Enabled
      TransparentSme: Disabled
      ProcConfigTdp: Maximum
      ProcX2Apic: Enabled
      ProcCcds: All
      CcdCores: All
      ControlledTurbo: Disabled
      OptimizerMode: Auto
      EmbSata: AhciMode
      SecurityFreezeLock: Enabled
      WriteCache: Disabled
      BiosNvmeDriver: DellQualifiedDrives
      BootMode: Uefi
      BootSeqRetry: Enabled
      GenericUsbBoot: Disabled
      HddPlaceholder: Disabled
      SysPrepClean: None
      SetBootOrderEn: AHCI
      pxeDev1Interface: NIC
      pxeDev1Protocol: IPv
      pxeDev1VlanEnDis: Disabled
      usbPorts: AllOn
      usbManagedPort: On
      IntegratedRaid: Enabled
      IntegratedNetwork1: Enabled
      EmbNic1Nic2: Enabled
      EmbVideo: Enabled
      PciePreferredIoBus: Disabled
      PcieEnhancedPreferredIo: Disabled
      SriovGlobalEnable: Disabled
      OsWatchdogTimer: Disabled
      DellAutoDiscovery: PlatformDefault
      SerialComm: OnNoConRedir
      serialPortAddress: Com
      ConTermType: Vt
      RedirAfterBoot: Enabled
      SysProfile: PerfOptimized
      PasswordStatus: Unlocked
      tpmSecurity: On
      Tpm2Hierarchy: Enabled
      PwrButton: Enabled
      AcPwrRcvry: Last
      AcPwrRcvryDelay: Immediate
      UefiVariableAccess: Standard
      SecureBoot: Disabled
      SecureBootPolicy: Standard
      SecureBootMode: DeployedMode
      TpmPpiBypassProvision: Disabled
      TpmPpiBypassClear: Disabled
      Tpm2Algorithm: SHA
      RedundantOsLocation: None
      MemTest: Disabled
      DramRefreshDelay: Minimum
      MemoryInterleaving: Auto
      CorrEccSmi: Enabled
      OppSrefEn: Disabled
      CECriticalSEL: Disabled
      PPROnUCE: Enabled
      numLock: On
      ErrPrompt: Enabled
      ForceInt10: Disabled
      DellWyseP25BIOSAccess: Enabled
  selectors:
    profileName: r7525
```