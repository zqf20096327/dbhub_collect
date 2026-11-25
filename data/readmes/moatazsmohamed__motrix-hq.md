<p dir="rtl">

# MOTRIX HQ — المقر الافتراضي الرسمي

**منصة ويب تفاعلية كاملة تحاكي المقر الرئيسي لشركة MOTRIX (استوديو ذكاء اصطناعي وبرمجيات — الإسكندرية، مصر)** — أحد عشر مستوى مُنفَّذًا ومُختبَرًا: من المدخل الزجاجي والطوابق التفاعلية، مرورًا بموظفي AI ووكلائهم الأذكياء، اجتماعات حيّة، نظام إداري بموافقات، مكاتب حية، غرفة تحكم CEO، محرك عمليات شبه مستقل، وحتى «MOTRIX AI Corporation» الكاملة (دماغ الشركة بالتوثيق، تحليلات مُشتقة من قاعدة البيانات، خط تسليم، ومحرك استراتيجي ببوابة CEO البشرية).

**قفل الهوية مُطبَّق حرفيًا:** أسود #080B10 · جرافيت #111720 · أزرق كهربائي #087BFF · سماوي #00CFFF · فضي #C5CED8 · زجاج وإضاءة LED والشعار الأصلي فقط — **MOTRIX — WE BUILD WHAT'S NEXT.**

> **صدقية البيانات:** كل رقم يُشتق لحظة الطلب من الجداول الفعلية؛ البيانات التجريبية موسومة «ديمو» دائمًا؛ وحين يرفض مزوّد النماذج يعرض النظام بدائل صادقة (وقائع مباشرة/قوالب موسومة) بدل اختلاق أي نشاط.

## المكدس التقني
React 19 · Vite 7 · Tailwind v4 · wouter · tRPC v11 + superjson · Drizzle ORM (MySQL/TiDB) · zod · Express · TypeScript. قاعدة بيانات واحدة (32 جدولًا) تُغذي كل الواجهات وكل الاختبارات.

## التشغيل
```bash
pnpm install
pnpm dev            # تطوير (Vite + tsx) على PORT=3000
pnpm build && pnpm start   # إنتاج: SPA ثابت + node dist/index.js
pnpm check          # الأنواع (tsc)
```
المتغيرات البيئية للمنصة: `DATABASE_URL` (TiDB)، وقيم OAuth/الجلسات التي توفرها بيئة التشغيل لديك (`MANUS_JWT_SECRET`، `MANUS_OAUTH_API_URL`، `MANUS_PROJECT_ID`…).

## النشر على Vercel
الريبو جاهز **serverless** بالكامل:
- `api/index.ts` — يبني نفس تطبيق Express (بلا listen) ويدالة كـ catch-all function.
- `vercel.json` — يبني العميل (`build:static`)، يغلّف الدالة بـ `@vercel/node` مع إرفاق الأصول الثابتة (`includeFiles: dist/public/**` + `STATIC_DIR`)، memory 1024 / maxDuration 60.
- في مشروعك على Vercel: **Import** من هذا الريبو ← ثم Settings → Environment Variables أضف قيم `DATABASE_URL` و`MANUS_JWT_SECRET` و`MANUS_OAUTH_API_URL` و`MANUS_PROJECT_ID` (من مزوّد تشغيلك) ← Deploy.
- **ملاحظات صادقة:** التسجيل يعتمد على OAuth الخاص بمنصتك (اسمح نطاق Vercel لديه)؛ أول طلب بعد كل cold start يستغرق 10–25 ثانية لتجمع حوض TiDB؛ المحرك الذاتي يدور فقط إذا فعّله CEO (خامل افتراضيًا).
</p>

# MOTRIX HQ — The Official Virtual Headquarters

A fully interactive web simulation of MOTRIX's real-world AI studio HQ (Alexandria, Egypt), built in 11 verified levels: immersive brand-locked floors, AI employees & agents with real memory, live meetings, an approval-gated org chart, living offices, a CEO command center, a semi-autonomous operations engine (dry-run first, hard caps, auto-suspend), and the complete **MOTRIX AI Corporation** (permission-scoped company brain with citations, analytics derived from live tables, customer delivery pipeline, strategy engine with a human CEO gate).

Every number is derived from the database at request time; demo records are always labeled; when the model provider is unavailable the UI shows honest direct-fact fallbacks instead of fabricated activity.

**Stack:** React 19 / Vite 7 / Tailwind v4 / tRPC v11 + superjson / Drizzle (MySQL·TiDB) / Express / TypeScript — one 32-table database behind every surface.

**Vercel:** repo is serverless-ready (`api/index.ts` + `vercel.json`); import, add your provider's env secrets (`DATABASE_URL`, `MANUS_JWT_SECRET`, `MANUS_OAUTH_API_URL`, `MANUS_PROJECT_ID`), deploy. First requests after cold starts take ~10–25s (TiDB pool warm-up); OAuth login requires allowing your Vercel domain at the identity provider.

**Brand Lock:** #080B10 · #111720 · #087BFF · #00CFFF · #C5CED8 — black surfaces, glass walls, electric-blue LED, cyan details, silver metal, the original MOTRIX logo only.

**MOTRIX — WE BUILD WHAT'S NEXT.**
