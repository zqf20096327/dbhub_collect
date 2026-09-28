# sypexgeo (Rust)

[![Crates.io](https://img.shields.io/crates/v/sypexgeo.svg)](https://crates.io/crates/sypexgeo)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Rust](https://img.shields.io/badge/rust-1.70%2B-orange.svg)](Cargo.toml)

Pure-Rust reader for the SypexGeo binary IP-to-geo database. Zero runtime dependencies, std only.

Supports **Country**, **City** and **City Max** database variants in file, in-memory and batch modes.

Port of [GLOBUS-studio/SypexGeo](https://github.com/GLOBUS-studio/SypexGeo) (PHP).

## Features

- Pure Rust — no C bindings, no external crates.
- Reads SypexGeo v2.x binary `.dat` files.
- File, in-memory and batch lookup modes (combinable as bit flags).
- Country code, country ID, city, and full city+region+country lookups.
- Full pack-format binary decoder (all 14 field types).
- IPv4 only; private/reserved ranges return empty/None.

## Requirements

- Rust 1.70 or newer.
- A SypexGeo binary database file — download from [sypexgeo.net](https://sypexgeo.net/en/download/).

## Installation

Published on [crates.io](https://crates.io/crates/sypexgeo):

```toml
[dependencies]
sypexgeo = "0.1"
```

Or via Cargo:

```bash
cargo add sypexgeo
```

## Usage

```rust
use sypexgeo::{SxGeo, mode};

let sx = SxGeo::open("/absolute/path/to/SxGeoCity.dat", mode::MEMORY)?;

sx.get_country("8.8.8.8");     // "US"
sx.get_country_id("8.8.8.8");  // internal numeric id
sx.get_city("8.8.8.8");        // Some(GeoCity { city, country })
sx.get_city_full("8.8.8.8");   // Some(GeoCityFull { city, region, country })
sx.get("8.8.8.8");             // City (City DB) or Country (Country DB)
sx.about();                    // database metadata
```

### Lookup modes

Modes are bit flags and may be combined:

| Constant        | Value | Behaviour                                          |
| --------------- | ----- | -------------------------------------------------- |
| `mode::FILE`    | 0     | Read from disk on every lookup. Lowest memory.     |
| `mode::MEMORY`  | 1     | Load the whole database into RAM. Fastest reads.   |
| `mode::BATCH`   | 2     | Pre-decode indices for faster repeated lookups.    |

```rust
let sx = SxGeo::open("/path/to/SxGeoCity.dat", mode::MEMORY | mode::BATCH)?;
```

## API reference

| Method | Returns |
| ------ | ------- |
| `open(path, flags)` | `Result<SxGeo, Error>` |
| `get(ip)` | `Option<LookupResult>` — City for City DB, Country otherwise |
| `get_country(ip)` | `String` — ISO 3166-1 alpha-2 code, empty for invalid IPs |
| `get_country_id(ip)` | `u32` — Internal numeric country ID, `0` for invalid IPs |
| `get_city(ip)` | `Option<GeoCity>` — `{ city, country }` |
| `get_city_full(ip)` | `Option<GeoCityFull>` — `{ city, region, country }` |
| `about()` | `About` — Database metadata |

Notes:
- IPv4 only. Private/reserved ranges (`10/8`, `127/8`, `0/8`) return empty/None.
- `open()` returns `Error::Io`, `Error::InvalidSignature`, or `Error::InvalidFormat`.

## Example

See [`examples/lookup.rs`](examples/lookup.rs) for the full example.

```bash
# Download a database from https://sypexgeo.net/en/download/
# and place it in tests/fixtures/, then:
cargo run --example lookup
```

```
SxGeo City EN  ·  utf-8  ·  5 995 121 blocks  ·  2025.12.19

8.8.8.8
  Country  US  (id: 225)
  City     Mountain View  37.3861, -122.0839
  Region   California  US-CA
  Country  United States  39.76, -98.5
```

## Testing

```bash
cargo test
```

Unit tests run without a database. To test against a real `.dat` file, place one in `tests/fixtures/` (see [tests/fixtures/README.md](tests/fixtures/README.md)) and run:

```bash
cargo test -- --ignored
```

## License

MIT, see [LICENSE](LICENSE).

## Credits

Ported from the PHP library maintained by [GLOBUS.studio](https://globus.studio) and Yevhen Leonidov, based on the original SypexGeo by zapimir and BINOVATOR.
