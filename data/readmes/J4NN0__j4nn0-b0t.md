# J4NN0 B0T

[![https://telegram.me/J4NN0_Bot](https://img.shields.io/badge/💬_Bot_Telegram-J4NN0_Bot-blue.svg)](https://telegram.me/J4NN0_Bot) 

The Bot is hosted on [Heroku](https://www.heroku.com/) and has been tested with Python `v3.9.7`.

J4NN0 BOT main features:
1. Store, delete, and view items on your private list using simple chat commands.
2. Set a timed reminder — the bot will notify you with your custom message when the time is up.

Check it out on telegram: [@J4NN0_Bot](http://telegram.me/J4NN0_Bot)

### Demo
[![Watch the video](https://img.youtube.com/vi/2pSjPOuMDhk/maxresdefault.jpg)](https://youtu.be/2pSjPOuMDhk)

# Table of Contents
- [Database](#database)
- [Bot usage](#bot-usage)
- [How to host BOT on Heroku](#how-to-host-bot-on-heroku)
- [Resources](#resources)

# Database

The bot uses a simple SQLite database consisting of a single table: `REMINDERS`

Table Structure:
- `CHATID`: Unique chat ID associated with the user.
- `USRNAME`: Telegram username of the user.
- `ITEM`: The item the user has added to their personal list.

Whenever a user adds or removes items from their list, the changes are immediately reflected in the database (insertions or deletions from the `REMINDERS` table).

To inspect or manage the database, you can use [DB Browser for SQLite](https://sqlitebrowser.org) to easily manage CRUD operations in SQLite databases via a graphical interface.

### Note

A local `.sqlite` database isn’t ideal for a finalized product. That said, SQLite was intentionally chosen for this side project to keep the setup simple and lightweight. It requires no external services, making it easy for anyone to run the bot locally or on platforms like Heroku without extra configuration.

# Bot usage

- ⭕ Developer
    - `/about`: to see info about developer
    
- 📝 List
    - `/addtolist <item>`: to add one or several items to your personal list.
    - `/rmfromlist <item>`: to remove  one or several items from your personal list.
    - `/show_list`: it shows all items in your personal list.
    - `/clear_list`: to delete all items from your personal list.

- 🔀 Random value
    - `/random <number>`: it will return a random number between 0 and <number>.

- ⏰ Alarm
    - `/timer <seconds>`: to set a timer and wait for your message.
    
- 🤖 Info about bot
    - `/help`:  to have info about all commands.

# How to host BOT on Heroku

1. Register on [Heroku](https://www.heroku.com/).
2. Download and install [Heroku CLI](https://devcenter.heroku.com/articles/getting-started-with-python#set-up) and [git](https://git-scm.com/downloads).
3. Create a project folder and put inside it the following files
        
       bot.py
       Procfile
       runtime.txt
       requirements.txt
       
   You can also have a `app.json` schema in order to declare environment variables, add-ons, and other information required to run an app on Heroku. More info [here](https://devcenter.heroku.com/articles/app-json-schema).

4. Put inside `Procfile`

       worker: python script.py
   
5. Put the python version you want to use in `runtime.txt`. 
   
    For instance, if you want to use Python `v3.6.6` just put inside the file:
   
       python-3.6.6

6. Specify explicit dependencies versions inside `requirements.txt`.
   
   For instance, I'm using [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) API.
   So my file `requirements.txt` will look like 
   
       python-telegram-bot==8.1.1
       
   To update this file, you can use the `pip freeze` command in your active virtual environment:
   
       pip freeze > requirements.txt
       
   More info [here](https://devcenter.heroku.com/articles/python-runtimes#selecting-a-runtime).
   
7. If you haven't already, log in to your Heroku account and follow the prompts to create a new SSH public key
   
       heroku login
   
8. Create git repository   

       git init
           
    or clone this repo
    
       git clone https://github.com/J4NN0/j4nn0-b0t.git
   
9. Create heroku app
   
       heroku create
   
10. Push your code (or deploy changes) into heroku app
   
        git add .
        git commit -m 'message'
        git push heroku master

11. Run your worker

        heroku ps:scale worker=1

12. Check logs with and enjoy your bot

        heroku logs --tail

# Resources

- [Your first bot](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions---Your-first-Bot)
- [Python Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [Code snippets](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#general-code-snippets)
- Officilia Telegram Bot docs
    - [Telegram Bot API](https://core.telegram.org/bots/api#forcereply)
    - [Telegram Bot’s documentation](https://python-telegram-bot.readthedocs.io/en/stable/index.html)
- [Getting Started on Heroku with Python](https://devcenter.heroku.com/articles/getting-started-with-python#set-up)
- [Sqlite3](https://docs.python.org/2/library/sqlite3.html)
