# DeadlineMate

Asisten tugas untuk mahasiswa yang memecah tenggat besar menjadi langkah kecil, lalu mengingatkan sebelum terlambat.

![DeadlineMate Banner](./docs/banner.png)

## Latar Belakang

Mahasiswa jarang gagal karena tidak mampu. Mereka gagal karena tidak tahu harus mulai dari mana (Task Paralysis), meremehkan waktu pengerjaan (Planning Fallacy), dan berhenti total setelah satu hari terlewat (Streak Fragility). Aplikasi to-do biasa hanya mencatat tugas. Ketiga masalah ini tidak tersentuh.

DeadlineMate menjawabnya dengan tiga pendekatan. AI Task Breakdown memecah tugas menjadi sub-langkah yang jelas. Gamifikasi dengan sistem Shield menjaga streak tetap adil. Push notification mengingatkan secara proaktif sebelum tenggat, bukan setelahnya.

## Screenshots

### Halaman Login

<table>
  <tr>
    <td align="center" width="70%">
      <img src="./docs/loginpage_desktop.png" alt="Halaman login di desktop"/><br />
      <sub>Desktop</sub>
    </td>
    <td align="center" width="30%">
      <img src="./docs/loginpage_mobile.png" alt="Halaman login di mobile"/><br />
      <sub>Mobile</sub>
    </td>
  </tr>
</table>

### Dashboard

<table>
  <tr>
    <td align="center" width="70%">
      <img src="./docs/dashboard_desktop.png" alt="Dashboard di desktop"/><br />
      <sub>Desktop</sub>
    </td>
    <td align="center" width="30%">
      <img src="./docs/dashboard_mobile.png" alt="Dashboard di mobile"/><br />
      <sub>Mobile</sub>
    </td>
  </tr>
</table>

### Tugas

<table>
  <tr>
    <td align="center" width="70%">
      <img src="./docs/task_desktop.png" alt="Halaman tugas di desktop"/><br />
      <sub>Desktop</sub>
    </td>
    <td align="center" width="30%">
      <img src="./docs/task_mobile.png" alt="Halaman tugas di mobile"/><br />
      <sub>Mobile</sub>
    </td>
  </tr>
</table>

## Fitur Utama

### Smart Scheduler (AI)

Pengguna menulis tugas dalam teks bebas, termasuk pesan yang ditempel dari grup chat. Model dipanggil lewat Vercel AI SDK dengan Groq. Outputnya dipaksa mengikuti skema terstruktur.

Setiap respons divalidasi dengan Zod sebelum disimpan. Jika model timeout, error, atau menghasilkan output yang gagal validasi, local parser mengambil alih. Pengguna tetap mendapat rencana, hanya tanpa bantuan model.

Tenggat internal tiap sub-langkah dihitung otomatis dari tenggat utama.

### Autentikasi dan Keamanan

Autentikasi memakai Auth.js v5 dengan dua provider: Google OAuth dan Credentials. Password di-hash dengan scrypt. Fitur forgot password mengirim tautan reset lewat Resend.

Middleware melindungi seluruh route aplikasi. Request tanpa sesi valid diarahkan ke halaman login.

### PWA dan Push Notifications

Aplikasi dapat diinstal sebagai PWA. Service Worker menangani notifikasi lewat Web Push API dengan kunci VAPID.

Pengingat dikirim oleh endpoint cron yang dipanggil terjadwal dan dilindungi `CRON_SECRET`. Tersedia juga endpoint untuk menguji push dari sisi pengembang.

### Task Management

- Deskripsi tugas dan file attachment lewat Vercel Blob
- Input suara memakai Web Speech API
- Filter kalender interaktif
- Grafik progress 7 hari

### Sistem Streak dan EXP

EXP diberikan berdasarkan ketepatan waktu penyelesaian.

| Kondisi | EXP |
| :--- | :---: |
| Selesai tepat waktu | +15 |
| Selesai terlambat | +5 |
| Terlambat dan tidak diselesaikan | -5 |

Shield menahan streak agar tidak reset saat satu hari terlewat. Pengguna yang sempat berhenti tidak kehilangan seluruh progres.

## Tech Stack

| Layer | Teknologi |
| :--- | :--- |
| Framework | Next.js 15 (App Router, Server Actions) |
| Bahasa | TypeScript strict mode |
| Styling | Tailwind CSS v4 dengan custom design tokens |
| Database | PostgreSQL (Neon) |
| ORM | Prisma 7 |
| Autentikasi | Auth.js v5 (NextAuth) |
| AI Engine | Vercel AI SDK + Groq |
| File Storage | Vercel Blob |
| Email Service | Resend |
| Push Notif | Web Push (VAPID) + Service Worker |
| Validasi | Zod |

## Menjalankan di Lokal

### Prasyarat

- Node.js v20 atau lebih baru
- PostgreSQL, lokal atau hosted (Neon)
- Kredensial Google OAuth, API key Groq, API key Resend, dan token Vercel Blob
- Sepasang kunci VAPID, dibuat dengan `npx web-push generate-vapid-keys`

### Instalasi

```bash
git clone https://github.com/mhdridwannst/DeadlineMate.git
cd DeadlineMate
npm install
cp .env.example .env
npx prisma migrate dev
npm run dev
```

Isi `.env` terlebih dahulu sebelum menjalankan migrasi. Aplikasi berjalan di `http://localhost:3000`.

### Environment Variables

| Variabel | Keterangan |
| :--- | :--- |
| `DATABASE_URL` | Connection string PostgreSQL |
| `AUTH_SECRET` | Secret untuk Auth.js. Generate dengan `openssl rand -base64 32` |
| `AUTH_GOOGLE_ID` | Client ID Google OAuth |
| `AUTH_GOOGLE_SECRET` | Client secret Google OAuth |
| `GROQ_API_KEY` | API key Groq untuk Smart Scheduler |
| `AI_MODEL` | Nama model, contoh `llama-3.3-70b-versatile` |
| `RESEND_API_KEY` | API key Resend untuk email forgot password |
| `BLOB_READ_WRITE_TOKEN` | Token Vercel Blob untuk file attachment |
| `NEXT_PUBLIC_VAPID_PUBLIC_KEY` | Kunci publik VAPID, dibaca di sisi client |
| `VAPID_PRIVATE_KEY` | Kunci privat VAPID, hanya di server |
| `VAPID_SUBJECT` | Kontak pengirim push, format `mailto:email@domain.com` |
| `CRON_SECRET` | Secret untuk mengamankan endpoint cron |

## Design Philosophy

Antarmuka memakai Neo-Brutalism: border tebal, shadow keras tanpa blur, dan kontras warna tinggi. Alasannya praktis. Hierarki visual terbaca cepat di layar kecil, dan elemen interaktif sulit salah dikenali.

Ikon di UI fungsional adalah SVG buatan sendiri, bukan emoji. Emoji dirender berbeda di tiap OS, tidak mengikuti tema terang atau gelap, dan ukurannya tidak konsisten dengan teks di sekitarnya. SVG memberi kontrol penuh atas stroke, warna, dan ukuran.

Interaksi memberi physical feedback. Tombol bergeser dan shadow-nya mengecil saat ditekan, sehingga setiap aksi punya konfirmasi visual yang langsung.

## Struktur Folder

```
prisma/                  Schema, migrasi, dan konfigurasi database
src/app/(app)/           Halaman utama: today, progress, kalender, profil
src/app/api/             API Routes (Auth, Upload, Cron, Push Test)
src/components/shell/    Layout, navigasi, tema, notif toggle
src/components/tugas/    Komponen domain tugas (DaftarTugas, Form, AI)
src/server/              Server Actions (Auth, AI Plan, Task, Push)
src/lib/                 Utilitas: DB, AI Model, Email, Waktu, Stats
```

## Tim

Dikembangkan oleh Kelompok 2 dari UKM Software Development 2026:

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/mhdridwannst">
        <img src="https://github.com/mhdridwannst.png" width="100" style="border-radius:50%" alt="Mhd. Ridwan"/><br />
        <sub><b>Mhd. Ridwan</b></sub>
      </a><br />
      Hacker
    </td>
    <td align="center">
      <a href="https://github.com/ridho-novianto">
        <img src="https://github.com/ridho-novianto.png" width="100" style="border-radius:50%" alt="Muhammad Slamet Ridho"/><br />
        <sub><b>Muhammad Slamet Ridho</b></sub>
      </a><br />
      Hipster
    </td>
    <td align="center">
      <a href="https://github.com/username3">
        <img src="https://github.com/username3.png" width="100" style="border-radius:50%" alt="Hervina Alivia Fitri"/><br />
        <sub><b>Hervina Alivia Fitri</b></sub>
      </a><br />
      Hustler
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="https://github.com/M-Zaki-Edi">
        <img src="https://github.com/M-Zaki-Edi.png" width="100" style="border-radius:50%" alt="M Zaki Edi"/><br />
        <sub><b>M Zaki Edi</b></sub>
      </a><br />
      Hacker
    </td>
    <td align="center">
      <a href="https://github.com/username5">
        <img src="https://github.com/username5.png" width="100" style="border-radius:50%" alt="Fahry Ibrahim"/><br />
        <sub><b>Fahry Ibrahim</b></sub>
      </a><br />
      Hipster
    </td>
    <td align="center">
      <a href="https://github.com/username6">
        <img src="https://github.com/username6.png" width="100" style="border-radius:50%" alt="Hamzah Asadullah"/><br />
        <sub><b>Hamzah Asadullah</b></sub>
      </a><br />
      Hustler
    </td>
  </tr>
</table>

## Lisensi

MIT License.
