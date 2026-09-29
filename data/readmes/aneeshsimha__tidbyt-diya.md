# 🪔 Tidbyt Diya - Flickering Oil Lamp

A beautiful, animated diya (Indian oil lamp) for your Tidbyt display. Features a realistic flickering flame animation that brings the warmth and serenity of a traditional diya to your desk.

Perfect for Diwali celebrations or year-round ambient display!

## Features

- 🔥 Realistic flickering flame animation
- 🎨 Authentic terracotta color palette
- ✨ Smooth 24-frame animation cycle
- 🪔 Front-facing aesthetic design
- 💫 Gentle flame sway and height variation

## Preview

The app displays a traditional clay diya with a warm, flickering flame that creates a calming, festive atmosphere on your Tidbyt screen.

## Installation

### Prerequisites

Install Pixlet, the Tidbyt app development tool:

```bash
# On macOS
brew install tidbyt/tidbyt/pixlet

# On Linux/Other
# Download from https://github.com/tidbyt/pixlet/releases
```

### Running the App

1. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/tidbyt-diya.git
cd tidbyt-diya
```

2. Render and preview the app:
```bash
pixlet render diya.star
pixlet serve diya.star
```

3. Open your browser to `http://localhost:8080` to see the preview

### Deploying to Your Tidbyt

1. Get your Tidbyt device ID and API token from the Tidbyt mobile app

2. Push the app to your device:
```bash
pixlet push --api-token YOUR_API_TOKEN YOUR_DEVICE_ID diya.star
```

## Customization

You can customize the app by modifying the color palette and animation timing in `diya.star`:

- `FLAME_*` colors: Adjust the flame appearance
- `DIYA_*` colors: Change the lamp's terracotta tones
- `delay` parameter: Control animation speed (default: 100ms)
- `flicker` patterns: Modify the flame movement logic

## Technical Details

- **Language**: Starlark (Tidbyt's Python-like language)
- **Resolution**: 64x32 pixels
- **Frame Rate**: ~10 FPS
- **Animation Frames**: 24

## Cultural Significance

The diya is a traditional oil lamp used in Indian culture, especially during Diwali, the Festival of Lights. It symbolizes the victory of light over darkness and knowledge over ignorance.

## License

MIT License - feel free to use and modify!

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve the animation or add new features.

## Credits

Created with ❤️ for the Tidbyt community
