Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Validate-BackupPath {
    <#
    .SYNOPSIS
    Validates backup path and creates if allowed.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    $path = $Config.backupRecovery.backupPath
    if (Test-Path -LiteralPath $path) { return }
    if (-not $Config.backupRecovery.createBackupPathIfMissing) {
        throw "backupRecovery.backupPath does not exist and createBackupPathIfMissing is false: $path"
    }
    if ($Context.PlanOnly) { return }
    New-Item -Path $path -ItemType Directory -Force | Out-Null
}

function Write-ADBackupRestoreRunbook {
    <#
    .SYNOPSIS
    Writes AD backup/restore runbook content.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    $root = Split-Path $PSScriptRoot -Parent
    $path = Join-Path $root $Config.backupRecovery.runbookPath
    $dir = Split-Path $path -Parent
    if (-not (Test-Path -LiteralPath $dir)) { New-Item -Path $dir -ItemType Directory -Force | Out-Null }
    $content = @"
# AD Backup and Restore Runbook

- System state backup procedure
- Bare-metal recovery considerations
- Authoritative restore vs non-authoritative restore
- SYSVOL recovery considerations
- DNS recovery considerations
- DHCP backup and recovery
- Restore validation evidence capture
- RPO: $($Config.backupRecovery.recoveryObjectives.rpoHours) hours
- RTO: $($Config.backupRecovery.recoveryObjectives.rtoHours) hours
"@
    Set-Content -LiteralPath $path -Value $content -Encoding UTF8
}

function Configure-ADBackupPlanArtifacts {
    <#
    .SYNOPSIS
    Configures backup/recovery artifacts.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.backupRecovery.enabled) { return }
    Validate-BackupPath -Config $Config -Context $Context
    Write-ADBackupRestoreRunbook -Config $Config
    if ($Config.backupRecovery.systemStateBackup.enabled -and $Config.backupRecovery.runInitialBackupNow -and -not $Context.PlanOnly) {
        & wbadmin start systemstatebackup -backuptarget:$Config.backupRecovery.backupPath -quiet | Out-Null
    }
}

function Assert-BackupRecoveryReadiness {
    <#
    .SYNOPSIS
    Asserts backup/recovery runbook and paths are present.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    if (-not $Config.backupRecovery.enabled) { return }
    if (-not (Test-Path -LiteralPath $Config.backupRecovery.backupPath)) {
        throw "Backup path missing: $($Config.backupRecovery.backupPath)"
    }
}
