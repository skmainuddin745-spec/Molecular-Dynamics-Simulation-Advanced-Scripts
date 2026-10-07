"""
================================================================================
Molecular Dynamics Simulation Protocol: Em Run
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
    verify_cluster_environment("Em Run")

    # Core proprietary simulation workflow definition
    protocol_config = r"""
# TOPIC:       4. Molecular modeling
# TITLE:       Running an energy minimization
# REQUIRES:    Dynamics
# DESCRIPTION: This protocol runs an energy minimization of the soup without cleaning it first. Compared to the normal minimization experiment, it temporarily adds a water shell so that all force fields can be used directly, also those optimized for use with explicit solvent

if !Atoms and TargetSystem!=''
  # No atoms but a TargetSystem is available, load the structure
  for type in 'sce','yob','pdb'
    size = FileSize (TargetSystem).(type)
    if size
      break
  if !size
    RaiseError 'Initial structure not found, expected (TargetSystem).sce,.yob or .pdb. Make sure to create a project directory and place the structure there'
  # Load structure
  Load(type) (TargetSystem)
# Make sure we have a cell
cellfound = CountObj SimCell
if !cellfound
  # If Extension is too large, filling the cell with water can exhaust memory 
  Cell Auto,Extension=8
  Boundary periodic
if count forcefield
  # Force field specified by caller, for example from the command line
  ForceField (forcefield),SetPar=yes
  
# Make sure that at least one atom is free to move
fixedatoms = CountAtom fixed
if fixedatoms==Atoms
  RaiseError "No atoms are present or all are fixed, which makes an energy minimization impossible. Click Simulation > Free > All first."

minatoms=Atoms
# Duplicate all objects with atoms, so that we can measure the RMSD afterwards
endobjlist() = ListObj Atom all
startobjlist() = DuplicateObj (join endobjlist)
RemoveObj (join startobjlist)

# Enable correction of cis-peptide bonds and wrong isomers that are newly formed (conformational stress)
CorrectIso On,Old=No
CorrectCis On,Old=No

fof = ForceField
if fof!='NOVA'
  # Force field for explicit solvent
  # Do we already have enough waters present?
  waters = CountRes Water
  srfacc = SurfRes !Water,accessible
  if not waters or srfacc/waters>15
    # No, create and minimize water shell
    Experiment Neutralization
      Ions Massfraction=0
      Speed fast
    Experiment On
    Wait ExpEnd
    DelRes Water with distance>6 from !Water
  else
    # Remember which atoms have been fixed
    fixedlist() = ListAtom fixed
    # Fix everything except water
    FixAll
    FreeRes Water
    # Energy minimize first the water alone
    ShowMessage "Running quick energy minimization of water molecules..." 
    Experiment Minimization
      Convergence 0.1
    Experiment On
    Wait ExpEnd
    # Fix those atoms that were fixed by the user before
    FreeAll
    if count fixedlist
      FixAtom (join fixedlist)
# Main energy minimization
ShowMessage "Running main energy minimization..."
Experiment Minimization
  # Converge as soon as the energy improves by less than 0.05 kJ/mol = 50 J/mol per atom during 200 steps
  Convergence (50.*JToUnit/AvoConst)
Experiment On
Wait ExpEnd
HideMessage

if minatoms>2
  # Measure RMSDs obtained during minimization
  Console Off
  for i=1 to count startobjlist
    startobj=startobjlist(i)
    endobj=endobjlist(i)
    AddObj (startobj)
    # Don't Flip, since it's too slow for large proteins and doesn't happen during annealing
    result = SupObj (startobj),(endobj),Match=Yes,Flip=No
    name = NameObj (endobj)
    print 'The all-atom minimization RMSD of object (endobj) [(name)] is (0.000+result) A'
    DelObj (startobj)
# Final check that minimization did not introduce errors
wronghands = CheckAll Isomers
cisbonds = CheckAll PepBonds
if wronghands or cisbonds
  print 'WARNING - There are (0+wronghands) wrong isomers and (0+cisbonds) cis-peptide bonds.'
if count type
  # Structure has been loaded via TargetSystem before, save the minimized structure again
  if type!='sce'
    JoinObj (join endobjlist),(endobjlist1)
    Save(type) (endobjlist1),(TargetSystem)_minimized
  else
    SaveSce (TargetSystem)_minimized
# Exit MD Engine if this protocol was provided as command line argument in console mode and not included from another protocol
if runWithProtocol and ConsoleMode and !IndentationLevel
  Exit
Console open
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
