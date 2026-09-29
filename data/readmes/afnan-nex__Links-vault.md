# LinkVault (Android)

> **"Copy a link once. Never lose it."**

LinkVault is a modern, privacy-first Android application designed to automatically detect and preserve URLs copied to the device clipboard. Every detected URL is stored locally with its complete timestamp and metadata, enabling users to revisit, copy, share, open, or insert previously copied links with ease.

---

## 🌟 Key Features

1. **Automatic URL Collection**: Seamlessly monitors clipboard changes and captures valid URLs without saving arbitrary text.
2. **Duplicate & Timestamp Preservation**: Every copy event creates a distinct record preserving its exact timestamp and time zone.
3. **Dedicated LinkVault Keyboard**: Custom Android `InputMethodService` that replaces traditional typing with an instant link insertion list, live search, quick actions (Copy, Share, Open), and an adaptive action key (SEND/DONE/ENTER).
4. **Swipe-to-Delete**: Right-to-left swipe with Material 3 delete affordance.
5. **Biometric-Guarded 30-Day Retention**: Deleted links are kept for 30 days and require biometric authentication (Fingerprint/Face/Device PIN) every single time they are accessed.
6. **Automatic Cleanup**: Daily WorkManager background worker automatically purges deleted links older than 30 days.
7. **JSON Backup & Restore**: Standard JSON export/import via Android's Storage Access Framework (SAF), preserving timestamps and duplicate entries.
8. **Excluded Applications**: Blacklist sensitive apps (password managers, banking apps) from clipboard monitoring.
9. **Material 3 Design**: Supports Dynamic Color, System default, Light, and Dark themes.
10. **100% Offline & Private**: All data is stored locally in Room SQLite with zero internet permissions.

---

## 🛠️ Architecture & Tech Stack

- **Platform**: Android 8.0+ (API 26+)
- **Architecture**: MVVM with Kotlin Coroutines & Flow
- **UI Framework**: Jetpack Compose + Material 3
- **Database**: Room SQLite (`LinkDatabase`, `LinkDao`, `LinkEntity`)
- **Preferences**: Jetpack DataStore Preferences
- **Background Processing**: WorkManager (`DeletedLinksCleanupWorker`)
- **Biometrics**: AndroidX Biometric (`BiometricPrompt`)
- **Custom Keyboard**: Android `InputMethodService` (`LinkVaultInputMethodService`)

---

## 📁 Package Structure

```
com.linkvault.app
├── data
│   ├── local
│   │   ├── LinkEntity.kt
│   │   ├── LinkDao.kt
│   │   └── LinkDatabase.kt
│   ├── preferences
│   │   └── AppPreferences.kt
│   ├── repository
│   │   └── LinkRepository.kt
│   └── importexport
│       └── ImportExportManager.kt
├── clipboard
│   ├── UrlDetector.kt
│   └── ClipboardMonitor.kt
├── biometric
│   └── BiometricAuthManager.kt
├── worker
│   └── DeletedLinksCleanupWorker.kt
├── keyboard
│   ├── LinkVaultInputMethodService.kt
│   └── KeyboardUi.kt
└── ui
    ├── theme
    │   ├── Color.kt
    │   ├── Type.kt
    │   └── Theme.kt
    ├── navigation
    │   ├── NavRoutes.kt
    │   └── AppNavigation.kt
    ├── components
    │   ├── LinkItemCard.kt
    │   └── ConfirmationDialog.kt
    ├── links
    │   ├── LinksViewModel.kt
    │   └── LinksScreen.kt
    ├── deleted
    │   ├── DeletedLinksViewModel.kt
    │   └── DeletedLinksScreen.kt
    ├── settings
    │   ├── SettingsViewModel.kt
    │   ├── SettingsScreen.kt
    │   ├── ExcludedAppsScreen.kt
    │   ├── AboutScreen.kt
    │   └── PrivacyPolicyScreen.kt
    └── MainActivity.kt
```

---

## 🚀 Building & Running

### Prerequisites
- Android Studio Iguana / Jellyfish / Ladybug or newer
- JDK 17+
- Android SDK (API 34)

### Steps
1. Open the project directory in Android Studio.
2. Allow Gradle to sync dependencies.
3. Select an Android device or emulator running Android 8.0 (API 26) or higher.
4. Click **Run** (`Shift + F10`).
5. (Optional) To enable the keyboard, go to **Settings → System → Languages & input → On-screen keyboard → Manage keyboards** and enable **LinkVault Keyboard**.
