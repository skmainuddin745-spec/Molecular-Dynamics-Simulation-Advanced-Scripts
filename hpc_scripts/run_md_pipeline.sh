#!/bin/bash
#=============================================================================
# Molecular Dynamics Pipeline Execution Wrapper
#=============================================================================
# This script robustly interfaces between the SLURM workload manager and the 
# underlying engine-agnostic Python macros (converted from legacy formats).
# It enforces strict error handling, I/O sanity checks, and MPI scaling.
#=============================================================================

set -eo pipefail # Fail fast on errors and piped failures

PIPELINE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MACRO_DIR="${PIPELINE_ROOT}/md_macros"
DATA_DIR="${PIPELINE_ROOT}/data"
RESULTS_DIR="${PIPELINE_ROOT}/results"

echo "Initializing MD Python Pipeline Wrapper..."
echo "Root Directory: ${PIPELINE_ROOT}"

# 1. Environment Sanitization
if [[ -z "${OMP_NUM_THREADS}" ]]; then
    export OMP_NUM_THREADS=1
    echo "Warning: OMP_NUM_THREADS not set. Defaulting to 1."
fi

# 2. Directory Scaffolding
mkdir -p "${RESULTS_DIR}"
mkdir -p "${DATA_DIR}"

# 3. Execution Function (MPI Wrapped)
#    Abstracts the invocation of the python modules ensuring MPI constraints
execute_python_macro() {
    local script_name=$1
    shift
    local target_script="${MACRO_DIR}/${script_name}"
    
    if [[ ! -f "${target_script}" ]]; then
        echo "Error: Critical macro script missing: ${target_script}" >&2
        exit 1
    fi

    echo "=========================================================="
    echo "Executing Pipeline Stage: ${script_name}"
    echo "MPI Procs: ${MPI_NUM_PROCS:-1} | Args: $@"
    echo "=========================================================="

    # If running inside SLURM, use mpirun/srun, otherwise standard python
    if [[ -n "${SLURM_JOB_ID}" ]]; then
        srun --mpi=pmix python3 "${target_script}" "$@"
    else
        python3 "${target_script}" "$@"
    fi

    local status=$?
    if [[ ${status} -ne 0 ]]; then
        echo "FATAL: ${script_name} failed with exit code ${status}" >&2
        exit ${status}
    fi
}

#=============================================================================
# RIGOROUS ANALYTICAL PIPELINE WORKFLOW
#=============================================================================

# Stage 1: System Refinement & Energy Minimization
# Flattens localized steric clashes and stabilizes the forcefield parameters
execute_python_macro "em_run.py" \
    --input "${DATA_DIR}/system_topology.pdb" \
    --output "${RESULTS_DIR}/minimized.pdb"

# Stage 2: NVT/NPT Equilibration
# Couples the thermostat/barostat to stabilize kinetic energy
execute_python_macro "md_run.py" \
    --input "${RESULTS_DIR}/minimized.pdb" \
    --ensemble "NPT" \
    --duration 500 \
    --temp 310 \
    --output_traj "${RESULTS_DIR}/equilibration.sim"

# Stage 3: High-Throughput Trajectory Analytics
# Extracts rigorous structural bioinformatics metrics (RMSD, RMSF, Rg)
execute_python_macro "md_analyze.py" \
    --trajectory "${RESULTS_DIR}/equilibration.sim" \
    --out_dir "${RESULTS_DIR}/analytics"

# Stage 4: MM/PBSA Binding Free Energy Calculations
# Submits frames for reciprocal continuum solvation modeling
execute_python_macro "binding energy/md_analyzebindenergy.py" \
    --trajectory "${RESULTS_DIR}/equilibration.sim" \
    --out_csv "${RESULTS_DIR}/analytics/mm_pbsa_binding_energies.csv"

echo "Pipeline execution completed successfully at $(date)."
