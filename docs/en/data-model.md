[Português](../modelo-de-dados.md) · **English**

# Data model

How the dataset represents Brazil's National Common Curricular Base (BNCC). The executable definition is in the [JSON Schemas](../../schema/). This document explains the modeling decisions for the people who will use the data.

## The principle: structural honesty

The BNCC has three different taxonomies. The dataset models them as three distinct entities, not as one generic type with null fields:

| | Early Childhood Education (EI) | Elementary and Lower Secondary Education (EF) | Upper Secondary Education (EM) |
|---|---|---|---|
| Entity | `objetivo` (learning objective; 93) | `habilidade` (skill; 1,304) | `habilidade` (skill; 183) |
| Code | `EI02TS01` | `EF67LP08` | `EM13LGG103` |
| Organization | field of experience | thematic unit, or fields of action + language practice (LP), or axis + thematic unit (LI) | knowledge area |
| Time frame | age group (3 bands) | year or block of years | not divided by grade (curricula define it) |
| Link to competency | none | no formal link per skill | area skills: 1, embedded in the code; LP: 1 to n, from the official spreadsheet |

LP is Língua Portuguesa (Portuguese Language). LI is Língua Inglesa (English Language).

## Identifiers

- **Official code when one exists** (`EF67LP08`): it is the primary key of the learning objectives (EI objectives and EF/EM skills).
- **Minted ID when none exists** (`cg-04`, `em-area-lgg-ce-01`, `ef-comp-lp-prat-leitura`): a stable kebab-case slug, immutable once published. The generic slug pattern (`id_slug`) is in `schema/definicoes.json`; the prefix of each type (e.g. `co-obj-`, `perfil-`) is in the schema of the corresponding file.

## Anatomy of the codes

The codes can be decoded (reference function: `pipeline/codigos.py`):

```
EI 02 TS 01    stage · age group (01 babies, 02 very young children, 03 young children) · field of experience · sequence
EF 67 EF 01    stage · year 01-09 or block (15, 69, 12, 35, 67, 89) · component · sequence
EM 13 LGG 103  stage · not divided by grade · area (3 letters) · competency (1st digit) + sequence
EM 13 LP  02   stage · not divided by grade · Portuguese Language (2 letters) · simple sequence
```

Caveats: the `EF` segment is ambiguous. It can mean the stage, a field of experience or Physical Education (Educação Física); its position tells which one. The sequence numbers do not imply pedagogical order or completeness.

## Entities of the structural backbone (`estrutura.json`)

- `documento_curricular` (curricular document): the provenance root (`bncc-2018`). Complements and future state curricula enter as new documents linked by `derivado_de` (derived from), with no change to the model.
- `etapas` (stages), `modalidades` (modalities; EJA, Youth and Adult Education, as a cross-cutting modality, with segments), `areas_conhecimento` (knowledge areas, per stage), `componentes_curriculares` (curricular components), `recortes_temporais` (time frames).
- Asymmetries are data, not exceptions: EM components without skills of their own have `tem_aprendizagens_proprias: false` (has its own learning objectives: false); LP and Mathematics in EM carry `destaque_legal` (legal emphasis; Law No. 13.415/2017); English Language in EF has `presenca.anos: [6..9]` (presence: years 6 to 9).
- `competencias_gerais` (general competencies; 10) and `competencias_especificas` (specific competencies; 105: of an area or of a component; component competencies exist only in areas with more than one component).

## The learning objectives

Besides the fields in the table above, each record carries:

- `vigencia` (validity): `{status: vigente | alterado | revogado, desde, ate}` (status: in force, amended or revoked; since; until). A published record is never deleted. A code is never reused.
- `fonte` (source): document (`documento`), file (`arquivo`), provenance (`proveniencia`), locator (`localizador`: spreadsheet row in EF and EM, PDF page in EI) and page in the officially approved (homologated) PDF (`localizador_pdf`). It is the audit trail of each record.
- EF: `objetos_conhecimento` (knowledge objects) as a list of references (an entity of its own, N:N relation).
- EI: `alinhamento` (alignment) links objectives of the same aspect across the three age groups (the official relation on p. 26 of the document, which most datasets lose). Alignments with 2 objectives reflect empty cells in the official table.

## The Computing complement (`computacao-2022`)

This is the first curricular document beyond BNCC 2018, and it proves the multi-document design of the model. `computacao-2022` (`tipo: complemento`, `derivado_de: bncc-2018`) holds the standards for Computing in Basic Education (annex to CNE/CEB Opinion No. 2/2022, established by CNE/CEB Resolution No. 1/2022) in `dados/computacao-2022/computacao.json`. CNE/CEB is the Basic Education Chamber of the National Education Council (CNE).

**141 learning objectives** with the component `CO` in their codes, with an organization of their own in each stage (structural honesty, as in the core):

| | EI | EF | EM |
|---|---|---|---|
| Entity | `objetivo` (11, preschool only: `EI03CO01` to `EI03CO11`) | `habilidade` (104: years 1 to 9 + blocks `EF15`/`EF69`) | `habilidade` (26: `EM13CO01` to `EM13CO26`) |
| Organization | axis | axis + knowledge object (with a parent/sub hierarchy in the final years) | specific competency of the complement (7) |

- **Axes** (3): Computational Thinking (Pensamento Computacional), Digital World (Mundo Digital), Digital Culture (Cultura Digital) (`co-eixo-*`).
- **Knowledge objects** (`co-obj-*`): the field `pai` (parent; required, `null` when the object has no parent) captures the hierarchy of the tables for the final years (e.g. `co-obj-tipos-de-dados` → parent `co-obj-programacao`).
- **Competencies**: 7 general competencies of the complement (`computacao-cg-*`) and 7 specific EM competencies (`computacao-em-ce-*`), to which the EM skills are linked.
- **Continuous sequences**: unlike BNCC 2018, the Computing numbering has no gaps (a contract checked in CI).
- Verification: the 141 texts are checked character by character against the official annex (`verificar_computacao.py`). Interpretation decisions are in entries 9, 10 and 13 of `DECISOES.md` (in Portuguese).
- Not in this version of the module: grouping descriptors, explanations and official examples from the annex (future iteration).

## Legal milestones and profiles

Two reference vocabularies come with the curricular core:

- `marcos_legais` (legal milestones; `marcos-legais.json`, 20 records): the normative acts that ground the BNCC and basic education, from the 1988 Constitution to Law No. 14.945/2024. Each record has `id`, `tipo` (type: constitution, amendment, law, resolution, opinion), `titulo` (title), `ementa` (summary of the act), `url_oficial` (official URL, always on a gov.br domain, checked to be online) and `relaciona` (typed links to entities of the dataset; e.g. Law No. 13.415/2017 `fundamenta_destaque` (grounds the legal emphasis of) LP and Mathematics in EM). No full text in v1.0; legal provisions as data are a future evolution.
- `perfis` (profiles; `perfis.json`, 5 records): a vocabulary of the roles in the school ecosystem (teacher, student, school administrator, parent or guardian, coordinator), with synonyms. It is a naming reference for applications that use the data; it carries no authorization logic.

Provenance note: the CNE PDFs moved from the old portal.mec.gov.br of the Ministry of Education (MEC), now offline, to `www.gov.br/mec/pt-br/cne/pdf/`. The recorded URLs follow this collection and were checked document by document (number, date and summary).

## What the model does not invent

- A formal progression between EF skills: the BNCC does not define one. The dataset offers structural approximations (same knowledge object, same practice) and nothing more.
- A skill-to-competency link in EF: the official document does not establish it per skill.
- Knowledge objects with different names in different years are different entities. Equivalences will require future curation, in a separate layer.

Full rationale for the interpretation decisions: [DECISOES.md](../../DECISOES.md) (in Portuguese). An English summary is in [Interpretation decisions: summary](decisions-summary.md).

## Field reference

Every field of every data file, with type, whether it is required, its meaning, allowed values and a real example, is in the [data dictionary](data-dictionary.md).
