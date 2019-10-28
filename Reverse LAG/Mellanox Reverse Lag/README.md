# Mellanox Reverse Lag Config

# Setup Notes

I had to plug the console cable into a specific USB slot on the server. It didn't
work in the first one I tried. See picture below.

![](USB_location.JPG)

# Running Updates

1. I pulled updates [here](https://mymellanox.force.com/support/SupportProductItem?id=a2v50000000JhmwAAC)
2. The system uses a web server target for updates. I had Apache running on a RHEL 8 box.
3. Download the update file and then upload it to your web server's root directory.
4. On the switch itself (over a console port) do the following:

        switch > enable
        switch # configure terminal
        switch (config) # show images

        # Delete the old image if it exists. It will be under
        # "Images available to be installed"

        switch (config) # image delete <old_image>