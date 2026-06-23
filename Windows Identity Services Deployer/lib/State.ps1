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

function Mark-PhaseComplete {
    <#
    .SYNOPSIS
    Writes phase completion marker.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][pscustomobject]$Config,
        [Parameter(Mandatory = $true)][string]$PhaseName
    )
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
