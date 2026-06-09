. "$PSScriptRoot\..\..\lib\Preconditions.ps1"

Describe 'Preconditions' {
    It 'returns pending reboot object shape' {
        $result = Test-PendingReboot
        (($result.PSObject.Properties.Name) -join ',') | Should Match 'IsPending'
        (($result.PSObject.Properties.Name) -join ',') | Should Match 'Details'
    }
}
