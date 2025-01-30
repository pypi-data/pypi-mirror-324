# source-faker
Generates fake source data for testing data ingestion pipeline


The output folder can be set to remote cloud storages as well, given that the necessary credentials are setup. 
Pandas takes care of the file writing, follow [their docs](https://pandas.pydata.org/docs/user_guide/io.html#reading-writing-remote-files) on how to authenticate and setup the `data_output` parameter to the remote path (e.g. s3://...) 