<div align="center">

<img src="https://img.icons8.com/fluency/96/note.png" width="72" alt="Driftnote logo" />

# ⚡ Driftnote

### Notes that never lose your work — online or offline.

Local-first note-taking for React Native, built so **offline reliability is a first-class feature**, not an afterthought.

[![Expo SDK](https://img.shields.io/badge/Expo-SDK%2054-000020?style=for-the-badge&logo=expo&logoColor=white)](https://expo.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-Strict-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![React Native](https://img.shields.io/badge/React_Native-Expo_Router_v6-61DAFB?style=for-the-badge&logo=react&logoColor=white)](https://reactnative.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

<br/>

`🔧 Install` · `▶️ Run` · `📱 Features` · `🗂️ Structure` · `🔐 Security`

</div>

---

## 📖 Overview

Driftnote writes every keystroke straight to a **local SQLite database**, so the app never blocks on a network connection. When connectivity returns, a background sync queue pushes your changes automatically — with conflict resolution built in for when the same note changes in two places at once.

> 💡 **In short:** you can write, edit, and organize notes with zero internet — and trust that everything reconciles cleanly the moment you're back online.

---

## ✨ Features

<table>
<tr>
<td width="60" align="center">📱</td>
<td><strong>Local-First SQLite</strong><br/>Notes are written directly to on-device SQLite (<code>expo-sqlite</code>) — no loading screens, no internet dependency.</td>
</tr>
<tr>
<td align="center">⚡</td>
<td><strong>Smart Sync Queue</strong><br/>Offline edits are queued with a pending status and pushed automatically once the connection is restored.</td>
</tr>
<tr>
<td align="center">⏱️</td>
<td><strong>Debounced Autosave</strong><br/>Edits save automatically 750ms after you stop typing — no save button, just a subtle <code>StatusPill</code> (<em>Saving…</em> → <em>Saved locally</em> → <em>Synced</em>).</td>
</tr>
<tr>
<td align="center">📜</td>
<td><strong>Version History</strong><br/>Every meaningful edit creates an immutable snapshot. Browse past versions and restore any of them in one tap.</td>
</tr>
<tr>
<td align="center">⚔️</td>
<td><strong>3-Way Conflict Resolution</strong><br/>An interactive modal lets you <strong>Keep Mine</strong>, <strong>Keep Synced Version</strong>, or <strong>Merge Both</strong> when a sync conflict occurs.</td>
</tr>
<tr>
<td align="center">🎨</td>
<td><strong>Figma-Inspired Auth Flow</strong><br/>Login, Create Account, Forgot Password, and Set New Password screens, plus a 1-tap demo mode for fast evaluation.</td>
</tr>
<tr>
<td align="center">🌗</td>
<td><strong>Light & Dark Themes</strong><br/>A custom design-token system (<code>#090D16</code> dark / <code>#F8FAFC</code> light) with the brand accent tied to the <em>Synced</em> status color.</td>
</tr>
<tr>
<td align="center">📳</td>
<td><strong>Haptic Feedback</strong><br/>Tactile feedback via <code>expo-haptics</code> on save, delete, and sync events.</td>
</tr>
</table>

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| 🖼️ **Framework** | React Native (Expo SDK 54) |
| 🧭 **Routing** | Expo Router v6, file-based, 4-tab bottom navigation |
| 🔷 **Language** | TypeScript (strict mode) |
| 🗄️ **Database** | `expo-sqlite` (v16 async API) |
| 🧠 **State** | Zustand (notes, sync queue, auth, and settings stores) |
| 💾 **Persistence** | `@react-native-async-storage/async-storage` |
| 🌐 **Network** | `expo-network` |
| 📳 **Haptics** | `expo-haptics` |

---

## 🗂️ Project Structure

```
driftnote/
├── app/                      # Expo Router file-based pages
│   ├── (tabs)/                 # Notes · Search · Sync · Settings
│   ├── _layout.tsx             # Root stack layout & DB init
│   ├── auth.tsx                # Authentication entry route
│   ├── editor.tsx              # Note editor (?id=...)
│   ├── history.tsx             # Version history (?id=...)
│   ├── onboarding.tsx          # Onboarding slides
│   └── splash.tsx              # Animated splash screen
│
└── src/
    ├── constants/
    │   └── theme.ts             # Design tokens (theme, typography)
    ├── components/
    │   ├── ConflictResolutionModal.tsx
    │   ├── NoteCard.tsx
    │   ├── StatusPill.tsx
    │   └── SyncDot.tsx
    ├── screens/
    │   ├── AuthScreen.tsx
    │   ├── NoteEditorScreen.tsx
    │   ├── NotesListScreen.tsx
    │   ├── OnboardingScreen.tsx
    │   ├── SearchScreen.tsx
    │   ├── SettingsScreen.tsx
    │   ├── SplashScreen.tsx
    │   ├── SyncStatusScreen.tsx
    │   └── VersionHistoryScreen.tsx
    ├── services/
    │   ├── db.ts                # SQLite schema & CRUD
    │   ├── network.ts           # Network checks & sync queue
    │   └── storage.ts           # AsyncStorage helper
    ├── store/
    │   ├── useAuthStore.ts
    │   ├── useNoteStore.ts
    │   ├── useSettingsStore.ts
    │   └── useSyncStore.ts
    └── types/
        └── note.ts               # Shared TypeScript interfaces
```

---

## 🚀 Getting Started

### ✅ Prerequisites

- Node.js v18+
- npm

### 📦 Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/driftnote.git
cd driftnote

# 2. Install dependencies
npm install

# 3. Start the Expo development server
npx expo start --clear
```

### 📲 Run on a Device

| Key | Target |
|:---:|---|
| `a` | 🤖 Android emulator / device |
| `i` | 🍎 iOS simulator |
| — | 📷 Scan the QR code with **Expo Go** on a physical device |

---

## 🔄 How Sync Works

```
✍️ Edit note  →  💾 Save to local SQLite  →  🟡 Queue as "pending"
                                                     │
                                     🌐 connection restored
                                                     ▼
                                        🔁 Background sync push
                                                     │
                              ┌──────────────────────┴──────────────────────┐
                              ▼                                             ▼
                    ✅ No conflict → Synced                  ⚔️ Conflict → Resolution modal
                                                          (Keep Mine · Keep Synced · Merge Both)
```

---

## 🔐 Security & Privacy

Notes live exclusively in your device's encrypted sandbox via SQLite. **Nothing leaves your phone** unless you configure a remote sync backend.

---

## 📄 License

Released under the [MIT License](LICENSE).

<div align="center">

Made with ⚡ for reliable, offline-first note-taking.

</div>
