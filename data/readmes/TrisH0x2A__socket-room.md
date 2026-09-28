<div align="center">
  <h1>Socket Room</h1>
  <p>A sleek, retro-terminal styled real-time chat application.</p>
  
  <p>
    <img src="https://img.shields.io/badge/Made_by-Trish0x2a-00ff00?style=for-the-badge&logo=github" alt="Author" />
    <img src="https://img.shields.io/badge/C-00599C?style=for-the-badge&logo=c&logoColor=white" alt="C" />
    <img src="https://img.shields.io/badge/Svelte-FF3E00?style=for-the-badge&logo=svelte&logoColor=white" alt="Svelte" />
    <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
    <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="License" />
  </p>
</div>

## Features
- **Fast Backend**: Written entirely in C using Mongoose.
- **Retro UI**: A beautiful, glowing terminal aesthetic built with Svelte & Vite.
- **Real-time WebSockets**: Instantaneous message delivery and live typing indicators.
- **Secure**: Features robust rate-limiting, cryptographically secure tokens (`/dev/urandom`), and SQL injection protection.
- **Room Support**: Join multiple distinct chat rooms.
- **Persistent Storage**: All messages and accounts are safely stored in a local SQLite database.

## Tech Stack
- **Backend**: C, Mongoose (HTTP/WS server), SQLite3
- **Frontend**: Svelte, Vite, Vanilla CSS

## Quick Start

### Prerequisites
- GCC (or equivalent C compiler)
- `make`
- Node.js & `pnpm` (for building the frontend)

### Build & Run
1. **Install Frontend Dependencies:**
   ```bash
   make install-web
   ```
2. **Build the Frontend:**
   ```bash
   make frontend
   ```
3. **Build & Run the Server:**
   ```bash
   make run-server
   ```
4. **Visit:** `http://localhost:8080`

### Development
To run the frontend dev server with hot-module replacement:
```bash
make run-web
```

## License
This project is open-sourced under the MIT License. See the [LICENSE](LICENSE) file for details.

---
