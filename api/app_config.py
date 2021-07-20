import os
from flask import Flask
from flask_socketio import SocketIO
from celery import Celery

# App configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Celery configuration
app.config['CELERY_BROKER_URL'] = os.getenv('CELERY_BROKER_URL')

# SocketIO configuration
app.config['SOCKETIO_BROKER_URL'] = os.getenv('SOCKETIO_BROKER_URL')

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Initialize SocketIO
socketio = SocketIO(app, message_queue=app.config['SOCKETIO_BROKER_URL'])
