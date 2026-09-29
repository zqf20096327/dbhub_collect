# TelegramStarsBot

**TelegramStarsBot** — это Telegram-бот для продажи изображений за Telegram Stars (XTR), внутреннюю валюту Telegram. Бот показывает пример приёма платежей в XTR, их подтверждения, сохранения информации в SQLite и отправки цифрового товара после успешной оплаты.

## Структура проекта

* **bot.py** — основной файл с логикой бота, обработчиками команд и платежей.
* **db.py** — модуль для работы с базой данных SQLite.
* **keyboards.py** — модуль с inline-клавиатурами.
* **config.py** — файл конфигурации с переменными окружения.
* **.env** — файл с секретными данными (не должен попадать в репозиторий).
* **img/** — каталог с изображениями для продажи.

## Установка и запуск через venv

### 1. Клонирование репозитория

```bash
git clone https://github.com/king-tri-ton/TelegramStarsBot
cd TelegramStarsBot
```

### 2. Создание виртуального окружения

**Windows:**

```bash
python -m venv venv
```

**Linux / macOS:**

```bash
python3 -m venv venv
```

### 3. Активация виртуального окружения

**Windows (cmd / PowerShell):**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 4. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 5. Настройка переменных окружения

Переименуй `.env.example` в `.env` и укажи данные:

```env
TOKEN='your_bot_token'
DATABASE='payments.db'
```

### 6. Запуск бота

```bash
python bot.py
```

### Функциональность

* `/start` — приветственное сообщение с кнопкой «Купить изображение».
* **Кнопка «Купить изображение»** — создаёт счёт на оплату 1 XTR.
* **Оплата Telegram Stars (XTR)** — встроенный платёж Telegram.
* **Успешный платёж**:

  * отправляется сообщение о принятии оплаты;
  * данные платежа сохраняются в SQLite;
  * пользователю отправляется изображение.
* `/paysupport` — информация об отсутствии возврата средств и поддержке.

## База данных

Таблица `payments`:

* `user_id` — ID пользователя Telegram
* `payment_id` — идентификатор платежа
* `amount` — сумма платежа
* `currency` — валюта (XTR)

База данных создаётся автоматически при запуске бота.

## Важно

* Файл `.env` обязательно добавь в `.gitignore`.
* Путь к изображению указывается вручную в `bot.py`.
* `provider_token` для XTR должен быть пустой строкой.

## Лицензия

Проект распространяется по лицензии [MIT](LICENSE).

## Контакты

По вопросам и предложениям:

* Telegram: [https://t.me/king_tri_ton](https://t.me/king_tri_ton)
* Email: [mdolmatov99@gmail.com](mailto:mdolmatov99@gmail.com)
* Также можно создавать issues в репозитории

---

by **King Triton**
