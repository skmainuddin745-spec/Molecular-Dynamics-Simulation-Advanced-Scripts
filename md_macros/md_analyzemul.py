def execute_md_protocol():
    """
    Executes the MD Protocol Configuration.
    """
    protocol_config = r"""
# TOPIC:       3. Molecular Dynamics
# TITLE:       Analyzing a molecular dynamics trajectory of multiple objects
# REQUIRES:    Dynamics
# DESCRIPTION: This macro analyzes a simulation and creates a table with energies and RMSDs from the starting structures for multiple objects

# The structure to analyze must be present with a .sce extension.
# You can either set the target structure by clicking on Options > Macro > Set target,
# by providing it as command line argument (see docs at Essentials > The command line),
# or by uncommenting the line below and specifying it directly.
#MacroTarget = 'c:\MyProject\1crn'

# Forcefield to use
ForceField AMBER14,SetPar=Yes

# Selection of objects to analyze
# If one of the objects is an oligomer, check the documentation of the 'Sup' command at 'analyzing a simulation' to avoid pitfalls.
objselection='Protein'

# The B-factors calculated from the root-mean-square fluctuations can be too large to fit them
# into the PDB file's B-factor column. Replace e.g. 1.0 with 0.1 to scale them down to 10%
bfactorscale=1.0

# First snapshot to be analyzed, increase number to ignore an equilibration period.
# (By default, md_run.mcr saves snapshots every 25ps, choosing 40 thus starts the analysis after 1 nanosecond)
firstsnapshot=0

# All snapshots will be superposed on this reference snapshot to calculate RMSDs etc.
# The starting structure is snapshot 0.
refsnapshot=0

# No change required below this point
# ===================================

# Do we have a target?
if MacroTarget==''
  RaiseError "This macro requires a target. Either edit the macro file or click Options > Macro > Set target to choose a target structure"

Clear
Console Off

# Load scene with water or other solvent
waterscene = FileSize (MacroTarget)_water.sce
solventscene = FileSize (MacroTarget)_solvent.sce
if waterscene
  LoadSce (MacroTarget)_water
elif solventscene 
  LoadSce (MacroTarget)_solvent
else
  RaiseError 'Could not find initial scene file (MacroTarget)_water.sce. You must run a simulation with the macro md_run first'

currobjlist() = ListObj (objselection)

ShowMessage "Preparing analysis, please wait..."
Wait 1

# Backwards compatibility: Starting with MD Engine version 12.8.1, XTC trajectories no longer contain a number in the filename
old = FileSize (MacroTarget)00000.xtc
if old
  RenameFile (MacroTarget)00000.xtc,(MacroTarget).xtc
# Determine trajectory format
for format in 'xtc','mdcrd','sim'
  found = FileSize (MacroTarget).(format)
  if found
    break

if refsnapshot
  # We superpose not on the initial structure, but on a certain snapshot
  if format=='sim'
    LoadSim (MacroTarget)(00000+refsnapshot)
  else
    Load(format) (MacroTarget),(refsnapshot+1)

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
    sim = FileSize (MacroTarget)(i).sim
    if not sim
      break
    LoadSim (MacroTarget)(i)
  else
    # Set last (end of file) to 1 if last snapshot loaded
    last = Load(format) (MacroTarget),(i+1)
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
  RaiseError "This macro is meant to analyze a molecular dynamics trajectory created with md_run, but none was found in this directory"

# Save table
header='____Time[ps] Energy[(EnergyUnit)]_____Bond _______Angle ____Dihedral ___Planarity _____Coulomb _________VdW '
for i=0 to supobjects
  if i<supobjects
    id=000+currobjlist(i+1)
  else
    id='AVR'
  header=header+'RMSDs-(id):CA ____Backbone __HeavyAtoms '
SaveTab default,(MacroTarget)_analysis,Format=Text,Columns=(8+(supobjects+1)*3),NumFormat=%12.3f,(header)

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
SavePDB (currobjlist(1)),(MacroTarget)_average
HideMessage

# Exit MD Engine if this macro was provided as command line argument in console mode and not included from another macro
if runWithMacro and ConsoleMode and !IndentationLevel
  Exit

    """
    return protocol_config

if __name__ == "__main__":
    execute_md_protocol()
