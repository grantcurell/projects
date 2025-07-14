
Before building, I had to modify the file `src/gemdyn/CMakeLists.txt` and change it to the below. All that is doing is adding the line `include_directories(BEFORE $ENV{FFTW_HOME}/include)`. I had to add that to get FFTW to compile.

```
cmake_minimum_required(VERSION 3.14)

message(STATUS "(EC) Generating gemdyn Makefile")

# -----------------------------------------------------------------------------
# Added so every target (including the one that compiles fftw3.F90) can see the
# Fortran‑2003 interface file fftw3.f03 without relying on per‑target flags.
# The environment variable FFTW_HOME must point to your OpenMP‑enabled FFTW
# installation, e.g.  export FFTW_HOME=$HOME/fftw-openmp
# -----------------------------------------------------------------------------
include_directories(BEFORE $ENV{FFTW_HOME}/include)

#----- Append EC specific module path
list(APPEND CMAKE_MODULE_PATH $ENV{EC_CMAKE_MODULE_PATH} ${CMAKE_SOURCE_DIR}/cmake_rpn/modules)

include(ec_init)           # Initialise compilers and ec specific functions
ec_git_version()           # Get version from git state
ec_parse_manifest()        # Parse MANIFEST file

project(${NAME} DESCRIPTION "${DESCRIPTION}" LANGUAGES C Fortran)
set(PROJECT_VERSION ${VERSION}${STATE})
set(gemdyn_VERSION ${PROJECT_VERSION} CACHE INTERNAL "gemdyn version" FORCE) # Needed for cascaded version identification
message(STATUS "(EC) ${PROJECT_NAME} version = ${PROJECT_VERSION}")

ec_build_info()            # Generate build information
include(ec_compiler_presets)

# To build without OpenMP, you have to add -DWITH_OPENMP=FALSE to the cmake command line
set(WITH_OPENMP TRUE CACHE BOOL "Control whether to use OpenMP")
include(ec_openmp)

if (NOT rmn_FOUND)
  find_package(rmn ${rmn_REQ_VERSION} COMPONENTS static REQUIRED)
endif()

if (NOT rpncomm_FOUND)
  find_package(rpncomm ${rpncomm_REQ_VERSION} REQUIRED)
endif()

if (NOT tdpack_FOUND)
  find_package(tdpack ${tdpack_REQ_VERSION} COMPONENTS static REQUIRED)
endif()

if (NOT vgrid_FOUND)
  find_package(vgrid ${vgrid_REQ_VERSION} COMPONENTS static REQUIRED)
endif()

# Adding specific flags for gemdyn
if (("${CMAKE_Fortran_COMPILER_ID}" STREQUAL "Intel") AND NOT ("${CMAKE_SYSTEM_NAME}" STREQUAL "CrayLinuxEnvironment"))
  if(CMAKE_Fortran_COMPILER_VERSION VERSION_GREATER 2021)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -qmkl")
    set(CMAKE_Fortran_FLAGS "${CMAKE_Fortran_FLAGS} -qmkl -static-intel -diag-disable 5268")
    set(CMAKE_EXE_LINKER_FLAGS_INIT "${CMAKE_EXE_LINKER_FLAGS_INIT} -qmkl")
  else()
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -mkl")
    set(CMAKE_Fortran_FLAGS "${CMAKE_Fortran_FLAGS} -mkl -static-intel -diag-disable 5268")
    set(CMAKE_EXE_LINKER_FLAGS_INIT "${CMAKE_EXE_LINKER_FLAGS_INIT} -mkl")
  endif()
elseif("${CMAKE_Fortran_COMPILER_ID}" STREQUAL "GNU")
  find_package(LAPACK)
  find_package(BLAS)
endif()

string(TIMESTAMP BUILD_DATE "%Y-%m-%d %H:%M")
if(DEFINED ENV{COMP_ARCH})
  set(EC_COMPILER "$ENV{COMP_ARCH}")
endif()
if(DEFINED ENV{ORDENV_ARCH})
  set(EC_ORDENV_ARCH "$ENV{ORDENV_ARCH}")
endif()
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/src/main/maincheckdmpart.in ${CMAKE_CURRENT_SOURCE_DIR}/src/main/maincheckdmpart.F90)
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/src/main/maingemgrid.in ${CMAKE_CURRENT_SOURCE_DIR}/src/main/maingemgrid.F90)

add_subdirectory(src/no_mpi gemdyn-no_mpi)
add_subdirectory(src gemdyn)
add_subdirectory(src/main gemdyn-main)

ec_build_config()                 # Create build configuration script
```



```bash
# Build git first
cd ~
curl -O https://mirrors.edge.kernel.org/pub/software/scm/git/git-2.43.0.tar.gz
tar -xzf git-2.43.0.tar.gz
cd git-2.43.0

make prefix=$HOME/.local/git all
make prefix=$HOME/.local/git install

# Add to your path
echo 'export PATH=$HOME/.local/git/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

## Build fftw
cd ~
wget http://www.fftw.org/fftw-3.3.10.tar.gz
tar -xzf fftw-3.3.10.tar.gz
cd fftw-3.3.10

./configure --prefix=$HOME/fftw-openmp --enable-openmp --enable-shared --enable-fortran
make -j$(nproc)
make install


# Compiling
module purge
module load gcc/13.1.0
module load openmpi/gcc/64/4.1.5
module load blas/gcc/64/3.11.0
module load lapack/gcc/64/3.11.0
module load hdf5/1.14.0
module load netcdf/gcc/64/gcc/64/4.9.2
. ./.common_setup gnu
mkdir build
cd bulid
export FFTW_HOME=$HOME/fftw-openmp                
cmake ..   -DCMAKE_PREFIX_PATH=$FFTW_HOME   -DFFTW_ROOT=$FFTW_HOME   -DCMAKE_Fortran_FLAGS="-I$FFTW_HOME/include -O2 -Wno-error" && make VERBOSE=1 2>&1 | tee /tmp/build.log
make -j${nproc}

```