# bncc.dev · dados abertos da BNCC

A Base Nacional Comum Curricular como dados estruturados, verificados e rastreáveis: as 1.580 aprendizagens das três etapas da educação básica (Educação Infantil, Ensino Fundamental e Ensino Médio), com competências, contextos de organização e proveniência registro a registro.

**Status: pré-release.** Dados completos e validados, aguardando revisão pedagógica e primeira release versionada (`dados-v1.0.0`). Não recomendado para produção até lá.

Mantido pela [Profy](https://profy.com.br), que é também sua primeira consumidora.

## O que tem aqui

| Pasta | Conteúdo |
|---|---|
| `dados/bncc-2018/` | O dataset em JSON: estrutura do sistema, 93 objetivos da EI (com alinhamentos entre faixas etárias), 1.304 habilidades do EF (com unidades temáticas, objetos de conhecimento, campos de atuação e práticas de linguagem), 183 habilidades do EM (com competências vinculadas) |
| `fontes/` | Os documentos oficiais do MEC dos quais tudo é extraído, com checksums |
| `pipeline/` | Scripts de extração, verificação e validação: qualquer pessoa reproduz o dataset a partir das fontes |
| `DECISOES.md` | Toda decisão de interpretação sobre inconsistências das fontes, documentada |
| `docs/` | Divisão aberto/comercial, relatório de validação |

## Por que confiar neste dado

1. **Cada registro aponta a fonte oficial**: aba e linha da planilha do MEC, mais a página do PDF homologado (campo `fonte`).
2. **Verificação automática**: 1.576 dos 1.580 textos batem caractere a caractere com o PDF homologado; os 4 restantes são divergências entre as próprias fontes oficiais, documentadas em `DECISOES.md` com a decisão tomada.
3. **Completude provada**: a varredura de códigos no PDF inteiro encontra exatamente os códigos presentes no dataset. Nada falta, nada sobra.
4. **Extração reprodutível**: rode `pipeline/` e chegue aos mesmos arquivos. O CI faz isso a cada mudança.

## Uso rápido

```bash
git clone https://github.com/marcosbeto/bnccdev.git
python3 -c "
import json
ef = json.load(open('bnccdev/dados/bncc-2018/ensino-fundamental.json'))
h = next(x for x in ef['habilidades'] if x['codigo'] == 'EF67LP08')
print(h['texto'])
print(h['fonte']['localizador_pdf'])
"
```

Exemplo de registro (Ensino Fundamental):

```json
{
  "codigo": "EF67LP08",
  "texto": "Identificar os efeitos de sentido devidos à escolha de imagens estáticas...",
  "componente": "ef-comp-lp",
  "anos": [6, 7],
  "organizacao": {
    "tipo": "campo_pratica",
    "campos_atuacao": ["ef-comp-lp-catu-campo-jornalistico-midiatico"],
    "pratica_linguagem": "ef-comp-lp-prat-leitura"
  },
  "objetos_conhecimento": ["ef-comp-lp-oc-efeitos-de-sentido-exploracao-da-multissemiose"],
  "vigencia": {"status": "vigente", "desde": "dados-2026.07", "ate": null},
  "fonte": {
    "localizador": "aba Língua Portuguesa, linha 229",
    "localizador_pdf": "Base-Nacional-Comum-Curricular-BNCC.pdf, página PDF 167"
  }
}
```

## Reproduzir a extração

```bash
cd pipeline
python3 extrair.py      # planilhas oficiais → dados/bncc-2018/*.json
python3 extrair_ei.py   # PDF homologado → educacao-infantil.json
python3 verificar.py    # confere cada texto contra o PDF; grava a página
python3 validar.py      # 18 contratos + completude (falha se algo divergir)
```

Dependências: Python 3 e `pdftotext` (poppler). Sem bibliotecas externas.

## Licenças

- **Dados** (`dados/`): [CC BY 4.0](dados/LICENSE.md). Os textos normativos da BNCC são atos oficiais, não protegidos por direito autoral (art. 8º da Lei 9.610/98); a licença cobre a compilação, estruturação e curadoria.
- **Código** (`pipeline/`): [MIT](LICENSE).

O que é aberto aqui é irrevogavelmente aberto: ver [docs/divisao-aberto-comercial.md](docs/divisao-aberto-comercial.md).

## Para agentes de IA

Leia `llms.txt` na raiz. Em resumo: consuma os JSONs de `dados/bncc-2018/`, use os códigos oficiais como chaves (`EF67LP08`, `EM13LGG103`, `EI02TS01`), nunca invente códigos ou textos de habilidade, e cite a fonte que acompanha cada registro.

## Roadmap

Pacote npm e PyPI, servidor MCP e páginas por habilidade chegam na próxima fase, construídos sobre este dataset. Correções de dados exigem referência à fonte oficial no PR.
