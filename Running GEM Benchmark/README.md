
## What is Global Environmental Multiscale (GEM) model

- [What is Global Environmental Multiscale (GEM) model](#what-is-global-environmental-multiscale-gem-model)
- [Background](#background)
  - [What are we doing here?](#what-are-we-doing-here)
  - [How are we going to do that?](#how-are-we-going-to-do-that)
  - [Ok, but **how** does GEM do that?](#ok-but-how-does-gem-do-that)
- [Install Prereqs](#install-prereqs)
- [Install](#install)


## Background

### What are we doing here?

Given how heady weather is, I think it's best to start with a problem statement that gets at the heart of what GEM does.

> Given the current state of the atmosphere, what will be the future weather hours or weeks from now across different parts of the world.

### How are we going to do that?

We collect a bunch of observational data from different sources - satellites, weather balloons, surface stations, radar, aircraft - all sorts of stuff - we shove it all into a big equation and then we guess. This is called numerical weather prediction.

### Ok, but **how** does GEM do that?

> NUMERICAL TECHNIQUES
> - Horizontal variable-resolution cell-integrated finite-element discretization reducing to the usual staggered finite differences discretization at uniform resolution in spherical geometry.
> - Semi-implicit semi-Lagrangian time discretization scheme which removes the overly- restrictive time step limitation imposed by the use of a more conventional Eulerian scheme.
> - Hydrostatic-pressure-type hybrid vertical coordinate.

Clear? If your reaction was like mine, probably not. I spent a lot of time reading to wrap my head around this so I'll break it down for you.

> "Horizontal variable-resolution cell-integrated finite-element discretization"

The model breaks the land and atmosphere into grid cells, like tiles on a map — but the cells can be smaller where you want more detail, like over mountains or cities, and larger where less precision is fine, like over the open ocean. *Cell-integrated* means we calculate the averages over each tile. You can imagine that over the tile there are all sorts of different values, but ultimately, while it reduces our accuracy a bit, we can instead take the average of all of them and use that. Obviously, the smaller the tile, the more accurate we get. *Finite-element* is a method for solving equations. If we have some irregular shape, we break it down into several simple shapes - e.g. a triangle. Once we have a bunch of triangles, we then solve the equation for each of those triangles instead, then we connect all  the pieces together, and then solve those simple equations.

> "the usual staggered finite differences discretization"

Ah yes, *the usual*. Usual here being subjective. Ok, this is a lot of math speak that basically means we would usually do a bunch of partial differentials to calculate the value. The problem is that calculating partial derivatives is expensive. What we do instead is look at all the weather and instead of calculating derivatives, we just look at what is happening nearby and calculate the delta between two points. While this is less accurate than calculating the derivative it is much faster.

> "in spherical geometry"

This one is a bit more straightforward. The Earth isn't flat (probably). GEM's math has to account for that. Ex: if wind is blowing long distances it has to curve; it doesn't blow straight.

> "Semi-implict semi-Lagrangian time discretization scheme"



## Install Prereqs

```bash
# Enable EPEL and CRB (or PowerTools) repository
sudo dnf install -y epel-release
sudo dnf config-manager --set-enabled crb || sudo dnf config-manager --set-enabled powertools

# Install development tools and common build utilities
sudo dnf groupinstall -y "Development Tools"
sudo dnf install -y \
  gcc \
  gcc-c++ \
  gcc-gfortran \
  cmake \
  git \
  make \
  pkgconf \
  which \
  expat \
  expat-devel \
  texinfo \
  doxygen \
  libxml2-devel \
  fftw-devel


# Install MPI (OpenMPI)
sudo dnf install -y openmpi openmpi-devel

# Load MPI paths into shell (optional but helpful)
echo 'export PATH=/usr/lib64/openmpi/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/lib64/openmpi/lib:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc

# Install NetCDF and HDF5 libraries
sudo dnf install -y \
  netcdf \
  netcdf-devel \
  netcdf-fortran \
  netcdf-fortran-devel \
  hdf5 \
  hdf5-devel

# Install math libraries (optional)
sudo dnf install -y \
  blas \
  blas-devel \
  lapack \
  lapack-devel

```

## Install

```bash
##################
# Install librmn #
##################
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

##################
# Install sverif #
##################
cd ~
git clone https://github.com/ECCC-ASTD-MRD/sverif.git
cd sverif
git submodule update --init --recursive

mkdir build
cd build
cmake -Drmn_ROOT=$HOME/librmn-install -DCMAKE_INSTALL_PREFIX=$HOME/sverif-install ..
make -j$(nproc)
make install

# Add sverif binaries to your path
export PATH=$HOME/sverif-install/bin:$PATH
echo 'export PATH=$HOME/sverif-install/bin:$PATH' >> ~/.bashrc

###############
# Install GEM #
###############
cd ~
git clone https://github.com/ECCC-ASTD-MRD/gem.git
cd gem
git checkout benchmark-5.3
git submodule update --init --recursive

# Download reference databases
./download-dbase.sh .
./download-dbase-benchmarks.sh .

# Set up environment (choose one of: intel | gnu | nvhpc)
. ./.common_setup gnu

# Build GEM
mkdir build
cd build
cmake ..
make -j$(nproc)
make work

```