. "$PSScriptRoot\..\..\lib\Config.ps1"

function New-BaseConfig {
    return [pscustomobject]@{
        schemaVersion = 1
        execution = @{
            statePath = 'C:\State'
            logPath = 'C:\Logs'
            transcriptPath = 'C:\Logs\t.log'
            jsonLogPath = 'C:\Logs\o.jsonl'
            evidencePath = 'C:\Evidence'
            resumeScheduledTaskName = 'Task'
        }
        proxmoxGuest = @{ enabled = $false }
        network = @{ enabled = $true; interfaceAlias = 'Eth0'; computerName = 'dc1'; timeZone = 'UTC'; ipv4 = @{ address = '10.0.0.10'; prefixLength = 24 } ; allowMultipleDefaultGateways = $false }
        roles = @{ activeDirectoryDomainServices = @{ enabled = $true }; dns = @{ enabled = $true }; dhcp = @{ enabled = $true }; wsus = @{ enabled = $false }; pki = @{ enabled = $false } }
        activeDirectory = @{ enabled = $true; domainName = 'example.com'; netbiosName = 'EXAMPLE'; allowSingleLabelDomain = $false; allowDotLocal = $false }
        dns = @{ enabled = $true; forwarders = @('1.1.1.1'); allowForwardersPointingToSelf = $true }
        dhcp = @{ enabled = $true; reconcileExisting = $false; scopes = @() }
        time = @{ enabled = $true; authoritativeForDomain = $true; externalNtpServers = @('time.example.net'); behaviorIfNotPdc = 'stop' }
        organizationalUnits = @{ enabled = $true; structure = @() }
        groups = @{ enabled = $true; items = @() }
        serviceAccounts = @{ enabled = $true; accounts = @() }
        gpo = @{ enabled = $true; allowModifyDefaultDomainPolicy = $true; gpos = @() }
        hardening = @{ enabled = $true }
        defender = @{ enabled = $true }
        firewall = @{ enabled = $true }
        eventForwarding = @{ enabled = $true }
        wazuh = @{ enabled = $false }
        pki = @{ enabled = $false }
        wsus = @{ enabled = $false }
        backupRecovery = @{ enabled = $true }
        vulnerabilityScanning = @{ enabled = $true }
        identityIntegrations = @{ enabled = $true }
        validation = @{ enabled = $true }
        reporting = @{ enabled = $true }
    }
}

Describe 'Config validation' {
    It 'fails when required top-level section is missing' {
        $config = New-BaseConfig
        $config.PSObject.Properties.Remove('network')
        { Assert-ProjectConfig -Config $config } | Should Throw
    }

    It 'fails on single-label domain when not allowed' {
        $config = New-BaseConfig
        $config.activeDirectory.domainName = 'lab'
        { Assert-ProjectConfig -Config $config } | Should Throw
    }

    It 'fails for invalid NetBIOS length' {
        $config = New-BaseConfig
        $config.activeDirectory.netbiosName = 'THISNAMEISWAYTOOLONG'
        { Assert-ProjectConfig -Config $config } | Should Throw
    }

    It 'fails when enabled feature has missing required value' {
        $config = New-BaseConfig
        $config.execution.statePath = $null
        { Assert-ProjectConfig -Config $config } | Should Throw
    }

    It 'fails on duplicate group names' {
        $config = New-BaseConfig
        $config.groups.items = @(
            [pscustomobject]@{ name = 'GG-1' },
            [pscustomobject]@{ name = 'GG-1' }
        )
        { Assert-ProjectConfig -Config $config } | Should Throw
    }

    It 'fails on duplicate service account samAccountName values' {
        $config = New-BaseConfig
        $config.serviceAccounts.accounts = @(
            [pscustomobject]@{ samAccountName = 'svc-a' },
            [pscustomobject]@{ samAccountName = 'svc-a' }
        )
        { Assert-ProjectConfig -Config $config } | Should Throw
    }
}
