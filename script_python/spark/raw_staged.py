import re
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, col
from pyspark.sql.types import DateType
from datetime import datetime

print("INFO: Starting spark session")
spark = SparkSession.builder.appName("raw-stagged").getOrCreate()

print("INFO: Reading data")
with open("./data-raw/b68fd18d-c01e-000c-2cc7-91006e06c16bsensor_data.json", "r") as file: data_raw = file.read()

print("INFO: Clean data")
data_body = [value for value in re.findall(r'"Body":"([^"]*)"', data_raw)]
data_body = [value.split('/') for value in data_body]

print("INFO: Create spark dataframe")
# temperature, pressure, air_speed, batery, batery
df = spark.createDataFrame(data_body, ["Temperature", "Pressure", "WindSpeed", "drop1", "drop2", "Location"])
df = df.drop("drop1").drop("drop2")
df = df.withColumn("Date", lit(datetime.now().date()).cast(DateType()))

print("INFO: Drop empty values")
df.na.drop()

print("INFO: Cast type of columns")
df = df.withColumn("Temperature", col("Temperature").cast("float"))\
       .withColumn("Pressure", col("Pressure").cast("float"))\
       .withColumn("WindSpeed", col("WindSpeed").cast("float"))

print("INFO: Saving data")
df.coalesce(1).write.parquet("data-stagged/")

print(df.show(n=5))
print(df)
spark.stop()
