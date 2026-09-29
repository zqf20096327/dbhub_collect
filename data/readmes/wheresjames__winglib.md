# Winglib

Winglib is a C++ utility and scripting library built around the
[Squirrel](http://squirrel-lang.org/) language.  The most important parts of
this tree are the native support library in `lib/oexlib`, the Squirrel binding
layer in `lib/sqbind`, and the optional native Squirrel modules in `sqmod`.

There are also applications, tools, installers, sample scripts, and old test
programs in this repository.  They are useful as examples and build targets,
but the heart of the project is the Squirrel runtime and the module ecosystem.

## What is in this repository?

```text
lib/oexlib/      Core C++ support library: strings, files, sockets, images,
                 time, logging, memory, HTTP sessions, SQLite wrappers, etc.

lib/sqbind/      Squirrel runtime integration.  This exports C++ classes and
                 helper functions into Squirrel and handles script threads,
                 message queues, module loading, and core built-in bindings.

sqmod/           Optional native modules loaded from Squirrel with
                 _self.load_module("name", "").  Each sqmod_* directory builds
                 one shared library.

sq/              Example Squirrel applications.

etc/scripts/     Many small Squirrel examples and module smoke tests.

app/             Host applications and experiments.  `app/sqrl` is the main
                 command-line Squirrel runner.

tools/           Build/helper utilities.  Most users do not need to start here.

dox/             Doxygen inputs for `oexlib`, `sqbind`, and `sqmod`.
```

## Architecture

At runtime, a host application creates a `CScriptThread` and a `CSqEngine`.
The engine registers the built-in classes from `lib/sqbind`, then runs a
Squirrel script.  Scripts get a global `_self` object, implemented by
`CSqEngineExport`, which provides runtime services such as:

- script inclusion and inline script execution
- dynamic native module loading
- file and resource path helpers
- thread and message queue management
- timers and simple scheduling
- shared property access between script threads
- binary share helpers
- console output and output capture
- process, service, shell, and platform helpers

Native modules in `sqmod` are shared libraries with a consistent service-style
entry point set:

- `SRV_GetModuleInfo`
- `SRV_Start`
- `SRV_Stop`
- `SQBIND_Export_Symbols`

`_self.load_module("curl", "")`, for example, looks for a decorated native
library named like `sqmod_curl` in module search directories such as `sqmod`,
`_sqmod`, and `modules`.  When found, the module is loaded and its exported
Squirrel classes are registered in the current VM.

## Core Squirrel bindings

`lib/sqbind` provides the baseline API available to scripts without loading
extra modules.  The most commonly used classes are:

| Class | Purpose |
| --- | --- |
| `CSqMulti` | Hierarchical key/value data, serialization, URL/parameter style data, and general structured values. |
| `CSqBinary` | Binary buffers, typed reads/writes, base16/base64, compression, fingerprints, and image/buffer utilities. |
| `CSqFile` | File I/O, path helpers, directory listing, and create/delete/copy/rename helpers. |
| `CSqSocket`, `CSqSockAddress` | TCP/UDP sockets, socket events, reads/writes, and address handling. |
| `CSqHttpServer` | Small embedded HTTP server with sessions, callbacks, folder mapping, headers, and optional compression. |
| `CSqSQLite` | SQLite database access, table checks, query execution, row results, and simple insert/update/delete helpers. |
| `CSqImage`, `CSqColor` | Image loading/saving, encoding/decoding, pixel access, resizing, filtering, and basic image operations. |
| `CSqTime`, `CSqTimeRange` | Date/time formatting, ranges, timestamps, and elapsed-time utilities. |
| `CSqSerialPort` | Serial port open/read/write and common port settings. |
| `CSqBinaryShare`, `CSqFifoShare`, `CSqVideoShare` | Shared-memory style binary, FIFO, and video buffer exchange. |
| `CSqDataLog` | Time-series style data logging. |
| `CSqPolygon` | Polygon and geometry helpers. |
| `CSqAviFile` | AVI writing helpers. |
| `CSqCapture`, `CSqEzdib`, `CSqGui` | Capture, bitmap, and small GUI/platform helpers. |

The built-in `_self` API is broad.  For details, start in
`lib/sqbind/sq_engine.h` and the `SQBIND_MEMBER_FUNCTION` registrations in
`lib/sqbind/sq_engine.cpp`.

## Optional Squirrel modules

Each directory under `sqmod/sqmod_*` builds one optional native module.  Module
names are the suffix after `sqmod_`; load them from Squirrel with:

```squirrel
_self.load_module("curl", "");
local curl = CSqCurl();
```

Core module set from the top-level `Makefile`:

| Module | Main exported classes | Capability |
| --- | --- | --- |
| `asio` | `CAsioDrv` | ASIO audio driver access. |
| `cell` | `CCellConnection` and cell support classes | Cell/backplane messaging and service/rack integration. |
| `crtmp` | `CRtmpServer` | RTMP server support through crtmp. |
| `curl` | `CSqCurl` | HTTP/FTP style transfers through libcurl. |
| `ffmpeg` | `CFfContainer`, `CFfDecoder`, `CFfEncoder`, `CFfCapture`, `CFfConvert`, audio encoder/decoder/resampler, `CFfTranscode`, `CFfFmt` | Media demuxing, decoding, encoding, capture, conversion, and transcoding. |
| `fftw` | `CSqFftw` | FFT and signal processing helpers. |
| `freetype2` | `CFtLibrary`, `CFtFace` | Font loading and rasterization through FreeType. |
| `gdchart` | `CGdcChart` | Chart creation and image output. |
| `gsoap` | `CGSoapDrv` | SOAP client/server style integration. |
| `live555` | `CLvRtspClient`, `CLvRtspServer` | RTSP client and server support. |
| `mysql` | `CSqMysql` | MySQL database access. |
| `openssl` | `CSqOpenSSL`, `COsslKey`, `COsslCert`, `CSqSSLPortFactory`, `CSqHash` | TLS/SSL ports, hashing, keys, signatures, and certificates. |
| `poco` | `CPoSmtp`, `CPoMessage` | SMTP and MIME message helpers through POCO. |
| `portaudio` | `CPaInput`, `CPaOutput` | Audio input and output streams. |
| `rtmpd` | `CRtmpdSession` | RTMP session support. |
| `ssh2` | `CSqSsh2` | SSH/SFTP style operations through libssh2. |
| `tinyxml` | `CSqXml` | XML parsing and generation. |

Additional modules are gated behind build flags or are less commonly built:

| Module | Main exported classes | Capability |
| --- | --- | --- |
| `freenect` | `CSqFreenect` | Kinect/libfreenect capture. |
| `gstreamer` | `CGsCapture` | GStreamer capture. |
| `haru` | `CHaruPdf` | PDF generation with libharu. |
| `irrlicht` | `CSqIrrlicht`, `CSqirrNode`, `CSqirrCamera`, `CSqirrTexture`, vectors, colors, lines, rectangles, physics helpers | 3D rendering and scene utilities. |
| `mimetic` | `CSqMimetic` | MIME parsing/generation through mimetic. |
| `quickfix` | `CSqQuickfix` | FIX protocol integration. |
| `test` | `CTestClass` | Minimal module example. |
| `usb` | `CSqUsb` | libusb access. |
| `vmime` | `CSqVMime`, `CVmMsg` | Mailbox/MIME message operations through VMime. |
| `webkit` | `CSqWebkit` | WebKit/wxWidgets style web view integration. |

The best way to discover exact methods is to open the module source and look
for `SQBIND_MEMBER_FUNCTION` registrations.  Most modules keep registrations
in `stdafx.cpp` or the primary module `.cpp` file.

## Running scripts

The primary command-line host is `app/sqrl`.  It can run a Squirrel file,
inline script text, base64-encoded script text, or script text from stdin.

Typical usage after building:

```sh
sqrl etc/scripts/test_curl.nut
sqrl -s "_self.echo(\"hello from squirrel\\n\");"
```

Useful script conventions:

- `_init()` is called when a script starts.
- `_idle()` is called repeatedly; returning a negative value ends many example scripts.
- `_self.include("file.nut")` includes another script.
- `_self.load_module("name", "")` loads a native module such as `curl`, `openssl`, or `ffmpeg`.
- `_self.queue()` returns the current message queue for callbacks.
- `CSqMulti` is the usual structured data object passed between scripts and callbacks.

Examples worth reading:

| Example | Demonstrates |
| --- | --- |
| `etc/scripts/test_curl.nut` | Loading `curl` and fetching a URL into `CSqBinary`. |
| `etc/scripts/test_openssl.nut` | RSA keys, signatures, certificates, and fingerprint images. |
| `etc/scripts/test_http.nut` and `etc/scripts/test_http_multi.nut` | Embedded HTTP server callbacks. |
| `etc/scripts/test_sqlite.nut` | SQLite access through `CSqSQLite`. |
| `etc/scripts/test_sockets.nut`, `test_sockets_server.nut`, `test_sntp_client.nut`, `test_sntp_server.nut` | TCP/UDP socket usage. |
| `etc/scripts/test_ffmpeg.nut`, `ffmpeg_portaudio.nut`, `ffmpeg_extract_keyframes.nut` | Media decoding and audio/video pipelines. |
| `etc/scripts/test_threads.nut`, `test_threads_1.nut`, `test_threads_2.nut` | Script threads and message queues. |
| `etc/scripts/test_memshare.nut` | Shared buffers and IPC-style data exchange. |

## Building

Winglib is designed to be built inside a
[deftbuild](https://github.com/wheresjames/deftbuild) workspace.  Deftbuild is
a GNU make based cross-platform and cross-compiler build system.  The local
`buildpath.mk` expects the repository to be located like this:

```text
buildroot/
  deftbuild/
    v1/
  lib/
    winglib/
```

The important line is:

```make
PRJ_LIBROOT := $(PRJ_RELROOT)/../../deftbuild/v1
```

That means most project makefiles assume `deftbuild/v1` is two levels above
their project directory.

### Deftbuild setup

From a fresh workspace, the deftbuild README describes this general shape:

```sh
mkdir buildroot
cd buildroot
git clone https://github.com/wheresjames/deftbuild.git
mkdir -p lib
cd lib
git clone https://github.com/wheresjames/winglib.git winglib
```

Deftbuild can check out and prepare third-party dependency groups.  Its command
line uses this form:

```sh
deftbuild [idx] [command] [groups] [projects] [ext]
```

Common commands include `checkout`, `applypatch`, `compile`, and `build`.
For this project, the Squirrel/module dependencies usually include projects
such as `SqPlus`, `sqlite`, `curl`, `openssl`, `ffmpeg`, `live555`, `poco`,
`portaudio`, `fftw`, `freetype2`, `mysql`, `tinyxml`, and others depending on
which `sqmod` targets you build.

### Building Winglib targets

Once dependencies are available and `deftbuild/v1` exists:

```sh
cd buildroot/lib/winglib
make
```

The top-level `Makefile` builds the core library, the Squirrel binding library,
the `sqrl` runner, selected Squirrel apps, and the default `sqmod` modules.

Useful build switches:

```sh
make DBG=1          # debug build, if supported by the deftbuild config
make UNICODE=1      # unicode build, if supported by the target
make PETS=1         # include extra apps and optional modules
make XMODS=1        # include experimental/extra modules listed under XMODS
make DOX=1          # include doxygen targets
make NOMULTI=1      # disable make's default parallel sub-build behavior
```

You can also build a specific project directly:

```sh
make -C lib/oexlib
make -C lib/sqbind
make -C app/sqrl
make -C sqmod/sqmod_curl
make -C sqmod/sqmod_openssl
```

## Adding a new Squirrel module

The existing modules all follow the same pattern:

1. Create `sqmod/sqmod_name/`.
2. Add a `Makefile` with `PRJ_TYPE := dll`, `PRJ_SUBROOT := _sqmod`, and the standard exports:
   `SRV_GetModuleInfo SRV_Start SRV_Stop SQBIND_Export_Symbols`.
3. Include `oexlib`, `sqbind`, `SqPlus`, `sqstdlib`, and `squirrel` in `PRJ_INCS` and `PRJ_LIBS`.
4. Register exported classes with `SQBIND_REGISTER_CLASS_BEGIN` and `SQBIND_MEMBER_FUNCTION`.
5. Export classes from `SQBIND_Export_Symbols`.
6. Load it from Squirrel with `_self.load_module("name", "")`.

`sqmod/sqmod_test` is the smallest place to start when copying the shape of a
module.

## Documentation

Doxygen inputs live in `dox/`:

- `dox/oexlib.dox`
- `dox/sqbind.dox`
- `dox/sqmod.dox`
- `dox/doxygen.cfg`

Build them with the `DOX=1` target if your deftbuild environment has the
required documentation tools.

## Security notes

This project exposes powerful native capabilities to scripts: filesystem
access, sockets, process execution, service control, dynamic library loading,
shared memory, TLS, databases, and media codecs.  Treat Squirrel scripts as
trusted code unless you have audited and sandboxed the specific host
application.

In particular:

- Avoid running untrusted scripts.
- Avoid passing untrusted input to shell/process helpers.
- Be careful with HTTP callbacks that write files, spawn commands, load modules, or serve arbitrary paths.
- Prefer explicit size limits for socket reads, binary buffers, uploads, and decoded media.
- Review platform-specific permission behavior before using shared memory or file creation in multi-user environments.

## License

Winglib is distributed under the permissive license in `LICENSE`.  In short,
source and binary redistribution are allowed for commercial and non-commercial
use, provided the copyright notice and license terms are retained.
