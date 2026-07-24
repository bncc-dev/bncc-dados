# Guia de gestão da comunidade

Manual operacional para quem gerencia a comunidade open source do bncc-dados. Complementa [CONTRIBUTING.md](../CONTRIBUTING.md) (regras para contribuidores) e [plano-abertura.md](plano-abertura.md) (estratégia de abertura).

## Princípios inegociáveis

1. **Fonte oficial acima de opinião.** Nenhuma mudança de dado entra sem citar ato oficial (MEC/CNE). Isso despersonaliza conflitos: a discussão nunca é "quem está certo", é "o que diz a fonte".
2. **Irrevogabilidade.** O que é aberto é irrevogavelmente aberto ([divisao-aberto-comercial.md](divisao-aberto-comercial.md)). Qualquer dúvida da comunidade sobre "e se vocês fecharem depois?" se responde com esse documento.
3. **O CI é o guardião técnico.** Reprodutibilidade caractere-a-caractere roda em todo PR. O gestor não precisa validar dados manualmente — precisa garantir que o processo foi seguido.

## Triagem de issues e PRs

Fluxo padrão:

1. **Classificar** com labels (criar no GitHub se ainda não existirem):
   - `correcao-dado` — divergência em relação à fonte oficial
   - `normativa` — mudança no mundo real (novo ato, revogação)
   - `schema` — proposta de mudança de formato
   - `derivado` — novo formato/integração (CSV, pacote, MCP)
   - `duvida` — pergunta de uso
   - `good-first-issue` — para novos contribuidores
2. **Exigir fonte**: issue de correção sem citação de fonte oficial → responder pedindo a fonte (modelo abaixo) e marcar `aguardando-fonte`. Sem fonte em 30 dias, fechar com comentário cordial.
3. **Interpretação divergente de fonte** → não decidir sozinho; escalar para os mantenedores e registrar a decisão em [DECISOES.md](../DECISOES.md).

Modelo de resposta para correção sem fonte:

> Obrigado por reportar! Para avaliarmos, precisamos da fonte oficial (documento do MEC/CNE, com página ou localizador) que embasa a correção — é a regra de ouro do projeto (ver CONTRIBUTING.md). Pode complementar?

### Prazos de resposta (metas, não SLAs)

| Item | Meta |
|---|---|
| Primeira resposta a issue/PR | 3 dias úteis |
| Revisão de PR com fonte citada e CI verde | 7 dias úteis |
| Dúvidas de uso | 5 dias úteis |

## O que aceitar e o que recusar

**Aceitar:** correções com fonte oficial; novos derivados/formatos; melhorias de docs; tooling do pipeline que não altere dados.

**Recusar (com cordialidade e link para a justificativa):**

- Interpretações pedagógicas ou "melhorias" no texto normativo — o projeto reproduz a fonte, não a edita.
- Dados de currículos estaduais/municipais como fonte de verdade — só atos federais entram no dataset canônico.
- Mudanças de schema sem discussão prévia em issue.
- Reutilização de códigos ou remoção de registros revogados — viola [versionamento.md](versionamento.md).

## Comunicação de releases

A cada data-version nova (ver processo em [versionamento.md](versionamento.md)):

1. Publicar a release no GitHub com o CHANGELOG da versão, destacando categoria `normativa` vs `correcao`.
2. Avisar consumidores dos pacotes (npm/PyPI/MCP) se houver impacto.
3. Mensagem curta nos canais da comunidade explicando **o que mudou e por quê** (com link para a fonte oficial que motivou).

## Crescimento da comunidade

- **Públicos-alvo**: edtechs, secretarias de educação, pesquisadores, devs de IA educacional. O servidor MCP é a porta de entrada para o público de IA — destacá-lo.
- **Good first issues**: manter sempre 3–5 abertas (novos derivados, docs, exemplos de consulta).
- **Reconhecimento**: agradecer nominalmente contribuidores no CHANGELOG e nas notas de release.
- **Métricas mensais sugeridas**: issues abertas/fechadas, tempo de primeira resposta, PRs de fora aceitos, downloads dos pacotes, estrelas.

## Conduta e escalonamento

- Aplicar o código de conduta do projeto (ver CONTRIBUTING.md; CODE_OF_CONDUCT dedicado previsto no plano de abertura).
- Comportamento hostil: 1º aviso em público, reincidência → moderação (ocultar/bloquear) e registro interno.
- Conflitos sobre conteúdo do dado **nunca** se resolvem por votação ou insistência — sempre pela fonte oficial; sem fonte clara, decisão dos mantenedores registrada em DECISOES.md.
