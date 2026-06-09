Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Install-RequiredWindowsFeatures {
    <#
    .SYNOPSIS
    Installs enabled Windows roles from YAML.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)

    $features = @()
    if ($Config.roles.activeDirectoryDomainServices.enabled) { $features += @{ Name = 'AD-Domain-Services'; Include = $Config.roles.activeDirectoryDomainServices.includeManagementTools } }
    if ($Config.roles.dns.enabled) { $features += @{ Name = 'DNS'; Include = $Config.roles.dns.includeManagementTools } }
    if ($Config.roles.dhcp.enabled) { $features += @{ Name = 'DHCP'; Include = $Config.roles.dhcp.includeManagementTools } }
    if ($Config.roles.wsus.enabled) { $features += @{ Name = 'UpdateServices'; Include = $Config.roles.wsus.includeManagementTools } }
    if ($Config.roles.pki.enabled) { $features += @{ Name = 'ADCS-Cert-Authority'; Include = $Config.roles.pki.includeManagementTools } }

    foreach ($feature in $features) {
        $existing = Get-WindowsFeature -Name $feature.Name
        if ($existing.Installed) { continue }
        if ($Context.PlanOnly) { continue }
        Install-WindowsFeature -Name $feature.Name -IncludeManagementTools:$feature.Include | Out-Null
    }
}

function Assert-WindowsFeaturesInstalled {
    <#
    .SYNOPSIS
    Verifies enabled role features are installed.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    $expected = @()
    if ($Config.roles.activeDirectoryDomainServices.enabled) { $expected += 'AD-Domain-Services' }
    if ($Config.roles.dns.enabled) { $expected += 'DNS' }
    if ($Config.roles.dhcp.enabled) { $expected += 'DHCP' }
    if ($Config.roles.wsus.enabled) { $expected += 'UpdateServices' }
    if ($Config.roles.pki.enabled) { $expected += 'ADCS-Cert-Authority' }
    foreach ($name in $expected) {
        if (-not (Get-WindowsFeature -Name $name).Installed) {
            throw "Required role feature not installed: $name"
        }
    }
}
