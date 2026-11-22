<p align="center">
  <img src="docs/images/banner.png" alt="Fit-OS: a gym coach in a WhatsApp group, with a dashboard for progress and lab results" width="100%">
</p>

# 💪 Fit-OS

![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-HTMX-009688?logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-WAL-003B57?logo=sqlite&logoColor=white)
![WhatsApp](https://img.shields.io/badge/WhatsApp-WAHA-25D366?logo=whatsapp&logoColor=white)
![Claude](https://img.shields.io/badge/Claude-optional-D97757?logo=anthropic&logoColor=white)
![Docker Compose](https://img.shields.io/badge/Docker-amd64%20%7C%20arm64-2496ED?logo=docker&logoColor=white)

A self-hosted personal trainer that lives in a WhatsApp group.

You open WhatsApp at the gym and it tells you what to train today. You type `8x72.5` after each set and it
logs it, tells you when you beat a record, and works out next week's weights. When the bench is taken you
type `ocupada` and it gives you the best substitute you can do with what's around you. A web dashboard
shows the long view: strength curves, weekly volume per muscle, body weight, and every blood test you've had
plotted against the reference ranges for your sex and age.

<p align="center">
  <img src="docs/images/today.png" alt="Today tab: the proposed session with targets per exercise, the week strip, hard sets per muscle and recent records" width="100%">
</p>

## Why

Gym apps want you to tap through screens with sweaty hands, sell you a subscription, and keep your
health data. What actually helps between sets is much smaller: *what's next, how much, and did I do better
than last time*. WhatsApp is already open on your phone, so Fit-OS lives there and asks for nothing but a
line of text per set.

It also needed to be honest about numbers. Progression, estimated 1RM, records, volume and lab status are
computed by plain, tested code. An AI coach (Claude) is an **optional** layer on top: it explains, answers
questions and adjusts plans, but it can only change your data through validated tools, and with it off the
app works fully.

And it runs at home: a mini PC, a Raspberry Pi or any small server, with your lab results and training log
in a SQLite file you own and encrypted backups only you can open.

## Features

**In the WhatsApp group**
- **Today's session** every morning, built from your program, schedule and the equipment at today's place
  (gym, home dumbbells, hotel…). Reply `1` to start, `2` to change place, `3` for another focus, `4` to rest.
- **Set logging** in free text: `10x40`, `8x72.5 r2`, `3 sets of 10 at 40`, `10x50lb`, `12 bw`, `to failure`, RPE.
- **Progressive overload** by double progression with RIR autoregulation, rounded to the weights you
  actually own; 🏆 on new estimated-1RM, weight or rep records.
- **Swaps on the spot**: `busy`, `another`, `no barbell` (or `ocupada`, `otra`, `no tengo barra`), ranked by
  movement pattern, muscle, equipment, injuries and load.
- **Exercise videos**: each card comes with the exercise animation as a short video; `video` and `how`
  on demand.
- Session summary with tonnage, PRs and what goes up next time; nudges if you go quiet; quiet hours.

**In the dashboard**
- **Train**: build today's workout on the web (the program's next day, or muscle groups like "chest +
  shoulders"; at the gym or at home; "no barbell today"), suggested or at random, swap or reroll any exercise,
  add or remove, then log every set with a rest timer. Works without WhatsApp and for days without signal.
- **Today**, **Workouts**, **Progress** (e1RM curves, body weight, weekly sets per muscle against a 10–20
  band, streaks), **Exercises** (a bank of 1,300+ with animations and your history on each).
- **Labs**: 29 biomarkers with reference ranges by sex and age, your own stricter goals, status per value,
  and an import that flags ambiguous values for review instead of guessing.
- **Profile** (goal, days, times, injuries, equipment per place) and **Settings** (morning plan, quiet
  hours, rest timers, RIR target, program template).
- **Coach** chat with Claude when enabled, with a daily budget; **Integrations** placeholders for Whoop,
  Apple Health and Garmin.

<table>
  <tr>
    <td><img src="docs/images/progress.png" alt="Progress: weekly hard sets per muscle, estimated 1RM curve, consistency and body weight"></td>
    <td><img src="docs/images/labs.png" alt="Labs overview: each biomarker with its latest value, status and trend"></td>
  </tr>
  <tr>
    <td align="center"><sub>Progress: weekly volume per muscle, e1RM, streak, body weight</sub></td>
    <td align="center"><sub>Labs: latest value, status and trend per marker</sub></td>
  </tr>
</table>

<p align="center">
  <img src="docs/images/lab-detail.png" alt="LDL detail: values over time against the reference band, value table, foods for and against" width="100%">
  <br><sub>A marker over time against the range for your sex and age, with food notes. All screenshots use synthetic demo data.</sub>
</p>

**Under the hood**
- **English and Spanish**: the dashboard and the bot speak your language (Settings), and the group
  understands commands in both, so `8x72.5 r2`, `busy` or `ocupada` all work.
- **Several people on one server**: each person has their own database and sees only their own data; an admin
  manages accounts and can look at anyone's dashboard read-only.
- One container, SQLite, ~100 MB of RAM; runs on amd64 and arm64.
- HTTPS + password through a Caddy sidecar; WhatsApp through your own or a shared
  [WAHA](https://waha.devlike.pro/); HMAC-signed webhooks; every chat that isn't the group is dropped
  before it's stored.
- Deploy, rollback and age-encrypted backups with one `make` command each, to any host over ssh.

## Quick start

Try it on your laptop with fake WhatsApp and synthetic data (Docker required, no keys):

```bash
git clone <repo-url> Fit-OS && cd Fit-OS
make dev          # http://localhost:8090
make catalog      # downloads the exercise dataset, converts the animations (~10 min)
make demo         # ~10 weeks of synthetic training, body weight and labs
```

Then open http://localhost:8090, and http://localhost:8090/dev/wa to play the WhatsApp side (`hoy`, `1`,
`10x40`, `busy`, `finish`).

To run it for real (a server, your WhatsApp number, a dashboard password), follow [setup](docs/setup.md).
It takes about fifteen minutes plus the one-time media conversion.

## Documentation

- [Setup](docs/setup.md): local try-out, a real install, connecting WhatsApp, your data, the optional coach,
  configuration reference, troubleshooting.
- [Usage](docs/usage.md): a training day in the group, every command, how the numbers are decided, the
  dashboard tabs, lab results.
- [Deployment](docs/deployment.md): deploying to any host, rollback, dashboard access, sharing WAHA,
  encrypted backups.
- [Architecture](docs/architecture.md): modules, the WhatsApp pipeline, scheduler, data, security model.
- [Development](docs/development.md): tests, migrations, the WhatsApp simulator, screenshots.
- [Design](docs/design.md) and [research](docs/research.md): the original plan and the reasoning behind it.

## Status

Phases 0 and 1 are built and deployed: WhatsApp loop, planning, logging, progression, substitutions,
exercise bank, labs, progress and the coach, in English and Spanish. Next: wearable integrations (Whoop,
Apple Health, Garmin) and nutrition logging.

## Contributing

Bug reports, ideas and pull requests are welcome. [CONTRIBUTING.md](CONTRIBUTING.md) explains how to set up
the project, run the tests, and the conventions the code follows.

## License

The code is released under the [MIT License](LICENSE). [CREDITS.md](CREDITS.md) lists every third-party
component and its license, the exercise media terms, and the scientific and clinical references behind the
numbers.

The exercise data comes from [hasaneyldrm/exercises-dataset](https://github.com/hasaneyldrm/exercises-dataset)
(MIT). The exercise animations are **© Gym visual** (https://gymvisual.com/), redistributed by that dataset
with attribution; they are downloaded when you import the catalog, are not stored in this repository, and
are for your own private use (see [CREDITS.md](CREDITS.md)). The screenshots hide them.
See [catalog/NOTICE.md](catalog/NOTICE.md). Fit-OS is not medical advice: lab ranges are references, and
your lab's printed range and your doctor come first.
