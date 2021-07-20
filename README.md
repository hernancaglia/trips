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

http://localhost:5000/weekly-avg?search=box&value={"x_lower":7, "x_upper":8.5, "y_lower":44, "y_upper":47}

