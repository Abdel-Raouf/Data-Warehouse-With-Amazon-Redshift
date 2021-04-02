# Purpose:

Putting into practice the following concepts:

- Data modeling (Applying Conceptual Modeling, then Construct Fact and Dimension Tables).
- Database Schema (Apply a specific schema to Fact and Dimension Tables, which suits our Data-Size and Structure => Star-Schema).
- ETL Pipeline (Construct an ETL Pipeline to Extract Data From Log Files on S3 Bucket, load Data to the Staging tables in Amazon Redshift which acts as a Data-Warehouse, then, apply various transformation needed on the Data, before inserting Data into Fact and Dimensional Tables).
- Dealing With a Data Warehouse (By Collecting Data from Multiple Sources `OLTP DBs`, then Transfering Data to `OLAP`, using an ETL process), putting in mind Various Data Warehouse Architectures (Kimball's `Bus Arch`, Inmon `CIF`, Data Marts).
- Provisioning an infrastructure on the cloud (Amazon Redshift).
- Dealing with Infrastructure as code (Iac) using either AWS python SDK (Boto3) or Terraform.
- Applying Table Design Optimization on Amazon Redshift (By using Various Distribution Styles and Sorting key, on the Partitioned tables), Which help in speeding up Queries.

# Project Description:

A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

As a data engineer, I'll build an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights in what songs their users are listening to.

# Data Sample:

- **Song Dataset**: Stored on S3 Bucket -> `'s3://udacity-dend/song_data'`

```
{"num_songs": 1, "artist_id": "ARD7TVE1187B99BFB1", "artist_latitude": null, "artist_longitude": null, "artist_location": "California - LA", "artist_name": "Casual", "song_id": "SOMZWCG12A8C13C480", "title": "I Didn't Mean To", "duration": 218.93179, "year": 0}
```

- **Log Dataset**: Stored on S3 Bucket -> `'s3://udacity-dend/log_data'`

```
{"artist":null,"auth":"Logged In","firstName":"Kaylee","gender":"F","itemInSession":0,"lastName":"Summers","length":null,"level":"free","location":"Phoenix-Mesa-Scottsdale, AZ","method":"GET","page":"Home","registration":1540344794796.0,"sessionId":139,"song":null,"status":200,"ts":1541106106796,"userAgent":"\"Mozilla\/5.0 (Windows NT 6.1; WOW64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/35.0.1916.153 Safari\/537.36\"","userId":"8"}
```

- **Log JsonPath File**: Contains Paths to Navigate the log data folders for the Json Log Files.

# Database Schema:

The schema used is the Star Schema: There is one main fact table containing all the measures associated with each event songplays, and 4-dimensional tables songs, artists, users and time, each with a primary key that is being referenced from the fact table.

Two Staging Tables, to load data from them into the Fact and Dimensional Tables.
![App_Look](https://github.com/Abdel-Raouf/Data-Warehouse-With-Amazon-Redshift/blob/main/images/Star-Schema.png)

# Data Model Selection:

We used a Data Warehouse based on the Columnar Data-Model (Amazon Redshift), Due to:

- Columnar Storage Architecture is very Efficient in Analytics, Due to Data related to the Same Column is Contiguously Stored on the Same Page (As a result, we fetch Data on Demand).
- Internally, Amazon Redshift is Based on Postgresql Engine (Which is Efficient proven), with Modified Extensions for Custom Columnar Storage.
- Amazon Redshift is a `MPP` DB, as it Parallelize the Execution of the Same Query on Multiple Cores (Slices), Due to there is different parts of the same table exists on Multiple Cores (Slices).
- Amazon Redshift is Cloud-Managed, so we can Scale Up or Down Easily on Demand.

# Project Structure

- `create_tables.py` -> This script will drop old tables (if exist) ad re-create new tables.
- `etl.py` -> This script executes the queries that extract JSON data from the S3 bucket and ingest them to Redshift.
- `sql_queries.py` -> This file contains variables with SQL statement in String formats, partitioned by CREATE, DROP, COPY and INSERT statement.
- `dhw.cfg` -> Configuration file contains info about `Redshift access info`, `IAM Role` and `S3` which contains links to Json Files.

# How to Run:

1. Run **create_tables.py** from terminal to set up the database and tables on Amazon Redshift DB.
2. Run **etl.py** from terminal to process and load data into Redshift.
