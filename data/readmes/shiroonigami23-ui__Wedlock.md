<div align="center">

<img src="assets/landing.png" alt="Wedlock Matrimony" width="100%">

# 💍 Wedlock Matrimony

### PHP-first matrimonial platform with K-means smart matching, moderation and membership plans

![PHP](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white) ![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white) ![Electron](https://img.shields.io/badge/Electron-47848F?style=for-the-badge&logo=electron&logoColor=white) ![Android](https://img.shields.io/badge/Android-3DDC84?style=for-the-badge&logo=android&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE) ![Last commit](https://img.shields.io/github/last-commit/shiroonigami23-ui/Wedlock?style=flat-square) ![Repo size](https://img.shields.io/github/repo-size/shiroonigami23-ui/Wedlock?style=flat-square) ![Top language](https://img.shields.io/github/languages/top/shiroonigami23-ui/Wedlock?style=flat-square) ![Status](https://img.shields.io/badge/status-live-blueviolet?style=flat-square)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/shiroonigami23-ui/Wedlock?quickstart=1) [![Download ZIP](https://img.shields.io/badge/Download-ZIP-2ea44f?style=flat-square&logo=github)](https://github.com/shiroonigami23-ui/Wedlock/archive/refs/heads/main.zip)

[**🚀 Live Demo**](https://sobran.lovestoblog.com) · [**Overview**](#-overview) · [**Features**](#-features) · [**Architecture**](#-architecture) · [**Getting Started**](#-getting-started) · [**Roadmap**](#-roadmap)

</div>

---

## 📖 Overview

**Wedlock** is a matrimonial platform built to run on free shared hosting such as **InfinityFree**. Members register,
build an editable profile and bio, and receive **smart match suggestions** computed with **unsupervised K-means clustering**
over profile vectors. Admins moderate every profile before it goes live, manage membership packages and site imagery,
and members exchange **connection requests**. Heavy match queries are accelerated with a file cache, and a GitHub Actions
workflow packages **APK and EXE** wrappers.

### ✨ Highlights

- **K-means matching** — profiles vectorised and clustered (`run_kmeans`) to suggest compatible members
- **Admin moderation** — approve / reject profiles before they're visible
- **Membership packages** with payment-confirmation flow
- **Fast on free hosting** — file-cache acceleration + skeleton loaders

## 🧩 Features

| Feature | What it does |
|---|---|
| **Accounts** | Register, login, logout |
| **Profile** | Editable profile, about and bio (`profile.php`) |
| **Smart matching** | K-means style clustering of profile vectors stored in `profile_vectors` |
| **Connections** | Send / accept / decline requests (`connections.php`) |
| **Packages** | Plans and subscription activation (`packages.php`) |
| **Admin panel** | Moderation, plans and site settings incl. template images (`admin.php`) |
| **Support** | Direct owner contact via WhatsApp (`contact.php`) |
| **Performance** | File cache in `storage/cache`, skeleton/loading animations |
| **Apps** | Desktop (Electron) wrapper + release workflow for APK/EXE |

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend | PHP 8+ (`includes/core.php`, `bootstrap.php`) |
| Database | MySQL / MariaDB |
| Front-end | Vanilla JS + CSS |
| Packaging | Electron desktop wrapper, GitHub Actions release |
| Hosting | InfinityFree |

## 🏗 Architecture

Page scripts share a bootstrap/core layer; matching runs as a clustering job over profile vectors.

```mermaid
flowchart LR
  U[Member] --> P[index · register · login · dashboard · profile · connections · packages]
  A[Admin] --> AD[admin.php]
  P & AD --> B[includes/bootstrap.php + core.php]
  B --> DB[(MySQL<br/>users · profiles · requests · packages · profile_vectors)]
  B --> KM[run_kmeans<br/>profile vectors → clusters]
  KM --> DB
  B --> C[(storage/cache)]
  P --> API[api.php]
```

➡️ Full design notes, data flow and design decisions: **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)**

## 📁 Project Structure

```text
Wedlock/
├── index.php · register.php · login.php · logout.php
├── dashboard.php · profile.php · connections.php · packages.php · contact.php
├── admin.php · api.php
├── includes/       # bootstrap.php, core.php, layout.php, config.local.sample.php
├── assets/         # app.js, style.css
├── database/schema.sql
├── storage/cache/
└── desktop/        # Electron wrapper
```

## 🚀 Getting Started

### Prerequisites

- PHP 8+ and MySQL/MariaDB

### 1. Get the code

Pick whichever method suits you:

| Method | Command |
|---|---|
| **HTTPS** | `git clone https://github.com/shiroonigami23-ui/Wedlock.git` |
| **SSH** | `git clone git@github.com:shiroonigami23-ui/Wedlock.git` |
| **GitHub CLI** | `gh repo clone shiroonigami23-ui/Wedlock` |
| **ZIP** | [Download](https://github.com/shiroonigami23-ui/Wedlock/archive/refs/heads/main.zip) and extract |
| **Codespaces** | [Open in browser](https://codespaces.new/shiroonigami23-ui/Wedlock?quickstart=1) — zero local setup, dev container preconfigured |

> 🔑 **Using SSH for the first time?** Generate a key with `ssh-keygen -t ed25519 -C "you@example.com"`, add the `.pub` contents at **GitHub → Settings → SSH and GPG keys**, then test with `ssh -T git@github.com`.

### 2. Install & set up

```bash
cd Wedlock
cp includes/config.local.sample.php includes/config.local.php   # DB credentials
# import database/schema.sql
```

### 3. Run

```bash
php -S localhost:8000      # open http://localhost:8000
```

## 🎮 Usage

1. Register and complete your profile and bio.
2. Wait for admin approval — then your profile becomes discoverable.
3. Open the dashboard to see suggested matches from your cluster.
4. Send connection requests; accept or decline incoming ones.
5. Upgrade via **Packages** for premium features.

## 🗺 Roadmap

**v1 — Platform (done)**

- [x] Accounts, profiles, moderation
- [x] K-means matching and connection requests
- [x] Packages, admin settings, caching
- [x] Live deployment + APK/EXE packaging

**v1.1 — Trust & safety**

- [ ] Photo verification and ID-check workflow
- [ ] Report / block users and rate-limit messages
- [ ] CSRF tokens and audit log on admin actions

**v1.2 — Better matching**

- [ ] Preference weights (location, community, education, lifestyle)
- [ ] Explainable match score ("why we matched you")
- [ ] In-app chat after mutual acceptance

**v2.0 — Growth**

- [ ] Online payments, multilingual UI (Hindi/English), notification emails

➡️ Detailed plan, milestones and long-term vision: **[docs/ROADMAP.md](docs/ROADMAP.md)**

## 🤝 Contributing

Contributions, issues and feature requests are welcome!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m "feat: add amazing feature"`
4. Push the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request against `main`

Check the [issues page](https://github.com/shiroonigami23-ui/Wedlock/issues) and the [roadmap](docs/ROADMAP.md) for ideas on where to help.

## 📜 Changelog

See [CHANGELOG.md](CHANGELOG.md) for the release history.

## 📄 License

Distributed under the **MIT** license. See [LICENSE](LICENSE) for details.

## 👤 Author

**Aryan Singh Chandel** (Shiro)

[![GitHub](https://img.shields.io/badge/GitHub-shiroonigami23--ui-181717?style=flat-square&logo=github)](https://github.com/shiroonigami23-ui)

<div align="center">

⭐ **If you find this project useful, consider giving it a star!** ⭐

</div>
