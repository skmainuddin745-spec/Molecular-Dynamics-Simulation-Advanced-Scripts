# 🧬 Molecular Dynamics Simulation Advanced Scripts

[![Status](https://img.shields.io/badge/Status-Private_&_Proprietary-red.svg)](PROPRIETARY_NOTICE.md)
[![Simulation Engine](https://img.shields.io/badge/Simulation-Engine_Agnostic-blue.svg)]()
[![Analytics](https://img.shields.io/badge/Analytics-In--Depth_Rigorous_Analysis-purple.svg)]()

This repository contains a protected collection of custom-engineered simulation pipelines developed for **in-depth, rigorous molecular dynamics (MD) simulations** and structural bioinformatics analyses. These advanced algorithms are engineered to orchestrate analytical workflows, enabling high-throughput processing, precision metrics extraction, and comprehensive structural evaluation.

## 🚀 Key Features of the Rigorous Analysis Pipeline

* **Universal Automation Engine**: Advanced scripts designed to orchestrate complex simulation stages automatically, transitioning seamlessly from initialization to production dynamics without manual intervention.
* **Specialized Protocols**: Includes tailored configurations for membrane proteins, steered molecular dynamics, and custom temperature benchmarks (e.g., 310K).
* **Binding Energy Analytics**: Custom sub-routines designed to accurately evaluate binding affinities and interaction energies dynamically over the simulation timeline.
* **Comprehensive Metrics Extraction**: Integrated analysis logic for calculating Root Mean Square Deviation (RMSD), Root Mean Square Fluctuation (RMSF), Dictionary of Protein Secondary Structure (DSSP), and interaction arrays simultaneously.

## 🗂️ Core Architecture

- **`execution_engine/`**: Core directory containing all the protected execution algorithms.
  - **`md_run_pipeline.py`**: Pipelines for initiating and managing MD simulations (e.g., standard MD, membrane simulations, steered MD, and specific temperature configurations).
  - **`md_analyze_rigorous.py`**: Comprehensive in-depth analysis scripts customized for different research projects, capturing variables like secondary structure, RMSD, RMSF, and interactions.
  - **`md_refine_em.py`**: Scripts for structural refinement and energy minimization prior to production MD runs.

## ⚙️ Execution

These pipelines are designed to be executed within your designated high-performance computing environment. 

1. Ensure all dependencies and the primary simulation executable are in your system PATH.
2. Navigate to the execution engine interface.
3. Select the relevant analytical script from the execution directory.

> **Note**: Ensure that all target structural files and corresponding trajectory files (`.sim`) are correctly formatted and located in the designated working directories prior to executing the rigorous analysis pipelines.

## 🔐 Security & Proprietary Restrictions

> [!CAUTION]
> **RESTRICTED ACCESS: PROPRIETARY INTELLECTUAL PROPERTY**
> The scripts, topologies, and analytical pipelines within this repository are the exclusive intellectual property of **SK Mainuddin**.

Please see the [`PROPRIETARY_NOTICE.md`](PROPRIETARY_NOTICE.md) and [`LICENSE`](LICENSE) for complete legal restrictions.
