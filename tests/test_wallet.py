# n1c_core/tests/test_wallet.py

import unittest
from n1c_core.wallet import WalletManager
from n1c_core.transaction import TransactionManager
from n1c_core.anchor import AnchorManager


class TestWallet(unittest.TestCase):

    def setUp(self):
        # Initialize Wallet and Anchor managers
        self.wallet_manager = WalletManager()
        self.anchor_manager = AnchorManager()

        # Create wallets
        self.alice = self.wallet_manager.create_wallet("Alice")
        self.bob = self.wallet_manager.create_wallet("Bob")

        # Fund Alice wallet
        self.alice.balance = 500.0

        # Register an anchor
        self.anchor = self.anchor_manager.register_anchor("anchor1", spread=3.0, tax_rate=1.0)

    # ---------------------------
    # Wallet Creation Tests
    # ---------------------------
    def test_create_wallet(self):
        self.assertTrue(self.wallet_manager.wallet_exists(self.alice.address))
        self.assertTrue(self.wallet_manager.wallet_exists(self.bob.address))
        self.assertIsNotNone(self.wallet_manager.get_private_key(self.alice.address))
        self.assertIsNotNone(self.wallet_manager.get_public_key(self.bob.address))

    # ---------------------------
    # Balance Tests
    # ---------------------------
    def test_get_balance(self):
        balance = self.wallet_manager.get_balance(self.alice.address)
        self.assertEqual(balance, 500.0)

    def test_recalculate_balance(self):
        # Create a transaction
        tx = TransactionManager.create_transaction(
            sender_wallet=self.alice,
            receiver_wallet=self.bob,
            amount=100.0,
            private_key=self.wallet_manager.get_private_key(self.alice.address),
            anchor=self.anchor
        )
        TransactionManager.apply_transaction(tx, self.alice, self.bob)

        # Recalculate balance
        recalculated = self.wallet_manager.recalculate_balance(self.alice.address)
        expected_fee = 100.0 * (self.anchor.spread / 100)
        expected_tax = 100.0 * (self.anchor.tax_rate / 100)
        expected_balance = 500.0 - 100.0 - expected_fee - expected_tax
        self.assertAlmostEqual(recalculated, expected_balance)

    # ---------------------------
    # Transaction History Tests
    # ---------------------------
    def test_transaction_history(self):
        tx = TransactionManager.create_transaction(
            sender_wallet=self.alice,
            receiver_wallet=self.bob,
            amount=50.0,
            private_key=self.wallet_manager.get_private_key(self.alice.address),
            anchor=self.anchor
        )
        TransactionManager.apply_transaction(tx, self.alice, self.bob)

        alice_history = self.wallet_manager.get_transactions(self.alice.address)
        bob_history = self.wallet_manager.get_transactions(self.bob.address)

        self.assertIn(tx, alice_history)
        self.assertIn(tx, bob_history)
        self.assertEqual(len(alice_history), 1)
        self.assertEqual(len(bob_history), 1)

    # ---------------------------
    # Key Management Tests
    # ---------------------------
    def test_keypair_exists(self):
        private_key = self.wallet_manager.get_private_key(self.alice.address)
        public_key = self.wallet_manager.get_public_key(self.alice.address)
        self.assertIsNotNone(private_key)
        self.assertIsNotNone(public_key)

    def test_wallet_existence_check(self):
        self.assertTrue(self.wallet_manager.wallet_exists(self.alice.address))
        self.assertFalse(self.wallet_manager.wallet_exists("nonexistent_wallet"))

if __name__ == "__main__":
    unittest.main()
