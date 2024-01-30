from __future__ import print_function
import ssl
import zipfile
import subprocess
import sys
import os
import os.path
import argparse
import pprint
import warnings
import shutil
import stat
from functools import partial
from itertools import chain

if sys.version_info[0] == 2:
    py3 = False
    import ConfigParser
    import urllib
if sys.version_info[0] == 3:
    py3 = True
    import urllib.request
    import tempfile
    sys.path.append('/mystic/telemetry/DCManager/venv/lib/python3.6/site-packages')
    sys.path.append('/mystic/telemetry/DCManager')
    import aiohttp
    import asyncio
    import json
    import traceback

    CURL_HEADER = 'curl --unix-socket /var/lib/vxrail/nginx/socket/nginx.sock -H "Content-Type: application/json" '
    HOST_DO_URL = 'http://127.0.0.1/rest/vxm/internal/do/v1/host/query -d '
    CONFIGURED_HOST_QUERY = '{"query": "{configuredHosts { name, hardware{ sn}}}"}'
    try:
        from Utils.gql_client.create_client import get_data_from_config_service
    except:
        from Utils.dao.create_client import get_data_from_config_service
class Helper:
    def __init__(self, section, file):
        self.readline = partial(next, chain(("[{0}]\n".format(section),), file, ("",)))


#version 2022.09.05 - copy /var/lib/vmware-marvin/trust/lin to /var/lib/vmware-marvin/trust/host_lin

# Properties of cert dir: applicationProperties.ssl.trust.certs.dir
CERT_PATH = '/var/lib/vmware-marvin/trust/'
CRL_PATH = '/var/lib/vmware-marvin/trust/crl/'
# CERT_PATH = '/tmp/trust/'
# CRL_PATH = '/tmp/trust/crl/'
APPLICATION_PROPERTIES = '/usr/lib/vmware-marvin/marvind/webapps/ROOT/WEB-INF/classes/application.properties'
RUNTIME_PROPERTIES = '/var/lib/vmware-marvin/runtime.properties'
MOCK_SEC = "mock"
VC_ADDRESS_PROPERTY = "data.vcenter.address"
VERSION = '2022.09.05'

def check_current_cert_with_default_vc():
    check_cert_with_default_vc(capath = CERT_PATH)


def check_cert_with_default_vc(cafile = None, capath = None):
    pass


def check_cert_with_host(capath, cafile, hostname, port):
    pass


def get_vc_address():
    rtConfig = ConfigParser.RawConfigParser(allow_no_value=True)
    with open(RUNTIME_PROPERTIES) as ifh:
        rtConfig.readfp(Helper(MOCK_SEC, ifh))
    return rtConfig.get(MOCK_SEC, "data.vcenter.address")


def get_cert_download(vcaddr, download_name=None, url=None):
    """Try download from specif URL if provided, or from https://vcaddr/certs/download , and if failed,
    from https://vcaddr/certs/download.zip"""
    if py3:
        if url is None:
            VC_CERT_URL = "https://{0}/certs/download.zip".format(vcaddr)
            if hasattr(ssl, "_create_unverified_context"):
                ssl._create_default_https_context = ssl._create_unverified_context
            urllib.request.urlretrieve(VC_CERT_URL, download_name)
        else:
            urllib.request.urlretrieve(url, download_name)
    else:
        if url is None:
            VC60_CERT_URL = "https://{0}/certs/download".format(vcaddr)
            VC65_CERT_URL = "https://{0}/certs/download.zip".format(vcaddr)
            # If Python ver is 2.7.9+, disable verification of SSL cert
            if hasattr(ssl, "_create_unverified_context"):
                ssl._create_default_https_context = ssl._create_unverified_context
            result = urllib.urlretrieve(VC60_CERT_URL, filename=download_name)
            if os.path.getsize(result[0]) == 0:
                # Try vc 6.5 url instead
                result = urllib.urlretrieve(VC65_CERT_URL, filename=download_name)
        else :
            result = urllib.urlretrieve(url, filename=download_name)
    print("Downloaded root CA certificate zip to " + download_name)


def save_cert(cert_pem, certname):
    if certname:
        cert_der = certname
    else:
        cert_der = os.tempnam(CERT_PATH, "CA_Cert_")

    vxrail_version = subprocess.check_output("rpm -qa | grep marvin", shell=True).decode().split('-')[2].strip()
    if py3:
        if vxrail_version >= '7.0.240':
            print("Root CA certificate {0} is saved at {1}.".format('/tmp/certs/lin', CERT_PATH))
            subprocess.check_call('cp -r {0} {1}'.format('/tmp/certs/lin', CERT_PATH), shell=True)
            subprocess.check_call('chown -R tcserver:pivotal {0}{1}'.format(CERT_PATH, 'lin'), shell=True)
            subprocess.check_call('chmod a+x {0}{1}'.format(CERT_PATH, 'lin'), shell=True)
            if vxrail_version >= '7.0.350':
                subprocess.check_call('cp -r {0}/* {1}{2}'.format('/tmp/certs/lin', CERT_PATH, 'host_lin'), shell=True)
        else:
            subprocess.check_call("openssl x509 -in {0} -out {1} -outform DER".format(cert_pem, cert_der), shell=True)
            print("Root CA certificate {0} is saved at {1}.".format(cert_pem, cert_der))
    else:
        subprocess.check_call("openssl x509 -in {0} -out {1} -outform DER".format(cert_pem, cert_der), shell=True)
        print("Root CA certificate {0} is saved at {1}.".format(cert_pem, cert_der))

    if vxrail_version < '7.0.240':
        subprocess.check_call('chown -R tcserver:pivotal {0}'.format(CERT_PATH), shell=True)


def save_crl(crl_pem, crlname):
    if py3:
        vxrail_version = subprocess.check_output("rpm -qa | grep marvin", shell=True).decode().split('-')[2].strip()
        if vxrail_version >= '7.0.240':
            return

    if crlname:
        crl_der = crlname
        try:
            subprocess.check_call("openssl crl -in {0} -out {1} -outform DER".format(crl_pem, crl_der), shell=True)
            print("Root CA certificate CRL {0} is saved at {1}.".format(crl_pem, crl_der))
            subprocess.check_call('chmod a+x {0}{1}'.format(CERT_PATH, 'crl'), shell=True)
            subprocess.check_call('chown -R tcserver:pivotal {0}{1}'.format(CERT_PATH, 'crl'), shell=True)
        except:
            print("Skipped saving CRL. ")

def save_cert_crl(cert_pem, crl_pem, certname, crlname):
    crl_der = ""

    if certname:
        cert_der = certname
    else:
        cert_der = os.tempnam(CERT_PATH, "CA_Cert_")

    subprocess.check_call("openssl x509 -in {0} -out {1} -outform DER".format(cert_pem, cert_der), shell=True)

    if crlname:
        crl_der = crlname

        try:
            subprocess.check_call("openssl crl -in {0} -out {1} -outform DER".format(crl_pem, crl_der), shell=True)
        except:
            print("Skipped saving CRL. ")

    print("Root CA certificate is saved at {0} and CRL is saved at {1}".format(cert_der, crl_der))
    # This may lead to permission issue
    stat_f = os.stat(CERT_PATH)
    os.chown(cert_der, stat_f.st_uid, stat_f.st_gid)
    os.chmod(cert_der, stat.S_IWUSR | stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

    try:
        os.chown(crl_der, stat_f.st_uid, stat_f.st_gid)
        os.chmod(crl_der, stat.S_IWUSR | stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
    except:
        crl_der = ""


def prepare_certs_dir(zfile):
    certzip = zipfile.ZipFile(zfile)
    certzip.testzip()
    namelist = certzip.namelist()
    targetlist = []
    if os.path.dirname(namelist[0]) == "certs":
        # This is vc 6.0 certs. Everything under /certs/
        targetlist = namelist
    else:
        # This is vc 6.5 certs. Choose everything under /certs/lin/
        targetlist = []
        for name in namelist:
            # Put everything begins with certs/lin as target
            if name.startswith("certs/lin"):
                targetlist.append(name)
    return targetlist, certzip


def download_server_cert(host, port, server_cert_file_name):
    return subprocess.check_output("echo | openssl s_client -connect {0}:{1} 2>/dev/null | openssl x509 -out {2}"
                                   .format(host, port, server_cert_file_name), shell=True)


def verify_cert_pair_list(certzip, namelist, host=None, port=443):
    if py3:
        if host is None:
            host = get_data_from_config_service("vcenter_host")['value']
        server_cert = tempfile.mkstemp()[1]
    else:
        if host is None:
            host = get_vc_address()
        server_cert = os.tmpnam()
    try:
        # Use openssl command to download server cert
        download_server_cert(host, port, server_cert)
    except subprocess.CalledProcessError as callerror:
        print("Failed to download certificate from %s:%s and write in %s, error code %i" \
              % host, port, server_cert, callerror.returncode)
        return None, None

    crl_file_list = list()
    # extract each of the pair and verify again the downloaded cert
    for certname, crlname in namelist:
        certfile = certzip.extract(certname, "/tmp")
        if crlname != "NoCRL":
            crlfile = certzip.extract(crlname, "/tmp")
            crl_file_list.append(crlfile)

    # verify vc cert by providing CApath : /tmp/certs/lin/
    ret = subprocess.call("openssl verify -CApath {0} {1}1>/dev/null 2>&1"
                          .format('/tmp/certs/lin/', server_cert), shell=True)
    #os.remove('/tmp/certs/lin/')
    if ret == 0:
        return namelist, certzip
    # If we reach here, no matching cert
    print("Failed to find CA cert that verifies cert from %s" % host)
    return None, None


def pinpoint_cert(targetlist, vcip, certzip):
    # First of all, create a dict with each hash name in the form of { <basename> : [<certname_ext>, <crlname_ext>]}
    for file in targetlist:
        certzip.extract(file, "/tmp")
    if py3:
        if vcip is None:
            host = get_data_from_config_service("vcenter_host")['value']
        server_cert = tempfile.mkstemp()[1]
    else:
        if vcip is None:
            host = get_vc_address()
        server_cert = os.tmpnam()
    try:
        # Use openssl command to download server cert
        download_server_cert(vcip, 443, server_cert)
    except subprocess.CalledProcessError as callerror:
        print("Failed to download certificate from %s:%s and write in %s, error code %i" \
              % vcip, 443, server_cert, callerror.returncode)
        return None, None
    os.chdir('/tmp')

    #modify file name, suffix should start from .0, .r0
    tmp_files = {}
    targetlist_new = []
    for name in targetlist:
        if '.r' in name:
            fn = name.split('.r')
            if fn[0] + '.r' in tmp_files:
                tmp_files[fn[0] + '.r'].append(fn[1])
            else:
                tmp_files[fn[0] + '.r'] = [fn[1]]
        else:
            fn = name.split('.')
            if fn[0] + '.' in tmp_files:
                tmp_files[fn[0] + '.'].append(fn[1])
            else:
                tmp_files[fn[0] + '.'] = [fn[1]]

    for (fn, fs) in tmp_files.items():
        ori_fs = [i for i in fs]
        fs.sort()
        #rename
        for i, nfn in enumerate(fs):
            os.rename(fn + nfn, fn + str(i))
            print("Renaming {} to {}".format(fn + nfn, fn + str(i)))
            targetlist_new.append(fn + str(i))

    ret = subprocess.call("openssl verify -CApath {0} {1} 1>/dev/null 2>&1"
                          .format('/tmp/certs/lin/', server_cert), shell=True)

    if ret == 0:
        print("Found certificates {0} that can verify server certificate".format(targetlist_new))
        print("Clean up existing certificates in {}".format(CERT_PATH))
        certs_f = os.listdir(CERT_PATH)
        for ctf in certs_f:
            if os.path.isfile(os.path.join(CERT_PATH, ctf)):
                print(" - Removing {}".format(os.path.join(CERT_PATH, ctf)))
                os.remove(os.path.join(CERT_PATH, ctf))
            if ctf == 'lin' or ctf == 'host_lin':
                new_certs_f = os.listdir(os.path.join(CERT_PATH, ctf))
                for nctf in new_certs_f:
                    if os.path.isfile(os.path.join(CERT_PATH, ctf, nctf)):
                        print(" - Removing {}".format(os.path.join(CERT_PATH, ctf, nctf)))
                        os.remove(os.path.join(CERT_PATH, ctf, nctf))
        print("Clean up existing crl files in {}".format(CRL_PATH))
        crls_f = os.listdir(CRL_PATH)
        for crlf in crls_f:
            if os.path.isfile(os.path.join(CRL_PATH, crlf)):
                print("Removing {}".format(os.path.join(CRL_PATH, crlf)))
                os.remove(os.path.join(CRL_PATH, crlf))
        for file in targetlist_new:
            if '.r' in file:
                crlfile = "/tmp/" + file
                if py3:
                    crlname_vxm = subprocess.check_output("openssl crl -in {0} -fingerprint -noout".
                                                          format(crlfile), shell=True).decode().split('=')[1].strip()
                else:
                    crlname_vxm = subprocess.check_output("openssl crl -in {0} -fingerprint -noout".
                                                      format(crlfile), shell=True).split('=')[1].strip()

                save_crl(crlfile, CRL_PATH + crlname_vxm)
            else:
                certfile = "/tmp/" + file
                if py3:
                    certname_vxm = subprocess.check_output("openssl x509 -in {0} -fingerprint -noout".
                                                           format(certfile), shell=True).decode().split('=')[1].strip()
                else:
                    certname_vxm = subprocess.check_output("openssl x509 -in {0} -fingerprint -noout".
                                                       format(certfile), shell=True).split('=')[1].strip()

                save_cert(certfile, CERT_PATH + certname_vxm)

    else:
        print("Failed to find a matching root CA certificate/CRL set that could verify vCenter certificate")

def shll(cmd, test="", shell=True, quiet=True):  # Python 3 Shell ruturns output and completion 1-Yes or 0-No
    err, out = cmd, ""
    try:
        if not shell:
            clst = cmd.split(' ') if isinstance(cmd, str) else cmd
            clst = [x for x in clst if x]
            p = subprocess.Popen(clst, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        else:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        x, y = p.communicate()
        out, err = x.decode('UTF-8').strip('\n'), y.decode('UTF-8').strip('\n')
        p_status = p.returncode
    except:
        p_status = 1
        if not quiet:
            traceback.format_exc()

    if not p_status:
        return str(out), True
    else:
        if not test: test = str(cmd)
        if not quiet:
            print("Failed command: %s  ->  %s" % (test, err))
        return str(err), False

def parse_argument():
    parser = argparse.ArgumentParser(description='vCenter Root CA certificate utility for VxRail Manager 4.0.x and '
                                                 '4.5.x. Need to run as root.')
    parser.add_argument('-u', '--downloadurl', help='specify download HTTP URL')
    parser.add_argument('-d', '--dryrun', action="store_true", help='only verify certificate, no import. NOT '
                                                                    'IMPLEMENTED')

    parser.add_argument('-i', '--vcip', help='ip address or FQDN of vCenter, use current property if not specified')
    args = parser.parse_args()
    return args


def main():
    print("Running script with version {}".format(VERSION))
    args = parse_argument()

    if args.downloadurl :
        downloadurl = args.downloadurl
        # TODO: verify URL format here
        print("Download certificate zip file from " + downloadurl)
    else:
        downloadurl=None

    if args.dryrun :
        dryrun = True
        print("No import will take place")
    else:
        dryrun = False

    if args.vcip :
        vcip = args.vcip
    else :
        if py3:
            vcip = get_data_from_config_service("vcenter_host")['value']
            vxrail_version = get_data_from_config_service("vxrail_version")['value']
        else:
            vcip = get_vc_address()
            vxrail_version = subprocess.check_output("rpm -qa | grep marvin", shell=True).decode().split('-')[2].strip()
    print("Verify certificate against vCenter " + vcip)

    if dryrun :
        # TODO : implement dryrun
        print("Dry run not implemented")
        sys.exit(-1)

    warnings.filterwarnings("ignore")
    if py3:
        rootcazip = tempfile.mkstemp()[1]
    else:
        rootcazip = os.tmpnam()
    if downloadurl:
        get_cert_download(vcip, download_name=rootcazip, url=downloadurl)
        print("Downloaded root CA certificate zip from " + downloadurl)
    else :
        get_cert_download(vcip, rootcazip)
        print("Downloaded root CA certificate zip from " + vcip)

    entrylist, cazip = prepare_certs_dir(rootcazip)

    # Find out the exact certs to import
    pinpoint_cert(entrylist, vcip, cazip)

    #remove /tmp/certs dir
    print("Remove /tmp/certs directory.")
    shutil.rmtree("/tmp/certs")

    #clean redis cache for vc/esxi crl info
    print("Delete saved CRL info in cacheservice...")
    if py3:
        if vxrail_version <= '7.0.350':
            subprocess.check_call('docker exec -uroot $(docker ps -q -f name=func_cacheservice) redis-cli -n 1 DEL VC_CRL_INFO_KEY', shell=True)
            subprocess.check_call('docker exec -uroot $(docker ps -q -f name=func_cacheservice) redis-cli -n 1 DEL ESXI_CRL_INFO_KEY', shell=True)
        else:
            subprocess.check_call('kubectl exec -it $(kubectl get pods -o=name | grep cacheservice | sed "s/^.\{4\}//") -- redis-cli -n 1 DEL VC_CRL_INFO_KEY', shell=True)
            subprocess.check_call('kubectl exec -it $(kubectl get pods -o=name | grep cacheservice | sed "s/^.\{4\}//") -- redis-cli -n 1 DEL ESXI_CRL_INFO_KEY', shell=True)
    #restart services
    print("Restarting vmware-marvin service...")
    subprocess.check_call("systemctl restart vmware-marvin", shell=True)
    print("Restarting runjars service...")
    subprocess.check_call("systemctl restart runjars", shell=True)

    #import hosts cert
    if py3:
        if vxrail_version >= '7.0.300':
            print("Importing ESXi hosts certificate into VxRail Manager...")
            try:
                host_query = CURL_HEADER + HOST_DO_URL + "'" + CONFIGURED_HOST_QUERY + "'"
                out, q = shll(host_query)
                configuredHosts = ((json.loads(out)).get('data')).get('configuredHosts')
                if configuredHosts is None:
                    print("No host configured.")
                else:
                    for host in configuredHosts:
                        host_sn = host.get('hardware', '').get('sn')
                        host_name = host.get('name')
                        if host_name is not None:
                            download_server_cert(host_name, 443, CERT_PATH + 'host/' + host_sn + ".cert")
                            subprocess.check_call('chown root:docker {0}host/{1}.cert'.format(CERT_PATH, host_sn),
                                                  shell=True)
                            subprocess.check_call('chmod 640 {0}host/{1}.cert'.format(CERT_PATH, host_sn), shell=True)
                            print('Import {} certificate done.'.format(host_name))
                        else:
                            print('Failed to import ESXi host cert into VxRail Manger!!!')
            except Exception as err:
                traceback.print_exc()
                print('Failed to import ESXi host cert into VxRail Manger!!!')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        pprint.pprint(e)
        sys.exit(-1)

