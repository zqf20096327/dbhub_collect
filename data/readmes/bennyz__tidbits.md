# Tidbits 📚

A Firefox browser extension for saving and organizing interesting excerpts from around the web.

## Features

- **Easy Saving**: Select any text on a webpage, right-click, and save it as a tidbit
- **Cloud Sync**: Automatically syncs across all your Firefox browsers via Firefox Sync
- **Organized Collection**: Browse all your saved excerpts in one place
- **Tagging System**: Categorize tidbits with custom tags
- **Search & Filter**: Quickly find tidbits by searching text or filtering by tags
- **Random Discovery**: Click the random button to rediscover forgotten gems
- **Favorites**: Star your most important tidbits
- **Source Tracking**: Every tidbit saves the source URL and page title
- **Storage Monitor**: Real-time display of sync storage usage with warnings
- **Export**: Download your entire collection as JSON

## Installation

### Install from Source (Development)

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd tidbits
   ```

2. **Create Icons** (optional but recommended)
   ```bash
   # Option 1: Using Python
   pip install Pillow
   python3 create-icons.py

   # Option 2: Manually create 48x48 and 96x96 PNG files
   # Place them in the icons/ directory
   ```

3. **Load the extension in Firefox**
   - Open Firefox and navigate to `about:debugging`
   - Click "This Firefox"
   - Click "Load Temporary Add-on"
   - Navigate to the extension directory and select `manifest.json`

   **Note**: Temporary extensions are removed when Firefox closes. For permanent installation during development:
   - Use [Firefox Developer Edition](https://www.mozilla.org/firefox/developer/) or [Firefox Nightly](https://www.mozilla.org/firefox/nightly/)
   - Or sign and install the extension (see "Building for Production" below)

### Building for Production

To create a signed extension for permanent installation:

1. **Package the extension**
   ```bash
   # Remove unnecessary files
   zip -r tidbits.zip . -x "*.git*" "create-icons.py" "icons/create-icons.html" "icons/README-ICONS.txt"
   ```

2. **Sign the extension**
   - Go to [addons.mozilla.org](https://addons.mozilla.org/developers/)
   - Create a developer account if you don't have one
   - Submit your extension for signing
   - Once approved, you can install the signed .xpi file permanently

### Enable Firefox Sync (Recommended)

To sync your tidbits across devices:

1. **Create a Firefox Account** (if you don't have one)
   - Click the menu button (☰) in Firefox
   - Click "Sign in to Sync"
   - Follow the prompts to create an account

2. **Sign in on all devices**
   - Sign into the same Firefox Account on all your devices
   - Your tidbits will automatically sync

3. **Verify sync is working**
   - Save a tidbit on one device
   - Open the extension on another device - it should appear within seconds

**No Firefox Account?** The extension works fine without sync - your tidbits will be stored locally on each device.

## Usage

### Saving Tidbits

1. **Select text** on any webpage (tweets, articles, quotes, etc.)
2. **Right-click** the selected text
3. **Choose "Save as Tidbit"** from the context menu
4. A notification will confirm the tidbit was saved

### Managing Tidbits

Click the Tidbits extension icon in your browser toolbar to open the popup.

#### Browsing
- All tidbits are displayed in reverse chronological order (newest first)
- Each card shows the text, source, timestamp, tags, and a link to the original page

#### Searching
- Type in the search box to filter tidbits by text content, source, or tags
- Search is real-time and case-insensitive

#### Filtering by Tags
- Use the tag dropdown to show only tidbits with a specific tag
- Combine tag filter with search for precise results

#### Adding Tags
1. Click the 🏷️ (tag) button on any tidbit card
2. Enter tags separated by commas (e.g., `inspiration, quotes, productivity`)
3. Click "Save"

#### Favorites
- Click the ⭐ (star) button to mark/unmark a tidbit as favorite
- Favorite tidbits have a gold border

#### Random Tidbit
- Click the 🎲 (dice) button in the header
- A random tidbit from your filtered collection will be displayed
- Click "Back to All Tidbits" to return to the full list

#### Deleting
- Click the 🗑️ (trash) button on any tidbit card
- Confirm the deletion

#### Exporting
- Click the 💾 (save) button in the header
- Your entire collection will be downloaded as a JSON file
- Filename format: `tidbits-export-YYYY-MM-DD.json`

## File Structure

```
tidbits/
├── manifest.json          # Extension configuration
├── background.js          # Background script (context menu, storage)
├── content.js            # Content script (runs on web pages)
├── popup/
│   ├── popup.html        # Popup interface
│   ├── popup.css         # Popup styles
│   └── popup.js          # Popup functionality
├── icons/
│   ├── icon-48.png       # Extension icon (48x48)
│   └── icon-96.png       # Extension icon (96x96)
├── create-icons.py       # Script to generate icons
└── README.md            # This file
```

## Data Storage & Sync

Tidbits are stored using the Firefox `browser.storage.sync` API. Your data:
- **Automatically syncs** across all your Firefox browsers when signed into your Firefox Account
- **End-to-end encrypted** by Firefox Sync
- **Works offline** - syncs when you're back online
- Can be exported anytime as JSON backup

### Storage Limits

Firefox Sync has storage quotas:
- **Total limit**: ~100KB for sync storage
- **Monitoring**: The extension shows storage usage in the stats bar
- **Warnings**: You'll get notifications if approaching the limit
- **What to do**: Export and delete old tidbits, or use selective tags to manage your collection

The popup displays real-time storage usage (e.g., "15 tidbits • 12.3KB / 100KB used"). A warning indicator (⚠️) appears when using more than 80% of quota.

### Data Format

Each tidbit is stored as:
```json
{
  "id": 1699999999999,
  "text": "The selected text",
  "source": "Page Title",
  "url": "https://example.com/page",
  "tags": ["tag1", "tag2"],
  "timestamp": "2024-01-15T10:30:00.000Z",
  "favorite": false
}
```

## Browser Compatibility

- **Firefox**: Fully supported (Manifest V2)
- **Firefox-based browsers**: Should work (Waterfox, LibreWolf, etc.)
- **Chrome/Edge**: Not compatible (uses Chrome-specific APIs)

## Privacy

This extension:
- ✅ Does not collect any analytics or telemetry
- ✅ Does not send data to any servers (except Firefox Sync when enabled)
- ✅ Does not track your browsing history
- ✅ Only accesses webpage content when you explicitly save a tidbit
- ✅ Uses Firefox Sync's end-to-end encryption for data synchronization
- ✅ Data synced through Mozilla's servers is encrypted - only you can decrypt it

**Note**: When you're signed into Firefox with a Firefox Account, your tidbits automatically sync across your devices using Mozilla's encrypted sync service. You maintain full control and can disable sync anytime in Firefox settings.

## Development

### Prerequisites
- Firefox Developer Edition or Nightly (for persistent development)
- Basic knowledge of HTML, CSS, and JavaScript
- Text editor or IDE

### Making Changes

1. Edit the relevant files
2. Reload the extension in `about:debugging`
3. Test your changes

### Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

[Add your license here]

## Changelog

### Version 1.1.0 (Firefox Sync)
- **NEW**: Automatic cloud sync across all Firefox devices
- **NEW**: Real-time storage quota monitoring in stats bar
- **NEW**: Visual warnings when approaching storage limits
- **NEW**: Error handling for quota exceeded scenarios
- Switched from local storage to Firefox Sync storage
- Updated documentation with sync setup instructions

### Version 1.0.0 (Initial Release)
- Save text excerpts from any webpage
- Browse and search saved tidbits
- Tag-based organization
- Favorites system
- Random tidbit discovery
- Export functionality
- Source tracking with clickable links

## Support

If you encounter issues or have suggestions:
- Open an issue on GitHub
- Include Firefox version and error messages if applicable

## Roadmap

Potential future features:
- Import functionality (restore from JSON)
- Firefox Sync support for cross-device sync
- Bulk operations (delete multiple, tag multiple)
- Dark mode
- Keyboard shortcuts
- Rich text formatting preservation
- Collections/folders
- Advanced search (regex, date ranges)
- Statistics dashboard

---

Made with ❤️ for Firefox users who love collecting knowledge
