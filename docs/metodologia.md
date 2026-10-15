**Português** · [English](en/methodology.md)

# Metodologia · a cadeia de confiança

Como o dado sai dos documentos oficiais e chega ao repositório, e por que dá para confiar em cada elo.

## 1. Fontes

Quatro documentos oficiais, arquivados em [`fontes/`](../fontes/) com checksums SHA-256 e proveniência documentada:

- Planilhas de EF e EM exportadas da ferramenta oficial do MEC (downloadbncc.mec.gov.br) em 23/06/2023, quando o serviço funcionava (o backend estava fora do ar em 07/2026).
- PDF da BNCC completa homologada (600 páginas), o documento canônico de verificação. A Educação Infantil é extraída diretamente dele, pois não há planilha disponível.
- Anexo ao Parecer CNE/CEB nº 2/2022 (Computação, 75 páginas), a fonte canônica do módulo `computacao-2022`. A estrutura dos quadros vem do mapa `fontes/computacao-estrutura.json`, e cada texto é conferido contra o anexo (decisões 10 e 13 do [DECISOES.md](../DECISOES.md)).

## 2. Extração determinística

`pipeline/extrair.py` e `pipeline/extrair_ei.py` transformam as fontes nos JSONs de `dados/bncc-2018/`. Sem intervenção manual, sem LLM na cadeia de dados: parsing determinístico, reproduzível por qualquer pessoa. Inconsistências encontradas nas fontes não são corrigidas silenciosamente: cada uma vira decisão documentada em [DECISOES.md](../DECISOES.md) (ex.: três habilidades do EM estavam em abas trocadas na planilha oficial; a área canônica é sempre a decodificada do código).

## 3. Verificação contra o documento homologado

`pipeline/verificar.py` compara o texto de cada um dos 1.580 registros com o PDF homologado, caractere a caractere após normalização tipográfica (ligaduras, hifenização de quebra, colunas intercaladas dos quadros). Resultado atual:

- **1.580 de 1.580 idênticos**, com a página do PDF gravada em `fonte.localizador_pdf`.
- **Nenhuma divergência aberta.** Os casos em que as fontes oficiais discordam entre si são resolvidos na própria extração e ficam registrados: correções da planilha contra o PDF em `CORRECOES_PDF` e limitações da camada de texto do PDF, com conferência visual, em `CONFERIDOS_VISUALMENTE` (decisão 12 do `DECISOES.md`).

## 4. Validação estrutural

Duas camadas, ambas com código de saída (quebram o CI):

- `pipeline/validar_schema.py`: os 7 arquivos de dados (estrutura, EI, EF, EM, marcos legais, perfis e Computação) contra os [JSON Schemas](../schema/), com autoteste negativo (registros corrompidos de propósito precisam ser rejeitados a cada execução).
- `pipeline/validar.py`: 29 checagens de contrato, incluindo gramática de todos os códigos, contagens-gabarito por componente e área (1.304 EF, 183 EM, 93 EI), integridade referencial, regras estruturais do domínio e **completude por varredura**: a busca de códigos no PDF inteiro encontra exatamente os códigos do dataset. Nada falta, nada sobra.

## 5. Derivados conferidos

`pipeline/derivar.py` gera SQLite e CSVs a partir dos JSONs, de forma determinística. O CI confere que os derivados commitados são idênticos aos regenerados (CSVs por diff; SQLite por dump lógico, imune a diferenças de versão da biblioteca).

## 6. CI: reprodutibilidade a cada mudança

O [workflow de validação](../.github/workflows/validacao.yml) executa a cadeia completa (extração, verificação, schemas, contratos, derivados) em toda mudança e falha se o dataset commitado divergir do reproduzido a partir das fontes. A reprodutibilidade não é uma promessa: é um teste que roda sempre.

## Validação cruzada externa

Além da cadeia interna, o dataset foi comparado com a base BNCC do Profy PEI (linhagem independente): 1.486 códigos em comum com textos 100% idênticos, e uma lacuna encontrada naquela base (EF35LP16), não neste dataset.

## Revisão pedagógica

Em julho de 2026, a Equipe Pedagógica da Profy revisou o dataset, com foco no ponto que a extração automática não consegue decidir sozinha: o **pareamento horizontal dos alinhamentos da Educação Infantil**. O documento oficial (p. 26) afirma que objetivos na mesma linha do quadro, entre grupos etários, tratam do mesmo aspecto do campo de experiências, mas o quadro não traz identificador desse vínculo. O pipeline o reconstrói pela posição sequencial do código (EI01TS01 → EI02TS01 → EI03TS01).

A revisão percorreu os 32 alinhamentos e **confirmou a heurística**: nenhum pareamento incorreto foi encontrado, incluindo os três casos de célula vazia no quadro oficial, que produzem alinhamentos de 2 objetivos em vez de 3 (`ei-align-eo-07`, `ei-align-et-07`, `ei-align-et-08`). A confirmação está registrada na nota de cada um dos 32 registros e na decisão 5 do [DECISOES.md](../DECISOES.md).

A revisão cobriu também uma amostra do módulo de Computação (`computacao-2022`), sem apontamentos.

## Limites conhecidos

- A planilha da Educação Infantil não existe publicamente (ferramenta do MEC fora do ar); a EI vem do PDF, com a mesma verificação.
- O pareamento dos alinhamentos da EI usa a posição sequencial dos códigos (heurística fiel ao quadro oficial), confirmada em revisão pedagógica (ver acima).
