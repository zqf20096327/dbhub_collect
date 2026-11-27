# Tidbyt Snow Report

A private Tidbyt app for Palisades Tahoe. A GitHub Action renders it every 30 minutes and pushes it to the device.

## Frames

1. **Now**: mid-mountain temp, today's high/low, and a surface call (SNOWING NOW, FRESH, SOFTENS 11A, SLUSHY BY 1P, FIRM AM, PACKED)
2. **Next 4 days**: highs colored by the slush line; today and the best day get a gray box, and the best day's name is gold
3. **Roads**: I-80 and SR-89 chain controls (only when they're up)

## Data

- NWS gridpoint forecast `STO/89,87` (7,385 ft, mid-mountain)
- USDA SNOTEL `784:CA:SNTL` "Palisades Tahoe" (8,010 ft): observed new snow and temps
- Caltrans District 3 chain controls

## Settings

Edit the `env:` block in `.github/workflows/push-to-tidbyt.yml`.

## Secrets

Repo → Settings → Secrets and variables → Actions:

- `TIDBYT_API_TOKEN`: Tidbyt app → Settings → General → Get API key
- `TIDBYT_DEVICE_ID`: shown on the same screen
- `TIDBYT_WORK_API_TOKEN` / `TIDBYT_WORK_DEVICE_ID`: the work Tidbyt (each device has its own key)

## Local preview

```
pixlet serve palisades_snow.star
```

Add `frame=N` (0–4) to the preview URL to see a single frame.

## Quiet hours

From 8:45pm to 7:45am Pacific (15 minutes of buffer around the 9:00pm–7:30am night clock) (`QUIET_START` / `QUIET_END` in the workflow), each run removes the app from both Tidbyts so a night clock can have the screen to itself. The 7:45am run pushes it back. GitHub's schedule can start runs a few minutes late.

To switch it by hand: Actions → Push to Tidbyt → Run workflow → pick `day` (push now) or `night` (remove now).
