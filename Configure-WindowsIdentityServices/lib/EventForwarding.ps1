Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Configure-WindowsEventCollector {
    <#
    .SYNOPSIS
    Configures event collector mode prerequisites.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.eventForwarding.enabled -or $Config.eventForwarding.mode -ne 'collector') { return }
    if ($Context.PlanOnly) { return }
    wecutil qc /q | Out-Null
}

function Configure-WindowsEventSource {
    <#
    .SYNOPSIS
    Configures event source mode prerequisites.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.eventForwarding.enabled -or $Config.eventForwarding.mode -ne 'source') { return }
    if ($Config.eventForwarding.source.configureWinRM -and -not $Context.PlanOnly) {
        Enable-PSRemoting -Force
    }
    if ($Config.eventForwarding.source.configureSubscriptionManager) {
        if ([string]::IsNullOrWhiteSpace([string]$Config.eventForwarding.source.subscriptionManagerServer)) {
            throw 'eventForwarding.source.subscriptionManagerServer is required when configureSubscriptionManager is true.'
        }
        if (-not $Context.PlanOnly) {
            $value = "Server=http://$($Config.eventForwarding.source.subscriptionManagerServer):5985/wsman/SubscriptionManager/WEC,Refresh=60"
            New-Item -Path 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\EventLog\EventForwarding\SubscriptionManager' -Force | Out-Null
            New-ItemProperty -Path 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\EventLog\EventForwarding\SubscriptionManager' -Name '1' -PropertyType String -Value $value -Force | Out-Null
        }
    }
}

function Import-EventSubscriptionFromXml {
    <#
    .SYNOPSIS
    Imports event subscription from configured XML file.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.eventForwarding.enabled -or $Config.eventForwarding.mode -ne 'collector') { return }
    $xmlPath = $Config.eventForwarding.collector.subscriptionXmlPath
    if ([string]::IsNullOrWhiteSpace([string]$xmlPath) -or -not (Test-Path -LiteralPath $xmlPath)) {
        throw 'Event subscription XML is required and must exist.'
    }
    if ($Context.PlanOnly) { return }
    wecutil cs $xmlPath | Out-Null
}

function Assert-EventForwardingState {
    <#
    .SYNOPSIS
    Validates event forwarding state.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    if (-not $Config.eventForwarding.enabled) { return }
    if ($Config.eventForwarding.mode -eq 'collector') {
        if ($Config.eventForwarding.validation.requireForwardedEventsLog) {
            if (-not (Get-WinEvent -ListLog $Config.eventForwarding.collector.destinationLog -ErrorAction SilentlyContinue)) {
                throw "Forwarded events log missing: $($Config.eventForwarding.collector.destinationLog)"
            }
        }
        if ($Config.eventForwarding.validation.requireSubscriptionPresent) {
            $subscriptions = wecutil es | Out-String
            if ($subscriptions -notmatch [regex]::Escape([string]$Config.eventForwarding.collector.subscriptionName)) {
                throw "WEF subscription missing: $($Config.eventForwarding.collector.subscriptionName)"
            }
        }
    }
}
