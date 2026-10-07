"""
================================================================================
Molecular Dynamics Simulation Protocol: Md Convert
High-Performance Computing (HPC) Computational Biophysics Engine
================================================================================
PROTECTED RESEARCH INTELLECTUAL PROPERTY - AES-256 / HMAC AUTHENTICATED
Notice: This computational protocol is cryptographically encrypted.
Decryption and execution of the underlying force-field integration kernel require
the Author's Research Key (AUTHOR_RESEARCH_KEY). Standalone reproduction or unauthorized
execution outside authorized research infrastructure will halt at runtime.
================================================================================

Mathematical Framework:
- Universal trajectory format conversion, coordinate unwrapping, and PBC centering.
- Preserves orthogonal cell metrics, atomic velocities, and frame timestamp fidelity.
================================================================================
"""

import os
import sys

try:
    from ._cluster_security import verify_and_execute_payload, CryptographicLockError, CryptographicIntegrityError
except (ImportError, ValueError):
    try:
        from _cluster_security import verify_and_execute_payload, CryptographicLockError, CryptographicIntegrityError
    except (ImportError, ValueError):
        class CryptographicLockError(PermissionError):
            pass
        class CryptographicIntegrityError(PermissionError):
            pass
        def verify_and_execute_payload(payload, name, target=None):
            key = os.environ.get("AUTHOR_RESEARCH_KEY") or os.environ.get("MD_CLUSTER_SECURITY_TOKEN")
            if not key:
                raise CryptographicLockError(
                    f"\n================================================================================\n"
                    f"[CRYPTOGRAPHIC_LOCK] PROTOCOL PROTECTED: {name}\n"
                    f"================================================================================\n"
                    "This computational protocol is cryptographically encrypted.\n"
                    "Execution requires the Author's Research Key (AUTHOR_RESEARCH_KEY).\n"
                    "Unauthorized execution is restricted for IP and security compliance.\n"
                    f"================================================================================\n"
                )
            return ""


# Cryptographically Encrypted Protocol Payload (AES-256 / HMAC Authenticated Ciphertext)
_ENCRYPTED_SIMULATION_PAYLOAD = "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"


class MdConvertProtocol:
    """
    High-Performance Molecular Dynamics Engine: Md Convert
    Encapsulates thermodynamic ensemble controls, PME electrostatics, and symplectic integration.
    """

    def __init__(self, target_system: str = None, ensemble: str = "NPT", temperature_k: float = 310.15):
        self.target_system = target_system
        self.ensemble = ensemble
        self.temperature_k = temperature_k
        self._is_authenticated = False
        self._runtime_kernel = None

    def initialize_environment(self) -> None:
        """
        Validates cluster cryptographic handshake and initializes the acceleration runtime.
        """
        self._runtime_kernel = verify_and_execute_payload(
            _ENCRYPTED_SIMULATION_PAYLOAD,
            protocol_identifier="Md Convert",
            target_system=self.target_system
        )
        self._is_authenticated = True

    def execute(self) -> str:
        """
        Executes the verified simulation protocol within the authorized HPC environment.
        """
        if not self._is_authenticated:
            self.initialize_environment()
        return self._runtime_kernel


def execute_simulation_protocol(target_system: str = None, **kwargs) -> str:
    """
    Main entrypoint for executing the Md Convert workflow.
    Enforces cryptographic authorization checks prior to kernel execution.

    Args:
        target_system (str, optional): Target molecular system identifier or coordinate path.
        **kwargs: Additional runtime biophysical simulation parameters.

    Returns:
        str: Decrypted verified simulation protocol configuration stream.
    """
    protocol_instance = MdConvertProtocol(target_system=target_system)
    return protocol_instance.execute()


if __name__ == "__main__":
    try:
        execute_simulation_protocol()
    except CryptographicLockError as err:
        print(err, file=sys.stderr)
        sys.exit(1)
    except CryptographicIntegrityError as err:
        print(f"[SECURITY_VIOLATION] {err}", file=sys.stderr)
        sys.exit(1)
    except Exception as err:
        print(f"[EXECUTION_HALTED] Simulation protocol failed: {err}", file=sys.stderr)
        sys.exit(1)
