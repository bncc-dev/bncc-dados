# Guia de contribuição

Obrigado pelo interesse em melhorar a fonte de referência da BNCC estruturada.

## A regra de ouro: correção exige fonte oficial

Este dataset registra o que os documentos oficiais dizem. Para propor uma correção de dado, o PR precisa apontar a fonte oficial que a sustenta: documento (MEC/CNE), página ou localizador e, se possível, print do trecho. Correções sem referência à fonte serão devolvidas com carinho.

Se a divergência for entre duas fontes oficiais (acontece: ver [DECISOES.md](DECISOES.md)), o PR deve propor também a entrada de decisão documentando qual fonte prevalece e por quê.

## Como contribuir

1. **Erro de dado** (texto, código, relação errada): abra uma issue com o código do registro, o valor atual, o valor correto e a fonte oficial.
2. **Erro de pipeline** (extração, verificação, validação): issue ou PR direto; os scripts estão em [`pipeline/`](pipeline/) e são stdlib puro (exceto `jsonschema` na validação de formato).
3. **Melhoria de schema ou documentação**: PRs bem-vindos; mudanças de formato passam por discussão em issue antes (afetam consumidores).

## Rodando o pipeline localmente

```bash
pip install --upgrade jsonschema   # única dependência (validação de formato)
cd pipeline
python3 extrair.py && python3 extrair_ei.py
python3 verificar.py
python3 validar_schema.py && python3 validar.py
python3 derivar.py
```

Requisitos: Python 3.10+ e `pdftotext` (poppler). O CI executa exatamente essa sequência e confere que o dataset commitado é idêntico ao reproduzido; PRs que alterem `dados/` sem alterar fonte ou pipeline vão falhar por definição.

## O que não aceitamos

- Dado sem proveniência (inclusive conteúdo gerado por LLM como se fosse oficial).
- Conteúdo interpretativo no núcleo canônico (comentários, desmembramentos, progressões inferidas). Isso pertence à futura camada de anotação, com fonte e licença próprias.
- Material de terceiros sem licença compatível (ex.: derivados CC BY-NC).

## Conduta

Respeito e boa-fé. Este projeto serve a educação pública brasileira; discussões técnicas com esse espírito.
