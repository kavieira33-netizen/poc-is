
import re
import unicodedata


# ============================================================
# 1. VOCABULÁRIO DE ENGENHARIA DE SOFTWARE
# ============================================================

SOFTWARE_TERMS = {
    "engenharia de software": 2.0,
    "software engineering": 2.0,
    "teste de software": 2.0,
    "software testing": 2.0,
    "teste de sistema": 1.5,
    "software maintenance": 2.0,
    "software verification": 1.5,
    "requirements engineering": 2.0,
    "engenharia de requisitos": 2.0,
    "program analysis": 1.5,
    "análise de programa": 1.5,
    "bug detection": 1.5,
    "detecção de bugs": 1.5,
    "code generation": 1.0,
    "geração de código": 1.0,
    "software development": 1.0,
    "desenvolvimento de software": 1.0,
    "programming languages": 1.0,
    "linguagens de programação": 1.0,
    "continuous integration": 1.0,
    "integração contínua": 1.0,
    "software architecture": 1.5,
    "arquitetura de software": 1.5,
    "program repair": 1.5,
    "reparo de programa": 1.5,
    "mutation testing": 2.0,
    "microservice architectures": 1.5,
    "test suite": 1.0,
    "code review": 2.0,
    "defect detection": 1.5,
    "test case generation": 2.0,
    "bug localization": 1.5,
    "regression testing": 1.5,
    "automated software testing": 2.0,
    "software quality": 1.5,
    "software maintenance": 2.0,
    "software process": 1.5,
    "software engineering process": 2.0,
    "requirements analysis": 1.5,
    "requirements validation": 1.5,
    "software design": 1.5,
    "software refactoring": 1.5,
    "continuous delivery": 1.0,
    "devops": 1.0,
    "model-based testing": 1.5,
    "automated program repair": 2.0,
    "program comprehension": 1.5,
    "software defect prediction": 1.5,
}


# ============================================================
# 2. VOCABULÁRIO DE SISTEMAS INTELIGENTES
# ============================================================

# Termos com evidência temática mais específica.
INTELLIGENT_TERMS = {
    "intelligent agents": 2.0,
    "agentes inteligentes": 2.0,
    "autonomous agents": 2.0,
    "agentes autônomos": 2.0,
    "multi-agent systems": 2.0,
    "sistemas multiagentes": 2.0,
    "multi-agent planning": 2.0,
    "vision-language agents": 2.0,
    "agentes de visão-linguagem": 2.0,
    "computer-using agents": 2.0,
    "AI agents": 1.5,
    "agentes de IA": 1.5,
    "intelligent systems": 2.0,
    "sistemas inteligentes": 2.0,
    "knowledge representation": 1.5,
    "representação do conhecimento": 1.5,
    "knowledge graph reasoning": 2.0,
    "knowledge graph": 1.5,
    "grafos de conhecimento": 1.5,
    "automated planning": 1.5,
    "planejamento automatizado": 1.5,
    "reinforcement learning": 1.5,
    "aprendizagem por reforço": 1.5,
    "aprendizado por reforço": 1.5,
    "autonomous systems": 1.5,
    "sistemas autônomos": 1.5,
    "autonomous robots": 1.5,
    "robôs autônomos": 1.5,
    "vision-language-action": 2.0,
    "vision language action": 2.0,
    "embodied AI": 1.5,
    "robotic manipulation": 1.5,
    "multi-agent reinforcement learning": 2.0,
    "explainable AI": 1.5,
    "IA explicável": 1.5,
    "AI-assisted code review": 2.0,
    "large language model agents": 2.0,
    "language model agents": 2.0,
    "neuro-symbolic": 1.5,
    "neuro-symbolic systems": 2.0,
    "symbolic reasoning": 1.5,
    "adaptive control": 1.5,
    "intelligent robotics": 2.0,
    "robotics": 1.0,
}


# Termos genéricos: isoladamente não comprovam aderência.
GENERIC_INTELLIGENT_TERMS = {
    "artificial intelligence": 0.8,
    "inteligência artificial": 0.8,
    "machine learning": 0.8,
    "aprendizado de máquina": 0.8,
    "aprendizagem de máquina": 0.8,
    "large language models": 0.8,
    "grandes modelos de linguagem": 0.8,
    "language models": 0.5,
    "modelos de linguagem": 0.5,
    "deep learning": 0.8,
    "aprendizado profundo": 0.8,
    "neural networks": 0.5,
    "redes neurais": 0.5,
    "foundation models": 0.5,
    "modelos fundacionais": 0.5,
    "vision-language": 0.8,
    "linguagem visual": 0.5,
}


# ============================================================
# 3. CATEGORIAS DO ARXIV E CRITÉRIOS
# ============================================================

SOFTWARE_CATEGORIES = {"cs.SE", "cs.PL"}

INTELLIGENT_CATEGORIES = {
    "cs.AI",
    "cs.MA",
    "cs.LG",
    "cs.RO",
}

MINIMUM_SCORE = 2.0
CATEGORY_BONUS = 0.3

# Um artigo precisa de evidência específica para ser
# automaticamente incluído.
# Termos genéricos isolados levam à revisão humana.


# ============================================================
# 4. NORMALIZAÇÃO
# ============================================================

def normalize(text):
    """Padroniza o texto para facilitar a comparação."""
    text = unicodedata.normalize("NFKD", text or "")

    text = "".join(
        char
        for char in text
        if not unicodedata.combining(char)
    )

    return re.sub(r"\s+", " ", text.lower()).strip()


# ============================================================
# 5. IDENTIFICAÇÃO DE TERMOS
# ============================================================

def is_negated(text, start):
    """
    Verifica se a ocorrência está em um contexto negado.
    Considera a frase anterior ao termo.
    """

    sentence_start = max(
        text.rfind(".", 0, start),
        text.rfind(";", 0, start),
        text.rfind("!", 0, start),
        text.rfind("?", 0, start),
    ) + 1

    context = text[sentence_start:start].strip()

    words = context.split()[-12:]
    context = " ".join(words)

    negations = [
        "not",
        "no",
        "never",
        "without",
        "does not",
        "do not",
        "did not",
        "doesn't",
        "don't",
        "is not",
        "are not",
        "was not",
        "were not",
        "isn't",
        "aren't",
        "wasn't",
        "weren't",
        "not develop",
        "not use",
        "not propose",
        "not present",
        "not focus",
        "nao",
        "nunca",
        "sem",
    ]

    # Evita interpretar "not only" como negação.
    if re.search(r"\bnot only\b", context):
        return False

    return any(
        re.search(
            rf"(?<!\w){re.escape(term)}(?!\w)",
            context,
        )
        for term in negations
    )


def find_matches(text, terms):
    """
    Encontra termos no texto.
    Prioriza expressões longas e evita duplicidade.
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

            if is_negated(text, start):
                continue

            matches.append(original_term)
            occupied.append((start, end))
            break

    return matches


# ============================================================
# 6. CÁLCULO DA PONTUAÇÃO
# ============================================================

def calculate_area_score(
    title_matches,
    abstract_matches,
    terms,
    category_match,
):
    """
    Título: peso multiplicado por 1,5.
    Resumo: peso integral.
    Categoria: bônus complementar de 0,3.
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

    # Categoria nunca classifica um artigo sozinha.
    if textual_score <= 0:
        return 0.0

    total_score = textual_score

    if category_match:
        total_score += CATEGORY_BONUS

    return round(min(5.0, total_score), 1)


# ============================================================
# 7. CLASSIFICAÇÃO DE UMA ÁREA
# ============================================================

def classify_area(
    title,
    abstract,
    specific_terms,
    generic_terms=None,
    category_match=False,
):
    """Calcula evidências específicas e genéricas de uma área."""

    title_specific = find_matches(title, specific_terms)
    abstract_specific = find_matches(abstract, specific_terms)

    title_generic = []
    abstract_generic = []

    if generic_terms:
        title_generic = find_matches(title, generic_terms)
        abstract_generic = find_matches(abstract, generic_terms)

    specific_title_score = sum(
        specific_terms[term] * 1.5
        for term in title_specific
    )

    specific_abstract_score = sum(
        specific_terms[term]
        for term in abstract_specific
    )

    generic_title_score = sum(
        generic_terms[term] * 1.5
        for term in title_generic
    ) if generic_terms else 0.0

    generic_abstract_score = sum(
        generic_terms[term]
        for term in abstract_generic
    ) if generic_terms else 0.0

    specific_score = (
        specific_title_score
        + specific_abstract_score
    )

    generic_score = (
        generic_title_score
        + generic_abstract_score
    )

    textual_score = specific_score + generic_score

    if textual_score > 0 and category_match:
        textual_score += CATEGORY_BONUS

    score = round(min(5.0, textual_score), 1)

    has_specific_evidence = specific_score >= MINIMUM_SCORE

    has_any_evidence = textual_score > 0

    return {
        "score": score,
        "specific_score": round(specific_score, 1),
        "generic_score": round(generic_score, 1),
        "specific_title": title_specific,
        "specific_abstract": abstract_specific,
        "generic_title": title_generic,
        "generic_abstract": abstract_generic,
        "has_specific_evidence": has_specific_evidence,
        "has_any_evidence": has_any_evidence,
    }


# ============================================================
# 8. CLASSIFICADOR PRINCIPAL
# ============================================================

def classify_article(article):
    """Classifica o artigo nas duas áreas do monitor."""

    title = normalize(article.get("title", ""))
    abstract = normalize(article.get("abstract", ""))

    categories = set(article.get("categories", []))

    software = classify_area(
        title,
        abstract,
        SOFTWARE_TERMS,
        category_match=bool(
            categories & SOFTWARE_CATEGORIES
        ),
    )

    intelligent = classify_area(
        title,
        abstract,
        INTELLIGENT_TERMS,
        generic_terms=GENERIC_INTELLIGENT_TERMS,
        category_match=bool(
            categories & INTELLIGENT_CATEGORIES
        ),
    )

    # Evidência suficiente para inclusão automática.
    software_confirmed = (
        software["has_specific_evidence"]
    )

    intelligent_confirmed = (
        intelligent["has_specific_evidence"]
    )

    topics = []

    if software_confirmed:
        topics.append("software_engineering")

    if intelligent_confirmed:
        topics.append("intelligent_systems")

    intersection = (
        software_confirmed
        and intelligent_confirmed
    )

    if intersection:
        topics.append("intersection")

    # Identificação de evidência parcial.
    any_evidence = (
    software["score"] >= 1.0
    or intelligent["score"] >= 1.0
)
    # Status: incluído, revisão ou excluído.
    if software_confirmed or intelligent_confirmed:
        status = "included"

    elif any_evidence:
        status = "review"

    else:
        status = "excluded"

    review_required = status == "review"

    # Artigos em revisão permanecem no fluxo de saída,
    # mas são identificados separadamente.
    included = status in {"included", "review"}

    overall_score = round(
        max(
            software["score"],
            intelligent["score"],
        ),
        1,
    )

    # ========================================================
    # JUSTIFICATIVA
    # ========================================================

    explanations = []

    if software["specific_title"]:
        explanations.append(
            "título com evidências de Engenharia de Software: "
            + ", ".join(software["specific_title"])
        )

    if software["specific_abstract"]:
        explanations.append(
            "resumo com evidências de Engenharia de Software: "
            + ", ".join(software["specific_abstract"])
        )

    if intelligent["specific_title"]:
        explanations.append(
            "título com evidências de Sistemas Inteligentes: "
            + ", ".join(intelligent["specific_title"])
        )

    if intelligent["specific_abstract"]:
        explanations.append(
            "resumo com evidências de Sistemas Inteligentes: "
            + ", ".join(intelligent["specific_abstract"])
        )

    if intelligent["generic_title"] or intelligent["generic_abstract"]:
        generic_matches = (
            intelligent["generic_title"]
            + intelligent["generic_abstract"]
        )

        explanations.append(
            "termos genéricos de IA encontrados: "
            + ", ".join(generic_matches)
        )

    if not explanations:
        explanations.append(
            "não foram encontrados termos temáticos suficientes"
        )

    justification = (
        " ".join(explanations)
        + f". Engenharia de Software: {software['score']}/5."
        + f" Sistemas Inteligentes: {intelligent['score']}/5."
    )

    if status == "included":
        justification = "INCLUÍDO AUTOMATICAMENTE. " + justification

    elif status == "review":
        justification = (
            "REVISÃO HUMANA NECESSÁRIA. "
            "Há evidências parciais ou genéricas, "
            "mas não suficientes para inclusão automática. "
            + justification
        )

    else:
        justification = "EXCLUÍDO. " + justification

    if intersection:
        justification += (
            " O artigo apresenta evidências específicas "
            "nas duas áreas e foi classificado na interseção."
        )

    return {
        **article,
        "relevance_score": overall_score,
        "software_engineering_score": software["score"],
        "intelligent_systems_score": intelligent["score"],
        "matched_topics": topics,
        "classification_status": status,
        "review_required": review_required,
        "justification": justification,
        "included": included,
    }
