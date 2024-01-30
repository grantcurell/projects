# How OS10 Installer Works

The OS10 installer is a binary file with a bash stub:

``` bash
#!/bin/sh

#######################################################################
# Dell OS10 Installer
#######################################################################

#######################################################################
# OS10 Data
export OS_NAME="Dell EMC Networking OS10 Enterprise"
export OS_VERSION="10.5.2.7"
export PLATFORM="generic-x86_64"
export ARCHITECTURE="x86_64"
export INTERNAL_BUILD_ID="Dell EMC OS10 Enterprise Edition Blueprint 1.0.0"
export BUILD_VERSION="10.5.2.7.374"
export BUILD_DATE="2021-07-28T04:48:06+0000"
#######################################################################

# Magic cookies for OS10 feature detection. DO NOT CHANGE!
# !OS10!1PART!

# Enable error handling
set -e

INSTALLER=$(realpath "$0")
TMP_DIR=$(mktemp -d)

cd $TMP_DIR

# Extract installer scripts
echo -n "Initializing installer ... "
sed -e '1,/^__INSTALLER__$/d;/^__IMAGE__$/,$d' "$INSTALLER" |
    base64 -d | tar xzf -
echo "OK"

# Load the installer library files
cd installer
. install_support.sh

install_main "$@"
rc="$?"

exit $rc

__INSTALLER__
<BASE_64_ENCODED_INSTALLER>

__IMAGE__
<BINARY_IMAGE_HERE>
```

What this does is grab the installer's name with `INSTALLER=$(realpath "$0")` and then extracts itself with `sed -e '1,/^__INSTALLER__$/d;/^__IMAGE__$/,$d' "$INSTALLER" | base64 -d | tar xzf -`. This grabs everything between the __INSTALLER__ and __IMAGE__ tags, base64 decodes it, and then extracts it with tar.