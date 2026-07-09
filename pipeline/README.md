# Pipeline de extração e validação

Reproduz o dataset a partir das fontes oficiais em `fontes/`. Qualquer pessoa pode rodar e conferir que chega aos mesmos arquivos de `dados/bncc-2018/`.

```bash
python3 extrair.py      # planilhas oficiais → estrutura + EF + EM
python3 extrair_ei.py   # PDF homologado → Educação Infantil
python3 verificar.py    # confere cada texto contra o PDF; grava a página em fonte.localizador_pdf
python3 validar.py      # 18 contratos + completude por varredura; sai com erro se algo falhar
```

Dependências: Python 3 (somente stdlib) e `pdftotext` (poppler).

| Script | Papel |
|---|---|
| `xlsx.py` | Leitor mínimo de xlsx com stdlib |
| `codigos.py` | Decodificador das três gramáticas de código (EI, EF, EM) |
| `extrair.py` | Planilhas → JSON (EF, EM, espinha estrutural) |
| `extrair_ei.py` | PDF → JSON (EI, com alinhamentos entre faixas etárias) |
| `verificar.py` | Match estrito de cada texto contra o PDF homologado |
| `validar.py` | Contratos, completude, diff de regressão (quando disponível) e relatório |

Relatórios gerados em `saida/` (não versionados). O CI executa exatamente esta sequência e ainda confere que o dataset commitado é idêntico ao reproduzido.
