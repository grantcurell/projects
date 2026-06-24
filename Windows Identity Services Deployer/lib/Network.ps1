Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Assert-InterfaceExists {
    <#
    .SYNOPSIS
    Ensures configured interface alias exists.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    $adapter = Get-NetAdapter -Name $Config.network.interfaceAlias -ErrorAction SilentlyContinue
    if (-not $adapter) {
        $available = (Get-NetAdapter | Select-Object -ExpandProperty Name) -join ', '
        throw "Network interface '$($Config.network.interfaceAlias)' not found. Available: $available"
    }
}

function Assert-NoMultipleDefaultGateways {
    <#
    .SYNOPSIS
    Ensures multiple default gateways are not present if disallowed.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    if ($Config.network.allowMultipleDefaultGateways) { return }
    $routes = Get-NetRoute -AddressFamily IPv4 -DestinationPrefix '0.0.0.0/0' -ErrorAction SilentlyContinue
    if (@($routes).Count -gt 1) {
        throw 'Multiple default gateways detected while network.allowMultipleDefaultGateways is false.'
    }
}

function Set-ComputerNameIfNeeded {
    <#
    .SYNOPSIS
    Renames computer and schedules reboot resume.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][pscustomobject]$Config,
        [Parameter(Mandatory = $true)][hashtable]$Context
    )
    if ($env:COMPUTERNAME -eq $Config.network.computerName) { return }
    if ($Context.PlanOnly) { return }
    Register-ResumeScheduledTask -Config $Config -ScriptPath (Join-Path (Split-Path -Parent $Config.__configPath) 'Configure-WindowsServer.ps1') -ConfigPath $Config.__configPath
    Rename-Computer -NewName $Config.network.computerName -Force -Restart
}

function Set-TimeZoneFromConfig {
    <#
    .SYNOPSIS
    Applies configured time zone.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if ($Context.PlanOnly) { return }
    Set-TimeZone -Id $Config.network.timeZone
}

function Set-StaticIPv4FromConfig {
    <#
    .SYNOPSIS
    Configures static IPv4 from YAML values.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if ($Context.PlanOnly) { return }
    $alias = $Config.network.interfaceAlias
    $current = Get-NetIPAddress -InterfaceAlias $alias -AddressFamily IPv4 -ErrorAction SilentlyContinue
    foreach ($entry in @($current | Where-Object { $_.IPAddress -ne $Config.network.ipv4.address })) {
        Remove-NetIPAddress -InterfaceAlias $alias -IPAddress $entry.IPAddress -Confirm:$false -ErrorAction SilentlyContinue
    }
    if (-not ($current | Where-Object { $_.IPAddress -eq $Config.network.ipv4.address })) {
        New-NetIPAddress -InterfaceAlias $alias -IPAddress $Config.network.ipv4.address -PrefixLength $Config.network.ipv4.prefixLength -DefaultGateway $Config.network.ipv4.defaultGateway
    }
}

function Set-DnsClientServersBeforePromotion {
    <#
    .SYNOPSIS
    Configures DNS client servers before AD promotion.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if ($Context.PlanOnly) { return }
    Set-DnsClientServerAddress -InterfaceAlias $Config.network.interfaceAlias -ServerAddresses @($Config.network.ipv4.dnsClientServersBeforePromotion)
}

function Set-DnsClientServersAfterPromotion {
    <#
    .SYNOPSIS
    Configures DNS client servers after AD promotion.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if ($Context.PlanOnly) { return }
    Set-DnsClientServerAddress -InterfaceAlias $Config.network.interfaceAlias -ServerAddresses @($Config.network.ipv4.dnsClientServersAfterPromotion)
}

function Assert-StaticIpApplied {
    <#
    .SYNOPSIS
    Verifies configured static IPv4 exists.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][pscustomobject]$Config,
        [Parameter(Mandatory = $true)][hashtable]$Context
    )
    if ($Context.PlanOnly) { return }
    $assigned = Get-NetIPAddress -InterfaceAlias $Config.network.interfaceAlias -AddressFamily IPv4 -ErrorAction SilentlyContinue
    if (-not ($assigned | Where-Object { $_.IPAddress -eq $Config.network.ipv4.address })) {
        throw 'Configured static IPv4 address is not applied.'
    }
}

function Assert-NetworkReady {
    <#
    .SYNOPSIS
    Runs network configuration sequence.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.network.enabled) { return }
    Assert-InterfaceExists -Config $Config
    Assert-NoMultipleDefaultGateways -Config $Config
    Set-TimeZoneFromConfig -Config $Config -Context $Context
    Set-StaticIPv4FromConfig -Config $Config -Context $Context
    Set-DnsClientServersBeforePromotion -Config $Config -Context $Context
    Assert-StaticIpApplied -Config $Config -Context $Context
}
