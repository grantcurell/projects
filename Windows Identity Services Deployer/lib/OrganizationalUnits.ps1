Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function New-OrganizationalUnitsFromConfig {
    <#
    .SYNOPSIS
    Creates configured OUs in dependency-safe order.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.organizationalUnits.enabled) { return }
    $domainDn = (Get-ADDomain).DistinguishedName
    $ordered = @($Config.organizationalUnits.structure | Sort-Object { ($_.'distinguishedNameRelative' -split ',').Count })
    foreach ($ou in $ordered) {
        $targetDn = "$($ou.distinguishedNameRelative),$domainDn"
        $existing = $null
        try {
            $existing = Get-ADOrganizationalUnit -Identity $targetDn -ErrorAction Stop
        }
        catch {
            $existing = $null
        }
        if ($existing) { continue }
        if ($Context.PlanOnly) { continue }
        try {
            New-ADOrganizationalUnit -Name (($ou.distinguishedNameRelative -split ',')[0] -replace '^OU=', '') -Path ($targetDn -replace '^[^,]+,', '') -Description $ou.description -ProtectedFromAccidentalDeletion:$Config.organizationalUnits.protectedFromAccidentalDeletion
        }
        catch {
            if ($_.Exception.Message -like '*already in use*') { continue }
            throw
        }
    }
}

function Assert-OrganizationalUnitsExist {
    <#
    .SYNOPSIS
    Verifies configured OUs exist.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    if (-not $Config.organizationalUnits.enabled) { return }
    $domainDn = (Get-ADDomain).DistinguishedName
    foreach ($ou in @($Config.organizationalUnits.structure)) {
        $targetDn = "$($ou.distinguishedNameRelative),$domainDn"
        $existing = $null
        try {
            $existing = Get-ADOrganizationalUnit -Identity $targetDn -ErrorAction Stop
        }
        catch {
            $existing = $null
        }
        if (-not $existing) {
            throw "Missing OU: $targetDn"
        }
    }
}
