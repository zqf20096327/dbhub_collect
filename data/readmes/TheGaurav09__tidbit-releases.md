# TidBit — The Antidote to Brainrot 📚✨

[![GitHub Release](https://img.shields.io/github/v/release/TheGaurav09/tidbit-releases?color=2457D6&label=Latest%20Release)](https://github.com/TheGaurav09/tidbit-releases/releases/latest)
[![Live Showcase Site](https://img.shields.io/badge/Live%20Showcase-GitHub%20Pages-00C853)](https://thegaurav09.github.io/tidbit-releases/)
[![Android Version](https://img.shields.io/badge/Android-8.0%2B%20%28API%2026%2B%29-blue)](https://github.com/TheGaurav09/tidbit-releases)
[![License](https://img.shields.io/badge/License-Proprietary-neutral)](LICENSE)

> **TidBit** is a distraction-free educational micro-learning Android application engineered to replace dopamine-heavy algorithmic feeds with vetted 60-second micro-lessons, Bud AI active recall checks, and a serene digital library.

🌐 **Official Live Showcase & Download Site**: [https://thegaurav09.github.io/tidbit-releases/](https://thegaurav09.github.io/tidbit-releases/)

---

## ⚡ Direct APK Download

Download the verified production release directly:

| File | Architecture | Size | Direct Link |
| :--- | :--- | :--- | :--- |
| **`tidbit-app-release.apk`** | ARM64-v8a, armeabi-v7a, x86_64 | ~10 MB | [⬇️ Download Latest APK](https://github.com/TheGaurav09/tidbit-releases/releases/latest/download/tidbit-app-release.apk) |
| **`sha256sum.txt`** | Cryptographic Checksum | < 1 KB | [🛡️ Download Checksum](https://github.com/TheGaurav09/tidbit-releases/releases/latest/download/sha256sum.txt) |

### 🛡️ Verify Cryptographic Integrity

To verify the authenticity of your downloaded APK against tampering:

**Windows (PowerShell):**
```powershell
Get-FileHash -Algorithm SHA256 tidbit-app-release.apk
```
*Expected SHA-256 for v2.0.9:* `326ae1c226a03914e254e10347b5afd2e8fb0adc415dcf30ac284283b7309531`

**Linux / macOS:**
```bash
sha256sum -c sha256sum.txt
```

---

## 🌟 Key Application Pillars

1. **60-Second Educational Shorts**: Vetted vertical micro-lessons across Science, Philosophy, Coding, Literature, and History. Zero commercial advertising, zero behavioral data profiling.
2. **Bud AI Intelligent Tutor**: Real-time context-aware active recall quizzes, instant explanatory feedback, and 3D flip flashcards based on the exact lesson transcript.
3. **BookNest E-Reader & Audiobooks**: Classical literature, custom font rendering, and neural text-to-speech audiobooks with 100% offline local caching.
4. **Cognitive Games Hub**: Vocabulary Spelling Bee, Word Match, Speed Math, and Code Breaker logic drills.
5. **Local-First Privacy Architecture**: Study notes, reading sessions, and preferences reside encrypted directly on your device.

---

## 🛠️ Showcase Landing Page (Source Code)

This repository also hosts the source code for the official TidBit showcase website, deployed automatically to **GitHub Pages**.

### Tech Stack
- **Framework**: React 19 + TypeScript
- **Bundler & Tooling**: Vite 6
- **Styling**: Tailwind CSS v4 + Motion
- **Design System**: "Quiet Liquid Glass" — high-legibility typography, frosted glass tokens, and responsive mobile mockups.

### Local Development
```bash
# 1. Install dependencies
npm install

# 2. Start local hot-reload dev server
npm run dev

# 3. Production build (generates /dist and /dist/404.html)
npm run build
```

### Automated GitHub Pages Deployment
Every push to the `main` branch automatically triggers the `.github/workflows/deploy.yml` workflow, building the production bundle and publishing directly to GitHub Pages.

---

## 🔒 Security & Privacy Charter

- **Zero Trackers**: No third-party ad networks or surveillance SDKs.
- **Hardware-Backed Encryption**: High-security keystore credential handling.
- **Open Integrity**: Every release binary is cryptographically signed and checksummed in public releases.

© 2026 Tidbit · Built with Focus
