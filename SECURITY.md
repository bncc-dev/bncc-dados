# Política de segurança

## Escopo

Este repositório publica um dataset e os scripts que o produzem. Não há serviço hospedado, autenticação nem dado pessoal aqui. As classes de problema relevantes são:

- Código do `pipeline/` que execute algo indesejado ao processar as fontes.
- Dependência comprometida ou workflow de CI explorável.
- Conteúdo malicioso embutido em arquivos de `fontes/` ou `derivados/`.
- Exposição acidental de segredo ou de dado pessoal em qualquer arquivo ou no histórico.

Erro de dado (texto divergente da fonte oficial, código errado, relação incorreta) **não é problema de segurança**: abra uma issue de correção normal, conforme o [CONTRIBUTING.md](CONTRIBUTING.md).

## Versões cobertas

Sempre o `main` e a data-version publicada mais recente. Este projeto está em pré-release (`dados-2026.07`); não há suporte retroativo a versões anteriores.

## Como reportar

Envie um e-mail para **contato@bncc.dev** com o assunto começando por `[seguranca]`. Inclua descrição, passos de reprodução e impacto estimado.

Não abra issue pública para vulnerabilidade antes do contato. Se preferir o canal do GitHub, use *Security > Report a vulnerability* (private vulnerability reporting), que também é privado.

## O que esperar

| Etapa | Prazo alvo |
|---|---|
| Confirmação de recebimento | 3 dias úteis |
| Avaliação inicial e classificação | 10 dias úteis |
| Correção ou plano de correção | conforme a severidade, comunicado na avaliação |

Créditos a quem reporta são dados no CHANGELOG e nas notas de release, salvo pedido de anonimato.
