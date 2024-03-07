from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("KafkaSparkIntegration") \
    .getOrCreate()

# Create DataFrame representing the stream of input lines from Kafka
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "kafka:9092") \
  .option("subscribe", "ticker-HITBTC-XLM-USDT") \
  .load()

df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

# Place your data processing logic here
# For example, writing the stream to the console
df.writeStream \
  .outputMode("append") \
  .format("console") \
  .start() \
  .awaitTermination()
