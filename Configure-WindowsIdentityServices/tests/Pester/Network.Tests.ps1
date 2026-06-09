. "$PSScriptRoot\..\..\lib\Network.ps1"

Describe 'Network PlanOnly behavior' {
    It 'does not call mutating command in PlanOnly' {
        $config = [pscustomobject]@{
            network = [pscustomobject]@{
                enabled = $true
                interfaceAlias = 'Ethernet'
                ipv4 = [pscustomobject]@{
                    address = '10.0.0.10'
                    prefixLength = 24
                    defaultGateway = '10.0.0.1'
                }
            }
        }
        $context = @{ PlanOnly = $true }
        Mock New-NetIPAddress {}
        Mock Get-NetIPAddress { @() }
        Set-StaticIPv4FromConfig -Config $config -Context $context
        Assert-MockCalled New-NetIPAddress -Times 0 -Exactly
    }
}
