# Grace Shop — Aplikasi Android (Flutter)

Aplikasi kasir (POS) Android untuk Grace Shop, terhubung langsung ke backend
yang sudah live di Railway:

- **Backend:** https://projectportofolio-production.up.railway.app
  (Node.js + TiDB MySQL, kode di repo `vikysimboh/projectportofolio`)
- **Paket:** `com.vikysimboh.graceshop`
- **Bahasa UI:** Bahasa Indonesia
- **Tema:** biru-putih Grace Shop (`#2563eb`)

## Fitur

- **Login** — nama pengguna + kata sandi, sesi cookie tersimpan
  (tetap login walau aplikasi ditutup; sesi server berlaku 24 jam).
  Akun admin pertama dibuat lewat halaman `/setup` di server bila belum ada.
- **Kasir** — grid produk, cari + saring kategori, ketuk untuk masuk
  keranjang, ubah jumlah, pilih metode bayar (Tunai / QRIS / Transfer /
  Kartu debit), checkout ke `POST /api/checkout`.
- **Produk** — daftar + stok; admin bisa tambah/ubah/hapus, kasir
  hanya melihat.
- **Transaksi** — daftar transaksi, cari, lihat detail, admin bisa
  membatalkan transaksi (stok dikembalikan server).
- **Laporan** (admin) — pendapatan & transaksi hari ini, ringkasan
  7/30/90 hari dari `GET /api/report`, produk terlaris, per metode bayar,
  penjualan harian.
- **Keluar** — tombol logout di AppBar; sesi server ikut dihapus.

Semua data berasal dari API live — tidak ada data contoh di dalam aplikasi.

## Menjalankan

```bash
flutter pub get
flutter run
```

## Membangun APK

```bash
flutter build apk --release
# Hasil: build/app/outputs/flutter-apk/app-release.apk
```

APK release ditandatangani dengan kunci debug bawaan Flutter bila belum
dikonfigurasi kunci rilis sendiri — cukup untuk dipasang di HP sendiri,
belum cocok untuk diunggah ke Google Play (butuh kunci rilis + App Bundle).

### Membangun ulang di VM ini (catatan lingkungan)

Toolchain sudah terpasang di VM ini (persisten di home dir):

- Flutter 3.35.5 + Dart 3.9.2 di `~/flutter`
- JDK Temurin 17.0.21 di `~/jdk-17.0.21+9`
- Android SDK di `~/android-sdk` (cmdline-tools, platform-tools 37.0.3,
  platform 35 + 36, build-tools 35.0.0 + 36.0.0, NDK 27.0.12077973,
  CMake 3.22.1)
- Gradle 8.12 sudah di-seed di `~/.gradle/wrapper/dists/` (wrapper jar
  proyek ini versi 2.10 — direktori dist memakai hash MD5 base-36 dari
  URL, `ejduaidbjup3bmmkhw3rie4zb`, plus file `.ok`)

Build di VM ini butuh tiga hal khusus (semuanya sudah terbukti):

1. **JVM harus pakai IPv4** — socket IPv6-mapped (`::ffff:127.0.0.1`)
   dicegat runtime VM sehingga daemon Gradle dan unduhan gagal.
   Set `JDK_JAVA_OPTIONS="-Djava.net.preferIPv4Stack=true"` dan
   `GRADLE_OPTS="-Djava.net.preferIPv4Stack=true"`.
2. **Proxy egress** — Java tidak membaca `https_proxy` dari env.
   `~/.gradle/gradle.properties` harus berisi `systemProp.http(s).proxyHost`
   (`hatch-egress-proxy:3128`, user `hatch-runtime`) — dan kata sandi
   proxy **berotasi tiap sesi exec**, jadi tulis ulang file itu dengan
   kata sandi dari `$https_proxy` saat ini SEBELUM menjalankan build.
3. **CA TLS proxy** — sertifikat CA bundle hatch sudah diimpor ke
   `~/jdk-17.0.21+9/lib/security/cacerts` (alias `hatch-ca-*`); tanpa
   ini unduhan dari `dl.google.com` gagal `PKIX path building failed`.
   Bila JDK diganti, impor ulang dari `/run/hatch/egress-tls/ca-bundle.pem`.

Perintah build lengkap di VM ini:

```bash
export PATH="$HOME/flutter/bin:$HOME/jdk-17.0.21+9/bin:$PATH"
export JAVA_HOME=$HOME/jdk-17.0.21+9
export ANDROID_HOME=$HOME/android-sdk ANDROID_SDK_ROOT=$HOME/android-sdk
export GRADLE_USER_HOME=$HOME/.gradle
export GRADLE_OPTS="-Djava.net.preferIPv4Stack=true"
export JDK_JAVA_OPTIONS="-Djava.net.preferIPv4Stack=true"
flutter build apk --release
```

Juga: `flutter pub get` biasa macet di VM ini (klien HTTP Dart tidak
bisa menjangkau pub.dev lewat proxy); dependensi sudah di-seed di
`~/.pub-cache` — gunakan `flutter pub get --offline`. `flutter doctor`
macet di pemeriksaan adb — lewati saja, build langsung.

## Struktur kode

```
lib/
  main.dart               # Tema + pemulihan sesi saat aplikasi mulai
  models/models.dart      # Product, AppTransaction, AppState, Report, ...
  services/api.dart       # Klien API + cookie jar (kasirku_session)
  utils/format.dart       # formatRupiah, formatTanggal
  screens/
    login_screen.dart
    home_screen.dart      # AppBar + navigasi bawah 4 tab + logout
    kasir_screen.dart
    produk_screen.dart
    transaksi_screen.dart
    laporan_screen.dart
test/
  api_parsing_test.dart   # Tes parsing JSON bentuk server
```

## Catatan API (dari server.js)

- Autentikasi memakai cookie `kasirku_session` (HttpOnly, 24 jam).
  Sesi disimpan di memori server — bila server Railway di-restart,
  sesi lama hangus dan aplikasi kembali ke layar login (401).
- `GET /api/state` -> `{products, transactions, stats, user}`
- `POST /api/checkout` -> body `{items: [{productId, qty}], customer, payment}`,
  payment wajib: Tunai, QRIS, Transfer, atau Kartu debit.
- `GET /api/transactions?limit=&offset=&search=`
- `POST /api/transactions/{id}/cancel` (admin)
- `GET /api/report?period=30` (admin)
- Produk: `POST /api/products`, `PUT /api/products/{id}`,
  `DELETE /api/products/{id}` (admin; hapus ditolak bila produk pernah
  masuk transaksi).
