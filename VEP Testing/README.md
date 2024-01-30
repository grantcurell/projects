# VEP Testing

1. Unscrew the tiny panel on the back. Underneath is microUSB. Plug in.
2. Bring up device manager. Look at ports. After the automatic driver installation a port should appear there with notation *Silicon Labs CP210x USB to UART Bridge (COMX)*. This is what you want to connect to
3. Open putty set to serial with speed 115200 and COM<YOUR_NUMBER>
4. You will need to download ESXi from the Dell website using your serial number. This is very important as the ESXi installation has unique drivers injected into it for your convienience. You could load vanilla ESXi and load the drivers yourself.
5. Burn ESXi to a flash drive using Rufus and plug it into the side of the VEP.
6. Power cycle the VEP and hit delete when prompted to open the firmware screen.
7. Set the flash drive as the highest priority for boot and then save and exit.
8. Install ESXi normally via the serial console.