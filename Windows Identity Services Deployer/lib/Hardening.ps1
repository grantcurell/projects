Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Write-SecurityDecisionsDocument {
    <#
    .SYNOPSIS
    Updates docs/security-decisions.md with applied and skipped controls.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    $projectRoot = Split-Path $PSScriptRoot -Parent
    $docPath = Join-Path $projectRoot 'docs\security-decisions.md'
    $content = @"
# Security Decisions

- hardening enabled: $($Config.hardening.enabled)
- STIG-aligned settings applied: event log sizing, SMB controls, LDAP controls, optional service disable list
- settings skipped because disabled:
  - FIPS controls enabled: $($Config.hardening.fipsAlignedCrypto.enabled)
  - Defender enabled: $($Config.defender.enabled)
  - Event forwarding enabled: $($Config.eventForwarding.enabled)
  - WSUS enabled: $($Config.wsus.enabled)
  - PKI enabled: $($Config.pki.enabled)
- FIPS decision approved: $($Config.hardening.fipsAlignedCrypto.approved)
"@
    Set-Content -LiteralPath $docPath -Value $content -Encoding UTF8
}

function Configure-EventLogSizes {
    <#
    .SYNOPSIS
    Configures Windows event log size limits.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if ($Context.PlanOnly) { return }
    $sizes = $Config.hardening.eventLogSizes
    & wevtutil sl Security /ms:($sizes.securityMaxSizeMb * 1MB) | Out-Null
    & wevtutil sl System /ms:($sizes.systemMaxSizeMb * 1MB) | Out-Null
    & wevtutil sl Application /ms:($sizes.applicationMaxSizeMb * 1MB) | Out-Null
}

function Configure-SmbSettings {
    <#
    .SYNOPSIS
    Configures SMB hardening values.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if ($Context.PlanOnly) { return }
    if ($Config.hardening.requireSmbSigning) {
        Set-SmbServerConfiguration -EnableSecuritySignature $true -RequireSecuritySignature $true -Force
    }
    if ($Config.hardening.disableSmbv1) {
        Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol -NoRestart -ErrorAction SilentlyContinue | Out-Null
    }
}

function ConfigureLdapSigningAndChannelBinding {
    <#
    .SYNOPSIS
    Applies LDAP signing and channel binding settings.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if ($Context.PlanOnly) { return }
    if ($Config.hardening.ldapSigning.requireSigning) {
        New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Services\NTDS\Parameters' -Name 'LDAPServerIntegrity' -Value 2 -PropertyType DWord -Force | Out-Null
    }
    if ($Config.hardening.channelBinding.enabled) {
        New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Services\NTDS\Parameters' -Name 'LdapEnforceChannelBinding' -Value 2 -PropertyType DWord -Force | Out-Null
    }
}

function Disable-UnnecessaryServicesFromConfig {
    <#
    .SYNOPSIS
    Disables only services explicitly listed in config.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    foreach ($svc in @($Config.hardening.unnecessaryServices)) {
        $existing = Get-Service -Name $svc.name -ErrorAction SilentlyContinue
        if (-not $existing) {
            if ($Config.hardening.missingServiceBehavior -eq 'stop') { throw "Service not found: $($svc.name)" }
            Write-Warning "Service not found: $($svc.name)"
            continue
        }
        if ($Context.PlanOnly) { continue }
        Set-Service -Name $svc.name -StartupType $svc.startupType
        if ($svc.stopService) { Stop-Service -Name $svc.name -Force -ErrorAction SilentlyContinue }
    }
}

function Get-OptionalConfigMember {
    <#
    .SYNOPSIS
    Returns a named member of a config object, or $null when absent.
    .DESCRIPTION
    StrictMode (Version Latest) throws when a non-existent property is referenced
    on a PSCustomObject. Optional config sections such as 'localSecurityOptions: {}'
    deserialize to objects with no members, so direct dotted access blows up. This
    helper safely probes both PSCustomObjects and hashtables.
    #>
    [CmdletBinding()]
    param([Parameter()]$Object, [Parameter(Mandatory = $true)][string]$Name)
    if ($null -eq $Object) { return $null }
    if ($Object -is [System.Collections.IDictionary]) {
        if ($Object.Contains($Name)) { return $Object[$Name] }
        return $null
    }
    if ($Object.PSObject.Properties.Name -contains $Name) {
        return $Object.PSObject.Properties[$Name].Value
    }
    return $null
}

function Configure-LocalSecurityOptions {
    <#
    .SYNOPSIS
    Applies selected local security options from config.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if ($Context.PlanOnly) { return }
    $lso = Get-OptionalConfigMember -Object $Config.hardening -Name 'localSecurityOptions'
    if ($null -eq $lso) { return }

    $rename = Get-OptionalConfigMember -Object $lso -Name 'renameGuestAccount'
    if ($rename -and (Get-OptionalConfigMember -Object $rename -Name 'enabled')) {
        $guest = Get-LocalUser -Name 'Guest' -ErrorAction SilentlyContinue
        if ($guest) {
            Rename-LocalUser -Name 'Guest' -NewName (Get-OptionalConfigMember -Object $rename -Name 'newName')
        }
    }

    $disable = Get-OptionalConfigMember -Object $lso -Name 'disableGuestAccount'
    if ($disable -and (Get-OptionalConfigMember -Object $disable -Name 'enabled')) {
        $newName = Get-OptionalConfigMember -Object $rename -Name 'newName'
        if ($newName) { Disable-LocalUser -Name $newName -ErrorAction SilentlyContinue }
        Disable-LocalUser -Name 'Guest' -ErrorAction SilentlyContinue
    }

    $restrict = Get-OptionalConfigMember -Object $lso -Name 'restrictAnonymous'
    if ($restrict -and (Get-OptionalConfigMember -Object $restrict -Name 'enabled')) {
        New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Lsa' -Name 'RestrictAnonymous' -PropertyType DWord -Value 1 -Force | Out-Null
    }
}

function Configure-FipsAlignedCryptoIfApproved {
    <#
    .SYNOPSIS
    Applies configured FIPS-aligned registry values only when approved.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.hardening.fipsAlignedCrypto.enabled -or -not $Config.hardening.fipsAlignedCrypto.approved) { return }
    foreach ($reg in @($Config.hardening.fipsAlignedCrypto.registrySettings)) {
        if ($Context.PlanOnly) { continue }
        New-Item -Path $reg.path -Force | Out-Null
        New-ItemProperty -Path $reg.path -Name $reg.name -Value $reg.value -PropertyType $reg.propertyType -Force | Out-Null
    }
}

function Apply-StigAlignedSettingsFromConfig {
    <#
    .SYNOPSIS
    Applies STIG-aligned baseline settings explicitly configured.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.hardening.enabled) { return }
    Configure-EventLogSizes -Config $Config -Context $Context
    Configure-SmbSettings -Config $Config -Context $Context
    ConfigureLdapSigningAndChannelBinding -Config $Config -Context $Context
    if ($Config.hardening.disableUnnecessaryServices) {
        Disable-UnnecessaryServicesFromConfig -Config $Config -Context $Context
    }
    Configure-LocalSecurityOptions -Config $Config -Context $Context
    Configure-FipsAlignedCryptoIfApproved -Config $Config -Context $Context
    Write-SecurityDecisionsDocument -Config $Config
}

function Assert-HardeningState {
    <#
    .SYNOPSIS
    Validates hardening baseline state.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    if (-not $Config.hardening.enabled) { return }
    if ($Config.hardening.requireSmbSigning) {
        $smb = Get-SmbServerConfiguration
        if (-not $smb.RequireSecuritySignature) {
            throw 'SMB signing is not required after hardening.'
        }
    }
}
