from influx_db import query_data
from src.constants import INFLUX_BUCKET, INFLUX_MEASUREMENT, INFLUXDB_HOST, INFLUX_TOKEN, INFLUX_ORG

################################################################################
# This script queries data from InfluxDB and prints the results to the console #
################################################################################

url = INFLUXDB_HOST
token = INFLUX_TOKEN
bucket = INFLUX_BUCKET
org = INFLUX_ORG
measurement= INFLUX_MEASUREMENT
time_range = "-1h"   

print(f"Configuration: url={url}, bucket={bucket}, org={org}, measurement={measurement}, time_range={time_range}")
if __name__ == '__main__':
    print(f"Querying InfluxDB at {url}...")
    query_data(measurement=measurement, bucket=bucket, url=url, token=token, org=org, limit=1, time_range=time_range)