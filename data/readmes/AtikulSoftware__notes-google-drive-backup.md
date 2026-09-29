# 📝 Notes App (with Google Drive Backup)

একটি সিম্পল Android Notes অ্যাপ, যেখানে নোটগুলো **SQLite Database**-এ সেভ করা হয় এবং **Google Drive** এর মাধ্যমে Backup ও Restore করা যায়। প্রজেক্টটি সম্পূর্ণভাবে **Java** দিয়ে তৈরি, কোনো ViewModel/LiveData ব্যবহার করা হয়নি - যাতে যে কেউ সহজে কোড বুঝে নিজের প্রয়োজনমতো ব্যবহার করতে পারে।

---

## ✨ ফিচারসমূহ

- নোট তৈরি, এডিট ও ডিলিট করা (CRUD)
- SQLite দিয়ে Local Database
- Google Account দিয়ে Authorize করে Google Drive-এ Backup
- Drive থেকে Restore করে সব নোট ফিরিয়ে আনা
- Backup/Restore চলাকালীন Progress Dialog
- Drive-এর **Hidden App Data Folder** ব্যবহার করা হয়েছে (ইউজারের Drive-এ আলাদাভাবে দেখা যায় না, শুধু এই অ্যাপই এটা access করতে পারে)

---

## 📸 স্ক্রিনশট

| হোম স্ক্রিন | নোট Add/Edit |
|---|---|
| ![Home Screen](screenshots/home_screen.jpg) | ![Add Note](screenshots/add_note.jpg) |
 
---


## 🛠️ টেকনোলজি

| বিষয় | লাইব্রেরি/টুল |
|---|---|
| Language | Java |
| Database | SQLite (SQLiteOpenHelper) |
| UI | RecyclerView, ConstraintLayout, Material Components |
| Authorization | Google Identity Services (AuthorizationClient) |
| Cloud Storage | Google Drive REST API (App Data Folder) |

---

## 📋 শুরু করার আগে যা যা লাগবে

1. [Android Studio](https://developer.android.com/studio) (সর্বশেষ Stable Version)
2. একটি Google Account
3. [Google Cloud Console](https://console.cloud.google.com/)-এ একটি Project

---

## 🚀 সেটআপ গাইড

### ধাপ ১: প্রজেক্ট Clone করা

```bash
git clone https://github.com/AtikulSoftware/notes-google-drive-backup.git
```

তারপর Android Studio দিয়ে প্রজেক্টটি ওপেন করো (`Open` → প্রজেক্ট ফোল্ডার সিলেক্ট করো) এবং Gradle sync শেষ হওয়া পর্যন্ত অপেক্ষা করো।

---

### ধাপ ২: Google Cloud Console-এ Project তৈরি করা

1. [Google Cloud Console](https://console.cloud.google.com/) এ যাও এবং একটি নতুন Project তৈরি করো (অথবা আগের কোনো Project সিলেক্ট করো - তবে নতুন Project রাখাই ভালো, যাতে অন্য অ্যাপের সেটিং-এর সাথে conflict না হয়)
2. উপরের সার্চ বার থেকে **"Google Drive API"** খুঁজে সেটি **Enable** করুন।

---

### ধাপ ৩: OAuth Consent Screen কনফিগার করা

1. **APIs & Services → OAuth consent screen** এ যাও
2. **User Type** হিসেবে **External** সিলেক্ট করো
3. App name, Support email ইত্যাদি পূরণ করো (App name-এ এই অ্যাপের নাম দাও, অন্য কোনো পুরনো প্রজেক্টের নাম নয়)
4. **Test users** সেকশনে গিয়ে যেই Gmail Account দিয়ে অ্যাপ Test করবে, সেই ইমেইলটি যোগ করো

> ⚠️ **গুরুত্বপূর্ণ:** App যতক্ষণ পর্যন্ত "Testing" মোডে থাকবে, ততক্ষণ শুধু Test Users হিসেবে যুক্ত করা Account দিয়েই Sign-in করা যাবে। অন্য কোনো Account দিয়ে করতে গেলে **"Access Blocked"** এরর আসবে।

---

### ধাপ ৪: Android OAuth Client ID তৈরি করা

1. **APIs & Services → Credentials → Create Credentials → OAuth Client ID** এ জান।
2. Application type হিসেবে **Android** সিলেক্ট করুন।
3. **Package name** দাও — যা `AndroidManifest.xml`-এ `package="..."` অথবা `build.gradle`-এ `applicationId` তে পাওয়া যাবে (যেমন: `com.devatikul.noteswithbackup`)
4. **SHA-1 certificate fingerprint** যোগ করতে হবে - নিচের ধাপ দেখো

---

### ধাপ ৫: SHA-1 Fingerprint বের করা

Android Studio-এর **Terminal** ওপেন করে এই কমান্ড রান করুন। :

```bash
./gradlew signingReport
```

আউটপুটে `Variant: debug` সেকশনের নিচে `SHA1:` লেখা একটা লাইন পাওয়া যাবে। সেই পুরো কোডটি কপি করে ধাপ ৪-এ SHA-1 ফিল্ডে বসিয়ে **Save** করো।

> এই পরিবর্তন Google-এর সিস্টেমে কার্যকর হতে কয়েক মিনিট সময় লাগতে পারে।

---

### ধাপ ৬: প্রজেক্ট Build ও Run করা

1. Android Studio-তে একটি Emulator বা রিয়েল ডিভাইস কানেক্ট করুন
2. **Run ▶️** বাটনে ক্লিক করুন
3. অ্যাপ চালু হলে কয়েকটি নোট তৈরি করুন
4. Menu থেকে **Backup to Drive** সিলেক্ট করো - প্রথমবার একটি Google Account সিলেক্ট করার এবং Permission দেওয়ার popup আসবে
5. Backup সফল হলে Toast মেসেজ দেখাবে

---

### ধাপ ৭: Restore চেক করা

Backup সিস্টেম সঠিকভাবে কাজ করছে কিনা চেক করতে:

1. অ্যাপের Data Clear করো (Settings → Apps → Notes With Backup → Storage → Clear Data) অথবা অ্যাপটি Uninstall করে আবার Install করো
2. অ্যাপ ওপেন করো - নোট লিস্ট খালি থাকবে
3. Menu থেকে **Restore from Drive** সিলেক্ট করো
4. আগের সব নোট ফিরে আসা উচিত

---

## 📁 প্রজেক্ট স্ট্রাকচার

```
app/src/main/java/com/devatikul/noteswithbackup/
├── Note.java                  → নোটের Model Class
├── NoteDatabaseHelper.java    → SQLite CRUD অপারেশন
├── NoteAdapter.java           → RecyclerView Adapter
├── MainActivity.java          → নোট লিস্ট স্ক্রিন
├── AddEditNoteActivity.java   → নোট Add/Edit স্ক্রিন
└── DriveBackupHelper.java     → Google Drive Backup/Restore লজিক
```

---

## ⚠️ সম্ভাব্য সমস্যা ও সমাধান

| সমস্যা | সমাধান |
|---|---|
| `Access Blocked` এরর | OAuth Consent Screen-এ Test User হিসেবে নিজের Gmail যোগ করো |
| Duplicate `META-INF` ফাইল এরর | `build.gradle`-এ `packaging { resources { excludes += [...] } }` ব্লক যোগ করো (কোডে উদাহরণ আছে) |
| Authorization বারবার fail হচ্ছে | SHA-1 এবং Package Name Cloud Console-এ ঠিকভাবে মিলছে কিনা চেক করো |

---

## 📜 লাইসেন্স

এই প্রজেক্টটি শেখার এবং ব্যক্তিগত ব্যবহারের জন্য উন্মুক্ত। ইচ্ছেমতো Fork, Modify এবং নিজের প্রজেক্টে ব্যবহার করা যাবে।

---

## 👨‍💻 তৈরি করেছেন

**DevAtikul**
🎥 YouTube: [DevAtikul](https://youtube.com/@devatikul) — Android ও Web Development টিউটোরিয়াল