def execute_md_protocol():
    """
    Executes the MD Protocol Configuration.
    """
    protocol_config = r"""
# TOPIC:       3. Molecular Dynamics
# TITLE:       Play back a molecular dynamics trajectory
# REQUIRES:    Dynamics
# DESCRIPTION: This macro provides an interactive molecular dynamics trajectory player

# You can either set the target structure by clicking on Options > Macro > Set target,
# by providing it as command line argument (see docs at Essentials > The command line),
# or by uncommenting the line below and specifying it directly.
#MacroTarget = 'c:\MyProject\1crn'

# Set playback waittime (1 is maximum playback speed)
waittime=12

# Forcefield to use (these is a MD Engine commands, so no '=' used)
# Note that the force field has no influence on the trajectory playback.
ForceField AMBER14

# If you press the 'Superpose on start structure' button, the following
# atoms will be superposed, use e.g. 'Backbone Res 30-40 80-95' to superpose on
# some core residues instead.
supatomsel='All'

# In case the simulation was run without 'CorrectDrift on' and the solute diffused
# through a periodic boundary, you can keep it centered here by specifying the number
# of an atom close to the core of the solute, which will be kept at the cell center.
central=0

# No changes required below this point!

# Speed up playback using short dummy cutoff and no longrange forces
Cutoff 2.62
Longrange None
# Do we have a target?
if MacroTarget==''
  RaiseError "This macro requires a target. Either edit the macro file or click Options > Macro > Set target to choose a target structure"
# Do we have a scene with water?
scene = FileSize (MacroTarget)_water.sce
if not scene
  RaiseError 'Could not find initial scene file (MacroTarget)_water.sce. You must run a simulation with the macro md_run first'
# Load the scene
Clear
LoadSce (MacroTarget)_water
# See if we can superpose on the start structure
supatoms = CountAtom (supatomsel) Obj 1
superposed=0
if supatoms
  # Create a copy of the starting structure to be used as superposition target
  superposed=1
  startobj = DuplicateObj 1
  RemoveObj (startobj)
  # Get a list of the start atom of each object to split them again later
  extraobjs=0
  objstart=1
  for i=1 to Objects
    objatoms = CountAtom Obj (i)
    if objatoms
      extraobjs=extraobjs+1
      startlist(extraobjs)=objstart
      objstart=objstart+objatoms
SwitchObj Water,off
# Pick a nice style
Style Backbone=Ribbon,Sidechain=Stick
Console off

# Create the MD trajectory player user interface
# Print headline to the HUD
PrintHUD
Font Arial,Height=20,Color=White,Spacing=1.5
PosText X=160,Y=8,Justify=Center
Print 'MD Trajectory Player'
FillRect X=25,Y=30,Width=270,Height=1,Color=White
Font Height=15,Spacing=1.5
PosText X=25,Y=50,Justify=Left
Print 'Snapshot:\nTime:'
# Create the clickable timer on the right
Font MonoSpaced,Spacing=1
gpos=240,120
FillRect (gpos1),(gpos2+5),Width=32,Height=241,Color=White
for i=0 to 10
  PosText (gpos1/8+6),(gpos2/12+i*2+1),Justify=Left
  Print '(i*10)%'
  FillRect (gpos1+32),(gpos2+i*24+5),Width=8,Height=1,Color=White
  # Top and bottom button have half the height
  if !i
    y=gpos2+6
    h=12
  else
    y=gpos2+i*24-7
    h=24-12*(i==10)
  ShowButton X=(gpos1+16),Y=(y),Width=30,Height=(h),Border=0,
             Color=(i*320/11),Action='Go ClickTimer,GoPar=(i)'
PosText (gpos1/8+3),(gpos2/12+22),Justify=Center
Print 'Click'
PosText (gpos1/8+3),(gpos2/12+23),Justify=Center
Print 'above'
# Create the buttons
Font Arial,Height=14,Color=White,Spacing=1.5
ShowButton 'Play',X=70,Y=120
ShowButton 'Pause',X=160,Y=120
ShowButton 'Step backward',X=120,Y=170
ShowButton 'Step forward',X=120,Y=220
ShowButton 'Fast backward',X=120,Y=270
ShowButton 'Fast forward',X=120,Y=320
ShowButton 'Rewind to start',X=120,Y=370

# Backwards compatibility: Starting with MD Engine version 12.8.1, XTC trajectories no longer contain a number in the filename
old = FileSize (MacroTarget)00000.xtc
if old
  RenameFile (MacroTarget)00000.xtc,(MacroTarget).xtc
# Determine trajectory format and last snapshot number
firstsnapshot=00000
for format in 'xtc','mdcrd','sim'
  found = FileSize (MacroTarget).(format)
  if found
    # It would take too long to scan the XTC/MDCrd file for the last snapshot
    lastsnapshot=-1
    filename='(MacroTarget).(format)'
    break
if format=='sim'
  # Quickly determine the last snapshot number
  lastsnapshot=firstsnapshot
  step=10000
  for j=1 to 5
    for k=1 to 9
      sim = FileSize (MacroTarget)(lastsnapshot+step).sim
      if not sim
        break
      lastsnapshot=lastsnapshot+step
    step=step/10

step=1
delay=waittime
i=firstsnapshot
if superposed
  # Add the superpose button
  Go SuperposeOnStartStructure

# Main playback loop
MainLoop:
while 1
  if i<0 and lastsnapshot!=-1
    i=i+1+lastsnapshot
  if i<0 or (lastsnapshot!=-1 and i>lastsnapshot)
    Go RewindToStart
  # Show the snapshot number, clearing the area before
  FillRect X=125,Y=48,Width=190,Height=50
  Font Height=15,Spacing=1.5
  PosText X=125,Y=50,Justify=Left
  Print '(1+i)/(0+lastsnapshot+1)\n'
  if lastsnapshot>0
    # Show the '>' at the timer on the right
    FillRect X=(gpos1-20),Y=(gpos2),Width=15,Height=260
    PosText X=(gpos1-20),Y=(gpos2+240*i/lastsnapshot-1)
    Print '>'
  # Load next snapshot
  if format=='sim'
    LoadSim (MacroTarget)(i)
  else
    last = Load(format) (filename),(i+1)
    if last
      lastsnapshot=0+i
  i=i+step
  # Show the snapshot time
  PosText X=125,Y=50
  simtime=Time
  Print '\n(0.0+simtime/1000) ps'
  if central
    # Keep a chosen atom at the center of the cell (Cell returns center as values 7-9) 
    _,_,_,_,_,_,cen() = Cell
    pos() = PosAtom (central)
    MoveAtom all,(cen-pos)
  if superposed
    # Remember the original object names and visibilities, will be changed by split/join
    namelist() = NameObj Atom (join startlist)
    switchlist() = SwitchObj Atom (join startlist)
    # Join all extra objects to the first one
    JoinObj Atom (join startlist),1
    # Superpose on the start structure using only the atom range belonging to
    # the original object 1 before the others were joined.
    AddObj (startobj)
    SupAtom (supatomsel) and 1-(startlist(2)-1),(supatomsel) Obj (startobj)
    RemoveObj (startobj)
    # Split the objects again and restore proper names
    SplitObj 1,Center=no,Atom (join startlist)
    # Restore original object names and visibilities
    for j=1 to count startlist
      NameObj Atom (startlist(j)),(namelist(j))
      SwitchObj Atom (startlist(j)),(switchlist(j))
    # The cell is not placed correctly now, switch it off 
    SwitchObj SimCell,off
  # Make sure that the simulation does not continue while we wait
  Sim Pause
  if step
    # Wait a bit
    Wait (delay)
  else
    # Pause mode, wait until next click
    Wait forever
  
# Press the Play button
Play:
step=1
delay=waittime
Go MainLoop
  
# Press the Pause button
Pause:
step=0
delay=waittime
Go MainLoop
  
# Press the step forward button
StepForward:
i=i+1
Go MainLoop

# Press the step backward button
StepBackward:
i=i-1
Go MainLoop

# Press the fast forward button
FastForward:
step=1
delay=1
Go MainLoop

# Press the fast backward button
FastBackward:
step=-1
delay=1
Go MainLoop

# Press the rewind to start button
RewindToStart:
i=firstsnapshot
if step<0
  Go Play
Go MainLoop

# Press the superpose on start structure button
SuperposeOnStartStructure:
Wait 10
superposed=superposed^1
if superposed
  buttoncol='303030'
  fontcol='Black'
else
  buttoncol='808080'
  fontcol='White'
Font Arial,Height=14,Color=(fontcol),Spacing=1.5
ShowButton 'Superpose on start structure',X=160,Y=420,Color=(buttoncol)
Font Arial,Height=14,Color=White,Spacing=1.5
Go MainLoop

# Click the timer on the right
ClickTimer:
if lastsnapshot!='?'
  i=lastsnapshot*GoPar/10
Go MainLoop



    """
    return protocol_config

if __name__ == "__main__":
    execute_md_protocol()
