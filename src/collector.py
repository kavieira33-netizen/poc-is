
import logging
import time
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse

import feedparser
import requests

from src.classifier import classify_article


API_URL = "https://export.arxiv.org/api/query"

CATEGORIES = [
    "cs.SE",
    "cs.AI",
    "cs.MA",
    "cs.LG",
    "cs.PL",
    "cs.RO",
]

LOOKBACK_DAYS = 7
MAX_RESULTS_PER_CATEGORY = 100
REQUEST_INTERVAL_SECONDS = 3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def collect_articles():
    """Fetch recent arXiv papers by category and classify their relevance."""

    cutoff = datetime.now(timezone.utc) - timedelta(
        days=LOOKBACK_DAYS
    )

    articles_by_id = {}

    for index, category in enumerate(CATEGORIES):

        logger.info("Searching arXiv category: %s", category)

        params = {
            "search_query": f"cat:{category}",
            "start": 0,
            "max_results": MAX_RESULTS_PER_CATEGORY,
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

        logger.info(
            "Articles received from %s: %d",
            category,
            len(feed.entries),
        )

        for entry in feed.entries:

            if not entry.get("published_parsed"):
                continue

            published = datetime(
                *entry.published_parsed[:6],
                tzinfo=timezone.utc,
            )

            if published < cutoff:
                continue

            article_id = urlparse(entry.id).path.split(
                "/abs/"
            )[-1]

            if article_id in articles_by_id:
                continue

            article = {
                "arxiv_id": article_id,
                "title": " ".join(entry.title.split()),
                "authors": [
                    author.name
                    for author in entry.get("authors", [])
                ],
                "abstract": " ".join(entry.summary.split()),
                "published_at": published.isoformat(),
                "updated_at": entry.get("updated", ""),
                "categories": [
                    tag.term for tag in entry.get("tags", [])
                ],
                "url": entry.link,
                "detected_at": datetime.now(
                    timezone.utc
                ).isoformat(),
            }

            classified = classify_article(article)

            # Preserve all classified records for the reports.
            articles_by_id[article_id] = classified

        # Respect the API interval between category requests.
        if index < len(CATEGORIES) - 1:
            time.sleep(REQUEST_INTERVAL_SECONDS)

    articles = list(articles_by_id.values())

    articles.sort(
        key=lambda article: article["published_at"],
        reverse=True,
    )

    status_counts = {
        "included": 0,
        "review": 0,
        "excluded": 0,
    }

    for article in articles:
        status = article.get("classification_status", "excluded")
        if status in status_counts:
            status_counts[status] += 1

    logger.info("Unique articles collected: %d", len(articles))
    logger.info("Included automatically: %d", status_counts["included"])
    logger.info("Pending human review: %d", status_counts["review"])
    logger.info("Excluded: %d", status_counts["excluded"])

    return articles


if __name__ == "__main__":
    try:
        results = collect_articles()

        for article in results:
            print(
                f'{article["relevance_score"]}/5 | '
                f'{article["classification_status"]} | '
                f'{article["title"]} | {article["url"]}'
            )

    except (requests.RequestException, ValueError) as exc:
        logger.error("Collection failed: %s", exc)
        raise
