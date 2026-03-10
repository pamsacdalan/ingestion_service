import asyncio
import logging
from news_client import fetch_articles
from processor import process_articles
from kinesis_producer import send_batch
from state_manager import save_last_timestamp
from config import POLL_INTERVAL

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)

async def run():
    while True:
        try:
            articles = await fetch_articles()
            processed, latest_timestamp = process_articles(articles)

            if processed:
                send_batch(processed)

                logger.info(f"Sent {len(processed)} records to Kinesis")

                if latest_timestamp:
                    save_last_timestamp(latest_timestamp)
        
        except Exception as e:
            logger.error(f"Ingestion error: {e}")
        
        await asyncio.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    asyncio.run(run())