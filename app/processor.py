from datetime import datetime
import hashlib

# In-memory cache
seen_article_ids = set()

def generate_article_id(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()

def clean_text(text):
    if not text:
        return None
    return text.strip()

def extract_content(article):
    content = article.get("content")

    if not content: # fallback to description if content is missing
        content = article.get("description")
    
    return clean_text(content)


def process_articles(articles):
    processed = []
    latest_timestamp = None

    for article in articles:
        url = article.get("url")
        title = article.get("title")

        if not url or not title:
            continue

        article_id = generate_article_id(url)

        # Skip duplicates
        if article_id in seen_article_ids:
            continue
        seen_article_ids.add(article_id)

        published = article.get("publishedAt")

        record = {
            "article_id": article_id,
            "source_name": clean_text(article["source"].get("name")),
            "title": clean_text(title),
            "content": extract_content(article),
            "url": url,
            "author": clean_text(article.get("author")),
            "published_at": published,
            "ingested_at": datetime.now().isoformat()
        }

        processed.append(record)

        if published and (not latest_timestamp or published > latest_timestamp):
            latest_timestamp = published
    
    return processed, latest_timestamp