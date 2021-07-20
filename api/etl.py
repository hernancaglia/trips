import pandas as pd
import mysql.connector
from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_extract, col, UserDefinedFunction
from pyspark.sql.types import StringType
from pyspark.sql.types import DoubleType
from app_config import celery, socketio
from datetime import datetime


def send_message(event, message, namespace, room):
    print(message)
    socketio.emit(event, {'msg': message}, namespace=namespace, room=room)


def get_data():
    spark = SparkSession \
        .builder \
        .config("spark.driver.memory", "15g") \
        .appName("trips") \
        .getOrCreate()
    df = spark.read.csv('/trips/data/trips.csv', header=True)

    return df


def clean_data(df):
    x_pattern = '(?<=\()(.*?)(?=\ )'
    y_pattern = UserDefinedFunction(lambda x: x.split(' ')[-1][:-1], StringType())
    origin_x = regexp_extract(df.origin_coord, x_pattern, 1)
    destination_x = regexp_extract(df.destination_coord, x_pattern, 1)

    df = df.withColumn("origin_x", origin_x.cast(DoubleType()))    
    df = df.select("*", y_pattern("origin_coord").cast(DoubleType()).alias('origin_y'))
    df = df.withColumn("destination_x", destination_x.cast(DoubleType()))
    df = df.select("*", y_pattern("destination_coord").cast(DoubleType()).alias('destination_y'))
    df = df.drop("origin_coord", "destination_coord")
    df = df.withColumnRenamed("datetime", "trip_datetime")

    return df


def load_data(df):
    df.write.format('jdbc').options(
        url='jdbc:mysql://database:3306/backend',
        driver='com.mysql.cj.jdbc.Driver',
        dbtable='trips',
        user='root',
        password='root').mode('append').save()


@celery.task
def run(session_id):

    room = session_id
    namespace = '/etl'

    send_message('msg', f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - Begin task {run.request.id}', namespace, room)
    send_message('msg', f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - Getting data', namespace, room)
    df = get_data()

    send_message('msg', f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - Cleaning data', namespace, room)
    df = clean_data(df)

    send_message('msg', f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - Loading data into database', namespace, room)
    load_data(df)

    send_message('msg', f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - {df.count()} rows inserted', namespace, room)
    send_message('msg', f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - End task {run.request.id}', namespace, room)
    send_message('status', f'End', namespace, room)
