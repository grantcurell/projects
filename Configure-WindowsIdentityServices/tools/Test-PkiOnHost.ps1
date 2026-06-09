Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$root = Split-Path $PSScriptRoot -Parent

. (Join-Path $root 'lib\Config.ps1')
. (Join-Path $root 'lib\Pki.ps1')

$cfg = Import-ProjectConfig -ConfigPath (Join-Path $root 'config.yaml')
Assert-ProjectConfig -Config $cfg

$ctx = @{ PlanOnly = $false }

Validate-PkiPlanFromConfig -Config $cfg
Install-AdcsRolesIfEnabled -Config $cfg -Context $ctx
Configure-RootCaIfEnabled -Config $cfg -Context $ctx
Configure-IssuingCaIfEnabled -Config $cfg -Context $ctx
Write-CertificateWorkflowDocumentation -Config $cfg
Assert-PkiState -Config $cfg

Write-Output 'PKI_FUNCTIONS_COMPLETED'
