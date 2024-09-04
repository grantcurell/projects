# Automatically Provision Dell Servers

This tutorial covers the various ways to automatically provision Dell servers.

- [Automatically Provision Dell Servers](#automatically-provision-dell-servers)
  - [Helpful Links](#helpful-links)
  - [Overview](#overview)
    - [When to Use OpenManage Enterprise (OME) and When Not](#when-to-use-openmanage-enterprise-ome-and-when-not)
  - [OME Workflow](#ome-workflow)
    - [Overview of Configuration for Both](#overview-of-configuration-for-both)
    - [Overview of How it Works After Config](#overview-of-how-it-works-after-config)
    - [Using Server Initiated Discovery](#using-server-initiated-discovery)
    - [Using a Custom Discovery Workflow](#using-a-custom-discovery-workflow)
  - [Entirely Custom Workflow](#entirely-custom-workflow)


## Helpful Links

- [OME Template Function](https://www.dell.com/support/manuals/en-us/dell-openmanage-enterprise/ome-3.4_ug/create-a-template-from-a-reference-device?guid=guid-c4b89f0b-7e15-48f6-9210-3ea1e2f74c61&lang=en-us)
- [OME Server Initiated Discovery](https://www.dell.com/support/kbdoc/en-us/000192340/training-video-that-covers-server-initiated-discovery-in-openmanage-enterprise)
- [Enabling OME Server Initiated Discovery](https://www.dell.com/support/manuals/en-au/dell-openmanage-enterprise/ome_3.5_ug/discover-servers-automatically-by-using-the-server-initiated-discovery-feature?guid=guid-23bd252f-9651-410a-88de-3f332d748b55&lang=en-us)
- [OME Download](https://www.dell.com/support/kbdoc/en-us/000175879/support-for-openmanage-enterprise)
- [OME Licensing Info](https://infohub.delltechnologies.com/p/new-openmanage-enterprise-advanced-ready-to-bring-new-customer-benefits/)
- [OME Auto Deploy Instructions](https://www.dell.com/support/manuals/en-us/dell-openmanage-enterprise/ome-3.4_ug/auto-deployment-of-configuration-on-yet-to-be-discovered-servers-or-chassis?guid=guid-4c0e00fb-fed3-443f-9ac8-66a0db461f0b&lang=en-us)
- [OME Create Auto Deployment Targets](https://www.dell.com/support/manuals/en-us/dell-openmanage-enterprise/ome-3.4_ug/create-auto-deployment-targets?guid=guid-0777321e-9232-4e02-b16f-1932def39879&lang=en-us)
- [Dell Whitepaper on OME Autodeploy](https://dl.dell.com/manuals/all-products/esuprt_software_int/esuprt_software_ent_systems_mgmt/dell-openmanage-enterprise_white-papers11_en-us.pdf)
- [Dell Update Manager Plugin](https://infohub.delltechnologies.com/p/update-manager-plugin-for-openmanage-enterprise-overview/)
- [Dell Server Initiated Discovery Whitepaper](https://dl.dell.com/manuals/all-products/esuprt_software_int/esuprt_software_ent_systems_mgmt/dell-openmanage-enterprise_white-papers15_en-us.pdf)
- [Discovery with Ansible](https://docs.ansible.com/ansible/latest/collections/dellemc/openmanage/ome_discovery_module.html#ansible-collections-dellemc-openmanage-ome-discovery-module)
- [OME API Discovery with Python/PowerShell](https://github.com/dell/OpenManage-Enterprise/blob/main/docs/API.md#invoke-discover-device)
- [Dell's API documentation](https://developer.dell.com/apis)
- [RedFish Documentation](https://developer.dell.com/apis/2978/versions/7.xx/docs/0WhatsNew.md)

## Overview

There are two predominant workflows for automatically deploying and provisioning Dell servers.

1. Use [OpenManage Enterprise (OME). OME is free](https://www.dell.com/support/kbdoc/en-us/000175879/support-for-openmanage-enterprise).
   1. The auto deployment feature requires the OME Advanced license to be present on the iDRAC but this is usually added by default by Dell. In my personal experience, I've never seen a server sold without it in all my time at Dell. More info about the difference between the licenses is [here](https://infohub.delltechnologies.com/p/new-openmanage-enterprise-advanced-ready-to-bring-new-customer-benefits/). If this is a concern just ask whoever is selling you the server (whether it be Dell directly or a partner) to make sure they put the OME Advanced license on the server if they haven't already.
   2. I have seen two variations of how OME deploys the server depending on how you want the initial discovery to occur.
2. Manually via the Dell APIs.

### When to Use OpenManage Enterprise (OME) and When Not

Unless there is a compelling reason not to use OME, it makes life significantly easier and is probably the better solution. 

Potential good reasons to not do **automated deployment** with OME (I bolded the automated deployment bit because for reasons I explain below, you're still going to end up using OME):

 1. You are using Bare Metal Orchestrator (BMO) and have a workflow built there
 2. You have a significant investment in a multi-vendor deployment solution and already have the in-house personnel and talent up, running, and using this solution

**Benefits of doing this with OME:**

1. Dell is on the hook for support
2. Unless you're going to build an entire patch management framework from scratch, which is a very bad idea because new you are on the hook for making sure patches are applied in the correct order, handling failures, reporting, code maintenance, repository maintenance, and all the other not-so-fun things that come with a custom patch management framework, you are going to want to use OME for patch management anyway. 
   1. I've worked with the TELCOs, they use OME. I cannot think of a valid reason to ever re-invent this wheel.
   2. I am also assuming you are not so cruel to your administrators that in 2024 (or whenever you read this) as to make them do manual patching.
      1. Seriously though, manual patching is bad.
   3. This supports custom repos with [Update Manager Plugin](https://infohub.delltechnologies.com/p/update-manager-plugin-for-openmanage-enterprise-overview/)
3. OME will automatically take care of BIOS-config templating.
   1. Again, this is another function you will have to manually build and maintain if you don't use OME. I have personally done this one. It's doable, but requires a lot of tedious, boilerplate, code and you will have to write a bunch of logic to handle all the boarder cases you might encounter. This becomes particularly miserable if you have multiple different servers you have to independently account for with multiple different BIOS templates.
   2. Again, this is why TELCOs use OME
4. You don't have to maintain a custom patch repository if you are on the internet.
   1. If you are a government or other customer in a SCIF or other such facility see [Offline Updates with OpenManage Enterprise](../Offline%20Updates%20with%20OpenManage%20Enterprise/)
5. OME provides power monitoring
6. OME provides config diff tracking
7. OME gives you a one stop shop to monitoring to including grouping servers and applying policies to them based on those groups
8. OME provides a convenient panel for getting to all the iDRACs
9.  OME will track all your warranties

Those are just the common benefits, there are a bunch of niche things it does as well that don't apply to everyone (ex: ServiceNow integration).

## OME Workflow

There are two workflows I see with OME: one using server initiated discovery and one where you do discovery with some code framework and load that into OME. If you are in a Dell environment then you probably just want to go ahead and use server initiated discovery. It's one less thing you have to maintain and it again is supported by Dell end to end. If you have a multi-vendor environment and have to build a discovery framework regardless, it may make more sense to centralize discovery in your custom framework. I describe both below.

An important note on understanding how OME works: OME controls the servers over iDRAC's RedFish API. Most everything you could do directly to the iDRAC over RedFish, you can also do centrally with OME.

### Overview of Configuration for Both

See [this link](https://dl.dell.com/manuals/all-products/esuprt_software_int/esuprt_software_ent_systems_mgmt/dell-openmanage-enterprise_white-papers11_en-us.pdf) for a Dell whitepaper on auto deploy.

1. Configure OpenManage Enterprise (OME) with the BIOS templates you want.
   You’ll configure the BIOS templates by taking a representative server and extracting the BIOS from it. [OME has a function for doing this](https://www.dell.com/support/manuals/en-us/dell-openmanage-enterprise/ome-3.4_ug/create-a-template-from-a-reference-device?guid=guid-c4b89f0b-7e15-48f6-9210-3ea1e2f74c61&lang=en-us) so you just make one server look exactly the way you want the rest, point OME at it, it saves that config, then you make that your template.
2. Configure OME for auto deploy to include pointing it at whatever ISO you want to be deployed to the different target servers. See [this documentation](https://www.dell.com/support/manuals/en-us/dell-openmanage-enterprise/ome-3.4_ug/auto-deployment-of-configuration-on-yet-to-be-discovered-servers-or-chassis?guid=guid-4c0e00fb-fed3-443f-9ac8-66a0db461f0b&lang=en-us)
3. Create a list of service tags with your various servers and put them in a CSV file
4. Create the auto deployment targets in OME. See [this documentation](https://www.dell.com/support/manuals/en-us/dell-openmanage-enterprise/ome-3.4_ug/create-auto-deployment-targets?guid=guid-0777321e-9232-4e02-b16f-1932def39879&lang=en-us)
5. [Create the auto deployment targets in OME](https://www.dell.com/support/manuals/en-us/dell-openmanage-enterprise/ome-3.4_ug/create-auto-deployment-targets?guid=guid-0777321e-9232-4e02-b16f-1932def39879&lang=en-us). This will tie specific templates/ISOs to specific groups. Those groups will be assigned to servers based on their service tags and then automatically applied.
   1. ISO files are mounted via network path via either CIFs or NFS
6. Use either a custom discovery framework via APIs or configure Dell's Server Initiated Discovery to register the servers with OME
7. Turn on new servers and watch them build themselves from nothing
8. As an added bonus, configure firmware updates in OME and set it to automatically update on next reboot for patch management.
   1. You can maintain custom repositories with [Update Manager Plugin](https://infohub.delltechnologies.com/p/update-manager-plugin-for-openmanage-enterprise-overview/) or you can simply download latest (it does this by default)

### Overview of How it Works After Config

1. (for server initiated discovery) Server goes to DHCP for DNS server, DNS server has OME's IP address registered
2. Server gets registered in OME either via server initiated discovery or you have custom Ansible/API/other workflow that registers it in OME
3. Once the server's iDRAC is registered in OME, OME launches the auto deployment process based on the server's registered service tag
4. OME applies appropriate BIOS template
   1. This can include all the custom properties for MX chassis or storage for things like IOMs
5. OME mounts ISO file via CIFs/NFS to the server
6. Server boots up and your automation workflow continues from there. Kickstart, windows unattended installation, etc

### Using Server Initiated Discovery

Dell has a whitepaper on server initiated discovery [here](https://dl.dell.com/manuals/all-products/esuprt_software_int/esuprt_software_ent_systems_mgmt/dell-openmanage-enterprise_white-papers15_en-us.pdf).

Dell servers are factory shipped with server initiated discovery on. The way it works is the iDRAC will check DNS and if an entry for OME is present, iDRAC will automatically register itself with OME which then kicks off the automated deployment process.

See [here](https://www.dell.com/support/manuals/en-au/dell-openmanage-enterprise/ome_3.5_ug/discover-servers-automatically-by-using-the-server-initiated-discovery-feature?guid=guid-23bd252f-9651-410a-88de-3f332d748b55&lang=en-us) for instructions on how to enable it. We have a YouTube video available [here](https://www.youtube.com/watch?v=p3NGoSrk4xI).

### Using a Custom Discovery Workflow

If you don't use server initiated discovery you will need to build a custom harness for discovering the server. All of these ultimately leverage either iDRAC's or OMEs APIs.

- The best way to do this is with Ansible. Dell has an entire team dedicated to supporting the Ansible module. See [here](https://docs.ansible.com/ansible/latest/collections/dellemc/openmanage/ome_discovery_module.html#ansible-collections-dellemc-openmanage-ome-discovery-module) for the discovery module documentation.
- There is an example of how to do discovery via API with Python/PowerShell [here](https://github.com/dell/OpenManage-Enterprise/blob/main/docs/API.md#invoke-discover-device). You will need to modify this code based on your particular framework but the script itself provides a good starting place to build from.
- Dell's API documentation is [here](https://developer.dell.com/apis)
  - RedFish is [here](https://developer.dell.com/apis/2978/versions/7.xx/docs/0WhatsNew.md)
  - OpenManage's API is [here](https://developer.dell.com/apis/5898/versions/4.0.0/docs/Introduction.md)

## Entirely Custom Workflow

- [Discovery with Ansible](https://docs.ansible.com/ansible/latest/collections/dellemc/openmanage/ome_discovery_module.html#ansible-collections-dellemc-openmanage-ome-discovery-module)
- [OME API Discovery with Python/PowerShell](https://github.com/dell/OpenManage-Enterprise/blob/main/docs/API.md#invoke-discover-device)
- [Dell's API documentation](https://developer.dell.com/apis)
- [RedFish Documentation](https://developer.dell.com/apis/2978/versions/7.xx/docs/0WhatsNew.md)
- [OME API Docs](https://developer.dell.com/apis/5898/versions/4.0.0/docs/Introduction.md)
- [iDRAC RedFish Scripting Examples](https://github.com/dell/iDRAC-Redfish-Scripting)
- [Modifying BIOS Attributes](https://docs.ansible.com/ansible/latest/collections/dellemc/openmanage/idrac_bios_module.html#ansible-collections-dellemc-openmanage-idrac-bios-module)
- [Firmware Upgrade Module](https://docs.ansible.com/ansible/latest/collections/dellemc/openmanage/idrac_firmware_module.html#ansible-collections-dellemc-openmanage-idrac-firmware-module)
- [OS Deployment Module](https://docs.ansible.com/ansible/latest/collections/dellemc/openmanage/idrac_os_deployment_module.html#ansible-collections-dellemc-openmanage-idrac-os-deployment-module)

You will need way more than just the above. You will need to do all the job management because you will need to handle errors, you will need to do templating, you will need to create custom reporting, and a lot more.
