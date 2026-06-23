Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Configure-FirewallProfilesFromConfig {
    <#
    .SYNOPSIS
    Configures firewall profiles from YAML.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.firewall.enabled -or -not $Config.firewall.configureProfiles) { return }
    if ($Context.PlanOnly) { return }
    foreach ($profileName in @('domain','private','public')) {
        $profile = $Config.firewall.profiles.$profileName
        $enabledValue = if ($profile.enabled) { 'True' } else { 'False' }
        Set-NetFirewallProfile -Profile $profileName -Enabled:$enabledValue -DefaultInboundAction $profile.defaultInboundAction -DefaultOutboundAction $profile.defaultOutboundAction
    }
}

function Enable-BuiltInFirewallRuleGroupsFromConfig {
    <#
    .SYNOPSIS
    Enables only built-in rule groups listed in YAML.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.firewall.enabled) { return }
    foreach ($group in @($Config.firewall.enableBuiltInRuleGroups)) {
        if ($Context.PlanOnly) { continue }
        Enable-NetFirewallRule -DisplayGroup $group -ErrorAction SilentlyContinue
    }
}

function Create-CustomFirewallRulesFromConfig {
    <#
    .SYNOPSIS
    Creates custom firewall rules exactly as declared.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.firewall.enabled) { return }
    foreach ($rule in @($Config.firewall.customRules)) {
        if ($Context.PlanOnly) { continue }
        if (-not (Get-NetFirewallRule -DisplayName $rule.displayName -ErrorAction SilentlyContinue)) {
            New-NetFirewallRule -DisplayName $rule.displayName -Direction $rule.direction -Action $rule.action -Profile $rule.profile -Protocol $rule.protocol -LocalPort $rule.localPort
        }
    }
}

function Assert-FirewallState {
    <#
    .SYNOPSIS
    Verifies firewall profiles are enabled.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    if (-not $Config.firewall.enabled) { return }
    $profiles = Get-NetFirewallProfile
    if ($profiles | Where-Object { -not $_.Enabled }) {
        throw 'One or more firewall profiles are disabled.'
    }
}
