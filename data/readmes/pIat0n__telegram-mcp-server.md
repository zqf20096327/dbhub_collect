# Telegram Secure MCP Server

The ultimate Model Context Protocol (MCP) server for Telegram, designed specifically to empower AI Agents (like Claude, Gemini, etc.) with secure, real-time, and multimodal access to your Telegram account.

Unlike other Telegram MCP implementations, this project focuses heavily on **privacy, cross-platform stability, multimodal native support, and performance**. 

## Why Choose Us? (Killer Features)

1. **Native Multimodal Audio & Video Parsing**: 
   AI Agents traditionally struggle with raw `.ogg` voice messages or proprietary Telegram video notes. Our server uses a bundled `ffmpeg` binary (via `imageio-ffmpeg`) to intercept and on-the-fly package audio files into standard `.mp4` containers. This allows advanced multimodal neural networks to natively "hear" and "see" the files without relying on unstable third-party APIs like Google Speech Recognition. It is completely cross-platform!
2. **AES-256 Memory Encryption**: 
   Your Telegram API keys and Session strings are extremely sensitive. Most MCPs leave them as plain `.env` files. We built an interactive `encrypt_setup.py` that derives an AES-256 key from a 4-digit PIN using PBKDF2. Your session is decrypted strictly into memory at runtime—no plain text keys ever touch the disk!
3. **Draft Support & Safety Boundaries**:
   AI agents can safely compose replies by utilizing the `save_draft` tool. You can review the draft in your Telegram app before sending it manually. Furthermore, this MCP is hardcoded to completely block access to Private Messages (DMs) and Bots. Only Group and Supergroup chats are accessible, providing an airtight security perimeter.
4. **Radar Mode (Real-Time Waiting)**:
   Say goodbye to API polling loops. Our server uses `asyncio.Event` to halt the AI's execution thread and instantly wake it up the millisecond a new message arrives in a specified chat.
5. **Ultra-Fast SQLite Caching**:
   We parse incoming messages locally in a background process, ensuring that the AI can instantly search the local SQLite database for context without constantly hammering the Telegram API.

---

## Prerequisites

- Python 3.9+ 
- macOS, Linux, or Windows
- A Telegram API ID and Hash (obtainable at [my.telegram.org](https://my.telegram.org))

*(Note for Linux users without a Desktop Environment: the PIN entry system utilizes `tkinter`. If you are running on a headless server, ensure `python3-tk` is installed and an X11/Wayland display is forwarded, or modify the code to use standard `input()`)*

## Installation (Cross-Platform)

1. Clone this repository.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your Telegram API credentials:
   ```env
   TELEGRAM_API_ID=12345678
   TELEGRAM_API_HASH=your_api_hash_here
   TELEGRAM_SESSION_NAME=master_account
   ```
4. Run the secure setup script to authenticate and encrypt your session:
   ```bash
   python encrypt_setup.py
   ```
   You will be asked to log in to Telegram via your phone number and verification code. After a successful login, a native GUI prompt will ask you to create a **4-digit PIN**. Your session will be encrypted to `config.enc` and you will be prompted to safely delete the `.env` and `.session` files.

## Running the Server

You can plug this server into your preferred MCP client (such as Claude Desktop, Cursor, or Antigravity IDE) by passing your environment's python executable pointing to `main.py`:

```json
{
  "mcpServers": {
    "TelegramMCP": {
      "command": "/path/to/your/venv/bin/python",
      "args": ["/path/to/Telegram-MCP-Release/main.py"]
    }
  }
}
```

Upon launching the MCP server, a small window will appear requesting your 4-digit PIN. Once entered, the server starts serving tools to your AI!

## Available Tools

- `list_my_chats`: List all group chats available to the AI.
- `find_my_chat`: Search for a specific group chat.
- `search_in_my_chats`: Global keyword search spanning the ultra-fast local SQLite cache and the Telegram Cloud.
- `get_chat_messages`: Fetch message history.
- `get_chat_messages_around`: Fetch context above and below a specific message.
- `get_chat_messages_after`: Fetch messages sequentially after a specific message.
- `search_global_public_chats`: Find public Telegram groups.
- `get_chat_info`: Detailed info about a chat.
- `download_message_media`: Downloads photos, documents, and intelligently converts `.ogg` voice notes to `.mp4` for direct AI ingestion.
- `send_message`: Send messages to permitted chats.
- `save_draft`: Save a composed message as a draft for human review.
- `wait_for_new_messages`: Suspends the AI until a new message arrives (Radar Mode).
