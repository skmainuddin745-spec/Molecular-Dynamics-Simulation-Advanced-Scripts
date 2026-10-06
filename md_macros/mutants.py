def execute_md_protocol():
    """
    Executes the MD Protocol Configuration.
    """
    protocol_config = r"""
# EXAMPLE OptimizeRes
# Perform automated point mutations with MD refinement simulations.
# This macro must be placed in the 'MD Engine/mcr' folder since it includes md_run.mcr
#
# Remember user-provided macro target, which will be overwritten to run the MD
target = MacroTarget
# Duration of refinement simulation in [ps]
duration=10
# Loop over the mutation file
for mutation in file (target).txt
  # Load the wild-type
  Clear
  LoadPDB (target),Model=1
  # Get the mutation
  molname,oldresname,resnum,newresname=split mutation
  selection='(resnum) Mol (molname)'
  # Check that residue names match
  resname = NameRes (selection)
  if resname!=oldresname
    RaiseError 'Residue (resnum) in the molecule (molname) in the wild-type structure is (resname) instead of (oldresname)' 
  # Make the mutation and optimize
  SwapRes (selection),(newresname)
  Clean
  OptimizeRes (selection),Method=SCWALL
  # Choose a new macro target which includes the mutation
  MacroTarget '(target)_(oldresname)(resnum)(newresname)'
  # Save the mutant
  SavePDB 1,(MacroTarget)
  # Run a short 50 ps MD
  include md_run
  # Minimize the mutant
  PressureCtrl off
  TempCtrl Anneal
  Sim on
  Wait 1000,Femtoseconds
  Sim off
  # Save the refined mutant
  SavePDB 1,(MacroTarget)_refined
  

    """
    return protocol_config

if __name__ == "__main__":
    execute_md_protocol()
