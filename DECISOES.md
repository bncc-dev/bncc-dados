**Português** · [English (resumo)](docs/en/decisions-summary.md)

# DECISOES.md · decisões de interpretação

Toda inconsistência encontrada nas fontes oficiais vira uma entrada aqui: contexto, decisão e fonte. Correções futuras exigem referência à fonte oficial no PR.

## 1. Rotação de linhas entre abas na planilha oficial do EM

Na planilha `BNCC_Ensino_Medio.xlsx` (exportada da ferramenta oficial em 23/06/2023), três habilidades estão em abas trocadas: EM13CNT310 na aba de Linguagens, EM13CHS606 na aba de Ciências da Natureza e EM13LGG105 na aba de Ciências Humanas.

**Decisão:** a área de cada habilidade é sempre a decodificada do código, nunca a aba onde a linha está. As três foram realocadas.

*Fonte: planilha oficial × decodificador de códigos (pipeline/codigos.py).*

## 2. EM13LP35: divergência de texto entre planilha e PDF homologado

A planilha traz "dimensionando a quantidade texto e imagem"; o PDF homologado (página PDF 520) traz "dimensionando a quantidade **de** texto e imagem".

**Decisão:** prevalece o PDF homologado. O dataset traz o texto do PDF.

## 3. EF03MA05: divergência de texto entre planilha e PDF homologado

A planilha omite o trecho ", inclusive os convencionais," presente no PDF homologado (página PDF 289).

**Decisão:** prevalece o PDF homologado.

## 4. EF02MA06 e EF07MA33: limitações da camada de texto do PDF

Nas páginas PDF 285 e 311, a extração de texto do PDF perde glifos (dígitos e o símbolo π). Não é divergência de conteúdo: é limitação técnica da camada de texto.

**Decisão:** prevalece a planilha, com conferência visual das páginas registrada.

*Revista em 10/08/2026 (ver decisão 12): para EF02MA06 a conclusão estava errada — era divergência real planilha × PDF, e o PDF prevalece. Para EF07MA33 (π) a decisão permanece.*

## 5. Alinhamento horizontal da EI reconstruído por posição sequencial

O documento oficial (p. 26) afirma que objetivos na mesma linha do quadro, entre grupos etários, referem-se a um mesmo aspecto do campo de experiências. O dataset materializa isso na entidade `alinhamento`, pareando objetivos pelo mesmo número sequencial (EI01TS01, EI02TS01, EI03TS01).

Células vazias do quadro oficial geram alinhamentos com 2 objetivos em vez de 3 (ei-align-eo-07, ei-align-et-07, ei-align-et-08): bebês têm menos objetivos nos campos EO e ET.

**Decisão:** heurística de pareamento por posição adotada e **confirmada em revisão pedagógica** (Equipe Pedagógica Profy, 07/2026), que percorreu os 32 alinhamentos e não encontrou pareamento incorreto. A nota de cada registro passou de "revisão pedagógica pendente" para o registro da confirmação.

## 6. Objetos de conhecimento: identidade por nome não cria progressão entre anos

Os nomes dos objetos de conhecimento variam entre anos e componentes; a deduplicação automática por texto não estabelece a travessia "mesmo objeto em anos anteriores".

**Decisão:** na v1.0, cada nome distinto é uma entidade distinta. Equivalências entre anos são trabalho de curadoria futura, em camada separada e com revisão registrada.

## 7. Vínculo habilidade x competência: assimetrias por etapa

No EM, as habilidades de área têm exatamente uma competência específica, embutida no código. As habilidades de Língua Portuguesa do EM não a têm no código, mas a planilha oficial traz o vínculo em coluna própria, multivalorado (ex.: "1,2,3").

**Decisão:** habilidades de área usam a competência decodificada; habilidades de LP usam as da planilha (1 a n). No EF não existe vínculo formal por habilidade no documento oficial, e o dataset não o inventa.

## 8. Ano/faixa: prevalece o código, não a célula da planilha

Quando o ano/faixa declarado na planilha divergir do decodificado do código, prevalece o código. Nenhum caso encontrado na extração atual; a regra fica registrada para o pipeline.

## 9. EF05CO011: código com três dígitos de sequência no anexo oficial de Computação

O anexo ao Parecer CNE/CEB nº 2/2022 imprime "(EF05CO011)" no quadro do 5º ano — o único código de Computação com sequência de 3 dígitos, vindo imediatamente após o EF05CO10. As planilhas de apoio da Sec. de Educação de Pernambuco reproduzem a mesma forma.

**Decisão:** canonizado como EF05CO11, seguindo a gramática de 2 dígitos dos demais 140 códigos do complemento. A forma impressa fica registrada no localizador da fonte do registro.

*Fonte: anexo ao Parecer CNE/CEB nº 2/2022 (quadro do 5º ano) × gramática dos códigos.*

## 10. Computação: estrutura via planilhas de Pernambuco, texto verificado pelo anexo

Os quadros do anexo oficial têm células mescladas em múltiplos níveis (eixo > objeto pai > sub-objeto) que a camada de texto do PDF embaralha. As planilhas da Secretaria de Educação de Pernambuco preservam as fronteiras de célula e forneceram a estrutura; variantes de nome geradas por quebra de linha dentro de células (ex.: "responsabilidad e") foram unificadas pela forma mais frequente.

**Decisão:** estrutura extraída das planilhas de PE (nunca fonte de verdade); todos os 141 textos de aprendizagem e 78 itens de estrutura verificados caractere a caractere contra o anexo oficial, que sempre prevalece. Os descritores de agrupamento, explicações e exemplos oficiais do anexo ficam para iteração futura do módulo. A coluna do currículo de Pernambuco não entra no dataset (dado estadual, insumo da Fase 5).

*Fonte: planilhas Sec. Educação de PE × anexo ao Parecer CNE/CEB nº 2/2022.*

## 11. Redistribuição das planilhas de Pernambuco no repositório público

As planilhas de apoio da Secretaria de Educação de Pernambuco são materiais públicos de formação, mas não trazem licença explícita de redistribuição. Como o `pipeline/extrair_computacao.py` depende delas, removê-las do repositório tornaria o módulo `computacao-2022` não reproduzível — o único do dataset nessa condição, contra a premissa central do projeto.

**Decisão (27/07/2026):** manter os arquivos no repositório, com atribuição explícita à Secretaria e finalidade declarada de reprodutibilidade de dado normativo público, e remover a pedido da Secretaria sem discussão. O metadado `dc:creator` de `6º ao 9º ANO - HABILIDADES - BNCC - Computação .xlsx`, que trazia o nome de uma pessoa física, foi removido: a atribuição institucional é pertinente, a identificação do servidor não. Nenhuma célula foi alterada e a extração segue produzindo 141/141 verificadas.

Registrado como risco assumido e não como ausência de risco. A alternativa avaliada — substituir as planilhas por um JSON com o mapa código → eixo → objeto, preservando a reprodutibilidade sem redistribuir os arquivos — permanece disponível caso a situação mude.

**Revista pela decisão 13 (14/10/2026).**

*Fonte: `fontes/README.md` (notas de proveniência) × auditoria de abertura de 27/07/2026.*

## 12. Auditoria independente de 10/08/2026: 11 correções de texto e reforma da verificação

Auditoria externa em três vias (duas determinísticas independentes + leitura visual de 100% dos registros) sobre `@bncc/dados 0.3.1` confirmou a estrutura de códigos perfeita (1.721 códigos, sem faltas nem sobras, páginas de origem corretas) e encontrou 8 registros com texto divergente do PDF homologado; a conferência visual das páginas durante a aplicação das correções encontrou mais 3 artefatos de hifenização no dataset.

As causas, todas de processo:

- **Ponto cego de prefixo**: `verificar.py` só conferia se o texto do dataset era prefixo do PDF; truncamentos (EF69LP34, EF69LP46 e os pontos finais de EF89LP19 e EF69AR16) nunca falhavam.
- **Aprovação silenciosa**: o fallback que compara ignorando espaços e hífens aprovou como "ok com nota" o texto corrompido de EF03LP20 ("campopo lítico-cidadão").
- **Decisões 2 e 3 documentadas e não aplicadas**: o extrator não tinha camada de correções, então EM13LP35 e EF03MA05 continuavam com o texto da planilha apesar da decisão registrada.
- **Decisão 4 parcialmente revista**: em EF02MA06 a desconfiança do PDF veio de extração corrompida da p. 285 ("por 2, 3, 4 e 5" virava "por e"); a página impressa é legível, termina em "estratégias pessoais." e **não** contém "ou convencionais". Era divergência real planilha × PDF, não perda de glifo. EF07MA33 (π) permanece como estava: dataset correto, limitação da camada de texto.

**Decisão:** o PDF homologado prevalece nos 11 casos (EF03LP20, EF69LP46, EF69LP34, EF02MA06, EF03MA05, EM13LP35, EF89LP19, EF69AR16, EF03LP11, EF04LP01, EF69LP48), agora aplicados de forma reproduzível pelo mapa `CORRECOES_PDF` em `pipeline/extrair.py`. O verificador passou a comparar a continuação do PDF após o fim do texto (elimina o ponto cego), e o fallback de hifenização não aprova mais sozinho: devolve `requer_conferencia_visual`, sanado apenas por exceção registrada em `CONFERIDOS_VISUALMENTE` com página conferida e motivo (hoje: EF07MA33, EF04GE08, EF03LP11, EF69LP48 — páginas 311, 379, 121 e 161 conferidas visualmente em 10/08/2026). Resultado após as correções: 1.580/1.580 ok.

*Fonte: PDF homologado (páginas 117, 121, 127, 153, 159, 161, 185, 211, 285, 289, 311, 379, 520, conferidas visualmente) × relatório da auditoria independente de 10/08/2026.*

## 13. Computação: mapa de estrutura próprio no lugar das planilhas de Pernambuco

A decisão 11 manteve no repositório as planilhas de apoio da Secretaria de Educação de Pernambuco, sem licença explícita de redistribuição, e registrou isso como risco assumido. O risco deixou de ser aceitável: o dataset vai ser submetido ao registro de Digital Public Goods, cuja regra para dados abertos exige que todo o conteúdo distribuído esteja sob licença aberta ou tenha direito de redistribuição comprovado. A alternativa que a decisão 11 deixou registrada resolve o problema sem perder reprodutibilidade.

**Decisão (14/10/2026):** as planilhas saem do repositório. Em seu lugar entra `fontes/computacao-estrutura.json`, um mapa produzido pelo projeto com eixo, objeto de conhecimento, competência, texto e localizador de origem de cada uma das 141 aprendizagens, além das competências do complemento. O mapa foi gerado uma vez por `pipeline/gerar_mapa_computacao.py` (o código de leitura das planilhas que antes ficava em `extrair_computacao.py`), que confere o SHA-256 de cada planilha antes de ler. `extrair_computacao.py` passa a ler só o mapa e o anexo oficial.

- O mapa não é fonte de verdade. `verificar_computacao.py` continua conferindo cada texto, eixo, objeto e competência caractere a caractere contra o anexo, que sempre prevalece.
- `dados/computacao-2022/computacao.json` sai idêntico byte a byte. O localizador de cada registro continua apontando para a planilha e a linha de onde a estrutura veio, que seguem descritas com nome e SHA-256 em `fontes/README.md`.
- A única mudança nos derivados é o metadado `fontes_sha256_16` do SQLite, que passa a listar o mapa no lugar das planilhas. Não há mudança de dado, logo não há nova data-version.
- Os arquivos continuam no histórico do git e nas versões já arquivadas no Zenodo. Reescrever o histórico quebraria clones e a correspondência entre commits e DOIs, e não foi feito.

*Fonte: decisão 11 × regra de licenciamento de Open Data do DPG Standard (indicador 2) × reprodução completa do pipeline em 14/10/2026 (1.580/1.580 e 141/141 ok, `dados/` sem diferença).*

## 14. Verificação do dicionário de dados (14/10/2026): nomes partidos, páginas de exemplo e campos sem definição

A preparação do dicionário de dados (`docs/dicionario-de-dados.md`) levou a duas verificações independentes, em modo somente leitura, contra os schemas, os dados, o pipeline e os PDFs oficiais. A integridade geral confirmou (schemas, unicidade, referências, varredura de códigos, checksums), mas apareceram defeitos de extração que nunca tinham sido conferidos porque a verificação cobria só o texto das aprendizagens.

**Nomes de contexto partidos por defeito de extração.** `pipeline/extrair.py` dividia a célula de objetos de conhecimento em uma entidade por linha; quatro nomes longos que a planilha quebra ao meio viraram oito objetos ("Fenômenos naturais (vulcões, terremotos e" + "tsunamis)", PDF 348; "Verbos modais: should, must, have to, may e" + "might", PDF 264; dois de LP, PDF 160 e 166). A prática de linguagem "Oralidade" absorveu a nota de rodapé da célula ("*Considerar todas as habilidades…", PDF 144 e 146) em uma variante usada por 3 habilidades. A unidade temática de LI "Estratégias de escrita: escrita e pós-escrita" ficou com o hífen de quebra ("pós- escrita"). Em Computação, o marcador "(cont.)" com que o anexo sinaliza a continuação do quadro do 9º ano (PDF 58: "COMPUTAÇÃO - 9º ANO (CONTINUAÇÃO)") virou dois objetos novos ("Segurança cibernética (cont.)" e seu pai).

**Decisão:** esses ids nunca representaram entidades da BNCC; são artefatos de extração, e corrigi-los é correção de erro nosso, não mudança de modelo. A regra "slug imutável após publicado" do `docs/modelo-de-dados.md` ganha a exceção explícita: um id gerado por defeito de extração pode ser removido, com o mapa de substituição publicado no CHANGELOG e aqui. O extrator passa a juntar linhas de continuação (linha que começa em minúscula), descartar notas de rodapé e desfazer hífens de quebra nos nomes de contexto; o gerador do mapa de Computação remove o marcador "(cont.)". Contratos novos no `validar.py` impedem regressão.

| Id removido | Substituído por |
|---|---|
| `ef-comp-ci-oc-fenomenos-naturais-vulcoes-terremotos-e`, `ef-comp-ci-oc-tsunamis` | `ef-comp-ci-oc-fenomenos-naturais-vulcoes-terremotos-e-tsunamis` |
| `ef-comp-li-oc-verbos-modais-should-must-have-to-may-e`, `ef-comp-li-oc-might` | `ef-comp-li-oc-verbos-modais-should-must-have-to-may-e-might` |
| `ef-comp-lp-oc-textualizacao-tendo-em-vista-suas-condicoes-de-producao-as-caracteristicas-do-genero-em-questao-o-estabelecimento-de-coesao`, `ef-comp-lp-oc-adequacao-a-norma-padrao-e-o-uso-adequado-de-ferramentas-de-edicao` | `ef-comp-lp-oc-textualizacao-tendo-em-vista-suas-condicoes-de-producao-as-caracteristicas-do-genero-em-questao-o-estabelecimento-de-coesao-adequacao-a-norma-padrao-e-o-uso-adequado-de-ferramentas-de-edicao` |
| `ef-comp-lp-oc-reconstrucao-da-textualidade-e-compreensao-dos-efeitos`, `ef-comp-lp-oc-de-sentidos-provocados-pelos-usos-de-recursos-linguisticos-e-multissemioticos` | `ef-comp-lp-oc-reconstrucao-da-textualidade-e-compreensao-dos-efeitos-de-sentidos-provocados-pelos-usos-de-recursos-linguisticos-e-multissemioticos` (já existia) |
| `ef-comp-lp-prat-oralidade-considerar-todas-as-habilidades-dos-eixos-leitura-e-producao-que-se-referem-a-textos-ou-producoes-orais-em-audio-ou-video` | `ef-comp-lp-prat-oralidade` (já existia) |
| `ef-comp-li-ut-estrategias-de-escrita-escrita-e-pos-escrita` | `ef-comp-li-ut-estrategias-de-escrita-escrita-e-pos-escrita` (id igual; só o `nome` muda) |
| `co-obj-seguranca-cibernetica-cont` | `co-obj-seguranca-cibernetica` (já existia) |
| `co-obj-sistemas-distribuidos-e-internet-cont` | `co-obj-sistemas-distribuidos-e-internet` (já existia) |

Os contextos do EF passam de 879 para 873 (objetos de conhecimento de 780 para 775) e os objetos de Computação de 61 para 59. Os ids `ef-comp-li-eixo-eixo-*` (a palavra "eixo" repetida, vinda do nome da planilha "Eixo oralidade") ficam como estão: não são defeito de extração, e sim o nome da planilha, e são referenciados por 88 habilidades.

**Página de verificação no capítulo "Estrutura".** O `verificar.py` devolvia a primeira página em que o texto casava. Para EI01TS01, EI02TS01, EI03TS01 (PDF 28) e EF01CI02 a EF01CI04 (PDF 31) essa página era o exemplo ilustrativo do capítulo "Estrutura" ("Como é possível observar no exemplo apresentado…"), não o quadro normativo (PDF 50 e 335). **Decisão:** o verificador ignora as páginas PDF 25 a 36 (o capítulo), e um contrato garante que nenhum localizador aponte para elas. As habilidades `EM13MAT` que aparecem em duas páginas normativas (listagem por competência e quadro por unidade temática) continuam com a primeira; as duas são oficiais.

**Competências nunca conferidas.** Os 115 textos de competências (10 gerais e 105 específicas) não passavam pelo verificador. Conferidos agora, dois divergiam da planilha para o PDF: `cg-09` trazia "cooperação,fazendo-se" sem espaço (PDF 12, quebra de linha na vírgula) e `ef-comp-lp-ce-04` trazia a ligadura tipográfica U+FB02 em "ﬂuência" (PDF 89), que quebrava buscas por "fluência". **Decisão:** prevalece o PDF; o `cg-09` entra no mapa `CORRECOES_PDF` e as ligaduras são desfeitas na limpeza da planilha. As competências ganham `fonte.localizador_pdf` e entram em `verificacao.json`.

**Proveniência e campos sem definição.** A proveniência da EI dizia "601 p." (o PDF tem 600; off-by-one do `split('\f')`); os 10 componentes do EM sem habilidades próprias traziam `p. 33 (PDF da estrutura)` em página impressa, sem `localizador_pdf` (agora "página PDF 35", a página em que a BNCC nomeia os componentes dentro das áreas); `fonte.url_oficial` existia no schema e nunca foi preenchido (removido); `presenca` era `null` nos 8 componentes do EF presentes em todos os anos (agora explícito, `[1, …, 9]`); `vigencia.ate` não tinha formato definido (data-version, como `desde`, da revogação ou da alteração normativa).

**Ementas dos marcos legais.** Em 11 dos 20 registros, `ementa` misturava a ementa oficial com comentário do projeto (artigos relevantes, homologação, apelido "LDB"). **Decisão:** `ementa` passa a trazer só a ementa oficial, transcrita da publicação no Planalto (conferida em 15/10/2026) ou do CNE; é `null` na Constituição, que não tem ementa, e traz o assunto nos pareceres, que também não têm. O comentário vai para `nota`. Mudança de schema aditiva (`schema-v1.1.0`): `ementa` anulável, `nota` definida, `url_oficial` removido de `fonte`, formato de `vigencia.desde` e `ate` fixado por padrão.

**Afirmação "a numeração tem lacunas legítimas".** Não se sustenta nos dados: agrupando os códigos por decodificação, a sequência é contínua a partir de 01 em todos os 120 grupos (contratos 5b e 8c). O sentido pretendido é outro: nem todo código bem formado existe. A frase correta é "um código bem formado que não está nos dados não existe na BNCC". Os textos deste repositório já usam essa forma; os pacotes, o servidor MCP e o site (25 arquivos) são corrigidos nos repositórios deles.

*Fonte: duas verificações independentes de 14/10/2026 × PDF homologado (páginas 12, 28, 31, 35, 50, 89, 144, 146, 160, 166, 264, 335, 348) × anexo de Computação (páginas 56 e 58) × ementas oficiais no Planalto (15/10/2026). Reprodução completa do pipeline: 1.580 aprendizagens e 115 competências ok, 141/141 em Computação.*

## Versões das fontes (contexto das decisões)

- Planilhas oficiais: exportadas de downloadbncc.mec.gov.br em 23/06/2023 (a ferramenta de exportação estava fora do ar em 09/07/2026, backend respondendo 503).
- PDF canônico: `Base-Nacional-Comum-Curricular-BNCC.pdf`, versão completa homologada (600 páginas). Atenção: o arquivo distribuído na página do Ensino Médio do site do MEC é o rascunho pré-homologação de 2018, com textos e numeração diferentes dos finais; ele não serve para verificação.
- Checksums em `fontes/README.md`.
