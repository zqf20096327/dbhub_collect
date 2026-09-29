# Yoghurt Growth Stats for Tidbyt / Tronbyt

⚠️ Recommended to use this app via Home Assistant together with TidbytAssistant for automatic updates and notifications.

This Pixlet app displays the current state of your homemade yoghurt fermentation on your Tidbyt. It features Minecraft-inspired pixel art, animated scenery, a day/night background and a live countdown until the yoghurt is ready.

## Features

- 🥛 Animated milk bucket while yoghurt is fermenting
- 🔥 Campfire animation (embers when inactive)
- 🌤️ Dynamic sky depending on local time
- ☁️ Animated clouds
- ✨ Fireflies during the evening
- ⏳ Minecraft-style hourglass / clock according to current time
- 🕒 Remaining fermentation time
- 📋 Wooden sign with current status

## Preview

![Pixlet Preview](preview.gif)
![Pixlet Preview](preview_dawn.webp)

## Requirements

- Home Assistant
- TidbytAssistant (recommended)
- One Home Assistant Timer entity
- One Home Assistant Boolean entity indicating whether yoghurt is currently fermenting

## Home Assistant Setup

### Helper Entities

Create the following helpers:

- `timer.yoghurt`
- `input_boolean.yoghurt_active`

The timer is used to display the remaining fermentation time.

The boolean controls whether the app displays an active fermentation or an idle scene.

## Configuration

Configure the app with:

- Home Assistant URL
- Long-lived Access Token
- Timer Entity
- Boolean Entity

Example:

```text
Home Assistant URL:
http://homeassistant.local:8123

Timer:
timer.yoghurt

Boolean:
input_boolean.yoghurt_active
```

## Display

When the timer is running the display shows:

- Remaining fermentation time
- Animated milk bucket
- Animated campfire
- Dynamic daytime sky
- Moving clouds
- Minecraft-inspired scenery

When the timer is idle:

- Campfire changes to glowing embers
- Milk bucket becomes static
- Countdown disappears
- Scene remains animated

## Time of Day

The background is selected automatically using the local system time.

Different skies are displayed for:

- 🌅 Sunrise
- ☀️ Day
- 🌇 Dusk
- 🌙 Night

No additional Home Assistant entities are required.

## Tronbyt

The application can be configured directly through the Tronbyt configuration interface.
