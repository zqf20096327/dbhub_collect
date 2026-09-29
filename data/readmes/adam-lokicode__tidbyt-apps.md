# Tidbyt Apps Collection

This directory contains multiple Tidbyt applications built with Pixlet and Starlark. Each app is organized in its own directory to avoid conflicts.

## Directory Structure

```
tidbyt-apps/
├── hello-app/          # Simple "Hello World" example
│   └── hello.star
├── clock-app/          # Time and date display
│   └── simple_clock.star
├── message-app/        # Scrolling message display
│   └── scrolling_message.star
└── my-first-app/       # Documentation and examples
    └── README.md
```

## Apps Overview

### 1. Hello App (`hello-app/hello.star`)

- **Purpose**: Basic "Hello, Tidbyt!" message
- **Features**: Simple text display
- **Best for**: Learning the basics of Tidbyt development

### 2. Clock App (`clock-app/simple_clock.star`)

- **Purpose**: Digital clock with date
- **Features**:
  - Current time display (12-hour format)
  - Current date
  - Welcome message
  - Clean, centered layout
- **Best for**: Functional time display on your Tidbyt

### 3. Message App (`message-app/scrolling_message.star`)

- **Purpose**: Scrolling message display
- **Features**:
  - Scrolling marquee text
  - Multiple text elements
  - Emoji support
  - Colorful design
- **Best for**: Custom messages and announcements

## Quick Start Guide

### Prerequisites

1. Install Pixlet (already done):
   ```bash
   brew install tidbyt/tidbyt/pixlet
   ```

### Running Apps Locally

1. **Preview any app in browser:**

   ```bash
   cd [app-directory]
   pixlet serve [app-file].star
   ```

   Then open http://localhost:8080

2. **Render app to image:**
   ```bash
   pixlet render [app-file].star
   ```

### Examples

```bash
# Preview the clock app
cd clock-app
pixlet serve simple_clock.star

# Preview the message app
cd message-app
pixlet serve scrolling_message.star

# Render the hello app
cd hello-app
pixlet render hello.star
```

### Deploying to Your Tidbyt Device

1. **Login to Tidbyt:**

   ```bash
   pixlet login
   ```

2. **List your devices:**

   ```bash
   pixlet devices
   ```

3. **Deploy an app:**

   ```bash
   # Render first
   pixlet render simple_clock.star

   # Push to device
   pixlet push <YOUR_DEVICE_ID> simple_clock.webp
   ```

## Development Tips

1. **One app per directory**: Pixlet loads all .star files in a directory, so keep apps separated
2. **Test frequently**: Use `pixlet render` to catch syntax errors quickly
3. **Use pixlet serve**: Great for real-time development with browser preview
4. **Check documentation**: Visit [Tidbyt Developer Docs](https://tidbyt.dev/docs/build/build-for-tidbyt) for advanced features

## Next Steps

- **Add API integration**: Fetch real weather, stock prices, or news
- **Create configuration schemas**: Allow users to customize your apps
- **Explore animations**: Use timing and state to create dynamic displays
- **Join the community**: Share your apps in the [Tidbyt Community Repository](https://github.com/tidbyt/community)

## Resources

- [Tidbyt Developer Documentation](https://tidbyt.dev/docs/build/build-for-tidbyt)
- [Pixlet GitHub Repository](https://github.com/tidbyt/pixlet)
- [Starlark Language Specification](https://github.com/bazelbuild/starlark)
- [Tidbyt Community Apps](https://github.com/tidbyt/community)
- [Tidbyt Discord Community](https://discord.com/invite/tidbyt)

Happy coding! 🚀✨
