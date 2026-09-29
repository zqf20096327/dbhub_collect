## Weather

Link to hourly weather forecast: `https://api.weather.gov/gridpoints/SEW/122,66/forecast/hourly`

Path to the data: `properties.periods[]`

interesting properties:
startTime
temperature
temperatureUnit
shortForecast

* Mostly Sunny
* Partly Sunny
* Partly Cloudy
* Mostly Cloudy
* Slight Chance Rain Showers
* Chance Rain Showers
* Slight Chance Light Rain
* Chance Light Rain

How to get the initial link? Translate the coordinates into forecastGridData:
`https://api.weather.gov/points/47.5744,-122.3855`

## Tidbyt

To create the UI, need to install [pixlet](https://github.com/tidbyt/pixlet):
`wget https://github.com/tidbyt/pixlet/releases/download/v0.17.0/pixlet_0.17.0_linux_amd64.tar.gz`

This has a dependency on [libwebp](https://packages.ubuntu.com/impish/libwebp-dev):
`sudo apt install libwebp-dev`

To preview, use `./pixlet serve sunrise.star`