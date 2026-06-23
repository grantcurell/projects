Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Write-ValidationEvidence {
    <#
    .SYNOPSIS
    Writes command output evidence file.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][string]$Path, [Parameter(Mandatory = $true)][string]$Content)
    $dir = Split-Path $Path -Parent
    if (-not (Test-Path -LiteralPath $dir)) { New-Item -Path $dir -ItemType Directory -Force | Out-Null }
    Set-Content -LiteralPath $Path -Value $Content -Encoding UTF8
}

function Invoke-DcDiag { [CmdletBinding()] param([pscustomobject]$Config) if ($Config.validation.commands.dcdiag) { Write-ValidationEvidence -Path $Config.validation.evidenceFiles.dcdiag -Content (& dcdiag | Out-String) } }
function Invoke-DcDiagDns { [CmdletBinding()] param([pscustomobject]$Config) if ($Config.validation.commands.dcdiagDns) { Write-ValidationEvidence -Path $Config.validation.evidenceFiles.dcdiagDns -Content (& dcdiag /test:DNS | Out-String) } }
function Invoke-RepadminSummary { [CmdletBinding()] param([pscustomobject]$Config) if ($Config.validation.commands.repadminReplSummary) { Write-ValidationEvidence -Path $Config.validation.evidenceFiles.repadmin -Content (& repadmin /replsummary | Out-String) } }
function Invoke-NltestDsGetDc { [CmdletBinding()] param([pscustomobject]$Config) if ($Config.validation.commands.nltestDsGetDc) { & nltest /dsgetdc:$Config.activeDirectory.domainName | Out-Null } }
function Test-DnsResolution {
    [CmdletBinding()]
    param([pscustomobject]$Config)
    if ($Config.validation.commands.resolveDomainName) { Resolve-DnsName $Config.activeDirectory.domainName | Out-Null }
    if ($Config.validation.commands.resolveLdapSrvRecord) { Resolve-DnsName "_ldap._tcp.dc._msdcs.$($Config.activeDirectory.domainName)" -Type SRV | Out-Null }
}
function Test-DhcpScopes { [CmdletBinding()] param([pscustomobject]$Config) if ($Config.validation.commands.dhcpServerv4Scopes) { Get-DhcpServerv4Scope -ErrorAction Stop | Out-Null } }
function Test-GpoReports { [CmdletBinding()] param([pscustomobject]$Config) if ($Config.validation.commands.gpoReport) { Generate-GpoReports -Config $Config } }
function Test-FirewallProfiles { [CmdletBinding()] param([pscustomobject]$Config) if ($Config.validation.commands.firewallProfile) { Get-NetFirewallProfile | Out-Null } }
function Test-DefenderStatus { [CmdletBinding()] param([pscustomobject]$Config) if ($Config.validation.commands.defenderStatus) { Get-MpComputerStatus | Out-Null } }
function Test-EventForwardingStatus { [CmdletBinding()] param([pscustomobject]$Config) if ($Config.validation.commands.eventForwardingStatus) { Assert-EventForwardingState -Config $Config } }
function Test-TimeStatus {
    [CmdletBinding()]
    param([pscustomobject]$Config)
    if ($Config.validation.commands.w32tmStatus) {
        Write-ValidationEvidence -Path (Join-Path $Config.execution.evidencePath 'w32tm-status.txt') -Content (& w32tm /query /status | Out-String)
    }
    if ($Config.validation.commands.w32tmConfiguration) {
        Write-ValidationEvidence -Path (Join-Path $Config.execution.evidencePath 'w32tm-configuration.txt') -Content (& w32tm /query /configuration | Out-String)
    }
}
function Test-WazuhStatus { [CmdletBinding()] param([pscustomobject]$Config) if ($Config.wazuh.enabled) { Assert-WazuhAgentState -Config $Config } }
function Test-WsusStatus { [CmdletBinding()] param([pscustomobject]$Config) if ($Config.wsus.enabled) { Assert-WsusState -Config $Config } }
function Test-PkiStatus { [CmdletBinding()] param([pscustomobject]$Config) if ($Config.pki.enabled) { Assert-PkiState -Config $Config } }

function Invoke-ValidationSuite {
    <#
    .SYNOPSIS
    Runs validation suite and writes evidence.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.validation.enabled) { return }
    Invoke-DcDiag -Config $Config
    Invoke-DcDiagDns -Config $Config
    Invoke-RepadminSummary -Config $Config
    Invoke-NltestDsGetDc -Config $Config
    Test-DnsResolution -Config $Config
    Test-DhcpScopes -Config $Config
    Test-GpoReports -Config $Config
    Test-FirewallProfiles -Config $Config
    Test-DefenderStatus -Config $Config
    Test-EventForwardingStatus -Config $Config
    Test-TimeStatus -Config $Config
    Test-WazuhStatus -Config $Config
    Test-WsusStatus -Config $Config
    Test-PkiStatus -Config $Config
}
