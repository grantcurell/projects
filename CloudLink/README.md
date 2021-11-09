# How Does CloudLink Work

## General Functioning

CloudLink provides encryption by using Microsoft BitLocker and dm-crypt ([How does dm-crypt work](https://www.linux.com/training-tutorials/how-encrypt-linux-file-system-dm-crypt/))for Linux to provide encryption.

CloudLink's VM encryption functionality enables you to use native OS encryption features to encrypt a machine's boot and data volumes in a multi tenant cloud environment. This encryption enables you to protect the integrity of the machine itself against unauthorized modifications.

CloudLink encrypts the machine boot and data volumes with unique keys that enterprise security administrators control. Neither cloud administrators nor other tenants in the cloud have access to the keys. By securing machines, you can define the security policy that must be met before passing the prestartup authorization, including verifying the integrity of the machine’s boot chain. This offers protection against tampering.

## Components

- CloudLink Center—The web-based interface for CloudLink that is used to manage machines that belong to the CloudLink environment (those machines on which CloudLink Agent has been installed). CloudLink Center:
  - Communicates with machines over Transport Layer Security (TLS)
  - Manages the encryption keys that are used to secure the boot volumes, data volumes, and devices for the machines
  - Configures the security policies
  - Monitors the security and operation events
  - Collects log data
- CloudLink Agent - The agent that runs on individual machines. It communicates with CloudLink Center for pre-startup authorization and decryption of BitLocker or dm-crypt encryption keys.

For Enterprise and PowerFlex—CloudLink Center is packaged as a virtual appliance that can be deployed in the enterprise on VMware ESXi or Microsoft Hyper-V. Download CloudLink Agent from CloudLink Center.

For Microsoft Azure or Azure Stack—CloudLink Center can be deployed from the Azure Gallery in a simple-to-deploy, self-contained image file that enables you to quickly start your business-critical operations by using CloudLink. Search the Azure Gallery for CloudLink to locate the image. Download CloudLink Agent from CloudLink Center

## Licensing

### General Licenses

- Evaluation license—This is a free trial license to test the CloudLink features. This license has an expiry date and is not allowed to be used in production. Use a subscription or a perpetual license that is purchased through Dell EMC for production purposes.
- Subscription license—This license expires on a predefined date and time. The subscription license period is for one, two, or three years only. Repurchase the subscription licenses at the end of their term.
- Perpetual license—This license never expires.

### License Types

- Encryption for Machines license—Licensed per machine for volume encryption. This license defines the number of machines, virtual, or bare metal, that can be protected using CloudLink Center.
- Encryption for Containers license—Enables data encryption for containers. A single Container license supports any number of Kubernetes clusters.
- Encryption for PowerFlex license—Encrypted capacity for PowerFlex
This license defines the total storage that can be encrypted using CloudLink Center.
- Key Management over [KMIP](https://wiki.openstack.org/wiki/KMIPclient) license—Licensed KMIP clients This license defines the number of KMIP clients that can be managed using CloudLink Center. With one Key Management over KMIP license you can create:
  - One KMIP Client
  - One CloudLink Center cluster
  - NOTE: To create additional KMIP Clients or CloudLink Center clusters, purchase additional Key Management over KMIP licenses.
- Key Management for SED license—Number of physical machines with SEDs. A single Key Management for SED license is used per physical machine regardless of the number of SEDs connected to that machine

## Installation Notes

- I followed the guide here for VMWare https://docs.delltechnologies.com/bundle/P_DG_CL_701/page/GUID-1EDFBE27-3218-43AD-9449-24374D5FE1F6.html
- The default user for the webui is secadmin
- Before I added VMs to my cluster I created a [machine group](https://docs.delltechnologies.com/bundle/P_DG_CL_701/page/GUID-516FA105-44B6-409B-918B-008006B19466.html) to put them in
- Make sure you add approved networks with IP ranges before installation or adding machines will fail with `IP address (192.168.1.95) not in group's approved networks`
  - Alternatively you will have to go to machines and accept the machine
- To install in standard mode on Linux run `sudo ./clagent.sh -S 192.168.1.86 -G cf41-f71e` where -S specifies the server and -G is the group key
## Questions

- What is vault mode?

![](images/2021-11-09-07-47-09.png)

- What are these three unique manual passcodes?

![](images/2021-11-09-07-49-28.png)

- Can it encrypt data in motion?
- How does the licensing work if you have multiple clusters?