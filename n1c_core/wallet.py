# n1c_core/wallet.py

from typing import Dict, List, Optional
from n1c_core.models import Wallet, Transaction
from n1c_core.utils import generate_wallet_address, generate_keypair


class WalletManager:
    """
    Manages wallets: creation, retrieval, balances, and transaction histories.
    """

    def __init__(self):
        # Wallet storage: address -> Wallet object
        self.wallets: Dict[str, Wallet] = {}

        # Private keys storage (in-memory, for demonstration purposes)
        self.private_keys: Dict[str, str] = {}
        self.public_keys: Dict[str, str] = {}

    # ---------------------------
    # Wallet Creation
    # ---------------------------
    def create_wallet(self, owner_name: str) -> Wallet:
        """
        Create a new wallet with a generated address and keypair.
        """
        address = generate_wallet_address(owner_name)
        if address in self.wallets:
            raise ValueError(f"Wallet with address {address} already exists")

        # Generate keypair
        private_key, public_key = generate_keypair()
        self.private_keys[address] = private_key
        self.public_keys[address] = public_key

        wallet = Wallet(
            address=address,
            balance=0.0,
            transactions=[]
        )
        self.wallets[address] = wallet
        return wallet

    # ---------------------------
    # Wallet Retrieval
    # ---------------------------
    def get_wallet(self, address: str) -> Optional[Wallet]:
        return self.wallets.get(address)

    def get_private_key(self, address: str) -> Optional[str]:
        return self.private_keys.get(address)

    def get_public_key(self, address: str) -> Optional[str]:
        return self.public_keys.get(address)

    # ---------------------------
    # Balance Management
    # ---------------------------
    def get_balance(self, address: str) -> float:
        wallet = self.get_wallet(address)
        if not wallet:
            raise ValueError("Wallet not found")
        return wallet.balance

    def recalculate_balance(self, address: str) -> float:
        """
        Recalculate balance from transaction history.
        """
        wallet = self.get_wallet(address)
        if not wallet:
            raise ValueError("Wallet not found")

        balance = 0.0
        for tx in wallet.transactions:
            if tx.receiver == address:
                balance += tx.amount
            if tx.sender == address:
                balance -= (tx.amount + tx.fee)
        wallet.balance = balance
        return balance

    # ---------------------------
    # Transaction History
    # ---------------------------
    def get_transactions(self, address: str) -> List[Transaction]:
        wallet = self.get_wallet(address)
        if not wallet:
            raise ValueError("Wallet not found")
        return wallet.transactions

    # ---------------------------
    # Utility Methods
    # ---------------------------
    def wallet_exists(self, address: str) -> bool:
        return address in self.wallets
