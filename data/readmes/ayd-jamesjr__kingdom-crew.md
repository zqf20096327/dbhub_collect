# Kingdom Crew Fellowship Website

Official website for Kingdom Crew Fellowship, UNILAK Rwamagana Campus.
HTML + CSS + vanilla JavaScript frontend, with an optional Node/Express backend (TiDB Cloud database + AI assistant).

## What works without any backend
Pages, navigation, events and gallery (from `config.js`), social links, the Bible reader (loads text from the free bible-api.com), form validation. The contact form and AI assistant **need the backend** because a static page cannot safely store messages or hide an API key.

## Folder map
```
kingdom-crew/
├── public/            <- the website (this is what visitors see)
│   ├── *.html         index, about, activities, events, gallery, bible, contact
│   ├── css/style.css  colours and layout (edit colours at the top)
│   ├── js/config.js   EDIT THIS: contacts, social links, events, gallery
│   ├── js/scriptures.js  Bible book summaries
│   ├── js/main.js     all interactive features
│   └── images/        put your logo and photos here
├── src/server.js      Express server + API
├── src/config/db.js   TiDB connection
├── schema.sql         database tables
├── .env.example       list of secret settings
└── package.json
```

## 1. Run it on your computer
1. Install Node.js (LTS) from nodejs.org.
2. Open the folder in VS Code, then open the terminal (Ctrl+`).
3. Run:
   ```
   npm install
   copy .env.example .env      (Mac/Linux: cp .env.example .env)
   npm start
   ```
4. Open http://localhost:3000. The site works immediately. Database and AI show friendly "not connected yet" messages until you fill `.env`.

Frontend only (no backend): open `public/index.html` with the VS Code "Live Server" extension.

## 2. Add your real details
Open `public/js/config.js`:
- Paste real Facebook, Instagram, TikTok, YouTube URLs and the **existing** WhatsApp Community invite link into the `social` block. Empty links show as "(soon)" and do not link anywhere.
- Edit `events` and `gallery`. For photos: copy the file into `public/images/`, then add `{ src: 'images/yourphoto.jpg', alt: 'Describe the photo', caption: 'Caption' }`.
- The official logo is in `public/images/` (`logo-full.png` for light backgrounds, `logo-full-light.png` for dark ones, `logo-emblem*.png` for the cross-and-Bible mark alone). To change it, replace those files keeping the same names.

## 3. Connect the database (TiDB Cloud)
1. Create a free TiDB Cloud Serverless cluster, click **Connect**, and copy host, port, user and password.
2. Open the **SQL Editor**, paste all of `schema.sql`, run it.
3. Put the values in `.env` (`DATABASE_HOST`, `DATABASE_PORT`, `DATABASE_USER`, `DATABASE_PASSWORD`, `DATABASE_NAME`). Restart `npm start`.
4. Visit http://localhost:3000/api/health. It should show `"database": true`.
5. Test: send a message on the Contact page, then run `SELECT * FROM inquiries;` in TiDB.

Mark an event published by inserting a row in `events` with `is_published = 1`. Delete the `DEMO:` row.

## 4. Connect the AI assistant (free option: Groq)
The browser never sees your key. It talks to `/api/chat` on your server, which calls the AI provider.
1. Go to console.groq.com, sign in, and create an API key. Groq's free tier needs no billing setup.
2. In `.env` set `AI_API_KEY=` to that key. The other three AI lines are already filled for Groq (`AI_BASE_URL`, `AI_MODEL`, `AI_FALLBACK_MODEL`).
3. Restart `npm start` and check http://localhost:3000/api/health shows `"ai": true`. Then open the chat button on the site and ask a question.
4. On Render, add the same four variables under Environment.

**Free limits (as reported by third-party guides in October 2026; confirm in your Groq console):** the main model allows roughly 1,000 requests and 200,000 tokens per day, the fallback model (`llama-3.1-8b-instant`) roughly 14,400 requests per day, both about 30 requests per minute. That is plenty for a fellowship site, but no free service is guaranteed. Providers can change limits or models, so the server retries once with the fallback model and shows a polite message if both are busy.

**Alternative: Google Gemini.** Get a key at aistudio.google.com and use the Gemini lines commented out in `.env.example`. Free-tier limits are lower and not fully published, and free-tier data handling differs by provider, so read each provider's terms before sending visitors' questions to it.

**OpenAI** works too (`AI_BASE_URL=https://api.openai.com/v1`), but its API is pay-as-you-go.

Built-in safeguards: 20 questions per 10 minutes per visitor, short answers, and a system prompt that forbids inventing fellowship facts and directs crisis situations to real people.

## 5. Put it on GitHub
```
git init
git add .
git commit -m "Kingdom Crew website"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/kingdom-crew.git
git push -u origin main
```
`.env` is ignored by `.gitignore`, so your secrets are not uploaded. Check this on GitHub before sharing.

## 6. Publish (pick one)
**A. Render (full site: database + AI)**
1. render.com > New > Web Service > connect your GitHub repo.
2. Build command `npm install`, start command `npm start`.
3. Under Environment, add every variable from `.env.example` with your real values.
4. Deploy. Render provides HTTPS. Free instances may sleep when idle, so the first visit can be slow. Check Render's current free-tier terms.

**B. GitHub Pages (static only, free)**
Settings > Pages > deploy from `main`, folder `/public` is not selectable on all setups; if so, move the contents of `public/` to the repo root or use a `gh-pages` branch. All links are relative, so a `/kingdom-crew/` subfolder URL works. For the form and AI to work from Pages, deploy the backend on Render, set `apiBase` in `config.js` to the Render URL, and set `ALLOWED_ORIGIN` on Render to your Pages address.

After publishing, replace `YOUR-SITE-ADDRESS` in `public/robots.txt` and `public/sitemap.xml`.

## 7. Updating later
Edit `config.js` (events, photos, links), commit and push. Render redeploys automatically.

## Checklist: real links to insert (in `public/js/config.js`)
- [ ] Facebook page URL
- [ ] Instagram profile URL
- [ ] TikTok profile URL
- [ ] YouTube channel URL
- [ ] WhatsApp Community invite link (the existing community)
- [ ] Real photos and events
- [ ] Leadership approval of motto, mission and vision (`about.html`)
- [ ] `YOUR-SITE-ADDRESS` in robots.txt and sitemap.xml

## Common problems
- **"Cannot find module"**: run `npm install` again.
- **Port in use**: change `PORT` in `.env`.
- **Database error**: check host/user/password, and that `schema.sql` was run.
- **AI "key is not valid"**: re-copy the key; no spaces or quotes.
- **Bible text will not load**: needs internet; check the passage spelling.

## Not built yet (honest scope)
Member accounts, admin dashboard, member directory and community feed from the larger master prompt are not in this version. The current database has only `inquiries` and `events`. Build those in later phases once this foundation is confirmed working.
