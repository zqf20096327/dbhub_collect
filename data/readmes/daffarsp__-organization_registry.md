# Organization Registration System

Organization Registration System adalah aplikasi web untuk pendaftaran anggota organisasi. Project ini dibangun sebagai project pribadi/portfolio dengan fokus pada alur pendaftaran yang sederhana, panel admin yang rapi, keamanan konfigurasi, dan kesiapan deployment ke production.

## Status Project

Saat ini project berada pada Phase 1: Project Initialization.

Yang sudah tersedia:

- Laravel sudah terpasang.
- Struktur dasar Laravel sudah tersedia.
- Blade, Vite, dan Tailwind CSS sudah masuk sebagai fondasi frontend.
- Konfigurasi environment dasar sudah tersedia melalui `.env.example`.

Yang belum dibuat dan akan dikerjakan pada phase berikutnya:

- Skema database `divisions` dan `registrations`.
- Model, migration, relationship, enum status, dan seeder.
- Public landing page dan form pendaftaran.
- Admin panel Filament.
- Dashboard statistik.
- Konfigurasi TiDB Cloud production.
- Konfigurasi deployment Vercel.

## Tech Stack

Stack saat ini:

| Bagian | Teknologi |
| --- | --- |
| Backend | Laravel 13.25.0 |
| Bahasa | PHP 8.4.17 lokal, requirement project `^8.3` |
| Frontend | Blade, Tailwind CSS 4, Vite 8 |
| Database lokal awal | SQLite |
| Testing | PHPUnit 12 |
| Code style | Laravel Pint |

Target stack project:

| Bagian | Teknologi |
| --- | --- |
| Admin panel | Filament, versi stabil yang kompatibel dengan Laravel |
| Database production | TiDB Cloud |
| Driver database | Laravel MySQL connection / PDO MySQL |
| Icon | Heroicons |
| Hosting | Vercel serverless |
| Repository | GitHub |

Catatan: TiDB Cloud kompatibel dengan MySQL, jadi project ini tetap memakai `DB_CONNECTION=mysql`. Tidak perlu membuat driver khusus TiDB.

## Tujuan Aplikasi

Project ini ditujukan untuk membuat sistem pendaftaran anggota organisasi yang:

- Mudah digunakan oleh calon anggota.
- Responsif untuk mobile, tablet, dan desktop.
- Memiliki admin panel untuk mengelola data pendaftaran.
- Aman untuk konfigurasi production.
- Mudah dikembangkan bertahap.
- Layak ditampilkan sebagai portfolio developer.

## Arsitektur

Public website:

```text
User
-> Public Website
-> Laravel
-> Eloquent ORM
-> TiDB Cloud
```

Admin panel:

```text
Admin
-> Filament
-> Laravel / Eloquent
-> TiDB Cloud
```

Deployment production:

```text
GitHub
-> Vercel
-> Laravel
-> PDO MySQL with TLS
-> TiDB Cloud
```

## Fitur Target

Public website:

- Landing page.
- Tentang organisasi.
- Visi dan misi.
- Daftar divisi.
- Kegiatan atau program organisasi.
- Benefit menjadi anggota.
- FAQ.
- CTA pendaftaran.
- Form pendaftaran.
- Halaman sukses setelah pendaftaran.

Admin panel:

- Login admin.
- Dashboard.
- CRUD divisi.
- Kelola data pendaftar.
- Review pendaftar.
- Filter dan search pendaftar.
- Detail pendaftar.
- Ubah status pendaftaran.
- Statistik pendaftaran.
- Export data jika memungkinkan.

## Rencana Database

Tabel utama yang akan dibuat:

### `users`

Dipakai untuk akun admin Filament.

### `divisions`

Kolom:

- `id`
- `name`
- `description`, nullable
- `is_active`, boolean, default `true`
- `created_at`
- `updated_at`

Relasi:

- Satu division memiliki banyak registration.

### `registrations`

Kolom:

- `id`
- `registration_number`, unique
- `name`
- `email`
- `phone`
- `gender`, nullable
- `birth_date`, nullable
- `school`, nullable
- `address`, nullable
- `division_id`, foreign key
- `reason`
- `organization_experience`, nullable
- `instagram`, nullable
- `status`
- `notes`, nullable
- `created_at`
- `updated_at`

Relasi:

- Satu registration dimiliki oleh satu division.

## Status Pendaftaran

Status akan dibuat memakai PHP Enum `RegistrationStatus`.

Value:

- `pending`
- `review`
- `accepted`
- `rejected`

Status ini harus konsisten di model, form, table, filter, badge, dashboard, dan business logic.

## Nomor Pendaftaran

Nomor pendaftaran akan dibuat otomatis ketika calon anggota mengirim form.

Format:

```text
REG-2026-0001
REG-2026-0002
REG-2026-0003
```

Nomor ini tidak menggunakan `id` database secara langsung. Logic generate nomor harus menjaga nilai tetap unique dan aman dari duplicate.

## Requirement Environment

Pastikan environment lokal memiliki:

- PHP 8.3 atau lebih baru.
- Composer 2.
- Node.js dan npm.
- Extension PHP umum untuk Laravel, terutama `pdo`, `pdo_mysql`, `openssl`, `mbstring`, `ctype`, `filter`, `hash`, `tokenizer`, dan `fileinfo`.
- Git.
- Database lokal SQLite atau MySQL.
- Akun TiDB Cloud untuk production.
- Akun Vercel untuk deployment production.

Untuk cek versi:

```bash
php -v
composer --version
npm -v
```

## Instalasi Lokal

Clone repository:

```bash
git clone <repository-url>
cd register_system
```

Install dependency PHP:

```bash
composer install
```

Install dependency frontend:

```bash
npm install
```

Copy environment file:

```bash
cp .env.example .env
```

Di Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Generate application key:

```bash
php artisan key:generate
```

Jalankan migration:

```bash
php artisan migrate
```

Jalankan server Laravel:

```bash
php artisan serve
```

Jalankan Vite di terminal terpisah:

```bash
npm run dev
```

Buka aplikasi:

```text
http://127.0.0.1:8000
```

## Konfigurasi Database Lokal

Untuk development awal, SQLite bisa dipakai agar setup lebih cepat.

Contoh `.env` lokal:

```env
DB_CONNECTION=sqlite
```

Pastikan file ini tersedia:

```text
database/database.sqlite
```

Jika ingin memakai MySQL lokal:

```env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=register_system
DB_USERNAME=root
DB_PASSWORD=
```

## Konfigurasi TiDB Cloud

Untuk production, gunakan TiDB Cloud melalui koneksi MySQL-compatible.

Contoh environment:

```env
DB_CONNECTION=mysql
DB_HOST=your-tidb-host
DB_PORT=4000
DB_DATABASE=your_database
DB_USERNAME=your_username
DB_PASSWORD=your_password
MYSQL_ATTR_SSL_CA=/absolute/path/to/ca.pem
```

Aturan penting:

- Jangan hard-code host, username, password, certificate path, atau `APP_KEY`.
- Jangan commit file `.env`.
- Jangan commit password database.
- Gunakan password yang dibuat dari dashboard TiDB Cloud.
- Jika TiDB meminta CA certificate, simpan file certificate di tempat aman dan referensikan lewat environment variable.
- Gunakan `APP_DEBUG=false` di production.

## Environment Production

Contoh variable production:

```env
APP_NAME="Organization Registration System"
APP_ENV=production
APP_KEY=
APP_DEBUG=false
APP_URL=https://your-domain.vercel.app

DB_CONNECTION=mysql
DB_HOST=your-tidb-host
DB_PORT=4000
DB_DATABASE=your_database
DB_USERNAME=your_username
DB_PASSWORD=your_password
MYSQL_ATTR_SSL_CA=

SESSION_DRIVER=database
CACHE_STORE=database
QUEUE_CONNECTION=database
```

Untuk Vercel/serverless, jangan mengandalkan local filesystem sebagai storage persistent. Jika nanti ada fitur upload file, gunakan object storage seperti Cloudflare R2, AWS S3, atau Supabase Storage.

## Struktur Folder

Struktur penting saat ini:

```text
app/
bootstrap/
config/
database/
public/
resources/
routes/
storage/
tests/
```

Folder yang akan bertambah pada phase berikutnya:

```text
app/Enums/
app/Models/Division.php
app/Models/Registration.php
app/Http/Controllers/
app/Filament/
resources/views/pages/
resources/views/components/
```

## Route Target

Public route:

```text
GET  /
GET  /pendaftaran
POST /pendaftaran
GET  /pendaftaran/sukses/{registration}
```

Admin route:

```text
GET /admin
```

## Validasi Form Pendaftaran

Field wajib:

- Nama lengkap.
- Email valid.
- Nomor WhatsApp.
- Divisi yang diminati.
- Alasan bergabung.

Field opsional:

- Jenis kelamin.
- Tanggal lahir.
- Asal sekolah atau kampus.
- Alamat.
- Pengalaman organisasi.
- Instagram.

Semua input harus divalidasi memakai Laravel validation dan dilindungi CSRF protection.

## Command Penting

Menjalankan server:

```bash
php artisan serve
```

Menjalankan Vite:

```bash
npm run dev
```

Build asset frontend:

```bash
npm run build
```

Menjalankan migration:

```bash
php artisan migrate
```

Menjalankan seeder:

```bash
php artisan db:seed
```

Menjalankan test:

```bash
php artisan test
```

Format kode:

```bash
vendor/bin/pint
```

Clear cache config:

```bash
php artisan optimize:clear
```

## Roadmap Development

Project akan dikerjakan bertahap:

| Phase | Fokus |
| --- | --- |
| 1 | Project initialization |
| 2 | Database dan koneksi TiDB |
| 3 | Models, migrations, dan relationships |
| 4 | Seeder admin dan divisions |
| 5 | Instalasi Filament |
| 6 | DivisionResource |
| 7 | RegistrationResource |
| 8 | Filament dashboard dan widgets |
| 9 | Public landing page |
| 10 | Public registration form |
| 11 | Validation dan registration number |
| 12 | Security hardening |
| 13 | Production configuration |
| 14 | Vercel deployment |
| 15 | TiDB production connection |
| 16 | Testing end-to-end |

## Checklist Phase 1

Phase 1 dianggap selesai jika:

- `composer install` berhasil.
- `npm install` berhasil.
- File `.env` sudah dibuat dari `.env.example`.
- `php artisan key:generate` berhasil.
- `php artisan migrate` berhasil.
- `php artisan serve` berjalan.
- `npm run dev` berjalan.
- Halaman awal Laravel bisa dibuka di browser.
- `.env` tidak masuk Git.
- Project sudah siap masuk GitHub.

## Security Notes

Hal yang wajib dijaga:

- Jangan commit `.env`.
- Jangan commit credential TiDB Cloud.
- Jangan expose `APP_KEY`.
- Gunakan `APP_DEBUG=false` di production.
- Gunakan Laravel validation untuk semua input public.
- Gunakan CSRF protection.
- Gunakan mass assignment protection.
- Batasi akses admin hanya melalui Filament authentication.
- Tambahkan rate limiting untuk endpoint pendaftaran jika traffic mulai tinggi.
- Jangan gunakan local filesystem sebagai storage production di Vercel.

## Deployment Notes

Target deployment adalah Vercel dengan Laravel berjalan sebagai serverless function.

File yang akan disiapkan pada phase deployment:

```text
vercel.json
api/index.php
```

Catatan penting untuk production:

- Set semua environment variable di dashboard Vercel.
- Pastikan TiDB Cloud mengizinkan koneksi dari environment production.
- Gunakan TLS/SSL sesuai instruksi TiDB Cloud.
- Jalankan migration production dengan hati-hati.
- Jangan bergantung pada file lokal untuk session, cache, queue, atau upload.

## Testing Checklist Sebelum Production

Sebelum deploy final, pastikan:

- Laravel berjalan lokal.
- Database terkoneksi.
- Migration berhasil.
- Seeder berhasil.
- Admin dapat login.
- CRUD division berjalan.
- CRUD registration berjalan.
- Public registration berjalan.
- Nomor pendaftaran tergenerate otomatis.
- Validasi form berjalan.
- Status pendaftaran dapat diubah.
- Dashboard menampilkan statistik.
- UI responsif di mobile, tablet, dan desktop.
- `APP_DEBUG=false` di production.
- TiDB Cloud menerima query dari production.
- Deployment Vercel berhasil.

## Lisensi

Project ini dibuat sebagai project pribadi dan portfolio. Sesuaikan lisensi sebelum repository dibuat public.
