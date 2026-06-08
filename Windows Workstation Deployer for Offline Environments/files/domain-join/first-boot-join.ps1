# first-boot-join.ps1
#
# Runs ONCE as SYSTEM at the end of Windows setup, before any interactive logon,
# invoked by W:\Windows\Setup\Scripts\SetupComplete.cmd (staged by deploy.ps1).
#
# Responsibilities:
#   * Resolve the authoritative computer name from the BIOS service tag.
#   * Domain enabled : Add-Computer -NewName <tag> -DomainName <fqdn> -OUPath <ou>
#                      -Credential <cred> -Force   (NEVER -Restart).
#   * Domain disabled: Rename-Computer -NewName <tag> -Force   (NEVER -Restart).
#   * ALWAYS scrub the transient credential + this script BEFORE rebooting, so the
#     scrub can never be skipped by a premature reboot.
#   * Reboot only as the final action via Restart-Computer -Force.
#
# The password is never written to the log.

$ErrorActionPreference = "Stop"

$ScriptDir = $PSScriptRoot
if (-not $ScriptDir) {
    $ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
}
$ConfigPath = Join-Path $ScriptDir "join-config.json"
$CredentialPath = Join-Path $ScriptDir "join.cred"
$ScriptPath = Join-Path $ScriptDir "first-boot-join.ps1"
$SetupCompletePath = Join-Path $ScriptDir "SetupComplete.cmd"
$LogPath = Join-Path $ScriptDir "join.log"

function Write-JoinLog {
    param([string]$Message)
    $line = "$(Get-Date -Format s) $Message"
    Write-Host $line
    try {
        Add-Content -Path $LogPath -Value $line -ErrorAction SilentlyContinue
    } catch {
    }
}

function Remove-Secret {
    param([string]$Path)
    if (Test-Path $Path) {
        try {
            # Best-effort overwrite before deletion.
            $bytes = [byte[]]::new((Get-Item $Path).Length)
            [System.IO.File]::WriteAllBytes($Path, $bytes)
        } catch {
        }
        Remove-Item -Path $Path -Force -ErrorAction SilentlyContinue
    }
}

function Get-DellServiceTag {
    $bios = Get-CimInstance -ClassName Win32_BIOS -ErrorAction Stop
    $serial = ($bios.SerialNumber | Out-String).Trim()
    $invalid = @(
        "", "0", "none", "default string", "system serial number",
        "to be filled by o.e.m.", "not specified", "not available", "unknown"
    )
    if ($invalid -contains $serial.ToLowerInvariant()) {
        throw "BIOS serial number '$serial' is not a valid service tag."
    }
    return $serial
}

$rebootRequired = $false
try {
    Write-JoinLog "first-boot-join starting."

    if (-not (Test-Path $ConfigPath)) {
        throw "join-config.json not found at $ConfigPath."
    }
    $config = Get-Content -Path $ConfigPath -Raw | ConvertFrom-Json

    $serviceTag = Get-DellServiceTag
    Write-JoinLog "Resolved service tag: $serviceTag"

    $domainEnabled = $false
    if ($null -ne $config.domain_join_enabled) {
        $domainEnabled = [bool]$config.domain_join_enabled
    }

    if ($domainEnabled) {
        $domainFqdn = [string]$config.domain_fqdn
        $ouPath = [string]$config.ou_path
        if ([string]::IsNullOrWhiteSpace($domainFqdn) -or [string]::IsNullOrWhiteSpace($ouPath)) {
            throw "Domain join enabled but domain_fqdn/ou_path missing from join-config.json (no defaults)."
        }
        if (-not (Test-Path $CredentialPath)) {
            throw "Domain join enabled but transient credential $CredentialPath is missing."
        }

        $credRaw = Get-Content -Path $CredentialPath -Raw | ConvertFrom-Json
        if ([string]::IsNullOrWhiteSpace([string]$credRaw.username) -or [string]::IsNullOrWhiteSpace([string]$credRaw.password)) {
            throw "Transient credential file is missing username/password."
        }
        $securePass = ConvertTo-SecureString ([string]$credRaw.password) -AsPlainText -Force
        $cred = New-Object System.Management.Automation.PSCredential(([string]$credRaw.username), $securePass)

        $joined = $false
        $maxAttempts = 3
        for ($attempt = 1; $attempt -le $maxAttempts -and -not $joined; $attempt++) {
            try {
                Write-JoinLog "Add-Computer attempt $attempt/$maxAttempts (name=$serviceTag, domain=$domainFqdn)."
                if ($env:COMPUTERNAME -ieq $serviceTag) {
                    Add-Computer -DomainName $domainFqdn -OUPath $ouPath -Credential $cred -Force -ErrorAction Stop
                } else {
                    Add-Computer -DomainName $domainFqdn -OUPath $ouPath -NewName $serviceTag -Credential $cred -Force -ErrorAction Stop
                }
                $joined = $true
                Write-JoinLog "Domain join succeeded."
            } catch {
                Write-JoinLog "Add-Computer attempt $attempt failed: $($_.Exception.Message)"
                if ($attempt -lt $maxAttempts) {
                    Start-Sleep -Seconds 30
                }
            }
        }

        if (-not $joined) {
            Write-JoinLog "Domain join failed after $maxAttempts attempts. Falling back to workgroup rename so the box is still named correctly."
            try {
                if ($env:COMPUTERNAME -ine $serviceTag) {
                    Rename-Computer -NewName $serviceTag -Force -ErrorAction Stop
                }
            } catch {
                Write-JoinLog "Workgroup rename also failed: $($_.Exception.Message)"
            }
        }
        $rebootRequired = $true
    }
    else {
        if ($env:COMPUTERNAME -ine $serviceTag) {
            Write-JoinLog "Domain join disabled. Renaming to $serviceTag (workgroup)."
            Rename-Computer -NewName $serviceTag -Force -ErrorAction Stop
            $rebootRequired = $true
        } else {
            Write-JoinLog "Domain join disabled and name already matches service tag; nothing to do."
        }
    }
}
catch {
    Write-JoinLog "FATAL: $($_.Exception.Message)"
}
finally {
    # Scrub BEFORE rebooting so a premature reboot can never skip credential removal.
    Remove-Secret -Path $CredentialPath
    Remove-Item -Path $ScriptPath -Force -ErrorAction SilentlyContinue
    Remove-Item -Path $SetupCompletePath -Force -ErrorAction SilentlyContinue
    Write-JoinLog "Scrub complete (credential + first-boot script removed)."

    if ($rebootRequired) {
        Write-JoinLog "Rebooting now (final action)."
        Restart-Computer -Force
    }
}
