import os
from pyspark.sql import SparkSession
from config.SparkConn import jdbcUrl, connectionProperties

# os.environ["PYSPARK_PYTHON"] = "C:Users\siyuan\AppData\Local\Programs\Python\Python38\python.exe"
# Init Spark
spark = SparkSession.builder \
    .appName("gcloud_sql") \
    .config("spark.jars", "../postgresql-42.6.0.jar") \
    .master("local").getOrCreate()

df = spark.read.jdbc(url=jdbcUrl, table="idc_team", properties=connectionProperties)

if __name__ == "__main__":
    df.show(2)