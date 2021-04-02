import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS song"
artist_table_drop = "DROP TABLE IF EXISTS artist"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES
staging_events_table_create = ("""
        CREATE TABLE IF NOT EXISTS staging_events(events_id INT IDENTITY(0,1) PRIMARY KEY, artist VARCHAR, auth VARCHAR, firstName VARCHAR, \
            gender VARCHAR, itemInSession INT, lastName VARCHAR, length FLOAT, level VARCHAR, location VARCHAR, \
                method VARCHAR, page VARCHAR, registration FLOAT, sessionId INT, song VARCHAR, status INT, ts TIMESTAMP, userAgent VARCHAR, userId INT)
""")

staging_songs_table_create = ("""
        CREATE TABLE IF NOT EXISTS staging_songs(song_id VARCHAR PRIMARY KEY, num_songs INT, artist_id VARCHAR, artist_latitude FLOAT, artist_longitude FLOAT, artist_location VARCHAR, \
            artist_name VARCHAR, title VARCHAR, duration FLOAT, year INT)
""")

songplay_table_create = ("""
        CREATE TABLE IF NOT EXISTS fact_songplays(songplay INT IDENTITY(0,1) PRIMARY KEY, start_time TIMESTAMP NOT NULL SORTKEY, user_id INT NOT NULL DISTKEY, level VARCHAR, song_id VARCHAR NOT NULL, \
                    artist_id VARCHAR NOT NULL, session_id INT, location VARCHAR, user_agent VARCHAR)
""")

user_table_create = ("""
        CREATE TABLE IF NOT EXISTS dim_users(user_id INT PRIMARY KEY SORTKEY DISTKEY, first_name VARCHAR NOT NULL, last_name VARCHAR NOT NULL, \
                    gender VARCHAR, level VARCHAR)
""")

song_table_create = ("""
        CREATE TABLE IF NOT EXISTS dim_songs(song_id VARCHAR PRIMARY KEY SORTKEY, title VARCHAR NOT NULL, artist_id VARCHAR NOT NULL, \
                    year INT, duration FLOAT NOT NULL) DISTSTYLE ALL;
""")

artist_table_create = ("""
        CREATE TABLE IF NOT EXISTS dim_artists(artist_id VARCHAR PRIMARY KEY SORTKEY, name VARCHAR NOT NULL, location VARCHAR, \
                        longitude FLOAT, latitude FLOAT) DISTSTYLE ALL;
""")

time_table_create = ("""
        CREATE TABLE IF NOT EXISTS dim_time(start_time TIMESTAMP PRIMARY KEY SORTKEY, hour INT, day INT, week_of_year INT, month INT, \
                    year INT, week_day INT) DISTSTYLE ALL;
""")

# STAGING TABLES
staging_events_copy = ("""
        COPY staging_events FROM {}
        CREDENTIALS 'aws_iam_role={}'
        TIMEFORMAT AS 'epochmillisecs'
        REGION 'us-west-2'
        FORMAT AS JSON {};
""").format(config.get('S3', 'LOG_DATA'), config.get('IAM_ROLE', 'ARN'), config.get('S3', 'LOG_JSONPATH'))

staging_songs_copy = ("""
        COPY staging_songs FROM {}
        CREDENTIALS 'aws_iam_role={}'
        REGION 'us-west-2'
        FORMAT AS JSON 'auto';
""").format(config.get('S3', 'SONG_DATA'), config.get('IAM_ROLE', 'ARN'))

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO fact_songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) 
    SELECT DISTINCT se.ts AS start_time,
        se.userId AS user_id,
        se.level As level,
        ss.song_id AS song_id,
        ss.artist_id AS artist_id,
        se.sessionId AS session_id,
        se.location AS location,
        se.userAgent AS user_agent
    FROM staging_events AS se
    JOIN staging_songs AS ss
    ON se.song = ss.title AND se.artist = ss.artist_name
    WHERE page = 'NextSong';
""")

user_table_insert = ("""
    INSERT INTO dim_users (user_id, first_name, last_name, gender, level) \
    SELECT DISTINCT userId AS user_id,
        firstName AS first_name,
        lastName AS last_name,
        gender AS gender,
        level AS level
    FROM staging_events AS se
    WHERE userId IS NOT NULL AND page = 'NextSong';     
""")

song_table_insert = ("""
    INSERT INTO dim_songs (song_id, title, artist_id, year, duration) \
    SELECT DISTINCT song_id,
        title,
        artist_id,
        year,
        duration
    FROM staging_songs AS ss
    WHERE song_id IS NOT NULL;
""")

artist_table_insert = ("""
    INSERT INTO dim_artists (artist_id, name, location, longitude, latitude) \
    SELECT DISTINCT artist_id AS artist_id,
        artist_name AS name,
        artist_location AS location,
        artist_longitude AS longitude,
        artist_longitude AS latitude
    FROM staging_songs AS ss
    WHERE artist_id IS NOT NULL;
""")

time_table_insert = ("""
    INSERT INTO dim_time (start_time, hour, day, week_of_year, month, year, week_day) \
    SELECT DISTINCT ts AS start_time,
        EXTRACT(hour FROM ts),
        EXTRACT(day FROM ts),
        EXTRACT(week FROM ts),
        EXTRACT(month FROM ts),
        EXTRACT(year FROM ts),
        EXTRACT(dayofweek FROM ts)
    FROM staging_events AS se
    WHERE start_time IS NOT NULL AND page = 'NextSong';
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create,
                        songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop,
                      songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert,
                        song_table_insert, artist_table_insert, time_table_insert]
