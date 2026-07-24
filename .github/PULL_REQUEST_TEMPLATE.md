<!--
Obrigado por contribuir. Preencha o que se aplica e apague o resto.
Mudanças de schema ou de formato precisam de discussão prévia em issue: elas afetam consumidores.
-->

## O que muda

<!-- Uma ou duas frases. Se resolve uma issue, escreva "Resolve #123". -->

## Categoria

- [ ] `correcao` (erro nosso, divergência em relação à fonte oficial)
- [ ] `normativa` (mudança nas normas oficiais)
- [ ] `schema` (formato dos dados; discutido antes em issue)
- [ ] `editorial` (docs, pipeline, tooling, sem mudança de dado)

## Fonte oficial

<!-- Obrigatório para correcao e normativa: documento (MEC ou CNE), página do PDF ou localizador na planilha. -->

## Checklist

- [ ] Não editei `dados/` nem `derivados/` à mão: a mudança veio de `fontes/` ou do `pipeline/`.
- [ ] Rodei o pipeline completo localmente e todos os passos terminaram com exit 0.
- [ ] Se mudei o shape dos dados, atualizei os arquivos correspondentes em `schema/`.
- [ ] Se houve decisão de interpretação entre fontes divergentes, registrei em `DECISOES.md`.
- [ ] Atualizei o `CHANGELOG.md` na seção não publicada.

```bash
cd pipeline
python3 extrair.py && python3 extrair_ei.py && python3 extrair_computacao.py
python3 verificar.py && python3 verificar_computacao.py
python3 validar_schema.py && python3 validar.py
python3 derivar.py
```
