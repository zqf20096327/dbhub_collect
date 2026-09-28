<p align="center">
  <img src="src-tauri/icons/128x128@2x.png" alt="GeminiSQL Logo" width="80" height="80">
</p>

<p align="center">
  <img src="designs/logo-text.svg" alt="GeminiSQL" width="300">
</p>

<p align="center">
  <strong>A modern, cross-platform SQL editor with AI-powered query generation</strong>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#screenshots">Screenshots</a> •
  <a href="#installation">Installation</a> •
  <a href="#development">Development</a> •
  <a href="#roadmap">Roadmap</a>
</p>

---

## Overview

GeminiSQL is a lightweight, fast, and intuitive SQL editor built with modern technologies. It combines the power of a native desktop application with AI capabilities to help you write SQL queries faster and more efficiently.

Built with **Tauri 2.0**, **React 19**, and **Rust**, GeminiSQL delivers a native experience with minimal resource usage while providing powerful features for database management.

## Features

### Core Features

- **Multi-tab Query Editor** - Work on multiple queries simultaneously with a tabbed interface
- **Intelligent SQL Autocomplete** - Context-aware suggestions for tables, columns, and SQL keywords
- **Schema Browser** - Explore database tables, columns, and relationships at a glance
- **Query Results Viewer** - View query results in a fast, virtualized table with column type indicators
- **Save & Organize Queries** - Save frequently used queries for quick access
- **Query History** - Access previously executed queries with timestamps and execution times

### AI-Powered Features

- **AI Query Generation** - Describe what you need in plain English, get SQL queries instantly
- **Query Explanation** - Understand what generated queries do with AI-powered explanations
- **Multiple AI Models** - Choose from Gemini 2.5 Pro, Gemini 2.5 Flash, or Gemini 3 Pro Preview
- **Schema-Aware Generation** - AI understands your database structure for accurate query generation

### User Experience

- **Dark/Light Theme** - Easy on the eyes with system theme detection
- **Keyboard Shortcuts** - Run queries (Cmd+Enter), save (Cmd+S), and more
- **Connection Management** - Save multiple database connections with color coding
- **Real-time Connection Status** - Always know your connection state

## Screenshots

### SQL Editor with Autocomplete
![SQL Editor](designs/img-1.png)
*Intelligent autocomplete with table and column suggestions*

### Save Query Dialog
![Save Query](designs/img-2.png)
*Organize your queries with names and descriptions*

### AI Assistant
![AI Assistant](designs/img-3.png)
*Generate SQL queries from natural language descriptions*

## Installation

### Download

Download the latest release for your platform from the [Releases](https://github.com/yourusername/geminisql/releases) page.

| Platform | Download |
|----------|----------|
| macOS (Apple Silicon) | `GeminiSQL_x.x.x_aarch64.dmg` |
| macOS (Intel) | `GeminiSQL_x.x.x_x64.dmg` |
| Windows | `GeminiSQL_x.x.x_x64-setup.exe` |
| Linux (Debian/Ubuntu) | `GeminiSQL_x.x.x_amd64.deb` |
| Linux (AppImage) | `GeminiSQL_x.x.x_amd64.AppImage` |

### Build from Source

See the [Development](#development) section below.

## Development

### Prerequisites

- [Node.js](https://nodejs.org/) (v18 or later)
- [Rust](https://www.rust-lang.org/tools/install) (latest stable)
- [Tauri CLI](https://tauri.app/v1/guides/getting-started/prerequisites)

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/geminisql.git
cd geminisql

# Install dependencies
npm install

# Run in development mode
npm run tauri dev

# Build for production
npm run tauri build
```

### Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 19, TypeScript, Tailwind CSS |
| Editor | CodeMirror 6 |
| State Management | Zustand |
| Backend | Rust, Tauri 2.0 |
| Database Drivers | SQLx (MySQL) |
| AI Integration | Google Gemini API |

## Configuration

### Google API Key (Required for AI Assistant)

To use the AI-powered query generation feature, you need to create a Google API key:

1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the generated API key
5. In GeminiSQL, click the **Settings** icon (gear) in the top-right corner
6. Paste your API key in the **"Google API Key"** field
7. Select your preferred AI model (Gemini 2.5 Pro, 2.5 Flash, or 3 Pro)

![Settings Page](designs/img-4.png)
*Settings page with API key and model selection*

> **Note:** API usage costs are billed directly to your Google account. GeminiSQL does not store or proxy your API requests - all AI calls are made directly from your device to Google's API. Check [Google AI pricing](https://ai.google.dev/pricing) for current rates.

### Database Connection

1. Click "New Connection" in the header
2. Select MySQL as the database type
3. Enter your connection details
4. Click "Test Connection" to verify
5. Click "Save & Connect"

## Roadmap

### Upcoming Features

- [ ] **PostgreSQL Support** - Full support for PostgreSQL databases
- [ ] **SSH Tunneling** - Connect to databases through SSH tunnels for secure remote access
- [ ] **Additional LLM Providers** - Support for OpenAI, Anthropic Claude, and other AI providers
- [ ] **Query Formatter** - Auto-format SQL queries for better readability
- [ ] **Export Results** - Export query results to CSV, JSON, and Excel formats

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Tauri](https://tauri.app/)
- SQL editing powered by [CodeMirror](https://codemirror.net/)
- AI capabilities powered by [Google Gemini](https://ai.google.dev/)
- Icons from [Lucide](https://lucide.dev/)

---

<p align="center">
  <strong>100% vibe coded with <a href="https://claude.ai/claude-code">Claude Code</a></strong>
</p>

<p align="center">
  Made with Rust and React
</p>
