"""Extrai o dataset completo de EF e EM das planilhas oficiais do MEC,
mais a espinha estrutural (áreas, componentes, competências, recortes).

Saídas (formato do schema v0.3):
  saida/estrutura.json           espinha comum
  saida/ensino-fundamental.json  1.304 habilidades + contextos de organização
  saida/ensino-medio.json        183 habilidades + competências de área
  saida/decisoes-extracao.json   decisões de interpretação encontradas
"""
import json
import re
import unicodedata
from pathlib import Path

from codigos import decodificar, COMPONENTES_EF, AREAS_EM
from xlsx import Planilha

AQUI = Path(__file__).parent
FONTES = AQUI.parent / 'fontes'
SAIDA = AQUI / 'saida'
DATASET = AQUI.parent / 'dados' / 'bncc-2018'
DATA_VERSION = 'dados-2026.07'

FONTE_EF = {'documento': 'bncc-2018', 'arquivo': 'BNCC_Ensino Fundamental.xlsx',
            'proveniencia': 'exportada de downloadbncc.mec.gov.br em 23/06/2023'}
FONTE_EM = {'documento': 'bncc-2018', 'arquivo': 'BNCC_Ensino_Medio.xlsx',
            'proveniencia': 'exportada de downloadbncc.mec.gov.br em 23/06/2023'}

DECISOES = []

SIGLA_POR_ABA_EF = {'Língua Portuguesa': 'LP', 'Arte': 'AR', 'Educação Física': 'EF',
                    'Língua Inglesa': 'LI', 'Matemática': 'MA', 'Ciências': 'CI',
                    'Geografia': 'GE', 'História': 'HI', 'Ensino Religioso': 'ER'}
AREA_POR_COMPONENTE_EF = {'LP': 'linguagens', 'AR': 'linguagens', 'EF': 'linguagens', 'LI': 'linguagens',
                          'MA': 'matematica', 'CI': 'ciencias-da-natureza',
                          'GE': 'ciencias-humanas', 'HI': 'ciencias-humanas', 'ER': 'ensino-religioso'}
PAPEL_POR_CABECALHO = {'COMPONENTE': 'componente', 'ANO/FAIXA': 'anos',
                       'UNIDADES TEMÁTICAS': 'unidade_tematica', 'CAMPOS DE ATUAÇÃO': 'campos_atuacao',
                       'PRÁTICAS DE LINGUAGEM': 'pratica_linguagem', 'EIXO': 'eixo',
                       'OBJETOS DE CONHECIMENTO': 'objetos', 'HABILIDADES': 'habilidade'}


def slug(texto):
    s = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-zA-Z0-9]+', '-', s).strip('-').lower()


def limpa(t):
    return re.sub(r'\s+', ' ', t or '').strip()


def anos_de(texto):
    nums = [int(n) for n in re.findall(r'(\d)º', texto)]
    if 'ao' in texto and len(nums) == 2:
        return list(range(nums[0], nums[1] + 1))
    return nums


# ------------------------------------------------------------------------- EF

def extrair_ef(pl):
    habilidades, contextos = [], {}  # contextos: unidades, objetos, campos, práticas, eixos

    def contexto(tipo, prefixo, nome, aba):
        cid = f'{prefixo}-{tipo}-{slug(nome)}'
        contextos.setdefault(cid, {'id': cid, 'tipo': tipo, 'nome': nome,
                                   'componente': prefixo, 'fonte': dict(FONTE_EF, localizador=f'aba {aba}')})
        return cid

    for aba, sigla in SIGLA_POR_ABA_EF.items():
        comp_id = f'ef-comp-{sigla.lower()}'
        papel = {}       # coluna → papel, lido do cabeçalho (linha 3)
        atual = {}       # forward-fill de células mescladas
        for n, cel in pl.linhas(aba):
            if n < 3:
                continue
            if n == 3:
                papel = {col: PAPEL_POR_CABECALHO[limpa(v)] for col, v in cel.items()
                         if limpa(v) in PAPEL_POR_CABECALHO}
                continue
            for col, valor in cel.items():
                if col in papel and valor.strip():
                    atual[papel[col]] = valor
            hab = limpa(atual.get('habilidade', ''))
            m = re.match(r'^\((EF\d{2}[A-Z]{2}\d{2})\)\s*(.+)$', hab, re.S)
            if not m or limpa(cel.get([c for c, p in papel.items() if p == 'habilidade'][0], '')) == '':
                continue
            codigo, texto = m.group(1), limpa(m.group(2))
            atual['habilidade'] = ''  # consome; forward-fill não vale p/ habilidade

            dec = decodificar(codigo)
            if dec['componente'] != sigla:
                DECISOES.append(f'EF: {codigo} na aba {aba!r}; realocado para '
                                f'{dec["componente_nome"]} pela decodificação do código.')
                comp_real = f"ef-comp-{dec['componente'].lower()}"
            else:
                comp_real = comp_id

            anos_planilha = anos_de(atual.get('anos', ''))
            if anos_planilha and anos_planilha != dec['anos']:
                DECISOES.append(f'EF: {codigo} — ano/faixa da planilha {anos_planilha} difere do código '
                                f'{dec["anos"]}; prevalece o código.')

            if 'campos_atuacao' in atual and comp_real == 'ef-comp-lp':
                org = {'tipo': 'campo_pratica',
                       'campos_atuacao': [contexto('catu', comp_real, limpa(c), aba)
                                          for c in atual['campos_atuacao'].split('\n') if limpa(c)],
                       'pratica_linguagem': contexto('prat', comp_real, limpa(atual.get('pratica_linguagem', '')), aba)}
            elif 'eixo' in atual and comp_real == 'ef-comp-li':
                org = {'tipo': 'eixo', 'eixo': contexto('eixo', comp_real, limpa(atual['eixo']), aba),
                       'unidade_tematica': contexto('ut', comp_real, limpa(atual.get('unidade_tematica', '')), aba)}
            else:
                org = {'tipo': 'unidade_tematica',
                       'unidade_tematica': contexto('ut', comp_real, limpa(atual.get('unidade_tematica', '')), aba)}

            objetos = [contexto('oc', comp_real, limpa(o), aba)
                       for o in (atual.get('objetos', '') or '').split('\n') if limpa(o)]

            habilidades.append({
                'codigo': codigo, 'documento': 'bncc-2018', 'texto': texto,
                'componente': comp_real, 'anos': dec['anos'], 'organizacao': org,
                'objetos_conhecimento': objetos,
                'vigencia': {'status': 'vigente', 'desde': DATA_VERSION, 'ate': None},
                'fonte': dict(FONTE_EF, localizador=f'aba {aba}, linha {n}'),
            })
    return habilidades, contextos


# ------------------------------------------------------------------------- EM

ABAS_HAB_EM = ['Hab. de Linguagens e suas Tecn', 'Hab. de Matemática e suas Tec',
               'Hab. de Ciências da Natureza ', 'Hab. de Ciências Humanas e So', 'Hab. de Língua Portuguesa']


def extrair_em(pl):
    habilidades, contextos = [], {}
    for aba in ABAS_HAB_EM:
        for n, cel in pl.linhas(aba):
            cod = (cel.get('B') or '').strip()
            if not re.match(r'^EM13', cod):
                continue
            dec = decodificar(cod)
            eh_lp = dec.get('componente') == 'LP'
            area_id = f"em-area-{dec['area'].lower()}"
            aba_esperada = 'Hab. de Língua Portuguesa' if eh_lp else {
                'LGG': 'Hab. de Linguagens e suas Tecn', 'MAT': 'Hab. de Matemática e suas Tec',
                'CNT': 'Hab. de Ciências da Natureza ', 'CHS': 'Hab. de Ciências Humanas e So'}[dec['area']]
            if aba != aba_esperada:
                DECISOES.append(f'EM: {cod} na aba {aba!r}; realocado para {area_id} pela decodificação do código.')

            if eh_lp:
                comps = [f'em-area-lgg-ce-{int(c):02d}' for c in re.findall(r'\d+', cel.get('D', ''))]
                if not comps:
                    DECISOES.append(f'EM/LP: {cod} sem competência na coluna D da planilha.')
                catu = limpa(cel.get('E', ''))
                catus = []
                if catu:
                    cid = f'em-comp-lp-catu-{slug(catu)}'
                    contextos.setdefault(cid, {'id': cid, 'tipo': 'catu', 'nome': catu, 'componente': 'em-comp-lp',
                                               'fonte': dict(FONTE_EM, localizador=f'aba {aba}')})
                    catus.append(cid)
            else:
                comps = [f"em-area-{dec['area'].lower()}-ce-{dec['competencia_especifica']:02d}"]
                catus = None

            habilidades.append({
                'codigo': cod, 'documento': 'bncc-2018', 'texto': limpa(cel.get('C', '')),
                'area': area_id, 'componente': 'em-comp-lp' if eh_lp else None,
                'competencias_especificas': comps, 'campos_atuacao_social': catus or None,
                'seriacao': None,
                'vigencia': {'status': 'vigente', 'desde': DATA_VERSION, 'ate': None},
                'fonte': dict(FONTE_EM, localizador=f'aba {aba!r}, linha {n}'),
            })
    return sorted(habilidades, key=lambda h: h['codigo']), contextos


# ------------------------------------------------------- competências e espinha

def extrair_competencias(pl_ef, pl_em):
    gerais_ef, gerais_em, especificas = [], [], []

    for n, cel in pl_ef.linhas('Competências gerais'):
        t = limpa(cel.get('A', ''))
        if n >= 3 and len(t) > 40:
            gerais_ef.append(t)
    for n, cel in pl_em.linhas('Competências Gerais'):
        t = limpa(cel.get('A', ''))
        if n >= 3 and len(t) > 40:
            gerais_em.append(t)
    if gerais_ef != gerais_em:
        DECISOES.append('Competências gerais divergem entre as planilhas de EF e EM — comparar e decidir fonte.')
    gerais = [{'id': f'cg-{i:02d}', 'documento': 'bncc-2018', 'tipo': 'geral', 'numero': i, 'texto': t,
               'fonte': dict(FONTE_EF, localizador='aba Competências gerais')}
              for i, t in enumerate(gerais_ef, 1)]

    # EF: abas "Comps. de X" — de área (5 áreas) ou de componente (áreas multi-componente)
    ABAS_COMP_EF = {
        'Comps. de Linguagens': ('area', 'ef-area-linguagens'),
        'Comps. de Matemática': ('area', 'ef-area-matematica'),
        'Comps. de Ciências da nature': ('area', 'ef-area-ciencias-da-natureza'),
        'Comps. de Ciências humanas': ('area', 'ef-area-ciencias-humanas'),
        'Comps. de Ensino religioso': ('area', 'ef-area-ensino-religioso'),
        'Comps. de Língua Portuguesa': ('componente', 'ef-comp-lp'),
        'Comps. de Arte': ('componente', 'ef-comp-ar'),
        'Comps. de Educação Física': ('componente', 'ef-comp-ef'),
        'Comps. de Língua Inglesa': ('componente', 'ef-comp-li'),
        'Comps. de Geografia': ('componente', 'ef-comp-ge'),
        'Comps. de História': ('componente', 'ef-comp-hi'),
    }
    for aba, (nivel, dono) in ABAS_COMP_EF.items():
        num = 0
        for n, cel in pl_ef.linhas(aba):
            t = limpa(cel.get('A', ''))
            if n >= 3 and len(t) > 40:
                num += 1
                especificas.append({'id': f'{dono}-ce-{num:02d}', 'documento': 'bncc-2018',
                                    'tipo': f'especifica_de_{nivel}', nivel: dono, 'numero': num, 'texto': t,
                                    'fonte': dict(FONTE_EF, localizador=f'aba {aba}')})

    ABAS_COMP_EM = {'Comp. de Linguagens e suas Tec': 'em-area-lgg', 'Comp. de Matemática e suas Te': 'em-area-mat',
                    'Comp. de Ciências da Natureza': 'em-area-cnt', 'Comp. de Ciências Humanas e S': 'em-area-chs'}
    for aba, area in ABAS_COMP_EM.items():
        for n, cel in pl_em.linhas(aba):
            num = (cel.get('A') or '').strip()
            if num.isdigit():
                especificas.append({'id': f'{area}-ce-{int(num):02d}', 'documento': 'bncc-2018',
                                    'tipo': 'especifica_de_area', 'area': area, 'numero': int(num),
                                    'texto': limpa(cel.get('B', '')),
                                    'fonte': dict(FONTE_EM, localizador=f'aba {aba}')})
    return gerais, especificas


def espinha(gerais, especificas):
    pdf = {'documento': 'bncc-2018', 'arquivo': 'Base-Nacional-Comum-Curricular-BNCC.pdf'}
    areas = (
        [{'id': f'ef-area-{s}', 'etapa': 'EF', 'nome': n, 'documento': 'bncc-2018'} for s, n in [
            ('linguagens', 'Linguagens'), ('matematica', 'Matemática'),
            ('ciencias-da-natureza', 'Ciências da Natureza'), ('ciencias-humanas', 'Ciências Humanas'),
            ('ensino-religioso', 'Ensino Religioso')]] +
        [{'id': f'em-area-{s.lower()}', 'etapa': 'EM', 'nome': n, 'documento': 'bncc-2018'}
         for s, n in AREAS_EM.items()])
    componentes = [{'id': f'ef-comp-{s.lower()}', 'etapa': 'EF', 'nome': n, 'sigla_codigo': s,
                    'area': f'ef-area-{AREA_POR_COMPONENTE_EF[s]}', 'tem_aprendizagens_proprias': True,
                    'presenca': {'anos': [6, 7, 8, 9]} if s == 'LI' else None}
                   for s, n in COMPONENTES_EF.items()]
    componentes += [{'id': 'em-comp-lp', 'etapa': 'EM', 'nome': 'Língua Portuguesa', 'sigla_codigo': 'LP',
                     'area': 'em-area-lgg', 'tem_aprendizagens_proprias': True,
                     'destaque_legal': 'Lei nº 13.415/2017'},
                    {'id': 'em-comp-mat', 'etapa': 'EM', 'nome': 'Matemática', 'sigla_codigo': None,
                     'area': 'em-area-mat', 'tem_aprendizagens_proprias': True,
                     'destaque_legal': 'Lei nº 13.415/2017',
                     'nota': 'detalhamento coincide com a área (componente único)'}]
    componentes += [{'id': f'em-comp-{slug(n)}', 'etapa': 'EM', 'nome': n, 'sigla_codigo': None,
                     'area': f'em-area-{a}', 'tem_aprendizagens_proprias': False,
                     'fonte': dict(pdf, localizador='p. 33 (PDF da estrutura)')}
                    for n, a in [('Arte', 'lgg'), ('Educação Física', 'lgg'), ('Língua Inglesa', 'lgg'),
                                 ('Biologia', 'cnt'), ('Física', 'cnt'), ('Química', 'cnt'),
                                 ('História', 'chs'), ('Geografia', 'chs'), ('Sociologia', 'chs'), ('Filosofia', 'chs')]]
    recortes = ([{'id': f'ei-grupo-0{i}', 'etapa': 'EI', 'tipo': 'grupo_etario', 'nome': n, 'faixa': f}
                 for i, (n, f) in enumerate([('Bebês', '0–1a6m'), ('Crianças bem pequenas', '1a7m–3a11m'),
                                             ('Crianças pequenas', '4a–5a11m')], 1)] +
                [{'id': f'ef-ano-{a:02d}', 'etapa': 'EF', 'tipo': 'ano', 'numero': a,
                  'segmento': 'anos_iniciais' if a <= 5 else 'anos_finais'} for a in range(1, 10)] +
                [{'id': 'em-sem-seriacao', 'etapa': 'EM', 'tipo': 'sem_seriacao',
                  'nota': 'habilidades sem seriação; progressão definida pelos currículos (BNCC p. 32, 34)'}])
    campos_ei = [{'id': f'ei-campo-{s.lower()}', 'nome': n, 'documento': 'bncc-2018'}
                 for s, n in [('EO', 'O eu, o outro e o nós'), ('CG', 'Corpo, gestos e movimentos'),
                              ('TS', 'Traços, sons, cores e formas'), ('EF', 'Escuta, fala, pensamento e imaginação'),
                              ('ET', 'Espaços, tempos, quantidades, relações e transformações')]]
    direitos = [{'id': f'ei-direito-{slug(n)}', 'nome': n, 'documento': 'bncc-2018'}
                for n in ['Conviver', 'Brincar', 'Participar', 'Explorar', 'Expressar', 'Conhecer-se']]
    return {
        'documento_curricular': [{'id': 'bncc-2018', 'nome': 'Base Nacional Comum Curricular',
                                  'tipo': 'base_nacional', 'esfera': 'federal', 'derivado_de': None},
                                 {'id': 'computacao-2022',
                                  'nome': 'Computação na Educação Básica (complemento à BNCC)',
                                  'tipo': 'complemento', 'esfera': 'federal', 'derivado_de': 'bncc-2018'}],
        'etapas': [{'id': 'EI', 'nome': 'Educação Infantil'}, {'id': 'EF', 'nome': 'Ensino Fundamental'},
                   {'id': 'EM', 'nome': 'Ensino Médio'}],
        'modalidades': [{'id': 'eja', 'nome': 'Educação de Jovens e Adultos', 'transversal_a': ['EF', 'EM'],
                         'segmentos': [{'id': 'eja-1', 'corresponde_a': 'EF anos iniciais'},
                                       {'id': 'eja-2', 'corresponde_a': 'EF anos finais'},
                                       {'id': 'eja-3', 'corresponde_a': 'EM'}]}],
        'areas_conhecimento': areas, 'componentes_curriculares': componentes,
        'recortes_temporais': recortes, 'campos_experiencias': campos_ei,
        'direitos_aprendizagem': direitos,
        'competencias_gerais': gerais, 'competencias_especificas': especificas,
    }


if __name__ == '__main__':
    SAIDA.mkdir(exist_ok=True); DATASET.mkdir(parents=True, exist_ok=True)
    pl_ef = Planilha(FONTES / 'BNCC_Ensino Fundamental.xlsx')
    pl_em = Planilha(FONTES / 'BNCC_Ensino_Medio.xlsx')

    hab_ef, ctx_ef = extrair_ef(pl_ef)
    hab_em, ctx_em = extrair_em(pl_em)
    gerais, especificas = extrair_competencias(pl_ef, pl_em)
    est = espinha(gerais, especificas)

    (DATASET / 'ensino-fundamental.json').write_text(json.dumps(
        {'habilidades': hab_ef, 'contextos_organizacao': sorted(ctx_ef.values(), key=lambda c: c['id'])},
        ensure_ascii=False, indent=2))
    (DATASET / 'ensino-medio.json').write_text(json.dumps(
        {'habilidades': hab_em, 'contextos_organizacao': sorted(ctx_em.values(), key=lambda c: c['id'])},
        ensure_ascii=False, indent=2))
    (DATASET / 'estrutura.json').write_text(json.dumps(est, ensure_ascii=False, indent=2))
    (SAIDA / 'decisoes-extracao.json').write_text(json.dumps(DECISOES, ensure_ascii=False, indent=2))

    from collections import Counter
    print(f'EF: {len(hab_ef)} habilidades', dict(Counter(h["componente"] for h in hab_ef)))
    print(f'EM: {len(hab_em)} habilidades', dict(Counter(h["area"] for h in hab_em)))
    print(f'contextos: EF {len(ctx_ef)}, EM {len(ctx_em)} | competências: {len(gerais)} gerais, {len(especificas)} específicas')
    print(f'decisões: {len(DECISOES)}')
    for d in DECISOES:
        print('  -', d)
