# iceberg-arrow-deps

Apache Arrow C++ dependency for the datainfra Iceberg + openGauss integration.

This repository provides a reproducible build script for Apache Arrow C++ 24.x,
which is required by the `iceberg_delta` extension. The resulting install tree
is placed next to this repository at `../arrow_install`.

## Layout

```text
iceberg-arrow-deps/       # this repository
├── README.md
├── build_arrow.sh        # build Apache Arrow C++ from source
├── .gitignore
└── apache-arrow-24.0.0.tar.gz   # pinned source tarball (committed for offline builds)

arrow_build/              # generated build directory (gitignored)
├── apache-arrow-24.0.0.tar.gz
├── arrow-apache-arrow-24.0.0/
└── build-24.0.0/

arrow_install/            # generated install prefix (gitignored)
├── include/arrow/...
└── lib64/libarrow.so*
```

## Quick start

```bash
cd /path/to/datainfra/iceberg-arrow-deps
./build_arrow.sh
```

On first run the script downloads `apache-arrow-24.0.0.tar.gz` into this
directory. The tarball is kept so subsequent runs do not re-download it.
The pinned tarball is also committed to the repository so that fresh clones
can build offline without internet access.

## Offline build

The repository already contains the pinned `apache-arrow-24.0.0.tar.gz`, so
offline builds work out of the box. If you need a different version, download
its tarball manually and place it in this directory before running
`build_arrow.sh`:

```bash
cd /path/to/datainfra/iceberg-arrow-deps
curl -LO https://archive.apache.org/dist/arrow/arrow-24.0.0/apache-arrow-24.0.0.tar.gz
./build_arrow.sh
```

## What gets built

Only the core Arrow C++ shared library with IPC support:

- `libarrow.so` (shared)
- Arrow IPC support (built into `libarrow`)

Heavy components such as Parquet, Dataset, Flight, Gandiva, HDFS, S3, and
Python bindings are disabled to keep build time reasonable.

## Integration

`iceberg-opengauss-build/env.sh` sets:

```bash
export ARROW_HOME="${ARROW_HOME:-$ICEBERG_OG_ROOT/arrow_install}"
```

`iceberg-opengauss-build/06-build-delta.sh` passes `-DARROW_HOME="$ARROW_HOME"`
to `iceberg_delta/CMakeLists.txt`. If you installed Arrow elsewhere, set
`ARROW_HOME` in your `local.env` or environment before building.

## Requirements

- CMake >= 3.10
- A C++17-capable compiler (the integration uses GCC 10.3 from binarylibs)
- `curl` or `wget` to download the source tarball on first build (unless the
  tarball is provided locally)

## Updating Arrow

To upgrade to a newer Arrow version:

1. Delete the old `apache-arrow-*.tar.gz` in this directory.
2. Update `ARROW_VERSION` in `build_arrow.sh`.
3. Re-run `./build_arrow.sh`.
