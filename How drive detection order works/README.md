# How It Works

1. BIOS initializes the hardware done in some order defined by the BIOS (or less euphemistically, UEFI in 2024). Usually, this follows whatever the priority settings are in BIOS or some firmware default.

2. BIOS reads the EFI system partition, finds the bootloader, fires up the bootloader, which then boots the kernel, which then probes all the devices itself, runs what's called the probe routine, which in turn loads the appropriate driver.

3. After the kernel detects the devices, `udev` takes over and it is `udev` which then populates `/dev` in the filesystem tree that you're used to seeing.

4. `udev` is the reason that names are consistent after you install the OS and correspondingly the reason they aren't consistent before you build the OS. `udev` sets rules to make sure that the same drive always gets the same name. For example, on my system, I don't even have a `/dev/sda`; I have `/dev/nvme0n1` and you can see the DEVNAME gets tied specifically to that via this `udev` entry:
    ```shell
    grant@linux-desktop:~$ udevadm info --query=all --name=/dev/nvme0n1
    P: /devices/pci0000:00/0000:00:0e.0/pci10000:e0/10000:e0:06.0/10000:e1:00.0/nvme/nvme0/nvme0n1
    N: nvme0n1
    L: 0
    S: disk/by-id/nvme-KXG70PNV2T04_NVMe_KIOXIA_2048GB_12KFC0BAFTW5
    S: disk/by-id/nvme-KXG70PNV2T04_NVMe_KIOXIA_2048GB_12KFC0BAFTW5_1
    S: disk/by-path/pci-0000:00:0e.0-pci-10000:e1:00.0-nvme-1
    S: disk/by-id/nvme-eui.00000000000000008ce38e0500a69153
    E: DEVPATH=/devices/pci0000:00/0000:00:0e.0/pci10000:e0/10000:e0:06.0/10000:e1:00.0/nvme/nvme0/nvme0n1
    E: DEVNAME=/dev/nvme0n1
    E: DEVTYPE=disk
    E: DISKSEQ=9
    E: MAJOR=259
    E: MINOR=0
    E: SUBSYSTEM=block
    E: USEC_INITIALIZED=1741074
    E: ID_SERIAL_SHORT=12KFC0BAFTW5
    E: ID_WWN=eui.00000000000000008ce38e0500a69153
    E: ID_MODEL=KXG70PNV2T04 NVMe KIOXIA 2048GB
    E: ID_REVISION=10904107
    E: ID_NSID=1
    E: ID_SERIAL=KXG70PNV2T04_NVMe_KIOXIA_2048GB_12KFC0BAFTW5_1
    E: ID_PATH=pci-0000:00:0e.0-pci-10000:e1:00.0-nvme-1
    E: ID_PATH_TAG=pci-0000_00_0e_0-pci-10000_e1_00_0-nvme-1
    E: ID_PART_TABLE_UUID=f568a189-cada-4d93-84aa-02c801567f50
    E: ID_PART_TABLE_TYPE=gpt
    E: DEVLINKS=/dev/disk/by-id/nvme-KXG70PNV2T04_NVMe_KIOXIA_2048GB_12KFC0BAFTW5 /dev/disk/by-id/nvme-KXG70PNV2T04_NVMe_KIOXIA_2048GB_12KFC0BAFTW5_1 /dev/disk/by-path/pci-0000:00:0e.0-pci-10000:e1:00.0-nvme-1 /dev/disk/by-id/nvme-eui.00000000000000008ce38e0500a69153
    E: TAGS=:systemd:
    E: CURRENT_TAGS=:systemd:
    ```

5. Modern OSs do not use `/dev*` for internal identification. Most (things now use a UUID. For example, if you go look at your GRUB config (`/boot/grub/grub.cfg`) this is what you'll see:
    ```plaintext
    menuentry 'Ubuntu' --class ubuntu --class gnu-linux --class gnu --class os $menuentry_id_option 'gnulinux-simple-1705d156-9547-4167-b99f-5a451b2d76cf' {
        recordfail
        load_video
        gfxmode $linux_gfx_mode
        insmod gzio
        if [ x$grub_platform = xxen ]; then insmod xzio; insmod lzopio; fi
        insmod part_gpt
        insmod ext2
        search --no-floppy --fs-uuid --set=root 1705d156-9547-4167-b99f-5a451b2d76cf
        linux /boot/vmlinuz-6.5.0-41-generic root=UUID=1705d156-9547-4167-b99f-5a451b2d76cf ro quiet splash $vt_handoff
        initrd /boot/initrd.img-6.5.0-41-generic
    ```

6. Which you can see directly ties to the partition UUID:
    ```shell
    grant@linux-desktop:~$ blkid
    /dev/nvme1n1p3: UUID="1705d156-9547-4167-b99f-5a451b2d76cf" BLOCK_SIZE="4096" TYPE="ext4" PARTUUID="50b9c87c-e57f-44e3-ac4d-4849f455b4f6"
    ```

7. If you want to be able to consistently reference some particularly drive in your kickstart you can do something like the  below in your %pre section. This logic selects the largest drive, replace the logic as appropriate for whatever unique criteria you want to use.
    ```shell
    # Installation to the largest drive
    %pre --interpreter=/bin/bash

    # Find the largest drive by capacity
    largest_drive=$(lsblk -bnd -o NAME,SIZE,TYPE | awk '$3=="disk"{print $1, $2}' | sort -k2 -n | tail -1 | cut -d' ' -f1)

    # Get the unique ID of the largest drive
    drive_id=$(ls -l /dev/disk/by-id/ | grep $largest_drive | head -1 | awk '{print $9}')

    # Export the drive_id for use in the %post section
    echo "drive_id=$drive_id" > /tmp/drive_id

    %end
    ```

8. Then in the main section reference the `$drive_id` variable (replace with however you are formatting the drives):
    ```shell
    # Use the identified drive for partitioning and installation
    %include /tmp/drive_id

    part / --fstype=ext4 --size=1 --grow --ondisk=${drive_id}
    part /boot --fstype=ext4 --size=500 --ondisk=${drive_id}
    part swap --size=2048 --ondisk=${drive_id}
    ```
