# MongoDB Docker Setup and Python Integration

This project provides a containerized MongoDB environment using Docker Compose, it includes Python scripts for data insertion and querying the data and a KNIME workflow file to load, train a Binary Classification model and predict data in KNIME.

---

## Project Structure

- [docker-compose.yml](./docker-compose.yaml) - Configuration for the MongoDB container.
- [data-insert.py](./data-insert.py) - Script to populate the database.
- [query-db.py](./query-db.py) - Script to retrieve data.
- [diabetes.csv](./diabetes.csv) - Diagnostic measurements of patients from [Kaggle](https://www.kaggle.com/datasets/mathchi/diabetes-data-set)
- [knime-workflows/diabetes_predictor.knwf](./knime-workflows/diabetes_predictor.knwf) - KNIME workflow to train a Binary Classification model to predict diabetes from a patient data.

## Setup Instructions

### 1. Prerequisites

Ensure you have the following installed:

- **Docker** and **Docker Compose**
- **Python 3.x**: With libraries
  - **PyMongo library**: `pip install pymongo`
  - **Pandas**: `pip install pandas`
- **KNIME Analytics Platform**: With extensions
  - KNIME Deep Learning - Tensorflow Integration
  - KNIME MongoDB Integration
  - KNIME Python Integration

### 2. Configuration

The `.env` file in the root directory to stores your database credentials. This file is automatically read by the `docker-compose.yml` file.

```env
MONGO_USERNAME=admin
MONGO_PASSWORD=your_password_here
```

### 3. Launch the Database

To start the MongoDB container in the background (detached mode), run:

`docker-compose up -d`

To verify the container is running, use:

`docker ps`

### 4. Data Operations

Once the database is active, use the provided Python scripts to interact with it.

#### 4.1. Insert Data

Point the `path` variable in [data-insert.py](./data-insert.py) to [diabetes.csv](./diabetes.csv) in you local file system.

Run the [data-insert.py](./data-insert.py) script to populate the database

`python data-insert.py`

#### 4.2. Query Data

Run the [query-db.py](./query-db.py) script to retrieve and view the stored information:

`python query-db.py`

### 5. Running the workflow in KNIME

The workflow sample uses Keras extensions to implement a model, which requires certain Python dependencies to be installed using conda environments. In order to setup KNIME for the Deep learning integrations, follow the instructions in [KNIME Documentation: Set Up Deep Learning](https://docs.knime.com/ap/latest/deep_learning_installation_guide/).

#### 5.1 Import the workflow

A workflow to load data from MongoDB database with datapreprocessing, training and evaluation steps have been exproted to [diabetes_predictor.knwf](./knime-workflows/diabetes_predictor.knwf)

To Import the workflow:

1.  Open KNIME Analytics Platform
2.  In **Local Space**
3.  Select **Import Workflow**
4.  Choose [diabetes_predictor.knwf](./knime-workflows/diabetes_predictor.knwf)

#### 5.2 Configure MongoDB connection

Configure **MongoDBConnector:**

1. Right click on the **MongoDB Connector** node -> Click on Configure
2. In the pop-up window, configure the hostname, port and authentication details required to connect the server. e.g., `localhost:27017`
3. Click on Apply
4. Execute the node, green indicates that the connection was successful. Red indicates error.

Configure **MongoDBReader:**

1. Right click on the **MongoDB Reader** node -> Click on Configure
2. Provide the database name and collection name. e.g., `database name: health_data, collection: diabetes`
3. Execute the node

#### 5.3 Configure Tensorflow Network Writer

1. Right click on the **Tensorflow Network Writer** node -> Click on Configure
2. Browse and provide the path to save the model.

#### 5.4 Execute the workflow

1. From Menu bar -> Click on Execute all

This will execute all the nodes in the workflow sequentially and save the model in a zip file to the provided path.

### 6. Stopping the Services

To stop the MongoDB instance and remove the containers, execute the follwoing command:

`docker-compose down`
