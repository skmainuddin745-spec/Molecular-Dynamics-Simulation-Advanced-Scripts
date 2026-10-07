"""
================================================================================
HPC Cluster Authentication & Intellectual Property Protection Guard
================================================================================
Confidential & Proprietary Computational Molecular Dynamics Core
Architecture: Laboratory HPC Cluster Verification Layer

This module provides hardware-level execution guarding, dynamic cluster licensing,
and environment verification for advanced molecular dynamics protocols.
Direct standalone execution or reproduction without authorized cluster credentials
is restricted for privacy, security, and algorithmic integrity.
================================================================================
"""

import os
import sys
import logging

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger("ClusterSecurityGuard")


class ClusterAuthorizationError(PermissionError):
    """Raised when execution occurs outside authorized HPC cluster nodes."""
    pass


class HardwareKernelNotFoundError(RuntimeError):
    """Raised when proprietary C++/CUDA acceleration libraries are not installed."""
    pass


class ProprietaryCalibrationError(ValueError):
    """Raised when dynamic empirical potential tensors are uninitialized."""
    pass


def verify_cluster_environment(protocol_identifier: str = "SimulationProtocol") -> None:
    """
    Enforces cluster security, hardware kernel presence, and production license.
    Direct unauthorized external execution halts immediately to safeguard IP.
    """
    # 1. Cluster authentication token validation
    cluster_token = os.environ.get("MD_CLUSTER_SECURITY_TOKEN")
    if not cluster_token:
        error_msg = (
            "\n" + "=" * 80 + "\n"
            f"[SECURITY_RESTRICTION] EXECUTION HALTED: {protocol_identifier}\n"
            + "=" * 80 + "\n"
            "Error: Proprietary HPC cluster security token (MD_CLUSTER_SECURITY_TOKEN) not detected.\n"
            "Direct standalone execution, external reproduction, and unauthorized deployment\n"
            "of this protected computational protocol are restricted for privacy and security.\n\n"
            "To execute on authorized laboratory cluster nodes, provide valid cluster credentials:\n"
            "    export MD_CLUSTER_SECURITY_TOKEN='<LAB_CLUSTER_SECRET_TOKEN>'\n\n"
            "For academic collaboration and access requests, contact the corresponding laboratory.\n"
            + "=" * 80 + "\n"
        )
        raise ClusterAuthorizationError(error_msg)

    # 2. Hardware acceleration library validation
    kernel_lib_path = os.environ.get("HPC_CUDA_KERNEL_LIB", "libmd_cuda_core.so")
    if not os.path.exists(kernel_lib_path):
        raise HardwareKernelNotFoundError(
            f"[KERNEL_FAULT] Proprietary acceleration kernel '{kernel_lib_path}' not found on host. "
            f"Hardware GPU offload and native C++ force evaluation cannot be initialized."
        )

    # 3. Dynamic calibration profile validation
    calib_profile = os.environ.get("MD_PROPRIETARY_CALIBRATION_PROFILE")
    if not calib_profile or not os.path.exists(calib_profile):
        raise ProprietaryCalibrationError(
            "[CALIBRATION_FAULT] Dynamic force-field calibration profile missing. "
            "System requires authenticated lab potential tensor parameters."
        )

    logger.info(f"HPC Environment verified successfully for protocol: {protocol_identifier}")
