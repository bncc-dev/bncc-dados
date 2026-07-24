# Plano de abertura do repositório

Análise e estratégia para tornar público o `bncc-dev/bncc-dados`, registrada em 2026-07-23. Complementa o compromisso já firmado em [divisao-aberto-comercial.md](divisao-aberto-comercial.md).

## Diagnóstico

O projeto foi arquitetado para ser aberto desde o primeiro commit. Estado verificado:

| Item | Situação |
|---|---|
| Visibilidade atual | Privado (`github.com/bncc-dev/bncc-dados`) |
| Licenças | MIT (código, `LICENSE`) + CC BY 4.0 (dados, `dados/LICENSE.md`) — corretas e commitadas |
| Segredos/PII | Varredura completa dos 14 commits do histórico (padrões de chaves de API, tokens GitHub/AWS/OpenAI/Slack, chaves privadas, senhas) em 2026-07-24: **nenhum segredo**; únicos matches são falsos positivos em português ("resenha", "desenhar"). O histórico completo pode ser aberto sem reescrita |
| Divisão aberto/comercial | Formalizada em `docs/divisao-aberto-comercial.md`, com regra de irrevogabilidade |
| Comunidade | `CONTRIBUTING.md` com regra "correção exige fonte oficial"; falta CODE_OF_CONDUCT dedicado, templates de issue/PR e GOVERNANCE |
| CI | Reprodutibilidade completa em todo push/PR (`.github/workflows/validacao.yml`) — protege a qualidade das contribuições automaticamente |
| Estado de release | Pré-release `dados-2026.07`; pacotes npm/PyPI/MCP em 0.1.x (repos separados) |

## Pontos a resolver antes do flip para público

### 1. Binários de terceiros em `fontes/` (único ponto jurídico real)

- **PDFs do MEC/CNE**: atos oficiais públicos; redistribuição defensável (art. 8º, Lei 9.610/98). Manter.
- **Planilhas da Sec. de Educação de PE** (`fontes/secedu-pernambuco/`): materiais de terceiros usados apenas como apoio de extração. **Decisão: revisar termos de uso ou remover do repo público**, substituindo por link à fonte + checksum SHA-256 (já mantido em `fontes/`). A reprodutibilidade não se perde: quem reproduz baixa da fonte original.

### 2. Arquivos grandes (~12 MB total)

Não bloqueante nesse tamanho. Opções, em ordem de preferência:

1. Deixar de versionar `derivados/` (geráveis pelo pipeline; o CI já os valida) e publicá-los em releases do GitHub.
2. Manter como está e reavaliar se o repo crescer.

### 3. Documentos de comunidade

Feito em 2026-07-24:

- `CODE_OF_CONDUCT.md`: Contributor Covenant 2.1 em pt-BR, canal de denúncia em contato@bncc.dev, com a ressalva explícita de que discordância técnica sobre dados não é violação de conduta.
- `SECURITY.md`: escopo (pipeline, CI, dependências, segredos), o que não é problema de segurança e prazos de resposta.
- `CITATION.cff`: faz o GitHub gerar citação formatada. Importante para o público de pesquisa, que é um dos alvos declarados.
- Templates em `.github/ISSUE_TEMPLATE/`: `correcao-de-dado` (campos obrigatórios de código, valor atual, valor proposto e fonte oficial, mais confirmação de que a fonte é ato federal), `mudanca-normativa`, `derivado-ou-formato`, e `config.yml` roteando dúvida de uso para Discussions e segurança para a política privada.
- `.github/PULL_REQUEST_TEMPLATE.md`: categoria da mudança, campo de fonte e checklist de pipeline, schema, DECISOES e CHANGELOG.

O template de correção automatiza a regra de ouro na origem: a fonte passa a ser campo obrigatório do formulário, em vez de pedido manual do mantenedor depois.

Ainda pendente:

- `GOVERNANCE.md` simples (quem decide interpretações de fonte; `DECISOES.md` já é metade disso). Pode vir depois da abertura.
- Criar no GitHub as labels previstas no [guia-comunidade.md](guia-comunidade.md) e habilitar Discussions (o `config.yml` já aponta para lá) e o private vulnerability reporting (o `SECURITY.md` já aponta para lá).
- Abrir de 3 a 5 `good-first-issue` antes do flip: repositório público sem issues não converte contribuidor.

### 4. Momento da abertura vs. release

Abrir já como pré-release é razoável e transparente (o README avisa "não recomendado para produção") e convida contribuição cedo. Alternativa: cravar `dados-v1.0.0` junto com a abertura. **Decisão pendente.**

## O que NÃO abrir

Pelo desenho da divisão aberto/comercial: apenas a coluna comercial (API hospedada, SLA, integrações sob medida, consultoria) — e nada disso vive neste repositório. Os repos dos pacotes npm/PyPI/MCP serão abertos também (compromisso público), mas exigem a mesma checagem de segredos antes.

Uma exceção fora da lógica comercial: o `bncc-benchmark-heldout` (itens reservados de avaliação) fica fechado por **razão metodológica**, não de negócio. Publicá-lo contamina o benchmark de forma permanente. Vale declarar isso explicitamente no `bncc-benchmark`, para não parecer incoerência com o discurso de abertura.

## Estratégia de comunidade

- **Escopo de contribuição já protegido**: correções exigem fonte oficial e o CI rejeita divergências automaticamente — qualidade garantida sem burocracia humana.
- **Públicos naturais**: edtechs, secretarias de educação, pesquisadores e desenvolvedores de ferramentas de IA educacional. O servidor MCP é a porta de entrada moderna — destacá-lo na comunicação.
- **Good first issues**: itens do roadmap do README e novos derivados (formatos, integrações).
- **Narrativa de lançamento**: ênfase no compromisso de irrevogabilidade e no CI de reprodutibilidade caractere-a-caractere — diferencial raro em datasets abertos.

## Sequência de execução

1. Remover/relinkar as planilhas de PE (`fontes/secedu-pernambuco/`).
2. ~~Adicionar `CODE_OF_CONDUCT.md` e templates de issue/PR.~~ Feito em 2026-07-24 (ver seção 3), junto com `SECURITY.md` e `CITATION.cff`.
3. Configurar o GitHub: labels do guia de comunidade, Discussions, private vulnerability reporting.
4. Decidir versionamento de `derivados/` e o momento da release.
5. Abrir de 3 a 5 good first issues.
6. Varredura de segredos no `bncc-pacotes` (mesmo critério aplicado aqui), já que os pacotes abrem por compromisso público.
7. Flip do repositório para público.
8. Anunciar (irrevogabilidade + reprodutibilidade + MCP).
