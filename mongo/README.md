# MongoDB Docker Setup and Python Integration

This project provides a containerized MongoDB environment using Docker, it includes Python scripts for data insertion and querying the data and a KNIME workflow to train a Binary Classification model to predict diabetes from patient data.

## Project Structure

* [__docker-compose.yml__](docker-compose.yml) - Configuration for the MongoDB container.
* [__data-insert.py__](data-insert.py) - Script to populate the database.
* [__query-db.py__](query-db.py) - Script to retrieve data.
* [__diabetes.csv__](diabetes.csv) - Diagnostic measurements of patients from __Kaggle__
* [__knime-workflows/diabetes_predictor.knwf__](knime-workflows/diabetes_predictor.knwf) - KNIME workflow to train a Binary Classification model to predict diabetes from patient data.

---

## Setup Instructions

### 1. Prerequisites

Ensure you have the following installed:

* **Docker** - [Download Docker Desktop](https://www.docker.com/products/docker-desktop)
* **Python 3.x** - With the following libraries:
  * PyMongo: `pip install pymongo`
  * Pandas: `pip install pandas`
* **KNIME Analytics Platform** - With the following extensions:
  * KNIME Deep Learning - Tensorflow Integration
  * KNIME MongoDB Integration
  * KNIME Python Integration

---

### 2. Launch MongoDB in Docker

#### 2.1 Start the Container

If running for the **first time**, pull and start the MongoDB container:
```bash
docker run -d --name mongodb_container -p 27017:27017 mongo:latest
```

If the container **already exists**, simply start it:
```bash
docker start mongodb_container
```

#### 2.2 Setup using Docker Compose (Alternative)

If you have the `docker-compose.yml` file, run:
```bash
docker compose up -d
```

#### 2.3 Verify the Container is Running
```bash
docker ps
```

You should see `mongodb_container` with status **Up** and port `0.0.0.0:27017->27017/tcp` ✅

#### 2.4 Verify MongoDB Health
```bash
docker exec -it mongodb_container mongosh
```

Inside mongosh shell run:
```js
db.runCommand({ ping: 1 })
```

Expected response:
```json
{ ok: 1 }
```

Type `exit` to leave the shell.

---

### 3. Configuration

Update the `path` variable in [`data-insert.py`](data-insert.py) to point to `diabetes.csv` in your local filesystem:
```python
path = "C:/path/to/diabetes.csv"
```

---

### 4. Data Operations

Navigate to the project folder first:
```bash
cd path/to/mongo
```

#### 4.1 Insert Data

Make sure the `path` variable in [`data-insert.py`](data-insert.py) points to `diabetes.csv` in your local filesystem.

Run the insert script to populate MongoDB with records from `diabetes.csv`:
```bash
python data-insert.py
```

Expected output:
```
Inserting 768 records...
Success! Data indexed in 'health_data.diabetes' collection.
Sample record from DB: {'_id': ObjectId('...'), 'Pregnancies': 6, 'Glucose': 148, ...}
```

#### 4.2 Query Data

Run the [`query-db.py`](query-db.py) script to retrieve and display the stored data:
```bash
python query-db.py
```

Expected output:
```
--- Fetching the first 5 records ---
Record 1: {'Pregnancies': 6, 'Glucose': 148, 'BloodPressure': 72, ...}
Record 2: {'Pregnancies': 1, 'Glucose': 85, 'BloodPressure': 66, ...}
...
```

---

### 5. Data Fields

The `diabetes.csv` dataset contains the following diagnostic measurements:

| Field | Description |
|---|---|
| `Pregnancies` | Number of times pregnant |
| `Glucose` | Plasma glucose concentration |
| `BloodPressure` | Diastolic blood pressure (mm Hg) |
| `SkinThickness` | Triceps skin fold thickness (mm) |
| `Insulin` | 2-Hour serum insulin (mu U/ml) |
| `BMI` | Body mass index |
| `DiabetesPedigreeFunction` | Diabetes pedigree function |
| `Age` | Age in years |
| `Outcome` | Class variable (0 or 1) |

---

### 6. Running the Workflow in KNIME

The workflow sample uses Keras extensions to implement an LSTM model, which requires certain Python dependencies to be installed using conda environments. In order to setup KNIME for the Deep learning integrations, follow the instructions in [KNIME Documentation: Set Up Deep Learning](https://docs.knime.com/ap/latest/deep_learning_installation_guide/).

#### 6.1 Import the Workflow

1. Open **KNIME Analytics Platform**
2. In **Local Space** on the left panel
3. Click **Import Workflow**
4. Choose [`knime-workflows/diabetes_predictor.knwf`](knime-workflows/diabetes_predictor.knwf)

#### 6.2 Configure MongoDB Connector

1. **Right click** on `MongoDB Connector` node → Click **Configure**
2. Fill in the connection details:
   - **Hostname:** `localhost`
   - **Port:** `27017`
   - **Authentication:** `None`
3. Click **Apply** → **OK**
4. **Right click** → **Execute** — green indicates success ✅

#### 6.3 Configure MongoDB Reader

1. **Right click** on `MongoDB Reader` node → Click **Configure**
2. Fill in:
   - **Database:** `health_data`
   - **Collection:** `diabetes`
3. Click **OK** → **Execute**

#### 6.4 Configure TensorFlow Network Writer

1. **Right click** on `TensorFlow Network Writer` node → Click **Configure**
2. Click **Browse** and provide the path to save the model
3. Click **OK**

#### 6.5 Execute the Workflow

1. From **Menu bar** → Click **Execute All**
2. This will execute all nodes sequentially and save the model as a zip file ✅

---

### 7. Stopping the Services

To stop the MongoDB container when done:
```bash
docker stop mongodb_container
```

To stop and remove using Docker Compose:
```bash
docker compose down
```

To stop and completely remove the container:
```bash
docker rm -f mongodb_container
```

---

## Troubleshooting

### Container Name Conflict
If you see a container name conflict error, remove the old container first:
```bash
docker rm -f mongodb_container
docker run -d --name mongodb_container -p 27017:27017 mongo:latest
```

### CSV File Not Found
Make sure the path to `diabetes.csv` in [`data-insert.py`](data-insert.py) is correct:
```python
path = "C:/Users/hp/Downloads/diabetes.csv"
```

### KNIME MongoDB Connection Failed
If the MongoDB Connector node turns red:
* Make sure the MongoDB container is running: `docker ps`
* Make sure **Authentication** is set to `None`
* Verify **Hostname** is `localhost` and **Port** is `27017`