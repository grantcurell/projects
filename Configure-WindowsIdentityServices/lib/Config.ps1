Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Test-IsAbsoluteWindowsPath {
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][string]$PathValue)
    return ($PathValue -match '^[A-Za-z]:\\' -or $PathValue -match '^\\\\')
}

function Convert-IPv4ToUInt32 {
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][string]$Address)
    $ip = [System.Net.IPAddress]::Parse($Address)
    $bytes = $ip.GetAddressBytes()
    [array]::Reverse($bytes)
    return [BitConverter]::ToUInt32($bytes, 0)
}

function Test-IPv4InSubnet {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][string]$Address,
        [Parameter(Mandatory = $true)][string]$NetworkAddress,
        [Parameter(Mandatory = $true)][int]$PrefixLength
    )
    $mask = [uint32]([math]::Pow(2, 32) - [math]::Pow(2, (32 - $PrefixLength)))
    $addrInt = Convert-IPv4ToUInt32 -Address $Address
    $netInt = Convert-IPv4ToUInt32 -Address $NetworkAddress
    return (($addrInt -band $mask) -eq ($netInt -band $mask))
}

function Assert-RequiredTopLevelSections {
    <#
    .SYNOPSIS
    Ensures every required top-level section exists.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    $required = @(
        'schemaVersion','environment','execution','proxmoxGuest','network','roles','activeDirectory','dns','dhcp',
        'time','organizationalUnits','groups','serviceAccounts','gpo','hardening','defender','firewall',
        'eventForwarding','wazuh','pki','wsus','backupRecovery','vulnerabilityScanning','identityIntegrations',
        'validation','reporting'
    )
    foreach ($name in $required) {
        if ($null -eq $Config.PSObject.Properties[$name]) {
            throw "Missing required top-level section: $name"
        }
    }
}

function Test-ConfigPathExists {
    <#
    .SYNOPSIS
    Validates that the YAML configuration path exists.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [ValidateNotNullOrEmpty()]
        [string]$ConfigPath
    )

    if (-not (Test-Path -LiteralPath $ConfigPath -PathType Leaf)) {
        throw "Config path does not exist: $ConfigPath"
    }
}

function Test-ConfigSchemaVersion {
    <#
    .SYNOPSIS
    Validates schemaVersion support.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [pscustomobject]$Config
    )

    if ($null -eq $Config.schemaVersion) {
        throw 'schemaVersion is required.'
    }
    if ([int]$Config.schemaVersion -ne 1) {
        throw "Unsupported schemaVersion: $($Config.schemaVersion). Supported: 1."
    }
}

function Get-RequiredConfigValue {
    <#
    .SYNOPSIS
    Returns a required value or throws.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [pscustomobject]$Config,
        [Parameter(Mandatory = $true)]
        [ValidateNotNullOrEmpty()]
        [string]$Path
    )

    $cursor = $Config
    foreach ($segment in ($Path -split '\.')) {
        if ($cursor -is [System.Collections.IDictionary]) {
            if (-not $cursor.Contains($segment)) {
                throw "Missing required setting: $Path"
            }
            $cursor = $cursor[$segment]
        }
        else {
            if ($null -eq $cursor.PSObject.Properties[$segment]) {
                throw "Missing required setting: $Path"
            }
            $cursor = $cursor.$segment
        }
    }
    if ($null -eq $cursor) {
        throw "Required setting is null: $Path"
    }
    if ($cursor -is [string] -and [string]::IsNullOrWhiteSpace($cursor)) {
        throw "Required setting is empty: $Path"
    }
    if ($cursor -is [System.Collections.IEnumerable] -and -not ($cursor -is [string])) {
        if (@($cursor).Count -eq 0) {
            throw "Required list is empty: $Path"
        }
    }
    return $cursor
}

function Assert-NoUnknownTopLevelSections {
    <#
    .SYNOPSIS
    Ensures no unknown top-level sections exist.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [pscustomobject]$Config
    )

    $known = @(
        'schemaVersion','environment','execution','proxmoxGuest','network','roles','activeDirectory','dns','dhcp',
        'time','organizationalUnits','groups','serviceAccounts','gpo','hardening','defender','firewall',
        'eventForwarding','wazuh','pki','wsus','backupRecovery','vulnerabilityScanning','identityIntegrations',
        'validation','reporting'
    )
    $actual = @($Config.PSObject.Properties.Name)
    $unknown = $actual | Where-Object { $_ -notin $known }
    if ($unknown) {
        throw "Unknown top-level section(s): $($unknown -join ', ')"
    }
}

function Assert-FeatureEnabledFlagsPresent {
    <#
    .SYNOPSIS
    Ensures each feature section has explicit enabled flag.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [pscustomobject]$Config
    )

    $sections = @(
        'proxmoxGuest','network','activeDirectory','dns','dhcp','time','organizationalUnits','groups',
        'serviceAccounts','gpo','hardening','defender','firewall','eventForwarding','wazuh',
        'pki','wsus','backupRecovery','vulnerabilityScanning','identityIntegrations','validation','reporting'
    )
    foreach ($section in $sections) {
        $value = Get-RequiredConfigValue -Config $Config -Path $section
        $hasEnabled = $false
        $enabledValue = $null
        if ($value -is [System.Collections.IDictionary]) {
            $hasEnabled = $value.Contains('enabled')
            if ($hasEnabled) { $enabledValue = $value['enabled'] }
        }
        else {
            $hasEnabled = ($null -ne $value.PSObject.Properties['enabled'])
            if ($hasEnabled) { $enabledValue = $value.enabled }
        }
        if (-not $hasEnabled) {
            throw "Missing required enabled flag: $section.enabled"
        }
        if ($enabledValue -isnot [bool]) {
            throw "enabled flag must be true/false: $section.enabled"
        }
    }
}

function Assert-RequiredSettingsForEnabledFeatures {
    <#
    .SYNOPSIS
    Validates required settings for enabled features.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [pscustomobject]$Config
    )

    Get-RequiredConfigValue -Config $Config -Path 'execution.statePath' | Out-Null
    Get-RequiredConfigValue -Config $Config -Path 'execution.logPath' | Out-Null
    Get-RequiredConfigValue -Config $Config -Path 'execution.transcriptPath' | Out-Null
    Get-RequiredConfigValue -Config $Config -Path 'execution.jsonLogPath' | Out-Null
    Get-RequiredConfigValue -Config $Config -Path 'execution.evidencePath' | Out-Null
    Get-RequiredConfigValue -Config $Config -Path 'execution.resumeScheduledTaskName' | Out-Null

    if ($Config.network.enabled) {
        Get-RequiredConfigValue -Config $Config -Path 'network.interfaceAlias' | Out-Null
        Get-RequiredConfigValue -Config $Config -Path 'network.computerName' | Out-Null
        Get-RequiredConfigValue -Config $Config -Path 'network.timeZone' | Out-Null
        $ip = Get-RequiredConfigValue -Config $Config -Path 'network.ipv4.address'
        if (-not [System.Net.IPAddress]::TryParse($ip, [ref]([ipaddress]::Any))) { throw 'network.ipv4.address must be a valid IP address.' }
        if ($ip -notmatch '^\d{1,3}(\.\d{1,3}){3}$') { throw 'network.ipv4.address must be IPv4.' }
        $prefix = [int](Get-RequiredConfigValue -Config $Config -Path 'network.ipv4.prefixLength')
        if ($prefix -lt 1 -or $prefix -gt 32) { throw 'network.ipv4.prefixLength must be 1..32.' }
        $gateway = [string](Get-RequiredConfigValue -Config $Config -Path 'network.ipv4.defaultGateway')
        if (-not [System.Net.IPAddress]::TryParse($gateway, [ref]([ipaddress]::Any))) { throw 'network.ipv4.defaultGateway must be a valid IP address.' }
    }

    if ($Config.activeDirectory.enabled) {
        $domainName = Get-RequiredConfigValue -Config $Config -Path 'activeDirectory.domainName'
        $netbios = Get-RequiredConfigValue -Config $Config -Path 'activeDirectory.netbiosName'
        if ($netbios.Length -lt 1 -or $netbios.Length -gt 15) { throw 'activeDirectory.netbiosName must be 1..15 characters.' }
        if ($domainName -notmatch '\.') {
            if (-not $Config.activeDirectory.allowSingleLabelDomain) { throw 'Single-label domain names are not allowed unless activeDirectory.allowSingleLabelDomain is true.' }
        }
        if ($domainName.EndsWith('.local') -and -not $Config.activeDirectory.allowDotLocal) {
            throw 'Domain names ending with .local are not allowed unless activeDirectory.allowDotLocal is true.'
        }
    }

    if ($Config.dns.enabled) {
        $forwarders = @(Get-RequiredConfigValue -Config $Config -Path 'dns.forwarders')
        $dcIp = $Config.network.ipv4.address
        foreach ($forwarder in $forwarders) {
            if (-not [System.Net.IPAddress]::TryParse([string]$forwarder, [ref]([ipaddress]::Any))) {
                throw "dns.forwarders contains invalid IP address: $forwarder"
            }
        }
        if (-not $Config.dns.allowForwardersPointingToSelf) {
            if ($forwarders -contains $dcIp) {
                throw 'dns.forwarders must not include the domain controller IP unless dns.allowForwardersPointingToSelf is true.'
            }
        }
    }

    if ($Config.time.enabled -and $Config.time.authoritativeForDomain) {
        $servers = @(Get-RequiredConfigValue -Config $Config -Path 'time.externalNtpServers')
        if (@($servers).Count -lt 1) { throw 'time.externalNtpServers must be non-empty for authoritative domain time.' }
        $allowed = @('stop','warn','skip')
        if ($Config.time.behaviorIfNotPdc -notin $allowed) {
            throw "time.behaviorIfNotPdc must be one of: $($allowed -join ', ')"
        }
    }

    if ($Config.dhcp.enabled) {
        Get-RequiredConfigValue -Config $Config -Path 'dhcp.serverDnsName' | Out-Null
        Get-RequiredConfigValue -Config $Config -Path 'dhcp.serverIpAddress' | Out-Null
        Get-RequiredConfigValue -Config $Config -Path 'dhcp.reconcileExisting' | Out-Null
        foreach ($scope in @($Config.dhcp.scopes)) {
            foreach ($required in @('name','scopeId','startRange','endRange','subnetMask','leaseDuration','state')) {
                if ($null -eq $scope.$required -or ($scope.$required -is [string] -and [string]::IsNullOrWhiteSpace($scope.$required))) {
                    throw "dhcp.scopes.$required is required."
                }
            }
            foreach ($ipKey in @('scopeId','startRange','endRange','subnetMask')) {
                if (-not [System.Net.IPAddress]::TryParse([string]$scope.$ipKey, [ref]([ipaddress]::Any))) {
                    throw "Invalid IPv4 value in DHCP scope '$($scope.name)': $ipKey=$($scope.$ipKey)"
                }
            }
            $subnetPrefix = (24)
            if ($scope.subnetMask -eq '255.255.255.0') { $subnetPrefix = 24 }
            elseif ($scope.subnetMask -eq '255.255.0.0') { $subnetPrefix = 16 }
            elseif ($scope.subnetMask -eq '255.0.0.0') { $subnetPrefix = 8 }
            elseif ($scope.subnetMask -eq '255.255.255.128') { $subnetPrefix = 25 }
            elseif ($scope.subnetMask -eq '255.255.255.192') { $subnetPrefix = 26 }
            elseif ($scope.subnetMask -eq '255.255.255.224') { $subnetPrefix = 27 }
            elseif ($scope.subnetMask -eq '255.255.255.240') { $subnetPrefix = 28 }
            elseif ($scope.subnetMask -eq '255.255.255.248') { $subnetPrefix = 29 }
            elseif ($scope.subnetMask -eq '255.255.255.252') { $subnetPrefix = 30 }
            else { throw "Unsupported DHCP subnet mask in scope '$($scope.name)': $($scope.subnetMask)" }

            if (-not (Test-IPv4InSubnet -Address $scope.startRange -NetworkAddress $scope.scopeId -PrefixLength $subnetPrefix)) {
                throw "DHCP scope startRange not inside scope subnet for '$($scope.name)'."
            }
            if (-not (Test-IPv4InSubnet -Address $scope.endRange -NetworkAddress $scope.scopeId -PrefixLength $subnetPrefix)) {
                throw "DHCP scope endRange not inside scope subnet for '$($scope.name)'."
            }
            $startInt = Convert-IPv4ToUInt32 -Address $scope.startRange
            $endInt = Convert-IPv4ToUInt32 -Address $scope.endRange
            if ($startInt -gt $endInt) {
                throw "DHCP scope startRange must be <= endRange for '$($scope.name)'."
            }
            foreach ($reservation in @($scope.reservations)) {
                if (-not [System.Net.IPAddress]::TryParse([string]$reservation.ipAddress, [ref]([ipaddress]::Any))) {
                    throw "DHCP reservation IP is invalid in scope '$($scope.name)': $($reservation.ipAddress)"
                }
                if (-not (Test-IPv4InSubnet -Address $reservation.ipAddress -NetworkAddress $scope.scopeId -PrefixLength $subnetPrefix)) {
                    throw "DHCP reservation IP is outside scope subnet in '$($scope.name)': $($reservation.ipAddress)"
                }
            }
        }
    }

    if ($Config.gpo.enabled) {
        Get-RequiredConfigValue -Config $Config -Path 'gpo.allowModifyDefaultDomainPolicy' | Out-Null
        $names = @($Config.gpo.gpos | ForEach-Object { $_.name })
        if (@($names | Select-Object -Unique).Count -ne @($names).Count) { throw 'Duplicate GPO names are not allowed.' }
        foreach ($gpo in @($Config.gpo.gpos)) {
            if ($null -eq $gpo.linkOrder) { throw "gpo.gpos.linkOrder is required for $($gpo.name)." }
        }
    }

    if ($Config.organizationalUnits.enabled) {
        $ouNames = @($Config.organizationalUnits.structure | ForEach-Object { $_.distinguishedNameRelative })
        if (@($ouNames | Select-Object -Unique).Count -ne @($ouNames).Count) { throw 'Duplicate OU distinguishedNameRelative values are not allowed.' }
    }

    if ($Config.groups.enabled) {
        $groupNames = @($Config.groups.items | ForEach-Object { $_.name })
        if (@($groupNames | Select-Object -Unique).Count -ne @($groupNames).Count) { throw 'Duplicate group names are not allowed.' }
    }

    if ($Config.serviceAccounts.enabled) {
        $sam = @($Config.serviceAccounts.accounts | ForEach-Object { $_.samAccountName })
        if (@($sam | Select-Object -Unique).Count -ne @($sam).Count) { throw 'Duplicate service account sAMAccountName values are not allowed.' }
    }

    foreach ($pathKey in @('execution.statePath','execution.logPath','execution.transcriptPath','execution.jsonLogPath','execution.evidencePath')) {
        $value = [string](Get-RequiredConfigValue -Config $Config -Path $pathKey)
        if (-not (Test-IsAbsoluteWindowsPath -PathValue $value)) {
            throw "$pathKey must be an absolute Windows path."
        }
    }
}

function Import-ProjectConfig {
    <#
    .SYNOPSIS
    Imports YAML config using required parser module.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [ValidateNotNullOrEmpty()]
        [string]$ConfigPath
    )

    Test-ConfigPathExists -ConfigPath $ConfigPath

    if (-not (Get-Module -ListAvailable -Name powershell-yaml)) {
        throw 'Required module powershell-yaml is missing. Install with: Install-Module powershell-yaml -Scope AllUsers'
    }

    Import-Module powershell-yaml -ErrorAction Stop
    $raw = Get-Content -LiteralPath $ConfigPath -Raw -Encoding UTF8
    $config = ConvertFrom-Yaml -Yaml $raw
    if ($null -eq $config) {
        throw 'Config file did not parse as valid YAML.'
    }
    return [pscustomobject]$config
}

function Assert-ProjectConfig {
    <#
    .SYNOPSIS
    Runs strict project configuration validation.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [pscustomobject]$Config
    )

    Assert-RequiredTopLevelSections -Config $Config
    Test-ConfigSchemaVersion -Config $Config
    Assert-NoUnknownTopLevelSections -Config $Config
    Assert-FeatureEnabledFlagsPresent -Config $Config
    Assert-RequiredSettingsForEnabledFeatures -Config $Config
}
