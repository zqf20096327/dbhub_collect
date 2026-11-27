<div align="center">

# 📅 Schedule Bot

**Telegram-бот с расписанием занятий для студенческих групп**

Показывает пары на день и неделю, подсказывает следующую, предупреждает об экзаменах и сообщает, когда расписание изменилось.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![aiogram](https://img.shields.io/badge/aiogram-3.x-2CA5E0?logo=telegram&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-asyncpg-4169E1?logo=postgresql&logoColor=white)

</div>

---

## ✨ Возможности

- **Расписание на любой день** — листание вперёд и назад кнопками, время, предмет, преподаватель и аудитория.
- **Следующая пара** — команда `/n` показывает, что идёт сейчас и что дальше, и сколько времени осталось.
- **Работает в группах** — ответы видны только тому, кто вызвал команду (эфемерные сообщения).
- **Уведомления об изменениях** — раз в сутки бот сверяет расписание и пишет в чат, если оно поменялось.
- **Экзамены** — ближайшие экзамены отображаются в расписании дня.
- **HTML-виджеты в Telegram** — интерактивный виджет расписания прямо в чате.
- **Виджет для iPhone** — готовый скрипт для приложения [Scriptable](https://apps.apple.com/app/id1405459188).
- **Админ-панель** — статистика, последние ошибки, проверка доступности чатов и рассылка.

## 📸 Демонстрация

<div align="center">

| Расписание в боте | Админ-панель | Виджет на экране iPhone |
| :---: | :---: | :---: |
| <img src="assets/schedule-bot.webp" alt="schedule-bot" width="250"> | <img src="assets/admin-panel.webp" alt="admin-panel" width="250"> | <img src="assets/widget_preview.webp" alt="widget_preview" width="250"> |

</div>


## 🔐 Безопасность

- Пароли хранятся в базе только в зашифрованном виде (Fernet, ключ в `ENCRYPTION_KEY`).
- Сообщение с паролем сразу удаляется из чата.
- Пароль можно удалить в любой момент кнопкой «Удалить мой пароль».
- Логины и пароли не попадают в логи, в том числе при включённом `JOURNAL_TRACE`.

## 🚀 Быстрый старт

### 1. Требования

- Python 3.10+
- PostgreSQL
- Токен бота от [@BotFather](https://t.me/BotFather)

### 2. Установка

```bash
git clone <url-репозитория>
cd schedule_bot
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Настройка

```bash
cp env.example .env
```

Сгенерируйте ключ шифрования и вставьте его в `ENCRYPTION_KEY`:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Таблицы в базе создаются автоматически при первом запуске.

### 4. Запуск

```bash
set -a && source .env && set +a
python bot.py
```

## ⚙️ Переменные окружения

| Переменная | Обязательна | Описание |
|---|:---:|---|
| `BOT_TOKEN` | ✅ | Токен бота от BotFather |
| `DATABASE_URL` | ✅ | Строка подключения к PostgreSQL |
| `ENCRYPTION_KEY` | ✅ | Ключ Fernet для шифрования паролей |
| `ADMIN_IDS` | | Telegram ID администраторов через запятую |
| `WIDGET_URL` | | Адрес сервера виджета для iPhone |
| `WIDGET_PUBLIC_URL` | | Публичный адрес сервера виджета (по умолчанию равен `WIDGET_URL`) |
| `WIDGET_SECRET` | | Секрет для связи бота с сервером виджета |
| `JOURNAL_TRACE` | | `1` — логировать запросы к журналу (метод, путь, статус, время) |

## 💬 Команды

| Команда | Описание |
|---|---|
| `/start` | Главный экран. Ссылка `?start=starosta` подключает группу, `?start=widget` открывает настройку виджета |
| `/s` | Расписание |
| `/n` | Следующая пара |
| `/widget` | Виджет для iPhone (только в личном чате) |
| `/admin` | Админ-панель (только для `ADMIN_IDS`) |

## 🧩 Как это работает

1. Староста (или любой студент группы) подключает группу: бот входит на сайт журнала и запоминает доступ.
2. Раз в сутки бот забирает расписание текущей и следующей недели и экзамены каждой группы.
3. Данные кэшируются в PostgreSQL, поэтому команды отвечают мгновенно и не нагружают сайт.
4. Если у расписания изменился хэш, чатам с включёнными уведомлениями приходит сообщение.
5. Если вход перестал работать, например сменился пароль, бот предупреждает пользователя и просит подключить группу заново.

## 🗂 Структура проекта

```
schedule_bot/
├── bot.py                  # точка входа
├── requirements.txt
├── env.example
└── app/
    ├── main.py             # запуск, команды, роутеры
    ├── config.py           # настройки из окружения
    ├── db.py               # PostgreSQL: схема и запросы
    ├── journal.py          # клиент сайта журнала
    ├── sync.py             # загрузка, кэш и проверка расписания
    ├── screens.py          # экраны: день, следующая пара, экзамены
    ├── render.py           # форматирование текста
    ├── ui.py, emojis.py    # отправка сообщений, кастомные эмодзи
    ├── timeutil.py         # время по Москве
    ├── logs.py             # логи и буфер ошибок
    └── handlers/
        ├── commands.py     # /start, /s, /n
        ├── login.py        # подключение группы
        ├── callbacks.py    # кнопки
        ├── iphone_widget.py# виджет для iPhone
        └── admin.py        # админ-панель и рассылка
```

## 🛠 Стек

[aiogram 3](https://docs.aiogram.dev/) · [aiohttp](https://docs.aiohttp.org/) · [asyncpg](https://magicstack.github.io/asyncpg/) · [cryptography](https://cryptography.io/)
