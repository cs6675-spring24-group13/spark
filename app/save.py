import requests

# File to upload
local_file_path = '/opt/bitnami/spark/kmeans_clusters.png'
hdfs_file_path = '/kmeans_clusters.png'

# WebHDFS URL
webhdfs_url = f'http://namenode:9870/webhdfs/v1{hdfs_file_path}?op=CREATE&overwrite=true'

# Read the local file content
with open(local_file_path, 'rb') as file:
    file_content = file.read()

# Upload the file to HDFS
response = requests.put(webhdfs_url, data=file_content)

if response.status_code == 201:
    print(f'Successfully uploaded {local_file_path} to HDFS at {hdfs_file_path}')
else:
    print(f'Failed to upload file: {response.text}')
