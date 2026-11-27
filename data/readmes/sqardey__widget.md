# 📅 IT TOP Schedule Widget

![Go](https://img.shields.io/badge/Go-1.26-00ADD8?style=flat-square&logo=go&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)
![iOS](https://img.shields.io/badge/iOS-Scriptable-111111?style=flat-square&logo=apple&logoColor=white)

**Текущая пара, следующее занятие и экзамены — прямо на экране iPhone.**

Go-сервис получает расписание из электронного журнала IT TOP, кеширует результаты и передаёт их виджету Scriptable.

В проект входят HTTP API, две версии JS-шаблонов, PostgreSQL и развёртывание через Docker Compose с nginx и HTTPS.

[Русский](#русский) · [English](#english)

---

## Русский

### ✨ Возможности

- **Расписание:** текущая и следующая пара, предмет, аудитория и время занятий.
- **Экзамены:** проверка наличия экзамена на сегодня.
- **Scriptable:** скачивание персональных скриптов через API.
- **Шифрование:** логины и пароли журнала сохраняются с использованием AES-256-GCM.
- **Кеширование:** расписание хранится отдельно для каждого пользователя.
- **Обновление:** автоматическая проверка актуальности при запросе и ручное обновление с cooldown.
- **Развёртывание:** Docker Compose, PostgreSQL, nginx и HTTPS.
- **Диагностика:** структурированные JSON-логи и идентификаторы запросов.
- **Завершение работы:** graceful shutdown по сигналу.

> Неофициальный учебный проект студента IT TOP. Работа зависит от доступности и формата API электронного журнала. Совместимость со всеми филиалами и аккаунтами не гарантируется.

### 🧩 Как это работает

1. Виджет отправляет запрос с персональным API-ключом.
2. Сервер находит пользователя в PostgreSQL.
3. Расшифровывает учётные данные для обращения к журналу.
4. Возвращает расписание из кеша или запрашивает обновление.
5. Scriptable отображает текущую и следующую пару.

| Компонент | Назначение |
| --- | --- |
| Scriptable | Получение JSON и отображение виджета |
| nginx | HTTPS и передача запросов Go-серверу |
| HTTP API | Обработка запросов и работа с пользователями |
| ScheduleCache | Кеш расписаний и правила обновления |
| Parser | Авторизация и запросы к журналу |
| PostgreSQL | Пользователи, API-ключи и зашифрованные учётные данные |

### 🔄 Правила обновления

| Событие | Поведение |
| --- | --- |
| Первое обращение | Загрузка расписания из журнала |
| Перезапуск сервера | Кеш пустой, расписание загружается заново |
| Смена дня | Загрузка расписания на новый день |
| Прошло 3 часа после обновления | Обновление при следующем запросе |
| Запрос с `force=1` | Обновление, если с последнего успешного обновления прошёл минимум час |
| Сохранение учётных данных через API | Сброс кеша пользователя |
| Журнал недоступен, но есть сегодняшние данные | Возврат сохранённого расписания |
| Журнал недоступен и сегодняшних данных нет | Ответ `502 Bad Gateway` |

**Фонового опроса нет:** актуальность кеша проверяется при обращении к API.

Текущий часовой пояс сервера — `Europe/Moscow`.

Кеш хранит только расписание, экзамен и время обновления. Логины, пароли и экземпляры parser в нём не сохраняются.

---

### 🚀 Запуск

Текущий Docker Compose рассчитан на **Linux VPS**. Приложение и nginx используют `network_mode: host`.

Потребуются:

- Docker Engine и Docker Compose.
- Git.
- Домен для HTTPS.
- Доступные порты `80` и `443`.

#### 1. Скачать проект

```bash
git clone https://github.com/sqardey/widget.git
cd widget
mkdir -p nginx certbot/www certbot/conf
```

#### 2. Настроить окружение

Создайте `.env` в корне проекта:

```dotenv
PORT=8081

CONN_STRING=postgres://postgres:CHANGE_ME@127.0.0.1:5433/widget_db?sslmode=disable

BOT_SECRET=REPLACE_WITH_BOT_SECRET
CREDENTIALS_KEY=REPLACE_WITH_BASE64_KEY

# Необязательно: удалите строку, если прокси не нужен.
PROXY_URL=socks5://127.0.0.1:40000
```

| Переменная | Описание |
| --- | --- |
| `PORT` | Порт приложения, по умолчанию `8080` |
| `CONN_STRING` | Строка подключения к PostgreSQL |
| `BOT_SECRET` | Секрет регистрации пользователей через API |
| `CREDENTIALS_KEY` | 32 случайных байта в Base64 для шифрования учётных данных |
| `PROXY_URL` | Необязательный прокси для запросов к журналу |

Создайте ключ шифрования:

```bash
openssl rand -base64 32
```

Создайте отдельный секрет бота:

```bash
openssl rand -hex 32
```

Скопируйте результаты в соответствующие переменные `.env`.

**Ключ шифрования создаётся один раз и должен сохраняться между перезапусками.** Его потеря сделает сохранённые учётные данные недоступными. Смена ключа требует отдельной миграции данных.

В `docker-compose.yml` задайте `POSTGRES_PASSWORD`, соответствующий паролю в `CONN_STRING`.

Для уже созданной базы изменение `POSTGRES_PASSWORD` в Compose не меняет пароль роли PostgreSQL.

> В текущем Compose база опубликована на `127.0.0.1:5433`. Приложение в сети `host` подключается к этому порту.

Не добавляйте `.env`, сертификаты и резервные копии базы в Git. Исключите их также из Docker build context через `.dockerignore`.

#### 3. Запустить приложение

```bash
docker compose up -d --build db widget-v2
```

Посмотреть логи:

```bash
docker compose logs --tail=50 widget-v2
```

Приложение слушает `127.0.0.1:PORT`. Публичные запросы принимает nginx.

Начальная SQL-схема применяется автоматически только при первом запуске PostgreSQL с пустым томом. Последующие миграции необходимо применять отдельно.

**Не удаляйте `pgdata` для повторного запуска SQL-инициализации — это удалит данные.**

---

### 🔐 nginx и HTTPS

В примерах используется домен:

```text
widget.sqardey.xyz
```

Для собственного развёртывания замените его в конфигурации nginx и при подстановке адреса в JS-шаблоны.

DNS-запись `A` должна указывать на IP VPS. Если есть запись `AAAA`, она также должна вести на этот сервер.

#### 1. Временная конфигурация для получения сертификата

Создайте `nginx/default.conf`:

```nginx
server {
    listen 80;
    server_name widget.sqardey.xyz;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 503;
    }
}
```

Запустите nginx:

```bash
docker compose up -d nginx
```

Получите сертификат:

```bash
docker compose run --rm certbot certonly \
  --webroot \
  --webroot-path /var/www/certbot \
  --cert-name widget.sqardey.xyz \
  -d widget.sqardey.xyz
```

#### 2. Основная конфигурация HTTPS

После успешного получения сертификата замените `nginx/default.conf`:

```nginx
server {
    listen 80;
    server_name widget.sqardey.xyz;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name widget.sqardey.xyz;

    ssl_certificate /etc/letsencrypt/live/widget.sqardey.xyz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/widget.sqardey.xyz/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;

    client_max_body_size 1m;

    # Отключаем обычный access log с API-ключами в URL.
    access_log off;

    location / {
        proxy_pass http://127.0.0.1:8081;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_connect_timeout 5s;
        proxy_read_timeout 180s;

        proxy_cache off;
    }
}
```

Порт в `proxy_pass` должен совпадать с `PORT` приложения.

Проверьте конфигурацию:

```bash
docker compose exec nginx nginx -t
```

Если проверка успешна, примените её:

```bash
docker compose exec nginx nginx -s reload
```

#### 3. Продление сертификата

Проверьте механизм продления:

```bash
docker compose run --rm certbot renew --dry-run
```

Добавьте в `crontab -e` пользователя с доступом к Docker, заменив абсолютный путь к проекту:

```cron
17 3 * * * cd /absolute/path/to/widget && docker compose run --rm -T certbot renew --quiet && docker compose exec -T nginx nginx -s reload
```

Certbot продлевает сертификат, когда подходит срок. Убедитесь, что cron работает на VPS.

---

### 📡 API

#### Добавление пользователя или обновление учётных данных

```http
POST /api/widget/newuser
X-Bot-Secret: <BOT_SECRET>
Content-Type: application/json
```

Тело запроса:

```json
{
  "tg_id": 123456789,
  "login": "your_journal_login",
  "password": "your_journal_password"
}
```

Ответ — `201 Created`:

```json
{
  "key": "YOUR_USER_API_KEY"
}
```

Сервер шифрует логин и пароль перед сохранением.

При повторном `tg_id`:

- обновляются учётные данные;
- сохраняется существующий API-ключ;
- сбрасывается кеш расписания.

Регистрация проверяет наличие полей, но не проверяет авторизацию в журнале. Неверный логин или пароль обнаружится при получении расписания.

> Не вставляйте открытые логины и пароли напрямую в БД: приложение ожидает зашифрованные значения. Старые записи требуют отдельной миграции с использованием текущего ключа шифрования.

#### Получение расписания

```http
GET /api/widget?key=<USER_API_KEY>
```

Запрос ручного обновления:

```http
GET /api/widget?key=<USER_API_KEY>&force=1
```

| Параметр | Обязательный | Назначение |
| --- | --- | --- |
| `key` | Да | Персональный API-ключ пользователя |
| `force` | Нет | `1` — запрос обновления с учётом серверного cooldown |

Пример ответа:

```json
{
  "has_exam": false,
  "current_class": {
    "name_subject": "Тестирование программного обеспечения",
    "audience": "304",
    "start_time": "14:00",
    "end_time": "15:30",
    "duration": 90
  },
  "next_class": {
    "name_subject": "Базы данных",
    "audience": "201",
    "start_time": "15:40",
    "end_time": "17:10",
    "duration": 90
  },
  "updated_at": "14:05"
}
```

При наличии экзамена добавляется объект:

```json
{
  "has_exam": true,
  "exam": {
    "name_subject": "Базы данных",
    "date": "2026-11-26"
  },
  "updated_at": "09:00"
}
```

Поля `current_class`, `next_class` и `exam` отсутствуют, если соответствующих данных нет.

Например, после окончания занятий:

```json
{
  "has_exam": false,
  "updated_at": "23:56"
}
```

**Это успешный ответ.** Он также возможен в день без занятий.

`updated_at` — время последнего успешного получения расписания из журнала.

#### Скачивание скриптов

Первая версия:

```http
GET /api/widget/script?key=<USER_API_KEY>
```

Вторая версия:

```http
GET /api/widget/script/v2?key=<USER_API_KEY>
```

Сервер возвращает JavaScript-файл с персональным ключом.

Если шаблон содержит `{{BASE_URL}}`, обработчик должен заменить его на публичный HTTPS-адрес. В готовом скрипте не должно оставаться заглушек `{{API_KEY}}` или `{{BASE_URL}}`.

Шаблоны встроены в бинарник через `go:embed`: после их изменения требуется пересборка приложения.

#### Коды ответов

| Код | Значение |
| --- | --- |
| `200` | Расписание или скрипт успешно получены |
| `201` | Учётные данные сохранены |
| `400` | Некорректный запрос или отсутствуют обязательные поля |
| `401` | Неверный/отсутствующий API-ключ расписания или секрет бота |
| `500` | Внутренняя ошибка, включая БД и расшифровку |
| `502` | Не удалось получить расписание из журнала |

Обработчики скачивания скриптов проверяют наличие параметра `key`. Проверка существования пользователя выполняется при запросе расписания.

---

### 📱 Установка виджета на iPhone

1. Установите [Scriptable](https://scriptable.app/).
2. Зарегистрируйте аккаунт через интеграцию бота с API.
3. Получите персональный скрипт через маршрут скачивания.
4. Импортируйте его в Scriptable.
5. Запустите скрипт внутри приложения.
6. Добавьте виджет Scriptable на экран и выберите установленный скрипт.

В актуальном шаблоне v2 предусмотрены:

- светлая и тёмная темы;
- несколько размеров;
- варианты для экрана блокировки;
- таймер текущей пары;
- отображение следующего занятия и экзамена;
- ручное обновление по нажатию.

**Проверьте адрес в скачанном скрипте:**

```js
const BASE_URL = "https://widget.sqardey.xyz";
```

Порт `8081` в публичном адресе не нужен: запрос проходит через nginx.

Частоту фонового обновления определяет iOS. Запрос `force=1` не отменяет серверный cooldown.

Скрипт содержит персональный API-ключ — не публикуйте его.

**Обновление шаблона на сервере не меняет файл на телефоне.** После изменений скачайте и установите скрипт повторно.

---

### 🛠 Разработка

Для запуска без Docker нужны Go 1.26+, PostgreSQL и переменные окружения процесса.

```bash
go mod download
go run ./cmd/server
```

Приложение самостоятельно не читает `.env`. При запуске через Compose переменные передаются с помощью `env_file`.

#### Структура проекта

| Путь | Содержимое |
| --- | --- |
| `cmd/server` | Запуск сервера и graceful shutdown |
| `internal/config` | Основная конфигурация |
| `internal/transport/http` | Маршруты, middleware, шифрование и JS-шаблоны |
| `internal/repository` | Работа с PostgreSQL |
| `internal/cache` | Кеш расписаний |
| `internal/parser` | HTTP-клиент журнала |
| `internal/domain` | Модели данных |
| `migrations` | SQL-схема |
| `nginx` | Конфигурация reverse proxy |

#### Полезные команды

```bash
# Запустить основные сервисы
docker compose up -d --build

# Посмотреть статус
docker compose ps

# Посмотреть логи
docker compose logs --tail=100 -f widget-v2 nginx

# Пересобрать приложение после изменения Go или JS-шаблонов
docker compose up -d --build widget-v2

# Проверить nginx
docker compose exec nginx nginx -t

# Перечитать конфигурацию nginx
docker compose exec nginx nginx -s reload
```

---

### 🔎 Диагностика

| Проблема | Что проверить |
| --- | --- |
| `404` на `/` | Главная страница не реализована. Проверяйте `/api/widget?key=...` |
| «Нет связи» на телефоне | Адрес в JS, доступность HTTPS с телефона, отсутствие старого порта `8081` |
| В скрипте остался `{{BASE_URL}}` | Подстановку адреса в обработчике соответствующей версии |
| `200`, но текущей и следующей пары нет | Занятия закончились либо сегодня их нет |
| Ошибка расшифровки | Ключ изменился, запись повреждена или в БД остались открытые данные |
| Ошибка PostgreSQL | Порт `5433`, пароль, строку подключения и `sslmode=disable` |
| `502` | Доступность журнала, учётные данные и прокси |
| Правки шаблона не появились | Пересборку Go-контейнера и повторное скачивание скрипта |
| nginx не находит сертификат | Сначала получите сертификат через временный HTTP-конфиг |

### 📌 Текущие ограничения

- Кеш находится в памяти и очищается при перезапуске.
- Неактивные пользователи автоматически из кеша не удаляются.
- После неудачного обновления нет отдельной паузы перед повторной попыткой.
- Таймауты Scriptable, Go-сервера и запросов к журналу требуют согласования.
- Расписание зависит от внешнего API, который может измениться.
- Время занятий интерпретируется с учётом текущего серверного часового пояса.

### 🤝 Участие в проекте

Issues и pull requests приветствуются.

В сообщении об ошибке укажите:

- что сделали;
- какой результат ожидали;
- что получили;
- логи без персональных данных и секретов.

Не прикладывайте `.env`, пароли, ключ шифрования и персональные API-ключи.

---

## English

### Overview

**A self-hosted Go service and Scriptable widgets for IT TOP College schedules.**

The service fetches the current and next class, checks today's exams and provides personalized JavaScript widgets for iPhone.

This is an unofficial student project. Availability depends on the journal API; compatibility with every campus is not guaranteed.

### Features

- Go standard library HTTP server.
- PostgreSQL 16 with `pgxpool`.
- AES-256-GCM encryption for stored journal credentials.
- Per-user schedule cache without retained credentials or parser instances.
- Two downloadable Scriptable templates.
- Light/dark themes and multiple widget layouts in v2.
- Docker Compose, nginx HTTPS termination, structured logs and graceful shutdown.

### Deployment

The supplied Compose uses **host networking on a Linux VPS**.

```bash
git clone https://github.com/sqardey/widget.git
cd widget
mkdir -p nginx certbot/www certbot/conf
```

Create `.env` using the example in the Russian section.

| Variable | Purpose |
| --- | --- |
| `PORT` | Application port |
| `CONN_STRING` | PostgreSQL connection string |
| `BOT_SECRET` | Secret required for user registration |
| `CREDENTIALS_KEY` | 32 random bytes encoded as Base64 |
| `PROXY_URL` | Optional proxy for journal requests |

Generate the encryption key:

```bash
openssl rand -base64 32
```

Keep the same key across restarts. Losing it makes existing credentials unreadable.

The current Compose exposes PostgreSQL at `127.0.0.1:5433`. Match the database password in Compose and the connection string.

```bash
docker compose up -d --build db widget-v2
```

Follow the nginx HTTP bootstrap, certificate issuance and HTTPS configuration above. Replace the example domain for your own deployment and schedule certificate renewal.

The application does not load `.env` itself. Compose supplies it through `env_file`.

### API

| Method | Route | Purpose |
| --- | --- | --- |
| `POST` | `/api/widget/newuser` | Create/update credentials |
| `GET` | `/api/widget?key=...` | Get current/next class and exam information |
| `GET` | `/api/widget?key=...&force=1` | Request a refresh |
| `GET` | `/api/widget/script?key=...` | Download the first widget template |
| `GET` | `/api/widget/script/v2?key=...` | Download the second widget template |

Registration requires the `X-Bot-Secret` header and a JSON body:

```json
{
  "tg_id": 123456789,
  "login": "your_journal_login",
  "password": "your_journal_password"
}
```

The response contains a personal API key.

Credentials are encrypted before insertion. Registration does not immediately validate journal authentication.

**Do not insert plaintext credentials directly into the database.** Existing plaintext records require a separate migration.

Schedules refresh on request after three hours, on a new day or when an eligible manual refresh is requested. Manual refresh has a one-hour cooldown.

Cached data from the same day may be returned if the journal is unavailable. A restart clears the cache.

Missing `current_class` and `next_class` fields are normal after classes end or on a day without classes.

### Scriptable

1. Install [Scriptable](https://scriptable.app/).
2. Register through the bot/API.
3. Download your personalized script.
4. Run it in Scriptable.
5. Select it in a Scriptable widget.

Check that the generated script contains a real API key and an HTTPS base URL without the internal Go port.

iOS controls background refresh timing. Changing server templates does not update previously downloaded scripts: rebuild the application and download the script again.

### Contributing

Bug reports and pull requests are welcome. Include the failing scenario, expected behaviour and sanitized logs.

Do not attach passwords, `.env`, encryption keys or personal API keys.

---

## 📄 Лицензия / License

Условия использования см. в [LICENSE](LICENSE).

See [LICENSE](LICENSE) for the repository's license terms.
````
