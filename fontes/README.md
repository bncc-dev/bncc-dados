**Português** · [English](README.en.md)

# Fontes oficiais

Matéria-prima canônica do dataset: os documentos oficiais e um mapa de estrutura produzido pelo projeto. Todos os registros do dataset são extraídos destes arquivos e verificados contra os documentos oficiais.

| Arquivo | O que é | Obtido em | SHA-256 |
|---|---|---|---|
| `BNCC_Ensino Fundamental.xlsx` | Exportação oficial da ferramenta do MEC (downloadbncc.mec.gov.br) | 23/06/2023 | `3e823abb2af70d76c6206f1743671315311ec2ef7a472054f67a64400a6ad5ea` |
| `BNCC_Ensino_Medio.xlsx` | Exportação oficial da ferramenta do MEC | 23/06/2023 | `f89493a6dcc8315a1803e0cbaa5966e582e13733798175fd3c5485c0c0dd4127` |
| `Base-Nacional-Comum-Curricular-BNCC.pdf` | BNCC completa homologada (600 p., três etapas). PDF canônico de verificação | 09/07/2026 | `81cd44ba5444ff1e8ff7b82d83512a49de9ce54efa72c4d285a452d3321128a4` |
| `anexo-ao-parecer-cneceb-no-2-2022-bncc-computacao.pdf` | Anexo ao Parecer CNE/CEB nº 2/2022: Computação, complemento à BNCC (75 p.). **Fonte canônica do módulo computacao-2022** | 11/07/2026 | `b0f021db3c7c2c042b821cec5fab7d77ed1888dbb61590461ce2afef404865b7` |
| `computacao-estrutura.json` | Mapa de estrutura do módulo computacao-2022 (eixos, objetos de conhecimento, competências e textos), produzido pelo projeto. **Não é fonte oficial**: cada texto e nome é verificado contra o anexo oficial no CI. Gerado por `pipeline/gerar_mapa_computacao.py` a partir das planilhas de apoio descritas abaixo; licença CC BY 4.0 | 14/10/2026 | `1bf7f01632886a9f7a2a6dc7d0eb0162b66fbab58642f98385a3881a95e6a002` |

Notas de proveniência:

- A ferramenta oficial de exportação estava fora do ar em 09/07/2026 (backend HTTP 503). As planilhas aqui arquivadas foram exportadas quando o serviço funcionava.
- A planilha da Educação Infantil não está disponível (ferramenta fora do ar); os objetivos da EI são extraídos diretamente do PDF homologado.
- Cuidado com versões: o PDF distribuído na página do Ensino Médio do site do MEC é o rascunho pré-homologação (2018), com textos diferentes dos finais. Use somente o PDF completo homologado.
- O anexo de Computação foi obtido do acervo atual do CNE (`www.gov.br/mec/pt-br/cne/pdf/pareceres-do-cne/ceb/2022/`), que fica atrás de proteção anti-bot (download exige navegador; o hash acima confere byte a byte com o servidor). O portal.mec.gov.br legado saiu do ar em jul/2026.
- O PDF do anexo tem tabela xref fora do padrão: o poppler (`pdftotext`/`pdfinfo`) não o lê diretamente. Para extração, normalizar antes com Ghostscript (`gs -dNOPAUSE -dBATCH -sDEVICE=pdfwrite`) — o arquivo aqui arquivado é o ORIGINAL intocado; a normalização é passo do pipeline (`pipeline/anexo_computacao.py`), nunca da fonte.
- O mapa `computacao-estrutura.json` substitui, desde 14/10/2026, as planilhas de apoio da Secretaria de Educação de Pernambuco que ficavam em `secedu-pernambuco/` (decisão 13 do `DECISOES.md`). Ele guarda a estrutura que a camada de texto do PDF embaralha (eixo, objeto de conhecimento, competência) e o texto de cada aprendizagem. Nada nele é fonte de verdade: `pipeline/verificar_computacao.py` confere cada texto caractere a caractere contra o anexo oficial, que sempre prevalece. Não edite o mapa à mão; regenere com o script.

## Planilhas de apoio não redistribuídas

O mapa foi gerado a partir destes quatro arquivos, que **não fazem parte do repositório** desde 14/10/2026 (decisão 13 do `DECISOES.md`). São materiais públicos de formação da Secretaria de Educação de Pernambuco sobre a BNCC Computação, obtidos pelo time em 11/07/2026, sem licença explícita de redistribuição. Ficam registrados aqui com nome e SHA-256 para rastreabilidade.

| Arquivo | O que é | Obtido em | SHA-256 |
|---|---|---|---|
| `COMPUTAÇÃO - EDUCAÇÃO INFANTIL .xlsx` | Planilha de apoio (Sec. de Educação de PE): estrutura dos quadros de EI | 11/07/2026 | `1c3df76a1ead3e2df93ecef9eb931ace8b4756d3f203e66188c41e5b97c8e48d` |
| `1º ao 5º ANO - HABILIDADES- BNCC - Computação.xlsx` | Planilha de apoio (PE): EF anos iniciais + bloco EF15 | 11/07/2026 | `78db18845598bb5efa3acf7e29ab6a2e12313c2913e1e4d7ab781070b40da53a` |
| `6º ao 9º ANO - HABILIDADES - BNCC - Computação .xlsx` | Planilha de apoio (PE): EF anos finais + bloco EF69 | 11/07/2026 | `202dab133d4b5b2ea3a0b49ce61792e40fa3cb82f2f45a4aadf892df30e4039c` |
| `COMPUTAÇÃO - ENSINO MÉDIO.xlsx` | Planilha de apoio (PE): EM por competência específica | 11/07/2026 | `8b19f82ddd4b7ad140dd23120ff005647a8d1b7b9b56a10dc6d6e398dba6cdf9` |

- Para regenerar o mapa, coloque os quatro arquivos em um diretório e rode `python3 pipeline/gerar_mapa_computacao.py /caminho/do/diretorio`. O script confere os SHA-256 acima antes de ler e reproduz o mapa byte a byte.
- A coluna "Habilidade(s) do Currículo de Pernambuco" dessas planilhas nunca entrou no dataset nem no mapa.
- **Metadado de autoria removido** de `6º ao 9º ANO - HABILIDADES - BNCC - Computação .xlsx` em 27/07/2026: a propriedade `dc:creator` do pacote OOXML trazia o nome de uma pessoa física. Só esse campo foi retirado. Por isso o SHA-256 registrado para este arquivo não confere com o do arquivo original recebido.
- **Origem exata**: estas planilhas não têm URL de origem documentada, só a data de obtenção. *(pendência aberta)*
- Até 14/10/2026 os arquivos eram redistribuídos neste diretório, com atribuição à Secretaria. Eles continuam no histórico do git e nas versões já publicadas no Zenodo. Contato para qualquer pedido da Secretaria: contato@bncc.dev.
