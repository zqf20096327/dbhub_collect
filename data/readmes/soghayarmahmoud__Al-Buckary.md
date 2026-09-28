<div align="center">

# 📖 Al-Buckary — صحيح البخاري

**The most comprehensive open-source Sahih Al-Bukhari mobile application**

[![Flutter](https://img.shields.io/badge/Flutter-3.8.1-02569B?logo=flutter&logoColor=white)](https://flutter.dev)
[![Dart](https://img.shields.io/badge/Dart-3.8-0175C2?logo=dart&logoColor=white)](https://dart.dev)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Android%20%7C%20iOS%20%7C%20Windows-blue)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg)](CONTRIBUTING.md)
[![GitHub Issues](https://img.shields.io/github/issues/soghayarmahmoud/Al-Buckary)](https://github.com/soghayarmahmoud/Al-Buckary/issues)
[![GitHub Stars](https://img.shields.io/github/stars/soghayarmahmoud/Al-Buckary)](https://github.com/soghayarmahmoud/Al-Buckary/stargazers)

*Read, search, bookmark, and learn from the complete Sahih Al-Bukhari collection — beautifully crafted with Flutter.*

</div>

---

## 🌟 Overview

**Al-Buckary** is a feature-rich mobile application that brings the complete **Sahih Al-Bukhari** hadith collection to your fingertips. Built with Flutter for cross-platform support, it provides a clean, modern reading experience with powerful features designed to help users study, memorize, and engage with the hadiths.

Whether you're a student of knowledge, a researcher, or someone looking to incorporate hadith reading into your daily routine — Al-Buckary is built for you.

---

## ✨ Features

### 📚 Complete Hadith Collection
All hadiths from **Sahih Al-Bukhari** organized across **97 chapters** (أبواب), searchable and accessible offline.

### 🔍 Advanced Search with FTS5
Lightning-fast full-text search powered by **SQLite FTS5** with Arabic diacritics normalization for accurate results.

### ⭐ Favorites & Collections
- **Favorites**: Mark hadiths you love for quick access
- **Custom Collections**: Organize hadiths into themed groups with color-coded labels

### 📝 Personal Notes
Attach personal notes to any hadith with color-coded categories — your private study companion.

### 🔖 Smart Bookmarks
Bookmark your reading position in each chapter and pick up exactly where you left off.

### 🖼️ Smart Share
Share hadiths as beautifully formatted images or plain text — perfect for social media and messaging apps.

### 📊 Reading Statistics
Track your reading journey with a calendar heatmap, streak tracking, session time, and weekly activity charts.

### 🔔 Daily Hadith Notifications
Receive a random hadith notification daily to keep you connected with the Sunnah.

### 🎨 Theme Customization
- **Dark & Light modes** with customizable primary color
- **Multiple Arabic fonts**: Cairo, Tajawal, Changa, Playpen Sans Arabic, Aref Ruqaa
- **Adjustable font size** for comfortable reading

### 📱 Cross-Platform
Built with Flutter — runs natively on **Android**, **iOS**, **Windows**, **macOS**, and **Linux**.

---

## 📸 Screenshots

<div align="center">
  <img src="1.jpg" width="180" alt="Home Screen" />
  <img src="2.jpg" width="180" alt="Hadiths List" />
  <img src="3.jpg" width="180" alt="Search" />
  <img src="4.jpg" width="180" alt="Favorites" />
</div>

<div align="center">
  <img src="5.jpg" width="180" alt="Collections" />
  <img src="6.jpg" width="180" alt="Notes" />
  <img src="7.jpg" width="180" alt="Statistics" />
  <img src="8.jpg" width="180" alt="Settings" />
</div>

<div align="center">
  <img src="9.jpg" width="180" alt="Smart Share" />
  <img src="10.jpg" width="180" alt="Dark Mode" />
  <img src="11.jpg" width="180" alt="Theme" />
  <img src="12.jpg" width="180" alt="About" />
</div>

---

## 🏗️ Architecture

```
lib/
├── main.dart                 # App entry point & providers setup
├── splash.dart               # Animated splash screen
├── database_helper.dart      # SQLite database with FTS5, migrations, self-healing
├── hadith_data.dart          # Pre-loaded hadith data (97 chapters)
│
├── models/                   # Data models
│   ├── hadith.dart           # Hadith model (id, text, chapterId, isFavorite)
│   ├── chaper.dart           # Chapter model (id, title, hadithCount)
│   ├── collection.dart       # Collection model
│   └── note.dart             # Note model
│
├── pages/                    # App screens
│   ├── home_page.dart        # Chapters list with search
│   ├── hadith_list_page.dart # Hadiths in a chapter with search & filtering
│   ├── hadith_page.dart      # Individual hadith view with actions
│   ├── favorite.dart         # Favorites page
│   ├── collections_page.dart # Custom collections management
│   ├── notes_page.dart       # All notes view
│   ├── statistics_page.dart  # Reading stats & calendar
│   ├── settings.dart         # App settings & customization
│   └── about_page.dart       # About the app
│
├── components/               # Reusable UI components
│   ├── hadith_card.dart      # Hadith display card with actions
│   ├── custom_appbar.dart    # Custom app bar with search
│   ├── bottom_navigation_bar.dart
│   ├── smart_share_dialog.dart
│   ├── notes_sheet.dart
│   └── ...
│
├── providers/                # State management (Provider)
│   ├── favorit_provider.dart # Favorites state
│   ├── bookmarks_provider.dart # Bookmark state
│   ├── statistics_provider.dart # Reading statistics
│   └── usage_tracker.dart    # Session time tracking
│
├── services/                 # Background services
│   ├── notification_service.dart # Daily hadith notifications
│   └── ad_service.dart       # Google Mobile Ads
│
└── themes/                   # Theming
    ├── theme_provider.dart   # Dynamic theme management
    ├── light_mode.dart
    └── dark_mode.dart
```

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| **Framework** | Flutter 3.8.1 |
| **Language** | Dart 3.8 |
| **State Management** | Provider |
| **Database** | SQLite (sqflite) with FTS5 full-text search |
| **Local Storage** | SharedPreferences |
| **Notifications** | flutter_local_notifications + WorkManager |
| **Ads** | Google Mobile Ads |
| **Sharing** | share_plus + screenshot |
| **Fonts** | Cairo, Tajawal, Changa, Playpen Sans Arabic, Aref Ruqaa |

---

## 🚀 Getting Started

### Prerequisites

- [Flutter SDK](https://docs.flutter.dev/get-started/install) (3.8.1 or later)
- [Android Studio](https://developer.android.com/studio) or [VS Code](https://code.visualstudio.com/)
- An Android/iOS emulator or physical device

### Installation

```bash
# Clone the repository
git clone https://github.com/soghayarmahmoud/Al-Buckary.git

# Navigate to the project directory
cd Al-Buckary

# Install dependencies
flutter pub get

# Run the app
flutter run
```

### Building for Production

```bash
# Android APK
flutter build apk --release

# Android App Bundle (for Play Store)
flutter build appbundle --release

# iOS (requires macOS)
flutter build ios --release
```

---

## 🗺️ Roadmap

We have an exciting roadmap planned across 4 milestones. Check out our [GitHub Issues](https://github.com/soghayarmahmoud/Al-Buckary/issues) for the full list!

### 🟢 Milestone 1 — Core Reading Experience
- Bookmark icon on hadith cards with scroll-to-bookmark
- Save and restore home page scroll position
- Hadith explanation (Sharh) with expandable UI

### 🔵 Milestone 2 — Learning & Engagement
- Chapter quiz system with scoring
- Companions biographies screen (سيرة الصحابة)
- Spaced repetition for hadith memorization
- Daily learning goals with streak enhancement

### 🟡 Milestone 3 — Statistics & Gamification
- Professional charts (pie, bar, line) with fl_chart
- Chapter completion certificates
- Achievement badges system

### 🔴 Milestone 4 — Authentication & Cloud Sync
- Firebase Authentication (Email, Google, Apple)
- Cloud sync for user progress (Firestore)
- User profile & community leaderboard
- Offline-first with background sync queue

---

## 🤝 Contributing

We welcome contributions from developers of all skill levels! Many of our issues are labeled `good first issue` and `help wanted` — perfect for beginners.

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'feat: add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

| Prefix | Usage |
|---|---|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation changes |
| `style:` | Formatting, no code change |
| `refactor:` | Code restructuring |
| `test:` | Adding tests |
| `chore:` | Tooling, dependencies |

### Development Tips

- The app uses **Provider** for state management — check `lib/providers/` for patterns
- Database schema is in `lib/database_helper.dart` with self-healing migrations
- Hadith data is pre-loaded from `lib/hadith_data.dart`
- All Arabic text should use `TextDirection.rtl`

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---
## ⭐ If you like this project, consider sponsoring me
## 💬 Contact

For inquiries, suggestions, or collaborations:

**Email:** [alsighiar@gmail.com](mailto:alsighiar@gmail.com)  
**GitHub:** [@soghayarmahmoud](https://github.com/soghayarmahmoud)

---

<div align="center">

**⭐ Star this repo if you find it useful!**

*بارك الله فيكم — May Allah bless your efforts in spreading knowledge.*

</div>
