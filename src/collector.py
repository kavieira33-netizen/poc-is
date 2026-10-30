
import logging
import time
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse

import feedparser
import requests

from src.classifier import classify_article


API_URL = "https://export.arxiv.org/api/query"
CATEGORIES = ["cs.SE", "cs.AI", "cs.MA", "cs.LG", "cs.PL", "cs.RO"]
LOOKBACK_DAYS = 7
MAX_RESULTS = 100

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def collect_articles():
    """Fetch recent arXiv papers and classify their relevance."""
    category_query = " OR ".join(
        f"cat:{category}" for category in CATEGORIES
    )

    params = {
        "search_query": f"({category_query})",
        "start": 0,
        "max_results": MAX_RESULTS,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }

    response = requests.get(
        API_URL,
        params=params,
        timeout=60,
        headers={"User-Agent": "arxiv-monitor/1.0"},
    )
    response.raise_for_status()

    feed = feedparser.parse(response.content)
    logger.info("Articles received from arXiv: %d", len(feed.entries))
    
    cutoff = datetime.now(timezone.utc) - timedelta(
        days=LOOKBACK_DAYS
    )

    articles = []
    seen_ids = set()

    for entry in feed.entries:
        published = datetime(*entry.published_parsed[:6],
                             tzinfo=timezone.utc)

        # Keep only papers first published within the lookback window.
        if published < cutoff:
            continue

        article_id = urlparse(entry.id).path.split("/abs/")[-1]

        # Ignore duplicate IDs returned by overlapping categories.
        if article_id in seen_ids:
            continue
        seen_ids.add(article_id)

        article = {
            "arxiv_id": article_id,
            "title": " ".join(entry.title.split()),
            "authors": [
                author.name for author in entry.get("authors", [])
            ],
            "abstract": " ".join(entry.summary.split()),
            "published_at": published.isoformat(),
            "updated_at": entry.get("updated", ""),
            "categories": [
                tag.term for tag in entry.get("tags", [])
            ],
            "url": entry.link,
            "detected_at": datetime.now(timezone.utc).isoformat(),
        }

        classified = classify_article(article)

        # Preserva todos os artigos classificados para os relatórios.
        # O status define se serão incluídos, revisados ou excluídos.
        articles.append(classified)

    logger.info("Relevant articles found: %d", len(articles))
    return articles


if __name__ == "__main__":
    try:
        results = collect_articles()
        for article in results:
            print(
                f'{article["relevance_score"]}/5 | '
                f'{article["title"]} | {article["url"]}'
            )
    except (requests.RequestException, ValueError) as exc:
        logger.error("Collection failed: %s", exc)
        raise
