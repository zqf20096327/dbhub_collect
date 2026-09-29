# תקוותנו | Tikvatenu

<div align="center">

**צעירים למען עתיד ישראל**

*Youth for the Future of Israel*

---

[עברית](#עברית) | [English](#english)

</div>

## עברית

### התקדמות הפיתוח

| שלב | סטטוס | תיאור |
|------|--------|-------|
| שלב 0: תיעוד | **הושלם** | plan.md + README.md |
| שלב 1: תשתית | **הושלם** | Next.js 15, i18n, לקוחות Supabase, ניווט, כל דפי השלד |
| שלב 2: בסיס נתונים והרשאות | **הושלם** | כל הטבלאות, RLS, אחסון, כניסת אדמין + דשבורד |
| שלב 3: מערכת אירועים | **הושלם** | CRUD אירועים, טפסי הרשמה, ניהול, ייצוא CSV |
| שלב 4: מגזין | **הושלם** | מאמרים עם תגיות, דפי מגזין ציבוריים |
| שלב 5: עמוד בית | **הושלם** | הירו, פיד, אינסטגרם, מאמר מומלץ |
| שלב 6: גלריה ואירועי עבר | **הושלם** | אלבומי תמונות, lightbox |
| שלב 7: אודות + הצטרפות + ליטוש | **הושלם** | דפי תוכן, טפסים, SEO, מייל אישור |
| שלב 8: הפצה | ממתין | Vercel, tikvatenu.com |

**עדכון אחרון**: 11.03.2026

### אודות הפרויקט

**תקוותנו** היא יוזמה של צעירים ציונים שרוצים להשפיע על החברה הישראלית דרך בניית גשרים בין קבוצות שונות. אנחנו מאמינים בשיח ישיר, מפגשים והיכרות כדרך להתמודד עם הקיטוב בחברה הישראלית.

האתר הזה הוא הבית הדיגיטלי של היוזמה - מקום מרכזי לניהול אירועים, פרסום תכנים, ויצירת קשר עם הקהילה.

### תכונות עיקריות

- **מערכת אירועים** - יצירת אירועים, הרשמה דינמית, ניהול משתתפים
- **מגזין רוח ותוכן** - מאמרי הגות, רוח, וכתבות עיתונאיות
- **פיד תוכן** - עמוד בית דינמי עם עדכונים שוטפים
- **גלריה** - אלבומי תמונות מאירועים
- **פאנל ניהול** - ממשק ידידותי לעורכים לא-טכנולוגיים
- **דו-לשוני** - עברית (RTL) ואנגלית (LTR) בלחיצת כפתור

### טכנולוגיות

| שכבה | טכנולוגיה |
|------|-----------|
| פריימוורק | Next.js 15 (App Router) |
| שפה | TypeScript |
| עיצוב | Tailwind CSS v4 |
| קומפוננטות | shadcn/ui (Radix) |
| בינלאומי | next-intl |
| בסיס נתונים | Supabase (PostgreSQL) |
| אחסון | Supabase Storage |
| עורך טקסט | Tiptap |
| אירוח | Vercel |

### דרישות מקדימות

- Node.js 18+
- npm או yarn
- חשבון [Supabase](https://supabase.com) (חינמי)
- חשבון [Vercel](https://vercel.com) (חינמי)

### התקנה

```bash
# שכפול הפרויקט
git clone https://github.com/YOUR_USERNAME/tikvatenu.git
cd tikvatenu

# התקנת תלויות
npm install

# הגדרת משתני סביבה
cp .env.example .env.local
# ערוך את .env.local עם מפתחות Supabase שלך

# הרצת שרת פיתוח
npm run dev
```

### משתני סביבה

צור קובץ `.env.local` עם המשתנים הבאים:

```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
RESEND_API_KEY=your_resend_api_key
```

### מבנה הפרויקט

```
tikvatenu/
├── src/
│   ├── app/[locale]/          # דפי האפליקציה (ציבוריים + אדמין)
│   ├── components/            # קומפוננטות React
│   │   ├── ui/               # קומפוננטות בסיס (shadcn/ui)
│   │   ├── layout/           # Header, Footer, ניווט
│   │   ├── home/             # קומפוננטות עמוד בית
│   │   ├── events/           # קומפוננטות אירועים
│   │   ├── magazine/         # קומפוננטות מגזין
│   │   ├── gallery/          # קומפוננטות גלריה
│   │   └── admin/            # קומפוננטות פאנל ניהול
│   ├── i18n/                 # הגדרות בינלאומיות
│   ├── messages/             # קבצי תרגום (he.json, en.json)
│   └── lib/                  # שירותים ועזרים
├── supabase/migrations/       # מיגרציות בסיס נתונים
└── public/                    # קבצים סטטיים
```

### ניווט באתר

```
[בית] [אודות] [אירועים] [רוח ותוכן] [הצטרפות]
```

5 פריטי ניווט בלבד - ברור ופשוט, ללא עומס קוגניטיבי.

---

## English

### Development Progress

| Phase | Status | Description |
|-------|--------|-------------|
| Phase 0: Documentation | **Complete** | plan.md + README.md |
| Phase 1: Foundation | **Complete** | Next.js 15, i18n, Supabase clients, navigation, all page stubs |
| Phase 2: Database & Admin Auth | **Complete** | All tables, RLS, storage, admin login + dashboard |
| Phase 3: Events System | **Complete** | Event CRUD, registration forms, management, CSV export |
| Phase 4: Magazine | **Complete** | Articles with tags, public magazine pages |
| Phase 5: Home Page & Feed | **Complete** | Hero, feed, Instagram, featured article |
| Phase 6: Gallery & Past Events | **Complete** | Photo albums, lightbox |
| Phase 7: About + Join Us + Polish | **Complete** | Content pages, forms, SEO, confirmation emails |
| Phase 8: Deployment | Pending | Vercel, tikvatenu.com domain |

**Last updated**: 2026-03-11

### About

**Tikvatenu** is a Zionist youth initiative dedicated to building bridges within Israeli society. We believe in direct dialogue, face-to-face encounters, and mutual understanding as the path to addressing polarization in Israeli society.

This website serves as the digital home for the initiative - a central hub for managing events, publishing content, and connecting with the community.

### Features

- **Event System** - Create events, dynamic registration forms, participant management
- **Magazine** - Thought pieces, spirit, and press articles
- **Content Feed** - Dynamic home page with live updates
- **Gallery** - Photo albums from events
- **Admin Panel** - User-friendly interface for non-technical editors
- **Bilingual** - Hebrew (RTL) and English (LTR) with one-click switching

### Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Next.js 15 (App Router) |
| Language | TypeScript |
| Styling | Tailwind CSS v4 |
| UI Components | shadcn/ui (Radix) |
| i18n | next-intl |
| Database | Supabase (PostgreSQL) |
| Storage | Supabase Storage |
| Rich Text | Tiptap |
| Hosting | Vercel |

### Prerequisites

- Node.js 18+
- npm or yarn
- [Supabase](https://supabase.com) account (free tier)
- [Vercel](https://vercel.com) account (free tier)

### Getting Started

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/tikvatenu.git
cd tikvatenu

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your Supabase keys

# Run development server
npm run dev
```

### Environment Variables

Create a `.env.local` file with:

```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
RESEND_API_KEY=your_resend_api_key
```

### Project Structure

```
tikvatenu/
├── src/
│   ├── app/[locale]/          # App pages (public + admin)
│   ├── components/            # React components
│   │   ├── ui/               # Base components (shadcn/ui)
│   │   ├── layout/           # Header, Footer, Navigation
│   │   ├── home/             # Home page components
│   │   ├── events/           # Event components
│   │   ├── magazine/         # Magazine components
│   │   ├── gallery/          # Gallery components
│   │   └── admin/            # Admin panel components
│   ├── i18n/                 # Internationalization config
│   ├── messages/             # Translation files (he.json, en.json)
│   └── lib/                  # Services and utilities
├── supabase/migrations/       # Database migrations
└── public/                    # Static assets
```

### Navigation

```
[Home] [About] [Events] [Magazine] [Join Us]
```

Just 5 navigation items - clean and focused, no cognitive overload.

### Deployment

The site is deployed on Vercel with automatic deployments from the main branch.

**Domain**: [tikvatenu.com](https://tikvatenu.com)

---

<div align="center">

**Built with hope for a shared future.**

*נבנה מתוך תקווה לעתיד משותף.*

</div>
