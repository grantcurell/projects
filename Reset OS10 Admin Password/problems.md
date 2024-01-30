# Resetting Dell OS10 Password

## Working Instructions

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


## Problems with online documentation

Based on [official instructions here](https://www.dell.com/support/manuals/us/en/04/networking-s4148f-on/smartfabric-os-user-guide-10-5-1/recover-linux-password?guid=guid-4263f287-20e8-4f25-8092-75a532f0c7ea&lang=en-us)

- Instructions are for resetting the linuxadmin account. Majority of audience are network engineers who have little understanding of Linux. Even for me, a Linux engineer who also does network engineering, and has done extensive work with OS10 had no idea a linuxadmin account even existed much less what it was used for.
- Having worked extensively with customers in the field, I have never met one that actually knew that OS10 is just Debian Linux much less understood the relationship between the Linux command line and the OS10 shell. The instructions seem to assume that you understand the relationship between the OS10 shell, the Linux command line, and the Linux users. The vast majority of the users of OS10 will not understand these distinctions.
- In my case the customer was very confused as to what linuxadmin was. They had never used it and after resetting the password for linuxadmin tried logging into the admin account and was confused when it didn't work
- They were then further confused because they tried to log into OS10 B thinking it was some sort of synchronized backup. Since it was identical to OS10 A they thought changes made there would synchronize between the two.
- The instructions do not tell you that the changes made to the password are temporary and will not persist through reboot.
- As far as I can tell, we do not have any documentation describing how to reset the admin account for the OS10 command line which is what virtually all customers will want to do.

## Suggestions

- Ensure that instructions for resetting the admin account password are easily accessible online
- Clarify the purpose of the linuxadmin account
- If there are plans to expose the Linux nature of OS10 to the customer, provide documentation clearly articulating the relationship between Linux and OS10 from the perspective of what is relevant to someone with a network engineering background. I am happy to help with this.