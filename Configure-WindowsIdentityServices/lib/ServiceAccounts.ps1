Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Initialize-GmsaSupportIfConfigured {
    <#
    .SYNOPSIS
    Initializes KDS root key when gMSA creation is enabled.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)

    if (-not $Config.serviceAccounts.createGroupManagedServiceAccounts) { return }
    foreach ($required in @('kdsRootKeyEffectiveTimeUtc', 'dnsHostNameSuffix')) {
        if ($null -eq $Config.serviceAccounts.gmsa.$required -or [string]::IsNullOrWhiteSpace([string]$Config.serviceAccounts.gmsa.$required)) {
            throw "serviceAccounts.gmsa.$required is required when createGroupManagedServiceAccounts is true."
        }
    }
    if ($Context.PlanOnly) { return }
    $existing = Get-KdsRootKey -ErrorAction SilentlyContinue
    if (-not $existing) {
        Add-KdsRootKey -EffectiveTime ([datetime]$Config.serviceAccounts.gmsa.kdsRootKeyEffectiveTimeUtc) | Out-Null
    }
}

function New-ServiceAccountsFromConfig {
    <#
    .SYNOPSIS
    Creates service accounts from YAML configuration.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.serviceAccounts.enabled) { return }
    Initialize-GmsaSupportIfConfigured -Config $Config -Context $Context

    $domainDn = (Get-ADDomain).DistinguishedName
    foreach ($account in @($Config.serviceAccounts.accounts)) {
        if ($account.type -eq 'gmsa') {
            if (-not $Config.serviceAccounts.createGroupManagedServiceAccounts) {
                throw "Service account '$($account.samAccountName)' is gmsa but createGroupManagedServiceAccounts is false."
            }
            if (-not $Context.PlanOnly) {
                $dnsHostName = "$($account.samAccountName).$($Config.serviceAccounts.gmsa.dnsHostNameSuffix)"
                $existingSvc = Get-ADServiceAccount -Identity $account.samAccountName -ErrorAction SilentlyContinue
                if (-not $existingSvc) {
                    New-ADServiceAccount -Name $account.samAccountName -DNSHostName $dnsHostName -Description $account.description | Out-Null
                }
            }
            continue
        }
        if ($account.type -ne 'standard') { throw "Unsupported service account type: $($account.type)" }
        $existing = Get-ADUser -Filter "SamAccountName -eq '$($account.samAccountName)'" -ErrorAction SilentlyContinue
        if (-not $existing) {
            if (-not $account.passwordPrompt) { throw "passwordPrompt must be true for account $($account.samAccountName)" }
            if ($Context.PlanOnly) { continue }
            $pwd = $null
            if ($env:CONFIGURE_WIS_SERVICEACCOUNT_PASSWORD) {
                $pwd = ConvertTo-SecureString -String $env:CONFIGURE_WIS_SERVICEACCOUNT_PASSWORD -AsPlainText -Force
            }
            else {
                $pwd = Read-Host -Prompt "Enter password for service account $($account.samAccountName)" -AsSecureString
            }
            New-ADUser -Name $account.name -SamAccountName $account.samAccountName -Path "$($account.pathRelative),$domainDn" -Description $account.description -Enabled:$account.enabled -AccountPassword $pwd -PasswordNeverExpires:$account.passwordNeverExpires
        }
        elseif ($account.resetPasswordIfExists) {
            if ($Context.PlanOnly) { continue }
            $pwdExisting = $null
            if ($env:CONFIGURE_WIS_SERVICEACCOUNT_PASSWORD) {
                $pwdExisting = ConvertTo-SecureString -String $env:CONFIGURE_WIS_SERVICEACCOUNT_PASSWORD -AsPlainText -Force
            }
            else {
                $pwdExisting = Read-Host -Prompt "Reset password for existing service account $($account.samAccountName)" -AsSecureString
            }
            Set-ADAccountPassword -Identity $account.samAccountName -Reset -NewPassword $pwdExisting
        }

        foreach ($group in @($account.groups)) {
            if (-not $Context.PlanOnly) {
                Add-ADGroupMember -Identity $group -Members $account.samAccountName -ErrorAction SilentlyContinue
            }
        }
    }
}

function Assert-ServiceAccountsExist {
    <#
    .SYNOPSIS
    Verifies configured service accounts exist.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    if (-not $Config.serviceAccounts.enabled) { return }
    foreach ($account in @($Config.serviceAccounts.accounts)) {
        if ($account.type -eq 'gmsa') {
            if (-not (Get-ADServiceAccount -Identity $account.samAccountName -ErrorAction SilentlyContinue)) {
                throw "Missing gMSA account: $($account.samAccountName)"
            }
        }
        elseif (-not (Get-ADUser -Filter "SamAccountName -eq '$($account.samAccountName)'" -ErrorAction SilentlyContinue)) {
            throw "Missing standard service account: $($account.samAccountName)"
        }
    }
}
