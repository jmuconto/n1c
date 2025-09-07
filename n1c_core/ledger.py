# n1c_core/ledger.py

from datetime import datetime
from typing import Dict, Optional
from n1c_core.models import Wallet, Transaction, Anchor
from n1c_core.ledger_rules import (
    verify_balance,
    validate_transaction,
    calculate_fee,
)


class Ledger:
    """
    Ledger class manages all wallets, transactions, and anchors.
    It enforces ledger rules and applies transactions.
    """

    def __init__(self):
        self.wallets: Dict[str, Wallet] = {}       # wallet address -> Wallet
        self.transactions: Dict[str, Transaction] = {}  # tx_id -> Transaction
        self.anchors: Dict[str, Anchor] = {}       # anchor_id -> Anchor

    # ---------------------------
    # Wallet Management
    # ---------------------------
    def create_wallet(self, address: str) -> Wallet:
        if address in self.wallets:
            raise ValueError(f"Wallet {address} already exists")
        wallet = Wallet(address=address, balance=0.0, transactions=[])
        self.wallets[address] = wallet
        return wallet

    def get_wallet(self, address: str) -> Optional[Wallet]:
        return self.wallets.get(address)

    # ---------------------------
    # Anchor Management
    # ---------------------------
    def register_anchor(self, anchor_id: str, spread: float = 2.0, tax_rate: float = 0.0) -> Anchor:
        if anchor_id in self.anchors:
            raise ValueError(f"Anchor {anchor_id} already exists")
        anchor = Anchor(anchor_id=anchor_id, spread=spread, tax_rate=tax_rate)
        self.anchors[anchor_id] = anchor
        return anchor

    def get_anchor(self, anchor_id: str) -> Optional[Anchor]:
        return self.anchors.get(anchor_id)

    # ---------------------------
    # Transaction Management
    # ---------------------------
    def add_transaction(
        self,
        tx_id: str,
        sender_address: str,
        receiver_address: str,
        amount: float,
        signature: str,
        anchor_id: Optional[str] = None,
    ) -> Transaction:
        """
        Add a new transaction to the ledger after validation.
        """
        if tx_id in self.transactions:
            raise ValueError(f"Transaction {tx_id} already exists")

        sender_wallet = self.get_wallet(sender_address)
        receiver_wallet = self.get_wallet(receiver_address)

        if not sender_wallet or not receiver_wallet:
            raise ValueError("Sender or receiver wallet does not exist")

        # Determine anchor fee if anchor provided
        anchor = self.get_anchor(anchor_id) if anchor_id else None
        fee = calculate_fee(amount, anchor.spread if anchor else 0.0)
        tax = amount * (anchor.tax_rate / 100) if anchor else 0.0

        tx = Transaction(
            tx_id=tx_id,
            sender=sender_address,
            receiver=receiver_address,
            amount=amount,
            fee=fee,
            timestamp=datetime.utcnow(),
            signature=signature,
        )

        # Validate transaction against rules
        if not validate_transaction(tx, sender_wallet, receiver_wallet):
            raise ValueError("Transaction validation failed")

        # Apply transaction
        sender_wallet.balance -= (amount + fee + tax)
        receiver_wallet.balance += amount

        # Record transaction in wallets and ledger
        sender_wallet.transactions.append(tx)
        receiver_wallet.transactions.append(tx)
        self.transactions[tx_id] = tx

        return tx

    # ---------------------------
    # Ledger Utilities
    # ---------------------------
    def get_transaction(self, tx_id: str) -> Optional[Transaction]:
        return self.transactions.get(tx_id)

    def get_all_transactions(self):
        return list(self.transactions.values())

    def recalculate_wallet_balance(self, address: str) -> float:
        """
        Recalculate wallet balance from transaction history.
        Useful for verification.
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
    # Validation Helpers
    # ---------------------------
    def verify_integrity(self) -> bool:
        """
        Verify that all wallets balances match transaction history.
        Returns True if all balances are consistent.
        """
        for wallet in self.wallets.values():
            calculated = self.recalculate_wallet_balance(wallet.address)
            if abs(calculated - wallet.balance) > 1e-8:  # Allow minor float rounding
                return False
        return True
