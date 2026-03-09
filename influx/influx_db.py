import pandas as pd
import datetime
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from .constants import INFLUXDB_HOST, INFLUX_TOKEN, INFLUX_ORG, INFLUX_BUCKET




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


def insert_data(df: pd.DataFrame, url="localhost:8086", token=INFLUX_TOKEN, org= INFLUX_ORG, measurement: str = 'liveCell', bucket_name: str = INFLUX_BUCKET):
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
        org=INFLUX_ORG,
        record=df,
        data_frame_measurement_name=measurement
    )
    print("data inserted ")

def query_data(
    measurement: str,
    bucket: str,
    url: str = "localhost:8086",
    token: str = INFLUX_TOKEN,
    org: str = INFLUX_ORG,
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

def check_bucket(url:str = INFLUXDB_HOST, token: str = INFLUX_TOKEN, org: str = INFLUX_ORG):
    client = InfluxDBClient(url=url, token=token, org=org)

    print("Buckets in org:")
    for b in client.buckets_api().find_buckets().buckets:
        print(f"- {b.name}")

    client.close()
