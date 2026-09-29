# Tidbyt ESPHome Display

An ESPHome config for the Tidbyt Gen2. It features dynamic scrolling text, album art, and real-time weather/time synchronization.

---

Thanks to [jon_2233](https://community.home-assistant.io/u/jon_2232/summary) and his post [here](https://community.home-assistant.io/t/esphome-on-tidbyt-gen-2/830367) for hardware info.

---

## Personal Configuration ##
Be sure to adjust your device encryption key as well as your weather entity before compiling.

---

## Available Entities

### Color Choosers (Light Entities)
Each line of text is exposed as an RGB light. Adjust the color wheel in Home Assistant to change the display in real-time.

* **light.track_title_color**: The scrolling song title.
* **light.artist_color**: The scrolling artist name.
* **light.album_color**: The scrolling album name (and Weather summary).
* **light.clock_color**: The HH:MM digital clock.
* **light.weather_color**: The current temperature text.
* **light.alert_color**: The full-screen emergency alert text.

### Controls & Sensors
* **select.display_mode**: Switch between `Clock`, `Weather`, and `Now Playing`.
* **number.brightness**: Controls the global intensity of the LEDs (0-255).
* **number.tidbyt_scroll_speed**: Controls text crawl speed (ms per pixel).
* **switch.display_power**: Master toggle to black out the screen.
* **text.alert_message**: Enter text here to override the screen with a scrolling alert.
* **binary_sensor.tidbyt_mode_touch**: Reflects the state of the physical touch sensor.



---

## Home Assistant Services

### `esphome.tidbyt_update_media`
Use this service to push metadata from your media players (Spotify, Apple Music, etc.) to the display.

| Field | Type | Description |
| :--- | :--- | :--- |
| `title` | string | The song name (auto-capitalized on device). |
| `artist` | string | The artist name (auto-capitalized on device). |
| `album` | string | The album name. |
| `image_path` | string | URL for the album art. |
| `is_playing` | boolean | If `true`, switches display to "Now Playing" mode. |

---

## Automations

### Spotify Sync Example
```yaml
alias: "Tidbyt: Spotify Sync"
trigger:
  - platform: state
    entity_id: media_player.spotify
action:
  - service: esphome.tidbyt_update_media
    data:
      title: "{{ state_attr('media_player.spotify', 'media_title') }}"
      artist: "{{ state_attr('media_player.spotify', 'media_artist') }}"
      album: "{{ state_attr('media_player.spotify', 'media_album') }}"
      image_path: "{{ state_attr('media_player.spotify', 'entity_picture') }}"
      is_playing: "{{ is_state('media_player.spotify', 'playing') }}"
