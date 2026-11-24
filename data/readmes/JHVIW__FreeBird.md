<p align="center">
  <img src="docs/assets/banner.png" alt="FreeBird: gratis boekhouding voor Nederlandse ondernemers" width="100%">
</p>

<p align="center">
  <a href="LICENSE"><img alt="Licentie: AGPL-3.0" src="https://img.shields.io/badge/licentie-AGPL--3.0-0B6E8E?style=flat-square"></a>
  <img alt="Next.js 15" src="https://img.shields.io/badge/Next.js-15-0F2534?style=flat-square&logo=nextdotjs&logoColor=white">
  <img alt="PostgreSQL 16" src="https://img.shields.io/badge/PostgreSQL-16-0F2534?style=flat-square&logo=postgresql&logoColor=white">
  <img alt="Docker" src="https://img.shields.io/badge/Docker-klaar-0F2534?style=flat-square&logo=docker&logoColor=white">
  <img alt="Gemaakt voor Nederland" src="https://img.shields.io/badge/gemaakt%20voor-🇳🇱%20ondernemers-E9742A?style=flat-square">
</p>

<p align="center">
  <b>Facturen, bank, bonnen, BTW-aangifte en jaaroverzicht in één app.</b><br>
  Op je eigen server, zonder abonnement. Je administratie blijft van jou.
</p>

<p align="center">
  <a href="#snel-starten">Snel starten</a> ·
  <a href="#wat-freebird-doet">Functies</a> ·
  <a href="#overstappen-van-moneybird">Overstappen</a> ·
  <a href="#veelgestelde-vragen">Veelgestelde vragen</a>
</p>

---

Een boekhoudpakket kost al snel een paar honderd euro per jaar, en de prijs gaat elk jaar omhoog. Ondertussen staat je administratie op de server van een ander, in een formaat dat je er niet makkelijk uit krijgt.

FreeBird is een volledige boekhouding voor zzp'ers en kleine ondernemers in Nederland. Je draait hem zelf, op een VPS van een paar euro per maand of op een server die je al hebt. Er zijn geen gebruikerslimieten, geen premium-functies en geen jaarlijkse prijsverhoging. De code is open, dus je kunt altijd zien wat er met je cijfers gebeurt.

<p align="center">
  <img src="docs/screenshots/dashboard.png" alt="Het overzicht van FreeBird met saldo, openstaande facturen, omzet en deadlines" width="100%">
</p>

## Wat FreeBird doet

### Verkopen
- **Facturen** met doorlopende nummering zonder gaten, als PDF en als **UBL 2.1 (Peppol BIS 3.0)** voor e-facturatie.
- **Betaallink** (bunq.me) op elke factuur, versturen via je eigen mailserver, **automatische herinneringen**.
- **Creditnota's** en **terugkerende facturen** (abonnementen, maandelijkse retainers).
- **Engelse facturen** per klant: PDF, BTW-vermelding, mail en herinneringen volgen de taal van de klant.
- **Sjablonen** voor opmaak (klassiek, modern of compact, met je eigen kleur, lettertype en logo), vaste factuurregels en mailteksten.
- **Conceptfactuur uit één zin**: "12 uur ontwerp voor Bakkerij Jansen à €85" wordt een factuur.

### Bank en inkoop
- **bunq-koppeling** via API key. Transacties komen direct binnen via een callback, met een sync elke 15 minuten als vangnet.
- **Automatisch afletteren**: betalingen worden gekoppeld aan facturen, bonnen en je eigen regels.
- **Bonnen per mail**: stuur facturen naar een eigen adres, FreeBird leest ze uit (PDF, foto of factuur in de mailtekst), boekt ze en koppelt de betaling.
- **Ontbrekende bonnen** zie je in één lijst, met een kant-en-klare mail om de factuur op te vragen.
- **Privé betaalde zakelijke kosten** en **bedrijfsmiddelen met afschrijving**.

### BTW en belasting
- **Kwartaalaangifte per rubriek**, klaar om over te nemen in Mijn Belastingdienst Zakelijk.
- **ICP-opgaaf**, **OSS** met drempelbewaking (en het IBAN-land als bewijs), verlegde BTW binnen en buiten de EU.
- **Controle vóór het indienen**: vaste checks (niet-verwerkte transacties, VIES, aansluiting ICP) plus een AI-controle op verkeerde BTW-codes.
- **Jaaroverzicht** met winst-en-verliesrekening, balans, invulhulp voor de aangifte inkomstenbelasting, urencriterium en een schatting van de belasting.
- Periodes **vergrendelen** na het indienen.

### Boekhouding zoals het hoort
- Echt **dubbel boekhouden**, met bedragen in centen. Elke mutatie is een journaalpost die op nul uitkomt.
- Wat definitief is, verandert nooit. Correcties gaan via een tegenboeking of creditnota, met een audit-log.
- **Export** van journaal en facturen naar CSV, voor je boekhouder of je eigen archief.

### AI als assistent, niet als baas
- Boekvoorstellen per banktransactie op basis van hoe jij eerder boekte.
- Bonnen uitlezen, regels voorstellen, fouten opsporen vóór de aangifte.
- **Vraag het FreeBird**: "Wat heb ik dit jaar aan software uitgegeven?" Het antwoord komt rechtstreeks uit je administratie.
- De AI doet alleen voorstellen. Er wordt pas iets geboekt als jij op bevestigen klikt. Zonder API key werkt alles gewoon, alleen zonder suggesties.

<table>
  <tr>
    <td width="50%"><img src="docs/screenshots/bank.png" alt="Banktransacties met boekvoorstellen"><p align="center"><sub>Bank: elke transactie met een voorstel</sub></p></td>
    <td width="50%"><img src="docs/screenshots/btw.png" alt="BTW-aangifte per rubriek met controles"><p align="center"><sub>BTW-aangifte per rubriek, met controles</sub></p></td>
  </tr>
  <tr>
    <td width="50%"><img src="docs/screenshots/facturen.png" alt="Overzicht van verkoopfacturen"><p align="center"><sub>Facturen met status en herinneringen</sub></p></td>
    <td width="50%"><img src="docs/screenshots/login.png" alt="Inlogscherm van FreeBird"><p align="center"><sub>Eén wachtwoord, je eigen server</sub></p></td>
  </tr>
</table>

## Voor wie

FreeBird is gemaakt voor **eenmanszaken en kleine ondernemingen in Nederland** die hun eigen boekhouding doen en een server kunnen (laten) draaien. Denk aan zzp'ers in IT, design, advies of de creatieve sector, en kleine webshops.

| Past goed | Past (nog) niet |
|---|---|
| Eenmanszaak met één administratie | Meerdere administraties of meerdere gebruikers |
| Diensten en verkoop aan klanten in NL, de EU en daarbuiten | Voorraadbeheer of kassasysteem |
| Zakelijke rekening bij bunq | Andere banken (nog geen import, zie [roadmap](#beperkingen-en-roadmap)) |
| Je wilt je data in eigen beheer | Je wilt helemaal niets met servers te maken hebben |

## Snel starten

Je hebt een server met **Docker** nodig en een (sub)domein dat ernaar wijst. Een kleine VPS (2 GB RAM) is genoeg.

```bash
git clone https://github.com/JHVIW/FreeBird.git
cd FreeBird
cp .env.example .env
```

Vul in `.env` de geheimen in:

```bash
openssl rand -base64 48   # → SESSION_SECRET
openssl rand -base64 32   # → APP_ENCRYPTION_KEY  (bewaar deze in je wachtwoordmanager)

# → ADMIN_PASSWORD_HASH_B64 (je inlogwachtwoord, minimaal 12 tekens)
docker run --rm -e PW='een-lang-wachtwoord' node:22-slim sh -c \
  "cd /tmp && npm i -s bcryptjs >/dev/null && node -e \"const b=require('bcryptjs');console.log(Buffer.from(b.hashSync(process.env.PW,12)).toString('base64'))\""
```

Zet `APP_URL` op je eigen domein, pas het domein aan in de `Caddyfile`, en start:

```bash
docker compose up -d --build
```

Caddy regelt automatisch een HTTPS-certificaat. Controleer `https://jouw-domein/api/health`; dat moet `{"ok":true}` geven. Daarna log je in met je wachtwoord.

> [!TIP]
> Eerst rondkijken? Draai FreeBird lokaal met voorbeelddata, zie [Lokaal ontwikkelen](#lokaal-ontwikkelen). Het demobedrijf heet *Studio Zwaluw* en heeft facturen, banktransacties en bonnen over een heel kwartaal.

### Via Coolify

Gebruik `docker-compose.coolify.yml`. Coolify's eigen proxy regelt HTTPS, dus Caddy is daar niet nodig.

1. **DNS:** maak een A-record naar je server. Gebruik je Cloudflare, zet de proxy dan **uit** (*DNS only*). Anders ziet FreeBird de IP's van Cloudflare in plaats van die van bunq, en weigert het de bank-callbacks.
2. **Resource:** nieuwe resource → *Public Repository* → deze repo, branch `main`, build pack **Docker Compose**, compose-locatie `/docker-compose.coolify.yml`.
3. **Domein:** zet bij de service `web` het domein op `https://boekhouding.jouwbedrijf.nl:3000`. De `:3000` vertelt Coolify naar welke containerpoort het moet routeren.
4. **Environment variables:** `APP_URL`, `APP_ENCRYPTION_KEY` en `ADMIN_PASSWORD_HASH_B64` (zie hierboven). Het databasewachtwoord en `SESSION_SECRET` genereert Coolify zelf. Optioneel: `DEEPSEEK_API_KEY`.
5. **Deploy** en controleer `/api/health`.

### Eerste keer inrichten

In de app, onder **Instellingen**:

1. **Bedrijf:** naam, adres, KvK, BTW-id en IBAN. Zonder deze gegevens kun je geen factuur definitief maken.
2. **Algemeen:** kies de startdatum van je administratie, bijvoorbeeld 1 januari. Banktransacties van daarvoor worden niet geïmporteerd.
3. **E-mail:** SMTP en IMAP van je eigen mailbox, en klik op *Verbinding testen*. Maak een map `Bonnen` aan met een mailregel die facturen daarheen verplaatst.
4. **bunq:** maak in de bunq-app een API key aan (Profiel › Beveiliging › Developers) en koppel hem. Vul het vaste IP van je server in; FreeBird registreert zelf de callback.
5. **AI (optioneel):** vul een DeepSeek API key in voor boekvoorstellen en het uitlezen van bonnen.
6. **Beginbalans:** boek via **Journaal** rekening 1000 Bank debet tegen 0900 Ondernemingsvermogen credit, op de startdatum. Zet openstaande debiteuren en crediteuren er ook in.

## Overstappen van Moneybird

FreeBird kan je hele Moneybird-administratie overnemen. Onder **Instellingen › Algemeen** vul je een Moneybird API-token (met leesrechten) en je administratie-id in. Daarna doe je op de pagina **Moneybird** drie stappen:

1. **Ophalen.** Contacten, verkoopfacturen met PDF, inkoopfacturen, bonnen, memoriaalboekingen, bijlagen en grootboekrapporten. Dat gebeurt op de achtergrond binnen de limieten van Moneybird en gaat na een herstart vanzelf verder. Alles komt in een **archief** dat je ook als ZIP kunt downloaden, voor de bewaarplicht van 7 jaar.
2. **Koppelen.** Je kiest bij elke Moneybird-rekening en elk BTW-tarief de bijbehorende FreeBird-rekening. De AI kan voorstellen doen.
3. **Overnemen,** in één transactie:
   - het beginsaldo en de maandtotalen tot de startdatum, zodat je jaaroverzicht compleet is;
   - kwartalen die je al vanuit Moneybird hebt aangegeven, worden vergrendeld;
   - facturen en inkoop die nog openstonden, zodat je betalingen erop kunt koppelen;
   - alles vanaf de startdatum als echte boekingen. Facturen behouden hun nummer en de nummering loopt door.

De overname is ongedaan te maken zolang er geen betalingen aan gekoppeld zijn en je nog geen BTW-periode in FreeBird hebt vergrendeld.

## BTW in het kort

| Situatie | Code | Rubriek |
|---|---|---|
| Klant in Nederland | V21 / V9 | 1a / 1b |
| Bedrijf in de EU met geldig (VIES) BTW-nummer, dienst | ICP_S | 3b + ICP-opgaaf |
| Particulier in een ander EU-land, onder de OSS-drempel | V21 | 1a |
| Particulier in een ander EU-land, boven de drempel | OSS (tarief van dat land) | OSS-aangifte |
| Bedrijf buiten de EU, dienst | NONEU_S | 1e |
| Inkoop met Nederlandse BTW | I21 / I9 | 5b |
| Inkoop van een dienst uit de EU (bijv. hosting) | RC_EU | 4b + 5b |
| Inkoop van een dienst van buiten de EU (bijv. SaaS uit de VS) | RC_NONEU | 4a + 5b |

FreeBird controleert bij het definitief maken van een factuur of OSS van toepassing is. Tarieven en drempels staan per jaar onder **Instellingen › Fiscale parameters**; controleer ze elk jaar in januari.

Indienen doe je zelf in Mijn Belastingdienst Zakelijk. Daarna klik je in FreeBird op *Vergrendel*: de periode gaat op slot en de BTW-saldi gaan naar 1550 *Af te dragen BTW*.

## AI en privacy

Alle AI-functies zijn optioneel en gebruiken [DeepSeek](https://platform.deepseek.com) (model in te stellen met `DEEPSEEK_MODEL`).

| Functie | Waar |
|---|---|
| Boekvoorstel per banktransactie, op basis van je eerdere boekingen | Bank |
| Alles in één keer boeken bij 90%+ zekerheid | Bank |
| Regelvoorstellen voor tegenpartijen die je vaker hetzelfde boekte (zonder AI) | Bank |
| Bonnen uitlezen: foto's via vision, PDF's via hun tekst | Inkoop |
| Mail opstellen om een ontbrekende factuur op te vragen | Inkoop › Ontbrekend |
| Foutcontrole vóór de aangifte | BTW |
| Conceptfactuur uit één zin | Facturen › Nieuw |
| Vragen aan je boekhouding | Vraag het FreeBird |

**Wat er naar de AI gaat:** namen, omschrijvingen, bedragen en het land van een IBAN, nooit de volledige IBAN. Bonnen gaan als afbeelding of tekst mee. Let op: DeepSeek verwerkt data in China. Wil je dat niet, laat de API key dan leeg.

*Vraag het FreeBird* laat de AI een SQL-query schrijven die draait onder een aparte database-rol (`freebird_ai`), in een read-only transactie met een timeout van 5 seconden. Die rol ziet geen instellingen, bestanden, e-mailadressen of IBAN's.

## Achtergrondtaken

De `worker`-container doet het werk dat je niet wilt onthouden:

| Taak | Wanneer |
|---|---|
| Bonnen ophalen uit je mailbox en bounces herkennen | elke 2 minuten |
| bunq-sync (vangnet naast de callback) | elke 15 minuten |
| AI-boekvoorstellen voor nieuwe transacties | elke 15 minuten |
| bunq-sessie vernieuwen en callback controleren | dagelijks 04:00 |
| Matching opnieuw draaien | dagelijks 05:00 |
| Afschrijvingen tot en met vorige maand | dagelijks 06:00 |
| Terugkerende facturen | dagelijks 07:00 |
| Herinneringen | dagelijks 09:00 |

De status van elke taak staat onderaan **Instellingen**.

## Back-ups

De `backup`-container maakt elke dag een `pg_dump` en een archief van alle bestanden in `./backups`, en bewaart ze 30 dagen. Zet deze map ook buiten de server, bijvoorbeeld met `rclone` naar opslag met versiebeheer. Je bent wettelijk verplicht je administratie 7 jaar te bewaren.

Test af en toe of een restore werkt:

```bash
pg_restore -h localhost -U freebird -d freebird_restore backups/freebird-JJJJ-MM-DD.dump
```

## Beveiliging

- Inloggen met één wachtwoord (bcrypt) en een sessiecookie van 30 dagen. Na 5 mislukte pogingen volgt een lockout van 5 minuten.
- API keys en mailwachtwoorden staan versleuteld in de database (AES-256-GCM met `APP_ENCRYPTION_KEY`).
- bunq-verzoeken worden ondertekend en antwoorden geverifieerd. Callbacks worden alleen geaccepteerd vanaf de IP-range van bunq, en de betaling wordt altijd opnieuw opgehaald via de API.
- Draai FreeBird altijd achter HTTPS. De meegeleverde Caddy-configuratie regelt dat.

Een kwetsbaarheid gevonden? Lees [SECURITY.md](SECURITY.md).

## Lokaal ontwikkelen

Je hebt Node.js 22 en PostgreSQL 16 nodig (of start Postgres met Docker).

```bash
npm ci
cp .env.example .env.local        # zet DATABASE_URL naar je lokale database
npm run db:migrate
npm run db:demo                   # alleen op een lege database: voorbeelddata
npm run dev                       # http://localhost:3000
npm run worker                    # achtergrondtaken (optioneel)
npm test                          # draait tegen TEST_DATABASE_URL
```

Schemawijzigingen: pas `src/db/schema.ts` aan, draai `npm run db:generate` en daarna `npm run db:migrate`.

### Techniek

| Laag | Keuze |
|---|---|
| App | Next.js 15 (App Router, server actions), React 19, TypeScript |
| Database | PostgreSQL 16 met Drizzle ORM |
| PDF en e-factuur | `@react-pdf/renderer`, UBL 2.1 / Peppol BIS 3.0 |
| Mail | Nodemailer (SMTP) en ImapFlow (IMAP) |
| Bank | bunq API met ondertekende requests |
| Tests | Vitest tegen een echte Postgres-database |

```
src/
├─ app/            pagina's (app router) en server actions
├─ components/     gedeelde UI
├─ db/             schema, migraties en seed (rekeningschema, BTW-codes)
├─ lib/            boekhoudkern: ledger, BTW, matching, facturen, bunq, AI
└─ worker/         achtergrondtaken
```

### API voor agents

Met `AGENT_API_TOKEN` zet je `/api/agent` aan. Daarmee kan een AI-agent (bijvoorbeeld Claude Code) facturen uploaden, boekingen voorstellen en alleen-lezen-queries draaien. Leeg betekent uit.

## Beperkingen en roadmap

Wat FreeBird nu **niet** doet:

- Eén gebruiker, één administratie, alleen euro's.
- Alleen bunq als bankkoppeling. Andere banken (CSV/CAMT.053-import, PSD2) staan bovenaan de wensenlijst.
- Geen directe indiening bij de Belastingdienst; daarvoor is een PKIoverheid-certificaat nodig. Je neemt de cijfers over in Mijn Belastingdienst Zakelijk.
- De bounce-herkenning voor mails is eenvoudig.

Ideeën en bijdragen zijn welkom, zie [CONTRIBUTING.md](CONTRIBUTING.md).

## Veelgestelde vragen

<details>
<summary><b>Is FreeBird echt gratis?</b></summary>

Ja. De software is gratis en open source onder de AGPL-3.0-licentie. Je betaalt alleen je eigen server (vaak €4 tot €8 per maand) en, als je de AI-functies gebruikt, de API-kosten van DeepSeek. Die blijven voor een kleine onderneming meestal beperkt tot hooguit een paar euro per maand.
</details>

<details>
<summary><b>Accepteert de Belastingdienst een administratie in FreeBird?</b></summary>

De Belastingdienst stelt eisen aan je administratie, niet aan je software: volledig, juist, controleerbaar en 7 jaar bewaard. FreeBird helpt daarbij met dubbel boekhouden, onveranderlijke boekingen, een audit-log, het archiveren van alle bonnen en facturen, en dagelijkse back-ups. Jij blijft verantwoordelijk voor de inhoud en voor het bewaren van de back-ups.
</details>

<details>
<summary><b>Kan mijn boekhouder erbij?</b></summary>

Je kunt het journaal en je facturen exporteren als CSV, en het jaaroverzicht printen of als PDF opslaan. Een aparte account voor je boekhouder is er nog niet.
</details>

<details>
<summary><b>Ik heb geen bunq. Kan ik FreeBird toch gebruiken?</b></summary>

Facturen, inkoop, BTW en het jaaroverzicht werken zonder bankkoppeling. Banktransacties moet je dan wel zelf boeken via het journaal. Een import voor andere banken staat op de roadmap.
</details>

<details>
<summary><b>Wat gebeurt er als ik mijn APP_ENCRYPTION_KEY kwijtraak?</b></summary>

Je boekhouding blijft gewoon werken, maar opgeslagen API keys en mailwachtwoorden zijn dan niet meer te lezen. Die vul je opnieuw in. Bewaar de sleutel in je wachtwoordmanager.
</details>

## Disclaimer

FreeBird is gereedschap, geen fiscaal advies. De BTW-logica volgt de Nederlandse regels zoals die bij het schrijven golden, maar regels en tarieven veranderen. Controleer je aangifte, en schakel bij twijfel een boekhouder of belastingadviseur in. De software wordt geleverd zonder garantie, zie de [licentie](LICENSE).

## Licentie

[GNU Affero General Public License v3.0](LICENSE). Je mag FreeBird gratis gebruiken, aanpassen en delen. Bied je een aangepaste versie aan als online dienst, dan moet je de broncode van die versie ook delen. Zo blijft FreeBird vrij voor iedereen.

<p align="center">
  <br>
  <img src="docs/assets/logo.svg" alt="" width="40"><br>
  <sub>Gemaakt in Nederland, voor ondernemers die liever ondernemen dan administreren.</sub>
</p>
