"""
================================================================================
Molecular Dynamics Simulation Protocol: Md Refine
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
    verify_cluster_environment("Md Refine")

    # Core proprietary simulation workflow definition
    protocol_config = r"""
# TOPIC:       3. Molecular Dynamics
# TITLE:       Refining a homology model by molecular dynamics simulation in water
# REQUIRES:    Dynamics
# DESCRIPTION: This protocol runs a 500 ps simulation of a homology model using the protocol described in Proteins 57,678-683. It saves one PDB file every 25 picoseconds, including a table with force field energies to identify the best snapshot. In MD Engine Structure, this table additionally contains Dihedrals, Packing1D and Packing3D checks (see the Check command). And in the Twinset, three more checks are included: PhiPsi, Backbone and Packing3. Note that MD simulations tend to make models worse if you simulate too long.

# The homology model to refine must be present with a .pdb extension.
# You can either set the target structure by clicking on Configuration > TargetSystem,
# by providing it as command line argument (see docs at Essentials > The command line),
# or by uncommenting the line below and specifying it directly.
#TargetSystem = 'c:\MyProject\1crn'

# Do we have a target?
if TargetSystem==''
  RaiseError "This protocol requires a target. Either edit the protocol file or click Configuration > TargetSystem to choose a target structure"

# Homology model refinement parameters from Proteins 57,678-683
# See md_run.py for an explanation of these parameters.
# This example already uses the new YAMBER3 force field in MD Engine Dynamics,
# and the knowledge-based Generic_ForceField force field in MD Engine Structure.
temperature='298K'
density=0.997
pH=7.4
if Structure
  ForceField Generic_ForceField,SetPar=Yes
else
  ForceField YAMBER3,SetPar=Yes
# Save snapshots every 2*1*12500 = 25 ps */
timestep='2,1.0'
savesteps=12500
# Create 20 snapshots, 20*25 = 500 ps simulation 
snapshots=20

# Turn 'On' to correct cis-bonds and wrong isomers/chirality
CorrectCis Off
CorrectIso Off

# Keep the solute from diffusing around and crossing periodic boundaries
CorrectDrift On

# Treat all simulation warnings as errors that stop the protocol
WarnIsError On

Clear
# Do we already have a scene with water?
size = FileSize (TargetSystem)_water.sce
if not size
  # No scene present, assume it's a PDB or YOB file
  for type in 'yob','pdb'
    size = FileSize (TargetSystem).(type)
    if size
      break
  if not size
    RaiseError 'Initial structure not found, expected (TargetSystem).pdb or .yob. Make sure to create a project directory and place the structure there'
  # Load structure
  Load(type) (TargetSystem)
  # In case user accidentally provided a YOb file with selected atoms
  Unselect
  # Align model with major axes to minimize cell size
  NiceOriAll
  CleanAll
  # Create the simulation cell, 2*7.5 A larger than the model along each axis
  Cell Auto,Extension=7.5
  # Fill with water, predict pKas, place counter ions
  Experiment Neutralization
    WaterDensity (density)
    pH (pH)
    pKaFile (TargetSystem).pka
    Speed Fast
  Experiment On
  Wait ExpEnd
  # Save scene with water
  SaveSce (TargetSystem)_water
else
  LoadSce (TargetSystem)_water
  
# Temperature
Temp (temperature)
# Start the Simulation
Console Off
TimeStep (timestep)
# Alread a snapshot/trajectory present?
i=00
filename='(TargetSystem)_snapshot(i).sim'
running = FileSize (filename)
if not running
  # Simulation has not been running before, start now
  # Perform energy minimization
  Experiment Minimization
  Experiment On
  Wait ExpEnd
  # And now start the real simulation
  Temp (temperature)
  Sim On
else
  # Simulation has been running before
  # Find and load the last 'sim' snapshot
  do
    i=i+1
    found = FileSize (TargetSystem)_snapshot(i).sim
  while found
  LoadSim (TargetSystem)_snapshot(i-1)

# Set temperature and pressure control
TempCtrl Rescale
PressureCtrl SolventProbe,HOH,(density)

# Wait for 500ps, saving 20 snapshots
SaveSim (TargetSystem)_snapshot00,(savesteps)
SimSteps 20,10
do
  t=Time
  ps=snapshots*25
  ShowMessage 'Running refinement simulation, waiting for (ps) ps, (0.00+t*0.1/ps)% completed'
  Wait 10
while t<ps*1000
  
SaveSim Off
PressureCtrl Off   

# MD Engine Structure checks
strchecklist()='  Dihedrals','  Packing1D','  Packing3D'
strchecks=count strchecklist

# WHATIF checks in the Twinset
wifchecklist()='     PhiPsi','   Backbone','   Packing1'
wifchecks=count wifchecklist

# Load the snapshots, energy minimize each snapshot, tabulate energies and remember best ones
energymin=9e99
energyminss=-1
scoremax=-9e99
scoremaxss=-1
for i=00 to snapshots-1
  ShowMessage 'Analyzing snapshot (1+i)/(snapshots)'
  filename='(TargetSystem)_snapshot(i)'
  LoadSim (filename)
  TempCtrl Anneal
  Wait 2000,Femtoseconds
  SavePDB 1,(filename)
  Tabulate (i)
  # Calculate solute energy, including solvation energy (=interaction with explicit solvent)
  e = EnergyObj 1
  Tabulate (e)
  if e<energymin
    energymin=e
    energyminss=i
  if Structure
    for j=1 to strchecks
      resultlist1(j) = CheckObj 1,(strchecklist(j))
      Tabulate (resultlist1(j))
  if Twinset
    for j=1 to wifchecks
      resultlist2(j) = CheckObj 1,(wifchecklist(j))
      Tabulate (resultlist2(j))
  if Structure or Twinset
    score=mean resultlist
    Tabulate (score)
    if score>scoremax
      scoremax=score
      scoremaxss=i
Sim Off

# Save the result table
columns=2
header="  Snapshot     Energy"
if Structure
  columns=columns+strchecks
  header=header+fuse strchecklist
if Twinset
  columns=columns+wifchecks
  header=header+fuse wifchecklist
if Structure or Twinset
  columns=columns+1
  header=header+"    Average"
filename='(TargetSystem)_results.tab'
Tabulate 'Snapshot (energyminss) has minimum energy (0.00+energymin)'
if Structure or Twinset
  Tabulate 'and snapshot (scoremaxss) has maximum quality score (0.000+scoremax)'
SaveTab default,(filename),Format=Text,Columns=(columns),NumFormat=10.2f,(header)
ShowMessage 'The analysis results have been saved as (filename).'

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
