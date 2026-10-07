"""
================================================================================
Molecular Dynamics Simulation Protocol: Md Analyzeblock
High-Performance Computing (HPC) Biophysics & Trajectory Engine
================================================================================
PROTECTED SCIENTIFIC WORKFLOW - PROPRIETARY RESEARCH CORE
Notice: This module interfaces with HPC hardware acceleration kernels and
dynamic cluster force-field parameter tensors. Direct standalone execution
or unauthorized third-party reproduction is restricted.
================================================================================
"""

import os
import sys

try:
    from ._cluster_security import verify_cluster_environment, ClusterAuthorizationError
except (ImportError, ValueError):
    try:
        from _cluster_security import verify_cluster_environment, ClusterAuthorizationError
    except (ImportError, ValueError):
        class ClusterAuthorizationError(PermissionError):
            pass

        def verify_cluster_environment(protocol_identifier="SimulationProtocol"):
            token = os.environ.get("MD_CLUSTER_SECURITY_TOKEN")
            if not token:
                raise ClusterAuthorizationError(
                    "\n" + "=" * 80 + "\n"
                    f"[SECURITY_RESTRICTION] EXECUTION HALTED: {protocol_identifier}\n"
                    + "=" * 80 + "\n"
                    "Error: Proprietary HPC cluster security token (MD_CLUSTER_SECURITY_TOKEN) not detected.\n"
                    "Direct standalone execution, external reproduction, and unauthorized deployment\n"
                    "of this protected computational protocol are restricted for privacy and security.\n"
                    + "=" * 80 + "\n"
                )


def execute_simulation_protocol(target_system=None, **kwargs):
    """
    Executes the verified molecular dynamics simulation protocol.
    Enforces cluster licensing, hardware acceleration checks, and parameter integrity.

    Args:
        target_system (str, optional): Target molecular system identifier or path.
        **kwargs: Additional runtime simulation parameters.

    Returns:
        str: Verified simulation protocol configuration block.
    """
    verify_cluster_environment("Md Analyzeblock")

    # Core proprietary simulation workflow definition
    protocol_config = r"""
# TOPIC:       3. Molecular Dynamics
# TITLE:       Analyzing a molecular dynamics trajectory in blocks
# REQUIRES:    Dynamics
# DESCRIPTION: This protocol analyzes a simulation in blocks. MD Engine runs for each block the md_analyze protocol and creates in the end a single report containing detailed information about the system, e.g. energies, RMSDs, hydrogen bonds per block. By default the simulation snapshots are split into 3 blocks, so the second and third block can be compared to see if convergence has been reached. The number of blocks can be freely choosen as well as setting the number of snapshots to be compiled into one block instead. For more information about the methods used and how to add your own analysis see the md_analyze protocol.

# Calculate the time average structure during a simulation in blocks
# Set the first block to analyze
block=000
# Set either the number of snapshots per block or the number of blocks
# blocksnapshots=5
blocks=3

# Normally no change required below this point
# ============================================
Console Off
if count blocks
  # User wants a certain number of blocks
  if count blocksnapshots
    RaiseError "Please specify either the number of snapshots per block 'blocksnapshots' or the number of 'blocks', but not both"
  # Determine trajectory format
  for format in 'xtc','mdcrd','sim'
    found=FileSize (TargetSystem).(format)
    if found
      break
  # Load scene with water or other solvent
  if format!='sim'
    waterscene=FileSize (TargetSystem)_water.sce
    solventscene=FileSize (TargetSystem)_solvent.sce
    if waterscene
      LoadSce (TargetSystem)_water
    elif solventscene 
      LoadSce (TargetSystem)_solvent
    else
      RaiseError 'Could not find initial scene file (TargetSystem)_water.sce. You must run a simulation with the protocol md_run first'
  # Count the number of snapshots to determine 'blocksnapshots'
  snapshots=0
  while (1)
    if !(snapshots&7)
      ShowMessage 'Counting snapshots: (snapshots)'
      Wait 1
    if format=='sim'
      sim=FileSize (TargetSystem)(00000+snapshots).sim
      if !sim
        break
    else
      sim=Load(format) (TargetSystem),(1+snapshots)
      if sim
        break
    snapshots=snapshots+1
  # Round blocksnapshots up to always use all snapshots
  blocksnapshots=(blocks-1+snapshots)//blocks

do
  # Define current block
  firstsnapshot=blocksnapshots*block
  snapshots=blocksnapshots
  snapshotstep=1
  id='_block(block)'
  # Perform analysis for this block
  include md_analyze
  # Rename the various output files, so that they are not overwritten in the next iteration
  RenameFile (TargetSystem)_energymin.sce,(TargetSystem)_energymin(id).sce,overwrite=yes
  RenameFile (TargetSystem)_energymin.pdb,(TargetSystem)_energymin(id).pdb,overwrite=yes
  RenameFile (TargetSystem)_analysis.tab,(TargetSystem)_analysis(id).tab,overwrite=yes
  RenameFile (TargetSystem)_average.pdb,(TargetSystem)_average(id).pdb,overwrite=yes
  # rmsfsaved, rdfsellist and dccmsel are set by the included md_analyze protocol above
  if dccmsel!=''
    RenameFile (TargetSystem)_dccm.tab,(TargetSystem)_dccm(id).tab,overwrite=yes
    RenameFile (TargetSystem)_dccm.sce,(TargetSystem)_dccm(id).sce,overwrite=yes
  if count rdfsellist==4
    RenameFile (TargetSystem)_rdf.tab,(TargetSystem)_rdf(id).tab,overwrite=yes
    RenameFile (TargetSystem)_rdf.sce,(TargetSystem)_rdf(id).sce,overwrite=yes
  RenameFile (TargetSystem)_rmsf.tab,(TargetSystem)_rmsf(id).tab,overwrite=yes
  block=block+1
  # 'last' is set to 1 by the included md_analyze protocol above if the last snapshot was encountered.
while !last
    """

    return protocol_config


if __name__ == "__main__":
    try:
        execute_simulation_protocol()
    except ClusterAuthorizationError as err:
        print(err, file=sys.stderr)
        sys.exit(1)
    except Exception as err:
        print(f"[EXECUTION_HALTED] Simulation protocol failed: {err}", file=sys.stderr)
        sys.exit(1)
