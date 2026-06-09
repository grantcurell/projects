Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Test-IsAdministrator {
    <#
    .SYNOPSIS
    Returns true when process is elevated.
    #>
    [CmdletBinding()]
    param()
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = [Security.Principal.WindowsPrincipal]::new($identity)
    return $principal.IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
}

function Assert-IsWindowsServer {
    <#
    .SYNOPSIS
    Ensures host OS is Windows Server.
    #>
    [CmdletBinding()]
    param()
    $os = Get-CimInstance -ClassName Win32_OperatingSystem
    if ($os.ProductType -eq 1) {
        throw "Unsupported OS '$($os.Caption)'. Windows Server is required."
    }
}

function Test-PendingReboot {
    <#
    .SYNOPSIS
    Checks pending reboot signals.
    #>
    [CmdletBinding()]
    param()

    $checks = @{
        cbs = Test-Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending'
        wu  = Test-Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired'
        pfr = $false
        crr = $false
    }

    $session = Get-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager' -ErrorAction SilentlyContinue
    if ($session -and $session.PSObject.Properties['PendingFileRenameOperations'] -and $session.PendingFileRenameOperations) { $checks.pfr = $true }

    $computer = Get-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\ComputerName\ActiveComputerName' -ErrorAction SilentlyContinue
    $pending = Get-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\ComputerName\ComputerName' -ErrorAction SilentlyContinue
    if ($computer -and $pending -and $computer.ComputerName -ne $pending.ComputerName) { $checks.crr = $true }

    return [pscustomobject]@{
        IsPending = ($checks.Values -contains $true)
        Details   = $checks
    }
}

function Assert-NoPendingRebootIfRequired {
    <#
    .SYNOPSIS
    Stops if pending reboot exists and config requires clean state.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)

    if (-not $Config.execution.requireCleanPendingReboot) { return }
    $pending = Test-PendingReboot
    if ($pending.IsPending) {
        throw "Pending reboot detected: $($pending.Details | ConvertTo-Json -Compress)"
    }
}

function Assert-ExecutionPolicyUsable {
    <#
    .SYNOPSIS
    Ensures execution policy allows script execution.
    #>
    [CmdletBinding()]
    param()
    $policy = Get-ExecutionPolicy
    if ($policy -in @('Restricted', 'AllSigned')) {
        throw "Execution policy '$policy' may block this script."
    }
}

function Assert-RequiredModules {
    <#
    .SYNOPSIS
    Verifies required modules declared in config.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)

    foreach ($module in @($Config.execution.requiredPowerShellModules)) {
        if (-not (Get-Module -ListAvailable -Name $module.name | Where-Object { $_.Version -ge [version]$module.minimumVersion })) {
            throw "Missing module $($module.name) minimumVersion $($module.minimumVersion). Install command: $($module.installCommand)"
        }
    }
}

function Assert-RequiredPowerShellCommands {
    <#
    .SYNOPSIS
    Verifies command dependencies.
    #>
    [CmdletBinding()]
    param()
    $commands = @('Install-WindowsFeature', 'Get-WindowsFeature', 'Get-NetAdapter')
    foreach ($name in $commands) {
        if (-not (Get-Command -Name $name -ErrorAction SilentlyContinue)) {
            throw "Required command not available: $name"
        }
    }
}

function Assert-NotDomainControllerForDifferentDomain {
    <#
    .SYNOPSIS
    Prevents configuring a DC for wrong domain.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    if (-not (Get-Command -Name Get-ADDomain -ErrorAction SilentlyContinue)) {
        return
    }
    try {
        $domain = Get-ADDomain -ErrorAction Stop
        if ($domain.DNSRoot -ne $Config.activeDirectory.domainName) {
            throw "Server is already a domain controller for a different domain: $($domain.DNSRoot)"
        }
    }
    catch {
        if ($_.Exception.Message -like '*different domain*') { throw }
        if ($_.Exception.Message -like '*The server is not operational*') { return }
        if ($_.Exception.Message -like '*cannot find an object*') { return }
    }
}

function Assert-NotDomainJoinedUnexpectedly {
    <#
    .SYNOPSIS
    Stops if machine is unexpectedly joined to another domain.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)

    $cs = Get-CimInstance -ClassName Win32_ComputerSystem
    if ($cs.PartOfDomain -and $cs.Domain -ne $Config.activeDirectory.domainName) {
        throw "Machine is joined to unexpected domain: $($cs.Domain)"
    }
}
