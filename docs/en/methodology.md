[Português](../metodologia.md) · **English**

# Methodology · the chain of trust

How the data goes from the official documents to the repository, and why each link in the chain can be trusted.

## 1. Sources

Four official documents, archived in [`fontes/`](../../fontes/README.en.md) with SHA-256 checksums and documented provenance:

- Spreadsheets for Elementary and Lower Secondary Education (EF) and Upper Secondary Education (EM), exported from the official tool of the Ministry of Education (MEC) (downloadbncc.mec.gov.br) on 2023-06-23, while the service was working (the backend was down in July 2026).
- The officially approved (homologated) PDF of Brazil's National Common Curricular Base (BNCC), complete edition (600 pages): the canonical document for verification. Early Childhood Education (EI) is extracted directly from it, because no spreadsheet is available.
- The annex of CNE/CEB Opinion 2/2022 (Computing, 75 pages), the canonical source of the `computacao-2022` module. The structure of its tables comes from the map `fontes/computacao-estrutura.json`, and every text is checked against the annex (decisions 10 and 13 in the [decisions summary](decisions-summary.md)).

## 2. Deterministic extraction

`pipeline/extrair.py` and `pipeline/extrair_ei.py` turn the sources into the JSON files in `dados/bncc-2018/`. No manual intervention and no LLM in the data chain: deterministic parsing that anyone can reproduce. Inconsistencies found in the sources are not silently corrected. Each one becomes a documented decision in the decisions log, [DECISOES.md](../../DECISOES.md) (in Portuguese). Example: three EM skills were on swapped tabs in the official spreadsheet; the canonical area is always the one decoded from the code.

## 3. Verification against the homologated document

`pipeline/verificar.py` compares the text of each of the 1,580 records with the homologated PDF, character by character, after typographic normalization (ligatures, line-break hyphenation, interleaved table columns). Current result:

- **1,580 of 1,580 identical**, with the PDF page recorded in `fonte.localizador_pdf`.
- **No open divergence.** Cases where the official sources disagree with each other are resolved in the extraction itself and are recorded: corrections of the spreadsheet against the PDF in `CORRECOES_PDF`, and limitations of the PDF text layer, with visual checking, in `CONFERIDOS_VISUALMENTE` (decision 12 in `DECISOES.md`).

## 4. Structural validation

Two layers, both with an exit code (they break CI):

- `pipeline/validar_schema.py`: the 7 data files (structure, EI, EF, EM, legal milestones, profiles and Computing) against the [JSON Schemas](../../schema/), with a negative self-test (deliberately corrupted records must be rejected on every run).
- `pipeline/validar.py`: 30 contract checks, including the grammar of all codes, expected reference counts per component and area (1,304 EF, 183 EM, 93 EI), referential integrity, structural domain rules and **completeness by full scan**: searching for codes across the whole PDF finds exactly the codes in the dataset. Nothing is missing, nothing is extra.

## 5. Checked derived files

`pipeline/derivar.py` generates SQLite and CSV files from the JSON files, deterministically. CI checks that the committed derived files are identical to the regenerated ones (CSVs by diff; SQLite by logical dump, which is immune to library version differences).

## 6. CI: reproducibility on every change

The [validation workflow](../../.github/workflows/validacao.yml) runs the full chain (extraction, verification, schemas, contracts, derived files) on every change, and fails if the committed dataset differs from the one reproduced from the sources. Reproducibility is not a promise: it is a test that always runs.

## External cross-validation

Beyond the internal chain, the dataset was compared with the BNCC database of Profy PEI (an independent lineage): 1,486 codes in common with 100% identical texts, and one gap found in that database (EF35LP16), not in this dataset.

## Pedagogical review

In July 2026, Profy's Pedagogical Team reviewed the dataset. The review focused on the point that automatic extraction cannot decide on its own: the **horizontal pairing of the Early Childhood Education alignments**. The official document (p. 26) states that objectives on the same row of the table, across age groups, address the same aspect of the field of experience. However, the table has no identifier for this link. The pipeline rebuilds it from the sequential position of the code (EI01TS01 → EI02TS01 → EI03TS01).

The review went through the 32 alignments and **confirmed the heuristic**: no incorrect pairing was found. This includes the three cases of an empty cell in the official table, which produce alignments of 2 objectives instead of 3 (`ei-align-eo-07`, `ei-align-et-07`, `ei-align-et-08`). The confirmation is recorded in the note of each of the 32 records and in decision 5 of the decisions log, [DECISOES.md](../../DECISOES.md) (in Portuguese).

The review also covered a sample of the Computing module (`computacao-2022`), with no issues raised.

## Known limits

- There is no public Early Childhood Education spreadsheet (the MEC tool is down). EI comes from the PDF, with the same verification.
- The pairing of EI alignments uses the sequential position of the codes (a heuristic faithful to the official table), confirmed in a pedagogical review (see above).
