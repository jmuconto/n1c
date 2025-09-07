# n1c_core/tests/test_ledger.py

import unittest
from datetime import datetime
from n1c_core.wallet import WalletManager
from n1c_core.transaction import TransactionManager
from n1c_core.ledger import Ledger
from n1c_core.anchor import AnchorManager
from n1c_core.utils import generate_keypair


class TestLedger(unittest.TestCase):

    def setUp(self):
        # Initialize managers
        self.wallet_manager = WalletManager()
        self.ledger = Ledger()
        self.anchor_manager = AnchorManager()

        # Create wallets
        self.alice = self.wallet_manager.create_wallet("Alice")
        self.bob = self.wallet_manager.create_wallet("Bob")

        # Store keys for signing
        self.alice_private = self.wallet_manager.get_private_key(self.alice.address)
        self.alice_public = self.wallet_manager.get_public_key(self.alice.address)

        # Fund Alice wallet for testing
        self.alice.balance = 1000.0

        # Register an anchor
        self.anchor = self.anchor_manager.register_anchor("anchor1", spread=5.0, tax_rate=2.0)

    # ---------------------------
    # Wallet Tests
    # ---------------------------
    def test_wallet_creation(self):
        self.assertTrue(self.wallet_manager.wallet_exists(self.alice.address))
        self.assertTrue(self.wallet_manager.wallet_exists(self.bob.address))
        self.assertEqual(self.alice.balance, 1000.0)
        self.assertEqual(self.bob.balance, 0.0)

    # ---------------------------
    # Transaction Tests
    # ---------------------------
    def test_create_transaction(self):
        tx = TransactionManager.create_transaction(
            sender_wallet=self.alice,
            receiver_wallet=self.bob,
            amount=200.0,
            private_key=self.alice_private,
            anchor=self.anchor
        )
        self.assertIsNotNone(tx.tx_id)
        self.assertEqual(tx.sender, self.alice.address)
        self.assertEqual(tx.receiver, self.bob.address)

    def test_apply_transaction(self):
        tx = TransactionManager.create_transaction(
            sender_wallet=self.alice,
            receiver_wallet=self.bob,
            amount=200.0,
            private_key=self.alice_private,
            anchor=self.anchor
        )
        TransactionManager.apply_transaction(tx, self.alice, self.bob)

        # Calculate expected fee and tax
        fee = 200.0 * (self.anchor.spread / 100)
        tax = 200.0 * (self.anchor.tax_rate / 100)
        expected_alice_balance = 1000.0 - 200.0 - fee - tax
        expected_bob_balance = 0.0 + 200.0

        self.assertAlmostEqual(self.alice.balance, expected_alice_balance)
        self.assertAlmostEqual(self.bob.balance, expected_bob_balance)

        # Transaction recorded in both wallets
        self.assertIn(tx, self.alice.transactions)
        self.assertIn(tx, self.bob.transactions)

    def test_invalid_transaction_insufficient_balance(self):
        tx = TransactionManager.create_transaction(
            sender_wallet=self.bob,
            receiver_wallet=self.alice,
            amount=500.0,
            private_key=self.wallet_manager.get_private_key(self.bob.address)
        )
        with self.assertRaises(ValueError):
            TransactionManager.apply_transaction(tx, self.bob, self.alice)

    # ---------------------------
    # Ledger Tests
    # ---------------------------
    def test_ledger_add_transaction(self):
        tx = self.ledger.add_transaction(
            tx_id="tx123",
            sender_address=self.alice.address,
            receiver_address=self.bob.address,
            amount=100.0,
            signature="dummy_signature",
            anchor_id=self.anchor.anchor_id
        )
        self.assertIn("tx123", self.ledger.transactions)
        self.assertIn(tx, self.alice.transactions)
        self.assertIn(tx, self.bob.transactions)

    def test_ledger_integrity(self):
        # Apply multiple transactions
        tx1 = self.ledger.add_transaction(
            tx_id="tx1",
            sender_address=self.alice.address,
            receiver_address=self.bob.address,
            amount=50.0,
            signature="dummy_signature",
            anchor_id=self.anchor.anchor_id
        )
        tx2 = self.ledger.add_transaction(
            tx_id="tx2",
            sender_address=self.alice.address,
            receiver_address=self.bob.address,
            amount=30.0,
            signature="dummy_signature",
            anchor_id=self.anchor.anchor_id
        )
        self.assertTrue(self.ledger.verify_integrity())

    def test_recalculate_balance(self):
        tx = self.ledger.add_transaction(
            tx_id="tx3",
            sender_address=self.alice.address,
            receiver_address=self.bob.address,
            amount=70.0,
            signature="dummy_signature",
            anchor_id=self.anchor.anchor_id
        )
        recalculated = self.ledger.recalculate_wallet_balance(self.alice.address)
        self.assertAlmostEqual(recalculated, self.alice.balance)

    # ---------------------------
    # Anchor Tests
    # ---------------------------
    def test_anchor_fee_calculation(self):
        fee = self.anchor_manager.calculate_fee(self.anchor.anchor_id, 100.0)
        self.assertAlmostEqual(fee, 5.0)

    def test_anchor_tax_calculation(self):
        tax = self.anchor_manager.calculate_tax(self.anchor.anchor_id, 100.0)
        self.assertAlmostEqual(tax, 2.0)


if __name__ == "__main__":
    unittest.main()
