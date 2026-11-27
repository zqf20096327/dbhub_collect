<div align="center">

<h1>Soll – Zeiterfassung und Dienstplan für dein Team.</h1>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/screenshots/heute-dark-desktop.png">
  <img src="docs/assets/screenshots/heute-light-desktop.png" alt="Soll auf dem Desktop: Stempeln mit laufender Arbeitszeit, Pausenhinweis nach § 4 ArbZG und Projekt-Stoppuhr" width="900">
</picture>

**Selbst gehostete Zeiterfassung mit Dienstplan für kleine Betriebe: Stempeln im Web, am Handy und am Tablet, Prüfung nach Arbeitszeitgesetz mit Paragraph, Monatsabschluss mit Prüfwert und DATEV-Export – ohne Kosten pro Kopf.**

[![CI](https://github.com/Speicherstadt/soll/actions/workflows/ci.yml/badge.svg)](https://github.com/Speicherstadt/soll/actions/workflows/ci.yml)
[![Lizenz: AGPL-3.0](https://img.shields.io/badge/Lizenz-AGPL--3.0-blue)](LICENSE)
[![Doku](https://img.shields.io/badge/Doku-soll.work-4f46e5?logo=zensical&logoColor=white)](https://soll.work/)
[![Demo](https://img.shields.io/badge/Demo-soll.work%2Fdemo-16a34a)](https://soll.work/demo/)
[![Docker](https://img.shields.io/badge/Container-amd64%20%7C%20arm64-2496ed?logo=docker&logoColor=white)](https://soll.work/installation.html)

[Warum?](#warum-soll) •
[Funktionen](#funktionen) •
[Screenshots](#screenshots) •
[Live-Demo](https://soll.work/demo/) •
[Umzug](#umzug-aus-anderen-tools) •
[Schnellstart](#schnellstart) •
[FAQ](#faq) •
[Dokumentation](https://soll.work/) •
[Entwicklung](#entwicklung)

<sub>English: self-hosted open-source time tracking and shift planning for small businesses in Germany, built around the BAG ruling (1 ABR 22/21) and German labour law (ArbZG, MiLoG, JArbSchG, MuSchG, BUrlG). Clock in via web, offline-capable PWA, or a shared tablet terminal, close months with a tamper-evident hash chain, and export payroll data to DATEV. The app supports German, English, Turkish, Polish, Ukrainian and Arabic (RTL); the [documentation](https://soll.work/) is in German.</sub>

</div>

## Warum Soll?

**Arbeitszeit erfassen, wie es das Gesetz verlangt – auf deinem eigenen Server.** 🇩🇪 🇪🇺

Seit dem Beschluss des Bundesarbeitsgerichts (BAG, 13.09.2022, 1 ABR 22/21) müssen Betriebe Beginn, Ende und Dauer der Arbeitszeit erfassen. Soll ist die selbst gehostete Open-Source-Lösung dafür: ein Container mit SQLite auf deinem eigenen Server oder NAS, ohne laufende Kosten pro Person.

- **Prüfung nach Paragraph statt Rätselraten:** Höchstarbeitszeit (§ 3 ArbZG), Pausen (§ 4 ArbZG), Ruhezeit (§ 5 ArbZG), Nacht-, Sonn- und Feiertage, Mindestlohn, Minijob-Grenze, Jugendschutz und Mutterschutz – jeder Befund nennt die konkrete Norm ([Regelwerk](https://soll.work/regeln.html)).
- **Unveränderlicher Monatsabschluss (GoBD):** Jede Schreiboperation hängt an der [Audit-Kette](https://soll.work/audit-kette.html); Beschäftigte bestätigen ihren Monat und erhalten auf dem Stundenzettel einen Prüfwert, der nachträgliche Änderungen aufdeckt.
- **Modular für jeden Betrieb:** Arbeitszeit, Dienstplan, Projektzeit und Terminal lassen sich einzeln ein- und ausschalten; wer nur Projektzeit oder nur Stempeln braucht, sieht auch nur das.
- **Keine Kosten pro Kopf:** 2 oder 50 Beschäftigte laufen auf derselben Instanz; bezahlt wird nur der eigene Server.
- **Reibungsloser Umzug:** Zeiten, Abwesenheiten, Kunden, Aufträge, Tätigkeiten, Schichten und Salden zum Stichtag aus anderen Werkzeugen oder Excel/CSV übernehmen ([Umzug](https://soll.work/umzug.html)).

## Funktionen

Kurz je Bereich; alle Details stehen auf der verlinkten Seite der [Dokumentation](https://soll.work/).

| Bereich | Was Soll kann |
|---|---|
| ⏱️ [Stempeln](https://soll.work/stempeln.html) | Kommen, Pause und Gehen im Browser oder als PWA auf dem Handy (auch offline mit signierter Warteschlange), Nachtrag und Korrektur mit Pflichtgrund |
| 📱 [Terminal](https://soll.work/terminal.html) | Geteiltes Android-Tablet am Eingang mit PIN, QR-Code oder NFC-Karte, auch ohne Netz |
| ⚖️ [Prüfung](https://soll.work/pruefung.html) · [Bereitschaft](https://soll.work/bereitschaft.html) · [Nacht & Sonntag](https://soll.work/nacht-sonntag.html) | Tägliche Prüfung nach [Regelwerk](https://soll.work/regeln.html), [Mindestlohn & Minijob](https://soll.work/mindestlohn.html), [JArbSchG & MuSchG](https://soll.work/jugend-mutterschutz.html) und [Feiertagen](https://soll.work/feiertage.html) je Bundesland |
| 🌴 [Abwesenheiten](https://soll.work/abwesenheiten.html) · [Konten](https://soll.work/konten.html) | Urlaub mit Verfallshinweis (EuGH / BAG), Krankmeldung und eAU-Frist, Kinderkrankentage, Überstundenkonto und Teamkalender |
| 📅 [Dienstplan](https://soll.work/dienstplan.html) | Schichtvorlagen, Bedarf je Rolle, Arbeitszeitprüfung bereits beim Einplanen, Entwurf und Veröffentlichung, Schichttausch und iCal-Kalender-Feed |
| 💼 [Projektzeit](https://soll.work/projektzeit.html) | Kunden, Aufträge mit Budgetwarnung, Tätigkeiten, Stundensätze, Stoppuhr, Auslastung, Stundennachweis-PDF mit Unterschrift und Übergabe an [Haben](https://github.com/Speicherstadt/haben) |
| 🔒 [Monatsabschluss](https://soll.work/monatsabschluss.html) · [Prüfexport](https://soll.work/pruefexport.html) | Bestätigung durch Beschäftigte, Abschluss durch den Betrieb, Stundenzettel-PDF mit Prüfwert und Prüfseite, [Verfahrensdokumentation](https://soll.work/verfahrensdokumentation.html) nach GoBD |
| 💶 [DATEV-Lohnexport](https://soll.work/datev.html) | Bewegungsdaten für LODAS und Lohn und Gehalt mit [steuerfreien Zuschlägen nach § 3b EStG](https://soll.work/zuschlaege.html) aus abgeschlossenen Monaten |
| 🔔 [Erinnerungen](https://soll.work/erinnerungen.html) | Hinweise per Web Push und E-Mail bei fehlender Stempelung, fälliger Pause, offenem Monat oder fehlender Bescheinigung |
| 🔐 [Anmeldung](https://soll.work/anmeldung.html) · [Einrichtung](https://soll.work/einrichtung.html) | Passkeys, Passwort, OpenID Connect, Einladungslinks; 6 Sprachen (`de`, `en`, `tr`, `pl`, `uk`, `ar` RTL) |
| 🛡️ [Datenschutz](https://soll.work/loeschkonzept.html) | [Infoblatt für Beschäftigte](https://soll.work/infoblatt.html), [Vorlage Betriebsvereinbarung](https://soll.work/betriebsvereinbarung.html), automatische Aussonderung abgelaufener Monate und DSGVO-Auskunft |
| 🔌 [REST-API & MCP](https://soll.work/api.html) | Versionierte Schnittstelle mit OpenAPI und schreibgeschützter MCP-Server für KI-Assistenten |

## Screenshots

<table>
  <tr>
    <td width="50%"><picture><source media="(prefers-color-scheme: dark)" srcset="docs/assets/screenshots/dienstplan-dark-desktop.png"><img src="docs/assets/screenshots/dienstplan-light-desktop.png" alt="Dienstplan mit Schichten je Person und Wochentag sowie Arbeitszeitprüfung"></picture><br><sub><b>Dienstplan</b>: Schichten planen mit Prüfung nach ArbZG</sub></td>
    <td width="50%"><picture><source media="(prefers-color-scheme: dark)" srcset="docs/assets/screenshots/projekte-dark-desktop.png"><img src="docs/assets/screenshots/projekte-light-desktop.png" alt="Projekte mit Aufträgen, Budgetanzeige und Verbrauchsstatus"></picture><br><sub><b>Projekte</b>: Aufträge, Budgets, Stundennachweise und Übergabe</sub></td>
  </tr>
  <tr>
    <td width="50%"><picture><source media="(prefers-color-scheme: dark)" srcset="docs/assets/screenshots/monat-dark-desktop.png"><img src="docs/assets/screenshots/monat-light-desktop.png" alt="Monatsabschluss mit Soll, Ist, Saldo, Bestätigung, Stundenzettel-PDF und Prüfwert"></picture><br><sub><b>Monatsabschluss</b>: Soll, Ist, Saldo, PDF und Prüfwert</sub></td>
    <td width="50%"><picture><source media="(prefers-color-scheme: dark)" srcset="docs/assets/screenshots/abwesenheiten-dark-desktop.png"><img src="docs/assets/screenshots/abwesenheiten-light-desktop.png" alt="Abwesenheiten mit Resturlaub, Überstunden, Kinderkrankentagen, Antrag und Teamkalender"></picture><br><sub><b>Abwesenheiten</b>: Konten, Urlaubsantrag, Krankmeldung und Teamkalender</sub></td>
  </tr>
</table>

## Umzug aus anderen Tools

Alle Daten werden in einem geführten [Umzugs-Assistenten](https://soll.work/umzug.html) vorab geprüft (Probelauf ohne Schreiben, Dubletten-Schutz, Aufbewahrung der Originaldatei unter ihrem SHA-256).

| Werkzeug | Weg | Was übernommen wird |
|---|---|---|
| **Clockodo** | API & CSV | Mitarbeiter, Zeiten, Abwesenheiten, Kunden, Projekte und Leistungen |
| **Kimai** | REST-API | Kunden, Projekte, Tätigkeiten und Zeitbuchungen als Zeiten & Projektzeit |
| **Personio** | API v2 & Excel/CSV | Mitarbeiter, Anwesenheiten mit Pausen, Abwesenheiten mit halben Tagen |
| **Papershift · Planday · Crewmeister** | API & Excel/CSV | Mitarbeiter, Zeiten, Abwesenheiten und geplante Schichten (Planday, Crewmeister) |
| **Toggl Track · Clockify** | API & CSV | Kunden, Projekte und Zeiten (Solo-Modus) |
| **Excel / CSV & Soll-CSV** | Datei | Freie Spaltenzuordnung (`.xlsx`/`.csv`) sowie Vorlagen für Salden zum Stichtag |

## Schnellstart

Soll läuft als einzelner Container mit SQLite (ohne Datenbankserver) für `amd64` und `arm64`:

```sh
mkdir soll && cd soll
curl -fsSLO https://raw.githubusercontent.com/Speicherstadt/soll/main/deploy/compose.yaml
curl -fsSL -o soll.env https://raw.githubusercontent.com/Speicherstadt/soll/main/deploy/soll.env.example
# in soll.env: SOLL_SECRET_KEY (openssl rand -base64 32) und SOLL_URL eintragen
docker compose up -d
docker compose exec soll soll backup   # Sicherung im laufenden Betrieb
```

Podman Quadlet, Sicherung & Wiederherstellung, Updates und alle Umgebungsvariablen stehen in der [Installationsanleitung](https://soll.work/installation.html). Zum lokalen Ausprobieren mit zwei Musterbetrieben gibt es [Demo-Daten](https://soll.work/demo.html) (`bun run demo`).

## FAQ

<details>
<summary><b>Muss ich die Arbeitszeit meiner Beschäftigten erfassen?</b></summary>

Ja. Seit dem Beschluss des Bundesarbeitsgerichts vom 13.09.2022 (1 ABR 22/21) gilt die Pflicht zur Erfassung von Beginn, Ende und Dauer für jeden Betrieb, für Minijobs bereits länger nach § 17 MiLoG.
</details>

<details>
<summary><b>Wie verhindert Soll nachträgliche Manipulationen (GoBD)?</b></summary>

Jede Schreiboperation hängt in derselben Transaktion ein Glied an die [Audit-Kette](https://soll.work/audit-kette.html) an. Nach dem [Monatsabschluss](https://soll.work/monatsabschluss.html) sind Zeiten gesperrt (Korrekturen laufen als Gegeneintrag mit Grund), und der Stundenzettel-PDF enthält einen Prüfwert, mit dem Beschäftigte den Stand auf der Prüfseite unabhängig verifizieren können. Die [Verfahrensdokumentation](https://soll.work/verfahrensdokumentation.html) entsteht direkt aus dem Betriebsstand.
</details>

<details>
<summary><b>Brauche ich eine eigene Stempeluhr?</b></summary>

Nein. Neben Browser und Handy-PWA reicht ein Android-Tablet am Eingang; gestempelt wird mit PIN, QR-Code oder NFC-Karte ([Terminal](https://soll.work/terminal.html)).
</details>

<details>
<summary><b>Werden meine Zugangsdaten beim Import aus anderen Tools gespeichert?</b></summary>

Nein. API-Tokens und Zugänge für den [Umzug](https://soll.work/umzug.html) werden nur für den jeweiligen Abruf verwendet und nirgends gespeichert.
</details>

<details>
<summary><b>Kann ich Soll mit Haben verbinden?</b></summary>

Ja. Abgerechnete Projektzeiten lassen sich als Leistungspositionen an [Haben](https://github.com/Speicherstadt/haben) übergeben ([Projektzeit](https://soll.work/projektzeit.html)).
</details>

## Dokumentation

Alles im Detail, mit Suche: **https://soll.work/**.

## Entwicklung

[![TypeScript](https://img.shields.io/badge/TypeScript-3178c6?logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![Bun](https://img.shields.io/badge/Bun-000000?logo=bun&logoColor=white)](https://bun.sh)
[![Hono](https://img.shields.io/badge/Hono-e36002?logo=hono&logoColor=white)](https://hono.dev)
[![SolidJS](https://img.shields.io/badge/Solid%202-2c4f7c?logo=solid&logoColor=white)](https://www.solidjs.com)
[![SQLite](https://img.shields.io/badge/SQLite-Drizzle-003b57?logo=sqlite&logoColor=white)](https://orm.drizzle.team)

Hinweise für Mitwirkende und Agenten stehen in [CLAUDE.md](CLAUDE.md), offene Punkte in [BAULISTE.md](BAULISTE.md), Aufbau und Befehle unter [Entwicklung](https://soll.work/entwicklung.html).

```sh
bun install
bun run check        # Typen, Lint, Solid-2-Prüfung, Tests, Build
bun run e2e          # Playwright: desktop, phone, terminal
bun run demo         # Demo-Daten: Weber Haustechnik & Café Elbblick
```

| Paket | Inhalt |
|---|---|
| `packages/arbeitszeit` | Prüfregeln, Feiertage, Jahreswerte, Soll/Ist, Konten, Zuschläge (reine Funktionen) |
| `packages/import` | Parser für Soll-CSV, Excel/CSV, Clockodo, Kimai, Personio, Papershift, Planday, Crewmeister, Toggl, Clockify |
| `packages/export` | DATEV-ASCII, CSV, PDF (Stundenzettel, Prüfexport, Stundennachweis, Verfahrensdokumentation) |
| `packages/ui` | UI-Komponenten nach `DESIGN.md` (Solid 2, Tailwind 4) |
| `apps/server` | Hono-API, Drizzle mit SQLite (WAL), Better Auth, Audit-Kette |
| `apps/web` | Solid-2-SPA/PWA, Terminal-Ansicht, Offline-Warteschlange |

## Mehr von uns

Weitere Open-Source-Apps für deinen eigenen Server: **[speicherstadt.org](https://speicherstadt.org)**

---

<div align="center">

⭐ **Gefällt dir Soll?** Ein [Stern auf GitHub](https://github.com/Speicherstadt/soll) hilft anderen, es zu finden.

<sub>Lizenz: <a href="LICENSE">AGPL-3.0</a><br>
Soll ist keine Rechtsberatung. Einstellungen nach Arbeitszeitgesetz, Zuschläge und Aufbewahrungsfristen vor dem Echtbetrieb prüfen.<br>
DATEV, Clockodo, Kimai, Personio, Papershift, Planday, Crewmeister, Toggl und Clockify sind Marken ihrer jeweiligen Inhaber; Soll steht in keiner Verbindung zu diesen Unternehmen.</sub>

</div>
