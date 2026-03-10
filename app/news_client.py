import aiohttp
import logging
from config import NEWS_API_KEY, QUERY, PAGE_SIZE
from state_manager import get_last_timestamp


NEWS_API_URL = "https://newsapi.org/v2/everything"

logger = logging.getLogger(__name__)


async def fetch_articles():

    params = {
        "q": QUERY,
        "apiKey": NEWS_API_KEY,
        "pageSize": PAGE_SIZE,
        "sortBy": "publishedAt",
        "language": "en",
    }

    last_timestamp = get_last_timestamp()

    if last_timestamp:
        params["from"] = last_timestamp
    

    async with aiohttp.ClientSession() as session:
        async with session.get(NEWS_API_URL, params=params) as response:
            if response.status != 200:
                text = await response.text()
                raise Exception(f"News API error: {text}")
            
            data = await response.json()
            articles = data.get("articles", [])

            logger.info(f"Fetched {len(articles)} articles")

            return articles
