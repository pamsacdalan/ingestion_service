import boto3
import json
import logging
import logging
from config import STREAM_NAME, AWS_REGION

logger = logging.getLogger(__name__)

kinesis = boto3.client("kinesis", region_name=AWS_REGION)

def send_batch(records):
    """
    Sends processed article records to an AWS Kinesis Data Stream in batches.
    Records are grouped into batches of up to 500, the maximum number of records allowed per
    PutRecords request in AWS Kinesis.

    """
    if not records:
        return
    
    batch = []

    for record in records:
        batch.append({
            "Data": json.dumps(record),
            "PartitionKey": record["article_id"]
        })

        if len(batch) == 500:
            response = kinesis.put_records(Records=batch, StreamName=STREAM_NAME)

            failed = response["FailedRecordCount"]
            if failed > 0:
                logger.warning(f"{failed} records failed to send")

            batch = []

    # send remaining records
    if batch:
        response = kinesis.put_records(Records=batch,StreamName=STREAM_NAME)

        failed = response["FailedRecordCount"]
        if failed > 0:
            logger.warning(f"{failed} records failed to send")

        return response