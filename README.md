# KNIME Data Integration Project

This repository contains containerized database environments and KNIME workflows for data integration and machine learning.

## Projects

### 🗄️ [MongoDB - Diabetes Prediction](mongo/)
A containerized MongoDB environment using Docker with Python scripts for inserting and querying diabetes patient data. Includes a KNIME workflow to train a Binary Classification model to predict diabetes from patient data.

**Tech Stack:** Docker, MongoDB, Python, KNIME

---

### 📈 [InfluxDB - UE Throughput](influx/)
A containerized InfluxDB environment using Docker with Python scripts for inserting and querying time-series UE throughput data from a cellular network dataset.

**Tech Stack:** Docker, InfluxDB 2.7, Python

---

## Quick Start

| Project | Database | Dataset | README |
|---|---|---|---|
| Diabetes Prediction | MongoDB | diabetes.csv | [README](mongo/README.md) |
| UE Throughput | InfluxDB | cells.csv | [README](influx/README.md) |

## Prerequisites
* **Docker** - [Download Docker Desktop](https://www.docker.com/products/docker-desktop)
* **Python 3.x**
* **KNIME Analytics Platform** - [Download KNIME](https://www.knime.com/downloads)
