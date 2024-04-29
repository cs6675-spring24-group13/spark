# from pyspark.sql import SparkSession
# from pyspark.sql.functions import col, window, avg, when, current_timestamp, expr, to_timestamp
# from pyspark.sql.types import StructType, StructField, StringType, DoubleType
# import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, window, avg, when, current_timestamp, expr, to_timestamp, from_json
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType
import pandas as pd
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

# Placeholder for global state
state = {
    "total_dropped": 0,
    "count_batches": 0,
    "min_dropped": float('inf'),
    "max_dropped": 0
}

def update_state(dropped_count):
    state['total_dropped'] += dropped_count
    state['count_batches'] += 1
    state['min_dropped'] = min(state['min_dropped'], dropped_count)
    state['max_dropped'] = max(state['max_dropped'], dropped_count)

    if state['count_batches'] > 0:
        average_dropped = state['total_dropped'] / state['count_batches']
    else:
        average_dropped = 0
    
    return (state['total_dropped'], state['min_dropped'], state['max_dropped'], average_dropped)

def process_batch(df, epoch_id):
    # Assuming receipt_timestamp is already converted to timestamp format and
    # watermarked
    if df.rdd.isEmpty():
        print("DataFrame is empty")
        return  # Skip further processing for this batch

    current_time = df.select(current_timestamp()).collect()[0][0]
    watermark_delay = pd.Timedelta('15 seconds')
    current_watermark = current_time - watermark_delay

    # Simulating the count of dropped rows (this would need actual logic to compare against a real watermark)
    dropped_count = df.filter(col("receipt_timestamp") < current_watermark).count()

    # Update state with the new dropped count
    total, min_dropped, max_dropped, average_dropped = update_state(dropped_count)

    # Here you can now log, print, or store these statistics somewhere
    print(f"Total Dropped: {total}, Min Dropped: {min_dropped}, Max Dropped: {max_dropped}, Average Dropped: {average_dropped}")

    # Perform your usual processing
    df.write.format("console").option("truncate", "true").save()

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

window_agg_df = parsed_df.groupBy(
    window(col("receipt_timestamp"), window_duration, slide_interval),
    col("symbol").alias("agg_symbol")  # Rename here
).agg(avg("bid").alias("avg_price"))

# Use DataFrame alias when performing join
joined_df = parsed_df.alias("raw").join(
    window_agg_df.alias("agg"),
    (col("raw.symbol") == col("agg.agg_symbol")),  # Use aliases in join condition
    "inner"
)

# Select columns using aliases to avoid ambiguity
trading_signals_df = joined_df.select(
    col("raw.receipt_timestamp"),
    col("raw.symbol"),
    col("raw.bid"),
    col("agg.avg_price"),
    when(col("raw.bid") > col("agg.avg_price"), "BUY")
        .when(col("raw.bid") < col("agg.avg_price"), "SELL")
        .otherwise("HOLD").alias("signal")
)

# Display the trading signals for each micro-batch
query = trading_signals_df \
    .writeStream \
    .outputMode("append") \
    .foreachBatch(process_batch) \
    .trigger(processingTime=slide_interval) \
    .start()

query.awaitTermination()
