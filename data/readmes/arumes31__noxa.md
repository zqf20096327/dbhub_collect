<div align="center">

<img src="client/frontend/public/branding/logo.png" alt="noXa logo" width="160" height="160" />

# noXa

**Self-hosted voice, video, screen sharing, and chat**

*Go server, Windows desktop client, installable mobile/web PWA, and PostgreSQL persistence.*

[![CI](https://github.com/arumes31/noxa/actions/workflows/ci.yml/badge.svg)](https://github.com/arumes31/noxa/actions/workflows/ci.yml)
[![golangci-lint](https://github.com/arumes31/noxa/actions/workflows/golangci-lint.yml/badge.svg)](https://github.com/arumes31/noxa/actions/workflows/golangci-lint.yml)
[![Security Analysis](https://github.com/arumes31/noxa/actions/workflows/security.yml/badge.svg)](https://github.com/arumes31/noxa/actions/workflows/security.yml)
[![Go Version](https://img.shields.io/github/go-mod/go-version/arumes31/noxa)](https://go.dev/)
[![Container Image](https://img.shields.io/badge/container-ghcr.io-blue?logo=docker)](https://github.com/arumes31/noxa/pkgs/container/noxa)
[![License](https://img.shields.io/github/license/arumes31/noxa)](LICENSE)

[Public test server](#public-test-server) • [Mobile / PWA](#mobile) • [Architecture](#architecture) • [Features](#features) • [Quick Start](#quick-start) • [Server Setup](#new-server-setup) • [Permissions](#permissions) • [ServerQuery API](#serverquery) • [Configuration](#configuration) • [Development](#development-and-checks) • [Operations](#operations)

---

<img width="1280" height="800" alt="Current noXa desktop client in OLED Midnight with fictional demo conversations" src="website/public/assets/screenshots/app-chat.png" />

*Actual client UI with fictional demo data; [capture details](website/README.md#product-screenshot-provenance).*


</div>

## 🌟 Overview

**noXa** combines voice channels, camera and screen sharing, direct and group
conversations, and channel forums in a desktop client and an installable web app. Its Go server uses a
framed control protocol, a **Pion WebRTC SFU**, PostgreSQL for persistent state,
and optional Redis pub/sub. Named roles control access and moderation.

The published desktop binary targets **Windows x64**. The Wails source also has
Linux/macOS platform code; CI exercises Windows and Linux, but does not publish
Linux/macOS desktop releases. The Vite frontend uses the native Go bridge: it is
not a standalone browser client. [`website/`](website/README.md) is a separate
static product/download website hosted at [noxa.wowcraft.pw](https://noxa.wowcraft.pw/).

<a id="public-test-server"></a>

### Try the public test server

| Open | Address |
| :--- | :--- |
| Website and downloads | [noxa.wowcraft.pw](https://noxa.wowcraft.pw/) |
| Mobile / browser client | [Launch the PWA](https://noxa.wowcraft.pw/app/) |
| Desktop server address (Server IP / hostname) | `wowcraft.pw` (default control port `12333`) |
| Windows x64 client | [Download for Windows](https://github.com/arumes31/noxa/releases/latest/download/noxa-client-windows-amd64.exe) |

This is a public **test server** for trying noXa. The Windows download redirects
to the current GitHub Release. GitHub Pages is no longer used.

Link your account through **Connections → PWA / Mobile login** in the desktop
client, or continue as a guest when the server permits it. The dialog includes a
QR code, a PWA link, and installation guidance. On Android, install from Chrome;
on iPhone/iPad, open in Safari and add to the Home Screen; on macOS, use Safari's
Add to Dock where available or Chrome's install option. Browser features and
system permissions determine the available voice, camera and notification tools.

<details>
<summary>More current interface screenshots</summary>

![Role management with fictional demo roles](website/public/assets/screenshots/app-roles.png)

<img src="website/public/assets/screenshots/pwa-chat.png" width="390" alt="Mobile PWA chat with fictional demo messages" />

</details>

> [!NOTE]
> **Encryption boundaries** (details in [Encryption](#encryption)): direct
> messages and private groups 

[...截断...]

are end-to-end encrypted with Olm (vodozemac),
> and channel voice, video and screen sharing are end-to-end encrypted with a
> key shared by the channel's members. Channel/global chat, forum bodies and
> private calls are **not** end-to-end encrypted yet. Upgrading? Deploy the
> server before or together with the clients: see
> [Upgrading to end-to-end encryption](#e2ee-upgrade).

<a id="encryption"></a>

### Encryption

**What is end-to-end encrypted.** Direct messages and private-group messages,
with their attachments, edits and deletes, between desktops and the mobile web
app:

- **Protocol.** Olm, the double ratchet as implemented by
  [vodozemac](https://github.com/matrix-org/vodozemac), compiled to
  WebAssembly and used by both clients (`noxa-olm-v1`). There is one Olm
  session per pair of devices; every device of the sender and of the
  recipients receives its own copy, and the conversation, sender, recipient
  device and message ID are authenticated inside every message. Keys ratchet
  forward with every message, so a session key stolen later cannot open
  earlier messages (copied history is the exception, see "New devices").
- **Primitives.** X25519 for the Olm handshake, AES-256-CBC with
  HMAC-SHA-256 for messages. The Olm MAC is **truncated to 64 bits**, as the
  Olm specification defines. Olm accounts are published as bundles signed by
  each device's Ed25519 noXa key; contacts verify devices against the
  identity they pinned (the account's first desktop and the devices it
  approved). Changed identities need explicit confirmation; account resets
  are accepted only through a signed reset chain.
- **Not claimed.** This is not the Signal protocol and is not wire-compatible
  with Signal or Matrix; it is not post-quantum.
- **Server role.** The server relays and stores ciphertext and enforces
  admission (complete device fanout, limits, membership) without being able
  to read messages. It still sees metadata: who talks to whom, when, message
  sizes and device lists.
- **Older history and older apps.** Direct messages from before this protocol
  used static X25519 + XSalsa20-Poly1305 (NaCl box) keys without forward
  secrecy. Updated apps never send that way. Older apps still can, and
  updated apps still show such messages, labelled as legacy encryption
  (readable, not editable). An updated app never falls back to the weaker
  encryption: if a contact has no end-to-end key yet, it does not send and
  says that the contact needs to update.
- **New devices.** Copying history to a newly linked device transfers
  readable records only (signed per transfer by the source device, never keys
  or sessions); copied records are marked as verified on the other device,
  not on the new one. The copy is sealed with the two devices' long-term
  X25519 keys (NaCl box) and kept by the server for up to 24 hours, so it has
  no forward secrecy: someone who stores it and later obtains one of those
  long-term keys can read the copied history.
- **Private-call signalling** still uses the static device keys (private-call
  media is not end-to-end encrypted, see below).
- **Guests.** A guest that signs in with an identity key (desktop password-less
  logins, browser guests) uses the same protocol for direct messages: its key
  is its own account root and registers its device itself. A browser guest has
  no desktop to vouch for the server, so it pins the server's certificate on
  first use; if the certificate changes, secure messaging pauses until the
  guest explicitly reviews and accepts the new fingerprint. Sessions without an
  identity key cannot send direct or group messages.

**Channel voice, video and screen sharing (`noxa-media-e2ee-v1`).** On a
server that advertises this capability, every channel microphone, camera,
screen and screen-audio frame is encrypted on the sending device before it
reaches the server's media relay (SFU), and decrypted only on the receiving
device. The frame cipher is the maintained LiveKit FrameC