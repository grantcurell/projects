#!/usr/bin/env bash
#
# Usage: ./submit_gem_bench_opt.sh <node_count> <ptopo> [gr_nj_value]
# Example: ./submit_gem_bench_opt.sh 29 "58x48x1" 896
# Example: ./submit_gem_bench_opt.sh 29 "58x48x1" (uses current gem_settings.nml)
#
# This script is used to submit a job to the cluster to run the GEM model with the given node count and topology.
# It will run the model and save the output to a job directory.
# The job directory will be named with the job ID, node count, topology, and grid_nj such as job_123456_nodes-29_58x48x1_1000.
# The job directory will be created in the job_outputs directory.
# The job directory will contain the submit script, environment variables, and output files.
# The job directory will contain the gem_settings.nml file.
#
# Check if arguments are provided
if [ $# -lt 2 ] || [ $# -gt 3 ]; then
    echo "Usage: $0 <node_count> <ptopo> [gr_nj_value]"
    echo "Example: $0 29 \"58x48x1\" 896"
    echo "Example: $0 29 \"58x48x1\" (uses current gem_settings.nml)"
    exit 1
fi

NODE_COUNT=$1
PTOPO=$2
GR_NJ_VALUE=$3

# Validate inputs
if ! [[ "$NODE_COUNT" =~ ^[0-9]+$ ]]; then
    echo "Error: node_count must be a positive integer"
    exit 1
fi

if ! [[ "$PTOPO" =~ ^[0-9]+x[0-9]+x[0-9]+$ ]]; then
    echo "Error: ptopo must be in format NxNxN (e.g., 58x48x1)"
    exit 1
fi

if [ ! -z "$GR_NJ_VALUE" ] && ! [[ "$GR_NJ_VALUE" =~ ^[0-9]+$ ]]; then
    echo "Error: gr_nj_value must be a positive integer"
    exit 1
fi

# Create job directory structure first if it doesn't exist
if [ ! -d "job_outputs" ]; then
    echo "Creating job_outputs directory..."
    mkdir -p "job_outputs"
else
    echo "job_outputs directory already exists"
fi

# Get the Gr_nj value for directory naming
if [ ! -z "$GR_NJ_VALUE" ]; then
    GR_NJ_FOR_DIR="$GR_NJ_VALUE"
else
    # Read from current gem_settings.nml
    GEM_SETTINGS_FILE="gem/$GEM_WORK/configurations/GEM_cfgs_GY_4km/cfg_0000/gem_settings.nml"
    if [ -f "$GEM_SETTINGS_FILE" ]; then
        GR_NJ_FOR_DIR=$(grep "Grd_nj" "$GEM_SETTINGS_FILE" | awk '{print $3}' | tr -d ',')
    else
        GR_NJ_FOR_DIR="unknown"
    fi
fi

# Create a temporary job directory name (we'll rename it after getting job ID)
TEMP_JOB_DIR="job_outputs/job_temp_${NODE_COUNT}_${PTOPO}_${GR_NJ_FOR_DIR}"
mkdir -p "$TEMP_JOB_DIR"

# Create a temporary SLURM script with the correct node count
TEMP_SCRIPT=$(mktemp)
cat > "$TEMP_SCRIPT" << EOF
#!/usr/bin/env bash
#SBATCH -N $NODE_COUNT
#SBATCH --job-name=gem-itq-bench
#SBATCH --time=3:00:00
#SBATCH --ntasks-per-node=192
#SBATCH --cpus-per-task=1
#SBATCH --mem=0
#SBATCH --exclusive
#SBATCH --no-requeue
#SBATCH --output=job_outputs/job_temp_${NODE_COUNT}_${PTOPO}_${GR_NJ_FOR_DIR}/slurm.out
#SBATCH --error=job_outputs/job_temp_${NODE_COUNT}_${PTOPO}_${GR_NJ_FOR_DIR}/slurm.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=davis.goodman@gmail.com

# Define DIR early so it's available for file paths
DIR=\$PWD

# Pass GR_NJ_VALUE from submit script
GR_NJ_VALUE=$GR_NJ_VALUE

module purge
module load gcc/13.3
module load fftw
# Pin specific versions to avoid conflicts
module load openmpi/5.0.3
module load ucx/1.16.0
module load libfabric/1.21.0

# Note: Compiler flags are applied during GEM build, not needed at runtime
#export EXTRA_MPI_PARMS="-map-by ppr:1:l3cache:pe=8 -bind-to core -report-bindings"
#export EXTRA_MPI_PARMS="-bind-to core -report-bindings"
export RMN_SINGLE_READER_BCAST=1
export RMN_BCAST_CHUNK_MB=16
export PRTE_MCA_prte_tmpdir_base="/tmp"
export OMP_NUM_THREADS=\$SLURM_CPUS_PER_TASK
export OMP_PLACES=cores
export OMP_PROC_BIND=spread
export FFTW_MEASURE=0               # keep FFTW plans lightweight
export OMP_STACKSIZE=4G

# Performance optimizations
export OMP_SCHEDULE=dynamic
export OMP_DYNAMIC=TRUE
export OMP_NESTED=TRUE
export OMP_MAX_ACTIVE_LEVELS=4
export OMP_THREAD_LIMIT=192

# Numerical stability improvements for high-resolution runs
export GEM_FP_EXCEPTIONS=ignore
export GEM_UNDERFLOW_ACTION=continue
export GEM_DENORMAL_ACTION=flush_to_zero
export GEM_NUMERICAL_PRECISION=double
export GEM_UNDERFLOW_HANDLING=strict
export GEM_DENORMAL_HANDLING=flush_to_zero
export GEM_FLOATING_POINT_EXCEPTIONS=ignore
export GEM_NUMERICAL_STABILITY=enhanced
 
# Enhanced MPI and network stability settings
export I_MPI_DEBUG=4
export I_MPI_HYDRA_BOOTSTRAP=ssh
export I_MPI_HYDRA_DEBUG=1
export FI_LOG_LEVEL=error
export FLEXIBLAS=aocl
export OMPI_MCA_pml=ucx
export OMPI_MCA_coll_hcoll_enable=0

# PRTE stability improvements
export PRTE_MCA_prte_tmpdir_base="/tmp"
export PRTE_MCA_prte_ess_base_verbose=5
export PRTE_MCA_prte_ess_tool_verbose=5
export PRTE_MCA_prte_ess_hnp_verbose=5
export PRTE_MCA_prte_ess_hnp_uri=file:///tmp/prte_uri_\$SLURM_JOB_ID
export PRTE_MCA_prte_ess_hnp_uri_file=/tmp/prte_uri_\$SLURM_JOB_ID
export PRTE_MCA_prte_ess_hnp_uri_file_cleanup=1
export PRTE_MCA_prte_ess_hnp_uri_file_cleanup_delay=10
export PRTE_MCA_prte_ess_hnp_uri_file_cleanup_retries=3
export PRTE_MCA_prte_ess_hnp_uri_file_cleanup_timeout=30
export PRTE_MCA_prte_ess_hnp_uri_file_cleanup_verbose=5

# UCX network stability settings for HDR200 with blocking ratio
export UCX_NET_DEVICES=mlx5_0:1
export UCX_TLS=rc,ud,sm
export UCX_RC_TIMEOUT=120s
export UCX_RC_RETRY_COUNT=7
export UCX_RNDV_THRESH=64k
export UCX_RNDV_SEND_THRESH=64k
export UCX_RNDV_RECV_THRESH=64k
export UCX_RC_FC_ENABLE=y
export UCX_RC_FC_WINDOW=8192
export UCX_WARN_UNUSED_ENV_VARS=n
# Additional MPI stability settings for HDR200 with blocking ratio
export OMPI_MCA_btl_openib_allow_ib=1
export OMPI_MCA_btl_openib_ib_timeout=60
export OMPI_MCA_btl_openib_ib_retry_count=15
export OMPI_MCA_btl_openib_ib_max_qp=2048
export OMPI_MCA_btl_openib_ib_max_cq=2048
export OMPI_MCA_btl_openib_ib_max_srq=2048
export OMPI_MCA_btl_openib_ib_max_send_wr=2048
export OMPI_MCA_btl_openib_ib_max_recv_wr=2048
export OMPI_MCA_btl_openib_ib_max_send_sge=2048
export OMPI_MCA_btl_openib_ib_max_recv_sge=2048
export OMPI_MCA_btl_openib_ib_max_inline_data=0
export OMPI_MCA_btl_openib_ib_rdmacm=1
export OMPI_MCA_btl_openib_ib_use_eager_rdma=1
export OMPI_MCA_btl_openib_ib_connect_timeout=60
export OMPI_MCA_btl_openib_ib_connect_retries=10
export OMPI_MCA_btl_openib_ib_connect_backoff=2
export OMPI_MCA_btl_openib_ib_connect_backoff_max=30

# Memory and process limits (make them optional to avoid permission errors)
ulimit -s unlimited 2>/dev/null || echo "Warning: Could not set stack size limit"
ulimit -n 65536 2>/dev/null || echo "Warning: Could not set file descriptor limit"

# Memory management optimizations
export MALLOC_TRIM_THRESHOLD_=131072
export MALLOC_MMAP_THRESHOLD_=131072
export MALLOC_MMAP_MAX_=65536

# Set floating-point environment for numerical stability
export FPU_MODE=strict
export FPU_PRECISION=double
export FPU_ROUNDING=nearest
export FPU_EXCEPTIONS=ignore

# Network diagnostics and cleanup
echo "=== Network Diagnostics ==="
echo "Job ID: \$SLURM_JOB_ID"
echo "Nodes: \$SLURM_NODELIST"
echo "Node count: \$SLURM_NNODES"
echo "Tasks per node: \$SLURM_NTASKS_PER_NODE"
echo "Total tasks: \$SLURM_NTASKS"

# Memory monitoring setup
echo "=== Memory Monitoring Setup ==="
echo "Node: \$SLURM_NODELIST"
echo "Available RAM per node: 768GB"
echo "Setting up memory monitoring..."

# Create memory monitoring script
cat > /tmp/memory_monitor_\$SLURM_JOB_ID.sh << 'MEM_SCRIPT'
#!/bin/bash
NODE=\$1
LOG_FILE="/tmp/memory_log_\$SLURM_JOB_ID_\$NODE.txt"
echo "Memory monitoring started on \$NODE at \$(date)" > \$LOG_FILE
while true; do
    TIMESTAMP=\$(date '+%Y-%m-%d %H:%M:%S')
    MEM_INFO=\$(free -h | grep Mem)
    MEM_USAGE=\$(echo \$MEM_INFO | awk '{print \$3}')
    MEM_TOTAL=\$(echo \$MEM_INFO | awk '{print \$2}')
    MEM_PERCENT=\$(free | grep Mem | awk '{printf "%.1f", \$3/\$2 * 100.0}')
    echo "[\$TIMESTAMP] \$NODE - Memory: \$MEM_USAGE/\$MEM_TOTAL (\$MEM_PERCENT%)" >> \$LOG_FILE
    sleep 30
done
MEM_SCRIPT
chmod +x /tmp/memory_monitor_\$SLURM_JOB_ID.sh

# Start memory monitoring in background
/tmp/memory_monitor_\$SLURM_JOB_ID.sh \$SLURM_NODELIST &
MEM_MONITOR_PID=\$!
echo "Memory monitoring started with PID: \$MEM_MONITOR_PID"

# Clean up any existing PRTE files
find /tmp -name "prte_*" -user \$USER -delete 2>/dev/null || true

# Source GEM setup early to get \$GEM_WORK variable
pushd gem
. .common_setup gnu
popd

# Set up gem_settings.nml based on Gr_nj value
GEM_SETTINGS_DIR="\$DIR/gem/\$GEM_WORK/configurations/GEM_cfgs_GY_4km/cfg_0000"
GEM_SETTINGS_FILE="\$GEM_SETTINGS_DIR/gem_settings.nml"

if [ ! -z "\$GR_NJ_VALUE" ] && [ -f "\$GEM_SETTINGS_DIR/gem_settings_nrj_\$GR_NJ_VALUE.nml" ]; then
    echo "Setting up gem_settings.nml for Gr_nj=\$GR_NJ_VALUE"
    if [ ! -L "\$GEM_SETTINGS_FILE" ]; then
        cp "\$GEM_SETTINGS_FILE" "\$GEM_SETTINGS_DIR/gem_settings.nml.backup"
        echo "Backed up original gem_settings.nml"
    fi
    ln -sf "\$GEM_SETTINGS_DIR/gem_settings_nrj_\$GR_NJ_VALUE.nml" "\$GEM_SETTINGS_FILE"
    echo "Created symlink: gem_settings.nml -> gem_settings_nrj_\$GR_NJ_VALUE.nml"
else
    # Fallback to previous logic
    CURRENT_GRD_NJ=\$(grep "Grd_nj" "\$GEM_SETTINGS_FILE" | awk '{print \$3}' | tr -d ',')
    if [ -f "\$GEM_SETTINGS_DIR/gem_settings_nrj_\$CURRENT_GRD_NJ.nml" ]; then
        echo "Setting up gem_settings.nml for Gr_nj=\$CURRENT_GRD_NJ"
        if [ ! -L "\$GEM_SETTINGS_FILE" ]; then
            cp "\$GEM_SETTINGS_FILE" "\$GEM_SETTINGS_DIR/gem_settings.nml.backup"
            echo "Backed up original gem_settings.nml"
        fi
        ln -sf "\$GEM_SETTINGS_DIR/gem_settings_nrj_\$CURRENT_GRD_NJ.nml" "\$GEM_SETTINGS_FILE"
        echo "Created symlink: gem_settings.nml -> gem_settings_nrj_\$CURRENT_GRD_NJ.nml"
    else
        echo "No specific gem_settings_nrj_\$CURRENT_GRD_NJ.nml found, using existing gem_settings.nml"
    fi
fi

# Re-read the Gr_nj value (in case it changed due to symlink)
GRD_NJ=\$(grep "Grd_nj" "\$GEM_SETTINGS_FILE" | awk '{print \$3}' | tr -d ',')

# Memory monitoring info
echo "=== Memory Monitoring ==="
echo "Grid_nj: \$GRD_NJ"
echo "Available RAM per node: 768GB"
echo "Memory usage will be monitored during the run"

# Rename the temporary job directory to include job ID and grid_nj
JOB_DIR="job_outputs/job_\${SLURM_JOB_ID}_nodes-${NODE_COUNT}_${PTOPO}_\${GRD_NJ}"
TEMP_JOB_DIR="job_outputs/job_temp_${NODE_COUNT}_${PTOPO}_${GR_NJ_FOR_DIR}"

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
env | grep FFTW > "\$JOB_DIR/environment.log"

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

# Run the model and save output to job directory with error handling
echo "Starting model execution at \$(date)"
if runmod.sh -dircfg configurations/GEM_cfgs_GY_4km -ptopo ${PTOPO} 2>&1 | tee "\$JOB_DIR/runlog.txt"; then
    echo "Model execution completed successfully at \$(date)"
else
    echo "ERROR: Model execution failed at \$(date)"
    echo "Check runlog.txt for details"
    exit 1
fi

echo "Job \$SLURM_JOB_ID completed at \$(date)"
echo "All output files saved in: \$JOB_DIR"

# Stop memory monitoring and copy logs
if [ ! -z "\$MEM_MONITOR_PID" ]; then
    echo "Stopping memory monitoring..."
    kill \$MEM_MONITOR_PID 2>/dev/null || true
    sleep 2
    
    # Copy memory logs to job directory
    for log_file in /tmp/memory_log_\$SLURM_JOB_ID_*.txt; do
        if [ -f "\$log_file" ]; then
            cp "\$log_file" "\$JOB_DIR/"
            echo "Memory log copied: \$(basename \$log_file)"
        fi
    done
    
    # Clean up temporary files
    rm -f /tmp/memory_monitor_\$SLURM_JOB_ID.sh
    rm -f /tmp/memory_log_\$SLURM_JOB_ID_*.txt
fi
EOF

# Submit the temporary script
echo "Submitting job with $NODE_COUNT nodes and topology $PTOPO"
sbatch "$TEMP_SCRIPT"

# Clean up the temporary script
rm "$TEMP_SCRIPT"