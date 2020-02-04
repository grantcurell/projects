# Bug Write Up

sfd_init.sh fails because it incorrectly checks ntp status. The failure condition can be replicated by using an ntp server
of `time.google.com` on template import for the OVA.

## Version

### SFD

SFD version is 1.1.0.

### Ubuntu

    admin@sfd.local@sfd:~$ cat /etc/*-release
    DISTRIB_ID=Ubuntu
    DISTRIB_RELEASE=16.04
    DISTRIB_CODENAME=xenial
    DISTRIB_DESCRIPTION="Ubuntu 16.04.6 LTS"
    NAME="Ubuntu"
    VERSION="16.04.6 LTS (Xenial Xerus)"
    ID=ubuntu
    ID_LIKE=debian
    PRETTY_NAME="Ubuntu 16.04.6 LTS"
    VERSION_ID="16.04"
    HOME_URL="http://www.ubuntu.com/"
    SUPPORT_URL="http://help.ubuntu.com/"
    BUG_REPORT_URL="http://bugs.launchpad.net/ubuntu/"
    VERSION_CODENAME=xenial
    UBUNTU_CODENAME=xenial

## Suggested Patch

### Patch

    admin@sfd.local@sfd:~$ diff -c sfd_init.sh.original sfd_init.sh.patch
    *** sfd_init.sh.original        2020-02-04 21:58:22.327755522 +0000
    --- sfd_init.sh.patch   2020-02-04 21:59:38.651751964 +0000
    ***************
    *** 188,194 ****
        echo "Checking if NTP is configured."
        until [[ $cnt -ge $max_tries ]]
        do
    !       ntpq -pn | awk '{print $2}' | xargs | grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}|PPS|GPS|LOCAL|LOCL"
            [[ "$?" -eq 0 ]] && echo "NTP synchronized successfully." && return 0
            cnt=$[$cnt+1]
            echo "Waiting for NTP to get configured. Sleeping for 10 seconds..."
    --- 188,194 ----
        echo "Checking if NTP is configured."
        until [[ $cnt -ge $max_tries ]]
        do
    !       ntpq -pn | awk '{print $1}' | sed -n '/^\*/p'
            [[ "$?" -eq 0 ]] && echo "NTP synchronized successfully." && return 0
            cnt=$[$cnt+1]
            echo "Waiting for NTP to get configured. Sleeping for 10 seconds..."

### Explanation

See below for a detailed explanation of my troubleshooting and additional information.

Based on the regex looking for an IP I'm guessing the intent was to verify that the server is synched to a remote NTP server. However there are two problems. The first is that it is looking at the refid (column 2) which is not the server you are synched to, but the server that the server you are pointing at is synched to. Second, there is no guarentee that an IP address will be in this column (or PPS/GPS/LOCAL/LOCL). This was my case. Instead, I would check for the line that has the synchronized server (starts with *). Using `ntpq -pn | awk '{print $1}' | sed -n '/^\*/p'`. You don't really need to check beyond that because it won't synchronize unless everything is working. Though if you want to take it a step further you could do: `ntpq -pn | awk '{print $1}' | sed -n '/^\*/p' | sed 's/\*//g' | grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}|PPS|GPS|LOCAL|LOCL"`.

## Detailed Explanation

- Page 17 step 1 of [the manual](https://downloads.dell.com/manuals/all-products/esuprt_networking_int/esuprt_networking_mgmt_software/smart-fabric-director_users-guide_en-us.pdf) doesn't work. There is no web server listening. It looks like on the first run the SFD service failed. There is no obvious log information output from the service. Suggest that `sfd_init.sh` print the log path to stdout on failure so that getting the service status will more obviously provide direction on where the problem is.

        # Dumped listening ports
        admin@sfd.local@sfd:~$ ss -ltn
        State       Recv-Q Send-Q                                  Local Address:Port                                                 Peer Address:Port
        LISTEN      0      128                                         127.0.0.1:39125                                                           *:*
        LISTEN      0      128                                                 *:22                                                              *:*
        LISTEN      0      128                                                :::9100                                                           :::*
        LISTEN      0      128                                                :::5555                                                           :::*
        LISTEN      0      128                                                :::22                                                             :::*

        # Checked service status after figuring out SFD ran a service
        admin@sfd.local@sfd:~$ systemctl status sfd
        ● sfd.service - NFC Bootstrap Service
        Loaded: loaded (/etc/systemd/system/sfd.service; enabled; vendor preset: enabled)
        Active: failed (Result: exit-code) since Tue 2020-02-04 20:38:10 UTC; 18min ago
        Main PID: 1327 (code=exited, status=1/FAILURE)

- Entire system will hard fail if NTP cannot start. I realized this is the cause of the failure above. This should not be the default behavior. Should continue and issue a warning. Most customers working on servers would not know how to troubleshoot this.

        ● ntp.service - LSB: Start NTP daemon
        Loaded: loaded (/etc/init.d/ntp; bad; vendor preset: enabled)
        Active: active (running) since Wed 2020-02-05 03:50:34 UTC; 10s ago
            Docs: man:systemd-sysv-generator(8)
        Process: 2235 ExecStop=/etc/init.d/ntp stop (code=exited, status=0/SUCCESS)
        Process: 2248 ExecStart=/etc/init.d/ntp start (code=exited, status=0/SUCCESS)
            Tasks: 2
        Memory: 1.5M
            CPU: 12ms
        CGroup: /system.slice/ntp.service
                └─2260 /usr/sbin/ntpd -p /var/run/ntpd.pid -g -u 112:117

        Feb 05 03:50:34 sfd ntpd[2260]: Listen and drop on 1 v4wildcard 0.0.0.0:123
        Feb 05 03:50:34 sfd ntpd[2260]: Listen normally on 2 lo 127.0.0.1:123
        Feb 05 03:50:34 sfd ntpd[2260]: Listen normally on 3 ens192 192.168.1.31:123
        Feb 05 03:50:34 sfd ntpd[2260]: Listen normally on 4 lo [::1]:123
        Feb 05 03:50:34 sfd ntpd[2260]: Listening on routing socket on fd #21 for interface updates
        Feb 05 03:50:35 sfd ntpd[2260]: Soliciting pool server 216.239.35.12
        Feb 05 03:50:36 sfd ntpd[2260]: Soliciting pool server 216.239.35.4
        Feb 05 03:50:37 sfd ntpd[2260]: Soliciting pool server 216.239.35.0
        Feb 05 03:50:38 sfd ntpd[2260]: Soliciting pool server 216.239.35.8
        Feb 05 03:50:39 sfd ntpd[2260]: Soliciting pool server 2001:4860:4806::
        -----RESTART NTP - END-----
        Checking if NTP service is running.
        NTP service is running.
        Checking if NTP is configured.
        Waiting for NTP to get configured. Sleeping for 10 seconds...
        
        ... SNIP ...

        Waiting for NTP to get configured. Sleeping for 10 seconds...
        NTP failed to get synced.
        NTP config failed


        # This failure seems to be erroneous. Checking the NTP service confirms it is working.
        admin@sfd.local@sfd:~$ systemctl status ntp
        ● ntp.service - LSB: Start NTP daemon
        Loaded: loaded (/etc/init.d/ntp; bad; vendor preset: enabled)
        Active: active (running) since Wed 2020-02-05 03:50:34 UTC; 6h left
            Docs: man:systemd-sysv-generator(8)
        Process: 2235 ExecStop=/etc/init.d/ntp stop (code=exited, status=0/SUCCESS)
        Process: 2248 ExecStart=/etc/init.d/ntp start (code=exited, status=0/SUCCESS)
            Tasks: 2
        Memory: 1.5M
            CPU: 81ms
        CGroup: /system.slice/ntp.service
                └─2260 /usr/sbin/ntpd -p /var/run/ntpd.pid -g -u 112:117
        admin@sfd.local@sfd:~$ ntpstat
        The program 'ntpstat' is currently not installed. You can install it by typing:
        sudo apt install ntpstat
        admin@sfd.local@sfd:~$ ntp -qn
        No command 'ntp' found, but there are 21 similar ones
        ntp: command not found
        admin@sfd.local@sfd:~$ ntpq -pn
            remote           refid      st t when poll reach   delay   offset  jitter
        ==============================================================================
        time.google.com .POOL.          16 p    -   64    0    0.000    0.000   0.000
        +216.239.35.12   .GOOG.           1 u   54   64  375   64.340  -91.086   8.997
        *216.239.35.4    .GOOG.           1 u   62   64  377   62.412  -83.944   8.385
        +216.239.35.0    .GOOG.           1 u   42   64  377   63.484  -83.978  10.080
        -216.239.35.8    .GOOG.           1 u   21   64  377   72.245  -73.087  15.674

- Problem isolated to:

        max_tries=30 # check counter till 30. (total 300 seconds)
        echo "Checking if NTP is configured."
        until [[ $cnt -ge $max_tries ]]
        do
        ntpq -pn | awk '{print $2}' | xargs | grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}|PPS|GPS|LOCAL|LOCL"
        [[ "$?" -eq 0 ]] && echo "NTP synchronized successfully." && return 0
        cnt=$[$cnt+1]
        echo "Waiting for NTP to get configured. Sleeping for 10 seconds..."
        sleep 10
        done

- The offending line is `ntpq -pn | awk '{print $2}' | xargs | grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}|PPS|GPS|LOCAL|LOCL"`. `ntpq -pn` has output formatted like this:

        admin@sfd.local@sfd:~$ ntpq -pn
        remote           refid      st t when poll reach   delay   offset  jitter
        ==============================================================================
        time.google.com .POOL.          16 p    -   64    0    0.000    0.000   0.000
        +216.239.35.12   .GOOG.           1 u   54   64  375   64.340  -91.086   8.997
        *216.239.35.4    .GOOG.           1 u   62   64  377   62.412  -83.944   8.385
        +216.239.35.0    .GOOG.           1 u   42   64  377   63.484  -83.978  10.080
        -216.239.35.8    .GOOG.           1 u   21   64  377   72.245  -73.087  15.674

- Based on the regex looking for an IP I'm guessing the intent was to verify that the server is synched to a remote NTP server. However there are two problems. The first is that it is looking at the refid which is not the server you are synched to, but the server that the server you are pointing at is synched to. Second, there is no guarentee that an IP address will be in this column (or PPS/GPS/LOCAL/LOCL). This was my case. See below for my `ntpq -pn` results. Instead, I would check for the line that has the synchronized server (starts with *). Using `ntpq -pn | awk '{print $1}' | sed -n '/^\*/p'`. You don't really need to check beyond that because it won't synchronize unless everything is working. Though if you want to take it a step further you could do: `ntpq -pn | awk '{print $1}' | sed -n '/^\*/p' | sed 's/\*//g' | grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}|PPS|GPS|LOCAL|LOCL"`.

### My ntpq -pn with time.google.com as my server

        admin@sfd.local@sfd:~$ ntpq -pn
            remote           refid      st t when poll reach   delay   offset  jitter
        ==============================================================================
        time.google.com .POOL.          16 p    -   64    0    0.000    0.000   0.000
        *216.239.35.12   .GOOG.           1 u   38   64  377   67.370   -0.549  23.161
        +216.239.35.4    .GOOG.           1 u   29   64  377   75.466   -1.691  22.089
        +216.239.35.0    .GOOG.           1 u   36   64  377   67.731   -1.434  24.201
        +216.239.35.8    .GOOG.           1 u   38   64  377   76.705   -0.042  22.436
