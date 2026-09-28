# Sound Cloud

**Sound Cloud** — современная аудиоплатформа для поиска, прослушивания и скачивания музыки. Музыканты могут загружать свои треки для бесплатного использования.

## Содержание

- [Функционал](#функционал)
- [Технологический стек](#технологический-стек)
- [Структура проекта](#структура-проекта)
- [Начало работы](#начало-работы)
- [Переменные окружения](#переменные-окружения)
- [Разработка](#разработка)
- [Тестирование](#тестирование)
- [Развертывание](#развертывание)
- [Лицензия](#лицензия)
- [Контакты](#контакты)

## Функционал

- Аутентификация через OAuth2 (Google, Spotify)
- Аутентификация пользователей на основе JWT
- Управление профилем пользователя
- CRUD для альбомов, плейлистов, треков, лицензий
- Загрузка, стриминг и скачивание музыки
- Избранные исполнители, комментарии к трекам
- Кастомная модель пользователя, валидация файлов, контроль доступа через nginx

## Технологический стек

- **Бэкенд:** Python 3.9+, Django 3.2, Django REST Framework
- **База данных:** PostgreSQL
- **Документация API:** Swagger (drf-yasg)
- **Контейнеризация:** Docker, docker-compose
- **Веб-сервер:** Nginx

## Структура проекта

```
sound_cloud/
├── src/
│   ├── oauth/           # Логика OAuth
│   ├── audio_library/   # Логика музыкальной библиотеки
│   ├── base/            # Базовые сервисы, permissions
│   ├── routes.py
│   └── __init__.py
├── config/              # Настройки Django, urls, wsgi/asgi
├── nginx/               # Конфиги Nginx, Dockerfile
├── static/              # Статические файлы
├── templates/           # Шаблоны
├── media/               # Загружаемые файлы
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh
├── manage.py
└── README.md
```

## Начало работы

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/your-org/sound_cloud.git
cd sound_cloud
```

### 2. Настройте переменные окружения

- Скопируйте `.env.example` в `.env.dev` и заполните ваши значения.

### 3. Соберите и запустите контейнеры

```bash
docker-compose up --build
```

### 4. Доступ к документации API

- Откройте [http://localhost/api/v1/swagger/](http://localhost/api/v1/swagger/) в вашем браузере.

### 5. Создайте суперпользователя

```bash
docker exec -it sound_cloud_web bash
python manage.py createsuperuser
```

### 6. (Опционально) Сброс базы данных

```bash
docker-compose down -v
```

## Переменные окружения

Создайте файл `.env.dev` на основе `.env.example` и укажите значения для:

- Настройки Django (`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`)
- База данных (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`)
- OAuth (`GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`)
- Nginx (`NGINX_HOST`, `NGINX_PORT`)

## Разработка

- Все зависимости указаны в `requirements.txt`.
- Для локальной разработки используйте Docker.
- Для хранения загружаемых файлов используйте папку `media/` (не забудьте добавить пустой файл `.gitkeep`).

## Тестирование

> **TODO:** Описать запуск тестов, если они реализованы.

## Развертывание

- Используйте переменные окружения для production.
- Проверьте настройки безопасности Django.
- Настройте постоянное хранилище для media-файлов.

## Лицензия

[BSD 3-Clause License](https://opensource.org/licenses/BSD-3-Clause)  
© 2021–настоящее время, DJWOMS — Omelchenko Michael

## Контакты

- [Сайт](https://collabteam.dev)
- [YouTube](https://youtube.com/playlist?list=PLF-NY6ldwAWosy6hAyKMwZozmEyq1J2fg)
- [Telegram](https://t.me/trueDjangoChannel)




