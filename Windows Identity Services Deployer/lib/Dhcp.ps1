Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Authorize-DhcpServerInAd {
    <#
    .SYNOPSIS
    Authorizes DHCP server in AD when configured.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.dhcp.enabled -or -not $Config.dhcp.authorizeInActiveDirectory) { return }
    if ($Context.PlanOnly) { return }
    if (-not (Get-DhcpServerInDC | Where-Object { $_.DnsName -eq $Config.dhcp.serverDnsName })) {
        Add-DhcpServerInDC -DnsName $Config.dhcp.serverDnsName -IPAddress $Config.dhcp.serverIpAddress
    }
}

function Configure-DhcpServerSettings {
    <#
    .SYNOPSIS
    Applies DHCP server-level settings.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.dhcp.enabled) { return }
    if ($Context.PlanOnly) { return }
    Set-DhcpServerSetting -ComputerName $Config.dhcp.serverDnsName -ConflictDetectionAttempts $Config.dhcp.conflictDetectionAttempts
}

function Configure-DhcpScopesFromConfig {
    <#
    .SYNOPSIS
    Creates or validates DHCP scopes from config.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.dhcp.enabled) { return }
    foreach ($scope in @($Config.dhcp.scopes)) {
        $existing = Get-DhcpServerv4Scope -ComputerName $Config.dhcp.serverDnsName -ScopeId $scope.scopeId -ErrorAction SilentlyContinue
        if (-not $existing) {
            if ($Context.PlanOnly) { continue }
            Add-DhcpServerv4Scope -ComputerName $Config.dhcp.serverDnsName -Name $scope.name -StartRange $scope.startRange -EndRange $scope.endRange -SubnetMask $scope.subnetMask -State $scope.state
            Set-DhcpServerv4Scope -ComputerName $Config.dhcp.serverDnsName -ScopeId $scope.scopeId -LeaseDuration ([timespan]::Parse($scope.leaseDuration))
            continue
        }
        $conflict = ($existing.StartRange -ne $scope.startRange) -or ($existing.EndRange -ne $scope.endRange) -or ($existing.SubnetMask -ne $scope.subnetMask)
        if ($conflict -and -not $Config.dhcp.reconcileExisting) {
            throw "Existing DHCP scope conflicts with YAML and dhcp.reconcileExisting is false: $($scope.scopeId)"
        }
    }
}

function Configure-DhcpScopeOptionsFromConfig {
    <#
    .SYNOPSIS
    Configures scope options from config.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.dhcp.enabled) { return }
    foreach ($scope in @($Config.dhcp.scopes)) {
        if ($Context.PlanOnly) { continue }
        Set-DhcpServerv4OptionValue -ComputerName $Config.dhcp.serverDnsName -ScopeId $scope.scopeId -Router @($scope.options.router) -DnsServer @($scope.options.dnsServers) -DnsDomain $scope.options.dnsDomain
        if ($scope.options.ntpServers) {
            Set-DhcpServerv4OptionValue -ComputerName $Config.dhcp.serverDnsName -ScopeId $scope.scopeId -OptionId 42 -Value @($scope.options.ntpServers)
        }
    }
}

function Configure-DhcpReservationsFromConfig {
    <#
    .SYNOPSIS
    Configures scope reservations from config.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.dhcp.enabled) { return }
    foreach ($scope in @($Config.dhcp.scopes)) {
        foreach ($reservation in @($scope.reservations)) {
            $existing = Get-DhcpServerv4Reservation -ComputerName $Config.dhcp.serverDnsName -ScopeId $scope.scopeId -IPAddress $reservation.ipAddress -ErrorAction SilentlyContinue
            if ($existing) { continue }
            if ($Context.PlanOnly) { continue }
            Add-DhcpServerv4Reservation -ComputerName $Config.dhcp.serverDnsName -ScopeId $scope.scopeId -IPAddress $reservation.ipAddress -ClientId $reservation.clientId -Name $reservation.name -Description $reservation.description
        }
    }
}

function Assert-DhcpConfiguration {
    <#
    .SYNOPSIS
    Validates expected DHCP scopes exist.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    if (-not $Config.dhcp.enabled) { return }
    foreach ($scope in @($Config.dhcp.scopes)) {
        if (-not (Get-DhcpServerv4Scope -ComputerName $Config.dhcp.serverDnsName -ScopeId $scope.scopeId -ErrorAction SilentlyContinue)) {
            throw "Missing DHCP scope: $($scope.scopeId)"
        }
    }
}
