Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Normalize-AdModeName {
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][string]$ModeName)
    switch ($ModeName) {
        'WinThreshold' { return 'Windows2016' }
        default { return $ModeName }
    }
}

function Get-DomainDistinguishedNameFromDomainName {
    <#
    .SYNOPSIS
    Converts DNS domain name to DN.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][string]$DomainName)
    return (($DomainName -split '\.') | ForEach-Object { "DC=$_"} ) -join ','
}

function Install-NewForestFromConfig {
    <#
    .SYNOPSIS
    Promotes server to first domain controller.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.activeDirectory.enabled) { return }
    if ($Config.activeDirectory.mode -ne 'newForest') { throw "unsupported mode: $($Config.activeDirectory.mode)" }

    try {
        $existing = Get-ADDomain -ErrorAction Stop
        if ($existing.DNSRoot -eq $Config.activeDirectory.domainName) { return }
    }
    catch {
    }

    if (-not $Config.activeDirectory.safeModeAdministratorPasswordPrompt) {
        throw 'secret backend not implemented. safeModeAdministratorPasswordPrompt must be true.'
    }
    if ($Context.PlanOnly) { return }
    if (-not (Get-WindowsFeature -Name 'AD-Domain-Services').Installed) {
        throw 'AD-Domain-Services is not installed. Run Preflight before domain promotion.'
    }
    Import-Module ADDSDeployment -ErrorAction Stop
    $dsrm = $null
    if ($env:CONFIGURE_WIS_DSRM_PASSWORD) {
        $dsrm = ConvertTo-SecureString -String $env:CONFIGURE_WIS_DSRM_PASSWORD -AsPlainText -Force
    }
    else {
        $dsrm = Read-Host -Prompt 'Enter DSRM password' -AsSecureString
    }

    Register-ResumeScheduledTask -Config $Config -ScriptPath (Join-Path (Split-Path -Parent $Config.__configPath) 'Configure-WindowsServer.ps1') -ConfigPath $Config.__configPath
    Install-ADDSForest `
        -DomainName $Config.activeDirectory.domainName `
        -DomainNetbiosName $Config.activeDirectory.netbiosName `
        -ForestMode $Config.activeDirectory.forestMode `
        -DomainMode $Config.activeDirectory.domainMode `
        -InstallDns:$Config.activeDirectory.installDns `
        -CreateDnsDelegation:$Config.activeDirectory.createDnsDelegation `
        -DatabasePath $Config.activeDirectory.databasePath `
        -LogPath $Config.activeDirectory.logPath `
        -SysvolPath $Config.activeDirectory.sysvolPath `
        -SafeModeAdministratorPassword $dsrm `
        -Force:$true
}

function Assert-ForestAndDomainMode {
    <#
    .SYNOPSIS
    Verifies configured forest and domain mode.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    $forest = Get-ADForest
    $domain = Get-ADDomain
    $expectedForest = Normalize-AdModeName -ModeName ([string]$Config.activeDirectory.forestMode)
    $expectedDomain = Normalize-AdModeName -ModeName ([string]$Config.activeDirectory.domainMode)
    if ($forest.ForestMode.ToString() -notlike "*$expectedForest*") { throw 'Forest mode mismatch.' }
    if ($domain.DomainMode.ToString() -notlike "*$expectedDomain*") { throw 'Domain mode mismatch.' }
}

function Assert-DomainControllerState {
    <#
    .SYNOPSIS
    Verifies domain controller state after promotion.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    $domain = Get-ADDomain
    if ($domain.DNSRoot -ne $Config.activeDirectory.domainName) { throw 'Domain name mismatch.' }
    if ($domain.NetBIOSName -ne $Config.activeDirectory.netbiosName) { throw 'NetBIOS name mismatch.' }
    if (-not (Test-Path 'C:\Windows\SYSVOL')) { throw 'SYSVOL not found.' }
    $netlogon = Get-SmbShare -Name 'NETLOGON' -ErrorAction SilentlyContinue
    if (-not $netlogon) { throw 'NETLOGON share not found.' }
    Assert-ForestAndDomainMode -Config $Config
}

function Rename-DefaultSiteIfConfigured {
    <#
    .SYNOPSIS
    Renames default AD site if requested.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.activeDirectory.site.renameDefaultSite) { return }
    if ($Context.PlanOnly) { return }
    $site = $null
    try {
        $site = Get-ADReplicationSite -Identity $Config.activeDirectory.site.defaultSiteCurrentName -ErrorAction Stop
    }
    catch {
        $existingNew = Get-ADReplicationSite -Identity $Config.activeDirectory.site.newSiteName -ErrorAction SilentlyContinue
        if ($existingNew) { return }
        return
    }
    if ($site -and $site.Name -ne $Config.activeDirectory.site.newSiteName) {
        Rename-ADObject -Identity $site.DistinguishedName -NewName $Config.activeDirectory.site.newSiteName
    }
}
