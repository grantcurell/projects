
- Download the NVIDIA Toolkit

You can get the NVIDIA toolkit from [here](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Rocky&target_version=9&target_type=runfile_local)

I used the rpm (network) version:

```bash
sudo dnf config-manager --add-repo https://developer.download.nvidia.com/compute/cuda/repos/rhel9/x86_64/cuda-rhel9.repo
sudo dnf clean all
sudo dnf -y install cuda-toolkit-12-5
```

- Download dependencies

```bash
sudo dnf groupinstall "Development Tools" "Development Libraries"
sudo dnf install cmake git libpng-devel libjpeg-devel jasper-devel openexr-devel libwebp-devel libtiff-devel tbb-devel libv4l-devel eigen3-devel python3 python3-devel python3-numpy python3-pip
sudo dnf install mesa-libGL mesa-libGL-devel
```

- Clone the repositories

```bash
git clone --recursive https://github.com/opencv/opencv.git
git clone --recursive https://github.com/opencv/opencv_contrib.git
cd opencv
mkdir build
cd build
```

- Configure CMake with CUDA Support
    - Note: I wasn't use `OPENCV_DNN_CUDA` so I turned it off. Apparently [it is bugged in current versions](https://github.com/opencv/opencv/issues/25426)

```bash
cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
      -D WITH_CUDA=ON \
      -D CUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda \
      -D OPENCV_DNN_CUDA=OFF \
      -D ENABLE_FAST_MATH=1 \
      -D CUDA_FAST_MATH=1 \
      -D WITH_CUBLAS=1 \
      -D BUILD_opencv_cudacodec=OFF \
      ..
```

- Build and install

```bash
make -j$(nproc)
sudo make install
sudo ldconfig
```

# New Instructions

```bash
# Install Toolkit
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-5

# Install Dependencies
sudo apt install -y build-essential cmake pkg-config unzip yasm git checkinstall \
libjpeg-dev libpng-dev libtiff-dev \
libavcodec-dev libavformat-dev libswscale-dev \
libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev \
libxvidcore-dev x264 libx264-dev libfaac-dev libmp3lame-dev libtheora-dev libvorbis-dev \
libopencore-amrnb-dev libopencore-amrwb-dev \
libxine2-dev libv4l-dev v4l-utils \
libgtk-3-dev \
python3-dev python3-pip python3-testresources \
libtbb-dev \
libatlas-base-dev gfortran \
libprotobuf-dev protobuf-compiler \
libgoogle-glog-dev libgflags-dev \
libgphoto2-dev libeigen3-dev libhdf5-dev doxygen
cd /usr/include/linux && sudo ln -s -f ../libv4l1-videodev.h videodev.h && cd ~ && \
sudo -H pip3 install -U pip numpy

# Download opencv
OPENCV_VERSION=4.10.0

cd ~/Downloads
wget -O opencv.zip https://github.com/opencv/opencv/archive/refs/tags/${OPENCV_VERSION}.zip
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/refs/tags/${OPENCV_VERSION}.zip
unzip opencv.zip
unzip opencv_contrib.zip

echo "Create a virtual environment for the Python binding module (OPTIONAL)"
sudo pip install virtualenv virtualenvwrapper
sudo rm -rf ~/.cache/pip
echo "Edit ~/.bashrc"
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv cv -p python3
pip install numpy

echo "Proceed with the installation"
cd opencv-${OPENCV_VERSION}
mkdir build
cd build

cmake \
    -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=$(python3 -c "import sys; print(sys.prefix)") \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D INSTALL_C_EXAMPLES=ON \
    -D WITH_TBB=ON \
    -D WITH_CUDA=OFF \
    -D BUILD_opencv_cudacodec=OFF \
    -D ENABLE_FAST_MATH=1 \
    -D CUDA_FAST_MATH=1 \
    -D WITH_CUBLAS=1 \
    -D WITH_V4L=ON \
    -D WITH_QT=OFF \
    -D WITH_OPENGL=ON \
    -D WITH_GSTREAMER=ON \
    -D OPENCV_GENERATE_PKGCONFIG=ON \
    -D OPENCV_PC_FILE_NAME=opencv.pc \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D OPENCV_PYTHON3_INSTALL_PATH=$(python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") \
    -D OPENCV_EXTRA_MODULES_PATH=/tmp/opencv_contrib/modules \
    -D PYTHON_EXECUTABLE=$(which python3) \
    -D BUILD_EXAMPLES=ON ..
```