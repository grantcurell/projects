Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Configure-PdcAuthoritativeTime {
    <#
    .SYNOPSIS
    Configures authoritative domain time on PDC emulator.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.time.enabled) { return }

    $isPdc = $true
    if ($Config.time.configureOnlyIfPdcEmulator) {
        $domain = Get-ADDomain
        $isPdc = ($domain.PDCEmulator -like "*$env:COMPUTERNAME*")
        if (-not $isPdc -and $Config.time.authoritativeForDomain) {
            switch ($Config.time.behaviorIfNotPdc) {
                'stop' { throw 'Local server is not PDC Emulator and behaviorIfNotPdc=stop.' }
                'warn' { Write-Warning 'Local server is not PDC Emulator. Skipping time configuration.'; return }
                'skip' { return }
            }
        }
    }
    if (-not $isPdc) { return }

    $manualPeerList = (@($Config.time.externalNtpServers) | ForEach-Object { "$_,$($Config.time.ntpFlags)" }) -join ' '
    if ($Context.PlanOnly) { return }
    $reliable = if ($Config.time.reliableTimeSource) { 'yes' } else { 'no' }
    & w32tm /config /syncfromflags:manual /manualpeerlist:$manualPeerList /reliable:$reliable /update | Out-Null
    Restart-Service -Name w32time -Force
    if ($Config.time.resyncAfterConfiguration) {
        & w32tm /resync /rediscover | Out-Null
    }
}

function Assert-TimeConfiguration {
    <#
    .SYNOPSIS
    Runs configured time validation commands.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    if (-not $Config.time.enabled) { return }
    if ($Config.time.validation.queryStatus) { & w32tm /query /status | Out-Null }
    if ($Config.time.validation.queryConfiguration) { & w32tm /query /configuration | Out-Null }
    if ($Config.time.validation.queryPeers) { & w32tm /query /peers | Out-Null }
}
