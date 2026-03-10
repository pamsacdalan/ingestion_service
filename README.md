# 📡 NewsAPI → Kinesis Ingestion Service



### OVERVIEW

This project implements a Python-based ingestion service that periodically retrieves news articles from the NewsAPI Everything endpoint, processes the data, and streams the structured records into an Amazon Kinesis Data Stream for downstream analytics and machine learning pipelines.

The service is designed to simulate a real-time data ingestion pipeline, ensuring that new articles are fetched regularly, validated, structured, and delivered efficiently to the streaming platform.

<br>

### 🏗 ARCHITECTURE
```
NewsAPI
   │
   ▼
Fetch Articles (HTTP API)
   │
   ▼
Data Processing
   ├── Field extraction
   ├── Text cleaning
   ├── Validation
   ├── Deduplication
   └── Metadata enrichment
   │
   ▼
Batch Records
   │
   ▼
Amazon Kinesis Data Stream
```

<br>

## ⚙️ FEATURES


#### API Integration

The service retrieves news articles from the **NewsAPI Everything API** using asynchronous HTTP requests with aiohttp. This helps reduce blocking during network I/O and improves responsiveness for periodic ingestion.




#### Data Processing

Incoming articles are processed and transformed into a standardized JSON schema containing:
```
* article_id (generated unique identifier)
* source_name
* title
* content
* url
* author
* published_at
* ingested_at
```

Processing steps include:

* Extracting relevant fields from the API response
* Cleaning text fields
* Validating required fields (```url```, ```title```)
* Generating a deterministic ```article_id``` from the article URL
* Adding an ingestion timestamp
* Removing duplicate articles




#### Streaming to Kinesis

Processed records are written to an **Amazon Kinesis Data Stream** using the ```PutRecords``` API.

To optimize throughput and reduce API overhead:
```
* Records are batched (max 500 per request) in accordance with Kinesis limits
* Failed records are logged for monitoring
```



#### Containerization

The application is containerized using **Docker** to ensure consistent runtime environments and portability.

<br>



## 📂 PROJECT STRUCTURE
```
news-ingestion-service
│
├── app
│   ├── main.py
│   ├── config.py
│   ├── news_client.py
│   ├── processor.py
│   ├── kinesis_producer.py
│   └── state_manager.py
│
├── requirements.txt
├── Dockerfile
├── .env
└── README.md
```

<br>

## ▶️ Running the Service Locally

1. Install dependencies
   ```
   pip install -r requirements.txt
   ```
   
2. Configure environment variables
   Example:
   ```
   NEWS_API_KEY=your_api_key
   AWS_REGION=ap-southeast-1
   STREAM_NAME=aurora-news-stream
   ```



3. Ensure AWS credentials are configured:
   ```
   aws configure
   ```


4. Run the ingestion service
   ```
   python app/main.py
   ```

<br>

## 🐳 DOCKER USAGE

1. Build the container:
   ```
   docker build -t news-ingestion .
   ```

3. Run the container:
   ```
   docker run --env-file .env news-ingestion
   ```


** For local Docker testing, mount your AWS credentials into the container so boto3 can authenticate with AWS Kinesis.

<br>

## Design Considerations
**Scalability**

Batching records improves ingestion throughput and reduces API overhead.


**Resilience**

Basic validation ensures malformed articles are skipped before entering the stream.


**Streaming Optimization**

Article retrieval is performed asynchronously using `aiohttp` to reduce blocking during network I/O operations. Kinesis publishing uses the standard `boto3` client, which             performs synchronous writes. For higher-throughput scenarios, this could be extended using asynchronous AWS clients.


**Deduplication**

Articles are uniquely identified using a hash derived from the article URL to prevent duplicate ingestion.



<br>

## 🔮 Future Improvements

Possible enhancements include:

* Retry logic for failed Kinesis records
* Persistent deduplication store (e.g., Redis)
* Add observability through metrics and structured monitoring
