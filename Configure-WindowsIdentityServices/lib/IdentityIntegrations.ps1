Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Assert-IdentityIntegrationPrerequisites {
    <#
    .SYNOPSIS
    Validates AD objects required by identity integrations.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    if (-not $Config.identityIntegrations.enabled) { return }
    if ($Config.identityIntegrations.gitlab.enabled -and $Config.identityIntegrations.gitlab.approved) {
        Get-ADUser -Filter "SamAccountName -eq '$($Config.identityIntegrations.gitlab.ldapBindAccountSam)'" -ErrorAction Stop | Out-Null
        Get-ADGroup -Identity $Config.identityIntegrations.gitlab.allowedGroup -ErrorAction Stop | Out-Null
    }
    if ($Config.identityIntegrations.keycloak.enabled -and $Config.identityIntegrations.keycloak.approved) {
        Get-ADUser -Filter "SamAccountName -eq '$($Config.identityIntegrations.keycloak.ldapBindAccountSam)'" -ErrorAction Stop | Out-Null
        Get-ADGroup -Identity $Config.identityIntegrations.keycloak.allowedGroup -ErrorAction Stop | Out-Null
    }
    if ($Config.identityIntegrations.yubiKey.enabled) {
        Get-ADGroup -Identity $Config.identityIntegrations.yubiKey.policyGroup -ErrorAction Stop | Out-Null
    }
}

function Write-GitLabAdIntegrationArtifact {
    <#
    .SYNOPSIS
    Writes GitLab LDAP integration example artifact.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.identityIntegrations.enabled -or -not $Config.identityIntegrations.gitlab.enabled) { return }
    if (-not $Config.identityIntegrations.gitlab.approved) { return }
    Get-ADUser -Filter "SamAccountName -eq '$($Config.identityIntegrations.gitlab.ldapBindAccountSam)'" -ErrorAction Stop | Out-Null
    Get-ADGroup -Identity $Config.identityIntegrations.gitlab.allowedGroup -ErrorAction Stop | Out-Null
    if ($Context.PlanOnly) { return }
    $bindDn = (Get-ADUser -Filter "SamAccountName -eq '$($Config.identityIntegrations.gitlab.ldapBindAccountSam)'").DistinguishedName
    $text = @"
GitLab LDAP example:
bind_dn=$bindDn
base_dn=$((Get-ADDomain).DistinguishedName)
allowed_group=$($Config.identityIntegrations.gitlab.allowedGroup)
"@
    Set-Content -LiteralPath $Config.identityIntegrations.gitlab.outputConfigSnippetPath -Value $text -Encoding UTF8
}

function Write-KeycloakAdFederationArtifact {
    <#
    .SYNOPSIS
    Writes Keycloak AD federation summary.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.identityIntegrations.enabled -or -not $Config.identityIntegrations.keycloak.enabled) { return }
    if (-not $Config.identityIntegrations.keycloak.approved) { return }
    Get-ADUser -Filter "SamAccountName -eq '$($Config.identityIntegrations.keycloak.ldapBindAccountSam)'" -ErrorAction Stop | Out-Null
    Get-ADGroup -Identity $Config.identityIntegrations.keycloak.allowedGroup -ErrorAction Stop | Out-Null
    if ($Context.PlanOnly) { return }
    $text = @"
Keycloak AD Federation Summary
connectionUrl: $($Config.identityIntegrations.keycloak.connectionUrl)
baseDn: $((Get-ADDomain).DistinguishedName)
allowedGroup: $($Config.identityIntegrations.keycloak.allowedGroup)
useKerberos: $($Config.identityIntegrations.keycloak.useKerberos)
kerberosRealm: $($Config.identityIntegrations.keycloak.kerberosRealm)
"@
    Set-Content -LiteralPath $Config.identityIntegrations.keycloak.outputConfigSummaryPath -Value $text -Encoding UTF8
}

function Write-YubiKeyPolicyArtifact {
    <#
    .SYNOPSIS
    Writes YubiKey policy notes and optional smart-card enforcement.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.identityIntegrations.enabled -or -not $Config.identityIntegrations.yubiKey.enabled) { return }
    Get-ADGroup -Identity $Config.identityIntegrations.yubiKey.policyGroup -ErrorAction Stop | Out-Null
    $text = @"
YubiKey policy group: $($Config.identityIntegrations.yubiKey.policyGroup)
requireSmartCardForInteractiveLogon: $($Config.identityIntegrations.yubiKey.requireSmartCardForInteractiveLogon)
applySmartCardRequirementToGroupMembers: $($Config.identityIntegrations.yubiKey.applySmartCardRequirementToGroupMembers)
certificateMappingPlanned: $($Config.identityIntegrations.yubiKey.certificateMappingPlanned)
"@
    if (-not $Context.PlanOnly) {
        Set-Content -LiteralPath $Config.identityIntegrations.yubiKey.notesPath -Value $text -Encoding UTF8
    }
    if ($Config.identityIntegrations.yubiKey.requireSmartCardForInteractiveLogon -and $Config.identityIntegrations.yubiKey.applySmartCardRequirementToGroupMembers -and -not $Context.PlanOnly) {
        $members = Get-ADGroupMember -Identity $Config.identityIntegrations.yubiKey.policyGroup -Recursive | Where-Object { $_.objectClass -eq 'user' }
        foreach ($member in $members) {
            Set-ADUser -Identity $member.SamAccountName -SmartcardLogonRequired $true
        }
    }
}
