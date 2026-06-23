Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Configure-DnsForwardersFromConfig {
    <#
    .SYNOPSIS
    Sets DNS forwarders from YAML.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.dns.enabled) { return }
    if ($Context.PlanOnly) { return }
    Set-DnsServerForwarder -IPAddress @($Config.dns.forwarders) -UseRootHint:$Config.dns.useRootHints
}

function Configure-ReverseLookupZonesFromConfig {
    <#
    .SYNOPSIS
    Creates reverse lookup zones declared in YAML.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.dns.enabled -or -not $Config.dns.createReverseLookupZones) { return }
    foreach ($zone in @($Config.dns.reverseLookupZones)) {
        if ($Context.PlanOnly) { continue }
        $zoneName = $null
        $parts = ([string]$zone.networkId) -split '/'
        if ($parts.Count -eq 2 -and [int]$parts[1] -eq 24) {
            $octets = $parts[0] -split '\.'
            if ($octets.Count -eq 4) {
                $zoneName = "$($octets[2]).$($octets[1]).$($octets[0]).in-addr.arpa"
            }
        }
        if ($zoneName -and (Get-DnsServerZone -Name $zoneName -ErrorAction SilentlyContinue)) {
            continue
        }
        try {
            Add-DnsServerPrimaryZone -NetworkId $zone.networkId -ReplicationScope $zone.replicationScope -ErrorAction Stop
        }
        catch {
            if ($_.Exception.Message -like '*already exists*' -or $_.FullyQualifiedErrorId -like '*9609*') { continue }
            throw
        }
    }
}

function Configure-DnsScavengingFromConfig {
    <#
    .SYNOPSIS
    Configures DNS scavenging if enabled.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.dns.enabled -or -not $Config.dns.scavenging.enabled) { return }
    if ($null -eq $Config.dns.scavenging.noRefreshIntervalDays -or $null -eq $Config.dns.scavenging.refreshIntervalDays) {
        throw 'dns.scavenging intervals are required when scavenging is enabled.'
    }
    if ($Context.PlanOnly) { return }
    Set-DnsServerScavenging -ScavengingState $true -NoRefreshInterval ([TimeSpan]::FromDays($Config.dns.scavenging.noRefreshIntervalDays)) -RefreshInterval ([TimeSpan]::FromDays($Config.dns.scavenging.refreshIntervalDays)) -ApplyOnAllZones
}

function Assert-DnsRecordsResolve {
    <#
    .SYNOPSIS
    Verifies required DNS records resolve.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    if (-not $Config.dns.enabled) { return }
    foreach ($record in @($Config.dns.requiredRecordsToValidate)) {
        Resolve-DnsName -Name $record.name -Type $record.type -ErrorAction Stop | Out-Null
    }
}

function Assert-DnsForwarders {
    <#
    .SYNOPSIS
    Verifies DNS forwarders match config.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    if (-not $Config.dns.enabled) { return }
    $current = (Get-DnsServerForwarder).IPAddress.IPAddressToString
    foreach ($ip in @($Config.dns.forwarders)) {
        if ($ip -notin $current) { throw "DNS forwarder missing: $ip" }
    }
}
