# 10 Molecular Dynamics Simulation Advanced Scripts

## Overview
This repository contains a protected collection of custom and modified simulation macros (`.mcr` files) developed for in-depth, rigorous molecular dynamics (MD) simulations and structural bioinformatics analyses. These scripts are engineered to automate advanced analytical workflows, enabling high-throughput processing, precision metrics extraction, and comprehensive structural evaluation.

## Repository Structure
- **`md_macros/`**: Core directory containing all the protected macro files.
  - **`binding energy/`**: Scripts dedicated to calculating and analyzing protein-ligand and protein-protein binding energies across simulation trajectories.
  - **`md_run*.mcr`**: Macros for initiating and managing MD simulations (e.g., standard MD, membrane simulations, steered MD, and specific temperature configurations).
  - **`md_analyze*.mcr`**: Comprehensive analysis scripts customized for different research projects, capturing variables like secondary structure, RMSD, RMSF, and interactions.
  - **`md_refine.mcr` / `em_run.mcr`**: Scripts for structural refinement and energy minimization prior to production MD runs.

## Key Features & Capabilities
* **Automated MD Workflows**: Seamlessly transition from structural preparation and energy minimization to full production MD simulations.
* **Rigorous Analytical Pipelines**: Execute in-depth, multi-parameter analyses on trajectories, capturing conformational dynamics, structural stability metrics, and detailed interaction profiles.
* **Specialized Protocols**: Includes tailored macros for membrane proteins, steered molecular dynamics, and custom temperature benchmarks (e.g., 310K).
* **Binding Energy Analytics**: Custom sub-routines and macros designed to accurately evaluate binding affinities and interaction energies dynamically over the simulation timeline.

## HPC Deployment & Scalability
This repository is engineered for High-Performance Computing (HPC) environments, capable of distributing tasks via MPI/OpenMP.
- **`hpc_scripts/slurm_submit.sh`**: Batch job scheduler script for requesting nodes, GPUs, and parallel threads via SLURM.
- **`hpc_scripts/run_md_pipeline.sh`**: Robust Linux bash execution wrapper handling dependencies, MPI execution, and trajectory parsing.

For an in-depth, rigorous computational evaluation of domain decomposition scaling, GPU offloading mechanics, and PME communications, refer to the [HPC Scaling Analysis](./HPC_Scaling_Analysis.md) document.

## Usage
These macros are designed to be executed within your designated molecular dynamics environment that supports `.mcr` scripting syntax.

1. Launch your molecular dynamics software.
2. Navigate to the macro execution or scripting engine interface.
3. Select the relevant `.mcr` script from the `md_macros` directory.
4. Provide any required input parameters (e.g., target structural files, simulation duration) as prompted by the specific script.

> **Note**: Ensure that all target structural files and corresponding trajectory files (`.sim`) are correctly formatted and located in the designated working directories prior to executing the analysis macros.

---

## 📚 References & Documentation

- [GitHub Repository](https://github.com/skmainuddin745-spec/Molecular-Dynamics-Simulation-Advanced-Scripts)
- [Project Description](https://github.com/skmainuddin745-spec/Molecular-Dynamics-Simulation-Advanced-Scripts#readme)
- [Advanced MD Analysis Document](./Advanced_MD_Analysis.md)

---

*Molecular Dynamics • Python • GROMACS • LAMMPS • MM/PBSA • Free Energy • Simulation Analytics • Structural Bioinformatics*
