. "$PSScriptRoot\..\..\lib\ActiveDirectory.ps1"

Describe 'Active Directory helper' {
    It 'converts domain to DN' {
        Get-DomainDistinguishedNameFromDomainName -DomainName 'lab.example.com' | Should Be 'DC=lab,DC=example,DC=com'
    }
}
