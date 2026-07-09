# Versionamento e ciclo de vida

Como o dataset evolui quando as fontes oficiais mudam, e o que os consumidores podem assumir.

## Duas trilhas de versão

- **Conteúdo**: data-version no formato `dados-AAAA.MM` (patch: `dados-AAAA.MM.N`). Atual: `dados-2026.07` (pré-release).
- **Formato**: semver dos JSON Schemas (`schema-v1.0.0`). Mudança aditiva = minor; mudança que quebra consumidores = major.

Releases são imutáveis (tags git). O histórico de textos vive nas releases; o estado vive no registro.

## Vigência no registro

Todo registro normativo carrega:

```json
"vigencia": {"status": "vigente", "desde": "dados-2026.07", "ate": null}
```

Regras invioláveis:

1. **Registro publicado nunca é apagado.** Revogação muda `status` para `revogado` e preenche `ate`; o registro permanece consultável.
2. **Código nunca é reutilizado**, nem para substituir habilidade revogada por outra parecida.
3. Toda mudança de conteúdo referencia a fonte oficial que a motivou.

## Taxonomia de eventos

| Evento | Exemplo | Tratamento |
|---|---|---|
| Mudança normativa | CNE altera ou revoga habilidade | Atualiza registro e vigência; changelog categoria `normativa`; nova data-version |
| Errata oficial | MEC corrige o documento | Como mudança normativa, com a errata como fonte |
| Novo ato ou complemento | Computação (CNE/CEB 2/2022) | Novo `documento_curricular` ligado por `derivado_de`; não altera os registros existentes |
| Correção de extração | Erro nosso em relação à fonte | Corrige o registro; changelog categoria `correcao`; data-version patch |
| Mudança de schema | Campo novo, renomeação | Semver do schema |

A distinção `normativa` (o mundo mudou) versus `correcao` (nós erramos) é obrigatória no changelog.

## Para consumidores

- Fixe a data-version que você validou; atualize deliberadamente lendo o changelog.
- `vigencia.status` existe para você filtrar: aplicações novas não deveriam sugerir aprendizagens revogadas.
- Os JSONs são a fonte canônica; SQLite e CSV são derivados gerados e conferidos no CI.
