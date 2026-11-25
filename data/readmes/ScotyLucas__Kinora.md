# Kinora

**Magyar** · [English](README.en.md)

[![CI](https://github.com/ScotyLucas/Kinora/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/ScotyLucas/Kinora/actions/workflows/ci.yml)

Saját gépen futó médiaszerver filmekhez és sorozatokhoz – a Jellyfin és a Plex alternatívája, magyar, angol és német webes felülettel.
A neve az 1890-es évek kézi „mozgókép-nézegetőjéből” jön.

Egyetlen Go bináris, beágyazott webes klienssel; SQLite adatbázis; az ffmpeg végzi az átkódolást.
Az elsődleges telepítési mód a Docker.

![Kezdőlap](docs/screenshots/05-home.png)

## Telepítés Dockerrel (ajánlott)

```yaml
# docker-compose.yml
services:
  kinora:
    image: ghcr.io/scotylucas/kinora:latest
    container_name: kinora
    ports:
      - "8096:8096"
      # - "8097:8097"              # Jellyfin-kompatibilis API, lásd lent
    environment:
      - TZ=Europe/Budapest
      - PUID=1000
      - PGID=1000
      # - KINORA_JELLYFIN_COMPAT=1  # Jellyfin-kompatibilis API, lásd lent
    volumes:
      - ./config:/config
      - ./cache:/cache
      - /path/to/movies:/media/movies:ro
      - /path/to/shows:/media/shows:ro
    # Intel/AMD hardveres gyorsítás:
    # devices: ["/dev/dri:/dev/dri"]
    # group_add: ["video", "render"]
    restart: unless-stopped
```

```sh
docker compose up -d
```

Ezután nyisd meg: `http://<szerver-ip>:8096`. Az első indításkor egy varázsló kéri a szerver nevét és az admin fiókot,
majd végigvezet a médiamappákon (a mappaválasztó eleve a `/media` mappában nyílik meg, add hozzá a `/media/movies` és `/media/shows`
mappát), a TMDB-kulcson, a hardveres gyorsítás tesztjén, a letöltőkliensen és az indexeren, végül a távoli elérésen. Minden lépés
kihagyható, és később pótolható az Admin oldalon; a varázsló az **Admin → Beállítások** oldalról újra megnyitható.
Az admin fiókot az hozza létre, aki elsőként beállítja a szervert. Ezért a Kinora a kezdő beállítást csak a helyi hálózatról
(vagy Tailscale-en át) fogadja el; ha mégis kívülről kell, `KINORA_ALLOW_REMOTE_SETUP=1`. Ahol minden kliens privát címről
érkezik (egyes Docker-beállítások), ez a szűrés nem tud különbséget tenni, ezért a beállítást így is érdemes azelőtt elvégezni,
hogy a szervert kívülről elérhetővé tennéd.

| Mappa a konténerben | Mire való | Mentsd? |
|---|---|---|
| `/config` | adatbázis (`kinora.db`), poszterek és képek | **igen** |
| `/cache` | átkódolt szegmensek, letöltések, feliratcache | nem kell |
| `/media/...` | a filmjeid, **csak olvasható** (`:ro`) – a Kinora soha nem ír ide | – |

### Környezeti változók

Minden beállítás megadható környezeti változóval is. Ilyenkor az admin felületen a mező zárolva van („környezeti változóból beállítva”).

| Változó | Alapérték | Leírás |
|---|---|---|
| `KINORA_ADDR` | `:8096` | figyelt cím |
| `KINORA_DATA` | `/config` (natívan `./data`) | adatbázis, képek |
| `KINORA_CACHE` | `/cache` (natívan `<data>/cache`) | átkódolás, letöltések |
| `KINORA_PUBLIC_URL` | – | nyilvános cím (meghívó linkekhez, QR-kódokhoz) |
| `KINORA_TMDB_KEY` | – | TMDB API kulcs (v3 kulcs vagy v4 token) |
| `KINORA_TMDB_API` | `https://api.themoviedb.org/3` | TMDB API-cím (proxy vagy tükör esetén) |
| `KINORA_METADATA_LANG` | `hu-HU` | alapértelmezett metaadat-nyelv (a kliensek a saját felületi nyelvükön kapják a címeket, ha az eltér) |
| `KINORA_WATCH_REGION` | a metaadat-nyelv országa | a Felfedezés streaming-kínálatának országa (kétbetűs kód, pl. `HU`) |
| `KINORA_ENCODER` | `auto` | `auto`, `h264_nvenc`, `h264_qsv`, `h264_vaapi`, `libx264` … |
| `KINORA_VIDEO_CODEC` | `auto` | `auto`: HEVC/AV1 kimenet, ha a kliens jelzi és a hardveres encoder működik; `h264`: csak H.264 |
| `KINORA_VAAPI_DEVICE` | `/dev/dri/renderD128` | VA-API eszköz |
| `KINORA_SCAN_INTERVAL_MIN` | `15` | periodikus szkennelés (perc, 0 = ki) |
| `KINORA_SERVER_NAME` | `Kinora` | szerver neve |
| `KINORA_LOG_FORMAT` | szöveg | `json` esetén JSON naplózás (a `docker logs` mindkettőt mutatja) |
| `KINORA_LOG_LEVEL` | `info` | `debug` |
| `KINORA_FFMPEG`, `KINORA_FFPROBE` | `ffmpeg`, `ffprobe` | saját ffmpeg útvonala |
| `KINORA_QUICKCONNECT` | `1` | belépés 6 jegyű kóddal TV-ről/telefonról (`0` = ki) |
| `KINORA_DISCOVERY` | `1` | szerverkeresés a helyi hálózaton (`0` = ki) |
| `KINORA_DISCOVERY_PORT` | `7359` | a felderítés UDP-portja (`0` = a figyelés sem indul el) |
| `KINORA_CORS_ORIGINS` | – | további app-originek tokenes CORS-hoz, vesszővel elválasztva |
| `KINORA_ACCENT` | – | akcentszín (`#rrggbb`), az appok is használják |
| `KINORA_LOGO` | – | logófájl (pl. `/config/logo.png`); induláskor átveszi, ha változott (PNG/JPG/WebP/SVG, max. 2 MB) |
| `KINORA_INITIAL_SERVER_NAME`, `KINORA_INITIAL_LOGO`, `KINORA_INITIAL_MEDIA` | – | csak az **első** induláskor: szervernév, logó, kezdő médiamappák (`Név=/út;/út2`); utána az adminfelületen módosíthatók – ezeket a telepítők állítják be |
| `KINORA_INTRO_DETECTION`, `KINORA_INTRO_WINDOW_MIN` | `1`, `10` | intró-/stáblista-felismerés be/ki, és hány percben keresse az intrót |
| `KINORA_JELLYFIN_COMPAT` | – | `1` = megnyitja a Jellyfin-kompatibilis API portját (az admin-beállítással együtt kapcsol be) |
| `KINORA_JELLYFIN_ADDR` | `:8097` | a Jellyfin-kompatibilis API címe |
| `KINORA_MAX_TRANSCODES` | – | egyszerre futó átkódolások felső korlátja az egész szerveren (fiókonként mindig legfeljebb 8) |
| `KINORA_ALLOW_NEWER_DB` | – | `1` = egy újabb Kinora-verzió adatbázisát is megnyitja (visszalépés után; saját felelősségre) |
| `KINORA_ALLOW_REMOTE_SETUP` | – | `1` = a kezdő beállítás (az első admin fiók) bármilyen címről elvégezhető; alapból csak a helyi hálózatról, loopbackről vagy Tailscale-ről |
| `TZ`, `PUID`, `PGID` | `UTC`, `1000`, `1000` | időzóna, a fájlok tulajdonosa |

### Melyik image-et válaszd?

| Tag | Mit tud | Méret (tömörítve / kicsomagolva) | Mikor válaszd |
|---|---|---|---|
| `latest` (és `vX.Y.Z`, `edge`) | szoftveres kódolás, **Intel** VA-API/Quick Sync (amd64), **NVIDIA** NVENC | ~165 MB / ~615 MB | Az esetek többségében: Intel iGPU-s NAS vagy mini PC, NVIDIA kártya, Raspberry Pi, vagy ha nincs GPU. |
| `latest-amd` (és `vX.Y.Z-amd`, `edge-amd`) | ugyanez, plusz **AMD** Radeon VA-API (Mesa radeonsi) | ~225 MB / ~855 MB | Csak AMD GPU-hoz vagy AMD APU-hoz (Ryzen iGPU), ha hardveres kódolást akarsz. |

Mindkettő amd64-re és arm64-re is elérhető (multi-arch manifest). Ha nem tudod, melyik kell, indítsd a `latest`-et, és nézd meg az
**Admin → Átkódolás** oldalon az encoder-önteszt eredményét. Ha AMD géped van, és a VA-API ott „nem elérhető”, válts `latest-amd`-re.

### Hardveres gyorsítás

- **Intel / AMD (VA-API, Quick Sync):** AMD GPU-hoz a `latest-amd` image kell. Vedd ki a kommentet a `devices: ["/dev/dri:/dev/dri"]` sor elől. Az entrypoint
  automatikusan belép abba a csoportba, amelyiké a `/dev/dri/*` eszköz (a render/video GID rendszerenként más), így a `group_add` sor el is hagyható.
- **NVIDIA:** NVIDIA driver + [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/) kell, majd:
  `docker compose -f docker-compose.yml -f docker-compose.nvidia.yml up -d`
- Az **Admin → Átkódolás** oldalon a Kinora minden encoderrel *ténylegesen* lekódol egy 1 másodperces tesztklipet, és megmutatja,
  melyik működik, mennyi idő alatt, és ha nem, mi a hibaüzenet. Az automatikus választás sorrendje: a beállított encoder, ha működik → az első működő
  hardveres encoder → szoftveres libx264. `KINORA_VIDEO_CODEC=auto` mellett ugyanannak a hardvernek a HEVC (vagy AV1) encodere megy helyette,
  ha a kliens jelzi a kodeket és az encoder átment a próbán; a HEVC/AV1 fMP4 HLS-szegmensekbe kerül.

### NAS tippek

- **Unraid:** Docker → Add Container, repository `ghcr.io/scotylucas/kinora:latest`, port 8096, path-ok: `/config` → `/mnt/user/appdata/kinora`,
  `/media` → `/mnt/user/media` (read only). `PUID=99`, `PGID=100` (nobody:users). Intel iGPU-hoz: Extra Parameters: `--device=/dev/dri`.
- **TrueNAS SCALE:** Custom App, a dataseteket hostPath-ként csatold, `PUID`/`PGID` legyen annak a felhasználónak az azonosítója, akié a dataset
  (általában `568:568` – apps). GPU: „GPU Configuration” → Intel/AMD.
- **Synology (Container Manager):** a `PUID`/`PGID` értékét SSH-n az `id <felhasználó>` paranccsal kérdezd le. A `/dev/dri` csak olyan modelleken érhető el,
  amelyekben Intel processzor van (pl. a „+” sorozat egy része). A `@eaDir` és `#recycle` mappákat a szkenner automatikusan kihagyja.
- Hálózati megosztás (SMB/NFS) esetén ha a megosztás leesik, a Kinora **nem töröl semmit**: a szkennelés hibával leáll, a hiányzó fájlok csak
  „hiányzó” jelölést kapnak, és visszatéréskor megmarad a megnézett állapotuk.

### Natív telepítés Linuxra (systemd)

```sh
curl -fsSL https://raw.githubusercontent.com/ScotyLucas/kinora/main/install.sh | bash
```

A telepítő letölti és ellenőrzi (SHA-256 + ed25519 aláírás) a legfrissebb kiadást, telepíti az ffmpeg-et, és systemd szolgáltatást készít,
amely a saját felhasználódként vagy dedikált `kinora` felhasználóként fut. Így a Kinora **bármelyik mappát látja, amit a szolgáltatás olvashat**,
és új mappát bármikor hozzáadhatsz. Ha egy mappát nem tud olvasni, a felület megmondja, miért, és megadja a javító parancsot.
Van `.deb` és `.rpm` csomag is. Részletek, jogosultságok, SMB/NFS-csatolás: [`docs/LINUX.md`](docs/LINUX.md).

**Dockerben utólag bármelyik mappa:** a `docker-compose.host.yml` csak olvashatóan becsatolja a `/home`, `/mnt`, `/media` és `/srv` mappát a `/host` alá
(`docker compose -f docker-compose.yml -f docker-compose.host.yml up -d`). A biztonsági mérlegelés a [`docs/LINUX.md`](docs/LINUX.md)-ben van.

### Windows

Windowson (Windows Serveren is) a Kinora natívan, Windows-szolgáltatásként fut, Docker nélkül, automatikus frissítéssel
(csak kiadott verziókra, hiba esetén visszaállással). Minden kiadáshoz tartozik egy `kinora-windows-amd64.zip`, a telepítés
egy PowerShell-parancs: [`docs/WINDOWS.md`](docs/WINDOWS.md). Asztali Windowson a Docker Desktop is megfelelő (lásd fent).

### Saját logó és név

Az **Admin → Beállítások → Megjelenés** oldalon tölthetsz fel logót sötét és világos háttérre (PNG, JPG, WebP vagy SVG, legfeljebb 2 MB).
A faviconét és az app-ikonokat a Kinora készíti el belőle, és az appok is ezt mutatják a belépő- és a kezdőképernyőn. Az SVG-t csak szkript
és külső hivatkozás nélkül fogadja el, és kizárólag képként szolgálja ki. Az első indítás varázslója is kér logót (nem kötelező).
Dockerben: `KINORA_LOGO=/config/logo.png`. A Linux-telepítő (`install.sh --logo`) az első induláskor adja át.

### Fordítás forrásból

Szükséges: Go 1.24+, C fordító (a sqlite miatt cgo kell), valamint `ffmpeg` és `ffprobe` a PATH-on.

```sh
go build -o kinora ./cmd/kinora
./kinora --data ./data          # http://localhost:8096
```

## Miben más a Kinora

A Jellyfin kiforrott, széles körben használt médiaszerver, és sok mindent tud, amiről ez a táblázat nem szól (többek
között Quick Connect, szülői felügyelet, következő epizód ajánlása, rengeteg kliens és plugin). A táblázat azt írja le,
amit a Kinora másképp csinál, vagy amit egy konténerben, beépítve ad.

| Terület | Mit csinál a Kinora |
|---|---|
| Kérések és letöltés egy konténerben | Beépített beszerzés: a felhasználók filmet és sorozatot kérhetnek, az admin jóváhagyja, a letöltőkliens (qBittorrent, Transmission, Deluge, SABnzbd, NZBGet) letölti, a Kinora beimportálja. Indexer: Torznab/Newznab vagy a beépített motor a Prowlarr közösségi leíróival. Ehhez nem kell külön Radarr, Sonarr, Prowlarr és Jellyseerr ([részletek](#beépített-beszerzés-radarrprowlarrjellyseerr-helyett)). |
| Váltás más szerverről | Import Jellyfinből (felhasználók, megnézett állapot, folytatási pozíció, kedvencek) és Sonarrból, Radarrból, Prowlarrból (figyelt címek, minőségprofilok, indexerek, letöltőkliensek). Mindegyik előnézettel indul, csak jóváhagyás után ír, és újrafuttatva nem duplikál ([docs/IMPORT.md](docs/IMPORT.md)). |
| Meglévő Jellyfin-kliensek | Opcionális Jellyfin-kompatibilis API külön porton, a Kinora jogosultságaival (gyerekprofil, könyvtár-korlátozás). A Kodi + JellyCon kipróbálva; mi működik és mi nem: [docs/JELLYFIN_COMPAT.md](docs/JELLYFIN_COMPAT.md). |
| Mérések | Kinora és Jellyfin egymás mellett, ugyanazon a generált könyvtáron, ugyanazokkal a korlátokkal: szkennelés, RAM/CPU, API-válaszidő, lejátszás indulása. Az eredmények – ahol a Kinora rosszabb, ott is: [docs/BENCHMARKS.md](docs/BENCHMARKS.md); a mérés megismételhető: `scripts/bench/`. |
| Szkennelés | Inkrementális: egy változatlan fájl egyetlen `stat()`, az ffprobe csak az új vagy változott fájlokra fut. Áthelyezés-felismerés (azonos méretű fájl = ugyanaz az elem, megmarad a megnézett állapot). Ha a gyökérmappa nem érhető el vagy hirtelen üres, a szkennelés nem nyúl a könyvtárhoz; az eltűnt fájl csak `missing` jelölést kap. |
| Profilok | Egy fiókon belül legfeljebb 8 profil, opcionális PIN, gyerekprofil korhatár-szinttel. A korlátozás minden végponton érvényes (lista, keresés, ajánló, stream, felirat, letöltés, képek, watch party), offline az appokban is. |
| Átlátható átkódolás | Encoder-önteszt, és a lejátszóban egy „Miért így megy?” panel: az okok közérthetően, a választott encoder, a forrás és az eszköz képességei, hiba esetén az ffmpeg utolsó hibasora. |
| Watch party | Szerveroldali óra: kis eltérésnél `playbackRate` 0,95/1,05, nagynál ugrás; ha valaki pufferel, a többiek legfeljebb 12 másodpercig várnak. Chat, reakciók, jelentés és tiltás. |
| Ajánlások és gyűjtemények | Helyben számolt, magyarázott ajánlósorok („mert szereted: Sci-Fi”, „Mert megnézted: X”); saját címkék, kézi és szabályalapú gyűjtemények élő előnézettel. Egy sorozat elrejthető a folytatási sorból megnézettnek jelölés nélkül. |
| Offline letöltés | Átkódolt letöltés 1080p–360p minőségben vagy eredeti fájlként; az iOS- és az Android-app a háttérben letölti és szerver nélkül is lejátssza; az Android-rész új, készüléken még nincs kipróbálva ([docs/OFFLINE.md](docs/OFFLINE.md)). |
| Magyar felhasználóknak | Magyar, angol és német felület; a nem UTF-8 magyar `.srt` CP1250-ként olvasva helyes ékezetekkel jelenik meg; profilonkénti felirat- és hangnyelv-sorrend. |
| Üzemeltetés | Egyetlen Go-bináris és SQLite; első indítási varázsló (médiamappák, TMDB, hardveres gyorsítás, letöltés, távoli elérés); egy kattintásos, futás közben is konzisztens adatbázis-mentés; meghívólinkek QR-kóddal. |

### Mérések: Kinora és Jellyfin

Egy laptopon (Intel Core i5-1235U, Docker Desktop), ugyanazon a 4 CPU-n és 4 GB-os korláttal, ugyanazon a generált,
10 002 videós könyvtáron, Jellyfin 12.4.0-val, internetes metaadat nélkül
([részletek, módszer és korlátok](docs/BENCHMARKS.md); megismételhető: `scripts/bench/`).

| | Kinora | Jellyfin |
|---|---|---|
| Első szkennelés (3 futás mediánja) | **565 s** | 846 s |
| Újraszkennelés változás nélkül | **0,3 s** | 21,8 s |
| RAM üresjáratban / terhelés alatt | **103 / 167 MiB** | 472 / 488 MiB |
| Főoldal / könyvtároldal / keresés (p50) | **30 / 7 / 10 ms** | 127 / 60 / 86 ms |
| 16 párhuzamos kliens | **162 művelet/s** | 17 művelet/s |
| Lejátszás indulása: direct play / átkódolás (p50) | **5 ms / 2,0 s** | 75 ms / 3,0 s |
| CPU üresjáratban | 0,4% | **0,1%** |

## Mappastruktúra

```
Movies/
  Blade Runner 2049 (2017)/Blade Runner 2049 (2017).mkv     ← a mappanév az elsődleges
  Blade Runner 2049 (2017)/movie.nfo, poster.jpg, fanart.jpg
  Blade Runner 2049 (2017)/Blade Runner 2049 (2017).hu.srt  ← <videónév>.<nyelv>[.forced].srt|vtt|ass
  The.Matrix.1999.1080p.BluRay.x264.mkv                     ← „The Matrix” (1999)
Shows/
  Breaking Bad (2008)/tvshow.nfo, poster.jpg
  Breaking Bad (2008)/Season 01/Breaking.Bad.S01E02.mkv
  Dark/Staffel 2/03 - Ghosts.mkv                            ← évadmappa + sorszám
  Aranyélet/2. évad/Aranyelet.S02E04.mkv
  Futurama/Specials/Futurama.S00E01.mkv                     ← 0. évad
  Seinfeld.S03E10.The.Old.Man.mkv                           ← lapos elrendezés is működik
```

- Felismert minták: `S01E02`, `S01E01E02` (dupla rész), `1x05`, évadmappa + `03 - Cím`. Évadmappák: `Season 01`, `S1`, `Staffel 2`,
  `Évad 2`, `2. évad`, `Specials`/`Extras` (= 0. évad).
- Kimarad: rejtett mappák, `@eaDir`, `#recycle`, `trailers`, `featurettes`, `behind the scenes`, valamint a 300 MB alatti `sample`/`-trailer` fájlok.
- Helyi metaadat: Kodi/Jellyfin-kompatibilis NFO (`movie.nfo`, `<videó>.nfo`, `tvshow.nfo`). Képek: `poster`/`folder`/`cover`,
  `fanart`/`backdrop`/`background`, `<videó>-poster`, `<videó>-thumb`, `season01-poster.jpg`. Ha nincs kép, a Kinora a videó kb. 20%-ánál készít egy képkockát.
- Online metaadat (opcionális): **Admin → Metaadat**, TMDB kulccsal. A helyi NFO-t és a kézzel javított elemeket soha nem írja felül.
  Rossz találat esetén a részletes oldalon a „Találat javítása” gombbal választhatsz másikat.

## Távoli elérés

**Tailscale** (a legegyszerűbb, nem kell portot nyitni): egy sidecar konténer csatlakozik a tailnetedhez, és a Kinora annak a hálózatán fut.

```sh
TS_AUTHKEY=tskey-... docker compose -f docker-compose.yml -f docker-compose.tailscale.yml up -d
```

A tailneten ezután `http://kinora:8096` címen éred el (MagicDNS), a helyi hálózaton továbbra is a megszokott címen.

**Cloudflare Tunnel** (saját domain, HTTPS): a Zero Trust felületén hozz létre egy tunnelt, a public hostname mutasson a `http://kinora:8096` címre, majd:

```sh
CF_TUNNEL_TOKEN=... KINORA_PUBLIC_URL=https://kinora.pelda.hu \
  docker compose -f docker-compose.yml -f docker-compose.cloudflared.yml up -d
```

Figyelem: a Cloudflare felhasználási feltételei korlátozhatják a nagy mennyiségű videóforgalmat a tunnelen.

**Reverse proxy:** a watch party WebSocketet használ, ezért add tovább az `Upgrade` és `Connection` fejléceket. Caddy-vel ehhez elég ennyi:
`reverse_proxy 127.0.0.1:8096`. Nginx-re kész példát találsz az **Admin → Csatlakozás** oldalon. A Kinora követi az `X-Forwarded-Proto`
fejlécet: HTTPS mögött a session cookie `Secure` jelzést kap.

## Kliensappok és telepítés telefonra

- **Android (telefon + Android TV), Samsung Tizen, LG webOS, iOS:** az `apps/` mappában, egy közös felülettel. Építés és telepítés: [`apps/README.md`](apps/README.md),
  a mai kipróbálás lépésről lépésre, Windowsról: [`docs/TESZTELES_MA.md`](docs/TESZTELES_MA.md).
- **iPhone ma, Mac nélkül:** a webkliens telepíthető webes app (PWA): Safari → Megosztás → „Főképernyőhöz adás”. Teljes képernyőn, saját ikonnal fut.
- **Belépés kóddal (Quick Connect):** a TV egy 6 jegyű kódot mutat; egy bejelentkezett eszközön (profil menü → **Eszköz csatlakoztatása**) jóváhagyod,
  és kiválasztod, melyik profillal lépjen be. A kód 5 percig él, egyszer használható; a próbálkozások IP-nként és felhasználónként korlátozottak.
- **Eszközök:** a Fiók oldalon látszanak a bejelentkezett eszközeid (név, platform, appverzió, IP, utolsó aktivitás), egyenként vagy egyszerre kiléptethetők;
  az admin az **Admin → Eszközök** oldalon mindet látja.
- **Szerverkeresés:** az appok UDP-broadcasttal (7359) vagy a helyi alhálózat pásztázásával találják meg a szervert. Dockerben a broadcast nem megy át
  a bridge hálózaton: ehhez `network_mode: host` kell (vagy a címet kézzel kell megadni).

Az appok a `POST /api/login` (vagy a Quick Connect) után kapott tokent `Authorization: Bearer <token>` fejlécben küldik. A CORS csak az app-originekre
(`capacitor://localhost`, `http(s)://localhost`, `null`) és csak tokenes kérésekre engedélyezett, `Access-Control-Allow-Credentials` nélkül.
A `<video>`/`<img>` számára a lejátszási válasz rövid életű, aláírt stream-tokent (`?st=`) tesz az URL-ekbe; ez elemre, felhasználóra és eszközre szól.

### Jellyfin-kompatibilis API (Infuse, Swiftfin, Findroid, Kodi)

A natív Jellyfin-kliensek is csatlakozhatnak a Kinorához, egy külön porton (alapból `8097`). Alapból ki van kapcsolva:

1. a compose-fájlban vedd ki a kommentből a `8097:8097` portot és a `KINORA_JELLYFIN_COMPAT=1` sort, majd indítsd újra a konténert;
2. a Kinorában: **Admin → Beállítások → Jellyfin-kompatibilis API** → be;
3. a kliensben szerverként a `http://<szerver-ip>:8097` címet add meg.

**Belépés:** felhasználónévként a fiók neve (a fiók első felnőtt profiljával lép be), vagy `fiók/profil` (pl. `kati/Gyerek`);
jelszóként a fiók jelszava, PIN-es profilnál a végére írva `#PIN` (pl. `jelszo#1234`). Öt hibás próbálkozás után a fiók
15 percre letiltódik arról a címről. **Quick Connect** is működik: a kliens kódját a Kinorában hagyod jóvá (profil menü →
**Eszköz csatlakoztatása**), és ott választod ki a profilt (PIN-es profilnál ott kell megadni a PIN-t).

Minden Kinora-szabály érvényes: gyerekprofil és korhatár, a fiók könyvtár-korlátozása, átkódolási korlátok. A belépett
kliensek a Kinora eszközlistájában látszanak, és onnan kiléptethetők. Ez részleges kompatibilitás (böngészés, lejátszás,
feliratok, folytatás, megnézett és kedvenc állapot); a webes alapú kliensek (Jellyfin Web, Jellyfin Media Player, a
hivatalos Android-app) nem működnek. A részletek és a kipróbált kliensek: [docs/JELLYFIN_COMPAT.md](docs/JELLYFIN_COMPAT.md).

## Beépített beszerzés (Radarr/Prowlarr/Jellyseerr helyett)

**Admin → Beszerzés:** rákeresel egy filmre, kiválasztasz egy kiadást (vagy a Kinora választja ki a minőségprofil alapján), a qBittorrent letölti, a Kinora pedig hardlinkkel beteszi a filmkönyvtárba (`Cím (Év) {imdb-tt…}/Cím (Év) - 1080p BluRay.mkv`) és beolvassa. Alapból ki van kapcsolva, és az nCore-on kívül nem tartalmaz trackert: a beépített indexer-motorhoz az admin a Prowlarr közösségi katalógusából (kb. 580 oldal) választhat egy kattintással, saját leírót tölthet fel, vagy Torznab/Newznab forrást (Jackett, Prowlarr) adhat meg. Cloudflare mögötti oldalakhoz FlareSolverr állítható be.
A Kinora és a qBittorrent ugyanazt a `/data` mappát lássa (benne `downloads/` és `media/`), így a hardlink működik, és a torrent tovább seedelhet. Ha a qBittorrent más útvonalon látja a letöltéseket, az adminban útvonal-leképezés állítható. **Felfedezés:** a felhasználók (gyerekprofil kivételével) filmet és sorozatot (évadonként) kérhetnek; az admin jóváhagyja (vagy minden kérés automatikus), a szerver pedig magától letölti, és szól, ha megérkezett. Letöltőkliens: qBittorrent, Transmission, Deluge, SABnzbd vagy NZBGet; indexer: Torznab vagy Newznab. Interaktív keresés, saját minőségprofilok és csere jobb minőségre is van. **Sorozatok:** a figyelt sorozatok hiányzó részeit (évadcsomagként is) és az új részeket magától letölti. A teljes terv és a mérföldkövek: [docs/BESZERZES.md](docs/BESZERZES.md).

## Mentés és visszaállítás

- **Admin → Beállítások → Adatbázis-mentés letöltése:** konzisztens pillanatkép (`VACUUM INTO`), futás közben is biztonságos.
- Visszaállítás: állítsd le a konténert, másold a mentést `config/kinora.db` néven a helyére, töröld a `kinora.db-wal`/`-shm` fájlokat, majd indítsd újra.
  A képeket (`config/images`) a következő szkennelés újra legenerálja, ha hiányoznak.

## Az ffmpeg választásáról

A kép a **Debian trixie saját `ffmpeg` csomagját** használja (7.1, `libzimg`/zscale tónusleképezéssel, VA-API, QSV (libmfx), NVENC (ffnvcodec)).
Mellette van az `intel-media-va-driver-non-free` (amd64, Gen8+ Intel iGPU), az `-amd` változatban pedig a `mesa-va-drivers` (AMD) is. Miért nem a `jellyfin-ffmpeg`?

- Ugyanabból a Debian-tárolóból jön amd64-re és arm64-re is, így a multi-arch build egyszerű és reprodukálható.
- A Kinora csak H.264 kimenetet és a szabványos `zscale`+`tonemap` láncot használja, ehhez nem kell a jellyfin-ffmpeg saját OpenCL/Vulkan tónusleképezése.
- A Kinora encoder-öntesztje úgyis megmutatja, mi működik az adott gépen.

Ha a jellyfin-ffmpeg kell (pl. újabb Intel Arc GPU-khoz), egy saját képben telepítsd, és add meg a
`KINORA_FFMPEG=/usr/lib/jellyfin-ffmpeg/ffmpeg` és `KINORA_FFPROBE=/usr/lib/jellyfin-ffmpeg/ffprobe` változót.

**Képméret.** A Debian ffmpeg-je a `libavdevice → libgl1 → … → mesa-libgallium → libllvm19` láncon keresztül behúzza a Mesa OpenGL-drivereit
és az LLVM-et (kb. 140 MB). Az ffmpeg parancssori eszköz soha nem hoz létre OpenGL kontextust, ezért az alap (`latest`) image-ből a build
`dpkg --force-depends`-szel eltávolítja a `libgl1-mesa-dri`, `mesa-libgallium`, `libllvm*` és `libz3-4` csomagot. Rögtön utána egy tesztkódolás is lefut,
ami ellenőrzi, hogy az ffmpeg ép. Ennek az ára, hogy az image-en belül az `apt` hiányzó függőséget jelez; a konténert nem is erre szánták.
A `latest-amd` image-ben ezek megmaradnak, mert az AMD VA-API driver (radeonsi) valóban használja az LLVM-et.
Maga a Kinora bináris kb. 10 MB.

Saját build: `docker build --target runtime .` (alap) vagy `docker build --target runtime --build-arg AMD=1 .` (AMD).

## Fejlesztés

```sh
go run ./cmd/kinora --data ./data --web ./web/static      # a webkliens a forrásból, frissítés után azonnal látszik
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

Ha nincs helyi Go vagy C fordító, a `scripts/go.sh` a toolchaint konténerben futtatja:

```sh
scripts/mkmedia.sh testmedia          # generált tesztkönyvtár (ffmpeg kell hozzá)
scripts/go.sh go vet ./...
scripts/go.sh go test ./...           # unit- és integrációs tesztek valódi médiafájlokkal
scripts/smoke.sh                      # image build + konténer + curl-ös végigjárás (setup → szkennelés → lejátszás → HLS)
BASE=http://127.0.0.1:18097 node scripts/e2e.mjs   # böngészős E2E (Playwright + Edge/Chrome), képernyőképekkel
```

Felépítés:

```
cmd/kinora/        belépési pont, flagek/env, graceful shutdown, healthcheck alparancs
internal/store/    SQLite séma és migrációk, auth/profilok/meghívók, elemek, szabálymotor, gyűjtemények, ajánló
internal/scanner/  fájlnév-felismerés, inkrementális szkenner, NFO, képek
internal/media/    ffprobe, lejátszási döntés, encoder-önteszt, HLS sessionök, WebVTT, letöltések
internal/meta/     opcionális TMDB metaadat
internal/party/    watch party hub (WebSocket)
internal/server/   HTTP API, middleware, webkliens kiszolgálása
web/static/        vanilla JS SPA (index.html, app.js, style.css, vendor/hls.js, vendor/qrcode-generator)
```

A webkliens többnyelvű (magyar, angol, német). A szövegek a `web/static/i18n/<nyelv>.js` fájlokban vannak; a magyar az alap, a hiányzó kulcsok arra esnek vissza. A nyelvet a böngésző beállítása adja, és a profilmenüben, a fiókoldalon vagy a bejelentkezésnél át lehet váltani (a választás a böngészőben marad meg). A szerver magyar üzeneteit (hibák, ajánlássorok, lejátszási indokok, watch party üzenetek) a kliens a nyelvi fájlok `srv`/`srvRe` táblájával fordítja. Hiányzó angol kulcsoknál a nem magyar nyelvek először az angolra esnek vissza.

**Nyelvek az adminban (Admin → Nyelvek):**
- **Exportálás:** bármelyik nyelv letölthető JSON-fájlként, az összes kulccsal együtt. A le nem fordított kulcsok a tartalék nyelv szövegével szerepelnek benne.
- **Importálás:** egy lefordított fájl visszatölthető. Ha a nyelv már létezik, a felület megerősítést kér a felülírás előtt.
- **Új nyelv:** megadod a kódot (pl. `fr`, `pt-br`), a nevet és a locale-t (pl. `fr-FR`; ez dönti el a számok formátumát és a többes számot). Indulhat üresen, vagy egy meglévő nyelv másolatából.
- **Szerkesztő:** kulcsonként mutatja a referenciaszöveget és a fordítást. Van kereső és „csak a fordítatlanok” szűrő; az üresen hagyott mező a tartalék nyelv szövegét használja.
- **Visszaállítás:** a beépített nyelvek (hu, en, de) módosításai felülírásként tárolódnak, és egy gombbal visszaállíthatók. A hozzáadott nyelvek törölhetők.

A mentett nyelvek a `<data>/i18n/<kód>.json` fájlokban vannak, és a kliens a `/i18n/custom.js` címről tölti be őket. A fájlformátum: `{"kinora_language": 1, "code": "fr", "name": "Français", "strings": {…}}`.
- A sablonokban `{0}`, `{1}`… jelöli a paramétereket, a `{0:00}` két számjegyre egészít ki.
- A többes szám egy objektum, `one`/`few`/`many`/`other` (és `=0`, `=1`…) kulcsokkal.
- A formátum részletes leírása a beépített `web/static/i18n/*.js` fájlok elején található.

**Az iPhone/iPad és az Apple TV app** ugyanezeket a nyelveket használja. Az appok saját szövegei a nyelvi fájlok `app` táblájában vannak; a kulcs az app magyar szövege, mint az `srv`-nél, így az adminban felvett új nyelv az appokat is fordítja, és a szerkesztő ezeket is mutatja. A szerver a `GET /api/languages` (lista verzióval) és a `GET /api/languages/<kód>` címen adja ki őket, bejelentkezés nélkül, a felülírásokkal és az angol tartalékkal együtt, csak a `locale`, `app`, `srv`, `srvRe` részt. Az app minden szerverhez csatlakozáskor szinkronizál: letölti az új vagy megváltozott nyelveket, és mindet megtartja az eszközön, akkor is, ha a szerver nem érhető el, vagy a nyelvet később törölték róla. A nyelv az app Beállítások → Nyelv oldalán (Apple TV-n a Beállítások fülön) választható; az „Automatikus” a készülék nyelvét követi, és ha az nincs meg, angolra, végül magyarra esik vissza. A widgetek és a Top Shelf ugyanazt a nyelvet használják. Ami magyar marad: a Siri/Parancsok rögzített szövegei és a rendszer engedélykérő szövegei.

Ha egy fordítást a projektbe is beküldenél, az exportált `strings` objektumból készíts új `web/static/i18n/<kód>.js` fájlt, és vedd fel az `index.html`-be.

### Tudatosan későbbre hagyva (v2)

Beépített relay/NAT-áttörés, offline letöltés az appokba, watch party az appokból, intro-felismerés audio-ujjlenyomattal,
trickplay előnézeti képek, zenei könyvtár, élő TV, hiányzó gyűjteményelemek TMDB-ből, Postgres, a natív appok fordítása.

## Dizájn

A felület a „kivilágított mozihomlokzat” gondolatára épül: a poszterek megvilágított plakáttartókban ülnek, az egyetlen akcentszín (borostyán)
csak annak jár, ami éppen „él” – a fókuszált kártya, a lejátszás, a haladás, az egyetlen elsődleges gomb. Két regiszter van ugyanazokból a
tokenekből: az **előcsarnok** (böngészés: a kép vezet, a felület hátralép) és a **vetítőfülke** (admin, szerkesztők: hajszálvonalak, táblák, tabuláris számok).

- Minden érték design token a `style.css` elején (`:root`): színskála, 4/8-as térköz-skála, betűméret-skála, két lekerekítés, 44 px-es érintési minimum, mozgás-időzítés.
- Betűk saját kiszolgálásból (`web/static/fonts`, SIL OFL): **Big Shoulders Display** a címekhez és számokhoz, **Atkinson Hyperlegible** a szövegekhez – mindkettő tartalmazza az ő/ű-t.
- Távirányító/billentyűzet: a nyilak térben mozgatják a fókuszt a sorok és rácsok között, a fókuszált plakáttartó kigyullad, és a kezdőlap homlokzata arra a filmre vált; Enter nyit, Esc visszalép.
- Kép nélküli könyvtárnál a kártya tipográfiai címkártya (cím + év), nem üres doboz.
- A régi felület képei összehasonlításhoz: `docs/screenshots/before/`.

## Képernyőképek

| | |
|---|---|
| ![Fókusz a távirányítóval](docs/screenshots/05b-home-focus.png) | ![Könyvtár](docs/screenshots/06-library.png) |
| ![Részletek](docs/screenshots/07-detail.png) | ![Miért kódol át?](docs/screenshots/10-player-transcode-why.png) |
| ![Watch party](docs/screenshots/19-party-host.png) | ![Smart gyűjtemény](docs/screenshots/14-smart-editor.png) |
| ![Encoder-önteszt](docs/screenshots/16-admin-transcode.png) | ![Telefon](docs/screenshots/21-phone-home.png) |

## Licenc

MIT. A vendorolt `hls.js` (Apache-2.0) és `qrcode-generator` (MIT) saját licence a `web/static/vendor/` mappában van.
