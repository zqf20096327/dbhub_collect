-Clone the project to your computer
Choose the data set from /datasets/folder. (DS from now)
-The metric value must be omitted. The value must be one of these:

| Metric    | Command Value|
| Eucledian |     "eu"     |
| Manhattan |     "ma"     |
| Minkowski |   "mi (m)"   |

-When Minkowski metric is chosen a value for root ( m ) must be specified.  

-The reference point(to which the distance is calculated and the points are sorted by that distance) type must be omitted. The values must be one of these:

|    Reference type        |     Command Value   |
|   Coordinate origin      |          "0"        |
| Maximum attribute values |         "max"       |
| Minimum attribute values |         "min"       |
|    Max,min,max,min....   |        "maxmin"     |
|   Min,max,min,max....    |        "minmax"     |


- On the project's main directory run:
java -jar TIDBSCAN.jar DS.txt radius minp [metric [m]] referenceType > out.txt

Example : java -jar TIDBSCAN.jar iris.txt 1 4 mi 2 max > out.txt

-The output will be in the main directory as "out.txt". 


