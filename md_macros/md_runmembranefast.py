def execute_md_protocol():
    """
    Executes the MD Protocol Configuration.
    """
    protocol_config = r"""
# TOPIC:       3. Molecular Dynamics
# TITLE:       Running a molecular dynamics simulation of a membrane protein with maximum speed
# REQUIRES:    Dynamics
# DESCRIPTION: This macro sets up and runs a simulation of a membrane protein as quickly as possible. It scans the protein for secondary structure elements with hydrophobic surface residues, orients it accordingly and embeds it in a membrane of adjustable lipid composition. Finally a 250 ps restrained equilibration simulation is run, which ensures that the membrane can adapt to the newly embedded protein. Then the real simulation starts.

# Choose maximum speed
speed='fast'
# Include the standard membrane simulation macro to do the work
include md_runmembrane

    """
    return protocol_config

if __name__ == "__main__":
    execute_md_protocol()
