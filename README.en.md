# [bncc.dev](https://bncc.dev) · open data of Brazil's National Common Curricular Base

[Português](README.md) · **English**

[![Validation](https://github.com/bncc-dev/bncc-dados/actions/workflows/validacao.yml/badge.svg)](https://github.com/bncc-dev/bncc-dados/actions/workflows/validacao.yml)
[![Data: CC BY 4.0](https://img.shields.io/badge/data-CC%20BY%204.0-lightgrey.svg)](dados/LICENSE.md)
[![Code: MIT](https://img.shields.io/badge/code-MIT-green.svg)](LICENSE)
[![Status: stable](https://img.shields.io/badge/status-stable-brightgreen.svg)](CHANGELOG.md)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21625233.svg)](https://doi.org/10.5281/zenodo.21625233)

Brazil's National Common Curricular Base (BNCC) as structured, verified and traceable data. The BNCC defines what every student in Brazilian basic education has the right to learn, and it is the mandatory reference for the curriculum of every school in the country. This dataset has 1,721 learning objectives: 1,580 from the three stages of basic education plus 141 from the Computing supplement (CNE/CEB Opinion 2/2022). Every record carries its competencies, organizational context and provenance, checked against the official document.

The texts of the learning objectives are in Portuguese, as in the official documents. Field names are in Portuguese too; every field is explained in the [data dictionary](docs/en/data-dictionary.md).

## Quick start

The shortest path is the packages built on top of this dataset:

```bash
npx -y @bncc/mcp        # MCP server: the BNCC available to your AI agent
npm install @bncc/dados # TypeScript/JavaScript
pip install bncc        # Python
```

Or straight from the data, with no dependency at all:

```bash
git clone https://github.com/bncc-dev/bncc-dados.git
cd bncc-dados
python3 -c "
import json
ef = json.load(open('dados/bncc-2018/ensino-fundamental.json'))
h = next(x for x in ef['habilidades'] if x['codigo'] == 'EF67LP08')
print(h['texto'])
print(h['fonte']['localizador_pdf'])
"
```

Sample record (Elementary and Lower Secondary Education):

```json
{
  "codigo": "EF67LP08",
  "texto": "Identificar os efeitos de sentido devidos à escolha de imagens estáticas...",
  "componente": "ef-comp-lp",
  "anos": [6, 7],
  "organizacao": {
    "tipo": "campo_pratica",
    "campos_atuacao": ["ef-comp-lp-catu-campo-jornalistico-midiatico"],
    "pratica_linguagem": "ef-comp-lp-prat-leitura"
  },
  "objetos_conhecimento": ["ef-comp-lp-oc-efeitos-de-sentido-exploracao-da-multissemiose"],
  "vigencia": {"status": "vigente", "desde": "dados-2026.07", "ate": null},
  "fonte": {
    "localizador": "aba Língua Portuguesa, linha 229",
    "localizador_pdf": "Base-Nacional-Comum-Curricular-BNCC.pdf, página PDF 167"
  }
}
```

`codigo` is the official code, `texto` the official text, `anos` the school years, `organizacao` and `objetos_conhecimento` the curricular context, `vigencia` the validity period, and `fonte` the source: the sheet and row of the Ministry of Education spreadsheet and the page of the officially approved (homologated) PDF.

**Status: stable.** First release: content `dados-2026.07`, format `schema-v1.0.0`. The data is complete, validated and pedagogically reviewed. Identifiers and format are covered by the [versioning](docs/en/versioning.md) guarantees: a change that breaks consumers requires a new major version of the schema.

Maintained by [Profy](https://profy.com.br), which is also its first consumer.

## Why trust this data

1. **Every learning objective points to the official source** (field `fonte`): sheet and row of the Ministry of Education (MEC) spreadsheet in EF and EM, PDF page in EI and page of the annex of CNE/CEB Opinion 2/2022 in Computing, always with the page of the official document where the text was checked (`localizador_pdf`).
2. **Automatic verification, character by character**: in BNCC 2018, all 1,580 texts match the homologated PDF. Where the official sources disagree with each other, the decision taken is documented in `DECISOES.md`, the decisions log. In the Computing supplement, 141 of 141 match the annex of CNE/CEB Opinion 2/2022.
3. **Proven completeness**: a scan of codes in the homologated PDF and in the Computing annex finds exactly the codes present in the dataset. Nothing is missing and nothing is extra.
4. **Reproducible extraction**: run `pipeline/` and you get the same files. Continuous integration does this on every change and fails on any difference.

## What is here

| Folder | Contents |
|---|---|
| `dados/bncc-2018/` | The dataset in JSON: system structure, 93 Early Childhood Education objectives (with alignments across age groups), 1,304 Elementary and Lower Secondary skills (with thematic units, knowledge objects, fields of action and language practices), 183 Upper Secondary skills (with linked competencies), 20 legal milestones with official URLs and 5 reference profiles |
| `dados/computacao-2022/` | The Computing supplement (CNE/CEB Opinion 2/2022): 141 learning objectives (11 EI, 104 EF, 26 EM) with axes, knowledge objects and their own competencies, verified against the official annex |
| `fontes/` | The official documents from MEC and CNE that everything is extracted from, with checksums, and the structure map of the Computing supplement ([details](fontes/README.en.md)) |
| `schema/` | JSON Schemas (draft 2020-12) that define and validate the format of each data file |
| `derivados/` | The same data in SQLite and CSV, generated from the JSON files (for SQL and spreadsheets) |
| `pipeline/` | Extraction, verification and validation scripts: anyone can reproduce the dataset from the sources |
| `DECISOES.md` | Every interpretation decision about inconsistencies in the sources, documented ([summary in English](docs/en/decisions-summary.md)) |
| `docs/` | Methodology, data model, versioning, installation and more (see [Documentation](#documentation)) |

## Other formats

The same data, besides JSON:

```bash
# SQL: Portuguese Language skills of year 6 with their language practice
sqlite3 derivados/bncc.sqlite "
SELECT h.codigo, c.nome FROM habilidade_ef h
JOIN contexto_organizacao c ON c.id = h.pratica_linguagem
JOIN habilidade_ef_ano a ON a.codigo = h.codigo
WHERE h.componente = 'ef-comp-lp' AND a.ano = 6 LIMIT 5;"
```

And `derivados/csv/` has one spreadsheet per entity, ready for Excel or Sheets. The JSON files remain the canonical source; the derived formats are generated and checked in continuous integration. The data format is defined by the JSON Schemas in `schema/`, validated on every change.

## Accessing the data

| Mechanism | Format | Where |
|---|---|---|
| Canonical files | JSON | [`dados/`](dados/) in this repository |
| Derived files | SQLite, SQL dump, CSV | [`derivados/`](derivados/) |
| Archived releases | ZIP of the repository, SQLite and CSV | [Zenodo, DOI 10.5281/zenodo.21625233](https://doi.org/10.5281/zenodo.21625233) |
| npm package | JSON embedded, TypeScript API | [@bncc/dados](https://www.npmjs.com/package/@bncc/dados) |
| PyPI package | JSON embedded, Python API | [bncc](https://pypi.org/project/bncc/) |
| MCP server | MCP tools over JSON | local: `npx -y @bncc/mcp`; hosted: `https://mcp.bncc.dev/mcp` |
| REST API | JSON, OpenAPI 3.1 | [api.bncc.dev](https://api.bncc.dev/v1/openapi.json), free, no key |
| Website | HTML, Markdown and CSV per page | [bncc.dev](https://bncc.dev) |

All of them serve the same data. The files in this repository and on Zenodo are the complete dataset; the packages, the MCP server, the API and the website are conveniences built on top of it. The API and the website code are private, and neither is required to use the data.

## Reproducing the extraction

```bash
cd pipeline
python3 extrair.py             # official spreadsheets → dados/bncc-2018/*.json
python3 extrair_ei.py          # homologated PDF → educacao-infantil.json
python3 extrair_computacao.py  # annex of CNE/CEB Opinion 2/2022 → computacao.json
python3 verificar.py           # checks each text against the PDF; records the page
python3 verificar_computacao.py # checks Computing against the official annex
python3 validar_schema.py      # JSON Schemas, with a negative self-test
python3 validar.py             # 29 contract and completeness checks (fails on any divergence)
python3 derivar.py             # generates derivados/ (SQLite and CSV) from the JSON files
```

This is exactly the sequence continuous integration runs, ending with a comparison between the committed dataset and the reproduced one.

Dependencies: Python 3.10+, `pdftotext` (poppler), `ghostscript` (to normalize the Computing annex) and `jsonschema>=4.18` (only for format validation). Full step by step, per operating system and with common problems: [docs/en/installation.md](docs/en/installation.md).

## Documentation

| Document | Purpose |
|---|---|
| [docs/en/data-model.md](docs/en/data-model.md) | How the BNCC is modeled: entities, codes, relations and what the model does not invent |
| [docs/en/data-dictionary.md](docs/en/data-dictionary.md) | Every field of every file: type, whether required, meaning, allowed values and a real example |
| [docs/en/methodology.md](docs/en/methodology.md) | The chain of trust: from official sources to continuous integration, with the verification numbers |
| [docs/en/versioning.md](docs/en/versioning.md) | Data-versions, validity of records and what consumers can rely on |
| [docs/en/installation.md](docs/en/installation.md) | Installation and first run (use the data or reproduce the pipeline) |
| [docs/en/decisions-summary.md](docs/en/decisions-summary.md) | Summary of every interpretation decision ([full log in Portuguese](DECISOES.md)) |
| [docs/en/content-policy.md](docs/en/content-policy.md) | What the dataset distributes, how errors and inappropriate content are detected and fixed, and how fast |
| [docs/en/open-and-commercial.md](docs/en/open-and-commercial.md) | What is open, what may be paid, and the rule that nothing moves from open to paid |
| [fontes/README.en.md](fontes/README.en.md) | The official sources, their checksums and provenance notes |
| [docs/relatorio-validacao.md](docs/relatorio-validacao.md) | Snapshot of the validation report for the current version (in Portuguese) |
| [CHANGELOG.md](CHANGELOG.md) | History by category: normative, correction, schema, editorial (in Portuguese) |
| [CONTRIBUTING.en.md](CONTRIBUTING.en.md) | How to propose corrections (rule: official source in the pull request) |
| [CODE_OF_CONDUCT.en.md](CODE_OF_CONDUCT.en.md) | Community code of conduct, including the protection of minors |
| [SECURITY.en.md](SECURITY.en.md) | How to report a security problem (a data error is a regular issue) |
| [AGENTS.md](AGENTS.md) | Guide for AI agents (in Portuguese; see also [llms.txt](llms.txt)) |

## Contributing

Data corrections are welcome, and there is a single golden rule: **every correction must cite the official source** (a MEC or CNE document, with page or locator). Continuous integration automatically checks the reproducibility of any change. Start with [CONTRIBUTING.en.md](CONTRIBUTING.en.md).

## For AI agents

Read `llms.txt` at the root. In short: consume the JSON files in `dados/bncc-2018/`, use the official codes as keys (`EF67LP08`, `EM13LGG103`, `EI02TS01`), never invent codes or skill texts, and cite the source that comes with each record.

## Dependencies and platform independence

No part of the dataset depends on closed or proprietary software.

- **To use the data:** nothing but a JSON, CSV or SQLite reader. The formats are open and require no library, service or account.
- **To reproduce the extraction:** Python 3.10+ (standard library only), poppler's `pdftotext` (GPL), Ghostscript (AGPL) and `jsonschema` (MIT, in [`requirements.txt`](requirements.txt)). All of these licenses are OSI-approved.
- **Hosting:** GitHub hosts the repository, and every release is also archived on Zenodo with a DOI. Any clone has everything needed to reproduce the dataset.
- **Packages and MCP:** the npm and PyPI packages embed the data and work offline. The MCP server hosted at mcp.bncc.dev runs on Cloudflare, but it is optional: `npx -y @bncc/mcp` runs the same server on your machine.

## Who maintains it

The project is maintained by [Profy Tecnologias Educacionais Ltda](https://profy.com.br) (CNPJ 53.669.787/0001-45, Brasília, Brazil), which holds the rights to the compilation, structure, identifiers and code. Technical lead: Marcos Roberto Martins de Oliveira. Contact: contato@bncc.dev. More at [bncc.dev/en/about](https://bncc.dev/en/about/).

## Licenses

- **Data** (`dados/`): [CC BY 4.0](dados/LICENSE.md). The normative texts of the BNCC are official acts and are not protected by copyright (Law 9,610/1998, art. 8, IV). The license covers the compilation, structure and curation, whose rights belong to Profy.
- **Code** (`pipeline/`): [MIT](LICENSE).

What is open here stays open, irrevocably: see [docs/en/open-and-commercial.md](docs/en/open-and-commercial.md).

To cite the dataset in a publication, use the `CITATION.cff` file at the root (the *Cite this repository* button in the sidebar generates the formatted citation).

## Packages and website

Built on this dataset and published in 0.x versions: the npm package [@bncc/dados](https://www.npmjs.com/package/@bncc/dados), the PyPI package [bncc](https://pypi.org/project/bncc/) and the MCP server [@bncc/mcp](https://www.npmjs.com/package/@bncc/mcp), with code in [bncc-pacotes](https://github.com/bncc-dev/bncc-pacotes). Every learning objective has a permanent page at [bncc.dev](https://bncc.dev).
