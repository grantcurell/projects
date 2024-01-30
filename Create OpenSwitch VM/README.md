# Create OpenSwitch VM

1. Download [onie-kvm.iso](https://archive.openswitch.net/onie/vm/onie_kvm.iso)
2. Create a VM - it must use BIOS boot mode
      1. *WARNING* If you are running on VMWare ESXi you must use an IDE hard drive!
      2. *WARNING* If you are running on VMWare ESXi you must use the E1000E driver for the network card!
3. Boot from the CD, but at the grub menu, hit tab to edit the options and remove all console options
      1. See: https://askubuntu.com/questions/771871/16-04-virtualbox-vm-from-vhd-file-hangs-at-non-blocking-pool-is-initialized
4. Once you drop to the ONIE command line run `sed -i 's/vda/sda/g' /lib/onie/onie-updater`
5. Workable fix: `sed 's/if \[ "$sha1.*/if false; then/g' /lib/onie/onie-updater`
6. Run `onie-self-update -e file://lib/onie/onie-updater`
7. Reboot.
8.  For whatever reason I couldn't get the discovery process to work so I ran `onie-discovery-stop`
9. Then run `onie-nos-install http://<SERVER_IP>/onie-installer`

## Faster fix that didn't work

1. Run `sha1sum /lib/onie/onie-updater` and note the sha1 hash
2. Run `sed "s/payload\=.*/payload_sha1=<YOURHASH>/g" /lib/onie/onie-updater`
3. I tried `sed "s/payload\=.*/payload_sha1=$(sha1sum <THING> | cut -d " " -f 1)/g" /lib/onie/onie-updater` and it wouldn't let me do it
