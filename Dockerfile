# Use a base image with Java pre-installed, as Hadoop requires Java
FROM openjdk:8-jdk

# Set environment variables for Hadoop
ENV HADOOP_VERSION 3.3.6
ENV HADOOP_HOME /opt/hadoop

# Download and extract Hadoop
RUN wget -qO- http://apache.mirrors.pair.com/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz | tar zxv -C /opt
RUN mv /opt/hadoop-$HADOOP_VERSION $HADOOP_HOME

# Add Hadoop bin/ and sbin/ to path
ENV PATH $PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Working directory in Hadoop home
WORKDIR $HADOOP_HOME
