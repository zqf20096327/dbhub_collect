# SEVM — SQLite · Express.js · Vue.js · MochiBerry

**SEVM** adalah ekosistem web yang berjalan *di atas* engine **MochiBerry**
dengan pemisahan arsitektur bersih: engine inti tetap ringan dan tidak
disentuh, sementara HTTP, SQLite, dan shim `node:*` hidup sebagai ekstensi
native `.dll` / `.so` / `.lbrct` yang dimuat saat runtime (pola
dlopen-style), tanpa compile ulang engine.

## Dua dunia modul

SEVM memisahkan **dua orientasi** modul — bedanya bukan "boleh/tidak", tapi
orientasi dominan:

| | `node_modules/` | `mochi_modules/` |
|---|---|---|
| orientasi | **JS / script / framework** | **native plugin engine** |
| isi utama | paket JavaScript (`package.json` + `index.js` + `lib/`) | shared object / DLL yang di-load ke engine |
| native lib | **boleh** — paket bisa membawa `.dll` / `.exe` / `.elf` di `bin/` | justru ini inti: `.dll` / `.so` / `.lbrct` |
| contoh | `express`, `net`, `sqlite`, `events`, `fs`, `mochinode` | `mochinode_net.dll`, `mochinode_sqlite.dll` |

Jadi `node_modules` = paket framework NodeJS-style (scripting/JS dominan, tapi
tetap boleh berisi lib native), sedangkan `mochi_modules` = plugin native
untuk engine (condong ke DLL/so).

## Struktur proyek (NodeJS style)

```
sevm/
├── package.json                 # manifest root (type: module, dependencies)
├── README.md
├── LICENSE
├── node_modules/                # paket JS/framework (NodeJS style)
│   ├── mochinode/               # loader inti: require(), loadNative(), resolver
│   │   ├── index.js
│   │   └── package.json
│   ├── express/                 # router kompatibilitas Express
│   │   ├── index.js
│   │   ├── package.json
│   │   └── README.md
│   ├── dynalib/                 # API dynalib(file, offset, symbol, abi, opts)
│   │   ├── index.js
│   │   ├── package.json
│   │   └── README.md
│   ├── net/                     # node:http di atas mochinode_net
│   │   ├── index.js
│   │   ├── lib/http.js          # parsing + response writer
│   │   └── package.json
│   ├── sqlite/                  # node:sqlite di atas mochinode_sqlite
│   ├── events/                  # node:events (EventEmitter)
│   └── fs/                      # node:fs di atas mbjs:std / mbjs:os
├── mochi_modules/               # plugin native engine
│   ├── mochinode_net.dll
│   ├── mochinode_sqlite.dll
│   ├── mochinode_dynalib.dll    # bridge libdynalib -> JS
│   └── README.md
├── native/                      # sumber C di balik plugin mochi_modules
│   ├── mbjs_runtime.h           # bootstrap resolve simbol engine
│   ├── mochinode_net.c
│   ├── mochinode_sqlite.c
│   └── mochinode_poke.c         # modul uji kelayakan
├── libdynalib/                  # subsistem C99 dynamic loader (107/107 test)
└── examples/
    └── sevm-app/                # aplikasi contoh (NodeJS style)
        ├── package.json
        ├── src/server.js
        └── public/
            ├── index.html       # Vue 3 SPA
            └── vue.global.prod.js
```

## Menjalankan demo

```bash
cd examples/sevm-app
mbjs.exe -m src/server.js

# lalu:
curl http://127.0.0.1:8080/api/health
curl http://127.0.0.1:8080/api/items
curl -X POST http://127.0.0.1:8080/api/items \
     -H "content-type: application/json" \
     -d '{"title":"Kirim laporan ke Bos"}'
```

Endpoint:

- `GET /` — Vue 3 SPA (build statis, client-side)
- `GET /api/items?q=` — JSON dari SQLite
- `POST /api/items` — INSERT ke SQLite
- `GET /api/health` — status engine/runtime

## Kontrak modul native engine (diverifikasi disassembly + source)

- Loader: `LoadLibraryA(path)` lalu `GetProcAddress(h, "mbjs_init_module")`,
  `m = init(ctx, module_name)`.
- Simbol ekspor **wajib** bernama `mbjs_init_module`.
- Specifier import **wajib** berakhiran `.dll`; path relatif di-resolve
  relatif ke direktori file pengimpor (`../` juga didukung).
- `AddModuleExportList` (nama) dipanggil di dalam `mbjs_init_module`;
  `SetModuleExportList` (nilai) dipanggil di init func modul.
- Modul native **tidak boleh** meng-import `mbjs.exe` (Windows error 126) —
  simbol engine di-resolve saat runtime dari host image (`GetModuleHandle(NULL)`),
  lihat `native/mbjs_runtime.h`.
- Engine harus mengekspor simbol `MBJS_*`; build `tier-core` yang sudah
  di-strip tidak punya export table sehingga plugin native tidak bisa resolve.

## Komponen

| Komponen | Status | Catatan |
|----------|--------|---------|
| `takegawa` (TGPM) | ✅ | subrepo/tool terpisah (`Archana-Berry-Studio/takegawa`) |
| `libdynalib` | ✅ 107/107 test | loader dinamis C99 lintas `.so`/`.dll`/`.lbrct`; juga di repo `Archana-Berry-Studio/libmochiberry` |
| `mochi_modules/mochinode_net.dll` | ✅ | server TCP/HTTP blocking (Winsock2) |
| `mochi_modules/mochinode_sqlite.dll` | ✅ | bridge SQLite (sqlite3 3.50.4, prepared stmt) |
| `mochi_modules/mochinode_dynalib.dll` | ✅ | bridge `dynalib()` ke JS (embed libdynalib, JIT trampoline) |
| `node_modules/*` | ✅ | shim `node:http`, `node:sqlite`, `node:events`, `node:fs`, Express, dynalib |
| Vue SPA | ✅ | `public/index.html` + `vue.global.prod.js` (offline) |
| demo HTTP | ✅ | `examples/sevm-app/src/server.js` → port 8080 |

## Agent & shim workflow

- `AGENTS.md` berisi kontrak arsitektur untuk agent: batas `mochi_modules/` vs `node_modules/`, layout modul baru, aturan ABI/dynalib, dan alur gap-driven.
- `MISSING_SHIMS.json` mencatat shim yang sudah ada dan yang masih kurang.
- `python script/scaffold_shim.py <nama> mochi` membuat kerangka modul native-first; mode `node` membuat paket JS-first hybrid.
- Toolchain cross-compile ada di `cmake/` (MinGW, Linux, Android NDK).

Shim baru: `mochitimers`, `mochiglobals`, `mochifetch`, dan `mochihttps` (delegasi ke WinHTTP lewat `mochihttp`).

## Catatan ukuran

Engine inti (build `tier-core`, sudah di-strip) ± **1.21 MB** — masih di atas
target < 1 MB. Ekstensi SEVM (net + sqlite DLL) masing-masing ± **60 KB** dan
tidak menambah ukuran engine karena dimuat saat runtime.
