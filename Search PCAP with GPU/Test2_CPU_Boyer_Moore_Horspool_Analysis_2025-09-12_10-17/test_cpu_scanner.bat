@echo off
REM Test runner for CPU PCAP Scanner
REM This script tests the CPU implementation

echo CPU PCAP Scanner Test Runner
echo =============================

REM Build the scanner
echo.
echo Step 1: Running CPU scanner tests...
python cpu_scanner.py

echo.
echo Step 2: Running comprehensive benchmark...
python cpu_benchmark.py
if %ERRORLEVEL% EQU 0 (
    echo ✓ Benchmark completed successfully
) else (
    echo ✗ Benchmark failed
)

echo.
echo CPU scanner tests completed!
echo Check results\ directory for detailed results.
pause
