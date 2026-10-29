import re
import unicodedata

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

}

INTELLIGENT_TERMS = {
    "agentes inteligentes": 2.0,
    "agentes de visão-linguagem": 2.0,
    "sistemas multiagentes": 2.0,
    "sistemas inteligentes": 2.0,
    "representação do conhecimento": 1.5,
    "planejamento automatizado": 1.5,
    "aprendizado de máquina": 1.5,
    "sistemas autônomos": 1.5,
    "inteligência artificial": 1.0,
    "aprendizagem por reforço": 1.5,
    "grandes modelos de linguagem": 1.5,
    "linguagem visual": 1.5,
    "agentes de IA": 1.5,
    "agente inteligente": 1.5,
    "intelligent agents": 2.0,
    "vision-language agents": 2.0,
    "multi-agent systems": 2.0,
    "intelligent systems": 2.0,
    "knowledge representation": 1.5,
    "automated planning": 1.5,
    "machine learning": 1.5,
    "autonomous systems": 1.5,
    "artificial intelligence": 1.0,
    "reinforcement learning": 1.5,
    "large language models": 1.5,
    "vision-language": 1.5,
    "AI agents": 1.5,
    "agentes autônomos": 2.0,
    "autonomous agents": 2.0,
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
        for match in re.finditer(rf"(?<!\w){re.escape(term)}(?!\w)", text):
            start, end = match.span()
            if any(start < old_end and end > old_start for old_start, old_end in occupied):
                continue
            matches.append(term)
            occupied.append((start, end))
            break
    return matches

def classify_article(article):
    title = normalize(article.get("title", ""))
    abstract = normalize(article.get("abstract", ""))
    categories = set(article.get("categories", []))
    
    # O título recebe mais importância do que uma menção passageira no resumo.
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
    
    # Avalie as duas áreas separadamente e, em seguida, calcule a relevância geral.
    software_score = round(5 * software_strength, 1)
    intelligent_score = round(5 * intelligent_strength, 1)
    
    topics = []

    if software_strength >= 0.30:
        topics.append("software_engineering")

    if intelligent_strength >= 0.30:
        topics.append("intelligent_systems")

    intersection = (
        "software_engineering" in topics
        and "intelligent_systems" in topics
    )

    if intersection:
        topics.append("intersection")
        
    # O monitor geral includes artigos relevantes para ambas as áreas.
    # A etiqueta de intersecção requer evidências para ambas as áreas.
    relevant = bool(topics) and overall_score >= 2.0
    explanations = []
    if software_title:
        explanations.append("o título contém conceitos de Engenharia de Software: " + ", ".join(software_title))
    elif software_abstract:
        explanations.append("o resumo contém conceitos de Engenharia de Software: " + ", ".join(software_abstract))
        
    if intelligent_title:
        explanations.append("o título contém conceitos de Sistemas Inteligentes: " + ", ".join(intelligent_title))
    elif intelligent_abstract:
        explanations.append("o resumo contém conceitos de Sistemas Inteligentes: " + ", ".join(intelligent_abstract))
        
    if software_category:
        explanations.append("há evidências adicionais na categoria cs.SE/cs.PL")
    if intelligent_category:
        explanations.append("há evidências adicionais em categorias de IA")
        
    if relevant and explanations:
        justification = (
            "Selecionado por evidências temáticas. "
            + "; ".join(explanations)
            + f". Aderência a Engenharia de Software: {software_score}/5."
            + f" Aderência a Sistemas Inteligentes: {intelligent_score}/5."
            + (
                " Embasamento textual das duas áreas."
                if intersection
                else " A interseção entre as duas áreas não foi confirmada."
            )
        )
    else:
        justification = "Não selecionado: evidência insuficiente de eficácia às áreas configuradas."
        
   
    return {
        **article,
        "relevance_score": overall_score,
        "software_engineering_score": software_score,
        "intelligent_systems_score": intelligent_score,
        "matched_topics": topics,
        "justification": justification,
        "included": relevant,
    }
