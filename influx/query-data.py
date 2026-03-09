from src.influx_db import query_data
from src.constants import INFLUX_BUCKET, INFLUX_MEASUREMENT
from src.helpers import load_config

################################################################################
# This script queries data from InfluxDB and prints the results to the console #
################################################################################


config = load_config()
url = f"http://localhost:{config['influxdb']['port']}"
token = config['influxdb']['token']
bucket = config['influxdb']['bucket']
org = config['influxdb']['org']
measurement= config['influxdb']['measurement']
time_range = "-1h"   

print(f"Configuration: url={url}, bucket={bucket}, org={org}, measurement={measurement}, time_range={time_range}")
if __name__ == '__main__':
    print(f"Querying InfluxDB at {url}...")
    query_data(measurement=measurement, bucket=bucket, url=url, token=token, org=org, limit=1, time_range=time_range)