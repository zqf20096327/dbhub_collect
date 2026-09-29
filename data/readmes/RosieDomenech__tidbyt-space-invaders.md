# Tidbyt Space Invaders 👾

**Author:** Rosie Domenech  
**Date:** April 2026  
**Description:** Retro Space Invaders animation for the Tidbyt 64x32 LED display. Features marching aliens, player ship, lasers, and bullets — all in classic arcade style.

---

## Preview

![Space Invaders Preview](spaceinvaders.gif)

---

## Features

- 👾 6 pixel-perfect invaders marching left and right
- 🦵 Classic alternating leg animation
- 🔴 Red alien laser firing down
- ⬜ Player bullet shooting up
- 🚀 Green player ship at the bottom
- ⭐ Starfield background
- 📊 Score display at the top

---

## Setup

### 1. Install Pixlet
```bash
# macOS
brew install tidbyt/tidbyt/pixlet

# Windows/Linux — download from:
# https://github.com/tidbyt/pixlet/releases
```

### 2. Clone this repo
```bash
git clone https://github.com/RosieDomenech/tidbyt-space-invaders.git
cd tidbyt-space-invaders
```

### 3. Preview in browser
```bash
pixlet serve spaceinvaders.star
# Open http://localhost:8080
```

### 4. Push to your Tidbyt
```bash
pixlet render spaceinvaders.star
pixlet push \
  --api-token YOUR_API_TOKEN \
  --installation-id space-invaders \
  YOUR_DEVICE_ID \
  spaceinvaders.webp
```

---

## Requirements

- [Pixlet](https://github.com/tidbyt/pixlet)
- A Tidbyt device + API token
