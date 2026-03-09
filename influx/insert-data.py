import pandas as pd
import datetime
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS





def explode(df):
     for col in df.columns:
             if isinstance(df.iloc[0][col], list):
                     df = df.explode(col)
             d = df[col].apply(pd.Series)
             df[d.columns] = d
             df = df.drop(col, axis=1)
     return df


def jsonToTable(df):
     df.index = range(len(df))
     cols = [col for col in df.columns if isinstance(df.iloc[0][col], (dict, list))]
     if len(cols) == 0:
             return df
     for col in cols:
             d = explode(pd.DataFrame(df[col], columns=[col]))
             d = d.dropna(axis=1, how='all')
             df = pd.concat([df, d], axis=1)
             df = df.drop(col, axis=1).dropna()
     return jsonToTable(df)


def time(df):
     df.index = pd.date_range(start=datetime.datetime.now(), freq='10ms', periods=len(df))
     df['measTimeStampRf'] = df['measTimeStampRf'].astype(str)
     return df


def insert_data(df: pd.DataFrame, url="localhost:8086", token="", org= "", measurement: str = 'liveCell', bucket_name: str = ""):
    # Connect to InfluxDB
    client = InfluxDBClient(url=url, token=token, org=org)

    # Create bucket if it doesn't exist
    buckets_api = client.buckets_api()
    existing_buckets = buckets_api.find_buckets().buckets
    if not any(bucket.name == bucket_name for bucket in existing_buckets):
        print(f"Bucket '{bucket_name}' not found. Creating...")
        buckets_api.create_bucket(bucket_name=bucket_name, org=org)
    else:
        print(f"Bucket '{bucket_name}' already exists.")



    # Force recent timestamps (so queries like -1h will work)
    now = datetime.datetime.now(datetime.timezone.utc)
    df.index = pd.date_range(start=now, periods=len(df), freq='10s')
    df['measTimeStampRf'] = df['measTimeStampRf'].astype(str)

    print(f"Writing {len(df)} rows to bucket '{bucket_name}'...\n data sample:")
    print(df.iloc[1])
    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(
        bucket=bucket_name,
        org="my-org",
        record=df,
        data_frame_measurement_name=measurement
    )
    print("data inserted ")

def query_data(
    measurement: str,
    bucket: str,
    url: str = "localhost:8086",
    token: str = "",
    org: str = "",
    limit: int = 1000,
    time_range: str = "-30d"
):
    """
    Query a specific measurement in a specific bucket and print results.
    """
    client = InfluxDBClient(url=url, token=token, org=org)
    flux_query = f'''
    from(bucket: "{bucket}")
      |> range(start: {time_range})
      |> filter(fn: (r) => r._measurement == "{measurement}")
      |> limit(n: {limit})
    '''
    tables = client.query_api().query(flux_query, org=org)
    for table in tables:
        print(f"Table: {table}")
        print(f"count of records: {len(table.records)}")
        for record in table.records:
            print(f"{record.get_time()} | {record.get_measurement()} | {record.get_field()}={record.get_value()}")
    client.close()

def check_bucket(url:str = "", token: str = "", org: str = ""):
    client = InfluxDBClient(url=url, token=token, org=org)

    print("Buckets in org:")
    for b in client.buckets_api().find_buckets().buckets:
        print(f"- {b.name}")

    client.close()


###########################################################################
# This script reads a CSV file and inserts its content into the  InfluxDB #
###########################################################################

url = f"http://localhost:8086"
token = "93ukPnhw6Yrr38ZTd4Ihdj8BgSIVQhb9Xu5bVk3qf7teMdj66gQxuypZB81GhqKaxNn_a02l93437KAYJ6zkAw=="
bucket = "UEdata1"
org = "my-org"
measurement= "UEThroughput"
time_range = "-1h"   

# sample DataFrame
df = pd.read_csv("/home/testbed/testbed/pipelien-generator/influx/cells.csv")
# Insert the DataFrame into InfluxDB
# insert_data(df,url=url, measurement=measurement, bucket_name=bucket, token=token, org=org)
# query data
query_data(measurement=measurement, bucket=bucket, url=url, token=token, org=org, limit=1, time_range=time_range)