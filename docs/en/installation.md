[Português](../instalacao.md) · **English**

# Installation and first run

A quick guide for anyone who wants to **use the data** or **reproduce the pipeline** locally.

## I just want to use the data

You do not need to install anything beyond what you already use:

- **JSON** (canonical source): files in `dados/bncc-2018/` and `dados/computacao-2022/`.
- **SQLite**: `derivados/bncc.sqlite`. Open it with `sqlite3` or any SQL client.
- **CSV**: `derivados/csv/`. One spreadsheet per entity, ready for Excel/Sheets.

```bash
git clone https://github.com/bncc-dev/bncc-dados.git
cd bncc-dados

# exemplo: 5 habilidades de Matemática do 3º ano
sqlite3 derivados/bncc.sqlite "
SELECT h.codigo, h.texto FROM habilidade_ef h
JOIN habilidade_ef_ano a ON a.codigo = h.codigo
WHERE h.componente = 'ef-comp-ma' AND a.ano = 3 LIMIT 5;"
```

## I want to reproduce the pipeline

### Prerequisites

- Python 3.10+
- `pdftotext` (poppler) and `ghostscript`
- `jsonschema` (the only external Python dependency)

macOS:

```bash
brew install poppler ghostscript
```

Debian/Ubuntu:

```bash
sudo apt install poppler-utils ghostscript
```

Python environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt   # jsonschema>=4.18
```

### Run

In this order, from `pipeline/`:

```bash
cd pipeline
python3 extrair.py              # official spreadsheets → dados/bncc-2018/*.json
python3 extrair_ei.py           # homologated PDF → educacao-infantil.json
python3 extrair_computacao.py   # Computing annex + structure map → computacao.json
python3 verificar.py            # checks each text against the official PDF
python3 verificar_computacao.py # checks Computing against the official annex
python3 validar_schema.py       # JSON Schemas, with a negative self-test
python3 validar.py              # 29 contract and completeness checks (fails on any divergence)
python3 derivar.py              # generates SQLite and CSV in derivados/
```

If everything passed and `git diff` is clean, you have reproduced the published dataset exactly. It is the same check that CI runs on every push.

## Common problems

| Symptom | Probable cause |
|---|---|
| `pdftotext: command not found` | poppler is not installed (see Prerequisites) |
| `ModuleNotFoundError: jsonschema` | venv not activated, or `pip install` not run |
| `git diff` shows changes after the derivation step | different tool versions; compare with CI (`.github/workflows/validacao.yml`) |

Questions or corrections: see [CONTRIBUTING.en.md](../../CONTRIBUTING.en.md). Data corrections require citing the official source.
