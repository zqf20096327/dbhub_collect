# Hand Gesture-Based Biometric Authentication System

A cybersecurity biometric authentication project featuring **two distinct versions**:
1. **Desktop GUI Application** (Python + CustomTkinter + OpenCV + SQLite)
2. **Web Portal Application** (Neumorphic UI + MediaPipe JS + WebCrypto + Firebase Cloud Firestore, ready for GitHub Pages & Vercel)

---

## 📌 Project Overview: The Two Versions

| Feature | 🖥️ Version 1: Desktop GUI App | 🌐 Version 2: Web Portal App |
| :--- | :--- | :--- |
| **Primary Use** | Local desktop program | Online web portal or local browser portal |
| **Interface** | CustomTkinter (Python GUI) | Modern Neumorphic UI (HTML5, CSS3, JS) |
| **Camera Tracking** | OpenCV (`cv2`) + MediaPipe Python | Browser MediaPipe JS (`@mediapipe/hands`) |
| **Cryptography** | Python `hashlib` (PBKDF2-HMAC-SHA256) | Native WebCrypto API (PBKDF2-HMAC-SHA256) |
| **Database** | Local SQLite (`gesture_login.db`) | **Firebase Cloud Firestore** + Local Demo Fallback |
| **Cloud / Hosting** | Local desktop only | **GitHub Pages**, **Vercel**, or local Flask (`:5001`) |
| **Entry Point** | `python app.py` | `index.html` (or `python web_app/app.py`) |

---

## ✋ Hand Gesture Values

Both versions use the same standard finger-counting biometric scheme:

| Value | Gesture |
| :---: | :--- |
| **0** | Fist (0 fingers raised) |
| **1** | One finger (Index finger) |
| **2** | Two fingers (Peace / Victory sign) |
| **3** | Three fingers |
| **4** | Four fingers |
| **5** | Open palm (All 5 fingers) |

> **Authentication Rule**: Passwords consist of your master text password + a sequential 3-gesture biometric key (e.g., `5 -> 0 -> 2`).

---

## 🖥️ Version 1: Python Desktop Application

Runs as a native desktop application with a CustomTkinter graphical window and local SQLite database.

### Setup & Run
1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch the desktop GUI:
   ```bash
   python app.py
   ```
   *(Or launch the terminal CLI version with `python app_cli.py`)*

### Key Files (Desktop App)
* `app.py`: Main desktop launcher
* `app_gui.py`: CustomTkinter GUI implementation
* `app_cli.py`: Terminal/command-line interface alternative
* `gesture_detector.py`: OpenCV + MediaPipe finger counting engine
* `database.py`: Local SQLite database operations (`gesture_login.db`)
* `security.py`: Python PBKDF2 salting and hashing

---

## 🌐 Version 2: Web Portal Application (Neumorphic & Cloud-Ready)

A modern, serverless web application that runs directly in any browser. It uses browser webcam tracking via MediaPipe JavaScript and client-side WebCrypto PBKDF2 cryptography.

### Running the Web Portal

#### Option A: 100% Static / GitHub Pages / Vercel (No Python Required)
* **Direct Browser**: Double-click or open `index.html` in your browser.
* **GitHub Pages**:
  1. Push this repository to GitHub.
  2. In your repo: **Settings** $\rightarrow$ **Pages** $\rightarrow$ Source: `Deploy from a branch` (`main`, `/ (root)`).
  3. GitHub provides a free, live HTTPS URL (e.g., `https://<username>.github.io/<repo>/`).
* **Vercel**:
  1. Import the GitHub repository into [Vercel](https://vercel.com).
  2. Deploy as a static site in seconds.

#### Option B: Local Flask Development Server
If you prefer running it locally via Flask:
```bash
source venv/bin/activate
python web_app/app.py
```
Open **[http://localhost:5001](http://localhost:5001)** in your browser.

---

### ☁️ Firebase Cloud Database Setup (Web Portal)

The Web Portal supports **Firebase Cloud Firestore** for permanent cloud storage across devices:

1. Create a free project at [console.firebase.google.com](https://console.firebase.google.com/).
2. Under **Build**, select **Firestore Database** $\rightarrow$ **Create Database** (start in Test mode).
3. Click the Web icon `</>` to register a web app and copy your config JSON:
   ```json
   {
     "apiKey": "AIzaSy...",
     "authDomain": "your-app.firebaseapp.com",
     "projectId": "your-app",
     "storageBucket": "your-app.appspot.com",
     "messagingSenderId": "...",
     "appId": "..."
   }
   ```
4. On the web portal, click the **Cloud: Local Demo** pill at the top-right corner, paste the JSON, and click **Save & Connect**.
   *(Note: If Firebase is not configured, the portal automatically operates in local fallback mode using browser storage so everything works seamlessly).*

### Key Files (Web Portal)
* `index.html`: Root web application file (Neumorphic UI)
* `style.css`: Neumorphism styling system, animations, and responsive layout
* `script.js`: MediaPipe hand tracking, hold-to-confirm gesture capture, and flow logic
* `firebase-config.js`: WebCrypto PBKDF2 hashing engine & Firebase Firestore repository
* `bg.png`: Futuristic schematic background artwork
* `web_app/`: Self-contained Flask version with its own SQLite database backup

---

## 🔒 Security Features (Both Versions)

* **PBKDF2-HMAC-SHA256**: 100,000 iterations for both text passwords and gesture sequences.
* **Cryptographic Salting**: Unique 16-byte random salt generated per secret to prevent rainbow table attacks.
* **Account Lockout Policy**: 3 consecutive failed attempts trigger a temporary 30-second lockout.
* **Security Audit Trail**: All authentication events (`SUCCESS`, `FAILED`, `REGISTERED`) with reasons and timestamps are permanently logged.
* **HTTPS Camera Protection**: Web camera streams strictly require HTTPS or `localhost` to safeguard user biometrics.
