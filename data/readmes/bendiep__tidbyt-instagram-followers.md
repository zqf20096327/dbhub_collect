# tidbyt-instagram-followers
> Display the follower count of an Instagram user on the Tidbyt

![IMG_1866](https://user-images.githubusercontent.com/8815089/189522793-522c0d57-1e6d-4d0e-a6ca-0e77405f8671.jpg)
<br>

### Design
I couldn't find any sort of Instagram (IG) API to retrieve follower count data.<br>
So I decided to create a simple Flask REST API that would scrape the follower count off of an IG users profile page.

### Limitations
- Requires hosting the Flask API somewhere
- Scraping API could possibly get IP blacklisted

### Run
```
# Step 1 - Start Flask App
python flask-api/app.py

# Step 2 - Set INSTAGRAM_USER in instagram_followers.star, line 6
INSTAGRAM_USER = "<INSTAGRAM USER>"

# Step 3 - Render and serve in browser (For testing only)
pixlet serve instagram_followers.star

# Step 4 - Render and generate WebP file
pixlet render instagram_followers.star

# Step 5 - Two methods for deploying WebP file to Tidbyt:
1. Single
pixlet push --api-token <YOUR API TOKEN> <YOUR DEVICE ID> instagram_followers.webp

2. As installation (displays in mobile app - will loop but data will be static)
pixlet push --api-token <YOUR API TOKEN> --installation-id InstagramFollows <YOUR DEVICE ID> instagram_followers.webp
```

### Automate
1. Create a bash script that executes Steps 4 and 5
2. Setup a cronjob for periodic updates
