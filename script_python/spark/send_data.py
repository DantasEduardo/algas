"""
CREATE TABLE IF NOT EXISTS `sensor_metrics` (
    id int PRIMARY KEY AUTO_INCREMENT,
    temperature DOUBLE,                      
    pressure  DOUBLE,                    
    windSpeed  DOUBLE,                    
    date DATE,
    country varchar(25),
    state varchar(25),
    city varchar(25)
);
"""

import mysql.connector
import pandas as pd

QUERY = "INSERT INTO sensor_metrics(temperature,pressure,windSpeed,date,country,state,city) VALUES (%s,%s,%s,%s,%s,%s,%s)"

print("INFO: Reading data")
df = pd.read_parquet("data-consumed/")
print(df.head(n=5))

registers = df.values.tolist()


print("INFO: Conecting with DB")
mydb = mysql.connector.connect(
    host = 'soy-bean-02211010.mysql.database.azure.com',
    user = 'root02211010',
    database = 'sensor_data',
    password = 'Urubu100',
    port = "3306")

mycursor = mydb.cursor()

print("INFO: Sending sensor data")
for values in registers:
    mycursor.execute(QUERY, values)
    mydb.commit()
