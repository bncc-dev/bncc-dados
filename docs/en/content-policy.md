[Português](../politica-de-conteudo.md) · **English**

# Content policy

What this dataset distributes, how errors and improper content are identified, how to report them and what happens after a report.

## What is distributed

- **Normative texts.** The texts of Brazil's National Common Curricular Base (BNCC) and of its Computing supplement, reproduced without changes from the official documents of the Ministry of Education (MEC) and the National Education Council (CNE) (see [`fontes/`](../../fontes/README.en.md)).
- **Project metadata.** Structure (stages, curricular components, axes, knowledge objects), identifiers, relationships, validity period and the provenance of each record (source file and page).

The dataset has no user-submitted content. Issues, pull requests and discussions are the only space for interaction, governed by the [code of conduct](../../CODE_OF_CONDUCT.en.md).

## What counts as a problem

- **Divergent text.** A record's text differs from the official document: a transcription error, truncation, hyphenation.
- **Wrong metadata.** An incorrect code, year, component, relationship or source page.
- **Improper content.** Anything that is neither official text nor project metadata, such as text inserted into a file by mistake or maliciously.
- **Personal data.** Any information that identifies a person in a repository file.

Disagreeing with the content of the BNCC itself is not a problem for this repository. The normative text is the responsibility of the CNE.

## How problems are identified

- **Automatic verification.** On every change, CI checks each text character by character against the officially approved (homologated) PDF and the official Computing annex. Any discrepancy fails the change.
- **Full reproduction.** CI rebuilds the entire dataset from the sources. A manual edit in `dados/` fails the change.
- **Format validation.** Closed JSON Schemas and 29 contract and completeness checks.
- **Independent audits.** The audit of 10 August 2026 read 100% of the records and resulted in 11 corrections. See decision 12 in the decisions log, [DECISOES.md](../../DECISOES.md) (in Portuguese).

## How to report

- **Data error:** an issue using the "Correção de dado" (data correction) template, with the record's code, the current value, the correct value and the official source with its page.
- **Normative change** (a new CNE resolution or opinion): an issue using the "Mudança normativa" (normative change) template.
- **Personal data, improper content or a vulnerability:** an email to **contato@bncc.dev**, without a public issue, as described in [SECURITY.en.md](../../SECURITY.en.md).

## What happens next

- **Error confirmed by the official source.** The fix goes into the extraction, never by hand, and is released in a new data-version, with an entry in [CHANGELOG.md](../../CHANGELOG.md) (in Portuguese) under the `correcao` (correction) category. If interpretation is involved, it becomes an entry in DECISOES.md, the decisions log.
- **Discrepancy between official sources.** The choice becomes a documented decision in DECISOES.md, with the reason.
- **Personal data or improper content.** It is removed from the current version as soon as it is identified, and the reporter receives a reply. Removal from the git history is assessed case by case.
- **Request without an official source.** It is sent back with a request for the source. If there is no reply within 30 days, the issue is closed.

## Target times

| Stage | Target time |
|---|---|
| First response to a correction issue | 3 business days |
| Assessment against the official source | 10 business days |
| Correction published, when the source confirms the error | in the next data-version |
| Removal of personal data or improper content | within 3 business days of the report, the same confirmation deadline as [SECURITY.en.md](../../SECURITY.en.md) |

These times are targets. Delays and exceptions are recorded in the issue itself.
