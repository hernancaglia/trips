"""
from pyspark.sql.functions import regexp_extract, col, UserDefinedFunction
from pyspark.sql.types import StringType
"""
import mysql.connector
import pandas
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import weekofyear, year


def get_trips():
    spark = SparkSession \
        .builder \
        .appName("trips") \
        .getOrCreate()

    sql = "SELECT * FROM backend.trips"

    df = spark.read.format("jdbc").options(
        url="jdbc:mysql://database:3306/backend",
        driver = "com.mysql.cj.jdbc.Driver",
        query = sql,
        user="root",
        password="root").load()
        
    return df


def get_weekly_avg(search, value):
    """
    Args:
        search (str): 'region' to search for a specific region
            or 'box' to use coordinates
        value (str_or_dict): Region name or coordinates dict
            Coordinates dict should have:
            x_upper (float)
            x_lower (float)
            y_upper (float)
            y_lower (float)
    
    Returns:
        json: weekly avg number of trips for the area
    """

    spark = SparkSession \
            .builder \
            .appName("trips") \
            .getOrCreate()


    if search == 'region':
        sql = f"""SELECT trip_datetime
            FROM backend.trips
            WHERE region = '{value}'
            """
    elif search == 'box':        
        box = json.loads(value)
        sql = f"""SELECT trip_datetime
            FROM backend.trips
            WHERE origin_x < {box['x_upper']}
                AND origin_y < {box['y_upper']}
                AND destination_x > {box['x_lower']}
                AND destination_y > {box['y_lower']}
            """

    df = spark.read.format("jdbc").options(
        url="jdbc:mysql://database:3306/backend",
        driver = "com.mysql.cj.jdbc.Driver",
        query = sql,
        user="root",
        password="root").load()

    df = df.withColumn('week_of_year', weekofyear(df.trip_datetime))
    df = df.withColumn('year', year(df.trip_datetime))
    count_perweekandyear = df.groupBy('week_of_year', 'year').count()
    avg_perweek = count_perweekandyear.groupBy('week_of_year').avg('count')

    # return df.toPandas().to_json(orient='values')  if we need to customize
    return avg_perweek.toJSON().collect()
