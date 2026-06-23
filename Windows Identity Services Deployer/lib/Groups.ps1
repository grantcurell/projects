Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function New-GroupsFromConfig {
    <#
    .SYNOPSIS
    Creates AD groups from YAML.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.groups.enabled) { return }
    $domainDn = (Get-ADDomain).DistinguishedName
    foreach ($group in @($Config.groups.items)) {
        $existing = $null
        try {
            $existing = Get-ADGroup -Identity $group.name -ErrorAction Stop
        }
        catch {
            $existing = $null
        }
        if ($existing) { continue }
        if ($Context.PlanOnly) { continue }
        try {
            New-ADGroup -Name $group.name -GroupScope $group.scope -GroupCategory $group.category -Description $group.description -Path "$($group.pathRelative),$domainDn"
        }
        catch {
            if ($_.Exception.Message -like '*already exists*' -or $_.Exception.Message -like '*already in use*') { continue }
            throw
        }
    }
}

function Add-GroupMembersFromConfig {
    <#
    .SYNOPSIS
    Adds explicitly listed members to groups.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.groups.enabled) { return }
    foreach ($group in @($Config.groups.items)) {
        foreach ($member in @($group.members)) {
            if ($Context.PlanOnly) { continue }
            Add-ADGroupMember -Identity $group.name -Members $member -ErrorAction SilentlyContinue
        }
    }
}

function Assert-GroupsExist {
    <#
    .SYNOPSIS
    Verifies configured groups exist.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    if (-not $Config.groups.enabled) { return }
    foreach ($group in @($Config.groups.items)) {
        $existing = $null
        try {
            $existing = Get-ADGroup -Identity $group.name -ErrorAction Stop
        }
        catch {
            $existing = $null
        }
        if (-not $existing) {
            throw "Missing group: $($group.name)"
        }
    }
}
