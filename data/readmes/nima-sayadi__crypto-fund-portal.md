# crypto-fund-portal

A crypto investment fund platform written in plain PHP. One of my earliest projects, built back in 2022. It is written with passion, without the use of any frameworks.

Investors can buy and redeem units in three USDT-based crypto funds (low, medium and high risk). Admins set each fund's daily unit price (NAV), approve every transaction, and track each investor's holdings.

## Features

**Investor side**
- Passwordless sign-up and login with a 6-digit email code
- Buy units by sending USDT to the fund's wallet (TRC20, ERC20 or BEP20) and attaching a transaction link or screenshot, with an optional maximum price
- Redeem units to a pre-approved withdrawal wallet, with an optional minimum price
- Per-fund statement (cardex) showing purchases, sales, remaining units and redemption fees
- Fund performance pages with interactive NAV charts and returns over 1 day, 1 week, and 1, 3, 6 and 12 months
- Investor profile questionnaire, wallet management, support tickets with attachments, and notifications

**Admin side**
- Daily NAV entry for each fund
- Approve or reject buy and sell requests; redemptions are matched against the investor's oldest units first (FIFO) and the per-unit redemption fee is deducted
- Manage fund wallets, redemption fees, fund names, users, investor wallets, tickets and admin accounts (super admin and admin roles)

## Tech stack
PHP with MySQLi prepared statements, MySQL/MariaDB, jQuery/AJAX, Highcharts (Highstock), Jalali (Persian) dates, RTL Persian interface.

## Getting started
1. Import `website.sql` into MySQL/MariaDB.
2. Set your database credentials in `DB/db.php`.
3. Serve the project from the web root on Apache with `mod_rewrite` enabled.

**Important:** This repository is not suitable for quick deployment and requires further improvements. For example, the login code is never actually emailed (it is only stored in the database), and the database credentials are hard-coded. It is a good repository for junior full-stack developers and a good start for seeing how a complete app works without a framework.

**EDIT:** Nowadays, with AI, this repo may not be that valuable anymore. However, keep in mind that if you learn from scratch and build your own stuff, you can become a senior developer who catches the AI's mistakes and can effectively fine-tune AI agents ;)

Enjoy!
