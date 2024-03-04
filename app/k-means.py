from pyspark.sql import SparkSession
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler
from pyspark.sql.functions import col

# Initialize a Spark session
spark = SparkSession.builder \
    .appName("KMeansECommerce") \
    .config("spark.driver.memory", "100m") \
    .getOrCreate()

# Load the dataset
data = spark.read.csv('hdfs://namenode:9000/data.csv', header=True, inferSchema=True)

# Fill in missing values if necessary
avg_days = data.agg({'days_since_prior_order': 'avg'}).first()[0]
data = data.fillna({'days_since_prior_order': avg_days})

# Select features for clustering and assemble them into a feature vector
feature_columns = ['order_dow', 'order_hour_of_day', 'days_since_prior_order']
assembler = VectorAssembler(inputCols=feature_columns, outputCol='features', handleInvalid='skip')
data = assembler.transform(data)

# Train a KMeans model
kmeans = KMeans().setK(3).setSeed(1)
model = kmeans.fit(data)

# Make predictions
predictions = model.transform(data)

# Define the output path on HDFS
output_path = "./result"

# Save the predictions to HDFS in parquet format
predictions_without_features = predictions.drop('features')

# Save the modified DataFrame to a CSV file in HDFS
predictions_without_features.write.csv(output_path, header=True, mode='overwrite')

# Stop the Spark session
spark.stop()
