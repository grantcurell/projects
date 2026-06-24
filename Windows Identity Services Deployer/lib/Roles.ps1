Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Install-RequiredWindowsFeatures {
    <#
    .SYNOPSIS
    Installs enabled Windows roles from YAML.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)

    # NOTE: AD CS (ADCS-Cert-Authority) is deliberately NOT installed here. Windows
    # blocks domain controller promotion when the Certificate Authority role is
    # already present ("Verification of prerequisites for Domain Controller
    # promotion failed. Certificate Server is installed."). The PKI role is
    # installed after promotion by Install-AdcsRolesIfEnabled in the PostPromotion
    # phase. Installing it pre-promotion poisons DCPromo.
    $features = @()
    if ($Config.roles.activeDirectoryDomainServices.enabled) { $features += @{ Name = 'AD-Domain-Services'; Include = $Config.roles.activeDirectoryDomainServices.includeManagementTools } }
    if ($Config.roles.dns.enabled) { $features += @{ Name = 'DNS'; Include = $Config.roles.dns.includeManagementTools } }
    if ($Config.roles.dhcp.enabled) { $features += @{ Name = 'DHCP'; Include = $Config.roles.dhcp.includeManagementTools } }
    if ($Config.roles.wsus.enabled) { $features += @{ Name = 'UpdateServices'; Include = $Config.roles.wsus.includeManagementTools } }

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
    # ADCS-Cert-Authority is intentionally absent: it is installed post-promotion
    # (see Install-RequiredWindowsFeatures note) so it must not be asserted here.
    $expected = @()
    if ($Config.roles.activeDirectoryDomainServices.enabled) { $expected += 'AD-Domain-Services' }
    if ($Config.roles.dns.enabled) { $expected += 'DNS' }
    if ($Config.roles.dhcp.enabled) { $expected += 'DHCP' }
    if ($Config.roles.wsus.enabled) { $expected += 'UpdateServices' }
    foreach ($name in $expected) {
        if (-not (Get-WindowsFeature -Name $name).Installed) {
            throw "Required role feature not installed: $name"
        }
    }
}
