# Tidbyt Events Display App

A dynamic Tidbyt app that displays upcoming events from Ticketmaster in the Ann Arbor, MI area. The app fetches live event data and shows the next upcoming event with scrolling text for long names.

## What It Does

- 🎭 Displays the next upcoming event from Ticketmaster
- 📅 Shows event date and time in a readable format
- 🏟️ Displays venue name with automatic scrolling for long names
- 🔄 Updates automatically with live data from the API
- ✨ Clean, colorful display optimized for Tidbyt's 64x32 pixel screen

## Display Format

```
🎭 Event #1:
[Event Name - scrolling if long]
7/5 7:30 PM
[Venue Name - scrolling if long]
```

## Prerequisites

### 1. Buy a Tidbyt Device

Purchase a Tidbyt from the official website:
- **Website**: [tidbyt.com](https://tidbyt.com)
- **Price**: ~$179 USD
- **What you get**: 64x32 LED display, Wi-Fi connectivity, mobile app

### 2. Install Pixlet

Pixlet is the development tool for creating Tidbyt apps.

#### macOS (using Homebrew):
```bash
brew install tidbyt/tidbyt/pixlet
```

#### Linux/Windows:
Download the latest release from [GitHub](https://github.com/tidbyt/pixlet/releases)

#### Verify Installation:
```bash
pixlet version
```

### 3. Install Pixi (Optional but Recommended)

Pixi is a package manager that makes running tasks easier:

#### macOS/Linux:
```bash
curl -fsSL https://pixi.sh/install.sh | bash
```

#### Windows:
```powershell
iwr -useb https://pixi.sh/install.ps1 | iex
```

### 4. Set Up Your Tidbyt Device

1. Download the Tidbyt mobile app (iOS/Android)
2. Follow the setup process to connect your device to Wi-Fi
3. Note your device ID (or use the command below to get it)

## Getting Your Device ID

To find your Tidbyt device ID, run:

```bash
pixlet devices
```

This will output something like:
```
moodily-motivating-majestic-dodo-a7d    Tidbyt #1234
```

The first part (`moodily-motivating-majestic-dodo-a7d`) is your device ID.

You can also extract just the device ID with:
```bash
pixlet devices | cut -d ' ' -f1
```

## How to Use This App

### Method 1: Using Pixi (Recommended)

The easiest way to deploy all three events is using the included `pixi.toml` configuration:

#### Deploy All Events:
```bash
pixi run deploy-all
```

This will:
1. Clean existing event apps
2. Render Event #1, #2, and #3 separately
3. Deploy all three to your Tidbyt
4. Show the final status

#### Individual Commands:
```bash
# Render individual events
pixi run render-event1    # Renders first event
pixi run render-event2    # Renders second event  
pixi run render-event3    # Renders third event

# Deploy individual events
pixi run deploy-event1    # Deploys first event
pixi run deploy-event2    # Deploys second event
pixi run deploy-event3    # Deploys third event

# Utility commands
pixi run clean           # Remove existing apps
pixi run list            # List installed apps
pixi run dev-render      # Quick render for development
pixi run dev-serve       # Serve app in browser for testing
```

### Method 2: Manual Pixlet Commands

If you prefer not to use Pixi, you can run the commands manually:

#### Render Different Events:
```bash
# First event
pixlet render events.star event_index=0

# Second event  
pixlet render events.star event_index=1

# Third event
pixlet render events.star event_index=2
```

#### Deploy to Device:
```bash
# Get your device ID
DEVICE_ID=$(pixlet devices | cut -d ' ' -f1)

# Deploy each event
pixlet push --installation-id event1 $DEVICE_ID events.webp
pixlet push --installation-id event2 $DEVICE_ID events.webp  
pixlet push --installation-id event3 $DEVICE_ID events.webp
```

### Method 3: Using the Deploy Script

You can also use the included shell script:

```bash
./deploy_events.sh
```

### Method 4: Automated Docker Deployment

For fully automated updates, you can run the app in a Docker container that updates your Tidbyt every hour:

```bash
# Using Docker Compose (recommended)
docker-compose up -d

# Using Docker directly
docker run -d \
  --name tidbyt-events-updater \
  --restart unless-stopped \
  --network host \
  -e TIDBYT_API_TOKEN=your_token_here \
  mrorbitman/tidbyt-events:latest
```

**Important**: You need a Tidbyt API token. Get it from:
- Run `pixlet login` and follow prompts
- Tidbyt mobile app → Settings → General → API Token
- [Tidbyt Developer Portal](https://tidbyt.dev/docs/publish/community-apps#api-token)

See [DOCKER.md](DOCKER.md) for complete Docker deployment instructions.

## Data Refresh Frequency

### How Often Does the App Update?

**Important**: The Tidbyt device does **NOT** continuously refresh data from the API. Here's how it actually works:

1. **At Render Time**: The app fetches data from the RSS feed when you run `pixlet render events.star`
2. **Static WebP Creation**: The fetched data is "baked into" the WebP animation file
3. **No Live Updates**: Once pushed to your Tidbyt, the display shows the same information until you manually update it

### To Get Fresh Data:

You need to manually re-render and re-push the apps:

#### Using Pixi:
```bash
pixi run deploy-all
```

#### Using Pixlet directly:
```bash
# Re-render with fresh data
pixlet render events.star event_index=0
pixlet render events.star event_index=1  
pixlet render events.star event_index=2

# Re-deploy to device
DEVICE_ID=$(pixlet devices | cut -d ' ' -f1)
pixlet push --installation-id event1 $DEVICE_ID events.webp
pixlet push --installation-id event2 $DEVICE_ID events.webp
pixlet push --installation-id event3 $DEVICE_ID events.webp
```

#### Using the Deploy Script:
```bash
./deploy_events.sh
```

### Automation Options:

To get regular updates, you could:

1. **Manual Updates**: Re-run the commands when you want fresh data
2. **Scheduled Script**: Create a cron job to run `pixi run deploy-all` periodically
3. **Tidbyt Community Apps**: Some community apps have server-side components that can push updates

### Why This Limitation Exists:

- **Battery Life**: Tidbyt devices are designed for long battery life
- **Network Efficiency**: Reduces constant network requests
- **Simplicity**: Apps are self-contained WebP animations
- **Reliability**: No dependency on external APIs staying online

## How the WebP Generation Works

1. **Starlark Code**: The `events.star` file contains the app logic written in Starlark (a Python-like language)

2. **Configuration**: The `event_index` parameter determines which event to display (0=first, 1=second, 2=third)

3. **API Call**: The app makes an HTTP request to `https://rss-feeds.jpc.io/api/ticketmaster-events`

4. **Data Parsing**: It parses the RSS XML response to extract:
   - Event title (cleaned of emoji)
   - Date and time (converted from RFC 2822 format)
   - Venue name (extracted from HTML description)

5. **Event Selection**: Based on `event_index`, it selects the appropriate event from the RSS feed

6. **Rendering**: Pixlet converts the Starlark code into frames of a 64x32 pixel animation

7. **WebP Output**: The frames are compiled into a WebP file that loops continuously

8. **Display**: Your Tidbyt downloads and displays the WebP animation

## App Architecture

### Main Components

- **`main(config)`**: Entry point that gets event index from config and creates display layout
- **`fetch_event(event_index)`**: Makes HTTP request and selects the specified event
- **`parse_event_by_index()`**: Extracts the Nth event from RSS XML
- **`extract_venue()`**: Parses venue name from HTML description
- **`parse_date()`**: Converts RFC 2822 timestamps to readable format

### Display Elements

- **Header**: "🎭 Event #N:" in gold (N = 1, 2, or 3)
- **Event Title**: Scrolling marquee in green
- **Date/Time**: Static text in light blue
- **Venue**: Scrolling marquee in pink

## Customization

### Change Colors

Edit the color values in `events.star`:
```starlark
color = "#FFD700"  # Gold
color = "#00FF00"  # Green
color = "#87CEEB"  # Light Blue
color = "#FF69B4"  # Pink
```

### Change Fonts

Available fonts:
- `"tom-thumb"` (3x5 pixels, very small)
- `"tb-8"` (larger, good for headers)
- `"6x13"` (medium size)

### Modify Layout

Adjust spacing with `render.Box(height = N)` where N is pixels.

### Add More Events

To show more than 3 events, add new tasks to `pixi.toml`:

```toml
render-event4 = { cmd = "pixlet render events.star event_index=3", env = { EVENT_INDEX = "3" } }
deploy-event4 = { cmd = "pixlet push --installation-id event4 $(pixlet devices | cut -d ' ' -f1) events.webp", depends_on = ["render-event4"] }
```

## Troubleshooting

### App Not Updating
- **Remember**: Apps don't auto-update! You must manually re-render and push
- Check your internet connection during render
- Verify the API endpoint is accessible: https://rss-feeds.jpc.io/api/ticketmaster-events
- Try re-running `pixi run deploy-all`

### Display Issues
- Ensure your device ID is correct: `pixlet devices`
- Check that Pixlet is properly installed: `pixlet version`
- Verify your Tidbyt is connected to Wi-Fi

### Pixi Issues
- Make sure Pixi is installed: `pixi --version`
- Try running commands manually if Pixi tasks fail
- Check that you're in the project directory with `pixi.toml`

### API Problems
- The app will show "Loading events..." if the API is unavailable during render
- Check the API endpoint: https://rss-feeds.jpc.io/api/ticketmaster-events
- Try rendering again after a few minutes

## Development Workflow

### Using Pixi:
1. **Edit** the `events.star` file
2. **Test** with `pixi run dev-serve` (opens in browser)
3. **Deploy** with `pixi run deploy-all`
4. **Repeat** step 3 whenever you want fresh data

### Using Pixlet directly:
1. **Edit** the `events.star` file
2. **Render** with `pixlet render events.star event_index=0`
3. **Test** with `pixlet serve events.star event_index=0` (optional)
4. **Push** to device with `pixlet push --installation-id events YOUR_DEVICE_ID events.webp`
5. **Repeat** steps 2-4 whenever you want fresh data

## Files in This Project

- **`events.star`**: Main application code
- **`pixi.toml`**: Pixi configuration with tasks for easy deployment
- **`deploy_events.sh`**: Shell script for deployment (alternative to Pixi)
- **`events.webp`**: Generated animation file (created by pixlet render)
- **`Dockerfile`**: Docker container definition for automated deployment
- **`docker-compose.yml`**: Docker Compose configuration for easy container management
- **`DOCKER.md`**: Complete Docker deployment guide
- **`README.md`**: This documentation

## API Information

The app uses the RSS feed from:
- **URL**: `https://rss-feeds.jpc.io/api/ticketmaster-events`
- **Format**: RSS 2.0 XML
- **Data**: Ticketmaster events in the Ann Arbor, MI area (48103)
- **Update Frequency**: The API updates regularly with new events
- **App Refresh**: Manual only - you must re-render to get fresh data

## Learn More

- **Pixlet Documentation**: [pixlet.dev](https://pixlet.dev)
- **Pixi Documentation**: [pixi.sh](https://pixi.sh)
- **Tidbyt Community**: [discuss.tidbyt.com](https://discuss.tidbyt.com)
- **Starlark Language**: [github.com/bazelbuild/starlark](https://github.com/bazelbuild/starlark)
- **Tidbyt App Gallery**: Browse other apps for inspiration

## License

This project is open source. Feel free to modify and share!

---

**Enjoy your dynamic event display!** 🎉
