$ErrorActionPreference = "Stop"

$Server = "{{ deployer.network.server_ip }}"
$CaptureShare = "\\$Server\capture"
$QualifiedUser = "$Server\{{ deployer.samba.username }}"
$PlainUser = "{{ deployer.samba.username }}"
$Password = "{{ deployer.samba.password }}"
$CaptureName = "{{ windows.goldimage.name }}"

$StagingLabel = "{{ windows.capture.staging_label }}"
$StagingDrive = "{{ windows.capture.staging_drive_letter }}"
$StagingMinBytes = [Int64]{{ windows.capture.staging_min_size_bytes }}
$DismCompress = "{{ windows.capture.dism_compress }}"
$UseDismVerify = "{{ windows.capture.dism_verify }}" -ieq "true"
$MinWimBytes = [Int64]{{ deployer.capture.min_wim_size_bytes }}

$StageRoot = "$StagingDrive`:\capture"
$ScratchDir = "$StagingDrive`:\scratch"
$LogsDir = "$StagingDrive`:\logs"
$LocalWim = "$StageRoot\deploy.wim"
$LocalCaptureLog = "$LogsDir\capture.log"
$DismLog = "$LogsDir\dism-capture.log"
$RoboLog = "$LogsDir\robocopy-deploy-wim.log"
$WimScript = "X:\Deploy\WimScript.ini"
$RemoteWim = "Z:\deploy.wim"
$RemoteCaptureLog = "Z:\capture.log"
$RemoteDismLog = "Z:\dism.log"
$RemoteRoboLog = "Z:\robocopy-deploy-wim.log"
$RemoteCaptureMarker = "Z:\capture-success.json"
$RemotePublishMarker = "Z:\{{ deployer.capture.success_marker_file }}"
$RemoteCaptureMarkerTmp = "$RemoteCaptureMarker.tmp"
$RemotePublishMarkerTmp = "$RemotePublishMarker.tmp"

function Write-Step {
    param([string]$Message)
    Write-Host ""
    Write-Host "==== $Message ===="
}

function Write-Log {
    param([string]$Message)
    $line = "$(Get-Date -Format s) $Message"
    Write-Host $line
    if ($LocalCaptureLog -and (Test-Path (Split-Path -Parent $LocalCaptureLog))) {
        Add-Content -Path $LocalCaptureLog -Value $line
    }
    if (Test-Path "Z:\") {
        try {
            Add-Content -Path $RemoteCaptureLog -Value $line -ErrorAction Stop
        } catch {
            Write-Host "WARN: Failed writing remote capture log line: $($_.Exception.Message)"
        }
    }
}

function Sync-LogFile {
    param(
        [string]$SourcePath,
        [string]$DestinationPath
    )
    if (-not (Test-Path $SourcePath)) {
        return
    }
    if (-not (Test-Path "Z:\")) {
        return
    }
    try {
        Copy-Item -Path $SourcePath -Destination $DestinationPath -Force -ErrorAction Stop
    } catch {
        Write-Host "WARN: Failed syncing log $SourcePath -> $DestinationPath: $($_.Exception.Message)"
    }
}

try {
    Write-Step "Initializing WinPE network"
    wpeinit
    Start-Sleep -Seconds 10

    Write-Step "Waiting for network readiness"
    $networkReady = $false
    for ($attempt = 1; $attempt -le 60; $attempt++) {
        ping -n 1 $Server | Out-Null
        if ($LASTEXITCODE -eq 0) {
            $networkReady = $true
            break
        }
        Write-Log "Network not ready yet ($attempt/60)"
        Start-Sleep -Seconds 2
    }

    if (-not $networkReady) {
        throw "Network never became ready for $Server"
    }

    Write-Step "Connecting SMB share"
    net use * /delete /y | Out-Null
    net use Z: /delete /y | Out-Null
    $mapped = $false
    for ($attempt = 1; $attempt -le 30 -and -not $mapped; $attempt++) {
        net use Z: /delete /y | Out-Null
        Write-Log "SMB map attempt $attempt/30 using qualified account"
        net use Z: $CaptureShare /user:$QualifiedUser $Password /persistent:no | Out-Null
        if ($LASTEXITCODE -eq 0) {
            $mapped = $true
            break
        }

        Write-Log "Qualified mapping failed, trying plain username"
        net use Z: $CaptureShare /user:$PlainUser $Password /persistent:no | Out-Null
        if ($LASTEXITCODE -eq 0) {
            $mapped = $true
            break
        }

        pushd $CaptureShare | Out-Null
        if ($LASTEXITCODE -eq 0) {
            popd | Out-Null
        }

        Start-Sleep -Seconds 2
    }

    if (-not $mapped) {
        throw "Failed to map $CaptureShare with explicit SMB credentials after retries"
    }

    $probeFile = "Z:\_write_test_$env:COMPUTERNAME.txt"
    "test" | Out-File -FilePath $probeFile -Encoding ascii -Force
    if (-not (Test-Path $probeFile)) {
        throw "SMB write probe failed on $CaptureShare"
    }
    Remove-Item -Path $probeFile -Force -ErrorAction SilentlyContinue

    Write-Step "Finding Windows volume"
    $volumes = Get-Volume | Where-Object {
        $_.DriveLetter -and
        $_.DriveLetter -notin @("X", "Z") -and
        (Test-Path "$($_.DriveLetter):\Windows\System32\Config\SYSTEM") -and
        (Test-Path "$($_.DriveLetter):\Windows\System32\ntoskrnl.exe")
    } | Sort-Object -Property Size -Descending

    if (-not $volumes) {
        throw "Could not find Windows installation volume"
    }

    $WindowsDrive = "$($volumes[0].DriveLetter):\"
    Write-Log "Windows volume detected at $WindowsDrive"

    Write-Step "Preparing dedicated local staging disk"
    $sourceLetter = $WindowsDrive.Substring(0, 1)
    $sourcePartition = Get-Partition -DriveLetter $sourceLetter -ErrorAction Stop
    $sourceDiskNumber = $sourcePartition.DiskNumber

    $candidateDisks = Get-Disk | Where-Object {
        $_.Number -ne $sourceDiskNumber -and
        $_.Size -ge $StagingMinBytes -and
        -not $_.IsReadOnly
    } | Sort-Object -Property Size -Descending

    if (-not $candidateDisks) {
        throw "No dedicated staging disk found. Attach a disk >= $StagingMinBytes bytes for capture staging."
    }

    $stageDisk = $candidateDisks[0]
    Write-Log "Using staging disk number $($stageDisk.Number) size $($stageDisk.Size)"

    Set-Disk -Number $stageDisk.Number -IsReadOnly $false -ErrorAction SilentlyContinue | Out-Null
    Clear-Disk -Number $stageDisk.Number -RemoveData -RemoveOEM -Confirm:$false
    Initialize-Disk -Number $stageDisk.Number -PartitionStyle GPT
    New-Partition -DiskNumber $stageDisk.Number -UseMaximumSize -DriveLetter $StagingDrive | Out-Null
    Format-Volume -DriveLetter $StagingDrive -FileSystem NTFS -NewFileSystemLabel $StagingLabel -Confirm:$false -Force | Out-Null

    New-Item -ItemType Directory -Path $StageRoot -Force | Out-Null
    New-Item -ItemType Directory -Path $ScratchDir -Force | Out-Null
    New-Item -ItemType Directory -Path $LogsDir -Force | Out-Null
    Set-Content -Path $LocalCaptureLog -Value "=== WinPE Capture Log ==="
    ipconfig /all | Out-File -FilePath $LocalCaptureLog -Append
    Sync-LogFile -SourcePath $LocalCaptureLog -DestinationPath $RemoteCaptureLog

    if (Test-Path $LocalWim) {
        Remove-Item -Path $LocalWim -Force
    }

    Write-Step "Capturing image"
    $verifyArg = ""
    if ($UseDismVerify) {
        $verifyArg = "/Verify"
    }
    $dismCmd = "dism /Capture-Image /ImageFile:`"$LocalWim`" /CaptureDir:`"$WindowsDrive`" /Name:`"$CaptureName`" /Description:`"Captured from Proxmox $CaptureName`" /Compress:$DismCompress /ConfigFile:`"$WimScript`" /ScratchDir:`"$ScratchDir`" /LogPath:`"$DismLog`" /LogLevel:4 /CheckIntegrity $verifyArg"
    Write-Log "Running: $dismCmd"
    cmd.exe /c $dismCmd
    Sync-LogFile -SourcePath $DismLog -DestinationPath $RemoteDismLog
    Sync-LogFile -SourcePath $LocalCaptureLog -DestinationPath $RemoteCaptureLog
    if ($LASTEXITCODE -ne 0) {
        if (Test-Path $DismLog) {
            Write-Host "DISM log tail ($DismLog):"
            Get-Content $DismLog -Tail 80 | ForEach-Object { Write-Host $_ }
        }
        throw "DISM capture failed with exit code $LASTEXITCODE"
    }

    $sizeBytes = (Get-Item $LocalWim).Length
    if ($sizeBytes -lt $MinWimBytes) {
        throw "Local WIM is below expected minimum size ($sizeBytes bytes)"
    }

    $localHash = (Get-FileHash -Path $LocalWim -Algorithm SHA256).Hash
    $captureSuccess = @{
        schema = 1
        phase = "local_capture"
        status = "success"
        image = "deploy.wim"
        bytes = $sizeBytes
        sha256 = $localHash
        dism_exit_code = 0
        robocopy_exit_code = -1
        completed_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    }
    $captureSuccess | ConvertTo-Json -Compress | Set-Content -Path $RemoteCaptureMarkerTmp -Encoding UTF8
    Move-Item -Path $RemoteCaptureMarkerTmp -Destination $RemoteCaptureMarker -Force
    Write-Log "Wrote capture-success marker."

    Write-Step "Publishing completed WIM to SMB"
    cmd.exe /c "robocopy `"$StageRoot`" `"Z:\`" deploy.wim /Z /J /R:5 /W:10 /NP /TEE /LOG+:`"$RoboLog`""
    $roboExit = $LASTEXITCODE
    Sync-LogFile -SourcePath $RoboLog -DestinationPath $RemoteRoboLog
    Sync-LogFile -SourcePath $DismLog -DestinationPath $RemoteDismLog
    Sync-LogFile -SourcePath $LocalCaptureLog -DestinationPath $RemoteCaptureLog
    if ($roboExit -ge 8) {
        throw "Robocopy failed with exit code $roboExit"
    }

    $remoteItem = Get-Item $RemoteWim -ErrorAction Stop
    if ($remoteItem.Length -ne $sizeBytes) {
        throw "Remote WIM size mismatch local=$sizeBytes remote=$($remoteItem.Length)"
    }
    $remoteHash = (Get-FileHash -Path $RemoteWim -Algorithm SHA256).Hash
    if ($remoteHash -ne $localHash) {
        throw "Remote WIM hash mismatch local=$localHash remote=$remoteHash"
    }

    dism /Get-WimInfo /WimFile:$RemoteWim | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Remote WIM validation failed with dism /Get-WimInfo"
    }

    $publishSuccess = @{
        schema = 1
        phase = "publish"
        status = "success"
        image = "deploy.wim"
        bytes = $sizeBytes
        sha256 = $remoteHash
        dism_exit_code = 0
        robocopy_exit_code = $roboExit
        completed_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    }
    $publishSuccess | ConvertTo-Json -Compress | Set-Content -Path $RemotePublishMarkerTmp -Encoding UTF8
    Move-Item -Path $RemotePublishMarkerTmp -Destination $RemotePublishMarker -Force
    Write-Log "Wrote publish-success marker."
    Write-Log "Capture complete. Marker publication finished before shutdown."
    Write-Step "Capture complete"
    wpeutil shutdown
} catch {
    Write-Log "FATAL: $($_.Exception.Message)"
    Sync-LogFile -SourcePath $DismLog -DestinationPath $RemoteDismLog
    Sync-LogFile -SourcePath $RoboLog -DestinationPath $RemoteRoboLog
    Sync-LogFile -SourcePath $LocalCaptureLog -DestinationPath $RemoteCaptureLog
    throw
} finally {
    Sync-LogFile -SourcePath $DismLog -DestinationPath $RemoteDismLog
    Sync-LogFile -SourcePath $RoboLog -DestinationPath $RemoteRoboLog
    Sync-LogFile -SourcePath $LocalCaptureLog -DestinationPath $RemoteCaptureLog
}
