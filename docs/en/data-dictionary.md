[Português](../dicionario-de-dados.md) · **English**

# Data dictionary

This dictionary describes every field in the data files of bncc.dev, the open data version of Brazil's National Common Curricular Base (BNCC): the six data files in `dados/bncc-2018/`, the file in `dados/computacao-2022/` and the two verification reports (`verificacao.json`), described at the end. For each field it gives the type, whether it is required, its meaning and a real example.

- The JSON files in [`dados/`](../../dados/) are canonical. The SQLite database and the CSV files in [`derivados/`](../../derivados/) are generated from them.
- Types and required fields come from the [JSON Schemas](../../schema/) (draft 2020-12, format `schema-v1.1.0`).
- Field names are in Portuguese and are stable identifiers. Do not translate them in code that uses the data. This page explains them in English.
- The entities and the modeling decisions are explained in the [Data model](data-model.md). Decisions about inconsistencies in the official sources are in [DECISOES.md](../../DECISOES.md) (in Portuguese; English summary in [decisions-summary.md](decisions-summary.md)).

Terms: MEC is the Ministry of Education. CNE is the National Education Council (CNE/CP is its Full Council and CNE/CEB its Basic Education Chamber). EI is Early Childhood Education, EF is Elementary and Lower Secondary Education, EM is Upper Secondary Education. LP is Língua Portuguesa (Portuguese Language) and LI is Língua Inglesa (English Language). "Homologated PDF" is the officially approved (homologated) PDF of the BNCC.

## How to read the tables

- **Field**: full path from the root of the file. `[]` marks a list item. Example: `habilidades[].fonte.localizador_pdf` is the field `localizador_pdf` of the object `fonte` of each item of the list `habilidades`.
- **Type**: JSON type defined in the schema. In parentheses, the named type from `schema/definicoes.json` (e.g. `id_slug`). `enum` and `const` mean fixed values. "or `null` (nullable)" marks fields that accept `null`.
- **Required**: "yes" when the schema requires the field (`required` list); "no" when it may be missing. In lists with variants (`oneOf`), the condition is given in parentheses.
- **Example**: a real value copied from the data. Long texts are shortened with "…". Values are in Portuguese, as in the data.
- `fonte` (source) and `vigencia` (validity) appear in many collections. Their inner fields are described once, in [Shared structures](#shared-structures).
- Every object in the schemas uses `additionalProperties: false`: no record may have fields other than the ones listed here.
- Each file is a JSON object whose keys are the collections listed in the file's section. All collections are required.
- Pages: "p. 26" is the number printed on the page of the document. "página PDF 28" (PDF page 28) is the position of the page in the PDF file, counted from 1. In the homologated BNCC PDF, printed page 26 is PDF page 28.

## Shared structures

### Identifiers and texts

Types defined in `schema/definicoes.json` and used in all files.

- **`id_slug`**: string with the pattern `^[a-z0-9]+(-[a-z0-9]+)*$` (lowercase letters without accents, digits and hyphens). Identifier minted by the project for entities without an official code. It is stable and does not change once published. Example: `ef-comp-lp-prat-leitura`.
- **`documento_ref`**: string with the same pattern as `id_slug`. Reference to the `id` of an item of `documento_curricular` (curricular document, in `estrutura.json`). Values in the data: `bncc-2018` and `computacao-2022`.
- **`texto_normativo`** (normative text): string with at least 10 characters. Official statement, copied from the official document and checked against it. Never empty, never invented.
- **`documento`** (document; a field in almost every record, outside `fonte`): curricular document the record belongs to (`documento_ref`). It is `bncc-2018` in `estrutura.json`, `educacao-infantil.json`, `ensino-fundamental.json` and `ensino-medio.json`, and `computacao-2022` in `computacao.json`.

### Official codes

The field `codigo` (code) of the learning objectives holds the official code, which is the primary key of the record. Each kind of code has a pattern in the schema:

- `codigo_ei`: `^EI0[123](EO|CG|TS|EF|ET)[0-9]{2}$`. Example: `EI02TS01`.
- `codigo_ef`: `^EF(0[1-9]|15|69|12|35|67|89)(AR|CI|EF|ER|GE|HI|LI|LP|MA)[0-9]{2}$`. Example: `EF67LP08`.
- `codigo_em`: `^EM13((LGG|MAT|CNT|CHS)[0-9]{3}|LP[0-9]{2})$`. Examples: `EM13LGG103`, `EM13LP02`.
- `codigo_computacao_ei`: `^EI03CO[0-9]{2}$`. Example: `EI03CO01`.
- `codigo_computacao_ef`: `^EF(0[1-9]|15|69)CO[0-9]{2}$`. Example: `EF06CO02`.
- `codigo_computacao_em`: `^EM13CO[0-9]{2}$`. Example: `EM13CO07`.

How to read each part of a code (reference function: `pipeline/codigos.py`):

- **EI** (`EI02TS01`): `EI` + age group (`01` babies, `02` very young children, `03` young children) + field of experience (`EO` O eu, o outro e o nós; `CG` Corpo, gestos e movimentos; `TS` Traços, sons, cores e formas; `EF` Escuta, fala, pensamento e imaginação; `ET` Espaços, tempos, quantidades, relações e transformações) + 2-digit sequence.
- **EF** (`EF67LP08`): `EF` + year (`01` to `09`) or block of years (`15` = years 1 to 5, `69` = years 6 to 9, `12` = years 1 and 2, `35` = years 3 to 5, `67` = years 6 and 7, `89` = years 8 and 9) + curricular component (`AR` Arts, `CI` Science, `EF` Physical Education, `ER` Religious Education, `GE` Geography, `HI` History, `LI` English Language, `LP` Portuguese Language, `MA` Mathematics) + 2-digit sequence.
- **EM** (`EM13LGG103`): `EM` + `13` (not divided by grade) + knowledge area (`LGG` Linguagens e suas Tecnologias, `MAT` Matemática e suas Tecnologias, `CNT` Ciências da Natureza e suas Tecnologias, `CHS` Ciências Humanas e Sociais Aplicadas) + 3 digits: the first is the number of the area's specific competency, the other two are the sequence. Portuguese Language uses `EM13LP` + 2-digit sequence, with no competency digit.
- **Computing** (component `CO`): `EI03CO` + sequence (preschool only); `EF` + year (`01` to `09`) or block (`15`, `69`) + `CO` + sequence; `EM13CO` + sequence, with no competency digit.
- Caveats: the segment `EF` can mean the stage, a field of experience or Physical Education (Educação Física), and its position tells which one. The sequence numbers do not imply pedagogical order or completeness. A well-formed code that is not in the data does not exist in the BNCC.

### Stage codes

Values used in `etapas[].id`, in the `etapa` (stage) fields, in `modalidades[].transversal_a` and in `marcos_legais[].relaciona[].entidade`:

- `EI`: Early Childhood Education (Educação Infantil).
- `EF`: Elementary and Lower Secondary Education (Ensino Fundamental).
- `EM`: Upper Secondary Education (Ensino Médio).

### `fonte`

Source (provenance) of the record: official document and locators. It is the audit trail of each record. Only `documento` is required; the other subfields appear depending on the collection (table below).

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `fonte` | object | depends on the collection | Provenance object. Whether it is required is stated in the `fonte` row of each collection. | `{"documento": "bncc-2018", "arquivo": "BNCC_Ensino Fundamental.xlsx", …}` |
| `fonte.documento` | string (`documento_ref`) | yes | Curricular document the record comes from. | `"bncc-2018"` |
| `fonte.arquivo` | string | no | File name of the official source, archived in [`fontes/`](../../fontes/). Values in the data: `BNCC_Ensino Fundamental.xlsx` and `BNCC_Ensino_Medio.xlsx` (official MEC spreadsheets), `Base-Nacional-Comum-Curricular-BNCC.pdf` (homologated BNCC PDF) and `anexo-ao-parecer-cneceb-no-2-2022-bncc-computacao.pdf` (Computing annex). | `"BNCC_Ensino Fundamental.xlsx"` |
| `fonte.proveniencia` | string | no | How and when the source was obtained, or how the record was built. Free text. | `"exportada de downloadbncc.mec.gov.br em 23/06/2023"` |
| `fonte.localizador` | string | no | Where the record is in the material it was extracted from. Formats in the data: `aba <nome>, linha <n>` (sheet and row of the MEC spreadsheets; competencies and organization contexts give only the sheet); `página PDF <n>` (EI, extracted from the homologated PDF, and the 10 EM components without learning objectives of their own, named on PDF page 35); `<planilha> · linha <n>` (computacao-2022: support spreadsheet of the Pernambuco State Department of Education that provided the structure, no longer in the repository, see decision 13 in DECISOES.md). | `"aba Língua Portuguesa, linha 229"` |
| `fonte.localizador_pdf` | string | no | Page of the official document where the text of the record was checked. It is the position of the page in the PDF file, not the printed number. BNCC 2018: `Base-Nacional-Comum-Curricular-BNCC.pdf, página PDF <n>`. computacao-2022: `página PDF <n>`, in the annex named in `fonte.arquivo`. Present in every learning objective, in the 115 BNCC 2018 competencies and in the 10 EM components without learning objectives of their own. It never points to the "Estrutura" chapter of the PDF (pages 25 to 36), which only has illustrative examples. | `"Base-Nacional-Comum-Curricular-BNCC.pdf, página PDF 167"` |

Subfields of `fonte` filled in each collection:

| File and collection | Subfields filled |
|---|---|
| `estrutura.json`: `componentes_curriculares` (10 of 21 items) | `documento`, `arquivo`, `proveniencia`, `localizador`, `localizador_pdf` |
| `estrutura.json`: `competencias_gerais`, `competencias_especificas` | `documento`, `arquivo`, `proveniencia`, `localizador`, `localizador_pdf` |
| `educacao-infantil.json`: `objetivos` | `documento`, `arquivo`, `proveniencia`, `localizador`, `localizador_pdf` |
| `ensino-fundamental.json` and `ensino-medio.json`: `habilidades` | `documento`, `arquivo`, `proveniencia`, `localizador`, `localizador_pdf` |
| `ensino-fundamental.json` and `ensino-medio.json`: `contextos_organizacao` | `documento`, `arquivo`, `proveniencia`, `localizador` |
| `computacao.json`: `competencias` | `documento`, `arquivo`, `proveniencia` |
| `computacao.json`: `objetivos_ei`, `habilidades_ef`, `habilidades_em` | `documento`, `arquivo`, `proveniencia`, `localizador`, `localizador_pdf` |

### `vigencia`

Validity: the normative life cycle of the record. Present, and required, in every learning objective: EI learning objectives, EF and EM skills, and the three lists of Computing learning objectives. Project rules ([versioning.md](versioning.md)): a published record is never deleted and a code is never reused.

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `vigencia` | object | yes (in every learning objective) | Validity object of the record. | `{"status": "vigente", "desde": "dados-2026.07", "ate": null}` |
| `vigencia.status` | enum | yes | Normative status. `vigente`: in force. `alterado`: record amended by a normative change. `revogado`: revoked; the record stays in the dataset and `ate` is filled. Every record in this version is `vigente`. Use it to filter: applications should not suggest revoked learning objectives. | `"vigente"` |
| `vigencia.desde` | string (pattern `dados-AAAA.MM` or `dados-AAAA.MM.N`, that is, `dados-YYYY.MM[.N]`) | yes | Data-version (version of the dataset content) in which the record entered the dataset. It is not the date of the normative act: the Computing records, from a 2022 standard, also have `dados-2026.07`. A correction patch does not change the `desde` of records already in the dataset. | `"dados-2026.07"` |
| `vigencia.ate` | string (same pattern as `desde`) or `null` (nullable) | yes | End of validity. `null` while the record is in force. When filled, it is the data-version in which the record stopped being valid as it stands: the one of the revocation (`status` = `revogado`) or of the normative change (`status` = `alterado`); the text stays as in the last version in force. Every record in this version has `null`. | `null` |

## `dados/bncc-2018/estrutura.json`

The structural backbone of the dataset: curricular documents, stages, modalities, knowledge areas, curricular components, time frames, fields of experience, learning rights, and general and specific competencies.

### `documento_curricular`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `documento_curricular` | array (at least 1 item) | yes | Curricular documents the records come from. It is the provenance root: every `documento` field points to an `id` in this list. 2 items in the data. | `[{"id": "bncc-2018", …}, {"id": "computacao-2022", …}]` |
| `documento_curricular[].id` | string (`id_slug`) | yes | Identifier of the document. | `"computacao-2022"` |
| `documento_curricular[].nome` | string | yes | Name of the document. | `"Computação na Educação Básica (complemento à BNCC)"` |
| `documento_curricular[].tipo` | enum | yes | Type of document. `base_nacional`: the BNCC itself (`bncc-2018`). `complemento`: complement to the BNCC (`computacao-2022`). `curriculo_estadual`: state curriculum. `curriculo_municipal`: municipal curriculum. The last two have no records in this version; the data model plans future state curricula as new documents. | `"complemento"` |
| `documento_curricular[].esfera` | enum | yes | Level of government of the document: `federal`, `estadual` (state) or `municipal`. Both current documents are `federal`. | `"federal"` |
| `documento_curricular[].derivado_de` | string (`id_slug`) or `null` (nullable) | yes | `id` of the document this one derives from. `null` in the root document (`bncc-2018`). | `"bncc-2018"` |

### `etapas`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `etapas` | array | yes | Stages of basic education. 3 items in the data. | `[{"id": "EI", "nome": "Educação Infantil"}, …]` |
| `etapas[].id` | enum (`EI`, `EF`, `EM`) | yes | Stage code (see [Stage codes](#stage-codes)). | `"EF"` |
| `etapas[].nome` | string | yes | Name of the stage. | `"Ensino Fundamental"` |

### `modalidades`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `modalidades` | array | yes | Modalities of education that cut across stages. 1 item in the data: Youth and Adult Education (Educação de Jovens e Adultos, EJA). | `[{"id": "eja", …}]` |
| `modalidades[].id` | string (`id_slug`) | yes | Identifier of the modality. | `"eja"` |
| `modalidades[].nome` | string | yes | Name of the modality. | `"Educação de Jovens e Adultos"` |
| `modalidades[].transversal_a` | array of enum (`EI`, `EF`, `EM`) | yes | Stages the modality cuts across. | `["EF", "EM"]` |
| `modalidades[].segmentos` | array of object | yes | Segments of the modality. 3 in EJA. | `[{"id": "eja-1", "corresponde_a": "EF anos iniciais"}, …]` |
| `modalidades[].segmentos[].id` | string (`id_slug`) | yes | Identifier of the segment. | `"eja-2"` |
| `modalidades[].segmentos[].corresponde_a` | string | yes | Part of basic education the segment corresponds to. Free text, not a reference to an `id`. Values in the data: `"EF anos iniciais"` (EF early years), `"EF anos finais"` (EF final years), `"EM"`. | `"EF anos finais"` |

### `areas_conhecimento`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `areas_conhecimento` | array | yes | Knowledge areas, per stage. 9 items: 5 in EF and 4 in EM. EI has no areas: it is organized by fields of experience. | `[{"id": "ef-area-linguagens", …}, …]` |
| `areas_conhecimento[].id` | string (`id_slug`) | yes | Identifier of the area. In the data: `ef-area-` + name in EF; `em-area-` + area code used in skill codes (`lgg`, `mat`, `cnt`, `chs`) in EM. | `"em-area-lgg"` |
| `areas_conhecimento[].etapa` | enum (`EI`, `EF`, `EM`) | yes | Stage of the area. Only `EF` and `EM` appear in the data. | `"EM"` |
| `areas_conhecimento[].nome` | string | yes | Official name of the area. | `"Linguagens e suas Tecnologias"` |
| `areas_conhecimento[].documento` | string (`documento_ref`) | yes | Curricular document of the area. | `"bncc-2018"` |

### `componentes_curriculares`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `componentes_curriculares` | array | yes | Curricular components of EF and EM. 21 items: 9 in EF and 12 in EM. | `[{"id": "ef-comp-ar", …}, …]` |
| `componentes_curriculares[].id` | string (`id_slug`) | yes | Identifier of the component. In the data it starts with `ef-comp-` or `em-comp-`. | `"ef-comp-li"` |
| `componentes_curriculares[].etapa` | enum (`EF`, `EM`) | yes | Stage of the component. | `"EF"` |
| `componentes_curriculares[].nome` | string | yes | Name of the component. | `"Língua Inglesa"` |
| `componentes_curriculares[].sigla_codigo` | string or `null` (nullable) | no | Code of the component inside skill codes (e.g. `LP` in `EF67LP08` and in `EM13LP02`). `null` when the component has no code of its own in skill codes: every EM component except Portuguese Language. | `"LI"` |
| `componentes_curriculares[].area` | string (`id_slug`) | yes | `id` of the knowledge area (`areas_conhecimento[].id`) the component belongs to. | `"ef-area-linguagens"` |
| `componentes_curriculares[].tem_aprendizagens_proprias` | boolean | yes | Has its own learning objectives: `true` when the component has its own skills in the dataset. `false` for 10 EM components (Arts, Physical Education, English Language, Biology, Physics, Chemistry, History, Geography, Sociology and Philosophy): in EM, the skills of these components are defined per area (BNCC, PDF page 35). | `false` |
| `componentes_curriculares[].presenca` | object or `null` (nullable) | no | Presence: the EF years in which the component is present. Present in the 9 EF components: English Language with `[6, 7, 8, 9]` (BNCC, final years) and the other 8 with `[1, 2, 3, 4, 5, 6, 7, 8, 9]`. The field is absent from EM components, because EM has no grade seriation. | `{"anos": [6, 7, 8, 9]}` |
| `componentes_curriculares[].presenca.anos` | array of integer (1 to 9) | yes (inside `presenca`) | EF years (1 to 9) in which the component appears. | `[6, 7, 8, 9]` |
| `componentes_curriculares[].destaque_legal` | string | no | Legal emphasis: the legal act that gives the component special status. Present in EM Portuguese Language and Mathematics: Law No. 13.415/2017 makes the study of these components mandatory in all three years of EM (record `lei-13415-2017` in `marcos-legais.json`). | `"Lei nº 13.415/2017"` |
| `componentes_curriculares[].nota` | string | no | Project note on the component. Present only in `em-comp-mat`. | `"detalhamento coincide com a área (componente único)"` |
| `componentes_curriculares[].fonte` | object ([`fonte`](#fonte)) | no | Source. Present only in the 10 EM components without learning objectives of their own: PDF page 35 (printed 33), where the BNCC names the components of each EM area. | `{"documento": "bncc-2018", "arquivo": "Base-Nacional-Comum-Curricular-BNCC.pdf", "proveniencia": "BNCC completa homologada (600 p.), obtida em 09/07/2026", "localizador": "página PDF 35", "localizador_pdf": "Base-Nacional-Comum-Curricular-BNCC.pdf, página PDF 35"}` |

### `recortes_temporais`

Each item follows one of three variants, set by `tipo`: `grupo_etario` (age group, EI), `ano` (year, EF) or `sem_seriacao` (not divided by grade, EM).

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `recortes_temporais` | array | yes | Time frames of each stage. 13 items: 3 age groups (EI), 9 years (EF) and 1 time frame not divided by grade (EM). | `[{"id": "ei-grupo-01", …}, …]` |
| `recortes_temporais[].id` | string (`id_slug`) | yes | Identifier. In the data: `ei-grupo-01` to `ei-grupo-03`, `ef-ano-01` to `ef-ano-09` and `em-sem-seriacao`. The field `grupo_etario` of EI learning objectives points to the `ei-grupo-*` ids. | `"ei-grupo-02"` |
| `recortes_temporais[].etapa` | const (`EI`, `EF` or `EM`, depending on the variant) | yes | Stage of the time frame. | `"EI"` |
| `recortes_temporais[].tipo` | const (`grupo_etario`, `ano` or `sem_seriacao`, depending on the variant) | yes | Kind of time frame. `grupo_etario`: EI age group. `ano`: EF school year. `sem_seriacao`: EM does not divide skills by year; curricula define the progression. | `"grupo_etario"` |
| `recortes_temporais[].nome` | string | yes (if `tipo` = `grupo_etario`) | Name of the age group. Exists only in this variant. | `"Crianças bem pequenas"` |
| `recortes_temporais[].faixa` | string | yes (if `tipo` = `grupo_etario`) | Age band, in years (`a`, anos) and months (`m`, meses). Babies: from 0 to 1 year and 6 months. Very young children: from 1 year and 7 months to 3 years and 11 months. Young children: from 4 years to 5 years and 11 months (BNCC, PDF page 28). The separator between the limits is the character U+2013; the example shows it as a JSON escape. | `"1a7m\u20133a11m"` |
| `recortes_temporais[].numero` | integer (1 to 9) | yes (if `tipo` = `ano`) | Number of the EF year. | `6` |
| `recortes_temporais[].segmento` | enum | yes (if `tipo` = `ano`) | EF segment. `anos_iniciais`: early years, 1 to 5. `anos_finais`: final years, 6 to 9. | `"anos_finais"` |
| `recortes_temporais[].nota` | string | no (only in the `sem_seriacao` variant) | Note on the time frame. | `"habilidades sem seriação; progressão definida pelos currículos (BNCC p. 32, 34)"` |

### `campos_experiencias`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `campos_experiencias` | array | yes | The 5 EI fields of experience, which organize the learning objectives. | `[{"id": "ei-campo-eo", …}, …]` |
| `campos_experiencias[].id` | string (`id_slug`) | yes | Identifier: `ei-campo-` + the field's code in skill codes, in lowercase (`eo`, `cg`, `ts`, `ef`, `et`). | `"ei-campo-ts"` |
| `campos_experiencias[].nome` | string | yes | Official name of the field. | `"Traços, sons, cores e formas"` |
| `campos_experiencias[].documento` | string (`documento_ref`) | yes | Curricular document. | `"bncc-2018"` |

### `direitos_aprendizagem`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `direitos_aprendizagem` | array | yes | The 6 learning and development rights of EI defined in the BNCC (PDF page 40). No other record in the dataset points to these ids. | `[{"id": "ei-direito-conviver", …}, …]` |
| `direitos_aprendizagem[].id` | string (`id_slug`) | yes | Identifier: `ei-direito-` + name. | `"ei-direito-conhecer-se"` |
| `direitos_aprendizagem[].nome` | string | yes | Name of the right. | `"Conhecer-se"` |
| `direitos_aprendizagem[].documento` | string (`documento_ref`) | yes | Curricular document. | `"bncc-2018"` |

### `competencias_gerais`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `competencias_gerais` | array (exactly 10 items) | yes | The 10 general competencies of basic education. | `[{"id": "cg-01", …}, …]` |
| `competencias_gerais[].id` | string (`id_slug`) | yes | Identifier: `cg-` + 2-digit number. | `"cg-01"` |
| `competencias_gerais[].documento` | string (`documento_ref`) | yes | Curricular document. | `"bncc-2018"` |
| `competencias_gerais[].tipo` | const `geral` | yes | Kind of competency. Always `geral` (general). | `"geral"` |
| `competencias_gerais[].numero` | integer (1 to 10) | yes | Number of the competency in the BNCC. | `1` |
| `competencias_gerais[].texto` | string (`texto_normativo`) | yes | Official statement of the competency. | `"Valorizar e utilizar os conhecimentos historicamente construídos sobre o mundo físico, social, cultural e digital …"` |
| `competencias_gerais[].fonte` | object ([`fonte`](#fonte)) | yes | Source: sheet "Competências gerais" of the official EF spreadsheet. | `{"arquivo": "BNCC_Ensino Fundamental.xlsx", "localizador": "aba Competências gerais", …}` |

### `competencias_especificas`

Each item follows one of two variants, set by `tipo`: area competency or component competency.

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `competencias_especificas` | array | yes | Specific competencies of an area or of a component, in EF and EM. 105 items: 56 area competencies and 49 component competencies. EM skills point to the EM area competencies. | `[{"id": "ef-area-linguagens-ce-01", …}, …]` |
| `competencias_especificas[].id` | string (`id_slug`) | yes | Identifier: `id` of the area or component + `-ce-` + 2-digit number. | `"em-area-lgg-ce-01"` |
| `competencias_especificas[].documento` | string (`documento_ref`) | yes | Curricular document. | `"bncc-2018"` |
| `competencias_especificas[].tipo` | const (`especifica_de_area` or `especifica_de_componente`, depending on the variant) | yes | `especifica_de_area`: competency of a knowledge area. `especifica_de_componente`: competency of a curricular component; it exists only in areas with more than one component (in the data: Portuguese Language, Arts, Physical Education, English Language, Geography and History, all in EF). | `"especifica_de_area"` |
| `competencias_especificas[].area` | string (`id_slug`) | yes (if `tipo` = `especifica_de_area`) | `id` of the area (`areas_conhecimento[].id`). | `"em-area-lgg"` |
| `competencias_especificas[].componente` | string (`id_slug`) | yes (if `tipo` = `especifica_de_componente`) | `id` of the component (`componentes_curriculares[].id`). | `"ef-comp-lp"` |
| `competencias_especificas[].numero` | integer (at least 1) | yes | Number of the competency within the area or component. | `1` |
| `competencias_especificas[].texto` | string (`texto_normativo`) | yes | Official statement of the competency. | `"Compreender o funcionamento das diferentes linguagens e práticas culturais (artísticas, corporais e verbais) …"` |
| `competencias_especificas[].fonte` | object ([`fonte`](#fonte)) | yes | Source: competencies sheet of the official EF or EM spreadsheet. | `{"arquivo": "BNCC_Ensino_Medio.xlsx", "localizador": "aba Comp. de Linguagens e suas Tec", …}` |

## `dados/bncc-2018/educacao-infantil.json`

The EI learning objectives and the alignments that link objectives of the same aspect across the three age groups. EI is extracted from the homologated PDF, because no official spreadsheet is available.

### `objetivos`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `objetivos` | array (at least 1 item) | yes | EI learning objectives. 93 in the data. | `[{"codigo": "EI01CG01", …}, …]` |
| `objetivos[].codigo` | string (`codigo_ei`) | yes | Official code, primary key of the record (see [Official codes](#official-codes)). | `"EI02TS01"` |
| `objetivos[].documento` | string (`documento_ref`) | yes | Curricular document. | `"bncc-2018"` |
| `objetivos[].texto` | string (`texto_normativo`) | yes | Official text of the learning objective, checked against the homologated PDF. | `"Criar sons com materiais, objetos e instrumentos musicais, para acompanhar diversos ritmos de música."` |
| `objetivos[].campo_experiencias` | string (`id_slug`) | yes | `id` of the field of experience (`campos_experiencias[].id` in `estrutura.json`). Matches the field segment of the code. | `"ei-campo-ts"` |
| `objetivos[].grupo_etario` | string (`id_slug`) | yes | `id` of the age group (`recortes_temporais[].id` in `estrutura.json`). Matches the age group digits of the code. | `"ei-grupo-02"` |
| `objetivos[].alinhamento` | string (`id_slug`) | yes | `id` of the alignment (`alinhamentos[].id`) that links this objective to the objectives of the same aspect in the other age groups. | `"ei-align-ts-01"` |
| `objetivos[].vigencia` | object ([`vigencia`](#vigencia)) | yes | Validity of the record. | `{"status": "vigente", "desde": "dados-2026.07", "ate": null}` |
| `objetivos[].fonte` | object ([`fonte`](#fonte)) | yes | Source: page of the homologated PDF the text was extracted from (`localizador`) and page where it was checked (`localizador_pdf`). | `{"localizador": "página PDF 49", "localizador_pdf": "Base-Nacional-Comum-Curricular-BNCC.pdf, página PDF 49", …}` |

### `alinhamentos`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `alinhamentos` | array | yes | Alignments: the official horizontal progression, objectives of the same aspect across age groups (BNCC p. 26). The dataset pairs objectives by the sequence number of the code, a heuristic confirmed by a pedagogical review (decision 5 in DECISOES.md). 32 items. | `[{"id": "ei-align-cg-01", …}, …]` |
| `alinhamentos[].id` | string (`id_slug`) | yes | Identifier: `ei-align-` + field code + sequence number. | `"ei-align-ts-01"` |
| `alinhamentos[].campo_experiencias` | string (`id_slug`) | yes | `id` of the field of experience shared by the aligned objectives. | `"ei-campo-ts"` |
| `alinhamentos[].objetivos` | array of string (`codigo_ei`), 2 to 3 items | yes | Codes of the aligned objectives, one per age group. The 3 alignments with 2 items (`ei-align-eo-07`, `ei-align-et-07`, `ei-align-et-08`) reflect empty cells in the official table. | `["EI01TS01", "EI02TS01", "EI03TS01"]` |
| `alinhamentos[].nota` | string | no | Record of how the pairing was made and reviewed. | `"pareamento pela posição sequencial nn, confirmado em revisão pedagógica (07/2026)"` |

## `dados/bncc-2018/ensino-fundamental.json`

The EF skills and the organization contexts they refer to: thematic units, knowledge objects, fields of action, language practices and axes.

### `habilidades`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `habilidades` | array (at least 1 item) | yes | EF skills. 1,304 in the data. | `[{"codigo": "EF01LP01", …}, …]` |
| `habilidades[].codigo` | string (`codigo_ef`) | yes | Official code, primary key of the record (see [Official codes](#official-codes)). | `"EF67LP08"` |
| `habilidades[].documento` | string (`documento_ref`) | yes | Curricular document. | `"bncc-2018"` |
| `habilidades[].texto` | string (`texto_normativo`) | yes | Official text of the skill, checked against the homologated PDF. | `"Identificar os efeitos de sentido devidos à escolha de imagens estáticas, sequenciação ou sobreposição de imagens, …"` |
| `habilidades[].componente` | string (`id_slug`) | yes | `id` of the curricular component (`componentes_curriculares[].id` in `estrutura.json`). It is always the component decoded from the code. | `"ef-comp-lp"` |
| `habilidades[].anos` | array of integer (1 to 9), at least 1 item | yes | EF years the skill applies to, decoded from the code. A block becomes the list of its years: `EF67` gives `[6, 7]`, `EF15` gives `[1, 2, 3, 4, 5]`. | `[6, 7]` |
| `habilidades[].organizacao` | object | yes | How the skill is organized in the official table. Three variants, set by `tipo`. The schema requires `campo_pratica` for Portuguese Language (`ef-comp-lp`) and `eixo` for English Language (`ef-comp-li`). | `{"tipo": "campo_pratica", "campos_atuacao": ["ef-comp-lp-catu-campo-jornalistico-midiatico"], "pratica_linguagem": "ef-comp-lp-prat-leitura"}` |
| `habilidades[].organizacao.tipo` | const (`unidade_tematica`, `campo_pratica` or `eixo`, depending on the variant) | yes | `unidade_tematica`: organized by thematic unit (every component except LP and LI; 825 skills). `campo_pratica`: fields of action and language practice (Portuguese Language; 391). `eixo`: axis and thematic unit (English Language; 88). | `"campo_pratica"` |
| `habilidades[].organizacao.unidade_tematica` | string (`id_slug`) | yes (if `tipo` = `unidade_tematica` or `eixo`) | `id` of the thematic unit in `contextos_organizacao` (`tipo` = `ut`). | `"ef-comp-ma-ut-numeros"` |
| `habilidades[].organizacao.campos_atuacao` | array of string (`id_slug`), at least 1 item | yes (if `tipo` = `campo_pratica`) | `id`s of the fields of action in `contextos_organizacao` (`tipo` = `catu`). In the data, each skill has exactly 1. | `["ef-comp-lp-catu-campo-jornalistico-midiatico"]` |
| `habilidades[].organizacao.pratica_linguagem` | string (`id_slug`) | yes (if `tipo` = `campo_pratica`) | `id` of the language practice in `contextos_organizacao` (`tipo` = `prat`). | `"ef-comp-lp-prat-leitura"` |
| `habilidades[].organizacao.eixo` | string (`id_slug`) | yes (if `tipo` = `eixo`) | `id` of the axis in `contextos_organizacao` (`tipo` = `eixo`). | `"ef-comp-li-eixo-eixo-oralidade"` |
| `habilidades[].objetos_conhecimento` | array of string (`id_slug`) | yes | `id`s of the knowledge objects in `contextos_organizacao` (`tipo` = `oc`). N:N relation. Knowledge objects with different names in different years are different entities (decision 6 in DECISOES.md). The schema sets no minimum; in the data each skill has 1 to 6. | `["ef-comp-lp-oc-efeitos-de-sentido-exploracao-da-multissemiose"]` |
| `habilidades[].vigencia` | object ([`vigencia`](#vigencia)) | yes | Validity of the record. | `{"status": "vigente", "desde": "dados-2026.07", "ate": null}` |
| `habilidades[].fonte` | object ([`fonte`](#fonte)) | yes | Source: sheet and row of the official EF spreadsheet (`localizador`) and page of the homologated PDF where the text was checked (`localizador_pdf`). | `{"localizador": "aba Língua Portuguesa, linha 229", "localizador_pdf": "Base-Nacional-Comum-Curricular-BNCC.pdf, página PDF 167", …}` |

### `contextos_organizacao`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `contextos_organizacao` | array | yes | Organization contexts: the entities that organize the EF tables, pointed to by the skills. 873 items: 775 knowledge objects, 77 thematic units, 9 language practices, 7 fields of action and 5 axes. | `[{"id": "ef-comp-ar-oc-arte-e-tecnologia", …}, …]` |
| `contextos_organizacao[].id` | string (`id_slug`) | yes | Identifier: `id` of the component + `-` + `tipo` + `-` + name as a slug. | `"ef-comp-lp-prat-leitura"` |
| `contextos_organizacao[].tipo` | enum | yes | Kind of context. `ut`: thematic unit (unidade temática). `oc`: knowledge object (objeto de conhecimento). `catu`: field of action (campo de atuação, LP only). `prat`: language practice (prática de linguagem, LP only). `eixo`: axis (LI only). | `"prat"` |
| `contextos_organizacao[].nome` | string | yes | Name as it appears in the official spreadsheet. | `"Leitura"` |
| `contextos_organizacao[].componente` | string (`id_slug`) | yes | `id` of the component the context belongs to. | `"ef-comp-lp"` |
| `contextos_organizacao[].fonte` | object ([`fonte`](#fonte)) | yes | Source: sheet of the official EF spreadsheet, with no row. | `{"arquivo": "BNCC_Ensino Fundamental.xlsx", "localizador": "aba Língua Portuguesa", …}` |

## `dados/bncc-2018/ensino-medio.json`

The EM skills, not divided by grade, and the fields of social action of Portuguese Language.

### `habilidades`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `habilidades` | array (at least 1 item) | yes | EM skills. 183 in the data: 129 area skills and 54 Portuguese Language skills. | `[{"codigo": "EM13CHS101", …}, …]` |
| `habilidades[].codigo` | string (`codigo_em`) | yes | Official code, primary key of the record (see [Official codes](#official-codes)). | `"EM13LGG103"` |
| `habilidades[].documento` | string (`documento_ref`) | yes | Curricular document. | `"bncc-2018"` |
| `habilidades[].texto` | string (`texto_normativo`) | yes | Official text of the skill, checked against the homologated PDF. | `"Analisar o funcionamento das linguagens, para interpretar e produzir criticamente discursos em textos de diversas semioses (visuais, verbais, sonoras, gestuais)."` |
| `habilidades[].area` | string (`id_slug`) | yes | `id` of the knowledge area (`areas_conhecimento[].id` in `estrutura.json`). It is always the area decoded from the code, never the spreadsheet sheet (decision 1 in DECISOES.md). LP skills belong to `em-area-lgg`. | `"em-area-lgg"` |
| `habilidades[].componente` | string (`id_slug`) or `null` (nullable) | yes | `em-comp-lp` in `EM13LP` skills; `null` in area skills. The schema requires `em-comp-lp` when the code starts with `EM13LP`. | `null` |
| `habilidades[].competencias_especificas` | array of string (`id_slug`), at least 1 item | yes | `id`s of the area specific competencies (`competencias_especificas[].id` in `estrutura.json`). Area skills: exactly 1, decoded from the code (the schema limits it to 1 when `componente` is `null`). LP skills: 1 to n, from the official spreadsheet; 1 to 3 in the data (decision 7 in DECISOES.md). | `["em-area-lgg-ce-01"]` |
| `habilidades[].campos_atuacao_social` | array of string (`id_slug`), at least 1 item, or `null` (nullable) | yes | LP skills only: `id`s of the fields of social action in `contextos_organizacao`, from the column of the official spreadsheet. `null` in area skills (the schema requires `null` when `componente` is `null`). | `["em-comp-lp-catu-todos-os-campos-de-atuacao-social"]` |
| `habilidades[].seriacao` | `null` (const) | yes | Always `null`: EM is not divided by grade, and curricula define the progression (BNCC p. 32 and 34). | `null` |
| `habilidades[].vigencia` | object ([`vigencia`](#vigencia)) | yes | Validity of the record. | `{"status": "vigente", "desde": "dados-2026.07", "ate": null}` |
| `habilidades[].fonte` | object ([`fonte`](#fonte)) | yes | Source: sheet and row of the official EM spreadsheet (`localizador`) and page of the homologated PDF where the text was checked (`localizador_pdf`). | `{"localizador": "aba 'Hab. de Linguagens e suas Tecn', linha 6", "localizador_pdf": "Base-Nacional-Comum-Curricular-BNCC.pdf, página PDF 493", …}` |

### `contextos_organizacao`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `contextos_organizacao` | array | yes | Fields of social action of EM Portuguese Language, pointed to by `habilidades[].campos_atuacao_social`. 6 items. | `[{"id": "em-comp-lp-catu-campo-artistico-literario", …}, …]` |
| `contextos_organizacao[].id` | string (`id_slug`) | yes | Identifier: `em-comp-lp-catu-` + name as a slug. | `"em-comp-lp-catu-campo-artistico-literario"` |
| `contextos_organizacao[].tipo` | const `catu` | yes | Always `catu` (field of action). | `"catu"` |
| `contextos_organizacao[].nome` | string | yes | Name as it appears in the official spreadsheet. | `"Campo artístico-literário"` |
| `contextos_organizacao[].componente` | const `em-comp-lp` | yes | Always `em-comp-lp` (EM Portuguese Language). | `"em-comp-lp"` |
| `contextos_organizacao[].fonte` | object ([`fonte`](#fonte)) | yes | Source: sheet "Hab. de Língua Portuguesa" of the official EM spreadsheet, with no row. | `{"arquivo": "BNCC_Ensino_Medio.xlsx", "localizador": "aba Hab. de Língua Portuguesa", …}` |

## `dados/bncc-2018/marcos-legais.json`

Legal milestones: references to the normative acts that ground the BNCC and basic education, with identification, summary, official link and links to entities of the dataset. The full text of the acts is not included.

### `marcos_legais`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `marcos_legais` | array (at least 15 items) | yes | Normative acts. 20 in the data. | `[{"id": "constituicao-1988", …}, …]` |
| `marcos_legais[].id` | string (`id_slug`) | yes | Identifier. In the data: kind of act, number and year (e.g. `lei-9394-1996`, `resolucao-cne-cp-2-2017`). | `"lei-13415-2017"` |
| `marcos_legais[].tipo` | enum | yes | Kind of act. `constituicao`: Federal Constitution. `emenda_constitucional`: constitutional amendment. `lei`: law. `resolucao`: resolution (in the data, all from the CNE). `parecer`: opinion (in the data, all from the CNE). | `"lei"` |
| `marcos_legais[].titulo` | string (at least 10 characters) | yes | Official title of the act, with number and date. | `"Lei nº 13.415, de 16 de fevereiro de 2017"` |
| `marcos_legais[].ementa` | string (at least 20 characters) or `null` (nullable) | yes | Official summary (ementa) of the act, transcribed from the official publication (Planalto for laws and the amendment, CNE for resolutions), checked on 15/10/2026. `null` for the Constitution, which has no summary. For the three CNE opinions, which have no summary either, it gives the subject of the opinion. Project commentary goes in `nota`. | `"Dispõe sobre o Estatuto da Criança e do Adolescente e dá outras providências."` |
| `marcos_legais[].url_oficial` | string (pattern `^https://[a-z0-9.-]+\.gov\.br/`) | yes | Official link to the act, always https on a gov.br domain. | `"https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2017/lei/l13415.htm"` |
| `marcos_legais[].nota` | string | no | Project commentary: what the act means for basic education and for this dataset (relevant articles and goals, approval, nicknames such as "LDB"). Never normative text. Present in 11 records. | `"As metas 2, 3 e 7 e suas estratégias preveem a base nacional comum curricular."` |
| `marcos_legais[].relaciona` | array of object | yes | Typed links between the act and entities of the dataset. It can be empty: `lei-8069-1990` and `lei-13146-2015` have no links. 28 links in total. | `[{"entidade": "EM", "natureza": "altera"}, …]` |
| `marcos_legais[].relaciona[].entidade` | string (`id_slug`) or enum (`EI`, `EF`, `EM`) | yes | Linked entity: a stage code or the `id` of an entity in `estrutura.json` (curricular document, modality, knowledge area, curricular component or specific competency). Values in the data: `bncc-2018`, `EI`, `EF`, `EM`, `eja`, `em-comp-lp`, `em-comp-mat`. | `"em-comp-lp"` |
| `marcos_legais[].relaciona[].natureza` | enum | yes | Nature of the link. Values in the list below. | `"fundamenta_destaque"` |

Values of `relaciona[].natureza`, with examples from the data:

- `fundamenta`: the act is a legal basis of the entity. E.g. the 1988 Constitution and Law No. 9.394/1996 (LDB, the national education law) for `bncc-2018`; Constitutional Amendment No. 59/2009 for `EI`, `EF` and `EM`.
- `fundamenta_destaque`: the act grounds the `destaque_legal` (legal emphasis) of the component. E.g. Law No. 13.415/2017 for `em-comp-lp` and `em-comp-mat`.
- `institui`: the act establishes the entity. E.g. CNE/CP Resolutions No. 2/2017 and No. 4/2018 for `bncc-2018`.
- `abrange`: the entity is within the scope of the act. E.g. CNE/CP Resolution No. 2/2017 for `EI` and `EF`; CNE/CP Resolution No. 4/2018 for `EM`.
- `altera`: the act changes the rules of the entity. E.g. Laws No. 13.415/2017 and No. 14.945/2024 for `EM`.
- `diretrizes`: the act sets curricular guidelines for the entity. E.g. CNE/CEB Resolution No. 5/2009 (National Curricular Guidelines for Early Childhood Education) for `EI`.
- `complementa`: the act complements the entity. E.g. CNE/CEB Opinion No. 2/2022 and CNE/CEB Resolution No. 1/2022 (Computing) for `bncc-2018`.

## `dados/bncc-2018/perfis.json`

Profiles: a reference vocabulary of the roles in the school ecosystem, for applications that use the data. It carries no authorization logic.

### `perfis`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `perfis` | array (at least 5 items) | yes | Reference roles. 5 in the data: teacher, student, school administrator, parent or guardian, and coordinator. | `[{"id": "perfil-professor", …}, …]` |
| `perfis[].id` | string (`id_slug`, starting with `perfil-`) | yes | Identifier of the role. | `"perfil-professor"` |
| `perfis[].nome` | string (at least 3 characters) | yes | Name of the role. | `"Professor"` |
| `perfis[].descricao` | string (at least 20 characters) | yes | Definition of the role. | `"Docente responsável por planejar, conduzir e avaliar o ensino dos componentes curriculares e das experiências de aprendizagem."` |
| `perfis[].sinonimos` | array of string (at least 3 characters each) | yes | Synonyms: other names used for the same role. | `["docente", "educador"]` |

## `dados/computacao-2022/computacao.json`

The Computing complement to the BNCC (annex to CNE/CEB Opinion No. 2/2022, established by CNE/CEB Resolution No. 1/2022): axes, knowledge objects, competencies and 141 learning objectives (11 EI learning objectives, 104 EF skills and 26 EM skills). The texts are checked against the official annex; the structure comes from the map `fontes/computacao-estrutura.json` (decisions 10 and 13 in DECISOES.md).

Local types, defined in `$defs` of `schema/computacao.schema.json`:

- `documento`: const `computacao-2022`. Every `documento` field in this file has this value.
- `eixo_ref`: enum with the 3 axis ids: `co-eixo-pensamento-computacional`, `co-eixo-mundo-digital`, `co-eixo-cultura-digital`.
- `objeto_ref`: string with the pattern `^co-obj-[a-z0-9]+(-[a-z0-9]+)*$`.

### `eixos`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `eixos` | array (exactly 3 items) | yes | The 3 axes of the complement: Computational Thinking (Pensamento Computacional), Digital World (Mundo Digital) and Digital Culture (Cultura Digital). | `[{"id": "co-eixo-pensamento-computacional", …}, …]` |
| `eixos[].id` | enum (`eixo_ref`) | yes | Identifier of the axis. | `"co-eixo-mundo-digital"` |
| `eixos[].documento` | const `computacao-2022` | yes | Curricular document. | `"computacao-2022"` |
| `eixos[].nome` | string (at least 3 characters) | yes | Official name of the axis. | `"Mundo Digital"` |

### `objetos_conhecimento`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `objetos_conhecimento` | array (at least 1 item) | yes | Knowledge objects of the Computing EF skills. 59 items, 30 of which have a `pai` (parent). 5 objects serve only as parents and are not pointed to directly by any skill. | `[{"id": "co-obj-algoritmos", …}, …]` |
| `objetos_conhecimento[].id` | string (`objeto_ref`) | yes | Identifier: `co-obj-` + name as a slug. | `"co-obj-tipos-de-dados"` |
| `objetos_conhecimento[].documento` | const `computacao-2022` | yes | Curricular document. | `"computacao-2022"` |
| `objetos_conhecimento[].nome` | string (at least 3 characters) | yes | Name as it appears in the annex. Two names end in "(cont.)", and their ids end in `-cont`. | `"Tipos de dados"` |
| `objetos_conhecimento[].pai` | string (`objeto_ref`) or `null` (nullable) | yes | `id` of the parent object, in the hierarchy of the tables for the final years. `null` when the object has no parent. | `"co-obj-programacao"` |

### `competencias`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `competencias` | array (at least 1 item) | yes | Competencies of the complement. 14 items: 7 general and 7 specific to EM. | `[{"id": "computacao-cg-01", …}, …]` |
| `competencias[].id` | string (`id_slug`) | yes | Identifier. In the data: `computacao-cg-` + number (general) or `computacao-em-ce-` + number (EM specific), with 2 digits. | `"computacao-em-ce-01"` |
| `competencias[].documento` | const `computacao-2022` | yes | Curricular document. | `"computacao-2022"` |
| `competencias[].tipo` | enum | yes | `geral_computacao`: general competency of the complement. `especifica_em_computacao`: specific Computing competency in EM; the EM skills point to these. | `"especifica_em_computacao"` |
| `competencias[].numero` | integer (at least 1) | yes | Number of the competency within its kind (1 to 7 in each kind, in the data). | `1` |
| `competencias[].texto` | string (`texto_normativo`) | yes | Official statement of the competency, checked against the annex. | `"Compreender as possibilidades e os limites da Computação para resolver problemas, …"` |
| `competencias[].fonte` | object ([`fonte`](#fonte)) | yes | Source: only `documento`, `arquivo` (the annex) and `proveniencia`. | `{"arquivo": "anexo-ao-parecer-cneceb-no-2-2022-bncc-computacao.pdf", "proveniencia": "competências específicas do EM (cabeçalho da planilha de EM, verificadas contra o anexo)", …}` |

### `objetivos_ei`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `objetivos_ei` | array (at least 1 item) | yes | Computing learning objectives in EI. The annex defines them for preschool only. 11 in the data. | `[{"codigo": "EI03CO01", …}, …]` |
| `objetivos_ei[].codigo` | string (`codigo_computacao_ei`) | yes | Official code, primary key of the record. | `"EI03CO01"` |
| `objetivos_ei[].documento` | const `computacao-2022` | yes | Curricular document. | `"computacao-2022"` |
| `objetivos_ei[].texto` | string (`texto_normativo`) | yes | Official text of the learning objective, checked against the annex. | `"Reconhecer padrão de repetição em sequência de sons, movimentos, desenhos."` |
| `objetivos_ei[].eixo` | enum (`eixo_ref`) | yes | `id` of the axis (`eixos[].id`). | `"co-eixo-pensamento-computacional"` |
| `objetivos_ei[].grupo_etario` | const `ei-grupo-03` | yes | Always `ei-grupo-03` (young children), an `id` of `recortes_temporais` in `estrutura.json`. | `"ei-grupo-03"` |
| `objetivos_ei[].vigencia` | object ([`vigencia`](#vigencia)) | yes | Validity of the record. | `{"status": "vigente", "desde": "dados-2026.07", "ate": null}` |
| `objetivos_ei[].fonte` | object ([`fonte`](#fonte)) | yes | Source: `arquivo` is the official annex; `localizador` points to the Pernambuco support spreadsheet and the row the structure came from; `localizador_pdf` is the page of the annex. | `{"localizador": "COMPUTAÇÃO - EDUCAÇÃO INFANTIL .xlsx · linha 4", "localizador_pdf": "página PDF 6", …}` |

### `habilidades_ef`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `habilidades_ef` | array (at least 1 item) | yes | Computing skills in EF: years 1 to 9 and the blocks `EF15` and `EF69`. 104 in the data. | `[{"codigo": "EF01CO01", …}, …]` |
| `habilidades_ef[].codigo` | string (`codigo_computacao_ef`) | yes | Official code, primary key of the record. | `"EF15CO01"` |
| `habilidades_ef[].documento` | const `computacao-2022` | yes | Curricular document. | `"computacao-2022"` |
| `habilidades_ef[].texto` | string (`texto_normativo`) | yes | Official text of the skill, checked against the annex. Some texts repeat under different codes, as in the annex (e.g. `EF06CO02` and `EF69CO02`). | `"Identificar as principais formas de organizar e representar a informação de maneira estruturada …"` |
| `habilidades_ef[].eixo` | enum (`eixo_ref`) | yes | `id` of the axis (`eixos[].id`). | `"co-eixo-pensamento-computacional"` |
| `habilidades_ef[].objetos_conhecimento` | array of string (`objeto_ref`), at least 1 item | yes | `id`s of the knowledge objects (`objetos_conhecimento[].id`). Always 1 item in the data. | `["co-obj-organizacao-e-representacao-da-informacao"]` |
| `habilidades_ef[].anos` | array of integer (1 to 9), at least 1 item | yes | EF years decoded from the code. Blocks: `EF15` = years 1 to 5; `EF69` = years 6 to 9. | `[1, 2, 3, 4, 5]` |
| `habilidades_ef[].vigencia` | object ([`vigencia`](#vigencia)) | yes | Validity of the record. | `{"status": "vigente", "desde": "dados-2026.07", "ate": null}` |
| `habilidades_ef[].fonte` | object ([`fonte`](#fonte)) | yes | Source, as in `objetivos_ei`. For `EF05CO11`, `localizador` records the form printed in the annex, `(EF05CO011)` (decision 9 in DECISOES.md). | `{"localizador": "1º ao 5º ANO - HABILIDADES- BNCC - Computação.xlsx · linha 61", "localizador_pdf": "página PDF 38", …}` |

### `habilidades_em`

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `habilidades_em` | array (at least 1 item) | yes | Computing skills in EM. 26 in the data. | `[{"codigo": "EM13CO01", …}, …]` |
| `habilidades_em[].codigo` | string (`codigo_computacao_em`) | yes | Official code, primary key of the record. | `"EM13CO01"` |
| `habilidades_em[].documento` | const `computacao-2022` | yes | Curricular document. | `"computacao-2022"` |
| `habilidades_em[].texto` | string (`texto_normativo`) | yes | Official text of the skill, checked against the annex. | `"Explorar e construir a solução de problemas por meio da reutilização de partes de soluções existentes."` |
| `habilidades_em[].competencia` | string (pattern `^computacao-em-ce-[0-9]{2}$`) | yes | `id` of the EM specific competency (`competencias[].id` with `tipo` = `especifica_em_computacao`). Unlike BNCC 2018 area skills, the code does not carry the competency. | `"computacao-em-ce-01"` |
| `habilidades_em[].vigencia` | object ([`vigencia`](#vigencia)) | yes | Validity of the record. | `{"status": "vigente", "desde": "dados-2026.07", "ate": null}` |
| `habilidades_em[].fonte` | object ([`fonte`](#fonte)) | yes | Source, as in `objetivos_ei`. | `{"localizador": "COMPUTAÇÃO - ENSINO MÉDIO.xlsx · linha 5", "localizador_pdf": "página PDF 66", …}` |

## Verification reports (`verificacao.json`)

`dados/bncc-2018/verificacao.json` (1,695 entries: 1,580 learning objectives and 115 competencies) and `dados/computacao-2022/verificacao.json` (141 entries) record the result of checking each text against the official document. They are generated by `pipeline/verificar.py` and `pipeline/verificar_computacao.py` on every pipeline run and have no JSON Schema. Each file is an object whose keys are the codes of the learning objectives or, in BNCC 2018, the `id`s of the competencies (`cg-01`, `ef-comp-lp-ce-04`).

| Field | Type | Present | Description | Example |
|---|---|---|---|---|
| `<codigo>.status` | string | always | Result of the check. Values possible in the code: `ok`, `ok_hifenizacao` (Computing only), `requer_conferencia_visual`, `divergente`, `nao_encontrado`. In the current data, every entry is `ok`. | `"ok"` |
| `<codigo>.pagina_pdf` | integer | when found | PDF page where the text was checked. | `101` |
| `<codigo>.arquivo_pdf` | string | always | File of the official document used in the check. | `"Base-Nacional-Comum-Curricular-BNCC.pdf"` |
| `<codigo>.nota` | string | in 4 BNCC 2018 entries | Note from the check, such as text that spans pages or a recorded visual check. | `"texto atravessa páginas"` |

## Open items

None. The three open items of the first version of this dictionary (`fonte.url_oficial` unused, `presenca` null without a defined meaning and `vigencia.ate` without a format) were resolved in `dados-2026.08` / `schema-v1.1.0` (decision 14 in DECISOES.md).
