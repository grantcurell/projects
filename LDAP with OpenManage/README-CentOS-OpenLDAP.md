# Setting Up OpenLDAP with OpenManage

## My Environment

### CentOS Version

    CentOS Linux release 8.2.2004 (Core)
    NAME="CentOS Linux"
    VERSION="8 (Core)"
    ID="centos"
    ID_LIKE="rhel fedora"
    VERSION_ID="8"
    PLATFORM_ID="platform:el8"
    PRETTY_NAME="CentOS Linux 8 (Core)"
    ANSI_COLOR="0;31"
    CPE_NAME="cpe:/o:centos:centos:8"
    HOME_URL="https://www.centos.org/"
    BUG_REPORT_URL="https://bugs.centos.org/"

    CENTOS_MANTISBT_PROJECT="CentOS-8"
    CENTOS_MANTISBT_PROJECT_VERSION="8"
    REDHAT_SUPPORT_PRODUCT="centos"
    REDHAT_SUPPORT_PRODUCT_VERSION="8"

    CentOS Linux release 8.2.2004 (Core)
    CentOS Linux release 8.2.2004 (Core)

### IPA Version

      [root@centos ~]# ipa --version
      VERSION: 4.8.4, API_VERSION: 2.235

### OpenManage Version

      Version 3.5.0 (Build 60)

## Helpful Resources

[Dell Tutorial](https://www.youtube.com/watch?v=pOojNfNbQ80&ab_channel=DellEMCSupport)

[Logs Explained](https://access.redhat.com/documentation/en-us/red_hat_directory_server/10/html/configuration_command_and_file_reference/logs-reference)

[LDAP Result Codes](https://access.redhat.com/documentation/en-us/red_hat_directory_server/10/html/configuration_command_and_file_reference/LDAP_Result_Codes)

[Helpful Post on Bind DN](https://serverfault.com/questions/616698/in-ldap-what-exactly-is-a-bind-dn)

[OpenManage User's Guide](https://topics-cdn.dell.com/pdf/dell-openmanage-enterprise_users-guide15_en-us.pdf)

## Install Instructions

1. Install CentOS8
      1.I installed CentOS minimal
      2.Make sure NTP is working correctly
2. Install OpenManage
3. For the OpenLDAP setup I followed [Install and Setup OpenLDAP on CentOS 8 by koromicha](https://kifarunix.com/install-and-setup-openldap-on-centos-8/#:~:text=To%20compile%20OpenLDAP%20on%20CentOS,you%20can%20proceed%20with%20installation.&text=With%20configure%20script%2C%20you%20can,various%20options%20while%20building%20OpenLDAP.)
4. I want the current version of OpenLDAP so I'll be building it from source.
5. Install dependencies with `dnf install -y cyrus-sasl-devel make libtool autoconf libtool-ltdl-devel openssl-devel libdb-devel tar gcc perl perl-devel wget vim`
6. Create non privileged system user: `useradd -r -M -d /var/lib/openldap -u 55 -s /usr/sbin/nologin ldap`
7. Pull tarball `wget https://www.openldap.org/software/download/OpenLDAP/openldap-release/openldap-2.4.54.tgz && tar xzf openldap-2.4.54.tgz && cd openldap-2.4.54`
8. Build and install OpenLDAP `./configure --prefix=/usr --sysconfdir=/etc --disable-static --enable-debug --with-tls=openssl --with-cyrus-sasl --enable-dynamic --enable-crypt --enable-spasswd --enable-slapd --enable-modules --enable-rlookups --enable-backends=mod --disable-ndb --disable-sql --disable-shell --disable-bdb --disable-hdb --enable-overlays=mod && make depend && make -j2 && make install`
9. Configure OpenLDAP `mkdir /var/lib/openldap /etc/openldap/slapd.d && chown -R ldap:ldap /var/lib/openldap && chown root:ldap /etc/openldap/slapd.conf`
10. Add an OpenLDAP systemd service `vim /etc/systemd/system/slapd.service`

        [Unit]
        Description=OpenLDAP Server Daemon
        After=syslog.target network-online.target
        Documentation=man:slapd
        Documentation=man:slapd-mdb

        [Service]
        Type=forking
        PIDFile=/var/lib/openldap/slapd.pid
        Environment="SLAPD_URLS=ldap:/// ldapi:/// ldaps:///"
        Environment="SLAPD_OPTIONS=-F /etc/openldap/slapd.d"
        ExecStart=/usr/libexec/slapd -u ldap -g ldap -h ${SLAPD_URLS} $SLAPD_OPTIONS

        [Install]
        WantedBy=multi-user.target

11. Check if your version of sudo supports lday with `sudo -V |  grep -i "ldap"` and confirm the below lines are present:

            ldap.conf path: /etc/sudo-ldap.conf
            ldap.secret path: /etc/ldap.secret

12. Make sure LDAP sudo schema is available with `rpm -ql sudo |  grep -i schema.openldap`. You should see `/usr/share/doc/sudo/schema.OpenLDAP`
13. Run:

            cp /usr/share/doc/sudo/schema.OpenLDAP  /etc/openldap/schema/sudo.schema
            cat << 'EOL' > /etc/openldap/schema/sudo.ldif
            dn: cn=sudo,cn=schema,cn=config
            objectClass: olcSchemaConfig
            cn: sudo
            olcAttributeTypes: ( 1.3.6.1.4.1.15953.9.1.1 NAME 'sudoUser' DESC 'User(s) who may  run sudo' EQUALITY caseExactIA5Match SUBSTR caseExactIA5SubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 )
            olcAttributeTypes: ( 1.3.6.1.4.1.15953.9.1.2 NAME 'sudoHost' DESC 'Host(s) who may run sudo' EQUALITY caseExactIA5Match SUBSTR caseExactIA5SubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 )
            olcAttributeTypes: ( 1.3.6.1.4.1.15953.9.1.3 NAME 'sudoCommand' DESC 'Command(s) to be executed by sudo' EQUALITY caseExactIA5Match SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 )
            olcAttributeTypes: ( 1.3.6.1.4.1.15953.9.1.4 NAME 'sudoRunAs' DESC 'User(s) impersonated by sudo (deprecated)' EQUALITY caseExactIA5Match SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 )
            olcAttributeTypes: ( 1.3.6.1.4.1.15953.9.1.5 NAME 'sudoOption' DESC 'Options(s) followed by sudo' EQUALITY caseExactIA5Match SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 )
            olcAttributeTypes: ( 1.3.6.1.4.1.15953.9.1.6 NAME 'sudoRunAsUser' DESC 'User(s) impersonated by sudo' EQUALITY caseExactIA5Match SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 )
            olcAttributeTypes: ( 1.3.6.1.4.1.15953.9.1.7 NAME 'sudoRunAsGroup' DESC 'Group(s) impersonated by sudo' EQUALITY caseExactIA5Match SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 )
            olcObjectClasses: ( 1.3.6.1.4.1.15953.9.2.1 NAME 'sudoRole' SUP top STRUCTURAL DESC 'Sudoer Entries' MUST ( cn ) MAY ( sudoUser $ sudoHost $ sudoCommand $ sudoRunAs $ sudoRunAsUser $ sudoRunAsGroup $ sudoOption $ description ) )
            EOL
            mv /etc/openldap/slapd.ldif /etc/openldap/slapd.ldif.bak


14. `vim /etc/openldap/slapd.ldif`

            dn: cn=config
            objectClass: olcGlobal
            cn: config
            olcArgsFile: /var/lib/openldap/slapd.args
            olcPidFile: /var/lib/openldap/slapd.pid

            dn: cn=schema,cn=config
            objectClass: olcSchemaConfig
            cn: schema

            dn: cn=module,cn=config
            objectClass: olcModuleList
            cn: module
            olcModulepath: /usr/libexec/openldap
            olcModuleload: back_mdb.la

            include: file:///etc/openldap/schema/core.ldif
            include: file:///etc/openldap/schema/cosine.ldif
            include: file:///etc/openldap/schema/nis.ldif
            include: file:///etc/openldap/schema/inetorgperson.ldif
            include: file:///etc/openldap/schema/ppolicy.ldif
            include: file:///etc/openldap/schema/sudo.ldif

            dn: olcDatabase=frontend,cn=config
            objectClass: olcDatabaseConfig
            objectClass: olcFrontendConfig
            olcDatabase: frontend
            olcAccess: to dn.base="cn=Subschema" by * read
            olcAccess: to * 
            by dn.base="gidNumber=0+uidNumber=0,cn=peercred,cn=external,cn=auth" manage 
            by * none

            dn: olcDatabase=config,cn=config
            objectClass: olcDatabaseConfig
            olcDatabase: config
            olcRootDN: cn=config
            olcAccess: to * 
            by dn.base="gidNumber=0+uidNumber=0,cn=peercred,cn=external,cn=auth" manage 
            by * none

15. Make sure `slapadd -n 0 -F /etc/openldap/slapd.d -l /etc/openldap/slapd.ldif -u` runs without error
16. Run `slapadd -n 0 -F /etc/openldap/slapd.d -l /etc/openldap/slapd.ldif && chown -R ldap:ldap /etc/openldap/slapd.d/* && systemctl daemon-reload && systemctl enable --now slapd && systemctl status slapd`
17. SLAPD LOGGING NOT WORKING
19. Run `slappasswd` and note the hash output.
### Helpful Commands

To start the IPA service use `ipactl start|stop|restart`. You can check the status with `ipactl status`.
