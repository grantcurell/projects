# Environment

## CentOS Version Info

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

## Kernel Version Info

    [root@elk ~]# uname -a
    Linux hostname 3.10.0-1062.9.1.el7.x86_64 #1 SMP Fri Dec 6 15:49:49 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux

## Elasticsearch/Kibana Version Info

I used 6.8.5 to set this up.

I only used a single node for this setup.

# Install Elasticsearch

1. Run `yum update -y && reboot` to make sure you are up to date
2. Begin by installing Java with `yum install -y java-1.8.0-openjdk`
3. Install Eleasticsearch with `yum install -y https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.8.5.rpm`
4. Edit the Elasticsearch configuration at `/etc/elasticsearch/elasticsearch.yml` and change the line `network.host` to have `0.0.0.0`
5. Start and enable the Elasticsearch service with `systemctl start elasticsearch && systemctl enable elasticsearch`

# Install Kibana

1. Install Kibana with `yum install -y https://artifacts.elastic.co/downloads/kibana/kibana-6.8.5-x86_64.rpm`
2. 