"""Decodificador de códigos da BNCC — as três gramáticas (schema §6) e a
gramática do complemento de Computação (anexo ao Parecer CNE/CEB 2/2022).

Entregável da Fase 1 (dado + função). Usado pela extração (realocação de
linhas em abas erradas) e pela consulta 5 do caso âncora.

Computação (componente CO, documento computacao-2022): EI03CO## (o anexo só
define objetivos para a pré-escola), EF##CO## (anos 01-09 e blocos 15/69) e
EM13CO## (sequência simples, sem dígito de competência no código).
"""
import re

CAMPOS_EI = {'EO': 'O eu, o outro e o nós', 'CG': 'Corpo, gestos e movimentos',
             'TS': 'Traços, sons, cores e formas', 'EF': 'Escuta, fala, pensamento e imaginação',
             'ET': 'Espaços, tempos, quantidades, relações e transformações'}
GRUPOS_EI = {'01': 'Bebês (0–1a6m)', '02': 'Crianças bem pequenas (1a7m–3a11m)',
             '03': 'Crianças pequenas (4a–5a11m)'}
COMPONENTES_EF = {'AR': 'Arte', 'CI': 'Ciências', 'EF': 'Educação Física', 'ER': 'Ensino Religioso',
                  'GE': 'Geografia', 'HI': 'História', 'LI': 'Língua Inglesa',
                  'LP': 'Língua Portuguesa', 'MA': 'Matemática'}
BLOCOS_EF = {'15': [1, 2, 3, 4, 5], '69': [6, 7, 8, 9], '12': [1, 2], '35': [3, 4, 5],
             '67': [6, 7], '89': [8, 9]}
BLOCOS_VALIDOS_POR_COMPONENTE = {'AR': {'15', '69'}, 'LP': {'15', '69', '12', '35', '67', '89'},
                                 'EF': {'12', '35', '67', '89'}}
AREAS_EM = {'LGG': 'Linguagens e suas Tecnologias', 'MAT': 'Matemática e suas Tecnologias',
            'CNT': 'Ciências da Natureza e suas Tecnologias', 'CHS': 'Ciências Humanas e Sociais Aplicadas'}


def decodificar(codigo):
    """Decodifica um código BNCC → dict estruturado, ou lança ValueError."""
    codigo = codigo.strip().upper()

    # ---- complemento de Computação (CO) ----
    m = re.fullmatch(r'EI03CO(\d{2})', codigo)
    if m:
        return {'codigo': codigo, 'etapa': 'EI', 'grupo_etario': '03',
                'grupo_etario_nome': GRUPOS_EI['03'], 'componente': 'CO',
                'componente_nome': 'Computação', 'documento': 'computacao-2022',
                'sequencia': int(m.group(1))}

    m = re.fullmatch(r'EF(\d{2})CO(\d{2})', codigo)
    if m:
        anos_str, seq = m.groups()
        if anos_str in ('15', '69'):
            anos = BLOCOS_EF[anos_str]
        elif anos_str.startswith('0') and 1 <= int(anos_str) <= 9:
            anos = [int(anos_str)]
        else:
            raise ValueError(f'{codigo}: ano/bloco {anos_str!r} inválido para Computação')
        return {'codigo': codigo, 'etapa': 'EF', 'anos': anos, 'bloco': anos_str in BLOCOS_EF,
                'componente': 'CO', 'componente_nome': 'Computação',
                'documento': 'computacao-2022', 'sequencia': int(seq)}

    m = re.fullmatch(r'EM13CO(\d{2})', codigo)
    if m:
        return {'codigo': codigo, 'etapa': 'EM', 'seriacao': None, 'componente': 'CO',
                'componente_nome': 'Computação', 'documento': 'computacao-2022',
                'sequencia': int(m.group(1))}

    m = re.fullmatch(r'EI(0[123])(EO|CG|TS|EF|ET)(\d{2})', codigo)
    if m:
        grupo, campo, seq = m.groups()
        return {'codigo': codigo, 'etapa': 'EI', 'grupo_etario': grupo,
                'grupo_etario_nome': GRUPOS_EI[grupo], 'campo_experiencias': campo,
                'campo_experiencias_nome': CAMPOS_EI[campo], 'sequencia': int(seq)}

    m = re.fullmatch(r'EF(\d{2})([A-Z]{2})(\d{2})', codigo)
    if m:
        anos_str, comp, seq = m.groups()
        if comp not in COMPONENTES_EF:
            raise ValueError(f'{codigo}: componente {comp!r} desconhecido')
        if anos_str in BLOCOS_EF:
            if anos_str not in BLOCOS_VALIDOS_POR_COMPONENTE.get(comp, set()):
                raise ValueError(f'{codigo}: bloco {anos_str!r} inválido para {COMPONENTES_EF[comp]}')
            anos = BLOCOS_EF[anos_str]
        elif anos_str.startswith('0') and 1 <= int(anos_str) <= 9:
            anos = [int(anos_str)]
        else:
            raise ValueError(f'{codigo}: ano/bloco {anos_str!r} inválido')
        return {'codigo': codigo, 'etapa': 'EF', 'anos': anos, 'bloco': anos_str in BLOCOS_EF,
                'componente': comp, 'componente_nome': COMPONENTES_EF[comp], 'sequencia': int(seq)}

    m = re.fullmatch(r'EM13([A-Z]{3})(\d)(\d{2})', codigo)
    if m and m.group(1) in AREAS_EM:
        area, ce, seq = m.groups()
        return {'codigo': codigo, 'etapa': 'EM', 'seriacao': None, 'area': area,
                'area_nome': AREAS_EM[area], 'competencia_especifica': int(ce), 'sequencia': int(seq)}

    m = re.fullmatch(r'EM13LP(\d{2})', codigo)
    if m:
        return {'codigo': codigo, 'etapa': 'EM', 'seriacao': None, 'area': 'LGG',
                'area_nome': AREAS_EM['LGG'], 'componente': 'LP',
                'competencia_especifica': None, 'sequencia': int(m.group(1))}

    raise ValueError(f'{codigo}: não corresponde a nenhuma gramática BNCC (EI/EF/EM)')
