import os
from dotenv  import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
STREAM_NAME = os.getenv("KINESIS_STREAM")
AWS_REGION = os.getenv("AWS_REGION", "ap-southeast-1")

QUERY = os.getenv("NEWS_QUERY", "technology")

POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", 30))
PAGE_SIZE = 100 # default

