# cash_flow
<p><b>Cash Flow Class Adalah Aplikasi Manajemen Uang Kas Berbasis Web Yang Di Bangun Menggunakan Bahasa Pemrogramman PHP+ Mysql Sebagai DBMS.
  Menggunakan Admin SB-2 Sebagai Admin Template, Source Ini Hanya Untuk Media Belajar Saja Dan Tidak Boleh Di Perjual belikan.</b></p>
  
  <b>Fitur:</b><br>
  <i>-Sistem Login & Logout</i><br>
  <i>-CRUD Manajemen Anggota</i><br>
  <i>-CRUD Manajemen Pemasukan</i><br>
  <i>-CRUD Manajemen Pengeluaran</i><br>
  <i>-Melihat Nunda Kas</i><br>
  <i>-Change Foto Dan Nama Admin</i><br>
  <i>-Change Password</i><br>
  
[![cashflow.png](https://i.postimg.cc/65GvpPZ2/cashflow.png)](https://postimg.cc/xcnCsttn)

## Refactor MVC + PDO (April 2026)

Proyek ini sudah selesai dimigrasikan dari pola procedural + mysqli ke arsitektur MVC + PDO.

### Struktur baru

- `cash_flow/app/Core` : Router, Controller, View, dan koneksi database PDO.
- `cash_flow/app/Controllers` : logika request per fitur.
- `cash_flow/app/Models` : query database dengan prepared statement PDO.
- `cash_flow/app/Views` : tampilan untuk seluruh modul aplikasi.
- `cash_flow/index.php` : front controller untuk routing.
- `cash_flow/.htaccess` : rewrite clean URL ke front controller.

### Modul MVC yang tersedia

- Autentikasi: login, logout, change password.
- Dashboard: ringkasan total kas, pengeluaran, dan jumlah anggota.
- Manajemen anggota: list, cari, tambah, edit, detail, hapus.
- Manajemen kas: setor, daftar, edit, hapus, nunda kas.
- Manajemen pengeluaran: catat, daftar, edit, hapus.
- Akun admin: profile, pengaturan profile, ubah password.
- Export laporan: anggota, kas, pengeluaran, nunda kas.

Semua file modul legacy di root `cash_flow/` sudah dihapus.

### Catatan

- Akses aplikasi langsung melalui front controller dengan clean URL (contoh: `/auth/login`, `/dashboard`, `/members`, `/cash`, `/expenses`).
