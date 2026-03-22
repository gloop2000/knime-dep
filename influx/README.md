# InfluxDB Docker Setup and Python Integration

This project provides a containerized InfluxDB environment using Docker, it includes Python scripts for data insertion and querying the time-series data.

## Project Structure

* __docker-compose.yaml__ - Configuration for the InfluxDB container.
* __insert-data.py__ - Script to insert CSV data into InfluxDB.
* __query-data.py__ - Script to retrieve and display data from InfluxDB.
* __influx_db.py__ - Helper functions for InfluxDB operations.
* __cells.csv__ - Time-series UE throughput measurements dataset.
* __src/constants.py__ - InfluxDB connection constants (token, org, bucket).
* __src/helpers.py__ - Helper function to load configuration.
* __src/influx_db.py__ - Query function used by query-data.py.

---

## Setup Instructions

### 1. Prerequisites

Ensure you have the following installed:

* **Docker** - [Download Docker Desktop](https://www.docker.com/products/docker-desktop)
* **Python 3.x** - With the following libraries:
  * InfluxDB client: `pip install influxdb-client`
  * Pandas: `pip install pandas`

---

### 2. Launch InfluxDB in Docker

#### 2.1 Start the Container

If running for the **first time**, pull and start the InfluxDB container:
```bash
docker run -d --name influxdb -p 8086:8086 influxdb:2.7
```

If the container **already exists**, simply start it:
```bash
docker start influxdb
```

#### 2.2 Setup InfluxDB (First Time Only)

Run the following command to initialize InfluxDB with credentials, organization and bucket:
```bash
docker exec -it influxdb influx setup \
  --username my-admin \
  --password my-password123 \
  --org my-org \
  --bucket UEdata1 \
  --force
```

#### 2.3 Verify the Container is Running
```bash
docker ps
```

You should see `influxdb` with status **Up** and port `0.0.0.0:8086->8086/tcp` ✅

#### 2.4 Verify InfluxDB Health
```bash
curl -i -X GET http://localhost:8086/health
```

Expected response:
```json
{"status":"pass", "message":"ready for queries and writes"}
```

#### 2.5 Get Authentication Token
```bash
docker exec -it influxdb influx auth list
```

Copy the token value and update it in `src/constants.py`.

---

### 3. Configuration

Update the `src/constants.py` file with your InfluxDB credentials:
```python
INFLUX_BUCKET="UEdata1"
INFLUX_MEASUREMENT="UEThroughput"
INFLUXDB_HOST="http://localhost:8086"
INFLUX_TOKEN="your-token-here"
INFLUX_ORG="my-org"
```

---

### 4. Data Operations

Navigate to the project folder first:
```bash
cd path/to/influx
```

#### 4.1 Insert Data

Make sure the following in `insert-data.py` are correct:
* The csv path points to `cells.csv` in your local filesystem
* The `token` matches the one from `docker exec -it influxdb influx auth list`
* The `insert_data()` function call is **NOT** commented out

Run the insert script to populate InfluxDB with 5000 rows from `cells.csv`:
```bash
python insert-data.py
```

Expected output:
```
Bucket 'UEdata1' already exists.
Writing 5000 rows to bucket 'UEdata1'...
data inserted
```

#### 4.2 Query Data

Run the query script to retrieve and display the stored data:
```bash
python query-data.py
```

Expected output:
```
Configuration: url=http://localhost:8086, bucket=UEdata1, org=my-org, measurement=UEThroughput
Querying InfluxDB at http://localhost:8086...
FluxRecord() table: 0, {..., '_field': 'availPrbDl', '_measurement': 'UEThroughput'}
FluxRecord() table: 1, {..., '_field': 'availPrbUl', '_measurement': 'UEThroughput'}
...
```

---

### 5. Data Fields

The `cells.csv` dataset contains the following UE throughput measurements:

| Field | Description |
|---|---|
| `du-id` | Distributed Unit identifier |
| `measTimeStampRf` | Measurement timestamp |
| `nrCellIdentity` | NR Cell identity |
| `throughput` | UE throughput value |
| `availPrbDl` | Available PRB downlink |
| `availPrbUl` | Available PRB uplink |
| `pdcpBytesDl` | PDCP bytes downlink |
| `pdcpBytesUl` | PDCP bytes uplink |
| `measPeriodPrb` | Measurement period PRB |
| `measPeriodPdcpBytes` | Measurement period PDCP bytes |
| `x` | X coordinate |
| `y` | Y coordinate |

---

### 6. Stopping the Services

To stop the InfluxDB container when done:
```bash
docker stop influxdb
```

To stop and completely remove the container:
```bash
docker rm -f influxdb
```

---

## Troubleshooting

### 401 Unauthorized Error
If you see a `401 Unauthorized` error, your token has expired or changed. Get a new token:
```bash
docker exec -it influxdb influx auth list
```

Then update the token in both `insert-data.py` and `src/constants.py`.

### Container Name Conflict
If you see a container name conflict error, remove the old container first:
```bash
docker rm -f influxdb
docker run -d --name influxdb -p 8086:8086 influxdb:2.7
```

### CSV File Not Found
Make sure the path to `cells.csv` in `insert-data.py` is correct. Use just the filename if running from the same folder:
```python
df = pd.read_csv("cells.csv")
```
