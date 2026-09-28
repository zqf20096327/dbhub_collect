# 📱 Litera-AI Monorepo (Mobile Client, Backend API, & AI Services)

<p align="center">
  <img src="apps/mobile/assets/images/logo.png" alt="Litera-AI Logo" width="240" height="240" />
</p>

[![Flutter](https://img.shields.io/badge/Flutter-3.x-blue?style=for-the-badge&logo=flutter)](https://flutter.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue?style=for-the-badge&logo=docker)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Active-blue?style=for-the-badge&logo=postgresql)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-Active-red?style=for-the-badge&logo=redis)](https://redis.io/)

---

## 📖 1. Latar Belakang & Gambaran Umum (Background & Overview)

**LITERA-AI Monorepo** adalah pusat pengembangan kode terpadu yang memuat seluruh infrastruktur aplikasi seluler (mobile client), layanan backend server, serta mesin kecerdasan buatan (predictive AI engine) dalam ekosistem **LITERA-AI (Literacy Intelligent Assistant)**. Monorepo ini dirancang khusus guna menyukseskan program **P-LIDM (Platform Inovasi Teknologi AI dengan Asesmen Diagnostik Adaptif)** untuk pemulihan kecakapan literasi membaca tingkat nasional.

### Mengapa Monorepo?
Untuk menjaga konsistensi tipe data, kecepatan sinkronisasi REST API, dan kemudahan deployment, seluruh komponen seluler, backend, dan AI disatukan dalam struktur repositori tunggal ini. Ini mempermudah tim pengembang melakukan pengujian integrasi (integration testing) secara simultan antara klien seluler Dart/Flutter dengan API server berbasis Python/FastAPI.

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

## 📂 2. Struktur Workspace & Penjelasan Modul (Workspace Structure)

```text
apps/
  ├── mobile/         # Klien aplikasi seluler lintas platform (Flutter)
  ├── backend/        # RESTful API Backend asinkron (FastAPI)
  └── ai/             # Modul penalaran keputusan kognitif & DDA (Python)
docs/                 # Spesifikasi ERD database, OpenAPI, arsitektur, & panduan desain
infra/                # Berkas konfigurasi deployment Docker Compose & Nginx
```

---

## 📱 3. Modul Klien Seluler (Flutter Mobile Client Detail)

Aplikasi mobile Litera-AI didesain sebagai media belajar interaktif siswa dengan fitur-fitur teknis utama sebagai berikut:

### A. Arsitektur & Manajemen State (State Management)
* Mengadopsi arsitektur berbasis fitur (feature-first architecture) untuk memisahkan domain data, domain bisnis (domain entities), dan layer presentasi UI.
* **State Management**: Sepenuhnya dikelola menggunakan **Riverpod** (Notifier & AsyncNotifier) untuk menghasilkan alur data satu arah (unidirectional data flow) yang reaktif, bersih, mudah diuji, dan aman dari memory leaks.
* **Routing**: Menggunakan **GoRouter** dengan perlindungan hak akses halaman (route authentication guards). Siswa yang belum melengkapi profil kognitif awal akan secara otomatis diarahkan ke halaman asesmen diagnostik terlebih dahulu sebelum masuk ke dashboard utama.

### B. Penyimpanan Offline-First & Antrean Sinkronisasi (Offline-First Storage)
* **Hive Database**: Menggunakan database NoSQL lokal Hive yang sangat cepat untuk melakukan caching seluruh koleksi novel sastra klasik, riwayat membaca, dan modul kuis siswa secara lokal.
* **Antrean Outbox Persisten (Offline Outbox Queue)**: Ketika murid mengerjakan tugas atau menjawab kuis saat koneksi internet terputus, seluruh jawaban disimpan sebagai antrean (*outbox task*) di lokal.
* **Synchronization Worker**: Begitu terdeteksi koneksi internet kembali aktif (`NetworkStatusBanner`), aplikasi secara otomatis memproses antrean tersebut ke API backend secara batch, serta memunculkan status sinkronisasi sukses ke pengguna secara real-time.

---

## ⚡ 4. Modul Server API Backend (FastAPI Backend Detail)

Backend Litera-AI dirancang untuk pemrosesan asinkron berkecepatan tinggi dengan fitur teknis sebagai berikut:

### A. Teknologi API Server
* **Asynchronous Engine**: Dibangun di atas **FastAPI** dengan runtime asinkron Python (`async/await`) untuk memproses ribuan request sinkronisasi data siswa secara paralel tanpa memblokir thread.
* **Database ORM**: Menggunakan **SQLAlchemy 2.x** asinkron terhubung ke PostgreSQL, dengan kontrol migrasi skema tabel dinamis menggunakan **Alembic**.
* **Caching & Session Manager**: Menggunakan **Redis** sebagai media caching data kuis yang sering diakses serta memvalidasi masa berlaku OTP.

### B. Index Endpoint Backend Utama
* `GET /api/v1/health` - Health check status koneksi database & redis cache.
* `POST /api/v1/auth/register` - Registrasi akun murid dan pembuatan record profil awal.
* `POST /api/v1/sync/batch` - Endpoint batch penerima sinkronisasi payload offline dari klien seluler.
* `GET /api/v1/materials/digital-library` - Mengambil katalog novel sastra digital yang telah dioptimalkan kompresinya.
* `GET /api/v1/monitoring/classroom-progress` - Rekap data keaktifan murid untuk dikirimkan ke web panel guru.

---

## 🤖 5. Modul Kecerdasan Buatan (Predictive AI Engine Detail)

Modul AI Litera-AI terpisah dalam package independen untuk memudahkan deployment mikro/serverless:

### A. Knowledge Tracing (KT)
* Memprediksi peluang keberhasilan murid menjawab suatu kategori soal (misal: penafsiran majas, penjelasan kosakata arkais) berdasarkan data historis pengerjaan latihan mereka menggunakan model klasifikasi Bayesian kognitif sederhana.

### B. Dynamic Difficulty Adjustment (DDA)
* Algoritma penyesuaian kesulitan otomatis yang berjalan setiap siswa menyelesaikan satu sub-kuis:
  - **Input**: Akurasi jawaban (%) dan durasi rata-rata pengerjaan soal.
  - **Logika**: Jika akurasi > 85% dengan durasi cepat, tingkat kognitif soal berikutnya ditingkatkan. Jika akurasi < 50%, tingkat kognitif diturunkan (DDA Decision Tree).
  - **Output**: ID set kuis berikutnya yang paling ideal dengan kondisi mental dan kompetensi siswa saat ini.

### 📦 5.5. Daftar Dependensi & Pustaka Utama (Monorepo Dependencies)

Monorepo Litera-AI membagi dependensi berdasarkan masing-masing modul untuk menjaga isolasi kode yang rapi:

#### 📱 Modul Mobile (Flutter/Dart)
| Library | Peran & Alasan Penggunaan (Purpose) |
|---|---|
| `flutter_riverpod` | State management reaktif yang modular dan aman dari memory leaks. |
| `go_router` | Routing berbasis deklaratif untuk mempermudah navigasi berproteksi auth guard. |
| `hive` & `hive_flutter` | Database NoSQL lokal yang sangat ringan dan cepat untuk caching offline-first. |
| `connectivity_plus` | Memantau perubahan konektivitas internet siswa secara real-time. |
| `http` | Melakukan request asinkron ke server FastAPI. |

#### ⚡ Modul Backend (FastAPI/Python)
| Library | Peran & Alasan Penggunaan (Purpose) |
|---|---|
| `fastapi` | RESTful API server asinkron dengan dokumentasi OpenAPI otomatis. |
| `sqlalchemy` | ORM asinkron terpopuler untuk interaksi data PostgreSQL. |
| `alembic` | Generator migrasi otomatis untuk melacak perubahan skema database. |
| `redis` | Caching token OTP JWT dan status pengerjaan kuis jangka pendek. |

#### 🤖 Modul AI Engine (Python)
| Library | Peran & Alasan Penggunaan (Purpose) |
|---|---|
| `numpy` | Pemrosesan matriks probabilitas kognitif siswa secara cepat. |
| `scipy` | Perhitungan statistik lanjutan untuk model evaluasi kognitif. |

---

## 🚀 6. Panduan Instalasi Lengkap (Setup & Installation)

### 💻 A. Menjalankan Aplikasi Mobile (Flutter)
1. Buka folder mobile:
   ```bash
   cd apps/mobile
   ```
2. Ambil seluruh paket library Dart dependencies:
   ```bash
   flutter pub get
   ```
3. Pastikan emulator Android/iOS Anda aktif, lalu jalankan aplikasi:
   ```bash
   flutter run
   ```

### ⚡ B. Menjalankan Backend API (FastAPI) Secara Lokal
1. Pindah ke direktori backend dan buat virtual environment Python:
   ```bash
   cd apps/backend
   python -m venv .venv
   source .venv/bin/activate  # OS Windows: .venv\Scripts\activate
   ```
2. Instal package backend beserta dependensi development:
   ```bash
   pip install -e ".[dev]"
   ```
3. Konfigurasikan file environment `.env` di dalam folder backend:
   ```env
   DATABASE_URL="postgresql+asyncpg://postgres:postgres123@localhost:5432/litera_backend_db"
   REDIS_URL="redis://localhost:6379/0"
   ```
4. Jalankan server lokal:
   ```bash
   uvicorn app.main:app --reload
   ```

### 🐳 C. Deployment Menggunakan Docker Compose (Sangat Direkomendasikan)
Untuk menjalankan seluruh ekosistem backend, database PostgreSQL, Redis, dan reverse proxy Nginx secara instan di server produksi atau lokal:
```bash
cd infra/docker
docker-compose up -d --build
```

---

## 📐 7. Diagram Arsitektur Sistem (System Architecture Diagram)

Alur integrasi asinkron antar komponen monorepo didokumentasikan dalam diagram arsitektur tingkat tinggi berikut:

```mermaid
graph TD
    subgraph Client_Space [Client Space]
        A[Flutter Mobile Client] -->|offline cache| B[(Hive Local Cache)]
        A -->|API Requests| C[Nginx Reverse Proxy]
    end
    subgraph Backend_Server [Backend Server]
        C -->|routes to /api/v1| D[FastAPI Backend Server]
        D -->|asynchronous ORM| E[(PostgreSQL Database)]
        D -->|session caching| F[(Redis Cache)]
    end
    subgraph AI_Engine [AI Engine]
        D -->|triggers KT & DDA| G[Predictive AI Engine]
        G -->|Knowledge Tracing / DDA decisions| D
```

### 🎬 7.5. Skenario Simulasi Penggunaan Ekosistem (System Simulation Scenarios)

Untuk memberikan gambaran yang lebih jelas tentang bagaimana data mengalir di platform ini, berikut adalah dua skenario penggunaan utama:

#### Skenario A: Pembuatan Kuis Otomatis oleh Guru
1. **Pilihan Novel**: Guru masuk ke `/guru/materials` dan memilih naskah novel klasik *Siti Nurbaya*.
2. **AI Generation**: Guru mengklik tombol "Buat Kuis dengan AI". Tindakan ini memicu pemrosesan template prompt kognitif di `server/ai/prompt-registry.ts`.
3. **Penyimpanan JSON**: API Gemini membalas dengan struktur array soal kuis (soal, pilihan jawaban, kunci, tingkat Bloom). Soal disimpan dalam field `Quiz.questions` berformat JSON di database PostgreSQL melalui Prisma.
4. **Push Notification**: Sistem memberitahu seluruh siswa kelas tersebut melalui WebSocket/Polling bahwa kuis membaca baru telah tersedia.

#### Skenario B: Pengambilan Asesmen oleh Siswa dan Analisis Guru
1. **Pengerjaan Soal**: Siswa menyelesaikan kuis di aplikasi mobile. Data nilai, tingkat kesulitan, dan durasi pengerjaan dikirim ke server.
2. **Pembaruan Profil**: Server memproses dan memperbarui record `StudentProgress` (misalnya, mengubah status tingkat membaca siswa dari "Pemula" menjadi "Menengah").
3. **Visualisasi Dashboard**: Guru membuka `/guru/reports` dan melihat chart dispersi nilai kelas terupdate, lengkap dengan identifikasi klaster siswa yang mengalami kesulitan membaca.
4. **Rekomendasi Orang Tua**: Wali murid masuk ke `/orang-tua` dan menerima instruksi taktis berbasis AI: *"Siswa mengalami kesulitan memahami majas sarkasme di Novel Salah Asuhan. Mohon dampingi dengan membacakan teks halaman 45-50 bersama."*

---

## 🎯 8. Kesimpulan & Rencana Masa Depan (Conclusion & Roadmap)

**LITERA-AI Monorepo** menyatukan kecepatan pengembangan lintas platform Flutter, kestabilan pemrosesan data asinkron FastAPI, serta akurasi klasifikasi mesin AI ke dalam sebuah kesatuan kode yang modular. Ekosistem ini tidak hanya tangguh dalam menghadapi variabilitas koneksi internet berkat skema *offline-first storage* yang solid, namun juga menjamin keandalan pengolahan data kognitif literasi siswa demi memajukan mutu pendidikan di Indonesia.

### 📌 Peta Jalan Masa Depan (Monorepo Roadmap):
* **Fase 1 (Selesai)**: Struktur monorepo modular, implementasi Hive local storage dengan sync queue worker di Flutter, API Endpoint asinkron FastAPI, dan decision logic DDA AI.
* **Fase 2 (Selesai)**: Implementasi penuh orkestrasi Docker Compose dan setup CI/CD GitHub Actions (`ci.yml` & `release.yml` untuk pembuatan APK otomatis saat rilis, serta `docker-publish.yml` untuk otomatisasi publikasi paket Docker di GitHub Packages).
* **Fase 3 (Mendatang)**: Integrasi Speech-to-Text berbasis AI di mobile client guna mendukung asesmen membaca nyaring secara interaktif langsung pada perangkat Android dan iOS.
