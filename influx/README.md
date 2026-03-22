# InfluxDB Docker Setup and Python Integration

This project provides a containerized InfluxDB environment using Docker, it includes Python scripts for data insertion and querying the time-series data and a KNIME workflow to train an LSTM model to predict throughput of a cell tower.

## Project Structure

* [__knime-influxdb2-integration-extension.zip__](https://drive.google.com/file/d/1JzU-6886-arwCi21VX587YRCRmF5J0xf/view?usp=sharing) - Knime extension to connect and read data from InfluxDB 2
* [__knime-workflows/cells.knwf__](knime-workflows/cells.knwf) - Example workflow to train, evaluate and save an LSTM model in KNIME
* [__src/constants.py__](src/constants.py) - InfluxDB connection constants (token, org, bucket).
* [__cells.csv__](cells.csv) - Time-series UE throughput measurements dataset.
* [__docker-compose.yaml__](docker-compose.yaml) - Configuration for the InfluxDB container.
* [__insert-data.py__](insert-data.py) - Script to insert CSV data into InfluxDB.
* [__query-data.py__](query-data.py) - Script to retrieve and display data from InfluxDB.
* [__influx_db.py__](influx_db.py) - Helper functions for InfluxDB operations.


---

## Setup Instructions

### 1. Prerequisites

Ensure you have the following installed:

* **Docker** - [Download Docker Desktop](https://www.docker.com/products/docker-desktop)
* **Python 3.x** - With the following libraries:
  * InfluxDB client: `pip install influxdb-client`
  * Pandas: `pip install pandas`
* **KNIME Analytics Platform** - With the following extensions:
  * KNIME Deep Learning - Tensorflow Integration
  * KNIME Python Integration
  * KNIME InfluxDB 2 Integration ([__knime-influxdb2-integration-extension.zip__](https://drive.google.com/file/d/1JzU-6886-arwCi21VX587YRCRmF5J0xf/view?usp=sharing)) *(see [installation steps](#61-install-the-extension-knime-influxdb-2-integration) for the custom extension)*
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

Copy the token value and update it in [`src/constants.py`](src/constants.py).

---

### 3. Configuration

Update the [`src/constants.py`](src/constants.py) file with your InfluxDB credentials:
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

Make sure the following in [`insert-data.py`](insert-data.py) are correct:
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

Run the [`query-data.py`](query-data.py) script to retrieve and display the stored data:
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

The [`cells.csv`](cells.csv) dataset contains the following UE throughput measurements:

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

### 6. Running the Workflow in KNIME

The workflow sample uses Keras extensions to implement an LSTM model, which requires certain Python dependencies to be installed using conda environments. In order to setup KNIME for the Deep learning integrations, follow the instructions in [KNIME Documentation: Set Up Deep Learning](https://docs.knime.com/ap/latest/deep_learning_installation_guide/).

#### 6.1 Install the extension: KNIME InfluxDB 2 Integration

Download and extract [__knime-influxdb2-integration-extension.zip__](https://drive.google.com/file/d/1JzU-6886-arwCi21VX587YRCRmF5J0xf/view?usp=sharing) to the local file system.

1. Open **KNIME Analytics Platform**
2. In **Local Space** on the left panel
3. Go to the **Menu bar**
4. Click on **Preferences**
5. In the Preferences window:
    1.  Expand **Install/Update**
    2.  Click on **Available Software Sites**
    3.  Click on **Add** in **Available Software Sites** view
    4.  Click on **Local** in the pop-up window
    5.  Select the extracted folder
    6.  Provide a name (e.g., `InfluxDB2 Integration`)
    7.  Click **Add**
6. You have setup the software site, to install the extension:
    1.  Go to the **Menu bar**
    2.  Click on **Install Extensions**
    3.  In the search/filter box, type **Influx**
    4.  Select **KNIME InfluxDB2 Integration**
    5.  Click **Next**, then **Finish**
7. Restart KNIME

After restarting, verify the installtion by opening a workflow and search for **InfluxDB Reader** in the node repository.

#### 6.2 Import the Workflow

1. Open **KNIME Analytics Platform**
2. In **Local Space** on the left panel
3. Click **Import Workflow**
4. Choose [`knime-workflows/cells.knwf`](knime-workflows/cells.knwf)

#### 6.3 Configure InfluxDB reader

1. Select **InfluxDB Reader** node
2. In the properties window to the right, fill in the values:
    - Database URL: http://localhost:8086
    - Access Token: <your-access-token>
    - Organization: my-org
    - Query: 
    ```bash
    from(bucket: "UEdata1")  |> range(start: -30d)  |> filter(fn: (r) => r["_measurement"] == "UEThroughput")  |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    ```
3. Apply and Execute

#### 6.4 Configure TensorFlow Network Writer

1. **Right click** on `TensorFlow Network Writer` node → Click **Configure**
2. Click **Browse** and provide the path to save the model
3. Click **OK**

#### 6.5 Execute the Workflow
The configuration of the rest of the nodes should be saved. You can now execute the workflow:

1. From **Menu bar** → Click **Execute All**
2. This will execute all nodes sequentially and save the model as a zip file ✅

### 7. Stopping the Services

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

Then update the token in both [`insert-data.py`](insert-data.py) and [`src/constants.py`](src/constants.py).

### Container Name Conflict
If you see a container name conflict error, remove the old container first:
```bash
docker rm -f influxdb
docker run -d --name influxdb -p 8086:8086 influxdb:2.7
```

### CSV File Not Found
Make sure the path to `cells.csv` in [`insert-data.py`](insert-data.py) is correct. Use just the filename if running from the same folder:
```python
df = pd.read_csv("cells.csv")
```