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

    if (Test-Path -LiteralPath $Config.execution.transcriptPath) {
        Remove-Item -LiteralPath $Config.execution.transcriptPath -Force
    }
    Start-Transcript -Path $Config.execution.transcriptPath -Force | Out-Null

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
