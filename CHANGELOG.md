# Changelog

Categorias: `normativa` (mudança nas normas oficiais) · `correcao` (erro nosso corrigido) · `schema` (formato) · `editorial` (docs, pipeline, sem mudança de dado).

## [Não publicado] · pré-release `dados-2026.07`

### Dados
- Dataset inicial completo: 1.580 aprendizagens (EI 93, EF 1.304, EM 183), 10 competências gerais, 105 competências específicas, 885 contextos de organização e espinha estrutural.
- Verificação contra o PDF homologado: 1.576/1.580 idênticos; 4 divergências entre fontes oficiais documentadas em DECISOES.md.
- Completude provada por varredura de códigos no PDF (1.580 = 1.580).

### Schema
- JSON Schemas draft 2020-12 para os 4 arquivos de dados (`schema-v1.0.0-rc`).

### Editorial
- Pipeline reprodutível com CI (extração, verificação, validação, derivados).
- Derivados SQLite e CSV gerados e conferidos.
- Documentação: modelo de dados, metodologia, versionamento, contribuição.

### Pendente para `dados-v1.0.0`
- Complemento de Computação (Parecer CNE/CEB 2/2022) como módulo versionado à parte (aguarda documento-fonte).
- Marcos legais mínimos (LDB, DCNs, resoluções: id, ementa, link, relações).
- Vocabulário de perfis (professor, aluno, gestor, responsável, coordenador).
- Registro da revisão pedagógica (Equipe Pedagógica Profy).
- Publicação do repositório e primeira tag.
