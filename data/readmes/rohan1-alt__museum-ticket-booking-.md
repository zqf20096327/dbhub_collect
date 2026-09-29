# Heritage Explorer — Indian Museum Ticket Booking

A PHP/MySQL web app for browsing Indian museums and booking entry tickets online. Deployed with **Render** (hosting) + **TiDB Cloud** (free MySQL-compatible database) — no local server required.

## What's in this app
- Landing page with all 6 museums, login/signup, cart, quiz, feedback
- Real user accounts (hashed passwords, PHP sessions) — not fake/localStorage
- A working booking form on every museum page that actually saves to the database
- "My Bookings" — logged-in users can see their own booking history
- An admin panel (`/php/admin.php`) that lists every booking — locked behind an admin login
- CSRF protection on every form that writes to the database
- Toast notifications instead of browser `alert()` popups
- Reliable, properly-licensed images (swapped out fragile Google-thumbnail hotlinks for Wikimedia Commons)

## Project Structure
```
museum-booking/
├── index.html                  # Landing page (real login/signup, mobile nav)
├── museums/                    # One page per museum, forms POST to /php/book_ticket.php
├── php/
│   ├── config.php              # Reads DB creds from env vars (safe to commit)
│   ├── book_ticket.php         # Handles booking form submissions (returns JSON)
│   ├── signup.php              # Creates a real account (hashed password) + session
│   ├── login.php                # Verifies credentials + starts a session
│   ├── logout.php               # Destroys the session
│   ├── session.php              # Lets the frontend check if a user is logged in
│   ├── csrf_token.php           # Issues a CSRF token for forms to submit back
│   ├── my_bookings.php          # Returns the logged-in user's own bookings
│   ├── admin_guard.php          # Blocks admin.php unless the session is an admin
│   └── admin.php               # Lists all bookings — admin only
├── sql/
│   └── schema.sql              # Database schema, sample museums, and a default admin account
├── assets/css/
│   ├── theme-heritage.css      # Shared theme (Kolkata, Delhi, Victoria Memorial)
│   ├── theme-modern.css        # Shared theme (CSMVS, Chennai, Salar Jung)
│   └── toast.css               # Shared toast notification styles
├── Dockerfile                  # Used by Render to build & run the app
```

---

## Part 1 — Accounts you need to create

You need exactly two free accounts. Neither needs a credit card.

### 1. GitHub (to hold your code)
1. Go to https://github.com/signup
2. Pick a username, enter your email, create a password, verify your email.
3. That's it — this is just where your code lives so Render can find it.

### 2. TiDB Cloud (your free database)
1. Go to https://tidbcloud.com and sign up (Google/GitHub sign-in works too).
2. Once in the dashboard, click **Create Cluster** → choose the **Serverless** tier (it's free).
3. Give it any name, pick a region close to you, and create it — takes about a minute.
4. Once it's ready, click **Connect** on your cluster. You'll see a host, port, username, and password — **copy all four somewhere safe**, you'll need them in Part 3.

### 3. Render (to host the actual website)
1. Go to https://render.com and sign up — easiest is "Sign up with GitHub" since you just made that account.
2. That links Render to your GitHub automatically, which makes Part 3 faster.

---

## Part 2 — Getting your code onto GitHub (step-by-step, no prior git needed)

Git is just a tool that tracks changes to your code and lets you upload ("push") it to GitHub. Here's the minimum you need.

### Step 1: Install git (if you don't have it)
- Windows: download from https://git-scm.com/downloads and run the installer (default options are fine).
- Mac: open Terminal and type `git --version` — if it's not installed, it'll prompt you to install it.

### Step 2: Create the repository on GitHub
1. Log into GitHub, click the **+** icon top-right → **New repository**.
2. Name it `museum-booking`.
3. Public or private both work fine once you've connected Render to your GitHub account — private is a good default if you don't want strangers browsing your code.
4. **Do NOT** check "Add a README" or ".gitignore" — you already have those in your project folder.
5. Click **Create repository**. GitHub will show you a page with some commands — keep this tab open.

### Step 3: Push your project folder
1. Unzip the project I gave you somewhere on your computer (e.g. Desktop).
2. Open a terminal (Command Prompt/PowerShell on Windows, Terminal on Mac) and navigate into the folder:
   ```bash
   cd Desktop/museum-booking
   ```
3. Run these commands one at a time (press Enter after each, wait for it to finish):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/<your-username>/museum-booking.git
   git push -u origin main
   ```
   Replace `<your-username>` with your actual GitHub username. The first time you push, it may open a browser window asking you to log into GitHub to confirm — that's normal, just approve it.
4. Refresh your GitHub repo page in the browser — you should now see all your files there.

**That's the whole git workflow you need for now.** Any time you make changes later and want to update GitHub, you just repeat:
```bash
git add .
git commit -m "describe what you changed"
git push
```

---

## Part 3 — Deploying on Render

### Step 1: Set up the database
1. In TiDB Cloud, open your cluster → **Chat2Query** or the **SQL Editor** (either works).
2. Paste in the entire contents of `sql/schema.sql` from this project and run it. This creates all the tables and adds the 6 museums plus a default admin account.

### Step 2: Create the web service on Render
1. In the Render dashboard, click **New → Web Service**.
2. Choose **Build and deploy from a Git repository**, then select your `museum-booking` repo.
3. Render will detect the `Dockerfile` automatically — leave **Environment** as **Docker**.
4. Choose the **Free** instance type.
5. Before clicking Create, scroll to **Environment Variables** and add these (using the values TiDB Cloud gave you):
   | Key | Value |
   |---|---|
   | `DB_HOST` | (from TiDB Cloud) |
   | `DB_PORT` | `4000` |
   | `DB_USER` | (from TiDB Cloud — includes a prefix like `xxxx.root`) |
   | `DB_PASS` | (from TiDB Cloud) |
   | `DB_NAME` | `museum_booking` |
6. Click **Create Web Service**. Render will build and deploy — takes a few minutes the first time.
7. When it's done, Render gives you a live URL like `https://museum-booking.onrender.com`. Open it — your site is live.

Render's free tier spins the service down after inactivity — the first visit after idling takes ~30-60 seconds to wake up. That's normal and expected on the free tier, not a bug.

### Step 3: Log into the admin panel
- Go to `https://<your-render-url>/index.html`, click **Login**.
- Email: `admin@heritage-explorer.local` — Password: `ChangeMe123!`
- **Change this password immediately** (sign up won't overwrite it — for now, the simplest way is to delete that row in TiDB Cloud's SQL editor and re-run just the admin INSERT line from `schema.sql` with a password you choose, hashed via any online bcrypt generator, or ask me to walk you through it).
- Once logged in as admin, an **Admin Panel** link appears in the nav — that's your bookings dashboard.

---

## Making changes later
Whenever you edit files locally and want them live again:
```bash
git add .
git commit -m "what you changed"
git push
```
Render automatically redeploys within a minute or two of every push — you don't need to touch the Render dashboard again.

## Image credits
A few images were swapped from unreliable Google-thumbnail hotlinks to stable Wikimedia Commons files, which require attribution under their Creative Commons licenses:
- Nataraja bronze (Government Museum, Chennai) — photo via Wikimedia Commons, CC BY 2.0
- Gandhara Gallery, Bharhut Stupa gateway, Egyptian mummy (Indian Museum, Kolkata) — photos by Biswarup Ganguly and West Bengal Wikimedians User Group, Wikimedia Commons, CC BY / CC BY-SA
- The Veiled Rebecca (Salar Jung Museum) — photo via Wikimedia Commons, CC BY-SA 4.0
- Victoria Memorial panorama — photo by PlaneMad, Wikimedia Commons, CC BY-SA 2.5

If you display these publicly, add a small "Images: Wikimedia Commons" credit line in your footer to stay compliant with the license terms.

## Known limitations / next steps
- No CSRF protection on the login/signup forms in edge cases involving multiple tabs open at once (rare, low risk) — the token refreshes on page load.
- No automated tests yet.
- No password reset flow (forgot password) — out of scope for now but a natural next addition.

## Tech
PHP (mysqli, prepared statements, sessions) · MySQL/TiDB · HTML/CSS/JS · Docker · Render
