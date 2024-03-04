FROM hadoop:base

# Namenode specific environment variables
ENV HDFS_CONF_dfs_namenode_name_dir=file:///hadoop/dfs/name
RUN mkdir -p /hadoop/dfs/name

COPY core-site.xml $HADOOP_HOME/etc/hadoop/core-site.xml
COPY hdfs-site.xml $HADOOP_HOME/etc/hadoop/hdfs-site.xml

# VOLUME /hadoop/dfs/name

COPY run-namenode.sh /run-namenode.sh
RUN chmod a+x /run-namenode.sh

CMD ["/run-namenode.sh"]
