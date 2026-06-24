Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Initialize-ProjectLogging {
    <#
    .SYNOPSIS
    Initializes transcript and JSONL logging.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [pscustomobject]$Config
    )

    foreach ($path in @($Config.execution.logPath, $Config.execution.evidencePath)) {
        if (-not (Test-Path -LiteralPath $path)) {
            New-Item -Path $path -ItemType Directory -Force | Out-Null
        }
    }

    # A previous or concurrent run (or an orphaned process that outlived its WinRM
    # client) can hold the transcript file open. A locked transcript must never abort
    # the whole deploy: try the configured path, fall back to a unique path if it is
    # locked, and finally continue without a transcript rather than throwing here.
    $transcriptPath = $Config.execution.transcriptPath
    try {
        if (Test-Path -LiteralPath $transcriptPath) {
            Remove-Item -LiteralPath $transcriptPath -Force -ErrorAction Stop
        }
    }
    catch {
        $transcriptPath = [System.IO.Path]::Combine(
            (Split-Path -Parent $transcriptPath),
            ('transcript-{0}.log' -f (Get-Date -Format 'yyyyMMddHHmmss'))
        )
    }
    try {
        Start-Transcript -Path $transcriptPath -Force | Out-Null
    }
    catch {
        Write-Warning "Could not start transcript at '$transcriptPath': $($_.Exception.Message). Continuing without a transcript."
    }

    if (-not (Test-Path -LiteralPath $Config.execution.jsonLogPath)) {
        New-Item -Path $Config.execution.jsonLogPath -ItemType File -Force | Out-Null
    }
}

function Write-OperationLog {
    <#
    .SYNOPSIS
    Writes structured JSON Lines log entry.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)] [pscustomobject]$Config,
        [Parameter(Mandatory = $true)] [string]$Phase,
        [Parameter(Mandatory = $true)] [string]$Component,
        [Parameter(Mandatory = $true)] [string]$Operation,
        [Parameter(Mandatory = $true)] [string]$Target,
        [Parameter(Mandatory = $true)] [hashtable]$InputValues,
        [Parameter(Mandatory = $true)] [string]$Result,
        [Parameter()] [string]$ErrorMessage
    )

    $entry = [ordered]@{
        timestamp   = (Get-Date).ToString('o')
        phase       = $Phase
        component   = $Component
        operation   = $Operation
        target      = $Target
        inputValues = $InputValues
        result      = $Result
        error       = $ErrorMessage
    }
    $json = ($entry | ConvertTo-Json -Depth 8 -Compress)
    Add-Content -LiteralPath $Config.execution.jsonLogPath -Value $json -Encoding UTF8
}

function Write-ProjectInfo {
    <#
    .SYNOPSIS
    Writes informational output.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][string]$Message)
    Write-Host "[INFO ] $Message"
}

function Write-ProjectWarning {
    <#
    .SYNOPSIS
    Writes warning output.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][string]$Message)
    Write-Warning $Message
}

function Write-ProjectError {
    <#
    .SYNOPSIS
    Writes error output.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][string]$Message)
    Write-Error $Message
}

function Stop-WithProjectError {
    <#
    .SYNOPSIS
    Writes and throws a terminating project error.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [pscustomobject]$Config,
        [Parameter(Mandatory = $true)]
        [string]$Phase,
        [Parameter(Mandatory = $true)]
        [string]$Component,
        [Parameter(Mandatory = $true)]
        [string]$Operation,
        [Parameter(Mandatory = $true)]
        [string]$Target,
        [Parameter(Mandatory = $true)]
        [hashtable]$InputValues,
        [Parameter(Mandatory = $true)]
        [string]$Message
    )

    Write-OperationLog -Config $Config -Phase $Phase -Component $Component -Operation $Operation -Target $Target -InputValues $InputValues -Result 'Failed' -ErrorMessage $Message
    throw $Message
}
