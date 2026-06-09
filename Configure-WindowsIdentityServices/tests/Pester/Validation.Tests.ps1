Describe 'No defaults in code patterns' {
    It 'contains no default network fallback strings' {
        $files = Get-ChildItem -Path "$PSScriptRoot\..\..\lib" -Filter '*.ps1' -Recurse
        $content = ($files | ForEach-Object { Get-Content -LiteralPath $_.FullName -Raw }) -join "`n"
        $content | Should Not Match 'pool\.ntp\.org'
        $content | Should Not Match 'lab\.local'
        $content | Should Not Match '192\.168\.1\.0/24'
    }
}
