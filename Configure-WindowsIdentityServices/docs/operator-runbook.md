# Operator Runbook

1. Install Windows Server.
2. Install Proxmox VirtIO drivers.
3. Install QEMU Guest Agent.
4. Enable QEMU Guest Agent in Proxmox VM Options.
5. Reboot.
6. Copy project to `C:\Admin\Configure-WindowsIdentityServices`.
7. Install required PowerShell modules manually if required.
8. Copy `config.example.yaml` to `config.yaml`.
9. Edit every setting.
10. Run PlanOnly.
11. Review planned operations.
12. Run actual configuration.
13. Enter Directory Services Restore Mode (DSRM) password when prompted.
14. Allow reboot.
15. Log in as domain Administrator.
16. Confirm resume task completes.
17. Run ValidateOnly.
18. Archive evidence directory.
