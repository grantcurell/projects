. "$PSScriptRoot\..\..\lib\Config.ps1"

Describe 'DNS no-defaults guardrails' {
    It 'fails if DNS forwarders include DC IP and not explicitly allowed' {
        $config = [pscustomobject]@{
            schemaVersion = 1
            execution = @{ statePath='C:\S'; logPath='C:\L'; transcriptPath='C:\L\t.log'; jsonLogPath='C:\L\j.log'; evidencePath='C:\E'; resumeScheduledTaskName='Task' }
            proxmoxGuest = @{ enabled = $false }
            network = @{ enabled = $true; interfaceAlias='E'; computerName='dc'; timeZone='UTC'; ipv4=@{address='10.0.0.10';prefixLength=24}; allowMultipleDefaultGateways=$false }
            roles = @{ activeDirectoryDomainServices=@{enabled=$false}; dns=@{enabled=$false}; dhcp=@{enabled=$false}; wsus=@{enabled=$false}; pki=@{enabled=$false} }
            activeDirectory = @{ enabled = $false }
            dns = @{ enabled = $true; allowForwardersPointingToSelf = $false; forwarders = @('10.0.0.10') }
            dhcp = @{ enabled = $false }
            time = @{ enabled = $false }
            organizationalUnits = @{ enabled = $false }
            groups = @{ enabled = $false }
            serviceAccounts = @{ enabled = $false }
            gpo = @{ enabled = $false }
            hardening = @{ enabled = $false }
            defender = @{ enabled = $false }
            firewall = @{ enabled = $false }
            eventForwarding = @{ enabled = $false }
            wazuh = @{ enabled = $false }
            pki = @{ enabled = $false }
            wsus = @{ enabled = $false }
            backupRecovery = @{ enabled = $false }
            vulnerabilityScanning = @{ enabled = $false }
            identityIntegrations = @{ enabled = $false }
            validation = @{ enabled = $false }
            reporting = @{ enabled = $false }
        }
        { Assert-ProjectConfig -Config $config } | Should Throw
    }
}
