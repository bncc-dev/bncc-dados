"""Extrai os objetivos de aprendizagem da EI (campo 'Traços, sons, cores e formas')
do PDF oficial de 2017 — a EI não tem planilha disponível (ferramenta do MEC fora
do ar; ver análise de fontes §8.5).

Estratégia: pdftotext em ordem de leitura; cada objetivo começa no marcador
"(EIggTSnn)" e termina no próximo marcador ou fim de bloco. O alinhamento
horizontal (mesmo aspecto entre grupos etários) é reconstruído pela posição
sequencial nn — heurística validada por contagem e marcada para revisão
pedagógica (candidata a DECISOES.md).
"""
import json
import re
import subprocess
from pathlib import Path

AQUI = Path(__file__).parent
PDF = AQUI.parent / 'fontes' / 'Base-Nacional-Comum-Curricular-BNCC.pdf'
SAIDA = AQUI / 'saida'
DATASET = AQUI.parent / 'dados' / 'bncc-2018'
DATA_VERSION = 'dados-2026.07'

GRUPOS = {'01': 'ei-grupo-01', '02': 'ei-grupo-02', '03': 'ei-grupo-03'}
FONTE = {'documento': 'bncc-2018', 'arquivo': 'Base-Nacional-Comum-Curricular-BNCC.pdf',
         'proveniencia': 'BNCC completa homologada (601 p.), obtida em 09/07/2026'}


CAMPOS = ['EO', 'CG', 'TS', 'EF', 'ET']


def extrair_todos():
    raw = subprocess.run(['pdftotext', '-enc', 'UTF-8', str(PDF), '-'],
                         capture_output=True, check=True).stdout.decode('utf-8')
    paginas = raw.split('\f')

    objetivos = {}
    pat = re.compile(r'\((EI(0[123])(EO|CG|TS|EF|ET)(\d{2}))\)\s*')
    for num_pag, pag in enumerate(paginas, start=1):
        marcadores = list(pat.finditer(pag))
        for i, m in enumerate(marcadores):
            codigo, grupo, campo, seq = m.group(1), m.group(2), m.group(3), m.group(4)
            fim = marcadores[i + 1].start() if i + 1 < len(marcadores) else len(pag)
            texto = pag[m.end():fim]
            # corta no fim da célula: quebra dupla ou cabeçalho de seção em caixa alta
            texto = re.split(r'\n\s*\n|CAMPO DE EXPERI|OBJETIVOS DE APRENDIZAGEM', texto)[0]
            texto = re.sub(r'-\s*\n\s*', '', texto)
            texto = re.sub(r'\s+', ' ', texto).strip()
            # o capítulo de estrutura traz exemplos (p. ~26) — fica com a ocorrência
            # da seção da EI (páginas posteriores), que tem a célula completa
            ja = objetivos.get(codigo)
            if ja is None or num_pag > ja['_pagina']:
                objetivos[codigo] = {
                    'codigo': codigo,
                    'documento': 'bncc-2018',
                    'texto': texto,
                    'campo_experiencias': f'ei-campo-{campo.lower()}',
                    'grupo_etario': GRUPOS[grupo],
                    'alinhamento': f'ei-align-{campo.lower()}-{seq}',
                    'vigencia': {'status': 'vigente', 'desde': DATA_VERSION, 'ate': None},
                    'fonte': dict(FONTE, localizador=f'página PDF {num_pag}'),
                    '_pagina': num_pag,
                }
    for o in objetivos.values():
        o.pop('_pagina')

    alinhamentos = {}
    for o in objetivos.values():
        alinhamentos.setdefault(o['alinhamento'], {
            'id': o['alinhamento'], 'campo_experiencias': o['campo_experiencias'], 'objetivos': [],
            'nota': 'pareamento pela posição sequencial nn (heurística; revisão pedagógica pendente)',
        })['objetivos'].append(o['codigo'])
    for a in alinhamentos.values():
        a['objetivos'].sort()

    return {'objetivos': sorted(objetivos.values(), key=lambda o: o['codigo']),
            'alinhamentos': sorted(alinhamentos.values(), key=lambda a: a['id'])}


if __name__ == '__main__':
    dados = extrair_todos()
    DATASET.mkdir(parents=True, exist_ok=True)
    (DATASET / 'educacao-infantil.json').write_text(json.dumps(dados, ensure_ascii=False, indent=2))
    from collections import Counter
    por_campo = Counter(o['campo_experiencias'] for o in dados['objetivos'])
    por_grupo = Counter(o['grupo_etario'] for o in dados['objetivos'])
    print(f"EI: {len(dados['objetivos'])} objetivos, {len(dados['alinhamentos'])} alinhamentos")
    print('  por campo:', dict(por_campo))
    print('  por grupo:', dict(por_grupo))
    incompletos = [a['id'] for a in dados['alinhamentos'] if len(a['objetivos']) != 3]
    print('  alinhamentos incompletos (≠3 objetivos):', incompletos or 'nenhum')
