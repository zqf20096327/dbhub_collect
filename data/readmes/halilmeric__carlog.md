# CARLOG — Araç Takip Paneli

Şirket araçlarınızı tek ekrandan takip edin: muayene, sigorta, kasko, bakım, lastik, ceza, masraf, sürücü ve belgeler. Süresi dolacak işler panelde görünür ve e-postayla hatırlatılır.

Ücretsiz ve açık kaynak. PHP ile yazıldı; cPanel'e dosyaları atıp kurulum sihirbazını doldurmanız yeterli. Composer, Node ya da SSH gerekmez.

![Genel bakış ekranı](docs/ekran/genel-bakis.jpg)

## Neler yapar

- **Araçlar** — plaka, marka, model, km, fotoğraf; aktif, pasif ve satıldı durumları.
- **Modüller** — her biri Ayarlar'dan tek tıkla açılır ya da kapanır. Kapatılan modülün kayıtları silinmez.
  - Muayene
  - Trafik sigortası
  - Kasko
  - Bakım ve servis (tarihe ve kilometreye göre sonraki bakım uyarısı)
  - Lastik (diş derinliği, durum, araçta ya da depoda)
  - Ceza (ödenene kadar takip)
  - Diğer masraflar
  - Sürücüler (ehliyet bitişi, zimmetli araç)
  - Belgeler (dosya yükleme, geçerlilik bitişi)
- **Yaklaşanlar** — geciken, 7 gün ve 30 gün içinde dolacak işler tek listede.
- **E-posta hatırlatması** — günde bir kez özet e-posta; kaç gün kala haber verileceğini siz belirlersiniz. Geciken işler haftada bir yeniden hatırlatılır.
- **Raporlar** — tarih aralığına göre araç ve modül bazında masraf; CSV olarak indirilir.
- **Arayüz** — açık ve koyu tema, telefonda da kullanılır.
- **Tek yönetici** — şifreli giriş, e-postayla şifre sıfırlama.

## Ekranlar

| Araçlar | Araç detayı |
|---|---|
| ![Araç kartları](docs/ekran/araclar.jpg) | ![Bir aracın künyesi ve yaklaşan işleri](docs/ekran/arac-detay.jpg) |

| Koyu tema | Telefon |
|---|---|
| ![Koyu temada genel bakış](docs/ekran/koyu-tema.jpg) | ![Telefonda yaklaşanlar listesi](docs/ekran/mobil.jpg) |

## Kurulum

Gerekenler: PHP 8.1 veya üstü, MySQL 5.7+ ya da MariaDB 10.2+, Apache ya da LiteSpeed.

1. cPanel'de bir veritabanı ve kullanıcı oluşturun.
2. Dosyaları `public_html` içine yükleyin.
3. Sitenin adresini açın ve kurulum sihirbazını doldurun. "Örnek veri yükle" kutusuyla paneli dolu halde deneyebilirsiniz.
4. Hatırlatma e-postaları için Ayarlar sayfasındaki komutu cPanel › Cron Jobs'a ekleyin.

Ayrıntılı adımlar: [KURULUM.md](KURULUM.md)

### Kendi bilgisayarınızda denemek

```bash
php -S localhost:8090
```

Ardından tarayıcıda `http://localhost:8090` adresini açın. Bu yalnızca deneme içindir; PHP'nin gömülü sunucusu `.htaccess` korumalarını uygulamaz.

## Yeni modül eklemek

Her modül `app/moduller/` içinde tek bir tanım dosyasıdır: alanları, ikonu ve hangi tarihin takip edileceğini yazar. Liste, form, uyarı ve rapor bu tanımdan üretilir; veritabanında değişiklik gerekmez. Mevcut dosyalardan birini kopyalayıp düzenlemek yeterlidir.

## Güvenlik

- Tüm sorgular hazırlanmış ifadelerle çalışır; her form CSRF belirteci taşır.
- Yüklenen dosyalar web'den doğrudan açılamaz, yalnızca giriş yapmış yöneticiye sunulur.
- `config.php` kurulumda oluşur ve depoya dahil değildir.

Bir güvenlik açığı bulursanız lütfen herkese açık bir kayıt açmak yerine depo sahibine doğrudan ulaşın.

## Kontrol

```bash
php tests/kontrol.php
```

Hatırlatma mantığını dener; `TAMAM` yazmalıdır.

## Lisans

[MIT](LICENSE) — ücretsiz kullanabilir, değiştirebilir ve dağıtabilirsiniz.

Birlikte gelen üçüncü taraf bileşenler kendi lisanslarıyla dağıtılır:

| Bileşen | Lisans |
|---|---|
| [Alpine.js](https://alpinejs.dev) 3.14 | MIT |
| [ApexCharts](https://apexcharts.com) 3.54 | MIT |
| [Barlow](https://github.com/jpt/barlow) yazı tipi | SIL Open Font License 1.1 ([metin](assets/fonts/OFL.txt)) |

Tasarım ve yazılım: [webhouse](https://wh.web.tr/)
