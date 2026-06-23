Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Validate-PkiPlanFromConfig {
    <#
    .SYNOPSIS
    Validates PKI topology and safety guardrails.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    if (-not $Config.pki.enabled) { return }
    if ($Config.pki.mode -ne 'offline-root-and-issuing-ca') {
        throw "Unsupported PKI mode: $($Config.pki.mode)"
    }
    if ($Config.pki.rootCa.enabled -and $Config.pki.issuingCa.enabled -and -not $Config.pki.allowRootAndIssuingOnSameServer) {
        throw 'Root and issuing CA on same host requires pki.allowRootAndIssuingOnSameServer=true.'
    }
    foreach ($sub in @('rootCa', 'issuingCa')) {
        if ($Config.pki.$sub.enabled) {
            foreach ($prop in @('caCommonName','validityYears','keyLength','hashAlgorithm','cryptoProvider')) {
                if ($null -eq $Config.pki.$sub.$prop -or [string]::IsNullOrWhiteSpace([string]$Config.pki.$sub.$prop)) {
                    throw "pki.$sub.$prop is required when pki.$sub.enabled is true."
                }
            }
        }
    }
    if ($Config.pki.certificateWorkflow.templates.Count -eq 0 -and $Config.pki.enabled) {
        throw 'pki.certificateWorkflow.templates must be listed when pki.enabled is true.'
    }
}

function Install-AdcsRolesIfEnabled {
    <#
    .SYNOPSIS
    Installs AD CS role when PKI is enabled.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.pki.enabled) { return }
    if ($Context.PlanOnly) { return }
    Install-WindowsFeature -Name ADCS-Cert-Authority -IncludeManagementTools | Out-Null
}

function Configure-RootCaIfEnabled {
    <#
    .SYNOPSIS
    Configures root CA when explicitly enabled.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.pki.enabled -or -not $Config.pki.rootCa.enabled) { return }
    if ($Context.PlanOnly) { return }
    $svc = Get-Service -Name CertSvc -ErrorAction SilentlyContinue
    if ($svc -and $svc.Status -eq 'Running') { return }
    try {
        Install-AdcsCertificationAuthority `
            -CAType StandaloneRootCA `
            -CACommonName $Config.pki.rootCa.caCommonName `
            -KeyLength ([int]$Config.pki.rootCa.keyLength) `
            -HashAlgorithmName $Config.pki.rootCa.hashAlgorithm `
            -CryptoProviderName $Config.pki.rootCa.cryptoProvider `
            -ValidityPeriod Years `
            -ValidityPeriodUnits ([int]$Config.pki.rootCa.validityYears) `
            -Force
    }
    catch {
        if ($_.Exception.Message -like '*already installed*' -or $_.Exception.Message -like '*private key*already exists*') {
            Set-Service -Name CertSvc -StartupType Automatic -ErrorAction SilentlyContinue
            Start-Service -Name CertSvc -ErrorAction SilentlyContinue
            return
        }
        throw
    }
}

function Configure-IssuingCaIfEnabled {
    <#
    .SYNOPSIS
    Configures issuing CA when explicitly enabled.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config, [Parameter(Mandatory = $true)][hashtable]$Context)
    if (-not $Config.pki.enabled -or -not $Config.pki.issuingCa.enabled) { return }
    if (Get-Service -Name CertSvc -ErrorAction SilentlyContinue) {
        return
    }
    if ($Context.PlanOnly) { return }
    Install-AdcsCertificationAuthority `
        -CAType EnterpriseSubordinateCA `
        -CACommonName $Config.pki.issuingCa.caCommonName `
        -KeyLength ([int]$Config.pki.issuingCa.keyLength) `
        -HashAlgorithmName $Config.pki.issuingCa.hashAlgorithm `
        -CryptoProviderName $Config.pki.issuingCa.cryptoProvider `
        -ValidityPeriod Years `
        -ValidityPeriodUnits ([int]$Config.pki.issuingCa.validityYears) `
        -Force
}

function Write-CertificateWorkflowDocumentation {
    <#
    .SYNOPSIS
    Writes certificate workflow artifact from config.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    if (-not $Config.pki.enabled) { return }
    $rootDir = [string]$Config.pki.certificateWorkflow.requestDirectory
    $issuedDir = [string]$Config.pki.certificateWorkflow.issuedDirectory
    if ([string]::IsNullOrWhiteSpace($rootDir) -or [string]::IsNullOrWhiteSpace($issuedDir)) {
        throw 'pki.certificateWorkflow.requestDirectory and issuedDirectory are required when pki.enabled is true.'
    }
    foreach ($dir in @($rootDir, $issuedDir)) {
        if (-not (Test-Path -LiteralPath $dir)) { New-Item -Path $dir -ItemType Directory -Force | Out-Null }
    }
    $docPath = Join-Path $issuedDir 'certificate-workflow.txt'
    $content = @"
PKI Workflow
Request directory: $rootDir
Issued directory: $issuedDir
Renewal warning days: $($Config.pki.certificateWorkflow.renewalWarningDays)
Templates:
$(@($Config.pki.certificateWorkflow.templates) -join [Environment]::NewLine)
"@
    Set-Content -LiteralPath $docPath -Value $content -Encoding UTF8
}

function Assert-PkiState {
    <#
    .SYNOPSIS
    Validates PKI state.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][pscustomobject]$Config)
    if (-not $Config.pki.enabled) { return }
    if ($Config.pki.rootCa.enabled -or $Config.pki.issuingCa.enabled) {
        $svc = Get-Service -Name CertSvc -ErrorAction SilentlyContinue
        if (-not $svc) {
            throw 'Certificate Services service (CertSvc) is not present.'
        }
    }
}
