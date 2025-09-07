# n1c_core/transaction.py

import uuid
from datetime import datetime
from typing import Optional
from n1c_core.models import Transaction, Wallet, Anchor
from n1c_core.ledger_rules import (
    verify_balance,
    validate_transaction,
    calculate_fee
)
from n1c_core.utils import sign_transaction, verify_signature


class TransactionManager:
    """
    Handles creation, validation, signing, and processing of transactions
    independently of the ledger. Can be used for pre-validation or offline signing.
    """

    @staticmethod
    def create_transaction(
        sender_wallet: Wallet,
        receiver_wallet: Wallet,
        amount: float,
        private_key: str,
        anchor: Optional[Anchor] = None
    ) -> Transaction:
        """
        Create a new signed transaction.

        Args:
            sender_wallet (Wallet): The sender's wallet object.
            receiver_wallet (Wallet): The receiver's wallet object.
            amount (float): Amount to transfer.
            private_key (str): Private key to sign the transaction.
            anchor (Anchor, optional): Optional anchor for fee/tax.

        Returns:
            Transaction: Signed transaction object ready to be added to ledger.
        """

        # Generate a unique transaction ID
        tx_id = str(uuid.uuid4())

        # Calculate fees
        fee = calculate_fee(amount, anchor.spread if anchor else 0.0)
        tax = amount * (anchor.tax_rate / 100) if anchor else 0.0

        # Create transaction object
        tx = Transaction(
            tx_id=tx_id,
            sender=sender_wallet.address,
            receiver=receiver_wallet.address,
            amount=amount,
            fee=fee,
            timestamp=datetime.utcnow(),
            signature=""  # To be signed
        )

        # Sign transaction
        tx.signature = sign_transaction(tx, private_key)

        return tx

    @staticmethod
    def is_valid_transaction(tx: Transaction, sender_wallet: Wallet, receiver_wallet: Wallet) -> bool:
        """
        Validate a transaction according to ledger rules.
        """
        # Verify balance
        if not verify_balance(sender_wallet, tx.amount, tx.fee):
            return False

        # Verify signature
        if not verify_signature(tx, sender_wallet.address):
            return False

        # Additional ledger validation
        return validate_transaction(tx, sender_wallet, receiver_wallet)

    @staticmethod
    def apply_transaction(tx: Transaction, sender_wallet: Wallet, receiver_wallet: Wallet):
        """
        Apply a validated transaction to the wallets.
        """
        if not TransactionManager.is_valid_transaction(tx, sender_wallet, receiver_wallet):
            raise ValueError("Transaction is invalid and cannot be applied")

        # Deduct amount + fee from sender
        sender_wallet.balance -= (tx.amount + tx.fee)

        # Add amount to receiver
        receiver_wallet.balance += tx.amount

        # Record transaction in both wallets
        sender_wallet.transactions.append(tx)
        receiver_wallet.transactions.append(tx)
