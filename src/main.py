
import logging
import sys

from src.collector import collect_articles
from src.report import generate_reports


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting arXiv monitoring process")

    try:
        articles = collect_articles()
        report_dir = generate_reports(articles)

        logger.info("Monitoring completed successfully")
        logger.info("Relevant articles: %d", len(articles))
        logger.info("Reports saved in: %s", report_dir.resolve())

        print(f"\nProcess completed. Articles found: {len(articles)}")
        print(f"Reports available in: {report_dir.resolve()}")

    except Exception:
        logger.exception("Monitoring process failed")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
