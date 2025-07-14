```bash
#!/bin/bash

# Comprehensive script to remove -fallow-argument-mismatch from ALL compiler flags
# This will prevent the flag from being added to C compilation

echo "Removing -fallow-argument-mismatch from ALL compiler flags..."

# Find all cmake files containing the problematic flag
files=$(grep -r -l "fallow-argument-mismatch" --include="*.cmake" . 2>/dev/null)

if [ -z "$files" ]; then
    echo "No files found containing -fallow-argument-mismatch"
    exit 0
fi

count=$(echo "$files" | wc -l)
echo "Found $count files containing the flag"

# Process each file
echo "$files" | while read -r file; do
    if [ -f "$file" ]; then
        echo "Processing: $file"

        # Create a backup
        cp "$file" "$file.backup"

        # Remove the flag from ALL compiler flags (not just Fortran)
        sed -i 's/-fallow-argument-mismatch//g' "$file"

        echo "  - Updated $file"
    fi
done

echo "Done! All instances of -fallow-argument-mismatch have been removed."
echo "You can now try building again."
echo ""
echo "To restore the files later, run: find . -name '*.cmake.backup' -exec bash -c 'cp \"{}\" \"\${1%.backup}\"' _ {} \;"
```

```bash
#!/usr/bin/env bash
#
# Usage: ./submit_gem_bench_opt.sh <node_count> <ptopo>
# Example: ./submit_gem_bench_opt.sh 29 "58x48x1"
#
# This script is used to submit a job to the cluster to run the GEM model with the given node count and topology.
# It will run the model and save the output to a job directory.
# The job directory will be named with the job ID, node count, topology, and grid_nj such as job_123456_nodes-29_58x48x1_1000.
# The job directory will be created in the job_outputs directory.
# The job directory will contain the submit script, environment variables, and output files.
# The job directory will contain the gem_settings.nml file.
#
# Check if arguments are provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 <node_count> <ptopo>"
    echo "Example: $0 29 \"58x48x1\""
    exit 1
fi

NODE_COUNT=$1
PTOPO=$2

# Validate inputs
if ! [[ "$NODE_COUNT" =~ ^[0-9]+$ ]]; then
    echo "Error: node_count must be a positive integer"
    exit 1
fi

if ! [[ "$PTOPO" =~ ^[0-9]+x[0-9]+x[0-9]+$ ]]; then
    echo "Error: ptopo must be in format NxNxN (e.g., 58x48x1)"
    exit 1
fi

# Create job directory structure first if it doesn't exist
if [ ! -d "job_outputs" ]; then
    echo "Creating job_outputs directory..."
    mkdir -p "job_outputs"
else
    echo "job_outputs directory already exists"
fi

# Create a temporary job directory name (we'll rename it after getting job ID)
TEMP_JOB_DIR="job_outputs/job_temp_${NODE_COUNT}_${PTOPO}"
mkdir -p "$TEMP_JOB_DIR"

# Create a temporary SLURM script with the correct node count
TEMP_SCRIPT=$(mktemp)
cat > "$TEMP_SCRIPT" << EOF
#!/usr/bin/env bash
#SBATCH -N $NODE_COUNT
#SBATCH -p normal
#SBATCH --job-name=gem-itq-bench
#SBATCH --time=3:00:00
#SBATCH --ntasks-per-node=128
#SBATCH --cpus-per-task=1
#SBATCH --mem=0
#SBATCH --exclusive
#SBATCH --no-requeue
#SBATCH --output=job_outputs/job_temp_${NODE_COUNT}_${PTOPO}/slurm.out
#SBATCH --error=job_outputs/job_temp_${NODE_COUNT}_${PTOPO}/slurm.err

# Define DIR early so it's available for file paths
DIR=\$PWD

module purge
module load autotools/1.4   pmix/3.2.3   xalt/3.1   TACC   gcc/13.2.0  impi/21.12    fftw3/3.3.10   cmake/3.29.5   mkl/24.1
#export EXTRA_MPI_PARMS="-bind-to core -report-bindings"
export RMN_SINGLE_READER_BCAST=1
export RMN_BCAST_CHUNK_MB=16
export PRTE_MCA_prte_tmpdir_base="/tmp"
export OMP_NUM_THREADS=\$SLURM_CPUS_PER_TASK
export OMP_PLACES=cores
export OMP_PROC_BIND=spread
export FFTW_MEASURE=0               # keep FFTW plans lightweight
export OMP_STACKSIZE=4G

#export I_MPI_DEBUG=4
#export I_MPI_HYDRA_BOOTSTRAP=ssh
#export I_MPI_HYDRA_DEBUG=1
export FI_LOG_LEVEL=error
export OMPI_MCA_pml=ucx
export OMPI_MCA_coll_hcoll_enable=0
ulimit -s unlimited

# Source GEM setup early to get \$GEM_WORK variable
pushd gem
. .common_setup gnu
popd

# Extract Grd_nj value from gem_settings.nml using \$GEM_WORK
GEM_SETTINGS_FILE="\$DIR/gem/\$GEM_WORK/configurations/GEM_cfgs_GY_4km/cfg_0000/gem_settings.nml"
GRD_NJ=\$(grep "Grd_nj" "\$GEM_SETTINGS_FILE" | awk '{print \$3}' | tr -d ',')

# Rename the temporary job directory to include job ID and grid_nj
JOB_DIR="job_outputs/job_\${SLURM_JOB_ID}_nodes-${NODE_COUNT}_${PTOPO}_\${GRD_NJ}"
TEMP_JOB_DIR="job_outputs/job_temp_${NODE_COUNT}_${PTOPO}"

# Rename the directory
echo "Current directory: \$(pwd)"
echo "TEMP_JOB_DIR: \$TEMP_JOB_DIR"
echo "JOB_DIR: \$JOB_DIR"
ls -la job_outputs/

if [ -d "\$TEMP_JOB_DIR" ]; then
    mv "\$TEMP_JOB_DIR" "\$JOB_DIR"
    echo "Successfully renamed \$TEMP_JOB_DIR to \$JOB_DIR"
else
    echo "ERROR: Temporary job directory \$TEMP_JOB_DIR not found"
    exit 1
fi

# Copy the submit script to the job directory
cp "\$0" "\$JOB_DIR/submit_script.sh"

echo "Job \$SLURM_JOB_ID started at \$(date)"
echo "Job directory: \$JOB_DIR"
echo "Nodes: ${NODE_COUNT}, Topology: ${PTOPO}, Grid_nj: \$GRD_NJ"
echo "FFTW_MEASURE = \$FFTW_MEASURE"
env  > "\$JOB_DIR/environment.log"

pushd gem
. .common_setup gnu
pushd \$GEM_WORK
export LOG_LEVEL='DEBUG'

# Copy gem settings to job directory using \$GEM_WORK
if [ -f "\$DIR/gem/\$GEM_WORK/configurations/GEM_cfgs_GY_4km/cfg_0000/gem_settings.nml" ]; then
    cp "\$DIR/gem/\$GEM_WORK/configurations/GEM_cfgs_GY_4km/cfg_0000/gem_settings.nml" "\$JOB_DIR/gem_settings.nml"
    echo "Copied gem_settings.nml to \$JOB_DIR/gem_settings.nml"
else
    echo "WARNING: gem_settings.nml file not found at expected location: \$DIR/gem/\$GEM_WORK/configurations/GEM_cfgs_GY_4km/cfg_0000/gem_settings.nml"
fi

runprep.sh -dircfg configurations/GEM_cfgs_GY_4km

# Run the model and save output to job directory
runmod.sh -dircfg configurations/GEM_cfgs_GY_4km -ptopo ${PTOPO} 2>&1 | tee "\$JOB_DIR/runlog.txt"

echo "Job \$SLURM_JOB_ID completed at \$(date)"
echo "All output files saved in: \$JOB_DIR"
EOF

# Submit the temporary script
echo "Submitting job with $NODE_COUNT nodes and topology $PTOPO"
sbatch "$TEMP_SCRIPT"

# Clean up the temporary script
rm "$TEMP_SCRIPT"
```