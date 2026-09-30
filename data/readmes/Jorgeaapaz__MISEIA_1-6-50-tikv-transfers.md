# TiKV Transfers

A **Rust + Next.js + Flutter payment system** backed by **TiKV** (distributed key-value store) that implements TANGLE-inspired transaction chaining with JSON-RPC 2.0 over an Ethereum-compatible cryptographic stack (secp256k1 + keccak256).

---

## Features Implemented

### 1. Rust JSON-RPC 2.0 API Server
Core payment engine built with Axum. Handles all account and transaction logic with ECDSA signature verification before any state mutation. TiKV operations use optimistic transactions to prevent race conditions on balance updates.

- `payment_getAccount` — fetch account state (address, balance, nonce)
- `payment_transfer` — submit a signed transfer; validates signature, nonce chain, and balance
- `payment_getTransaction` — retrieve a transaction by hash
- `payment_getTransactionHistory` — paginated history per address
- `payment_listAccounts` — enumerate all seeded accounts

### 2. TANGLE-Inspired Nonce Chaining
Each transaction's `nonce` equals the `hash` of the sender's previous confirmed transaction (`"0x0"` for the first). This forms a per-account directed chain enforcing strict ordering without a global sequence number.

### 3. BIP-39 / BIP-44 Seed & Genesis Data
A `seed` binary derives 10 Ethereum-style accounts from the standard test mnemonic (`test test test … junk`, path `m/44'/60'/0'/0/i`), funds each with 10,000 units, then generates ~100 cryptographically signed and nonce-chained transfers, writing all state directly to TiKV.

### 4. Express Communication Server
WebSocket + REST relay between the Next.js web app and the Flutter mobile app for out-of-band transaction approval. Tracks pending approvals in-memory with UUID identifiers.

### 5. Next.js Web Application
Full-stack UI for browsing accounts/balances, initiating transfers, and viewing transaction details. Signs transactions client-side using the sender's private key via `secp256k1` + `keccak256` before submitting to the Rust API.

### 6. Flutter Mobile Approval App
Receives `approval:request` events over WebSocket from the Express server, presents the transaction details to the user, and emits `approval:response` back. Acts as a hardware-wallet-style second factor.

---

## Project Structure

```
tikv-transfers/
├── api/                          # Rust JSON-RPC 2.0 API server
│   ├── src/
│   │   ├── main.rs               # Axum HTTP server entry point
│   │   ├── lib.rs                # Library root
│   │   ├── rpc.rs                # JSON-RPC method dispatcher
│   │   ├── models.rs             # Transaction, Account, Signature structs
│   │   ├── db.rs                 # TiKV client layer (accounts + transactions)
│   │   ├── crypto.rs             # secp256k1, keccak256, address derivation, signing
│   │   └── bin/seed.rs           # BIP-39 genesis seeder
│   └── Cargo.toml
├── comms-server/                 # Express relay server (Node.js + TypeScript)
│   └── src/index.ts              # REST + WebSocket approval relay
├── web/                          # Next.js 14 web application
│   ├── app/
│   │   ├── page.tsx              # Account list + balances
│   │   ├── transfer/page.tsx     # Transfer form with mobile approval flow
│   │   ├── tx/[hash]/page.tsx    # Transaction detail page
│   │   └── account/[address]/page.tsx  # Account history
│   └── lib/
│       ├── rpc-client.ts         # Typed JSON-RPC 2.0 fetch wrapper
│       └── crypto-client.ts      # Client-side signing (secp256k1 + keccak256)
├── mobile/                       # Flutter mobile approval app
│   └── lib/
│       ├── main.dart             # App entry + routing
│       ├── screens/home_screen.dart      # Pending approvals list
│       ├── screens/approval_screen.dart  # Tx details + Approve/Reject
│       ├── services/comms_service.dart   # WebSocket client to Express server
│       └── models/approval_request.dart  # ApprovalRequest model
├── docker-compose.yml            # TiKV v7.5 + PD node topology
└── CLAUDE.md                     # Project architecture reference
```

---

## Design Patterns / Architecture

### Layered Architecture (Rust API)
```
HTTP (Axum)  →  RPC dispatcher (rpc.rs)  →  DB layer (db.rs)  →  TiKV
                       ↕
               Crypto layer (crypto.rs)
```
Each layer has a single responsibility: the RPC layer parses and routes, the DB layer handles all TiKV I/O, and the crypto layer is purely functional (no I/O).

### Event-Driven Approval Flow (Express + WebSocket)
The Express server acts as a message broker: it stores pending approvals keyed by UUID, pushes events to Flutter over WebSocket, and fans out results back to the waiting web client — all without the web app and mobile app ever connecting directly.

### Account Model (Ethereum-Compatible)
Uses balance-based accounting (not UTXO). Each `Account` struct tracks `balance: u128` and `nonce: String` (the hash of the last confirmed tx). TiKV keys follow a prefix namespace:

| TiKV Key Pattern | Value |
|---|---|
| `account:{address}` | JSON `Account` |
| `tx:{tx_hash}` | JSON `Transaction` |
| `tx_index:{address}:{timestamp_ms}:{tx_hash}` | `tx_hash` |

---

## How It Works

A transfer begins in the Next.js UI, which sends an approval request to the Express relay server. The Express server pushes a WebSocket event to the Flutter app, the user approves on mobile, and the web app receives confirmation. The web app then signs the transaction client-side (`keccak256` hash → `secp256k1` ECDSA) and submits it via `payment_transfer` to the Rust API, which verifies the signature, checks the nonce chain, updates balances under an optimistic TiKV transaction, and returns the transaction hash.

```rust
// Rust: verify signature before any state write
let msg = build_tx_hash(&from, &to, value, &nonce, timestamp);
crypto::verify_signature(&msg, &params.signature, &from)?;

// Optimistic TiKV transaction for atomic balance update
let mut txn = client.begin_optimistic().await?;
let sender_key = format!("account:{from}");
let mut sender: Account = txn.get(sender_key.clone()).await?.into();
sender.balance -= value;
sender.nonce = tx_hash.clone();
txn.put(sender_key, serde_json::to_vec(&sender)?).await?;
txn.commit().await?;
```

---

## Getting Started

### Prerequisites

- [Rust](https://rustup.rs/) 1.75+
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (for TiKV)
- [Node.js](https://nodejs.org/) 20+
- [Flutter](https://flutter.dev/docs/get-started/install) 3.x (optional, for mobile)

### Clone

```bash
git clone https://github.com/Jorgeaapaz/MISEIA_1-6-50-tikv-transfers.git
cd MISEIA_1-6-50-tikv-transfers
```

### 1 — Start TiKV

```bash
docker-compose up -d
# Wait ~15 s for PD health check to pass
```

### 2 — Seed Genesis Data

```bash
cd api
TIKV_PD_ADDR=127.0.0.1:2379 cargo run --bin seed
```

### 3 — Start Rust API

```bash
cd api
TIKV_PD_ADDR=127.0.0.1:2379 RPC_LISTEN_ADDR=0.0.0.0:8545 cargo run --bin server
```

### 4 — Start Express Comms Server

```bash
cd comms-server
npm install
PORT=3001 RUST_API_URL=http://localhost:8545 npm run dev
```

### 5 — Start Next.js Web App

```bash
cd web
npm install
# .env.local already contains default values
npm run dev
# Open http://localhost:3000
```

### 6 — Run Flutter App (optional)

```bash
cd mobile
flutter pub get
flutter run
```

---

## Example Output

### Seed run

```
[INFO] Derived 10 accounts from BIP-39 mnemonic
[INFO] Funded account 0x1234...abcd with 10000 units
...
[INFO] Generated and stored 100 signed transactions
[INFO] Seeding complete
```

### Transfer request (JSON-RPC)

```json
POST http://localhost:8545
{
  "jsonrpc": "2.0", "id": 1, "method": "payment_transfer",
  "params": {
    "from": "0xf39fd6e51aad88f6f4ce6ab8827279cfffb92266",
    "to":   "0x70997970c51812dc3a010c7d01b50e0d17dc79c8",
    "value": 250,
    "nonce": "0x0",
    "signature": { "v": 27, "r": "0xabc...", "s": "0xdef..." }
  }
}

// Success
{ "jsonrpc": "2.0", "id": 1, "result": { "tx_hash": "0x9f3a..." } }
```

### Error cases

```json
// Insufficient balance
{ "jsonrpc": "2.0", "id": 1, "error": { "code": -32000, "message": "Insufficient balance" } }

// Wrong nonce
{ "jsonrpc": "2.0", "id": 1, "error": { "code": -32001, "message": "Invalid nonce" } }

// Bad signature
{ "jsonrpc": "2.0", "id": 1, "error": { "code": -32002, "message": "Invalid signature" } }
```

---

## Development Ports

| Service | Port |
|---|---|
| Rust API | 8545 |
| Express Comms | 3001 |
| Next.js Web | 3000 |
| TiKV PD | 2379 |
| TiKV Store | 20160 |

---

## Updates — 2026-06-10

- Added session chapter to `RETROSPECTIVA-2026-05-04.md`: full explanation of the five components (TiKV, Rust API, Express comms, Next.js, Flutter), their connection diagram (Mermaid), and the complete transfer flow walkthrough.
