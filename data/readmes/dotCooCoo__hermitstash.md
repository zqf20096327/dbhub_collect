<p align="center"><img src="https://raw.githubusercontent.com/dotCooCoo/hermitstash/main/public/img/logos/purple.svg" width="120" alt="HermitStash"></p>
<h1 align="center">HermitStash</h1>
<p align="center"><strong>Stash it quietly. Share it instantly.</strong><br>Post-quantum encrypted, self-hosted file upload server.</p>
<p align="center"><a href="https://github.com/dotCooCoo/hermitstash-sync">HermitStash Sync</a> — companion desktop sync client</p>

<p align="center">
  <a href="https://apps.umbrel.com/app/hermitstash">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://apps.umbrel.com/badge-light.svg">
      <img src="https://apps.umbrel.com/badge-dark.svg" alt="Get it on the Umbrel App Store" height="46">
    </picture>
  </a>
</p>

<p align="center">
  <a href="https://blamejs.com">
    <img src="https://raw.githubusercontent.com/blamejs/blamejs/main/assets/BlameJS_Logo.png" width="96" alt="blamejs">
  </a>
</p>
<p align="center">
  Built on <a href="https://blamejs.com"><strong>blamejs</strong></a> — the vendored Node framework that owns its stack.<br>
  Crypto envelopes, session storage, mTLS CA management, vault sealing, body parsers, rate limiting, and the WebSocket layer all come from <a href="https://github.com/blamejs/blamejs">blamejs</a>; HermitStash composes them into a product.
</p>

---

> **A note before you dive in.**
>
> HermitStash is my first public repo. It started as a weekend project to solve my own problem — sharing files with clients without trusting third-party cloud storage — and grew from there. I use it daily and it works for me, but I'm sharing it publicly knowing that "works for me" and "is fit for your use case" are different things.
>
> A few things I want to be honest about:
>
> - **I'm not a cryptographer.** I've used well-reviewed primitives and tried to assemble them carefully, but I haven't had this audited, and there are almost certainly things I don't know that I don't know. I've written [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md) as a detailed design document specifically so that review is *possible* — it describes every protocol, lists known limitations honestly, and includes specific questions for cryptographers. If that's you: thank you, and please open an issue.
> - **This is a personal project.** I maintain it solo, in my spare time, and I can't promise fast response times or backwards compatibility.
> - **I'm not currently accepting code contributions** (more on that below), but bug reports, security findings, and feedback are genuinely welcome — they're how I learn.
>
> If HermitStash is useful to you, that's wonderful. If you're considering it for anything where the consequences of a security flaw matter, please weigh that against the fact that no professional has reviewed this code.
>
> — .CooCoo ([@dotCooCoo](https://github.com/dotCooCoo))

> **Status:** Personal project · Not audited · API may change · Use at your own risk

---

## Quick Start

```bash
git clone https://github.com/dotCooCoo/hermitstash.git
cd hermitstash
node server.js
```

No config files. No build step. No `npm install` — all dependencies are vendored in the repo with zero npm runtime packages. First run generates the vault keypair and creates default accounts. Configure everything from the admin panel.

**Default admin:** `admin@hermitstash.com` with a **randomly-generated password printed to stdout** on first boot. The same password is also written to `data/initial-admin-password.txt` (mode 0600) so it survives container restart. Read it from your `docker logs` or the file, log in, and complete the setup wizard — the wizard walks you through changing the admin email and password, setting your site name, configuring the passkey relying party (rpOrigin/rpId), and generating a session secret. The plaintext password file is deleted automatically when setup completes.

## Why HermitStash?

- **Post-quantum encryption** — your files are protected against both today's computers

[...截断...]

 and tomorrow's quantum computers
- **Zero plaintext** — every database field, every file, every audit log entry is encrypted or hashed before touching disk
- **Self-hosted** — your server, your keys, your data. No third-party cloud
- **Zero dependencies at runtime** — `node server.js` is the entire setup. All crypto libraries are vendored and committed
- **One-command deploy** — Docker or bare metal, no build step, no config files needed

## Built on blamejs

[<img align="right" src="https://raw.githubusercontent.com/blamejs/blamejs/main/assets/BlameJS_Logo.png" width="120" alt="blamejs">](https://blamejs.com)

HermitStash is composed on top of [**blamejs**](https://blamejs.com) — a Node framework that vendors its standard library instead of pulling it from npm at runtime, with security defaults wired in from line zero. Every primitive HermitStash uses for crypto, transport, storage, and identity flows through the framework:

- `b.crypto` — envelope versioning, ML-KEM-1024 + P-384 hybrid encrypt/decrypt, XChaCha20-Poly1305 packed format, SHA3-512, namespaced hashes
- `b.vault` + `b.vaultWrap` + `b.cryptoField` — vault key load/seal/unseal, passphrase-wrapped at-rest sealing, sealed-column registry for the data layer
- `b.session` — sessions with PQC sealed cookies, /24 IPv4 + /64 IPv6 fingerprint binding, tmpfs-backed `localDbThin` storage, sid-rotation on login
- `b.mtlsCa` + `b.mtlsEngine` — mTLS CA generation, client cert issuance, sealed-PEM at-rest, generation tracking
- `b.middleware.{apiEncrypt, rateLimit, bodyParser, cors, csrfProtect, securityHeaders, botGuard}` — the request pipeline
- `b.parsers.{json, multipart}` — RFC 7578 / RFC 8187 / POISONED_KEYS / HPE_* hardened body parsing
- `b.objectStore` — SigV4 S3-compatible backend (AWS, DigitalOcean Spaces, MinIO, Backblaze)
- `b.scheduler`, `b.backup`, `b.router`, `b.websocket`, `b.auth.password` (Argon2id), `b.auth.totp` (SHA-512), `b.safeUrl`, `b.sanitize`, `b.atomicFile`, `b.requestHelpers`, `b.constants`

The framework's source tree lives at [`lib/vendor/blamejs/`](lib/vendor/blamejs/), and [`lib/vendor/MANIFEST.json`](lib/vendor/MANIFEST.json) records the pinned release. [`scripts/vendor-update.sh blamejs [version]`](scripts/vendor-update.sh) refreshes it from the npm registry as `@blamejs/core`, and stops before unpacking when the tarball does not match the registry's published sha512 integrity value. HermitStash has no npm runtime packages: `package.json` has no `dependencies` block.

## Crypto Suite

For the detailed design — protocols, security goals, non-goals, adversary model, key hierarchy, known limitations, and open questions for reviewers — see [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md). The table below is a summary.

All cryptographic operations use NIST-standardized post-quantum algorithms:

| Layer | Algorithm | Standard | Purpose |
|-------|-----------|----------|---------|
| **KEM** | ML-KEM-1024 + P-384 ECDH hybrid | FIPS 203 + NIST P-384 | Key encapsulation (PQC + classical) |
| **Symmetric** | XChaCha20-Poly1305 | RFC 8439 extended | Data encryption (192-bit nonce, constant-time) |
| **KDF** | SHAKE256 | FIPS 202 (XOF) | Key derivation from KEM shared secrets |
| **Hash** | SHA3-512 | FIPS 202 | Integrity, email/IP hashing, checksums |
| **Webhook MAC** | HMAC-SHA256 (Standard Webhooks) | RFC 2104 | Webhook delivery signatures |
| **Password** | Argon2id | RFC 9106 | Memory-hard password hashing |
| **Signatures** | SLH-DSA-SHAKE-256f (default) / ML-DSA-87 (legacy) | FIPS 205 / 204 | Digital signatures. New keys default to SLH-DSA-SHAKE-256f; existing ML-DSA-87 keys continue to verify (algorithm auto-detected from key PEM) |
| **mTLS certificates** | ML-DSA-87 (sync CA) / ECDSA-P384-SHA384 (browser CA) | FIPS 204 / NIST P-384 | Sync/machine client certs are signed by a post-quantum CA; browser-import certs are signed by a separate classical CA that browsers and OS keystores can actually verify and import |
| **Random** | SHA3-512(entropy) |