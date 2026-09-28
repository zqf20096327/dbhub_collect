# django-react-blog

Blog web application written using Javascript with React for Frontend, Python with Django for Backend and PostgreSQL as a default database.

## Features

- Publish posts as a verified staff member
- Read public posts
- Write/read comments
- Fully functional user with password veryfing/reseting using e-mail
- Authentication thanks to JWT Tokens

## Screenshots

### [Click to see more](https://github.com/syqu22/django-react-blog/tree/main/media/screenshots)

![image](https://raw.githubusercontent.com/syqu22/django-react-blog/main/media/screenshots/01.png)
![image](https://raw.githubusercontent.com/syqu22/django-react-blog/main/media/screenshots/04.png)
![image](https://raw.githubusercontent.com/syqu22/django-react-blog/main/media/screenshots/07.png)
![image](https://raw.githubusercontent.com/syqu22/django-react-blog/main/media/screenshots/11.png)
![image](https://raw.githubusercontent.com/syqu22/django-react-blog/main/media/screenshots/14.png)

## Installation

1. First clone the repository to use it localy:

        git clone https://github.com/syqu22/flask-pastebin.git

    Then install all required libraries  through:

        pip install -r requirements.txt

2. Rename the `.env.sample` to `.env`, then fill it with all the needed keys. `POSTGRES` is for the database access, `EMAIL` is for the email authentication and `SECRET_KEY` is the secret key for the application.

3. Now you need to create a Postgre database with name `blog_db` then do all the migrations using command:

        py manage.py makemigrations

    and:

        py manage.py migrate

4. For the frontend you need to run these commands from the `/frontend` folder:

        npm install

    to download all the needed NPM packages and then to start the frontend Dev server:

        npm run dev

5. Finally you can start the frontend server from base project folder by running:

        py manage.py runserver
