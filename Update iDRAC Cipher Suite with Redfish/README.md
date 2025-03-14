# Update iDRAC Cipher Suite with Redfish

How to do this is detailed [in this article](https://dl.dell.com/manuals/all-products/esuprt_software_int/esuprt_software_ent_systems_mgmt/idrac9-lifecycle-controller-v33-series_White-Papers11_en-us.pdf)

You can obtain all of the iDRAC attributes with the below script:

```python
import requests
import json
import base64

# iDRAC Credentials and Information
IDRAC_IP = "YOUR_IP"  # Change this to your iDRAC IP
USERNAME = "root"
PASSWORD = "calvin"

# Redfish API Endpoint for iDRAC Attributes
URL = f"https://{IDRAC_IP}/redfish/v1/Managers/iDRAC.Embedded.1/Attributes"

# Construct the Authentication Header
headers = {
    "Authorization": "Basic " + base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode(),
    "Content-Type": "application/json"
}

# Disable SSL warnings (iDRAC typically uses self-signed certificates)
requests.packages.urllib3.disable_warnings()

# Send GET request to retrieve all attributes
try:
    response = requests.get(URL, headers=headers, verify=False)

    if response.status_code == 200:
        data = response.json()
        print("\n✅ Successfully retrieved iDRAC attributes:\n")
        print(json.dumps(data, indent=4))  # Pretty print JSON response

        # Extract Cipher Select related attributes
        print("\n🔍 Cipher Select Related Settings:\n")
        for key, value in data.get("Attributes", {}).items():
            if "Cipher" in key or "TLS" in key or "Encryption" in key:
                print(f"{key}: {value}")

    else:
        print(f"\n❌ Failed to retrieve attributes. HTTP {response.status_code}")
        print("Response:", response.text)

except requests.exceptions.RequestException as e:
    print(f"\n❌ Error retrieving iDRAC attributes: {e}")
```

You can change the cipher suite properties with the below. Simply change the string `NEW_CIPHERS` to whatever you need it to be.

```python
import requests
import json
import base64

# iDRAC Credentials and Information
IDRAC_IP = "YOUR_IP"  # Change to your iDRAC IP
USERNAME = "root"
PASSWORD = "calvin"

# Redfish API Endpoint for iDRAC Attributes
URL = f"https://{IDRAC_IP}/redfish/v1/Managers/iDRAC.Embedded.1/Attributes"

# New Cipher String to Apply
NEW_CIPHERS = "aes256-gcm@openssh.com"  # Change this to the desired cipher string

# Construct the Authentication Header
headers = {
    "Authorization": "Basic " + base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode(),
    "Content-Type": "application/json"
}

# Construct the JSON payload for updating the ciphers
payload = {
    "Attributes": {
        "SSHCrypto.1.Ciphers": NEW_CIPHERS
    }
}

# Disable SSL warnings (iDRAC typically uses self-signed certificates)
requests.packages.urllib3.disable_warnings()

# Send PATCH request to update cipher settings
try:
    response = requests.patch(URL, headers=headers, data=json.dumps(payload), verify=False)

    if response.status_code in [200, 204]:
        print("\n✅ Successfully updated iDRAC SSH ciphers.")
    else:
        print(f"\n❌ Failed to update SSH ciphers. HTTP {response.status_code}")
        print("Response:", response.text)

except requests.exceptions.RequestException as e:
    print(f"\n❌ Error updating iDRAC SSH ciphers: {e}")

```

Example output:

```bash
python.exe "update_cipher_suite.py"

✅ Successfully updated iDRAC SSH ciphers.

Process finished with exit code 0
```

Here it is in PowerShell:

```bash
# iDRAC Credentials and Information
$IDRAC_IP = "YOUR_IP"   # Change this to your iDRAC IP
$USERNAME = "root"
$PASSWORD = "calvin"

# Redfish API Endpoint for iDRAC Attributes
$URL = "https://$IDRAC_IP/redfish/v1/Managers/iDRAC.Embedded.1/Attributes"

# New Cipher String to Apply
$NEW_CIPHERS = "aes256-gcm@openssh.com"  # Change this to the desired cipher string

# Construct the Basic Authentication Header
$base64AuthInfo = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("$USERNAME`:$PASSWORD"))
$headers = @{
    "Authorization" = "Basic $base64AuthInfo"
    "Content-Type"  = "application/json"
}

# Construct the JSON payload for updating the ciphers
$body = @{
    "Attributes" = @{
        "SSHCrypto.1.Ciphers" = $NEW_CIPHERS
    }
} | ConvertTo-Json -Depth 3

# Ignore SSL certificate errors (iDRAC often has a self-signed certificate)
[System.Net.ServicePointManager]::ServerCertificateValidationCallback = { $true }

# Send PATCH request to update cipher settings
try {
    $response = Invoke-RestMethod -Uri $URL -Method Patch -Headers $headers -Body $body -ContentType "application/json"

    Write-Host "`n✅ Successfully updated iDRAC SSH ciphers." -ForegroundColor Green
}
catch {
    Write-Host "`n❌ Failed to update SSH ciphers." -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)"
    if ($_.Exception.Response) {
        $errorResponse = $_.Exception.Response.GetResponseStream()
        $reader = New-Object System.IO.StreamReader($errorResponse)
        Write-Host "`nResponse:`n$($reader.ReadToEnd())" -ForegroundColor Yellow
    }
}

```