$ErrorActionPreference = "Stop"

# Portable addressing: boot.wim never contains the deployer IP.
# The configured name is only a fallback label; the deployer is always this client's
# DHCP server (it serves DHCP, DNS, SMB and HTTP from a single IP), so we discover
# that IP at runtime. This avoids depending on name resolution, which is unreliable
# in WinPE for single-label names (no DNS suffix/devolution), while still keeping the
# deployer IP out of the image.
#
# WinPE DHCP/DNS bring-up is racy on a cold PXE boot: the script can start before the
# NIC has a lease, at which point no DHCP server is known yet. We therefore re-run this
# discovery on every network-probe attempt (stage 1) rather than only once, so a slow
# lease can never pin us to an unresolvable single-label name and fail SMB with error 53.
$ConfiguredDeployServer = "{{ deployer.offline.hostname }}"
$DeployServer = $ConfiguredDeployServer
$DeployShareUser = "{{ deployer.samba.username }}"
$DeploySharePassword = "{{ deployer.samba.password }}"
# Resolved from $DeployServer once the network is confirmed reachable (Update-DeploySharePaths).
$DeploySharePath = $null
$DeployShareFallbackPath = $null
$JoinSharePath = $null
$StopAfterStage = "{{ windows.deploy.stop_after_stage | lower }}".Trim().ToLowerInvariant()
$PauseBetweenStages = [System.Convert]::ToBoolean("{{ windows.deploy.pause_between_stages | bool }}")
$AutoReboot = [System.Convert]::ToBoolean("{{ windows.deploy.auto_reboot | bool }}")
$MinimumTargetDiskSizeBytes = {{ windows.deploy.minimum_target_disk_size_bytes }}
$MappedDrive = "Z:"
$MappedWimPath = "$MappedDrive\images\deploy.wim"
$MappedWimFallbackPath = "$MappedDrive\deploy.wim"
$SiteConfigPath = "$MappedDrive\site\domain.json"
$NamingConfigPath = "$MappedDrive\site\naming.json"
$DiskpartScript = "X:\Deploy\diskpart-runtime.txt"
$TranscriptPath = "X:\Deploy\deploy.log"
# Staged first-boot artifacts (baked into boot.wim alongside deploy.ps1).
$FirstBootSource = "X:\Deploy\first-boot-join.ps1"
$ValidStopStages = @("none", "network", "smb", "siteconfig", "servicetag", "artifact", "disk", "partition", "apply", "stagejoin", "bcdboot")

# Populated by stages so finally{} can do a single unmap.
$script:DeployShareMapped = $false
$script:DomainJoinEnabled = $false
$script:DomainConfig = $null
$script:NamingConfig = $null
$script:ComputerName = $null

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

function Resolve-DeployServerAddress {
    # Goal: end up with the deployer's IP ADDRESS, never a single-label name. The WinPE
    # SMB redirector frequently cannot resolve single-label names (no DNS suffix /
    # devolution), so `net use \\win-deploy\...` fails with "System error 53" even though
    # .NET DNS and the TCP/445 probe succeed against that same name. We therefore convert
    # the deployer to an IP, trying in order:
    #   1) the DHCP server address (the deployer is always this client's DHCP server), and
    #   2) .NET DNS resolution of the configured name (works via the deployer's own DNS).
    # Safe to call repeatedly: until the NIC has a lease both lookups are no-ops and the
    # caller retries.
    $candidate = $null

    try {
        $dhcpServer = (Get-CimInstance -ClassName Win32_NetworkAdapterConfiguration -ErrorAction Stop |
            Where-Object {
                $_.IPEnabled -and $_.DHCPEnabled -and
                $_.DHCPServer -and
                $_.DHCPServer -ne "255.255.255.255" -and
                $_.DHCPServer -ne "0.0.0.0"
            } |
            Select-Object -First 1 -ExpandProperty DHCPServer)
        if (-not [string]::IsNullOrWhiteSpace($dhcpServer)) {
            $candidate = $dhcpServer
        }
    } catch {
        # NIC not ready yet.
    }

    if ([string]::IsNullOrWhiteSpace($candidate)) {
        try {
            $candidate = ([System.Net.Dns]::GetHostAddresses($ConfiguredDeployServer) |
                Where-Object { $_.AddressFamily -eq [System.Net.Sockets.AddressFamily]::InterNetwork } |
                Select-Object -First 1).IPAddressToString
        } catch {
            # Name not resolvable yet.
        }
    }

    if (-not [string]::IsNullOrWhiteSpace($candidate)) {
        if ($script:DeployServer -ne $candidate) {
            Write-Host "Resolved deploy server to IP $candidate (configured name '$ConfiguredDeployServer')."
        }
        $script:DeployServer = $candidate
    }
}

function Update-DeploySharePaths {
    $script:DeploySharePath = "\\$($script:DeployServer)\deploy"
    $script:DeployShareFallbackPath = "\\$($script:DeployServer)\capture"
    $script:JoinSharePath = "\\$($script:DeployServer)\join"
}

function Ensure-DeployShareMapped {
    # Idempotent: maps Z: exactly once and keeps it mapped for the whole run.
    if ($script:DeployShareMapped) {
        return
    }

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
        $script:DeployShareMapped = $true
        Write-Host "Mapped credentialed deploy share $DeploySharePath as $MappedDrive"
        return
    }

    Write-Host "Credentialed deploy share map failed; trying guest capture share fallback."
    cmd.exe /c "net use $MappedDrive /delete /y" | Out-Host
    & net.exe use $MappedDrive $DeployShareFallbackPath /persistent:no
    if ($LASTEXITCODE -eq 0) {
        $script:DeployShareMapped = $true
        Write-Host "Mapped guest capture share $DeployShareFallbackPath as $MappedDrive"
        return
    }

    throw "SMB mapping to deploy share failed. Refusing to continue without a network deploy.wim path."
}

function Read-RequiredJson {
    param([string]$Path, [string]$Description)
    if (-not (Test-Path $Path)) {
        throw "$Description not found at $Path."
    }
    try {
        return Get-Content -Path $Path -Raw | ConvertFrom-Json
    } catch {
        throw "$Description at $Path is not valid JSON: $($_.Exception.Message)"
    }
}

function Get-RequiredProperty {
    param($Object, [string]$Name, [string]$Context)
    if ($null -eq $Object.$Name -or [string]::IsNullOrWhiteSpace([string]$Object.$Name)) {
        throw "$Context is missing required key '$Name' (no defaults allowed)."
    }
    return $Object.$Name
}

function Get-DellServiceTag {
    $bios = Get-CimInstance -ClassName Win32_BIOS -ErrorAction Stop
    $serial = ($bios.SerialNumber | Out-String).Trim()
    $invalid = @(
        "", "0", "none", "default string", "system serial number",
        "to be filled by o.e.m.", "not specified", "not available", "unknown"
    )
    if ($invalid -contains $serial.ToLowerInvariant()) {
        throw "BIOS serial number '$serial' is not a valid Dell service tag. For lab VMs set: qm set <vmid> --smbios1 serial=7ABC123"
    }
    return $serial
}

function Resolve-DeployWimPath {
    Ensure-DeployShareMapped
    foreach ($candidate in @($MappedWimPath, $MappedWimFallbackPath)) {
        if (Test-Path $candidate) {
            Write-Host "Using deploy.wim from SMB path $candidate"
            return $candidate
        }
    }
    throw "SMB share mapped but deploy.wim was not found at expected paths ($MappedWimPath, $MappedWimFallbackPath)."
}

function Get-DeploymentTargetDisk {
    param([Int64]$MinimumSizeBytes)

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
    param([int]$DiskNumber, [string]$PreferredLetter = "W")

    $preferredPartition = Get-Partition -DiskNumber $DiskNumber -ErrorAction Stop |
        Where-Object { $_.DriveLetter -eq $PreferredLetter } |
        Select-Object -First 1
    if ($null -ne $preferredPartition -and (Test-Path "$PreferredLetter`:\Windows\System32")) {
        return $PreferredLetter
    }

    $windowsPartition = Get-Partition -DiskNumber $DiskNumber -ErrorAction Stop |
        Where-Object { $_.DriveLetter -and (Test-Path "$($_.DriveLetter):\Windows\System32") } |
        Select-Object -First 1
    if ($null -eq $windowsPartition) {
        throw "Unable to locate deployed Windows volume on target disk $DiskNumber."
    }
    return [string]$windowsPartition.DriveLetter
}

function Resolve-EfiDriveLetter {
    param([int]$DiskNumber, [string]$PreferredLetter = "S")

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

function Set-OfflineComputerName {
    param(
        [string]$WindowsDrive,
        [string]$Name
    )

    # Stamp the authoritative computer name (service tag) into the offline image's
    # specialize pass so the machine boots ALREADY named correctly, before OOBE.
    #
    # Why this matters: if the machine instead booted with a random name and
    # first-boot-join used `Add-Computer -NewName <tag>`, the rename fails with
    # "The account already exists" whenever a computer account for <tag> is already
    # in AD -- which is exactly the case when re-imaging the same physical machine
    # (same service tag). By naming the box <tag> up front, first-boot-join takes the
    # join-by-existing-name path (`Add-Computer ... -Force`, no -NewName), which
    # cleanly takes over / re-uses the existing account and is idempotent for
    # re-images.
    $pantherUnattend = "$WindowsDrive`:\Windows\Panther\unattend.xml"
    if (-not (Test-Path $pantherUnattend)) {
        throw "Offline unattend not found at $pantherUnattend; cannot set authoritative ComputerName."
    }

    [xml]$ua = Get-Content -Path $pantherUnattend -Raw
    $ns = New-Object System.Xml.XmlNamespaceManager($ua.NameTable)
    $ns.AddNamespace("u", "urn:schemas-microsoft-com:unattend")
    $cnNodes = $ua.SelectNodes("//u:settings[@pass='specialize']/u:component[@name='Microsoft-Windows-Shell-Setup']/u:ComputerName", $ns)
    if ($null -eq $cnNodes -or $cnNodes.Count -eq 0) {
        throw "No specialize ComputerName element found in $pantherUnattend; cannot set authoritative ComputerName."
    }
    foreach ($n in $cnNodes) { $n.InnerText = $Name }
    $ua.Save($pantherUnattend)
    Write-Host "Stamped offline ComputerName '$Name' into $pantherUnattend (specialize pass)."
}

function Invoke-StageJoin {
    param([string]$WindowsDrive)

    # Set the authoritative offline ComputerName (= service tag) in the applied image
    # so the box boots already named correctly and the domain join is re-image safe.
    Set-OfflineComputerName -WindowsDrive $WindowsDrive -Name $script:ComputerName

    # Beyond the ComputerName above, deploy.ps1 only drops the first-boot script
    # (and, when domain join is enabled, the transient credential) into the image.
    $scriptsDir = "$WindowsDrive`:\Windows\Setup\Scripts"
    New-Item -ItemType Directory -Path $scriptsDir -Force | Out-Null

    if (-not (Test-Path $FirstBootSource)) {
        throw "First-boot join script not found at $FirstBootSource (it must be baked into boot.wim)."
    }
    Copy-Item -Path $FirstBootSource -Destination "$scriptsDir\first-boot-join.ps1" -Force

    # SetupComplete.cmd runs automatically as SYSTEM at the end of Windows setup.
    $setupComplete = @"
@echo off
powershell.exe -ExecutionPolicy Bypass -NoProfile -File "%~dp0first-boot-join.ps1" >> "%SystemRoot%\Setup\Scripts\join.log" 2>&1
"@
    Set-Content -Path "$scriptsDir\SetupComplete.cmd" -Value $setupComplete -Encoding ASCII

    # Non-secret first-boot config (name policy + domain target).
    $joinConfig = [ordered]@{
        domain_join_enabled = [bool]$script:DomainJoinEnabled
        computer_name       = $script:ComputerName
        max_length          = [int]$script:NamingConfig.max_length
    }
    if ($script:DomainJoinEnabled) {
        $joinConfig.domain_fqdn = [string]$script:DomainConfig.domain_fqdn
        $joinConfig.ou_path = [string]$script:DomainConfig.ou_path
        $joinConfig.domain_netbios = [string]$script:DomainConfig.domain_netbios
    }
    ($joinConfig | ConvertTo-Json) | Set-Content -Path "$scriptsDir\join-config.json" -Encoding UTF8

    if (-not $script:DomainJoinEnabled) {
        Write-Host "Domain join disabled: staged rename-only first-boot script (no credential)."
        return
    }

    # Domain join enabled: fetch the delegated credential from the authenticated
    # [join] share and stage it transiently with SYSTEM/Administrators-only ACLs.
    cmd.exe /c "net use $JoinSharePath /delete /y >nul 2>&1" | Out-Null
    & net.exe use $JoinSharePath $DeploySharePassword "/user:$DeployShareUser" /persistent:no
    if ($LASTEXITCODE -ne 0) {
        throw "Domain join is enabled but the authenticated [join] share ($JoinSharePath) is unreachable. Refusing to continue."
    }
    try {
        $remoteCred = "$JoinSharePath\join.cred"
        if (-not (Test-Path $remoteCred)) {
            throw "Domain join enabled but join.cred was not found on the [join] share."
        }
        $credTarget = "$scriptsDir\join.cred"
        Copy-Item -Path $remoteCred -Destination $credTarget -Force

        # Lock the transient credential to SYSTEM + Administrators only.
        Run-Cmd -Command "icacls `"$credTarget`" /inheritance:r" -FailureMessage "Failed to reset ACL inheritance on transient credential"
        Run-Cmd -Command "icacls `"$credTarget`" /grant:r *S-1-5-18:F *S-1-5-32-544:F" -FailureMessage "Failed to restrict ACL on transient credential"
        Write-Host "Staged first-boot join script + transient credential (SYSTEM/Administrators only)."
    }
    finally {
        cmd.exe /c "net use $JoinSharePath /delete /y >nul 2>&1" | Out-Null
    }
}

if ($ValidStopStages -notcontains $StopAfterStage) {
    throw "Invalid stop_after_stage '$StopAfterStage'. Valid values: $($ValidStopStages -join ', ')"
}

Start-Transcript -Path $TranscriptPath -Force
try {
    cmd.exe /c "reg add HKCU\Console /v QuickEdit /t REG_DWORD /d 0 /f >nul 2>&1" | Out-Null
    Disable-ConsoleQuickEditRuntime

    Write-Step "Deployment stage 1: network check"
    ipconfig /all
    # PXE/WinPE networking (DHCP lease, DNS, first-hop ARP) can take a few seconds
    # to settle. Retry so an unattended deployment tolerates a slow bring-up instead
    # of failing on a single cold-start probe.
    #
    # NOTE: Test-Connection (ICMP) is unreliable in WinPE because it depends on the
    # WMI ping provider, which is not present in WinPE. Instead, probe the actual SMB
    # port (445) on the deploy server with a TCP connect. This both resolves the
    # deploy server's name via DNS and validates the dependency we truly need.
    $networkReady = $false
    $maxNetworkAttempts = 30
    for ($attempt = 1; $attempt -le $maxNetworkAttempts -and -not $networkReady; $attempt++) {
        # Re-resolve the deployer to an IP each attempt: on a cold boot the lease/DNS may
        # not be ready on the first pass, so this upgrades $DeployServer from the configured
        # single-label name to the deployer IP as soon as either lookup succeeds. Using an
        # IP (not the name) is what lets `net use` work in WinPE.
        Resolve-DeployServerAddress
        # Require an actual IP before proceeding: net use against a single-label name
        # fails with error 53 in WinPE, so we wait until resolution yields an address.
        $parsedDeployIp = $null
        $deployServerIsIp = [System.Net.IPAddress]::TryParse($DeployServer, [ref]$parsedDeployIp)
        if (-not $deployServerIsIp) {
            Write-Host "Deployer not resolved to an IP yet (have '$DeployServer'); attempt $attempt/$maxNetworkAttempts; waiting..."
            Start-Sleep -Seconds 6
            continue
        }
        $tcpClient = $null
        try {
            $tcpClient = New-Object System.Net.Sockets.TcpClient
            $async = $tcpClient.BeginConnect($DeployServer, 445, $null, $null)
            if ($async.AsyncWaitHandle.WaitOne(3000, $false) -and $tcpClient.Connected) {
                $tcpClient.EndConnect($async)
                $networkReady = $true
            }
        } catch {
            $networkReady = $false
        } finally {
            if ($null -ne $tcpClient) {
                $tcpClient.Close()
            }
        }
        if (-not $networkReady) {
            Write-Host "Deploy server $DeployServer (SMB/445) not reachable yet (attempt $attempt/$maxNetworkAttempts); waiting..."
            Start-Sleep -Seconds 6
        }
    }
    if (-not $networkReady) {
        throw "Cannot reach deploy server $DeployServer on SMB port 445 after $maxNetworkAttempts attempts."
    }
    # Network confirmed: freeze the resolved server into the SMB share paths used by
    # every later stage (Ensure-DeployShareMapped, Resolve-DeployWimPath, Invoke-StageJoin).
    Update-DeploySharePaths
    Write-Host "Deploy server $DeployServer is reachable on SMB port 445."
    Complete-Stage -StageName "network"

    Write-Step "Deployment stage 2: map deploy share (single persistent SMB session)"
    Ensure-DeployShareMapped
    Complete-Stage -StageName "smb"

    Write-Step "Deployment stage 3: read site config"
    $script:DomainConfig = Read-RequiredJson -Path $SiteConfigPath -Description "Site domain config (domain.json)"
    $script:NamingConfig = Read-RequiredJson -Path $NamingConfigPath -Description "Site naming config (naming.json)"
    if ($null -eq $script:DomainConfig.enabled) {
        throw "domain.json is missing required key 'enabled'."
    }
    $script:DomainJoinEnabled = [bool]$script:DomainConfig.enabled
    if ($script:DomainJoinEnabled) {
        [void](Get-RequiredProperty -Object $script:DomainConfig -Name "domain_fqdn" -Context "domain.json")
        [void](Get-RequiredProperty -Object $script:DomainConfig -Name "ou_path" -Context "domain.json")
    }
    [void](Get-RequiredProperty -Object $script:NamingConfig -Name "max_length" -Context "naming.json")
    Write-Host "Domain join enabled: $script:DomainJoinEnabled"
    Complete-Stage -StageName "siteconfig"

    Write-Step "Deployment stage 4: resolve service tag -> computer name"
    $script:ComputerName = Get-DellServiceTag
    $maxLen = [int]$script:NamingConfig.max_length
    if ($script:ComputerName.Length -gt $maxLen) {
        throw "Service tag '$($script:ComputerName)' exceeds naming.max_length ($maxLen)."
    }
    if ($script:ComputerName -notmatch '^[A-Za-z0-9-]+$') {
        throw "Service tag '$($script:ComputerName)' contains characters invalid for a computer name."
    }
    Write-Host "Computer name (service tag): $($script:ComputerName)"
    Complete-Stage -StageName "servicetag"

    Write-Step "Deployment stage 5: verify deploy.wim is reachable"
    $resolvedMappedWimPath = Resolve-DeployWimPath
    Complete-Stage -StageName "artifact"

    Write-Step "Deployment stage 6: target disk detection"
    $targetDisk = Get-DeploymentTargetDisk -MinimumSizeBytes $MinimumTargetDiskSizeBytes
    $TargetDiskNumber = $targetDisk.Number
    Write-Host "Deployment target disk number: $TargetDiskNumber"
    Write-Host "Deployment target disk size (bytes): $($targetDisk.Size)"
    Complete-Stage -StageName "disk"

    Write-Step "Deployment stage 7: disk partitioning"
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

    Write-Step "Deployment stage 8: apply deploy.wim"
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

    Write-Step "Deployment stage 9: stage first-boot naming + join"
    Invoke-StageJoin -WindowsDrive "W"
    Complete-Stage -StageName "stagejoin"

    Write-Step "Deployment stage 10: create boot files with bcdboot"
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
    # Single unmap of the persistent deploy share.
    cmd.exe /c "net use $MappedDrive /delete /y" | Out-Host
    try {
        Stop-Transcript | Out-Null
    } catch {
        # Ignore transcript shutdown failures.
    }
}
