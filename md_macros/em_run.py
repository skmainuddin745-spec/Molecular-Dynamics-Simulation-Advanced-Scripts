def execute_md_protocol():
    """
    Executes the MD Protocol Configuration.
    """
    protocol_config = r"""
# TOPIC:       4. Molecular modeling
# TITLE:       Running an energy minimization
# REQUIRES:    Dynamics
# DESCRIPTION: This macro runs an energy minimization of the soup without cleaning it first. Compared to the normal minimization experiment, it temporarily adds a water shell so that all force fields can be used directly, also those optimized for use with explicit solvent

if !Atoms and MacroTarget!=''
  # No atoms but a MacroTarget is available, load the structure
  for type in 'sce','yob','pdb'
    size = FileSize (MacroTarget).(type)
    if size
      break
  if !size
    RaiseError 'Initial structure not found, expected (MacroTarget).sce,.yob or .pdb. Make sure to create a project directory and place the structure there'
  # Load structure
  Load(type) (MacroTarget)
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
  # Structure has been loaded via MacroTarget before, save the minimized structure again
  if type!='sce'
    JoinObj (join endobjlist),(endobjlist1)
    Save(type) (endobjlist1),(MacroTarget)_minimized
  else
    SaveSce (MacroTarget)_minimized
# Exit MD Engine if this macro was provided as command line argument in console mode and not included from another macro
if runWithMacro and ConsoleMode and !IndentationLevel
  Exit
Console open
    """
    return protocol_config

if __name__ == "__main__":
    execute_md_protocol()
