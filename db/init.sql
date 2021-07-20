CREATE TABLE IF NOT EXISTS trips (
    id int NOT NULL AUTO_INCREMENT,
    region varchar(255) NOT NULL,
    origin_x decimal(17, 2) NOT NULL,
    origin_y decimal(17, 2) NOT NULL,
    destination_x decimal(17, 2) NOT NULL,
    destination_y decimal(17, 2) NOT NULL,
    trip_datetime datetime NOT NULL,
    datasource varchar(255) NOT NULL,
    data_timestamp datetime DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);