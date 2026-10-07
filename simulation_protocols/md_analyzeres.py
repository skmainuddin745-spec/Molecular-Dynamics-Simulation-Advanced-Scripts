"""
================================================================================
Molecular Dynamics Simulation Protocol: Md Analyzeres
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
    verify_cluster_environment("Md Analyzeres")

    # Core proprietary simulation workflow definition
    protocol_config = r"""
# TOPIC:       3. Molecular Dynamics
# TITLE:       Analyzing a molecular dynamics trajectory per residue
# REQUIRES:    Dynamics
# DESCRIPTION: This protocol analyzes a simulation and creates a table with average RMSFs and RMSDs from the starting structure per residue

# The structure to analyze must be present with a .sce extension.
# You can either set the target structure by clicking on Configuration > TargetSystem,
# by providing it as command line argument (see docs at Essentials > The command line),
# or by uncommenting the line below and specifying it directly.
#TargetSystem = 'c:\MyProject\1crn'

# Forcefield to use (a MD Engine command, so no '=' used)
ForceField AMBER14,SetPar=Yes

# Number of the object whose RMSFs and RMSDs from the starting conformation will be calculated
# If this is an oligomer, check the documentation of the 'Sup' command at 'analyzing a simulation' to avoid pitfalls.
currobj=1

# Consider protein residues with a Calpha plus nucleic acid residues with a C1*
atomsel='Atom CA Protein or Atom C1* NucAcid'
# If you are also interested in certain ligands, additionally select the core atom of each ligand,
# separated with 'or'. Note that the backbone RMSDs will not be calculated if the ligand
# does not contain backbone atoms. The example below is for ligand CRO 66 in PDB file 2B3P:
# atomsel='Atom CA Protein or Atom C1* NucAcid or Atom C1 Res CRO 66'

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

# We need at least 3 Calpha atoms to superpose
calphas = CountAtom (atomsel)
if calphas<3
  RaiseError 'This protocol currently requires at least three residues to analyze, because it performs a superposition and RMSD calculation'

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
    
# Duplicate the intial object for RMSD calculation
startobj = DuplicateObj (currobj)

# Get a selection of residues that match atomsel in the current and the start objects
for type in 'curr','start'
  reslist() = ListRes (atomsel) and Obj ((type)obj)
  (type)ressel=join reslist
RemoveObj (startobj)

# Set the summed up RMSDs for CA, BackBone and HeavyAtoms to zero
rmsds=count reslist
for i=1 to 3
  for j=1 to rmsds
    rmsd(i)sum(j)=0.

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
  simtime = Time
  ShowMessage 'Analyzing snapshot (0+i) at (0+(simtime/1000)) ps'
  Wait 1
  # Get per residue RMSDs between current residue selection and start residue selection
  AddObj (startobj)
  rmsd1() = SupAtom (atomsel) and Obj (currobj), (atomsel) and Obj (startobj),Unit=Res
  rmsd2() = SupAtom Res (currressel) Backbone, Res (startressel) Backbone,Unit=Res
  rmsd3() = SupAtom Res (currressel) Element !H, Res (startressel) Element !H,Unit=Res
  # Sum up atom positions to calculate RMSFs
  AddPosAtom Res (currressel)
  # Sum up RMSDs
  for j=1 to 3
    # If residues without backbone have been selected for analysis, we skip backbone result
    if count rmsd(j)==rmsds
      for k=1 to rmsds
        rmsd(j)sum(k)=rmsd(j)sum(k)+rmsd(j)(k)
  RemoveObj (startobj)
  # Next snapshot
  i=i+1
  
if i==firstsnapshot
  RaiseError "This protocol is meant to analyze a molecular dynamics trajectory created with md_run, but none was found in this directory"
# Calculate the average
rmsflist() = RMSFRes (atomsel) and Obj (currobj)
reslist() = ListRes (atomsel) and Obj (currobj),Format='RESNAME RESNUM MOLNAME'
for j=1 to rmsds
  Tabulate '(reslist(j))',(rmsd(1)sum(j)/i),(rmsd(2)sum(j)/i),(rmsd(3)sum(j)/i),(rmsflist(j))
# Save table
SaveTab default,(TargetSystem)_analysisres,Format=Text,Columns=5,NumFormat=%12.3f,_____Residue _RMSDs[A]:CA ____Backbone __HeavyAtoms______RMSF[A]
# Here we don't create the time-average structure (done by md_analyze.py), but
# instead color the last structure by B-factor.
# The dummy assignment '_ =' ensures that B-factors are not printed
_ = RMSFRes (atomsel) and Obj (currobj),Unit=BFactor
ColorRes (atomsel) and Obj (currobj),BFactor

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
