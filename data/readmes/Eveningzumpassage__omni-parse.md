### Telegram-бот: кнопки, канал, формат

```bash
set OMNI_BOT_TOKEN=<токен BotFather>      # .bot_token, в git не попадает
set OMNI_BOT_OWNERS=<твой numeric id>     # кому отвечает, можно несколько через запятую
python -m omni.bot
```

Экран бота — инлайн-кнопки: `Лента`, `Абузы`, `Источники`, `Цифры`, теги `Промо / Триалы / Сливы`, `Подписка: вкл/выкл`, `Формат: кратко/полно`, `Пост в канал`.

Команды: `/new [N]`, `/abuse [тег]`, `/find <слово>`, `/src <слово>`, `/run <категория>`, `/add <url>`, `/auto [N]`, `/stats`, `/sub [@канал]`, `/unsub [@канал]`, `/subs`, `/post [@канал]`.

**Постинг в канал.** Добавь бота админом канала с правом публикации и отправь `/sub @твойканал` — бот каждые 5 минут проверяет новые абузы и публикует только те, что появились после подписки. `/post @твойканал` — опубликовать подборку сразу, `/unsub @твойканал` — остановить. Дальше можно подключить свой бот: код один, токен свой, база общая.

**Формат текста.** `кратко` — заголовок, источник, тег. `полно` — плюс ссылка на запись. Переключается кнопкой и хранится на чат/канал: канал можно держать в одном формате, личку — в другом.

**Про ключи не публикуем.** Тег `keys` отфильтрован на уровне бота (`HIDE_TAGS` в `omni/bot.py`): записи, у которых после фильтра не осталось тегов, не попадают ни в `/abuse`, ни в автопостинг.

# omni-parse

Один парсер под любую тему: Reddit, форумы, поисковики, X/Twitter, карточки товаров и платные search-API — в одну SQLite-базу с FTS5, дедупом и рейтингом.

Ставится без ключей. Платные провайдеры включаются сами, если в окружении есть ключ.

## Состояние на сейчас

- **источников: 869** в 11 категориях (662 базовых + 207 из реестра абузов + 19 Telegram-каналов, дубли вырезаны), **записей в базе: 9889** (421 с ценой, 120 прогонов), из них 3135 из реестра абузов и 2966 из Telegram (превью + своя сессия)
- **типы записей: 14** — каждая запись размечена по смыслу: новость 3693 · софт 516 · уязвимость 402 · релиз 361 · модель 331 · вопрос 265 · цена 205 · гайд 194 · датасет 126 · слив 90 · триал 41 · промо 34 · вакансия 21 · перепродажа 10
- **X/Twitter: 30 аккаунтов** читаются без API-ключей через `api.fxtwitter.com` (313 твитов в базе)
- вкладки панели: `Лента` · `Источники` · `Прогоны` · `Абузы`; полоса чипов «тип», фильтр «только с ценой», сортировка `score/fresh/price`, экспорт CSV
- health-аудит: живой/мёртвый/непроверенный по каждому источнику, причина в примечании
- Telegram-бот на той же базе: `/new`, `/abuse`, `/find`, `/src`, `/run`, `/add`, `/auto`, `/sum`, `/tr`, `/stats`
- тесты: `tests/test_regress.py` — 16 проверок на те же баги, что ловило ревью; CI: `.github/workflows/ci.yml` (py3.10/3.11/3.12)
- автоаудит: `tools/selfcheck.py` обновляет `REPORT.md` и гоняет тесты, `tools/autocommit.sh` коммитит и пушит в Gitea + GitHub

| категория | источников |
|---|---|
| `company` | 135 |
| `community` | 131 |
| `security` | 99 |
| `papers` | 72 |
| `forum` | 57 |
| `models` | 40 |
| `abuse` | 40 |
| `company_cn` | 34 |
| `release` | 30 |
| `benchmark` | 16 |
| `company_kr` | 11 |

## Панель

```bash
python -m omni serve --port 8077
# http://127.0.0.1:8077/?view=abuse
```

`?view=feed|src|runs|abuse`, горячие клавиши `1..4`, палитра `Ctrl K`, категории в URL (`?cat=`), кнопка «авто-добавление» ищет новые фиды на уже подключённых хостах и сохраняет только те, что реально отдали записи.

## Что умеет

| Провайдер | Что тянет | Ключ |
|---|---|---|
| `reddit` | поиск по постам и комментариям через api.pullpush.io (архив Reddit) + публичный json как запас | нет |
| `forums` | Discourse (9 инстансов), Hacker News (Algolia), Lobsters, XenForo, веб-версии Telegram-каналов | нет |
| `ddg` | html-выдача DuckDuckGo | нет |
| `bing` | html-выдача Bing, ссылки раскодируются из `ck/a?...u=a1<base64url>` | нет |
| `mojeek` | html Mojeek (свой индекс, без капчи) | нет |
| `x` | без платного API: oembed по URL твита, syndication-таймлайн профиля, поиск твитов через ddg/bing/mojeek | нет |
| `tavily` | Tavily search | `TAVILY_API_KEY` |
| `exa` | Exa search + текст страниц | `EXA_API_KEY` |
| `you` | You.com search | `YOU_API_KEY` |
| `firecrawl` | Firecrawl search | `FIRECRAWL_API_KEY` |
| `cards` | карточки товаров: JSON-LD Product/Offer, OpenGraph, microdata, цена/валюта/наличие | нет |
| `treg` | treg-поиск | `TREG_TOKEN` |
| `feed` | обход реестра из 450 лент/API без запроса (см. ниже) | нет |

`python -m omni providers` печатает, что реально поднялось в этом окружении.

## Что было сломано и что стало (по ревью)

Отдельный заход по Telegram: адаптер `tg_web` тянул в базу `Channel created`,
`Channel photo updated` и посты из одной ссылки — 150 мусорных записей из 285.
После переписывания: 0 служебных, заголовки из тела поста
(`СЛИВ: 1300+ АККАУНТОВ ДЛЯ ВАС!` вместо `🛑`); чистка старых — `tools/purge_tg_junk.py --apply`,
обновление заголовков без перезаписи базы — `tools/fixtg.py`.
Скор получил сигнал абуза (`omni/rank.py`, `ABUSE_TERMS`): утечки, CVE, эксплойты, комбо-листы,
сливы ключей и аккаунтов дают до +1.8 — топ базы теперь инциденты, а не релизы.
Пересчёт существующих записей — `tools/rescore.py --apply`.

Замеры сняты на этой машине, до и после правок. Скепсис к ревью тоже был: два пункта не подтвердились, они отмечены.

| пункт | было | стало |
|---|---|---|
| `/run` в боте | `new += store.add(items)` → `TypeError`, команда падала всегда | `n_new, _dup = store.add(items)`; прогон отдаёт `готово: собрано 1, новых 1` |
| параметры API | `?limit=-1` → вся база (SQLite `LIMIT -1`), `?limit=abc` → трейс и обрыв | `limit=-1` → 1 строка, `abc` → 40, `99999` → 200 (HTTP 200 во всех трёх) |
| соединения SQLite | `with conn()` коммитит без `close()`: 200 вызовов → +76 хендлов | `with db()` (commit/rollback/close): 200 вызовов → +0 |
| троттлинг | 24 вызова на хост при 0.3с проходили за 0.9с вместо 6.9с | слот резервируется до сна, тест держит паузу и в 6 потоков |
| владелец бота | пустой `OMNI_BOT_OWNERS` → владельцем становился первый написавший | без env бот в read-only: `/new /abuse /find /src /stats`, мутации отбиваются |
| мёртвый `abuse_sources.py` | 237 строк, 0 импортов | подключён: +191 источник категории `abuse` (31 дубль отсеян по url) |
| дубли реестра | дубли по url | `all_sources()` дедуплицирует: 853 источника = 853 уникальных url |
| `JOBS` в панели | рос без границ, 500 запусков → 500 записей | eviction до 300 при переходе через 400 |
| `push_new` | уходили самые старые записи окна (`fresh[-per_chat:]`) | уходят самые свежие (`fresh[:per_chat]`) |
| `ai.py` | `sleep(1.5 + attempt)` и после последней попытки | спит только перед повтором |

Что из ревью не подтвердилось: `rank.py` не мёртвый — его зовёт `cli.py` в трёх местах; дублей в реестре был один, а не 38 (на старой базе ревью их было больше). `except Exception` осталось 59 на ~5000 строк: часть глушит сетевые парсеры осознанно, но в панели ни один запрос больше не отдаёт трейс — параметры валидируются до вызова.

## Установка

```bash
pip install -r requirements.txt
cp .env.example .env   # ключи по желанию, ни один не обязателен
```

## Быстрый старт

```bash
# что доступно
python -m omni providers

# поиск по одной теме в четырёх бесплатных источниках
python -m omni search "scraping twitter without api" --providers reddit,forums,ddg,bing --limit 12 --show 10

# реестр источников: сколько и каких
python -m omni sources
python -m omni sources --category papers,security --list

# обход реестра БЕЗ запроса: 589 источников -> база
python -m omni feed --category community --limit 8
python -m omni feed --limit 15            # всё подряд
python -m omni feed --only arxiv_cs_ai,hn_top,reddit_localllama

# прогон по списку тем из themes.txt (по теме на строку)
python -m omni fanout --providers reddit,forums,ddg,bing --limit 10

# топ базы, статистика, поиск по своей базе
python -m omni top --limit 20
python -m omni stats
python -m omni find "proxy"

# карточки товаров по URL
python -m omni cards https://example.com/product

# выгрузка
python -m omni export --format jsonl --out data/dump.jsonl
```

## Реестр источников

`omni/sources.py` + `omni/sources_ext.py` — **589 источников в 9 категориях**, у каждого свой адаптер и флаг вкл/выкл:

- **papers 49** — arxiv по 25+ разделам (cs.AI/LG/CL/CV/RO/IR/CR/SE/NE/MA/DC/DB/HC/SD/CY, stat.ML, eess.AS/SP/IV, math.OC, q-bio.NC, cs.GR, cs.AR, cs.PF), HF daily papers, OpenAlex, Semantic Scholar, Papers with Code, Connected Papers
- **company 95** — ленты OpenAI, Google AI/Research/DeepMind, Microsoft Research, NVIDIA, Apple ML, Amazon Science, HF, Meta AI, Mistral, Cohere, Together, Perplexity, Groq, Cerebras, Stability, Databricks, Anyscale, Modal, W&B, LangChain, LlamaIndex, vLLM, Replicate, Fireworks, SambaNova, Scale, xAI, Salesforce, AWS ML, Azure AI, Anthropic, AI2, EleutherAI, LAION, Runway, ElevenLabs, Deepgram, AssemblyAI, Pinecone, Weaviate, Qdrant, Chroma, Unsloth, Axolotl
- **company_cn 31** — Qwen, DeepSeek changelog, Moonshot, Zhipu, Baichuan, MiniMax, StepFun, 01.AI, InternLM, ChatGLM + GitHub-орги Tencent-Hunyuan, PaddlePaddle, bytedance, mindspore-ai, QwenLM, deepseek-ai, MoonshotAI, THUDM, OpenBMB, Shanghai-AI-Lab
- **company_kr 10** — Kakao tech, Naver Cloud/D2, Samsung Research, LG AI Research, Upstage, Rebellions, Twelve Labs, FriendliAI
- **community 49** — HN top/new/ask/show, Lobsters (4 тега), GeekNews, Reddit: LocalLLaMA, OpenAI, singularity, MachineLearning, deeplearning, netsec, programming, rust, golang, Python, webdev, selfhosted, devops, datascience, androiddev, javascript, linux, experienced_devs
- **security 45** — THN, BleepingComputer, Krebs, SANS ISC, Packet Storm, CISA advisories + CISA KEV (JSON), NVD CVE (JSON), Exploit-DB, Project Zero, PortSwigger, GitHub Security, Rapid7, Qualys, Tenable, CrowdStrike, SentinelOne, Unit42, Talos, Securelist, WeLiveSecurity, Malwarebytes, Schneier, Graham Cluley, HackerOne hacktivity, Bugcrowd, Intigriti, YesWeHack, CTFtime, OWASP, SANS diaries, Risky Business, tl;dr sec, Detection Engineering
- **forum 31** — 10 Discourse-инстансов (discuss.python, community.openai, forum.cursor, discuss.huggingface, forum.obsidian, community.cloudflare, discuss.elastic, forum.gitlab, community.home-assistant, discuss.grafana), XenForo BHW, веб-версии Telegram-каналов (durov, telegram, AI-каналы), Stack Overflow tags, Reddit-миграции
- **models 18** — HF trending/new (модели, спейсы, датасеты), HF по 6 пайплайн-тегам, Ollama library + search, LM Studio catalog, OpenRouter models + pricing (JSON), Civitai, Replicate explore
- **benchmark 10** — Open LLM Leaderboard, LMArena, Artificial Analysis, Epoch AI, SWE-bench, LiveBench, HELM, MTEB, BigCodeBench, Chatbot Arena

Адаптеры: `rss`, `generic_json`, `or_models`, `cisa_kev`, `nvd`, `json` (HF, HN, OpenAlex, S2, Discourse), `html` (список + детальная), `github_org`. Медленные хосты (reddit, github, HF, arxiv, openrouter) обходятся последовательно с паузой, остальные — в 8 потоков. Для arxiv RSS, который часто отдаёт пустое, есть fallback на официальный API (`export.arxiv.org/api/query`).

## Панель и команды

```
python -m omni serve --port 8077      # веб-панель + JSON API (без сборки, без npm)
python -m omni feed --limit 10        # обход всего реестра
python -m omni doctor --fix           # проверить источники и подобрать рабочие фиды
python -m omni digest --out data/digest.md
```

Панель — две вкладки:

1. **лента** — счётчики (записей, с ценой, прогонов, источников, включённых), поиск по базе, фильтр по категориям, кнопка «собрать ленту» с прогрессом и разбивкой fetched/new/dup/empty.
2. **источники** — менеджер реестра:
   - таблица всех 589 источников: переключатель вкл/выкл, категория, тип, url, статус (жив / мёртв / не проверен), число записей;
   - фильтр по имени/url и по категории;
   - **подключить источник** — форма (имя, url, категория): тип и адаптер определяются по url автоматически (`/rss` → rss, `.json`/`/api/` → generic_json, `github.com/org` → github_org, `t.me/s/` → tg_web), запись живёт в SQLite и сразу участвует в обходах;
   - **проверить всё / проверить категорию** — фоновой джоб: реальный фетч каждого источника, запись `status/items/note/checked`, прогресс `done/total, живых/мёртвых`;
   - **вкл все / выкл все** — массово по текущему фильтру;
   - удаление своих источников (реестровые только выключаются).

Выключенный источник не дёргается ни панелью, ни `omni feed`, ни `omni doctor` — фильтр применяется в `sources.pick()`.

API: `GET /api/stats`, `GET /api/items?category=&q=&limit=&offset=`, `GET /api/sources?category=&q=`,
`POST /api/sources/toggle {name,enabled}`, `POST /api/sources/add {name,category,url}`,
`POST /api/sources/remove {name}`, `POST /api/sources/check {name|names|category|all}`,
`POST /api/feed {category,limit}`, `GET /api/job/<id>`.

Состояние источников — таблицы `source_flags` и `source_custom` в той же SQLite (`data/omni.sqlite3`).


## Типы записей (не путать с категорией источника)

Категория отвечает «откуда», тип — «что именно». Одна запись получает до 3 типов, они лежат в `items.types` и отдаются в API (`/api/types`, `?type=leak`), видны бейджами в панели, попадают в CSV.

`слив` · `триал` · `софт` · `промо` · `перепродажа` · `уязвимость` · `релиз` · `гайд` · `датасет` · `модель` · `вакансия` · `цена` · `вопрос` · `новость`

Правила лежат в `omni/taxonomy.py`: взвешенные RU/EN-паттерны, порог по весу, чтобы «free» в рекламе не превращалось в «триал».

## Telegram-каналы: реальные абузы без сессии

Публичное веб-превью `t.me/s/<канал>` — ни Telethon, ни api_id, ни токена бота.
Адаптер `tg_web` берёт `div.tgme_widget_message_text`, режет служебное
(`Channel created`, `Channel photo updated`, `pinned`), пустыши и посты из одной ссылки,
заголовок собирает из первой содержательной строки, дату — из `time[datetime]`, просмотры — из
`tgme_widget_message_views`. Для каналов с тегом `leak` порог ниже: они пишут коротко
(«<домен> 2M users»), и раньше такие посты отбрасывались как мусор.

Проверка каналов — `python tools/tg_discover.py --file data/tg_cand.txt --min 2`:
печатает по каждому статус, сколько постов даёт парсер и сколько из них новые.
Из 87 проверенных каналов живых 19; выкинуты те, у кого превью пустое
(`leakbase`, `abuse_ch`, `cracked_io`, `ai_zona`, `gpt_bot_news`, `codeby` — только
`Channel created` и инвайт-ссылки).

Живые: `thehackernews`, `bleepingcomputer`, `cvefeed`, `vulnwatch`, `ransomware_news`,
`breachradar`, `poc_in_github`, `hunt_news`, `vxunderground`, `true_secator`, `infosec_ru`,
`xakep_ru`, `prompt_injection`, `ai_newz`, `neurohive`, `neuralshit`, `seeallochnaya`,
`ai_free_ru`, `ai_products`, `addmetana`, `alstack`.

Один прогон этих каналов: 324 поста, 0 пустых источников.

### Своя сессия: глубина вместо 20 постов

Веб-превью отдаёт ~20 последних постов. Свой аккаунт (Telethon) по тем же каналам
берёт 200: прогон 20 каналов дал **2832 поста, 2592 новых записи** (остальное дубли).
Каналы с выключенным превью тоже читаются, но пустые не оживают: у `leakbase`
и через сессию 4 поста — только инвайты.

Секретов в репозитории нет, всё через окружение:

```bash
export OMNI_TG_SESSION=/path/to/account        # .session без расширения
export OMNI_TG_API_ID=... OMNI_TG_API_HASH=...
python -m omni pump thehackernews,cvefeed --limit 200 --apply
```

Без env команда честно говорит, что сессии нет, и парсер продолжает работать
на веб-превью. Аудит пула сессий — `tg_alive_audit.py`: из 856 файлов живыми
оказались 121 (остальные unauthorized/битые), их и берём.

Ещё по ходу: у CVE-каналов тело advisory без идентификатора в заголовке —
теперь `CVE-2026-97254 · Improper Neutralization...`, таких заголовков 471.

## X / Twitter без ключей

- `omni/providers/x.py` → `profile(handle)` тянет ленту через `api.fxtwitter.com/2/profile/<handle>/statuses`: полный текст, метрики (лайки, репосты, просмотры), дата, язык.
- адаптер `x_user` в `omni/feeds.py`, источники — `omni/sources_x.py` (30 живых хендлов: abuse/security/models/community).
- путь `syndication.twitter.com` (429 для всех IP, включая VPS и прокси) и nitter-зеркала (410/403/0) выпилены — не тратить время.
- свой хендл добавляется как источник: `{"name": "x_ник", "category": "abuse", "kind": "tweet", "url": "https://x.com/ник", "adapter": "x_user", "extra": {"handle": "ник"}}`.

## Ключи парсеров: один пул на весь комбайн

Ключи не лежат в коде и не уходят в git — только локально и в env.

- `python tools/build_vault.py` — собирает пул из `MASTER_KEYS.csv` и локальных дампов в `data/vault.json` (файл в `.gitignore`, значения никогда не печатаются).
- `python -m omni keys` / `python -m omni keys --service firecrawl -v` — сводка: сервис, сколько ключей, сколько готовых, маски.
- `python tools/vault_check.py` — живая проверка: помечает `live / dead / rate / nofund`.
- Рантайм `omni/vault.py`: сначала env (`FIRECRAWL_API_KEY`, `TAVILY_API_KEY`, …), потом пул; ротация по кругу; остывание ключа после 401/402/403 — час, после 429 — 10 минут. Один мёртвый ключ не ломает прогон.
- Провайдеры поиска/скрейпа (`firecrawl`, `tavily`, `exa`, `serper`, `jina`, `apify`) берут ключ из пула автоматически — отдельная настройка не нужна.
- Панель: `GET /api/keys` — сводка по сервисам без значений, строка «N ключей · M сервисов» в сайдбаре.
- В пуле сейчас 66 сервисов и ~9.9k записей; из парсерных: `firecrawl` 70 (живые, поиск проверен), `2captcha` 36, `anticaptcha` 15, `capsolver` 1, `telegram` 77 ботов; ключи `openai/deepseek/openrouter` идут на перевод и саммари.
- Капча для закрытых площадок: `2captcha`/`anticaptcha`/`capsolver` из того же пула.

## abuse-radar внутрь реестра

Радар (домены + каналы + посты) больше не отдельная система:

- `python -m omni radar` — dry-run: сколько доменов с каким score и сколько живых каналов.
- `python -m omni radar --apply --min-score 20` — пишет `data/radar_sources.json`: домены становятся HTML-источниками, каналы — Telegram-источниками (`tg_web`).
- `python -m omni radar --import-posts` — заливает посты каналов радара в общую базу как обычные записи (типы, score, фильтры, бот работают сразу).
- Источники радара помечены `opt_in`: в обычном обходе их нет, чтобы 2.5k новых источников не тормозили ленту. Берутся явно: `omni feed --tags radar` или `--category abuse`.
- Дефолтный путь к базе радара: `C:/Users/User/tmp/abuse_radar/radar_server.db`, переопределяется `--db`.

## Китайские и дарк-форумы

- `python tools/wave_cn.py [--apply]` — проверяет живые китайские/азиатские площадки и генерирует `omni/sources_cn.py`. Живых 9: 52pojie, nodeseek, kanxue, anquanke, 4hou, xz.aliyun, ithome, cnbeta, v2ex.
- `omni/sources_dark.py` — дарк/крэк-форумы, реально отдающие темы без логина: `cracked.st`, `nulledbb.com`, `forum.tuts4you.com`, `leak.sx` (плюс существующий набор `ab_*`).
- Для площадок под JS-челленджем: `python tools/cf_cookies.py [host …]` — открывает сайт настоящим браузером (Camoufox), ждёт прохода проверки, снимает cookies в `data/cookies.json` (вне git), после чего `omni/net.py` подставляет их сам. Проверка: `python tools/cf_cookies.py --check`.
- `net.get(..., proxy=…)` — принудительный прокси для отдельного источника (например CF-форумы через чистый DE-выход).
- Честное ограничение: `xss.is`, `exploit.in` (форум), `blackhatworld`, `hackforums` отдают контент только аккаунту — cookie-прохода мало, нужен логин.

## Автоаудит и непрерывные коммиты

- `python tools/selfcheck.py` — компиляция пакета, счётчики базы, распределение типов, топ источников, поиск дублей и пустых источников; пишет блок в `REPORT.md` и историю в `data/selfcheck.jsonl`.
- `bash tools/autocommit.sh [--feed]` — самоаудит (+ подкачка, если `--feed`), коммит только при реальных изменениях, пуш в оба ремоута.
- cron: каждые 6 часов аудит-коммит, каждые 12 часов аудит + подкачка источников.
- `omni dedupe [--apply]` — схлопывает дубли по url (или source+title при пустом url), вставка тоже дедуплицирует по url.

## Как устроено

- `omni/net.py` — лестница транспорта: httpx → curl_cffi (подмена TLS-фингерпринта) → прокси из env. Троттлинг по хосту, лимит байт, пометка блокировок.
- `omni/model.py` — единая схема записи: провайдер, тип, url, заголовок, текст, автор, дата, теги, цена, счёт, simhash.
- `omni/filter.py` — релевантность: запрос должен быть покрыт текстом (≥60% терминов) и хотя бы один термин — в заголовке. Для русского сравнивает по 5-символьному префиксу, иначе морфология убивает совпадения.
- `omni/store.py` — SQLite WAL + FTS5, таблицы `items`, `bands`, `runs`. Дедуп: simhash по шинглам, сравнение по Хэммингу ≤3 по бакетам.
- `omni/rank.py` — вес провайдера, свежесть, наличие цены, вовлечение.
- `omni/providers/` — по файлу на семейство источников, реестр в `__init__.py`.

## Реальные прогоны

```
python -m omni search "scraping twitter without api" --providers reddit,forums,ddg,bing
  bing 10 ok | ddg 10 ok | forums 10 ok | reddit 8 ok
  собрано 38, новых 31, дублей 7

python -m omni fanout   # 8 тем из themes.txt
  итого новых 200, дублей 5

python -m omni stats
  записей 266 | прогонов 56 (ok 37)
  ddg=93 bing=85 forums=56 reddit=32
```

## Ограничения

- Reddit напрямую с серверных IP отдаёт 403 — используется архив pullpush; свежие посты (последние часы) в архиве могут отсутствовать.
- X/Twitter без токена: доступны только публичные встраивания и таймлайн профиля, полноценного полнотекстового поиска нет.
- mojeek отдаёт пустую страницу при агрессивном троттлинге — провайдер помечается, остальные работают.
- `cards` не обходит защиту от парсинга: если страница рендерится JS, разметки в html не будет.

## Лицензия

MIT.

## Абузы, авто-добавление и Telegram-бот

- **абузы**: категория `abuse` — 31 живая площадка (XenForo/Discourse/Telegram/RSS), включая свои каналы, классификатор `omni/abuse.py` раскладывает записи по тегам `ключи / промо / триалы / сливы / софт / продажа / новости`. В панели — отдельная вкладка (`?view=abuse`), в боте — `/abuse [тег]`.
- **авто-добавление**: `omni/discover.py` ищет фиды на уже подключённых хостах и каталогах, проверяет их теми же адаптерами и сохраняет только те, что реально отдали записи. В панели — кнопка «авто-добавление», в API — `POST /api/discover?hosts=40&add=25`.
- **новости**: любые RSS/Atom/JSON-ленты (редакции, релизы, сообщества) подключаются как обычный источник или через `/add <url>` в боте — отдельной схемы не требуется.

### Telegram-бот

```bash
set OMNI_BOT_TOKEN=<токен BotFather>
set OMNI_BOT_ALLOW=<твой numeric id>
python -m omni.bot
```

Команды: `/new [N]`, `/abuse [тег]`, `/find <слово>`, `/src <слово>`, `/run <категория>`, `/add <url>`, `/stats`. Бот работает на той же базе и том же реестре, что панель; отвечает только id из `OMNI_BOT_ALLOW`.



## ИИ: перевод и саммари

Абузные площадки в основном не на русском: nodeloc (китайский), afflift и BHW (английский). Лента переводится на лету, подборка сворачивается в саммари — 3-5 пунктов, что раздают, платно или халява, где.

**Подключение.** Любой OpenAI-совместимый эндпоинт:

```bash
set OMNI_AI_KEY=<ключ>                       # обязателен только для ИИ-функций
set OMNI_AI_BASE=https://api.reformboss.com/v1
set OMNI_AI_MODEL=gpt-6.1-sol                # по умолчанию он же
```

Если `OMNI_AI_KEY` не задан, `omni/ai.py` ищет ключ в конфиге Hermes (`custom_providers` с `reformboss` в `base_url`). Без ключа парсер работает как раньше: ИИ-функции молча выключаются, кнопки пишут «ИИ не подключён».

**В боте:** кнопки `ИИ-саммари`, `Перевод: вкл/выкл`, `Саммари в подписке: вкл/выкл`; команды `/sum [тег]`, `/tr <id|слово>`. Перевод включается на чат/канал: в канале можно держать русский формат, в личке — оригинал.

**Автопостинг.** Если для канала включено «саммари в подписке», бот перед списком новых абузов пишет ИИ-сводку, дальше 5 находок с переводом заголовков.

**В панели:** вкладка `Абузы` → кнопка `ИИ-саммари` (`GET /api/summary?tag=promo&limit=14`).

**Как это сделано:** `omni/ai.py`, только stdlib (`urllib`), ретраи с падением на `glm-5.3` и `qwen3.8-flash`, если основная модель отдала 503/429. Переводы и саммари кэшируются в таблице `ai_cache` по хешу текста — повторные прогоны не тратят токены. Ключи не пишутся в репозиторий и не логируются.

## Что нужно подключить

1. **Python 3.11+** и зависимости: `pip install -r requirements.txt` (httpx, curl_cffi, bs4, lxml). Больше ничего не обязательно — база создаётся сама в `data/omni.sqlite3`.
2. **Ни одного ключа не нужно.** Reddit (архив), форумы (Discourse/XenForo/веб-Telegram), HN, arXiv, GitHub, HF, поисковики работают без регистрации. Платные search-API (`TAVILY_API_KEY`, `EXA_API_KEY`, `YOU_API_KEY`, `FIRECRAWL_API_KEY`) подхватываются из env, если они есть: с ними больше покрытие, без них проект полностью рабочий.
3. **Свои источники**: `python -m omni add <url> --category forum --tags мои`, кнопка «авто-добавление» в панели, `POST /api/discover` или `/auto` в боте. Адрес проверяется живым запросом и сохраняется только если реально отдал записи (проверено: `omni add https://lobste.rs/rss` → `добавлен manual_lobste_rs · rss · 6 записей`).
4. **Свои ключи, прокси и куки** — всё через env или `config.json` рядом с проектом:
```json
{"proxy_mode": "list",
 "proxies": ["http://user:pass@host:port"],
 "cookies": {"site.com": "session=abc; csrf=xyz"}}
```
   - ключи: `TAVILY_API_KEY`, `EXA_API_KEY`, `YOU_API_KEY`, `FIRECRAWL_API_KEY`, `JINA_API_KEY`, `SERPER_API_KEY`, `BRAVE_API_KEY`, `X_BEARER`, `REDDIT_CLIENT_ID` + `REDDIT_SECRET`, `TREG_TOKEN`, `GITHUB_TOKEN` — подхватываются из `.env`/env, `omni providers` показывает, что подключилось;
   - прокси: `proxy_mode` = `off` | `list` | `env` (`OMNI_PROXIES=http://p1,http://p2`) — используется третьим шагом лестницы, когда прямой запрос упёрся в блок (проверено: прямой egress 178.150.68.140 → через прокси 150.241.69.145);
   - куки: `cookies` в `config.json` или `OMNI_COOKIES='{"site.com":"a=b"}'` — подставляются по хосту с матчем по суффиксу (проверено на echo-эндпоинте: обе куки дошли);
   - свой сервер: `python -m omni serve --port 8077` поднимает панель и JSON API, за nginx/Caddy это уже удалённый инстанс на своей машине, база едет в `OMNI_DB`.
5. **Свой бот**: токен BotFather в `OMNI_BOT_TOKEN`, свой numeric id в `OMNI_BOT_OWNERS`, бота админом канала и `/sub @канал`.

## Проект обновляется

Проект живой: реестр источников, адаптеры и классификатор абузов правятся по мере того, как площадки ломают разметку. Обновление:

```bash
git pull
pip install -r requirements.txt
python -m omni serve --port 8077     # панель
python -m omni.bot                    # бот, если нужен
```

База в `data/` не перезаписывается — источники, здоровье и подписки остаются на месте. Ближайшие шаги: отдельная новостная лента с группировкой по сюжетам, скоринг абузов по свежести и частоте площадки, экспорт подборки в канал по расписанию.
