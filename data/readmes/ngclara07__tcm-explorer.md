<!-- README Documentation: Own Laptop (Local Machine Environment) -->

# TCM Explorer – Web Application Documentation
## A Node.js + MySQL web platform for querying Traditional Chinese Medicine (TCM) knowledge graphs

## 📌 Overview

TCM Explorer is a lightweight Node.js web application designed to explore structured TCM knowledge, including:

* Herbs
* Ingredients
* Protein targets
* Diseases
* Therapeutic class associations
* Toxicity and safety relationships

The app provides interactive dashboards, research question visualisations, and SQL-powered insights.
This document explains how to install, configure, and run the application from scratch.

# 📁 Project Structure

```php
tcm-webapp/
│
├── routes/
│   └── index.js           # All route handlers & SQL queries
│
├── views/
│   ├── dashboard.ejs      # Main dashboard page
│   ├── RQ1.ejs … RQ5.ejs  # Research Question pages
│   ├── partials/          # Header & footer templates
│
├── public/
│   └── css / js           # Static assets
│
├── data/                  # CSV files for loading MySQL tables
│
├── app.js                 # Express app setup
├── package.json           # Dependencies
├── package-lock.json      # Lock file
├── db.js                  # MySQL connection
├── schema.sql             # MySQL schema
├── .env                   # Environment variables
└── readme.md              # Documentation
```

## 🛠️ 1. System Requirements

| Component | Version | 
| --------- | ------- |
| Node.js | v16+ |
| MySQL | v8+ |
| npm | v8+ |
| OS | Windows / macOS / Linux |

## 🗄️ 2. Database Setup

Step 2.1 — Create the MySQL database

```sql
CREATE DATABASE tcm_db;
USE tcm_db;
```

Step 2.2 — Import your normalised tables

Each CSV should be cleaned before loading.

Example loading command:

```sql
LOAD DATA LOCAL INFILE 'path/to/Ingredient_Main_clean.csv'
INTO TABLE ingredient_main
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
```

Ensure MySQL allows local imports:

```ini
[mysqld]
local_infile=1

[mysql]
local_infile=1
```
Restart MySQL afterwards

#Step 2.3 — Create a restricted MySQL user

The web application must not connect using root.

```sql
CREATE USER 'tcm_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT SELECT ON tcm_db.* TO 'tcm_user'@'localhost';
FLUSH PRIVILEGES;
```

## 🌐 3. Configure Application

Create a .env file in the project root:

```init
DB_HOST=localhost
DB_USER=tcm_user
DB_PASS=your_password
DB_NAME=tcm_db
PORT=3000
``` 

## 📦 4. Install Dependencies

In the project directory:

```bash
npm install
```

This installs:

* express
* mysql2
* dotenv
* ejs
* chart.js (client-side)

## ▶️ 5. Start the Web Application

Run:

```bash
npm start
```

or

```bash
node app.js
```

If successful, you should see:

```nginx
TCM Explorer running on http://localhost:3000
```

Open your browser and visit:

👉 http://localhost:3000

## 📊 6. Application Features

6.1 Dashboard

Displays:

* Total number of herbs, ingredients, diseases, targets
* Preview tables (50 rows each)
* Links to research question pages

6.2 Research Question Pages (RQ1–RQ5)

| RQ | Description | Output |
| -- | ----------- | ------ |
| RQ1 | Disease–herb coverage | Bar chart + table | 
| RQ2 | Herbal Polypharmacy Index | Ranking table
| RQ3 | Drug-like ingredients | Filtered ingredient–target profile
| RQ4 | Herbs with most therapeutic class diversity | Table + bar chart
| RQ5 | Toxic herbs and their therapeutic classes | Chart + table

Each page shows:

* SQL query
* Table of results
* Visualisation (Chart.js)

## 🔐 7. Security Considerations

✔ Dedicated least-privilege MySQL user
✔ App uses prepared statements via mysql2
✔ .env protects sensitive credentials
✔ Server validates inputs for all dynamic queries

## 🛠️ 8. Troubleshooting

❗ Local infile not allowed

Enable in MySQL:

```sql
SET GLOBAL local_infile = 1;
```

❗ ingredients.forEach is not a function

Cause: SQL query returned a single object instead of array.
Fix: Use destructuring correctly:

```js
const [ingredients] = await db.query("...");
```

❗ Broken ingredient CSV

Ensure CSV cleaned before loading (no multi-line cells, no commas without quotes).

📌 9. Future Extensions

* API endpoints for RQ results
* Searchable herb & ingredient library
* Knowledge graph visualisation
* Authentication system

## ✅ 10. Summary

This README provides complete instructions to:

1. Install dependencies
2. Set up MySQL database
3. Load cleaned datasets
4. Configure secure environment variables
5. Run the Node.js application
6. Understand core features and research modules
