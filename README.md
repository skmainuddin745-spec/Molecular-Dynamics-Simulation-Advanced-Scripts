# Molecular Dynamics Simulation Advanced Protocols & HPC Pipelines

## Overview
This repository contains a protected suite of advanced Molecular Dynamics (MD) simulation protocols, High-Performance Computing (HPC) pipelines, and structural bioinformatics analytics engines. The protocols automate multi-stage computational biophysics workflows, enabling high-throughput trajectory sampling, thermodynamic ensemble equilibration, precision free energy evaluation, and correlated dynamics extraction.

## Repository Architecture
- **`simulation_protocols/`**: Core directory containing protected computational protocol modules.
  - **`binding_energy/`**: Sub-directory dedicated to endpoint binding free energy evaluation and continuum solvation modeling across trajectory ensembles.
  - **`md_run*.py`**: Comprehensive simulation engines governing system equilibration and production MD (e.g., standard NPT/NVT, physiological 310.15 K, lipid bilayer membrane self-assembly, steered pulling MD, and accelerated timesteps).
  - **`md_analyze*.py`**: High-throughput trajectory analytics extracting RMSD, RMSF, radius of gyration, dynamic cross-correlation matrices (DCCM), and secondary structure transitions.
  - **`em_run*.py` & `md_refine.py`**: Steepest descent / conjugate gradient energy minimization, hydrogen bonding network optimization, and simulated annealing refinement.
  - **`_cluster_security.py`**: HPC cluster authentication, hardware acceleration verification, and intellectual property protection guard layer.
- **`hpc_scripts/`**: Enterprise HPC cluster orchestration scripts.
  - **`slurm_submit.sh`**: SLURM batch scheduler submission requesting multi-GPU acceleration, MPI tasks, and OpenMP thread pinning.
  - **`run_md_pipeline.sh`**: Robust Linux bash execution wrapper managing dependencies, process monitoring, and pipeline stages.

## Key Biophysical Capabilities
* **Hierarchical Multi-Timestep Integration**: Fast-varying force decomposition extending timesteps up to 5.0 fs via rigid bond constraints (SHAKE/LINCS equivalents).
* **Long-Range Electrostatics**: Particle-Mesh Ewald (PME) reciprocal grid space resolution with strict Periodic Boundary Conditions (PBC).
* **Thermodynamic Ensembles**: Stochastic Langevin / velocity-rescaling thermostats (NVT) and isotropic/anisotropic barostats (NPT) for solution and membrane phases.
* **Binding Free Energy Analytics (MM/PBSA)**: Endpoint free energy decomposition coupling molecular mechanics with Poisson-Boltzmann continuum solvation and non-polar surface area estimations.

## HPC Deployment & Scalability
The workflow is engineered for distributed execution across multi-GPU supercomputing clusters:
- **MPI & OpenMP Hybrid Scaling**: Spatial domain decomposition coupled with intra-node multi-threading to bypass 3D-FFT communication bottlenecks.
- **GPU Kernel Offloading**: Direct delegation of non-bonded pair potentials (Lennard-Jones and real-space Coulombic) to streaming multiprocessors.

For an in-depth theoretical and empirical scaling derivation, see the [HPC Scaling Analysis](./HPC_Scaling_Analysis.md) document.
For detailed biophysical equations and mathematical foundations, see the [Advanced MD Analysis](./Advanced_MD_Analysis.md) document.

## Intellectual Property Protection & Cluster Guard
> [!NOTE]
> All simulation protocols in this repository are protected research workflows. To safeguard proprietary potential calibrations and ensure computational reproducibility:
> - **Cluster Verification**: Protocols verify cluster hardware authorization (`MD_CLUSTER_SECURITY_TOKEN`) and require calibrated potential tensors.
> - **Execution Guard**: Standalone external execution outside authorized research cluster nodes halts automatically with a descriptive security exception.
> - **Collaboration Access**: For academic collaboration or access to production binaries and parameter sets, contact the corresponding research laboratory.

---

## References & Documentation
- [Advanced MD Analysis Document](./Advanced_MD_Analysis.md)
- [HPC Scaling Analysis Document](./HPC_Scaling_Analysis.md)
- [Implementation Architecture](./implementation_plan.md)

---
*Molecular Dynamics • Python • HPC Workflows • GROMACS • LAMMPS • MM/PBSA • Free Energy • Simulation Analytics • Structural Bioinformatics*
