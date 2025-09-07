# n1c_core/config.py

import os
from pathlib import Path

# ---------------------------
# General Project Settings
# ---------------------------
PROJECT_NAME = "N1C"
PROJECT_VERSION = "0.1.0"
DEBUG = True  # Set False for production
LOG_LEVEL = "DEBUG" if DEBUG else "INFO"

# ---------------------------
# Ledger Settings
# ---------------------------
DEFAULT_ANCHOR_SPREAD = 2.0   # Minimum anchor spread in %
MAX_ANCHOR_SPREAD = 7.0       # Maximum anchor spread in %
DEFAULT_ANCHOR_TAX = 0.0      # Default anchor tax in %
DEFAULT_TRANSACTION_FEE = 0.0 # Base fee if no anchor

# ---------------------------
# Wallet Settings
# ---------------------------
DEFAULT_WALLET_BALANCE = 0.0
WALLET_ADDRESS_PREFIX = "n1c_"

# ---------------------------
# Network / P2P Settings
# ---------------------------
DEFAULT_NODE_HOST = "127.0.0.1"
DEFAULT_NODE_PORT = 8000
MAX_PEERS = 50
PEER_DISCOVERY_INTERVAL = 30  # Seconds between peer discovery attempts
LEDGER_SYNC_INTERVAL = 60     # Seconds between ledger sync

# ---------------------------
# Paths
# ---------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
LEDGER_DB_PATH = BASE_DIR / "data" / "ledger.db"
WALLET_KEYS_PATH = BASE_DIR / "data" / "keys"

# Ensure directories exist
os.makedirs(LEDGER_DB_PATH.parent, exist_ok=True)
os.makedirs(WALLET_KEYS_PATH, exist_ok=True)

# ---------------------------
# Cryptography Settings
# ---------------------------
SIGNATURE_ALGORITHM = "Ed25519"
KEY_SIZE = 256  # Bits for Ed25519 (fixed standard)

# ---------------------------
# Misc Settings
# ---------------------------
MAX_TRANSACTION_AMOUNT = 1_000_000.0  # Example limit
TRANSACTION_ID_LENGTH = 32
