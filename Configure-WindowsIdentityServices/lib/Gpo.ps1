Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Test-HasConfigProperty {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]$Object,
        [Parameter(Mandatory = $true)][string]$Name
    )
    if ($Object -is [System.Collections.IDictionary]) {
        return $Object.Contains($Name)
    }
    return ($null -ne $Object.PSObject.Properties[$Name])
}

function New-GposFromConfig {
    <#
    .SYNOPSIS
    Creates configured GPOs if missing.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.gpo.enabled) { return }
    foreach ($gpo in @($Config.gpo.gpos)) {
        if (Get-GPO -Name $gpo.name -ErrorAction SilentlyContinue) { continue }
        if ($Context.PlanOnly) { continue }
        New-GPO -Name $gpo.name | Out-Null
    }
}

function Link-GposFromConfig {
    <#
    .SYNOPSIS
    Links GPOs to domain or OU targets in explicit order.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.gpo.enabled) { return }
    $domainDn = (Get-ADDomain).DistinguishedName
    $ordered = @($Config.gpo.gpos | Sort-Object linkOrder)
    foreach ($gpo in $ordered) {
        $target = if ($gpo.target -eq 'domain') { $domainDn } else { "$($gpo.linkDistinguishedNameRelative),$domainDn" }
        if ($Context.PlanOnly) { continue }
        $linkEnabled = if ($gpo.enabled) { 'Yes' } else { 'No' }
        $enforced = if ($gpo.enforced) { 'Yes' } else { 'No' }
        try {
            New-GPLink -Name $gpo.name -Target $target -Enforced $enforced -LinkEnabled $linkEnabled -Order $gpo.linkOrder | Out-Null
        }
        catch {
            if ($_.Exception.Message -like '*already linked*') {
                Set-GPLink -Name $gpo.name -Target $target -Enforced $enforced -LinkEnabled $linkEnabled -Order $gpo.linkOrder | Out-Null
            }
            else {
                throw
            }
        }
        Configure-PasswordAndLockoutPolicy -Config $Config -Gpo $gpo -Context $Context
        Configure-AuditPolicy -Gpo $gpo -Context $Context
        Configure-FirewallPolicy -Gpo $gpo -Context $Context
        Configure-RemovableMediaPolicy -Gpo $gpo -Context $Context
        Configure-ScreenLockPolicy -Gpo $gpo -Context $Context
        Configure-WsusPolicy -Gpo $gpo -Context $Context
    }
}

function Configure-PasswordAndLockoutPolicy {
    <#
    .SYNOPSIS
    Configures password and lockout policy.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][pscustomobject]$Gpo, [Parameter(Mandatory = $true)][hashtable]$Context)
    $hasPasswordPolicy = Test-HasConfigProperty -Object $Gpo.settings -Name 'passwordPolicy'
    $hasLockoutPolicy = Test-HasConfigProperty -Object $Gpo.settings -Name 'lockoutPolicy'
    if (-not $hasPasswordPolicy -and -not $hasLockoutPolicy) { return }
    if (-not $Config.gpo.allowModifyDefaultDomainPolicy) {
        throw 'Password policy requested but gpo.allowModifyDefaultDomainPolicy is false. Fine-grained policy automation is required before proceeding.'
    }
    if ($Context.PlanOnly) { return }
    if ($Gpo.target -ne 'domain') {
        throw "Password/lockout policy GPO '$($Gpo.name)' must target domain."
    }
    if ($hasPasswordPolicy) {
        $pp = $Gpo.settings.passwordPolicy
        Set-ADDefaultDomainPasswordPolicy `
            -Identity (Get-ADDomain).DNSRoot `
            -MinPasswordLength ([int]$pp.minimumPasswordLength) `
            -PasswordHistoryCount ([int]$pp.passwordHistoryCount) `
            -MaxPasswordAge ([timespan]::FromDays([int]$pp.maximumPasswordAgeDays)) `
            -MinPasswordAge ([timespan]::FromDays([int]$pp.minimumPasswordAgeDays)) `
            -ComplexityEnabled ([bool]$pp.complexityEnabled) `
            -ReversibleEncryptionEnabled ([bool]$pp.reversibleEncryptionEnabled)
    }
    if ($hasLockoutPolicy) {
        $lp = $Gpo.settings.lockoutPolicy
        Set-ADDefaultDomainPasswordPolicy `
            -Identity (Get-ADDomain).DNSRoot `
            -LockoutThreshold ([int]$lp.lockoutThreshold) `
            -LockoutDuration ([timespan]::FromMinutes([int]$lp.lockoutDurationMinutes)) `
            -LockoutObservationWindow ([timespan]::FromMinutes([int]$lp.lockoutObservationWindowMinutes))
    }
}

function Configure-AuditPolicy {
    <#
    .SYNOPSIS
    Applies audit policy settings.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Gpo, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not (Test-HasConfigProperty -Object $Gpo.settings -Name 'auditPolicy')) { return }
    if (-not $Gpo.settings.auditPolicy.enabled) { return }
    if ($Context.PlanOnly) { return }
    foreach ($category in $Gpo.settings.auditPolicy.categories.PSObject.Properties.Name) {
        & auditpol /set /category:$category /success:enable /failure:enable | Out-Null
    }
}

function Configure-FirewallPolicy {
    <#
    .SYNOPSIS
    Applies firewall policy settings through registry-backed GPO values.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Gpo, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not (Test-HasConfigProperty -Object $Gpo.settings -Name 'firewall')) { return }
    if (-not $Gpo.settings.firewall.enabled -or $Context.PlanOnly) { return }
    Set-GPRegistryValue -Name $Gpo.name -Key 'HKLM\Software\Policies\Microsoft\WindowsFirewall\DomainProfile' -ValueName 'EnableFirewall' -Type DWord -Value 1
    Set-GPRegistryValue -Name $Gpo.name -Key 'HKLM\Software\Policies\Microsoft\WindowsFirewall\PrivateProfile' -ValueName 'EnableFirewall' -Type DWord -Value 1
    Set-GPRegistryValue -Name $Gpo.name -Key 'HKLM\Software\Policies\Microsoft\WindowsFirewall\PublicProfile' -ValueName 'EnableFirewall' -Type DWord -Value 1
}

function Configure-RemovableMediaPolicy {
    <#
    .SYNOPSIS
    Applies removable media policy settings.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Gpo, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not (Test-HasConfigProperty -Object $Gpo.settings -Name 'removableMedia')) { return }
    if ($Context.PlanOnly) { return }
    if ($Gpo.settings.removableMedia.denyWriteAccess) {
        Set-GPRegistryValue -Name $Gpo.name -Key 'HKLM\Software\Policies\Microsoft\Windows\RemovableStorageDevices' -ValueName 'Deny_Write' -Type DWord -Value 1
    }
    if ($Gpo.settings.removableMedia.denyExecuteAccess) {
        Set-GPRegistryValue -Name $Gpo.name -Key 'HKLM\Software\Policies\Microsoft\Windows\RemovableStorageDevices' -ValueName 'Deny_Execute' -Type DWord -Value 1
    }
}

function Configure-ScreenLockPolicy {
    <#
    .SYNOPSIS
    Applies screen lock policy settings.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Gpo, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not (Test-HasConfigProperty -Object $Gpo.settings -Name 'screenLock')) { return }
    if (-not $Gpo.settings.screenLock.enabled -or $Context.PlanOnly) { return }
    Set-GPRegistryValue -Name $Gpo.name -Key 'HKCU\Software\Policies\Microsoft\Windows\Control Panel\Desktop' -ValueName 'ScreenSaveActive' -Type String -Value '1'
    Set-GPRegistryValue -Name $Gpo.name -Key 'HKCU\Software\Policies\Microsoft\Windows\Control Panel\Desktop' -ValueName 'ScreenSaverIsSecure' -Type String -Value '1'
    Set-GPRegistryValue -Name $Gpo.name -Key 'HKCU\Software\Policies\Microsoft\Windows\Control Panel\Desktop' -ValueName 'ScreenSaveTimeOut' -Type String -Value ([string]$Gpo.settings.screenLock.timeoutSeconds)
}

function Configure-WsusPolicy {
    <#
    .SYNOPSIS
    Applies WSUS client policy settings when enabled.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Gpo, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not (Test-HasConfigProperty -Object $Gpo.settings -Name 'wsus')) { return }
    if (-not $Gpo.settings.wsus.enabled) { return }
    if ([string]::IsNullOrWhiteSpace([string]$Gpo.settings.wsus.serverUrl)) {
        throw "WSUS policy enabled for GPO $($Gpo.name) but settings.wsus.serverUrl is empty."
    }
    if ($Context.PlanOnly) { return }
    Set-GPRegistryValue -Name $Gpo.name -Key 'HKLM\Software\Policies\Microsoft\Windows\WindowsUpdate' -ValueName 'WUServer' -Type String -Value $Gpo.settings.wsus.serverUrl
    Set-GPRegistryValue -Name $Gpo.name -Key 'HKLM\Software\Policies\Microsoft\Windows\WindowsUpdate' -ValueName 'WUStatusServer' -Type String -Value $Gpo.settings.wsus.serverUrl
    Set-GPRegistryValue -Name $Gpo.name -Key 'HKLM\Software\Policies\Microsoft\Windows\WindowsUpdate\AU' -ValueName 'UseWUServer' -Type DWord -Value 1
}

function Generate-GpoReports {
    <#
    .SYNOPSIS
    Exports HTML reports for configured GPOs.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    if (-not $Config.gpo.enabled) { return }
    $outDir = $Config.validation.evidenceFiles.gpoReportDirectory
    if (-not (Test-Path -LiteralPath $outDir)) { New-Item -Path $outDir -ItemType Directory -Force | Out-Null }
    foreach ($gpo in @($Config.gpo.gpos)) {
        Get-GPOReport -Name $gpo.name -ReportType Html -Path (Join-Path $outDir "$($gpo.name).html")
    }
}

function Assert-GpoLinks {
    <#
    .SYNOPSIS
    Verifies configured GPO links are present.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    if (-not $Config.gpo.enabled) { return }
    foreach ($gpo in @($Config.gpo.gpos)) {
        if (-not (Get-GPO -Name $gpo.name -ErrorAction SilentlyContinue)) {
            throw "Missing GPO: $($gpo.name)"
        }
    }
}
