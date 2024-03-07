Prepare for docker compose-------To build images for hdfs

In root dir: docker build -t hadoop:base .

In hdfs-namenode: docker build -t hadoop:namenode .

In hdfs-datanode: docker build -t hadoop:datanode .


Run the docker compose:

docker compose up --scale spark-worker=3 -d

On namenode Run : hdfs dfs -put /data/data.csv /data.csv

To enable anyone to write and access, on hadoop namenode run: hdfs dfs -chmod 777 /

On Spark master Run : 

  pip3 install numpy pandas matplotlib requests; bin/spark-submit --master spark://spark-master:7077 /opt/spark-apps/k-means.py

To save the file to hdfs, on spark master run:

  python3 /opt/spark-apps/save.py

To view the saved file:

For docker network, i have not find a good way to view file on host locally, because files are on datanode, when localhost request resouce from hdfs, Namenode server will send the datanode dns name to localhost, and redirect host to a path on the dns name, but host machine can't resolve it. So the way is to use VSC to "attach to running container", then curl the file with(I want to see the result image, here is a demo):

curl -L "http://localhost:9870/webhdfs/v1/kmeans_clusters.png?op=OPEN" -o kmeans_clusters.png

And open the file in VSC


### Connect to Kafka

- run above docker compose to start spark

- git clone realtime-data-analysis repo

```
git clone https://github.com/cs6675-spring24-group13/realtime-data-analysis.git
```

- run docker compose at above repo's root dir

```
docker compose up -d
```


- in spark master, run program below. kafka-connect.py is a sample program that basically stdout the kafka's event only

```
bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1 --master spark://spark-master:7077 /opt/spark-apps/kafka-connect.py
```

