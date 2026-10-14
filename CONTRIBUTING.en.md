[Português](CONTRIBUTING.md) · **English**

# Contributing guide

Thank you for your interest in improving the reference source for the structured version of Brazil's National Common Curricular Base (BNCC).

## The golden rule: a correction requires an official source

This dataset records what the official documents say. To propose a data correction, the PR must point to the official source that supports it: the document (from the Ministry of Education (MEC) or the National Education Council (CNE)), the page or locator and, if possible, a screenshot of the passage. Corrections without a reference to the source will be kindly sent back.

If the discrepancy is between two official sources, the PR must also propose the decision entry documenting which source prevails and why. This does happen: see the decisions log, [DECISOES.md](DECISOES.md) (in Portuguese). An English summary is in [docs/en/decisions-summary.md](docs/en/decisions-summary.md).

## How to contribute

1. **Data error** (wrong text, code or relationship): open an issue with the record's code, the current value, the correct value and the official source.
2. **Pipeline error** (extraction, verification, validation): an issue or a direct PR; the scripts are in [`pipeline/`](pipeline/) and use only the Python standard library (except `jsonschema`, for format validation).
3. **Schema or documentation improvement**: PRs are welcome; format changes are discussed in an issue first (they affect consumers).

## Running the pipeline locally

```bash
pip install -r requirements.txt    # the only Python dependency (jsonschema, format validation)
cd pipeline
python3 extrair.py && python3 extrair_ei.py && python3 extrair_computacao.py
python3 verificar.py && python3 verificar_computacao.py
python3 validar_schema.py && python3 validar.py
python3 derivar.py
```

Requirements: Python 3.10+, `pdftotext` (poppler) and `ghostscript` (to normalize the Computing annex). CI runs exactly this sequence and checks that the committed dataset is identical to the reproduced one; PRs that change `dados/` (the data) without changing a source or the pipeline will fail by definition.

## What we do not accept

- Data without provenance (including LLM-generated content presented as official).
- Interpretive content in the canonical core (commentary, breakdowns, inferred progressions). That belongs in the future annotation layer, with its own source and license.
- Third-party material without a compatible license (e.g. CC BY-NC derivatives).

## Conduct

Respect and good faith. This project serves Brazilian public education; technical discussions should carry that spirit. The full rules and the reporting channel are in [CODE_OF_CONDUCT.en.md](CODE_OF_CONDUCT.en.md).

Disagreeing about data is not a conduct violation: disagreements about the dataset's content are always settled by the official source, never by insistence or personal authority.

## Security

Security problems (pipeline, CI, dependencies, accidental exposure of a secret) do not go in a public issue: see [SECURITY.en.md](SECURITY.en.md). A data error is not a security problem; it is a normal correction issue.
