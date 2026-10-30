
import re
import unicodedata


# ============================================================
# 1. VOCABULÁRIO DE ENGENHARIA DE SOFTWARE
# ============================================================

SOFTWARE_TERMS = {
    # Área e ciclo de vida
    "software engineering": 2.0,
    "engenharia de software": 2.0,
    "software development": 1.5,
    "desenvolvimento de software": 1.5,
    "software lifecycle": 1.5,
    "ciclo de vida de software": 1.5,
    "software process": 1.5,
    "processo de software": 1.5,
    "software engineering process": 2.0,
    "software maintenance": 2.0,
    "software evolution": 1.5,
    "software modernization": 1.5,
    "legacy software": 1.5,
    "legacy code": 1.5,
    "modernizacao de software": 1.5,
    "manutencao de software": 2.0,
    "evolucao de software": 1.5,
    "codigo legado": 1.5,

    # Requisitos, arquitetura e projeto
    "requirements engineering": 2.0,
    "engenharia de requisitos": 2.0,
    "requirements analysis": 1.5,
    "requirements validation": 1.5,
    "requirements elicitation": 1.5,
    "software requirements": 1.5,
    "requisitos de software": 1.5,
    "software architecture": 1.5,
    "arquitetura de software": 1.5,
    "software design": 1.5,
    "projeto de software": 1.5,
    "software product line": 1.5,
    "software modeling": 1.5,
    "modelagem de software": 1.5,
    "design patterns": 1.0,
    "microservice architecture": 1.5,
    "microservice architectures": 1.5,
    "arquitetura de microsservicos": 1.5,

    # Testes, qualidade e verificação
    "software testing": 2.0,
    "teste de software": 2.0,
    "automated software testing": 2.0,
    "teste automatizado de software": 2.0,
    "software test": 1.5,
    "software verification": 1.5,
    "verificacao de software": 1.5,
    "software validation": 1.5,
    "validacao de software": 1.5,
    "mutation testing": 2.0,
    "teste de mutacao": 2.0,
    "regression testing": 1.5,
    "teste de regressao": 1.5,
    "model-based testing": 1.5,
    "test case generation": 2.0,
    "geracao de casos de teste": 2.0,
    "test suite": 1.0,
    "test oracle": 1.5,
    "test coverage": 1.5,
    "cobertura de testes": 1.5,
    "software quality": 1.5,
    "qualidade de software": 1.5,
    "software reliability": 1.5,
    "confiabilidade de software": 1.5,
    "software defect": 1.5,
    "software defects": 1.5,
    "defect detection": 1.5,
    "bug detection": 1.5,
    "deteccao de defeitos": 1.5,
    "deteccao de bugs": 1.5,
    "bug localization": 1.5,
    "localizacao de bugs": 1.5,

    # Código, linguagens e análise
    "program analysis": 1.5,
    "static analysis": 1.5,
    "analise estatica": 1.5,
    "dynamic analysis": 1.5,
    "analise dinamica": 1.5,
    "code analysis": 1.5,
    "analise de codigo": 1.5,
    "source code": 1.0,
    "codigo-fonte": 1.0,
    "programming languages": 1.5,
    "linguagens de programacao": 1.5,
    "program comprehension": 1.5,
    "compreensao de programas": 1.5,
    "code comprehension": 1.5,
    "code review": 2.0,
    "revisao de codigo": 2.0,
    "code generation": 1.5,
    "geracao de codigo": 1.5,
    "code refactoring": 1.5,
    "software refactoring": 1.5,
    "refatoracao de codigo": 1.5,
    "program repair": 1.5,
    "automated program repair": 2.0,
    "reparo automatico de programas": 2.0,
    "program synthesis": 1.5,
    "sintese de programas": 1.5,
    "compiler optimization": 1.5,
    "otimizacao de compiladores": 1.5,
    "static code analysis": 1.5,
    "code clone detection": 1.5,
    "deteccao de clones de codigo": 1.5,

    # Segurança de software
    "software security": 1.5,
    "seguranca de software": 1.5,
    "software vulnerability": 1.5,
    "software vulnerabilities": 1.5,
    "vulnerability detection": 1.5,
    "vulnerability repair": 1.5,
    "deteccao de vulnerabilidades": 1.5,
    "correcao de vulnerabilidades": 1.5,
    "secure software development": 1.5,
    "desenvolvimento seguro de software": 1.5,
    "static application security testing": 2.0,

    # Operação, entrega e ferramentas
    "continuous integration": 1.5,
    "integracao continua": 1.5,
    "continuous delivery": 1.5,
    "continuous deployment": 1.5,
    "entrega continua": 1.5,
    "implantacao continua": 1.5,
    "ci/cd": 1.0,
    "devops": 1.5,
    "software deployment": 1.0,
    "software configuration management": 1.5,
    "gerenciamento de configuracao de software": 1.5,
    "build systems": 1.0,
    "build system": 1.0,
    "dependency management": 1.0,
    "gerenciamento de dependencias": 1.0,
    "software repository": 1.0,
    "repositorio de software": 1.0,
    "open-source software": 1.0,
    "software ecosystem": 1.0,
    "ecossistema de software": 1.0,
}


# ============================================================
# 2. VOCABULÁRIO DE SISTEMAS INTELIGENTES
# ============================================================

INTELLIGENT_TERMS = {
    # Agentes e sistemas multiagentes
    "intelligent systems": 2.0,
    "sistemas inteligentes": 2.0,
    "intelligent agents": 2.0,
    "agentes inteligentes": 2.0,
    "autonomous agents": 2.0,
    "agentes autonomos": 2.0,
    "multi-agent systems": 2.0,
    "multiagent systems": 2.0,
    "sistemas multiagentes": 2.0,
    "multi-agent planning": 2.0,
    "multi-agent reinforcement learning": 2.0,
    "cooperative agents": 1.5,
    "agentes cooperativos": 1.5,
    "agent-based systems": 1.5,
    "sistemas baseados em agentes": 1.5,
    "AI agents": 1.5,
    "agentes de IA": 1.5,
    "large language model agents": 2.0,
    "language model agents": 2.0,
    "computer-using agents": 2.0,
    "vision-language agents": 2.0,

    # Representação e raciocínio
    "knowledge representation": 1.5,
    "representacao do conhecimento": 1.5,
    "knowledge graph reasoning": 2.0,
    "knowledge graphs": 1.5,
    "knowledge graph": 1.5,
    "grafos de conhecimento": 1.5,
    "symbolic reasoning": 1.5,
    "raciocinio simbolico": 1.5,
    "automated reasoning": 1.5,
    "raciocinio automatizado": 1.5,
    "neuro-symbolic systems": 2.0,
    "neuro-symbolic": 1.5,
    "ontological reasoning": 1.5,
    "ontology learning": 1.5,
    "aprendizagem de ontologias": 1.5,

    # Aprendizado e decisão
    "reinforcement learning": 1.5,
    "aprendizagem por reforco": 1.5,
    "aprendizado por reforco": 1.5,
    "deep reinforcement learning": 2.0,
    "multi-agent reinforcement learning": 2.0,
    "automated planning": 1.5,
    "planejamento automatizado": 1.5,
    "decision-making systems": 1.5,
    "sistemas de tomada de decisao": 1.5,
    "adaptive control": 1.5,
    "controle adaptativo": 1.5,
    "intelligent decision support": 1.5,
    "suporte inteligente a decisao": 1.5,

    # Robótica e sistemas autônomos
    "autonomous systems": 1.5,
    "sistemas autonomos": 1.5,
    "autonomous robots": 1.5,
    "robos autonomos": 1.5,
    "intelligent robotics": 2.0,
    "robotic manipulation": 1.5,
    "robotics": 1.0,
    "robotica": 1.0,
    "embodied AI": 1.5,
    "vision-language-action": 2.0,
    "vision language action": 2.0,
    "autonomous navigation": 1.5,
    "navegacao autonoma": 1.5,
    "human-robot interaction": 1.5,
    "interacao humano-robo": 1.5,

    # IA explicável e sistemas cognitivos
    "explainable AI": 1.5,
    "explainable artificial intelligence": 1.5,
    "IA explicavel": 1.5,
    "interpretable machine learning": 1.5,
    "aprendizado de maquina interpretavel": 1.5,
    "cognitive architectures": 1.5,
    "arquiteturas cognitivas": 1.5,
    "intelligent decision-making": 1.5,
    "AI-assisted code review": 2.0,
    "revisao de codigo assistida por IA": 2.0,
    "sistemas especialistas": 1.5,
    "expert systems": 1.5,
    "sistemas especialistas": 1.5,
    "expert systems": 1.5,
}


# Termos genéricos não são suficientes, isoladamente,
# para inclusão automática.
GENERIC_INTELLIGENT_TERMS = {
    "artificial intelligence": 0.8,
    "inteligencia artificial": 0.8,
    "machine learning": 0.8,
    "aprendizado de maquina": 0.8,
    "aprendizagem de maquina": 0.8,
    "large language models": 0.8,
    "large language model": 0.8,
    "grandes modelos de linguagem": 0.8,
    "language models": 0.5,
    "modelos de linguagem": 0.5,
    "deep learning": 0.8,
    "aprendizado profundo": 0.8,
    "neural networks": 0.5,
    "redes neurais": 0.5,
    "foundation models": 0.5,
    "modelos fundacionais": 0.5,
    "computer vision": 0.5,
    "visao computacional": 0.5,
    "natural language processing": 0.5,
    "processamento de linguagem natural": 0.5,
}


# ============================================================
# 3. CATEGORIAS DO ARXIV E CRITÉRIOS
# ============================================================

SOFTWARE_CATEGORIES = {"cs.SE", "cs.PL"}
INTELLIGENT_CATEGORIES = {"cs.AI", "cs.MA", "cs.LG", "cs.RO"}

MINIMUM_SCORE = 2.0
REVIEW_SCORE = 1.0
CATEGORY_BONUS = 0.3


# ============================================================
# 4. NORMALIZAÇÃO
# ============================================================

def normalize(text):
    """Remove diferenças de caixa, acentos e espaços excedentes."""
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(
        char for char in text
        if not unicodedata.combining(char)
    )
    return re.sub(r"\s+", " ", text.lower()).strip()


# ============================================================
# 5. IDENTIFICAÇÃO DE TERMOS E CONTEXTO
# ============================================================

def is_negated(text, start):
    """
    Verifica se há negação imediatamente antes do termo.
    A expressão 'not only' não é considerada negação.
    """
    sentence_start = max(
        text.rfind(".", 0, start),
        text.rfind(";", 0, start),
        text.rfind("!", 0, start),
        text.rfind("?", 0, start),
    ) + 1

    context = text[sentence_start:start].strip()
    context = " ".join(context.split()[-8:])

    if re.search(r"\bnot\s+only\b", context):
        context = re.sub(r"\bnot\s+only\b", "", context)

    negation_patterns = [
        r"\bnot\b",
        r"\bno\b",
        r"\bnever\b",
        r"\bwithout\b",
        r"\bdoes\s+not\b",
        r"\bdo\s+not\b",
        r"\bdid\s+not\b",
        r"\bdoesn't\b",
        r"\bdon't\b",
        r"\bisn't\b",
        r"\baren't\b",
        r"\bwasn't\b",
        r"\bweren't\b",
        r"\bnao\b",
        r"\bnunca\b",
        r"\bsem\b",
    ]

    return any(re.search(pattern, context) for pattern in negation_patterns)


def find_matches(text, terms):
    """
    Encontra cada expressão no máximo uma vez por campo.
    Expressões mais longas são avaliadas primeiro para evitar
    contar simultaneamente uma expressão e seu fragmento.
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
        if not normalized_term:
            continue

        pattern = rf"(?<!\w){re.escape(normalized_term)}(?!\w)"

        for match in re.finditer(pattern, text):
            start, end = match.span()

            overlaps = any(
                start < old_end and end > old_start
                for old_start, old_end in occupied
            )
            if overlaps or is_negated(text, start):
                continue

            matches.append(original_term)
            occupied.append((start, end))
            break

    return matches


# ============================================================
# 6. CLASSIFICAÇÃO DE UMA ÁREA
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

    specific_score = specific_title_score + specific_abstract_score
    generic_score = generic_title_score + generic_abstract_score
    textual_score = specific_score + generic_score

    # A categoria do arXiv é apenas um reforço,
    # nunca evidência isolada.
    if textual_score > 0 and category_match:
        textual_score += CATEGORY_BONUS

    score = round(min(5.0, textual_score), 1)
    specific_score = round(specific_score, 1)

    return {
        "score": score,
        "textual_score": round(specific_score + generic_score, 1),
        "specific_score": specific_score,
        "generic_score": round(generic_score, 1),
        "specific_title": title_specific,
        "specific_abstract": abstract_specific,
        "generic_title": title_generic,
        "generic_abstract": abstract_generic,
        "has_specific_evidence": specific_score >= MINIMUM_SCORE,
        "has_any_evidence": textual_score > 0,
    }


# ============================================================
# 7. CLASSIFICADOR PRINCIPAL
# ============================================================

def classify_article(article):
    """Classifica um artigo em Engenharia de Software e Sistemas Inteligentes."""

    title = normalize(article.get("title", ""))
    abstract = normalize(article.get("abstract", ""))
    categories = set(article.get("categories", []))

    software = classify_area(
        title,
        abstract,
        SOFTWARE_TERMS,
        category_match=bool(categories & SOFTWARE_CATEGORIES),
    )

    intelligent = classify_area(
        title,
        abstract,
        INTELLIGENT_TERMS,
        generic_terms=GENERIC_INTELLIGENT_TERMS,
        category_match=bool(categories & INTELLIGENT_CATEGORIES),
    )

    # A inclusão automática exige evidência textual específica
    # em pelo menos uma das áreas.
    software_confirmed = software["has_specific_evidence"]
    intelligent_confirmed = intelligent["has_specific_evidence"]

    topics = []
    if software_confirmed:
        topics.append("software_engineering")
    if intelligent_confirmed:
        topics.append("intelligent_systems")

    intersection = software_confirmed and intelligent_confirmed
    if intersection:
        topics.append("intersection")

    # O bônus da categoria arXiv não conta como evidência textual
    # para encaminhar um artigo à revisão humana.
    any_evidence = (
        software["textual_score"] >= REVIEW_SCORE
        or intelligent["textual_score"] >= REVIEW_SCORE
    )

    if software_confirmed or intelligent_confirmed:
        status = "included"
    elif any_evidence:
        status = "review"
    else:
        status = "excluded"

    review_required = status == "review"

    # Mantém incluídos e itens para revisão no fluxo de saída.
    # Excluídos também são retornados para auditoria e contagem.
    included = status in {"included", "review"}

    overall_score = round(
        max(software["score"], intelligent["score"]),
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

    generic_matches = (
        intelligent["generic_title"]
        + intelligent["generic_abstract"]
    )
    if generic_matches:
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
            "Há evidências parciais ou genéricas, mas não suficientes "
            "para inclusão automática. "
            + justification
        )
    else:
        justification = "EXCLUÍDO. " + justification

    if intersection:
        justification += (
            " O artigo apresenta evidências específicas nas duas áreas "
            "e foi classificado na interseção."
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
