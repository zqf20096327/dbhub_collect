# Database Doctor

[![Validate](https://github.com/Clahen86/ha-database-doctor/actions/workflows/validate.yml/badge.svg)](https://github.com/Clahen86/ha-database-doctor/actions/workflows/validate.yml)

**Keeps your Home Assistant database small and correct: see what fills it – every entity, not just energy – clean up safely, and keep it from growing back. Plus wrong numbers in the energy dashboard fixed with one tap.**

> Called *Energy Doctor* before 0.8.

[English](#english) · [Dansk](#dansk)

## English

Home Assistant records everything, and two things go wrong over time: a meter that resets or drops out puts absurd numbers in the energy dashboard, and the database keeps growing until Home Assistant starts and backs up slowly. Database Doctor adds a panel to the sidebar that finds both, explains them in plain words and fixes them – only with Home Assistant's own functions, and nothing that something uses is ever touched.

### Overview

<p><img src="docs/panel-overview.png" alt="Overview: what fills the database, a suggestion, save less often, size over time and a health check" width="300"></p>

- **What fills the database** by group, how fast it grows and when the disk is full.
- **One suggestion** with how much it saves, e.g. history of devices that are gone and old history that nothing uses.
- **Size over time** with a forecast: doing nothing vs. after *Optimise*.
- **Health check:** the database on an SD card, a database so big that starting is slow, the recorder's settings and the last backup.
- **Explain with AI (optional):** pick an AI task entity under *Configure*, and the panel explains your database in plain words.

### Wrong numbers in Energy

<p><img src="docs/panel-energy.png" alt="Energy: spikes, gaps, statistics warnings and use no device explains" width="300"></p>

- **Spikes and negative hours** are set to what is normal for that meter, with Home Assistant's own *Adjust sum*. The price of the same hour is fixed with it, and the panel says why the meter jumped (it was unavailable or went to 0).
- **Gaps:** when a meter was offline and everything came at once, the use is spread over the missing hours.
- **Statistics warnings** that Home Assistant shows under *Statistics* (unit changed, entity gone …) in one place, fixed with its own functions.
- **Use no device explains:** how much of your grid use the devices in Energy explain, with energy meters you can add in one tap.
- **A watch** checks twice a day and tells you about new wrong numbers. Every fix can be undone.

### What takes up the most

<p><img src="docs/panel-data.png" alt="Data: what takes up the most, per device, with where it is used" width="300"></p>

One row per device, with a clear status – *History used – keep*, *Used – only its value*, *Can be cleaned*, *Saves a lot* or *Deleted* – and one button that does the right thing. Tap a row to see each entity, how often it saves and where it is used: automations, scripts, scenes, graphs, dashboards, the energy dashboard, helpers and your YAML files. Filter and search when the list is long.

Database Doctor reads how each entity is used, not just where its name appears: the YAML configuration is loaded the way Home Assistant loads it (with `!include` and packages), and only what really reads the history – graphs, the energy dashboard, `statistics`, `history_stats` and `filter` sensors, and code like AppDaemon's `get_history` – keeps the history. Automations and templates only need the value now, so their old history can go. Code in add-ons that Home Assistant can't read (for example AppDaemon on Home Assistant OS) is pointed out, and **Never touch** keeps any entity out of every suggestion. Apps (add-ons) that name sensors in their own settings files – Energy Pilot, Predbat, EMHASS and others – keep those sensors' history too; an app can also list what it reads in a small JSON file in its folder.

**Stop saving** with one tap: for Zigbee2MQTT devices the value is stopped at its source (Zigbee2MQTT's own *filtered_attributes*), so nothing new is recorded and the entity keeps its last value.

### Save less often

<p><img src="docs/panel-settings.png" alt="Settings: save less often, profiles, how long details are kept" width="300"></p>

- **Profiles for the whole house** – Sparse, Balanced, Detailed – or three levels per group: temperature and climate, energy meters, other sensors. Or a level per device, or *Never touch*.
- It uses Zigbee2MQTT's own *throttle* option, **only on devices with nothing but sensors**. Lights, plugs, buttons (also remotes with only battery and signal sensors), motion and door sensors are never slowed down, and anything an automation or graph uses never goes below Normal. *Why not these?* lists the devices it leaves alone and why.
- **New devices** get the same automatically, and unused signal-strength (linkquality) entities can be switched off.
- **How long details are kept**, per group: e.g. 3 days of second-by-second detail – graphs and hourly statistics always stay.
- **Stop saving** an entity: Database Doctor never changes your YAML, so it collects the lines for `configuration.yaml` for you to copy.

### Safe by design

- Data is only changed with the recorder's own functions (*Adjust sum*, import of statistics, purge) – never raw SQL. The database is otherwise only read, in a read-only session, to count what fills it.
- Fixes and changes of how often devices save can be undone. A clean-up can't, so it offers Home Assistant's own backup first.
- An entity that is gone but still used somewhere (an old meter in the energy dashboard, a paused AppDaemon app's sensor) is never offered for clean-up, and statistics the energy dashboard shows are never removed.
- **Make the file smaller** runs by itself after a clean-up only on SQLite. On MariaDB and PostgreSQL it locks the tables for a while and needs as much free space as they take, so there you start it when it suits you. Free disk space is only shown when the database is on Home Assistant's own machine.
- Your YAML files are never written.

### Help and answers

Press **🛟 Help** at the top of the panel to write what's wrong and attach up to 3 pictures. It goes privately to the developer with a short diagnosis (no names, addresses or passwords) – only when you press *Send*. When the developer answers – also on an error the app reported – the answer shows under 🛟 Help with a notification in Home Assistant, and you can write back. Errors in the app are sent anonymously so they can be fixed; turn it off under 🛟 Help. With it, once a day, how it is set up goes along – the database engine, its size in rough steps, how long history is kept and which integrations write the most – with no names or entity IDs; the full entity names only if you turn on *Share my setup* under 🛟 Help.

## Installation

1. HACS → search for **Database Doctor** → Download. (Not in HACS yet? Add `https://github.com/Clahen86/ha-database-doctor` as a custom repository of type *Integration*.)
2. Restart Home Assistant.
3. Settings → Devices & services → Add integration → **Database Doctor**.
4. Open **Database Doctor** in the sidebar.

Languages: English, Danish, German, Swedish, Dutch and French. Early version – feedback is welcome in [issues](https://github.com/Clahen86/ha-database-doctor/issues).

---

## Dansk

**Holder din Home Assistant-database lille og korrekt: se hvad der fylder – alle entiteter, ikke kun energi – ryd sikkert op, og hold den fra at vokse igen. Og forkerte tal i Energi-dashboardet rettes med ét tryk.**

Home Assistant gemmer alt, og med tiden går to ting galt: en måler, der nulstilles eller falder ud, giver skøre tal i Energi, og databasen vokser, til opstart og backup bliver langsomme. Database-doktor er et panel i sidemenuen, der finder begge dele, forklarer dem med almindelige ord og retter dem – kun med Home Assistants egne funktioner, og det, der bruges, røres aldrig.

### Overblik

<p><img src="docs/panel-overview.png" alt="Overblik" width="300"></p>

Hvad der fylder, hvor hurtigt det vokser, og hvornår disken er fuld. Ét forslag med, hvor meget det sparer, en graf med prognose (uden at gøre noget og efter *Optimer*) og et sundhedstjek. Vælger du en AI under *Konfigurer*, kan panelet forklare din database.

### Fejl i Energi

<p><img src="docs/panel-energy.png" alt="Energi" width="300"></p>

Spring og negative timer sættes til det normale for måleren med Home Assistants egen *Juster sum*, og prisen for samme time rettes med. Huller, hvor en måler var væk, fordeles over de manglende timer. Home Assistants statistik-advarsler samles ét sted, og du ser, hvor meget af forbruget enhederne i Energi forklarer. En vagt giver besked om nye fejl. Alt kan fortrydes.

### Fylder mest

<p><img src="docs/panel-data.png" alt="Data" width="300"></p>

Én linje pr. enhed med en klar status og én knap, der gør det rigtige. Tryk på en linje for at se hver entitet, hvor tit den gemmer, og hvor den bruges.

### Gem sjældnere

<p><img src="docs/panel-settings.png" alt="Indstillinger" width="300"></p>

Profiler for hele huset eller niveau pr. gruppe og pr. enhed via Zigbee2MQTTs egen *throttle* – kun på enheder med rene sensorer. Lys, stik, knapper (også fjernbetjeninger med kun batteri- og signalsensorer), bevægelses- og dørsensorer sættes aldrig ned, og det, der bruges – også af en automation, selv om sensoren ikke gemmes – kommer aldrig under Normal. Nye enheder får det samme. Du vælger også, hvor længe detaljerne gemmes, mens grafer og timeværdier altid bliver.

### Sikker

- Slettede enheder, der stadig bruges et sted (fx en gammel måler i Energi), foreslås aldrig ryddet, og statistik, Energi-dashboardet viser, slettes aldrig.
- **Gør filen mindre** kører kun af sig selv på SQLite. På MariaDB og PostgreSQL låser det tabellerne et stykke tid og kræver lige så meget fri plads, så dér starter du det selv.

### Installation

1. HACS → søg efter **Database Doctor** → Download. (Ikke i HACS endnu? Tilføj `https://github.com/Clahen86/ha-database-doctor` som brugerdefineret repository af typen *Integration*.)
2. Genstart Home Assistant.
3. Indstillinger → Enheder og tjenester → Tilføj integration → **Database Doctor**.
4. Åbn **Database-doktor** i sidemenuen.

### Hjælp og svar

Tryk på **🛟 Hjælp** øverst i panelet for at skrive, hvad der er galt, og vedhæfte op til 3 billeder. Det går privat til udvikleren med en kort diagnose (ingen navne, adresser eller koder) – kun når du trykker *Send*. Når udvikleren svarer – også på en fejl, appen har sendt – står svaret under 🛟 Hjælp, og du får en besked i Home Assistant. Du kan skrive tilbage derfra. Fejl i appen sendes anonymt, så de kan blive rettet; slå det fra under 🛟 Hjælp. Med det sendes én gang om dagen også, hvordan den er sat op – databasetypen, størrelsen i grove trin, hvor længe historikken gemmes, og hvilke integrationer der skriver mest – uden navne eller entity-id'er; de fulde entity-navne kun hvis du slår *Del min opsætning* til under 🛟 Hjælp.
