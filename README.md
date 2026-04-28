# data_ingestion_pipeline
This is my personal data engineering project version of a real-world project translating an enterprise pattern into my own architecture.


## Problem Statement
The organization depended on external data sources to support critical business processes. However, the existing transfer workflow required files to be downloaded locally before being uploaded to cloud storage. This created multiple operational risks.

The business needed a more reliable and scalable approach to move data efficiently from source systems into cloud storage.
Click <a href="">here</a> to view statement.


## Project Objectives
The primary objective of the project was to design a modern ingestion pipeline that could transfer large unstructured data directly from external sources into cloud storage.


## Proposed Solution
I designed a direct-to-cloud streaming pipeline that ingests data in chunks from external sources and uploads it directly into cloud object storage.
Instead of storing files temporarily on local servers, data moves continuously through the pipeline from source to destination.

## Solution Architecture
Components Used:
•	FastAPI & Python
•	Amazon S3
•	PostgreSQL


