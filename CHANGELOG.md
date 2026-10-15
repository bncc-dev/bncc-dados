# Changelog

Categorias: `normativa` (mudança nas normas oficiais) · `correcao` (erro nosso corrigido) · `schema` (formato) · `editorial` (docs, pipeline, sem mudança de dado).

## [dados-2026.08] — 2026-10-15

### Dados
- **Onze ids removidos por defeito de extração** (nove contextos de organização do EF e dois objetos de conhecimento de Computação) (`correcao`, decisão 14 do DECISOES.md): quatro objetos de conhecimento do EF partidos em dois pela quebra de linha da célula (Ciências EF07CI12 a EF07CI16, Língua Inglesa EF09LI16, Língua Portuguesa EF67LP10, EF69LP47 e EF69LP48), a variante de "Oralidade" com a nota de rodapé no nome (EF69LP10 a EF69LP12) e os dois objetos "(cont.)" de Computação (EF09CO05, marcador de continuação do quadro no anexo). O mapa completo id antigo → id novo está na decisão 14. Contextos do EF: 879 → 873 (objetos 780 → 775); objetos de Computação: 61 → 59. A unidade temática de LI `…-pos-escrita` mantém o id e corrige o nome ("pós- escrita" → "pós-escrita").
- **Seis páginas de verificação corrigidas** (`correcao`): EI01TS01, EI02TS01 e EI03TS01 apontavam a página PDF 28 e EF01CI02 a EF01CI04 a página 31, exemplos ilustrativos do capítulo "Estrutura"; agora apontam os quadros normativos (50 e 335). O verificador ignora o capítulo.
- **Competências verificadas contra o PDF** (`correcao`): os 115 textos de competências entram na verificação e ganham `fonte.localizador_pdf`. Dois corrigidos: `cg-09` ("cooperação,fazendo-se" → "cooperação, fazendo-se") e `ef-comp-lp-ce-04` (ligadura "ﬂ" → "fl").
- **Proveniência** (`correcao`): EI com "600 p." em vez de "601 p."; os 10 componentes do EM sem habilidades próprias com `proveniencia`, `localizador` "página PDF 35" e `localizador_pdf`, em vez de "p. 33 (PDF da estrutura)"; `presenca` explícita (`[1, …, 9]`) nos 8 componentes do EF presentes em todos os anos.
- **Marcos legais** (`correcao`): `ementa` passa a trazer só a ementa oficial (transcrita do Planalto ou do CNE; `null` na Constituição, que não tem ementa; nos três pareceres do CNE, o campo "ASSUNTO" do cabeçalho) e o comentário do projeto vai para `nota`, em 11 registros. A nota do Parecer CNE/CEB 2/2022 deixa de falar em "futuro módulo de Computação".

### Schema
- `schema-v1.1.0` (aditiva): `marcos_legais[].ementa` anulável e `nota` definida como comentário do projeto; `fonte.url_oficial` removido (nunca preenchido); `vigencia.desde` e `vigencia.ate` com padrão `dados-AAAA.MM[.N]`, e `ate` definido como a data-version da revogação ou da alteração normativa.

### Editorial
- **Versão no metadado dos derivados** (`editorial`): `meta.data_version` do SQLite vinha do `vigencia.desde` do primeiro registro e dizia `dados-2026.07` mesmo no patch `.07.1`. Agora vem de `version` no `CITATION.cff`, fonte única da versão da release. `schema_version` passa a `schema-v1.1.0`.
- **Derivados** (`editorial`): `objetivos-ei.csv` ganha `fonte_localizador_pdf`, como os outros CSVs de aprendizagens; os CSVs de competências ganham a mesma coluna. Tag `dados-2026.08`, release no GitHub e depósito no Zenodo (DOI da versão `10.5281/zenodo.23403987`) feitos em 15/10/2026.
- Referências soltas a documentos que não estão no repositório ("schema doc §10", "§7.1", "schema v0.3", "análise de fontes §8.5") removidas de schemas e scripts; docstring do `extrair_ei.py` atualizada (cinco campos, PDF homologado).
- **Numeração contínua, não "lacunas legítimas"** (`editorial`): o `AGENTS.md` e o modelo de dados afirmavam que a numeração da BNCC 2018 tem lacunas. Não tem: decodificando cada código (etapa, anos ou grupo etário, componente ou área + competência), todos os grupos vão de 1 a n. A impressão de lacuna vem dos códigos de EM, em que a centena é a competência (`EM13LGG105` → `EM13LGG201`). O contrato 5b do `validar.py` passa a provar a continuidade na BNCC 2018, como o 8c já fazia para Computação. Sem mudança de dado.
- **Planilhas de apoio de Pernambuco fora do repositório** (`editorial`, decisão 13 do DECISOES.md): `fontes/computacao-estrutura.json`, mapa de estrutura produzido pelo projeto, substitui as quatro planilhas da Secretaria de Educação de PE, que não tinham licença explícita de redistribuição. A leitura das planilhas foi para `pipeline/gerar_mapa_computacao.py`, e `pipeline/extrair_computacao.py` passa a ler só o mapa e o anexo oficial. `dados/` sai idêntico; nos derivados muda só o metadado `fontes_sha256_16`, que agora lista o mapa.
- **Documentação em inglês** (`editorial`): `README.en.md`, `docs/en/` (modelo de dados, metodologia, versionamento, instalação, política de conteúdo, divisão aberto/comercial e resumo das decisões), `fontes/README.en.md` e versões em inglês de CONTRIBUTING, CODE_OF_CONDUCT e SECURITY.
- **Dicionário de dados** (`editorial`): `docs/dicionario-de-dados.md` e `docs/en/data-dictionary.md` descrevem cada campo de cada arquivo (tipo, obrigatoriedade, significado, valores e exemplo real), cobrindo todos os caminhos dos JSON Schemas. O português segue como versão de referência.
- **Política de conteúdo** (`editorial`): `docs/politica-de-conteudo.md` descreve o que o dataset distribui, como erros e conteúdo indevido são identificados, reportados e corrigidos, e os prazos-alvo.
- **Código de conduta** (`editorial`): nova seção sobre crianças e adolescentes (sem dado de estudante em issues, prioridade nas denúncias, canal por e-mail).
- **Titularidade e dependências** (`editorial`): copyright do `LICENSE` em nome da Profy Tecnologias Educacionais Ltda, titularidade explícita em `dados/LICENSE.md` (agora bilíngue), cidade da sede corrigida no `CITATION.cff`, `requirements.txt` com a dependência do pipeline e seções de dependências, formas de acesso e quem mantém no README.
- **Números de verificação atualizados** (`editorial`): README, `docs/metodologia.md` e o snapshot `docs/relatorio-validacao.md` ainda traziam 1.576/1.580, de antes da auditoria de 10/08/2026. O resultado vigente é 1.580/1.580.

## [dados-2026.07.1] — 2026-08-10

### Dados
- **11 textos corrigidos contra o PDF homologado** (`correcao`), a partir de auditoria independente de 10/08/2026 (três vias: duas determinísticas + visual, 100% dos registros) e conferência visual das páginas: EF03LP20 ("campopo lítico-cidadão" → "campo político-cidadão"), EF69LP46 e EF69LP34 (truncamentos — faltavam ~448 e ~55 caracteres finais), EF02MA06 (removido "ou convencionais", ausente do PDF), EF03MA05 (restaurado ", inclusive os convencionais,"), EM13LP35 (restaurado o "de" em "quantidade de texto"), EF89LP19 e EF69AR16 (pontos finais), EF03LP11, EF04LP01 e EF69LP48 (artefatos de hifenização: "gráfico- visuais" → "gráfico-visuais", "fonema--grafema" → "fonema-grafema", "gráfico- espacial" → "gráfico-espacial"). Verificação após correção: **1.580/1.580 ok**. Decisão 12 do DECISOES.md; decisão 4 parcialmente revista (EF02MA06).

### Editorial
- Verificador (`pipeline/verificar.py`) reformado: compara a continuação do PDF após o fim do texto do dataset (elimina o ponto cego de prefixo que deixava truncamentos passarem) e o fallback de hifenização não aprova mais silenciosamente — exige conferência visual registrada (`CONFERIDOS_VISUALMENTE`, com página e motivo).
- Extrator (`pipeline/extrair.py`) ganhou a camada `CORRECOES_PDF`: as correções planilha → PDF homologado agora são aplicadas de forma reproduzível na extração, em vez de editadas à mão no dado.
- Contagem de páginas do PDF canônico corrigida na documentação: 600, não 601 (off-by-one do `split('\f')` do pdftotext).
- Derivados (SQLite, SQL, CSVs) regenerados.

## [dados-2026.07] — 2026-07-27

### Dados
- Dataset inicial completo: 1.580 aprendizagens (EI 93, EF 1.304, EM 183), 10 competências gerais, 105 competências específicas, 885 contextos de organização e espinha estrutural.
- Verificação contra o PDF homologado: 1.576/1.580 idênticos; 4 divergências entre fontes oficiais documentadas em DECISOES.md.
- Completude provada por varredura de códigos no PDF (1.580 = 1.580).
- Marcos legais mínimos: 20 atos normativos (Constituição de 1988 a Lei nº 14.945/2024) com ementa, URL oficial verificada (acervo atual do CNE em gov.br/mec; o portal.mec.gov.br legado saiu do ar) e relações tipadas com entidades do dataset.
- Vocabulário de perfis: professor, aluno, gestor, responsável, coordenador, com sinônimos.
- **Complemento de Computação** (`normativa`): novo documento curricular `computacao-2022` (anexo ao Parecer CNE/CEB 2/2022, Resolução CNE/CEB 1/2022) com 141 aprendizagens (11 EI, 104 EF, 26 EM), 3 eixos, 61 objetos de conhecimento (com hierarquia) e 14 competências. Estrutura extraída das planilhas de apoio da Sec. de Educação de PE; **todos os textos verificados caractere a caractere contra o anexo oficial** (141/141 idênticos). Decisões 9 e 10 do DECISOES.md (inclui a canonização do EF05CO011 → EF05CO11, typo do documento oficial). Total do dataset: **1.721 aprendizagens**.

### Schema
- JSON Schemas draft 2020-12 para os 6 arquivos de dados (`schema-v1.0.0-rc`), incluindo marcos legais e perfis.

### Editorial
- Pipeline reprodutível com CI (extração, verificação, validação, derivados).
- Derivados SQLite e CSV gerados e conferidos.
- Documentação: modelo de dados, metodologia, versionamento, contribuição.
- Preparação para abertura: `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1 em pt-BR), `SECURITY.md`, `CITATION.cff` e templates de issue e PR, com o template de correção exigindo fonte oficial como campo obrigatório.

- Revisão pedagógica (Equipe Pedagógica Profy, 07/2026): os 32 alinhamentos da Educação Infantil percorridos, heurística de pareamento sequencial confirmada sem apontamentos; amostra do módulo de Computação revisada, também sem apontamentos. Registro em `docs/metodologia.md` e na decisão 5 do `DECISOES.md`.

### Schema
- `schema-v1.0.0`: formato estável; o sufixo `-rc` sai com esta release.
