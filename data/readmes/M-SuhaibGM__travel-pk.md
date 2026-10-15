
# 🌍 Travel — Modern Tour Booking Platform

A full-stack, production-ready travel booking platform built with **Next.js 16**, **Prisma**, **TiDB Cloud**, **NextAuth v5**, and **Stripe**. Browse tours, book experiences, pay securely, and manage everything from a role-protected admin panel.

![Next.js](https://img.shields.io/badge/Next.js-16-black?logo=next.js)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?logo=typescript)
![Prisma](https://img.shields.io/badge/Prisma-7-2D3748?logo=prisma)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-v4-38B2AC?logo=tailwindcss)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ Features

### 🧭 Customer-Facing

- **Landing page** with auto-playing hero slider, search bar, and featured tours
- **Browse tours** with filters (destination, price range, duration) + pagination
- **Tour detail pages** with image gallery, itinerary, highlights, reviews, and a sticky booking sidebar
- **Wishlist** — save tours with a heart toggle
- **Reviews** — verified customer reviews with star ratings and breakdown bars
- **Booking flow** — embedded Stripe Payment Element (no redirect), 3D Secure ready
- **Confirmation emails** via Resend
- **User account** — profile, bookings, wishlist, settings, cancel booking with refund
- **Recommendations** — personalized "Recommended for you" based on recently viewed tours
- **Destinations** — browse all destinations by country
- **Dark mode** — light, dark, and system theme toggle
- **Multi-currency** — USD, EUR, GBP, PKR, AED, JPY with live conversion
- **Multi-country** — flag selector with auto currency switching

### 🛠️ Admin Panel

- **Role-protected** `/admin` area (only `ADMIN` users)
- **Dashboard** — revenue, bookings, tours, users, recent bookings, top tours
- **Tours CRUD** — create, edit, publish/unpublish, feature/unfeature, delete
- **Destinations CRUD** — manage all destinations
- **Bookings management** — filter by status, view details, issue refunds, resend confirmation emails
- **Reviews moderation** — hide or delete reviews
- **Users list** — see all users and their booking counts
- **Image uploads** — via UploadThing (drag-and-drop)
- **Collapsible sidebar** — cookie-persisted

### 🔒 Security

- **NextAuth v5** with Google + Apple OAuth
- **Role-based access control** (RBAC)
- **Middleware protection** at the edge for `/admin`, `/account`, `/book`
- **In-memory rate limiting** on auth and booking endpoints
- **TLS-encrypted** database connection (TiDB Cloud `sslaccept=strict`)
- **PCI-compliant** payments via Stripe Elements (card data never touches your server)

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| **Framework** | Next.js 16 (App Router, Turbopack) |
| **Language** | TypeScript 5 |
| **Database** | TiDB Cloud (MySQL-compatible) |
| **ORM** | Prisma 7 + `@prisma/adapter-mariadb` |
| **Auth** | NextAuth v5 (`next-auth@5.0.0-beta`) |
| **Payments** | Stripe Payment Intents + Elements |
| **Emails** | Resend + React Email |
| **File Uploads** | UploadThing |
| **UI** | Tailwind CSS v4 + shadcn/ui + Radix UI |
| **Icons** | Lucide + Simple Icons + Country Flag Icons |
| **Notifications** | Sonner |
| **Fonts** | Aeonik (self-hosted) |

---

## 📦 Prerequisites

Before you begin, make sure you have:

- **Node.js** 20+ (recommended: 22+)
- **npm** or **pnpm**
- A **TiDB Cloud** account ([sign up free](https://tidbcloud.com))
- A **Stripe** account ([sign up free](https://stripe.com))
- A **Resend** account ([sign up free](https://resend.com))
- A **Google Cloud** project (for OAuth)
- An **UploadThing** account ([sign up free](https://uploadthing.com))
- (Optional) An **Apple Developer** account for Sign in with Apple

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/travel-pk.git
cd travel-pk
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Set Up Environment Variables

Create `.env` at the project root:

```env
# ==========================================
# DATABASE (TiDB Cloud)
# ==========================================
DATABASE_URL="mysql://user:password@gateway01.region.prod.aws.tidbcloud.com:4000/travel-db?sslaccept=strict"

# Individual values (used by the MariaDB adapter)
DATABASE_HOST="gateway01.region.prod.aws.tidbcloud.com"
DATABASE_PORT="4000"
DATABASE_USER="your-user.root"
DATABASE_PASSWORD="your-password"
DATABASE_NAME="travel-db"

# ==========================================
# AUTH
# ==========================================
AUTH_SECRET="generate-with-openssl-rand-base64-32"
AUTH_URL="http://localhost:3000"
NEXTAUTH_URL="http://localhost:3000"

# Google OAuth
GOOGLE_CLIENT_ID="xxx.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET="GOCSPX-xxxxx"

# Apple OAuth (optional)
APPLE_CLIENT_ID="com.yourdomain.travel"
APPLE_CLIENT_SECRET="eyJhbGciOi..."
APPLE_TEAM_ID="XXXXXXXXXX"
APPLE_KEY_ID="XXXXXXXXXX"
APPLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----"

# ==========================================
# STRIPE
# ==========================================
STRIPE_SECRET_KEY="sk_test_..."
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY="pk_test_..."

# ==========================================
# RESEND
# ==========================================
RESEND_API_KEY="re_..."
EMAIL_FROM="Travel <onboarding@resend.dev>"

# ==========================================
# UPLOADTHING
# ==========================================
UPLOADTHING_TOKEN="eyJhcGlLZXkiOiJ..."

# ==========================================
# APP
# ==========================================
NEXT_PUBLIC_APP_URL="http://localhost:3000"
```

Generate `AUTH_SECRET`:
```bash
openssl rand -base64 32
```

### 4. Set Up the Database

```bash
# Push schema to TiDB Cloud
npx prisma generate
npx prisma db push

# Seed 12 destinations + 30 tours
npm run db:seed
```

### 5. Run the Dev Server

```bash
npm run dev
```

Visit **http://localhost:3000** 🎉

### 6. Make Yourself an Admin

After signing in with Google, run this SQL in your TiDB Cloud SQL Editor:

```sql
UPDATE User SET role = 'ADMIN' WHERE email = 'your-email@gmail.com';
```

Sign out and back in. You'll now see **Admin Dashboard** in your navbar dropdown.

---

## 📁 Project Structure

```
travel-pk/
├── app/
│   ├── (public)/
│   │   ├── page.tsx                    # Landing page
│   │   ├── tours/                      # Tour listing + detail
│   │   ├── destinations/               # Destinations grid
│   │   └── login/                      # OAuth login
│   ├── (protected)/
│   │   ├── book/                       # Booking + payment + success
│   │   ├── account/                    # Profile, bookings, wishlist, settings
│   │   └── admin/                      # Admin dashboard + CRUD
│   ├── api/
│   │   ├── auth/                       # NextAuth routes
│   │   ├── bookings/                   # Create intent, confirm, cancel, refund
│   │   ├── reviews/                    # Submit, edit, delete
│   │   ├── wishlist/                   # Add, remove
│   │   ├── uploadthing/                # File router
│   │   └── admin/                      # Admin mutations
│   ├── error.tsx                       # Error boundary
│   ├── not-found.tsx                   # Custom 404
│   ├── loading.tsx                     # Root loading
│   └── layout.tsx                      # Root layout + providers
├── components/
│   ├── ui/                             # shadcn components
│   ├── admin/                          # Admin-specific components
│   ├── reviews/                        # Review components
│   ├── navbar.tsx                      # Main navbar
│   ├── footer.tsx                      # Footer
│   ├── hero-slider.tsx                 # Auto-playing hero slider
│   ├── wishlist-button.tsx             # Heart toggle
│   ├── star-rating.tsx                 # Star rating
│   └── theme-toggle.tsx                # Dark mode toggle
├── lib/
│   ├── auth.ts                         # NextAuth config
│   ├── db.ts                           # Prisma client
│   ├── stripe.ts                       # Stripe server SDK
│   ├── stripe/client.ts                # Stripe.js loader
│   ├── resend.ts                       # Resend client
│   ├── uploadthing.ts                  # UploadThing helpers
│   ├── currency.ts                     # Currency config
│   ├── countries.ts                    # Country config
│   ├── rate-limit.ts                   # Rate limiter
│   └── utils.ts                        # Tailwind cn helper
├── emails/
│   └── booking-confirmation.tsx        # Email template
├── prisma/
│   ├── schema.prisma                   # Database schema
│   └── seed.ts                         # Seed script
├── public/
│   └── fonts/                          # Aeonik woff2 files
├── .env                                # Environment variables (gitignored)
├── .env.example                        # Example template
├── next.config.ts                      # Next.js config
├── prisma.config.ts                    # Prisma 7 config
└── package.json
```

---

## 🗄️ Database Schema

| Model | Purpose |
|---|---|
| `User` | Accounts with role (USER / ADMIN) and preferences |
| `Account`, `Session`, `VerificationToken` | NextAuth v5 tables |
| `Authenticator` | WebAuthn support |
| `Destination` | Countries / cities with images |
| `Tour` | Tours with pricing, itinerary, images, highlights |
| `Booking` | Customer bookings with status + payment info |
| `Wishlist` | Saved tours per user |
| `Review` | Verified customer reviews (1 per completed booking) |

View the schema in `prisma/schema.prisma`.

---

## 🧪 Available Scripts

| Command | What It Does |
|---|---|
| `npm run dev` | Start dev server (Turbopack) |
| `npm run build` | Production build |
| `npm run start` | Start production server |
| `npm run lint` | Run ESLint |
| `npm run db:seed` | Seed destinations + tours |
| `npx prisma studio` | Launch Prisma Studio (data GUI) |
| `npx prisma generate` | Regenerate Prisma client |
| `npx prisma db push` | Push schema changes to DB |
| `npx prisma migrate dev` | Create a migration |

---

## 🔑 Key Environment Variables Reference

| Variable | Where to Get It |
|---|---|
| `DATABASE_URL` | TiDB Cloud → Cluster → Connect → Prisma |
| `GOOGLE_CLIENT_ID` / `SECRET` | [Google Cloud Console](https://console.cloud.google.com) → APIs & Services → Credentials |
| `STRIPE_SECRET_KEY` | [Stripe Dashboard → API Keys](https://dashboard.stripe.com/test/apikeys) |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | Same page — the "Publishable key" |
| `RESEND_API_KEY` | [Resend → API Keys](https://resend.com/api-keys) |
| `UPLOADTHING_TOKEN` | [UploadThing Dashboard](https://uploadthing.com/dashboard) → API Keys |

---

## 💳 Stripe Test Cards

| Card Number | Behavior |
|---|---|
| `4242 4242 4242 4242` | ✅ Success |
| `4000 0000 0000 0002` | ❌ Card declined |
| `4000 0025 0000 3155` | 🔐 3D Secure required |
| `4000 0000 0000 9995` | ❌ Insufficient funds |

Any future expiry, any 3-digit CVC, any ZIP.

---

## 🚢 Deployment

### Deploy to Vercel

1. **Push to GitHub**
2. **Import to Vercel** at [vercel.com/new](https://vercel.com/new)
3. **Add environment variables** (see reference above)
   - **Secrets** (`DATABASE_URL`, `STRIPE_SECRET_KEY`, `AUTH_SECRET`, `RESEND_API_KEY`, `UPLOADTHING_TOKEN`) → type: **Secret**
   - **Public** (`NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`, `NEXT_PUBLIC_APP_URL`) → type: **Config**
4. **Deploy**

### Post-Deploy

1. Update `AUTH_URL` and `NEXTAUTH_URL` to your Vercel domain
2. Add Vercel domain to **Google OAuth** redirect URIs: `https://yourdomain.vercel.app/api/auth/callback/google`
3. Configure **Stripe webhooks** at `https://yourdomain.vercel.app/api/webhooks/stripe`
4. Verify your **Resend domain** for production emails
5. Promote yourself to admin in the production DB

---

## 🐛 Troubleshooting

### `ECONNREFUSED 127.0.0.1:4000`

Your adapter isn't reading the DB host. Verify `lib/db.ts` parses `DATABASE_URL` correctly.

### `PrismaClientConstructorValidationError`

You removed the adapter but didn't remove `previewFeatures = ["driverAdapters"]` from `schema.prisma`. Do both.

### Prisma Studio stream errors

Known bug with Node.js 22+. Workaround:
```bash
CHECKPOINT_DISABLE=1 npx prisma studio
```

### `getaddrinfo EAI_AGAIN http-undefined`

Your TiDB adapter isn't loaded correctly. Switch to `@prisma/adapter-mariadb` with a parsed `DATABASE_URL`.

### Emails not sending

Check that `.env` has `RESEND_API_KEY` and `EMAIL_FROM`. With `onboarding@resend.dev`, you can only send to the email you signed up to Resend with.

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- [Next.js](https://nextjs.org) — the framework
- [Prisma](https://prisma.io) — the ORM
- [TiDB Cloud](https://tidbcloud.com) — the database
- [Stripe](https://stripe.com) — the payments
- [Resend](https://resend.com) — the emails
- [UploadThing](https://uploadthing.com) — the file uploads
- [shadcn/ui](https://ui.shadcn.com) — the UI components
- [Lucide](https://lucide.dev) — the icons
- [Unsplash](https://unsplash.com) — the images

---

## 📬 Contact

**Muhammad Suhaib** — [@m-suhaibgm](https://github.com/m-suhaibgm)

Project link: [https://github.com/yourusername/travel-pk](https://github.com/yourusername/travel-pk)

---

**⭐ If you find this project useful, please star it on GitHub!**
```

---

## 📋 How to Use This README

1. **Save it** as `README.md` at the **project root** (next to `package.json`)
2. **Replace placeholders**:
   - `yourusername` → your GitHub username
   - `your-email@gmail.com` → your email
   - `yourdomain.vercel.app` → your Vercel domain
   - Contact section → your actual info
3. **Add a LICENSE file** (MIT is fine — 1-minute setup on GitHub)
4. **Add screenshots** later in a `## Screenshots` section — recruiters and users love them

## 🎁 Bonus — Screenshots Section

Add this after the "Features" section once you have screenshots:

```markdown
## 📸 Screenshots

### Landing Page
![Landing](docs/screenshots/landing.png)

### Tour Detail
![Tour detail](docs/screenshots/tour-detail.png)

### Admin Dashboard
![Admin](docs/screenshots/admin-dashboard.png)

### Booking Flow
![Booking](docs/screenshots/booking.png)
```

Then create a `docs/screenshots/` folder and drop PNG files in.
