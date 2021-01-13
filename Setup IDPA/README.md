# Setup IDPA

## Version

    DP4400

## Current Documentation

[Manual](https://dl.dell.com/content/docu97727_Integrated_Data_Protection_Appliance_2.5_Product_Guide.pdf?language=en_US)

[Setup Guide](https://www.delltechnologies.com/el-gr/collaterals/unauth/technical-guides-support-information/2019/06/docu94051.pdf)

### Notes

IDPA DP4400 model is a hyperconverged, 2U system that a user can install and configure onsite. The DP4400 includes a virtual edition of Avamar server (AVE) as the Backup Server node, a virtual edition of Data Domain system (DDVE) as the Protection Storage node, Cloud Disaster Recovery, IDPA System Manager as a centralized system management, an Appliance Configuration Manager(ACM) for simplified configuration and upgrades, Search, Reporting and Analytics, and a compute node that hosts the virtual components and the software.


## Components

### Appliance administration

The ACM provides a web-based interface for configuring, monitoring, and upgrading the appliance.The ACM dashboard displays a summary of the configuration of the individual components. It also enables the administrators to monitor the appliance, modify configuration details such as expanding the Data Domain disk capacity, change the common password for the appliance, change LDAP settings, update customer information, and change the values in the General Settings panel. The ACM dashboard enables you to upgrade the system and its components. It also displays the health information of the Appliance Server and VMware components.

### Backup administration

The IDPA uses Avamar Virtual Edition (AVE) servers fo-r the DP5xxx and DP4xxx models and a physical Avamar for DP8xxxx to perform backup operations, with the data being stored in a Data Domain system. Generally, when using the Avamar Administrator Management Console, all Avamar servers look and behave the same. The main differences among the Avamar server configurations are the number of nodes and disk drives that are reported in the Server Monitor console. You can also add an Avamar NDMP Accelerator (one NDMP Accelerator node is supported in DP4400 and DP5800) to enable backup and recovery of NAS systems. For more information about the configuration details, see Table 3. Configuration options for each model on page 9. The Avamar NDMP Accelerator uses the network data management protocol (NDMP) to enable backup and recovery of network attached storage (NAS) systems. The accelerator  performs NDMP processing and then sends the data directly to the Data Domain Server (Data Domain Virtual Edition Storage).

## Instructions

1. Set up 12 continuous IP addresses in DNS. They must be in the same subnet. idrac can be separate
2. 