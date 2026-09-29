# [](https://github.com/fourstops/tidbyt-json/edit/main/README.md#tidbyt-json)tidbyt-json

Send sensor data to JSON using Python for use in Tidbyt. 

This example uses the BME280 sensor and outputs data to a json file on a web server. Using a shell script and crontab, the json file is updated every 10 seconds with new sensor data. 

    * * * * * sh /home/pi/tidbyt-json/run.sh
