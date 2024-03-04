FROM hadoop:base

# Datanode specific environment variables
ENV HDFS_CONF_dfs_datanode_data_dir=file:///hadoop/dfs/data
RUN mkdir -p /hadoop/dfs/data

COPY core-site.xml $HADOOP_HOME/etc/hadoop/core-site.xml
COPY hdfs-site.xml $HADOOP_HOME/etc/hadoop/hdfs-site.xml
    
# VOLUME /hadoop/dfs/data

COPY run-datanode.sh /run-datanode.sh
RUN chmod a+x /run-datanode.sh

CMD ["/run-datanode.sh"]
