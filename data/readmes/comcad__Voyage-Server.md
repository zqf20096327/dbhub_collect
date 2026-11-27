<div align="center">

<img src="https://github.com/user-attachments/assets/f3327f7f-5a19-403d-b881-d540287cdf14" width="120" height="120" alt="Voyage Server logo" />

# Voyage Server: Version 83 Game Server

**An open-source version 83 game server that reads the Voyage assets, with an admin page in your browser.**
Java · Part of Voyage, with Voyage-Client and Voyage-Editor

<br />

![Status](https://img.shields.io/badge/status-alpha-yellow?style=for-the-badge)
![License](https://img.shields.io/github/license/comcad/Voyage-Server?style=for-the-badge)

![Java](https://img.shields.io/badge/Java-21-ED8B00?style=flat-square&logo=openjdk&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=flat-square&logo=docker&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.4-4479A1?style=flat-square&logo=mysql&logoColor=white)
[![Based on Cosmic](https://img.shields.io/badge/Based%20on-Cosmic-blue?style=flat-square)](https://github.com/P0nk/Cosmic)
[![Stars](https://img.shields.io/github/stars/comcad/Voyage-Server?style=flat-square&logo=github)](https://github.com/comcad/Voyage-Server/stargazers)
[![Forks](https://img.shields.io/github/forks/comcad/Voyage-Server?style=flat-square&logo=github)](https://github.com/comcad/Voyage-Server/forks)
[![Last commit](https://img.shields.io/github/last-commit/comcad/Voyage-Server?style=flat-square)](https://github.com/comcad/Voyage-Server/commits/main)

</div>
<img width="2864" height="1440" alt="Screenshot of Voyage Server" src="https://github.com/user-attachments/assets/2d72787d-5755-4b06-9a80-4650fbfe319b" />

<br />

**Voyage Server** is an open-source **version 83 game server**: a fork of [Cosmic](https://github.com/P0nk/Cosmic) that reads the game data from the assets folder the [Voyage WZ Extractor](https://github.com/comcad/Voyage-Wz-Extractor) makes, the same folder [Voyage-Client](https://github.com/comcad/Voyage-Client) serves and [Voyage-Editor](https://github.com/comcad/Voyage-Editor) publishes into. It runs with its database in one Docker container and has an admin page of its own.

The repository contains everything needed to deploy it except the game data: the server's source, its scripts and settings, the database setup, and the Docker files. You bring the assets folder, made from your own game files.

> [!WARNING]
> Voyage Server is in **alpha**. Expect rough edges.

## 🧭 The Voyage Projects

Voyage is made up of four projects that work together, all reading one assets folder made from your own game files:

| Project | What it does |
|---|---|
| [Voyage-Client](https://github.com/comcad/Voyage-Client) | The web client: serves the game to browsers and relays them to the game server |
| **Voyage-Server** (this one) | The game server: a fork of [Cosmic](https://github.com/P0nk/Cosmic) that reads the same assets, with an admin page |
| [Voyage-Editor](https://github.com/comcad/Voyage-Editor) | The map, item, NPC, monster and quest editor: publishes what you make into the assets' `customs` folder |
| [Voyage-Wz-Extractor](https://github.com/comcad/Voyage-Wz-Extractor) | Turns your own `.wz` files into the assets folder the other three read |

```
voyage-assets/                 # made by the extractor from your own .wz files
├── Map/ Npc/ String/ ...
└── customs/                   # what Voyage-Editor publishes: files that stand in for the assets' own
Voyage-Client/  Voyage-Server/  Voyage-Editor/    # each pointed at ../voyage-assets
```

## ✨ Features

| | Area | What's included |
|---|---|---|
| 🎮 | **Gameplay** | The full v83 game: every class and its skills, quests and party quests, bosses and expeditions, events, shops and trading, parties, guilds and families, the Cash Shop and more |
| 📦 | **Voyage assets** | Reads each `.img` from its JSON file in the assets folder: no XML `wz` folder to keep beside it |
| 🗂️ | **Customs** | A file in the assets' `customs` folder is read in place of the assets' own, and a new one is read as well, so what you publish with Voyage-Editor reaches the game server too |
| 🛡️ | **Admin page** | How the server is doing, who is playing, a notice to everyone, restart and shut down, the worlds and every setting, and the console, in your browser |
| 👑 | **One admin account** | Made on the first start with the password you choose; the repository ships no accounts and no passwords |
| 🐳 | **One container** | The server and its MySQL database in one Docker container; settings and scripts are mounted, so a change takes a restart, not a rebuild |
| 🌍 | **Worlds & rates** | Worlds, channels, rates and messages, changed from the admin page or `config.yaml` |
| 🔄 | **Close to upstream** | Only what Voyage needs is changed, so updates from upstream can be brought in |

## 🧩 How It Works

```
┌──────────────────┐   WebSocket   ┌──────────────────┐     TCP     ┌──────────────────────────┐
│     Browser      │ ◄───────────► │  Voyage-Client   │ ◄─────────► │ voyage-server container  │
│   (Voyage.js)    │               │   web + relay    │  8484, 75xx │ game server  ·  MySQL    │
└──────────────────┘               └────────▲─────────┘             │ admin page (8585)        │
                                            │ reads                 └────────────▲─────────────┘
                                   ┌────────┴────────────────────────────────────┴─┐
                                   │  voyage-assets/  (extracted WZ: JSON, PNG)    │
                                   │  └── customs/  ◄── Voyage-Editor publishes    │
                                   └───────────────────────────────────────────────┘
```

Players' browsers reach the server through Voyage-Client, which relays them to its login port (8484) and channels. The server reads the game data from the assets folder, with the `customs` folder's files in place of the assets' own, so players and the server see the same game. The database runs beside it in the same container, and the admin page is served by the server itself.

## 📋 Requirements

- A folder of version 83 `*.wz` files (your own), extracted with the [Voyage-Wz-Extractor](https://github.com/comcad/Voyage-Wz-Extractor)
- **Either** Docker (with Compose) **or** Java 21 and MySQL 8
- [Voyage-Client](https://github.com/comcad/Voyage-Client), to play in a browser

## 🚀 Quick Start: Deploy the Server

### 1. Clone the repo

```sh
git clone https://github.com/comcad/Voyage-Server.git
cd Voyage-Server
```

### 2. Extract assets

The WZ extractor lives in its own repo: **[Voyage-Wz-Extractor](https://github.com/comcad/Voyage-Wz-Extractor)** (pure Node, zero dependencies).

> [!NOTE]
> Use your own version 83 `.wz` files.

```sh
cd ..                                # beside Voyage-Server, not inside it
git clone https://github.com/comcad/Voyage-Wz-Extractor
cd Voyage-Wz-Extractor
node wz-extract.mjs <path-to-wz-folder> ../voyage-assets
cd ../Voyage-Server
```

The assets folder is shared: Voyage-Server, Voyage-Client and Voyage-Editor all point at the same one (here `voyage-assets`, beside the repos). If you already run the client, use its assets folder and skip this step.

### 3. Configure

```sh
cp .env.example .env
```

Fill in `.env`: `VOYAGE_ASSETS` (where the assets folder is) and `VOYAGE_ADMIN_PASSWORD` (the password of the admin page and of the in-game admin account; make it long). `.env` is gitignored. Everything else is in `config.yaml` (see [Settings](#%EF%B8%8F-settings)).

### 4. Run it

<details>
<summary><b>🐳 Option A: Docker (recommended)</b></summary>

<br />

Builds the image (compiles the server), then runs the server and its MySQL database in one container.

```sh
docker compose up -d --build
docker compose logs -f
# → "The Voyage server is now online"
```

The first start takes a few minutes: it builds the server, sets up the database (every table and the game's shops, drops and the rest) and makes the admin account. Later starts take seconds.

It listens on 8484 (login) and 7575-7577 (world 1's channels), the admin page on 8585 and the database on 127.0.0.1:3307. The database's files are kept in `database/docker-db-data`. Manage it with `docker compose restart` (after a change to `config.yaml` or `scripts/`), `docker compose up -d --build` (after a change to the Java code) and `docker compose down`.

</details>

<details>
<summary><b>☕ Option B: Java directly</b></summary>

<br />

Make a MySQL 8 database called `voyage` and a user for it, and put them in `config.yaml` (`DB_HOST`, `DB_URL_FORMAT`, `DB_USER`, `DB_PASS`). The server makes its tables on the first start. Set `ASSETS_PATH` in `config.yaml` to the assets folder, and `ADMIN_PORT` and `ADMIN_PASSWORD` for the admin page and the admin account.

```sh
./mvnw package -Dmaven.test.skip     # mvnw.cmd on Windows
./launch.sh                          # launch.bat on Windows
```

</details>

### 5. Play

Point Voyage-Client at this machine: in its `conf/client.conf`, `Relay.Servers = "voyage=<this machine's address>"` (`127.0.0.1` when they run on the same machine), and restart it. The client's machine needs to reach this one's ports 8484 and 7575-7577 (and each further world's channels). Open the client and log in as **`admin`** with the password from `.env`: the server made that account on its first start, with the character **Admin** at GM level 6. Players make their own accounts by logging in with a name that has none (`AUTOMATIC_REGISTER`). 🎮

## ⚙️ Settings

`.env` holds this machine's own settings for Docker; `config.yaml` holds every setting of the server, each with a note beside it. `config.yaml` is mounted into the container: **restart the server after a change** (`docker compose restart`, or Restart on the admin page). The admin page's **Server** tab edits it too.

| Where | Key | Default | Meaning |
|---|---|---|---|
| `.env` | `VOYAGE_ASSETS` | `../voyage-assets` | The assets folder, mounted into the container |
| `.env` | `VOYAGE_ADMIN_PASSWORD` | (none) | The admin page's password, and the admin account's when it is first made; without it the page stays off and no admin account is made |
| `.env` | `VOYAGE_ADMIN_PORT` | `8585` | The admin page's port on this machine |
| `config.yaml` | `ASSETS_PATH` | `"../voyage-assets"` | The assets folder when running without Docker (the `ASSETS_PATH` environment variable wins) |
| `config.yaml` | `ADMIN_PORT`, `ADMIN_PASSWORD` | `0`, `""` | The admin page without Docker (the environment variables of the same names win) |
| `config.yaml` | `WORLDS` | `1` | How many worlds; each world's channels, rates and messages are under `worlds:` |
| `config.yaml` | `DB_URL_FORMAT`, `DB_HOST`, `DB_USER`, `DB_PASS` | `voyage` on `localhost`, `root` | The database (Docker sets `DB_HOST` to the container's own) |
| `config.yaml` | `ENABLE_PIN`, `ENABLE_PIC` | `false` | Whether players set a PIN and a PIC (deleting a character needs a PIC) |
| `config.yaml` | `AUTOMATIC_REGISTER` | `true` | Logging in with a name that has no account makes one |

More worlds need their channels' ports opened: a line for each in `docker-compose.yml` (world 2's channels are 7675-7677, world 3's 7775-7777, and so on).

## 🛡️ Admin Page

Set `VOYAGE_ADMIN_PASSWORD` and open `http://<this machine>:8585`. Without a password it stays off.

| Tab | What it is for |
|---|---|
| **Server** | Online or starting, uptime, who is playing in each world and channel, memory, where the game data comes from; **Restart** and **Shut down**; a notice to everyone in the game; the worlds (channels, rates, messages) and every other setting of `config.yaml`, changed in the file line by line with its comments kept; the console as it is written |
| **Players** | Every character, online or not: its account, level, job, map, world, channel and when it was last online. Search by character or account name, filter by status, world, job, level and GM, and sort by any column. **Kick** and **Ban** for each (a ban lasts so many minutes, hours or days, or for good, and the player is told for how long), **Unban** for a banned account, and **GM level** (0 to 6, at once for a player in the game). **New account** makes an account for testing |

Restart ends the server with exit code 75, and the container (or `launch.sh` / `launch.bat`) starts it again; Shut down ends it. Saving settings keeps a copy of the file as it was (`config.yaml.before-admin`).

> [!CAUTION]
> The sign-in is a password over plain HTTP. Keep the port off the internet (or behind HTTPS), and use a long password.

## 🗂️ Customs

The server reads each `.img` from the assets folder, but reads a file in the `customs` folder (laid out like the assets) in place of the assets' file of the same name, and reads a file that only `customs` has as well. That is where [Voyage-Editor](https://github.com/comcad/Voyage-Editor) publishes. Scripts too: `customs/scripts/<path>` is run in place of the server's own `scripts/<path>`, which is where the editor publishes the dialogue of an NPC made there (`customs/scripts/npc/<number>.js`). Monsters' drops too: `customs/server/mob-drops.json` (written by the editor) gives each monster listed there its drops in place of its drops in the database; one not listed keeps the database's. It is read again when it changes, so `!reloaddrops` takes a change in as well as a restart. The server reads each file the first time it needs it and keeps it, so restart the server after publishing. The assets folder is only ever read.

## 📁 Project Layout

<details>
<summary><b>Click to expand the directory tree</b></summary>

```
Voyage-Server/
├── src/main/java/
│   ├── provider/json/       # reads the assets' JSON (and the customs folder in front of it)
│   ├── net/server/admin/    # the admin page's server, the console it shows, and the admin account
│   └── ...                  # the game server
├── src/main/resources/
│   ├── admin/               # the admin page (HTML, CSS, JavaScript), served from the jar
│   └── db/                  # the database setup (Liquibase) and admin-account.sql
├── scripts/                 # NPC, quest, portal, map, event and item scripts (JavaScript)
├── config.yaml              # every setting of the server
├── .env.example             # this machine's settings for Docker: copy to .env
├── Dockerfile               # builds the server and puts it in MySQL's image
├── docker-compose.yml       # the container: ports, the assets folder, the database's files
├── docker/start.sh          # starts MySQL, then the server (again after a Restart)
├── launch.sh, launch.bat    # start it without Docker
├── database/docker-db-data/ # the database's files: gitignored
├── docs/                    # upstream's README (UPSTREAM-README.md) and notes
├── handbook/                # the handbook: items, mobs, maps and more by id
├── tools/                   # tools for the game data
├── pom.xml, mvnw            # the build (Maven)
└── LICENSE                  # AGPL-3.0
```

</details>

## ❓ FAQ

<details>
<summary><b>What is a server emulator?</b></summary>

<br />

A program that does what the official game servers do (logins, worlds, maps, monsters, items, quests) so that the game client can be played against it. Voyage Server is one for version 83, based on Cosmic and the long line of open-source emulators before it.

</details>

<details>
<summary><b>Does it come with the game files?</b></summary>

<br />

No. You supply your own version 83 `.wz` files and extract them with the [Voyage-Wz-Extractor](https://github.com/comcad/Voyage-Wz-Extractor); the server, the client and the editor all read that folder.

</details>

<details>
<summary><b>How do I log in as the admin?</b></summary>

<br />

Set `VOYAGE_ADMIN_PASSWORD` in `.env` before the first start. The server then makes the account `admin` with that password and the character Admin at GM level 6. If you started it without one, set it and restart: the account is made then. After that it is left alone, so its password is changed in the game or the database, not in `.env`.

</details>

<details>
<summary><b>How do I add worlds or channels?</b></summary>

<br />

On the admin page's **Server** tab (or in `config.yaml`): the number of worlds, and each world's channels. Then open their ports in `docker-compose.yml` and restart.

</details>

<details>
<summary><b>How do I back up the database?</b></summary>

<br />

`docker exec voyage-server mysqldump -uroot voyage > backup.sql`. Its files are also kept in `database/docker-db-data`.

</details>

<details>
<summary><b>Can I bring in updates from upstream?</b></summary>

<br />

Yes. This repository keeps Cosmic's history without its XML game data, so its commits are not the same as upstream's and a plain merge won't line up. Voyage Server changes only what it needs, though, so upstream's changes still apply cleanly: run `git remote add upstream https://github.com/P0nk/Cosmic.git` and `git fetch upstream`, then `git cherry-pick` the commits you want (`git log upstream/master` lists them). What is different is listed under [Credits](#-credits).

</details>

## 💬 Community

Questions, feedback, or want to help test? Come hang out on Discord.

[![Discord](https://img.shields.io/badge/Discord-discord.gg%2FSCVxm6tB4g-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/SCVxm6tB4g)

## 🙏 Credits

- **Cosmic:** [Cosmic](https://github.com/P0nk/Cosmic) by Ponk and its contributors, and the servers it comes from, from OdinMS (2008) to HeavenMS (2019): see [`docs/UPSTREAM-README.md`](docs/UPSTREAM-README.md)
- **What Voyage changed:** the JSON reader and `ASSETS_PATH` (`provider/json`, `DataProviderFactory`), the admin page and the admin account (`net/server/admin`), one container with MySQL, no `wz` folder (in the history either), and no account with a known password in the database setup

## 📄 License

- **License:** [AGPL-3.0](LICENSE), the same license as Cosmic. If you run a changed copy for others to play, offer them its source.


## ⚠️ Disclaimer

### No Game Assets Included
This repository contains **no** copyrighted game assets: no `.wz` files, extracted images, audio, maps or any other game data. It contains only source code.

To use this software, you must supply your own legally obtained copy of the game files. You are solely responsible for making sure you have the legal right to possess and use them. The contributors do not provide, host, link to or distribute these files, and will not help anyone obtain them.

### Intended Use
This software is provided for educational, research and interoperability purposes, and for use with self-hosted servers on a private, non-commercial basis. It is not intended to circumvent any technological protection measure, to replace or compete with any official product or service, or to be used for commercial gain.

The contributors do not sell this software, charge for access or accept payment for in-game items or advantages. Anyone who does so with this software acts on their own account and at their own risk.

### License Scope
The AGPL-3.0 license in this repository applies **only** to its source code. It grants no rights to any third party's trademarks, assets or other intellectual property.

### No Warranty
THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR CONTRIBUTORS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY ARISING FROM THE USE OF THIS SOFTWARE.

### Your Responsibility
You are responsible for complying with all applicable laws, and with any license or terms of service that apply to the game files and servers you use.


<div align="right">

[⬆ Back to top](#voyage-server-version-83-game-server)

</div>
