# Ekwo OS

**Ekwo** is open source accounting, ready to use on **[Ekwo Cloud](https://cloud.ekwo.ai)**: the web application for your invoices, your bank statements, your VAT returns and the electronic invoices your country uses, in your own instance, with an account opened in a minute. **Ekwo OS** is the free and open source core it runs on, under AGPL-3.0: install it on your own Supabase project and own your accounting data, forever.

Built and maintained by **Ekwo**. Ekwo OS is a schema, the rules of each country as data, and the tools — a command line and an MCP server — with which you, your accountant and the AI agent you choose work in the same books, each with their own access. Ekwo reads any supplier invoice, in any language, with the AI model you choose, and every entry is posted on your confirmation. What Ekwo is, and its limits: [DISCLAIMER.md](DISCLAIMER.md).

![An empty Supabase project, npx ekwo-os init, ekwo status, a company, a sale invoice posted and its VAT return prepared, for two countries side by side](docs/demo/install.gif)

*From an empty Supabase project to a prepared VAT return, for two countries
side by side. How it was recorded: [`docs/demo/`](docs/demo/).*

**Try it on your own books.** Already using Claude? [Start with
Claude](docs/start-with-claude.md) goes from a free Supabase project to your
own books taken over, questioned and your next VAT return prepared, in about
twenty minutes. Or open the same books in the web application,
[Ekwo Cloud](https://cloud.ekwo.ai).

---

## Why Ekwo

> The long version — financial autonomy for every business, accounting as a
> commons, a network rather than a vendor — is in [MANIFESTO.md](MANIFESTO.md).

**The data belongs to the business, and the work of keeping the books can be
done by software the business also owns.** So the whole accounting core is
open, the data sits in a Postgres database you control, and the interface is
designed for machines as much as for people. Supabase gives the schema a REST
API for free, and an MCP server sits on top of it, so an AI agent can book a
purchase, match a payment or prepare a VAT return on your own data — as you,
under your own row level security, without the data leaving your account.

What ships today:

- **The core** — schema, posting rules, taxes, reports, financial statements,
  as migrations you apply to a database you control.
- **A country pack for every country listed below**, each a versioned set of
  data with a year of books that proves it.
- **`ekwo`, the command line** — one command installs everything on your own
  Supabase project; the same tool then keeps books from a terminal.
- **The MCP server**, hosted at `https://mcp.ekwo.ai/mcp` or run locally with
  `npx @ekwo-ai/mcp`, so any AI agent can operate the books.
- **Modules** for fixed assets, budgets, corporate income tax and electronic
  invoicing.
- **Format libraries** under MIT — the files administrations, banks and
  e-invoicing networks exchange, written and read.

Who it is for: a company that wants to keep its own books with an AI at the
keyboard; an accounting firm that runs several companies inside one
installation; a developer who needs a real double-entry core with tax rules as
data rather than as code; and anyone who wants to leave a proprietary system
with the books intact.

## What is in this repository

A double-entry accounting core for Postgres. There is no server to run:
Supabase turns the schema into a REST API with an OpenAPI description, and row
level security decides who sees what.

- **Double entry, enforced by the database.** An entry cannot be posted unless
  it balances, and a locked period refuses writes at the trigger — not in a
  form validator.
- **Documents and entries are two layers.** An invoice answers to EN 16931 and
  Peppol; an entry answers to the chart of accounts. Keeping them apart keeps
  both honest.
- **Country rules are data.** A tax points at the ledger accounts it posts to
  and at the boxes of the declaration it feeds. Adding a régime is a row, not a
  release.
- **Every label is data, in every language a country pack publishes.**
  Identifiers stay English; what a person reads comes from the pack, in the
  language of the company or of the reader. See
  [`docs/languages.md`](docs/languages.md).
- **Every country a pack, out of the box.** <!-- generated:countries -->United Arab Emirates (`ae`), Albania (`al`), Հայաստան (`am`), Angola (`ao`), Argentina (`ar`), Austria (`at`), Australia (`au`), Azərbaycan (`az`), Bosna i Hercegovina (`ba`), Bangladesh (`bd`), Belgium (`be`), Burkina Faso (`bf`), България (`bg`), البحرين (`bh`), Bénin (`bj`), Bermuda (`bm`), Brunei Darussalam (`bn`), Bolivia (`bo`), Canada (`ca`), République démocratique du Congo (`cd`), Centrafrique (`cf`), Congo (`cg`), Schweiz (`ch`), Côte d’Ivoire (`ci`), Chile (`cl`), Cameroun (`cm`), 中国 (`cn`), Colombia (`co`), Costa Rica (`cr`), Cyprus (`cy`), Czechia (`cz`), Germany (`de`), Danmark (`dk`), Dominican Republic (`do`), Algérie (`dz`), Ecuador (`ec`), Estonia (`ee`), مصر (`eg`), España (`es`), Ethiopia (`et`), Finland (`fi`), France (`fr`), Gabon (`ga`), United Kingdom (`gb`), საქართველო (`ge`), Guernsey (`gg`), Ghana (`gh`), Guinée (`gn`), Guinée équatoriale (`gq`), Ελλάδα (`gr`), Guatemala (`gt`), Guinée-Bissau (`gw`), Hong Kong (`hk`), Honduras (`hn`), Croatia (`hr`), Magyarország (`hu`), Indonesia (`id`), Ireland (`ie`), Israel (`il`), India (`in`), Ísland (`is`), Italia (`it`), Jersey (`je`), 日本 (`jp`), Kenya (`ke`), Comores (`km`), 대한민국 (`kr`), Kuwait (`kw`), Cayman Islands (`ky`), Қазақстан (`kz`), Sri Lanka (`lk`), Lietuva (`lt`), Luxembourg (`lu`), Latvija (`lv`), Maroc (`ma`), Moldova (`md`), Crna Gora (`me`), Северна Македонија (`mk`), Mali (`ml`), 澳門 (`mo`), Malta (`mt`), Mauritius (`mu`), México (`mx`), Malaysia (`my`), Moçambique (`mz`), Niger (`ne`), Nigeria (`ng`), Nicaragua (`ni`), Nederland (`nl`), Norge (`no`), New Zealand (`nz`), Oman (`om`), Panamá (`pa`), Perú (`pe`), Philippines (`ph`), Pakistan (`pk`), Polska (`pl`), Portugal (`pt`), Paraguay (`py`), Qatar (`qa`), Romania (`ro`), Srbija (`rs`), Rwanda (`rw`), Saudi Arabia (`sa`), Sverige (`se`), Singapore (`sg`), Slovenia (`si`), Slovensko (`sk`), Sénégal (`sn`), El Salvador (`sv`), Tchad (`td`), Togo (`tg`), ประเทศไทย (`th`), Tunisie (`tn`), Türkiye (`tr`), 臺灣 (`tw`), Tanzania (`tz`), Україна (`ua`), Uganda (`ug`), United States (`us`), Uruguay (`uy`), British Virgin Islands (`vg`), Việt Nam (`vn`), Kosova (`xk`), South Africa (`za`), Zambia (`zm`) and Zimbabwe (`zw`)<!-- /generated --> — each with its chart of accounts, its tax codes, its
  declaration boxes and its financial statements, and all of them installed by
  `ekwo init`, so one installation keeps companies in any of these countries.
  The version and review status of each are in
  [`docs/packs.md`](docs/packs.md#the-packs-of-this-checkout).
- **Statutory files.** The French FEC, XBRL annual accounts, Peppol UBL and
  Factur-X invoices, recapitulative statements — written from the ledger by the
  format libraries.
- **Tested on real Postgres.** The test suite runs the migrations, the seeds,
  the accounting scenarios, the installer and the MCP server against Postgres
  compiled to WebAssembly.

## Modules

The core lives in the `public` schema. Beside it, a module is a schema of its
own, with its own migrations, row level security and tests, enabled per
company.

| Module code | Schema | What it does |
|---|---|---|
| [`assets`](modules/fixed-assets/) | `fixed_assets` | Fixed assets, their depreciation schedule and their disposal. Durations and methods are country pack data. |
| [`budgets`](modules/budgets/) | `budgets` | A budget per financial year and the variance against the ledger. |
| [`tax`](modules/corporate-tax/) | `tax` | Corporate income tax estimated from the books: adjustments, losses and rates are country pack data. An estimate until an owner calls it final. |
| [`einvoicing`](modules/einvoicing/) | `einvoicing` | The electronic invoice of a posted sale, in the format the company's country pack declares, checked against the rules of that format, and every sending with its state. |

```sh
npx -y ekwo-os@latest module list                          # what is here, and what the database holds
npx -y ekwo-os@latest module enable assets --company "…"   # turn one on for a company
```

Then add the module's schema to the project's exposed schemas (Supabase
dashboard → Project Settings → API); `ekwo module enable` prints the line.

A module never writes the ledger directly: it hands its lines to the core,
which applies the same balancing, numbering and lock rules as everywhere else.
[`docs/modules.md`](docs/modules.md) is how to write one.

## Install on your own Supabase project

Create a project at [supabase.com](https://supabase.com) — the free plan is
enough to start — and point the installer at it. Node 20 or later is the only
thing you need locally: no Supabase CLI, no Docker, no clone.

```sh
npx -y ekwo-os@latest init
```

It asks for the connection string, the country, the chart of accounts and the
language where the pack offers a choice, your organisation, the first company
and the address of the first administrator. Then it applies the migrations,
loads every country pack, creates that administrator in *your* Supabase Auth
and opens the first financial year. Running it twice creates nothing twice.

Ekwo does not create the project and does not pay for it: your books are on
your account from the first row. The installation guide, with every flag and
the four settings to change on your project before going live, is
[`packages/cli`](packages/cli/README.md).

Asking an AI agent to do it with you? Point it at [`AGENTS.md`](AGENTS.md).
Each country also has its own step-by-step page on
[ekwo.ai/countries](https://ekwo.ai/countries/), and the whole documentation is
served to a model as `https://ekwo.ai/llms.txt`.

### Keeping it running

```sh
npx -y ekwo-os@latest status    # schema version installed against available, instance, companies
npx -y ekwo-os@latest migrate   # apply what a new release adds
npx -y ekwo-os@latest doctor    # every object this release defines, row level security, privileges
```

### By hand, with the Supabase CLI

The installer is a convenience, not a requirement: the migrations are ordinary
SQL, and `supabase db push` writes the same history table `ekwo migrate` does.

```sh
git clone https://github.com/Ekwo-ai/ekwo-os.git && cd ekwo-os
supabase link --project-ref <your-project-ref>
supabase db push                       # applies supabase/migrations in order
```

Then apply the reference seeds, all of them, in this order (the list is
written from `packs/` and is the one `supabase/config.toml` declares):

<details>
<summary>The reference seeds</summary>

<!-- generated:seeds -->
```sh
psql "$DATABASE_URL" -f supabase/seed/00_currencies.sql
psql "$DATABASE_URL" -f supabase/seed/00_territories.sql
psql "$DATABASE_URL" -f supabase/seed/05_framework_generic.sql
psql "$DATABASE_URL" -f supabase/seed/100_pack_uy.sql
psql "$DATABASE_URL" -f supabase/seed/101_pack_ec.sql
psql "$DATABASE_URL" -f supabase/seed/102_pack_bo.sql
psql "$DATABASE_URL" -f supabase/seed/103_pack_py.sql
psql "$DATABASE_URL" -f supabase/seed/104_pack_do.sql
psql "$DATABASE_URL" -f supabase/seed/105_pack_cr.sql
psql "$DATABASE_URL" -f supabase/seed/106_pack_gt.sql
psql "$DATABASE_URL" -f supabase/seed/107_pack_pa.sql
psql "$DATABASE_URL" -f supabase/seed/108_pack_in.sql
psql "$DATABASE_URL" -f supabase/seed/109_pack_cn.sql
psql "$DATABASE_URL" -f supabase/seed/10_pack_be.sql
psql "$DATABASE_URL" -f supabase/seed/110_pack_ge.sql
psql "$DATABASE_URL" -f supabase/seed/111_pack_md.sql
psql "$DATABASE_URL" -f supabase/seed/112_pack_rs.sql
psql "$DATABASE_URL" -f supabase/seed/113_pack_ba.sql
psql "$DATABASE_URL" -f supabase/seed/114_pack_al.sql
psql "$DATABASE_URL" -f supabase/seed/115_pack_mk.sql
psql "$DATABASE_URL" -f supabase/seed/116_pack_me.sql
psql "$DATABASE_URL" -f supabase/seed/117_pack_bh.sql
psql "$DATABASE_URL" -f supabase/seed/118_pack_om.sql
psql "$DATABASE_URL" -f supabase/seed/119_pack_gh.sql
psql "$DATABASE_URL" -f supabase/seed/11_pack_fr.sql
psql "$DATABASE_URL" -f supabase/seed/120_pack_tz.sql
psql "$DATABASE_URL" -f supabase/seed/121_pack_ug.sql
psql "$DATABASE_URL" -f supabase/seed/122_pack_rw.sql
psql "$DATABASE_URL" -f supabase/seed/123_pack_xk.sql
psql "$DATABASE_URL" -f supabase/seed/124_pack_kz.sql
psql "$DATABASE_URL" -f supabase/seed/125_pack_pk.sql
psql "$DATABASE_URL" -f supabase/seed/126_pack_bd.sql
psql "$DATABASE_URL" -f supabase/seed/127_pack_lk.sql
psql "$DATABASE_URL" -f supabase/seed/128_pack_am.sql
psql "$DATABASE_URL" -f supabase/seed/129_pack_az.sql
psql "$DATABASE_URL" -f supabase/seed/12_pack_lu.sql
psql "$DATABASE_URL" -f supabase/seed/130_pack_hn.sql
psql "$DATABASE_URL" -f supabase/seed/131_pack_sv.sql
psql "$DATABASE_URL" -f supabase/seed/132_pack_ni.sql
psql "$DATABASE_URL" -f supabase/seed/133_pack_et.sql
psql "$DATABASE_URL" -f supabase/seed/134_pack_mu.sql
psql "$DATABASE_URL" -f supabase/seed/135_pack_mz.sql
psql "$DATABASE_URL" -f supabase/seed/136_pack_ao.sql
psql "$DATABASE_URL" -f supabase/seed/137_pack_zm.sql
psql "$DATABASE_URL" -f supabase/seed/138_pack_bm.sql
psql "$DATABASE_URL" -f supabase/seed/139_pack_ky.sql
psql "$DATABASE_URL" -f supabase/seed/13_pack_ee.sql
psql "$DATABASE_URL" -f supabase/seed/140_pack_vg.sql
psql "$DATABASE_URL" -f supabase/seed/141_pack_gg.sql
psql "$DATABASE_URL" -f supabase/seed/142_pack_qa.sql
psql "$DATABASE_URL" -f supabase/seed/143_pack_kw.sql
psql "$DATABASE_URL" -f supabase/seed/144_pack_bn.sql
psql "$DATABASE_URL" -f supabase/seed/145_pack_mo.sql
psql "$DATABASE_URL" -f supabase/seed/146_pack_je.sql
psql "$DATABASE_URL" -f supabase/seed/147_pack_zw.sql
psql "$DATABASE_URL" -f supabase/seed/14_pack_gb.sql
psql "$DATABASE_URL" -f supabase/seed/15_pack_us.sql
psql "$DATABASE_URL" -f supabase/seed/16_pack_ie.sql
psql "$DATABASE_URL" -f supabase/seed/17_pack_nl.sql
psql "$DATABASE_URL" -f supabase/seed/18_pack_de.sql
psql "$DATABASE_URL" -f supabase/seed/19_pack_es.sql
psql "$DATABASE_URL" -f supabase/seed/20_pack_sn.sql
psql "$DATABASE_URL" -f supabase/seed/21_pack_ci.sql
psql "$DATABASE_URL" -f supabase/seed/22_pack_bj.sql
psql "$DATABASE_URL" -f supabase/seed/23_pack_bf.sql
psql "$DATABASE_URL" -f supabase/seed/24_pack_cm.sql
psql "$DATABASE_URL" -f supabase/seed/25_pack_cf.sql
psql "$DATABASE_URL" -f supabase/seed/26_pack_km.sql
psql "$DATABASE_URL" -f supabase/seed/27_pack_cg.sql
psql "$DATABASE_URL" -f supabase/seed/28_pack_ga.sql
psql "$DATABASE_URL" -f supabase/seed/29_pack_gn.sql
psql "$DATABASE_URL" -f supabase/seed/30_pack_gw.sql
psql "$DATABASE_URL" -f supabase/seed/31_pack_gq.sql
psql "$DATABASE_URL" -f supabase/seed/32_pack_ml.sql
psql "$DATABASE_URL" -f supabase/seed/33_pack_ne.sql
psql "$DATABASE_URL" -f supabase/seed/34_pack_cd.sql
psql "$DATABASE_URL" -f supabase/seed/35_pack_td.sql
psql "$DATABASE_URL" -f supabase/seed/36_pack_tg.sql
psql "$DATABASE_URL" -f supabase/seed/37_pack_it.sql
psql "$DATABASE_URL" -f supabase/seed/38_pack_id.sql
psql "$DATABASE_URL" -f supabase/seed/39_pack_my.sql
psql "$DATABASE_URL" -f supabase/seed/40_pack_au.sql
psql "$DATABASE_URL" -f supabase/seed/41_pack_nz.sql
psql "$DATABASE_URL" -f supabase/seed/42_pack_mx.sql
psql "$DATABASE_URL" -f supabase/seed/43_pack_pt.sql
psql "$DATABASE_URL" -f supabase/seed/44_pack_ph.sql
psql "$DATABASE_URL" -f supabase/seed/45_pack_ar.sql
psql "$DATABASE_URL" -f supabase/seed/46_pack_cl.sql
psql "$DATABASE_URL" -f supabase/seed/47_pack_co.sql
psql "$DATABASE_URL" -f supabase/seed/48_pack_pe.sql
psql "$DATABASE_URL" -f supabase/seed/49_pack_ng.sql
psql "$DATABASE_URL" -f supabase/seed/50_pack_sg.sql
psql "$DATABASE_URL" -f supabase/seed/51_pack_jp.sql
psql "$DATABASE_URL" -f supabase/seed/52_pack_hk.sql
psql "$DATABASE_URL" -f supabase/seed/53_pack_tw.sql
psql "$DATABASE_URL" -f supabase/seed/54_pack_kr.sql
psql "$DATABASE_URL" -f supabase/seed/55_pack_vn.sql
psql "$DATABASE_URL" -f supabase/seed/56_pack_th.sql
psql "$DATABASE_URL" -f supabase/seed/57_pack_ua.sql
psql "$DATABASE_URL" -f supabase/seed/58_pack_ca.sql
psql "$DATABASE_URL" -f supabase/seed/60_pack_ae.sql
psql "$DATABASE_URL" -f supabase/seed/61_pack_se.sql
psql "$DATABASE_URL" -f supabase/seed/62_pack_ch.sql
psql "$DATABASE_URL" -f supabase/seed/63_pack_at.sql
psql "$DATABASE_URL" -f supabase/seed/64_pack_pl.sql
psql "$DATABASE_URL" -f supabase/seed/65_pack_dk.sql
psql "$DATABASE_URL" -f supabase/seed/66_pack_no.sql
psql "$DATABASE_URL" -f supabase/seed/67_pack_fi.sql
psql "$DATABASE_URL" -f supabase/seed/68_pack_cz.sql
psql "$DATABASE_URL" -f supabase/seed/69_pack_sk.sql
psql "$DATABASE_URL" -f supabase/seed/70_pack_hu.sql
psql "$DATABASE_URL" -f supabase/seed/71_pack_sa.sql
psql "$DATABASE_URL" -f supabase/seed/72_pack_ro.sql
psql "$DATABASE_URL" -f supabase/seed/73_pack_bg.sql
psql "$DATABASE_URL" -f supabase/seed/74_pack_hr.sql
psql "$DATABASE_URL" -f supabase/seed/75_pack_si.sql
psql "$DATABASE_URL" -f supabase/seed/76_pack_gr.sql
psql "$DATABASE_URL" -f supabase/seed/77_pack_lt.sql
psql "$DATABASE_URL" -f supabase/seed/78_pack_lv.sql
psql "$DATABASE_URL" -f supabase/seed/79_pack_cy.sql
psql "$DATABASE_URL" -f supabase/seed/80_pack_mt.sql
psql "$DATABASE_URL" -f supabase/seed/81_pack_is.sql
psql "$DATABASE_URL" -f supabase/seed/82_pack_tr.sql
psql "$DATABASE_URL" -f supabase/seed/83_pack_eg.sql
psql "$DATABASE_URL" -f supabase/seed/84_pack_ma.sql
psql "$DATABASE_URL" -f supabase/seed/85_pack_tn.sql
psql "$DATABASE_URL" -f supabase/seed/86_pack_dz.sql
psql "$DATABASE_URL" -f supabase/seed/87_pack_il.sql
psql "$DATABASE_URL" -f supabase/seed/88_pack_za.sql
psql "$DATABASE_URL" -f supabase/seed/89_pack_ke.sql
```
<!-- /generated -->

</details>

Skip `supabase/seed/90_demo_company.sql` unless you want sample data. Then, as
a signed-in user: `init_instance()`, `claim_instance_admin()`, a `companies`
row with yourself as `owner` in `company_members`,
`install_country_template()` and a first `fiscal_years` row — the same steps
the installer runs.

## The schema in twenty lines

```
instance                                 one row: who installed it, where, which edition
instance_admins                          instance administrators
capabilities ── role_capabilities         what may be done, and what each preset holds
companies ─┬─ company_members            who may read or write, and what they may do
           ├─ company_invitations        an address invited, a token hashed
           ├─ api_keys                   machine access, scoped to capabilities
           ├─ fiscal_years               periods, open or closed
           ├─ accounts                   chart of accounts, 18 account types
           ├─ journals ── journal_sequences
           ├─ contacts                   customers, suppliers, employees
           ├─ taxes ── tax_postings      ledger account + declaration box, per tax
           ├─ entries ── entry_lines     the ledger; lines carry the truth
           ├─ products                   what a line is filled in from, never stock
           ├─ documents ── document_lines invoices, credit notes, quotes
           ├─ payments                   money in and out
           ├─ reconciliations            bilateral matching, by amount
           ├─ bank_accounts ── bank_statements ── bank_transactions
           ├─ analytic_axes ── analytic_values ── entry_line_analytics
           └─ attachments                files, polymorphic
user_preferences                         one row per person, null everywhere
```

`post_document()` turns a document into an entry. `trial_balance`,
`general_ledger`, `aged_balance`, `vat_return`, `ec_sales_list`,
`financial_statement` and `fec_lines` read the ledger back.
`opening_balance()` takes over the balances of whatever kept the books before,
and `close_fiscal_year()` closes a year the way the country pack says.
[`docs/schema.md`](docs/schema.md) describes every table and column, and
[`docs/mapping.md`](docs/mapping.md) lines them up against EN 16931.

## Who may do what

One installation belongs to one customer, so there is no `tenant_id`.
`instance_admins` says who may create companies and invite people, and
`company_members` gives each person a preset on each company:

| Preset | Holds |
|---|---|
| `viewer` | every `.read` — the books, the documents, the chart, the catalogue |
| `client` | what a viewer holds, plus handing a file over to whoever keeps the books |
| `accountant` | that, plus writing and posting, matching, the settings and the year-end close |
| `owner` | that, plus the company itself and its members |

What the policies actually test is a **capability** — `documents.post`,
`payments.write`, `year_end.close` and the rest of
`select * from capabilities`. A member can be granted or refused one
capability without inventing a role. A firm keeps the books of many companies
in one installation, and the person who runs one of them is a `client` of that
one and sees no other ([`docs/firms.md`](docs/firms.md)). People are invited
with `invite_member()`; your users live in your own Supabase Auth, and Ekwo
never holds an account.

**Keys for machines.** A script — a nightly import, a till, a bank feed — gets
a key from `create_api_key()`: scoped to one company and a list of
capabilities, never more than the person who issued it holds, stored as a
hash, and withdrawn with `revoke_api_key()`. It reaches the REST API through
the `X-Ekwo-Api-Key` header ([`docs/machine-access.md`](docs/machine-access.md)).
Never hand a script the `service_role` key.

## The TypeScript packages

- [`ekwo-os`](packages/cli/) — the `ekwo` command line: installing, operating,
  and keeping books as a signed-in person. Every command takes `--json`.
- [`@ekwo-ai/mcp`](packages/mcp/) — the MCP server. It acts **as the user**,
  never as `service_role`, and every write goes through the schema's own
  functions. Hosted at `https://mcp.ekwo.ai/mcp` for clients that add remote
  servers (sign-in in the browser, nothing stored in a configuration file), or
  `npx -y @ekwo-ai/mcp@latest` over stdio.
- [`@ekwo-ai/core`](packages/core/) — the types of the schema, a typed client,
  and the book-keeping functions the command line and the MCP server share.

```ts
import { EkwoClient } from '@ekwo-ai/core';
import { createClient } from '@supabase/supabase-js';

const ekwo = new EkwoClient(createClient(url, key));

await ekwo.postDocument(documentId);
const balance = await ekwo.trialBalance({ companyId, from: '2026-01-01', to: '2026-12-31' });
const boxes   = await ekwo.vatReturn({ companyId, from: '2026-07-01', to: '2026-09-30' });
```

## Format libraries

[`packages/formats/`](packages/formats/) holds one MIT package per file
format, organised by format and never by country. None imports the core: the
core produces rows, and a library turns rows into a file, or a file into rows.

- **Written from the ledger:** the French FEC ([`fec`](packages/formats/fec/)),
  XBRL annual accounts ([`xbrl-cbso`](packages/formats/xbrl-cbso/)), a
  periodic VAT return ([`vat-consignment`](packages/formats/vat-consignment/)),
  and four recapitulative statements of European Union supplies
  ([`intra-consignment`](packages/formats/intra-consignment/),
  [`des`](packages/formats/des/), [`ecdf`](packages/formats/ecdf/),
  [`vd`](packages/formats/vd/)).
- **Electronic invoices, written and read:**
  [`peppol-ubl`](packages/formats/peppol-ubl/) (Peppol BIS Billing 3.0) and
  [`factur-x`](packages/formats/factur-x/) (Factur-X and ZUGFeRD). Both also
  read a received invoice into the same shape, ready to become a purchase draft.
- **Bank statements, read:** [`camt053`](packages/formats/camt053/),
  [`coda`](packages/formats/coda/), [`cfonb120`](packages/formats/cfonb120/).
- **Books kept elsewhere, read:** [`trial-balance`](packages/formats/trial-balance/),
  [`journal-items`](packages/formats/journal-items/),
  [`journal-report`](packages/formats/journal-report/),
  [`transaction-journal`](packages/formats/transaction-journal/),
  [`xaf`](packages/formats/xaf/) and the FEC — what `ekwo import` takes over
  ([`docs/compatibility.md`](docs/compatibility.md)).

## Community and cloud

The line is operational, not functional. Everything a bookkeeper can do alone
is here and always will be.

| Ekwo OS, on your Supabase | Managed edition, on [ekwo.ai](https://ekwo.ai) |
|---|---|
| The whole schema, migrations, row level security | Provisioning and running the instance |
| Journals, entries, matching, charts of accounts | Backups, restores, version upgrades |
| Invoicing, credit notes, taxes, reports, statutory files | AI agents you set up, acting on your instructions |
| Importing bank files and books kept elsewhere | Bank connections under contract |
| Writing and checking electronic invoices | A Peppol access point to send and receive them |
| Everything above, forever, for nothing | Transmission to administrations, on the business's instruction |

The test: does it keep working on its own, with us or without us? If yes, it
belongs here, under AGPL, and no licence key gates it. If no, it is a service,
because something has to be kept alive for it — a contract, a certificate, a
credential, a machine. [`docs/cloud-services.md`](docs/cloud-services.md) lists
them, and says what will never be sold.

## Security

Row level security is the whole model: every table carries it, every policy
asks one question — `has_capability()` — and the reports run as the caller. An
anonymous request sees nothing. The MCP server and the command line refuse a
`service_role` key for keeping books, and the CI fails if a table ever arrives
without a policy.

Three things the schema cannot do for you, printed by `ekwo init` at the end
of every installation: **turn off public sign-ups** on your Supabase project,
**keep two administrators**, and **keep the `service_role` key off every
machine that does not need it**. See
[`packages/cli`](packages/cli/README.md#before-you-go-live-four-things-on-your-project)
and [SECURITY.md](SECURITY.md).

## What this is not

Ekwo is open source data infrastructure. It is not an accounting firm and
gives no accounting, tax, financial, legal or investment advice. Your books,
returns and filings are yours; a country pack is a reading of the rules at a
date, and a review is a professional's good-faith reading, not a guarantee.
Where accounting and tax are regulated professions, consult a professional
authorised in your country. [DISCLAIMER.md](DISCLAIMER.md) says this in full,
and is published at [ekwo.ai/disclaimer](https://ekwo.ai/disclaimer/). Read it
before you file anything.

## Finding your way

Most folders carry a short README saying what lives there:
[`supabase/`](supabase/), [`modules/`](modules/), [`packages/cli/`](packages/cli/),
[`packages/mcp/`](packages/mcp/), [`packages/core/`](packages/core/),
[`tests/`](tests/) and [`docs/`](docs/), which holds the long-form reference.
Each country pack under [`packs/`](packs/) has its own README. Where the project is heading:
[`docs/road-to-1.0.md`](docs/road-to-1.0.md). A few names are renamed before
1.0, each with an alias for at least one minor release:
[the names that change before 1.0](docs/releasing.md#names-that-change-before-10).

## Development

```sh
npm install
npm run typecheck
npm test          # applies every migration and seed to an in-memory Postgres
npm run build
```

Tests use [PGlite](https://pglite.dev): no Docker and no local Postgres. A
development checkout needs Node 22 or later.

## Contributing

Issues and pull requests are welcome. Contributions require the
[Contributor Licence Agreement](CLA.md); see [CONTRIBUTING.md](CONTRIBUTING.md)
for how to work on the schema without breaking a database somebody already
installed.

## Licence

[AGPL-3.0-only](LICENSE) © Karuna Co OÜ (Estonian registry code 14510673),
trading as Ekwo. Installing Ekwo OS and running it for your own organisation —
modified or not — puts no obligation on you. The share-alike clause applies
only if you modify it *and* offer that modified version to people outside your
organisation over a network.

**The format libraries under [`packages/formats/`](packages/formats/) are
MIT**, each with its own `LICENSE`. A file format should be readable and
writable by anyone.

"Ekwo" and the Ekwo logo are trademarks and are not covered by the licence.
Fork the code; do not call the fork Ekwo.
