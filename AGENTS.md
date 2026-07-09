# AGENTS.md · guia para agentes de IA

Instruções para agentes de código e assistentes trabalhando neste repositório ou consumindo estes dados.

## O que é isto

Dataset aberto e verificado da BNCC (Base Nacional Comum Curricular brasileira): 1.580 aprendizagens das três etapas da educação básica, com proveniência por registro. Os JSONs em `dados/bncc-2018/` são a fonte canônica; SQLite e CSV em `derivados/` são gerados.

## Regras que nunca se quebram

1. **Nunca invente códigos ou textos de habilidade.** Se um código não está em `dados/`, ele não existe na BNCC. A numeração tem lacunas legítimas; não interpole.
2. **Nunca edite `dados/` ou `derivados/` à mão.** Tudo é gerado pelo pipeline a partir de `fontes/`; o CI reprova edição manual. Para mudar um dado, mude a extração ou registre decisão em DECISOES.md, e sempre com fonte oficial.
3. **A área ou componente de uma habilidade é a decodificada do código** (`pipeline/codigos.py`), nunca a posição em uma aba ou tabela.
4. **Textos normativos são imutáveis por nós.** Divergência entre fontes oficiais vira entrada em DECISOES.md, não escolha silenciosa.
5. Conteúdo interpretativo (comentários, progressões inferidas, desmembramentos) não entra no núcleo canônico.

## Mapa do domínio em 30 segundos

- Três taxonomias distintas: EI tem `objetivos` por campo de experiências e grupo etário (com `alinhamento` entre faixas); EF tem `habilidades` com unidades temáticas ou campos de atuação + práticas (LP) ou eixos (LI); EM tem `habilidades` por área, sem seriação, com competências vinculadas.
- Códigos são decodificáveis: `EF67LP08` = Fundamental, anos 6 e 7, Língua Portuguesa, 8ª da sequência. Use `pipeline/codigos.py`.
- Todo registro tem `fonte` (planilha + página do PDF) e `vigencia` (filtre `status = vigente`).
- Detalhes: `docs/modelo-de-dados.md`.

## Trabalhando no pipeline

- Python stdlib puro (exceção: `jsonschema>=4.18` só em `validar_schema.py`). Não adicione dependências sem discussão.
- Sequência: `extrair.py` → `extrair_ei.py` → `verificar.py` → `validar_schema.py` → `validar.py` → `derivar.py`. Todos precisam terminar com exit 0.
- Qualquer mudança de shape dos dados exige mudança correspondente em `schema/` (os schemas são fechados por design).
- Idioma do projeto: português brasileiro, em código e documentação. Em documentos públicos, não use travessão (—); prefira vírgula, dois-pontos ou parênteses.

## Consumindo os dados

```python
import json
ef = json.load(open('dados/bncc-2018/ensino-fundamental.json'))
por_codigo = {h['codigo']: h for h in ef['habilidades']}
h = por_codigo['EF67LP08']   # sempre por código, nunca por posição
```

Ao citar uma aprendizagem para um usuário, inclua o código e, quando relevante, a fonte (`fonte.localizador_pdf`).
