# TikView for Android

A standalone Android app (Android 10 or newer) that works without a computer. It can:

- **Follow streamers.** Live status is checked every 90 seconds, and you get a notification when one of them goes live.
- **Watch videos and lives** in a full-screen viewer.
- **Record lives** with one tap, or turn on **auto-record** for a streamer. Recording keeps going with the screen off. Recordings are saved as MP4.
- **Download videos** and save them to your Gallery (Movies/TikView).
- **Share from TikTok.** In the TikTok app, tap **Share → TikView** on any video to open or download it.

Light and dark mode follow your phone's setting automatically. Tap the round button at the top to choose Light or Dark instead.

## Get the app (GitHub builds it for you)

1. Make a free account at github.com, then create a new **private** repository named `tikview-android`.
2. Upload everything in this folder, including the hidden `.github` folder. On a computer, the easiest way is **Add file → Upload files**, then drag the whole unzipped folder in.
3. Open the repository's **Actions** tab. The "Build TikView APK" job starts on its own and takes about 10 minutes.
4. When it's done, go to **Releases** on your phone (signed in to GitHub). Download `TikView-N.apk` and open it.
5. Android will ask to **allow installing apps from this source**. Allow it, then tap **Install**.

**Updates:** GitHub rebuilds the app every Monday with the newest TikTok fixes. To rebuild now, go to **Actions → Build TikView APK → Run workflow**. Install the new APK over the old one, and your streamers and downloads stay.

## Tips

- **Auto-record and live alerts** work while TikView is open or in the background, or while its "TikView" notification is showing. If you swipe the app away, it stops checking.
- Some phones (Samsung, Xiaomi, Huawei…) close background apps aggressively. Go to **Settings → Apps → TikView → Battery** and pick **Unrestricted**.
- If videos stop loading, TikTok probably changed something. Rebuild the app as described under Updates.

## For developers

This is a Kotlin app. The UI runs in a WebView (`app/src/main/assets/index.html`). The engine is written in Python and runs through Chaquopy (`app/src/main/python/tikview_core.py`, using yt-dlp). Media3 ExoPlayer is the viewer, and Media3 Transformer turns recordings into MP4. To build it locally, open the folder in Android Studio and run it.

Please be fair to creators: downloads and recordings are for personal viewing only.
