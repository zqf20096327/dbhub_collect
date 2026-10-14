# DANA QRIS Gateway — Starter

Payment gateway DANA dengan QRIS dinamis (MPM), SQLite, dan notifikasi Telegram.

## Setup

```bash
# 1. Install
npm install

# 2. Generate RSA key (PKCS#8) — upload public key ke DANA Merchant Portal
mkdir -p keys
openssl genrsa -out keys/private.pem 2048
openssl rsa -in keys/private.pem -pubout -out keys/public.pem

# 3. Copy env
cp .env.example .env
#    isi DANA_PARTNER_ID, DANA_CLIENT_SECRET dari dashboard.dana.id sandbox
#    isi TELEGRAM_BOT_TOKEN & TELEGRAM_CHAT_ID (opsional, untuk notif)

# 4. Jalankan
npm start
```

## Endpoints

| Method | Path | Fungsi |
|--------|------|--------|
| POST | `/api/payments` | Buat QRIS dinamis — body: `{"amount": 50000, "title": "Produk X"}` |
| GET | `/api/payments/:ref` | Cek status invoice |
| GET | `/api/payments` | List + stats 100 transaksi terakhir |
| POST | `/v1.0/debit/notify` | Webhook DANA Finish Notify (path wajib SNAP) |
| GET | `/health` | Healthcheck |

## Response Create Payment

```json
{
  "partnerReferenceNo": "INV20260913a1b2c3d4e5",
  "amount": "50000.00",
  "qrContent": "0002010102112658...",
  "qrImage": "data:image/png;base64,...",
  "statusUrl": "/api/payments/INV20260913a1b2c3d4e5",
  "expiresIn": 900
}
```

`qrImage` langsung bisa dipakai: `<img src="data:image/png;base64,...">`

## Flow

1. Frontend → `POST /api/payments` → dapat `qrImage` → tampilkan QR
2. User scan pakai DANA/GoPay/OVO/dll (QRIS interoperable)
3. DANA → webhook ke `/v1.0/debit/notify` → status jadi `PAID`
4. Telegram bot kirim notifikasi "✅ Pembayaran Masuk"
5. Frontend polling `GET /api/payments/:ref` (atau upgrade ke WebSocket nanti)

## Struktur

```
src/
├── index.js     — Express server + endpoints + webhook
├── dana.js      — SNAP auth (RSA sign, HMAC, B2B token) + DANA API wrapper
├── db.js        — SQLite (better-sqlite3, WAL mode) + helpers idempotent
└── telegram.js  — Notifikasi Telegram
```

## Keamanan

- `keys/` dan `.env` **jangan** di-commit (tambahkan ke .gitignore)
- Webhook diverifikasi HMAC_SHA512; signature invalid → 401
- `markPaid()` idempotent — webhook dobel tidak dobel-notif
- Semua payload webhook tersimpan di `webhook_events` untuk audit

## TODO sebelum production

- [ ] Daftar merchant resmi: dashboard.dana.id → Gapura Custom Checkout
- [ ] Upload public key → dapat PARTNER_ID, CLIENT_SECRET (sandbox)
- [ ] Selesaikan checklist UAT di Merchant Portal
- [ ] Ganti `DANA_ENV=production` + key production baru
- [ ] Deploy Railway: tambah Volume untuk `./data` (SQLite) dan `./keys`
