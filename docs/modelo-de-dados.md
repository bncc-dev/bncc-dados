# Modelo de dados

Como o dataset representa a BNCC. A definição executável está nos [JSON Schemas](../schema/); este documento explica as decisões de modelagem para quem vai consumir o dado.

## O princípio: honestidade estrutural

A BNCC tem três taxonomias diferentes, e o dataset as modela como três entidades distintas, não como um tipo genérico com campos nulos:

| | Educação Infantil | Ensino Fundamental | Ensino Médio |
|---|---|---|---|
| Entidade | `objetivo` (93) | `habilidade` (1.304) | `habilidade` (183) |
| Código | `EI02TS01` | `EF67LP08` | `EM13LGG103` |
| Organização | campo de experiências | unidade temática, ou campos de atuação + prática de linguagem (LP), ou eixo (LI) | área do conhecimento |
| Recorte temporal | grupo etário (3 faixas) | ano ou bloco de anos | sem seriação (currículos definem) |
| Vínculo com competência | não há | não há vínculo formal por habilidade | de área: 1, embutida no código; LP: 1 a n, da planilha oficial |

## Identificadores

- **Código oficial quando existe** (`EF67LP08`): é a chave primária das aprendizagens.
- **ID cunhado quando não existe** (`cg-04`, `em-area-lgg-ce-01`, `ef-comp-lp-prat-leitura`): slug estável em kebab-case, imutável após publicado. O padrão de cada tipo está em `schema/definicoes.json`.

## Anatomia dos códigos

Os códigos são decodificáveis (função de referência: `pipeline/codigos.py`):

```
EI 02 TS 01    etapa · grupo etário (01 bebês, 02 bem pequenas, 03 pequenas) · campo · sequência
EF 67 EF 01    etapa · ano 01-09 ou bloco (15, 69, 12, 35, 67, 89) · componente · sequência
EM 13 LGG 103  etapa · sem seriação · área (3 letras) · competência (1º dígito) + sequência
EM 13 LP  02   etapa · sem seriação · Língua Portuguesa (2 letras) · sequência simples
```

Cuidados: o segmento `EF` é ambíguo (etapa, campo de experiências ou Educação Física; a posição desambigua) e a numeração sequencial não implica ordem pedagógica nem completude.

## Entidades da espinha estrutural (`estrutura.json`)

- `documento_curricular`: raiz de proveniência (`bncc-2018`). Complementos e currículos estaduais futuros entram como novos documentos ligados por `derivado_de`, sem mudança de modelo.
- `etapas`, `modalidades` (EJA como transversal, com segmentos), `areas_conhecimento` (por etapa), `componentes_curriculares`, `recortes_temporais`.
- Assimetrias são dados, não exceções: componentes do EM sem habilidades próprias têm `tem_aprendizagens_proprias: false`; LP e Matemática no EM carregam `destaque_legal` (Lei nº 13.415/2017); Língua Inglesa no EF tem `presenca.anos: [6..9]`.
- `competencias_gerais` (10) e `competencias_especificas` (105: de área ou de componente; componente só existe em área multicomponente).

## As aprendizagens

Cada registro carrega, além dos campos da tabela acima:

- `vigencia`: `{status: vigente | alterado | revogado, desde, ate}`. Registro publicado nunca é apagado; código nunca é reutilizado.
- `fonte`: documento, arquivo, proveniência, localizador na planilha e página no PDF homologado (`localizador_pdf`). É a cadeia de auditoria de cada registro.
- EF: `objetos_conhecimento` como lista de referências (entidade própria, relação N:N).
- EI: `alinhamento` liga objetivos do mesmo aspecto entre as três faixas etárias (relação oficial da p. 26 do documento, que a maioria dos datasets perde). Alinhamentos com 2 objetivos refletem células vazias do quadro oficial.

## O complemento de Computação (`computacao-2022`)

Primeiro documento curricular além da BNCC 2018, provando o desenho multi-documento do modelo: `computacao-2022` (`tipo: complemento`, `derivado_de: bncc-2018`) traz as normas de Computação na Educação Básica (anexo ao Parecer CNE/CEB nº 2/2022, instituído pela Resolução CNE/CEB nº 1/2022) em `dados/computacao-2022/computacao.json`.

**141 aprendizagens** com componente `CO` nos códigos, com organização própria por etapa (honestidade estrutural, como no núcleo):

| | EI | EF | EM |
|---|---|---|---|
| Entidade | `objetivo` (11, só pré-escola: `EI03CO01`–`11`) | `habilidade` (104: anos 1–9 + blocos `EF15`/`EF69`) | `habilidade` (26: `EM13CO01`–`26`) |
| Organização | eixo | eixo + objeto de conhecimento (com hierarquia pai/sub nos anos finais) | competência específica do complemento (7) |

- **Eixos** (3): Pensamento Computacional, Mundo Digital, Cultura Digital (`co-eixo-*`).
- **Objetos de conhecimento** (`co-obj-*`): campo `pai` opcional captura a hierarquia dos quadros dos anos finais (ex.: `co-obj-tipos-de-dados` → pai `co-obj-programacao`).
- **Competências**: 7 gerais do complemento (`computacao-cg-*`) e 7 específicas do EM (`computacao-em-ce-*`), às quais as habilidades do EM se vinculam.
- **Sequências contínuas**: diferente da BNCC 2018, a numeração de Computação não tem lacunas (contrato no CI).
- Verificação: os 141 textos são conferidos caractere a caractere contra o anexo oficial (`verificar_computacao.py`); decisões de interpretação nas entradas 9 e 10 do `DECISOES.md`.
- Fora desta versão do módulo: descritores de agrupamento, explicações e exemplos oficiais do anexo (iteração futura).

## Marcos legais e perfis

Dois vocabulários de referência acompanham o núcleo curricular (schema doc §7):

- `marcos_legais` (`marcos-legais.json`, 20 registros): os atos normativos que fundamentam a BNCC e a educação básica, da Constituição de 1988 à Lei nº 14.945/2024. Cada registro traz `id`, `tipo` (constituição, emenda, lei, resolução, parecer), `titulo`, `ementa`, `url_oficial` (sempre domínio gov.br, verificada no ar) e `relaciona` (vínculos tipados com entidades do dataset, ex.: a Lei nº 13.415/2017 `fundamenta_destaque` LP e Matemática no EM). Sem texto integral na v1.0; dispositivos como dados são evolução futura.
- `perfis` (`perfis.json`, 5 registros): vocabulário dos papéis do ecossistema escolar (professor, aluno, gestor, responsável, coordenador), com sinônimos. É referência de nomenclatura para aplicações consumidoras; não carrega lógica de autorização.

Nota de proveniência: os PDFs do CNE migraram do antigo portal.mec.gov.br (fora do ar) para `www.gov.br/mec/pt-br/cne/pdf/`; as URLs registradas seguem esse acervo, conferidas documento a documento (número, data e ementa).

## O que o modelo não inventa

- Progressão formal entre habilidades do EF: a BNCC não a define; o dataset oferece aproximações estruturais (mesmo objeto de conhecimento, mesma prática) e nada além.
- Vínculo habilidade x competência no EF: o documento oficial não o estabelece por habilidade.
- Objetos de conhecimento com nomes diferentes entre anos são entidades diferentes; equivalências exigirão curadoria futura, em camada separada.

Racional completo das decisões de interpretação: [DECISOES.md](../DECISOES.md).
