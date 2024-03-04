#!/bin/bash

# Format the NameNode if it's the first time the container is run
if [ ! -d "$HDFS_CONF_dfs_namenode_name_dir/current" ]; then
  echo "Y" | $HADOOP_HOME/bin/hdfs namenode -format
fi

# Start the NameNode daemon
$HADOOP_HOME/sbin/hadoop-daemon.sh start namenode

# hdfs dfs -put /data/data.csv /data.csv

# Keep the container running
tail -f $HADOOP_HOME/logs/*
