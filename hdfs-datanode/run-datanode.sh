#!/bin/bash

# Start the DataNode daemon
$HADOOP_HOME/sbin/hadoop-daemon.sh start datanode

# Keep the container running
tail -f $HADOOP_HOME/logs/*
