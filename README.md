# [bncc.dev](https://bncc.dev) · dados abertos da BNCC

[![Validação](https://github.com/bncc-dev/bncc-dados/actions/workflows/validacao.yml/badge.svg)](https://github.com/bncc-dev/bncc-dados/actions/workflows/validacao.yml)
[![Dados: CC BY 4.0](https://img.shields.io/badge/dados-CC%20BY%204.0-lightgrey.svg)](dados/LICENSE.md)
[![Código: MIT](https://img.shields.io/badge/c%C3%B3digo-MIT-green.svg)](LICENSE)
[![Status: pré-release](https://img.shields.io/badge/status-pr%C3%A9--release-orange.svg)](CHANGELOG.md)

A Base Nacional Comum Curricular como dados estruturados, verificados e rastreáveis: 1.721 aprendizagens, sendo as 1.580 das três etapas da educação básica mais as 141 do complemento de Computação (Parecer CNE/CEB 2/2022). Cada registro traz competências, contextos de organização e proveniência, conferido contra o documento oficial.

## Uso rápido

O caminho mais curto são os pacotes construídos sobre este dataset:

```bash
npx -y @bncc/mcp        # servidor MCP: a BNCC ao alcance do seu agente de IA
npm install @bncc/dados # TypeScript/JavaScript
pip install bncc        # Python
```

Ou direto dos dados, sem dependência alguma:

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

Exemplo de registro (Ensino Fundamental):

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

**Status: pré-release.** Dados completos e validados, aguardando revisão pedagógica e primeira release versionada (`dados-v1.0.0`); os pacotes acima estão em 0.1.x e chegam à 1.0 junto com ela. Até lá, os identificadores e o formato podem mudar.

Mantido pela [Profy](https://profy.com.br), que é também sua primeira consumidora.

## Por que confiar neste dado

1. **Cada registro aponta a fonte oficial**: aba e linha da planilha do MEC, mais a página do PDF homologado (campo `fonte`).
2. **Verificação automática, caractere a caractere**: na BNCC 2018, 1.576 dos 1.580 textos batem com o PDF homologado, e os 4 restantes são divergências entre as próprias fontes oficiais, documentadas em `DECISOES.md` com a decisão tomada. No complemento de Computação, 141 de 141 batem com o anexo do Parecer CNE/CEB 2/2022.
3. **Completude provada**: a varredura de códigos no PDF homologado e no anexo de Computação encontra exatamente os códigos presentes no dataset. Nada falta, nada sobra.
4. **Extração reprodutível**: rode `pipeline/` e chegue aos mesmos arquivos. O CI faz isso a cada mudança e reprova qualquer divergência.

## O que tem aqui

| Pasta | Conteúdo |
|---|---|
| `dados/bncc-2018/` | O dataset em JSON: estrutura do sistema, 93 objetivos da EI (com alinhamentos entre faixas etárias), 1.304 habilidades do EF (com unidades temáticas, objetos de conhecimento, campos de atuação e práticas de linguagem), 183 habilidades do EM (com competências vinculadas), 20 marcos legais com URL oficial e 5 perfis de referência |
| `dados/computacao-2022/` | O complemento de Computação (Parecer CNE/CEB 2/2022): 141 aprendizagens (11 EI, 104 EF, 26 EM) com eixos, objetos de conhecimento e competências próprias, verificadas contra o anexo oficial |
| `fontes/` | Os documentos oficiais do MEC dos quais tudo é extraído, com checksums |
| `schema/` | JSON Schemas (draft 2020-12) que definem e validam o formato de cada arquivo de dados |
| `derivados/` | O mesmo dado em SQLite e CSV, gerados dos JSONs (para SQL e planilhas) |
| `pipeline/` | Scripts de extração, verificação e validação: qualquer pessoa reproduz o dataset a partir das fontes |
| `DECISOES.md` | Toda decisão de interpretação sobre inconsistências das fontes, documentada |
| `docs/` | Metodologia, modelo de dados, versionamento, instalação e mais (ver [Documentação](#documentação)) |

## Outros formatos

O mesmo dado, além do JSON:

```bash
# SQL: habilidades de LP do 6º ano com sua prática de linguagem
sqlite3 derivados/bncc.sqlite "
SELECT h.codigo, c.nome FROM habilidade_ef h
JOIN contexto_organizacao c ON c.id = h.pratica_linguagem
JOIN habilidade_ef_ano a ON a.codigo = h.codigo
WHERE h.componente = 'ef-comp-lp' AND a.ano = 6 LIMIT 5;"
```

E `derivados/csv/` traz uma planilha por entidade, pronta para Excel/Sheets. Os JSONs continuam sendo a fonte canônica; os formatos derivados são gerados e conferidos no CI. O formato dos dados é definido pelos JSON Schemas em `schema/`, validados a cada mudança.

## Reproduzir a extração

```bash
cd pipeline
python3 extrair.py             # planilhas oficiais → dados/bncc-2018/*.json
python3 extrair_ei.py          # PDF homologado → educacao-infantil.json
python3 extrair_computacao.py  # anexo do Parecer CNE/CEB 2/2022 → computacao.json
python3 verificar.py           # confere cada texto contra o PDF; grava a página
python3 verificar_computacao.py # confere Computação contra o anexo oficial
python3 validar_schema.py      # JSON Schemas, com autoteste negativo
python3 validar.py             # 29 checagens de contrato e completude (falha se algo divergir)
python3 derivar.py             # gera derivados/ (SQLite e CSV) a partir dos JSONs
```

É exatamente a sequência que o CI executa, terminando na comparação entre o dataset commitado e o reproduzido.

Dependências: Python 3.10+, `pdftotext` (poppler), `ghostscript` (normalização do anexo de Computação) e `jsonschema>=4.18` (apenas na validação de formato). Passo a passo completo, por sistema operacional e com problemas comuns: [docs/instalacao.md](docs/instalacao.md).

## Documentação

| Documento | Para quê |
|---|---|
| [docs/modelo-de-dados.md](docs/modelo-de-dados.md) | Como a BNCC está modelada: entidades, códigos, relações e o que o modelo não inventa |
| [docs/metodologia.md](docs/metodologia.md) | A cadeia de confiança: das fontes oficiais ao CI, com os números da verificação |
| [docs/versionamento.md](docs/versionamento.md) | Data-versions, vigência dos registros e o que consumidores podem assumir |
| [docs/instalacao.md](docs/instalacao.md) | Instalação e primeira execução (usar os dados ou reproduzir o pipeline) |
| [DECISOES.md](DECISOES.md) | Toda decisão de interpretação sobre as fontes, documentada |
| [docs/relatorio-validacao.md](docs/relatorio-validacao.md) | Snapshot do relatório de validação da versão atual |
| [CHANGELOG.md](CHANGELOG.md) | Histórico por categoria (normativa, correção, schema, editorial) |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Como propor correções (regra: fonte oficial no PR) |
| [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | Código de conduta da comunidade |
| [SECURITY.md](SECURITY.md) | Como reportar problema de segurança (erro de dado é issue normal) |
| [docs/guia-comunidade.md](docs/guia-comunidade.md) | Manual operacional de gestão da comunidade open source |
| [AGENTS.md](AGENTS.md) | Guia para agentes de IA (também: [llms.txt](llms.txt)) |

## Como contribuir

Correções de dados são bem-vindas, e a regra de ouro é uma só: **toda correção precisa citar a fonte oficial** (documento do MEC/CNE, com página ou localizador). O CI verifica automaticamente a reprodutibilidade de qualquer mudança. Comece por [CONTRIBUTING.md](CONTRIBUTING.md).

## Para agentes de IA

Leia `llms.txt` na raiz. Em resumo: consuma os JSONs de `dados/bncc-2018/`, use os códigos oficiais como chaves (`EF67LP08`, `EM13LGG103`, `EI02TS01`), nunca invente códigos ou textos de habilidade, e cite a fonte que acompanha cada registro.

## Licenças

- **Dados** (`dados/`): [CC BY 4.0](dados/LICENSE.md). Os textos normativos da BNCC são atos oficiais, não protegidos por direito autoral (art. 8º da Lei 9.610/98); a licença cobre a compilação, estruturação e curadoria.
- **Código** (`pipeline/`): [MIT](LICENSE).

O que é aberto aqui é irrevogavelmente aberto: ver [docs/divisao-aberto-comercial.md](docs/divisao-aberto-comercial.md).

Para citar o dataset em publicação, use o `CITATION.cff` na raiz (o botão *Cite this repository* na barra lateral gera a citação formatada).

## Roadmap

Já disponíveis como pré-release (0.1.x): pacote npm [@bncc/dados](https://www.npmjs.com/package/@bncc/dados), pacote PyPI [bncc](https://pypi.org/project/bncc/) e servidor MCP [@bncc/mcp](https://www.npmjs.com/package/@bncc/mcp), todos em [Uso rápido](#uso-rápido). As versões 1.0 saem com a release `dados-v1.0.0`, junto com as páginas por habilidade em [bncc.dev](https://bncc.dev).

## In English

**BNCC as open, verified data.** The BNCC is Brazil's national curriculum framework, mandatory across all schools. This repository publishes it as structured JSON: 1,721 learning objectives with competencies, organizational context and per-record provenance (official document and page), verified character by character against the documents published by the Ministry of Education, with a fully reproducible extraction pipeline checked on every commit.

Data is licensed [CC BY 4.0](dados/LICENSE.md), code [MIT](LICENSE). Install with `npm install @bncc/dados`, `pip install bncc`, or run `npx -y @bncc/mcp` for an MCP server that gives your AI agent access to the curriculum. Documentation is in Portuguese.
