# 🎓 Litera-AI Web Platform (Control Center)

<p align="center">
  <img src="public/logo.png" alt="Litera-AI Logo" width="240" height="240" />
</p>

[![Next.js](https://img.shields.io/badge/Next.js-15-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3.4-blue?style=for-the-badge&logo=tailwind-css)](https://tailwindcss.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?style=for-the-badge&logo=typescript)](https://www.typescriptlang.org/)
[![Prisma](https://img.shields.io/badge/Prisma-ORM-teal?style=for-the-badge&logo=prisma)](https://www.prisma.io/)
[![Gemini](https://img.shields.io/badge/Gemini_AI-API-orange?style=for-the-badge&logo=google-gemini)](https://deepmind.google/technologies/gemini/)

---

## 📖 1. Latar Belakang & Deskripsi Proyek (Background & Project Description)

**LITERA-AI Web Platform** merupakan pusat kendali terintegrasi (Control Center) yang dirancang untuk mengelola seluruh ekosistem **LITERA-AI (Literacy Intelligent Assistant)**. Proyek ini dibangun sebagai solusi digital inovatif di bawah naungan inisiatif **P-LIDM (Platform Inovasi Teknologi AI dengan Asesmen Diagnostik Adaptif)**, dengan misi utama memulihkan dan meningkatkan kemampuan literasi membaca serta penalaran kritis (logical reasoning) bagi generasi muda Indonesia.

### Permasalahan & Solusi (The Problem & Solution)
Berdasarkan data asesmen standar nasional dan PISA (Program for International Student Assessment), tingkat literasi membaca dan pemahaman teks sastra di kalangan murid sekolah Indonesia memerlukan intervensi taktis dan adaptif. Litera-AI memecahkan masalah ini dengan menyediakan jalur pembelajaran sastra yang dipersonalisasi:
* **Bagi Siswa**: Menggunakan aplikasi mobile untuk pengerjaan kuis adaptif berbasis AI, asisten membaca karya klasik, dan editor penulisan.
* **Bagi Guru**: Menggunakan dashboard web ini untuk memonitor hasil belajar, melacak kelemahan individu/kelas secara real-time, dan membagikan materi pengajaran digital.
* **Bagi Orang Tua**: Menggunakan portal web ini untuk mendampingi perkembangan kognitif literasi anak dengan arahan rekomendasi asisten AI di rumah.

Melalui integrasi dengan **Google Gemini AI API**, platform ini secara otomatis merumuskan soal kuis sastra dengan tingkat kesulitan berjenjang (Taksonomi Bloom) berdasarkan buku sastra klasik Indonesia pilihan guru (seperti angkatan Balai Pustaka, Pujangga Baru, hingga angkatan 45).

### 🔄 Alur Penggunaan Aplikasi (Application Workflow)

Sistem Litera-AI bekerja secara end-to-end melalui tahapan berikut untuk memberikan bimbingan belajar literasi sastra yang adaptif:

1. **Pendaftaran Akun & Penentuan Peran (Multi-Role Authentication)**:
   - Pengguna (Murid, Guru, Orang Tua) mendaftar dan masuk ke sistem menggunakan autentikasi JWT-OTP yang aman di aplikasi mobile atau web control center.
2. **Asesmen Diagnostik Awal (Initial Diagnostic Assessment)**:
   - Saat murid pertama kali membuka aplikasi mobile, mereka wajib mengikuti kuis asesmen awal untuk menilai tingkat pemahaman membaca (reading level: Pemula, Menengah, Mahir).
3. **Pemetaan Jalur Belajar Personal (Personalized Learning Path)**:
   - Berdasarkan hasil asesmen, mesin AI menentukan daftar novel sastra klasik Indonesia yang paling cocok untuk dibaca oleh murid tersebut.
4. **Membaca dengan Asisten Interaktif (Interactive Reading)**:
   - Murid membaca naskah sastra klasik di aplikasi. Saat menemui kosakata sulit atau majas, murid dapat menekan teks tersebut untuk mendapatkan penjelasan konteks instan dari asisten AI.
5. **Kuis Evaluasi Adaptif (Adaptive Quizzing & DDA)**:
   - Setelah menyelesaikan bab membaca, murid mengerjakan kuis. Mesin AI (DDA) memantau akurasi jawaban dan durasi pengerjaan untuk menentukan tingkat kesulitan soal berikutnya secara dinamis.
6. **Pemantauan Guru & Orang Tua (Teacher & Parent Monitoring)**:
   - Seluruh data keaktifan dan perkembangan kognitif murid disinkronkan ke server. Guru dapat memantau dispersi nilai kelas di dashboard web, dan orang tua dapat membaca rekomendasi panduan membaca dari AI untuk diterapkan di rumah.

---

## 🔬 1.5. Konsep Dasar & Struktur Fungsi (Core Concepts & Function Structure)

Sistem Litera-AI didasarkan pada metodologi pedagogi modern dan arsitektur rekayasa perangkat lunak terdistribusi berikut:

### 1. Konsep Pedagogi & Kecerdasan Buatan (Pedagogical & AI Concepts)
* **Asesmen Diagnostik Adaptif (Adaptive Diagnostic Assessment)**:
  Pendekatan evaluasi kognitif awal menggunakan klasifikasi berbasis kemahiran membaca (Reading Proficiency Level). Asesmen tidak hanya menilai benar/salah jawaban, tetapi juga memetakan kemampuan interpretasi alur, pengenalan gaya bahasa (majas), dan pemahaman semantik teks.
* **Dynamic Difficulty Adjustment (DDA)**:
  Sistem penyesuaian kesulitan kuis secara real-time yang memposisikan belajar murid dalam *Zone of Proximal Development (ZPD)*. Algoritma DDA memantau parameter rasio kebenaran (accuracy) dan latensi respon pengerjaan (response time) untuk menentukan tingkat kesulitan soal berikutnya secara dinamis, guna meminimalkan rasa frustrasi (jika soal terlalu sulit) atau kebosanan (jika soal terlalu mudah).
* **Knowledge Tracing (Penelusuran Pengetahuan)**:
  Menganalisis akumulasi riwayat kuis murid untuk memetakan kekuatan dan kelemahan spesifik kognitif sastra mereka (misalnya, pengenalan majas personifikasi vs metafora).

### 2. Struktur Fungsi Utama Program (Core Functional Structure)
* **Modul Keamanan & Autentikasi (Auth & Security Hub)**:
  - Fungsi: Mengatur izin akses multi-role (Guru, Orang Tua, Siswa, Admin).
  - Logika Keamanan: Implementasi OTP token berdurasi pendek berbasis JWT (Json Web Token) untuk login aman serta logging IP Address pada audit log.
* **Mesin Pembuat Soal Gemini AI (Gemini AI Quiz Generation Engine)**:
  - Fungsi: Membuat soal kuis sastra secara otomatis.
  - Logika: Menerima naskah novel dari pustaka digital, memproses prompt terstruktur (Taksonomi Bloom) melalui API Gemini, menghasilkan array JSON soal berformat terstandarisasi.
* **Modul Sinkronisasi Data Luar Jaringan (Offline Data Sync Hub)**:
  - Fungsi: Sinkronisasi database klien seluler dengan database server PostgreSQL.
  - Logika: Menggunakan SQLite/Hive di sisi klien untuk antrean outbox, kemudian diproses dalam mode batch request oleh API backend FastAPI untuk pembaruan record `StudentProgress` dan analitik monitoring kelas guru.
* **Dashboard Analitik Guru & Orang Tua (Visual Analytics & Recommendations)**:
  - Fungsi: Pengolahan data statistik keaktifan dan skor kuis menjadi visualisasi chart dispersion, serta penayangan tips bimbingan AI bagi orang tua.

---

## ✨ 2. Fungsionalitas Modul (Detailed Module Features)

### 👨‍🏫 A. Dashboard Pendidik (Teacher Dashboard Hub)
1. **Analitik Visual & Dispersi Skor (Visual Analytics)**:
   - Grafik interaktif untuk melacak waktu rata-rata membaca teks per halaman.
   - Peta pemahaman membaca kelas (distribusi nilai kuis, penguasaan majas, pemahaman alur cerita).
   - Identifikasi otomatis bagi murid yang membutuhkan perhatian khusus (*students at risk*).
2. **Mesin Pembuat Kuis AI Otomatis (Generative AI Quiz Builder)**:
   - Guru memilih novel sastra klasik Indonesia (misal: *Siti Nurbaya*, *Salah Asuhan*, *Ronggeng Dukuh Paruk*).
   - AI memproses naskah dan menghasilkan pertanyaan pilihan ganda atau esai pendek dengan rentang kesulitan kognitif yang bervariasi.
3. **Manajemen Bahan Ajar & Tugas Kelas**:
   - Distribusi buku membaca digital (.pdf / epub) langsung ke antrean aplikasi siswa.
   - Pengaturan batas waktu pengerjaan tugas (due dates).

### 👪 B. Portal Pemantau Wali Murid (Parent Portal)
1. **Laporan Kinerja Berkala**:
   - Rekap mingguan pengerjaan latihan menulis esai dan kuis membaca anak.
   - Perbandingan progress kognitif anak terhadap standar kurikulum nasional.
2. **Rekomendasi Pendampingan Belajar Rumah (AI Home-Reading Guide)**:
   - Chatbot rekomendasi yang dilatih khusus untuk menyarankan buku sastra alternatif dan topik diskusi keluarga berdasarkan riwayat belajar anak.

### 🛡️ C. Sistem Kredensial & Audit Keamanan (Security & Auditing)
1. **Dual OTP (One-Time Password) Token Flow**:
   - Setiap upaya login untuk peran guru dan administrator melewati verifikasi OTP berbasis SMS/Email yang dienkripsi menggunakan Token JWT (Json Web Token) berdurasi pendek (short-lived tokens).
2. **Logging Audit Log Komprehensif**:
   - Mencatat seluruh jejak audit administratif (siapa mengakses data apa, waktu login, dan perubahan parameter kelas) untuk mencegah kebocoran data.

---

## 🗄️ 3. Skema Basis Data & Model (Database Schema & Models)

Proyek ini menggunakan **Prisma ORM** untuk mendefinisikan relasi database PostgreSQL. Berikut adalah model utama yang diimplementasikan:

```prisma
// Ringkasan Model Utama
model User {
  id            String          @id @default(uuid())
  email         String          @unique
  name          String
  role          Role
  createdAt     DateTime        @default(now())
  classrooms    Classroom[]     // Relasi bagi Guru
  studentProgress StudentProgress? // Relasi bagi Murid
  auditLogs     AuditLog[]
}

enum Role {
  ADMIN
  EDUCATOR    // Guru
  STUDENT     // Murid
  PARENT      // Orang Tua
}

model Classroom {
  id          String      @id @default(uuid())
  code        String      @unique // Kode unik akses siswa
  name        String
  subject     String
  teacherId   String
  teacher     User        @relation(fields: [teacherId], references: [id])
  students    Student[]
  quizzes     Quiz[]
}

model StudentProgress {
  id            String    @id @default(uuid())
  studentId     String    @unique
  student       User      @relation(fields: [studentId], references: [id])
  readingLevel  String    @default("Pemula") // Pemula, Menengah, Mahir
  points        Int       @default(0)
  quizzesTaken  Int       @default(0)
  averageScore  Float     @default(0.0)
}

model Quiz {
  id          String      @id @default(uuid())
  title       String
  classId     String
  classroom   Classroom   @relation(fields: [classId], references: [id])
  questions   Json        // Menyimpan array soal buatan Gemini AI
  createdAt   DateTime    @default(now())
}

model AuditLog {
  id        String    @id @default(uuid())
  userId    String
  user      User      @relation(fields: [userId], references: [id])
  action    String    // Tindakan (Login, Generate Quiz, Add Material)
  ipAddress String
  createdAt DateTime  @default(now())
}
```

---

## 🔌 4. Antarmuka API Web (API Route Index)

Platform web melayani pertukaran data API asinkron dengan rincian berikut:

| Route Path | Method | Auth | Deskripsi |
|---|---|---|---|
| `/api/auth/login` | `POST` | None | Autentikasi awal pengguna menggunakan Email & Password. Menghasilkan session cookie. |
| `/api/auth/send-otp` | `POST` | None | Mengirimkan kode verifikasi OTP ke kontak pengguna yang terdaftar. |
| `/api/auth/verify-otp` | `POST` | None | Memverifikasi OTP dan menerbitkan token otentikasi JWT permanen. |
| `/api/auth/me` | `GET` | Bearer Token | Memperoleh data profil login pengguna yang aktif beserta hak aksesnya. |
| `/api/assessment/submit` | `POST` | Student Token | Mengirimkan respon jawaban asesmen diagnostik untuk evaluasi level kognitif literasi. |
| `/api/otp/audit-logs` | `GET` | Admin Token | Mengambil daftar logs aktivitas audit sistem keamanan OTP untuk keamanan transaksi data. |

---

## 📂 5. Struktur Direktori Lengkap (Folder Structure)

```text
src/
├── app/                  # File routing utama berbasis Next.js App Router
│   ├── (app)/            # Halaman aplikasi setelah terautentikasi
│   │   ├── guru/         # Modul guru (assignments, attendance, calendar, classes, materials, reports, settings)
│   │   ├── orang-tua/    # Modul orang tua (monitoring perkembangan kognitif anak)
│   │   └── siswa/        # Modul visualisasi data kuis siswa web
│   ├── admin/            # Panel audit administratif sistem
│   ├── api/              # Route API endpoints (OTP, Auth, Assessment)
│   ├── forgot-password/  # Halaman pemulihan password
│   ├── register/         # Pendaftaran akun multi-role
│   └── page.tsx          # Landing page utama Litera-AI (interaktif dengan landing page premium)
├── components/           # Komponen UI global & reusable layouting
│   ├── layout/           # Sidebar, Header, AppLayout yang responsif
│   └── auth-guard.tsx    # Halaman pembatas akses otentikasi peran (role restriction guard)
├── lib/                  # Utilitas sistem, instance Prisma, dan Zustand global store
├── repositories/         # Layer repository pattern untuk interaksi langsung dengan database PostgreSQL
├── server/               # Konfigurasi asisten AI
│   ├── ai/               # Gemini API Client wrapper
│   └── prompt-registry.ts# Template prompt sistem untuk pembuatan bank soal terstruktur
└── services/             # Layer business logic aplikasi (OTP verification, Auth logic, DB sync)
```

### 📦 5.5. Daftar Dependensi & Pustaka Utama (Dependencies & Key Libraries)

Untuk memastikan keandalan pemrosesan asinkron dan estetika antarmuka premium, platform web Litera-AI menggunakan pustaka utama berikut:

| Pustaka (Library) | Versi | Peran & Alasan Penggunaan (Purpose) |
|---|---|---|
| `next` | `16.2.10` | Framework utama React untuk rendering Server-Side (SSR) & routing halaman asinkron secara cepat. |
| `@google/genai` | `^2.10.0` | Integrasi langsung dengan API Generative AI Google (Gemini) untuk pemrosesan teks sastra dan pembuatan kuis otomatis. |
| `@prisma/client` | `^7.8.0` | Object Relational Mapper (ORM) tipe-aman untuk komunikasi data yang efisien ke PostgreSQL. |
| `zustand` | `^5.0.14` | Manajemen state global client yang sangat ringan untuk mengelola status peran login tanpa overhead re-render. |
| `next-auth` | `^5.0.0-beta` | Sistem pengelolaan sesi otentikasi multi-role yang aman dan teruji. |
| `framer-motion` | `^12.42.2` | Engine animasi mikro untuk transisi dashboard dan accordion FAQ yang smooth dan premium. |
| `nodemailer` | `^7.0.13` | Pengiriman email berisi token OTP untuk verifikasi masuk lapis ganda. |
| `bcryptjs` | `^3.0.3` | Enkripsi hashing password pengguna sebelum disimpan ke database PostgreSQL. |

---

## 🚀 6. Panduan Instalasi & Eksekusi (Installation & Deployment)

### Langkah 1: Kloning & Persiapan Sistem
Pastikan Node.js v18/v20+ dan PostgreSQL telah terpasang dan berjalan di server lokal.

### Langkah 2: Setup Konfigurasi `.env`
Buat file `.env` pada direktori root proyek Next.js:
```env
DATABASE_URL="postgresql://postgres:password123@localhost:5432/litera_web_db?schema=public"
GEMINI_API_KEY="AIzaSyA..."
OTP_SECRET="your-super-secret-jwt-key"
```

### Langkah 3: Instalasi Dependensi Node
```bash
npm install
```

### Langkah 4: Migrasi Database & Seeding Data Awal
Proses ini akan membuat tabel relasi database PostgreSQL secara otomatis dan mengisinya dengan materi sastra awal:
```bash
npx prisma db push
npx prisma db seed
```

### Langkah 5: Jalankan Mode Pengembangan (Development Mode)
```bash
npm run dev
```
Aplikasi web dapat diakses langsung pada port default [http://localhost:3000](http://localhost:3000).

### Langkah 6: Jalankan Melalui Docker (Running via Docker)
Anda juga dapat membangun image dan menjalankan aplikasi ini di dalam container:
```bash
docker build -t litera-web-platform .
docker run -p 3000:3000 --env-file .env litera-web-platform
```

---

## 📐 7. Alur Kontrol & Data (Data & Control Flow)

Berikut adalah diagram alur visual bagaimana interaksi antar peran diatur dan terhubung secara internal dengan database PostgreSQL serta model generatif Gemini AI:

```mermaid
graph TD
    A[Browser Client] -->|Routes| B[Next.js App Router]
    subgraph Pages [Pages & Roles]
        B -->|/guru| C[Teacher Dashboard]
        B -->|/orang-tua| D[Parent Portal]
        B -->|/siswa| E[Student Visualizer]
    end
    subgraph Backend_Services [Backend Services]
        C & D & E -->|actions / handlers| F[Services & Logic Layer]
        F -->|ORM mapping| G[Prisma Client]
        G -->|reads/writes| H[(PostgreSQL DB)]
        F -->|Generates Questions| I[Gemini AI Client]
    end
```

### 🎬 7.5. Skenario Simulasi Penggunaan Ekosistem (System Simulation Scenarios)

Untuk memberikan gambaran yang lebih jelas tentang bagaimana data mengalir di platform ini, berikut adalah dua skenario penggunaan utama:

#### Skenario A: Pembuatan Kuis Otomatis oleh Guru
1. **Pilihan Novel**: Guru masuk ke `/guru/materials` dan memilih naskah novel klasik *Siti Nurbaya*.
2. **AI Generation**: Guru mengklik tombol "Buat Kuis dengan AI". Tindakan ini memicu pemrosesan template prompt kognitif di `server/ai/prompt-registry.ts`.
3. **Penyimpanan JSON**: API Gemini membalas dengan struktur array soal kuis (soal, pilihan jawaban, kunci, tingkat Bloom). Soal disimpan dalam field `Quiz.questions` berformat JSON di database PostgreSQL melalui Prisma.
4. **Push Notification**: Sistem memberitahu seluruh siswa kelas tersebut melalui WebSocket/Polling bahwa kuis membaca baru telah tersedia.

#### Skenario B: Pemantauan Progress Kognitif Siswa oleh Orang Tua & Guru
1. **Pengerjaan Soal**: Siswa menyelesaikan kuis di aplikasi mobile. Data nilai, tingkat kesulitan, dan durasi pengerjaan dikirim ke server.
2. **Pembaruan Profil**: Server memproses dan memperbarui record `StudentProgress` (misalnya, mengubah status tingkat membaca siswa dari "Pemula" menjadi "Menengah").
3. **Visualisasi Dashboard**: Guru membuka `/guru/reports` dan melihat chart dispersi nilai kelas terupdate, lengkap dengan identifikasi klaster siswa yang mengalami kesulitan membaca.
4. **Rekomendasi Orang Tua**: Wali murid masuk ke `/orang-tua` dan menerima instruksi taktis berbasis AI: *"Siswa mengalami kesulitan memahami majas sarkasme di Novel Salah Asuhan. Mohon dampingi dengan membacakan teks halaman 45-50 bersama."*

---

## 🎯 8. Kesimpulan & Visi Ke Depan (Conclusion & Roadmap)

**LITERA-AI Web Platform** memegang peran krusial sebagai pusat administrasi, visualisasi, dan pemantauan bagi guru serta orang tua untuk berkolaborasi mendampingi tumbuh kembang literasi anak secara sinergis. Kombinasi arsitektur Next.js 15 yang modern dan serverless-ready, data mapping aman Prisma, serta kecerdasan buatan Gemini AI menjamin bahwa Litera-AI siap digunakan dalam skala luas di sekolah-sekolah di Indonesia.

### 📌 Peta Jalan Pengembangan (Roadmap):
* **Fase 1 (Selesai)**: Struktur dasar dashboard, login multi-role aman, generator soal adaptif dengan Gemini AI, dan koneksi Prisma DB.
* **Fase 2 (Dalam Pengembangan)**: Implementasi analitik grafik interaktif yang menampilkan klaster kognitif siswa secara visual (Clustering Analysis) dan otomatisasi publikasi paket Docker di GitHub Packages (Selesai).
* **Fase 3 (Mendatang)**: Modul evaluasi berbicara (speech-to-text pronunciation analyzer) guna menilai aspek pelafalan murid secara interaktif di browser.
