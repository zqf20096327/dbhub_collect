# Representable PA +

Representable is creating maps of communities to fight for equal and impartial representation. The core web app is written in Django with Javascript/HTML/CSS frontend and Postgres/PostGIS backend.

- There is a mapping & visualization app that allows orgs and users to draw their communities of interests. This is written in React & built using `createreactapp` and `Material UI`.
- In development is a dashboard component that allows orgs to define their turfs to do census outreach. This is build in Vue, Flask, and Airflow.  

[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg)](https://github.com/prettier/prettier) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

### Documentation
Check out our [Docs](https://docs.representable.org) site for a guide to installing Representable and contributing to various parts of the site. If you find any issues, we would love to know! Please open an issue request for any incomplete documentation.

#### Quick start

```bash
cp .env.example .env # update the variables

docker compose up -d
docker compose exec app /bin/bash

# run once to: setup the database, superuser, and test the app
export DJANGO_SETTINGS_MODULE=representable.settings.dev 
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata states.json
python manage.py collectstatic
python manage.py test

# run the django server
python manage.py runserver 0:8000 --settings=representable.settings.dev
```

In another terminal run 

```bash
docker compose exec app-plus /bin/bash
uv run python app.py
```

If you need a live vue instance

```bash
docker compose exec app-plus /bin/bash
cd vue-project
bun run dev --port 8888 --host 0.0.0.0
```

###### Tips

- If you update .env, you must run `source .env` to refresh it in your container.

### General Issue Reporting
For bug reports and general feature requests, please open a [Github issue](https://github.com/Representable/representable/issues/new/choose). We welcome all feedback and suggestions!

### Reporting Security Issues
We take security very seriously at Representable.org. Please send an email to [team@representable.org](mailto:team@representable.org) with any security issues and we'll open a private issue request with your concerns. We aim to respond to all security issues in a timely manner.

### Representable Contributors
Our core team of engineers is currently 6 members strong, though we've been supported by many others along the way. See more about our team and how we work at [representable.org/about](https://representable.org/about/)

- Somya Arora
- Kyle Barnes
- Chukwuagoziem Uzoegwu
- Jason Yuan
- Anna Eaton
- Izzy Zaller

### Founders
Representable began as a final project for Princeton University course Advanced Programming Techniques, taught by Brian Kernighan. The original project team is:

- Theodor Marcu
- Lauren Johnston
- Preeti Iyer
- Somya Arora
- Kyle Barnes

### License
Representable is under the GPL-3.0 License.
