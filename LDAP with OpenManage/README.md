# Setting Up FreeIPA with OpenManage

Conclusion: Currently FreeIPA isn't supported or tested against OpenManage. See [the User's Guide](https://topics-cdn.dell.com/pdf/dell-openmanage-enterprise_users-guide15_en-us.pdf) page 137.

I'm going to try it with OpenLDAP

## My Environment

### RHEL Version

      NAME="Red Hat Enterprise Linux"
      VERSION="8.2 (Ootpa)"
      ID="rhel"
      ID_LIKE="fedora"
      VERSION_ID="8.2"
      PLATFORM_ID="platform:el8"
      PRETTY_NAME="Red Hat Enterprise Linux 8.2 (Ootpa)"
      ANSI_COLOR="0;31"
      CPE_NAME="cpe:/o:redhat:enterprise_linux:8.2:GA"
      HOME_URL="https://www.redhat.com/"
      BUG_REPORT_URL="https://bugzilla.redhat.com/"

      REDHAT_BUGZILLA_PRODUCT="Red Hat Enterprise Linux 8"
      REDHAT_BUGZILLA_PRODUCT_VERSION=8.2
      REDHAT_SUPPORT_PRODUCT="Red Hat Enterprise Linux"
      REDHAT_SUPPORT_PRODUCT_VERSION="8.2"
      Red Hat Enterprise Linux release 8.2 (Ootpa)
      Red Hat Enterprise Linux release 8.2 (Ootpa)

### FreeIPA Version

      [root@centos ~]# ipa --version
      VERSION: 4.8.4, API_VERSION: 2.235

### OpenManage Version

      Version 3.4.1 (Build 24)

## Helpful Resources

[Dell Tutorial](https://www.youtube.com/watch?v=pOojNfNbQ80&ab_channel=DellEMCSupport)

[Logs Explained](https://access.redhat.com/documentation/en-us/red_hat_directory_server/10/html/configuration_command_and_file_reference/logs-reference)

[LDAP Result Codes](https://access.redhat.com/documentation/en-us/red_hat_directory_server/10/html/configuration_command_and_file_reference/LDAP_Result_Codes)

[Helpful Post on Bind DN](https://serverfault.com/questions/616698/in-ldap-what-exactly-is-a-bind-dn)

## Install Instructions

1. Install RHEL
2. Change hostname
   1. `hostname freeipa.grant.lan && hostnamectl set-hostname freeipa.grant.lan`
   2. Change in /etc/hostname
   3. Configure DNS to return for this hostname. Double check with `dig +short freeipa.grant.lan A && dig +short -x 192.168.1.95`
5. Follow [RHEL's instructions](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html-single/installing_identity_management/index)
   1. I used Chapter 5 for primary installation
6. 6. Run `kinit admin` - this allows you to use the command line tools otherwise they'll complain about kerberos.
7.  Log into FreeIPA server at `https://<your_hostname>`. In my case, Windows popped up a username and password prompt. That prompt didn't work - I had to exit it and then log into the webGUI.
8.  Go to Users and then directory services in OpenManage. I used the following:
    1.  Note: You can get the Bind DN by running `ldapsearch` from the command line.
9.  Create a new user and new group in the UI and assign the new user to the new group.
10. Install OpenManage
11. Go to Application Settings -> Directory Services

![](images/2020-10-21-11-24-14.png)

12.  Substitute with your values and then click test. I wasn't able to get this to work with the generic admin user. In the test screen I used that new user to connect to directory services

### Helpful Commands

To start the IPA service use `ipactl start|stop|restart`. You can check the status with `ipactl status`.

## Errors Encountered

### Failure to Import Groups

1. I used the settings defined here:

![](images/2020-10-21-11-24-14.png)

2. When I went to import the users from a group I received the following:

![](images/2020-10-21-13-22-09.png)

The code in question:

![](images/2020-10-21-13-23-00.png)

Below was the value of `u` at runtime:

      [
      {
            "userTypeId":2,
            "objectGuid":null,
            "objectSid":null,
            "directoryServiceId":13483,
            "name":"grantgroup",
            "password":"",
            "userName":"grantgroup",
            "roleId":"10",
            "locked":false,
            "isBuiltin":false,
            "enabled":true
      }
      ]

## Notes

Bind DN he did: uid=<name>,cn=users,cn=accounts,dc=grant,dc=lan
cn=accounts,dc=grant,dc=lan