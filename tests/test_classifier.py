
import json
from pathlib import Path

import pytest

from src.classifier import classify_article


FIXTURE_PATH = (
    Path(__file__).parent
    / "fixtures"
    / "artigos_ficticios_teste.json"
)


with open(FIXTURE_PATH, encoding="utf-8") as file:
    ARTICLES = json.load(file)


@pytest.mark.parametrize(
    "article",
    ARTICLES,
    ids=[article["test_case"] for article in ARTICLES],
)
def test_classifier_expected_results(article):
    expected_included = article["expected_included"]
    expected_topics = article["expected_topics"]

    # Remove os campos usados apenas para validar o teste.
    input_article = {
        key: value
        for key, value in article.items()
        if key not in {
            "expected_included",
            "expected_topics",
            "test_case",
        }
    }

    result = classify_article(input_article)

    assert result["included"] == expected_included, (
        f'{article["test_case"]}: '
        f'inclusão esperada={expected_included}, '
        f'recebida={result["included"]}, '
        f'nota={result["relevance_score"]}'
    )

    assert set(result["matched_topics"]) == set(expected_topics), (
        f'{article["test_case"]}: '
        f'temas esperados={expected_topics}, '
        f'recebidos={result["matched_topics"]}'
    )
