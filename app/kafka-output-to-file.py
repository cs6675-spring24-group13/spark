from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("KafkaSparkIntegration") \
    .getOrCreate()
spark.conf.set("spark.sql.streaming.metricsEnabled", "true")

# Create DataFrame representing the stream of input lines from Kafka
# available topic: ticker-BEQUANT, ticker-HITBTC
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "kafka:9092") \
  .option("subscribe", "ticker-BEQUANT") \
  .load()

processed_df = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

# Define the path where the output files will be saved
outputPath = "/opt/spark-outputs"

# Writing the stream to a file
# Trigger the query every 5 minutes
query = processed_df.writeStream \
  .outputMode("append") \
  .format("csv") \
  .option("path", outputPath) \
  .option("checkpointLocation", "/opt/spark-outputs/checkpoints") \
  .trigger(processingTime='5 minutes') \
  .start() \
  .awaitTermination()