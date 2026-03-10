# NewsAPI → Kinesis Ingestion Service



### Overview

This project implements a Python-based ingestion service that periodically retrieves news articles from the NewsAPI Everything endpoint, processes the data, and streams the structured records into an Amazon Kinesis Data Stream for downstream analytics and machine learning pipelines.

The service is designed to simulate a real-time data ingestion pipeline, ensuring that new articles are fetched regularly, validated, structured, and delivered efficiently to the streaming platform.



### Architecture

NewsAPI
│
▼
Fetch Articles (HTTP API)
│
▼
Data Processing

* Field extraction
* Text cleaning
* Validation
* Deduplication
* Metadata enrichment
  │
  ▼
  Batch Records
  │
  ▼
  Amazon Kinesis Data Stream



### Features



##### API Integration

The service retrieves news articles from the NewsAPI Everything API using a configurable query and API key.



##### Data Processing

Incoming articles are processed and transformed into a standardized JSON schema containing:

* article\_id (generated unique identifier)
* source\_name
* title
* content
* url
* author
* published\_at
* ingested\_at
* 

Processing steps include:

* Extracting relevant fields from the API response
* Cleaning text fields
* Validating required fields (url, title)
* Generating a deterministic article\_id from the article URL
* Adding an ingestion timestamp
* Removing duplicate articles



##### Streaming to Kinesis

Processed records are written to an Amazon Kinesis Data Stream using the PutRecords API.

To optimize throughput and reduce API overhead:

* Records are batched (max 500 per request) in accordance with Kinesis limits
* Failed records are logged for monitoring



##### Containerization

The application is containerized using Docker to ensure consistent runtime environments and portability.



##### Project Structure

news-ingestion-service
│
├── app
│   ├── main.py
│   ├── config.py
│   ├── news\_client.py
│   ├── processor.py
│   ├── kinesis\_producer.py
│   └── state\_manager.py
│
├── requirements.txt
├── Dockerfile
├── .env
└── README.md



## Running the Service Locally

1. Install dependencies
   pip install -r requirements.txt
   
2. Configure environment variables
   Example:
   NEWS\_API\_KEY=your\_api\_key
   AWS\_REGION=ap-southeast-1
   STREAM\_NAME=aurora-news-stream



Ensure AWS credentials are configured:
   aws configure



3. Run the ingestion service
   python app/main.py



## Docker Usage

Build the container:
docker build -t news-ingestion .

Run the container:
docker run --env-file .env news-ingestion

** For local Docker testing, mount your AWS credentials into the container so boto3 can authenticate with AWS Kinesis.


## Design Considerations

* Scalability
  Batching records improves ingestion throughput and reduces API overhead.
* Redilience
  Basic validation ensures malformed articles are skipped before entering the stream.
* Streaming Optimization
  Using the Kinesis PutRecords API allows efficient batch ingestion.
* Deduplication
  Articles are uniquely identified using a hash derived from the article URL.



## Future Improvements

Possible enhancements include:

* Retry logic for failed Kinesis records
* Persistent deduplication store (e.g., Redis)
* Async fetching for lower latency
* Cloud deployment (AWS ECS / Lambda)
* Observability via CloudWatch metrics
