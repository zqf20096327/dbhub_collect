<div dir="rtl">

<div align="center">

# Penny

**אפליקציית כסף רגועה למשקי בית בישראל, שרצה אצלכם במחשב.**
הבנקים, התקציב והעתיד שלכם במקום אחד, בלי שהנתונים יוצאים מהבית.

[![Downloads](https://img.shields.io/github/downloads/Sergey-Bar/Penny/total?style=flat-square&color=2ea44f&label=downloads)](https://github.com/Sergey-Bar/Penny/releases)
[![Release](https://img.shields.io/github/v/release/Sergey-Bar/Penny?style=flat-square&color=5541cc)](https://github.com/Sergey-Bar/Penny/releases/latest)
[![CI](https://img.shields.io/github/actions/workflow/status/Sergey-Bar/Penny/ci.yml?branch=main&style=flat-square&label=tests)](https://github.com/Sergey-Bar/Penny/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

[אתר](https://sergey-bar.github.io/Penny/) · [דמו לחיץ](https://sergey-bar.github.io/Penny/demo/) · [דמו חי](https://penny-finance-demo.vercel.app) · [הורדה](https://github.com/Sergey-Bar/Penny/releases/latest) · [English](README.en.md)

![לוח הבקרה של Penny עם משק בית לדוגמה](website/demo/he/home.webp)

</div>

התנועות נמשכות ישירות מהבנקים ומחברות האשראי בישראל, נשמרות בקובץ SQLite אחד אצלכם במחשב, והאפליקציה עוזרת בשאלות שבאמת חשובות כאן: האם אני עומד בתקציב החודש, האם יש לי כרית ביטחון, האם אני משלם יותר מדי דמי ניהול, והאם אני מקבל את כל הטבות המס שמגיעות לי. היא מאזינה רק ל-127.0.0.1, מצפינה את פרטי ההתחברות לבנק ב-AES-256-GCM, ולא פונה לשום מקום חוץ מהבנק, ומספק AI אם בחרתם כזה. עברית קודם כול, עם ממשק מלא גם באנגלית.

> [!WARNING]
> זה כלי אישי שרץ רק על המחשב שלכם. משיכת נתונים אוטומטית מבנקים עלולה להפר את תנאי השימוש שלהם. השתמשו בו רק לחשבונות שלכם ועל המחשב שלכם. **אל תפעילו אותו כשירות באינטרנט.**

## יכולות

- **18 בנקים וחברות אשראי בישראל** בסנכרון יומי, וגם ייבוא דוחות CSV/XLSX וגיליון חכם שמקבל כל טבלה
- **פנסיה וחסכונות** מכלל, הראל, מיטב, מנורה ומגדל, או מהדוח של הסוכן
- **תקציבים, תחזית תזרים ו"כסף על השולחן"**: סכום שנתי אחד לעמלות, כסף שיושב בעו"ש והטבות מס שמגיעות לכם
- **יותר מ-25 מחשבונים ישראליים**: נקודות זיכוי והחזר מס, דמי ניהול בפנסיה, משכנתא, שכירות או קנייה ועוד
- **בוט טלגרם**: משוב על הוצאות, קוד חד-פעמי מהבנק בזמן סנכרון, התראות סנכרון וסיכום שלוש פעמים בשבוע
- **סיווג חכם גם בלי AI**, או עם Claude, מודל Ollama מקומי או סוכן CLI שכבר מותקן אצלכם
- **פרופילים למשק הבית**, גישה מהטלפון ברשת הביתית (בהפעלה מפורשת), נעילת אפליקציה, גיבויים מוצפנים ו[שרת MCP](docs/mcp.md) לסוכני AI

הרשימה המלאה (באנגלית): [docs/features.md](docs/features.md).

## התקנה

**אפליקציה לשולחן העבודה (Windows, macOS):** מורידים את המתקין מ[הגרסה האחרונה](https://github.com/Sergey-Bar/Penny/releases/latest). ב-Windows היא מתעדכנת לבד.

**Docker (Windows, Mac, לינוקס):** מתקינים [Docker Desktop](https://www.docker.com/products/docker-desktop/), ואז:

<div dir="ltr">

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/Sergey-Bar/Penny/main/install-docker.sh | bash
```

```powershell
# Windows (PowerShell)
irm https://raw.githubusercontent.com/Sergey-Bar/Penny/main/install-docker.ps1 | iex
```

</div>

הפקודה מורידה את הגרסה האחרונה לתיקייה `~/Penny`, בונה אותה ופותחת את **http://127.0.0.1:41234**. הנתונים נשמרים ב-volume של Docker בשם `penny-data`.

**עדכון:** מריצים שוב את אותה פקודה. היא מגבה את הנתונים, בונה את הגרסה החדשה (כולל הבדיקות) וחוזרת לגרסה הקודמת אם משהו נכשל.

התקנה מקוד המקור, אפשרויות נוספות ופתרון בעיות: [docs/install.md](docs/install.md). ייבוא קבצי דוחות ודוח פנסיה: [docs/importing.md](docs/importing.md).

## עוד מידע

ב[אתר](https://sergey-bar.github.io/Penny/) יש סיור ביכולות, מדריכים ודמו לחיץ. אבטחה: [SECURITY.md](SECURITY.md) ו-[docs/security.md](docs/security.md). מה השתנה: [CHANGELOG.md](CHANGELOG.md).

## תרומה לפרויקט

בקשות משיכה מתקבלות בשמחה, במיוחד בנקים חדשים, ספקי AI ונתוני מס ישראליים עם מקור רשמי. הכנת סביבה, כללים ומפת קוד: [CONTRIBUTING.md](CONTRIBUTING.md). על פרצת אבטחה מדווחים בפרטיות לפי [SECURITY.md](SECURITY.md).

## רישיון

MIT. ראו [LICENSE](LICENSE) ו-[NOTICE.md](NOTICE.md) לייחוס לפרויקטים שעליהם זה נבנה.

נבנה על [`israeli-bank-scrapers`](https://github.com/eshaham/israeli-bank-scrapers),‏ [Next.js](https://nextjs.org/),‏ [React](https://react.dev/),‏ [`shadcn/ui`](https://ui.shadcn.com/) על [`base-ui`](https://base-ui.com/),‏ [`better-sqlite3`](https://github.com/WiseLibs/better-sqlite3),‏ [`next-intl`](https://next-intl.dev/),‏ [BoopFace](https://github.com/CX-ArtLab/BoopFace) של CX ArtLab ‏(MIT, הפנים של פיפ), [Anthropic Claude](https://www.anthropic.com/) ו-[Ollama](https://ollama.com/).

</div>
