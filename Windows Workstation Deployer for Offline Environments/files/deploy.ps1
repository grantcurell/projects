$ErrorActionPreference = "Stop"

$DeployServer = "{{ deployer.network.server_ip }}"
$DeployWimHttpUrl = "http://{{ deployer.network.server_ip }}/images/deploy.wim"
$DeploySharePath = "\\{{ deployer.network.server_ip }}\deploy"
$DeployShareFallbackPath = "\\{{ deployer.network.server_ip }}\capture"
$DeployShareUser = "{{ deployer.samba.username }}"
$DeploySharePassword = "{{ deployer.samba.password }}"
$StopAfterStage = "{{ windows.deploy.stop_after_stage | lower }}".Trim().ToLowerInvariant()
$PauseBetweenStages = [System.Convert]::ToBoolean("{{ windows.deploy.pause_between_stages | bool }}")
$AutoReboot = [System.Convert]::ToBoolean("{{ windows.deploy.auto_reboot | bool }}")
$TargetDiskNumber = {{ windows.deploy.target_disk_number }}
$MinimumTargetDiskSizeBytes = {{ windows.deploy.minimum_target_disk_size_bytes }}
$MappedDrive = "Z:"
$MappedWimPath = "$MappedDrive\images\deploy.wim"
$MappedWimFallbackPath = "$MappedDrive\deploy.wim"
$DiskpartScript = "X:\Deploy\diskpart-runtime.txt"
$TranscriptPath = "X:\Deploy\deploy.log"
$ValidStopStages = @("none", "network", "artifact", "disk", "partition", "apply", "bcdboot")

function Write-Step {
    param([string]$Message)
    Write-Host ""
    Write-Host "==== $Message ===="
}

function Run-Cmd {
    param([string]$Command, [string]$FailureMessage)
    cmd.exe /c $Command
    if ($LASTEXITCODE -ne 0) {
        throw "$FailureMessage (exit code $LASTEXITCODE)"
    }
}

function Run-ProcessWithHeartbeat {
    param(
        [string]$FilePath,
        [string[]]$ArgumentList,
        [string]$FailureMessage,
        [int]$HeartbeatSeconds = 30
    )

    $process = Start-Process -FilePath $FilePath -ArgumentList $ArgumentList -PassThru
    $start = Get-Date
    while (-not $process.HasExited) {
        Start-Sleep -Seconds $HeartbeatSeconds
        if (-not $process.HasExited) {
            $elapsed = [int]((Get-Date) - $start).TotalSeconds
            Write-Host "[$(Get-Date -Format o)] $FilePath still running ($elapsed s elapsed)"
        }
    }

    if ($process.ExitCode -ne 0) {
        throw "$FailureMessage (exit code $($process.ExitCode))"
    }
}

function Complete-Stage {
    param([string]$StageName)

    if ($PauseBetweenStages) {
        Read-Host "Stage '$StageName' complete. Press Enter to continue"
    }

    if ($StopAfterStage -eq $StageName) {
        Write-Host "Stopping after stage '$StageName' by configuration."
        exit 0
    }
}

function Disable-ConsoleQuickEditRuntime {
    try {
        Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public static class ConsoleNative {
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern IntPtr GetStdHandle(int nStdHandle);
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern bool GetConsoleMode(IntPtr hConsoleHandle, out uint lpMode);
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern bool SetConsoleMode(IntPtr hConsoleHandle, uint dwMode);
}
"@ -ErrorAction SilentlyContinue

        $STD_INPUT_HANDLE = -10
        $ENABLE_QUICK_EDIT_MODE = 0x0040
        $ENABLE_EXTENDED_FLAGS = 0x0080
        $inputHandle = [ConsoleNative]::GetStdHandle($STD_INPUT_HANDLE)
        if ($inputHandle -ne [IntPtr]::Zero) {
            [uint32]$mode = 0
            if ([ConsoleNative]::GetConsoleMode($inputHandle, [ref]$mode)) {
                $mode = ($mode -bor $ENABLE_EXTENDED_FLAGS) -band (-bnot $ENABLE_QUICK_EDIT_MODE)
                [void][ConsoleNative]::SetConsoleMode($inputHandle, $mode)
            }
        }
    } catch {
        Write-Host "Warning: could not disable QuickEdit on current console. $($_.Exception.Message)"
    }
}

function Map-DeployShare {
    cmd.exe /c "net use $MappedDrive /delete /y" | Out-Host

    $netUseArgs = @(
        "use",
        $MappedDrive,
        $DeploySharePath,
        $DeploySharePassword,
        "/user:$DeployShareUser",
        "/persistent:no"
    )
    & net.exe @netUseArgs
    if ($LASTEXITCODE -eq 0) {
        return $true
    }

    Write-Host "Credentialed deploy share map failed, trying capture guest share fallback."
    cmd.exe /c "net use $MappedDrive /delete /y" | Out-Host
    & net.exe use $MappedDrive $DeployShareFallbackPath /persistent:no
    if ($LASTEXITCODE -eq 0) {
        return $true
    }

    return $false
}

function Resolve-DeployWimPath {
    if (-not (Map-DeployShare)) {
        throw "SMB mapping to deploy share failed. Refusing to continue without a network deploy.wim path."
    }

    foreach ($candidate in @($MappedWimPath, $MappedWimFallbackPath)) {
        if (Test-Path $candidate) {
            Write-Host "Using deploy.wim from SMB path $candidate"
            return $candidate
        }
    }

    cmd.exe /c "net use $MappedDrive /delete /y" | Out-Host
    throw "SMB share mapped but deploy.wim was not found at expected paths ($MappedWimPath, $MappedWimFallbackPath)."
}

function Get-DeploymentTargetDisk {
    param(
        [Int64]$MinimumSizeBytes
    )

    Write-Host "Available disks:"
    Get-Disk | Format-Table Number, FriendlyName, SerialNumber, BusType, Size, PartitionStyle, IsBoot, IsSystem, IsReadOnly, OperationalStatus -AutoSize

    $candidateDisks = Get-Disk | Where-Object {
        -not $_.IsReadOnly -and
        $_.OperationalStatus -eq "Online" -and
        $_.Size -ge $MinimumSizeBytes -and
        $_.BusType -notin @("USB", "SD", "MMC")
    } | Sort-Object -Property Size -Descending

    if (-not $candidateDisks) {
        throw "No suitable deployment target disk found. Minimum size: $MinimumSizeBytes bytes."
    }

    $targetDisk = $candidateDisks[0]

    Write-Host "Selected largest deployment target disk:"
    $targetDisk | Format-List Number, FriendlyName, SerialNumber, BusType, Size, PartitionStyle, IsBoot, IsSystem, IsReadOnly, OperationalStatus

    if ($targetDisk.IsBoot -or $targetDisk.IsSystem) {
        throw "Refusing to deploy to disk $($targetDisk.Number) because it is marked Boot/System."
    }

    return $targetDisk
}

function Get-FreeDriveLetter {
    param([string[]]$Candidates)

    foreach ($candidate in $Candidates) {
        if (-not (Get-PSDrive -Name $candidate -ErrorAction SilentlyContinue)) {
            return $candidate
        }
    }

    throw "No free drive letter found from candidates: $($Candidates -join ', ')"
}

function Resolve-WindowsDriveLetter {
    param(
        [int]$DiskNumber,
        [string]$PreferredLetter = "W"
    )

    $preferredPartition = Get-Partition -DiskNumber $DiskNumber -ErrorAction Stop |
        Where-Object { $_.DriveLetter -eq $PreferredLetter } |
        Select-Object -First 1

    if ($null -ne $preferredPartition -and (Test-Path "$PreferredLetter`:\Windows\System32")) {
        return $PreferredLetter
    }

    $windowsPartition = Get-Partition -DiskNumber $DiskNumber -ErrorAction Stop |
        Where-Object {
            $_.DriveLetter -and
            (Test-Path "$($_.DriveLetter):\Windows\System32")
        } |
        Select-Object -First 1

    if ($null -eq $windowsPartition) {
        throw "Unable to locate deployed Windows volume on target disk $DiskNumber."
    }

    return [string]$windowsPartition.DriveLetter
}

function Resolve-EfiDriveLetter {
    param(
        [int]$DiskNumber,
        [string]$PreferredLetter = "S"
    )

    $efiPartition = Get-Partition -DiskNumber $DiskNumber -ErrorAction Stop |
        Where-Object { $_.GptType -eq "{C12A7328-F81F-11D2-BA4B-00A0C93EC93B}" } |
        Select-Object -First 1

    if ($null -eq $efiPartition) {
        throw "No EFI system partition found on target disk $DiskNumber."
    }

    $efiVolume = $efiPartition | Get-Volume -ErrorAction SilentlyContinue
    if ($null -ne $efiVolume -and $efiVolume.DriveLetter) {
        return [string]$efiVolume.DriveLetter
    }

    $assignLetter = $PreferredLetter
    if (Get-PSDrive -Name $assignLetter -ErrorAction SilentlyContinue) {
        $assignLetter = Get-FreeDriveLetter -Candidates @("S","R","T","U","V","P","Q","O","N")
    }

    $efiPartition | Set-Partition -NewDriveLetter $assignLetter -ErrorAction Stop | Out-Null
    return $assignLetter
}

if ($ValidStopStages -notcontains $StopAfterStage) {
    throw "Invalid stop_after_stage '$StopAfterStage'. Valid values: $($ValidStopStages -join ', ')"
}

Start-Transcript -Path $TranscriptPath -Force
try {
    # Prevent accidental console clicks from pausing output/execution in WinPE.
    cmd.exe /c "reg add HKCU\Console /v QuickEdit /t REG_DWORD /d 0 /f >nul 2>&1" | Out-Null
    Disable-ConsoleQuickEditRuntime

    Write-Step "Deployment stage 1: network check"
    ipconfig /all
    if (-not (Test-Connection -ComputerName $DeployServer -Count 3 -Quiet)) {
        throw "Cannot reach deploy server $DeployServer"
    }
    Complete-Stage -StageName "network"

    Write-Step "Deployment stage 2: deploy.wim reachability check (SMB)"
    if (-not (Map-DeployShare)) {
        throw "SMB mapping to deploy share failed."
    }

    Write-Host "SMB deploy share mapped as $MappedDrive"
    cmd.exe /c "net use $MappedDrive /delete /y" | Out-Host
    Complete-Stage -StageName "artifact"

    Write-Step "Deployment stage 3: target disk detection"
    $targetDisk = Get-DeploymentTargetDisk -MinimumSizeBytes $MinimumTargetDiskSizeBytes
    $TargetDiskNumber = $targetDisk.Number
    Write-Host "Deployment target disk number: $TargetDiskNumber"
    Write-Host "Deployment target disk size (bytes): $($targetDisk.Size)"
    Complete-Stage -StageName "disk"

    Write-Step "Deployment stage 4: disk partitioning"
    @"
select disk $TargetDiskNumber
clean
convert gpt

create partition efi size=260
format quick fs=fat32 label="System"
assign letter=S

create partition msr size=16

create partition primary
format quick fs=ntfs label="Windows"
assign letter=W
"@ | Set-Content -Path $DiskpartScript -Encoding ASCII

    Run-Cmd -Command "diskpart /s $DiskpartScript" -FailureMessage "Disk partitioning failed"

    Write-Host "Disk layout after partitioning:"
    Get-Disk -Number $TargetDiskNumber | Format-List *
    Get-Partition -DiskNumber $TargetDiskNumber | Format-Table DiskNumber, PartitionNumber, DriveLetter, GptType, Size, Type -AutoSize
    Get-Volume | Format-Table DriveLetter, FileSystemLabel, FileSystem, Size, DriveType -AutoSize

    $efiPartition = Get-Partition -DiskNumber $TargetDiskNumber |
        Where-Object { $_.GptType -eq "{C12A7328-F81F-11D2-BA4B-00A0C93EC93B}" } |
        Select-Object -First 1
    if ($null -eq $efiPartition) {
        throw "Diskpart did not create an EFI system partition on disk $TargetDiskNumber."
    }

    $efiVolume = $efiPartition | Get-Volume -ErrorAction Stop
    if ($efiVolume.FileSystem -ne "FAT32") {
        throw "EFI partition on disk $TargetDiskNumber is not FAT32. Found: $($efiVolume.FileSystem)"
    }

    $windowsPartition = Get-Partition -DiskNumber $TargetDiskNumber |
        Where-Object { $_.DriveLetter -eq "W" } |
        Select-Object -First 1
    if ($null -eq $windowsPartition) {
        throw "Diskpart did not create Windows partition W: on disk $TargetDiskNumber."
    }

    $windowsVolume = $windowsPartition | Get-Volume -ErrorAction Stop
    if ($windowsVolume.FileSystem -ne "NTFS") {
        throw "Windows partition W: on disk $TargetDiskNumber is not NTFS. Found: $($windowsVolume.FileSystem)"
    }
    Complete-Stage -StageName "partition"

    Write-Step "Deployment stage 5: apply deploy.wim"
    $resolvedMappedWimPath = Resolve-DeployWimPath
    $wPartition = Get-Partition -DriveLetter W -ErrorAction Stop
    if ($wPartition.DiskNumber -ne $TargetDiskNumber) {
        throw "Refusing to apply image: W: is on disk $($wPartition.DiskNumber), expected target disk $TargetDiskNumber."
    }
    Run-ProcessWithHeartbeat -FilePath "dism.exe" -ArgumentList @(
        "/Apply-Image",
        "/ImageFile:$resolvedMappedWimPath",
        "/Index:1",
        "/ApplyDir:W:\"
    ) -FailureMessage "DISM apply failed" -HeartbeatSeconds 30
    Complete-Stage -StageName "apply"

    Write-Step "Deployment stage 6: create boot files with bcdboot"
    $windowsDriveLetter = Resolve-WindowsDriveLetter -DiskNumber $TargetDiskNumber -PreferredLetter "W"
    $efiDriveLetter = Resolve-EfiDriveLetter -DiskNumber $TargetDiskNumber -PreferredLetter "S"
    $efiCheckPartition = Get-Partition -DriveLetter $efiDriveLetter -ErrorAction Stop
    if ($efiCheckPartition.DiskNumber -ne $TargetDiskNumber) {
        throw "EFI drive $efiDriveLetter`: is on disk $($efiCheckPartition.DiskNumber), expected target disk $TargetDiskNumber."
    }
    Write-Host "Using Windows volume: $windowsDriveLetter`:"
    Write-Host "Using EFI system volume: $efiDriveLetter`:"
    Run-Cmd -Command "bcdboot $windowsDriveLetter`:\Windows /s $efiDriveLetter`: /f UEFI" -FailureMessage "BCDBoot failed"
    $bcdPath = "$efiDriveLetter`:\EFI\Microsoft\Boot\BCD"
    if (-not (Test-Path $bcdPath)) {
        throw "BCDBoot completed but BCD file was not found at $bcdPath"
    }
    Write-Host "Created BCD at $bcdPath"
    & bcdedit.exe /store $bcdPath /enum all
    if ($LASTEXITCODE -ne 0) {
        throw "BCD exists at $bcdPath but bcdedit could not read it."
    }
    Complete-Stage -StageName "bcdboot"

    # Non-fatal cleanup after successful deployment.
    cmd.exe /c "net use $MappedDrive /delete /y" | Out-Host

    if ($AutoReboot) {
        Write-Step "Deployment complete. Rebooting to local disk"
        Start-Sleep -Seconds 10
        wpeutil reboot
    } else {
        Write-Step "Deployment complete. Auto reboot is disabled by configuration."
        Write-Host "Switch VM boot order to local disk and reboot manually."
    }
}
finally {
    try {
        Stop-Transcript | Out-Null
    } catch {
        # Ignore transcript shutdown failures.
    }
}
