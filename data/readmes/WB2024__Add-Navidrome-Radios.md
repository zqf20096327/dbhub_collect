# [![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Support-yellow?logo=buy-me-a-coffee)](https://buymeacoffee.com/succinctrecords)

# 🎵 Navidrome Radio Station Manager

A powerful CLI tool to search, browse, and manage internet radio stations for [Navidrome](https://www.navidrome.org/) using the [Radio-Browser](https://www.radio-browser.info/) API.

![Python](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Navidrome](https://img.shields.io/badge/Navidrome-Compatible-orange.svg)

## ✨ Features

- 🔍 **Multiple Search Options**
  - Search by station name
  - Search by genre/tag (jazz, rock, classical, etc.)
  - Search by country
  - Browse top voted stations

- 📄 **Pagination**
  - Navigate through results 10 at a time
  - Jump to specific pages
  - Never lose track with global numbering

- ✅ **Flexible Selection**
  - Select individual stations
  - Select ranges (e.g., 1-5)
  - Select all on current page
  - Multi-select across pages

- 🎯 **Smart Management**
  - Duplicate detection (won't add existing stations)
  - No Navidrome restart required
  - Direct database integration
  - View existing stations

- �️ **Debugging Tools**
  - Verbose debug mode with `--debug` flag
  - Database schema inspection
  - Side-by-side station comparison
  - Full error stack traces

- 🔧 **Easy Configuration**
  - Auto-saves database path on first run
  - No need to edit the script
  - Cross-platform config storage
  - Change path anytime via menu

- �🖥️ **User-Friendly Interface**
  - Clean CLI with intuitive commands
  - Visual selection markers
  - Progress feedback
  - Summary reports

## 📋 Prerequisites

- Python 3.6 or higher
- Navidrome installed and running
- Access to Navidrome's SQLite database
- Internet connection (for Radio-Browser API)

### Python Dependencies

```bash
pip3 install requests
```

That's it! The script only requires the `requests` library. All other dependencies are part of Python's standard library.

## 🚀 Installation

### Quick Install

```bash
# 1. Download the script
curl -o /usr/local/bin/navidrome-radio https://raw.githubusercontent.com/WB2024/Add-Navidrome-Radios/main/navidrome-radio.py

# 2. Make it executable
sudo chmod +x /usr/local/bin/navidrome-radio

# 3. (Optional) Create an alias
echo "alias nr='navidrome-radio'" >> ~/.bashrc
source ~/.bashrc
```

### Manual Install

```bash
# 1. Clone the repository
git clone https://github.com/WB2024/Add-Navidrome-Radios.git
cd Add-Navidrome-Radios

# 2. Copy to /usr/local/bin
sudo cp navidrome-radio.py /usr/local/bin/navidrome-radio

# 3. Make it executable
sudo chmod +x /usr/local/bin/navidrome-radio

# 4. (Optional) Create an alias
echo "alias nr='navidrome-radio'" >> ~/.bashrc
source ~/.bashrc
```

## ⚙️ Configuration

### First-Time Setup

On first run, the script will prompt you to enter your Navidrome database path. This is saved automatically and remembered for future runs:

```
📌 FIRST-TIME SETUP: Database Path Required
======================================================================

This tool needs to know the location of your Navidrome database.

Common locations:
  Docker:  /path/to/navidrome/data/navidrome.db
  Linux:   /var/lib/navidrome/navidrome.db
  Windows: C:\ProgramData\Navidrome\navidrome.db

Enter full path to navidrome.db: _
```

### Config File Locations

| OS | Location |
|-----|----------|
| Linux/Mac | `~/.config/navidrome-radio/config.json` |
| Windows | `%APPDATA%\navidrome-radio\config.json` |

### Changing Database Path

You can change the database path anytime:

1. **Via menu:** Select option 4 "Change database path"
2. **Via command line:** `navidrome-radio --reset-config`
3. **Override once:** `navidrome-radio /path/to/other/navidrome.db`

**To find your Navidrome database path:**

If using Docker, check your docker-compose.yml for the volume mount to `/data`:

```yaml
volumes:
  - /your/path/to/navidrome/data:/data
```

Your database will be at `/your/path/to/navidrome/data/navidrome.db`

## 📖 Usage

### Basic Usage

```bash
# Run normally (uses saved database path, prompts on first run)
navidrome-radio

# Run with custom database path (one-time override)
navidrome-radio /path/to/navidrome.db

# Show help
navidrome-radio --help
```

### Debug Mode

```bash
# Enable verbose debug logging
navidrome-radio --debug

# Debug mode with custom path
navidrome-radio --debug /path/to/navidrome.db
```

Debug mode shows:
- Exact values being inserted into the database
- Generated IDs and timestamps  
- SQL execution details
- Full stack traces on errors

### Configuration Commands

```bash
# Reset saved configuration (will prompt for path again)
navidrome-radio --reset-config

# Show current config and help
navidrome-radio --help
```

### Using the Alias (if configured)

```bash
nr
```

## 🎮 Interactive Guide

### Main Menu

```
📁 Database: /path/to/navidrome.db

MAIN MENU

1. Search and add radio stations
2. View existing stations in database
3. Inspect database (debug)
4. Change database path
5. Exit
```

### Database Inspection Menu

Option 3 opens the debug inspection menu:

```
🔍 DATABASE INSPECTION (Debug)

1. View radio table schema
2. View latest station details (all columns)
3. Search and view station details
4. Compare two stations side by side
5. Back to main menu
```

This is useful for troubleshooting when stations don't appear in Navidrome.

### Search Options

```
🔍 SEARCH RADIO STATIONS

1. Search by name
2. Search by genre/tag
3. Search by country
4. Browse top voted stations
5. Back to main menu
```

### Navigation Commands

When browsing search results:

| Command | Description |
|---------|-------------|
| `[number]` | Toggle selection for a specific station (e.g., `25`) |
| `[n1-n2]` | Select a range on current page (e.g., `1-5`) |
| `n` or `next` | Go to next page |
| `p` or `prev` | Go to previous page |
| `page [n]` | Jump to specific page (e.g., `page 5`) |
| `all` | Select all stations on current page |
| `none` | Deselect all stations |
| `add` | Add selected stations to Navidrome |
| `back` | Return to search menu |

## 💡 Examples

### Example 1: Search by Country

```
Select option: 1
Enter country: UK

✅ Found 450 stations!

Page 1 of 45 (Showing 1-10 of 450)
Selected: 0 station(s)

[ ] 1. BBC Radio 1                                      (Page #1)
    Country: UK           Tags: pop, rock
    Bitrate: 320 kbps | Votes: 1250
[ ] 2. BBC Radio 2                                      (Page #2)
    Country: UK           Tags: pop, variety
    Bitrate: 320 kbps | Votes: 980
...

Commands: 1-5      (select range on page)
         25        (select station #25)
         n         (next page)
         add       (add selected to Navidrome)
```

### Example 2: Search by Genre

```
Select option: 2
Enter genre/tag: jazz

✅ Found 127 stations!

Select stations and use 'add' to import to Navidrome
```

### Example 3: Quick Selection Workflow

```
1. Search for "classical" stations
2. Type "1-5" to select first 5 stations
3. Type "n" to go to next page
4. Type "3" to also select station #13
5. Type "add" to import all selected
6. Refresh Navidrome web interface - stations appear immediately!
```

## 🐳 Docker Users

If you're running Navidrome in Docker, make sure you're accessing the database file on the **host**, not inside the container.

### Finding Your Database Path

Check your `docker-compose.yml`:

```yaml
services:
  navidrome:
    volumes:
      - /srv/navidrome/data:/data
      - /srv/music:/music:ro
```

Your database is at: `/srv/navidrome/data/navidrome.db`

## 🔧 Troubleshooting

### "Database not found" Error

**Problem:** Script can't find the database file.

**Solution:**
1. Verify your database path is correct
2. Check file permissions: `ls -l /path/to/navidrome.db`
3. If using Docker, ensure you're using the host path, not container path

### Stations Don't Appear in Navidrome

**Problem:** Added stations but don't see them in the web interface.

**Solution:**
1. Refresh your browser (hard refresh: Ctrl+F5)
2. Clear browser cache
3. Restart Navidrome (especially with Docker)
4. Verify stations were added: Run option 2 in main menu

**If stations still don't appear, use debug mode to diagnose:**

```bash
# Run with debug flag
navidrome-radio --debug

# Then use option 3 "Inspect database" to:
# 1. View the radio table schema (check for missing columns)
# 2. Compare a working station (added via web UI) with a CLI-added one
```

This comparison can reveal if Navidrome's schema has changed and requires additional columns.

### "Error searching Radio-Browser" Message

**Problem:** Can't connect to Radio-Browser API.

**Solution:**
1. Check your internet connection
2. Radio-Browser may be temporarily down
3. Try again in a few minutes
4. Try a different search term

### Permission Denied

**Problem:** Can't write to database.

**Solution:**
```bash
# Check database permissions
ls -l /path/to/navidrome.db

# If needed, adjust permissions (be careful!)
sudo chmod 664 /path/to/navidrome.db

# Or run script with appropriate user
sudo -u navidrome navidrome-radio
```

## 🗂️ File Structure

```
Add-Navidrome-Radios/
├── navidrome-radio.py    # Main script
├── README.md             # This file
└── LICENSE               # MIT License
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Ideas for Contributions

- [ ] Add support for importing from M3U/PLS playlist files
- [ ] Export selected stations to JSON
- [ ] Filter by bitrate/codec
- [ ] Sort results (by votes, bitrate, name)
- [ ] Delete stations from database
- [ ] Edit existing station details
- [ ] Batch operations (import all from genre)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Navidrome](https://www.navidrome.org/) - Amazing self-hosted music server
- [Radio-Browser](https://www.radio-browser.info/) - Community-driven radio station database
- All contributors and users of this tool

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/WB2024/Add-Navidrome-Radios/issues)
- **Discussions:** [GitHub Discussions](https://github.com/WB2024/Add-Navidrome-Radios/discussions)

## 🌟 Star History

If you find this tool useful, please consider giving it a star! ⭐

## 📸 Screenshots

### Main Menu
```
================================================================================
🎵  NAVIDROME RADIO STATION MANAGER  🎵
================================================================================

📁 Database: /srv/navidrome/data/navidrome.db

MAIN MENU

1. Search and add radio stations
2. View existing stations in database
3. Inspect database (debug)
4. Change database path
5. Exit
```

### Search Results with Pagination
```
📻 FOUND 450 STATIONS - SELECT TO ADD
Page 1 of 45 (Showing 1-10 of 450)
Selected: 3 station(s)

[✓] 1. BBC Radio 1                                      (Page #1)
     Country: UK           Tags: pop, rock
     Bitrate: 320 kbps | Votes: 1250
[ ] 2. BBC Radio 2                                      (Page #2)
     Country: UK           Tags: pop, variety
     Bitrate: 320 kbps | Votes: 980
```

### Success Summary
```
================================================================================
📊 SUMMARY: 15 added, 2 skipped
================================================================================

💡 Refresh your Navidrome web interface to see the new stations!
```

## 🔄 Changelog

### Version 1.1.0 (2026-02-25)
- Added `--debug` flag for verbose logging
- Added database inspection menu (schema viewer, station comparison)
- Added persistent configuration file (no more editing the script!)
- Added `--reset-config` option
- Added option to change database path from menu
- Improved error messages with debug stack traces
- Auto-prompts for database path on first run

### Version 1.0.0 (2026-02-17)
- Initial release
- Search by name, genre, country
- Browse top voted stations
- Pagination support (10 items per page)
- Multi-select functionality
- Duplicate detection
- Direct database integration

---

**Made with ❤️ for the Navidrome community**
