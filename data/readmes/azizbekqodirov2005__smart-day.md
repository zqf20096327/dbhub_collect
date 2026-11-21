# Smart Day — eslatmalar va kunlik reja

**Jonli versiya:** https://smartdayuz.netlify.app

O‘zbek tilidagi eslatmalar va kunlik reja ilovasi. Telefonga ilova kabi o‘rnatiladi (PWA) va eslatmalarni **aniq belgilangan soniyada** push-bildirishnoma qilib yuboradi — ilova yopiq yoki telefon qulflangan bo‘lsa ham.

<p>
  <img src="docs/screenshots/desktop-bugun.png" alt="Bugun sahifasi (kompyuter)" width="100%">
</p>
<p>
  <img src="docs/screenshots/mobile-bugun.png" alt="Bugun sahifasi (telefon)" width="32%">
  <img src="docs/screenshots/mobile-forma.png" alt="Yangi vazifa qo‘shish" width="32%">
  <img src="docs/screenshots/mobile-kalendar.png" alt="Kalendar (qorong‘i mavzu)" width="32%">
</p>

## Imkoniyatlar

- **Bugun** — hafta tasmasi, kunlik bajarilish, keyingi eslatma va soatma-soat jadval (hozirgi vaqt chizig‘i bilan)
- **Eslatmalar** — bir martalik yoki takrorlanuvchi (har kuni / hafta / oy), 5–60 daqiqa oldin eslatish, “keyinroq eslatish”
- **Vaqt ajratish** — dars, uchrashuv, sport uchun boshlanish va tugash vaqti, tez davomiylik tugmalari
- **Kalendar** — oy ko‘rinishi, istalgan kunga vazifa qo‘shish, kunni boshqa kunga nusxalash, haftalik va oylik maqsadlar
- **Statistika** — kunlik/haftalik/oylik bajarilish, ketma-ket kunlar, kategoriyalar bo‘yicha vaqt taqsimoti
- **Bildirishnomalar** — Web Push (VAPID), Chrome/Android’da aniq soniyada ko‘rsatish, ilova ichida ruxsat so‘rash, 6 xil eslatma ohangi
- Yorug‘ va qorong‘i mavzu, 320px dan katta ekrangacha moslashuvchan dizayn, oflayn ishlaydigan qobiq

## Texnologiyalar

| Qism | Texnologiya |
|---|---|
| Frontend | Vanilla JavaScript (ES modules), CSS, Service Worker, Web Push, Lucide SVG ikonkalar, Onest shrifti |
| Backend | Node.js, Express 5, Zod, JWT (httpOnly cookie), bcrypt, web-push |
| Hosting | Netlify Functions (API) + Netlify Scheduled Function (har daqiqada eslatmalar) |
| Baza | Supabase Postgres (lokalda — PGlite, o‘rnatish shart emas) |

## Muallif

**Azizbek Qodirov** — [AzbekDev](https://t.me/AzbekDev) · [azbek.uz](https://azbek.uz)

---

**Arxitektura:** statik frontend + **Netlify Functions** (API) + **Netlify Scheduled Function** (har daqiqada eslatmalarni yuboradi) + **Supabase Postgres** (baza). Lokal ishlab chiqishda baza kerak emas — ichki Postgres (PGlite) ishlaydi.

## Tezkor boshlash (kompyuteringizda, VS Code terminalida)

Node.js **20 yoki yangiroq** kerak (`node -v` bilan tekshiring).

```bash
cd smart-day
npm install
npm start
```

Brauzerda oching: **http://localhost:3000** → “Ro‘yxatdan o‘tish”.

Lokalda birinchi ishga tushirishda server **o‘zi** `JWT_SECRET` va VAPID kalitlarini yaratib `.env` fayliga yozadi. Hech narsa qo‘lda kiritish shart emas.

> `localhost` da push ishlaydi. Telefonda sinash uchun **HTTPS** kerak (pastdagi “Deploy: Netlify + Supabase” bo‘limiga qarang).

## Loyiha tuzilmasi

```
netlify/functions/
  api.mjs         – butun /api (Express) Netlify Function sifatida
  scheduler.mjs   – har daqiqada ishlaydi: vaqti kelgan eslatmalarga push yuboradi
netlify.toml      – publish papkasi, /api yo‘naltirish, xavfsizlik sarlavhalari (CSP)
supabase/schema.sql – baza jadvallari + RLS (Supabase SQL Editor’da bir marta ishga tushiriladi)
server/
  index.js        – lokal server (`npm start`) + ichki scheduler
  app.js          – Express, xavfsizlik (helmet, CSP), bazadagi login cheklovi
  api.js          – barcha API: auth, vazifalar, kategoriyalar, maqsadlar, statistika, push
  auth.js         – JWT (httpOnly cookie), requireAuth
  db.js           – Postgres: Supabase (`pg`) yoki lokal PGlite
  tasks.js        – eslatma vaqtini hisoblash, takrorlanuvchi vazifalar
  scheduler.js    – vaqti kelgan eslatmalarni topib push yuboradi
  push.js         – web-push (VAPID), eskirgan obunalarni tozalash
  time.js         – Asia/Tashkent vaqt zonasi bilan ishlash
  logger.js       – xatolar: konsol (Netlify Logs) + logs jadvali
public/
  index.html, manifest.webmanifest, sw.js (Service Worker)
  css/app.css     – dizayn tizimi (#0B0D12 / #8B5CF6 / #3B82F6)
  js/             – ilova (app.js, views.js, ui.js, api.js, push.js, sound.js)
scripts/
  smoke-test.mjs  – backend avtotesti (`npm test`)
  gen-icons.mjs, make-pwa-icons.py – ikonkalar
```

## Ma‘lumotlar bazasi jadvallari

| Jadval | Vazifasi |
|---|---|
| `users` | foydalanuvchi, parol hash (bcrypt), sozlamalar, vaqt zonasi |
| `categories` | kategoriyalar (rang + ikonka); 8 ta standart, o‘zingiznikini qo‘shish mumkin |
| `tasks` | eslatmalar (`kind='reminder'`) va kunlik reja bandlari (`kind='plan'`) |
| `push_subscriptions` | har bir qurilmaning push obunasi |
| `goals` | haftalik / oylik maqsadlar |
| `logs` | xatolar va push jurnali |
| `rate_limits` | login/ro‘yxatdan o‘tish urinishlarini cheklash (serverless uchun bazada) |

`tasks.remind_at` — push yuboriladigan aniq vaqt (UTC), `tasks.notified_at` — yuborilgan vaqt. Shu ikkisi bir eslatma uchun **takroriy xabar yuborilmasligini** ta‘minlaydi (`NULL` = hali yuborilmagan, `0` = o‘tkazib yuborilgan, `>0` = yuborilgan vaqt).

Takrorlanuvchi vazifalarda (har kuni/hafta/oy) har bir sana alohida qator; bildirishnoma yuborilgach, bajarilganda yoki kun o‘tib ketganda keyingi sana **avtomatik** yaratiladi.

## API kalitlari va maxfiy sozlamalar

Tashqi pullik xizmat kerak emas. Maxfiy qiymatlar (lokalda `.env`, Netlify’da *Environment variables*):

| Qiymat | Nima uchun | Qayerdan olinadi |
|---|---|---|
| `DATABASE_URL` | Supabase bazasiga ulanish | Supabase → **Connect → Transaction pooler** (port **6543**) |
| `JWT_SECRET` | login sessiyasini imzolash | `node -e "console.log(require('crypto').randomBytes(48).toString('hex'))"` |
| `VAPID_PUBLIC_KEY` | brauzer obunasi uchun (ochiq) | `npx web-push generate-vapid-keys` |
| `VAPID_PRIVATE_KEY` | pushni imzolash — **faqat serverda** | xuddi shu juftlik |
| `VAPID_SUBJECT` | push xizmatlariga aloqa manzili: `mailto:sizning@emailingiz.uz` | o‘z emailingiz |

Muhim: `.env` ni GitHub’ga **yuklamang** (`.gitignore` da bor). VAPID kalitlarini keyin o‘zgartirsangiz, barcha qurilmalar push’ni qayta yoqishi kerak. Supabase’ning `service_role`/`anon` kalitlari **kerak emas** va ishlatilmaydi.

## Deploy: Netlify + Supabase

**1) Supabase (baza)**
1. [supabase.com](https://supabase.com) → New project (parolni eslab qoling; region — sizga yaqin, masalan Frankfurt).
2. Chap menyu → **SQL Editor → New query** → `supabase/schema.sql` faylining **hammasini** joylab **Run** bosing. (Jadvallar yaratiladi va RLS yoqiladi — ochiq API orqali ma’lumotga kirib bo‘lmaydi.)
3. Yuqoridagi **Connect** tugmasi → **Transaction pooler** → URI’ni nusxalang (`postgresql://postgres.xxxx:[PAROL]@...pooler.supabase.com:6543/postgres`). `[PAROL]` o‘rniga o‘z parolingizni yozing. Bu `DATABASE_URL`.

**2) Netlify**
1. Loyihani GitHub’ga yuklang → Netlify → **Add new site → Import from Git**. Sayt nomini o‘zingiz tanlang. Build sozlamalari `netlify.toml` dan o‘qiladi (build buyrug‘i kerak emas).
2. **Site configuration → Environment variables** ga qo‘shing: `DATABASE_URL`, `JWT_SECRET`, `VAPID_PUBLIC_KEY`, `VAPID_PRIVATE_KEY`, `VAPID_SUBJECT`.
3. **Deploys → Trigger deploy**. Tugagach `https://sizning-sayt.netlify.app` HTTPS bilan tayyor — telefonda oching, ro‘yxatdan o‘ting, Sozlamalar → Bildirishnomalar → “Yoqish”.
4. Tekshiruv: **Logs → Functions → scheduler** da har daqiqada ishga tushish ko‘rinadi. `https://…/api/health` → `{"ok":true}`.

**Bilish kerak bo‘lgan cheklovlar**
- Eslatma aniqligi **±1 daqiqa**: scheduler har daqiqada bir marta ishlaydi (Netlify’da bundan tez bo‘lmaydi).
- **Supabase bepul loyihasi ~1 hafta hech kim kirmasa “pauza”ga tushadi** (Dashboard’dan “Restore” bilan tiklanadi). Scheduler har daqiqada bazaga murojaat qilgani uchun, odatda bu faol saytda yuz bermaydi, lekin kafolat emas.
- Netlify bepul rejasida funksiya vaqti ~10 soniya; scheduler 7 soniyalik byudjet bilan ishlaydi va qolgan eslatmalarni keyingi daqiqaga qoldiradi.
- Production’da kalitlar yo‘q bo‘lsa funksiya ataylab xato beradi (har deployda yangi kalit yaratilib, sessiyalar buzilmasligi uchun).

## Telefonga o‘rnatish

- **Android (Chrome):** saytni oching → menyu → “Ilovani o‘rnatish” (yoki Sozlamalar → “O‘rnatish”). Keyin Sozlamalar → Bildirishnomalar → “Yoqish”.
- **iPhone/iPad (iOS 16.4+):** faqat **Safari** → Ulashish → **“Bosh ekranga qo‘shish”**, so‘ng ilovani **Bosh ekrandagi belgidan** oching va shu yerdan bildirishnomani yoqing. Oddiy Safari tabida iOS push bermaydi.
- **Kompyuter (Chrome/Edge):** manzil qatoridagi o‘rnatish belgisi.

## Ovozli signal haqida (brauzer cheklovi)

- Sayt **yopiq** yoki fonda bo‘lsa: ovozni **qurilma/OT bildirishnoma ovozi** chaladi. Brauzer o‘z audio faylimizni majburan ijro etishga ruxsat bermaydi. Telefonda “Bezovta qilmang”, ovoz va bildirishnoma kanali sozlamalarini tekshiring.
- Sayt **ochiq** bo‘lsa: tanlangan ohang (Klassik/Zang/Signal/Ohang) 3 marta chalinadi va ekranda “Bajarildi / 10 daqiqa keyin” banneri chiqadi.
- Push bildirishnomasida ham **“Bajarildi”** va **“10 daqiqa keyin”** tugmalari bor (Android/desktop Chrome).

## Xavfsizlik

- Parollar bcrypt bilan hash qilinadi; sessiya `httpOnly` + `SameSite=Lax` cookie’da (productionda `Secure`).
- Har bir API so‘rovi foydalanuvchi bo‘yicha filtrlanadi (`user_id`); boshqa foydalanuvchi ma‘lumotiga kirib bo‘lmaydi (testlangan).
- Barcha kirishlar `zod` bilan tekshiriladi; login/ro‘yxatdan o‘tishga so‘rovlar chegarasi; CSP, helmet.
- Avatar faqat `png/jpeg/webp` data-URL (≤400 KB) qabul qilinadi.

## Testlar

```bash
npm test
```

55 ta backend tekshiruvi: auth, ma‘lumotlar ajratilganligi, CRUD, push (sinov rejimida), takroriy xabar yo‘qligi, snooze, takrorlanish, vaqt zonasi o‘zgarishi, statistika, Netlify handler va bazadagi login cheklovi. Testlar xotiradagi haqiqiy Postgres (PGlite) bilan ishlaydi — Supabase talab qilinmaydi.

## Cheklovlar va keyingi qadamlar

- Frontend **build talab qilmaydigan** sof JavaScript (ES modullar) — React/TypeScript/Tailwind o‘rniga. Keyinchalik React’ga ko‘chirish mumkin (API tayyor).
- Email orqali parolni tiklash yo‘q (email xizmati kerak bo‘ladi).
- Push faqat qurilma internetga ulangan bo‘lsa yetib boradi.
- Lokal ishga tushirish: `npm start` (ichki Postgres `data/pg` papkasida). Lokalda ham Supabase’dan foydalanish uchun `.env` ga `DATABASE_URL` yozing.
