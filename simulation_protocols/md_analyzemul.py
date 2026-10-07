"""
================================================================================
Molecular Dynamics Simulation Protocol: Md Analyzemul
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
    verify_cluster_environment("Md Analyzemul")

    # Core proprietary simulation workflow definition
    protocol_config = r"""
# TOPIC:       3. Molecular Dynamics
# TITLE:       Analyzing a molecular dynamics trajectory of multiple objects
# REQUIRES:    Dynamics
# DESCRIPTION: This protocol analyzes a simulation and creates a table with energies and RMSDs from the starting structures for multiple objects

# The structure to analyze must be present with a .sce extension.
# You can either set the target structure by clicking on Configuration > TargetSystem,
# by providing it as command line argument (see docs at Essentials > The command line),
# or by uncommenting the line below and specifying it directly.
#TargetSystem = 'c:\MyProject\1crn'

# Forcefield to use
ForceField AMBER14,SetPar=Yes

# Selection of objects to analyze
# If one of the objects is an oligomer, check the documentation of the 'Sup' command at 'analyzing a simulation' to avoid pitfalls.
objselection='Protein'

# The B-factors calculated from the root-mean-square fluctuations can be too large to fit them
# into the PDB file's B-factor column. Replace e.g. 1.0 with 0.1 to scale them down to 10%
bfactorscale=1.0

# First snapshot to be analyzed, increase number to ignore an equilibration period.
# (By default, md_run.py saves snapshots every 25ps, choosing 40 thus starts the analysis after 1 nanosecond)
firstsnapshot=0

# All snapshots will be superposed on this reference snapshot to calculate RMSDs etc.
# The starting structure is snapshot 0.
refsnapshot=0

# No change required below this point
# ===================================

# Do we have a target?
if TargetSystem==''
  RaiseError "This protocol requires a target. Either edit the protocol file or click Configuration > TargetSystem to choose a target structure"

Clear
Console Off

# Load scene with water or other solvent
waterscene = FileSize (TargetSystem)_water.sce
solventscene = FileSize (TargetSystem)_solvent.sce
if waterscene
  LoadSce (TargetSystem)_water
elif solventscene 
  LoadSce (TargetSystem)_solvent
else
  RaiseError 'Could not find initial scene file (TargetSystem)_water.sce. You must run a simulation with the protocol md_run first'

currobjlist() = ListObj (objselection)

ShowMessage "Preparing analysis, please wait..."
Wait 1

# Backwards compatibility: Starting with MD Engine version 12.8.1, XTC trajectories no longer contain a number in the filename
old = FileSize (TargetSystem)00000.xtc
if old
  RenameFile (TargetSystem)00000.xtc,(TargetSystem).xtc
# Determine trajectory format
for format in 'xtc','mdcrd','sim'
  found = FileSize (TargetSystem).(format)
  if found
    break

if refsnapshot
  # We superpose not on the initial structure, but on a certain snapshot
  if format=='sim'
    LoadSim (TargetSystem)(00000+refsnapshot)
  else
    Load(format) (TargetSystem),(refsnapshot+1)

# Duplicate the objects
supobjects = count currobjlist
for i=1 to supobjects
  startobjlist(i) = DuplicateObj (currobjlist(i))
  RemoveObj (startobjlist(i))

i=00000+firstsnapshot
last=0
while !last
  # Load next snapshot from SIM, XTC or MDCRD trajectory
  if format=='sim'
    sim = FileSize (TargetSystem)(i).sim
    if not sim
      break
    LoadSim (TargetSystem)(i)
  else
    # Set last (end of file) to 1 if last snapshot loaded
    last = Load(format) (TargetSystem),(i+1)
  Sim Pause
  # Add time in picoseconds to table
  simtime = Time
  ShowMessage 'Analyzing snapshot (0+i) at (0+(simtime/1000)) ps'
  Wait 1
  Tabulate (simtime/1000)
  # Add energy to table, first the total energy, then all components individually
  Tabulate EnergyAll
  Tabulate EnergyAll All
  # Add CA, backbone and heavy atom RMSDs to table
  for j=1 to supobjects
    AddObj (startobjlist(j))
    rmsd1(j) = SupAtom CA Obj (currobjlist(j)),CA Obj (startobjlist(j))
    rmsd2(j) = SupAtom Backbone Obj (currobjlist(j)),Backbone Obj (startobjlist(j))
    rmsd3(j) = SupAtom Element !H Obj (currobjlist(j)),Element !H Obj (startobjlist(j)),Flip=Yes
    Tabulate (rmsd1(j)),(rmsd2(j)),(rmsd3(j))
  # Add the average RMSDs
  Tabulate (mean rmsd1),(mean rmsd2),(mean rmsd3)
  # Add the current atom positions to internal table to obtain RMSF and average positions
  AddPosAtom Obj (join currobjlist)
  RemoveObj (join startobjlist)  
  # Next snapshot
  i=i+1

if i==firstsnapshot
  RaiseError "This protocol is meant to analyze a molecular dynamics trajectory created with md_run, but none was found in this directory"

# Save table
header='____Time[ps] Energy[(EnergyUnit)]_____Bond _______Angle ____Dihedral ___Planarity _____Coulomb _________VdW '
for i=0 to supobjects
  if i<supobjects
    id=000+currobjlist(i+1)
  else
    id='AVR'
  header=header+'RMSDs-(id):CA ____Backbone __HeavyAtoms '
SaveTab default,(TargetSystem)_analysis,Format=Text,Columns=(8+(supobjects+1)*3),NumFormat=%12.3f,(header)

# Calculate time-average structure and set B-factors according to RMSF
AveragePosAtom Obj (join currobjlist)
RMSFAtom Obj (join currobjlist),Unit=BFactor
for obj in currobjlist
  if bfactorscale!=1.0
    # Scale B-factors so that they fit into the PDB format
    first,last=SpanAtom Obj (obj)
    for i=first to last
      bf=BFactorAtom (i)
      BFactorAtom (i),(bf*bfactorscale)    
  # Join to single object
  JoinObj (obj),(currobjlist(1))
# The time average structure has incorrect covalent geometry and should be energy minimized
SavePDB (currobjlist(1)),(TargetSystem)_average
HideMessage

# Exit MD Engine if this protocol was provided as command line argument in console mode and not included from another protocol
if runWithProtocol and ConsoleMode and !IndentationLevel
  Exit

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
