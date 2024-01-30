# esrally (INCOMPLETE)

## My Environment

### CentOS Version Info

    CentOS Linux release 7.7.1908 (Core)
    NAME="CentOS Linux"
    VERSION="7 (Core)"
    ID="centos"
    ID_LIKE="rhel fedora"
    VERSION_ID="7"
    PRETTY_NAME="CentOS Linux 7 (Core)"
    ANSI_COLOR="0;31"
    CPE_NAME="cpe:/o:centos:centos:7"
    HOME_URL="https://www.centos.org/"
    BUG_REPORT_URL="https://bugs.centos.org/"

    CENTOS_MANTISBT_PROJECT="CentOS-7"
    CENTOS_MANTISBT_PROJECT_VERSION="7"
    REDHAT_SUPPORT_PRODUCT="centos"
    REDHAT_SUPPORT_PRODUCT_VERSION="7"

    CentOS Linux release 7.7.1908 (Core)
    CentOS Linux release 7.7.1908 (Core)

### Kernel Version Info

    [root@elk ~]# uname -a
    Linux hostname 3.10.0-1062.9.1.el7.x86_64 #1 SMP Fri Dec 6 15:49:49 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux

### Elasticsearch/Kibana Version Info

I used 6.8.5 to set this up.

I only used a single node for this setup.

## Installation

1. Run install `yum install -y python3`
2. Download Java 12 from [the Java archive](https://www.oracle.com/technetwork/java/javase/downloads/java-archive-javase12-5440181.html). You will unfortunately have to make an account.

3. Add the wandisco repo to install a current version of git. `vim /etc/yum.repos.d/wandisco-git.repo`. Add the below to the file.

        [wandisco-git]
        name=Wandisco GIT Repository
        baseurl=http://opensource.wandisco.com/centos/7/git/$basearch/
        enabled=1
        gpgcheck=1
        gpgkey=http://opensource.wandisco.com/RPM-GPG-KEY-WANdisco

4. Add their GPG keys with `rpm --import http://opensource.wandisco.com/RPM-GPG-KEY-WANdisco`
5. Run `yum install -y git gcc python3-devel`
6. Run `pip3 install esrally` to install Rally.
7. 