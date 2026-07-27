# Fontes oficiais

Matéria-prima canônica do dataset. Todos os registros do dataset são extraídos destes arquivos e verificados contra o PDF.

| Arquivo | O que é | Obtido em | SHA-256 |
|---|---|---|---|
| `BNCC_Ensino Fundamental.xlsx` | Exportação oficial da ferramenta do MEC (downloadbncc.mec.gov.br) | 23/06/2023 | `3e823abb2af70d76c6206f1743671315311ec2ef7a472054f67a64400a6ad5ea` |
| `BNCC_Ensino_Medio.xlsx` | Exportação oficial da ferramenta do MEC | 23/06/2023 | `f89493a6dcc8315a1803e0cbaa5966e582e13733798175fd3c5485c0c0dd4127` |
| `Base-Nacional-Comum-Curricular-BNCC.pdf` | BNCC completa homologada (601 p., três etapas). PDF canônico de verificação | 09/07/2026 | `81cd44ba5444ff1e8ff7b82d83512a49de9ce54efa72c4d285a452d3321128a4` |
| `anexo-ao-parecer-cneceb-no-2-2022-bncc-computacao.pdf` | Anexo ao Parecer CNE/CEB nº 2/2022: Computação, complemento à BNCC (75 p.). **Fonte canônica do módulo computacao-2022** | 11/07/2026 | `b0f021db3c7c2c042b821cec5fab7d77ed1888dbb61590461ce2afef404865b7` |
| `secedu-pernambuco/COMPUTAÇÃO - EDUCAÇÃO INFANTIL .xlsx` | Planilha de apoio (Sec. de Educação de PE): estrutura dos quadros de EI | 11/07/2026 | `1c3df76a1ead3e2df93ecef9eb931ace8b4756d3f203e66188c41e5b97c8e48d` |
| `secedu-pernambuco/1º ao 5º ANO - HABILIDADES- BNCC - Computação.xlsx` | Planilha de apoio (PE): EF anos iniciais + bloco EF15 | 11/07/2026 | `78db18845598bb5efa3acf7e29ab6a2e12313c2913e1e4d7ab781070b40da53a` |
| `secedu-pernambuco/6º ao 9º ANO - HABILIDADES - BNCC - Computação .xlsx` | Planilha de apoio (PE): EF anos finais + bloco EF69 | 11/07/2026 | `202dab133d4b5b2ea3a0b49ce61792e40fa3cb82f2f45a4aadf892df30e4039c` |
| `secedu-pernambuco/COMPUTAÇÃO - ENSINO MÉDIO.xlsx` | Planilha de apoio (PE): EM por competência específica | 11/07/2026 | `8b19f82ddd4b7ad140dd23120ff005647a8d1b7b9b56a10dc6d6e398dba6cdf9` |

Notas de proveniência:

- A ferramenta oficial de exportação estava fora do ar em 09/07/2026 (backend HTTP 503). As planilhas aqui arquivadas foram exportadas quando o serviço funcionava.
- A planilha da Educação Infantil não está disponível (ferramenta fora do ar); os objetivos da EI são extraídos diretamente do PDF homologado.
- Cuidado com versões: o PDF distribuído na página do Ensino Médio do site do MEC é o rascunho pré-homologação (2018), com textos diferentes dos finais. Use somente o PDF completo homologado.
- O anexo de Computação foi obtido do acervo atual do CNE (`www.gov.br/mec/pt-br/cne/pdf/pareceres-do-cne/ceb/2022/`), que fica atrás de proteção anti-bot (download exige navegador; o hash acima confere byte a byte com o servidor). O portal.mec.gov.br legado saiu do ar em jul/2026.
- O PDF do anexo tem tabela xref fora do padrão: o poppler (`pdftotext`/`pdfinfo`) não o lê diretamente. Para extração, normalizar antes com Ghostscript (`gs -dNOPAUSE -dBATCH -sDEVICE=pdfwrite`) — o arquivo aqui arquivado é o ORIGINAL intocado; a normalização é passo do pipeline (`pipeline/anexo_computacao.py`), nunca da fonte.
- As planilhas de `secedu-pernambuco/` (materiais públicos de formação da Secretaria de Educação de Pernambuco sobre a BNCC Computação, obtidos pelo time em 11/07/2026) são **apoio de extração, nunca fonte de verdade**: fornecem a estrutura de células que a camada de texto do PDF embaralha. Todos os textos extraídos são verificados caractere a caractere contra o anexo oficial, que sempre prevalece (`pipeline/verificar_computacao.py`; racional em `DECISOES.md`, entrada 10). A coluna "Habilidade(s) do Currículo de Pernambuco" dessas planilhas não entra no dataset.
- **Metadado de autoria removido** de `6º ao 9º ANO - HABILIDADES - BNCC - Computação .xlsx` em 27/07/2026: a propriedade `dc:creator` do pacote OOXML trazia o nome de uma pessoa física, que não tem por que ser republicado. Só esse campo foi retirado; nenhuma célula, fórmula ou aba foi tocada, e a extração produz exatamente o mesmo dado (141/141 verificadas). Por isso o SHA-256 deste arquivo **não** confere com o do arquivo original recebido — é a única fonte deste diretório que não é byte-a-byte a original. Os outros três arquivos estão intocados.
- **Origem exata a registrar**: diferentemente das demais fontes, estas planilhas não têm URL de origem documentada — só a data de obtenção. Preencher a URL aqui assim que localizada. *(pendência aberta)*
- **Base da redistribuição**: são materiais públicos de formação, republicados aqui com atribuição à Secretaria de Educação de Pernambuco e com a finalidade única de tornar reproduzível a extração de um dado normativo público (o anexo do Parecer CNE/CEB nº 2/2022). Não há licença explícita de redistribuição nesses arquivos, e o projeto os remove a pedido da Secretaria, sem discussão. Contato: contato@bncc.dev.
