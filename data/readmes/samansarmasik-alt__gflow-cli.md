# gflow — Google AI Flow CLI

Google hesabınızla (Gmail) **Google AI Flow** (`labs.google/fx/tools/flow`) üzerinden ücretsiz fotoğraf ve kredi-korumalı video üretimi yapan, her çıktıyı benzersiz ID ve prompt geçmişiyle SQLite katalogda tutan komut satırı aracı.

## Özellikler

- **Doğal Google Oturumu (Chrome CDP):** Bot korumasına takılmadan bilgisayardaki gerçek Chrome'u izole bir profille (`~/.gflow/chrome-profile`) açar. Varsayılan **headless** (arka planda görünmez), `--headed` ile görünür.
- **Ücretsiz Fotoğraf Üretimi:** `nano-banana`, `nano-banana-pro` (2.1), `imagen-4` modelleriyle varsayılan 0 kredi üretim.
- **Agent Mode & Modal Koruması:** Google Flow Ajan Modu varsayılan kapalı tutulur (`--agent-mode` ile açılır); güncelleme / "Yenilikler" dialog'ları otomatik kapatılır.
- **Kredi Güvenlik Kilidi:** Video üretimi (`veo-3.1-lite`, `veo-3.1-fast`, `veo-3.1-quality`, `omni-flash-1.2`) ve 0'dan fazla kredi harcayan tüm işlemler `--confirm-credits` olmadan **asla** çalışmaz (`exit code 2`).
- **Stil Presetleri (`gflow preset`):** `youtube-thumb`, `product-studio`, `cinematic`, `shorts`, `character-sheet`, `ui-icon` hazır profilleri + özel preset kaydetme.
- **Batch Manifest & Resume (`gflow batch`):** JSON manifest ile toplu üretim, `--dry-run` toplam kredi hesabı, `.lock.json` ile kaldığı yerden devam (`--resume`) ve `--dedupe` cache.
- **Prompt Dosyası & Referans Yükleme:** Uzun promptlar için `--prompt-file`, çoklu referans görsel/ID yükleme (`--ref photo.png,img_0001`), sidecar `--write-meta` ve geçici dosyalar için `--ttl` + `gflow prune`.
- **Benzersiz ID & SQLite Katalog:** Her çıktı `img_0001`, `vid_0001` ID'siyle; prompt, model, oran, kalite, kredi, SHA-256, proje, etiket ve soy ağacı (`parentId`) bilgileriyle saklanır.
- **AI Ajan Dostu:** Tüm komutlar `--json` destekler ve `gflow schema` tek seferde makine-okunabilir rehber döner.

## Kurulum

```bash
git clone https://github.com/samansarmasik-alt/gflow-cli.git
cd gflow-cli
npm install
npm link
```

Antigravity eklentisini kurmak için `plugin/` klasörünü `~/.gemini/config/plugins/google-flow/` altına kopyalamanız yeterlidir.

## Hızlı Başlangıç

```bash
# 1. Google hesabıyla giriş (izole Chrome açılır)
gflow auth login

# 2. Oturum ve kredi bakiyesi kontrolü
gflow auth status

# 3. Ücretsiz 2 adet 4:3 fotoğraf üret
gflow image -p "Minimalist studio photo of matte black coffee mug, soft light" -a 4:3 -n 2 --project marka

# 4. Geçmişi ve ID'leri gör
gflow list
gflow show img_0001
gflow search "coffee"

# 5. Bir fotoğrafı remix et (farklı oran + ek prompt)
gflow remix img_0001 -a 16:9 --append-prompt "warm morning sunlight"

# 6. Video maliyeti hesapla (üretim yapmaz)
gflow video -p "Slow cinematic pan over the coffee mug, rising steam" --first-frame img_0001 --dry-run

# 7. Kullanıcı onayından sonra video üret
gflow video -p "Slow cinematic pan over the coffee mug, rising steam" --first-frame img_0001 --confirm-credits
```

## Sorun Giderme

```bash
gflow doctor      # Chrome, CDP, SQLite ve oturum kontrolü
gflow calibrate   # Google Flow UI değişirse DOM/ARIA elementlerini yeniden tarar
```
