# OceanBaseCL

A customized build of **OceanBase CE 4.4.2** (`v4.4.2_CE`).

This repository is a **proof-of-concept**: it demonstrates the full lifecycle of
modifying a hardcoded behavior in OceanBase's C++ source, compiling the project
from scratch, and producing a working `observer` binary — then verifying the
change on a running cluster.

The experiment completed successfully. See [Result](#result) below.

---

## What was changed

The goal was to lower the minimum allowed value of `PIECE_SWITCH_INTERVAL`
(the log-archiving piece switch interval, used when archiving redo logs to S3).
In stock OceanBase CE this minimum is **hardcoded to 1 day**, which rejects any
attempt to set a shorter interval:

```
ALTER SYSTEM SET LOG_ARCHIVE_DEST='LOCATION=s3://... PIECE_SWITCH_INTERVAL=1h' TENANT='bench';
-- stock build: ERROR — invalid piece_switch_interval out of range [1d,7d]
```

Three source files were modified:

| File | Change |
|------|--------|
| `src/share/backup/ob_backup_config.cpp` | Lowered the hardcoded minimum from `1d` to `1h` (`MIN_LOG_ARCHIVE_PIECE_SWITCH_INTERVAL`), and updated the range error message accordingly. **This is the functional change.** |
| `src/observer/main.cpp` | Version banner tag (`observer -V`) changed to `OceanBase_CE_CL`. |
| `src/share/system_variable/ob_system_variable.cpp` | SQL-visible version strings (`version()` and `version_comment`) tagged `OceanBase_CE_CL`. |

> Note: OceanBase validates `PIECE_SWITCH_INTERVAL` in two layers. The low-level
> validity check in `ob_backup_struct` already permits values down to 1 minute,
> so the effective 1-day gate lives entirely in `ob_backup_config.cpp`. Only that
> one constant needed to change to allow `1h`.

The `_CL` version tag is purely cosmetic — it exists so a running instance can be
identified as this custom build via `observer -V` or `SELECT version();`.

---

## Why the 1-day default exists

The stock minimum is not arbitrary. A shorter piece switch interval produces more
frequent archive "pieces", which means more small objects on the archive target
(S3) and higher archive-management overhead. Lowering it to `1h` is appropriate
for testing and benchmarking workloads; use a shorter interval in production only
deliberately.

---

## Build environment

- **OS:** AlmaLinux 9.6 (RHEL 9 family)
- **glibc:** 2.34
- **Compiler:** Clang 17 (bundled by OceanBase's `build.sh --init`)
- **Source tag:** `v4.4.2_CE` (commit `e859d1b9c9`)

### Build steps

```bash
git clone https://github.com/Constantine-SRV/OceanBaseCL.git
cd OceanBaseCL
git checkout oceanbase-cl

# system prerequisites
sudo dnf install -y git wget rpm cpio make glibc-devel glibc-headers \
                    binutils m4 libtool libaio python3
sudo alternatives --install /usr/bin/python python /usr/bin/python3 1

# fetch dependencies + configure (downloads a prebuilt toolchain)
bash build.sh release --init

# compile just the observer
cd build_release
make observer -j4
```

The resulting binary is at:

```
build_release/src/observer/observer
```

---

## Result

The custom binary built and ran successfully. `observer -V` on the running server:

```
observer (OceanBase_CE_CL 4.4.2.0)
REVISION: 1-e859d1b9c9a6d11d856f4fed5b6385f1a6795820
BUILD_BRANCH: HEAD
BUILD_TIME: Jun 29 2026 10:30:45
BUILD_FLAGS: RelWithDebInfo
BUILD_INFO:
Copyright (c) 2011-present OceanBase Inc.
```

The custom tag is also visible from SQL:

```sql
SELECT version();
-- 5.7.25-OceanBase_CE_CL-v4.4.2.0

SHOW VARIABLES LIKE 'version_comment';
-- OceanBase_CE_CL 4.4.2.0 (r1-e859d1b9c9a6d11d856f4fed5b6385f1a6795820) (Built Jun 29 2026 10:30:45)
```

And the previously rejected command now succeeds — `PIECE_SWITCH_INTERVAL=1h`
is accepted instead of failing with `out of range [1d,7d]`.

---

## Prebuilt binary

A stripped, gzip-compressed `observer` binary is attached to the
[Releases](../../releases) page.

```bash
gunzip observer-cl.gz
```

**Compatibility:** the prebuilt binary is dynamically linked against **glibc 2.34**.
It runs on RHEL / AlmaLinux / Rocky 9+ and recent Ubuntu, but **not** on el7/el8
(glibc < 2.34), where it fails with `GLIBC_2.34 not found`. For older systems,
rebuild from source in a matching environment.

---

## License

OceanBase CE is licensed under **Mulan PubL v2**. This fork retains the original
`LICENSE` and all upstream copyright notices. It is a modification of OceanBase CE
for evaluation purposes and is not affiliated with or endorsed by OceanBase.
