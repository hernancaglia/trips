FROM jupyter/pyspark-notebook

USER root

RUN apt-get update
RUN apt-get -y install rabbitmq-server

USER $NB_UID

WORKDIR /trips/api

COPY requirements.txt requirements.txt
COPY mysql-connector-java-8.0.25.jar $SPARK_HOME/jars/mysql-connector-java-8.0.25.jar

EXPOSE 5000

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
