[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$ConfigPath,

    [Parameter()]
    [switch]$PlanOnly,

    [Parameter()]
    [switch]$ValidateOnly,

    [Parameter()]
    [ValidateSet('Preflight', 'PromoteDomainController', 'PostPromotion', 'Validate')]
    [string]$Phase
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSCommandPath
$libRoot = Join-Path $projectRoot 'lib'

. (Join-Path $libRoot 'Config.ps1')
. (Join-Path $libRoot 'Logging.ps1')
. (Join-Path $libRoot 'State.ps1')
. (Join-Path $libRoot 'Preconditions.ps1')
. (Join-Path $libRoot 'ProxmoxGuest.ps1')
. (Join-Path $libRoot 'Network.ps1')
. (Join-Path $libRoot 'Roles.ps1')
. (Join-Path $libRoot 'ActiveDirectory.ps1')
. (Join-Path $libRoot 'Dns.ps1')
. (Join-Path $libRoot 'Dhcp.ps1')
. (Join-Path $libRoot 'Time.ps1')
. (Join-Path $libRoot 'OrganizationalUnits.ps1')
. (Join-Path $libRoot 'Groups.ps1')
. (Join-Path $libRoot 'ServiceAccounts.ps1')
. (Join-Path $libRoot 'Gpo.ps1')
. (Join-Path $libRoot 'Hardening.ps1')
. (Join-Path $libRoot 'Defender.ps1')
. (Join-Path $libRoot 'Firewall.ps1')
. (Join-Path $libRoot 'EventForwarding.ps1')
. (Join-Path $libRoot 'Wazuh.ps1')
. (Join-Path $libRoot 'Pki.ps1')
. (Join-Path $libRoot 'Wsus.ps1')
. (Join-Path $libRoot 'BackupRecovery.ps1')
. (Join-Path $libRoot 'VulnerabilityScanning.ps1')
. (Join-Path $libRoot 'IdentityIntegrations.ps1')
. (Join-Path $libRoot 'Validation.ps1')
. (Join-Path $libRoot 'Report.ps1')

function Invoke-ProjectPhase {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [ValidateSet('Preflight', 'PromoteDomainController', 'PostPromotion', 'Validate')]
        [string]$PhaseName,

        [Parameter(Mandatory = $true)]
        [pscustomobject]$Config,

        [Parameter(Mandatory = $true)]
        [hashtable]$Context
    )

    switch ($PhaseName) {
        'Preflight' {
            Assert-NoPendingRebootIfRequired -Config $Config
            Assert-ExecutionPolicyUsable
            Assert-RequiredModules -Config $Config
            Assert-RequiredPowerShellCommands
            Assert-IsWindowsServer
            Assert-NotDomainJoinedUnexpectedly -Config $Config
            Assert-NotDomainControllerForDifferentDomain -Config $Config
            Assert-ProxmoxGuestReady -Config $Config -Context $Context
            Set-ComputerNameIfNeeded -Config $Config -Context $Context
            Assert-NetworkReady -Config $Config -Context $Context
            Install-RequiredWindowsFeatures -Config $Config -Context $Context
            if (-not $Context.PlanOnly) {
                Assert-WindowsFeaturesInstalled -Config $Config
            }
            Mark-PhaseComplete -Config $Config -PhaseName 'roles-installed'
            Mark-PhaseComplete -Config $Config -PhaseName 'preflight-complete'
        }
        'PromoteDomainController' {
            Install-NewForestFromConfig -Config $Config -Context $Context
            Mark-PhaseComplete -Config $Config -PhaseName 'ad-promoted'
        }
        'PostPromotion' {
            Assert-DomainControllerState -Config $Config
            Rename-DefaultSiteIfConfigured -Config $Config -Context $Context
            Configure-DnsForwardersFromConfig -Config $Config -Context $Context
            Configure-ReverseLookupZonesFromConfig -Config $Config -Context $Context
            Configure-DnsScavengingFromConfig -Config $Config -Context $Context
            Authorize-DhcpServerInAd -Config $Config -Context $Context
            Configure-DhcpServerSettings -Config $Config -Context $Context
            Configure-DhcpScopesFromConfig -Config $Config -Context $Context
            Configure-DhcpScopeOptionsFromConfig -Config $Config -Context $Context
            Configure-DhcpReservationsFromConfig -Config $Config -Context $Context
            Configure-PdcAuthoritativeTime -Config $Config -Context $Context
            New-OrganizationalUnitsFromConfig -Config $Config -Context $Context
            New-GroupsFromConfig -Config $Config -Context $Context
            Add-GroupMembersFromConfig -Config $Config -Context $Context
            New-ServiceAccountsFromConfig -Config $Config -Context $Context
            New-GposFromConfig -Config $Config -Context $Context
            Link-GposFromConfig -Config $Config -Context $Context
            Apply-StigAlignedSettingsFromConfig -Config $Config -Context $Context
            Configure-DefenderFromConfig -Config $Config -Context $Context
            Configure-FirewallProfilesFromConfig -Config $Config -Context $Context
            Enable-BuiltInFirewallRuleGroupsFromConfig -Config $Config -Context $Context
            Create-CustomFirewallRulesFromConfig -Config $Config -Context $Context
            Configure-WindowsEventCollector -Config $Config -Context $Context
            Configure-WindowsEventSource -Config $Config -Context $Context
            Import-EventSubscriptionFromXml -Config $Config -Context $Context
            Install-WazuhAgentFromConfig -Config $Config -Context $Context
            Configure-WazuhAgentFromConfig -Config $Config -Context $Context
            Validate-PkiPlanFromConfig -Config $Config
            Install-AdcsRolesIfEnabled -Config $Config -Context $Context
            Configure-RootCaIfEnabled -Config $Config -Context $Context
            Configure-IssuingCaIfEnabled -Config $Config -Context $Context
            Write-CertificateWorkflowDocumentation -Config $Config
            Install-WsusIfEnabled -Config $Config -Context $Context
            Configure-WsusFromConfig -Config $Config -Context $Context
            Configure-ADBackupPlanArtifacts -Config $Config -Context $Context
            Configure-ScanCredentialSupport -Config $Config -Context $Context
            Write-VulnerabilityScanningRunbook -Config $Config
            Write-GitLabAdIntegrationArtifact -Config $Config -Context $Context
            Write-KeycloakAdFederationArtifact -Config $Config -Context $Context
            Write-YubiKeyPolicyArtifact -Config $Config -Context $Context
            Mark-PhaseComplete -Config $Config -PhaseName 'post-promotion-complete'
        }
        'Validate' {
            Invoke-ValidationSuite -Config $Config -Context $Context
            Assert-DnsRecordsResolve -Config $Config
            Assert-DnsForwarders -Config $Config
            Assert-DhcpConfiguration -Config $Config
            Assert-TimeConfiguration -Config $Config
            Assert-OrganizationalUnitsExist -Config $Config
            Assert-GroupsExist -Config $Config
            Assert-ServiceAccountsExist -Config $Config
            Assert-GpoLinks -Config $Config
            Assert-HardeningState -Config $Config
            Assert-DefenderState -Config $Config
            Assert-FirewallState -Config $Config
            Assert-EventForwardingState -Config $Config
            Assert-WazuhAgentState -Config $Config
            Assert-PkiState -Config $Config
            Assert-WsusState -Config $Config
            Assert-BackupRecoveryReadiness -Config $Config
            Assert-VulnerabilityScanningReadiness -Config $Config
            Assert-IdentityIntegrationPrerequisites -Config $Config
            Mark-PhaseComplete -Config $Config -PhaseName 'validation-complete'
        }
    }
}

function Invoke-Project {
    [CmdletBinding()]
    param()

    if (-not (Test-IsAdministrator)) {
        throw 'Administrator privileges are required.'
    }

    $config = Import-ProjectConfig -ConfigPath $ConfigPath
    Assert-ProjectConfig -Config $config
    Add-Member -InputObject $config -NotePropertyName '__configPath' -NotePropertyValue $ConfigPath -Force

    Initialize-ProjectLogging -Config $config
    Initialize-ProjectState -Config $config

    $context = @{
        PlanOnly        = [bool]$PlanOnly
        ValidateOnly    = [bool]$ValidateOnly
        WhatIfPreference = $WhatIfPreference
        PlanExecutable  = $true
        PlanIssues      = [System.Collections.Generic.List[string]]::new()
    }

    Write-ProjectInfo -Message 'Configuration imported and validated.'

    $resumeState = Get-ProjectState -Config $config
    $selectedPhases = @()
    if ($ValidateOnly) {
        $selectedPhases = @('Validate')
    }
    elseif ($Phase) {
        $selectedPhases = @($Phase)
    }
    elseif ($resumeState.currentPhase) {
        $selectedPhases = @($resumeState.currentPhase, 'PostPromotion', 'Validate')
    }
    else {
        $selectedPhases = @('Preflight', 'PromoteDomainController', 'PostPromotion', 'Validate')
    }

    foreach ($phaseName in $selectedPhases) {
        Set-ProjectState -Config $config -StateName 'current-phase' -Data @{ currentPhase = $phaseName; updatedAt = (Get-Date).ToString('o') }
        Write-OperationLog -Config $config -Phase $phaseName -Component 'Main' -Operation 'PhaseStart' -Target $phaseName -InputValues @{} -Result 'Started'
        Invoke-ProjectPhase -PhaseName $phaseName -Config $config -Context $context
        Write-OperationLog -Config $config -Phase $phaseName -Component 'Main' -Operation 'PhaseEnd' -Target $phaseName -InputValues @{} -Result 'Completed'
    }

    Write-HumanReadableSummary -Config $config
    Write-JsonSummary -Config $config
    Write-FinalReport -Config $config -Success $true -FailedChecks @('None')

    if ($PlanOnly -and -not $context.PlanExecutable) {
        throw "PlanOnly completed with non-executable plan. Issues: $($context.PlanIssues -join '; ')"
    }

    Unregister-ResumeScheduledTask -Config $config
}

try {
    Invoke-Project
}
catch {
    try {
        if ($config) {
            Set-ProjectState -Config $config -StateName 'failure' -Data @{
                timestamp = (Get-Date).ToString('o')
                message   = $_.Exception.Message
            }
            Write-ProjectError -Message $_.Exception.Message
            Write-FinalReport -Config $config -Success $false -FailedChecks @($_.Exception.Message)
        }
    }
    catch {
    }
    throw
}
