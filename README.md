# Trips

Data Engineering project using trips data

## Instructions

Install Docker and Docker Compose

Run project:

```bash
$ docker-compose up
```

## Access MySQL database

```bash
docker exec -it trips_db bash
mysql -u testuser -padmin123
use backend
show tables;
SELECT * FROM trips LIMIT 10;
```

## Subscribe to ETL status

http://localhost:5000

If ran from a browser, you can use the 'Start ETL' button to run the ETL. You can also run it using GET as explained below.

## Run ETL using GET

http://localhost:5000/run_etl

## Weekly Average Trips Report

Get the weekly average number of trips for an area, defined by a region or by a coordinates box.

Example using a region:

http://localhost:5000/weekly-avg?search=region&value=hamburg

Example using coordinates:

http://localhost:5000/weekly-avg?search=box&value={"x_lower":7,"x_upper":8.5,"y_lower":44,"y_upper":47}

## Test using 1 million rows

Load test_raw_bigtrips table with 1.024.000 rows (this can take about 5 minutes):

http://localhost:5000/load_bigtrips

Run the test ETL (about 2 minutes):

http://localhost:5000/test_bigtrips

After receiving the 'test_bigtrips loaded' message, the clean data is available in the bigtrips table:
```bash
mysql> show tables;
+-------------------+
| Tables_in_backend |
+-------------------+
| bigtrips          |
| test_bigtrips     |
| trips             |
+-------------------+

mysql> select count(*) from bigtrips;
+----------+
| count(*) |
+----------+
|  1024000 |
+----------+

mysql> select * from bigtrips limit 5;
+--------+---------------------+------------+-------------------+-------------------+-------------------+-------------------+
| region | trip_datetime       | datasource | origin_x          | origin_y          | destination_x     | destination_y     |
+--------+---------------------+------------+-------------------+-------------------+-------------------+-------------------+
| Prague | 2018-05-28 09:03:40 | funny_car  |  14.4973794438195 | 50.00136875782316 | 14.43109483523328 | 50.04052930943246 |
| Prague | 2018-05-28 09:03:40 | funny_car  |  14.4973794438195 | 50.00136875782316 | 14.43109483523328 | 50.04052930943246 |
| Prague | 2018-05-28 09:03:40 | funny_car  |  14.4973794438195 | 50.00136875782316 | 14.43109483523328 | 50.04052930943246 |
| Turin  | 2018-05-21 02:54:04 | baba_car   | 7.672837913286881 |  44.9957109242058 | 7.720368637535126 | 45.06782385393849 |
| Turin  | 2018-05-21 02:54:04 | baba_car   | 7.672837913286881 |  44.9957109242058 | 7.720368637535126 | 45.06782385393849 |
+--------+---------------------+------------+-------------------+-------------------+-------------------+-------------------+
```
