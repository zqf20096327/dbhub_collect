# API CALL APPLICATION (ACA) - Laravel 10.x + Blade

A clean, modern UI for managing and executing OpenAI prompt calls.

Features
- Admin login and password change
- API CALL Master maintenance (list, create, update)
- Execute screen (select prompt, edit original/result textareas)
- History CSV download (by prompt and date range; only prompts with history ON)
- External API endpoint for ACA calls with IP authorization and error codes
- Tailwind CSS + Vite for styling
- Well-structured, maintainable code

Requirements
- PHP 8.1+
- Composer
- Node.js 18+
- MySQL/PostgreSQL/SQLite (configure in .env)

Quick Start
1) Create a fresh Laravel 10 app (recommended)
   composer create-project laravel/laravel aca
   cd aca

2) Copy the files from this download into your Laravel app root,
   merging folders (app, routes, database, resources, config, etc.).
   - If prompted to overwrite routes, views, or config, choose overwrite.
   - If you already have config/services.php, manually add the "openai" block from this project’s config/services.php into yours.

3) Install PHP deps and generate key
   composer install
   php artisan key:generate

4) Configure .env
   - Set DB connection
   - Add defaults for OpenAI:
     OPENAI_API_KEY_DEFAULT=sk-xxxx
     OPENAI_ORG_ID_DEFAULT=org_xxxx

5) Migrate and seed
   php artisan migrate --seed
   # Seeded admin:
   # email: admin@example.com
   # pass : admin1234

6) Frontend (Tailwind + Vite)
   npm install
   npm run dev
   # for production: npm run build

7) Run
   php artisan serve

URLs
- Admin login: /admin/login
- API master: /admin/prompts
- Execute: /admin/run
- History download: /admin/history
- Admin password: /admin/password
- External API: POST /api/aca/call  { "id": <prompt_id>, "text": "原文..." }

Notes
- List masks sensitive keys; update screen reveals them.
- Prompt text shows only the first 20 chars in the list.
- If a prompt lacks API key/ID and “デフォルト使用” is ON, it uses .env defaults.
- IP allow list: comma-separated; empty means no restriction.
- Error codes: 0 (OK), 9 (Error).

Production Hardening (optional)
- Add rate limiting to /api/aca/call
- Use Laravel guards/policies for multi-admin
- Support CIDR IP ranges
- Enable soft deletes on prompts/histories
