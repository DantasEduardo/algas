from pyspark.sql import SparkSession
from pyspark.sql.functions import split, when, col

print("INFO: Starting spark session")
spark = SparkSession.builder.appName("raw-stagged").getOrCreate()

print("INFO: Reading data")
df = spark.read.parquet("data-stagged/")

print("INFO: Clean data")
split_col = split(df["Location"], "-")
df = df.withColumn("Country", split_col.getItem(0))\
       .withColumn("State", split_col.getItem(1))\
       .withColumn("City", split_col.getItem(2))

df = df.drop("Location")

df = df.withColumn("Country", when(col("Country") == "BR", "Brazil"))\
       .withColumn("State", when(col("State") == "SP", "Sao Paulo"))\
       .withColumn("City", when(col("City") == "Sp", "Sao Paulo"))

print("INFO: Saving data")
df.coalesce(1).write.parquet("data-consumed/")

print(df.show(n=5))
print(df)
spark.stop()
