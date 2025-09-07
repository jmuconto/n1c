# N1C Architecture

N1C is a decentralized digital currency designed to enable inclusive payments globally. The system consists of three main layers:

## 1. Core Layer (`n1c_core`)
- Contains business logic and models.
- Modules:
  - `models.py` – Wallets, Transactions, Anchors.
  - `ledger_rules.py` – Transaction validation, balance checks, fee calculation.
  - `wallet.py`, `transaction.py`, `anchor.py` – Core operations.

## 2. Network Layer (`n1c_network`)
- Handles peer-to-peer communication between nodes.
- Modules:
  - `node.py` – Node behaviour and lifecycle.
  - `p2p.py` – Peer discovery and messaging.
  - `sync.py` – Ledger synchronization across nodes.
  - `broadcast.py` – Transaction broadcast.

## 3. API Layer (`n1c_api`)
- Provides a FastAPI interface for wallets, transactions, and anchors.
- Modules:
  - `main.py` – FastAPI entry point.
  - `routers/` – Endpoints by domain (wallet, transaction, anchor).
  - `schemas/` – Pydantic models for request/response validation.
  - `services/` – API-specific services calling core logic.

## 4. Additional Components
- `scripts/` – Utilities for deployment, key generation, ledger initialization.
- `tests/` – Unit and integration tests.
- `docker/` – Docker and docker-compose configurations for running nodes.

## Data Flow
1. User submits transaction via FastAPI endpoint.
2. Service layer validates transaction using `ledger_rules.py`.
3. Transaction is applied to the ledger and wallet balances.
4. Transaction is broadcast to peer nodes for synchronization.
5. Anchors apply fees/spreads as configured.
