@echo off
setlocal enabledelayedexpansion

call "{{ windows.winpe_builder.adk_dir }}\Deployment Tools\DandISetEnv.bat"

rmdir /s /q {{ windows.winpe_builder.winpe_deploy_dir }} 2>nul
rmdir /s /q {{ windows.winpe_builder.winpe_capture_dir }} 2>nul

call copype amd64 {{ windows.winpe_builder.winpe_deploy_dir }}
call copype amd64 {{ windows.winpe_builder.winpe_capture_dir }}

set OC={{ windows.winpe_builder.adk_dir }}\Windows Preinstallation Environment\amd64\WinPE_OCs

Dism /Mount-Image /ImageFile:{{ windows.winpe_builder.winpe_deploy_dir }}\media\sources\boot.wim /Index:1 /MountDir:{{ windows.winpe_builder.winpe_deploy_dir }}\mount

mkdir {{ windows.winpe_builder.winpe_deploy_dir }}\mount\Deploy

copy {{ windows.winpe_builder.build_dir }}\scripts\deploy.ps1 {{ windows.winpe_builder.winpe_deploy_dir }}\mount\Deploy\deploy.ps1
copy {{ windows.winpe_builder.build_dir }}\scripts\first-boot-join.ps1 {{ windows.winpe_builder.winpe_deploy_dir }}\mount\Deploy\first-boot-join.ps1
copy {{ windows.winpe_builder.build_dir }}\scripts\diskpart-uefi.txt {{ windows.winpe_builder.winpe_deploy_dir }}\mount\Deploy\diskpart-uefi.txt
copy {{ windows.winpe_builder.build_dir }}\scripts\startnet.cmd {{ windows.winpe_builder.winpe_deploy_dir }}\mount\Windows\System32\startnet.cmd

Dism /Add-Package /Image:{{ windows.winpe_builder.winpe_deploy_dir }}\mount /PackagePath:"%OC%\WinPE-WMI.cab"
Dism /Add-Package /Image:{{ windows.winpe_builder.winpe_deploy_dir }}\mount /PackagePath:"%OC%\WinPE-NetFX.cab"
Dism /Add-Package /Image:{{ windows.winpe_builder.winpe_deploy_dir }}\mount /PackagePath:"%OC%\WinPE-Scripting.cab"
Dism /Add-Package /Image:{{ windows.winpe_builder.winpe_deploy_dir }}\mount /PackagePath:"%OC%\WinPE-PowerShell.cab"
Dism /Add-Package /Image:{{ windows.winpe_builder.winpe_deploy_dir }}\mount /PackagePath:"%OC%\WinPE-StorageWMI.cab"
Dism /Add-Package /Image:{{ windows.winpe_builder.winpe_deploy_dir }}\mount /PackagePath:"%OC%\WinPE-DismCmdlets.cab"

if exist {{ windows.winpe_builder.drivers_dir }} (
  echo Injecting storage drivers from {{ windows.winpe_builder.drivers_dir }} into deploy WinPE...
  Dism /Image:{{ windows.winpe_builder.winpe_deploy_dir }}\mount /Add-Driver /Driver:{{ windows.winpe_builder.drivers_dir }} /Recurse
  if errorlevel 1 (
    echo DISM Add-Driver failed for deploy WinPE.
    Dism /Unmount-Image /MountDir:{{ windows.winpe_builder.winpe_deploy_dir }}\mount /Discard
    exit /b 1
  )
  Dism /Image:{{ windows.winpe_builder.winpe_deploy_dir }}\mount /Get-Drivers | findstr /I "Intel iaStor RST Storage"
)

Dism /Unmount-Image /MountDir:{{ windows.winpe_builder.winpe_deploy_dir }}\mount /Commit

Dism /Mount-Image /ImageFile:{{ windows.winpe_builder.winpe_capture_dir }}\media\sources\boot.wim /Index:1 /MountDir:{{ windows.winpe_builder.winpe_capture_dir }}\mount

mkdir {{ windows.winpe_builder.winpe_capture_dir }}\mount\Deploy

copy {{ windows.winpe_builder.build_dir }}\scripts\capture.ps1 {{ windows.winpe_builder.winpe_capture_dir }}\mount\Deploy\capture.ps1
copy {{ windows.winpe_builder.build_dir }}\scripts\WimScript.ini {{ windows.winpe_builder.winpe_capture_dir }}\mount\Deploy\WimScript.ini

echo wpeinit > {{ windows.winpe_builder.winpe_capture_dir }}\mount\Windows\System32\startnet.cmd
echo powershell.exe -ExecutionPolicy Bypass -NoProfile -File X:\Deploy\capture.ps1 >> {{ windows.winpe_builder.winpe_capture_dir }}\mount\Windows\System32\startnet.cmd

Dism /Add-Package /Image:{{ windows.winpe_builder.winpe_capture_dir }}\mount /PackagePath:"%OC%\WinPE-WMI.cab"
Dism /Add-Package /Image:{{ windows.winpe_builder.winpe_capture_dir }}\mount /PackagePath:"%OC%\WinPE-NetFX.cab"
Dism /Add-Package /Image:{{ windows.winpe_builder.winpe_capture_dir }}\mount /PackagePath:"%OC%\WinPE-Scripting.cab"
Dism /Add-Package /Image:{{ windows.winpe_builder.winpe_capture_dir }}\mount /PackagePath:"%OC%\WinPE-PowerShell.cab"
Dism /Add-Package /Image:{{ windows.winpe_builder.winpe_capture_dir }}\mount /PackagePath:"%OC%\WinPE-StorageWMI.cab"
Dism /Add-Package /Image:{{ windows.winpe_builder.winpe_capture_dir }}\mount /PackagePath:"%OC%\WinPE-DismCmdlets.cab"

if exist {{ windows.winpe_builder.drivers_dir }} (
  echo Injecting storage drivers from {{ windows.winpe_builder.drivers_dir }} into capture WinPE...
  Dism /Image:{{ windows.winpe_builder.winpe_capture_dir }}\mount /Add-Driver /Driver:{{ windows.winpe_builder.drivers_dir }} /Recurse
  if errorlevel 1 (
    echo DISM Add-Driver failed for capture WinPE.
    Dism /Unmount-Image /MountDir:{{ windows.winpe_builder.winpe_capture_dir }}\mount /Discard
    exit /b 1
  )
  Dism /Image:{{ windows.winpe_builder.winpe_capture_dir }}\mount /Get-Drivers | findstr /I "Intel iaStor RST Storage"
)

Dism /Unmount-Image /MountDir:{{ windows.winpe_builder.winpe_capture_dir }}\mount /Commit

call MakeWinPEMedia /ISO {{ windows.winpe_builder.winpe_capture_dir }} {{ windows.winpe_builder.build_dir }}\winpe_capture.iso

copy {{ windows.winpe_builder.winpe_deploy_dir }}\media\sources\boot.wim {{ windows.winpe_builder.build_dir }}\boot.wim
copy "{{ windows.winpe_builder.adk_dir }}\Windows Preinstallation Environment\amd64\Media\bootmgr" {{ windows.winpe_builder.build_dir }}\bootmgr
mkdir {{ windows.winpe_builder.build_dir }}\boot 2>nul
copy "{{ windows.winpe_builder.adk_dir }}\Windows Preinstallation Environment\amd64\Media\Boot\BCD" {{ windows.winpe_builder.build_dir }}\boot\BCD
copy "{{ windows.winpe_builder.adk_dir }}\Windows Preinstallation Environment\amd64\Media\Boot\boot.sdi" {{ windows.winpe_builder.build_dir }}\boot\boot.sdi
mkdir {{ windows.winpe_builder.build_dir }}\efi\boot 2>nul
mkdir {{ windows.winpe_builder.build_dir }}\efi\microsoft\boot 2>nul
copy "{{ windows.winpe_builder.adk_dir }}\Windows Preinstallation Environment\amd64\Media\EFI\Boot\bootx64.efi" {{ windows.winpe_builder.build_dir }}\efi\boot\bootx64.efi
copy "{{ windows.winpe_builder.adk_dir }}\Windows Preinstallation Environment\amd64\Media\EFI\Microsoft\Boot\BCD" {{ windows.winpe_builder.build_dir }}\efi\microsoft\boot\BCD

echo Done.
