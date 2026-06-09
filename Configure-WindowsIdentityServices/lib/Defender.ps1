Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Configure-DefenderFromConfig {
    <#
    .SYNOPSIS
    Configures Microsoft Defender according to YAML.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.defender.enabled -or -not $Config.defender.configureMicrosoftDefender) { return }
    if ($Context.PlanOnly) { return }
    Set-MpPreference -DisableRealtimeMonitoring:(!$Config.defender.realTimeProtection)
    Set-MpPreference -MAPSReporting ($(if ($Config.defender.cloudProtection) { 2 } else { 0 }))
    Set-MpPreference -SubmitSamplesConsent ($(if ($Config.defender.sampleSubmission) { 1 } else { 2 }))
    if ($Config.defender.exclusions.paths) { Add-MpPreference -ExclusionPath @($Config.defender.exclusions.paths) }
    if ($Config.defender.exclusions.processes) { Add-MpPreference -ExclusionProcess @($Config.defender.exclusions.processes) }
    if ($Config.defender.exclusions.extensions) { Add-MpPreference -ExclusionExtension @($Config.defender.exclusions.extensions) }
    if ($Config.defender.onboarding.enabled) {
        if ([string]::IsNullOrWhiteSpace([string]$Config.defender.onboarding.scriptPath)) { throw 'defender.onboarding.scriptPath is required when onboarding.enabled is true.' }
        & $Config.defender.onboarding.scriptPath
    }
}

function Assert-DefenderState {
    <#
    .SYNOPSIS
    Validates Defender operational state.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    if (-not $Config.defender.enabled) { return }
    Get-MpComputerStatus -ErrorAction Stop | Out-Null
}
