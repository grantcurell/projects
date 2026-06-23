. "$PSScriptRoot\..\..\lib\Config.ps1"

Describe 'DHCP validation' {
    It 'fails when scope required fields are missing' {
        $config = [pscustomobject]@{
            schemaVersion = 1
            execution = @{ statePath='C:\S'; logPath='C:\L'; transcriptPath='C:\L\t.log'; jsonLogPath='C:\L\j.log'; evidencePath='C:\E'; resumeScheduledTaskName='Task' }
            proxmoxGuest = @{ enabled = $false }
            network = @{ enabled = $false }
            roles = @{ activeDirectoryDomainServices=@{enabled=$false}; dns=@{enabled=$false}; dhcp=@{enabled=$false}; wsus=@{enabled=$false}; pki=@{enabled=$false} }
            activeDirectory = @{ enabled = $false }
            dns = @{ enabled = $false }
            dhcp = @{ enabled = $true; reconcileExisting=$false; scopes = @([pscustomobject]@{ name='bad'; scopeId='10.10.0.0' }) }
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
