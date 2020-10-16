# Setting Up OpenLDAP with OpenManage

## My Environment

### CentOS Version

      grant@ubuntuldap:~$ cat /etc/*-release
      DISTRIB_ID=Ubuntu
      DISTRIB_RELEASE=20.04
      DISTRIB_CODENAME=focal
      DISTRIB_DESCRIPTION="Ubuntu 20.04.1 LTS"
      NAME="Ubuntu"
      VERSION="20.04.1 LTS (Focal Fossa)"
      ID=ubuntu
      ID_LIKE=debian
      PRETTY_NAME="Ubuntu 20.04.1 LTS"
      VERSION_ID="20.04"
      HOME_URL="https://www.ubuntu.com/"
      SUPPORT_URL="https://help.ubuntu.com/"
      BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
      PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
      VERSION_CODENAME=focal
      UBUNTU_CODENAME=focal


### OpenLDAP Version

      [root@centos ~]# ipa --version
      VERSION: 4.8.4, API_VERSION: 2.235

### OpenManage Version

      Version 3.5.0 (Build 60)

## Helpful Resources

[Dell Tutorial](https://www.youtube.com/watch?v=pOojNfNbQ80&ab_channel=DellEMCSupport)

[LDAP Result Codes](https://access.redhat.com/documentation/en-us/red_hat_directory_server/10/html/configuration_command_and_file_reference/LDAP_Result_Codes)

[Helpful Post on Bind DN](https://serverfault.com/questions/616698/in-ldap-what-exactly-is-a-bind-dn)

[OpenManage User's Guide](https://topics-cdn.dell.com/pdf/dell-openmanage-enterprise_users-guide15_en-us.pdf)

## Install Instructions

1. I followed [this tutorial](https://medium.com/@benjamin.dronen/installing-openldap-and-phpldapadmin-on-ubuntu-20-04-lts-7ef3ca40dc00) to set up OpenLDAP on Ubuntu
2. 