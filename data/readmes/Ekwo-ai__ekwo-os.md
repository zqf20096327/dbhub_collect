# Ekwo OS

**Ekwo OS** is free and open source data infrastructure for accounting, finance and tax, under AGPL-3.0: a schema, the rules of each country as data, and tools, for businesses and their accountants. Install it on your own Supabase project and own your accounting data, forever. It is software — not an accounting firm, and not accounting, tax or financial advice ([DISCLAIMER.md](DISCLAIMER.md)).
Built and maintained by **Ekwo**. A fully managed edition — your own instance, operated for you, with the AI agents you configure acting on your instructions — is available at **[ekwo.ai](https://ekwo.ai)**.

![An empty Supabase project, npx ekwo-os init, ekwo status, a company, a sale invoice posted and its VAT return prepared, for the United Kingdom and Estonia side by side](docs/demo/install.gif)

*An empty Supabase project to a prepared VAT return, for two countries side by
side, with the published `ekwo-os` 0.5.0. How it was recorded, and a longer
cut: [`docs/demo/`](docs/demo/).*

**Try it on your own books.** Already using Claude? [Start with
Claude](docs/start-with-claude.md) goes from a free Supabase project to your
own books taken over, questioned and your next VAT return prepared — Claude
Desktop or Claude Code, about twenty minutes — or open the same books in
the web application, [Ekwo Cloud](https://cloud.ekwo.ai).

---

## Why Ekwo

> The long version — financial autonomy for every business, accounting as a
> commons, a network rather than a vendor — is in [MANIFESTO.md](MANIFESTO.md).

Accounting software has settled into two shapes, and both take something
from you. The SaaS keeps your books on its servers, behind its API and its
price list, and leaving means exporting a PDF. The open-source ERP gives you
the code but keeps the parts that save time — bank feeds, automatic matching,
invoice recognition — for the paid edition and a network of integrators.

Ekwo is built on a different premise: **the data belongs to the business,
and the work of keeping the books can be done by software that the business
also owns.** So the whole accounting core is open, the data sits in a Postgres
database that you control, and the interface is designed for machines as
much as for people. A REST API and an OpenAPI description come free with
Supabase, and an MCP server sits on top of them, so an AI agent can book a
purchase, match a payment, prepare a VAT return or produce a FEC on your own
data — as you, under your own row level security, without the data ever
leaving your account.

What we are building, in order:

1. **This repository — the core.** Schema, posting rules, VAT, reports, the
   FEC, and the country packs. Done, tested, installable today.
2. **`npx -y ekwo-os@latest init`** — point it at your own Supabase project
   and it applies the schema, seeds the country rules, creates the first
   administrator and the first company, in one command. Done; see
   [`packages/cli`](packages/cli/).
3. **The MCP server** — so any AI agent can operate the books: read the
   ledger, raise an invoice, post it, match a payment, pull the VAT return or
   the FEC. Two ways to reach it, and they are the same server:
   **`https://mcp.ekwo.ai/mcp`**, hosted, which a client that speaks
   Streamable HTTP and OAuth adds as a URL, and `npx @ekwo-ai/mcp` over stdio,
   for a client that launches its servers itself. Done; see
   [`packages/mcp`](packages/mcp/). The web application is
   [Ekwo Cloud](https://cloud.ekwo.ai), and it opens an instance you run
   yourself as well as one we host.
4. **Any country as a versioned pack of data**, with one golden test per
   country. Every folder of [`packs/`](packs/) ships today — the list is under
   [What is in this repository](#what-is-in-this-repository) — and more arrive
   every week. The plan is in [`docs/international.md`](docs/international.md).
5. **Format libraries** as independent MIT packages, in
   [`packages/formats/`](packages/formats/), organised by format and never by
   country: the [French FEC](packages/formats/fec/),
   [Factur-X](packages/formats/factur-x/),
   [XBRL for the NBB](packages/formats/xbrl-cbso/), the
   [Belgian VAT return](packages/formats/vat-consignment/),
   [Peppol BIS Billing 3.0](packages/formats/peppol-ubl/), four
   recapitulative statements and three readers of bank statements —
   [camt.053](packages/formats/camt053/), [CODA](packages/formats/coda/) and
   [CFONB 120](packages/formats/cfonb120/) — exist today; MT940 waits for
   somebody who needs it.

Who it is for: a company that wants to keep its own books with an AI at the
keyboard; an accounting firm that runs several companies inside one
installation; a developer who needs a real double-entry core with VAT rules
as data rather than as code; and anyone who wants to leave a proprietary
system with the books intact.

What we sell, so that this stays free: a managed edition at
[ekwo.ai](https://ekwo.ai) where the same schema runs on your own Supabase
project, and Ekwo operates the application, the AI agents you set up, the bank
connections, the Peppol access point and the channels to the administrations.
It is infrastructure, not a service that keeps the books: the books and the filings stay
the business's and its accountant's. The Community edition
stands on its own, with us or without us, for as long as its owner wants it to.
That is the test every feature has to pass before it lands here.

## What is in this repository

A double-entry accounting core for Postgres. It is the schema, the posting
rules and the reports, as migrations you apply to a database you control.
There is no server to run: Supabase turns the schema into a REST API with an
OpenAPI description, and row level security decides who sees what.

- **Double entry, enforced by the database.** Amounts are positive, a
  reversal flips the side, an entry cannot be posted unless it balances, and
  a locked period refuses writes at the trigger — not in a form validator.
- **Documents and entries are two layers, joined by a foreign key.** An
  invoice answers to EN 16931 and Peppol; an entry answers to the chart of
  accounts and to the FEC. Keeping them apart keeps both honest.
- **Country rules are data.** A tax points at the ledger accounts it posts to
  and at the boxes of the VAT return it feeds. Adding a régime is a row, not
  a release.
- **Every label is data, in every language the country pack publishes.**
  Identifiers and error codes are English and never move; what a person reads
  is a row. Belgium ships its chart of accounts, its journals, its VAT codes,
  its declaration boxes and its annual accounts in French, Dutch, German and
  English, and a company keeping its books in Dutch reads Dutch throughout.
  [`docs/languages.md`](docs/languages.md) is the mechanism.
- **Every country a pack, out of the box.** <!-- generated:countries -->United Arab Emirates (`ae`), Albania (`al`), Argentina (`ar`), Austria (`at`), Australia (`au`), Bosna i Hercegovina (`ba`), Belgium (`be`), Burkina Faso (`bf`), България (`bg`), البحرين (`bh`), Bénin (`bj`), Bolivia (`bo`), Canada (`ca`), République démocratique du Congo (`cd`), Centrafrique (`cf`), Congo (`cg`), Schweiz (`ch`), Côte d’Ivoire (`ci`), Chile (`cl`), Cameroun (`cm`), 中国 (`cn`), Colombia (`co`), Costa Rica (`cr`), Cyprus (`cy`), Czechia (`cz`), Germany (`de`), Danmark (`dk`), Dominican Republic (`do`), Algérie (`dz`), Ecuador (`ec`), Estonia (`ee`), مصر (`eg`), España (`es`), Finland (`fi`), France (`fr`), Gabon (`ga`), United Kingdom (`gb`), საქართველო (`ge`), Ghana (`gh`), Guinée (`gn`), Guinée équatoriale (`gq`), Ελλάδα (`gr`), Guatemala (`gt`), Guinée-Bissau (`gw`), Hong Kong (`hk`), Croatia (`hr`), Magyarország (`hu`), Indonesia (`id`), Ireland (`ie`), Israel (`il`), India (`in`), Ísland (`is`), Italia (`it`), 日本 (`jp`), Kenya (`ke`), Comores (`km`), 대한민국 (`kr`), Қазақстан (`kz`), Lietuva (`lt`), Luxembourg (`lu`), Latvija (`lv`), Maroc (`ma`), Moldova (`md`), Crna Gora (`me`), Северна Македонија (`mk`), Mali (`ml`), Malta (`mt`), México (`mx`), Malaysia (`my`), Niger (`ne`), Nigeria (`ng`), Nederland (`nl`), Norge (`no`), New Zealand (`nz`), Oman (`om`), Panamá (`pa`), Perú (`pe`), Philippines (`ph`), Polska (`pl`), Portugal (`pt`), Paraguay (`py`), Romania (`ro`), Srbija (`rs`), Rwanda (`rw`), Saudi Arabia (`sa`), Sverige (`se`), Singapore (`sg`), Slovenia (`si`), Slovensko (`sk`), Sénégal (`sn`), Tchad (`td`), Togo (`tg`), ประเทศไทย (`th`), Tunisie (`tn`), Türkiye (`tr`), 臺灣 (`tw`), Tanzania (`tz`), Україна (`ua`), Uganda (`ug`), United States (`us`), Uruguay (`uy`), Việt Nam (`vn`), Kosova (`xk`) and South Africa (`za`)<!-- /generated --> — each with its chart of accounts, its tax codes, its
  declaration boxes and its annual accounts, and each installed by `ekwo init`.
  The United Kingdom was the first that is not a Member State of the European
  Union; the United States, with the sales and use taxes of three states and
  no value added tax, the first without a VAT; Senegal and Côte d'Ivoire the
  first on the SYSCOHADA chart the OHADA member States share, written once in
  [`packs/ohada/`](packs/ohada/). The version and the certification of each
  are in [`docs/packs.md`](docs/packs.md#the-packs-of-this-checkout).
- **The French FEC.** Eighteen columns, the arrêté du 29 juillet 2013, with
  the reconciliation letter and the sub-ledger code the format requires.
- **Modules, one Postgres schema each.** Fixed assets, budgets and corporate
  income tax ship with this release, in `fixed_assets`, `budgets` and `tax`. A
  module depends on the socle by foreign key, reaches the ledger only through
  one function, and is enabled per company. The socle ignores its modules.
- **Tested on real Postgres.** The test suite runs the migrations, the seeds,
  the accounting scenarios, the installer and the MCP server against Postgres
  compiled to WebAssembly.

## Modules

The socle is `public`. Beside it, a module is a schema of its own with its own
migrations, its own row level security and its own tests.

| Module code | Schema | What it does |
|---|---|---|
| [`assets`](modules/fixed-assets/) | `fixed_assets` | Fixed assets, their depreciation schedule and their disposal. Durations, declining coefficients and the prorata convention are country pack data. |
| [`budgets`](modules/budgets/) | `budgets` | A budget per financial year and the variance against what the ledger holds. No country data, and nothing written to the ledger. |
| [`tax`](modules/corporate-tax/) | `tax` | Corporate income tax estimated from the books, line by line: the adjustments, the losses, the rates and their conditions are country pack data, and what a company declares about itself is its own. An estimate until an owner calls it final. Nothing written to the ledger. |

```sh
npx -y ekwo-os@latest module list                          # what is here, and what the database holds
npx -y ekwo-os@latest module migrate                       # apply their migrations and country seeds
npx -y ekwo-os@latest module enable assets --company "…"   # turn one on for a company
```

Then add the schema to the project's exposed schemas — Supabase dashboard →
Project Settings → API, or `[api] schemas` in `supabase/config.toml`. No
migration can do that: it is a setting of the API and not of the database, and
`ekwo module enable` prints the line every time.

**A module never writes the ledger by hand.** It hands its lines to
`post_module_entry()`, which builds the draft and calls `post_entry()` — so
sides, rounding, numbering and period locks stay in one place. The entry is
tagged `(module_code, ref)`, unique per company, which is what makes running a
depreciation twice a no-op rather than a duplicate. A test over every file of
`modules/**` refuses a write to `entries` or `entry_lines`.

[`docs/modules.md`](docs/modules.md) is how to write one.

## Install on your own Supabase project

Create a project at [supabase.com](https://supabase.com) — the free plan is
enough to start — and point the installer at it. Node 22 or later is the only
thing you need locally: no Supabase CLI, no Docker, no clone.

```sh
npx -y ekwo-os@latest init
```

The version is part of the command, as for the MCP server below: from inside a
clone of this repository, a bare `npx ekwo-os` finds the workspace package of
the same name and answers `ekwo: command not found`.

Asking an AI agent to do it with you? Point it at
[`AGENTS.md`](AGENTS.md): what it needs, the commands, and what it must never
do. Once installed, [`docs/agents.md`](docs/agents.md) is its first session in
five steps, on the MCP server and on the command line alike. Each country also has its own step-by-step page on the site, generated
from its pack, and the whole documentation is served to a model as
`https://ekwo.ai/llms.txt`.

It asks for the connection string, the country, the chart of accounts and the
language where the pack offers a choice, your organisation, the first company
and the address of the first administrator, then applies the
migrations, seeds the chart of accounts and the VAT codes, creates that
administrator in *your* Supabase Auth and runs the six steps below. Every step
checks before it acts, so running it twice creates nothing twice.

Ekwo does not create the project and does not pay for it. Your books are on
your account from the first row, which is the only version of "you own your
data" that survives the maintainer going away. Full flags, environment variables and the
non-interactive form are in [`packages/cli`](packages/cli/).

### What it does underneath

Six steps, in this order. They are ordinary SQL, and running them by hand is a
supported path — with the Supabase CLI, `supabase db push` applies the same
migrations and writes the same history table the installer does.

```sql
-- 1. Record the installation. Once, ever.
select init_instance('My Organisation', 'BE', 'community');

-- 2. Take the administrator seat. The first user to ask takes it; after
--    that, only an administrator can appoint another.
select claim_instance_admin();

-- 3. Create the company. Only an instance administrator may.
insert into companies (name, country, fiscal_country, currency_code)
values ('My Company', 'BE', 'BE', 'EUR')
returning id;

-- 4. Put yourself on its books. Administering the installation is not the
--    same as being a member of a company.
insert into company_members (company_id, user_id, role)
values ('<company-id>', auth.uid(), 'owner');

-- 5. Chart of accounts, journals, taxes and the company's default accounts.
--    The third argument is the language of the labels; left out, the company's.
select install_country_template('<company-id>', 'BE', 'fr');

-- 6. The first financial year.
insert into fiscal_years (company_id, name, start_date, end_date)
values ('<company-id>', 'FY2026', date '2026-01-01', date '2026-12-31');
```

Steps 1 and 2 are plain inserts underneath — `init_instance()` writes the
single `instance` row and `claim_instance_admin()` writes one row in
`instance_admins`. The functions exist so the bootstrap rules live in the
database rather than in whichever client happens to run first.

`install_country_template` copies the chart of accounts, the journals and the
taxes, and wires the company's default accounts — receivable, payable,
suspense, retained earnings — and its journals. It also records, in
`company_packs`, which version of which country pack this company copied, so
a later release can say what has moved since.

Those seeds are compiled from [`packs/`](packs/): a country is a manifest, a
chart of accounts as CSV and a taxes file, and `ekwo pack build` turns one
into the SQL above. The format is in [`docs/packs.md`](docs/packs.md).

The installer does steps 1 and 2 in a particular order for a reason worth
knowing. It holds a database connection, not a session, so `auth.uid()` is
NULL and row level security is bypassed rather than satisfied: it cannot *be*
the first user. So it creates that user through the Supabase Auth admin API
first — which also needs the `service_role` key, the only reason the key is
ever asked for — and writes the rows that user will be recognised by second.

By hand instead, with the Supabase CLI:

```sh
git clone https://github.com/Ekwo-ai/ekwo-os.git && cd ekwo-os
supabase link --project-ref <your-project-ref>
supabase db push                       # applies supabase/migrations in order
```

Then the reference seeds, every one of them and in this order:

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
psql "$DATABASE_URL" -f supabase/seed/12_pack_lu.sql
psql "$DATABASE_URL" -f supabase/seed/13_pack_ee.sql
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

These are the files `config.toml` lists under `[db.seed]`, which is what
`supabase db reset` applies on a local project — and the same set `ekwo init`
loads. Both lists are written from `packs/` by `ekwo pack build`, so a country
added there is in them without anybody editing this page. Leave `05_framework_generic.sql` out and the installation
has a chart of accounts but no financial statements for a chart that declares
none of its own; leave `00_territories.sql` out and the recapitulative
statement refuses to run at all, by name, rather than reporting every customer
as outside the European Union.

Skip `supabase/seed/90_demo_company.sql` unless you want the sample data, and
then run the six steps of [What it does underneath](#what-it-does-underneath)
as a signed-in user. The two routes are
interchangeable: `ekwo migrate` and `supabase db push` read and write the same
`supabase_migrations.schema_migrations`.

### Keeping it running

```sh
npx -y ekwo-os@latest status    # schema version installed against available, instance, companies
npx -y ekwo-os@latest migrate   # apply what a new release adds
npx -y ekwo-os@latest doctor    # every object this release defines, row level security, orphaned memberships, statements
npx -y ekwo-os@latest demo      # the sample company, on explicit request only
```

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
           ├─ taxes ── tax_postings      ledger account + VAT box, per tax
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

One installation belongs to one customer, so there is no `tenant_id`
anywhere: `instance` is that fact, in one row. Inside it, `instance_admins`
says who may create companies and invite people, and `company_members` gives
each person `owner`, `accountant`, `viewer` or `client` on each company — a
firm keeps the books of forty companies in one installation, and the person who
runs one of them is a `client` of that one and does not know the others exist
([`docs/firms.md`](docs/firms.md)). Your users live
in your own Supabase Auth; Ekwo never holds an account.

**Registering with Ekwo is optional and empty by default.** `contact_email`
and `registered_at` on the instance row stay null unless you call
`register_instance()`, nothing in this repository reads them, and
`unregister_instance()` puts them back. `ekwo init` asks the question once, at
the end, and the default answer is no. Community works unregistered, forever,
and `edition` gates no feature.

`post_document(id)` turns a document into an entry. `trial_balance`,
`general_ledger`, `aged_balance`, `vat_return`, `ec_sales_list`,
`financial_statement` and `fec_lines` read it back — `financial_statement` on the schemes of the country
pack, such as the Belgian abbreviated model or the French liasse, or on a generic
framework by account type that fits any chart of accounts. The FEC of a
financial year opens on its *à-nouveaux*, computed from the ledger and never
posted, and carries the result of a year nobody has closed yet, so the file
rebuilds the balance sheet it belongs to.
`opening_balance(company, year, lines)` takes the trial balance of whatever
kept the books before, and `close_fiscal_year(year)` closes a year the way the
country pack says — straight to retained earnings, into a current-year result
account, or through the appropriation accounts — with `reopen_fiscal_year` for
a close run too early. An invoice is printed from three views —
`document_header`, `document_line_items` and `document_legal_mentions` — so a
renderer reads the seller, the buyer, the amounts, the lines and the sentences
the law requires without being configured with any of them.
`docs/schema.md` describes every table and column; `docs/mapping.md` lines each
one up against EN 16931 and the FEC; `docs/languages.md` says how a label
reaches a reader in their own language.

## Who may do what

**A role is a preset. A capability is what a policy tests.** `owner`,
`accountant`, `viewer` and `client` are rows in `role_capabilities`, and what the
schema actually checks is a code from `capabilities` — `documents.post`,
`payments.write`, `settings.write`, `members.manage`, `year_end.close` and
fifteen more. Read `select * from capabilities order by area, code` on your own
installation: that list is the vocabulary, and a module adds its own to it.

| Preset | Holds |
|---|---|
| `viewer` | every `.read` — the books, the documents, the chart, the catalogue |
| `client` | what a viewer holds, plus `documents.deposit`: handing a file over to whoever keeps the books, and nothing else |
| `accountant` | that, plus writing and posting, matching, the settings and the year-end close |
| `owner` | that, plus `company.write` and `members.manage` |

**One member can be adjusted without inventing a role.**
`company_members.capabilities_granted` adds, `capabilities_revoked` takes away,
and a revoke wins over a grant and over the preset — an owner who may not close
a year is a separation of duties, not a mistake.

```sql
-- a bookkeeper who posts invoices and never touches a period lock
update company_members
   set capabilities_granted = array['documents.post'],
       capabilities_revoked = array['company.write']
 where company_id = :company and user_id = :user;

select member_capabilities(:company);   -- what you may do here
```

**Inviting somebody who has no account yet.** `invite_member()` returns a token
**once** — only a sha256 of it is stored — and the person accepts it themselves,
signed in with the address it was sent to:

```sql
select * from invite_member(:company, 'her@example.com', 'accountant',
                            '["members.manage"]'::jsonb);
-- she signs up in your Supabase Auth, then, as herself:
select * from accept_invitation('<the token>');
```

An invitation is single use, expires, and is withdrawn with
`revoke_invitation()`. The MCP server offers `invite_member`,
`list_invitations` and `revoke_invitation`; accepting is the invitee's own act
and has no tool.

**Removing a member, or changing their preset.** `remove_member(:company,
:user)` takes somebody out — leaving a company oneself needs no
`members.manage` — and `set_member_role(:company, :user, 'viewer')` moves a
member to another preset, clearing the capabilities granted or revoked on them
so far. Neither lets the last owner of a company go: promote the successor
first. `company_members_list(:company)` lists the members with the address
each signed up with, for whoever holds `members.manage`. The MCP server offers
`remove_member` and `set_member_role`.

## Keys for machines

A script — a nightly import, a till, a bank feed — has no browser to sign in
with. Do not hand it the `service_role` key, which bypasses row level security
by construction, and do not create a user for it. Issue a key:

```sql
select * from create_api_key(:company, 'Nightly bank import',
                             '["bank.write", "bank.read"]'::jsonb,
                             now() + interval '1 year');
```

The secret comes back once and is stored as a sha256. A key belongs to **one
company**, does exactly what its capabilities say, and can never carry a
capability the person issuing it does not hold themselves — so withdrawing
somebody's capability withdraws the keys they left behind. `revoke_api_key()`
stops one for good.

A key is presented for the length of a transaction, not for a session:

```sql
begin;
select * from use_api_key('ekwo_…');   -- has_capability() now answers for it
insert into bank_transactions (…) values (…);
commit;
```

Two consequences worth knowing before you build on it. A key is **not a
session**: `auth.uid()` stays null, so what it reaches is what a policy asks a
capability for — the tables of its company — and not the reference tables or
the company row. And because PostgREST runs every request in its own
transaction, `use_api_key()` cannot be a separate HTTP call: a key is for a
client that holds a connection, which is what the MCP server's self-hosted
route does.

## The TypeScript packages

`packages/core` carries the types of the schema and a typed client over its
functions, with no runtime dependency beyond an optional
`@supabase/supabase-js`. The FEC moved out to `@ekwo-ai/fec`, because a file
format is MIT; the re-exports `@ekwo-ai/core` kept for one version are gone
since `v0.2.0`, so import the generator from the package that owns it.
`packages/cli` is the `ekwo` command above; outside this repository it has one
runtime dependency, the Postgres driver, and it never writes a password or a
key to disk — `ekwo login` keeps a session, in the user's own configuration
directory and never inside a repository, and no command that keeps books takes
a `service_role` key. It keeps books too — `ekwo doc new`, `ekwo post`, `ekwo payment record` — through the functions the MCP server calls, which moved into `packages/core` for that, and computes no amount of its own. Every command takes `--json` and ends on an exit code that tells a wrong call
(2) from the database refusing (3).

```ts
import { EkwoClient } from '@ekwo-ai/core';
import { createClient } from '@supabase/supabase-js';

const ekwo = new EkwoClient(createClient(url, key));

await ekwo.postDocument(documentId);
const balance = await ekwo.trialBalance({ companyId, from: '2026-01-01', to: '2026-12-31' });
const boxes   = await ekwo.vatReturn({ companyId, from: '2026-07-01', to: '2026-09-30' });
const fec     = await ekwo.generateFec({ companyId, from: '2026-01-01', to: '2026-12-31' });
```

`packages/mcp` is the Model Context Protocol server, published as
`@ekwo-ai/mcp`. It is the same idea as the client above, for an agent
rather than for your code: tools over stdio — read the chart of accounts,
create a draft invoice, post it, register a bank account, record and match a
payment, import an opening balance, close a year, pull the trial balance, the
aged balance, the VAT return or the FEC — plus the chart of accounts and the taxes as resources, and two prompts for
closing a month and preparing a return.

It runs **as the user**, never as `service_role`: it signs in with their
address and password, or takes their access token, and row level security
decides the rest. Every ledger write goes through the schema's own functions,
so nothing in the server writes an `entries` row, and nothing in it can unpost
an entry. Configuration is a block of environment variables in
`claude_desktop_config.json` or `.mcp.json`; see
[`packages/mcp`](packages/mcp/).

### Hosted, at `https://mcp.ekwo.ai/mcp`

The same server, reachable as a URL, for a client that adds remote servers
rather than launching them — claude.ai, or any other that speaks **Streamable
HTTP**. Nothing is installed and no key is written into a configuration file:
the server answers an unauthenticated call with `401` and a
`WWW-Authenticate` header naming its protected-resource metadata, the client
follows it to the authorization server, and the person approves the connection
in their browser. Dynamic client registration (RFC 7591) means the client
needs no credentials of its own, and the scope asked for is `books`.

Point a client at the URL and it discovers the rest:

```
https://mcp.ekwo.ai/mcp
```

An agent reading this without a browser can start from
[`/.well-known/oauth-protected-resource`](https://mcp.ekwo.ai/.well-known/oauth-protected-resource),
which names the authorization server and the scope.

### Over stdio, as a local process

```sh
npx -y @ekwo-ai/mcp@latest
```

The version is part of the command: from inside a clone of this repository, a
bare `npx @ekwo-ai/mcp` finds the unbuilt workspace package and answers
`ekwo-mcp: command not found`.

## Format libraries

They live in [`packages/formats/`](packages/formats/), under MIT, one package
per format and never one per country. Each imports nothing from the core and
declares the row shapes it reads in its own types, so any book-keeping system
that can produce those columns can use them:

- [`@ekwo-ai/fec`](packages/formats/fec/) — the French *fichier des écritures
  comptables*: eighteen columns, the arrêté du 29 juillet 2013.
- [`@ekwo-ai/factur-x`](packages/formats/factur-x/) — Factur-X and ZUGFeRD
  e-invoices: EN 16931 CII XML and PDF/A-3 embedding.
- [`@ekwo-ai/peppol-ubl`](packages/formats/peppol-ubl/) — invoices and credit
  notes as the Peppol network carries them: UBL 2.1, Peppol BIS Billing 3.0,
  with every published rule the file breaks named by its identifier. Writing
  the file is free; sending it takes an access point.
- [`@ekwo-ai/xbrl-cbso`](packages/formats/xbrl-cbso/) — XBRL for the annual
  accounts filed with the National Bank of Belgium.
- [`@ekwo-ai/vat-consignment`](packages/formats/vat-consignment/) — the Belgian
  periodic VAT return, as Intervat takes it, written from the figures a
  declaration was filed with rather than from a second computation.
- [`@ekwo-ai/intra-consignment`](packages/formats/intra-consignment/),
  [`@ekwo-ai/des`](packages/formats/des/),
  [`@ekwo-ai/ecdf`](packages/formats/ecdf/) and
  [`@ekwo-ai/vd`](packages/formats/vd/) — the recapitulative statements of
  European Union supplies, for Belgium, France, Luxembourg and Estonia.

- [`@ekwo-ai/camt053`](packages/formats/camt053/) — the one that reads: an
  ISO 20022 bank statement (camt.053, versions 02 to 14) into statements and
  lines, amounts as decimal strings, an account that is an IBAN or is not, and
  a balance that is checked and never corrected. Its own strict XML reader,
  because a statement is a file somebody else wrote.

They are not dependencies of the core: the core produces rows, and a brick
turns rows into a file. The one place they meet is a test.

## Community and cloud

The line is operational, not functional. Everything a bookkeeper can do alone
is here and always will be.

| Ekwo OS, on your Supabase | Managed edition, on [ekwo.ai](https://ekwo.ai) |
|---|---|
| The whole schema, migrations, row level security | Provisioning and running the instance |
| Journals, entries, matching, charts of accounts | Backups, restores, version upgrades |
| Invoicing, credit notes, VAT, reports, FEC | AI agents you set up, acting on your instructions |
| Manual import of bank files | Bank connections under contract |
| Generating the files: XBRL, Factur-X, the VAT return, the EC sales lists | Peppol access point, certificate included |
| Everything above, forever, for nothing | Transmission to Intervat, Teledec, the NBB, on the business's instruction |

The test is simple: does it keep working on its own, with us or without us? If
yes, it belongs here, under AGPL, and no licence key gates it. If no, it is a
service, because something has to be kept alive for it to work: a contract, a
certificate, a credential, a machine. Those services are operated by Ekwo
(Karuna Co OÜ) and are not part of this repository — there is no commercial
subdirectory here, and nothing here needs them.
[`docs/cloud-services.md`](docs/cloud-services.md) lists them, and says what
will never be sold.

## Security

Row level security is the whole model: every table carries it, every policy
is a function of `auth.uid()` — through `has_capability()`, which is the one
question a policy asks — the reports run as the caller, and the views run with
the caller's rights. An anonymous request sees nothing and may call nothing but
the policy helpers. The MCP server refuses a `service_role` key.
`tests/rls.test.ts` and `tests/capabilities.test.ts` prove who may read and who
may write, and the CI fails if a table ever arrives without a policy.

Three things the schema cannot do for you:

- **Turn off public sign-ups** on your Supabase project (Authentication →
  Sign In / Providers → *Allow new users to sign up*). Ekwo invites people;
  it never needs strangers to be able to create an account. A stranger with
  an account sees nothing, but there is no reason to let them in.
- **Keep two administrators.** If the last row of `instance_admins` goes —
  a deleted user cascades — the seat reopens to the first signed-in user
  who claims it, by design, so that an installation is never locked out.
  `ekwo doctor` warns when an installation has no administrator left.
- **Keep the `service_role` key off every machine that does not need it.**
  It bypasses row level security by construction. The CLI needs it once, to
  create the first administrator; nothing else in this repository does. A
  script that needs to work on its own gets an API key, which is scoped to one
  company and to a list of capabilities — see *Keys for machines* above.

## What this is not

Ekwo is open source data infrastructure. It is not an accounting firm and
gives no accounting, tax, financial, legal or investment advice. Your books,
returns and filings are yours, and the software is yours to change; a country
pack is our reading of the rules at a date, and a review is a professional's
good-faith reading, not a guarantee. Where accounting and tax are regulated
professions — in the European Union, the United Kingdom, the United States,
the OHADA States and elsewhere — consult a professional authorised in your
country. [DISCLAIMER.md](DISCLAIMER.md) says this in full, and it is published
at [ekwo.ai/disclaimer](https://ekwo.ai/disclaimer/). Read it before you file
anything.

## Finding your way

Each folder carries a short README saying what lives there and the rule
that applies to it: [`supabase/`](supabase/), [`supabase/migrations/`](supabase/migrations/),
[`supabase/seed/`](supabase/seed/), [`packages/core/`](packages/core/),
[`packages/cli/`](packages/cli/), [`packages/mcp/`](packages/mcp/), [`modules/`](modules/),
[`tests/`](tests/), [`docs/`](docs/) and [`scripts/`](scripts/). The long-form
reference is in `docs/`.

A few names still carry the vocabulary of one tax régime — `vat_return` for the
periodic return of every country, among others. They are renamed before 1.0,
each with an alias for at least one minor release:
[the names that change before 1.0](docs/releasing.md#names-that-change-before-10)
lists them with what to call instead.

Where the project is heading: [`docs/road-to-1.0.md`](docs/road-to-1.0.md)
says what version 1.0 will promise for the whole 1.x line, and the proofs —
each one checkable, several of them open to anybody who keeps books — that
come before the tag.

## Development

```sh
npm install
npm run typecheck
npm test          # applies every migration and seed to an in-memory Postgres
npm run build     # builds every workspace; the CLI copies supabase/ into its dist
```

Tests use [PGlite](https://pglite.dev), so no Docker and no local Postgres.
`tests/helpers/supabase-shim.sql` stands in for Supabase's `auth` schema and
its API roles; it is a test file and never ships.

## Contributing

Issues and pull requests are welcome. Contributions require the
[Contributor Licence Agreement](CLA.md); see [CONTRIBUTING.md](CONTRIBUTING.md)
for how to work on the schema without breaking a database somebody already
installed.

## Licence

[AGPL-3.0-only](LICENSE) © Karuna Co OÜ (Estonian registry code 14510673),
trading as Ekwo. Installing Ekwo OS and running it for your
own organisation — modified or not — puts no obligation on you. The share-alike
clause bites only if you modify it *and* offer that modified version to people
outside your organisation over a network.

**The format libraries under [`packages/formats/`](packages/formats/) are
MIT**, each with its own `LICENSE`. Their value is ubiquity: a file format
should be readable and writable by anyone, including a competitor.

"Ekwo" and the Ekwo logo are trademarks and are not covered by the licence.
Fork the code; do not call the fork Ekwo.
