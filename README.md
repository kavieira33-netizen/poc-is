# Monitor Inteligente de Papers do arXiv

**Proof of Concept (PoC) — Software Engineering & Intelligent Systems**

## 1. Visão geral

Esta solução automatiza o monitoramento de novos artigos científicos publicados no [arXiv](https://arxiv.org/), com foco em duas áreas de interesse:

- Software Engineering (Engenharia de Software).
- Intelligent Systems (Sistemas Inteligentes).

A aplicação coleta artigos recentes, extrai seus metadados, aplica uma classificação heurística de relevância e gera relatórios para apoiar a identificação de publicações relacionadas às áreas monitoradas.

A execução pode ocorrer manualmente ou de forma automatizada pelo GitHub Actions.

## 2. Arquitetura da solução

O projeto está organizado em componentes independentes:

- **Collector:** consulta as categorias do arXiv, coleta os artigos e remove duplicidades.
- **Classifier:** analisa os metadados e classifica os artigos por relevância temática.
- **Report:** gera relatórios em Markdown, JSON e CSV.
- **Main:** coordena a execução dos componentes.
- **GitHub Actions:** automatiza a execução diária e disponibiliza os relatórios como artefatos.

### Fluxo de execução

1. Consulta às categorias selecionadas do arXiv.
2. Coleta e consolidação dos artigos.
3. Análise textual e cálculo dos indicadores de relevância.
4. Classificação dos artigos.
5. Geração dos relatórios.
6. Disponibilização dos resultados.

## 3. Tecnologias utilizadas

- Python 3.12
- Requests
- Feedparser
- Pytest
- GitHub Actions
- API de consulta do arXiv

## 4. Estrutura do projeto

```text
poc-is/
├── .github/
│   └── workflows/
│       └── daily-monitor.yml
├── src/
│   ├── collector.py
│   ├── classifier.py
│   ├── report.py
│   └── main.py
├── tests/
│   ├── fixtures/
│   │   └── artigos_ficticios_teste.json
│   └── test_classifier.py
├── reports/
├── requirements.txt
└── README.md
```

## 5. Instalação e execução

### Pré-requisitos

- Python 3.12
- Git
- Acesso à internet

### 5.1 Windows

Abra o PowerShell e execute:

```powershell
git clone https://github.com/kavieira33-netizen/poc-is.git
cd poc-is

python -m venv .venv
.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
```

Para executar os testes:

```powershell
python -m pytest -v
```

Para iniciar o monitoramento:

```powershell
python -m src.main
```

### 5.2 Linux e macOS

Abra o terminal e execute:

```bash
git clone https://github.com/kavieira33-netizen/poc-is.git
cd poc-is

python3.12 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
```

Para executar os testes:

```bash
python -m pytest -v
```

Para iniciar o monitoramento:

```bash
python -m src.main
```

## 6. Estratégia de classificação

A solução utiliza critérios heurísticos baseados em palavras-chave e evidências textuais dos artigos, considerando título, resumo e categorias.

Cada artigo recebe indicadores de relevância para as duas áreas monitoradas e uma nota geral de aderência, de 0 a 5.

A classificação contempla três situações:

| Status | Significado |
|---|---|
| Included | Artigo identificado como relevante automaticamente. |
| Review | Artigo com potencial de relevância, encaminhado para avaliação humana. |
| Excluded | Artigo sem evidências suficientes de aderência temática. |

A classificação também apresenta justificativa e tópicos identificados, permitindo compreender os critérios utilizados.

## 7. Relatórios gerados

A execução produz três formatos de saída:

- `latest.md`: relatório legível com os artigos identificados e suas classificações.
- `articles.json`: dados estruturados dos artigos.
- `articles.csv`: dados tabulares para análise e utilização em ferramentas externas.

Os arquivos são armazenados no diretório `reports/`.

Na execução automatizada, o GitHub Actions disponibiliza os arquivos como artefato denominado `arxiv-monitor-report`.

## 8. Agendamento automático

O workflow `daily-monitor.yml` executa diariamente pelo GitHub Actions.

Configuração:

```yaml
schedule:
  - cron: "17 10 * * *"
```

A execução ocorre às 10h17 UTC (7h17 no horário de Brasília).

Também é possível iniciar o processo manualmente pela opção **Actions → Daily arXiv Monitor → Run workflow**.

Antes do monitoramento, o workflow instala as dependências e executa os testes automatizados.

## 9. Testes

Os testes automatizados validam o comportamento do classificador utilizando artigos fictícios de teste.

Para executar localmente:

```bash
python -m pytest -v
```

## 10. Limitações e evolução

Esta versão é uma prova de conceito funcional, com classificação heurística baseada em palavras-chave e evidências textuais.

Entre as limitações identificadas estão:

- Possibilidade de falsos positivos e falsos negativos.
- Dependência da cobertura do vocabulário utilizado na classificação.
- Necessidade de avaliação humana dos artigos classificados como `Review`.
- Limite de coleta configurado por categoria.

Como evolução, estão previstas a ampliação do vocabulário, a avaliação de precisão e recall e a experimentação com métodos semânticos e modelos de inteligência artificial para aprimorar a identificação de artigos relevantes.

---

**Versão:** POC v1.0  
**Projeto:** Monitor Inteligente de Papers do arXiv  
**Repositório:** https://github.com/kavieira33-netizen/poc-is
