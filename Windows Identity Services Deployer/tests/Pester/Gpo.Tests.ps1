. "$PSScriptRoot\..\..\lib\Config.ps1"

Describe 'GPO validation' {
    It 'fails on duplicate GPO names' {
        $config = [pscustomobject]@{
            schemaVersion = 1
            execution = @{ statePath='C:\S'; logPath='C:\L'; transcriptPath='C:\L\t.log'; jsonLogPath='C:\L\j.log'; evidencePath='C:\E'; resumeScheduledTaskName='Task' }
            proxmoxGuest = @{ enabled = $false }
            network = @{ enabled = $false }
            roles = @{ activeDirectoryDomainServices=@{enabled=$false}; dns=@{enabled=$false}; dhcp=@{enabled=$false}; wsus=@{enabled=$false}; pki=@{enabled=$false} }
            activeDirectory = @{ enabled = $false }
            dns = @{ enabled = $false }
            dhcp = @{ enabled = $false }
            time = @{ enabled = $false }
            organizationalUnits = @{ enabled = $false }
            groups = @{ enabled = $false }
            serviceAccounts = @{ enabled = $false }
            gpo = @{ enabled = $true; allowModifyDefaultDomainPolicy=$true; gpos = @(
                [pscustomobject]@{ name='GPO-A'; linkOrder=1 },
                [pscustomobject]@{ name='GPO-A'; linkOrder=2 }
            ) }
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
