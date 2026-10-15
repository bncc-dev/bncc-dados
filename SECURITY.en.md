[Português](SECURITY.md) · **English**

# Security policy

## Scope

This repository publishes a dataset and the scripts that produce it. There is no hosted service, no authentication and no personal data here. The relevant classes of problem are:

- Code in `pipeline/` that executes something unwanted when processing the sources.
- A compromised dependency or an exploitable CI workflow.
- Malicious content embedded in files in `fontes/` (official sources) or `derivados/` (derived formats).
- Accidental exposure of a secret or of personal data in any file or in the history.

A data error (text that differs from the official source, a wrong code, an incorrect relationship) **is not a security problem**: open a normal correction issue, as described in [CONTRIBUTING.en.md](CONTRIBUTING.en.md).

## Supported versions

Always `main` and the most recent published data-version (`dados-2026.07.1`); there is no retroactive support for earlier versions.

## How to report

Send an email to **contato@bncc.dev** with a subject line starting with `[seguranca]` (Portuguese for "security"). Include a description, steps to reproduce and the estimated impact.

Do not open a public issue for a vulnerability before making contact. If you prefer the GitHub channel, use *Security > Report a vulnerability* (private vulnerability reporting), which is also private.

## What to expect

| Stage | Target time |
|---|---|
| Acknowledgment of receipt | 3 business days |
| Initial assessment and classification | 10 business days |
| Fix or fix plan | depending on severity, communicated in the assessment |

Reporters are credited in the CHANGELOG and in the release notes, unless they ask to remain anonymous.
