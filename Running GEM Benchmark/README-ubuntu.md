Here's the Ubuntu-compatible version of your instructions. This assumes you're using Ubuntu 20.04+:

---

### Enable Universe and Multiverse Repositories (Ubuntu's equivalent of EPEL/CRB)

```bash
sudo add-apt-repository universe
sudo add-apt-repository multiverse
sudo apt update
```

---

### Install Development Tools and General Build Dependencies

```bash
sudo apt install -y \
  build-essential \
  gfortran \
  cmake \
  git \
  make \
  pkgconf \
  libexpat1-dev \
  texinfo \
  doxygen \
  libxml2-dev \
  libfftw3-dev \
  libnetcdf-dev \
  libnetcdff-dev \
  libhdf5-dev \
  libblas-dev \
  liblapack-dev
```

---

### Install MPI (OpenMPI)

```bash
sudo apt install -y openmpi-bin libopenmpi-dev
```

OpenMPI will already be in your path on Ubuntu. If needed:

```bash
echo 'export PATH=/usr/lib/x86_64-linux-gnu/openmpi/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/openmpi/lib:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
```

---

### Install `librmn`

```bash
cd ~
git clone https://github.com/ECCC-ASTD-MRD/librmn.git
cd librmn
git checkout alpha
git submodule update --init --recursive

mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=$HOME/librmn-install ..
make -j$(nproc)
make install
```

---

### Install `sverif`

```bash
cd ~
git clone https://github.com/ECCC-ASTD-MRD/sverif.git
cd sverif
git submodule update --init --recursive

mkdir build
cd build
cmake -Drmn_ROOT=$HOME/librmn-install -DCMAKE_INSTALL_PREFIX=$HOME/sverif-install ..
make -j$(nproc)
make install
```

Add to `PATH` permanently:

```bash
echo 'export PATH=$HOME/sverif-install/bin:$PATH' >> ~/.bashrc
export PATH=$HOME/sverif-install/bin:$PATH
```

---

Let me know if you want to include a section on testing the install.
