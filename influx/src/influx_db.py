from influxdb_client import InfluxDBClient

def query_data(measurement, bucket, url, token, org, limit=10, time_range="-1h"):
    client = InfluxDBClient(url=url, token=token, org=org)
    query = f'from(bucket: "{bucket}") |> range(start: {time_range}) |> filter(fn: (r) => r._measurement == "{measurement}") |> limit(n: {limit})'
    tables = client.query_api().query(query, org=org)
    for table in tables:
        for record in table.records:
            print(record)
    client.close()