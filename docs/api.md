# N1C API Reference

The N1C API is built using FastAPI. All endpoints return JSON responses and accept JSON payloads.

## Base URL
http://localhost:8000/api/v1

## Endpoints

### Wallets
- **Create Wallet**
  - `POST /wallets/`
  - Request:
    ```json
    {
      "owner_name": "Alice"
    }
    ```
  - Response:
    ```json
    {
      "address": "n1c1qxyz...",
      "balance": 0.0
    }
    ```

- **Get Wallet**
  - `GET /wallets/{address}`
  - Response:
    ```json
    {
      "address": "n1c1qxyz...",
      "balance": 100.0,
      "transactions": []
    }
    ```

### Transactions
- **Send Transaction**
  - `POST /transactions/`
  - Request:
    ```json
    {
      "sender": "n1c1qxyz...",
      "receiver": "n1c1abcd...",
      "amount": 50.0
    }
    ```
  - Response:
    ```json
    {
      "tx_id": "tx1234",
      "status": "success"
    }
    ```

### Anchors
- **Get Anchor Info**
  - `GET /anchors/{anchor_id}`
  - Response:
    ```json
    {
      "anchor_id": "anchor1",
      "spread": 3.5,
      "tax_rate": 2.0
    }
    ```

### Error Codes
- `400` – Bad Request
- `404` – Not Found
- `500` – Internal Server Error
