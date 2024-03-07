from pyspark.sql import SparkSession
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler
import matplotlib.pyplot as plt

# Initialize a Spark session
spark = SparkSession.builder \
    .appName("KMeansECommerce") \
    .config("spark.driver.memory", "100m") \
    .getOrCreate()

# Load the dataset
df = spark.read.csv('hdfs://namenode:9000/data.csv', header=True, inferSchema=True)

# Define the columns to be used as features
columns = ["feature1", "feature2", "feature3"]  # Replace with your actual column names

# Combine features into a single vector column
vec_assembler = VectorAssembler(inputCols=columns, outputCol="features")
df_vector = vec_assembler.transform(df)

# Apply K-means clustering
kmeans = KMeans(featuresCol="features", k=3)  # Set k=3 clusters
model = kmeans.fit(df_vector)

# Make predictions
predictions = model.transform(df_vector)

# Show results
predictions.select("features", "prediction").show()

# Collect data to a Pandas DataFrame for visualization
pandas_df = predictions.select("features", "prediction").toPandas()

# Extract individual features from the 'features' column for plotting
pandas_df["feature1"] = pandas_df["features"].apply(lambda x: x[0])
pandas_df["feature2"] = pandas_df["features"].apply(lambda x: x[1])
pandas_df["feature3"] = pandas_df["features"].apply(lambda x: x[2])

# Plot the data
plt.figure(figsize=(10, 6))
for cluster in range(3):  # Assuming k=3 clusters
    clustered_data = pandas_df[pandas_df["prediction"] == cluster]
    plt.scatter(clustered_data["feature1"], clustered_data["feature2"], label=f"Cluster {cluster}")

plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.legend()
plt.title("K-means Clustering Results")

# Save the plot locally
plot_filename = "kmeans_clusters.png"
plt.savefig(plot_filename)

# Stop the Spark session
spark.stop()
