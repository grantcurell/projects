# Running Offline Updates with OME

1. Download [Dell Repository Manager](https://www.dell.com/support/driver/us/en/19/DriversDetails?driverid=v8ym0)
2. `chmod +x <binary name>` then run with `./<binary_name>`.
3. On Ubuntu Desktop, open terminal, run `sudo apt-get install xdg-utils firefox openjfx -y`
4. I used Apache to host my web server. My configuration is below.

        <VirtualHost *:80>
        # The ServerName directive sets the request scheme, hostname and port that
        # the server uses to identify itself. This is used when creating
        # redirection URLs. In the context of virtual hosts, the ServerName
        # specifies what hostname must appear in the request's Host: header to
        # match this virtual host. For the default virtual host (this file) this
        # value is not decisive as it is used as a last resort host regardless.
        # However, you must set it for any further virtual host explicitly.
        #ServerName www.example.com

        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/html
        Alias "/dell/" "/opt/dell/catelogs/"

        <Directory "/opt/dell/catelogs/">
                Options Indexes FollowSymLinks MultiViews
                AllowOverride None
                Order allow,deny
                allow from all
                Require all granted
        </Directory>

        # Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
        # error, crit, alert, emerg.
        # It is also possible to configure the loglevel for particular
        # modules, e.g.
        #LogLevel info ssl:warn

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        # For most configuration files from conf-available/, which are
        # enabled or disabled at a global level, it is possible to
        # include a line for only one particular virtual host. For example the
        # following line enables the CGI configuration for this host only
        # after it has been globally disabled with "a2disconf".
        #Include conf-available/serve-cgi-bin.conf
        </VirtualHost>

        # vim: syntax=apache ts=4 sw=4 sts=4 sr noet

5. I downloaded all the catelogs to /opt/dell/catelogs/fc640
6. You then have to go open the Dell EMC Repository Manager -> Export -> Export
   1. This has to be in the web server root! There is a bug in OME that causes it to send out the wrong URLs if the URI path requires forwardslashes. See [this post](https://www.dell.com/community/Dell-OpenManage-Essentials/Dell-OpenManage-Reports-TCP-Window-Full/m-p/7473117#M14933) for details on why.
   2. **WARNING** You have to download the Windows 64 bit versions of the updates for it to work! Even if you are using Linux the idrac only accepts the Windows EXE files.
7. Firmware compliance -> Catelog Management -> Add
   1. Share Address: <YOUR_UP> (nothing else)
   2. Catalog File Path: /catalog.xml (cannot have anything else)
8. Go back to Firmware Compliance -> Create Baseline
   1. Select your local catalog
   2. Give it a name
   3. Add the hosts you discovered
