[Português (registro completo)](../../DECISOES.md) · **English (summary)**

# Interpretation decisions: summary

Every inconsistency found in the official sources becomes an entry in [`DECISOES.md`](../../DECISOES.md) (in Portuguese), with context, decision and source. This page summarizes each entry in English. The Portuguese log is the authoritative version; future corrections must cite the official source in the pull request.

Terms: MEC is Brazil's Ministry of Education, CNE is the National Education Council, EI is Early Childhood Education, EF is Elementary and Lower Secondary Education, EM is Upper Secondary Education. "Homologated PDF" is the officially approved BNCC document.

| # | Topic | Decision |
|---|---|---|
| 1 | Rows in the wrong sheet of the official EM spreadsheet (EM13CNT310, EM13CHS606, EM13LGG105) | The knowledge area of a skill is always the one decoded from its code, never the sheet where the row sits. The three skills were relocated. |
| 2 | EM13LP35: the spreadsheet omits the word "de" that the homologated PDF has (PDF page 520) | The homologated PDF prevails. |
| 3 | EF03MA05: the spreadsheet omits the passage ", inclusive os convencionais," present in the homologated PDF (PDF page 289) | The homologated PDF prevails. |
| 4 | EF02MA06 and EF07MA33: the PDF text layer loses glyphs (digits, the π symbol) on PDF pages 285 and 311 | The spreadsheet prevails, with visual checks of the pages recorded. Revised by decision 12: for EF02MA06 it was a real spreadsheet × PDF divergence and the PDF prevails; for EF07MA33 the decision stands. |
| 5 | Horizontal alignment of EI objectives across age groups, which the official document describes (p. 26) but does not encode | The dataset pairs objectives by sequential number (EI01TS01, EI02TS01, EI03TS01) in the `alinhamento` entity. Empty cells produce three alignments with 2 objectives instead of 3. The pairing was confirmed by Profy's pedagogical team (07/2026), which reviewed all 32 alignments. |
| 6 | Knowledge objects have names that vary across years and components | In v1.0, each distinct name is a distinct entity. Equivalences across years are future curation work, in a separate layer and with recorded review. |
| 7 | Skill × competency links differ by stage | EM area skills use the specific competency decoded from the code. EM Portuguese Language skills use the competencies listed in the official spreadsheet (one or more). EF has no formal link per skill in the official document, and the dataset does not invent one. |
| 8 | Year or year range in the spreadsheet different from the one decoded from the code | The code prevails. No case was found in the current extraction; the rule is recorded for the pipeline. |
| 9 | EF05CO011: the only Computing code printed with three sequence digits in the official annex | Canonicalized as EF05CO11, following the two-digit grammar of the other 140 codes. The printed form is kept in the record's source locator. |
| 10 | Computing: the PDF text layer scrambles the merged cells of the annex tables | Structure taken from support spreadsheets of the Pernambuco State Department of Education, never as source of truth. All 141 texts and 78 structure items are checked character by character against the official annex, which always prevails. The Pernambuco state curriculum column does not enter the dataset. |
| 11 | Redistribution of the Pernambuco spreadsheets, which have no explicit redistribution license (27/07/2026) | Kept in the repository with attribution, as an accepted risk, so the Computing module stayed reproducible. Personal metadata (`dc:creator`) was removed from one file. Revised by decision 13. |
| 12 | Independent audit of 10/08/2026: three-way check (two independent deterministic checks plus visual reading of 100% of the records) | Found 8 records with text diverging from the homologated PDF, plus 3 hyphenation artifacts found during the fix. The PDF prevails in all 11 cases, now applied reproducibly through `CORRECOES_PDF` in `pipeline/extrair.py`. The verifier was reformed to close a prefix blind spot, and its hyphenation fallback no longer approves on its own: it requires a recorded visual check (`CONFERIDOS_VISUALMENTE`). Result: 1,580/1,580 ok. |
| 13 | Computing: removing the Pernambuco spreadsheets from the repository (14/10/2026) | The spreadsheets left the repository. `fontes/computacao-estrutura.json`, a structure map produced by the project, replaces them; it was generated once by `pipeline/gerar_mapa_computacao.py`, which checks each spreadsheet's SHA-256 before reading. The map is not a source of truth: every text, axis, knowledge object and competency is still checked against the official annex. `dados/` stays byte-for-byte identical, so there is no new data-version. The files remain in the git history and in the releases already archived on Zenodo. |

## Source versions

- Official spreadsheets: exported from downloadbncc.mec.gov.br on 23/06/2023 (the export tool was offline on 09/07/2026, with the backend returning 503).
- Canonical PDF: `Base-Nacional-Comum-Curricular-BNCC.pdf`, the full homologated version (600 pages). The file linked on the Upper Secondary page of the MEC website is the 2018 pre-homologation draft, with different texts and numbering; it is not used for verification.
- Checksums: [`fontes/README.en.md`](../../fontes/README.en.md).
