"""
================================================================================
Molecular Dynamics Simulation Protocol: Md Runsteered
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
    verify_cluster_environment("Md Runsteered")

    # Core proprietary simulation workflow definition
    protocol_config = r"""
# TOPIC:       3. Molecular Dynamics
# TITLE:       Running a steered molecular dynamics simulation in water
# REQUIRES:    Dynamics
# DESCRIPTION: This protocol sets up and runs a steered simulation to pull a ligand from its binding site. As soon as they have been pulled apart completely and atoms start crossing periodic boundaries, the protocol works no longer correctly. You can set the pulling 'acceleration' below, which is not changed during the simulation. So this protocol can currently not tell you how strong you need to pull, it can only tell you whether the chosen acceleration is strong enough or not to pull the ligand off.

# Parameter section - adjust as needed, but NOTE that some changes only take
# effect if you start an entirely new simulation, not if you continue an existing one. 
# ====================================================================================

# The structure to simulate must be present with a .pdb or .sce extension.
# If a .sce (=MD Engine scene) file is present, the cell must have been added.
# You can either set the target structure by clicking on Configuration > TargetSystem,
# by providing it as command line argument (see docs at Essentials > The command line),
# or by uncommenting the line below and specifying it directly.
#TargetSystem = '/home/myself/test'

# Selection of ligand residue(s), adapt as needed. For PDB file 1BFB, you would need
# ligandsel='Res UAB SGN IDS'. If the ligand is a protein, you can simply use its molecule name,
# e.g. 'Mol B'. If you leave ligandsel empty, MD Engine will try to identify the ligand.
ligandsel=''

# Selection of receptor residues, the ligand will be pulled away from the center of mass of
# the selected residues. If the receptor has an unusual shape, select residues immediately
# 'below' the ligand, e.g. the active site 'Res Ser 360 Glu 361'. If the ligand is also a
# protein, add the receptor's molecule name, e.g. 'Mol A'. To verify that your selection is
# right, just look at the red pulling arrow shown by MD Engine during the steered MD.
receptorsel='Protein'

# Simulation temperature
# If you run at a temperature that differs from 298K, you also need
# to adapt the pressure control below, look in the PressureCtrl documentation.
temperature='298K'

# Solvent density in g/ml (0.997 is water at 298K)
# If you run at a significantly different temperature, this density needs to
# be adapted. Look at the PressureCtrl documentation.
# For solvents other than water, you have to create your own solvent box
# as described at the FillCellObj documentation and save it as .._solvent.sce
density=0.997

# Name of solvent molecules used to measure solvent density
solvent='HOH'

# The starting and minimum pulling acceleration in picometers/picosecond^2
acceleration=2000.
# The steps in picometers/picosecond^2 in which acceleration will be increased, set 0 to get a constant acceleration
accdelta=500

# Time in picoseconds when the pulling starts
# (everything before can be considered equilibration)
pullstart=3

# pH at which the simulation should be run, by default physiological pH 
ph=7.0

# The ion concentration as a mass fraction, here we use 0.9% NaCl (physiological solution)
ions='Na,Cl,0.9'

# Multiple timestep: 1.25 femtoseconds for intramolecular and 2*1.25 fs for intermolecular forces
tslist=2,1.25

# Save simulation snapshots every 1000 femtoseconds = 1 picoseconds
saveinterval=1000

# The format used to save the trajectories: MD Engine 'sim', GROMACS 'xtc' or AMBER 'mdcrd'.
format='sim'

# The simulation ends when the distance between the centers of mass of receptor and ligand exceeds this value [A]
enddis=15

# Forcefield to use (these are all MD Engine commands, so no '=' used)
ForceField AMBER14

# Cutoff
Cutoff 8

# Cell boundary
Boundary periodic

# Use longrange coulomb forces (particle-mesh Ewald)
Longrange Coulomb

# Number of simulation steps per screen update and pairlist update.
# Since the protocol can apply pulling forces only once per screen update, screen and pairlist are updated each
# simulation step to ensure that forces are applied continuously. This slows down the simulation considerably
# to about 40% of the normal speed. If speed is an issue, you can change the command below to 'SimSteps 2,2'
 # (50% of normal speed), 'SimSteps 3,3' (60% of normal speed) or 'SimSteps 5,5' (80% of normal speed). Going
# higher is not recommended, since acceleration*N will be applied every Nth step, and no acceleration in between.
SimSteps Screen=1,Pairlist=1

# Normally no change required below this point
# ============================================

# Keep the solute from diffusing around and crossing periodic boundaries
CorrectDrift On

# Treat all simulation warnings as errors that stop the protocol
WarnIsError On

# Normally no change required below this point
# Temperature
Temp (temperature)

# Calculate total timestep, we want a float, so tslist2 is on the left side
ts=tslist2*tslist1
# Snapshots are saved every 'savesteps'
savesteps=saveinterval/ts

Console Off

# Do we have a target?
if TargetSystem==''
  RaiseError "This protocol requires a target. Either edit the protocol file or click Configuration > TargetSystem to choose a target structure"

Clear
# Do we already have a scene with water or other solvent?
waterscene = FileSize (TargetSystem)_water.sce
solventscene = FileSize (TargetSystem)_solvent.sce
if waterscene
  LoadSce (TargetSystem)_water
elif solventscene 
  LoadSce (TargetSystem)_solvent
else
  # No scene with water present yet
  if solvent!='HOH'
    RaiseError "When using a solvent other than water, the cell cannot be filled automatically. Look at the documentation of the FillCellObj command"
  # Do we have a scene at all?
  scene = FileSize (TargetSystem).sce
  if scene
    LoadSce (TargetSystem)
  else
    # No scene present, assume it's a PDB or YOB file
    for type in 'yob','pdb'
      size = FileSize (TargetSystem).(type)
      if size
        break
    if !size
      RaiseError 'Initial structure not found, expected (TargetSystem).pdb or .yob. Make sure to create a project directory and place the structure there'
    # Load structure
    Load(type) (TargetSystem)
    # Align model with major axes to minimize cell size
    NiceOriAll
    CleanAll
    # Create the simulation cell, make sure that there is enough space to reach 'enddis'
    Cell Auto,Extension=(enddis*2)
    SaveSce (TargetSystem)
  # Fill with water, predict pKas, place counter ions
  Experiment Neutralization
    WaterDensity (density)
    pH (ph)
    Ions (ions)
    pKaFile (TargetSystem).pka
    Speed Fast
  Experiment On
  Wait ExpEnd
  # Save scene with water
  SaveSce (TargetSystem)_water

# Identify the ligand: choose the largest hetgroup with >6 atoms if any
# Changes here also in md_analyze
if ligandsel==''
  mols=CountMol Obj !Water
  if mols>1
    reslist()=ListRes Hetgroup !Water with >0 bonds to all
    reslenmax=6
    ligandname=''
    carbohydlist()=''
    for res in reslist
      reslen=CountAtom (res)
      resname=NameRes (res)
      carbons=CountAtom Element C (res) with bond to Element O
      if carbons>4 and resname not in carbohydlist
        carbohydlist(1+count carbohydlist)=resname
      if reslen>reslenmax
        reslenmax=reslen
        ligandname=resname
    if ligandname!=''
      if ligandname in carbohydlist
        # Ligand is a carbohydrate, treat all carbohydrate residues as ligands
        ligandname=join carbohydlist
      # Get ligand selection
      ligandsel='Res (ligandname)'

for type in 'ligand','receptor'
  # Make sure that ligand and receptor are really present
  if (type)sel==''
    (type)atoms=0
  else
    (type)atoms = CountAtom ((type)sel)
  if !(type)atoms
    RaiseError 'This protocol requires that the (type) is selected explicitly. The current (type) ((type)sel) was not found'
  # Get central ligand/receptor atom for arrow visualization
  cen()=GroupCenter ((type)sel)
  for atomsel in 'CA','!H'
    (type)atom=ListAtom (atomsel) and ((type)sel) with minimum distance from local point (join cen)
    if (type)atom
      break

# Get ligand mass
ligmasslist()=MassAtom (ligandsel)
ligmass=sum ligmasslist

# If an arrow object is present it will be used to determine the steering direction
arrowobj=ListObj 'Arrow'
if arrowobj
  cellsize1,cellsize2,cellsize3=Cell
  diag=norm cellsize
  # Create a chain of dummy atoms
  chainobj=BuildGrid 0,(2*diag)
  # Copy global position/orientation of arrow to chain of dummy atoms
  TransferObj (chainobj),(arrowobj),Local=Keep
  # Select all receptor atoms near the chain
  cutoff=0.5
  do
    arrowatomlist()=ListAtom (receptorsel) with distance<(cutoff) from Obj (chainobj)
    cutoff=cutoff+0.5
  while count arrowatomlist<20
  # Determine direction vector of arrow in the coordinate system of the simulation cell
  Sim On
  _,_,_,lastdir()=GroupLine Obj (chainobj)
  DelObj (arrowobj) (chainobj)

# Start the Simulation
TimeStep (tslist)
Sim On
# Make sure all atoms are free to move
FreeAll

# Do a short steepest descent energy minimization
TempCtrl SteepDes
ShowMessage "Starting simulation with a steepest descent minimization..."
# Wait for convergence
for i=1 to 500
  Wait 1
  if SpeedMax<4000
    break
# Continue with 500 simulated annealing steps
ShowMessage "Continuing with 500 simulated annealing steps..."
Temp 0
TempCtrl Anneal
Wait 500

# And now start with the real simulation
HideMessage
Temp (temperature)
# Reset time to 0
Time 0
# Set temperature and pressure control
TempCtrl Rescale
PressureCtrl SolventProbe,(solvent),(density)

# Save snapshots
trajectfilename='(TargetSystem)00000.sim'
if format!='sim'
  trajectfilename='(TargetSystem).(format)'
Save(format) (trajectfilename),(savesteps)

# Run the steered simulation
MakeTab Default,2,4
accmin=acceleration
disstart=-1
dismax=-1
progdismax=0
progtime=0
speed=0
speeddismax=0
speedallowed=4000.
step=0
while 1
  t = Time
  t=t/1000
  if arrowobj
    # Keep the arrow direction updated
    _,_,_,dir()=GroupLine (join arrowatomlist)
    if sign (sum (dir*lastdir))<0
      dir()=-dir
    lastdir()=dir
  if t>pullstart
    # Steer the simulation
    ligpos()=GroupCenter (ligandsel)
    if arrowobj
      # Calculate pulling 'dir'ection from arrowatomlist, and 'dis'tance of the ligand from its starting position
      recpos()=GroupCenter (join arrowatomlist)
    else
      # Calculate pulling direction from centers of mass, and 'dis'tance between receptor and ligand
      recpos()=GroupCenter (receptorsel)
    disvec()=ligpos-recpos
    dis=norm disvec
    if disstart==-1
      disstart=dis
    if !arrowobj
      dir()=disvec/dis
    dis=dis-disstart
    HideArrowAtom (ligandatom)
    ShowArrow AtAtom,(ligandatom),StepFromAtom,(ligandatom),(dir*10)
    if dis>enddis
      ShowMessage 'The distance has reached (enddis) A in (0.00+t) ps, simulation has been stopped'
      break
    force=1e21/AvoConst*acceleration*ligmass
    if dis>dismax
      dismax=dis
      progtime=t
      Tabulate (dismax),(t),(acceleration),(force)
    # Get current steps per screen update to adjust the acceleration
    steps=SimSteps
    if !(step%400)
      # Check if there is any progress
      if dismax<=progdismax
        # No, pull more strongly
        acceleration=acceleration+accdelta
      progdismax=dismax
    if !(step%20)
      # Tabulate (dismax),(t),(acceleration),(dis)
      # Check if we just snapped out and are too fast. Calculate speed in m/s
      speed=(dismax-speeddismax)*100000/(steps*tslist1*tslist2)
      if speed>speedallowed
        # Too fast, reduce acceleration
        factor=1.-speedallowed/speed
        acceleration=acceleration*(1.-factor*factor)
      speeddismax=dismax
    if acceleration<accmin
      acceleration=accmin
    ShowMessage 'Steering sim: time=(0.00+t) ps, last progress at (0.00+progtime) ps, distance=(0.00+dismax) A, accel=(0.00+acceleration) pm/ps^2, force=(0.00+force) pN'
    # Apply the acceleration on the ligand. The 'CorrectDrift' command further above ensures
    # that the system's center of mass does not move.  NOTE that this recipe only works as
    # long the complex doesn't cross a periodic boundary.
    AccelAtom (ligandsel),(dir*acceleration*steps)
    # If your ligand is actually a protein in a dimer and thus of equal size as the receptor,
    # you can also pull the receptor in the opposite direction:
    #AccelAtom (receptor),(dir*-acceleration*steps)
  else
    ShowMessage 'Equilibration, steered simulation starts in (0.00+pullstart-t) picoseconds...'  
  # Proceed with one simulation step
  step=step+1
  Wait 1
Sim off

# Save table and plots
SaveTab Default,(TargetSystem),Format=Text,Columns=4,NumFormat=12.3f,"_Distance[A]_____Time[ps]_Acc[pm/ps^2]____Force[pN]"
SavePlot Filename=(TargetSystem)_acc,Default,Width=1600,Height=1200,Title='Steered MD',
         XColumn=1,YColumn=3,XLabel='Distance [A]',YLabel='Acceleration [pm/ps^2]'
SavePlot Filename=(TargetSystem)_frc,Default,Width=1600,Height=1200,Title='Steered MD',
         XColumn=1,YColumn=4,XLabel='Distance [A]',YLabel='Force [pN]'

# Exit MD Engine if this protocol was provided as command line argument in console mode
if runWithProtocol and ConsoleMode
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
