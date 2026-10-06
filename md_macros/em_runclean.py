def execute_md_protocol():
    """
    Executes the MD Protocol Configuration.
    """
    protocol_config = r"""
# TOPIC:       4. Molecular modeling
# TITLE:       Running an energy minimization
# REQUIRES:    Dynamics
# DESCRIPTION: This macro cleans the soup and then runs an energy minimization. Compared to the normal minimization experiment, it temporarily adds a water shell so that all force fields can be used directly, also those optimized for use with explicit solvent

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
# Prepare the structure for minimization
CleanAll
if Structure
  # Optimize the hydrogen-bonding network
  OptHydAll
# Run the normal minimization protocol
include em_run

    """
    return protocol_config

if __name__ == "__main__":
    execute_md_protocol()
