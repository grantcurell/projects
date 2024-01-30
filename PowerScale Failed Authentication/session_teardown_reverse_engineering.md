# How Does Session Teardown Work?

I received a question about how the PowerScale does session teardown so below I walk through a mid-level overview of what that looks like. PowerScale leverages Apache so let's first understand what session teardown looks like from the webserver perspective.

## Session Teardown in Apache

A highly detailed technical explanation of how Apache server handles session teardown, leading to a 204 response, involves understanding both the HTTP protocol and the specific implementation of session management in Apache.

### HTTP Protocol and the 204 Response

- **204 No Content**: In HTTP, a 204 status code indicates that the server has successfully processed the request, but is not returning any content. This is often used in situations where the server's response itself is not important, but the confirmation of successful processing is.

1. **Request Reception**: When a request to terminate a session (typically a DELETE request) is received, Apache first parses and interprets the HTTP request.
2. **Session Identification**: Apache identifies the session to be terminated. This is done with a session identifier.
3. **Session Management**: Apache uses modules for session management. These modules are responsible for creating, maintaining, and destroying sessions. When a session teardown is requested, the relevant module locates the session in its storage (which could be memory, a database, etc.).
4. **Session Validation**: Before proceeding with the teardown, Apache checks if the session exists and whether the client making the request has the right to terminate it.
5. **Resource Cleanup**: Upon successful validation, Apache instructs the session management module to release any resources associated with the session. This includes things like freeing memory, deleting session data from any running applications, and revoking authentication tokens.
6. **Session Destruction**: The session is then marked for destruction. This means it's effectively invalidated and cannot be used for further requests.
7. **Client Notification**: After the session is terminated, Apache sends a response back to the client. If there is no additional content to return (which is typical for session teardown), a 204 No Content response is used. This response is merely an acknowledgment that the request was successfully processed and the session was terminated.
8. **Logging and Monitoring**: Apache logs this interaction for administrative and security purposes. This could include information about the request, the client IP, the session identifier, and the outcome of the operation.

To demonstrate this I wrote [trace_teardown.py](./trace_teardown.py). It sets up a session with the PowerScale and then tears it down. Now we can't see the guts of the PowerScale with this code (I'll get to that) but we can see all the Apache-side handling.

```
C:\Users\grant\AppData\Local\Programs\Python\Python310\python.exe "C:\Users\grant\Documents\code\grantcurell.github.io\docs\PowerScale Failed Authentication\trace_teardown.py" 
DEBUG:__main__:Attempting to authenticate and create a session...
DEBUG:urllib3.connectionpool:Starting new HTTPS connection (1): 10.10.25.80:8080
DEBUG:urllib3.connectionpool:https://10.10.25.80:8080 "POST /session/1/session HTTP/1.1" 201 104
DEBUG:__main__:Authentication response: 201, {"services":["platform","namespace"],"timeout_absolute":14400,"timeout_inactive":900,"username":"root"}

DEBUG:__main__:Session successfully created. Cookies: {'isicsrf': '25cd0346-4204-4c5d-be1d-49630c78c4ff', 'isisessid': 'eyJhbGciOiJQUzUxMiJ9.eyJhdWQiOlsicGxhdGZvcm0iLCJuYW1lc3BhY2UiXSwiZXhwIjoxNzAxMjA5NDM4LCJpYXQiOjE3MDExOTUwMzgsIm9uZWZzL2NzcmYiOiIyNWNkMDM0Ni00MjA0LTRjNWQtYmUxZC00OTYzMGM3OGM0ZmYiLCJvbmVmcy9pcCI6IjE3Mi4xNi41LjE1NSIsIm9uZWZzL25vbmNlIjozOTM4NzI5NDg2NTQ2MDY1NjU2LCJvbmVmcy9zZXNzaW9uIjoiZThkYzYyM2ItOWM5Yy00YmE3LWE2MjAtYzQzZTdkNzBhMzlhIiwib25lZnMvdWEiOiJweXRob24tcmVxdWVzdHMvMi4yOC4xIiwib25lZnMvemlkIjoxLCJzdWIiOiJyb290In0K.nnaDPBOw6ZSHT66mguImZZL57PsMkodUG9S2Nop0_B3r3oSwgX-1CkL4R70_oGRDMPztaskMOVSbc0YsvHXERI9IqEdE2jZaseIAZIOmUEaqPDgpjEZzkBMAiqsAcp9kFAxhDInZHzJobJn7kSa3RBKFD1rr6fi8_MljtennkX8IWpwPOWutkVMN6MNGM0YUAPPLD6qnQ1VcbFeYZU6unljhj7-n7eLrvoOfWprWjTh6vtT1jHF-Ecu_uD5Tue5IMkivsAEFnti5-TCas1qatmWYG2jlXrOoHEH7q0fEv5ZUWO6T-jGxGLZtp4E01EBJzudlaSfCZqTpL4JPaZOgbJEyFiQU2BQp7Ik0lRkLqTUO40f1lJDDnIK4xDbiN_4cIGowQjq0yTcKlu-FW9hIC2xGajoICIAuMBIJz9mEh4R_Gcvap_K1vPo796Hib3xyM-fgdeUzS3GwTVBuBWPczZQP2UMLmKSFeJuuMDbsB3_tu4V_xqnsmxWSyP-E_Btudwi75lEOJNnA7N-vrU1VK8IyBEsNU2TIJ4f_BjTE3gMvyRsk-BXayqmQ4u9PwPOTISLKGpDGuAAgYEryb9N48O_AKojglMcGEdonHLI-ep4ajWV3es6KWCmpvblQ2tpP8mTVhIRVi4xefYUG_ZCF23CrtOgoYur843lz7Mx5iS0%3D'}
DEBUG:__main__:Attempting to close the session...
DEBUG:urllib3.connectionpool:Starting new HTTPS connection (1): 10.10.25.80:8080
DEBUG:urllib3.connectionpool:https://10.10.25.80:8080 "DELETE /session/1/session HTTP/1.1" 204 0
DEBUG:__main__:Session closure response: 204, 
DEBUG:__main__:Session successfully closed.
```

Here you can see the steps listed above play out to include visibility on both the session ID and the Cross-Site Request Forgery (CSRF) token.

Now in addition to the above PowerScale is going to do a whole bunch of things internally and tracing each line of what happens would be an extremely long essay so we'll hit the highlights. Below is a copy of [PowerScale's webui_http.conf](#apache-config) which defines Apache's behaviors for any given thing. From this we have a very clear idea of how session teardown works on the PowerScale.

The provided configuration file for PowerScale, which is leveraging Apache, offers insights into how Apache is configured and potentially how it handles sessions in this environment. Let’s break down some key parts of the configuration related to session management and their implications:

1. **Session Authentication Modules**: 
   - `mod_auth_isilon` - PowerScale's custom auth handler. This is handled by the shared library `mod_auth_isilon.so`. Now we don't have visibility into the code here, but realistically, these things follow design patterns that are pretty constant. If we were so inclined we could attach a debugger here, but the reality is we can make some pretty safe assumptions just based on how everyone does auth with Apache. The module is going to have all the code related to user authentication incluing the JWT tokens mentioned here [README.md](./README.md), it will handle session management and expiry, and it will likely make calls out to some other service for things like RBAC.
   - `IsiAuthSessionSecurity ip_check agent_check` indicates additional security checks for session validation, like IP address and user-agent consistency.
2. **Worker Module Configuration**: 
   - `mpm_worker_module` is used, which tells us it's a multi-threaded processing model. This module allows efficient handling of multiple concurrent connections,  crucial for session management in a high-traffic environment.
3. **FastCGI for External Handlers**:
   - FastCGI (`mod_fastcgi`) is configured to communicate with external servers/processes like `isi_papi_d`, `isi_rsapi_d`, and `isi_object_d`. These external servers are responsible for handling other parts of the session lifecycle.
4. **Session-Specific Directives**:
   - `<Location /session/1/session>` tells us that session management (creation, validation, teardown) is handled by a specific handler (`SetHandler session-service`).
   - `IsiAuthSessionTimeoutInactive` and `IsiAuthSessionTimeoutAbsolute` directives give session timeout settings
5. **Virtual Host Configuration**:
   - Within the `<VirtualHost>` section, you can see session-specific details. 
     - We see that SSL is enforced
     - CSP is present
     - There are a series of custom error documents which can be returned
     - There are a lot of custom URL rewrites
     - Specific URLs are handled by [FastCGI](https://en.wikipedia.org/wiki/FastCGI). This includes all the APIs
6. **ErrorDocument Directives**:
   - Custom error documents for various HTTP status codes, including those that might be relevant to session handling (e.g., 401 Unauthorized).

### Understanding Session Teardown

Apache itself, as configured here, doesn't directly reveal the mechanisms of session teardown. However, the combination of the worker module, SSL settings, custom authentication module, and external FastCGI processes suggests a complex session handling mechanism that is likely controlled both by Apache and additional PowerScale components.

#### Teardown Process:

1. **Session Termination Request**: A request to terminate a session (a DELETE request to the session endpoint) is received by Apache.
2. **Request Handling**: Apache, through its worker module, accepts and processes the request
3. **Custom Authentication Module Processing**: The `mod_auth_isilon` module, along with any session-related directives, validate the session and the request, ensuring that it's legitimate and authorized.
4. **Communication with External Handlers**: If session management is partially offloaded to external processes (as seen in the FastCGI configuration), Apache forwards the relevant information to these processes.
5. **Session Invalidating and Cleanup**: The responsible component (Apache module or external handler) invalidates the session, cleans up associated resources, and updates any necessary data stores.
6. **Response to Client**: Once the session is successfully terminated, a response is sent back to the client. In the case of a successful teardown without further content, a 204 No Content response.

## Apache Config

```
# X: ----------------
# X: This file is automatically generated and should not be
# X: edited directly.  If you must make changes to the
# X: contents of this file it should be done via the PowerScale
# X: Web UI, or via the template file located at
# X: /etc/mcp/templates/webui_httpd.conf
# X: ----------------

# =================================================
# Basic settings
# =================================================
Listen 8080 https

# =================================================
# Modules
# =================================================
LoadModule unixd_module modules/mod_unixd.so
LoadModule ssl_module modules/mod_ssl.so
LoadModule authz_core_module modules/mod_authz_core.so
LoadModule authn_core_module modules/mod_authn_core.so
LoadModule authz_host_module modules/mod_authz_host.so
LoadModule authz_user_module modules/mod_authz_user.so
LoadModule mpm_worker_module modules/mod_mpm_worker.so
LoadModule auth_isilon_module modules/mod_auth_isilon.so
LoadModule cgid_module modules/mod_cgid.so
LoadModule fastcgi_module modules/mod_fastcgi.so
LoadModule alias_module modules/mod_alias.so
LoadModule deflate_module modules/mod_deflate.so
LoadModule dir_module modules/mod_dir.so
LoadModule filter_module modules/mod_filter.so
LoadModule headers_module modules/mod_headers.so
LoadModule log_config_module modules/mod_log_config.so
LoadModule mime_module modules/mod_mime.so
LoadModule reqtimeout_module modules/mod_reqtimeout.so
LoadModule rewrite_module modules/mod_rewrite.so
LoadModule setenvif_module modules/mod_setenvif.so

User daemon
Group daemon
UseCanonicalName On
ServerRoot "/usr/local/apache2"
DocumentRoot "/usr/local/www/static"
PidFile "/var/apache2/run/webui_httpd.pid"
Mutex flock:/var/apache2/run mpm-accept
EnableMMAP Off
EnableSendfile On
KeepAlive On
MaxKeepAliveRequests 500
KeepAliveTimeout 15

## Implementing Clickjacking protection
Header always set X-Frame-Options "sameorigin"
## MIME types advertised in the Content-Type headers should not be changed
## requires mod_headers.so (don't comment this line out)
Header always set X-Content-Type-Options "nosniff"
Header always set X-XSS-Protection "1; mode=block"


#Hiding apache version in http header
ServerTokens Prod
ServerSignature Off

### Fix for CVE-2003-1567: HTTP TRACE / TRACK Methods Allowed ###
TraceEnable off

# Enable/Disable IsiAuthSessionSecurity agent_check and ip_check
# IsiAuthSessionSecurity ip_check -> ip_check enabled
# IsiAuthSessionSecurity -ip_check -> ip_check disabled
# IsiAuthSessionSecurity agent_check -> agent_check enabled
# IsiAuthSessionSecurity -agent_check -> agent_check disabled
IsiAuthSessionSecurity ip_check agent_check

# We must use a single process, multi-threaded server to correctly
# cache user credentials (fds) across Platform API sessions.
# StartServers: initial number of server processes to start
# MaxRequestWorkers: maximum number of simultaneous client connections
# MinSpareThreads: minimum number of worker threads which are kept spare
# MaxSpareThreads: maximum number of worker threads which are kept spare
# ThreadsPerChild: constant number of worker threads in each server process
# MaxConnectionsPerChild: maximum number of requests a server process serves
<IfModule mpm_worker_module>
    ServerLimit 1
    StartServers 1
    MaxRequestWorkers 64
    MinSpareThreads 10
    MaxSpareThreads 25
    ThreadsPerChild 64
    MaxConnectionsPerChild 0
</IfModule>

# =================================================
# REQTIMEOUT
# =================================================
<IfModule reqtimeout_module>
    RequestReadTimeout handshake=0 header=20-40,MinRate=500 body=20,MinRate=500
</IfModule>

# =================================================
# Logging, Errors, User Agent
# =================================================
LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined
# Log errors with syslog to /var/log/apache2/webui_httpd_error.log
ErrorLog syslog:local2
LogLevel error

ErrorDocument 500 /httpd/500Text.html
ErrorDocument 400 /httpd/400Text.html

SetEnvIf User-Agent ".*MSIE.*" \
         nokeepalive ssl-unclean-shutdown \
         downgrade-1.0 force-response-1.0

# =================================================
# Platform API
# =================================================
<IfModule fastcgi_module>
    FastCgiExternalServer /usr/sbin/isi_papi_d -socket /var/run/papi.sock -pass-cred -idle-timeout 600
</IfModule>

# =================================================
# Remote-Service API
# =================================================
<IfModule fastcgi_module>
    FastCgiExternalServer /usr/sbin/isi_rsapi_d -socket /var/run/isi_rsapi_d.sock -pass-cred -idle-timeout 600
</IfModule>

# =================================================
# Object API
# =================================================
<IfModule fastcgi_module>
    FastCgiExternalServer /usr/sbin/isi_object_d -pass-cred -idle-timeout 2147483647 -socket /var/run/isi_object_d.sock
</IfModule>

# =================================================
# Files
# =================================================
AcceptFilter http none
AcceptFilter https none

<IfModule dir_module>
    DirectoryIndex isilonnoindex.none
</IfModule>

<Directory />
    Options FollowSymLinks
    AllowOverride None
    Require all denied
</Directory>

<Directory "/usr/local/www/static">
    Options Indexes FollowSymLinks MultiViews
    AllowOverride None
    <LimitExcept GET POST DELETE HEAD>
        Require all denied
    </LimitExcept>
</Directory>

<FilesMatch "^\.ht">
    Require all denied
</FilesMatch>

<IfModule mime_module>
    TypesConfig conf/mime.types
    AddEncoding gzip .gz
    AddEncoding x-compress .Z
    AddType application/x-compress .Z
    AddType application/x-gzip .gz .tgz
</IfModule>

# =================================================
# SSL
# =================================================
<IfModule ssl_module>
    AddType application/x-x509-ca-cert .crt
    AddType application/x-pkcs7-crl .crl
    SSLPassPhraseDialog builtin
    #SSLSessionCache dbm:/var/run/ssl_scache
    SSLSessionCache none
    SSLSessionCacheTimeout 300
    Mutex flock:/var/apache2/run ssl-cache
    SSLRandomSeed startup file:/dev/urandom 1024
    SSLRandomSeed connect file:/dev/urandom 1024
    SSLProtocol -all -TLSv1.1 +TLSv1.2
    SSLCipherSuite ECDHE+aRSA+AES:DHE+aRSA+AES:ECDHE+ECDSA+AES:@STRENGTH
    SSLHonorCipherOrder on
    SSLCompression off
    SSLSessionTickets off
    SSLPassPhraseDialog exec:/etc/mcp/scripts/httpd_keypass.py
    SSLProxyCheckPeerCN off
    SSLProxyCheckPeerName off
    SSLProxyCheckPeerExpire off
    SSLOpenSSLConfCmd DHParameters /usr/local/apache24/conf/webui_dhparams.pem
    SSLOpenSSLConfCmd Curves prime256v1:secp384r1:secp521r1
</IfModule>

# =================================================
# Platform API Virtual Hosts
# =================================================
<VirtualHost _default_:8080>
    SSLEngine on
    SSLCertificateFile /ifs/.ifsvar/modules/isi_certs/system/server/zone_1/certs/794429aa484f2be3114356307ea2ff0bf004a8fbaa66e3e9c8647a923720f1ba.crt
    SSLCertificateKeyFile /ifs/.ifsvar/modules/isi_certs/system/server/zone_1/private/794429aa484f2be3114356307ea2ff0bf004a8fbaa66e3e9c8647a923720f1ba.key
    DocumentRoot "/usr/local/www/static"
    ServerAdmin support@isilon.com
    Header set Content-Security-Policy "default-src 'self' 'unsafe-inline' 'unsafe-eval' data:; script-src 'self' 'unsafe-eval'; style-src 'unsafe-inline' 'self'; "

    # Log access with syslog to /var/log/apache2/webui_httpd_access.log
    CustomLog "|$ logger -t httpd -p local3.info" combined

    AddOutputFilterByType DEFLATE text/css text/javascript application/javascript application/x-javascript
    BrowserMatch ^Mozilla/4 gzip-only-text/html
    BrowserMatch ^Mozilla/4\.0[678] no-gzip
    BrowserMatch \bMSIE !no-gzip !gzip-only-text/html
    AllowEncodedSlashes On
    ErrorDocument 503 /httpd/503Text.html
    ErrorDocument 400 /httpd/400WebUIText.html
    ErrorDocument 401 /httpd/401WebUIText.html
    ErrorDocument 403 /httpd/403WebUIText.html
    ErrorDocument 404 /httpd/404WebUIText.html
    ErrorDocument 405 /httpd/405WebUIText.html
    ErrorDocument 422 /httpd/422WebUIText.html
    ErrorDocument 423 /httpd/423WebUIText.html
    ErrorDocument 424 /httpd/424WebUIText.html
    ErrorDocument 500 /httpd/500WebUIText.html

    <IfModule rewrite_module>
        RewriteEngine On
        #Uncomment these lines to debug rewrite rules
        #RewriteLog  "/var/log/apache2/webui_httpd_error.log"
        #RewriteLogLevel 9
        # Redirect internal subrequests to an error to prevent them from being
        # redirected to another module and causing another authentication.
        RewriteCond %{IS_SUBREQ} t
        RewriteRule ^ - [G]

        # Restrict unnecessary http methods
        RewriteCond %{REQUEST_METHOD} ^(PATCH|OPTIONS|TRACK|CONNECT|TRACE|COPY|LINK|UNLINK|PURGE|LOCK|UNLOCK|PROPFIND|VIEW)
        RewriteRule .* - [L,R=405]
        RewriteCond %{REQUEST_METHOD} ^(PATCH|OPTIONS|TRACK|CONNECT|TRACE|COPY|LINK|UNLINK|PURGE|LOCK|UNLOCK|PROPFIND|VIEW)
        RewriteRule .* - [L,R=405]
        RewriteCond %{REQUEST_METHOD} ^(PATCH|OPTIONS|TRACK|CONNECT|TRACE|COPY|LINK|UNLINK|PURGE|LOCK|UNLOCK|PROPFIND|VIEW)
        RewriteRule .* - [L,R=405]

        # Older UI versions will redirect to (legacy) Login
        # after an upgrade.  Force them into the new system
        RewriteRule ^/$ /v2/html/OneFS.html
        RewriteRule ^/Login.* /v2/html/OneFS.html
        RewriteRule ^/cloudpool_eula.* /v2/html/cloudpool_eula.txt
        RewriteRule ^/OneFS$ /v2/html/OneFS.html

        # Reroute legacy /Status to base URI
        RewriteRule ^/Status* https://%{SERVER_ADDR}:8080/ [L,R]

        RewriteCond %{DOCUMENT_ROOT}%{REQUEST_FILENAME}.gz -f
        RewriteRule (.*\.(html|js|css))$ $1.gz [L]

        # Rewrite all request past /OneFS to v3
        RewriteRule ^/OneFS/(.*) /v3/$1

        # For v3 requests, if the file exists on disk, serve it
        RewriteCond %{REQUEST_FILENAME} ^/v3 [NC]
        RewriteCond %{DOCUMENT_ROOT}%{REQUEST_FILENAME}.gz -f
        RewriteRule (.*)$ $1.gz [L]

        RewriteCond %{REQUEST_FILENAME} ^/v3 [NC]
        RewriteCond %{DOCUMENT_ROOT}%{REQUEST_FILENAME} -f
        RewriteRule ^ - [L]

        # For all request to v3 that do no exists (like 404) return the index file so
        # the app can handle them
        RewriteRule ^/v3 /v3/index.html.gz [L]

        # Stop requests for static files
        RewriteRule ^/(json|v2|vasa-catalog|httpd)/.* $0 [L]


              RewriteRule ^/namespace(.*) /namespace$1 [PT]

        RewriteRule ^/object(.*) - [R=503]
        RewriteRule ^/webhdfs(.*) - [R=503]
        RewriteRule ^/imagetransfer(.*) - [R=503]
        RewriteRule ^/jmx(.*) - [R=503]

        RewriteRule ^/authenticate /session/1/session [P]
        RewriteRule ^/objectstore(.*) /object$1 [PT]
        RewriteRule ^/favicon.ico /v2/images/favicon.ico [L]
        RewriteRule ^/MIBs/(.*) "/usr/share/snmp/mibs/$1" [L]
        RewriteRule ^/MIBs-DEFs/(.*) "/usr/share/snmp/defs/$1" [L]
        RewriteRule ^/platform(.*) /platform$1 [PT]
        RewriteRule ^/remote-service(.*) /remote-service$1 [PT]
        RewriteRule ^/session(.*) /session$1 [PT]
        RewriteRule ^/mod_ssl:error:HTTP-request https://%{SERVER_ADDR}:8080/ [L,R]
    </IfModule>

    <FilesMatch .*\.html.gz>
        ForceType text/html
    </FilesMatch>

    <FilesMatch .*\.css.gz>
        ForceType text/css
    </FilesMatch>

    <FilesMatch .*\.js.gz>
        ForceType application/javascript
    </FilesMatch>

    <Directory "/usr/share/snmp/mibs">
        Options Indexes MultiViews
        ForceType application/octet-stream
        AllowOverride None
        Require all granted
    </Directory>
    <Directory "/usr/share/snmp/defs">
        Options Indexes MultiViews
        ForceType application/octet-stream
        AllowOverride None
        Require all granted
    </Directory>

    <Location /webhdfs>
        RemoveEncoding .gz .Z
    </Location>



    Header always add Strict-Transport-Security: "max-age=31536000;"

    # =================================================
    # Platform API
    # =================================================
    Alias /platform /usr/sbin/isi_papi_d
    <Location /platform>
        AuthType Isilon
        IsiAuthName "platform"
        IsiAuthTypeBasic Off
        IsiAuthTypeSessionCookie On
        IsiDisabledZoneAllow Off
        IsiMultiZoneAllow On
        IsiCsrfCheck On
        Require valid-user
        SetHandler fastcgi-script
        Options +ExecCGI
        ErrorDocument 400 /httpd/400PAPIText.html
        ErrorDocument 401 /httpd/401PAPIText.html
        ErrorDocument 403 /httpd/403PAPIText.html
        ErrorDocument 404 /httpd/404PAPIText.html
        ErrorDocument 405 /httpd/405PAPIText.html
        ErrorDocument 422 /httpd/422PAPIText.html
        ErrorDocument 423 /httpd/423PAPIText.html
        ErrorDocument 424 /httpd/424PAPIText.html
        ErrorDocument 500 /httpd/500PAPIText.html
    </Location>

    <Location /session/1/session>
        SetHandler session-service
        IsiAuthServices platform remote-service namespace
        ForceType text/plain
        ErrorDocument 401 /json/401.json

    </Location>

    <Location /session/1/saml/logout/slostatus>
        SetHandler saml-logout-slo
        ErrorDocument 401 /json/401.json

    </Location>

    <Location /session/1/saml/logout/session>
        SetHandler saml-logout-session
        ErrorDocument 401 /json/401.json

    </Location>

    # Authentication is not required to access these resources
    <Location /platform/*/cluster/identity>
        IsiAuthIgnore GET
    </Location>
    <Location /platform/*/cluster/identity/>
        IsiAuthIgnore GET
    </Location>
    <Location /platform/*/cluster/brand>
        IsiAuthIgnore GET
    </Location>
    <Location /platform/*/auth/users/*/change-password>
        IsiAuthIgnore PUT
    </Location>
    <Location /platform/*/auth/providers/saml-services/settings>
        IsiAuthIgnore GET
    </Location>
    <Location /platform/*/auth/providers/saml-services>
        IsiAuthIgnore GET
    </Location>
    <Location /platform/*/upgrade/cluster/mixed-mode>
        IsiAuthIgnore GET
    </Location>
    <Location /platform/*/cluster/version>
        IsiAuthIgnore GET
    </Location>



    # =================================================
    # Object API
    # =================================================

    Alias /namespace /usr/sbin/isi_object_d
    <Location /namespace>
        AuthType Isilon
        IsiAuthName "namespace"
        IsiAuthTypeBasic Off
        IsiAuthTypeSessionCookie On
        IsiDisabledZoneAllow Off
        IsiMultiZoneAllow On
        IsiCsrfCheck On
        Require valid-user
        SetHandler fastcgi-script
        Options +ExecCGI
        ErrorDocument 401 /json/401.json
        Header set Content-Security-Policy "default-src 'none'"
    </Location>

    # =================================================
    # Remote-Service API
    # =================================================
    Alias /remote-service /usr/sbin/isi_rsapi_d
    <Location /remote-service>
        AuthType Isilon
        IsiAuthName "remote-service"
        IsiAuthTypeBasic Off
        IsiAuthTypeSessionCookie On
        Require valid-user
        SetHandler fastcgi-script
        Options +ExecCGI
        ErrorDocument 401 /json/401.json
    </Location>


    # Session timeouts
    IsiAuthSessionTimeoutInactive 900
    IsiAuthSessionTimeoutAbsolute 14400
    Timeout 500

</VirtualHost>
```