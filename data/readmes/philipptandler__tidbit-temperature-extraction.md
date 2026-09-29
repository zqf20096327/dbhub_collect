# TidbiT-temperature-extraction
This is for reading, plotting, interpolating temperature measurments form HOBO
TidbiT temperature loggers. The intended use is to have an estimate of
temperature measurements for a given TidbiT (via name or ID) at a given time.
This can be used to compare TidbiT measurements with temperature values in a
thermal orthomosaic. This repository is designed for Selkirk Innovates internal
used, but can of course be adapted.

# The Problem
Consider you have a thermal orthomosaic of a study area, with maybe ten TidbiT 
temperature loggers distributed across the study area. You then want to extract 
the temperature measured by the TidbiT loggers at the time of the survey. But 
the larger the study area, and the longer the duration of it takes to complete 
the survey, the less the assumtion holds that each pixel has a constant 
temperature for the time of the survey. Therefore, to compare the TidbiT
measurements with the orthomosaic, it would be crucial to know the time the
drone passed over a particular TidbiT's location, and then extract the 
temperature measured by this particular TidbiT at this particular time. The drone 
passes over a TidbiT's location many times and takes multiple images. Here, I 
refer to the timesstamp as the time of an image was taken which contains
the TidbiT's location. As the problem suggests, there are two steps in this process:
First, to extract the teimstamps the drone passes over the TidbiTs location.
Second, to extract the temperautre of the TidbiT at this specific time.

# Usage
## Step 1: Extract Times of the orthomosaic
This repository is built for extracting temperatures in Agisoft Metashape, but 
I am sure this can be adapted to work in other environments. 

To extract the timestamps of the individual photos that captured a TidbiT's location, 
follow those steps in Agisoft Metashape:

1. Make sure the TidbiT's locations are loaded. To ddo this, go to Reference 
Pane > Import Reference, select location file of TidbiT's, choose CRS, 
check Northing and Easting > OK).

2. Display the locations of the TidbiTs and the Camera locations.

3. Make sure no photos are selected. Then, Using the Circular 'Selection' tool,
select photos around a TidbiT's location marker within reasonable distance (I 
press on the marker and drag the circle until it has 10 to 20 camera locations 
selected. Choose the radius accoding to flight height and width of the camera angle.)
This gives all the photos and respective imestamps that contribute to the temperautre 
at the TidbiTs location.

4. Run `extract_times_selectedImages.py`:
In Agisoft Metashape, go to Tools > Run Script > choose above script.
This script writes the times into a file called `Times_SelectedImages_from_AgisoftMetashape.csv`.

5. Copy this into a spreadsheet which holds the all timestamps and TidbiT IDs.
I typically also write the Coordinates, TidbiT Name, and further TB meta information in there, but that's not required.
Tip: I would recommend to load the GNSS data of the TidbiTs including metadata in QGIS, 
extract the temperature of the orthomosaic at the TidbiT's locations, and export.
This can then serve as template to fill in the extracted timestamps (you will 
need one line for each timestamp, not one for each TidbiT), so the spreadsheet
will grow quite a bit.

6. Repeat for all TidbiT locations, resulting in one master spreadsheed. Save as `.csv`.
This should contain for all TitbiTs location all the timestamps that location was passed by the drone.


## Step 2: Extract Temperatures of the TidbiTs

In this step, the extracted timestamps are used to extract the temperature of the
TidbiTs by interpolating the TidbiT time series. This results in individual temperature values
for each image timestamp, which is then averaged. So essentially each
TidbiT location and timestamp is matched with the TidbiT time series to extract the 
temperature at the exact time.

1. Make sure all the TidbiT time series are prepared in a directory, lets call it `prepared`,
and all the temperature time series are named after the `TidbiT's` ID, e.g. `prepared/21459191.csv`

2. Make sure all time formats are the same for all temperature time series.

3. In `config/config.R`, adjust the time format and column names or numbers.

4. The file `config/tidbit_name_id_lib.csv` is a library for TidbiT names with
their ID. This can be useful to e.g. plot the timeseries using the Name rather the ID.

5. Run `extract_tidbit_temperature.R`. Specify the directory `prepared` with the TidbiT time series.

   - `TB_lib()` returns the current library of TidbiT names and IDs
   
   - `TB_temp()` and `TB_plot()` return the temperature at a particular time, or plot the temperature for a range of time.
   They take either `name` or `ID` as argument, as well as `time`, or `time_start` and `time_end`, respectively, 
   or `datetime`, `datetime_start` and `datetime_end` respectively.
   The time must be in 24h format `17:30:45`, datetime in `2025-09-04 08:13:23` format.
   
   - `batch_TB_temp()` calculates for each TidbiT location and each timestamp 
   the temperature by interpolating the TidbiT timeseries. It writes the
   result in two tables as csv files. One with all the temperatures at the time of each image, 
   and one where the temperature is averaged for each TidbiT location.
   
6. The resulting tables can then be used to compare the TidbiT measured temperatre
with the temperature from the orthomosaic.


Typically, if sth doesnt work, check the `config/config.R` file and make sure it
is consistent with the formating in the files.






