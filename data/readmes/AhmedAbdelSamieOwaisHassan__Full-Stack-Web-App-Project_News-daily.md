# NewsDaily

A simple news website built with PHP, MySQL, and Bootstrap. Browse articles, create an account, sign in, and publish articles with images.

## Features

- Browse articles and navigate between pages.
- Create an account and sign in.
- Publish articles and upload their images.
- Arabic and English language support.

## Requirements

- PHP with the `mysqli` extension.
- MySQL / MariaDB or Cloud Database (e.g., TiDB Cloud).
- A local server (like XAMPP) or cloud deployment platform (like Vercel).

## 🗄️ Database & Cloud Deployment

This project is deployed live on **Vercel** using a cloud-hosted MySQL-compatible database.

- **Database Hosting:** Cloud database created and hosted on [TiDB Cloud (PingCAP)](https://docs.pingcap.com/).
- **Deployment Platform:** Hosted on **Vercel** with PHP serverless runtime.
- **Security:** Secure SSL connection configured using Environment Variables on Vercel.

### ⚙️ Environment Variables

To connect to the database (either locally or on Vercel), set up the following environment variables:

- `DB_HOST` - Database host address (e.g., your TiDB Cloud cluster host)
- `DB_USER` - Database username
- `DB_PASSWORD` - Database password
- `DB_NAME` - Database name (`site_news_project`)
- `DB_PORT` - Database port (default: `4000` for TiDB / `3306` for local MySQL)

---

## Run Locally with XAMPP

1. Copy the project into the `htdocs` folder.
2. Start Apache and MySQL from the XAMPP Control Panel.
3. Create a database named `site_news_project` in phpMyAdmin.
4. Import the tables from `db/queries.sql`.
5. Update the database connection settings or `.env` / environment variables to match your local configuration.
6. Open `http://localhost/your-project-folder/` in your browser.

> **Note:** Uploaded article images are stored in `assets/image/postImage/`. Make sure this folder exists and is writable.

---

## Screenshots

| Homepage                                     | Article page                                    |
| -------------------------------------------- | ----------------------------------------------- |
| ![Homepage](assets/screenshots/homepage.png) | ![Article page](assets/screenshots/article.png) |

| Login page                                  | Registration page                                     |
| ------------------------------------------- | ----------------------------------------------------- |
| ![Login page](assets/screenshots/login.png) | ![Registration page](assets/screenshots/register.png) |

| Add post page                                    | Update post page                                       |
| ------------------------------------------------ | ------------------------------------------------------ |
| ![Add post page](assets/screenshots/AddPost.png) | ![Update post page](assets/screenshots/UpdatePost.png) |

GitHub can store and share the project source code, but GitHub Pages does not run PHP or MySQL. To publish the website, upload the files to hosting that supports PHP and MySQL, create the database there, and update the connection settings in `inc/connection.php`. Do not commit real passwords or database credentials to a public repository.
