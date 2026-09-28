# 📕 کتاب جامع Redis — آموزش کامل فارسی

<div dir="rtl">

کتاب آنلاین رایگان فارسی **Redis** با ۲۵ فصل جامع، ۱۲۰+ دستور، ۲۰+ نمودار و Cheat Sheet کامل. از مبانی تا موضوعات پیشرفته: Streams، Cluster، Sentinel، Lua Scripting، Caching Patterns، Modules و یکپارچه‌سازی با Python/Node.js.

## ✨ ویژگی‌ها

- 📚 **۲۵ فصل جامع** — از مقدمه تا Best Practices
- 🎨 **طراحی تیره مدرن** — الهام‌گرفته از Catppuccin Mocha
- 📱 **کاملاً واکنش‌گرا** — موبایل، تبلت، دسکتاپ
- 🔍 **جستجوی آنی** — با میانبر `Ctrl+K` / `Cmd+K`
- 📊 **۲۰+ نمودار Mermaid** — معماری، flowchart، sequence diagram
- 💻 **Syntax Highlighting** — برای Bash، Python، JavaScript، Lua، YAML، JSON، SQL و...
- 📋 **دکمه کپی کد** — روی هر بلوک کد
- ⌨️ **پیمایش با کیبورد** — با کلیدهای جهت‌نما
- 🖨️ **پشتیبانی از چاپ** — تبدیل خودکار به سبک سیاه‌سفید برای PDF
- 🔌 **۱۰۰٪ آفلاین** — هیچ درخواست خارجی ندارد (تمام فونت‌ها و کتابخانه‌ها لوکال هستند)
- ⚡ **سبک و سریع** — بدون فریم‌ورک، فقط vanilla JS

## 📖 فهرست فصل‌ها

1. مقدمه و تاریخچه Redis
2. نصب و راه‌اندازی
3. شروع با redis-cli
4. ساختار داده‌ها و Keyspace
5. String (رشته)
6. List (لیست)
7. Hash (هش)
8. Set (مجموعه)
9. Sorted Set (مجموعه مرتب)
10. Bitmap و Bitfield
11. HyperLogLog
12. Stream (جریان داده)
13. Pub/Sub (انتشار/اشتراک)
14. تراکنش‌ها و Pipeline
15. کلیدها، TTL و Eviction
16. الگوهای Caching
17. Lua Scripting
18. امنیت و ACL
19. پایداری داده (RDB و AOF)
20. Replication و Sentinel
21. Redis Cluster
22. ماژول‌های Redis
23. مانیتورینگ و Performance
24. Docker و Kubernetes
25. Python/Node و Best Practices
- **واژه‌نامه** — مرجع کامل اصطلاحات

## 🚀 استفاده

### مشاهده آنلاین

کتاب به‌صورت آنلاین در GitHub Pages در دسترس است:

🌐 [https://a-talebifard.github.io/redis-book/](https://a-talebifard.github.io/redis-book/)


### استفاده محلی (Local)

برای مشاهده‌ی کتاب روی سیستم خودتان:

```bash
# کلون کردن ریپازیتوری
git clone https://github.com/A-talebifard/redis-book.git
cd redis-book

# روش ۱: با Python
python3 -m http.server 8000

# روش ۲: با Node.js
npx serve

# روش ۳: با PHP
php -S localhost:8000

# روش ۴: فقط فایل index.html را در مرورگر باز کنید
# (همه‌چیز آفلاین کار می‌کند)
```

سپس به آدرس `http://localhost:8000` در مرورگر بروید.

### با Docker

```bash
docker run -d \
    --name redis-book \
    -p 8000:80 \
    -v $(pwd):/usr/share/nginx/html \
    nginx:alpine
```

## 🎯 مخاطب

این کتاب برای:

- **توسعه‌دهندگان وب** که می‌خواهند از Redis به‌عنوان cache یا message queue استفاده کنند
- **مهندسان DevOps** که Redis را در production مدیریت می‌کنند
- **معماران سیستم** که برای High Availability و Scalability طراحی می‌کنند
- **دانشجویان** که می‌خواهند پایگاه‌های داده‌ی NoSQL را یاد بگیرند
- **هر کسی** که علاقه‌مند به یادگیری Redis از صفر تا پیشرفته است

## 🛠️ ساختار پروژه

```
redis-book/
├── index.html              # فایل اصلی کتاب (Single Page)
├── css/
│   ├── style.css           # استایل اصلی (Catppuccin Mocha)
│   └── atom-one-dark.min.css  # تم highlight.js
├── js/
│   ├── book.js             # منطق تعاملی (TOC, search, copy, ...)
│   ├── mermaid.min.js      # موتور نمودار
│   ├── highlight.min.js    # پشتیبانی اصلی syntax highlighting
│   ├── highlight-bash.min.js
│   ├── highlight-python.min.js
│   ├── highlight-javascript.min.js
│   ├── highlight-lua.min.js
│   ├── highlight-yaml.min.js
│   ├── highlight-json.min.js
│   ├── highlight-ini.min.js
│   ├── highlight-nginx.min.js
│   ├── highlight-sql.min.js
│   ├── highlight-dockerfile.min.js
│   ├── highlight-markdown.min.js
│   └── highlight-powershell.min.js
├── fonts/                  # فونت‌های لوکال (Vazirmatn, JetBrains Mono, Inter)
│   ├── Vazirmatn-*.ttf     # فونت فارسی
│   ├── JetBrainsMono-*.ttf # فونت کد
│   └── Inter-*.ttf         # فونت لاتین
└── img/
    └── avatar.jpg          # تصویر نویسنده
```

## ⌨️ میانبرهای کیبورد

| کلید | عملکرد |
|------|--------|
| `Ctrl+K` / `Cmd+K` | باز کردن جستجو |
| `Esc` | بستن جستجو |
| `→` | فصل بعدی |
| `←` | فصل قبلی |
| `Ctrl+P` | چاپ / ذخیره به‌عنوان PDF |

## 🎨 طراحی

این کتاب با الهام از:

- **پالت رنگی Catppuccin Mocha** برای ظاهر تیره‌ی چشم‌نواز
- **فونت Vazirmatn** برای متن فارسی
- **فونت JetBrains Mono** برای کد
- **فونت Inter** برای متن لاتین

طراحی شده است.

## 📝 مجوز

این پروژه تحت مجوز **MIT** منتشر شده است. برای جزئیات بیشتر فایل [LICENSE](LICENSE) را ببینید.

## 🤝 مشارکت

- اگر خطایی پیدا کردید یا پیشنهادی دارید، [Issue](https://github.com/A-talebifard/redis-book/issues) جدید باز کنید
- Pull Request‌ها welcome هستند
- اگر این کتاب برایتان مفید بود، یک ⭐ به ریپازیتوری بدهید

## 📞 ارتباط با نویسنده

- **GitHub:** [@A-talebifard](https://github.com/A-talebifard)
- **LinkedIn:** [abbastalebifard](https://www.linkedin.com/in/abbastalebifard/)

## 🙏 تشکر از

- **سالواتوره سانفیلیپو (antirez)** — خالق Redis
- **تیم Redis Inc.** — توسعه‌دهندگان فعلی
- **جامعه متن‌باز** — برای ابزارهای Mermaid، highlight.js و Catppuccin

---

© 1405 — A-Talebifard. تمام حقوق محفوظ است.

</div>

---

# 📕 Comprehensive Redis Book — Persian Edition

A free online Persian book about **Redis** with 25 comprehensive chapters, 120+ commands, 20+ diagrams, and a complete cheat sheet. From fundamentals to advanced topics: Streams, Cluster, Sentinel, Lua Scripting, Caching Patterns, Modules, and Python/Node.js integration.

## ✨ Features

- 📚 **25 comprehensive chapters** — from introduction to Best Practices
- 🎨 **Modern dark theme** — inspired by Catppuccin Mocha
- 📱 **Fully responsive** — mobile, tablet, desktop
- 🔍 **Instant search** — with `Ctrl+K` / `Cmd+K` shortcut
- 📊 **20+ Mermaid diagrams** — architecture, flowcharts, sequence diagrams
- 💻 **Syntax Highlighting** — for Bash, Python, JavaScript, Lua, YAML, JSON, SQL, etc.
- 📋 **Copy code button** — on every code block
- ⌨️ **Keyboard navigation** — with arrow keys
- 🖨️ **Print support** — automatic conversion to black-and-white for PDF
- 🔌 **100% offline** — no external requests (all fonts and libraries are local)
- ⚡ **Lightweight and fast** — no framework, just vanilla JS

## 🚀 Usage

### Online

The book is available online via GitHub Pages:

🌐 [https://a-talebifard.github.io/redis-book/](https://a-talebifard.github.io/redis-book/)

### Local

```bash
git clone https://github.com/A-talebifard/redis-book.git
cd redis-book
python3 -m http.server 8000
# Open http://localhost:8000
```

Or simply open `index.html` in your browser — everything works offline.

## 📝 License

MIT License — see [LICENSE](LICENSE) for details.

## 📞 Contact

- **GitHub:** [@A-talebifard](https://github.com/A-talebifard)
- **LinkedIn:** [abbastalebifard](https://www.linkedin.com/in/abbastalebifard/)

---

© 2026 — A-Talebifard. All rights reserved.
