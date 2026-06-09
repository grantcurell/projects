Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Install-WsusIfEnabled {
    <#
    .SYNOPSIS
    Ensures WSUS prerequisites when enabled.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.wsus.enabled) { return }
    foreach ($required in @('contentDirectory','upstreamServer','upstreamPort')) {
        if ([string]::IsNullOrWhiteSpace([string]$Config.wsus.$required)) { throw "wsus.$required is required when WSUS is enabled." }
    }
    if (@($Config.wsus.products).Count -eq 0) { throw 'wsus.products must be non-empty when wsus.enabled is true.' }
    if (@($Config.wsus.classifications).Count -eq 0) { throw 'wsus.classifications must be non-empty when wsus.enabled is true.' }
    if (@($Config.wsus.computerTargetGroups).Count -eq 0) { throw 'wsus.computerTargetGroups must be non-empty when wsus.enabled is true.' }
    if ($Context.PlanOnly) { return }
    if (-not (Test-Path -LiteralPath $Config.wsus.contentDirectory)) {
        New-Item -Path $Config.wsus.contentDirectory -ItemType Directory -Force | Out-Null
    }
    if (-not (Get-Service -Name WsusService -ErrorAction SilentlyContinue)) {
        Install-WindowsFeature -Name UpdateServices -IncludeManagementTools | Out-Null
    }
}

function Configure-WsusProductsClassifications {
    <#
    .SYNOPSIS
    Configures WSUS products and classifications from YAML.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.wsus.enabled -or $Context.PlanOnly) { return }
    [void][reflection.assembly]::LoadWithPartialName('Microsoft.UpdateServices.Administration')
    $server = [Microsoft.UpdateServices.Administration.AdminProxy]::GetUpdateServer()
    $subscription = $server.GetSubscription()
    $allProducts = $server.GetUpdateCategories() | Where-Object { $_.Type -eq 'Product' }
    $allClasses = $server.GetUpdateClassifications()
    foreach ($name in @($Config.wsus.products)) {
        $match = $allProducts | Where-Object { $_.Title -eq $name }
        if (-not $match) { throw "WSUS product not found: $name" }
        $subscription.SetUpdateCategories(@($match))
    }
    foreach ($name in @($Config.wsus.classifications)) {
        $match = $allClasses | Where-Object { $_.Title -eq $name }
        if (-not $match) { throw "WSUS classification not found: $name" }
        $subscription.SetUpdateClassifications(@($match))
    }
    $subscription.Save()
}

function Configure-WsusComputerTargetGroups {
    <#
    .SYNOPSIS
    Configures WSUS computer target groups from YAML.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.wsus.enabled -or $Context.PlanOnly) { return }
    [void][reflection.assembly]::LoadWithPartialName('Microsoft.UpdateServices.Administration')
    $server = [Microsoft.UpdateServices.Administration.AdminProxy]::GetUpdateServer()
    foreach ($groupName in @($Config.wsus.computerTargetGroups)) {
        $existing = $server.GetComputerTargetGroups() | Where-Object { $_.Name -eq $groupName }
        if (-not $existing) {
            [void]$server.CreateComputerTargetGroup($groupName)
        }
    }
}

function Configure-WsusAutoApprovalRules {
    <#
    .SYNOPSIS
    Configures WSUS auto-approval rules from YAML.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.wsus.enabled -or $Context.PlanOnly) { return }
    [void][reflection.assembly]::LoadWithPartialName('Microsoft.UpdateServices.Administration')
    $server = [Microsoft.UpdateServices.Administration.AdminProxy]::GetUpdateServer()
    foreach ($rule in @($Config.wsus.autoApprovalRules)) {
        if ([string]::IsNullOrWhiteSpace([string]$rule.name)) { throw 'wsus.autoApprovalRules[].name is required.' }
        $existing = $server.GetInstallApprovalRules() | Where-Object { $_.Name -eq $rule.name }
        if ($existing) { continue }
        $newRule = $server.CreateInstallApprovalRule($rule.name)
        $newRule.Enabled = $true
        $newRule.Save()
    }
}

function Write-PatchManagementRunbook {
    <#
    .SYNOPSIS
    Ensures WSUS runbook paths exist.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    if (-not $Config.wsus.enabled) { return }
    foreach ($path in @($Config.wsus.emergencyPatching.runbookPath, $Config.wsus.rollback.runbookPath)) {
        $fullPath = Join-Path (Split-Path $PSScriptRoot -Parent) $path
        $dir = Split-Path $fullPath -Parent
        if (-not (Test-Path -LiteralPath $dir)) { New-Item -Path $dir -ItemType Directory -Force | Out-Null }
        if (-not (Test-Path -LiteralPath $fullPath)) { New-Item -Path $fullPath -ItemType File -Force | Out-Null }
    }
}

function Configure-WsusFromConfig {
    <#
    .SYNOPSIS
    Applies WSUS configuration sequence.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.wsus.enabled) { return }
    if (-not $Context.PlanOnly) {
        & wsusutil postinstall CONTENT_DIR=$($Config.wsus.contentDirectory) | Out-Null
    }
    Configure-WsusProductsClassifications -Config $Config -Context $Context
    Configure-WsusComputerTargetGroups -Config $Config -Context $Context
    Configure-WsusAutoApprovalRules -Config $Config -Context $Context
    Write-PatchManagementRunbook -Config $Config
}

function Assert-WsusState {
    <#
    .SYNOPSIS
    Validates WSUS state.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    if (-not $Config.wsus.enabled) { return }
    $svc = Get-Service -Name WsusService -ErrorAction SilentlyContinue
    if (-not $svc) { throw 'WSUS service not found.' }
}
