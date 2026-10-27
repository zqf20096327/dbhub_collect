# SIPASD - Sistem Informasi Pengelolaan Arsip Surat Dispora
**Dinas Kepemudaan dan Olahraga Provinsi Kalimantan Selatan**  
*Klasifikasi: Repositori E-Arsip Surat Digital Berbasis Web Responsif - Kerja Praktik TI UNISKA*

[![CI Status](https://github.com/Dhani078/SIPASD/actions/workflows/ci.yml/badge.svg)](https://github.com/Dhani078/SIPASD/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Framework: Next.js 15](https://img.shields.io/badge/Framework-Next.js%2015-black.svg)](https://nextjs.org/)
[![Database: TiDB Serverless](https://img.shields.io/badge/Database-TiDB%20Serverless-blue.svg)](https://tidb.cloud/)
[![Storage: Cloudinary & Google Drive](https://img.shields.io/badge/Storage-Cloudinary%20%26%20Drive-blue.svg)](https://cloudflare.com/)
[![Live URL: sipasd.my.id](https://img.shields.io/badge/Live-sipasd.my.id-047857.svg)](https://www.sipasd.my.id)

> **Live Production**: [https://www.sipasd.my.id](https://www.sipasd.my.id) *(Mirror: [https://sipasd.vercel.app](https://sipasd.vercel.app))*

---

## 🏛️ Latar Belakang & Masalah Riil Google Drive
Sekretariat Dispora Provinsi Kalimantan Selatan (Jalan Pramuka No. 4 Banjarmasin) menyimpan arsip surat hasil pindaian (*scan*) pada akun Google Drive `arsipdispora2026` (folder `sistem magang`). 

Kondisi eksisting penyimpanan Google Drive:
1. Berkas PDF hanya ditumpuk dalam folder `Surat Masuk 2026` (171 file) dan `Surat Keluar 2026` (249 file) tanpa metadata terstruktur.
2. Penamaan file manual acak (contoh: `0973(14 Agustus 2026).pdf`, `4302(1).pdf`, `7480-82, 3 surat_20260902_0001.pdf`).
3. Google Drive tidak memiliki filter klasifikasi dinas (Permendagri/Pergub), tidak ada pencatatan riwayat disposisi fisik pimpinan, dan tidak bisa mengekspor buku agenda resmi kedinasan.
4. Temu-kembali dokumen memakan waktu **15-30 menit** karena staf harus membuka satu per satu file PDF untuk mengetahui isinya.

**SIPASD** hadir sebagai **Katalog Repositori E-Arsip Digital Terindeks**. Sistem mengintegrasikan seluruh 420+ arsip riil TA 2026 ke dalam basis data cloud berindeks, memotong waktu temu-kembali dokumen menjadi **< 2 detik** via peramban HP dan PC.

---

## 👥 Matriks Hak Akses Pengguna (RBAC)

| Role | Identitas Akun | Peruntukan Jabatan | Hak Akses & Wewenang |
| :--- | :--- | :--- | :--- |
| **Super Admin** | `pengarsip` / `developer` | Pemberi Tugas / Developer | Manajemen akun, master klasifikasi surat, konfigurasi sistem, audit trail. |
| **Petugas Arsip** | `tu_umum` | Staf Tata Usaha / Arsiparis | Pengindeksan arsip surat baru, input metadata disposisi fisik, ekspor buku agenda. |
| **Pimpinan** | `kadis` / `sekretaris` | Kepala Dinas / Sekretaris | Pencarian cepat dokumen, monitoring volume arsip dinas, rekapitulasi agenda. |
| **Bidang / Seksi** | `kabid_pora` / `subbag_keuangan` | Kepala Bidang / Kasubbag | Pencarian dan pratinjau arsip surat disposisi sesuai bidang tugasnya. |

### Identitas Akun Pengguna

| Username | Hak Akses Kedinasan | Nama Aparatur | Tingkat Peran (RBAC) | Jabatan Struktural / Fungsional |
|----------|---------------------|---------------|----------------------|---------------------------------|
| `pengarsip` | Dikelola Staf TU | Rana Nur Syifa | SUPER_ADMIN | Analis Anggaran - Sekretariat (Pengelola Arsip Digital) |
| `developer` | Khusus Pengembang | Muhammad Rizki Ramadhani | SUPER_ADMIN | Mahasiswa Magang TI UNISKA (Developer) |
| `admin` | Administrator IT | Administrator IT Dispora | SUPER_ADMIN | Pranata Komputer Ahli Pertama |
| `kadis` | Pimpinan Dinas | Pebriadin Hapiz, AP, M.Si | PIMPINAN | Kepala Dinas Kepemudaan dan Olahraga |
| `tu_umum` | Petugas Kearsipan | Staf Agenda TU Dispora | PETUGAS_ARSIP | Pengadministrasi Persuratan |
| `subbag_keuangan` | Verifikator Keuangan | Norika Fajriana, SH, MH | BIDANG | Kasubbag Perencanaan & Keuangan |
| `kabid_pora` | Kepala Bidang Teknis | Budiono, S.Pd, M.AP | BIDANG | Kepala Bidang Pembudayaan Olahraga |

Kata sandi setiap akun kedinasan disimpan dalam bentuk salted hash Bcrypt dan dirahasiakan untuk menjaga integritas data kearsipan daerah.

---

## 🚀 Fitur Utama Sistem E-Arsip

### 1. Katalog & Pencarian Multi-Filter Instan (< 2 Detik)
- Mesin pencari cepat berbasis kata kunci: Nomor Surat, Nomor Agenda, Asal/Tujuan Instansi, Perihal, Ringkasan, dan Kode Klasifikasi.
- Filter berdasarkan rentang tanggal surat/diterima dan status sifat surat (*Biasa, Penting, Segera, Kilat*).
- Nomor surat, tanggal, asal/tujuan instansi, dan perihal diisi dari isi berkas PDF asli (bukan nilai contoh). Rincian metode dan cakupannya ada di `docs/METADATA_DARI_PDF.md`.

### 2. Built-in In-Browser PDF Streaming Viewer
- Membaca dokumen PDF pindaian langsung di layar peramban tanpa wajib mengunduh file fisik.
- Dukungan mode *Split-Screen View* pada komputer kerja (tabel metadata di kiri, viewer PDF di kanan).
- Mode kartu responsif dan pratinjau nyaman di layar ponsel pintar (*smartphone*).

### 3. Dokumentasi Riwayat Disposisi Fisik
- Mencatat dokumentasi lembar disposisi kertas yang sudah ditandatangani basah pimpinan: pejabat pendisposisi, tanggal disposisi, bidang tujuan, instruksi tertulis, dan catatan khusus.
- Nama pejabat pendisposisi diisi dari isi berkas PDF asli (alamat tujuan dan badan surat), bukan nilai seragam. Rincian metode dan sebarannya ada di `docs/DISPOSISI_DARI_PDF.md`.
- Fitur cetak ulang salinan Lembar Disposisi standar Pemprov Kalsel.

### 4. Manajemen Klasifikasi & Jadwal Retensi Arsip (JRA)
- Pengelompokan kode klasifikasi dinas standar Permendagri / Pergub Kalsel:
  * `005` (Undangan)
  * `045` (Kearsipan)
  * `426` (Keolahragaan)
  * `427` (Kepemudaan)
  * `800` (Kepegawaian)
  * `900` (Keuangan)
- Informasi masa retensi aktif dan inaktif dokumen arsip negara.

### 5. Riwayat Disposisi Fisik (Status Tracking Real-time)
- Halaman khusus monitoring status penyelesaian disposisi surat: **Belum Diproses, Sedang Proses, Selesai**.
- Filter status dengan counter live per kategori.
- Search engine multi-kolom: nomor agenda, perihal, instansi, pejabat, bidang tujuan.
- Badge warna status (merah = Belum Diproses, kuning = Proses, hijau = Selesai).

### 6. Distribusi Ekspedisi (Buku Ekspedisi Surat Keluar)
- Pencatatan distribusi pengiriman surat keluar: tanggal kirim, nama kurir pengirim, nama penerima, telepon, catatan.
- Tabel 241 surat keluar TA 2026 dengan modal form "Catat Distribusi".
- Ekspor Buku Ekspedisi ke Excel untuk laporan kedinasan.

### 7. 5 Tombol Aksi Dokumen Tabel & Fitur Edit Arsip
- Setiap baris tabel arsip memiliki 5 tombol aksi dokumen: **Lihat PDF** (streaming CDN), **Unduh** (unduh langsung file fisik), **Disposisi** (cetak lembar disposisi), **Edit** (ubah metadata & disposisi), dan **Hapus**.
- Modal pengeditan metadata naskah (`EditLetterModal.tsx`) terhubung langsung ke endpoint `PUT /api/letters` dan mutasi TiDB Cloud secara real-time.

### 8. Filter Tahun Cerdas & Maxx Mode Responsif
- Dropdown tahun fleksibel: Tahun Berjalan (2026, 2025, 2024), Tahun Masa Depan (2027-2200), Rentang Historis (2000-2020, < 2000), dan input kustom bebas.
- Maxx Mode pada ponsel pintar (< 768px) dan iPad/tablet (768px - 1024px) dengan breakpoint drawer 992px, 100vw x 100dvh PDF viewer, dan proteksi 0 overflow horizontal.

### 9. Ekspor Buku Agenda Otomatis (Format Excel .xlsx)
- Ekspor rekapitulasi Buku Agenda Surat Masuk dan Surat Keluar ke format spreadsheet Microsoft Excel resmi sesuai format baku laporan pertanggungjawaban dinas.
- 11 kolom standar: No. Agenda, Jenis, Nomor Surat, Tanggal, Asal/Tujuan, Perihal, Sifat, Venue, Bidang, Instruksi Disposisi, Catatan.
- Header hijau Dispora, freeze pane row 1, auto-filter aktif.

### 10. Backup Otomatis Ganda (Cloudinary + Google Drive)
- **Cloudinary CDN**: Storage primer untuk streaming preview PDF instan (signed URL anti-401).
- **Google Drive**: Backup sekunder via OAuth 2.0 ke folder dinas (Surat Masuk: 420+ file, Surat Keluar: 241 file).
- Retry logic 2x dengan exponential backoff untuk reliability 99%.
- Fallback URL folder jika upload gagal setelah 2 retry.

---

## 🛠️ Tumpukan Teknologi (Cloud-Native & Zero Cost)

- **Frontend & Fullstack**: Next.js 15 (App Router, React 19, TypeScript).
- **Styling**: Tailwind CSS v4 (Responsif Mobile & PC, 0 Horizontal Overflow).
- **Basis Data**: TiDB Cloud Serverless (MySQL Compatible, SSL Strict, Gratis 25 GB).
- **Penyimpanan Dokumen**: Cloudinary CDN (primer untuk streaming pratinjau instan) & Google Drive (sekunder via OAuth 2.0 akun dinas kuota 5 TB, 420 berkas fisik tersimpan 100%).
- **Hosting Publik**: Vercel Edge Network (HTTPS Otomatis, Domain Resmi https://www.sipasd.my.id).

---

## 🧪 Testing & Quality Assurance

### Unit & Integration Tests
```bash
npm test
```
Test suite verifikasi 6 dimensi:
1. **TiDB Connection**: 170 Surat Masuk, 241 Surat Keluar, 5 Users, 5 Bidang, 6 Klasifikasi
2. **Cloudinary Signed URL**: Anti-401 streaming signature valid
3. **Code Modular Ratio**: Semua 58 files ≤ 200 LOC (zero god objects)
4. **Zero Em-Dash Invariant**: 0 em-dash di 108 project files (readability)
5. **Security Headers**: API auth guards aktif di gateway & routes
6. **Zero Hardcoded Secrets**: Semua credentials via env vars

### E2E Production Tests
```bash
python tests/e2e/production-test.py
```
Browser automation (Playwright) test 8 skenario real user:
1. Login & cookie persistence
2. Dashboard stats load
3. Upload surat masuk baru (PDF + metadata)
4. PDF preview & GDrive backup link
5. Cetak lembar disposisi
6. Distribusi ekspedisi (surat keluar)
7. Riwayat disposisi (filter status + search)
8. Ekspor Buku Agenda Excel

**Output**: 8 screenshots bukti di `tests/e2e/screenshots/`

---

## 📋 Environment Variables (Production)

Tambahkan di Vercel Dashboard → Project Settings → Environment Variables:

```env
# Database
DATABASE_URL="mysql://user:pass@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/sipasd?ssl=true"

# Auth
JWT_SECRET="random-256-bit-secret"

# Cloudinary CDN (PDF Streaming Primer)
CLOUDINARY_CLOUD_NAME="your-cloud-name"
CLOUDINARY_API_KEY="123456789012345"
CLOUDINARY_API_SECRET="AbCdEfGhIjKlMnOpQrStUvWxYz"

# Google Drive OAuth 2.0 (Backup Sekunder)
GOOGLE_CLIENT_ID="402272632756-xxxx.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET="GOCSPX-xxxxxxxxxxxxx"
GOOGLE_REFRESH_TOKEN="1//0gwBpFFHSqFKICgYIARAAGBASNwF-L9Irnxxx"
GOOGLE_DRIVE_SM_FOLDER_ID="1deTFD7oICTXkkMs5HzS-bhtZzvCqfW9n"
GOOGLE_DRIVE_SK_FOLDER_ID="1rgWCFwULt8awBCVIuomy7cELKqEtbdkx"
```

---

## 📦 Struktur Repositori

```
SIPASD/
├── docs/
│   ├── BAB_1_PENDAHULUAN_DRAFT.md    # Naskah Laporan Magang Bab I
│   ├── BAB_2_PROFIL_INSTANSI_DRAFT.md# Naskah Laporan Magang Bab II
│   ├── BAB_3_ANALISIS_PERANCANGAN_DRAFT.md # Naskah Laporan Magang Bab III
│   ├── BAB_4_IMPLEMENTASI_PENGUJIAN_DRAFT.md # Naskah Laporan Magang Bab IV
│   ├── BAB_5_PENUTUP_DRAFT.md        # Naskah Laporan Magang Bab V
│   ├── DAFTAR_PUSTAKA.md             # Rujukan Format APA 7th Edition
│   ├── DATABASE_SCHEMA.md            # Kamus Data & SQL DDL 8 Tabel
│   ├── UML_DIAGRAMS.md               # Use Case, Activity, Sequence, Class Diagram
│   ├── SECURITY_AUDIT.md             # Matriks OWASP Top 10 & Validasi PDF
│   ├── SOP_KEDINASAN.md              # 5 SOP Pengelolaan Arsip Dispora
│   ├── SKRIPSI_UPGRADE_ROADMAP.md    # Blueprint Skripsi S1 (OCR & Naive Bayes)
│   ├── DEPLOYMENT_GUIDE.md           # Panduan Deployment Cloud Zero Cost
│   └── IMPORT_MIGRATION_GUIDE.md     # Skrip Import 420 Berkas Riil PDF
├── AGENT.md                          # Panduan Agen Otonom & Aturan Zero-Slop
├── SPEC.md                           # Dokumen Spesifikasi Resmi
├── task_plan.md                      # Rencana Kerja Bertahap
├── findings.md                       # Analisis Data Riil Google Drive Dispora
├── progress.md                       # Log Catatan Kronologis Pengerjaan
└── README.md                         # Dokumentasi Utama Ini
```

---

## 👨‍💻 Kontributor & Pengembang Tunggal (Sole Contributor)

Proyek ini dirancang, dibangun, dan dipelihara secara mandiri (100% Solo Project) oleh satu-satunya pengembang:

* **Nama Lengkap**: Muhammad Rizki Ramadhani
* **NPM**: 2310010406
* **Program Studi**: S1 Teknik Informatika, Fakultas Teknologi Informasi
* **Perguruan Tinggi**: Universitas Islam Kalimantan (UNISKA) Muhammad Arsyad Al Banjari Banjarmasin
* **Akun GitHub**: [@Dhani078](https://github.com/Dhani078)
* **Email Resmi**: dhanisepeda@gmail.com
* **Instansi Magang**: Sekretariat Dinas Kepemudaan dan Olahraga Provinsi Kalimantan Selatan
* **Peran**: Lead Software Engineer, System Architect & Sole Contributor

> **Catatan Integritas Akademik & Repositori**: Repositori ini dikembangkan secara individual sebagai produk Kerja Praktik (Magang). Seluruh komit, penulisan kode, perancangan basis data, integrasi cloud, dan naskah dokumentasi dibuat secara mandiri tanpa kontributor lain.

---

## 👤 Informasi Mahasiswa
- **Nama**: Muhammad Rizki Ramadhani
- **NPM**: 2310010406
- **Program Studi**: S1 Teknik Informatika - Fakultas Teknologi Informasi
- **Perguruan Tinggi**: Universitas Islam Kalimantan (UNISKA) MAB Banjarmasin
- **Instansi Magang**: Sekretariat Dinas Kepemudaan dan Olahraga Provinsi Kalimantan Selatan
- **Tahun**: 2026
