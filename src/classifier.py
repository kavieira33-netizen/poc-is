
import re
import unicodedata


# Pesos dos termos relacionados à Engenharia de Software.
SOFTWARE_TERMS = {
    "engenharia de software": 2.0,
    "teste de software": 2.0,
    "manutenção de software": 2.0,
    "engenharia de requisitos": 2.0,
    "análise de programa": 1.5,
    "detecção de bugs": 1.5,
    "verificação de software": 1.5,
    "geração de código": 1.0,
    "desenvolvimento de software": 1.0,
    "linguagens de programação": 1.0,
    "integração contínua": 1.0,
    "arquitetura de software": 1.5,
    "reparo de programa": 1.5,
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
    "mutation testing": 2.0,
    "microservice architectures": 1.5,
    "test suite": 1.0,
    "code review": 2.0,
    "defect detection": 1.5,
    "test case generation": 2.0,
    "bug localization": 1.5,
}


# Pesos dos termos relacionados a Sistemas Inteligentes.
INTELLIGENT_TERMS = {
    "agentes inteligentes": 2.0,
    "agentes de visão-linguagem": 2.0,
    "sistemas multiagentes": 2.0,
    "sistemas inteligentes": 2.0,
    "representação do conhecimento": 1.5,
    "planejamento automatizado": 1.5,
    "aprendizado de máquina": 1.0,
    "sistemas autônomos": 1.5,
    "inteligência artificial": 0.8,
    "aprendizagem por reforço": 1.5,
    "grandes modelos de linguagem": 1.0,
    "linguagem visual": 1.0,
    "agentes de IA": 1.5,
    "agente inteligente": 1.5,
    "intelligent agents": 2.0,
    "vision-language agents": 2.0,
    "multi-agent systems": 2.0,
    "intelligent systems": 2.0,
    "knowledge representation": 1.5,
    "automated planning": 1.5,
    "machine learning": 1.0,
    "autonomous systems": 1.5,
    "artificial intelligence": 0.8,
    "reinforcement learning": 1.5,
    "large language models": 1.0,
    "vision-language": 1.0,
    "AI agents": 1.5,
    "agentes autônomos": 2.0,
    "autonomous agents": 2.0,
    "AI-assisted code review": 2.0,
    "explainable AI": 1.5,
    "large language model agents": 2.0,
    "language model agents": 2.0,
    "multi-agent planning": 2.0,
    "knowledge graph": 1.5,
    "robotics": 1.0,
    "autonomous robots": 1.5,
}


# Categorias complementares do arXiv.
SOFTWARE_CATEGORIES = {"cs.SE", "cs.PL"}
INTELLIGENT_CATEGORIES = {"cs.AI", "cs.MA", "cs.LG", "cs.RO"}

# Pontuação mínima para reconhecer uma área.
MINIMUM_SCORE = 2.0

# A categoria acrescenta evidência, mas nunca classifica sozinha.
CATEGORY_BONUS = 0.5


def normalize(text):
    """Padroniza o texto para facilitar a comparação dos termos."""
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(
        char
        for char in text
        if not unicodedata.combining(char)
    )
    return re.sub(r"\s+", " ", text.lower()).strip()


def find_matches(text, terms):
    """
    Localiza termos no texto.
    Prioriza expressões mais longas para evitar duplicidade.
    """
    matches = []
    occupied = []

    normalized_terms = [
        (normalize(term), term)
        for term in terms
    ]

    for normalized_term, original_term in sorted(
        normalized_terms,
        key=lambda item: len(item[0]),
        reverse=True,
    ):
        for match in re.finditer(
            rf"(?<!\w){re.escape(normalized_term)}(?!\w)",
            text,
        ):
            start, end = match.span()

            if any(
                start < old_end and end > old_start
                for old_start, old_end in occupied
            ):
                continue

            matches.append(original_term)
            occupied.append((start, end))
            break

    return matches


def calculate_area_score(
    title_matches,
    abstract_matches,
    terms,
    category_match,
):
    """
    Calcula a pontuação de uma área.

    Título: peso multiplicado por 1,5.
    Resumo: peso integral.
    Categoria arXiv: bônus complementar de 0,5.
    """
    title_score = sum(
        terms[term] * 1.5
        for term in title_matches
    )

    abstract_score = sum(
        terms[term]
        for term in abstract_matches
    )

    textual_score = title_score + abstract_score

    # Sem evidência textual, a categoria não gera pontuação.
    if textual_score <= 0:
        return 0.0

    total_score = textual_score

    if category_match:
        total_score += CATEGORY_BONUS

    return round(min(5.0, total_score), 1)


def classify_article(article):
    """Classifica um artigo nas áreas de interesse do monitor."""

    title = normalize(article.get("title", ""))
    abstract = normalize(article.get("abstract", ""))

    categories = set(article.get("categories", []))

    # Identificação das evidências no título.
    software_title = find_matches(title, SOFTWARE_TERMS)
    intelligent_title = find_matches(title, INTELLIGENT_TERMS)

    # Identificação das evidências no resumo.
    software_abstract = find_matches(abstract, SOFTWARE_TERMS)
    intelligent_abstract = find_matches(abstract, INTELLIGENT_TERMS)

    # Evidências complementares nas categorias.
    software_category = bool(
        categories & SOFTWARE_CATEGORIES
    )

    intelligent_category = bool(
        categories & INTELLIGENT_CATEGORIES
    )

    # Cálculo independente das duas áreas.
    software_score = calculate_area_score(
        software_title,
        software_abstract,
        SOFTWARE_TERMS,
        software_category,
    )

    intelligent_score = calculate_area_score(
        intelligent_title,
        intelligent_abstract,
        INTELLIGENT_TERMS,
        intelligent_category,
    )

    # Identificação das áreas efetivamente reconhecidas.
    topics = []

    if software_score >= MINIMUM_SCORE:
        topics.append("software_engineering")

    if intelligent_score >= MINIMUM_SCORE:
        topics.append("intelligent_systems")

    # A interseção exige classificação nas duas áreas.
    intersection = (
        "software_engineering" in topics
        and "intelligent_systems" in topics
    )

    if intersection:
        topics.append("intersection")

    relevant = bool(topics)

    # Pontuação geral corresponde à maior aderência individual.
    overall_score = round(
        max(software_score, intelligent_score),
        1,
    )

    # Construção da justificativa.
    explanations = []

    if software_title:
        explanations.append(
            "o título contém conceitos de Engenharia de Software: "
            + ", ".join(software_title)
        )

    if software_abstract:
        explanations.append(
            "o resumo contém conceitos de Engenharia de Software: "
            + ", ".join(software_abstract)
        )

    if intelligent_title:
        explanations.append(
            "o título contém conceitos de Sistemas Inteligentes: "
            + ", ".join(intelligent_title)
        )

    if intelligent_abstract:
        explanations.append(
            "o resumo contém conceitos de Sistemas Inteligentes: "
            + ", ".join(intelligent_abstract)
        )

    if software_category and software_score > 0:
        explanations.append(
            "a categoria do arXiv fornece evidência complementar "
            "para Engenharia de Software"
        )

    if intelligent_category and intelligent_score > 0:
        explanations.append(
            "a categoria do arXiv fornece evidência complementar "
            "para Sistemas Inteligentes"
        )

    if relevant:
        justification = (
            "Selecionado por evidências temáticas. "
            + "; ".join(explanations)
            + f". Aderência a Engenharia de Software: {software_score}/5."
            + f" Aderência a Sistemas Inteligentes: {intelligent_score}/5."
        )

        if intersection:
            justification += (
                " O artigo apresenta evidências nas duas áreas."
            )
        else:
            justification += (
                " A interseção entre as duas áreas não foi confirmada."
            )

    else:
        justification = (
            "Não selecionado: evidência temática insuficiente "
            "para atingir a pontuação mínima das áreas configuradas."
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
