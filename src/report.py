
import csv
import json
from datetime import datetime, timezone
from pathlib import Path


REPORT_DIR = Path("reports")


def get_status(article):
    """
    Obtém o status da classificação.
    Mantém compatibilidade com registros antigos.
    """
    status = article.get("classification_status")

    if status in {"included", "review", "excluded"}:
        return status

    if article.get("included", False):
        return "included"

    return "excluded"


def format_article(article):
    """Formata os dados de um artigo para o relatório Markdown."""

    status_labels = {
        "included": "Incluído automaticamente",
        "review": "Pendente de revisão humana",
        "excluded": "Excluído",
    }

    status = get_status(article)

    return [
        f"## {article.get('title', 'Sem título')}",
        "",
        f"- **Status:** {status_labels[status]}",
        f"- **arXiv ID:** {article.get('arxiv_id', '')}",
        f"- **URL:** {article.get('url', '')}",
        f"- **Autores:** {', '.join(article.get('authors', []))}",
        f"- **Publicado em:** {article.get('published_at', '')}",
        f"- **Categorias:** {', '.join(article.get('categories', []))}",
        f"- **Nota geral:** {article.get('relevance_score', 0)}/5",
        f"- **Engenharia de Software:** "
        f"{article.get('software_engineering_score', 0)}/5",
        f"- **Sistemas Inteligentes:** "
        f"{article.get('intelligent_systems_score', 0)}/5",
        f"- **Temas:** {', '.join(article.get('matched_topics', []))}",
        f"- **Justificativa:** {article.get('justification', '')}",
        "",
        "**Resumo**",
        "",
        article.get("abstract", "Resumo não disponível"),
        "",
        "---",
        "",
    ]


def generate_reports(articles):
    """
    Gera relatórios Markdown, CSV e JSON.

    Os registros recebidos são separados em:
    - Incluídos automaticamente;
    - Pendentes de revisão humana;
    - Excluídos.
    """

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    run_date = datetime.now(timezone.utc).strftime(
        "%Y-%m-%d %H:%M UTC"
    )

    # Separa os artigos conforme o status.
    included_articles = [
        article for article in articles
        if get_status(article) == "included"
    ]

    review_articles = [
        article for article in articles
        if get_status(article) == "review"
    ]

    excluded_articles = [
        article for article in articles
        if get_status(article) == "excluded"
    ]

    # Ordena cada grupo pela pontuação geral.
    sort_articles = lambda items: sorted(
        items,
        key=lambda item: item.get("relevance_score", 0),
        reverse=True,
    )

    included_articles = sort_articles(included_articles)
    review_articles = sort_articles(review_articles)
    excluded_articles = sort_articles(excluded_articles)

    # --------------------------------------------------------
    # RELATÓRIO MARKDOWN
    # --------------------------------------------------------

    lines = [
        "# arXiv Monitor — Relatório de Artigos",
        "",
        f"Execução: {run_date}",
        "",
        "## Resumo da execução",
        "",
        f"- **Total de registros recebidos:** {len(articles)}",
        f"- **Incluídos automaticamente:** {len(included_articles)}",
        f"- **Pendentes de revisão humana:** {len(review_articles)}",
        f"- **Excluídos:** {len(excluded_articles)}",
        "",
        "## 1. Artigos incluídos automaticamente",
        "",
    ]

    if included_articles:
        for article in included_articles:
            lines.extend(format_article(article))
    else:
        lines.extend(["Nenhum artigo incluído automaticamente.", ""])

    lines.extend([
        "## 2. Artigos pendentes de revisão humana",
        "",
    ])

    if review_articles:
        for article in review_articles:
            lines.extend(format_article(article))
    else:
        lines.extend(["Nenhum artigo pendente de revisão.", ""])

    lines.extend([
        "## 3. Artigos excluídos",
        "",
    ])

    if excluded_articles:
        for article in excluded_articles:
            lines.extend(format_article(article))
    else:
        lines.extend(["Nenhum artigo excluído recebido pelo relatório.", ""])

    (REPORT_DIR / "latest.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    # --------------------------------------------------------
    # RELATÓRIO JSON
    # --------------------------------------------------------

    json_data = []

    for article in articles:
        record = article.copy()
        record["classification_status"] = get_status(article)
        record["review_required"] = (
            record["classification_status"] == "review"
        )
        json_data.append(record)

    (REPORT_DIR / "articles.json").write_text(
        json.dumps(
            json_data,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    # --------------------------------------------------------
    # RELATÓRIO CSV
    # --------------------------------------------------------

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
        "software_engineering_score",
        "intelligent_systems_score",
        "matched_topics",
        "classification_status",
        "review_required",
        "justification",
        "detected_at",
    ]

    with (REPORT_DIR / "articles.csv").open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fields,
        )

        writer.writeheader()

        for article in articles:
            row = article.copy()

            row["classification_status"] = get_status(article)

            row["review_required"] = (
                row["classification_status"] == "review"
            )

            for field in (
                "authors",
                "categories",
                "matched_topics",
            ):
                value = row.get(field, [])

                if isinstance(value, list):
                    row[field] = "; ".join(value)

            writer.writerow({
                field: row.get(field, "")
                for field in fields
            })

    return REPORT_DIR
