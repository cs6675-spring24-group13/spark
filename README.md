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

- sample kafka event data (every line is a new event)

```
{"exchange":"HITBTC","symbol":"XLM-USDT","bid":0.11924,"ask":0.119283,"timestamp":1709146868.173,"receipt_timestamp":1709146868.180787}
{"exchange":"HITBTC","symbol":"XLM-USDT","bid":0.11924,"ask":0.119288,"timestamp":1709146868.373,"receipt_timestamp":1709146868.397893}
{"exchange":"HITBTC","symbol":"XLM-USDT","bid":0.119247,"ask":0.119288,"timestamp":1709146868.574,"receipt_timestamp":1709146868.5954921}
{"exchange":"HITBTC","symbol":"XLM-USDT","bid":0.119247,"ask":0.119283,"timestamp":1709146868.974,"receipt_timestamp":1709146869.012954}
{"exchange":"HITBTC","symbol":"XLM-USDT","bid":0.119247,"ask":0.119288,"timestamp":1709146869.374,"receipt_timestamp":1709146869.4037209}
{"exchange":"HITBTC","symbol":"XLM-USDT","bid":0.119247,"ask":0.119283,"timestamp":1709146869.975,"receipt_timestamp":1709146870.0044413}
{"exchange":"HITBTC","symbol":"XLM-USDT","bid":0.119247,"ask":0.119288,"timestamp":1709146870.376,"receipt_timestamp":1709146870.409218}
{"exchange":"HITBTC","symbol":"XLM-USDT","bid":0.119247,"ask":0.119288,"timestamp":1709146870.676,"receipt_timestamp":1709146870.872053}
{"exchange":"HITBTC","symbol":"XLM-USDT","bid":0.119247,"ask":0.119283,"timestamp":1709146870.776,"receipt_timestamp":1709146870.87225}
{"exchange":"HITBTC","symbol":"XLM-USDT","bid":0.119247,"ask":0.119288,"timestamp":1709146871.077,"receipt_timestamp":1709146871.4190223}
{"exchange":"HITBTC","symbol":"XLM-USDT","bid":0.119252,"ask":0.119288,"timestamp":1709146872.078,"receipt_timestamp":1709146872.2285795}
{"exchange":"HITBTC","symbol":"XLM-USDT","bid":0.119288,"ask":0.119306,"timestamp":1709146872.579,"receipt_timestamp":1709146872.6436334}
{"exchange":"HITBTC","symbol":"XLM-USDT","bid":0.119291,"ask":0.119306,"timestamp":1709146872.779,"receipt_timestamp":1709146872.78021}
{"exchange":"HITBTC","symbol":"XLM-USDT","bid":0.119295,"ask":0.119347,"timestamp":1709146873.58,"receipt_timestamp":1709146873.587899}
{"exchange":"HITBTC","symbol":"XLM-USDT","bid":0.119312,"ask":0.119347,"timestamp":1709146873.881,"receipt_timestamp":1709146874.0210495}
```

