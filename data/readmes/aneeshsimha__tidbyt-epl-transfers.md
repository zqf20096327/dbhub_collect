# EPL Transfers for Tidbyt

A real-time English Premier League transfer tracker for Tidbyt's 64x32 LED matrix display. Shows recent player transfers with club badges in a sleek LED scoreboard style.

![EPL Transfers](https://img.shields.io/badge/Tidbyt-64x32-brightgreen) ![Starlark](https://img.shields.io/badge/language-Starlark-blue)

## Features

- ⚽ **Live EPL Transfers**: Shows most recent Premier League player transfers
- 🎨 **Club Badges**: Displays official team logos (12x12 pixels)
- 📊 **Transfer Details**: Player name, clubs, transfer type (loan/free/fee)
- 🎬 **Smooth Animations**: Cycles through multiple transfers
- ⚡ **Smart Caching**: Respects API rate limits (1-hour cache)
- 🎮 **User Configuration**: Enter your own API key via Tidbyt app settings

## Screenshots

*App cycles through recent transfers showing badges, player names, and transfer details*

```
┌────────────────────────────────────────────┐
│ EPL XFERS                           ●      │
├────────────────────────────────────────────┤
│                                            │
│        [MUN] → [MCI]                       │
│         Marcus Rashford                    │
│             €75M                           │
│                                            │
└────────────────────────────────────────────┘
```

## Setup

### Prerequisites

1. **Tidbyt Device** - Physical Tidbyt display device
2. **API-Football Key** - Free API key from [api-football.com](https://www.api-football.com/)
   - Sign up for free account
   - Free tier: 100 requests/day (sufficient for this app)
3. **Pixlet CLI** (for local development)
   ```bash
   # macOS
   brew install tidbyt/tidbyt/pixlet

   # Other platforms - download from https://tidbyt.dev
   ```

### Installation

#### Option 1: Install from Tidbyt Mobile App (Recommended)

1. Open the Tidbyt mobile app
2. Go to "Discover Apps"
3. Search for "EPL Transfers"
4. Tap "Install"
5. Enter your API-Football key when prompted
6. Done! Transfers will appear on your Tidbyt

#### Option 2: Local Development

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/tidbyt-epl-transfers.git
   cd tidbyt-epl-transfers
   ```

2. Get your API key from [api-football.com](https://www.api-football.com/)

3. Test locally (replace with your API key):
   ```bash
   pixlet serve epl_transfers.star api_key="YOUR_API_KEY_HERE"
   ```

4. Open browser to `http://localhost:8080` to preview

5. Push to your Tidbyt device:
   ```bash
   pixlet push <device-id> epl_transfers.star api_key="YOUR_API_KEY_HERE"
   ```

   Find your device ID in the Tidbyt mobile app settings.

## Configuration

### API-Football Key

This app requires an API-Football key to fetch transfer data. The free tier (100 requests/day) is sufficient since the app caches data for 1 hour.

**Get Your Key:**
1. Visit [api-football.com](https://www.api-football.com/)
2. Create a free account
3. Navigate to "My Dashboard"
4. Copy your API key
5. Enter it in the Tidbyt app settings for this app

**Rate Limits:**
- Free tier: 100 requests/day
- App caches data for 1 hour
- Maximum daily requests: ~24 (well within limits)

## How It Works

### Data Flow

1. **Fetch Transfers**: Queries API-Football for recent EPL transfers
2. **Cache Data**: Stores results for 1 hour to respect rate limits
3. **Parse Response**: Extracts player names, clubs, transfer types
4. **Fetch Badges**: Downloads club logos (cached for 24 hours)
5. **Render Display**: Creates 64x32 pixel LED display
6. **Animate**: Cycles through transfers every few seconds

### Display Layout

- **Header** (8px tall): "EPL XFERS" with live indicator
- **Divider** (1px): Accent line
- **Transfer Card** (23px tall):
  - Club badges (12x12px each)
  - Arrow between badges
  - Player name (scrolling if long)
  - Transfer type (LOAN, FREE, or fee)

### Caching Strategy

- **Transfer data**: 1 hour cache
- **Club badges**: 24 hour cache
- **HTTP responses**: Pixlet automatically caches
- Ensures app stays within API rate limits

## Development

### Project Structure

```
tidbyt-epl-transfers/
├── epl_transfers.star    # Main Starlark app
├── manifest.yaml         # App metadata for Tidbyt Community
├── README.md             # This file
└── .gitignore           # Ignore sensitive files
```

### Local Testing

```bash
# Render static image
pixlet render epl_transfers.star api_key="YOUR_KEY"

# Live preview (auto-reloads on save)
pixlet serve epl_transfers.star api_key="YOUR_KEY"

# Check for lint errors
pixlet check epl_transfers.star
```

### Customization

**Change colors:**
```python
# In epl_transfers.star
COLOR_HEADER = "#37003c"  # EPL purple (change this)
COLOR_ACCENT = "#00ff85"  # EPL cyan (change this)
```

**Adjust animation speed:**
```python
# In main() function
return render.Root(
    delay = 150,  # Milliseconds per frame (lower = faster)
    ...
)
```

**Change cache duration:**
```python
CACHE_TTL = 3600  # Seconds (3600 = 1 hour)
```

## API Reference

### API-Football Endpoints Used

**Transfers Endpoint:**
```
GET https://v3.football.api-sports.com/transfers?league=39
```

**Headers:**
```
x-rapidapi-key: YOUR_KEY
x-rapidapi-host: v3.football.api-sports.com
```

**Response:** See [API-Football documentation](https://www.api-football.com/documentation-v3#tag/Transfers)

### Supported EPL Clubs

App includes badge URLs for all 20 Premier League teams:
- Arsenal, Aston Villa, Bournemouth, Brentford, Brighton
- Burnley, Chelsea, Crystal Palace, Everton, Fulham
- Leeds United, Leicester, Liverpool, Manchester City
- Manchester United, Newcastle, Nottingham Forest
- Southampton, Tottenham, West Ham, Wolves

## Publishing to Tidbyt Community

To submit this app to the official Tidbyt Community Apps:

1. Fork [tidbyt/community](https://github.com/tidbyt/community)
2. Copy files to `/apps/epltransfers/`
3. Test thoroughly on real device
4. Create pull request with description
5. Wait for review from Tidbyt team

**Community Requirements:**
- Clean, well-commented code
- Error handling for API failures
- Efficient caching (respect rate limits)
- User-friendly configuration
- Documentation

## Troubleshooting

### "Please configure your API key"
- You need to add your API-Football key in the app settings
- Get a free key from api-football.com

### "No recent transfers found"
- This is normal during quiet transfer windows
- API may not have recent EPL transfers
- Try again during transfer window (January/Summer)

### "API request failed"
- Check your API key is valid
- Verify you haven't exceeded rate limits (100/day)
- Check api-football.com status

### Badges not loading
- Badge URLs may have changed
- API-Football may have updated endpoints
- Check CLUB_BADGES dictionary in code

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Test your changes locally
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Credits

- **Data**: [API-Football](https://www.api-football.com/)
- **Platform**: [Tidbyt](https://tidbyt.com/)
- **Club Badges**: Official Premier League team logos

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/tidbyt-epl-transfers/issues)
- **Tidbyt Docs**: [tidbyt.dev](https://tidbyt.dev)
- **API Docs**: [api-football.com/documentation](https://www.api-football.com/documentation-v3)

---

Made with ⚽ for Tidbyt
