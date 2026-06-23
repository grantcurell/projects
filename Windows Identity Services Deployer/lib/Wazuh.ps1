Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Install-WazuhAgentFromConfig {
    <#
    .SYNOPSIS
    Installs Wazuh agent from local/UNC MSI path.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.wazuh.enabled) { return }
    foreach ($required in @('agentMsiPath','managerAddress','deploymentMode')) {
        if ([string]::IsNullOrWhiteSpace([string]$Config.wazuh.$required)) { throw "wazuh.$required is required when enabled." }
    }
    if ($Config.wazuh.deploymentMode -ne 'silent') { return }
    if ($Context.PlanOnly) { return }
    Start-Process msiexec.exe -ArgumentList "/i `"$($Config.wazuh.agentMsiPath)`" /qn WAZUH_MANAGER=`"$($Config.wazuh.managerAddress)`"" -Wait -NoNewWindow
}

function Configure-WazuhAgentFromConfig {
    <#
    .SYNOPSIS
    Starts configured Wazuh service.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.wazuh.enabled -or $Context.PlanOnly) { return }
    Start-Service -Name $Config.wazuh.serviceName -ErrorAction SilentlyContinue
}

function Assert-WazuhAgentState {
    <#
    .SYNOPSIS
    Validates Wazuh service status.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    if (-not $Config.wazuh.enabled -or -not $Config.wazuh.validateServiceRunning) { return }
    $service = Get-Service -Name $Config.wazuh.serviceName -ErrorAction SilentlyContinue
    if (-not $service -or $service.Status -ne 'Running') { throw "Wazuh service not running: $($Config.wazuh.serviceName)" }
}
