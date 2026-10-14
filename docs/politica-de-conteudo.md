**Português** · [English](en/content-policy.md)

# Política de conteúdo

O que este dataset distribui, como erros e conteúdo indevido são identificados, como reportar e o que acontece depois do reporte.

## O que é distribuído

- **Textos normativos.** Os textos da BNCC e do complemento de Computação, reproduzidos sem alteração a partir dos documentos oficiais do MEC e do CNE (ver [`fontes/`](../fontes/README.md)).
- **Metadados do projeto.** Estrutura (etapas, componentes, eixos, objetos de conhecimento), identificadores, relações, vigência e proveniência de cada registro (arquivo e página da fonte).

O dataset não tem conteúdo enviado por usuários. Issues, pull requests e discussões são o único espaço de interação, regido pelo [código de conduta](../CODE_OF_CONDUCT.md).

## O que conta como problema

- **Texto divergente.** O texto de um registro difere do documento oficial: erro de transcrição, truncamento, hifenização.
- **Metadado errado.** Código, ano, componente, relação ou página de fonte incorretos.
- **Conteúdo indevido.** Qualquer coisa que não seja texto oficial nem metadado do projeto, como texto inserido por engano ou de forma maliciosa em um arquivo.
- **Dado pessoal.** Qualquer informação que identifique uma pessoa em um arquivo do repositório.

Discordar do conteúdo da BNCC em si não é problema deste repositório. O texto normativo é responsabilidade do CNE.

## Como os problemas são identificados

- **Verificação automática.** A cada mudança, o CI confere cada texto caractere a caractere contra o PDF homologado e o anexo oficial de Computação. Qualquer divergência reprova a mudança.
- **Reprodução completa.** O CI refaz o dataset inteiro a partir das fontes. Edição manual em `dados/` reprova a mudança.
- **Validação de formato.** JSON Schemas fechados e 29 checagens de contrato e completude.
- **Auditorias independentes.** A auditoria de 10/08/2026 leu 100% dos registros e resultou em 11 correções (decisão 12 do [DECISOES.md](../DECISOES.md)).

## Como reportar

- **Erro de dado:** issue com o template "Correção de dado", com o código do registro, o valor atual, o valor correto e a fonte oficial com página.
- **Mudança normativa** (nova resolução ou parecer do CNE): issue com o template "Mudança normativa".
- **Dado pessoal, conteúdo indevido ou vulnerabilidade:** e-mail para **contato@bncc.dev**, sem issue pública, conforme o [SECURITY.md](../SECURITY.md).

## O que acontece depois

- **Erro confirmado pela fonte oficial.** A correção entra na extração, nunca à mão, e sai em uma nova data-version, com entrada no [CHANGELOG.md](../CHANGELOG.md) (categoria `correcao`). Se houver interpretação, ela vira entrada no DECISOES.md.
- **Divergência entre fontes oficiais.** A escolha vira decisão documentada no DECISOES.md, com o motivo.
- **Dado pessoal ou conteúdo indevido.** Sai da versão atual assim que identificado, e quem reportou recebe retorno. A remoção do histórico do git é avaliada caso a caso.
- **Pedido sem fonte oficial.** Volta com o pedido da fonte. Sem resposta em 30 dias, a issue é fechada.

## Prazos

| Etapa | Prazo-alvo |
|---|---|
| Primeira resposta a uma issue de correção | 3 dias úteis |
| Avaliação contra a fonte oficial | 10 dias úteis |
| Correção publicada, quando a fonte confirma o erro | na data-version seguinte |
| Remoção de dado pessoal ou conteúdo indevido | até 3 dias úteis depois do reporte, o mesmo prazo de confirmação do [SECURITY.md](../SECURITY.md) |

Os prazos são metas. Atrasos e exceções ficam registrados na própria issue.
