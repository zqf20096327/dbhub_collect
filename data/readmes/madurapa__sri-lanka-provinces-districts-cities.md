# Sri Lanka Provinces Districts Cities Database


### About

This is a MySQL version of Sri Lankan Provinces => Districts => Cities, and related data. Each city has longitude, latitude, and postal code (postcode) other than its name.

### Data Errors
If you discover wrong translations or any other issues, please use the issue tracker to mention or send a pull request with the changes.

There are three SQL files,
 1. provinces.sql (Names of nine provinces)
 2. districts.sql (All districts related to each province)
 3. cities.sql (All cities related to each district)


### Updates

* July 18, 2016 - Changed the structure of cities table ability to add sub-city names.
* April 25, 2022 - Completed translations in all three languages.


### Statistics

*  Provinces - 9
*  Districts - 25
*  Cities - 2154


### Sample tables structure with data

**Provinces**

| id  | name_en | name_si  | name_ta |
| --- | ------- | -------- | ------- |
| 1   | Western | බස්නාහිර  | மேல     |
| 2   | Central | මධ්‍යම   | மத்தி     |


**Districts**

| id  | province_id| name_en      | name_si      | name_ta      |
| --- | ---------- | ------------ | ------------ | ------------ |
| 1   | 6          | Ampara       | අම්පාර        | அம்பாறை      |
| 2   | 8          | Anuradhapura | අනුරාධපුරය    | அனுராதபுரம்     |


**Cities**

| id  | district_id | name_en   | name_si  | name_ta  | sub_name_en | sub_name_si | sub_name_ta | postcode | latitude  | longitude |
| --- | ---         | ---       | ---      | ---       | ---        | ---         | ---         | ---      | ---       | ---       |
| 338 | 5           | Colombo 8 | කොළඹ 8 | கொழும்பு 8 | Borella    | බොරැල්ල     | பொறளை    | 00800     | 6.914722  | 79.877778 |
| 376 | 5           | Colombo 6 | කොළඹ 6 | கொழும்பு 6 | Wellawatta | වැල්ලවත්ත   | வெள்ளவத்தை | 00600     | 6.874657  | 79.860483 |


### Installation

To prevent unnecessary errors from occurring, start to import or execute provinces.sql, then districts.sql, and lastly cities.sql


### Usage

**Advantages of latitude and longitude**

* Integrate with Google Maps or any map-related service to show the exact place of the city on the map.
* Find locations within a certain radius of a given latitude/longitude.

**Find nearby locations using the Haversine formula**

Here's the SQL statement that will find the closest locations within a radius of 25 kilometers to the 7.358849, 81.280133 coordinate. It calculates the distance based on the latitude/longitude of that row and the target latitude/longitude and then asks for only rows where the distance value is less than 25, ordering the whole query by distance.

```SQL
SELECT id, name_en, name_si, name_ta, (6371 * ACOS(COS(RADIANS(7.358849)) * COS(RADIANS(latitude)) * COS(RADIANS(longitude) - RADIANS(81.280133)) + SIN(RADIANS(7.358849)) * SIN(RADIANS(latitude)))) AS distance
FROM cities
HAVING distance < 25
ORDER BY distance
```
<em>The above assumes that you have distance in kilometers.  If distance is in miles then replace 6371 with 3959.</em>

References:

* https://en.wikipedia.org/wiki/Haversine_formula
* https://stackoverflow.com/questions/574691/mysql-great-circle-distance-haversine-formula

### Note

* This free database does not guarantee the complete list of cities in Sri Lanka.
* Feel free to contribute to the project.


### Translation status

**Provinces**
> 
> | සිංහල | தமிழ |  
> | ---- | ---- |
> | 100% | 100% |

**Districts**
> 
> | සිංහල | தமிழ |  
> | ---- | ---- |
> | 100% | 100% |

**Cities**
> 
> | සිංහල | தமிழ |  
> | ---- | ---- |
> | 100% | 100% |

