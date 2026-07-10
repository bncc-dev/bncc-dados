# Changelog

Categorias: `normativa` (mudança nas normas oficiais) · `correcao` (erro nosso corrigido) · `schema` (formato) · `editorial` (docs, pipeline, sem mudança de dado).

## [Não publicado] · pré-release `dados-2026.07`

### Dados
- Dataset inicial completo: 1.580 aprendizagens (EI 93, EF 1.304, EM 183), 10 competências gerais, 105 competências específicas, 885 contextos de organização e espinha estrutural.
- Verificação contra o PDF homologado: 1.576/1.580 idênticos; 4 divergências entre fontes oficiais documentadas em DECISOES.md.
- Completude provada por varredura de códigos no PDF (1.580 = 1.580).
- Marcos legais mínimos: 20 atos normativos (Constituição de 1988 a Lei nº 14.945/2024) com ementa, URL oficial verificada (acervo atual do CNE em gov.br/mec; o portal.mec.gov.br legado saiu do ar) e relações tipadas com entidades do dataset.
- Vocabulário de perfis: professor, aluno, gestor, responsável, coordenador, com sinônimos.

### Schema
- JSON Schemas draft 2020-12 para os 6 arquivos de dados (`schema-v1.0.0-rc`), incluindo marcos legais e perfis.

### Editorial
- Pipeline reprodutível com CI (extração, verificação, validação, derivados).
- Derivados SQLite e CSV gerados e conferidos.
- Documentação: modelo de dados, metodologia, versionamento, contribuição.

### Pendente para `dados-v1.0.0`
- Complemento de Computação (Parecer CNE/CEB 2/2022) como módulo versionado à parte. Documento-fonte localizado (anexo do parecer no acervo do CNE, URL registrada em `marcos-legais.json`); entra em data-version posterior, conforme o gate do lançamento.
- Registro da revisão pedagógica (Equipe Pedagógica Profy).
- Publicação do repositório e primeira tag.
