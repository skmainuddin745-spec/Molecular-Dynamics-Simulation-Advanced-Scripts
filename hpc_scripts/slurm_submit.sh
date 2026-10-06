#!/bin/bash
#=============================================================================
# SLURM Job Submission Script for Molecular Dynamics Pipeline
#=============================================================================
#SBATCH --job-name=MD_Rigorous_Analysis
#SBATCH --output=logs/md_pipeline_%j.out
#SBATCH --error=logs/md_pipeline_%j.err
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=16
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:2               # Request 2 GPUs per node (for hardware acceleration)
#SBATCH --time=48:00:00            # Walltime limit (48 hours)
#SBATCH --partition=gpu_accel      # Target partition
#SBATCH --mem=128G                 # Request 128 GB RAM per node
#SBATCH --mail-type=ALL            # Email notification at start, end, and fail
#=============================================================================

# 1. Environment Purge and Module Loading
module purge
module load gcc/11.2.0
module load openmpi/4.1.2
module load cuda/11.7
module load python/3.10
module load gromacs/2022.3-gpu    # Example native engine dependency

# 2. Parallel Computing Environment Variables
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export MPI_NUM_PROCS=$((SLURM_NNODES * SLURM_NTASKS_PER_NODE))
export HWLOC_HIDE_ERRORS=1

# Hardware sanity checks
echo "======================================================"
echo "Starting MD Job at: $(date)"
echo "SLURM Job ID: $SLURM_JOB_ID"
echo "Nodes Allocated: $SLURM_JOB_NODELIST"
echo "OMP Threads: $OMP_NUM_THREADS | MPI Procs: $MPI_NUM_PROCS"
echo "GPUs Available:"
nvidia-smi --query-gpu=name,pci.bus_id,memory.total --format=csv,noheader
echo "======================================================"

# 3. Setup Working Directory and Execute Pipeline
WORK_DIR=${SLURM_SUBMIT_DIR}
cd ${WORK_DIR}

# Ensure logs directory exists
mkdir -p logs

# 4. Launch the wrapper pipeline script
bash ./hpc_scripts/run_md_pipeline.sh

echo "======================================================"
echo "MD Job Completed at: $(date)"
echo "======================================================"
