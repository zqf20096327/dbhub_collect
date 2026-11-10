# ransack

Multi-RAT cellular survey and recon for DragonOS. ransack fuses what several different sensors see —
an SDR, a rooted Qualcomm phone, a Rayhunter — into a single SQLite database with a versioned REST/SSE
API. LTE, 5G NR, 2G/GSM, and NB-IoT cells all land in the same `cells` table, merged on PLMN and cell
identity, so a GSM sighting and an LTE decode of one tower become one row instead of two. The name is
RAN (radio access network) + ransack.

Survey is passive, receive-only. A separate, human-driven plane captures subscriber identities
(IMSI/TMSI/IMEI) and is for your own network, a licensed engagement, or a shielded lab only.

ransack is a thin control plane: a daemon (`ransackd`) that owns the database, the API, and radio
arbitration, plus a set of small sensors that each wrap one proven tool (srsRAN, gr-gsm, Sni5Gect,
QCSuper, LTESniffer, FALCON, Rayhunter) and feed the shared DB. It does not reimplement the DSP — it
drives the tools the box already ships.

## Status

| Capability | Status | Notes |
|---|---|---|
| LTE survey (`cell_search` + MIB) | Validated OTA | LimeSDR Mini 2, live cells on bands 5 and 71 |
| LTE SIB1 identity (PLMN/TAC/cell-id) | Link-margin limited | MIB decodes on weak signal; SIB1 needs a few dB more |
| 5G NR survey + SIB1 | Validated OTA | Live NR cell on n25 |
| 2G/GSM survey — gr-gsm on SDR | Validated OTA | Parse confirmed against a live osmo-nid cell |
| 2G/GSM survey — OsmocomBB phone | Validated OTA | `cell_log` through a Motorola C118 |
| NB-IoT find (`cell_search_nbiot`) | Validated | Syncs to anchors; `--decode` (SIB1-NB) needs signal margin |
| Modem DIAG ingest (QCSuper) | Validated | Captures 2G/3G/4G/5G; ransack parses LTE SIB1 today (3G/UMTS not yet) |
| Rayhunter connector | Tested | Firmware v0.6.1 - v0.11.2 |
| LTE identity (LTESniffer DL/UL) | Parser validated | Self-test passes; live TMSI/IMSI pending decodable coverage |
| LTE activity (FALCON PDCCH) | File-validated | Real O2-DE recording; live capture pending |
| REST/SSE API + daemon | Validated | Crash recovery, idempotent operations, socket activation |
| Sensor fusion + gpsd geotag | Validated | Cross-RAT merge on PLMN + cell-id; RSRP-weighted tower estimate |

## Built for DragonOS Resolute (26.04)

ransack assumes the heavy pieces are already on the box, and the supported platform is
[DragonOS](https://cemaxecuter.com/) Resolute (Ubuntu 26.04), where the cellular toolchain it
orchestrates is pre-installed: srsRAN 4G, gr-gsm, Sni5Gect, QCSuper, LTESniffer / ltesniffer-dl,
FALCON, the LimeSuite stack, and gpsd.

ransack does not bundle these — it drives them. Every sensor is fail-soft: a missing tool degrades that
one sensor and reports why, rather than breaking the rest. You can run it off DragonOS, but you have to
provide those tools yourself (see [Install](#install)). Treat 26.04 Resolute as the target.

## Sensors

| RAT | Survey | Wraps | Identity / deeper |
|---|---|---|---|
| 2G / GSM | `ransack-gsm` | gr-gsm `grgsm_scanner`, or OsmocomBB on a Calypso phone | `ransack-imsi` (IMSI/TMSI) |
| LTE / 4G | `ransack`, `ransack-sweep` | srsRAN `cell_search` + `srsue`, tshark SIB decode | `ransack-lte-ue` (LTESniffer), `ransack-pdcch` (FALCON) |
| NB-IoT | `ransack-nbiot` | srsRAN `cell_search_nbiot` + `npdsch_ue` | |
| 5G NR | `ransack-nr` | Sni5Gect scanner (SSB, then MIB/SIB1) | |
| modem (2G-5G) | `ransack-modem` | QCSuper reading a Qualcomm DIAG stream | |
| recorded | `ransack-rayhunter` | EFF Rayhunter recordings + its alerts | |

Coverage notes: QCSuper logs the full 2G/3G/4G/5G DIAG stream, so the 3G/UMTS signalling is in the
pcap — ransack just doesn't parse it into cells yet. Today `ransack-modem` extracts LTE (E-UTRA) SIB1
cell identity from that capture; UMTS has a schema column but no decoder wired to it. 5G here is survey
only; Sni5Gect's transmit/effect side is out of scope for this repo.

### Radios

Use the classic LimeSuite `driver=lime` for the srsRAN LTE path — limesuiteng rejects the mid-stream
sample-rate changes `cell_search` makes.

| SDR | LTE / NB-IoT | GSM | 5G NR | LTE identity |
|---|---|---|---|---|
| LimeSDR (`driver=lime`) | yes | yes | | |
| USRP B210 / X310 | yes | yes | yes (UHD only) | downlink 1 SDR; uplink needs 2x B210 + GPSDO |
| bladeRF | yes | yes | | |
| Pluto / HackRF / RTL-SDR | NB-IoT: experimental | via SoapySDR | | |

The modem sensor needs a rooted Qualcomm phone (adb) or a USB DIAG modem; the phone-based 2G path
needs a Calypso handset (Motorola C1xx and similar) running OsmocomBB.

## Usage

```bash
ransack -b 12                                  # survey LTE band 12 into the DB
ransack-sweep --preset us                      # fan every common US band across all SDRs at once
ransack-cells                                  # list what's been found
ransack-gsm  scan --band PCS1900               # survey 2G
ransack-nr   scan                              # survey 5G NR (SSB -> SIB1)
ransack-nbiot scan --decode                    # find NB-IoT anchors and decode SIB1-NB
ransack-menu                                   # interactive TUI over all of the above
```

Example run:

```
$ ransack -b 12
[ransack] cell_search band 12 ...
[ransack] EARFCN 5035 PCI 493: PLMN 001-01 TAC 1 CID 100
[ransack] EARFCN 5110 PCI 288: PLMN 001-01 TAC 1 CID 101
[ransack] done. 2 cells in ~/.ransack/cells.sqlite

$ ransack-cells
 earfcn  band   pci      plmn    tac      cell_id  last_seen
   5035    12   493   001-01   1    100  2026-08-17T20:41:05Z
   5110    12   288   001-01   1     101  2026-08-17T20:41:52Z
```

### Survey, then engage

One shared table means you survey once and target anything you found. For LTE a single `--earfcn`
resolves the frequency, band, PCI, and PRB (and the uplink frequency) from the survey row:

```bash
ransack -b 12                                          # survey
ransack-lte-ue monitor --earfcn 5035 --mode 0          # downlink: TMSI/paging, one SDR
ransack-lte-ue monitor --earfcn 5035 --mode 1 \        # uplink+downlink: IMSI/IMEI/UE-capability
    --serial-a <dl-serial> --serial-b <ul-serial>      #   2x B210 + GPSDO
```

For 2G: `ransack-gsm scan`, then `ransack-imsi catch --auto` points the catcher at the strongest GSM
cell found. That chain uses a bound UDP socket, not a raw sniff, so it needs no sudo.

## API

`ransackd` serves a versioned REST/SSE API on `127.0.0.1:8082`.

```
POST /v1/scans   {"bands":[12,71]}            start a scan            -> {"scan_id": 42}
GET  /v1/cells?band=12&seen_within=2h         discovered cells (filtered)
GET  /v1/events                               live SSE: cell_found, scan_progress, scan_done, ...
GET  /v1/map                                  estimated tower positions + observations as GeoJSON
GET  /v1/export?format=csv                    bulk pull
```

Also: `health`, `version`, `ready`, `describe`, `sdrs`, `cells/<id>`, `cells/<id>/measurements`,
`observations`, `plmns`, `scans`, `scans/<id>`, plus `POST /v1/monitor` and `DELETE /v1/scans/<id>`.
The SSE journal is durable, so a client (or the daemon after a restart) can replay from the last event
id it saw.

## MCP

ransack ships a Contract 1.0 capability descriptor
(`share/dragon-agent/providers.d/ransack.json`) rather than its own MCP server. DragonOS's
`dragon-mcp-gateway` reads that descriptor, renders each capability as an MCP tool, and routes calls to
`ransackd`'s `/v1`. It is pure stdlib over stdio, opens no port, and needs no key of its own.

```bash
claude mcp add dragon -- dragon-mcp-gateway
```

ransack then appears as `ransack__scan_band`, `ransack__list_cells`, `ransack__list_plmns`,
`ransack__geolocate_cells`, plus the lifecycle tools (`operation_status`, `operation_results`,
`operation_cancel`, `ready`).

Two properties worth stating plainly:

- The API key lives with the agent, not with ransack. Claude Code uses your own Anthropic login or
  `ANTHROPIC_API_KEY`; DragonOS's `dragon-rf-agent` reads `dragon-brain`'s key from
  `/etc/dragon-brain.conf`, then `~/.config/dragon-brain.conf`, then the environment. Without a key the
  CLIs, TUI, and API still work fully.
- The descriptor exposes only the passive survey. The identity-capture tools are not in it, so an agent
  driving the gateway cannot trigger a subscriber-identity capture — that plane is CLI-only.

## Runs as you, not root

ransack writes your `~/.ransack/cells.sqlite` and runs the survey without sudo. SDR realtime priority
comes from the `usrp` group, not root; the GSM catcher listens on a bound UDP socket instead of
raw-sniffing, so it never needs `CAP_NET_RAW`. If a tool genuinely does need sudo, `ransackd` still
resolves `~` to your home via `SUDO_USER`, so the database never forks into `/root`.

## Install

On DragonOS Resolute the whole toolchain is already on the image:

```bash
sudo apt install ./ransack_*.deb
```

The daemon is socket-activated: systemd holds `127.0.0.1:8082` and starts `ransackd` on the first
request. Config lives at `/etc/ransack/config.yml`.

Off DragonOS, install the runtime and add only the tools for the sensors you want:

```bash
sudo apt install python3 python3-flask python3-yaml python3-jsonschema sqlite3 tshark iproute2 curl
sudo dpkg -i ransack_*.deb        # or run bin/ransack* out of the repo
```

| Sensor | Needs |
|---|---|
| LTE / NB-IoT | srsRAN 4G (`cell_search`, `srsue`, `cell_search_nbiot`, `npdsch_ue`) |
| 5G NR | Sni5Gect |
| GSM / identity | gr-gsm, OsmocomBB, an IMSI-catcher |
| modem | QCSuper + a rooted Qualcomm phone or DIAG modem |
| LTE identity | LTESniffer (uplink: 2x B210 + GPSDO) and/or ltesniffer-dl (downlink, one SDR) |
| LTE activity | FALCON |
| geotagging | gpsd (optional; positions are null without a fix) |

SDR drivers: UHD for USRP, SoapySDR classic `driver=lime` for LimeSDR, the respective Soapy/UHD modules
for bladeRF/HackRF/RTL.

## Configuration

`/etc/ransack/config.yml` (or `~/.ransack/config.yml`). Everything is optional:

```yaml
api:     { host: 127.0.0.1, port: 8082 }
db:      ~/.ransack/cells.sqlite
device:  { driver: lime, args: "driver=lime,rxant=LNAW" }
scan:    { default_bands: [2, 4, 5, 12, 13, 71], gain: 55, secs: 25, recurse: true }
gps:     { enabled: auto, host: 127.0.0.1, port: 2947, max_age_s: 5 }
```

Most sensors also take an environment override for the radio (`RANSACK_NBIOT_ARGS`,
`RANSACK_GSM_SDR_ARGS`, `RANSACK_NR_DEV`, ...) so you can point one at a second SDR.

## Legal

The survey plane is passive receive-only — it reads the broadcast SIBs and SSBs cells already
transmit. The identity plane (IMSI/TMSI/IMEI) is different: run it only against a network you own,
under a licensed engagement, or in a shielded enclosure with a test SIM. Every run is logged to the
`scans` table. You are responsible for compliance with local law.

## License

GPL-2.0-or-later, Copyright 2025-2026 CEMAXECUTER LLC. See [LICENSE](LICENSE).
