<p align="center">
  <img src="services/web_server/static/og-image.png" alt="Silocat: big files, zero knowledge" width="100%" />
</p>

<p align="center">
  <a href="LICENSE"><img alt="Licence: AGPL-3.0" src="https://img.shields.io/badge/licence-AGPL--3.0-ff4655" /></a>
  <a href="https://silo.cat"><img alt="silo.cat" src="https://img.shields.io/badge/hosted-silo.cat-16161a" /></a>
  <a href="SECURITY.md"><img alt="Security policy" src="https://img.shields.io/badge/security-policy-3ecf8e" /></a>
</p>

Silocat is file sharing and storage with optional end-to-end encryption. Turn on
password protection and files are encrypted in your browser before a single byte
moves, so the server stores ciphertext it cannot open. Drop a file, share a link,
and for encrypted uploads nobody in between can read it. Leave password protection
off (the default) and the file is uploaded unencrypted, which the server can read.

Live at **[silo.cat](https://silo.cat)**. Run it yourself with the compose file
below, or read the code and decide for yourself whether to believe us.

## What it does

- **Optionally encrypted before it leaves.** Turn on password protection and
  each chunk is sealed with XChaCha20-Poly1305, keyed by Argon2id from your
  password on your device. Lose the password and the file is gone. No recovery,
  no backdoor, no exceptions. Leave it off and the upload is unencrypted.
- **No account needed.** Drop up to 20 GB anonymously and share the link. A key
  in your browser lets you manage those uploads later. Anonymous drops expire
  after seven days.
- **Fast.** Files are chunked and transferred directly against object storage,
  and the share link works before the upload finishes.
- **Whole folders.** Drop a directory and the structure survives the trip.
- **Share links you control.** Public, one-time, or off, with optional link
  passwords and expiry.
- **Secure delivery, both directions.** Send files out, or create a request link
  and have anyone send files straight into your account, no sign-up on their end.
  Delivery receipts show you who opened a link, and when.
- **Privacy is free for everyone.** Every privacy feature (encryption, link
  passwords, expiry, basic and one-time sharing) is free on every tier. We never
  paywall security. Paid plans add space and delivery workflow tools
  (request-a-file and delivery receipts), not privacy.

## How the encryption works

| Stage | What happens | Who can read it |
|---|---|---|
| Select | You pick files. Nothing has moved. | Only you |
| Encrypt | With password protection on, libsodium encrypts each chunk with a key Argon2id derives from your password, on your device. With it off, nothing is encrypted. | Only you |
| Upload | An encrypted file travels as ciphertext, an unencrypted one as the plain file. TLS wraps either in transit. | Only you if encrypted, otherwise us too |
| Store | We hold the blobs (ciphertext when encrypted, otherwise the plain file) plus metadata we can read: filenames, folder names, size, timestamps, and a hash of the file's plaintext. | You, plus us: metadata always, contents if unencrypted |
| Share | The link carries no key. For an encrypted file you pass the password separately. An unencrypted file opens for anyone with the link, unless you also set a link password. | Link + password if encrypted, otherwise anyone with the link |
| Download | For an encrypted file, the recipient's browser fetches ciphertext and decrypts locally. An unencrypted file downloads as uploaded. | Whoever has the password if encrypted, otherwise anyone with the link |
| Delete | Blobs are unlinked immediately and scrubbed in the next sweep. | No one |

Zero-knowledge is not zero-metadata. Even for encrypted uploads, we can see the
filename, the folder names, the size, and the timestamps, and the content hash
we store is a hash of the file's plaintext, so we can confirm whether a specific
known file was uploaded. We cannot see the contents of an encrypted file. If your
threat model includes that metadata, Silocat does not solve it.

## Self-hosting

Everything you need is here, including a bundled Postgres and MinIO, so a laptop
or a single VPS is enough.

```bash
git clone https://github.com/clickswave/silocat
cd silocat
cp env.selfhost.example .env          # set the passwords and secrets
docker compose -f orchestration/docker-compose.selfhost.yml --env-file .env up -d
```

The app comes up at `http://localhost:12001`.

Optional integrations (SMTP, Google OAuth, Turnstile, Razorpay billing, GeoIP)
switch on when their variables are filled in and stay off otherwise. See
[`env.selfhost.example`](env.selfhost.example) for the full reference.

A few things worth knowing:

- **Storage** defaults to the bundled MinIO. Point the `CF_R2_*` variables at
  Cloudflare R2, Backblaze B2 or any S3-compatible store for production.
- **GeoLite2** lookups need MaxMind's free database, which their licence does
  not let us redistribute. Download it and set `GEOLITE2_DB_PATH`, or leave it
  blank to disable GeoIP.
- **Retention** is configurable: `WATCHCAT_SHADOW_TTL_DAYS` (anonymous drops,
  default 7), `WATCHCAT_TRASH_TTL_DAYS` (trash, default 30) and
  `WATCHCAT_ORDER_TTL_DAYS` (abandoned checkouts, default 7). If you change
  them, change the copy that promises them.
- **Web deployment**: the hosted silo.cat serves the frontend from Cloudflare
  Pages. The self-host compose builds a standalone Node server with
  `@sveltejs/adapter-node` (see `services/web_server/Dockerfile.selfhost`) and
  runs that, not the dev server. Put it behind a TLS-terminating reverse proxy
  (Caddy, nginx, Traefik) in a real deployment; it listens on `:12001`.

## Architecture

Two services and a scheduler.

**web_server** is the SvelteKit frontend and the only tier that talks to the
API. It holds the infra secret, does the client-side crypto, uploads through
presigned URLs, and serves the public share pages.

**api_switch** is a Rust/Axum backend on `0.0.0.0:31337`. It owns all data and
storage logic and runs its own migrations on startup. Every route requires a
shared secret in a header (`WEB_SERVER_COMMUNICATION_SECRET`), so only our own
backends can reach it. The `/admin` tree sits behind a second, independent
secret and is served on its own hostname; the public zone returns 404 for it.
Both gates fail closed, so an unset secret means reachable by nobody.

**WatchCat** is the same `api_switch` binary run with `WATCHCAT_MODE=1`. It
enforces the retention the UI promises: expiring anonymous drops, emptying trash
after its window, and reclaiming abandoned uploads.

Storage is any S3-compatible object store, addressed as three buckets: `shadow`
for anonymous uploads, `sanctum` for account storage, `dp` for display pictures.
Clients transfer chunks directly against storage. For an encrypted upload that
means ciphertext is all the store ever sees; an unencrypted upload is stored as
the plain file.

## API

Every account gets an API key, visible and rotatable under **Settings → API**.
Send it as `X-Api-Key`.

Encryption happens client-side, so the HTTP API stores whatever bytes it is
sent: ciphertext for an encrypted file, the plain file otherwise. Give the
official client a password and it does the encryption for you:

```bash
npm install @clickswave/silocat-client
```

```js
import { Silocat } from '@clickswave/silocat-client';

const silo = new Silocat({ apiKey: process.env.SILOCAT_API_KEY });

const file = await silo.upload(bytes, {
  name: 'contract.pdf',
  password: 'correct-horse-battery-staple'
});

const { url } = await silo.share(file.id, { type: 'public' });
```

Full reference at [silo.cat/api](https://silo.cat/api), library source in
[`packages/client`](packages/client). The raw endpoints are documented too, but
encrypting through them means implementing Argon2id, chunking and
XChaCha20-Poly1305 exactly as the app does. Get a parameter wrong and the upload
succeeds while the file becomes permanently undecryptable, which is why the
client exists.

## Development

The dev compose expects the monorepo layout used by the hosted deployment
(external `clickswave_network`, shared Postgres). For hacking on Silocat alone,
use the self-host compose above: it is fully self-contained.

```bash
# frontend
cd services/web_server && npm install && npm run dev

# backend
cd services/api_switch && cargo run
```

`api_switch` compiles against a checked-in query cache, so it builds without a
database. If you change SQL, regenerate it with `cargo sqlx prepare` or CI will
fail.

## Security

Found something? **[SECURITY.md](SECURITY.md)** has the reporting address, our
response times, and an explicit scope. Please do not open a public issue for
anything security-relevant.

The short version of what we guarantee: for a file uploaded with password
protection we hold only ciphertext, and we do not hold your decryption passwords
or anything that can recover them. A file uploaded without password protection
is stored unencrypted, and we can read it.

## Licence

[AGPL-3.0](LICENSE). If you run a modified Silocat as a network service, you
have to offer your users the modified source. That is deliberate: the trust
story of zero-knowledge encryption depends on the code staying inspectable,
wherever it runs.

Built by [Clickswave Labs](https://clickswave.org).
