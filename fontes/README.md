# Fontes oficiais

Matéria-prima canônica do dataset. Todos os registros do dataset são extraídos destes arquivos e verificados contra o PDF.

| Arquivo | O que é | Obtido em | SHA-256 |
|---|---|---|---|
| `BNCC_Ensino Fundamental.xlsx` | Exportação oficial da ferramenta do MEC (downloadbncc.mec.gov.br) | 23/06/2023 | `3e823abb2af70d76c6206f1743671315311ec2ef7a472054f67a64400a6ad5ea` |
| `BNCC_Ensino_Medio.xlsx` | Exportação oficial da ferramenta do MEC | 23/06/2023 | `f89493a6dcc8315a1803e0cbaa5966e582e13733798175fd3c5485c0c0dd4127` |
| `Base-Nacional-Comum-Curricular-BNCC.pdf` | BNCC completa homologada (601 p., três etapas). PDF canônico de verificação | 09/07/2026 | `81cd44ba5444ff1e8ff7b82d83512a49de9ce54efa72c4d285a452d3321128a4` |

Notas de proveniência:

- A ferramenta oficial de exportação estava fora do ar em 09/07/2026 (backend HTTP 503). As planilhas aqui arquivadas foram exportadas quando o serviço funcionava.
- A planilha da Educação Infantil não está disponível (ferramenta fora do ar); os objetivos da EI são extraídos diretamente do PDF homologado.
- Cuidado com versões: o PDF distribuído na página do Ensino Médio do site do MEC é o rascunho pré-homologação (2018), com textos diferentes dos finais. Use somente o PDF completo homologado.
