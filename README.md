In root file: docker build -t hadoop:base .

In hdfs-namenode: docker build -t hadoop:namenode .

In hdfs-datanode: docker build -t hadoop:datanode .

docker compose up --scale spark-worker=3 -d

On namenode Run : hdfs dfs -put /data/data.csv /data.csv

On Spark master Run : pip3 install numpy; bin/spark-submit --master spark://spark-master:7077 /opt/spark-apps/k-means.py
