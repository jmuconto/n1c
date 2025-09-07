# N1C Ledger Design

The N1C ledger is the backbone of the decentralized currency system. It ensures secure, tamper-resistant, and verifiable transactions between wallets while supporting anchors and fees.

---

## 1. Ledger Overview

- **Decentralized**: Each node maintains its own copy of the ledger.
- **Transaction-Based**: Ledger consists of a sequential list of transactions.
- **Double-Entry-Like**: Each transaction affects both sender and receiver wallets.

**Ledger Responsibilities:**

1. Maintain wallet balances.
2. Validate transactions according to rules.
3. Apply fees and anchor spreads.
4. Synchronize with other nodes in the network.

---

## 2. Ledger Structure

### 2.1 Transaction Model

Each transaction contains:

```python
Transaction:
    tx_id: str        # Unique identifier
    sender: str       # Sender wallet address
    receiver: str     # Receiver wallet address
    amount: float     # Amount to transfer
    fee: float        # Transaction fee
    timestamp: datetime
    signature: str    # Cryptographic signature of sender

Wallet:
    address: str
    balance: float
    transactions: List[Transaction]

Anchor:
    anchor_id: str
    spread: float     # Percentage (e.g., 2% - 7%)
    tax_rate: float   # Tax applied to transactions
