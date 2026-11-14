# Telegram Bot "Girls und Card"

Коллекционная карточная игра (CCG) в Telegram с внутриигровой экономикой. 
Аудитория: **700+ активных пользователей** (международное сообщество).

👉 **Ссылка на бота:** [@Girls_und_card_bot] (https://t.me/Girls_und_card_bot) 
*(Бот развернут на изолированной Ubuntu VM, возможны редкие перезагрузки при обновлении кода)*

## 🚀 Возможности
- **Гача-система:** Выдача карточек с редкостью от 2 до 4 звезд (с защитой от спама — раз в час).
- **Инвентарь:** Группировка дубликатов (до 5 штук в стопке).
- **Экономика:** Внутренние баллы, переводы между пользователями (`/give`), магазин карточек (`/buy`).
- **Крафт:** Переработка дубликатов в карты выше уровнем (`/craft`).
- **Торговля:** Обмен карточками между игроками (`/givecard`).
- **Мини-игра:** Слот-машина "Казино" с асинхронной анимацией (`/casino`).

## 🛠 Стек технологий
- **Язык:** Python 3
- **Библиотека:** Aiogram 3, python-dotenv
- **База данных:** SQLite (sqlite3)
- **Инфраструктура:** Ubuntu VM, systemd (автозапуск), VPN-туннель (для доступа к Telegram API).

## 📸 Скриншоты
![Меню с командами](https://github.com/Knizhniknikita/Girls_und_card_bot/blob/main/screens/Botscreen2.png?raw=true)
![Выдача карточки](https://github.com/Knizhniknikita/Girls_und_card_bot/blob/main/screens/Botscreen1.png?raw=true)
![Мини-игра Казино](https://github.com/Knizhniknikita/Girls_und_card_bot/blob/main/screens/Botscreen3.png?raw=true)

## ⚙️ Как запустить локально (Пошагово)
1. **Скачайте проект** (или сделайте `git clone`).
2. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
