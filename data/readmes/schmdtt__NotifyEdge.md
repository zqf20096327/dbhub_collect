# NotifyEdge Bot

Telegram-бот для напоминаний с гибкими расписаниями, мультипользовательской поддержкой и панелью администратора.

A Telegram reminder bot with flexible scheduling, multi-user support and an admin panel.

**Live → [@NotifyEdge_bot](https://t.me/NotifyEdge_bot)**

---

## Возможности / Features

- 🌅 Ежедневные напоминания в заданное время
- 📅 По дням недели (один или несколько)
- 🔄 Каждые N дней
- 1️⃣ Однократные напоминания — сегодня, завтра или на конкретную дату
- 🔖 Опциональное название напоминания (с авто-нумерацией)
- ⏰ Действия после уведомления — выполнено, отложить (15 мин / 30 мин / 1 час), отключить
- 🌍 Индивидуальный часовой пояс для каждого пользователя
- ⛔ Лимит 50 активных напоминаний на пользователя
- 🛡 Панель администратора — статистика, список пользователей, поиск, рассылка

---

## Как работает / How it works

При добавлении напоминания бот вычисляет ближайшее время срабатывания и создаёт задание в APScheduler. После каждого срабатывания задание автоматически пересчитывается на следующий интервал. При перезапуске все активные напоминания восстанавливаются из базы данных.

When a reminder is added, the bot calculates the nearest fire time and schedules a job via APScheduler. After each trigger, the job is automatically rescheduled for the next occurrence. On restart, all active reminders are recovered from the SQLite database.

---

## Требования / Requirements

- Python 3.11+
- Токен Telegram-бота от [@BotFather](https://t.me/BotFather)
- Telegram ID администратора (получить через [@userinfobot](https://t.me/userinfobot))

---

## Установка / Setup

```bash
git clone https://github.com/schmdtt/NotifyEdge.git
cd NotifyEdge
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Скопируй `.env.example` в `.env` и заполни:

```env
BOT_TOKEN=your_bot_token_here
ADMIN_ID=your_telegram_id
```

Запуск:

```bash
python bot.py
```

---

## Деплой на сервер / Production

```ini
[Unit]
Description=NotifyEdge Bot
After=network.target

[Service]
WorkingDirectory=/opt/notifyedge
ExecStart=/opt/notifyedge/venv/bin/python /opt/notifyedge/bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
systemctl enable --now notifyedge
journalctl -u notifyedge -f
```

---

## Структура проекта / Project structure

```
├── bot.py                   # Точка входа / Entry point
├── config.py                # Переменные окружения / Environment config
├── database.py              # SQLite CRUD
├── scheduler.py             # APScheduler — планирование заданий
├── handlers/
│   ├── start.py             # Онбординг, выбор таймзоны
│   ├── menu.py              # Главное меню
│   ├── add_reminder.py      # FSM добавления напоминания
│   ├── list_reminders.py    # Просмотр и редактирование
│   ├── notifications.py     # Кнопки действий на уведомлении
│   ├── settings.py          # Настройки пользователя
│   └── admin.py             # Панель администратора
├── keyboards/
│   ├── main.py
│   ├── reminder.py
│   └── timezone.py
└── utils/
    └── time_utils.py        # Расчёт расписаний, форматирование времени
```

---

## Стек / Stack

- [aiogram 3.x](https://docs.aiogram.dev/) — Telegram Bot API
- [APScheduler](https://apscheduler.readthedocs.io/) — планировщик задач
- [aiosqlite](https://aiosqlite.omnilib.dev/) — асинхронный SQLite
- [pytz](https://pythonhosted.org/pytz/) — работа с часовыми поясами
