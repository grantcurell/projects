@echo off
REM Build script for CUDA PCAP scanner on Windows
REM Requires NVIDIA CUDA Toolkit and libpcap development libraries

echo Building CUDA PCAP Scanner...

REM Set CUDA path
set CUDA_PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v13.0
set NVCC=%CUDA_PATH%\bin\nvcc.exe

REM Check if nvcc is available
if not exist "%NVCC%" (
    echo ERROR: nvcc not found at %NVCC%
    echo Please install NVIDIA CUDA Toolkit.
    pause
    exit /b 1
)

REM Check if libpcap headers are available
if not exist "C:\Program Files\Npcap\Include\pcap.h" (
    echo WARNING: libpcap headers not found in default location.
    echo You may need to install Npcap SDK or WinPcap SDK.
    echo Continuing with build...
)

REM Build the CUDA program
echo Compiling gpupcapgrep.cu...
"%NVCC%" -O3 -std=c++17 -Xcompiler /openmp -lpcap -o gpupcapgrep.exe gpupcapgrep.cu

if %ERRORLEVEL% EQU 0 (
    echo Build successful! gpupcapgrep.exe created.
    echo.
    echo Usage: gpupcapgrep.exe file.pcap -s "pattern1" -s "pattern2" ...
    echo Example: gpupcapgrep.exe "PCAP Files\synthetic_100mb.pcapng" -s "password" -s "GET /"
) else (
    echo Build failed! Check error messages above.
    pause
    exit /b 1
)

pause
