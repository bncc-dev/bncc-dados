**Português** · [English](en/data-dictionary.md)

# Dicionário de dados

Este dicionário descreve todos os campos dos arquivos de dados do bncc.dev: os seis arquivos de dados de `dados/bncc-2018/`, o de `dados/computacao-2022/` e os dois relatórios de verificação (`verificacao.json`), descritos ao final. Para cada campo, informa o tipo, se é obrigatório, o significado e um exemplo real.

- Os arquivos JSON em [`dados/`](../dados/) são a fonte canônica. O SQLite e os CSVs de [`derivados/`](../derivados/) são gerados a partir deles.
- Tipo e obrigatoriedade vêm dos [JSON Schemas](../schema/) (draft 2020-12, formato `schema-v1.1.0`).
- Os nomes de campo estão em português e são identificadores estáveis. Não os traduza no código que consome os dados.
- As entidades e as decisões de modelagem estão explicadas no [Modelo de dados](modelo-de-dados.md). As decisões sobre inconsistências das fontes oficiais estão em [DECISOES.md](../DECISOES.md).

## Como ler as tabelas

- **Campo**: caminho completo a partir da raiz do arquivo. `[]` indica um item de lista. Exemplo: `habilidades[].fonte.localizador_pdf` é o campo `localizador_pdf` do objeto `fonte` de cada item da lista `habilidades`.
- **Tipo**: tipo JSON definido no schema. Entre parênteses, o tipo nomeado de `schema/definicoes.json` (ex.: `id_slug`). `enum` e `const` indicam valores fixos. "ou `null` (anulável)" marca os campos que aceitam `null`.
- **Obrigatório**: "sim" quando o schema exige o campo (lista `required`); "não" quando ele pode faltar. Em listas com variantes (`oneOf`), a condição aparece entre parênteses.
- **Exemplo**: valor real copiado dos dados. Textos longos foram encurtados com "…".
- `fonte` e `vigencia` aparecem em muitas coleções. Os campos internos deles são descritos uma vez, em [Estruturas comuns](#estruturas-comuns).
- Todos os objetos dos schemas usam `additionalProperties: false`: nenhum registro pode ter campos além dos listados aqui.
- Cada arquivo é um objeto JSON cujas chaves são as coleções listadas na seção do arquivo. Todas as coleções são obrigatórias.
- Páginas: "p. 26" é o número impresso na página do documento. "página PDF 28" é a posição da página no arquivo PDF, contada a partir de 1. No PDF homologado da BNCC, a página impressa 26 é a página PDF 28.

## Estruturas comuns

### Identificadores e textos

Tipos definidos em `schema/definicoes.json` e usados em todos os arquivos.

- **`id_slug`**: string com o padrão `^[a-z0-9]+(-[a-z0-9]+)*$` (letras minúsculas sem acento, números e hífens). Identificador cunhado pelo projeto para entidades sem código oficial. É estável e não muda depois de publicado. Exemplo: `ef-comp-lp-prat-leitura`.
- **`documento_ref`**: string com o mesmo padrão de `id_slug`. Referência ao `id` de um item de `documento_curricular` (em `estrutura.json`). Valores nos dados: `bncc-2018` e `computacao-2022`.
- **`texto_normativo`**: string com no mínimo 10 caracteres. Enunciado oficial, copiado do documento oficial e conferido contra ele. Nunca vazio, nunca inventado.
- **`documento`** (campo presente em quase todos os registros, fora de `fonte`): documento curricular a que o registro pertence (`documento_ref`). Vale `bncc-2018` em `estrutura.json`, `educacao-infantil.json`, `ensino-fundamental.json` e `ensino-medio.json`, e `computacao-2022` em `computacao.json`.

### Códigos oficiais

O campo `codigo` das aprendizagens guarda o código oficial, que é a chave primária do registro. Cada tipo de código tem um padrão no schema:

- `codigo_ei`: `^EI0[123](EO|CG|TS|EF|ET)[0-9]{2}$`. Exemplo: `EI02TS01`.
- `codigo_ef`: `^EF(0[1-9]|15|69|12|35|67|89)(AR|CI|EF|ER|GE|HI|LI|LP|MA)[0-9]{2}$`. Exemplo: `EF67LP08`.
- `codigo_em`: `^EM13((LGG|MAT|CNT|CHS)[0-9]{3}|LP[0-9]{2})$`. Exemplos: `EM13LGG103`, `EM13LP02`.
- `codigo_computacao_ei`: `^EI03CO[0-9]{2}$`. Exemplo: `EI03CO01`.
- `codigo_computacao_ef`: `^EF(0[1-9]|15|69)CO[0-9]{2}$`. Exemplo: `EF06CO02`.
- `codigo_computacao_em`: `^EM13CO[0-9]{2}$`. Exemplo: `EM13CO07`.

Como ler cada parte do código (função de referência: `pipeline/codigos.py`):

- **EI** (`EI02TS01`): `EI` + grupo etário (`01` bebês, `02` crianças bem pequenas, `03` crianças pequenas) + campo de experiências (`EO` O eu, o outro e o nós; `CG` Corpo, gestos e movimentos; `TS` Traços, sons, cores e formas; `EF` Escuta, fala, pensamento e imaginação; `ET` Espaços, tempos, quantidades, relações e transformações) + sequência de 2 dígitos.
- **EF** (`EF67LP08`): `EF` + ano (`01` a `09`) ou bloco de anos (`15` = 1º ao 5º, `69` = 6º ao 9º, `12` = 1º e 2º, `35` = 3º ao 5º, `67` = 6º e 7º, `89` = 8º e 9º) + componente (`AR` Arte, `CI` Ciências, `EF` Educação Física, `ER` Ensino Religioso, `GE` Geografia, `HI` História, `LI` Língua Inglesa, `LP` Língua Portuguesa, `MA` Matemática) + sequência de 2 dígitos.
- **EM** (`EM13LGG103`): `EM` + `13` (sem seriação) + área (`LGG` Linguagens e suas Tecnologias, `MAT` Matemática e suas Tecnologias, `CNT` Ciências da Natureza e suas Tecnologias, `CHS` Ciências Humanas e Sociais Aplicadas) + 3 dígitos: o primeiro é o número da competência específica da área, os outros dois são a sequência. Língua Portuguesa usa `EM13LP` + sequência de 2 dígitos, sem dígito de competência.
- **Computação** (componente `CO`): `EI03CO` + sequência (só pré-escola); `EF` + ano (`01` a `09`) ou bloco (`15`, `69`) + `CO` + sequência; `EM13CO` + sequência, sem dígito de competência.
- Cuidados: o segmento `EF` pode significar a etapa, um campo de experiências ou Educação Física, e a posição desfaz a ambiguidade. A numeração sequencial não indica ordem pedagógica nem completude. Um código bem formado que não está nos dados não existe na BNCC.

### Siglas de etapa

Valores usados em `etapas[].id`, nos campos `etapa`, em `modalidades[].transversal_a` e em `marcos_legais[].relaciona[].entidade`:

- `EI`: Educação Infantil.
- `EF`: Ensino Fundamental.
- `EM`: Ensino Médio.

### `fonte`

Proveniência do registro: documento oficial e localizadores. É a cadeia de auditoria de cada registro. Só `documento` é obrigatório; os demais subcampos aparecem conforme a coleção (tabela abaixo).

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|---|---|---|---|---|
| `fonte` | object | depende da coleção | Objeto de proveniência. Se é obrigatório ou não está indicado na linha `fonte` de cada coleção. | `{"documento": "bncc-2018", "arquivo": "BNCC_Ensino Fundamental.xlsx", …}` |
| `fonte.documento` | string (`documento_ref`) | sim | Documento curricular de origem do registro. | `"bncc-2018"` |
| `fonte.arquivo` | string | não | Nome do arquivo oficial de origem, arquivado em [`fontes/`](../fontes/). Valores nos dados: `BNCC_Ensino Fundamental.xlsx` e `BNCC_Ensino_Medio.xlsx` (planilhas oficiais do MEC), `Base-Nacional-Comum-Curricular-BNCC.pdf` (PDF homologado da BNCC) e `anexo-ao-parecer-cneceb-no-2-2022-bncc-computacao.pdf` (anexo de Computação). | `"BNCC_Ensino Fundamental.xlsx"` |
| `fonte.proveniencia` | string | não | Como e quando a fonte foi obtida, ou como o registro foi montado. Texto livre. | `"exportada de downloadbncc.mec.gov.br em 23/06/2023"` |
| `fonte.localizador` | string | não | Onde o registro está no material de onde foi extraído. Formatos nos dados: `aba <nome>, linha <n>` (planilhas do MEC; competências e contextos de organização trazem só a aba); `página PDF <n>` (EI, extraída do PDF homologado, e os 10 componentes do EM sem aprendizagens próprias, nomeados na página PDF 35); `<planilha> · linha <n>` (computacao-2022: planilha de apoio da Secretaria de Educação de Pernambuco de onde veio a estrutura, que não está mais no repositório, ver decisão 13 do DECISOES.md). | `"aba Língua Portuguesa, linha 229"` |
| `fonte.localizador_pdf` | string | não | Página do documento oficial em que o texto do registro foi conferido. É a posição da página no arquivo PDF, não o número impresso. BNCC 2018: `Base-Nacional-Comum-Curricular-BNCC.pdf, página PDF <n>`. computacao-2022: `página PDF <n>`, no anexo indicado em `fonte.arquivo`. Presente em todas as aprendizagens, nas 115 competências da BNCC 2018 e nos 10 componentes do EM sem aprendizagens próprias. Nunca aponta para o capítulo "Estrutura" do PDF (páginas 25 a 36), que só traz exemplos ilustrativos. | `"Base-Nacional-Comum-Curricular-BNCC.pdf, página PDF 167"` |

Subcampos de `fonte` preenchidos em cada coleção:

| Arquivo e coleção | Subcampos preenchidos |
|---|---|
| `estrutura.json`: `componentes_curriculares` (10 de 21 itens) | `documento`, `arquivo`, `proveniencia`, `localizador`, `localizador_pdf` |
| `estrutura.json`: `competencias_gerais`, `competencias_especificas` | `documento`, `arquivo`, `proveniencia`, `localizador`, `localizador_pdf` |
| `educacao-infantil.json`: `objetivos` | `documento`, `arquivo`, `proveniencia`, `localizador`, `localizador_pdf` |
| `ensino-fundamental.json` e `ensino-medio.json`: `habilidades` | `documento`, `arquivo`, `proveniencia`, `localizador`, `localizador_pdf` |
| `ensino-fundamental.json` e `ensino-medio.json`: `contextos_organizacao` | `documento`, `arquivo`, `proveniencia`, `localizador` |
| `computacao.json`: `competencias` | `documento`, `arquivo`, `proveniencia` |
| `computacao.json`: `objetivos_ei`, `habilidades_ef`, `habilidades_em` | `documento`, `arquivo`, `proveniencia`, `localizador`, `localizador_pdf` |

### `vigencia`

Ciclo de vida normativo do registro. Presente, e obrigatório, em todas as aprendizagens: objetivos da EI, habilidades do EF e do EM e as três listas de aprendizagens de Computação. Regras do projeto ([versionamento.md](versionamento.md)): registro publicado nunca é apagado e código nunca é reutilizado.

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|---|---|---|---|---|
| `vigencia` | object | sim (em todas as aprendizagens) | Objeto de vigência do registro. | `{"status": "vigente", "desde": "dados-2026.07", "ate": null}` |
| `vigencia.status` | enum | sim | Situação normativa. `vigente`: em vigor. `alterado`: registro alterado por mudança normativa. `revogado`: revogado; o registro continua no dataset e `ate` é preenchido. Todos os registros desta versão são `vigente`. Use para filtrar: aplicações não deveriam sugerir aprendizagens revogadas. | `"vigente"` |
| `vigencia.desde` | string (padrão `dados-AAAA.MM` ou `dados-AAAA.MM.N`) | sim | Data-version (versão do conteúdo do dataset) em que o registro entrou no dataset. Não é a data do ato normativo: os registros de Computação, de norma de 2022, também trazem `dados-2026.07`. Um patch de correção não muda o `desde` de quem já estava no dataset. | `"dados-2026.07"` |
| `vigencia.ate` | string (mesmo padrão de `desde`) ou `null` (anulável) | sim | Fim da vigência. `null` enquanto o registro está vigente. Quando preenchido, é a data-version em que o registro deixou de valer tal como está: a da revogação (`status` = `revogado`) ou a da alteração normativa (`status` = `alterado`); o texto permanece o da última versão vigente. Todos os registros desta versão têm `null`. | `null` |

## `dados/bncc-2018/estrutura.json`

A espinha estrutural do dataset: documentos curriculares, etapas, modalidades, áreas, componentes, recortes temporais, campos de experiências, direitos de aprendizagem e competências gerais e específicas.

### `documento_curricular`

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|---|---|---|---|---|
| `documento_curricular` | array (mínimo 1 item) | sim | Documentos curriculares de onde vêm os registros. É a raiz de proveniência: todo campo `documento` aponta para um `id` desta lista. 2 itens nos dados. | `[{"id": "bncc-2018", …}, {"id": "computacao-2022", …}]` |
| `documento_curricular[].id` | string (`id_slug`) | sim | Identificador do documento. | `"computacao-2022"` |
| `documento_curricular[].nome` | string | sim | Nome do documento. | `"Computação na Educação Básica (complemento à BNCC)"` |
| `documento_curricular[].tipo` | enum | sim | Tipo do documento. `base_nacional`: a própria BNCC (`bncc-2018`). `complemento`: complemento à BNCC (`computacao-2022`). `curriculo_estadual`: currículo estadual. `curriculo_municipal`: currículo municipal. Os dois últimos não têm registros nesta versão; o modelo de dados prevê currículos estaduais futuros como novos documentos. | `"complemento"` |
| `documento_curricular[].esfera` | enum | sim | Esfera federativa do documento: `federal`, `estadual` ou `municipal`. Os dois documentos atuais são `federal`. | `"federal"` |
| `documento_curricular[].derivado_de` | string (`id_slug`) ou `null` (anulável) | sim | `id` do documento do qual este deriva. `null` no documento raiz (`bncc-2018`). | `"bncc-2018"` |

### `etapas`

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|---|---|---|---|---|
| `etapas` | array | sim | Etapas da educação básica. 3 itens nos dados. | `[{"id": "EI", "nome": "Educação Infantil"}, …]` |
| `etapas[].id` | enum (`EI`, `EF`, `EM`) | sim | Sigla da etapa (ver [Siglas de etapa](#siglas-de-etapa)). | `"EF"` |
| `etapas[].nome` | string | sim | Nome da etapa. | `"Ensino Fundamental"` |

### `modalidades`

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|---|---|---|---|---|
| `modalidades` | array | sim | Modalidades de ensino que atravessam etapas. 1 item nos dados: Educação de Jovens e Adultos (EJA). | `[{"id": "eja", …}]` |
| `modalidades[].id` | string (`id_slug`) | sim | Identificador da modalidade. | `"eja"` |
| `modalidades[].nome` | string | sim | Nome da modalidade. | `"Educação de Jovens e Adultos"` |
| `modalidades[].transversal_a` | array de enum (`EI`, `EF`, `EM`) | sim | Etapas que a modalidade atravessa. | `["EF", "EM"]` |
| `modalidades[].segmentos` | array de object | sim | Segmentos da modalidade. 3 na EJA. | `[{"id": "eja-1", "corresponde_a": "EF anos iniciais"}, …]` |
| `modalidades[].segmentos[].id` | string (`id_slug`) | sim | Identificador do segmento. | `"eja-2"` |
| `modalidades[].segmentos[].corresponde_a` | string | sim | Recorte da educação básica a que o segmento corresponde. Texto livre, não é referência a `id`. Valores nos dados: `"EF anos iniciais"`, `"EF anos finais"`, `"EM"`. | `"EF anos finais"` |

### `areas_conhecimento`

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|---|---|---|---|---|
| `areas_conhecimento` | array | sim | Áreas do conhecimento, por etapa. 9 itens: 5 do EF e 4 do EM. A EI não tem áreas: organiza-se por campos de experiências. | `[{"id": "ef-area-linguagens", …}, …]` |
| `areas_conhecimento[].id` | string (`id_slug`) | sim | Identificador da área. Nos dados: `ef-area-` + nome no EF; `em-area-` + sigla de área dos códigos (`lgg`, `mat`, `cnt`, `chs`) no EM. | `"em-area-lgg"` |
| `areas_conhecimento[].etapa` | enum (`EI`, `EF`, `EM`) | sim | Etapa da área. Nos dados aparecem só `EF` e `EM`. | `"EM"` |
| `areas_conhecimento[].nome` | string | sim | Nome oficial da área. | `"Linguagens e suas Tecnologias"` |
| `areas_conhecimento[].documento` | string (`documento_ref`) | sim | Documento curricular da área. | `"bncc-2018"` |

### `componentes_curriculares`

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|---|---|---|---|---|
| `componentes_curriculares` | array | sim | Componentes curriculares do EF e do EM. 21 itens: 9 do EF e 12 do EM. | `[{"id": "ef-comp-ar", …}, …]` |
| `componentes_curriculares[].id` | string (`id_slug`) | sim | Identificador do componente. Nos dados começa com `ef-comp-` ou `em-comp-`. | `"ef-comp-li"` |
| `componentes_curriculares[].etapa` | enum (`EF`, `EM`) | sim | Etapa do componente. | `"EF"` |
| `componentes_curriculares[].nome` | string | sim | Nome do componente. | `"Língua Inglesa"` |
| `componentes_curriculares[].sigla_codigo` | string ou `null` (anulável) | não | Sigla do componente dentro dos códigos das habilidades (ex.: `LP` em `EF67LP08` e em `EM13LP02`). `null` quando o componente não tem sigla própria nos códigos: todos os do EM, exceto Língua Portuguesa. | `"LI"` |
| `componentes_curriculares[].area` | string (`id_slug`) | sim | `id` da área do conhecimento (`areas_conhecimento[].id`) a que o componente pertence. | `"ef-area-linguagens"` |
| `componentes_curriculares[].tem_aprendizagens_proprias` | boolean | sim | `true` quando o componente tem habilidades próprias no dataset. `false` em 10 componentes do EM (Arte, Educação Física, Língua Inglesa, Biologia, Física, Química, História, Geografia, Sociologia e Filosofia): no EM, as habilidades desses componentes são definidas por área (BNCC, página PDF 35). | `false` |
| `componentes_curriculares[].presenca` | object ou `null` (anulável) | não | Anos do EF em que o componente está presente. Presente nos 9 componentes do EF: Língua Inglesa com `[6, 7, 8, 9]` (BNCC, anos finais) e os outros 8 com `[1, 2, 3, 4, 5, 6, 7, 8, 9]`. Nos componentes do EM o campo não aparece, porque o EM não tem seriação. | `{"anos": [6, 7, 8, 9]}` |
| `componentes_curriculares[].presenca.anos` | array de integer (1 a 9) | sim (dentro de `presenca`) | Anos do EF (1º ao 9º) em que o componente aparece. | `[6, 7, 8, 9]` |
| `componentes_curriculares[].destaque_legal` | string | não | Ato legal que dá destaque ao componente. Presente em Língua Portuguesa e Matemática do EM: a Lei nº 13.415/2017 torna obrigatórios os estudos e práticas desses componentes nos três anos do EM (registro `lei-13415-2017` em `marcos-legais.json`). | `"Lei nº 13.415/2017"` |
| `componentes_curriculares[].nota` | string | não | Observação do projeto sobre o componente. Presente só em `em-comp-mat`. | `"detalhamento coincide com a área (componente único)"` |
| `componentes_curriculares[].fonte` | object ([`fonte`](#fonte)) | não | Proveniência. Presente só nos 10 componentes do EM sem aprendizagens próprias: a página PDF 35 (impressa 33), em que a BNCC nomeia os componentes de cada área do EM. | `{"documento": "bncc-2018", "arquivo": "Base-Nacional-Comum-Curricular-BNCC.pdf", "proveniencia": "BNCC completa homologada (600 p.), obtida em 09/07/2026", "localizador": "página PDF 35", "localizador_pdf": "Base-Nacional-Comum-Curricular-BNCC.pdf, página PDF 35"}` |

### `recortes_temporais`

Cada item segue uma de três variantes, definidas por `tipo`: `grupo_etario` (EI), `ano` (EF) ou `sem_seriacao` (EM).

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|---|---|---|---|---|
| `recortes_temporais` | array | sim | Recortes de tempo de cada etapa. 13 itens: 3 grupos etários (EI), 9 anos (EF) e 1 recorte sem seriação (EM). | `[{"id": "ei-grupo-01", …}, …]` |
| `recortes_temporais[].id` | string (`id_slug`) | sim | Identificador. Nos dados: `ei-grupo-01` a `ei-grupo-03`, `ef-ano-01` a `ef-ano-09` e `em-sem-seriacao`. O campo `grupo_etario` dos objetivos da EI aponta para os ids `ei-grupo-*`. | `"ei-grupo-02"` |
| `recortes_temporais[].etapa` | const (`EI`, `EF` ou `EM`, conforme a variante) | sim | Etapa do recorte. | `"EI"` |
| `recortes_temporais[].tipo` | const (`grupo_etario`, `ano` ou `sem_seriacao`, conforme a variante) | sim | Tipo de recorte. `grupo_etario`: faixa de idade da EI. `ano`: ano escolar do EF. `sem_seriacao`: o EM não divide as habilidades por ano; a progressão é definida pelos currículos. | `"grupo_etario"` |
| `recortes_temporais[].nome` | string | sim (se `tipo` = `grupo_etario`) | Nome do grupo etário. Só existe nessa variante. | `"Crianças bem pequenas"` |
| `recortes_temporais[].faixa` | string | sim (se `tipo` = `grupo_etario`) | Faixa de idade, em anos (`a`) e meses (`m`). Bebês: de 0 a 1 ano e 6 meses. Crianças bem pequenas: de 1 ano e 7 meses a 3 anos e 11 meses. Crianças pequenas: de 4 anos a 5 anos e 11 meses (BNCC, página PDF 28). O separador entre os limites é o caractere U+2013; no exemplo ele aparece como escape JSON. | `"1a7m\u20133a11m"` |
| `recortes_temporais[].numero` | integer (1 a 9) | sim (se `tipo` = `ano`) | Número do ano do EF. | `6` |
| `recortes_temporais[].segmento` | enum | sim (se `tipo` = `ano`) | Segmento do EF. `anos_iniciais`: 1º ao 5º ano. `anos_finais`: 6º ao 9º ano. | `"anos_finais"` |
| `recortes_temporais[].nota` | string | não (só na variante `sem_seriacao`) | Observação sobre o recorte. | `"habilidades sem seriação; progressão definida pelos currículos (BNCC p. 32, 34)"` |

### `campos_experiencias`

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|---|---|---|---|---|
| `campos_experiencias` | array | sim | Os 5 campos de experiências da EI, que organizam os objetivos de aprendizagem. | `[{"id": "ei-campo-eo", …}, …]` |
| `campos_experiencias[].id` | string (`id_slug`) | sim | Identificador: `ei-campo-` + sigla do campo nos códigos, em minúsculas (`eo`, `cg`, `ts`, `ef`, `et`). | `"ei-campo-ts"` |
| `campos_experiencias[].nome` | string | sim | Nome oficial do campo. | `"Traços, sons, cores e formas"` |
| `campos_experiencias[].documento` | string (`documento_ref`) | sim | Documento curricular. | `"bncc-2018"` |

### `direitos_aprendizagem`

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|---|---|---|---|---|
| `direitos_aprendizagem` | array | sim | Os 6 direitos de aprendizagem e desenvolvimento da EI definidos na BNCC (página PDF 40). Nenhum outro registro do dataset aponta para estes ids. | `[{"id": "ei-direito-conviver", …}, …]` |
| `direitos_aprendizagem[].id` | string (`id_slug`) | sim | Identificador: `ei-direito-` + nome. | `"ei-direito-conhecer-se"` |
| `direitos_aprendizagem[].nome` | string | sim | Nome do direito. | `"Conhecer-se"` |
| `direitos_aprendizagem[].documento` | string (`documento_ref`) | sim | Documento curricular. | `"bncc-2018"` |

### `competencias_gerais`

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|---|---|---|---|---|
| `competencias_gerais` | array (exatamente 10 itens) | sim | As 10 competências gerais da educação básica. | `[{"id": "cg-01", …}, …]` |
| `competencias_gerais[].id` | string (`id_slug`) | sim | Identificador: `cg-` + número com 2 dígitos. | `"cg-01"` |
| `competencias_gerais[].documento` | string (`documento_ref`) | sim | Documento curricular. | `"bncc-2018"` |
| `competencias_gerais[].tipo` | const `geral` | sim | Tipo da competência. Sempre `geral`. | `"geral"` |
| `competencias_gerais[].numero` | integer (1 a 10) | sim | Número da competência na BNCC. | `1` |
| `competencias_gerais[].texto` | string (`texto_normativo`) | sim | Enunciado oficial da competência. | `"Valorizar e utilizar os conhecimentos historicamente construídos sobre o mundo físico, social, cultural e digital …"` |
| `competencias_gerais[].fonte` | object ([`fonte`](#fonte)) | sim | Proveniência: aba "Competências gerais" da planilha oficial do EF. | `{"arquivo": "BNCC_Ensino Fundamental.xlsx", "localizador": "aba Competências gerais", …}` |

### `competencias_especificas`

Cada item segue uma de duas variantes, definidas por `tipo`: de área ou de componente.

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|---|---|---|---|---|
| `competencias_especificas` | array | sim | Competências específicas de área ou de componente, do EF e do EM. 105 itens: 56 de área e 49 de componente. As habilidades do EM apontam para as competências de área do EM. | `[{"id": "ef-area-linguagens-ce-01", …}, …]` |
| `competencias_especificas[].id` | string (`id_slug`) | sim | Identificador: `id` da área ou do componente + `-ce-` + número com 2 dígitos. | `"em-area-lgg-ce-01"` |
| `competencias_especificas[].documento` | string (`documento_ref`) | sim | Documento curricular. | `"bncc-2018"` |
| `competencias_especificas[].tipo` | const (`especifica_de_area` ou `especifica_de_componente`, conforme a variante) | sim | `especifica_de_area`: competência de uma área do conhecimento. `especifica_de_componente`: competência de um componente; só existe em áreas com mais de um componente (nos dados: Língua Portuguesa, Arte, Educação Física, Língua Inglesa, Geografia e História, todos do EF). | `"especifica_de_area"` |
| `competencias_especificas[].area` | string (`id_slug`) | sim (se `tipo` = `especifica_de_area`) | `id` da área (`areas_conhecimento[].id`). | `"em-area-lgg"` |
| `competencias_especificas[].componente` | string (`id_slug`) | sim (se `tipo` = `especifica_de_componente`) | `id` do componente (`componentes_curriculares[].id`). | `"ef-comp-lp"` |
| `competencias_especificas[].numero` | integer (mínimo 1) | sim | Número da competência dentro da área ou do componente. | `1` |
| `competencias_especificas[].texto` | string (`texto_normativo`) | sim | Enunciado oficial da competência. | `"Compreender o funcionamento das diferentes linguagens e práticas culturais (artísticas, corporais e verbais) …"` |
| `competencias_especificas[].fonte` | object ([`fonte`](#fonte)) | sim | Proveniência: aba de competências da planilha oficial do EF ou do EM. | `{"arquivo": "BNCC_Ensino_Medio.xlsx", "localizador": "aba Comp. de Linguagens e suas Tec", …}` |

## `dados/bncc-2018/educacao-infantil.json`

Os objetivos de aprendizagem da EI e os alinhamentos que ligam objetivos do mesmo aspecto entre os três grupos etários. A EI é extraída do PDF homologado, porque não há planilha oficial disponível.

### `objetivos`

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|---|---|---|---|---|
| `objetivos` | array (mínimo 1 item) | sim | Objetivos de aprendizagem da EI. 93 nos dados. | `[{"codigo": "EI01CG01", …}, …]` |
| `objetivos[].codigo` | string (`codigo_ei`) | sim | Código oficial, chave primária do registro (ver [Códigos oficiais](#códigos-oficiais)). | `"EI02TS01"` |
| `objetivos[].documento` | string (`documento_ref`) | sim | Documento curricular. | `"bncc-2018"` |
| `objetivos[].texto` | string (`texto_normativo`) | sim | Texto oficial do objetivo, conferido contra o PDF homologado. | `"Criar sons com materiais, objetos e instrumentos musicais, para acompanhar diversos ritmos de música."` |
| `objetivos[].campo_experiencias` | string (`id_slug`) | sim | `id` do campo de experiências (`campos_experiencias[].id` em `estrutura.json`). Corresponde à sigla de campo do código. | `"ei-campo-ts"` |
| `objetivos[].grupo_etario` | string (`id_slug`) | sim | `id` do grupo etário (`recortes_temporais[].id` em `estrutura.json`). Corresponde aos dígitos de grupo do código. | `"ei-grupo-02"` |
| `objetivos[].alinhamento` | string (`id_slug`) | sim | `id` do alinhamento (`alinhamentos[].id`) que liga este objetivo aos objetivos do mesmo aspecto nos outros grupos etários. | `"ei-align-ts-01"` |
| `objetivos[].vigencia` | object ([`vigencia`](#vigencia)) | sim | Vigência do registro. | `{"status": "vigente", "desde": "dados-2026.07", "ate": null}` |
| `objetivos[].fonte` | object ([`fonte`](#fonte)) | sim | Proveniência: página do PDF homologado de onde o texto foi extraído (`localizador`) e página onde foi conferido (`localizador_pdf`). | `{"localizador": "página PDF 49", "localizador_pdf": "Base-Nacional-Comum-Curricular-BNCC.pdf, página PDF 49", …}` |

### `alinhamentos`

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|---|---|---|---|---|
| `alinhamentos` | array | sim | Progressão horizontal oficial: objetivos do mesmo aspecto entre grupos etários (BNCC p. 26). O dataset pareia os objetivos pelo número sequencial do código, heurística confirmada em revisão pedagógica (decisão 5 do DECISOES.md). 32 itens. | `[{"id": "ei-align-cg-01", …}, …]` |
| `alinhamentos[].id` | string (`id_slug`) | sim | Identificador: `ei-align-` + sigla do campo + número sequencial. | `"ei-align-ts-01"` |
| `alinhamentos[].campo_experiencias` | string (`id_slug`) | sim | `id` do campo de experiências comum aos objetivos alinhados. | `"ei-campo-ts"` |
| `alinhamentos[].objetivos` | array de string (`codigo_ei`), 2 a 3 itens | sim | Códigos dos objetivos alinhados, um por grupo etário. Os 3 alinhamentos com 2 itens (`ei-align-eo-07`, `ei-align-et-07`, `ei-align-et-08`) refletem células vazias do quadro oficial. | `["EI01TS01", "EI02TS01", "EI03TS01"]` |
| `alinhamentos[].nota` | string | não | Registro de como o pareamento foi feito e revisado. | `"pareamento pela posição sequencial nn, confirmado em revisão pedagógica (07/2026)"` |

## `dados/bncc-2018/ensino-fundamental.json`

As habilidades do EF e os contextos de organização a que elas se referem: unidades temáticas, objetos de conhecimento, campos de atuação, práticas de linguagem e eixos.

### `habilidades`

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|---|---|---|---|---|
| `habilidades` | array (mínimo 1 item) | sim | Habilidades do EF. 1.304 nos dados. | `[{"codigo": "EF01LP01", …}, …]` |
| `habilidades[].codigo` | string (`codigo_ef`) | sim | Código oficial, chave primária do registro (ver [Códigos oficiais](#códigos-oficiais)). | `"EF67LP08"` |
| `habilidades[].documento` | string (`documento_ref`) | sim | Documento curricular. | `"bncc-2018"` |
| `habilidades[].texto` | string (`texto_normativo`) | sim | Texto oficial da habilidade, conferido contra o PDF homologado. | `"Identificar os efeitos de sentido devidos à escolha de imagens estáticas, sequenciação ou sobreposição de imagens, …"` |
| `habilidades[].componente` | string (`id_slug`) | sim | `id` do componente curricular (`componentes_curriculares[].id` em `estrutura.json`). É sempre o componente decodificado do código. | `"ef-comp-lp"` |
| `habilidades[].anos` | array de integer (1 a 9), mínimo 1 item | sim | Anos do EF a que a habilidade se aplica, decodificados do código. Um bloco vira a lista de seus anos: `EF67` dá `[6, 7]`, `EF15` dá `[1, 2, 3, 4, 5]`. | `[6, 7]` |
| `habilidades[].organizacao` | object | sim | Como a habilidade está organizada no quadro oficial. Três variantes, definidas por `tipo`. O schema exige `campo_pratica` para Língua Portuguesa (`ef-comp-lp`) e `eixo` para Língua Inglesa (`ef-comp-li`). | `{"tipo": "campo_pratica", "campos_atuacao": ["ef-comp-lp-catu-campo-jornalistico-midiatico"], "pratica_linguagem": "ef-comp-lp-prat-leitura"}` |
| `habilidades[].organizacao.tipo` | const (`unidade_tematica`, `campo_pratica` ou `eixo`, conforme a variante) | sim | `unidade_tematica`: organizada por unidade temática (todos os componentes, exceto LP e LI; 825 habilidades). `campo_pratica`: campos de atuação e prática de linguagem (Língua Portuguesa; 391). `eixo`: eixo e unidade temática (Língua Inglesa; 88). | `"campo_pratica"` |
| `habilidades[].organizacao.unidade_tematica` | string (`id_slug`) | sim (se `tipo` = `unidade_tematica` ou `eixo`) | `id` da unidade temática em `contextos_organizacao` (`tipo` = `ut`). | `"ef-comp-ma-ut-numeros"` |
| `habilidades[].organizacao.campos_atuacao` | array de string (`id_slug`), mínimo 1 item | sim (se `tipo` = `campo_pratica`) | `id`s dos campos de atuação em `contextos_organizacao` (`tipo` = `catu`). Nos dados, cada habilidade tem exatamente 1. | `["ef-comp-lp-catu-campo-jornalistico-midiatico"]` |
| `habilidades[].organizacao.pratica_linguagem` | string (`id_slug`) | sim (se `tipo` = `campo_pratica`) | `id` da prática de linguagem em `contextos_organizacao` (`tipo` = `prat`). | `"ef-comp-lp-prat-leitura"` |
| `habilidades[].organizacao.eixo` | string (`id_slug`) | sim (se `tipo` = `eixo`) | `id` do eixo em `contextos_organizacao` (`tipo` = `eixo`). | `"ef-comp-li-eixo-eixo-oralidade"` |
| `habilidades[].objetos_conhecimento` | array de string (`id_slug`) | sim | `id`s dos objetos de conhecimento em `contextos_organizacao` (`tipo` = `oc`). Relação N:N. Objetos com nomes diferentes entre anos são entidades diferentes (decisão 6 do DECISOES.md). O schema não fixa mínimo; nos dados cada habilidade tem de 1 a 6. | `["ef-comp-lp-oc-efeitos-de-sentido-exploracao-da-multissemiose"]` |
| `habilidades[].vigencia` | object ([`vigencia`](#vigencia)) | sim | Vigência do registro. | `{"status": "vigente", "desde": "dados-2026.07", "ate": null}` |
| `habilidades[].fonte` | object ([`fonte`](#fonte)) | sim | Proveniência: aba e linha da planilha oficial do EF (`localizador`) e página do PDF homologado onde o texto foi conferido (`localizador_pdf`). | `{"localizador": "aba Língua Portuguesa, linha 229", "localizador_pdf": "Base-Nacional-Comum-Curricular-BNCC.pdf, página PDF 167", …}` |

### `contextos_organizacao`

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|---|---|---|---|---|
| `contextos_organizacao` | array | sim | Entidades de organização dos quadros do EF, apontadas pelas habilidades. 873 itens: 775 objetos de conhecimento, 77 unidades temáticas, 9 práticas de linguagem, 7 campos de atuação e 5 eixos. | `[{"id": "ef-comp-ar-oc-arte-e-tecnologia", …}, …]` |
| `contextos_organizacao[].id` | string (`id_slug`) | sim | Identificador: `id` do componente + `-` + `tipo` + `-` + nome em slug. | `"ef-comp-lp-prat-leitura"` |
| `contextos_organizacao[].tipo` | enum | sim | Tipo do contexto. `ut`: unidade temática. `oc`: objeto de conhecimento. `catu`: campo de atuação (só LP). `prat`: prática de linguagem (só LP). `eixo`: eixo (só LI). | `"prat"` |
| `contextos_organizacao[].nome` | string | sim | Nome da planilha oficial, com a célula normalizada: linhas partidas pela quebra de linha são reunidas, nota de rodapé e hífen de quebra são descartados (decisão 14). | `"Leitura"` |
| `contextos_organizacao[].componente` | string (`id_slug`) | sim | `id` do componente a que o contexto pertence. | `"ef-comp-lp"` |
| `contextos_organizacao[].fonte` | object ([`fonte`](#fonte)) | sim | Proveniência: aba da planilha oficial do EF, sem linha. | `{"arquivo": "BNCC_Ensino Fundamental.xlsx", "localizador": "aba Língua Portuguesa", …}` |

## `dados/bncc-2018/ensino-medio.json`

As habilidades do EM, sem seriação, e os campos de atuação social de Língua Portuguesa.

### `habilidades`

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|---|---|---|---|---|
| `habilidades` | array (mínimo 1 item) | sim | Habilidades do EM. 183 nos dados: 129 de área e 54 de Língua Portuguesa. | `[{"codigo": "EM13CHS101", …}, …]` |
| `habilidades[].codigo` | string (`codigo_em`) | sim | Código oficial, chave primária do registro (ver [Códigos oficiais](#códigos-oficiais)). | `"EM13LGG103"` |
| `habilidades[].documento` | string (`documento_ref`) | sim | Documento curricular. | `"bncc-2018"` |
| `habilidades[].texto` | string (`texto_normativo`) | sim | Texto oficial da habilidade, conferido contra o PDF homologado. | `"Analisar o funcionamento das linguagens, para interpretar e produzir criticamente discursos em textos de diversas semioses (visuais, verbais, sonoras, gestuais)."` |
| `habilidades[].area` | string (`id_slug`) | sim | `id` da área do conhecimento (`areas_conhecimento[].id` em `estrutura.json`). É sempre a área decodificada do código, nunca a aba da planilha (decisão 1 do DECISOES.md). As habilidades de LP pertencem a `em-area-lgg`. | `"em-area-lgg"` |
| `habilidades[].componente` | string (`id_slug`) ou `null` (anulável) | sim | `em-comp-lp` nas habilidades `EM13LP`; `null` nas habilidades de área. O schema exige `em-comp-lp` quando o código começa com `EM13LP`. | `null` |
| `habilidades[].competencias_especificas` | array de string (`id_slug`), mínimo 1 item | sim | `id`s das competências específicas de área (`competencias_especificas[].id` em `estrutura.json`). Habilidades de área: exatamente 1, decodificada do código (o schema limita a 1 quando `componente` é `null`). Habilidades de LP: 1 a n, da planilha oficial; nos dados, de 1 a 3 (decisão 7 do DECISOES.md). | `["em-area-lgg-ce-01"]` |
| `habilidades[].campos_atuacao_social` | array de string (`id_slug`), mínimo 1 item, ou `null` (anulável) | sim | Só nas habilidades de LP: `id`s dos campos de atuação social em `contextos_organizacao`, vindos da coluna da planilha oficial. `null` nas habilidades de área (o schema exige `null` quando `componente` é `null`). | `["em-comp-lp-catu-todos-os-campos-de-atuacao-social"]` |
| `habilidades[].seriacao` | `null` (const) | sim | Sempre `null`: o EM não tem seriação, e a progressão é definida pelos currículos (BNCC p. 32 e 34). | `null` |
| `habilidades[].vigencia` | object ([`vigencia`](#vigencia)) | sim | Vigência do registro. | `{"status": "vigente", "desde": "dados-2026.07", "ate": null}` |
| `habilidades[].fonte` | object ([`fonte`](#fonte)) | sim | Proveniência: aba e linha da planilha oficial do EM (`localizador`) e página do PDF homologado onde o texto foi conferido (`localizador_pdf`). | `{"localizador": "aba 'Hab. de Linguagens e suas Tecn', linha 6", "localizador_pdf": "Base-Nacional-Comum-Curricular-BNCC.pdf, página PDF 493", …}` |

### `contextos_organizacao`

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|---|---|---|---|---|
| `contextos_organizacao` | array | sim | Campos de atuação social de Língua Portuguesa do EM, apontados por `habilidades[].campos_atuacao_social`. 6 itens. | `[{"id": "em-comp-lp-catu-campo-artistico-literario", …}, …]` |
| `contextos_organizacao[].id` | string (`id_slug`) | sim | Identificador: `em-comp-lp-catu-` + nome em slug. | `"em-comp-lp-catu-campo-artistico-literario"` |
| `contextos_organizacao[].tipo` | const `catu` | sim | Sempre `catu` (campo de atuação). | `"catu"` |
| `contextos_organizacao[].nome` | string | sim | Nome da planilha oficial, com a célula normalizada: linhas partidas pela quebra de linha são reunidas, nota de rodapé e hífen de quebra são descartados (decisão 14). | `"Campo artístico-literário"` |
| `contextos_organizacao[].componente` | const `em-comp-lp` | sim | Sempre `em-comp-lp` (Língua Portuguesa do EM). | `"em-comp-lp"` |
| `contextos_organizacao[].fonte` | object ([`fonte`](#fonte)) | sim | Proveniência: aba "Hab. de Língua Portuguesa" da planilha oficial do EM, sem linha. | `{"arquivo": "BNCC_Ensino_Medio.xlsx", "localizador": "aba Hab. de Língua Portuguesa", …}` |

## `dados/bncc-2018/marcos-legais.json`

Referências aos atos normativos que fundamentam a BNCC e a educação básica: identificação, ementa, link oficial e relações com entidades do dataset. O texto integral dos atos não está incluído.

### `marcos_legais`

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|---|---|---|---|---|
| `marcos_legais` | array (mínimo 15 itens) | sim | Atos normativos. 20 nos dados. | `[{"id": "constituicao-1988", …}, …]` |
| `marcos_legais[].id` | string (`id_slug`) | sim | Identificador. Nos dados: tipo do ato, número e ano (ex.: `lei-9394-1996`, `resolucao-cne-cp-2-2017`). | `"lei-13415-2017"` |
| `marcos_legais[].tipo` | enum | sim | Tipo do ato. `constituicao`: Constituição Federal. `emenda_constitucional`: emenda à Constituição. `lei`: lei. `resolucao`: resolução (nos dados, todas do CNE). `parecer`: parecer (nos dados, todos do CNE). | `"lei"` |
| `marcos_legais[].titulo` | string (mínimo 10 caracteres) | sim | Título oficial do ato, com número e data. | `"Lei nº 13.415, de 16 de fevereiro de 2017"` |
| `marcos_legais[].ementa` | string (mínimo 20 caracteres) ou `null` (anulável) | sim | Ementa oficial do ato, transcrita da publicação oficial (Planalto para leis e emenda, CNE para resoluções), conferida em 15/10/2026. `null` na Constituição, que não tem ementa. Nos três pareceres do CNE, que também não têm ementa, traz o campo "ASSUNTO" do cabeçalho do parecer, transcrito literalmente do PDF do CNE (conferido em 15/10/2026). Comentário do projeto fica em `nota`. | `"Dispõe sobre o Estatuto da Criança e do Adolescente e dá outras providências."` |
| `marcos_legais[].url_oficial` | string (padrão `^https://[a-z0-9.-]+\.gov\.br/`) | sim | Link oficial do ato, sempre https em domínio gov.br. | `"https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2017/lei/l13415.htm"` |
| `marcos_legais[].nota` | string | não | Comentário do projeto: o que o ato significa para a educação básica e para este dataset (artigos e metas relevantes, homologação, apelidos como "LDB"). Nunca é texto normativo. Presente em 11 registros. | `"As metas 2, 3 e 7 e suas estratégias preveem a base nacional comum curricular."` |
| `marcos_legais[].relaciona` | array de object | sim | Vínculos tipados do ato com entidades do dataset. Pode ser vazia: `lei-8069-1990` e `lei-13146-2015` não têm vínculos. 28 vínculos no total. | `[{"entidade": "EM", "natureza": "altera"}, …]` |
| `marcos_legais[].relaciona[].entidade` | string (`id_slug`) ou enum (`EI`, `EF`, `EM`) | sim | Entidade vinculada: sigla de etapa ou `id` de entidade de `estrutura.json` (documento curricular, modalidade, área, componente ou competência específica). Valores nos dados: `bncc-2018`, `EI`, `EF`, `EM`, `eja`, `em-comp-lp`, `em-comp-mat`. | `"em-comp-lp"` |
| `marcos_legais[].relaciona[].natureza` | enum | sim | Natureza do vínculo. Valores na lista abaixo. | `"fundamenta_destaque"` |

Valores de `relaciona[].natureza`, com exemplos dos dados:

- `fundamenta`: o ato é fundamento legal da entidade. Ex.: Constituição de 1988 e Lei nº 9.394/1996 (LDB) para `bncc-2018`; Emenda Constitucional nº 59/2009 para `EI`, `EF` e `EM`.
- `fundamenta_destaque`: o ato fundamenta o `destaque_legal` do componente. Ex.: Lei nº 13.415/2017 para `em-comp-lp` e `em-comp-mat`.
- `institui`: o ato institui a entidade. Ex.: Resoluções CNE/CP nº 2/2017 e nº 4/2018 para `bncc-2018`.
- `abrange`: a entidade está no alcance do ato. Ex.: Resolução CNE/CP nº 2/2017 para `EI` e `EF`; Resolução CNE/CP nº 4/2018 para `EM`.
- `altera`: o ato altera as regras da entidade. Ex.: Leis nº 13.415/2017 e nº 14.945/2024 para `EM`.
- `diretrizes`: o ato fixa diretrizes curriculares para a entidade. Ex.: Resolução CNE/CEB nº 5/2009 (Diretrizes Curriculares Nacionais para a Educação Infantil) para `EI`.
- `complementa`: o ato complementa a entidade. Ex.: Parecer CNE/CEB nº 2/2022 e Resolução CNE/CEB nº 1/2022 (Computação) para `bncc-2018`.

## `dados/bncc-2018/perfis.json`

Vocabulário de referência dos papéis do ecossistema escolar, para aplicações que usam os dados. Não traz lógica de autorização.

### `perfis`

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|---|---|---|---|---|
| `perfis` | array (mínimo 5 itens) | sim | Papéis de referência. 5 nos dados: professor, aluno, gestor, responsável e coordenador. | `[{"id": "perfil-professor", …}, …]` |
| `perfis[].id` | string (`id_slug`, começando com `perfil-`) | sim | Identificador do papel. | `"perfil-professor"` |
| `perfis[].nome` | string (mínimo 3 caracteres) | sim | Nome do papel. | `"Professor"` |
| `perfis[].descricao` | string (mínimo 20 caracteres) | sim | Definição do papel. | `"Docente responsável por planejar, conduzir e avaliar o ensino dos componentes curriculares e das experiências de aprendizagem."` |
| `perfis[].sinonimos` | array de string (mínimo 3 caracteres cada) | sim | Outros nomes usados para o mesmo papel. | `["docente", "educador"]` |

## `dados/computacao-2022/computacao.json`

O complemento de Computação à BNCC (anexo ao Parecer CNE/CEB nº 2/2022, instituído pela Resolução CNE/CEB nº 1/2022): eixos, objetos de conhecimento, competências e 141 aprendizagens (11 objetivos da EI, 104 habilidades do EF e 26 do EM). Os textos são conferidos contra o anexo oficial; a estrutura vem do mapa `fontes/computacao-estrutura.json` (decisões 10 e 13 do DECISOES.md).

Tipos locais, definidos em `$defs` de `schema/computacao.schema.json`:

- `documento`: const `computacao-2022`. Todo campo `documento` deste arquivo tem esse valor.
- `eixo_ref`: enum com os 3 ids de eixo: `co-eixo-pensamento-computacional`, `co-eixo-mundo-digital`, `co-eixo-cultura-digital`.
- `objeto_ref`: string com o padrão `^co-obj-[a-z0-9]+(-[a-z0-9]+)*$`.

### `eixos`

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|---|---|---|---|---|
| `eixos` | array (exatamente 3 itens) | sim | Os 3 eixos do complemento: Pensamento Computacional, Mundo Digital e Cultura Digital. | `[{"id": "co-eixo-pensamento-computacional", …}, …]` |
| `eixos[].id` | enum (`eixo_ref`) | sim | Identificador do eixo. | `"co-eixo-mundo-digital"` |
| `eixos[].documento` | const `computacao-2022` | sim | Documento curricular. | `"computacao-2022"` |
| `eixos[].nome` | string (mínimo 3 caracteres) | sim | Nome oficial do eixo. | `"Mundo Digital"` |

### `objetos_conhecimento`

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|---|---|---|---|---|
| `objetos_conhecimento` | array (mínimo 1 item) | sim | Objetos de conhecimento das habilidades do EF de Computação. 59 itens, dos quais 30 têm `pai`. 4 objetos servem só como pai e não são apontados diretamente por habilidades. | `[{"id": "co-obj-algoritmos", …}, …]` |
| `objetos_conhecimento[].id` | string (`objeto_ref`) | sim | Identificador: `co-obj-` + nome em slug. | `"co-obj-tipos-de-dados"` |
| `objetos_conhecimento[].documento` | const `computacao-2022` | sim | Documento curricular. | `"computacao-2022"` |
| `objetos_conhecimento[].nome` | string (mínimo 3 caracteres) | sim | Nome como aparece no anexo, sem o marcador "(cont.)" com que o anexo indica a continuação de um quadro na página seguinte (decisão 14). | `"Tipos de dados"` |
| `objetos_conhecimento[].pai` | string (`objeto_ref`) ou `null` (anulável) | sim | `id` do objeto pai, na hierarquia dos quadros dos anos finais. `null` quando o objeto não tem pai. | `"co-obj-programacao"` |

### `competencias`

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|---|---|---|---|---|
| `competencias` | array (mínimo 1 item) | sim | Competências do complemento. 14 itens: 7 gerais e 7 específicas do EM. | `[{"id": "computacao-cg-01", …}, …]` |
| `competencias[].id` | string (`id_slug`) | sim | Identificador. Nos dados: `computacao-cg-` + número (gerais) ou `computacao-em-ce-` + número (específicas do EM), com 2 dígitos. | `"computacao-em-ce-01"` |
| `competencias[].documento` | const `computacao-2022` | sim | Documento curricular. | `"computacao-2022"` |
| `competencias[].tipo` | enum | sim | `geral_computacao`: competência geral do complemento. `especifica_em_computacao`: competência específica de Computação no EM; as habilidades do EM apontam para elas. | `"especifica_em_computacao"` |
| `competencias[].numero` | integer (mínimo 1) | sim | Número da competência dentro do seu tipo (1 a 7 em cada tipo, nos dados). | `1` |
| `competencias[].texto` | string (`texto_normativo`) | sim | Enunciado oficial da competência, conferido contra o anexo. | `"Compreender as possibilidades e os limites da Computação para resolver problemas, …"` |
| `competencias[].fonte` | object ([`fonte`](#fonte)) | sim | Proveniência: só `documento`, `arquivo` (o anexo) e `proveniencia`. | `{"arquivo": "anexo-ao-parecer-cneceb-no-2-2022-bncc-computacao.pdf", "proveniencia": "competências específicas do EM (cabeçalho da planilha de EM, verificadas contra o anexo)", …}` |

### `objetivos_ei`

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|---|---|---|---|---|
| `objetivos_ei` | array (mínimo 1 item) | sim | Objetivos de aprendizagem de Computação na EI. O anexo só os define para a pré-escola. 11 nos dados. | `[{"codigo": "EI03CO01", …}, …]` |
| `objetivos_ei[].codigo` | string (`codigo_computacao_ei`) | sim | Código oficial, chave primária do registro. | `"EI03CO01"` |
| `objetivos_ei[].documento` | const `computacao-2022` | sim | Documento curricular. | `"computacao-2022"` |
| `objetivos_ei[].texto` | string (`texto_normativo`) | sim | Texto oficial do objetivo, conferido contra o anexo. | `"Reconhecer padrão de repetição em sequência de sons, movimentos, desenhos."` |
| `objetivos_ei[].eixo` | enum (`eixo_ref`) | sim | `id` do eixo (`eixos[].id`). | `"co-eixo-pensamento-computacional"` |
| `objetivos_ei[].grupo_etario` | const `ei-grupo-03` | sim | Sempre `ei-grupo-03` (crianças pequenas), `id` de `recortes_temporais` em `estrutura.json`. | `"ei-grupo-03"` |
| `objetivos_ei[].vigencia` | object ([`vigencia`](#vigencia)) | sim | Vigência do registro. | `{"status": "vigente", "desde": "dados-2026.07", "ate": null}` |
| `objetivos_ei[].fonte` | object ([`fonte`](#fonte)) | sim | Proveniência: `arquivo` é o anexo oficial; `localizador` aponta a planilha de apoio de Pernambuco e a linha de onde veio a estrutura; `localizador_pdf` é a página do anexo. | `{"localizador": "COMPUTAÇÃO - EDUCAÇÃO INFANTIL .xlsx · linha 4", "localizador_pdf": "página PDF 6", …}` |

### `habilidades_ef`

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|---|---|---|---|---|
| `habilidades_ef` | array (mínimo 1 item) | sim | Habilidades de Computação no EF: anos 1 a 9 e blocos `EF15` e `EF69`. 104 nos dados. | `[{"codigo": "EF01CO01", …}, …]` |
| `habilidades_ef[].codigo` | string (`codigo_computacao_ef`) | sim | Código oficial, chave primária do registro. | `"EF15CO01"` |
| `habilidades_ef[].documento` | const `computacao-2022` | sim | Documento curricular. | `"computacao-2022"` |
| `habilidades_ef[].texto` | string (`texto_normativo`) | sim | Texto oficial da habilidade, conferido contra o anexo. Alguns textos se repetem em códigos diferentes, como no anexo (ex.: `EF06CO02` e `EF69CO02`). | `"Identificar as principais formas de organizar e representar a informação de maneira estruturada …"` |
| `habilidades_ef[].eixo` | enum (`eixo_ref`) | sim | `id` do eixo (`eixos[].id`). | `"co-eixo-pensamento-computacional"` |
| `habilidades_ef[].objetos_conhecimento` | array de string (`objeto_ref`), mínimo 1 item | sim | `id`s dos objetos de conhecimento (`objetos_conhecimento[].id`). Nos dados, sempre 1 item. | `["co-obj-organizacao-e-representacao-da-informacao"]` |
| `habilidades_ef[].anos` | array de integer (1 a 9), mínimo 1 item | sim | Anos do EF decodificados do código. Blocos: `EF15` = 1º ao 5º; `EF69` = 6º ao 9º. | `[1, 2, 3, 4, 5]` |
| `habilidades_ef[].vigencia` | object ([`vigencia`](#vigencia)) | sim | Vigência do registro. | `{"status": "vigente", "desde": "dados-2026.07", "ate": null}` |
| `habilidades_ef[].fonte` | object ([`fonte`](#fonte)) | sim | Proveniência, como em `objetivos_ei`. Em `EF05CO11`, o `localizador` registra a forma impressa no anexo, `(EF05CO011)` (decisão 9 do DECISOES.md). | `{"localizador": "1º ao 5º ANO - HABILIDADES- BNCC - Computação.xlsx · linha 61", "localizador_pdf": "página PDF 38", …}` |

### `habilidades_em`

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|---|---|---|---|---|
| `habilidades_em` | array (mínimo 1 item) | sim | Habilidades de Computação no EM. 26 nos dados. | `[{"codigo": "EM13CO01", …}, …]` |
| `habilidades_em[].codigo` | string (`codigo_computacao_em`) | sim | Código oficial, chave primária do registro. | `"EM13CO01"` |
| `habilidades_em[].documento` | const `computacao-2022` | sim | Documento curricular. | `"computacao-2022"` |
| `habilidades_em[].texto` | string (`texto_normativo`) | sim | Texto oficial da habilidade, conferido contra o anexo. | `"Explorar e construir a solução de problemas por meio da reutilização de partes de soluções existentes."` |
| `habilidades_em[].competencia` | string (padrão `^computacao-em-ce-[0-9]{2}$`) | sim | `id` da competência específica do EM (`competencias[].id` com `tipo` = `especifica_em_computacao`). Diferente das habilidades de área da BNCC 2018, o código não carrega a competência. | `"computacao-em-ce-01"` |
| `habilidades_em[].vigencia` | object ([`vigencia`](#vigencia)) | sim | Vigência do registro. | `{"status": "vigente", "desde": "dados-2026.07", "ate": null}` |
| `habilidades_em[].fonte` | object ([`fonte`](#fonte)) | sim | Proveniência, como em `objetivos_ei`. | `{"localizador": "COMPUTAÇÃO - ENSINO MÉDIO.xlsx · linha 5", "localizador_pdf": "página PDF 66", …}` |

## Relatórios de verificação (`verificacao.json`)

`dados/bncc-2018/verificacao.json` (1.695 entradas: 1.580 aprendizagens e 115 competências) e `dados/computacao-2022/verificacao.json` (141 entradas) registram o resultado da conferência de cada texto contra o documento oficial. São gerados por `pipeline/verificar.py` e `pipeline/verificar_computacao.py` a cada execução do pipeline e não têm JSON Schema. Cada arquivo é um objeto cujas chaves são os códigos das aprendizagens ou, na BNCC 2018, os `id` das competências (`cg-01`, `ef-comp-lp-ce-04`).

| Campo | Tipo | Presente | Descrição | Exemplo |
|---|---|---|---|---|
| `<codigo>.status` | string | sempre | Resultado da conferência. Valores possíveis no código: `ok`, `ok_hifenizacao` (só Computação), `requer_conferencia_visual`, `divergente`, `nao_encontrado`. Nos dados atuais, todas as entradas são `ok`. | `"ok"` |
| `<codigo>.pagina_pdf` | inteiro | quando encontrado | Página do PDF em que o texto foi conferido. | `101` |
| `<codigo>.arquivo_pdf` | string | sempre | Arquivo do documento oficial usado na conferência. | `"Base-Nacional-Comum-Curricular-BNCC.pdf"` |
| `<codigo>.nota` | string | em 4 entradas da BNCC 2018 | Observação da conferência, como texto que atravessa páginas ou conferência visual registrada. | `"texto atravessa páginas"` |

## Pendências

Nenhuma. As três pendências da primeira versão deste dicionário (`fonte.url_oficial` sem uso, `presenca` nula sem significado definido e `vigencia.ate` sem formato) foram resolvidas na `dados-2026.08` / `schema-v1.1.0` (decisão 14 do DECISOES.md).
