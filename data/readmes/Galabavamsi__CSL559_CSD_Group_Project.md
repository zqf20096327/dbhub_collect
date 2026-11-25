# JustInTimeFarm2Home

Produce from farms to homes through small local hubs. A farmer lists a lot from a phone. The nearest hub with room
weighs it, grades it and packs it into units. A customer nearby buys from that hub's shelves, seeing which farm
each pack came from and when it was picked. A delivery agent carries several neighbours' orders in one trip and
hands each over against a code the customer reads out.

It runs for two cities: **Bhilai** (tier 2, four hubs, one beside IIT Bhilai) and **Bangalore** (tier 1, two
hubs). It is one FastAPI application on PostgreSQL with PostGIS, plain web pages for the hub's staff, and one phone
app for customers, farmers and delivery agents. A copy called staging runs on AWS in Mumbai.

**New to the project? Read [`docs/HANDOVER.md`](docs/HANDOVER.md) first.** It covers where things stand, where
everything is, how to run, test, deploy and build, who holds what, and what is known to be wrong.

## See it

Staging is a demo: orders are not real and no money moves.

| What | Where | Sign-in |
| --- | --- | --- |
| **Phone app** for Android (customer, farmer, delivery agent) | [Release `app-staging-2026-11-24`](https://github.com/Galabavamsi/CSL559_CSD_Group_Project/releases/tag/app-staging-2026-11-24) | An email address; a six-digit code is sent to it |
| **Hub desk**: customer, picker and store side by side, with live events | https://staging.farm2home.galabavamsi.com/ | Staff password |
| **Ops dashboard**: what needs action, then each figure beside its target | https://staging.farm2home.galabavamsi.com/ops.html | Staff password |
| **Intake**: weigh, grade and put away a farm lot | https://staging.farm2home.galabavamsi.com/intake.html?store=6 | Staff password |
| **Picker**: claim an order, scan each unit, pack | https://staging.farm2home.galabavamsi.com/picker.html?store=6 | Staff password |
| **Network map**: zones, demand, requests for delivery, where to open a hub | https://staging.farm2home.galabavamsi.com/network.html?city=bhilai | Staff password |
| **API**: every call, with a form to try it | https://staging.farm2home.galabavamsi.com/docs | None to read |
| **Report**: system design, the screens in pictures, measurements | [`docs/handbook/JustInTimeFarm2Home-handbook.pdf`](docs/handbook/JustInTimeFarm2Home-handbook.pdf) | |

- **Hubs:** `store=6` is BH-04 IIT Bhilai. The others are 3 BH-01 Civic Centre, 4 BH-02 Nehru Nagar and 5 BH-03 Durg
  in Bhilai, and 1 DS-01 Central and 2 DS-02 North in Bangalore. On the hub desk and the dashboard, choose the hub
  from the menu at the top.
- **Staff password:** each hub page asks for it once in a sign-in box, and the browser remembers it. It is kept in
  AWS Secrets Manager under `farm2home/staging/staff-password`, never in this repository. Any number of people can
  be signed in at once, each on their own device.
- **Networks:** some block the staging address (a campus Wi-Fi did). The app and pages then cannot connect; mobile
  data works.
- **To show the whole flow from phones**, follow [`docs/DEMO_ON_A_PHONE.md`](docs/DEMO_ON_A_PHONE.md).

## What it does

| Who | What they can do |
| --- | --- |
| **Farmer** (phone) | Register a farm where they stand. List a lot: the nearest hub with room is chosen and a morning drop slot given. See the hub's grade and the kilograms accepted and rejected |
| **Hub receiver** (web) | See the lots on their way, with each farm's record. Weigh and grade a lot; it is packed into units. Put each portion in the bin the screen names; it is on sale from that moment |
| **Customer** (phone) | Choose where to deliver; the hub whose zone covers the address serves it, and an address nobody serves can ask for delivery. See only what that hub can deliver now, with each pack's grade, harvest date, use-by date and farm. Buy a batch in its last day 30% cheaper. Hold the cart for ten minutes and pay the hub's own bill. Follow the order to the door; cancel until it is packed |
| **Hub picker** (web) | Claim the next order, or three in one walk when it is busy. Lines come in walking order, oldest batch first, and every unit is checked by barcode. An empty shelf moves the line to another bin or drops it. Packing commits the sale |
| **Delivery agent** (phone) | Choose a hub and go on duty. Be given a trip of packed orders, with the stops in the shortest round. Check each bag out by its crate slot. At each door, type the customer's four-digit code, or report why the order could not be handed over |
| **Hub and city staff** (web) | Watch stock, orders and events live. Restock packaged goods from a warehouse, forecast, put fast sellers near the desk, count stock. See on a map the demand the hubs turned away and the requests for delivery, with suggested sites, and open a hub there in one step |

**800 automated tests** cover these. Among them: twenty buyers racing for the last unit, two customers shown the
same last cheap packs, and an order going from paid to delivered with nobody at the hub.

**Not built:** a map in the app and the agent's position, a time of arrival, real payment, what the hub does with a
bag that comes back, and hubs asking farms for what they expect to sell. [`docs/HANDOVER.md`](docs/HANDOVER.md)
section 14 puts them in order.

## How it is put together

```
app/
  main.py            builds the app and plugs in every module
  config.py          every setting, read from the environment
  models.py          every table                    migrations/ holds every change to them
  events.py          an event bus with an outbox table; it stands in for Kafka
  clock.py           today's date where the hubs are (India), not where the server is
  background.py      the timed jobs: expired holds, expiry, stalled orders, trips, restocking
  demo_supply.py     staging only: demo farms deliver when a hub runs low
  demo_hub.py        staging only: an order no picker starts is picked and packed
  modules/           one package per service; each has service.py (the rules) and router.py (HTTP)
    accounts/        sign-in by emailed code, sessions, profiles
    serviceability/  cities, hubs, delivery zones as H3 cells, opening a hub, requests for delivery
    farms/           farms, listings, choosing a hub, weighing and grading
    inbound/         goods receipts and putaway       slotting/   which bin an item lives in
    inventory/       the only code that changes stock: holds, sales, counts, expiry, the ledger
    catalogue/       what a customer is told about a pack, and the rescue price
    orders/          a customer's order, its bill, its timeline
    fulfilment/      a pick job per paid order        pickpack/   claim, scan, empty shelf, pack
    delivery/        agents on duty, trips, bags checked out, the door code
    replenishment/   forecasting/   assortment/   network_planning/   dashboard/
web/                 the hub's pages (plain HTML, CSS and JavaScript; no build step)
mobile/              the phone app (Expo, React Native): one app, three roles
infra/               AWS: CloudFormation templates; scripts that test, deploy and smoke-test
scripts/             the end-to-end recorder, the app build, load tests, experiments, demo data
tests/               800 tests (pytest, against PostgreSQL with PostGIS)
docs/                handover, design, architecture, journal, the report
```

Three rules the code keeps everywhere:

- **One module changes stock.** Every other module asks `inventory`. Every change is a row in a ledger, and an
  audit compares the totals, the bins and the ledger at any time.
- **A state change is one guarded update.** Claiming an order, taking a trip, confirming a hold: each is an
  `UPDATE ... WHERE state = <what it was>`, so two people doing it at once cannot both succeed.
- **What must happen together happens in one transaction.** An order is written inside the payment that creates
  it; a trip is formed inside the packing that makes it due; an event is written with the change it describes.

On AWS: the API in one container on ECS Fargate, behind a load balancer with a web firewall; PostgreSQL 16 on RDS
with a standby in a second zone; tests and images built by CodeBuild; five CloudFormation stacks.
[`infra/README.md`](infra/README.md) has the details.

## Run it yourself

You need Python 3.10 or newer (the image uses 3.12) and PostgreSQL 16 with PostGIS. With Docker, this starts a
database on `localhost:5432` (user, password and database are all `darkstore`, the app's default) and the app:

```bash
docker compose up -d postgres
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
DEMO_PRODUCE=on DEMO_HUBS=on DEMO_SUPPLY=on python -m uvicorn app.main:app --reload
```

The tables and the demo data are made on first start. The three settings add the produce, Bhilai's hubs, and the
demo farms that keep every hub stocked with produce, Bangalore's included. Without them you get the original
prototype's two Bangalore stores and their groceries. For
a database elsewhere, set `DARKSTORE_DB=postgresql://user:password@host:5432/database` first. Or run everything in
Docker with `docker compose up --build`.

Then open http://localhost:8000 (the hub desk), `/ops.html`, `/picker.html`, `/intake.html`, `/network.html` and
`/docs`. Locally the staff password is `demo`, and sign-in codes for the phone app are written to the server's log.

**The phone app**, in `mobile/` ([`mobile/README.md`](mobile/README.md) has more):

```bash
npm install
npx expo start                                                  # built-in demo data: any email, code 123456
EXPO_PUBLIC_API_URL=http://<this machine>:8000 npx expo start   # against your own API
```

For a phone to reach your own API, start the API with `--host 0.0.0.0` (it listens on this machine only otherwise),
and only on a network you trust: locally every staff account has the password `demo`.

**Tests** need a PostGIS database they may wipe: `DARKSTORE_TEST_DB=<url> python -m pytest -q`. The usual way is on
AWS, which needs nothing installed: `infra\test.ps1 -Ref <branch>` runs them for any commit and marks it on GitHub.

**Monitoring locally:** `docker compose --profile monitoring up --build` adds Prometheus and Grafana; their
configuration is in `monitoring/`.

## Logging in

Two kinds of login, never mixed:

- **People using the phone app** (customers, farmers, delivery agents) sign in with a six-digit code sent to their
  email address. There are no passwords. A session lasts 60 minutes and renews itself for up to 30 days. A delivery
  agent's account is made by an admin, unless `AGENT_SELF_SIGNUP` is on, as it is on staging.
- **Hub and city staff** log in with a username and a password and get a token that lasts 30 minutes. The accounts
  are `picker<n>`, `packer<n>`, `receiver<n>` and `manager<n>` for hub number `n`, and the city-wide `ops` and
  `admin`. Staff may act only on their own hub; `ops` can read every hub; `/v1/admin/*` needs `admin`. Every call a
  logged-in staff member makes, refused or not, is kept in an audit log (`GET /v1/audit`).

The reads a shopper needs before signing in (whether an address is served, the list of hubs, a hub's shop and
availability) need no login. Logins, address lookups, availability and holds are rate-limited: about 20 calls a
second per address, then `429` (`app/rate_limit.py`). Outside local development set `JWT_SECRET` and
`DEMO_PASSWORD`; the built-in defaults are public.

```bash
TOKEN=$(curl -s localhost:8000/v1/auth/login -H "Content-Type: application/json" \
  -d '{"username":"manager1","password":"demo"}' | python -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
curl localhost:8000/v1/stores/1/dashboard -H "Authorization: Bearer $TOKEN"
```

## Making a change

[`CONTRIBUTING.md`](CONTRIBUTING.md) has the whole routine. In short: a branch and a pull request for every change;
`infra\test.ps1 -Ref <branch>` must pass before merging; a new migration for every table change, never an edited
one; a decision goes in [`docs/DESIGN.md`](docs/DESIGN.md) with its reason; a journal entry in
[`docs/journal/`](docs/journal/README.md) says what was built and what went wrong. No secrets or account ids in any
file: the repository is public.

To deploy, `infra\deploy.ps1 -Env staging -Ref main` (about fifteen minutes; [`infra/README.md`](infra/README.md)).

## Documents

| Document | Read it to |
| --- | --- |
| [`docs/HANDOVER.md`](docs/HANDOVER.md) | Take the project on: status, where things are, how to, access, known faults, what next |
| [`docs/DESIGN.md`](docs/DESIGN.md) | Know why each rule is the way it is, what else was considered and what it costs |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Find your way around the code and the rules it keeps |
| [`docs/journal/`](docs/journal/README.md) | See what was built each day, and what went wrong |
| [`docs/handbook/`](docs/handbook/README.md) | Read the report |
| [`docs/DEMO_ON_A_PHONE.md`](docs/DEMO_ON_A_PHONE.md), [`docs/DEMO_SCRIPT.md`](docs/DEMO_SCRIPT.md) | Show it: from phones; on the hub desk |
| [`infra/README.md`](infra/README.md), [`mobile/README.md`](mobile/README.md) | Run it on AWS; work on the phone app |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Make a change |
| [`docs/history/`](docs/history/README.md) | See the university group project this began as |

## Where it came from

This began as a university group project (CSL559): a dark-store prototype of the micro-warehousing part of a
quick-commerce app, built by four students against the group's high-level design. Its stock, picking, restocking,
forecasting and slotting code is still the base of the hub. The prototype as the group left it is the git tag
`darkstore-final`; their plan, guides and report are in [`docs/history/`](docs/history/README.md). From 23 November
2026 it was rebuilt into JustInTimeFarm2Home for a live demo in Bhilai on 3 and 4 December 2026.
