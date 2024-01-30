# Reset OS10 Admin Password

Video: https://youtu.be/0VfJCa8s7yo

1. Connect to the serial console port. The serial settings are 115,200 baud, 8 data bits, and no parity.
2. Reboot or power up the system.
3. Press ESC at the Grub prompt to view the boot menu. The OS10-A partition is selected by default.

        +-------------------------------------+
        |*OS10-A                              |
        | OS10-B                              |
        | ONIE                                |
        +-------------------------------------+

4. Press e to open the OS10 GRUB editor.
      1.Use the arrow keys to navigate to the end of the line that has set os_debug_args= and then add init=/bin/bash.

            +---------------------------------------------------------+
            |setparams 'OS10-A'                                       |
            |                                                         |
            | set os_debug_args="init=/bin/bash"                      |       
            | select_image A                                          |
            | boot_os                                                 |
            |                                                         |
            +---------------------------------------------------------+

5. Press Alt + 0. The system boots to a root shell without a password.
6. At the root prompt run `passwd admin` and set the password to whatever you want
7. Run `reboot -f` to reboot the system
8. When the system reboots log into the admin account with your new password. That password is temporary and *is not permanently written to the system*.
9. Enter configuration mode with `configure terminal` and then run `username admin password <YOURPASSWORD> role sysadmin` to change the password
10. Run `write memory` to make the changes permanent.

## Startup Config Location

/config/etc/opt/dell/os10/db_init/startup.xml