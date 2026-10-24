# Vacancely

[![CI](https://github.com/Blaums/vacancely/actions/workflows/ci.yml/badge.svg)](https://github.com/Blaums/vacancely/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Self-hosted job board harvester + AI evaluator — crawl job boards, score every posting against **your own CV**, and review the results in a multi-user dashboard.

Self-hosted job harvester + AI evaluator. It crawls job boards, prefilters
postings, scores them against **your own CV** with an LLM, keeps a per-profile
job database, and ships a web dashboard to review results, labels and skill
gaps.

Each account owns its own profiles; profiles, jobs, rules and golden sets are
isolated per profile.

![Vacancely dashboard — every posting scored against the profile's CV](docs/dashboard.png)

![Skills gap — which skills the market asks for that your CV lacks, with the evidence behind each](docs/skills.png)

## Features

- **Harvesting** — JSON APIs, HTML boards and JS-rendered pages (Playwright),
  with per-domain crawl strategies that improve over time.
- **Two-stage filtering** — keyword/rule prefilter, then embeddings (fastembed)
  + LLM scoring (any OpenAI-compatible API; DeepSeek by default).
- **Per-profile evaluation** — CV, target role, location, keywords, languages
  and rules all belong to the profile, not to the app.
- **Dashboard** — jobs, applications, sources, rules, CV editor, settings,
  multi-user login.
- **Skill-gap analysis** — which skills the market asks for that your CV lacks.
- **Self-improvement loop** — proposes changes to `improvable.py` and validates
  them against a labelled *golden set* before promoting anything.
- **Async workers** — Celery + Redis for background harvests.
- **Typed, linted, tested** — `ruff` (E/F/W/I/UP) and a `pytest` suite on the
  pure functions run in CI on every push.

## Quick start (Docker)

```bash
cp .env.example .env          # then fill in DEEPSEEK_API_KEY + secrets
docker compose up -d --build
```

Open http://localhost:5000, register an account and create a profile.
The schema is created automatically on first boot.

Required in `.env`:

| Variable | Meaning |
|---|---|
| `DEEPSEEK_API_KEY` | API key for the OpenAI-compatible provider |
| `DEEPSEEK_BASE_URL` / `DEEPSEEK_MODEL` | optional overrides |
| `ENCRYPTION_KEY` | Fernet key used to encrypt stored provider keys |
| `SESSION_SECRET` | long random string, signs the session cookie |
| `POSTGRES_*` | DB credentials used by `docker-compose.yml` |
| `LOG_LEVEL` | optional; `INFO` by default, `DEBUG`/`WARNING` to taste |

Generate secrets:

```bash
python -c "import base64,os;print(base64.urlsafe_b64encode(os.urandom(32)).decode())"  # ENCRYPTION_KEY
python -c "import secrets;print(secrets.token_urlsafe(32))"                            # SESSION_SECRET
```

## Run without Docker

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
cp .env.example .env          # set DATABASE_URL + REDIS_URL to your local services
python run.py --dashboard
```

## Commands

```bash
python run.py                     # one harvest + evaluation run
python run.py --dashboard         # start the Flask dashboard
python run.py --create-golden-set # seed a golden set from your harvested history
python run.py --golden-coverage   # show language/role coverage gaps
python run.py --test-golden-set   # evaluate the current pipeline against it
python run.py --self-improve      # propose + validate an improvement
python run.py --load-golden examples/golden_set_security_engineer.json --profile-id 1
```

## Golden sets

A golden set is a small labelled regression suite (public postings only) used by
`--self-improve`. `examples/golden_set_security_engineer.json` is a ready-made
example for security-engineer roles — import it and adjust the labels, or build
your own from your own harvest history. See `examples/README.md`.

## Project layout

```
core/      harvesting, fetching, AI evaluation, embeddings, crawler strategies
modes/     harvest flow, golden-set testing, self-improvement
storage/   SQLAlchemy models, repositories, schema bootstrap
web/       Flask app factory (app.py), blueprints (routes/), static frontend
tests/     pytest suite for the pure functions
examples/  example golden set
```

## Development

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
pip install pytest ruff

ruff check .          # lint
python -m pytest -q   # unit tests (no DB, no network)
```

CI (`.gitlab-ci.yml`) runs the same two commands on every push. The tests cover
only side-effect-free helpers deliberately: salary parsing, normalization,
prompt-injection/SSRF guards, strategy validation and AI-JSON parsing.

## Security notes

- `.env`, `cv_active.json` and `runtime/` are git-ignored; never commit them.
- API keys stored through the UI are encrypted with `ENCRYPTION_KEY`. Changing
  that key makes previously stored keys unreadable.
- The dashboard uses password auth with per-user profiles; run it behind a
  reverse proxy with TLS if it is exposed beyond localhost. Set
  `COOKIE_SECURE=1` there: it marks the session cookie `Secure` and enables
  HSTS. Login attempts are throttled to 10 failures per username+IP per 15
  minutes.
- The container runs as uid 10001 with `no-new-privileges`. Chromium needs
  `--no-sandbox` inside the container, so never run the image as root.
- Postgres and Redis are **not** published on the host by default; use
  `docker-compose.override.yml.example` if you need `psql` from your machine.

## Author

Built by [Blaums](https://github.com/Blaums) — [LinkedIn](https://www.linkedin.com/in/rihard/).

## License

Released under the [MIT License](LICENSE) © 2026 Rihards Jānis Blaums.
