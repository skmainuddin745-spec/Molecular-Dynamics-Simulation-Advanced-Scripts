def execute_md_protocol():
    """
    Executes the MD Protocol Configuration.
    """
    protocol_config = r"""
# TOPIC:       3. Molecular Dynamics
# TITLE:       Analyzing a molecular dynamics trajectory in blocks
# REQUIRES:    Dynamics
# DESCRIPTION: This macro analyzes a simulation in blocks. MD Engine runs for each block the md_analyze macro and creates in the end a single report containing detailed information about the system, e.g. energies, RMSDs, hydrogen bonds per block. By default the simulation snapshots are split into 3 blocks, so the second and third block can be compared to see if convergence has been reached. The number of blocks can be freely choosen as well as setting the number of snapshots to be compiled into one block instead. For more information about the methods used and how to add your own analysis see the md_analyze macro.

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
    found=FileSize (MacroTarget).(format)
    if found
      break
  # Load scene with water or other solvent
  if format!='sim'
    waterscene=FileSize (MacroTarget)_water.sce
    solventscene=FileSize (MacroTarget)_solvent.sce
    if waterscene
      LoadSce (MacroTarget)_water
    elif solventscene 
      LoadSce (MacroTarget)_solvent
    else
      RaiseError 'Could not find initial scene file (MacroTarget)_water.sce. You must run a simulation with the macro md_run first'
  # Count the number of snapshots to determine 'blocksnapshots'
  snapshots=0
  while (1)
    if !(snapshots&7)
      ShowMessage 'Counting snapshots: (snapshots)'
      Wait 1
    if format=='sim'
      sim=FileSize (MacroTarget)(00000+snapshots).sim
      if !sim
        break
    else
      sim=Load(format) (MacroTarget),(1+snapshots)
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
  RenameFile (MacroTarget)_energymin.sce,(MacroTarget)_energymin(id).sce,overwrite=yes
  RenameFile (MacroTarget)_energymin.pdb,(MacroTarget)_energymin(id).pdb,overwrite=yes
  RenameFile (MacroTarget)_analysis.tab,(MacroTarget)_analysis(id).tab,overwrite=yes
  RenameFile (MacroTarget)_average.pdb,(MacroTarget)_average(id).pdb,overwrite=yes
  # rmsfsaved, rdfsellist and dccmsel are set by the included md_analyze macro above
  if dccmsel!=''
    RenameFile (MacroTarget)_dccm.tab,(MacroTarget)_dccm(id).tab,overwrite=yes
    RenameFile (MacroTarget)_dccm.sce,(MacroTarget)_dccm(id).sce,overwrite=yes
  if count rdfsellist==4
    RenameFile (MacroTarget)_rdf.tab,(MacroTarget)_rdf(id).tab,overwrite=yes
    RenameFile (MacroTarget)_rdf.sce,(MacroTarget)_rdf(id).sce,overwrite=yes
  RenameFile (MacroTarget)_rmsf.tab,(MacroTarget)_rmsf(id).tab,overwrite=yes
  block=block+1
  # 'last' is set to 1 by the included md_analyze macro above if the last snapshot was encountered.
while !last
    """
    return protocol_config

if __name__ == "__main__":
    execute_md_protocol()
