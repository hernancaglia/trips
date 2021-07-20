import os
from pyspark.sql import SparkSession
from app_config import app, socketio
import reporting
from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from flask_socketio import join_room, leave_room
import uuid
import time 
import random
from distutils.util import strtobool
from random import randint
import etl


@app.route("/", methods=['GET'])
def index():
    if 'uuid' not in session:
        session['uuid'] = str(uuid.uuid4())

    return render_template('index.html')


@app.route("/run_etl", methods=['GET', 'POST'])
def run_etl():
    session_id = str(session['uuid'])
    task = etl.run.delay(session_id=session_id)
    
    return jsonify({'id': task.id})


@socketio.on('join_etl', namespace='/etl')
def on_room():
    room = str(session['uuid'])
    print(f'join room {room}')
    join_room(room)


@app.route('/weekly-avg')
def get_weekly_avg():
    search = request.args.get('search')
    value = request.args.get('value')
    report = reporting.get_weekly_avg(search, value)
    return jsonify(report)


@app.route('/get_trips')
def get_trips():
    df = reporting.get_trips()
    df.write.csv('get_trips.csv', header=True)
    return jsonify('trips downloaded')


@app.route('/load_bigtrips')
def load_raw_bigtrips():
    # Load test_raw_bigtrips table with 1 million rows 
    df = etl.get_data()

    for i in range(11):
        df = df.union(df)

    print('Loading 1M rows to database...')
    for i in range(5):
        df.write.format('jdbc').options(
            url='jdbc:mysql://database:3306/backend',
            driver='com.mysql.cj.jdbc.Driver',
            dbtable='test_raw_bigtrips',
            user='root',
            password='root').mode('append').save()
    
    return jsonify('1,103,500 rows inserted into test_raw_bigtrips')


@app.route('/test_bigtrips')
def test_bigtrips():
    # Get 1 million rows from database
    spark = SparkSession \
        .builder \
        .config("spark.driver.memory", "15g") \
        .appName("trips") \
        .getOrCreate()

    df = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:mysql://database:3306/backend") \
        .option("dbtable", "test_bigtrips") \
        .option("user", "root") \
        .option("password", "root") \
        .load()

    df = etl.clean_data(df)

    df.write.format('jdbc').options(
        url='jdbc:mysql://database:3306/backend',
        driver='com.mysql.cj.jdbc.Driver',
        dbtable='bigtrips',
        user='root',
        password='root').mode('append').save()

    return jsonify('test_bigtrips loaded')


@socketio.on('connect')  # BEING USED
def socket_connect():
    pass


if __name__ == '__main__':
    # socketio.run(app, host='0.0.0.0', port=5000) MINE
    socketio.run(
        app=app,
        host=os.getenv('FLASK_RUN_HOST'),
        port=os.getenv('FLASK_RUN_PORT'),
        debug=strtobool(os.getenv('FLASK_DEBUG'))
    )
