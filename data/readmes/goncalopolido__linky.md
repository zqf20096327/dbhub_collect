# Linky

A minimalist URL shortening app.

<p align="center">
  <img src="https://github.com/user-attachments/assets/199bdcab-65c7-47b8-8f71-f71ca7ccf769" alt="Linky Preview">
</p>

---

## Features

* Custom short URLs for memorable links.
* Duplicate prevention, ensuring identical URLs always generate the same short code.
* Automatic dark and light theme based on the user's system preferences.
* Fully responsive interface for all devices.
* SQLite database for lightweight and reliable storage.
* Express.js backend with efficient request routing.

---

## Requirements

* Node.js
* npm

> [!TIP]
> Using the latest LTS version of Node.js is recommended for the best compatibility and performance.

---

## Quick Start

Clone the repository:

```bash
git clone https://github.com/goncalopolido/linky
```

Navigate to the project directory and install the dependencies:

```bash
cd linky
npm install
```

Start the application:

```bash
npm start
```

> [!IMPORTANT]
> Ensure all dependencies have been installed successfully before starting the server. Otherwise, the application will fail to launch.

Once the server is running, Linky will be available at:

```text
http://localhost:3000
```

---

## Live Demo

> [!WARNING]
> The public demo has been disabled due to repeated abuse. Even with all shortened URLs automatically expiring every 10 minutes, the service continued to be misused.
>
> ~~**[linky.polido.pt](https://linky.polido.pt)**~~
>
> There are currently no plans to bring it back. If a more suitable solution is implemented in the future, the demo may return.

---

## Technical Details

Linky uses:

* **Express.js** for the backend server.
* **better-sqlite3** for SQLite database operations.
* **CSS** for styling without external frameworks.
* **JavaScript** for frontend functionality.

---

## Notes

> [!TIP]
> If you are self-hosting Linky, you can modify or completely disable the URL expiration policy to better suit your own deployment.

> [!WARNING]
> If the SQLite database is deleted or becomes corrupted, all existing shortened URLs will be permanently lost unless regular backups are maintained.
