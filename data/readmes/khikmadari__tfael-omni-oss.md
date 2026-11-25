# TFAEL-OMNI v2.0

**Bahasa Indonesia** | [English](README.en.md)

Dibuat oleh [khikmadari](https://github.com/khikmadari).

TFAEL-OMNI adalah platform pusat komando terpadu (single pane of glass). Satu layar memadukan peta taktis, OSINT, analisis intelijen, pemantauan keamanan siber, forensik digital, dan aplikasi agen lapangan Android. Seluruh sistem dijalankan di komputer atau server sendiri (self-hosted).

> **Status: prototipe.** Proyek ini dibuat oleh tim TFAEL Labs untuk Kartika Cyber Hackathon 2026 dan kini dibuka sebagai open source agar dapat dikembangkan bersama. Baca bagian [Batasan saat ini dan peta jalan](#batasan-saat-ini-dan-peta-jalan) sebelum memakainya untuk keperluan sungguhan.

## Tampilan

TFAEL-OMNI menghimpun informasi dari sumber terbuka (open-source intelligence, OSINT) dan menyajikannya sebagai satu gambaran umum situasi.

![Layar pembuka: bola dunia berputar menuju Indonesia, disertai ringkasan berita, gempa, dan peringatan cuaca](docs/img/00-pembuka.jpg)

Layar pembuka yang tampil setelah login.

| SITREP | C4ISR |
|---|---|
| ![SITREP: sebaran gempa dan peringatan cuaca pada peta Indonesia](docs/img/01-sitrep.jpg) | ![C4ISR: peta taktis dengan unit lapangan](docs/img/02-c4isr.jpg) |
| **OSINT Profiler** | **SIEM** |
| ![OSINT Profiler: hasil penelusuran pelat nomor contoh](docs/img/03-osint.jpg) | ![SIEM: antrean alert dengan teknik MITRE ATT&CK](docs/img/04-siem.jpg) |
| **DFIR** | **Intel Graph** |
| ![DFIR: chain of custody dengan hash berantai](docs/img/05-dfir.jpg) | ![Intel Graph: jaringan keterkaitan antarentitas](docs/img/06-intel-graph.jpg) |
| **BotRadar** | **Admin** |
| ![BotRadar: skor bot tiap akun pada data demo](docs/img/07-botradar.jpg) | ![Admin: tabel izin tiap peran](docs/img/08-admin.jpg) |

Aplikasi agen Android dengan peta 2D dan 3D:

<p>
  <img src="docs/img/09-android-2d.jpg" width="250" alt="Aplikasi agen Android: peta 2D">
  <img src="docs/img/10-android-3d.jpg" width="250" alt="Aplikasi agen Android: peta 3D">
</p>

## Daftar Isi

- [Fitur](#fitur)
- [Teknologi](#teknologi)
- [Instalasi](#instalasi)
  - [macOS](#macos)
  - [Windows](#windows)
  - [Docker](#docker)
- [Login pertama](#login-pertama)
- [Panduan penggunaan](#panduan-penggunaan)
- [Fitur opsional](#fitur-opsional)
- [Aplikasi Android dan radio](#aplikasi-android-dan-radio)
- [Konfigurasi](#konfigurasi)
- [Struktur proyek](#struktur-proyek)
- [Batasan saat ini dan peta jalan](#batasan-saat-ini-dan-peta-jalan)
- [Berkontribusi](#berkontribusi)
- [Lisensi](#lisensi)
- [Disclaimer](#disclaimer)

## Fitur

| Modul | Fungsi |
|---|---|
| **C4ISR** | Peta taktis, pelacakan unit, geofence, geolokasi menara seluler, triangulasi Cell-ID dengan metode least-squares, dan analisis CCTV publik. |
| **OSINT** | Penelusuran sembilan jenis indikator: domain, alamat IP, surel, nomor telepon, nama orang, nama pengguna, pelat nomor kendaraan, koordinat, dan URL. |
| **Intel Graph** | Knowledge graph, pattern of life, dan skor risiko sasaran. |
| **SIEM siber-fisik** | Aturan deteksi dengan pemetaan MITRE ATT&CK, deteksi impossible travel, dan playbook SOAR. |
| **Forensik digital** | Evidence vault dengan hash chain, pemeriksaan EXIF dan ELA, YARA rules, serta berita acara dalam bentuk PDF. |
| **Media sosial** | Pengambilan data Twitter/X dan deteksi Coordinated Inauthentic Behavior (CIB). |
| **SITREP** | Berita daring, gempa, dan peringatan dini cuaca BMKG pada satu peta. |
| **Agen lapangan** | Aplikasi Android untuk melaporkan posisi, baterai, dan sinyal seluler, dengan peta 2D dan 3D. |

Sebagian fitur memanggil layanan luar, yaitu OpenCellID/Unwired Labs, BMKG, GeoIP, dan media sosial. Sebagian besar panggilan keluar dari server dapat dimatikan dengan `OMNI_AIRGAP=1`.

## Teknologi

| Bagian | Teknologi |
|---|---|
| Server | Python (server HTTP dari standard library) dan SQLite |
| Antarmuka web | React, TypeScript, dan Vite |
| Aplikasi Android | Kotlin, osmdroid (peta 2D), dan MapLibre GL JS (peta 3D) |

## Instalasi

Perangkat lunak yang perlu disiapkan:

| Perangkat lunak | Versi | Kegunaan |
|---|---|---|
| Python | 3.10 atau lebih baru (disarankan 3.12) | Menjalankan server |
| Node.js | 22 atau lebih baru | Membangun antarmuka web |
| Git | Versi apa pun | Mengunduh kode |

Git boleh dilewati. Sebagai gantinya, klik **Code → Download ZIP** di halaman GitHub, lalu ekstrak berkasnya.

### macOS

Semua perintah dijalankan di aplikasi **Terminal**.

**1. Pasang prasyarat.** Cara termudah adalah [Homebrew](https://brew.sh):

```bash
brew install python@3.12 node git
```

Tanpa Homebrew, unduh pemasang dari [python.org](https://www.python.org/downloads/) dan [nodejs.org](https://nodejs.org/), lalu ganti `python3.12` pada langkah 3 dengan `python3`.

**2. Unduh kode.**

```bash
git clone https://github.com/khikmadari/tfael-omni-oss.git
cd tfael-omni-oss
```

**3. Pasang pustaka Python** di lingkungan terpisah (virtual environment) agar tidak bercampur dengan Python sistem.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements-server.txt
```

**4. Bangun antarmuka web.** Hasilnya ditulis ke folder `frontend/`.

```bash
npm install --prefix tfael-omni
npm run build --prefix tfael-omni
```

**5. Jalankan server.** Ganti sandinya dengan sandi pilihan Anda.

```bash
OMNI_BOOTSTRAP_PASSWORD="ganti-dengan-sandi-anda" python backend/server.py 8080
```

**6. Buka `http://localhost:8080`** di peramban, lalu ikuti bagian [Login pertama](#login-pertama).

Untuk menjalankan server lagi di lain waktu, cukup ulangi `source .venv/bin/activate` dan langkah 5.

### Windows

Semua perintah dijalankan di **PowerShell**. Langkah Windows disusun dari pembacaan kode dan belum diuji langsung oleh tim. Bila ada kendala, laporkan melalui tab Issues.

**1. Pasang prasyarat** dengan winget, yang sudah tersedia di Windows 10 dan 11:

```powershell
winget install Python.Python.3.12
winget install OpenJS.NodeJS.LTS
winget install Git.Git
```

Setelah selesai, tutup PowerShell lalu buka kembali agar perintah baru dikenali. Tanpa winget, unduh pemasang dari [python.org](https://www.python.org/downloads/) (centang **Add python.exe to PATH**), [nodejs.org](https://nodejs.org/), dan [git-scm.com](https://git-scm.com/).

**2. Unduh kode.**

```powershell
git clone https://github.com/khikmadari/tfael-omni-oss.git
cd tfael-omni-oss
```

**3. Pasang pustaka Python** di lingkungan terpisah (virtual environment).

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r backend\requirements-server.txt
```

Bila muncul galat "running scripts is disabled on this system", jalankan perintah berikut lalu ulangi baris kedua:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**4. Bangun antarmuka web.** Hasilnya ditulis ke folder `frontend\`.

```powershell
npm install --prefix tfael-omni
npm run build --prefix tfael-omni
```

**5. Jalankan server.** Ganti sandinya dengan sandi pilihan Anda.

```powershell
$env:PYTHONUTF8 = "1"
$env:OMNI_BOOTSTRAP_PASSWORD = "ganti-dengan-sandi-anda"
python backend\server.py 8080
```

Bila Windows Firewall bertanya, pilih **Allow** hanya untuk jaringan privat. Pilih **Cancel** bila server hanya dibuka dari komputer yang sama.

**6. Buka `http://localhost:8080`** di peramban, lalu ikuti bagian [Login pertama](#login-pertama).

Untuk menjalankan server lagi di lain waktu, cukup ulangi `.venv\Scripts\Activate.ps1` dan langkah 5.

### Docker

Cara ini sama di macOS dan Windows, dan hanya memerlukan [Docker Desktop](https://www.docker.com/products/docker-desktop/). Python dan Node.js tidak perlu dipasang.

```bash
git clone https://github.com/khikmadari/tfael-omni-oss.git
cd tfael-omni-oss
docker build -t tfael-omni .
docker run --rm -p 8080:8080 -e OMNI_BOOTSTRAP_PASSWORD="ganti-dengan-sandi-anda" tfael-omni
```

Data pada cara ini hilang ketika kontainer dihentikan. Tambahkan `-v tfael-data:/data` pada perintah `docker run` agar data tersimpan.

## Login pertama

1. Buka `http://localhost:8080`.
2. Isi **Callsign** dengan `komandan`.
3. Isi **Access Code** dengan sandi yang Anda tetapkan pada `OMNI_BOOTSTRAP_PASSWORD`.

Akun bawaan lain memakai sandi yang sama:

| Callsign | Peran |
|---|---|
| `komandan` | Komandan (akses penuh) |
| `analis.intel` | Analis |
| `operator.c2` | Operator |
| `admin.sistem` | Admin |

Hal yang perlu diketahui:

- `OMNI_BOOTSTRAP_PASSWORD` perlu diset setiap kali server dijalankan. Tanpa variabel itu, sandi dibuat acak dan akun wajib mengganti sandi, sedangkan antarmuka web belum menyediakan formulir ganti sandi.
- Server mengisi data contoh fiktif saat pertama kali menyala. Jalankan dengan `OMNI_DEMO=0` untuk server tanpa data contoh.
- Data tersimpan di `backend/tfael_omni.db`. Hapus berkas itu untuk mengulang dari awal.
- Tekan `Ctrl+C` di Terminal atau PowerShell untuk menghentikan server.

## Panduan penggunaan

Cara memakai tiap ruang kerja dijelaskan langkah demi langkah di [`docs/PANDUAN_PENGGUNAAN.md`](docs/PANDUAN_PENGGUNAAN.md). Panduan itu mencakup SITREP, C4ISR, OSINT Profiler, SIEM, DFIR, Intel Graph, BotRadar, Admin, aplikasi agen Android, dan masalah yang sering muncul.

## Fitur opsional

Fitur berikut hanya aktif bila pustakanya dipasang. Server mendeteksinya sendiri saat menyala.

| Fitur | Yang perlu dipasang |
|---|---|
| Pemindaian YARA rules | `pip install yara-python` |
| OCR (membaca teks pada gambar) | `pip install pytesseract` dan program Tesseract: `brew install tesseract` (macOS) atau `winget install UB-Mannheim.TesseractOCR` (Windows) |
| Transkripsi suara | `pip install faster-whisper` |
| Deteksi objek (YOLO) | `pip install ultralytics` |

## Aplikasi Android dan radio

Aplikasi agen Android dijelaskan di [`android/README.md`](android/README.md). Alamat server bawaan aplikasi perlu diganti dengan alamat server Anda sendiri melalui Pengaturan → Lanjutan. Integrasi radio dijelaskan di [`docs/PANDUAN_RADIO.md`](docs/PANDUAN_RADIO.md).

## Konfigurasi

Server diatur melalui environment variable berikut:

| Variabel | Fungsi | Contoh |
|---|---|---|
| `OMNI_BOOTSTRAP_PASSWORD` | Kata sandi akun bawaan. Bila tidak diset, sandi dibuat acak dan ditampilkan sekali di log saat server menyala. | `Omni#Rahasia2026` |
| `OMNI_AGENT_KEY` | Kunci pra-berbagi untuk perangkat lapangan. Bila kosong, kunci dibuat acak setiap server menyala. | `FIELD-KEY-7a3f...` |
| `OMNI_ALLOWED_ORIGINS` | Daftar origin yang boleh mengakses lintas-asal, dipisah koma. Kosong berarti semua permintaan CORS ditolak. | `https://console.markas.local` |
| `OMNI_LOGIN_MAX_FAILS` | Jumlah gagal login sebelum akun dan IP terkunci sementara (bawaan `5`). | `5` |
| `OMNI_LOGIN_LOCK_SECONDS` | Lama penguncian dalam detik (bawaan `900`, yaitu 15 menit). | `900` |
| `OMNI_AIRGAP` | `1` untuk mematikan panggilan keluar ke GeoIP, BMKG, layanan geolokasi sel, dan media sosial. | `1` |
| `OMNI_DEMO` | `0` untuk server bersih tanpa data contoh. | `0` |
| `OMNI_DEMO_HINT` | `1` untuk membagikan kunci agen ke aplikasi lapangan melalui `/api/v2/agent/demo-key` agar mudah dicoba. Jangan diaktifkan pada server yang dipakai sungguhan. | `1` |
| `OMNI_DB_PATH` | Letak berkas basis data bila ingin disimpan di luar folder kode. | `/data/tfael_omni.db` |

Contoh menjalankan server untuk pemakaian sungguhan di macOS atau Linux:

```bash
OMNI_ALLOWED_ORIGINS="https://console.markas.local" \
OMNI_AGENT_KEY="FIELD-KEY-7a3f91c2" \
OMNI_BOOTSTRAP_PASSWORD="Omni#RahasiaAwal2026" \
OMNI_AIRGAP=1 \
OMNI_DEMO=0 \
python backend/server.py 8080
```

## Struktur proyek

| Folder atau berkas | Isi |
|---|---|
| [`backend/`](backend/) | Server API `/api/v2/*` dan seluruh mesin analisis. Titik masuknya adalah [`backend/server.py`](backend/server.py). |
| [`tfael-omni/`](tfael-omni/) | Kode sumber antarmuka web. Hasil build ditulis ke `frontend/`. |
| [`android/`](android/) | Aplikasi agen lapangan untuk Android. |
| [`deploy/`](deploy/) | Panduan deployment dengan Docker dan Railway. |
| [`tools/`](tools/) | Skrip pendukung, misalnya impor data OpenCellID. |
| [`docs/`](docs/) | Panduan penggunaan dan panduan radio. |

## Batasan saat ini dan peta jalan

- **Hanya data fiktif, sejalan dengan UU PDP.** Repositori ini sengaja tidak memuat data pribadi maupun data operasional sungguhan, sejalan dengan UU No. 27 Tahun 2022 tentang Pelindungan Data Pribadi. Seluruh data bawaan adalah contoh fiktif, dan data sungguhan hanya boleh diolah oleh pihak yang memiliki dasar hukum.
- **Evidence vault masih tahap peragaan.** Pratinjau barang bukti di `frontend/uploads/` belum dilindungi login dan penamaannya mudah ditebak. Jangan menyimpan bukti sungguhan sebelum kontrol akses ini selesai dibuat.
- **Pengaturan ulang sandi dilakukan oleh Admin.** Formulir ganti sandi mandiri untuk akun yang wajib mengganti sandi belum tersedia dan masuk peta jalan.
- **Radio APRS/LoRa menunggu validasi perangkat keras.** Dekodernya sudah tersedia di sisi perangkat lunak, tetapi belum pernah diuji dengan perangkat radio asli.
- **Aplikasi Android diuji otomatis di emulator.** Setiap perubahan aplikasi dibangun dan diuji di GitHub Actions. Pengujian pada beragam ponsel fisik masih terbatas.
- **Data Twitter/X mengutamakan API resmi.** Jalur cadangan melalui Nitter bergantung pada instance publik yang kini banyak tidak aktif.

## Berkontribusi

Kontribusi terbuka untuk siapa saja dengan alur berikut:

1. Fork repo ini, lalu buat branch baru dari `main`.
2. Lakukan perubahan dan jalankan pengujian backend dengan `python -m pytest backend/tests` (memerlukan `pip install pytest`).
3. Kirim pull request yang menjelaskan perubahan beserta alasannya.

Kontribusi yang paling berdampak saat ini:

- **Uji di ponsel Anda.** Pasang aplikasi agen Android di ponsel yang berbeda, lalu laporkan merek, versi Android, dan hasilnya. Kontribusi ini tidak memerlukan kemampuan menulis kode.
- **Jadi penguji Windows pertama.** Ikuti langkah instalasi Windows di README ini, lalu laporkan bagian yang gagal atau kurang jelas.
- **Hidupkan jalur radio.** Uji integrasi APRS/LoRa dengan perangkat radio sungguhan dan bantu menyempurnakan dekodernya.
- **Perkuat pengambilan data Twitter/X.** Perbarui jalur pengambilan data agar tetap andal ketika instance Nitter publik tidak aktif.
- **Tutup dua celah yang sudah diketahui.** Buat formulir ganti sandi mandiri dan lindungi berkas di `frontend/uploads/` dengan login.
- **Kurangi ketergantungan pada data contoh.** Bantu modul yang masih mengandalkan data contoh agar dapat mengolah masukan dari pengguna, lalu lengkapi dokumentasi dan pengujiannya.

Bug dan usulan dapat dilaporkan melalui tab Issues. Panduan lengkapnya ada di [`CONTRIBUTING.md`](CONTRIBUTING.md). Celah keamanan dilaporkan sesuai [`SECURITY.md`](SECURITY.md), bukan melalui issue publik.

## Lisensi

Kode ini dirilis dengan lisensi MIT; lihat berkas [`LICENSE`](LICENSE). Pustaka opsional yang dipasang terpisah mengikuti lisensinya masing-masing, misalnya ultralytics (YOLO) yang berlisensi AGPL-3.0. Font dan data peta pihak ketiga yang ikut di repo ini dicatat di [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## Disclaimer

> [!WARNING]
> TFAEL-OMNI disediakan hanya untuk **tujuan pendidikan**, **riset keamanan yang berizin**, dan **investigasi OSINT yang bersifat defensif**. Pengembang tidak bertanggung jawab atas penyalahgunaan, akibat yang tidak diinginkan, maupun tuntutan hukum yang timbul dari pemakaian perangkat lunak ini.

Pengguna bertanggung jawab penuh atas cara perangkat lunak ini dipakai, termasuk kepatuhan terhadap hukum yang berlaku, misalnya UU ITE dan UU Pelindungan Data Pribadi. Fitur link pelacak (`/checkin`), force GPS ping melalui SMS biner, dan pengambilan data media sosial bersifat dual-use, sehingga hanya boleh dipakai dengan dasar hukum dan izin yang sah.
