Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Initialize-ProjectState {
    <#
    .SYNOPSIS
    Initializes state directory and state files.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)

    if (-not (Test-Path -LiteralPath $Config.execution.statePath)) {
        New-Item -Path $Config.execution.statePath -ItemType Directory -Force | Out-Null
    }
}

function Get-ProjectState {
    <#
    .SYNOPSIS
    Reads current phase state if present.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)

    $file = Join-Path $Config.execution.statePath 'current-phase.json'
    if (-not (Test-Path -LiteralPath $file)) {
        return @{ currentPhase = $null }
    }

    $raw = Get-Content -LiteralPath $file -Raw | ConvertFrom-Json
    $phase = $null
    if ($raw -is [System.Collections.IDictionary]) {
        if ($raw.Contains('currentPhase')) { $phase = $raw['currentPhase'] }
    }
    elseif ($null -ne $raw -and ($raw.PSObject.Properties.Name -contains 'currentPhase')) {
        $phase = $raw.currentPhase
    }

    return @{ currentPhase = $phase }
}

function Set-ProjectState {
    <#
    .SYNOPSIS
    Writes a named state JSON file.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][pscustomobject]$Config,
        [Parameter(Mandatory = $true)][string]$StateName,
        [Parameter(Mandatory = $true)][hashtable]$Data
    )

    $file = Join-Path $Config.execution.statePath "$StateName.json"
    $Data | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $file -Encoding UTF8
}

function Test-PhaseComplete {
    <#
    .SYNOPSIS
    Returns whether phase marker file exists.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][pscustomobject]$Config,
        [Parameter(Mandatory = $true)][string]$PhaseName
    )
    $file = Join-Path $Config.execution.statePath "$PhaseName.json"
    return (Test-Path -LiteralPath $file)
}

function Get-ProjectPhaseCompletionMap {
    <#
    .SYNOPSIS
    Maps orchestration phase names to completion marker files.
    #>
    [CmdletBinding()]
    param()
    return [ordered]@{
        Preflight               = 'preflight-complete'
        PromoteDomainController = 'ad-promoted'
        PostPromotion           = 'post-promotion-complete'
        Validate                = 'validation-complete'
    }
}

function Get-ProjectPhaseSequence {
    <#
    .SYNOPSIS
    Returns ordered phase names for the requested run mode.
    #>
    [CmdletBinding()]
    param([Parameter()][bool]$PlanOnly)
    if ($PlanOnly) {
        return @('Preflight', 'PromoteDomainController')
    }
    return @('Preflight', 'PromoteDomainController', 'PostPromotion', 'Validate')
}

function Test-ProjectConverged {
    <#
    .SYNOPSIS
    Returns true when validation has completed successfully.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    return Test-PhaseComplete -Config $Config -PhaseName 'validation-complete'
}

function Remove-ProjectFailure {
    <#
    .SYNOPSIS
    Clears a prior failure marker so idempotent retries can proceed.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    $file = Join-Path $Config.execution.statePath 'failure.json'
    if (Test-Path -LiteralPath $file) {
        Remove-Item -LiteralPath $file -Force
    }
}

function Get-IncompleteProjectPhases {
    <#
    .SYNOPSIS
    Selects phases that still need work, skipping completed markers on re-run.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][pscustomobject]$Config,
        [Parameter()][bool]$PlanOnly,
        [Parameter()][bool]$ValidateOnly,
        [Parameter()][string]$ExplicitPhase = ''
    )

    if ($ValidateOnly) {
        return @('Validate')
    }
    if ($ExplicitPhase) {
        return @($ExplicitPhase)
    }

    $sequence = Get-ProjectPhaseSequence -PlanOnly:$PlanOnly
    if ($PlanOnly) {
        return $sequence
    }

    if (Test-ProjectConverged -Config $Config) {
        return @('Validate')
    }

    $completionMap = Get-ProjectPhaseCompletionMap
    $incomplete = [System.Collections.Generic.List[string]]::new()
    foreach ($phaseName in $sequence) {
        $marker = [string]$completionMap[$phaseName]
        if (-not (Test-PhaseComplete -Config $Config -PhaseName $marker)) {
            [void]$incomplete.Add($phaseName)
        }
    }

    if ($incomplete.Count -eq 0) {
        return @('Validate')
    }

    $resumeState = Get-ProjectState -Config $Config
    $resumePhase = [string]$resumeState['currentPhase']
    if ($resumePhase -and $incomplete.Contains($resumePhase)) {
        $startIndex = $incomplete.IndexOf($resumePhase)
        if ($startIndex -gt 0) {
            return @($incomplete.GetRange($startIndex, $incomplete.Count - $startIndex))
        }
    }

    if (-not (Get-WindowsFeature -Name 'AD-Domain-Services').Installed) {
        if (-not $incomplete.Contains('Preflight')) {
            return @('Preflight') + @($incomplete | Where-Object { $_ -ne 'Preflight' })
        }
    }

    return @($incomplete)
}

function Mark-PhaseComplete {
    <#
    .SYNOPSIS
    Writes phase completion marker.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][pscustomobject]$Config,
        [Parameter(Mandatory = $true)][string]$PhaseName,
        [Parameter()][hashtable]$Context
    )
    if ($Context -and $Context.PlanOnly) { return }
    Set-ProjectState -Config $Config -StateName $PhaseName -Data @{ completedAt = (Get-Date).ToString('o') }
}

function Register-ResumeScheduledTask {
    <#
    .SYNOPSIS
    Registers reboot-resume scheduled task.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][pscustomobject]$Config,
        [Parameter(Mandatory = $true)][string]$ScriptPath,
        [Parameter(Mandatory = $true)][string]$ConfigPath
    )

    $taskName = [string]$Config.execution.resumeScheduledTaskName
    $action = New-ScheduledTaskAction -Execute 'PowerShell.exe' -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$ScriptPath`" -ConfigPath `"$ConfigPath`""
    $trigger = New-ScheduledTaskTrigger -AtStartup
    $principal = New-ScheduledTaskPrincipal -UserId 'SYSTEM' -RunLevel Highest -LogonType ServiceAccount
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Force | Out-Null
}

function Unregister-ResumeScheduledTask {
    <#
    .SYNOPSIS
    Removes reboot-resume scheduled task.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)

    $taskName = [string]$Config.execution.resumeScheduledTaskName
    if (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue) {
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    }
}
