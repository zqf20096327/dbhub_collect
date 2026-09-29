# tidbyt-mealviewer-worker

A Cloudflare worker that uses the Browser Rendering API and MealViewer to display the next school lunch on a Tidbyt.

![image](https://github.com/user-attachments/assets/09967c9a-91f7-44ab-b646-c38f7f13e357)

# Install

1. clone this repo
1. run `npm install` from your terminal
1. fill in your `.dev.vars` file
  - `SCHOOL_ID`: your school's from [MealViewer](https://schools.mealviewer.com/) (last part of the URL)
  - `DEVICE_ID`: your device ID from the Tidbyt app, **Settings > Developer > Get API Key**
  - `API_KEY`: your API key, also  from the Tidbyt app, **Settings > Developer > Get API Key**
1. run `npm start`, hit the displayed URL to make sure it works.

# Deploy

1. run `wrangler secret put SCHOOL_ID`, and enter the value from your `.dev.vars` file
1. run `wrangler secret put DEVICE_ID`, and enter the value from your `.dev.vars` file
1. run `wrangler secret put API_KEY`, and enter the value from your `.dev.vars` file
1. run `npm run deploy`
