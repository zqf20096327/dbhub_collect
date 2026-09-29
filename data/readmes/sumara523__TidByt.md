##To run server locally:

`python3 boat.py`

Will run on http://127.0.0.1:5000

##To run the tidbyt on pixlet CLI

first download pixlet:
https://tidbyt.dev/docs/build/installing-pixlet

After you have the CLI tool installed, run

`pixlet serve helloworld.star`

This will launch the app on http://127.0.0.1:8080

##To depoly to your own tidbyt device

first login and get the device ID (should be the text thats just hyphenated):

`pixlet login`

`pixlet devices`

To deploy:

`pixlet render helloworld.star`

`pixlet push <Your Device ID> helloworld.webp`

***After you host boat.py to your Rasperry Pi Mattieu, you will need to update BOAT_SERVER_URL in helloworld.star file with the new url, but keep the appended "/get_bridge_status" because that url is where the bridge status information is fetched from. Bonne chance!