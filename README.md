docker compose up --scale spark-worker=3 -d\n
On namenode Run : hdfs dfs -put /data/data.csv /data.csv\n
On Spark master Run : pip3 install numpy; bin/spark-submit --master spark://spark-master:7077 /opt/spark-apps/k-means.py\n
