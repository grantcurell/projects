param(
    [Parameter(Mandatory = $true)]
    [string]$DriverUrl,

    [Parameter(Mandatory = $true)]
    [string]$DriversRoot,

    [Parameter(Mandatory = $true)]
    [string]$Filename,

    [Parameter(Mandatory = $true)]
    [string]$ExtractSubdir,

    [Parameter(Mandatory = $true)]
    [string]$DriverVersion
)

$ErrorActionPreference = "Stop"

$IsAdmin = ([Security.Principal.WindowsPrincipal] `
    [Security.Principal.WindowsIdentity]::GetCurrent()
).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $IsAdmin) {
    throw "prepare-winpe-storage-driver.ps1 must run as Administrator."
}

$DriverExe = Join-Path $DriversRoot $Filename
$ExtractDir = Join-Path $DriversRoot $ExtractSubdir
$MarkerFile = Join-Path $ExtractDir ".driver-prepared"

New-Item -ItemType Directory -Force -Path $DriversRoot, $ExtractDir | Out-Null

$needsDownload = -not (Test-Path $DriverExe)
$needsExtract = -not (Test-Path $MarkerFile)

if (Test-Path $MarkerFile) {
    $marker = Get-Content -Path $MarkerFile -Raw
    if ($marker.Trim() -ne $DriverVersion) {
        Write-Host "Driver version changed ($marker -> $DriverVersion). Re-extracting."
        $needsExtract = $true
    }
}

if ($needsDownload) {
    throw "Driver package not found at $DriverExe. Upload it to the WinPE builder before running prepare-winpe-storage-driver.ps1."
} else {
    Write-Host "Driver package already present at $DriverExe"
}

if ($needsExtract -or $needsDownload) {
    Write-Host "Extracting Dell driver package to $ExtractDir"
    if (Test-Path $ExtractDir) {
        Get-ChildItem -Path $ExtractDir -Force | Where-Object { $_.Name -ne '.' -and $_.Name -ne '..' } | Remove-Item -Recurse -Force
    }

    $extractProcess = Start-Process -FilePath $DriverExe -ArgumentList @("/s", "/e=$ExtractDir") -Wait -PassThru
    if ($extractProcess.ExitCode -ne 0) {
        throw "Driver extraction failed with exit code $($extractProcess.ExitCode)."
    }

    $InfFiles = Get-ChildItem -Path $ExtractDir -Recurse -Filter *.inf -ErrorAction SilentlyContinue
    if (-not $InfFiles) {
        throw "No .inf files found after extraction under $ExtractDir"
    }

    Write-Host "Found $($InfFiles.Count) driver .inf file(s) under $ExtractDir"
    Set-Content -Path $MarkerFile -Value $DriverVersion -Encoding Ascii
} else {
    Write-Host "Storage driver already prepared at $ExtractDir (version $DriverVersion)"
}

Write-Output "OK"
