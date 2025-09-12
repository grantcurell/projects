@echo off
REM Test runner for CUDA PCAP Scanner
REM This script builds the scanner and runs basic tests

echo CUDA PCAP Scanner Test Runner
echo =============================

REM Build the scanner
echo.
echo Step 1: Building CUDA scanner...
call build.bat
if %ERRORLEVEL% NEQ 0 (
    echo Build failed! Cannot continue with tests.
    pause
    exit /b 1
)

REM Check if scanner was created
if not exist "gpupcapgrep.exe" (
    echo ERROR: Scanner executable not found after build!
    pause
    exit /b 1
)

echo.
echo Step 2: Running basic functionality test...

REM Test with 1 pattern
echo Testing with 1 pattern...
gpupcapgrep.exe "PCAP Files\synthetic_50mb.pcapng" -s "password" > test_output_1.txt 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✓ 1 pattern test passed
) else (
    echo ✗ 1 pattern test failed
    type test_output_1.txt
)

REM Test with 7 patterns
echo.
echo Testing with 7 patterns...
gpupcapgrep.exe "PCAP Files\synthetic_50mb.pcapng" -s "password" -s "GET" -s "POST" -s "HTTP" -s "HTTPS" -s "User-Agent" -s "Authorization" > test_output_7.txt 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✓ 7 pattern test passed
) else (
    echo ✗ 7 pattern test failed
    type test_output_7.txt
)

REM Test with 14 patterns
echo.
echo Testing with 14 patterns...
gpupcapgrep.exe "PCAP Files\synthetic_50mb.pcapng" -s "password" -s "GET" -s "POST" -s "HTTP" -s "HTTPS" -s "User-Agent" -s "Authorization" -s "admin" -s "login" -s "session" -s "token" -s "malware" -s "virus" -s "exploit" -s "vulnerability" > test_output_14.txt 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✓ 14 pattern test passed
) else (
    echo ✗ 14 pattern test failed
    type test_output_14.txt
)

echo.
echo Step 3: Running comprehensive benchmark...
python cuda_benchmark.py
if %ERRORLEVEL% EQU 0 (
    echo ✓ Benchmark completed successfully
) else (
    echo ✗ Benchmark failed
)

echo.
echo Test runner completed!
echo Check results\ directory for detailed results.
pause
