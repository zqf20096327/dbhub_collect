# SharpLink URL Shortener (Web App)

<div align="right">

[![CI](https://img.shields.io/github/actions/workflow/status/SagarBiswas-MultiHAT/SharpLink-URL-Allies/ci.yml?branch=main)](https://github.com/SagarBiswas-MultiHAT/SharpLink-URL-Allies/actions)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-pytest-orange)](https://github.com/SagarBiswas-MultiHAT/SharpLink-URL-Allies)
[![License](https://img.shields.io/github/license/SagarBiswas-MultiHAT/SharpLink-URL-Allies)](https://github.com/SagarBiswas-MultiHAT/SharpLink-URL-Allies/blob/main/LICENSE)
[![Last commit](https://img.shields.io/github/last-commit/SagarBiswas-MultiHAT/SharpLink-URL-Allies)](https://github.com/SagarBiswas-MultiHAT/SharpLink-URL-Allies/commits)
[![Live](https://img.shields.io/badge/live-sharplink.onrender.com-brightgreen)](https://sharplink.onrender.com/)

</div>

This project lets you turn a long link into a short link.

![](pics/sharplink.onrender.com.png)

## Live: https://sharplink.onrender.com/

Example:

- Long : https://youtu.be/oUp4SWSrYYk?si=Z7r-93Y6WbqYXrns
- Short (yours) : https://sharplink.onrender.com/MultiHAT
- mirror (TinyURL) : https://tinyurl.com/2d89to88

When someone opens the short link, the website sends them to the long link.

## What you can do (Features)

### 1) Make a short link

You paste a big URL, press **Generate**, and you get a new short link.

### 2) Choose your own short name (Custom alias)

You can pick the end part of the link (the “nickname”).

Example:

- Alias: `my-launch`
- Short link becomes: `http://YOUR-COMPUTER:5000/my-launch`

If you leave it empty, the app will make a random one for you.

### 3) Make the link expire (Expires at)

You can choose a date and time.

- Before that time: the short link works.
- After that time: the page shows **Link expired**.

If you leave it empty, the link never expires.

### 4) Also create a TinyURL link (optional)

There is a checkbox called **Also create a TinyURL mirror**.

If you turn it on, the app will also ask TinyURL to create a short link that points to the same long URL.

Important: TinyURL does NOT let us choose a custom alias using this simple API.

### 5) Copy buttons

You can press **Copy** to copy the link.

Note: copying works best on `https://` or `http://localhost`. On `http://<LAN-IP>` some browsers block copying; the app tries a safe fallback, but a few browsers may still block it.

## How to run it (Windows PowerShell)

### Step 1: Make a virtual environment (a safe Python bubble)

Run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 2: Install the project packages

Run:

```powershell
pip install -r requirements.txt
```

### Step 3: Start the web app

Run:

```powershell
set FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5000
```

### Step 4: Open the website

Open this in your browser:

http://localhost:5000

## How to use it (In the browser)

1. Open the website.
2. Paste your long link into **Destination URL**.
3. (Optional) Type a **Custom alias**.
4. (Optional) Pick an **Expires at** date/time.
5. (Optional) Turn on **TinyURL mirror**.
6. Click **Generate**.
7. Copy the short link and share it.

## Where the links are saved

Your short links are saved in a small SQLite database file on your computer:

- `data/url_store.db`

If a legacy `data/url_store.json` exists, the app will migrate it on first run.

You can override the database location with:

```powershell
$env:SHARPLINK_DB_PATH="C:\path\to\url_store.db"
```

You can also use a `.env` file. See [.env.example](.env.example).

This file remembers:

- the long URL
- when the short link was created
- when it expires (if you set it)

## "Accessible from anywhere" (Very important)

This app creates short links that work **from your computer/server**.

That means:

- If your computer is OFF, links won’t work.
- If people are not on your network, they cannot reach your computer unless you deploy it online.

To make links work for everyone on the internet, you must deploy this app on a public server (hosting).

## For developers (Optional API)

You can also call the backend directly:

- `POST /api/shorten`
  - JSON body example:
    ```json
    {
      "url": "https://example.com",
      "alias": "custom",
      "expires_at": "2025-12-31T23:59",
      "use_tiny": true
    }
    ```

- `GET /ALIAS`
  - Redirects to the long URL
  - Returns **410** if expired

## Quick checks

- Health check: http://localhost:5000/health

## Testing

Install dev dependencies:

```powershell
pip install -r requirements-dev.txt
```

Run tests:

```powershell
pytest
```

## Security notes

- Only `http://` and `https://` URLs are accepted.
- Aliases are length-limited and restricted to letters, numbers, `-`, and `_`.
- API requests are rate-limited by IP.
- If you deploy publicly, add abuse controls and monitoring.

## Rate limiting (production)

The default limiter uses in-memory storage, which is fine for local testing but not for production.
Use Redis in production by setting:

```powershell
$env:RATELIMIT_STORAGE_URI="redis://localhost:6379/0"
```

Or add the same to your `.env` file. See [.env.example](.env.example).

## Credits

Developed by Sagar Biswas: https://github.com/SagarBiswas-MultiHAT
