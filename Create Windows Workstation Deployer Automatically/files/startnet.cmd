wpeinit
{% if windows.deploy_debug.startup_pause | bool %}
echo WinPE started. Press any key to continue deploy script.
pause
{% endif %}
powershell.exe -ExecutionPolicy Bypass -NoProfile -File X:\Deploy\deploy.ps1
