# DC Metro Arrivals → Tidbyt (push service)

Renders the DC Metro Arrivals app once a minute and pushes it to a stock Tidbyt through Tidbyt's push API. Your device keeps its normal firmware; this shows up as one more app in your rotation.

## Deploy on Railway

1. Put these files (`Dockerfile`, `push.sh`, `dc_metro_arrivals.star`, `README.md`) in a new GitHub repository. It can be private.
2. In Railway, create a new project and choose **Deploy from GitHub repo**, then pick that repository. Railway finds the Dockerfile and builds it.
3. Open the service's **Variables** tab and add the variables below.
4. Open **Deployments → View logs**. You should see `pushed` once a minute, and the app should appear on your Tidbyt within a minute or two.

The service needs no public URL or port; it only makes outgoing requests.

## Variables

| Variable | Required | Example | Notes |
| --- | --- | --- | --- |
| `TIDBYT_API_TOKEN` | yes | `eyJhbGci...` | Tidbyt app → your device → Settings → General → Get API Key |
| `TIDBYT_DEVICE_ID` | yes | `happy-blue-otter-123` | Shown with the API key |
| `WMATA_API_KEY` | yes | `38b5...` | developer.wmata.com profile page |
| `STATION` | one of these two | `A01,C01` | Station code(s); see the station list in `dc_metro_arrivals.star` |
| `BUS_STOPS` | one of these two | `1001195,1002222` | Up to 3 stop IDs from the stop sign |
| `LINE` | no | `RD` | `RD` `OR` `YL` `GR` `BL` `SV`, default all |
| `TRAIN_DEST` | no | `Glenmont` | Only trains whose destination contains this |
| `BUS_ROUTES` | no | `C53,D10` | Only these routes |
| `WALK_RAIL` / `WALK_BUS` | no | `5` | Hide arrivals sooner than this many minutes |
| `PUSH_INTERVAL` | no | `60` | Seconds between updates |

## Troubleshooting

- `push failed: HTTP 401` or `403`: the Tidbyt token or device ID is wrong, or was regenerated.
- `push failed` with another code: Tidbyt's push service may be down. If it never works, switch the device to Tronbyt.
- The display says the WMATA key was rejected: check `WMATA_API_KEY`.
- To remove the app from your rotation, stop the Railway service, then delete the "dcmetro" installation in the Tidbyt app if it lingers.
