# Swap Kernel on Rocky 9

Pull the Linux kernel from [here](https://www.kernel.org/)

```bash
# Pull in Rocky's existing config
cp -f /boot/config-$(uname -r) .config

# This accepts all the defaults for the new kernel options
yes "" | make -j$(nproc --all) oldconfig
make -j$(nproc)
make -j$(nproc) modules
make -j$(nproc) modules_install
grub2-mkconfig -o /boot/efi/EFI/rocky/grub.cfg
# sudo dnf reinstall grub2-efi-x64 shim-x64
```

**CERTIFICATE ERROR** If you get a certificate error you need to get `rhel.pem` from the kernel source. [Follow these instructions](https://unix.stackexchange.com/a/769359/240147)

**RANDOM ERRORS** I also had some random errors I think were due to race conditions. I just dropped it down to `make -j 10` and it worked.
