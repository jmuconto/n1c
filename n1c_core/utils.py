# n1c_core/utils.py

import hashlib
import uuid
from typing import Tuple
from n1c_core.models import Transaction
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

# ---------------------------
# Wallet Utilities
# ---------------------------

def generate_wallet_address(owner_name: str) -> str:
    """
    Generate a unique wallet address based on owner name and random UUID.
    """
    random_part = str(uuid.uuid4())
    base_string = f"{owner_name}-{random_part}"
    address = hashlib.sha256(base_string.encode()).hexdigest()
    return f"n1c_{address[:32]}"  # shorten to 32 chars for readability


def generate_keypair() -> Tuple[str, str]:
    """
    Generate an Ed25519 keypair for signing and verification.
    Returns (private_key_pem, public_key_pem) as strings.
    """
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    # Serialize keys to PEM format
    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_bytes.decode(), public_bytes.decode()


# ---------------------------
# Transaction Utilities
# ---------------------------

def sign_transaction(tx: Transaction, private_key_pem: str) -> str:
    """
    Sign a transaction using sender's private key.
    Returns base64-encoded signature string.
    """
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode(),
        password=None
    )
    message = _transaction_message(tx)
    signature = private_key.sign(message.encode())
    return signature.hex()


def verify_signature(tx: Transaction, public_key_pem: str) -> bool:
    """
    Verify transaction signature using sender's public key.
    Returns True if signature is valid.
    """
    from cryptography.exceptions import InvalidSignature
    public_key = serialization.load_pem_public_key(public_key_pem.encode())
    message = _transaction_message(tx)
    try:
        public_key.verify(bytes.fromhex(tx.signature), message.encode())
        return True
    except InvalidSignature:
        return False


def _transaction_message(tx: Transaction) -> str:
    """
    Serialize transaction fields into a canonical string for signing/verifying.
    Excludes the signature field itself.
    """
    return f"{tx.tx_id}|{tx.sender}|{tx.receiver}|{tx.amount}|{tx.fee}|{tx.timestamp.isoformat()}"
