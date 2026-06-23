<#
.SYNOPSIS
    Interactive console wizard (TUI) that builds a validated config.yaml for
    Configure-WindowsServer.ps1.

.DESCRIPTION
    Walks an operator through every environment-specific setting the Windows Server
    identity-host build needs, validating each answer LIVE (IP addresses, prefix
    lengths, NetBIOS/domain rules, DHCP ranges, uniqueness, etc.) and re-prompting on
    bad input. Settings that are a reviewed security/policy baseline rather than
    per-environment values (GPOs, hardening, firewall, Defender, OU/group structure,
    validation/reporting) are inherited from config.example.yaml and should be reviewed
    directly in the generated file.

    The reviewed baseline is loaded from config.example.yaml (or an existing config.yaml
    if you choose to edit it), the wizard overlays your answers, writes config.yaml, and
    then runs the project's own Assert-ProjectConfig validator as a final gate so the
    file is guaranteed to load cleanly into Configure-WindowsServer.ps1.

    PowerShell only, no extra dependencies beyond the powershell-yaml module that the
    main script already requires. Run it on the Windows Server you are configuring.

.PARAMETER ExamplePath
    Template to seed the baseline from. Default: .\config.example.yaml.

.PARAMETER OutputPath
    Where to write the generated operator config. Default: .\config.yaml.

.EXAMPLE
    .\New-WindowsServerConfig.ps1

.EXAMPLE
    .\New-WindowsServerConfig.ps1 -OutputPath .\config.yaml
#>
[CmdletBinding()]
param(
    [string]$ExamplePath = (Join-Path (Split-Path -Parent $PSCommandPath) 'config.example.yaml'),
    [string]$OutputPath = (Join-Path (Split-Path -Parent $PSCommandPath) 'config.yaml')
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# --------------------------------------------------------------------------------------
# Dependencies
# --------------------------------------------------------------------------------------
if (-not (Get-Module -ListAvailable -Name powershell-yaml)) {
    throw 'Required module powershell-yaml is missing. Install with: Install-Module powershell-yaml -Scope AllUsers'
}
Import-Module powershell-yaml -ErrorAction Stop

# --------------------------------------------------------------------------------------
# Console helpers
# --------------------------------------------------------------------------------------
function Write-Banner {
    param([string]$Text)
    Write-Host ''
    Write-Host ('=' * 78) -ForegroundColor DarkCyan
    Write-Host "  $Text" -ForegroundColor Cyan
    Write-Host ('=' * 78) -ForegroundColor DarkCyan
}

function Write-Note {
    param([string]$Text)
    Write-Host "  $Text" -ForegroundColor DarkGray
}

function Write-FieldHelp {
    param(
        [string]$Title,
        [string]$Description
    )
    Write-Host ''
    Write-Host "  $Title" -ForegroundColor White
    Write-Host ('  ' + ('─' * 48)) -ForegroundColor DarkGray
    Write-Host "  $Description" -ForegroundColor DarkGray
}

function Write-Bad {
    param([string]$Text)
    Write-Host "  ! $Text" -ForegroundColor Yellow
}

# Test-* validators return $null when valid, otherwise a human-readable error string.
function Test-IPv4Value {
    param([string]$Value)
    $any = [ipaddress]::Any
    if (($Value -match '^\d{1,3}(\.\d{1,3}){3}$') -and [ipaddress]::TryParse($Value, [ref]$any)) { return $null }
    return 'Enter a valid IPv4 address (e.g. 192.168.1.10).'
}

function Test-AbsoluteWindowsPath {
    param([string]$Value)
    if ($Value -match '^[A-Za-z]:\\' -or $Value -match '^\\\\') { return $null }
    return 'Enter an absolute Windows path (e.g. C:\ProgramData\App or \\server\share).'
}

function ConvertTo-UInt32IPv4 {
    param([string]$Address)
    $bytes = ([ipaddress]::Parse($Address)).GetAddressBytes()
    [array]::Reverse($bytes)
    return [BitConverter]::ToUInt32($bytes, 0)
}

# Maps the dotted subnet masks the project supports to a prefix length.
$script:SupportedMasks = [ordered]@{
    '255.255.255.0'   = 24
    '255.255.0.0'     = 16
    '255.0.0.0'       = 8
    '255.255.255.128' = 25
    '255.255.255.192' = 26
    '255.255.255.224' = 27
    '255.255.255.240' = 28
    '255.255.255.248' = 29
    '255.255.255.252' = 30
}

function Test-IPv4InSubnetValue {
    param([string]$Address, [string]$NetworkAddress, [int]$PrefixLength)
    $mask = [uint32]([math]::Pow(2, 32) - [math]::Pow(2, (32 - $PrefixLength)))
    return ((ConvertTo-UInt32IPv4 $Address) -band $mask) -eq ((ConvertTo-UInt32IPv4 $NetworkAddress) -band $mask)
}

# Read-* helpers re-prompt until the answer is valid. Pressing Enter keeps the current
# value (shown in brackets) when one exists.
function Read-Text {
    param(
        [string]$Label,
        [string]$Current,
        [scriptblock]$Validate,
        [switch]$AllowEmpty
    )
    while ($true) {
        $hint = ''
        if (-not [string]::IsNullOrEmpty($Current)) { $hint = " [$Current]" }
        $answer = Read-Host "$Label$hint"
        if ([string]::IsNullOrWhiteSpace($answer)) {
            if (-not [string]::IsNullOrEmpty($Current)) { return $Current }
            if ($AllowEmpty) { return '' }
            Write-Bad 'A value is required.'
            continue
        }
        $answer = $answer.Trim()
        if ($Validate) {
            $err = & $Validate $answer
            if ($err) { Write-Bad $err; continue }
        }
        return $answer
    }
}

function Read-YesNo {
    param([string]$Label, [bool]$Current)
    $shown = if ($Current) { 'Y/n' } else { 'y/N' }
    while ($true) {
        $answer = Read-Host "$Label [$shown]"
        if ([string]::IsNullOrWhiteSpace($answer)) { return $Current }
        switch -regex ($answer.Trim().ToLower()) {
            '^(y|yes)$' { return $true }
            '^(n|no)$' { return $false }
            default { Write-Bad 'Enter y or n.' }
        }
    }
}

function Read-Choice {
    param([string]$Label, [string[]]$Options, [string]$Current)
    while ($true) {
        Write-Host $Label
        for ($i = 0; $i -lt $Options.Count; $i++) {
            $mark = if ($Options[$i] -eq $Current) { ' (current)' } else { '' }
            Write-Host ("    [{0}] {1}{2}" -f ($i + 1), $Options[$i], $mark)
        }
        $answer = Read-Host "Select 1-$($Options.Count)"
        if ([string]::IsNullOrWhiteSpace($answer) -and -not [string]::IsNullOrEmpty($Current)) { return $Current }
        $n = 0
        if ([int]::TryParse($answer, [ref]$n) -and $n -ge 1 -and $n -le $Options.Count) { return $Options[$n - 1] }
        Write-Bad 'Invalid selection.'
    }
}

function Read-IntInRange {
    param([string]$Label, [int]$Min, [int]$Max, $Current)
    $validate = {
        param($x)
        $n = 0
        if (-not [int]::TryParse($x, [ref]$n)) { return 'Enter a whole number.' }
        if ($n -lt $Min -or $n -gt $Max) { return "Must be between $Min and $Max." }
        return $null
    }.GetNewClosure()
    $value = Read-Text -Label "$Label ($Min-$Max)" -Current ([string]$Current) -Validate $validate
    return [int]$value
}

function Read-IPv4 {
    param([string]$Label, [string]$Current)
    return Read-Text -Label $Label -Current $Current -Validate { param($v) Test-IPv4Value $v }
}

function Read-IPv4List {
    param([string]$Label, [string[]]$Current, [scriptblock]$ExtraValidate)
    Write-Note "$Label - comma-separated IPv4. Press Enter to keep: $($Current -join ', ')"
    while ($true) {
        $answer = Read-Host 'Value'
        if ([string]::IsNullOrWhiteSpace($answer)) { return , $Current }
        $items = @($answer -split ',' | ForEach-Object { $_.Trim() } | Where-Object { $_ })
        if ($items.Count -eq 0) { Write-Bad 'Enter at least one address.'; continue }
        $bad = @($items | Where-Object { Test-IPv4Value $_ })
        if ($bad.Count -gt 0) { Write-Bad "Invalid IPv4: $($bad -join ', ')"; continue }
        if ($ExtraValidate) {
            $err = & $ExtraValidate $items
            if ($err) { Write-Bad $err; continue }
        }
        return , $items
    }
}

# --------------------------------------------------------------------------------------
# Load the baseline
# --------------------------------------------------------------------------------------
Write-Banner 'Windows Identity Services Deployer - configuration wizard'
Write-Note 'Builds and validates config.yaml. Press Ctrl+C any time to abort (nothing is'
Write-Note 'written until the very end).'

$basePath = $ExamplePath
if (Test-Path -LiteralPath $OutputPath) {
    Write-Host ''
    if (Read-YesNo "An existing config.yaml was found. Edit it instead of starting from the template?" $true) {
        $basePath = $OutputPath
    }
}
if (-not (Test-Path -LiteralPath $basePath)) {
    throw "Baseline config not found: $basePath"
}
Write-Note "Baseline: $basePath"
$cfg = ConvertFrom-Yaml -Yaml (Get-Content -LiteralPath $basePath -Raw -Encoding UTF8)
if ($null -eq $cfg) { throw "Baseline did not parse as YAML: $basePath" }

# --------------------------------------------------------------------------------------
# execution
# --------------------------------------------------------------------------------------
Write-Banner '1/10  Execution paths and behavior'
Write-Note 'Where the script stores state, logs, and proof-of-work on this server.'
Write-Note 'Use absolute Windows paths. Press Enter to keep the bracketed default.'
$exec = $cfg['execution']
Write-FieldHelp 'State path' 'Checkpoint/resume data so the run can continue after a reboot mid-promotion.'
$exec['statePath'] = Read-Text -Label 'State path' -Current ([string]$exec['statePath']) -Validate { param($v) Test-AbsoluteWindowsPath $v }
Write-FieldHelp 'Log path' 'Folder for general run logs (errors and step messages).'
$exec['logPath'] = Read-Text -Label 'Log path' -Current ([string]$exec['logPath']) -Validate { param($v) Test-AbsoluteWindowsPath $v }
Write-FieldHelp 'Transcript path' 'Full PowerShell transcript file (commands and output) for this run.'
$exec['transcriptPath'] = Read-Text -Label 'Transcript path' -Current ([string]$exec['transcriptPath']) -Validate { param($v) Test-AbsoluteWindowsPath $v }
Write-FieldHelp 'JSON operation log path' 'Machine-readable log file (one JSON record per line) for auditing or tooling.'
$exec['jsonLogPath'] = Read-Text -Label 'JSON operation log path' -Current ([string]$exec['jsonLogPath']) -Validate { param($v) Test-AbsoluteWindowsPath $v }
Write-FieldHelp 'Evidence path' 'Folder for validation artifacts: dcdiag, repadmin, GPO reports, summaries, final report.'
$exec['evidencePath'] = Read-Text -Label 'Evidence path' -Current ([string]$exec['evidencePath']) -Validate { param($v) Test-AbsoluteWindowsPath $v }
Write-FieldHelp 'Resume scheduled task name' 'Windows scheduled task name that re-runs the script after reboot during AD promotion.'
$exec['resumeScheduledTaskName'] = Read-Text -Label 'Resume scheduled task name' -Current ([string]$exec['resumeScheduledTaskName'])

# --------------------------------------------------------------------------------------
# proxmoxGuest
# --------------------------------------------------------------------------------------
Write-Banner '2/10  Proxmox guest integration'
$pmx = $cfg['proxmoxGuest']
$pmx['enabled'] = Read-YesNo 'Is this server a Proxmox VM (check VirtIO/QEMU guest agent)?' ([bool]$pmx['enabled'])
if ($pmx['enabled']) {
    $pmx['requireVirtioDrivers'] = Read-YesNo '  Require VirtIO drivers present?' ([bool]$pmx['requireVirtioDrivers'])
    $pmx['requireQemuGuestAgent'] = Read-YesNo '  Require QEMU Guest Agent service?' ([bool]$pmx['requireQemuGuestAgent'])
    $pmx['allowSilentGuestToolsInstall'] = Read-YesNo '  Allow silent guest-tools install if missing?' ([bool]$pmx['allowSilentGuestToolsInstall'])
    if ($pmx['allowSilentGuestToolsInstall']) {
        $pmx['guestToolsInstallerPath'] = Read-Text -Label '  Guest tools installer path' -Current ([string]$pmx['guestToolsInstallerPath'])
    }
}

# --------------------------------------------------------------------------------------
# network
# --------------------------------------------------------------------------------------
Write-Banner '3/10  Network and host identity'
$net = $cfg['network']
$net['enabled'] = $true
$net['computerName'] = Read-Text -Label 'Computer name (hostname)' -Current ([string]$net['computerName']) -Validate {
    param($v)
    if ($v.Length -lt 1 -or $v.Length -gt 15) { return 'Hostname must be 1-15 characters.' }
    if ($v -notmatch '^[A-Za-z0-9-]+$') { return 'Hostname may contain only letters, digits, and hyphens.' }
    return $null
}
$net['interfaceAlias'] = Read-Text -Label 'Network interface alias (e.g. Ethernet)' -Current ([string]$net['interfaceAlias'])
$net['timeZone'] = Read-Text -Label 'Time zone (e.g. UTC, Eastern Standard Time)' -Current ([string]$net['timeZone'])
$ipv4 = $net['ipv4']
$ipv4['address'] = Read-IPv4 -Label 'Static IPv4 address' -Current ([string]$ipv4['address'])
$ipv4['prefixLength'] = Read-IntInRange -Label 'IPv4 prefix length' -Min 1 -Max 32 -Current $ipv4['prefixLength']
$ipv4['defaultGateway'] = Read-IPv4 -Label 'Default gateway' -Current ([string]$ipv4['defaultGateway'])
Write-Note 'Before promotion the server should point DNS at itself; after promotion at loopback.'
$ipv4['dnsClientServersBeforePromotion'] = Read-IPv4List -Label 'DNS servers BEFORE promotion' -Current @($ipv4['dnsClientServersBeforePromotion'])
$ipv4['dnsClientServersAfterPromotion'] = Read-IPv4List -Label 'DNS servers AFTER promotion' -Current @($ipv4['dnsClientServersAfterPromotion'])

# --------------------------------------------------------------------------------------
# activeDirectory
# --------------------------------------------------------------------------------------
Write-Banner '4/10  Active Directory (new forest)'
$ad = $cfg['activeDirectory']
$ad['enabled'] = $true
$ad['allowDotLocal'] = [bool]$ad['allowDotLocal']
$ad['allowSingleLabelDomain'] = [bool]$ad['allowSingleLabelDomain']
$adValidate = {
    param($v)
    if ($v -notmatch '\.' -and -not $ad['allowSingleLabelDomain']) { return 'Single-label domains are not allowed. Use a dotted FQDN (e.g. corp.example.com).' }
    if ($v.ToLower().EndsWith('.local') -and -not $ad['allowDotLocal']) { return '.local domains are discouraged and not allowed by this config.' }
    return $null
}.GetNewClosure()
$ad['domainName'] = Read-Text -Label 'AD domain FQDN (e.g. corp.example.com)' -Current ([string]$ad['domainName']) -Validate $adValidate
$ad['netbiosName'] = Read-Text -Label 'NetBIOS name (1-15 chars, e.g. CORP)' -Current ([string]$ad['netbiosName']) -Validate {
    param($v)
    if ($v.Length -lt 1 -or $v.Length -gt 15) { return 'NetBIOS name must be 1-15 characters.' }
    if ($v -notmatch '^[A-Za-z0-9-]+$') { return 'NetBIOS name may contain only letters, digits, and hyphens.' }
    return $null
}
$ad['forestMode'] = Read-Text -Label 'Forest functional level' -Current ([string]$ad['forestMode'])
$ad['domainMode'] = Read-Text -Label 'Domain functional level' -Current ([string]$ad['domainMode'])
$ad['databasePath'] = Read-Text -Label 'NTDS database path' -Current ([string]$ad['databasePath']) -Validate { param($v) Test-AbsoluteWindowsPath $v }
$ad['logPath'] = Read-Text -Label 'NTDS log path' -Current ([string]$ad['logPath']) -Validate { param($v) Test-AbsoluteWindowsPath $v }
$ad['sysvolPath'] = Read-Text -Label 'SYSVOL path' -Current ([string]$ad['sysvolPath']) -Validate { param($v) Test-AbsoluteWindowsPath $v }
if ($ad.Contains('site')) {
    $ad['site']['renameDefaultSite'] = Read-YesNo 'Rename the default AD site?' ([bool]$ad['site']['renameDefaultSite'])
    if ($ad['site']['renameDefaultSite']) {
        $ad['site']['newSiteName'] = Read-Text -Label '  New site name' -Current ([string]$ad['site']['newSiteName'])
    }
}

# --------------------------------------------------------------------------------------
# dns
# --------------------------------------------------------------------------------------
Write-Banner '5/10  DNS'
$dns = $cfg['dns']
$dns['enabled'] = $true
$dns['allowForwardersPointingToSelf'] = [bool]$dns['allowForwardersPointingToSelf']
$dcIp = [string]$ipv4['address']
$fwdValidate = {
    param($items)
    if (-not $dns['allowForwardersPointingToSelf'] -and ($items -contains $dcIp)) {
        return "Forwarders must not include this server's own IP ($dcIp)."
    }
    return $null
}.GetNewClosure()
$dns['forwarders'] = Read-IPv4List -Label 'DNS forwarders' -Current @($dns['forwarders']) -ExtraValidate $fwdValidate
# Reverse lookup zone(s): default to this host's /24.
$defaultRevNet = ($dcIp -replace '\.\d+$', '.0') + '/24'
if (Read-YesNo "Create a reverse lookup zone for ${defaultRevNet}?" $true) {
    $zone = @{ networkId = $defaultRevNet; replicationScope = 'Forest' }
    $dns['createReverseLookupZones'] = $true
    $dns['reverseLookupZones'] = @($zone)
}
# Validation records derived from the domain name.
$dns['requiredRecordsToValidate'] = @(
    @{ name = [string]$ad['domainName']; type = 'A' },
    @{ name = "_ldap._tcp.dc._msdcs.$([string]$ad['domainName'])"; type = 'SRV' }
)

# --------------------------------------------------------------------------------------
# dhcp
# --------------------------------------------------------------------------------------
Write-Banner '6/10  DHCP'
$dhcp = $cfg['dhcp']
$dhcp['enabled'] = Read-YesNo 'Configure DHCP on this server?' ([bool]$dhcp['enabled'])
if ($dhcp['enabled']) {
    $dhcp['authorizeInActiveDirectory'] = Read-YesNo '  Authorize the DHCP server in Active Directory?' ([bool]$dhcp['authorizeInActiveDirectory'])
    $dhcp['reconcileExisting'] = Read-YesNo '  Reconcile/overwrite an existing conflicting scope?' ([bool]$dhcp['reconcileExisting'])
    $dhcp['serverDnsName'] = Read-Text -Label '  DHCP server DNS name (FQDN)' -Current ([string]$dhcp['serverDnsName'])
    $dhcp['serverIpAddress'] = Read-IPv4 -Label '  DHCP server IP address' -Current ([string]$dhcp['serverIpAddress'])
    if (Read-YesNo '  Redefine DHCP scopes now (otherwise keep the baseline scopes)?' $false) {
        $scopes = @()
        do {
            Write-Host ''
            Write-Note "Scope #$($scopes.Count + 1)"
            $name = Read-Text -Label '  Scope name' -Current ''
            $mask = Read-Choice -Label '  Subnet mask:' -Options @($script:SupportedMasks.Keys) -Current '255.255.255.0'
            $prefix = [int]$script:SupportedMasks[$mask]
            $scopeId = Read-Text -Label '  Scope network ID (e.g. 192.168.10.0)' -Current '' -Validate { param($v) Test-IPv4Value $v }
            $startValidate = {
                param($v)
                $e = Test-IPv4Value $v; if ($e) { return $e }
                if (-not (Test-IPv4InSubnetValue -Address $v -NetworkAddress $scopeId -PrefixLength $prefix)) { return "Address is not inside $scopeId/$prefix." }
                return $null
            }.GetNewClosure()
            $startRange = Read-Text -Label '  Start of range' -Current '' -Validate $startValidate
            $endValidate = {
                param($v)
                $e = Test-IPv4Value $v; if ($e) { return $e }
                if (-not (Test-IPv4InSubnetValue -Address $v -NetworkAddress $scopeId -PrefixLength $prefix)) { return "Address is not inside $scopeId/$prefix." }
                if ((ConvertTo-UInt32IPv4 $v) -lt (ConvertTo-UInt32IPv4 $startRange)) { return 'End of range must be >= start of range.' }
                return $null
            }.GetNewClosure()
            $endRange = Read-Text -Label '  End of range' -Current '' -Validate $endValidate
            $router = Read-IPv4List -Label '  Router (gateway) option' -Current @($scopeId -replace '\.\d+$', '.1')
            $dnsServers = Read-IPv4List -Label '  DNS servers option' -Current @($dcIp)
            $dnsDomain = Read-Text -Label '  DNS domain option' -Current ([string]$ad['domainName'])
            $ntpServers = Read-IPv4List -Label '  NTP servers option' -Current @($dcIp)
            $scope = @{
                name         = $name
                scopeId      = $scopeId
                startRange   = $startRange
                endRange     = $endRange
                subnetMask   = $mask
                leaseDuration = '8.00:00:00'
                state        = 'Active'
                options      = @{
                    router     = $router
                    dnsServers = $dnsServers
                    dnsDomain  = $dnsDomain
                    ntpServers = $ntpServers
                }
                reservations = @()
            }
            $scopes += $scope
        } while (Read-YesNo '  Add another scope?' $false)
        $dhcp['scopes'] = $scopes
    }
}

# --------------------------------------------------------------------------------------
# time
# --------------------------------------------------------------------------------------
Write-Banner '7/10  Domain time'
$time = $cfg['time']
$time['enabled'] = $true
$time['authoritativeForDomain'] = Read-YesNo 'Make this server authoritative time source for the domain?' ([bool]$time['authoritativeForDomain'])
if ($time['authoritativeForDomain']) {
    Write-Note 'External NTP servers are DNS names or IPs; at least one is required.'
    while ($true) {
        $answer = Read-Host "External NTP servers (comma-separated) [$(@($time['externalNtpServers']) -join ', ')]"
        if ([string]::IsNullOrWhiteSpace($answer)) { break }
        $items = @($answer -split ',' | ForEach-Object { $_.Trim() } | Where-Object { $_ })
        if ($items.Count -lt 1) { Write-Bad 'Enter at least one NTP server.'; continue }
        $time['externalNtpServers'] = $items
        break
    }
    $time['behaviorIfNotPdc'] = Read-Choice -Label 'If this server is NOT the PDC emulator:' -Options @('stop', 'warn', 'skip') -Current ([string]$time['behaviorIfNotPdc'])
}

# --------------------------------------------------------------------------------------
# serviceAccounts
# --------------------------------------------------------------------------------------
Write-Banner '8/10  Service accounts'
$svc = $cfg['serviceAccounts']
$svc['enabled'] = Read-YesNo 'Create service accounts?' ([bool]$svc['enabled'])
if ($svc['enabled']) {
    $existing = @($svc['accounts'] | ForEach-Object { $_['samAccountName'] })
    Write-Note "Baseline accounts: $($existing -join ', ')"
    if (Read-YesNo '  Redefine the service account list now?' $false) {
        $accounts = @()
        do {
            $sam = Read-Text -Label '  sAMAccountName (e.g. svc-app-ldap)' -Current ''
            $desc = Read-Text -Label '  Description' -Current "$sam service account"
            $accounts += @{
                name                  = $sam
                samAccountName        = $sam
                type                  = 'standard'
                pathRelative          = 'OU=Service Accounts'
                description           = $desc
                enabled               = $true
                passwordPrompt        = $true
                passwordNeverExpires  = $false
                userCannotChangePassword = $true
                resetPasswordIfExists = $false
                groups                = @()
            }
        } while (Read-YesNo '  Add another service account?' $false)
        $svc['accounts'] = $accounts
    }
    Write-Note 'Service account passwords are prompted at run time, never stored in YAML.'
}

# --------------------------------------------------------------------------------------
# Optional features
# --------------------------------------------------------------------------------------
Write-Banner '9/10  Optional features'
Write-Note 'Each must be explicitly on or off. Enable only what you have prepared.'

$pki = $cfg['pki']
$pki['enabled'] = Read-YesNo 'Enable PKI (AD Certificate Services)?' ([bool]$pki['enabled'])
if ($pki['enabled'] -and $pki.Contains('rootCa') -and [bool]$pki['rootCa']['enabled']) {
    $pki['rootCa']['caCommonName'] = Read-Text -Label '  Root CA common name' -Current ([string]$pki['rootCa']['caCommonName'])
}
if ($cfg['roles'].Contains('pki')) { $cfg['roles']['pki']['enabled'] = [bool]$pki['enabled'] }

$wsus = $cfg['wsus']
$wsus['enabled'] = Read-YesNo 'Enable WSUS?' ([bool]$wsus['enabled'])
if ($wsus['enabled']) {
    $wsus['contentDirectory'] = Read-Text -Label '  WSUS content directory' -Current ([string]$wsus['contentDirectory']) -Validate { param($v) Test-AbsoluteWindowsPath $v }
}
if ($cfg['roles'].Contains('wsus')) { $cfg['roles']['wsus']['enabled'] = [bool]$wsus['enabled'] }

$evt = $cfg['eventForwarding']
$evt['enabled'] = Read-YesNo 'Enable Windows Event Forwarding?' ([bool]$evt['enabled'])

$wz = $cfg['wazuh']
$wz['enabled'] = Read-YesNo 'Enable Wazuh agent?' ([bool]$wz['enabled'])
if ($wz['enabled']) {
    $wz['agentMsiPath'] = Read-Text -Label '  Wazuh agent MSI path (local or UNC)' -Current ([string]$wz['agentMsiPath'])
    $wz['managerAddress'] = Read-Text -Label '  Wazuh manager address' -Current ([string]$wz['managerAddress'])
}

$idi = $cfg['identityIntegrations']
$idi['enabled'] = Read-YesNo 'Write identity-integration artifacts (GitLab/Keycloak/YubiKey)?' ([bool]$idi['enabled'])

$bkp = $cfg['backupRecovery']
if ($bkp.Contains('backupPath')) {
    $bkp['backupPath'] = Read-Text -Label 'AD backup path' -Current ([string]$bkp['backupPath']) -Validate { param($v) Test-AbsoluteWindowsPath $v }
}

Write-Note 'GPO baseline, hardening, firewall, Defender, OU/group structure, validation and'
Write-Note 'reporting are inherited from the template. Review them directly in config.yaml.'

# --------------------------------------------------------------------------------------
# Write + validate
# --------------------------------------------------------------------------------------
Write-Banner '10/10  Write and validate'

if (Test-Path -LiteralPath $OutputPath) {
    if (-not (Read-YesNo "Overwrite existing $OutputPath ?" $true)) {
        Write-Bad 'Aborted without writing.'
        return
    }
}

$yaml = ConvertTo-Yaml -Data $cfg
Set-Content -LiteralPath $OutputPath -Value $yaml -Encoding UTF8
Write-Host ''
Write-Host "Wrote $OutputPath" -ForegroundColor Green

# Final authoritative validation using the project's own validator.
$configLib = Join-Path (Split-Path -Parent $PSCommandPath) 'lib\Config.ps1'
. $configLib
try {
    $loaded = Import-ProjectConfig -ConfigPath $OutputPath
    Assert-ProjectConfig -Config $loaded
    Write-Host ''
    Write-Host 'Validation PASSED. config.yaml is ready.' -ForegroundColor Green
    Write-Host 'Next: preview with' -NoNewline; Write-Host '  .\Configure-WindowsServer.ps1 -ConfigPath .\config.yaml -PlanOnly' -ForegroundColor Cyan
}
catch {
    Write-Host ''
    Write-Host "Validation FAILED: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host 'config.yaml was written but needs a manual fix before it will run.' -ForegroundColor Yellow
}
