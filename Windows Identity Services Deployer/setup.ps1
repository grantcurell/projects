#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$RootDir = Split-Path -Parent $PSCommandPath
$Wizard = Join-Path $RootDir 'scripts\identity-config-wizard.py'

function Get-PythonCommand {
    foreach ($name in @('python', 'python3', 'py')) {
        $cmd = Get-Command $name -ErrorAction SilentlyContinue
        if ($cmd) { return $cmd.Source }
    }
    throw 'Python 3 is required for the configuration wizard. Install Python 3 and rerun .\setup.ps1'
}

$python = Get-PythonCommand
& $python -c @'
import importlib.util, subprocess, sys
required = {"textual": "textual", "yaml": "pyyaml"}
missing = [pkg for mod, pkg in required.items() if importlib.util.find_spec(mod) is None]
if missing:
    print("Installing Python dependencies for setup wizard:", ", ".join(missing))
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", *missing])
'@

& $python $Wizard
