Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Write-HumanReadableSummary {
    <#
    .SYNOPSIS
    Writes human-readable validation summary.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    if (-not $Config.reporting.enabled -or -not $Config.reporting.writeHumanReadableSummary) { return }
    $domain = $Config.activeDirectory.domainName
    $pdc = ''
    try {
        $ad = Get-ADDomain -ErrorAction Stop
        $domain = $ad.DNSRoot
        $pdc = $ad.PDCEmulator
    }
    catch {
    }
    $content = @"
WindowsIdentityServicesDeployer summary
Host: $env:COMPUTERNAME
Domain: $domain
PDC Emulator: $pdc
Evidence path: $($Config.execution.evidencePath)
"@
    Set-Content -LiteralPath $Config.reporting.summaryPath -Value $content -Encoding UTF8
}

function Write-JsonSummary {
    <#
    .SYNOPSIS
    Writes JSON summary artifact.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    if (-not $Config.reporting.enabled -or -not $Config.reporting.writeJsonSummary) { return }
    $domain = $Config.activeDirectory.domainName
    try { $domain = (Get-ADDomain -ErrorAction Stop).DNSRoot } catch {}
    $summary = [ordered]@{
        hostname = $env:COMPUTERNAME
        domain   = $domain
        written  = (Get-Date).ToString('o')
    }
    $summary | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $Config.reporting.jsonSummaryPath -Encoding UTF8
}

function Write-FinalReport {
    <#
    .SYNOPSIS
    Writes final report JSON artifact.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][pscustomobject]$Config,
        [Parameter(Mandatory = $true)][bool]$Success,
        [Parameter(Mandatory = $true)][string[]]$FailedChecks
    )
    $forestModeRuntime = $Config.activeDirectory.forestMode
    $domainModeRuntime = $Config.activeDirectory.domainMode
    $domainRuntime = $Config.activeDirectory.domainName
    $pdcEmulatorRuntime = $null
    try {
        $forest = Get-ADForest -ErrorAction Stop
        $domain = Get-ADDomain -ErrorAction Stop
        $forestModeRuntime = $forest.ForestMode.ToString()
        $domainModeRuntime = $domain.DomainMode.ToString()
        $domainRuntime = $domain.DNSRoot
        $pdcEmulatorRuntime = $domain.PDCEmulator
    }
    catch {
    }
    $hardeningActions = @()
    if ($Config.hardening.enabled) {
        $hardeningActions += 'eventLogSizes'
        if ($Config.hardening.requireSmbSigning) { $hardeningActions += 'smbSigning' }
        if ($Config.hardening.disableSmbv1) { $hardeningActions += 'disableSmbv1' }
        if ($Config.hardening.ldapSigning.requireSigning) { $hardeningActions += 'ldapSigning' }
        if ($Config.hardening.channelBinding.enabled) { $hardeningActions += 'channelBinding' }
    }
    $installedRoles = @()
    foreach ($roleName in @('activeDirectoryDomainServices','dns','dhcp','wsus','pki')) {
        $roleConfig = $Config.roles.$roleName
        $isEnabled = $false
        if ($roleConfig -is [System.Collections.IDictionary]) {
            $isEnabled = [bool]$roleConfig['enabled']
        }
        else {
            $isEnabled = [bool]$roleConfig.enabled
        }
        if ($isEnabled) { $installedRoles += $roleName }
    }

    $report = [ordered]@{
        success                     = $Success
        hostname                    = $env:COMPUTERNAME
        domain                      = $domainRuntime
        domainController            = (Get-WindowsFeature -Name AD-Domain-Services -ErrorAction SilentlyContinue).Installed
        forestMode                  = $forestModeRuntime
        domainMode                  = $domainModeRuntime
        installedRoles              = $installedRoles
        dnsForwarders               = @($Config.dns.forwarders)
        reverseZones                = @($Config.dns.reverseLookupZones)
        dhcpScopes                  = @($Config.dhcp.scopes)
        pdcEmulator                 = $pdcEmulatorRuntime
        ntpSource                   = @($Config.time.externalNtpServers)
        ouCount                     = @($Config.organizationalUnits.structure).Count
        groupCount                  = @($Config.groups.items).Count
        serviceAccountCount         = @($Config.serviceAccounts.accounts).Count
        gpoCount                    = @($Config.gpo.gpos).Count
        hardeningActionsApplied     = $hardeningActions
        defenderStatus              = $Config.defender.enabled
        firewallStatus              = $Config.firewall.enabled
        eventForwardingStatus       = $Config.eventForwarding.enabled
        wazuhStatus                 = $Config.wazuh.enabled
        pkiStatus                   = $Config.pki.enabled
        wsusStatus                  = $Config.wsus.enabled
        backupRecoveryReadiness     = $Config.backupRecovery.enabled
        vulnerabilityScanReadiness  = $Config.vulnerabilityScanning.enabled
        identityIntegrationArtifacts = @(
            $Config.identityIntegrations.gitlab.outputConfigSnippetPath,
            $Config.identityIntegrations.keycloak.outputConfigSummaryPath,
            $Config.identityIntegrations.yubiKey.notesPath
        )
        failedChecks                = $FailedChecks
        evidenceFilePaths           = $Config.validation.evidenceFiles
    }
    $report | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $Config.validation.evidenceFiles.finalReport -Encoding UTF8
}
