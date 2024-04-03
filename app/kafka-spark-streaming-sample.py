from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, avg, max, min, from_unixtime
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

# {"exchange":"BEQUANT","symbol":"ETH-USDT","bid":3327.748,"ask":3328.3,"timestamp":1712140770.536,"receipt_timestamp":1712140770.666301}
schema = StructType([
    StructField("exchange", StringType()),
    StructField("symbol", StringType()),
    StructField("bid", DoubleType()),
    StructField("ask", DoubleType()),
    StructField("timestamp", DoubleType()),
    StructField("receipt_timestamp", DoubleType())
])

# Create a SparkSession
spark = SparkSession \
    .builder \
    .appName("KafkaSparkIntegration") \
    .getOrCreate()

spark.conf.set("spark.sql.streaming.metricsEnabled", "true")

# Create DataFrame representing the stream of input lines from Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "ticker-BEQUANT") \
    .load()

# Parse the value column as JSON and apply the schema
parsed_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Define the window duration and slide interval
window_duration = "1 minute"
slide_interval = "30 seconds"
parsed_df = parsed_df.withColumn("receipt_timestamp", from_unixtime(col("receipt_timestamp"), "yyyy-MM-dd HH:mm:ss.SSSSSS"))

# Group by symbol and calculate aggregations within the window
aggregated_df = parsed_df \
    .groupBy(
        window(col("receipt_timestamp"), window_duration, slide_interval),
        col("symbol")
    ) \
    .agg(
        avg("bid").alias("avg_bid"),
        avg("ask").alias("avg_ask"),
        max("bid").alias("max_bid"),
        min("ask").alias("min_ask"),
        max("timestamp").alias("last_timestamp")
    )

# Write the aggregated data to the console
query = aggregated_df \
    .writeStream \
    .outputMode("update") \
    .format("console") \
    .option("truncate", "false") \
    .start()

query.awaitTermination()