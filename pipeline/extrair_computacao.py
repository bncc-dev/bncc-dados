"""Extrai o complemento de Computação (anexo ao Parecer CNE/CEB 2/2022)
→ dados/computacao-2022/computacao.json.

Insumos: o anexo oficial (fontes/anexo-ao-parecer-cneceb-no-2-2022-bncc-computacao.pdf),
de onde vem a página de cada código, e o mapa de estrutura
fontes/computacao-estrutura.json (eixos, objetos de conhecimento, competências
e textos), gerado uma vez por gerar_mapa_computacao.py a partir das planilhas
de apoio da Secretaria de Educação de Pernambuco (decisão 13 do DECISOES.md).
O mapa nunca é fonte de verdade: cada texto é verificado caractere a caractere
contra o anexo oficial por verificar_computacao.py, e o PDF sempre prevalece.

Escopo núcleo (decisão de 11/07): eixos, objetos de conhecimento (com
hierarquia pai/sub nos anos finais), competências do complemento e as 141
aprendizagens. Os descritores de agrupamento, explicações e exemplos do
anexo ficam para iteração futura (DECISOES.md).
"""
import json
import re
from pathlib import Path

from anexo_computacao import ANEXO, paginas_anexo
from codigos import decodificar
from extrair import slug

AQUI = Path(__file__).parent
MAPA = AQUI.parent / 'fontes' / 'computacao-estrutura.json'
DATASET = AQUI.parent / 'dados' / 'computacao-2022'
DATA_VERSION = 'dados-2026.07'

EIXOS = {'PENSAMENTO COMPUTACIONAL': 'co-eixo-pensamento-computacional',
         'MUNDO DIGITAL': 'co-eixo-mundo-digital',
         'CULTURA DIGITAL': 'co-eixo-cultura-digital'}
EIXOS_NOME = {'co-eixo-pensamento-computacional': 'Pensamento Computacional',
              'co-eixo-mundo-digital': 'Mundo Digital',
              'co-eixo-cultura-digital': 'Cultura Digital'}

# O anexo oficial imprime "(EF05CO011)", único código com 3 dígitos de
# sequência, claramente o 11º do 5º ano (vem após EF05CO10). Canonizado
# para a gramática dos demais 140; decisão registrada em DECISOES.md e a
# forma impressa fica no localizador da fonte.
CANONIZACOES = {'EF05CO011': 'EF05CO11'}


def fonte(arquivo_xlsx, linha, pagina_pdf, impresso=None, codigo=None):
    loc = f'{arquivo_xlsx} · linha {linha}'
    if impresso and codigo and impresso != codigo:
        loc += f' · impresso como ({impresso}) no anexo e na planilha (DECISOES.md)'
    return {'documento': 'computacao-2022', 'arquivo': ANEXO.name,
            'proveniencia': 'estrutura via planilhas Sec. Educação de Pernambuco; texto verificado contra o anexo oficial',
            'localizador': loc,
            'localizador_pdf': f'página PDF {pagina_pdf}'}


def fonte_de(item, pagina_por_codigo):
    return fonte(item['planilha'], item['linha'], pagina_por_codigo[item['codigo']],
                 item['impresso'] or item['codigo'], item['codigo'])


def vigencia():
    return {'status': 'vigente', 'desde': DATA_VERSION, 'ate': None}


def paginas_por_codigo():
    """Primeira página do anexo onde cada código aparece como marcador."""
    paginas = paginas_anexo()
    onde = {}
    for num, pag in enumerate(paginas, start=1):
        for cod in re.findall(r'\((E[IFM]\d{2}CO\d{2,3})\)', pag):
            onde.setdefault(CANONIZACOES.get(cod, cod), num)
    return onde


def id_objeto(nome):
    return f'co-obj-{slug(nome)}'


def principal():
    mapa = json.loads(MAPA.read_text())
    pagina_por_codigo = paginas_por_codigo()

    competencias = (
        [{'id': f'computacao-cg-{c["numero"]:02d}', 'documento': 'computacao-2022',
          'tipo': 'geral_computacao', 'numero': c['numero'], 'texto': c['texto'],
          'fonte': {'documento': 'computacao-2022', 'arquivo': ANEXO.name,
                    'proveniencia': 'competências gerais do complemento (cabeçalho das planilhas de EF, verificadas contra o anexo)'}}
         for c in mapa['competencias_gerais']] +
        [{'id': f'computacao-em-ce-{c["numero"]:02d}', 'documento': 'computacao-2022',
          'tipo': 'especifica_em_computacao', 'numero': c['numero'], 'texto': c['texto'],
          'fonte': {'documento': 'computacao-2022', 'arquivo': ANEXO.name,
                    'proveniencia': 'competências específicas do EM (cabeçalho da planilha de EM, verificadas contra o anexo)'}}
         for c in mapa['competencias_especificas_em']])

    objetos = [{'id': id_objeto(o['nome']), 'documento': 'computacao-2022', 'nome': o['nome'],
                'pai': id_objeto(o['pai']) if o['pai'] else None}
               for o in mapa['objetos_conhecimento']]
    objetos.sort(key=lambda o: o['id'])
    ids_objetos = {o['id'] for o in objetos}

    objetivos_ei = [{
        'codigo': o['codigo'], 'documento': 'computacao-2022', 'texto': o['texto'],
        'eixo': o['eixo'], 'grupo_etario': 'ei-grupo-03', 'vigencia': vigencia(),
        'fonte': fonte_de(o, pagina_por_codigo),
    } for o in mapa['objetivos_ei']]

    habilidades_ef = []
    for h in mapa['habilidades_ef']:
        obj = id_objeto(h['objeto'])
        if obj not in ids_objetos:
            raise SystemExit(f'{h["codigo"]}: objeto fora da lista do mapa: {h["objeto"]!r}')
        habilidades_ef.append({
            'codigo': h['codigo'], 'documento': 'computacao-2022', 'texto': h['texto'],
            'eixo': h['eixo'], 'objetos_conhecimento': [obj],
            'anos': decodificar(h['codigo'])['anos'], 'vigencia': vigencia(),
            'fonte': fonte_de(h, pagina_por_codigo),
        })
    habilidades_ef.sort(key=lambda h: (h['anos'][0], len(h['anos']), h['codigo']))

    habilidades_em = [{
        'codigo': h['codigo'], 'documento': 'computacao-2022', 'texto': h['texto'],
        'competencia': f'computacao-em-ce-{h["competencia_especifica"]:02d}', 'vigencia': vigencia(),
        'fonte': fonte_de(h, pagina_por_codigo),
    } for h in mapa['habilidades_em']]

    dados = {
        'eixos': [{'id': i, 'documento': 'computacao-2022', 'nome': n}
                  for i, n in EIXOS_NOME.items()],
        'objetos_conhecimento': objetos,
        'competencias': competencias,
        'objetivos_ei': objetivos_ei,
        'habilidades_ef': habilidades_ef,
        'habilidades_em': habilidades_em,
    }
    DATASET.mkdir(parents=True, exist_ok=True)
    (DATASET / 'computacao.json').write_text(json.dumps(dados, ensure_ascii=False, indent=2))
    print(f'computacao-2022: EI {len(objetivos_ei)} + EF {len(habilidades_ef)} + EM {len(habilidades_em)} '
          f'= {len(objetivos_ei) + len(habilidades_ef) + len(habilidades_em)} aprendizagens · '
          f'{len(objetos)} objetos · {len(competencias)} competências')


if __name__ == '__main__':
    principal()
