# Setting Up vRealize

## Setting Credentials

I had to get on the Linux command line to set the credentials. I did the following:

1. When you hit the grub menu, add init=/bin/bash to drop to a command line.
2. Once you get to the command line run `sudo passwd root` and set that password.
3. Run `sudo passwd admin` to reset the local admin account. Note: This is not the admin account you need to get to the web frontend.
4. Run `$VMWARE_PYTHON_BIN $VCOPS_BASE/../vmware-vcopssuite/utilities/sliceConfiguration/bin/vcopsSetAdminPassword.py --reset` to reset the admin account for the web GUI. Note: Despite what the documentation says, the username is not admin@local, it is admin. There are also password complexity requirements.