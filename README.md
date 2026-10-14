# [bncc.dev](https://bncc.dev) · dados abertos da BNCC

**Português** · [English](README.en.md)

[![Validação](https://github.com/bncc-dev/bncc-dados/actions/workflows/validacao.yml/badge.svg)](https://github.com/bncc-dev/bncc-dados/actions/workflows/validacao.yml)
[![Dados: CC BY 4.0](https://img.shields.io/badge/dados-CC%20BY%204.0-lightgrey.svg)](dados/LICENSE.md)
[![Código: MIT](https://img.shields.io/badge/c%C3%B3digo-MIT-green.svg)](LICENSE)
[![Status: estável](https://img.shields.io/badge/status-est%C3%A1vel-brightgreen.svg)](CHANGELOG.md)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21625233.svg)](https://doi.org/10.5281/zenodo.21625233)

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

**Status: estável.** Primeira release: conteúdo `dados-2026.07`, formato `schema-v1.0.0`. Dados completos, validados e revisados pedagogicamente. Os identificadores e o formato passam a valer sob as garantias de [versionamento](docs/versionamento.md): mudança que quebre consumidores exige nova major do schema.

Mantido pela [Profy](https://profy.com.br), que é também sua primeira consumidora.

## Por que confiar neste dado

1. **Cada aprendizagem aponta a fonte oficial** (campo `fonte`): aba e linha da planilha do MEC no EF e no EM, página do PDF na EI e página do anexo do Parecer CNE/CEB 2/2022 em Computação, sempre com a página do documento oficial em que o texto foi conferido (`localizador_pdf`).
2. **Verificação automática, caractere a caractere**: na BNCC 2018, os 1.580 textos batem com o PDF homologado. Onde as próprias fontes oficiais divergem, a decisão tomada está documentada em `DECISOES.md`. No complemento de Computação, 141 de 141 batem com o anexo do Parecer CNE/CEB 2/2022.
3. **Completude provada**: a varredura de códigos no PDF homologado e no anexo de Computação encontra exatamente os códigos presentes no dataset. Nada falta, nada sobra.
4. **Extração reprodutível**: rode `pipeline/` e chegue aos mesmos arquivos. O CI faz isso a cada mudança e reprova qualquer divergência.

## O que tem aqui

| Pasta | Conteúdo |
|---|---|
| `dados/bncc-2018/` | O dataset em JSON: estrutura do sistema, 93 objetivos da EI (com alinhamentos entre faixas etárias), 1.304 habilidades do EF (com unidades temáticas, objetos de conhecimento, campos de atuação e práticas de linguagem), 183 habilidades do EM (com competências vinculadas), 20 marcos legais com URL oficial e 5 perfis de referência |
| `dados/computacao-2022/` | O complemento de Computação (Parecer CNE/CEB 2/2022): 141 aprendizagens (11 EI, 104 EF, 26 EM) com eixos, objetos de conhecimento e competências próprias, verificadas contra o anexo oficial |
| `fontes/` | Os documentos oficiais do MEC e do CNE dos quais tudo é extraído, com checksums, e o mapa de estrutura do complemento de Computação |
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

## Formas de acesso

| Mecanismo | Formato | Onde |
|---|---|---|
| Arquivos canônicos | JSON | [`dados/`](dados/) neste repositório |
| Arquivos derivados | SQLite, dump SQL, CSV | [`derivados/`](derivados/) |
| Releases arquivadas | ZIP do repositório, SQLite e CSV | [Zenodo, DOI 10.5281/zenodo.21625233](https://doi.org/10.5281/zenodo.21625233) |
| Pacote npm | JSON embutido, API em TypeScript | [@bncc/dados](https://www.npmjs.com/package/@bncc/dados) |
| Pacote PyPI | JSON embutido, API em Python | [bncc](https://pypi.org/project/bncc/) |
| Servidor MCP | ferramentas MCP sobre o JSON | local: `npx -y @bncc/mcp`; hospedado: `https://mcp.bncc.dev/mcp` |
| API REST | JSON, OpenAPI 3.1 | [api.bncc.dev](https://api.bncc.dev/v1/openapi.json), gratuita, sem chave |
| Site | HTML, Markdown e CSV por página | [bncc.dev](https://bncc.dev) |

Todos servem o mesmo dado. Os arquivos deste repositório e do Zenodo são o dataset completo; pacotes, servidor MCP, API e site são conveniências construídas sobre ele. O código da API e o do site são privados, e nenhum dos dois é necessário para usar os dados.

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
| [docs/dicionario-de-dados.md](docs/dicionario-de-dados.md) | Cada campo de cada arquivo: tipo, obrigatoriedade, significado, valores permitidos e exemplo real |
| [docs/metodologia.md](docs/metodologia.md) | A cadeia de confiança: das fontes oficiais ao CI, com os números da verificação |
| [docs/versionamento.md](docs/versionamento.md) | Data-versions, vigência dos registros e o que consumidores podem assumir |
| [docs/instalacao.md](docs/instalacao.md) | Instalação e primeira execução (usar os dados ou reproduzir o pipeline) |
| [DECISOES.md](DECISOES.md) | Toda decisão de interpretação sobre as fontes, documentada |
| [docs/relatorio-validacao.md](docs/relatorio-validacao.md) | Snapshot do relatório de validação da versão atual |
| [CHANGELOG.md](CHANGELOG.md) | Histórico por categoria (normativa, correção, schema, editorial) |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Como propor correções (regra: fonte oficial no PR) |
| [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | Código de conduta da comunidade |
| [SECURITY.md](SECURITY.md) | Como reportar problema de segurança (erro de dado é issue normal) |
| [docs/politica-de-conteudo.md](docs/politica-de-conteudo.md) | O que o dataset distribui, como erros e conteúdo indevido são identificados e corrigidos, e em que prazo |
| [AGENTS.md](AGENTS.md) | Guia para agentes de IA (também: [llms.txt](llms.txt)) |

## Como contribuir

Correções de dados são bem-vindas, e a regra de ouro é uma só: **toda correção precisa citar a fonte oficial** (documento do MEC/CNE, com página ou localizador). O CI verifica automaticamente a reprodutibilidade de qualquer mudança. Comece por [CONTRIBUTING.md](CONTRIBUTING.md).

## Para agentes de IA

Leia `llms.txt` na raiz. Em resumo: consuma os JSONs de `dados/bncc-2018/`, use os códigos oficiais como chaves (`EF67LP08`, `EM13LGG103`, `EI02TS01`), nunca invente códigos ou textos de habilidade, e cite a fonte que acompanha cada registro.

## Dependências e independência de plataforma

Nenhuma parte do dataset depende de software fechado ou proprietário.

- **Para usar os dados:** nada além de um leitor de JSON, CSV ou SQLite. Os formatos são abertos e não exigem biblioteca, serviço ou conta.
- **Para reproduzir a extração:** Python 3.10+ (só a biblioteca padrão), `pdftotext` do poppler (GPL), Ghostscript (AGPL) e `jsonschema` (MIT, em [`requirements.txt`](requirements.txt)). Todas as licenças são aprovadas pela OSI.
- **Hospedagem:** o GitHub hospeda o repositório, e cada release também fica arquivada no Zenodo com DOI. Qualquer clone tem tudo o que é preciso para reproduzir o dataset.
- **Pacotes e MCP:** os pacotes npm e PyPI trazem os dados embutidos e funcionam sem internet. O servidor MCP hospedado em mcp.bncc.dev roda na Cloudflare, mas é opcional: `npx -y @bncc/mcp` roda o mesmo servidor na sua máquina.

## Quem mantém

O projeto é mantido pela [Profy Tecnologias Educacionais Ltda](https://profy.com.br) (CNPJ 53.669.787/0001-45, Brasília, Brasil), titular dos direitos sobre a compilação, a estrutura, os identificadores e o código. Responsável técnico: Marcos Roberto Martins de Oliveira. Contato: contato@bncc.dev. Mais em [bncc.dev/sobre](https://bncc.dev/sobre/).

## Licenças

- **Dados** (`dados/`): [CC BY 4.0](dados/LICENSE.md). Os textos normativos da BNCC são atos oficiais, não protegidos por direito autoral (art. 8º, IV, da Lei 9.610/98). A licença cobre a compilação, a estruturação e a curadoria, cujos direitos pertencem à Profy.
- **Código** (`pipeline/`): [MIT](LICENSE).

O que é aberto aqui é irrevogavelmente aberto: ver [docs/divisao-aberto-comercial.md](docs/divisao-aberto-comercial.md).

Para citar o dataset em publicação, use o `CITATION.cff` na raiz (o botão *Cite this repository* na barra lateral gera a citação formatada).

## Pacotes e site

Construídos sobre este dataset e publicados em versões 0.x: o pacote npm [@bncc/dados](https://www.npmjs.com/package/@bncc/dados), o pacote PyPI [bncc](https://pypi.org/project/bncc/) e o servidor MCP [@bncc/mcp](https://www.npmjs.com/package/@bncc/mcp), com código em [bncc-pacotes](https://github.com/bncc-dev/bncc-pacotes). Cada aprendizagem tem uma página permanente em [bncc.dev](https://bncc.dev).

## In English

The full English documentation starts at [README.en.md](README.en.md): what the dataset is, how it is made and verified, the data model, licenses, dependencies, content policy and how to contribute.
