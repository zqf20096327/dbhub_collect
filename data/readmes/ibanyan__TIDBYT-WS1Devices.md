# TIDBYT-WS1Devices
View your Workspace ONE UEM information on your Tidbyt.


If you own a TIDBYT you will be able to install these apps.  Feel free to fork them off and make new apps targeting Workspace ONE UEM.
Hopefully you will find these apps, their embeded comments, and instructions useful enough to create your own apps.  If you do, or you just have some feedback, please email me at ibanyan@gmail.com

Both of these apps are in the TIDBYT app store.  The versions here are exactly the same, just without the part that integrates with the TIDBYT mobile app.
That integration allows the user to enter the required info for the apps to work, in the mobile app itself.
You may decide not to use these apps from the official store because of security concerns.  Thats OK because luckily TIDBYT lets you push your own apps.

The way you can use these apps effectively is by writing a small and simple script that re-pushes them on a cadence (say once an hour).
[I'll include a few examples of scripts here in the future when time permits, or if anyone else would like to share some, I'll include them here]

You will need PIXLET. You can get it here: https://tidbyt.dev/docs/build/installing-pixlet
PIXLET will be used to compile (or as it is called render) the app, and send it to your TIDBYT.

Prep:

Get your TIDBYT's device ID and API key.
- Open the TIDBYT app on your phone, tap the cog icon, and tap General.
- Tap Get API key
- Tap Copy to Clipboard for each one at a time and paste them both in a text editor.

Get your Workspace ONE UEM API user credentials and the tenant code
- The tenant code is the AirWatchAPI Key in the REST API screen.
- The API admin user's credentials. You may need to create a new admin user with at least the API role unless you have one already created.
- Today this app only supports Basic authentication.
- Basic username and password in plain text.  The code will convert it to Base64.

Your tenant's API URL.
- This is your tenant URL but changing cn to as.
- For example the regular console URL could be https://cn135.awmdm.com and the API URL would be https://as135.awmdm.com

Your tenant's root OG ID number.
- To find this, look at the number at the end of the URL after navigating to OG Details page.

One-time Setup.
- Edit the app file you want to use (WSONEDevices.star and/or WSONEDevByType.star) and paste in the required info from your tenant.
- Save the file.

Send the apps to your TIDBYT:

- Open Terminal (macOS and Linux) or Command Line (Windows) and change to the folder where your saved the edited files (WSONEDevices.star and/or WSONEDevByType.star)
- Type: pixlet render NameOfApp.star
- e.g. pixlet render WSONEDevices.star
- e.g. pixlet render WSONEDevByType.star
- 
- A new file called NameOfApp.wepb should appear in the folder.
- e.g. WSONEDevices.webp
- e.g. WSONEDevByType.webp
- 
- Type: pixlet push --installation-id WSONEDevices --api-token your_TIDBYT_API_token "your_TIDBYT_Device_ID" WSONEDevices.webp
- Type: pixlet push --installation-id WSONEDevByType --api-token your_TIDBYT_API_token "your_TIDBYT_Device_ID" WSONEDevByType.webp

Pushing the apps to your TIDBYT one time will display the information frozen in time.  It will never update.
To get the apps to update, you'll need to write a short script to render the apps and push them to your TIDBYT on a schedule, say once an hour.
Your script will need to execute these to lines repeatedly:
- pixlet render WSONEDevices.star
- pixlet render WSONEDevByType.star
- pixlet push --installation-id WSONEDevices --api-token your_TIDBYT_API_token "your_TIDBYT_Device_ID" WSONEDevices.webp
- pixlet push --installation-id WSONEDevByType --api-token your_TIDBYT_API_token "your_TIDBYT_Device_ID" WSONEDevByType.webp


