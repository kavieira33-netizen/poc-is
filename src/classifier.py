
import re
import unicodedata


SOFTWARE_TERMS = {
    "software engineering": 2.0,
    "software testing": 2.0,
    "software maintenance": 2.0,
    "requirements engineering": 2.0,
    "program analysis": 1.5,
    "bug detection": 1.5,
    "software verification": 1.5,
    "code generation": 1.0,
    "software development": 1.0,
    "programming languages": 1.0,
    "continuous integration": 1.0,
    "software architecture": 1.5,
    "program repair": 1.5,
}

INTELLIGENT_TERMS = {
    "intelligent agents": 2.0,
    "vision-language agents": 2.0,
    "multi-agent systems": 2.0,
    "intelligent systems": 2.0,
    "knowledge representation": 1.5,
    "automated planning": 1.5,
    "machine learning": 1.5,
    "reasoning": 1.0,
    "autonomous systems": 1.5,
    "artificial intelligence": 1.0,
    "neural networks": 1.0,
    "reinforcement learning": 1.5,
    "large language models": 1.5,
    "vision-language": 1.5,
    "ai agents": 1.5,
    "intelligent agent": 1.5,
}

SOFTWARE_CATEGORIES = {"cs.SE", "cs.PL"}
INTELLIGENT_CATEGORIES = {"cs.AI", "cs.MA", "cs.LG", "cs.RO"}


def normalize(text):
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(
        char for char in text
        if not unicodedata.combining(char)
    )
    return re.sub(r"\s+", " ", text.lower()).strip()


def find_matches(text, terms):
    """Return matching terms, prioritizing longer phrases."""
    matches = []
    occupied = []

    for term in sorted(terms, key=len, reverse=True):
        for match in re.finditer(
            rf"(?<!\w){re.escape(term)}(?!\w)", text
        ):
            start, end = match.span()

            if any(start < old_end and end > old_start
                   for old_start, old_end in occupied):
                continue

            matches.append(term)
            occupied.append((start, end))
            break

    return matches


def classify_article(article):
    title = normalize(article.get("title", ""))
    abstract = normalize(article.get("abstract", ""))
    categories = set(article.get("categories", []))

    # The title receives more importance than a passing mention
    # in the abstract.
    software_title = find_matches(title, SOFTWARE_TERMS)
    intelligent_title = find_matches(title, INTELLIGENT_TERMS)

    software_abstract = find_matches(abstract, SOFTWARE_TERMS)
    intelligent_abstract = find_matches(abstract, INTELLIGENT_TERMS)

    software_category = bool(categories & SOFTWARE_CATEGORIES)
    intelligent_category = bool(categories & INTELLIGENT_CATEGORIES)

    software_evidence = software_title + software_abstract
    intelligent_evidence = intelligent_title + intelligent_abstract

    software_strength = min(
        1.0,
        0.65 * bool(software_title)
        + 0.25 * bool(software_abstract)
        + 0.10 * software_category,
    )
    intelligent_strength = min(
        1.0,
        0.65 * bool(intelligent_title)
        + 0.25 * bool(intelligent_abstract)
        + 0.10 * intelligent_category,
    )

    # Score the two areas separately, then calculate overall relevance.
    software_score = round(5 * software_strength, 1)
    intelligent_score = round(5 * intelligent_strength, 1)

    intersection = (
        bool(software_title or software_abstract)
        and bool(intelligent_title or intelligent_abstract)
    )

    overall_score = round(
        5 * (0.5 * software_strength + 0.5 * intelligent_strength),
        1,
    )

    topics = []
    if software_strength >= 0.30:
        topics.append("software_engineering")
    if intelligent_strength >= 0.30:
        topics.append("intelligent_systems")
    if intersection:
        topics.append("intersection")

    # The general monitor includes articles relevant to either area.
    # The intersection label requires evidence for both areas.
    relevant = bool(topics) and overall_score >= 1.5

    explanations = []

    if software_title:
        explanations.append(
            "o título contém conceitos de Engenharia de Software: "
            + ", ".join(software_title)
        )
    elif software_abstract:
        explanations.append(
            "o resumo contém conceitos de Engenharia de Software: "
            + ", ".join(software_abstract)
        )

    if intelligent_title:
        explanations.append(
            "o título contém conceitos de Sistemas Inteligentes: "
            + ", ".join(intelligent_title)
        )
    elif intelligent_abstract:
        explanations.append(
            "o resumo contém conceitos de Sistemas Inteligentes: "
            + ", ".join(intelligent_abstract)
        )

    if software_category:
        explanations.append("há evidência adicional na categoria cs.SE/cs.PL")
    if intelligent_category:
        explanations.append("há evidência adicional em categorias de IA")

    if relevant and explanations:
        justification = (
            "Selecionado por evidências temáticas. "
            + "; ".join(explanations)
            + f". Aderência a Engenharia de Software: {software_score}/5."
            + f" Aderência a Sistemas Inteligentes: {intelligent_score}/5."
            + (
                " Há evidência textual das duas áreas."
                if intersection
                else " A interseção entre as duas áreas não foi confirmada."
            )
        )
    else:
        justification = (
            "Não selecionado: evidência insuficiente de aderência "
            "às áreas configuradas."
        )

    return {
        **article,
        "relevance_score": overall_score,
        "software_engineering_score": software_score,
        "intelligent_systems_score": intelligent_score,
        "matched_topics": topics,
        "justification": justification,
        "included": relevant,
    }

INTELLIGENT_TERMS = {
    "intelligent agents": 2.0,
    "multi-agent systems": 2.0,
    "knowledge representation": 1.5,
    "automated planning": 1.5,
    "machine learning": 1.5,
    "reasoning": 1.0,
    "autonomous systems": 1.5,
    "artificial intelligence": 1.0,
    "neural networks": 1.0,
    "intelligent systems": 2.0,
}

SOFTWARE_CATEGORIES = {"cs.SE", "cs.PL"}
INTELLIGENT_CATEGORIES = {"cs.AI", "cs.MA", "cs.LG", "cs.RO"}


def normalize(text):
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(
        char for char in text
        if not unicodedata.combining(char)
    )
    return re.sub(r"\s+", " ", text.lower()).strip()


def classify_article(article):
    title = normalize(article.get("title", ""))
    abstract = normalize(article.get("abstract", ""))
    categories = set(article.get("categories", []))
    full_text = f"{title} {abstract}"

    software_matches = [
        term for term in SOFTWARE_TERMS if term in full_text
    ]
    intelligent_matches = [
        term for term in INTELLIGENT_TERMS if term in full_text
    ]

    software_score = min(
        2.0,
        sum(SOFTWARE_TERMS[t] for t in software_matches) / 2.0
    )
    intelligent_score = min(
        2.0,
        sum(INTELLIGENT_TERMS[t] for t in intelligent_matches) / 2.0
    )

    software_category = bool(categories & SOFTWARE_CATEGORIES)
    intelligent_category = bool(categories & INTELLIGENT_CATEGORIES)

    category_score = 0.5 * (
        int(software_category) + int(intelligent_category)
    )
    intersection_score = (
        1.0 if software_matches and intelligent_matches else 0.0
    )
    technical_score = (
        1.0 if software_matches or intelligent_matches else 0.0
    )

    score = round(min(
        5.0,
        software_score / 2.0
        + intelligent_score / 2.0
        + category_score
        + intersection_score
        + technical_score
    ), 1)

    topics = []
    if software_matches or software_category:
        topics.append("software_engineering")
    if intelligent_matches or intelligent_category:
        topics.append("intelligent_systems")
    if software_matches and intelligent_matches:
        topics.append("intersection")

    relevant = bool(topics) and score >= 2.0

    reasons = []
    if software_matches:
        reasons.append(
            "termos de Engenharia de Software: "
            + ", ".join(software_matches)
        )
    if intelligent_matches:
        reasons.append(
            "termos de Sistemas Inteligentes: "
            + ", ".join(intelligent_matches)
        )
    if software_category:
        reasons.append("categoria de Engenharia de Software/programação")
    if intelligent_category:
        reasons.append("categoria de Sistemas Inteligentes")

    justification = (
        "Artigo selecionado: " + "; ".join(reasons) + "."
        if relevant
        else "Baixa aderência aos critérios temáticos configurados."
    )

    return {
        **article,
        "relevance_score": score,
        "matched_topics": topics,
        "justification": justification,
        "included": relevant,
    }
