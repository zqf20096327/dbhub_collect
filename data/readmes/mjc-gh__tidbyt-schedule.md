Small Ruby program for periodically rendering and pushing [Tidbyt
apps](https://tidbyt.dev/).

## Setup

1. Clone this repo and run `bundle install` to install the required
   gems.
2. Create a config.yml file and add your Tidbyt [API Device
   ID](https://tidbyt.dev/docs/integrate/pushing-apps#pixlet-push).
   ```
   :device_id: [your-tidbyt-device-id]
   :apps:
    - :name: hourly_forecast
      :path: tidbyt-ushourlyforecast
      :every: 15
   ```

3. Execute `ruby run.rb` ideally using screen or tmux on a server. The
   idea is to let this program run indefinitely and periodically render
   and push new updates to your Tidbyt device.

   You may also want to use the `TZ` environment variable to adjust
   times to your local timezone: `TZ="US/Eastern" ruby run.rb`.

## Output

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                                  Tidbyt Apps
                            2023-03-04 - 11:58:48AM
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ App Name                       ┃ Last Rendered        ┃ Last Pushed          ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╊━━━━━━━━━━━━━━━━━━━━━━╊━━━━━━━━━━━━━━━━━━━━━━┫
┃ hourly_forecast                ┃ 11:53AM 3/4/23       ┃ 11:53AM 3/4/23       ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━┛
```
