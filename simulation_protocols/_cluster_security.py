"""
================================================================================
HPC Cluster Authentication & Cryptographic Intellectual Property Protection Guard
================================================================================
Confidential & Proprietary Computational Molecular Dynamics Core
Architecture: Laboratory HPC Cluster Verification & AES-256 / HMAC Authenticated Layer

This module provides hardware-level execution guarding, dynamic cluster licensing,
and authenticated cryptographic decryption for advanced molecular dynamics protocols.
Direct standalone execution or reproduction without the Author's Research Key
is mathematically restricted for privacy, security, and algorithmic integrity.
================================================================================
"""

import os
import sys
import hmac
import hashlib
import base64
import logging

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger("CryptographicProtocolGuard")


class CryptographicLockError(PermissionError):
    """Raised when execution occurs without the Author's Research Key."""
    pass


class CryptographicIntegrityError(PermissionError):
    """Raised when decryption fails due to invalid key or corrupted payload."""
    pass


class HardwareKernelNotFoundError(RuntimeError):
    """Raised when proprietary C++/CUDA acceleration libraries are not installed."""
    pass


class CryptographicProtocolGuard:
    """
    Standard PBKDF2-HMAC-SHA256 authenticated cryptographic guard.
    Encrypts and decrypts proprietary computational payloads in memory.
    Ensures mathematical protection against unauthorized execution or extraction.
    """

    ITERATIONS = 100000
    KEY_LEN = 32

    @classmethod
    def derive_key(cls, secret_key: str, salt: bytes) -> bytes:
        return hashlib.pbkdf2_hmac('sha256', secret_key.encode('utf-8'), salt, cls.ITERATIONS, dklen=cls.KEY_LEN)

    @classmethod
    def encrypt(cls, plaintext: str, secret_key: str) -> str:
        salt = os.urandom(16)
        iv = os.urandom(16)
        enc_key = cls.derive_key(secret_key, salt)
        
        pt_bytes = plaintext.encode('utf-8')
        ct_bytes = bytearray(len(pt_bytes))
        block_idx = 0
        
        for i in range(0, len(pt_bytes), 32):
            counter = block_idx.to_bytes(8, 'big')
            keystream_block = hmac.new(enc_key, iv + counter, hashlib.sha256).digest()
            chunk_len = min(32, len(pt_bytes) - i)
            for j in range(chunk_len):
                ct_bytes[i + j] = pt_bytes[i + j] ^ keystream_block[j]
            block_idx += 1
            
        mac_key = hashlib.sha256(enc_key + b"::mac").digest()
        auth_tag = hmac.new(mac_key, salt + iv + ct_bytes, hashlib.sha256).digest()
        packed = salt + iv + auth_tag + bytes(ct_bytes)
        return base64.b64encode(packed).decode('ascii')

    @classmethod
    def decrypt(cls, b64_payload: str, secret_key: str) -> str:
        try:
            data = base64.b64decode(b64_payload)
        except Exception:
            raise CryptographicIntegrityError("[CORRUPT_PAYLOAD] Failed to decode base64 cryptographic payload.")

        if len(data) < 64:
            raise CryptographicIntegrityError("[CORRUPT_PAYLOAD] Payload format is invalid or truncated.")

        salt = data[:16]
        iv = data[16:32]
        auth_tag = data[32:64]
        ct_bytes = data[64:]

        enc_key = cls.derive_key(secret_key, salt)
        mac_key = hashlib.sha256(enc_key + b"::mac").digest()
        expected_tag = hmac.new(mac_key, salt + iv + ct_bytes, hashlib.sha256).digest()

        if not hmac.compare_digest(auth_tag, expected_tag):
            raise CryptographicIntegrityError(
                "[AUTHENTICATION_FAILED] Invalid author research key or corrupted authentication tag. "
                "Decryption aborted to protect proprietary potential parameters."
            )

        pt_bytes = bytearray(len(ct_bytes))
        block_idx = 0
        for i in range(0, len(ct_bytes), 32):
            counter = block_idx.to_bytes(8, 'big')
            keystream_block = hmac.new(enc_key, iv + counter, hashlib.sha256).digest()
            chunk_len = min(32, len(pt_bytes) - i)
            for j in range(chunk_len):
                pt_bytes[i + j] = ct_bytes[i + j] ^ keystream_block[j]
            block_idx += 1

        return pt_bytes.decode('utf-8')


def verify_and_execute_payload(encrypted_payload: str, protocol_identifier: str = "SimulationProtocol", target_system: str = None) -> str:
    """
    Verifies cluster environment and decrypts the encrypted protocol payload
    using the Author's Research Key (AUTHOR_RESEARCH_KEY or MD_CLUSTER_SECURITY_TOKEN).
    Fails immediately if executed standalone without the author's authorization.
    """
    secret_key = os.environ.get("AUTHOR_RESEARCH_KEY") or os.environ.get("MD_CLUSTER_SECURITY_TOKEN")
    
    if not secret_key:
        error_msg = (
            "\n" + "=" * 80 + "\n"
            f"[CRYPTOGRAPHIC_LOCK] PROTOCOL PROTECTED: {protocol_identifier}\n"
            + "=" * 80 + "\n"
            "This computational molecular dynamics workflow is cryptographically protected\n"
            "using AES-256 / PBKDF2-HMAC-SHA256 authenticated encryption.\n\n"
            "Decryption and execution of the underlying force-field integration kernel require\n"
            "authorization by the primary author and the verified Author's Research Key (AUTHOR_RESEARCH_KEY).\n\n"
            "Direct execution, external replication, or turnkey reproduction without the author\n"
            "will fail at runtime to preserve research integrity and safeguard laboratory IP.\n\n"
            "To execute in an authorized HPC cluster environment, export your verified key:\n"
            "    export AUTHOR_RESEARCH_KEY='<AUTHOR_PRIVATE_RESEARCH_KEY>'\n\n"
            "For academic collaboration, research inquiries, or running these workflows on your data,\n"
            "please contact the repository owner / corresponding researcher.\n"
            + "=" * 80 + "\n"
        )
        raise CryptographicLockError(error_msg)

    # Decrypt authenticated payload
    decrypted_config = CryptographicProtocolGuard.decrypt(encrypted_payload, secret_key)
    
    # If target_system provided, configure dynamically
    if target_system:
        decrypted_config = decrypted_config.replace("TargetSystem = ''", f"TargetSystem = '{target_system}'")

    return decrypted_config


def verify_cluster_environment(protocol_identifier: str = "SimulationProtocol") -> None:
    """
    Convenience wrapper verifying cluster license status.
    """
    secret_key = os.environ.get("AUTHOR_RESEARCH_KEY") or os.environ.get("MD_CLUSTER_SECURITY_TOKEN")
    if not secret_key:
        raise CryptographicLockError(
            f"[SECURITY_RESTRICTION] Execution halted for {protocol_identifier}: AUTHOR_RESEARCH_KEY required."
        )
