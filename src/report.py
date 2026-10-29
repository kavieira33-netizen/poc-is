
import csv
import json
from datetime import datetime, timezone
from pathlib import Path


REPORT_DIR = Path("reports")


def generate_reports(articles):
    """Generate Markdown, CSV and JSON reports."""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    run_date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Human-readable Markdown report
    lines = [
        "# arXiv Monitor — Relatório de Artigos",
        "",
        f"Execução: {run_date}",
        f"Artigos selecionados: {len(articles)}",
        "",
    ]

    for article in sorted(
        articles,
        key=lambda item: item.get("relevance_score", 0),
        reverse=True,
    ):
        lines.extend([
            f"## {article.get('title', 'Sem título')}",
            "",
            f"- **arXiv ID:** {article.get('arxiv_id', '')}",
            f"- **URL:** {article.get('url', '')}",
            f"- **Autores:** {', '.join(article.get('authors', []))}",
            f"- **Publicado em:** {article.get('published_at', '')}",
            f"- **Categorias:** {', '.join(article.get('categories', []))}",
            f"- **Nota de relevância:** "
            f"{article.get('relevance_score', 0)}/5",
            f"- **Temas:** {', '.join(article.get('matched_topics', []))}",
            f"- **Justificativa:** {article.get('justification', '')}",
            "",
            "**Resumo**",
            "",
            article.get("abstract", "Resumo não disponível"),
            "",
            "---",
            "",
        ])

    (REPORT_DIR / "latest.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )

    # Structured JSON report
    (REPORT_DIR / "articles.json").write_text(
        json.dumps(articles, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # Spreadsheet-compatible CSV report
    fields = [
        "arxiv_id",
        "title",
        "authors",
        "abstract",
        "published_at",
        "updated_at",
        "categories",
        "url",
        "relevance_score",
        "matched_topics",
        "justification",
        "detected_at",
    ]

    with (REPORT_DIR / "articles.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        for article in articles:
            row = article.copy()
            for field in ("authors", "categories", "matched_topics"):
                row[field] = "; ".join(row.get(field, []))
            writer.writerow({
                field: row.get(field, "")
                for field in fields
            })

    return REPORT_DIR
