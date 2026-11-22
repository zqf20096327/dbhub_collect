# Dark Store Prototype

A working prototype of the **micro-warehousing module** of a Blinkit-style quick-commerce app.
It follows the team's High-Level Design (HLD): one module per HLD service, one Inventory Service
that owns every stock change, and a checkout hold that makes overselling impossible.

It is a *modular monolith*: a single FastAPI app with SQLite, so anyone can run it in two minutes
with no setup. The module boundaries are the same as the HLD's service boundaries, so each part
can later be split out, moved to PostgreSQL, or put behind Kafka without a redesign.

## Live demo

Hosted on the course's lab servers. The addresses work only from the campus network.

| What | Where |
| --- | --- |
| The three demo stations (customer, picker, store ops) | http://10.1.75.53:6250 |
| Ops dashboard, picker phone screen, store network map | http://10.1.75.53:6250/ops.html, [`/picker.html`](http://10.1.75.53:6250/picker.html), [`/network.html`](http://10.1.75.53:6250/network.html) |
| API reference | http://10.1.75.53:6250/docs |
| Monitoring (Grafana, *Dark store* dashboard) | http://10.1.75.53:6252 |

It is a shared demo: the data is reset often and the demo accounts use the password `demo`, so do not enter anything
real.

## What works today

| Flow | What you can do |
| --- | --- |
| Find a store | Give a location, get the serving store and an ETA, or "not serviceable" |
| Shop | See only the items that store can deliver right now (available = on hand − held − a small safety buffer) |
| Checkout | Hold a whole cart for 10 minutes; the cart is held whole or not at all |
| Pay or cancel | Paying creates a pick job; cancelling or timing out gives the stock back; a paid order can still be cancelled until it is packed |
| Pick | A picker claims the next order and gets lines in walking order, oldest batch first; when 4 or more orders wait, a picker takes 3 in one walk, one tote each |
| Scan | Every line is checked by barcode; a wrong item is rejected; units can be scanned one at a time |
| Empty shelf | The bin's count is corrected (units other orders are still waiting for stay until their picker gets there), the line moves to another bin, or is dropped if none is left; if only some were there ("found 4 of 6"), those are kept |
| Pack and hand off | Packing commits the sale and assigns a rider; the rider checks in for the crate slot, and the bag is handed over only if the scanned bag is that rider's order |
| Restock | Low items are reordered from the hub every 15 minutes or on demand, in whole cases and within free shelf space; a truck is scanned onto the dock and each line is sellable the moment it is put away, while damaged or short-dated units never enter stock |
| Forecast | Reorder points are recalculated from a weekday-aware forecast; three models are compared by measured error (WAPE) |
| Watch | An ops dashboard with problems first and every HLD 12 KPI beside its target, plus a live event feed for each store |

Automated tests cover these flows and the permission rules, including twenty buyers racing for the last unit.

## Quick start

You need Python 3.10 or newer.

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app (the database and demo data are created on first start)
python -m uvicorn app.main:app --reload
```

Then open:

- **http://localhost:8000** for the demo screens (customer, picker and store ops side by side)
- **http://localhost:8000/ops.html** for the ops dashboard (KPIs against HLD 12 targets, updated live)
- **http://localhost:8000/picker.html** for the picker's phone screen: one line at a time, big buttons
- **http://localhost:8000/docs** for the interactive API reference
- **http://localhost:8000/metrics** for Prometheus metrics (alert rules in `docs/ARCHITECTURE.md`, section 9)

Run the tests with `python -m pytest -q`; `tests/test_end_to_end.py` walks the whole demo script through
the API with real logins. Reset the demo data with the button on the ops desk, or with `python -m app.seed`.

To load-test a running app (about 90% reads, 10% checkout holds, a fifth of them paid) and see p50 and p99
per endpoint against the HLD's 100 ms read target, start the app with the rate limit off
(`RATE_LIMIT_PER_SECOND=0 python -m uvicorn app.main:app`; the script is one client) and run
`python scripts/load_test.py --seconds 60 --reset`.

The demo data has one week of sales, too little to judge a forecast model: its accuracy shows as not
available. To try the models on two months of history, run `python scripts/generate_sales.py`, then call
`GET /v1/forecasting/compare?store_id=1` in `/docs`.

To pick on a real phone, start the app with `python -m uvicorn app.main:app --host 0.0.0.0` and open
`http://<laptop-ip>:8000/picker.html?store=1` on a phone on the same Wi-Fi. Do this only on a network you trust:
every demo account has the same password.

Two fulfilment experiments run on a throwaway copy of the demo data, so they need no server and leave
`darkstore.db` alone: `python scripts/compare_picking.py` compares walking with and without batch picking, and
`python scripts/simulate_orders.py` has scripted pickers clear 100 paid orders through the API, then prints the
fulfilment KPIs beside their HLD 12 targets (`--pickers 3`, `--single`, `--step 0.2` to change the run).
`python scripts/compare_slotting.py` does the same for slotting: the walk of 200 random orders before and after
the slotting plan is applied.

To see where a new store should go, run `python scripts/generate_demand.py`, then open
**http://localhost:8000/network.html**.

### With Docker

If you have Docker, one command builds and starts the app on http://localhost:8000
(the SQLite file is kept in a Docker volume, so data survives restarts):

```bash
docker compose up --build
```

To run the app on PostgreSQL, the HLD's database, instead of the SQLite file:

```bash
DARKSTORE_DB=postgresql://darkstore:darkstore@postgres:5432/darkstore docker compose --profile postgres up --build
```

`DARKSTORE_DB` is the only setting that changes: any PostgreSQL URL works, including a hosted database such as
Amazon RDS (then leave out `--profile postgres`). Without Docker, set `DARKSTORE_DB` the same way before
`python -m uvicorn app.main:app`. The app creates its tables in an empty database and migrates an existing one
when it starts (`CONTRIBUTING.md`, "When you change the database tables").

To also start Prometheus and Grafana (HLD 12 monitoring):

```bash
docker compose --profile monitoring up --build
```

- **Grafana** at http://localhost:3000 opens on the *Dark store* dashboard; viewing needs no login (to edit, log in as
  `admin` with `GRAFANA_ADMIN_PASSWORD`, default `admin`, local only).
- **Prometheus** at http://localhost:9090 scrapes the app every 5 seconds and evaluates the alert rules from
  `docs/ARCHITECTURE.md` section 9 (*Alerts* tab; nothing is sent anywhere, there is no Alertmanager).
- Both listen on this machine only. Their configuration is in `monitoring/`.
- To fill the graphs, run the load test against it: start with `RATE_LIMIT_PER_SECOND=0 docker compose --profile
  monitoring up --build` (the load test is one client), then `python scripts/load_test.py --seconds 120`.

![Grafana dashboard during a load test](docs/img/grafana-dashboard.png)

`docker compose down -v` stops everything and deletes the stored data.

**On a server:** [docs/DEPLOY_AWS.md](docs/DEPLOY_AWS.md) puts the prototype on one AWS EC2 instance with Docker,
with the settings in `deploy.env` (template: `deploy.env.example`), plus optional RDS, HTTPS and monitoring.

## Logging in

Customer endpoints (serviceability, availability, reservations) are open, but rate-limited: about 20 calls a
second per address, with bursts of 40 (`RATE_LIMIT_PER_SECOND`, `RATE_LIMIT_BURST`; 0 turns it off), and `429`
beyond that. Everything else needs a
staff token. The demo data has `picker1`, `packer1`, `receiver1`, `manager1` (and `...2` for the
second store), plus city-wide `ops` and `admin`. They all use the password `demo`.

```bash
TOKEN=$(curl -s localhost:8000/v1/auth/login -H "Content-Type: application/json" \
  -d '{"username":"manager1","password":"demo"}' | python -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
curl localhost:8000/v1/stores/1/dashboard -H "Authorization: Bearer $TOKEN"
```

In `/docs`, press *Authorize* and paste the token. The demo screens log in by themselves.
Tokens last 30 minutes. Outside local development set `JWT_SECRET` (signing key) and
`DEMO_PASSWORD` in the environment; the built-in defaults are public.

Staff may act only on their own store: pickers and packers pick and pack, receivers and managers
receive goods, managers adjust stock and run replenishment and forecasting, `ops` can read every
store, and `/v1/admin/*` needs `admin`.

Every call a logged-in staff member makes to a protected endpoint, refused or not, is kept in an audit log.
`admin` reads it newest first at `GET /v1/audit` (`?username=picker1&limit=50` to narrow it).

## Five-minute tour

1. On the **customer** station, press *Check delivery*, add 8 milk and 1 ice cream, then *Hold my items*.
   On the **ops** station the "Held" column changes at once; "On hand" does not.
2. Press *Pay now*. An `order.paid` event appears and "Waiting for a picker" becomes 1.
3. On the **picker** station press *Get next order*. The milk is split across two bins: the batch
   that expires first is picked first.
4. Try *Scan a wrong item* (rejected), then *Scan item* on each line, then *Mark packed*.
   Only now does "On hand" drop: the sale is committed at packing.
5. On the ops station press *Check what needs reordering*, then *Hub dispatches truck*, then
   *Receive truck*. The bread is back in stock and visible to the customer.

`docs/DEMO_SCRIPT.md` has the full script for presenting, including the "last ice cream" race.

## Project layout

```
app/
  main.py            builds the app and plugs in every module
  config.py          every tunable number (hold time, lead time, thresholds)
  db.py              database engine and sessions
  models.py          all tables (HLD section 7.1)
  events.py          in-process event bus that stands in for Kafka
  seed.py            demo data
  modules/           one package per HLD service; each has service.py (logic) + router.py (HTTP)
    serviceability/  inventory/  fulfilment/  pickpack/  inbound/  replenishment/
    forecasting/     slotting/   assortment/  network_planning/    dashboard/
web/                 the demo screens (plain HTML, CSS and JavaScript; no build step)
scripts/             developer tools; generate_sales.py writes 60 days of seeded sales history
tests/               pytest suite
docs/                architecture notes, team plan and one guide per team member
```

## How the prototype maps to the HLD

| HLD service | Module | In the prototype | Simplified for now |
| --- | --- | --- | --- |
| 1 Serviceability | `serviceability` | H3 cell to store lookup, ETA, zone shrinks when the store is busy | Zones are rebuilt by hand (`POST /v1/admin/rebuild-zones`); a cell has one store, so a busy or closed store's customers are not passed to a neighbour |
| 2 Assortment | `assortment` | List, add and drop SKUs per store; add, drop and shelf-room recommendations from the last 30 days of sales | Recommendations only: a manager applies them |
| 3 Inventory | `inventory` | ATP with a per-SKU safety buffer (`PUT /v1/stores/{id}/stock-settings/{sku_id}`), atomic holds, confirm, release (race-proof), automatic expiry sweep every `SWEEP_INTERVAL_SECONDS`, adjustments, ledger, FEFO allocation that skips expired batches, hourly expiry write-off and near-expiry report (`GET /v1/stores/{id}/near-expiry`), `Idempotency-Key` header on stock adjustments, 2-second ATP cache for whole-store availability, cleared on every stock write (`app/cache.py`), blind cycle counts with manager approval above `COUNT_AUTO_APPROVE_VALUE` and an inventory accuracy KPI, stock audit of level, bins and ledger (`GET /v1/admin/stock-audit`), checkout race test (`scripts/load_checkout.py`: 200 buyers, 50 units), every bin quantity changed by one conditional `UPDATE`, `swap_line` (substitutes) and `move` (bin to bin) for other modules | saved keys are never cleaned up; a write-off does not cancel a paid order holding those units (the picker's empty-shelf report settles it) |
| 4 Fulfilment Orchestrator | `fulfilment` | Job per paid order, pick tasks, state machine, store busy flag; cancel a paid order until it is packed (`POST /v1/fulfilment-jobs/{id}/cancel`, holds given back, `order.cancelled` published); KPIs: order-to-pack p50/p90, fill rate, items per picker-hour (`GET /v1/stores/{id}/fulfilment-metrics`); stalled orders (no claim, scan or shelf report for `PICK_STALL_MINUTES`) go back to the queue every `STALL_CHECK_SECONDS`, or are flagged if items are in a tote (`GET /v1/stores/{id}/attention`, also bags waiting over `RIDER_WAIT_MINUTES`) | A packed order cannot be cancelled (that is a return, not built); the store manager stands in for the Order service that would call cancel and refund; a stalled order with items in a tote is only flagged, for a person to fetch; a revived handheld is kept out of another picker's order only if it sends `picker_id` (the demo station does) |
| 5 Pick & Pack | `pickpack` | Picker phone screen (`/picker.html`); claim next order, or at peak a batch of up to `BATCH_SIZE` in one walk, one tote each (`GET /v1/pickers/{id}/next-batch`; `scripts/compare_picking.py` measures the walking saved), scan check unit by unit (`scanned_qty`, `picked_at` per line), empty-shelf fallback with partial finds (`{"found": n}`), a substitute offered for dropped units (same category, no dearer than the missing item, nearest price) and `order.line_dropped` for the refund, pack | A category is one kind of item, so the demo catalogue has one offer: frozen peas for missing ice cream; batches are only the oldest orders, not grouped by where their items are; in the demo the picker accepts a substitute on the customer's behalf (`POST /v1/fulfilment-jobs/{id}/substitutions`; only the item on offer, so the customer is never charged more than they were refunded), where a real app would ask the customer; units found but not scanned are trusted without a barcode check; a batch that expires while being picked cannot be scanned any more: *Not on shelf* moves the rest to a fresh batch, and units already in the tote are delivered |
| 6 Slotting | `slotting` | Fast movers nearest the packing desk: each zone's SKUs ranked by units sold a day over 14 days get bins in walking order (`GET /v1/slotting/plan`), and `POST /v1/slotting/apply` moves the batches with `inventory.move`, never past a bin's capacity, skipping batches a picker is on the way to; new deliveries go to a SKU's planned bin first; a delivery is split over bins with room | Re-sorts bins only within a temperature zone; apply records the moves at once, so staff carry the stock straight away, at a quiet time; no affinity rule (items bought together) |
| 7 Forecasting | `forecasting` | Moving average, weekday average and exponential smoothing compared by WAPE backtest; reorder points with safety stock from forecast errors | Daily, not hourly; no weather or festivals |
| 8 Replenishment | `replenishment` | Reorder-point check every 15 minutes and on demand, whole cases, capped by free bin space (most urgent first), in-transit stock, stop reordering one SKU before dropping it or change its reorder point (`PUT /v1/stores/{id}/reorder-settings/{sku_id}`), supply KPIs (`GET /v1/stores/{id}/supply-kpis`) | Run the timer in one app instance (`REPLENISHMENT_INTERVAL_MINUTES=0` on the others) |
| 9 Inbound | `inbound` | Saved goods receipts in five steps (`/v1/goods-receipts/open`, `/{id}/scans`, `/{id}/putaway-tasks`, `/{id}/putaway`, `/{id}/close`): scanned units (with their batch and expiry) wait on the dock, each line is sellable the moment it is put away, damaged units and batches with under half their shelf life left are never stocked, and closing reports ordered versus received (`send_back=true` returns what is left on the dock); a receipt with nothing scanned cannot close (`409 nothing_scanned`), and one opened or scanned by mistake is cancelled until anything is put away (`/{id}/cancel`), so the truck can still be received; putaway within bin capacity (`409 bin_full`); `Idempotency-Key` on every write; the one-call `POST /v1/goods-receipts` runs the five steps | The ops screen receives a truck in one call; the five steps are API only |
| 10 Network Planning | `network_planning` | Orders and turned-away lookups per H3 cell, greedy max-coverage site suggestions, no-go cells, map at `/network.html` | Demand is generated (`scripts/generate_demand.py`); no-go cells are a config list, not a zoning check |
| 11 Rider Handoff | `fulfilment` (`riders.py`) | A rider assigned when the order is packed; `POST /v1/riders/{id}/arrive` gives the crate slot; handover takes `rider_id` and `scanned_order_id` and refuses a wrong bag (`409 wrong_bag`) or rider (`409 wrong_rider`); packed-to-handover p90 in the fulfilment KPIs | No real rider system: riders are made up from a fixed list; the desk checks riders in and scans for them |
| Kafka | `events.py` | Events written to an outbox table; a relay pushes them to sinks (a WebSocket feed per store) and marks them published; lag shown on the dashboard | No broker yet; the relay runs inside the app |
| PostgreSQL + Redis | `db.py`, `cache.py`, `migrations/` | SQLite by default, PostgreSQL when `DARKSTORE_DB` is a `postgresql://` URL (the tests pass on both); Alembic migrations, applied at start-up; ATP cache in each app process (Redis stand-in) | No sharding (every stock query already filters by `store_id`); on an empty database, start one app instance first (two starting together would both load the demo data); each app instance has its own cache, so another instance can be up to 2 s behind |
| Auth, gateway | `auth.py` | Login with a signed token; roles and own-store checks on every staff endpoint; audit log of staff calls (`GET /v1/audit`); per-client rate limit on the open endpoints (`429`) | No gateway or mutual TLS; the rate limit is per process and per IP address; the audit log is never pruned and skips calls with no valid token; customer endpoints are open; demo accounts share one password |

Every "simplified" cell is a task in one of the member guides.

## Team documents

- [`docs/TEAM_PLAN.md`](docs/TEAM_PLAN.md): who owns what, milestones, and how the four parts fit together
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md): how the code is organised and the rules everyone follows
- [`docs/guide-member-1-inventory.md`](docs/guide-member-1-inventory.md): Inventory and stock integrity
- [`docs/guide-member-2-fulfilment.md`](docs/guide-member-2-fulfilment.md): Order fulfilment (pick, pack, handoff)
- [`docs/guide-member-3-supply.md`](docs/guide-member-3-supply.md): Supply (forecasting, replenishment, inbound, slotting)
- [`docs/guide-member-4-platform.md`](docs/guide-member-4-platform.md): Platform, store network and screens
- [`docs/DEMO_SCRIPT.md`](docs/DEMO_SCRIPT.md): the script for presenting the prototype
- [`docs/EDGE_NODE.md`](docs/EDGE_NODE.md): design note for the in-store edge node (HLD 5), with an outage experiment
- [`CONTRIBUTING.md`](CONTRIBUTING.md): branches, pull requests and the checks to run before pushing
