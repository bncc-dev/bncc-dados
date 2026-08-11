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

## Versões das fontes (contexto das decisões)

- Planilhas oficiais: exportadas de downloadbncc.mec.gov.br em 23/06/2023 (a ferramenta de exportação estava fora do ar em 09/07/2026, backend respondendo 503).
- PDF canônico: `Base-Nacional-Comum-Curricular-BNCC.pdf`, versão completa homologada (600 páginas). Atenção: o arquivo distribuído na página do Ensino Médio do site do MEC é o rascunho pré-homologação de 2018, com textos e numeração diferentes dos finais; ele não serve para verificação.
- Checksums em `fontes/README.md`.
