# Changelog

Categorias: `normativa` (mudança nas normas oficiais) · `correcao` (erro nosso corrigido) · `schema` (formato) · `editorial` (docs, pipeline, sem mudança de dado).

## [Não publicado] · pré-release `dados-2026.07`

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

### Pendente para `dados-v1.0.0`
- Registro da revisão pedagógica (Equipe Pedagógica Profy) — incluindo amostra do módulo de Computação, que entrou na v1.0 por decisão de 11/07/2026.
- Publicação do repositório e primeira tag.
