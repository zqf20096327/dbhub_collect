# TIDBYT Sonos Album Art

A TIDBYT app that displays album art from your currently playing Sonos speaker.

## Features

- Displays album art from your Sonos speaker on your TIDBYT display
- Shows track title and artist name
- Automatically updates when the song changes
- Supports multiple Sonos speakers (select by room name)

## Prerequisites

- A [TIDBYT](https://tidbyt.com/) device
- A Sonos speaker on your local network
- A server/computer running the Sonos proxy (for local network access)

## Architecture

Since TIDBYT apps run in the cloud and cannot directly access your local network, this solution uses a two-part architecture:

1. **Sonos Proxy Server** - A small web service running on your local network that exposes Sonos data
2. **TIDBYT App** - The Starlark app that fetches data from your proxy and displays it

## Setup

### 1. Deploy the Sonos Proxy

You'll need to run a proxy server on your local network that can communicate with your Sonos speakers. Options include:

#### Option A: Node-Sonos-HTTP-API (Recommended)

```bash
# Clone and run node-sonos-http-api
git clone https://github.com/jishi/node-sonos-http-api.git
cd node-sonos-http-api
npm install
npm start
```

This runs on port 5005 by default. You'll need to expose this to the internet (via ngrok, Cloudflare Tunnel, or your own domain).

#### Option B: Custom Proxy

See the `proxy/` directory for a simple Python-based proxy example.

### 2. Expose Your Proxy to the Internet

The TIDBYT cloud needs to reach your proxy. Options:

- **ngrok**: `ngrok http 5005`
- **Cloudflare Tunnel**: Free and more permanent solution
- **Reverse proxy**: If you have a domain and static IP

### 3. Configure the TIDBYT App

Set the following configuration options in the app:

| Option | Description | Example |
|--------|-------------|---------|
| `proxy_url` | URL of your Sonos proxy | `https://your-proxy.ngrok.io` |
| `room_name` | Sonos room/speaker name | `Living Room` |

## Local Development

### Install Pixlet

```bash
# macOS
brew install tidbyt/tidbyt/pixlet

# Linux/Windows - download from releases
# https://github.com/tidbyt/pixlet/releases
```

### Run the App Locally

```bash
# Serve the app with live reload
pixlet serve sonos_album_art.star

# Render a single frame
pixlet render sonos_album_art.star proxy_url="http://localhost:5005" room_name="Living Room"

# Push to your TIDBYT device
pixlet push --api-token YOUR_API_TOKEN YOUR_DEVICE_ID sonos_album_art.star
```

### Get Your TIDBYT API Token and Device ID

1. Go to https://tidbyt.com/
2. Log in to your account
3. Find your device and get the API token from settings

## Configuration Options

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `proxy_url` | Yes | - | URL of your Sonos HTTP proxy |
| `room_name` | Yes | - | Name of your Sonos room/speaker |
| `show_artist` | No | `true` | Show artist name below track title |
| `scroll_speed` | No | `50` | Text scroll speed (ms per frame) |

## How It Works

1. The TIDBYT app makes an HTTP request to your Sonos proxy
2. The proxy queries your local Sonos speaker for current playback state
3. If music is playing, the proxy returns track info including album art URL
4. The app fetches the album art image and scales it for the 64x32 display
5. Track title and artist scroll below the album art

## Troubleshooting

### "No music playing" shown
- Verify your Sonos is actively playing music
- Check the room name matches exactly (case-sensitive)
- Test your proxy URL directly in a browser

### Album art not showing
- Some sources (like local files) may not have album art URLs
- Check if the album art URL is accessible from the internet

### Connection errors
- Ensure your proxy is running and exposed to the internet
- Verify the proxy URL is correct and accessible
- Check firewall settings

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- [TIDBYT](https://tidbyt.com/) for the awesome display
- [Pixlet](https://github.com/tidbyt/pixlet) for the development framework
- [node-sonos-http-api](https://github.com/jishi/node-sonos-http-api) for Sonos integration
