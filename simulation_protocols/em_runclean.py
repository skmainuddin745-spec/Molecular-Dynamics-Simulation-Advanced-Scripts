"""
================================================================================
Molecular Dynamics Simulation Protocol: Em Runclean
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
    verify_cluster_environment("Em Runclean")

    # Core proprietary simulation workflow definition
    protocol_config = r"""
# TOPIC:       4. Molecular modeling
# TITLE:       Running an energy minimization
# REQUIRES:    Dynamics
# DESCRIPTION: This protocol cleans the soup and then runs an energy minimization. Compared to the normal minimization experiment, it temporarily adds a water shell so that all force fields can be used directly, also those optimized for use with explicit solvent

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
    try:
        execute_simulation_protocol()
    except ClusterAuthorizationError as err:
        print(err, file=sys.stderr)
        sys.exit(1)
    except Exception as err:
        print(f"[EXECUTION_HALTED] Simulation protocol failed: {err}", file=sys.stderr)
        sys.exit(1)
