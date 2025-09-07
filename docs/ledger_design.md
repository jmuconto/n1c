# N1C Ledger Design

The N1C ledger is a decentralized, transaction-based ledger ensuring secure, tamper-proof balances.

## 1. Ledger Structure
- **Double-entry-like system**:
  - Each transaction affects sender and receiver wallets.
- **Transaction Record**:
  ```python
  Transaction:
      tx_id: str
      sender: str
      receiver: str
      amount: float
      fee: float
      timestamp: datetime
      signature: str
