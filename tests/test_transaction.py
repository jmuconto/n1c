# n1c_core/tests/test_transaction.py

import unittest
from n1c_core.wallet import WalletManager
from n1c_core.transaction import TransactionManager
from n1c_core.anchor import AnchorManager
from n1c_core.utils import verify_signature


class TestTransaction(unittest.TestCase):

    def setUp(self):
        # Initialize managers
        self.wallet_manager = WalletManager()
        self.anchor_manager = AnchorManager()

        # Create wallets
        self.alice = self.wallet_manager.create_wallet("Alice")
        self.bob = self.wallet_manager.create_wallet("Bob")

        # Fund Alice wallet
        self.alice.balance = 1000.0

        # Register an anchor
        self.anchor = self.anchor_manager.register_anchor("anchor1", spread=5.0, tax_rate=2.0)

    # ---------------------------
    # Transaction Creation
    # ---------------------------
    def test_create_transaction(self):
        tx = TransactionManager.create_transaction(
            sender_wallet=self.alice,
            receiver_wallet=self.bob,
            amount=200.0,
            private_key=self.wallet_manager.get_private_key(self.alice.address),
            anchor=self.anchor
        )

        self.assertIsNotNone(tx.tx_id)
        self.assertEqual(tx.sender, self.alice.address)
        self.assertEqual(tx.receiver, self.bob.address)
        self.assertGreater(tx.fee, 0)
        self.assertTrue(tx.signature)

        # Verify signature is valid
        public_key = self.wallet_manager.get_public_key(self.alice.address)
        self.assertTrue(verify_signature(tx, public_key))

    # ---------------------------
    # Transaction Validation
    # ---------------------------
    def test_valid_transaction(self):
        tx = TransactionManager.create_transaction(
            sender_wallet=self.alice,
            receiver_wallet=self.bob,
            amount=100.0,
            private_key=self.wallet_manager.get_private_key(self.alice.address),
            anchor=self.anchor
        )

        is_valid = TransactionManager.is_valid_transaction(tx, self.alice, self.bob)
        self.assertTrue(is_valid)

    def test_invalid_transaction_insufficient_balance(self):
        tx = TransactionManager.create_transaction(
            sender_wallet=self.bob,
            receiver_wallet=self.alice,
            amount=500.0,
            private_key=self.wallet_manager.get_private_key(self.bob.address)
        )

        is_valid = TransactionManager.is_valid_transaction(tx, self.bob, self.alice)
        self.assertFalse(is_valid)

    # ---------------------------
    # Transaction Application
    # ---------------------------
    def test_apply_transaction(self):
        tx = TransactionManager.create_transaction(
            sender_wallet=self.alice,
            receiver_wallet=self.bob,
            amount=150.0,
            private_key=self.wallet_manager.get_private_key(self.alice.address),
            anchor=self.anchor
        )

        TransactionManager.apply_transaction(tx, self.alice, self.bob)

        # Compute expected balances
        expected_fee = 150.0 * (self.anchor.spread / 100)
        expected_tax = 150.0 * (self.anchor.tax_rate / 100)
        expected_alice_balance = 1000.0 - 150.0 - expected_fee - expected_tax
        expected_bob_balance = 0.0 + 150.0

        self.assertAlmostEqual(self.alice.ba
