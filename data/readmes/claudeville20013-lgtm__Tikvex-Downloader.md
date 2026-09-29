# Tikvex – Official Website

**Videos in HD. No Watermark.**

Landing page for the Tikvex app — a fast, free TikTok video downloader that saves videos in high quality without any watermark.

## Live site

Once published with GitHub Pages:

```
https://https://github.com/claudeville20013-lgtm/tikvex/
```

(or your custom domain)

## Features highlighted

- **High Quality** – Download videos in HD  
- **No Watermark** – Clean & original videos  
- **Fast & Easy** – Paste link → download  
- **100% Safe & Secure** – Always free  

## Deploy to GitHub Pages

### Option A – New repository

1. Create a new repository on GitHub named `tikvex` (or any name you like).
2. Upload all files from this folder (`index.html`, `styles.css`, `script.js`, `assets/`, `README.md`).
3. Go to **Settings → Pages**.
4. Under **Source**, select **Deploy from a branch**.
5. Choose branch `main` (or `master`) and folder `/ (root)`.
6. Click **Save**. Your site will be live in 1–2 minutes.

### Option B – GitHub CLI / terminal

```bash
# From this folder
git init
git add .
git commit -m "Initial Tikvex landing page"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/tikvex.git
git push -u origin main
```

Then enable Pages as described above.

### Custom domain (optional)

Add a `CNAME` file in the root with your domain, then configure DNS according to GitHub’s docs.

## Local preview

Open `index.html` in a browser, or run a simple server:

```bash
# Python
python3 -m http.server 8080

# Node
npx serve .
```

Visit `http://localhost:8080`.

## Project structure

```
tikvex-website/
├── index.html          # Main landing page
├── styles.css          # Styles
├── script.js           # Mobile menu + smooth scroll
├── assets/
│   └── images/         # App screenshots & promo art
└── README.md
```

## Customize

- Replace the “Get on Android / iOS” button links in `index.html` with your real store URLs when ready.
- Update the year or add privacy/terms links in the footer as needed.

---

© 2026 Tikvex
