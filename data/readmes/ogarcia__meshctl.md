<div align="center">

<img src="assets/icons/app.svg" alt="meshctl" width="128" height="128">

# meshctl

**A lean control panel for your [Meshtastic](https://meshtastic.org/) and [MeshCore](https://meshcore.co.uk/) radios**

*Chat on them, see the mesh around them on a map, follow every packet they hear, and set them up.*

[![CI](https://img.shields.io/github/actions/workflow/status/ogarcia/meshctl/ci.yml?branch=master&style=for-the-badge&label=CI&logo=githubactions&logoColor=white)](https://github.com/ogarcia/meshctl/actions/workflows/ci.yml)
[![Latest release](https://img.shields.io/github/v/release/ogarcia/meshctl?include_prereleases&style=for-the-badge&label=version&color=9a5b00)](https://github.com/ogarcia/meshctl/releases/latest)
[![License: GPL v3](https://img.shields.io/badge/license-GPL--3.0-9a5b00?style=for-the-badge)](LICENSE)
<br>
[![Rust](https://img.shields.io/badge/Rust-one%20binary-e66100?style=for-the-badge&logo=rust&logoColor=white)](#installing)
[![Meshtastic · MeshCore](https://img.shields.io/badge/Meshtastic%20%C2%B7%20MeshCore-67ea94?style=for-the-badge)](#goals)
[![Desktop app](https://img.shields.io/badge/desktop-Windows%20%C2%B7%20Flatpak-4a5568?style=for-the-badge)](#installing)
[![Container image](https://img.shields.io/badge/container-ghcr.io-2496ed?style=for-the-badge&logo=docker&logoColor=white)](https://github.com/ogarcia/meshctl/pkgs/container/meshctl)

[Website](https://meshctl.ogarcia.me/) · [Installing](#installing) · [Running](#running) · [Access](#access) · [Changelog](CHANGELOG.md)

<img src="https://meshctl.ogarcia.me/shots/en-map.webp" alt="meshctl's map: the mesh around A Coruña, its nodes coloured by how many hops away they are, beside the radio's pages and channels" width="860">

</div>

---

A lean control panel for your mesh radios: control them, see the mesh around
them, chat, and trace routes. That is the whole list.

meshctl stays connected to your radios around the clock, keeps what they hear
in SQLite, and serves a web interface and an API from a single binary. One
radio or a dozen, Meshtastic and MeshCore, all from the same panel; on a
server, in a container, as a desktop app, or as an app on your phone.

> [!WARNING]
> **meshctl is young.** Until 1.0, a release may change the interface, the
> API and the database: each one tries to carry your database forward, but
> nothing is promised yet. Between releases, `master` changes, and breaks,
> from one commit to the next. Try it, and tell what you find; do not rely on
> it for anything that matters.

## Goals

- **Your radios:** as many as you have, added and changed from the panel.
- **Each node:** its identity, role, channels and LoRa settings.
- **The mesh:** every node heard, when, how well and how far, on a list and a
  map.
- **Chat:** channels and direct messages, with history kept while you were away.
- **Traceroutes:** on demand, with their history.
- **Automatic replies:** if someone writes this, answer with that, where you
  say, from the daemon: a ping with the hops it took and its signal, say.
- **Notifications:** of the messages heard where you say, a channel's maybe
  only when it mentions you; in the browser, and from the apps with their
  window closed.
- **One binary**, small enough for a Raspberry Pi or a router, with the web
  interface built in; and a desktop app, for Windows and Linux, and an Android
  app, with the same inside.
- **An API** that every client uses, the web interface included, documented at
  `/api/docs`.

## Non-goals

Written down so that they stay that way. A feature request for any of these is
a reason to point at another tool, not to grow this one.

- Bots, automations or scheduled messages.
- MQTT, Matrix or any other bridge. See
  [loratrix](https://github.com/ogarcia/loratrix) for that.
- Telemetry dashboards, charts or statistics beyond what a node says about
  itself.
- Network-wide monitoring and analysis. See
  [Meshview](https://github.com/meshview/meshview) for that.
- Users, roles and permissions. See [Access](#access).
- Sharing one radio between several clients. Put
  [tasticsplitter](https://github.com/ogarcia/tasticsplitter) in front of it,
  and point meshctl at it as if it were the radio.

Meshtastic comes first. MeshCore radios connect, and show their nodes and
chats, but they can do less than Meshtastic ones for now.

## Installing

Each [release](https://github.com/ogarcia/meshctl/releases) brings:

- **The daemon**, `meshctld`, for Linux (x86_64 and aarch64, static, any
  distribution) and macOS (Apple silicon and Intel), with the interface
  inside: unpack it and run it.
- **The desktop app** for Windows, portable: unzip the folder somewhere you
  can write to and run `meshctl.exe`. What it keeps goes beside it.
- **The desktop app** for Linux, as a Flatpak:
  `flatpak install --user meshctl-*-linux-x86_64.flatpak`.
- **The Android app**, an APK: `android-arm64` for nearly every phone,
  `android-arm` for older 32-bit ones.
- **A container image**, below.

The desktop app runs the daemon within itself, on this machine alone, and
shows the panel in its own window. Closing it keeps it listening to your
radios, and notifying you, unless you say otherwise in its settings: in the
tray on Windows, as a background app on Linux. `meshcore://` links open in
it, to add the node or channel they hold.

The Android app does the same on the phone: radios over the network, by USB
(with a cable or an OTG adapter) and by Bluetooth, picked from those plugged
in or heard nearby. It keeps listening with the app closed if you say so in
its settings, with a notification that tells it is. `meshcore://` links, and
links shared to it from the Meshtastic or MeshCore apps, open in it. Android
asks, the first time, to let the browser or the files app install it.

To have it kept up to date, [Obtainium](https://github.com/ImranR98/Obtainium)
follows the releases. From the phone, add it set up already, for [nearly
every phone][obtainium-arm64] or for [an older 32-bit one][obtainium-arm]; or
by hand: add `https://github.com/ogarcia/meshctl` as an app and, as each
release brings both APKs, set its *Filter APKs by regular expression* to
`android-arm64\.apk$` (`android-arm\.apk$` on a 32-bit phone). It tells when
a new one is out, and installs it over the one you have.

[obtainium-arm64]: https://apps.obtainium.imranr.dev/redirect?r=obtainium://app/%7B%22id%22%3A%22me.ogarcia.meshctl%22%2C%22url%22%3A%22https%3A%2F%2Fgithub.com%2Fogarcia%2Fmeshctl%22%2C%22author%22%3A%22ogarcia%22%2C%22name%22%3A%22meshctl%22%2C%22additionalSettings%22%3A%22%7B%5C%22apkFilterRegEx%5C%22%3A%5C%22android-arm64%5C%5C%5C%5C.apk%24%5C%22%7D%22%7D
[obtainium-arm]: https://apps.obtainium.imranr.dev/redirect?r=obtainium://app/%7B%22id%22%3A%22me.ogarcia.meshctl%22%2C%22url%22%3A%22https%3A%2F%2Fgithub.com%2Fogarcia%2Fmeshctl%22%2C%22author%22%3A%22ogarcia%22%2C%22name%22%3A%22meshctl%22%2C%22additionalSettings%22%3A%22%7B%5C%22apkFilterRegEx%5C%22%3A%5C%22android-arm%5C%5C%5C%5C.apk%24%5C%22%7D%22%7D

## Running

```sh
meshctld
```

That is all it needs: open http://127.0.0.1:7434. It keeps its database in
`./data` (`--data` or `MESHCTL_DATA` to put it elsewhere) and, the first time,
the panel asks for a radio.

Trying it on your own machine, leave `MESHCTL_TOKEN` unset: without it, only
this machine reaches meshctl, and nothing asks for a token. Set one when it
listens beyond this machine (see [Access](#access)); then the panel asks for
it, once, in each browser.

A radio's address is one of:

```text
192.168.1.10              on the network, port 4403 (5000 for MeshCore)
radio.lan:4404            on the network, another port
/dev/ttyACM0              plugged in, at 115200
/dev/ttyUSB0@921600       plugged in, at another speed
```

A radio serves one client at a time. If something else (the phone app, say)
also needs it, put [tasticsplitter](https://github.com/ogarcia/tasticsplitter)
in front and give meshctl its address instead.

### In a container

Each release, and every push to master, builds an image, for amd64 and arm64:
`latest` is the last release (`0.4.0`, `0.4` name them too), `master` the
last commit. To try it on your own machine:

```sh
podman run -d --name meshctl -p 127.0.0.1:7434:7434 \
    -v meshctl:/var/lib/meshctl \
    ghcr.io/ogarcia/meshctl:latest
```

In the container, meshctl listens on every interface, port 7434, and keeps its
database in `/var/lib/meshctl`, the volume above. Its clock is in UTC, which
is the time automatic replies tell: give it yours with `-e TZ=Europe/Madrid`,
say. The port above is published
on this machine alone, so no token is needed. To reach it from elsewhere,
publish it as `-p 7434:7434` and set a token (`-e MESHCTL_TOKEN=a-long-secret`)
or put a proxy in front (see [Access](#access)).

A radio on USB is a device passed in, which the container's user must be
allowed to open. With rootless podman, keep your own groups:

```sh
podman run … --device /dev/ttyACM0 --group-add keep-groups …
```

With docker, add the group that owns the device:

```sh
docker run … --device /dev/ttyACM0 --group-add "$(stat -c %g /dev/ttyACM0)" …
```

`master` follows master, and the warning above with it: a newer image may not
open the database an older one made. If it does not start after an update,
remove the volume and add your radios again.

### As an app from a phone's browser

Where meshctl runs elsewhere, on a server or a Raspberry Pi, the panel installs
as an app on any phone, from the browser's menu, with its own icon and window;
on Android, links shared to it (from the Meshtastic or MeshCore apps, say) open
it to add what they hold. Browsers allow that, and the camera that reads QR
codes, over HTTPS or on this very machine: put meshctl behind a proxy with
HTTPS to have them from elsewhere.

## Access

meshctl listens on `127.0.0.1:7434` by default, so only the machine it runs on
can reach it. To reach it from elsewhere, set `MESHCTL_LISTEN` (for example
`0.0.0.0:7434`) and protect it in one of two ways:

- **A reverse proxy with its own authentication** in front (nginx or Caddy with
  basic auth, Authelia, Authentik…). Use HTTPS if it is reachable from outside
  your network.
- **An access token**: set `MESHCTL_TOKEN`, and clients send it in the
  `X-Meshctl-Token` header. It does not use `Authorization`, so it can be
  combined with a proxy's basic auth.

Both together work too: the proxy asks who is there and puts the token on
every request it passes on, so its users never see meshctl ask for it, while
whoever reaches meshctl's own port past the proxy still needs it. The event
stream takes the token from the header of the request that opens it, as the
API does from each of its requests. With nginx:

```nginx
location / {
    # Whatever authentication the proxy asks for: basic, OIDC…
    auth_basic "meshctl";
    auth_basic_user_file /etc/nginx/meshctl.htpasswd;

    proxy_pass http://127.0.0.1:7434;
    proxy_set_header X-Meshctl-Token "a-long-secret";

    # The event stream is a WebSocket.
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 1h;
}
```

meshctl warns at startup when it listens beyond this machine without a token.

## Building

```sh
# The interface first, so that the daemon embeds it.
(cd web && trunk build --release)
cargo build --release
```

The daemon is `target/release/meshctld`. Built without the interface, it still
serves the API and tells you at `/` what is missing.

The web interface needs [trunk](https://trunkrs.dev) and the
`wasm32-unknown-unknown` target (`rustup target add wasm32-unknown-unknown`).

The desktop app is `cargo build --release -p meshctl-desktop`, after the
interface; on Linux it needs WebKitGTK's development files (`webkit2gtk-4.1`).
`desktop/flatpak/build.sh` builds it for the Flatpak, and says how to pack
it.

The Android app needs the Android SDK and NDK, Java 17 or later and the Tauri
CLI (`cargo install tauri-cli`); after the interface:

```sh
cd desktop
ANDROID_HOME=~/Android/Sdk NDK_HOME=~/Android/Sdk/ndk/<version> \
  cargo tauri android build --apk --split-per-abi --target aarch64
```

Signed with your key if `desktop/gen/android/keystore.properties` says where
it is (`storeFile`, `keyAlias` and `password`), unsigned if not.

## Development

```sh
git config core.hooksPath .githooks   # format and clippy before each commit
cargo run                              # the daemon, on 127.0.0.1:7434,
                                       # without a token
(cd web && trunk serve)                # the interface on 127.0.0.1:7435,
                                       # rebuilt on change, API proxied
cargo run -p meshctl-core --example probe -- <host> [port] [seconds]
                                       # what a radio says, line by line;
                                       # read only, never transmits
```

| Crate     | What it is                                                     |
| --------- | -------------------------------------------------------------- |
| `proto`   | Meshtastic protobufs (vendored) and the stream framing         |
| `core`    | The link to a radio over TCP or serial, and the domain model   |
| `api`     | The types the daemon and its clients share; compiles to WASM   |
| `server`  | The daemon, `meshctld`: a library and its binary               |
| `web`     | The Leptos interface (client-side rendered), with translations |
| `desktop` | The desktop app, with Tauri: the daemon in a window of its own |

Translations are in `web/locales/`, one JSON file per language, English being
the reference. Using a key English does not declare is a compile error; one
another language lacks is a build warning, and shows in English meanwhile.
