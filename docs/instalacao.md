# Instalação e primeira execução

Guia rápido para quem quer **usar os dados** ou **reproduzir o pipeline** localmente.

## Só quero usar os dados

Não precisa instalar nada além do que já usa:

- **JSON** (fonte canônica): arquivos em `dados/bncc-2018/` e `dados/computacao-2022/`.
- **SQLite**: `derivados/bncc.sqlite`. Abra com `sqlite3` ou qualquer cliente SQL.
- **CSV**: `derivados/csv/`. Uma planilha por entidade, pronta para Excel/Sheets.

```bash
git clone https://github.com/bncc-dev/bncc-dados.git
cd bncc-dados

# exemplo: 5 habilidades de Matemática do 3º ano
sqlite3 derivados/bncc.sqlite "
SELECT h.codigo, h.texto FROM habilidade_ef h
JOIN habilidade_ef_ano a ON a.codigo = h.codigo
WHERE h.componente = 'ef-comp-ma' AND a.ano = 3 LIMIT 5;"
```

## Quero reproduzir o pipeline

### Pré-requisitos

- Python 3.10+
- `pdftotext` (poppler) e `ghostscript`
- `jsonschema` (única dependência Python externa)

macOS:

```bash
brew install poppler ghostscript
```

Debian/Ubuntu:

```bash
sudo apt install poppler-utils ghostscript
```

Ambiente Python:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install "jsonschema>=4.18"
```

### Executar

Na ordem, a partir de `pipeline/`:

```bash
cd pipeline
python3 extrair.py      # planilhas oficiais → dados/bncc-2018/*.json
python3 extrair_ei.py   # PDF homologado → educacao-infantil.json
python3 verificar.py    # confere cada texto contra o PDF oficial
python3 validar.py      # schemas + 18 contratos (falha se algo divergir)
python3 derivar.py      # gera SQLite e CSV em derivados/
```

Se tudo passou e `git diff` está limpo, você reproduziu exatamente o dataset publicado. É a mesma checagem que o CI faz em todo push.

## Problemas comuns

| Sintoma | Causa provável |
|---|---|
| `pdftotext: command not found` | poppler não instalado (ver pré-requisitos) |
| `ModuleNotFoundError: jsonschema` | venv não ativado ou `pip install` faltando |
| `git diff` mostra mudanças após derivar | versão diferente das ferramentas; compare com o CI (`.github/workflows/validacao.yml`) |

Dúvidas ou correções: veja [CONTRIBUTING.md](../CONTRIBUTING.md). Correções de dados exigem citação da fonte oficial.
