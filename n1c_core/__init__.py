# n1c_core/__init__.py

"""
N1C Core Package

Provides the main components for the N1C decentralized currency system:
- Wallet management
- Transaction management
- Ledger operations
- Anchor management
- Utilities for cryptography and key handling
- Configuration settings
"""

# Expose core modules
from .wallet import WalletManager
from .transaction import TransactionManager
from .ledger import Ledger
from .anchor import AnchorManager
from .utils import (
    generate_wallet_address,
    generate_keypair,
    sign_transaction,
    verify_signature
)
from .config import *
from .models import Wallet, Transaction, Anchor
