# VMWare APIs

- [VMWare APIs](#vmware-apis)
  - [VxRail](#vxrail)
    - [Upgrading VxRail with Windows Curl](#upgrading-vxrail-with-windows-curl)
  - [Example Code for PowerShell 5](#example-code-for-powershell-5)
    - [Version Used for Testing](#version-used-for-testing)
  - [Log Locations](#log-locations)

## VxRail

[API Cookbook](vxrail_api_cookbook.pdf)

### Upgrading VxRail with Windows Curl

```
curl -k --user "administrator@vsphere.local:<PASSWORD>" --request POST "https://<VXRAIL_IP_ADDRESS>/rest/vxm/v1/lcm/upgrade" --header "Content-Type: application/json" --data "{\"bundle_file_locator\": \"/tmp/VXRAIL_COMPOSITE-4.7.for_4.x.x.zip \",\"vxrail\": {\"vxm_root_user\": {\"username\": \"root\",\"password\": \"<PASSWORD>\"}},\"vcenter\":{\"vc_admin_user\": {\"username\": \"administrator@vsphere.local\",\"password\": \"<PASSWORD>\"},\"vcsa_root_user\": {\"username\": \"root\",\"password\": \"<PASSWORD>\"},\"psc_root_user\": {\"username\": \"root\",\"password\": \"<PASSWORD>\"}}}"
```

Note: psc_root_user should be the same as vCenter root user

## Example Code for PowerShell 5

```powershell
$RESTAPIServer = "YOUR_VCENTER"
$RESTAPIUser = "administrator@vsphere.local" // Or whatever user you want
$RESTAPIPassword = "PASSWORD"

add-type @"
    using System.Net;
    using System.Security.Cryptography.X509Certificates;
    public class TrustAllCertsPolicy : ICertificatePolicy {
        public bool CheckValidationResult(
            ServicePoint srvPoint, X509Certificate certificate,
            WebRequest request, int certificateProblem) {
            return true;
        }
    }
"@
[System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAllCertsPolicy
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]'Ssl3,Tls,Tls11,Tls12'

$BaseAuthURL = "https://" + $RESTAPIServer + "/rest/com/vmware/cis/"
$BaseURL = "https://" + $RESTAPIServer + "/rest/vcenter/"
$vCenterSessionURL = $BaseAuthURL + "session"
$Header = @{"Authorization" = "Basic "+[System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($RESTAPIUser+":"+$RESTAPIPassword))}
$Type = "application/json"

Try 
{
    $vCenterSessionResponse = Invoke-RestMethod -Uri $vCenterSessionURL -Headers $Header -Method POST -ContentType $Type
}
Catch 
{
    $_.Exception.ToString()
    $error[0] | Format-List -Force
}

# Extracting the session ID from the response
$vCenterSessionHeader = @{'vmware-api-session-id' = $vCenterSessionResponse.value}

$VMListURL = $BaseURL+"datacenter"
Write-Host "Sending request to URL: ${VMListURL}"
Try 
{
    $VMListJSON = Invoke-RestMethod -Method Get -Uri $VMListURL -TimeoutSec 100 -Headers $vCenterSessionHeader -ContentType $Type
    $VMList = $VMListJSON.value
}
Catch 
{
    $_.Exception.ToString()
    $error[0] | Format-List -Force
}


$VMList | Format-Table -AutoSize
```

### Version Used for Testing

```powershell
PS C:\Users\grant\Downloads> (Get-Host).Version

Major  Minor  Build  Revision
-----  -----  -----  --------
5      1      19041  1023
```

## Log Locations

Relevant logs are in /var/log/vmware/vapi/endpoint

The `vcentershim.log`  will tell you about errors occurring (like a 500 internal server error)

The `endpoint.log` will tell you about things like 404 errors

`endpoint-access.log` will show you who is accessing the server.