Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Test-ProxmoxVirtioDrivers {
    <#
    .SYNOPSIS
    Checks for expected Proxmox guest device patterns.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    $devices = Get-PnpDevice -ErrorAction SilentlyContinue
    foreach ($pattern in @($Config.proxmoxGuest.expectedDeviceNamePatterns)) {
        if (-not ($devices | Where-Object { $_.FriendlyName -like "*$pattern*" -or $_.Manufacturer -like "*$pattern*" })) {
            return $false
        }
    }
    return $true
}

function Test-QemuGuestAgent {
    <#
    .SYNOPSIS
    Checks whether QEMU guest agent service exists.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    return [bool](Get-Service -Name $Config.proxmoxGuest.qemuGuestAgentServiceName -ErrorAction SilentlyContinue)
}

function Install-QemuGuestAgentIfAllowed {
    <#
    .SYNOPSIS
    Optionally installs guest tools from configured path.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][pscustomobject]$Config,
        [Parameter(Mandatory = $true)][hashtable]$Context
    )
    if (-not $Config.proxmoxGuest.allowSilentGuestToolsInstall) {
        throw 'QEMU Guest Agent missing. Manual installation required per YAML policy.'
    }
    if (-not (Test-Path -LiteralPath $Config.proxmoxGuest.guestToolsInstallerPath)) {
        throw "Guest tools installer not found: $($Config.proxmoxGuest.guestToolsInstallerPath)"
    }
    if ($Context.PlanOnly) { return }
    Start-Process -FilePath $Config.proxmoxGuest.guestToolsInstallerPath -ArgumentList '/S' -Wait -NoNewWindow
}

function Assert-ProxmoxGuestReady {
    <#
    .SYNOPSIS
    Validates Proxmox guest readiness requirements.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][pscustomobject]$Config,
        [Parameter(Mandatory = $true)][hashtable]$Context
    )
    if (-not $Config.proxmoxGuest.enabled) { return }

    if ($Config.proxmoxGuest.requireVirtioDrivers -and -not (Test-ProxmoxVirtioDrivers -Config $Config)) {
        throw 'Required VirtIO/QEMU devices were not detected.'
    }
    if ($Config.proxmoxGuest.requireQemuGuestAgent -and -not (Test-QemuGuestAgent -Config $Config)) {
        Install-QemuGuestAgentIfAllowed -Config $Config -Context $Context
    }
    $svc = Get-Service -Name $Config.proxmoxGuest.qemuGuestAgentServiceName -ErrorAction SilentlyContinue
    if ($svc -and $svc.Status -ne 'Running' -and -not $Context.PlanOnly) {
        Start-Service -Name $svc.Name
    }
}
