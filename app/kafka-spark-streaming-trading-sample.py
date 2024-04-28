from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, avg, when, from_unixtime, to_timestamp
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

# Define the schema for the incoming JSON data
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


# Define the watermark on the receipt_timestamp column
watermark_threshold = "15 seconds"
parsed_df = parsed_df.withColumn("receipt_timestamp", to_timestamp(col("receipt_timestamp")))
parsed_df = parsed_df.withWatermark("receipt_timestamp", watermark_threshold)

# Define the window duration and slide interval
window_duration = "1 minute"
slide_interval = "30 seconds"

# Group by symbol and calculate the average price within each window
# window_agg_df = parsed_df \
#     .groupBy(
#         window(col("receipt_timestamp"), window_duration),
#         col("symbol").alias("agg_symbol")
#     ) \
#     .agg(avg("bid").alias("avg_price"))

# joined_df = parsed_df.join(
#     window_agg_df,
#     [parsed_df["symbol"] == window_agg_df["agg_symbol"]],
#     "inner"
# ).select(parsed_df["*"], window_agg_df["avg_price"])
window_agg_df = parsed_df.groupBy(
    window(col("receipt_timestamp"), window_duration, slide_interval),
    col("symbol")
).agg(avg("bid").alias("avg_price"))

joined_df = parsed_df.join(
    window_agg_df,
    (parsed_df["symbol"] == window_agg_df["symbol"]) &
    (parsed_df["receipt_timestamp"].between(window_agg_df["window"].start, window_agg_df["window"].end))
)
# Generate buy/sell signals based on the current price and average price
trading_signals_df = joined_df \
    .withColumn("signal", 
                when(col("bid") > col("avg_price"), "BUY")
                .when(col("bid") < col("avg_price"), "SELL")
                .otherwise("HOLD")
    ) \
    .select(
        "receipt_timestamp",
        "symbol",
        "bid",
        "avg_price",
        "signal"
    )

# debugQuery = parsed_df.writeStream \
#     .outputMode("append") \
#     .format("console") \
#     .option("truncate", "false") \
#     .queryName("DebugQuery") \
#     .start()
# debugQuery.awaitTermination()


# Display the trading signals for each micro-batch
query = trading_signals_df \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .trigger(processingTime=slide_interval) \
    .start()

query.awaitTermination()