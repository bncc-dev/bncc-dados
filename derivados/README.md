# Derivados · gerados, não editar

Tudo neste diretório é gerado por `pipeline/derivar.py` a partir dos JSONs de `dados/bncc-2018/` (que são a fonte canônica). Edições manuais aqui serão sobrescritas e reprovadas no CI.

| Arquivo | O que é |
|---|---|
| `bncc.sqlite` | Banco relacional completo: tabelas espelho + junções N:N (habilidade x objeto, habilidade x competência, alinhamento x objetivo, anos), índices e tabela `meta` (data_version, checksums das fontes) |
| `bncc.sql` | Dump lógico do banco (texto). É ele que o CI compara para conferir reprodutibilidade, já que os bytes do .sqlite variam entre versões da biblioteca |
| `csv/*.csv` | Uma planilha por entidade principal, formato amigável a editor de planilhas: colunas de lista usam o separador `" | "` (ex.: `anos = "6 | 7"`). Relações completas ficam no SQLite |

Exemplo de consulta:

```bash
sqlite3 derivados/bncc.sqlite "
SELECT h.codigo, c.nome AS pratica FROM habilidade_ef h
JOIN contexto_organizacao c ON c.id = h.pratica_linguagem
JOIN habilidade_ef_ano a ON a.codigo = h.codigo
WHERE h.componente = 'ef-comp-lp' AND a.ano = 6 LIMIT 5;"
```
