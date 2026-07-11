"""Extrai o complemento de Computação (anexo ao Parecer CNE/CEB 2/2022)
→ dados/computacao-2022/computacao.json.

Estratégia (plano de 11/07/2026): as planilhas da Secretaria de Educação de
Pernambuco (fontes/secedu-pernambuco/) fornecem a ESTRUTURA — células de
eixo/objeto/competência preservadas, que a camada de texto do PDF embaralha.
Elas nunca são fonte de verdade: cada texto extraído é verificado caractere
a caractere contra o anexo oficial por verificar_computacao.py, e o PDF
sempre prevalece. A página de cada código no anexo entra em fonte.localizador_pdf.

Escopo núcleo (decisão de 11/07): eixos, objetos de conhecimento (com
hierarquia pai/sub nos anos finais), competências do complemento e as 140
aprendizagens. Os descritores de agrupamento, explicações e exemplos do
anexo ficam para iteração futura (DECISOES.md).
"""
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from anexo_computacao import ANEXO, paginas_anexo
from codigos import decodificar
from extrair import limpa, slug
from xlsx import NS, Planilha

AQUI = Path(__file__).parent
PE = AQUI.parent / 'fontes' / 'secedu-pernambuco'
DATASET = AQUI.parent / 'dados' / 'computacao-2022'
DATA_VERSION = 'dados-2026.07'

ARQ_EI = 'COMPUTAÇÃO - EDUCAÇÃO INFANTIL .xlsx'
ARQ_EF_INICIAIS = '1º ao 5º ANO - HABILIDADES- BNCC - Computação.xlsx'
ARQ_EF_FINAIS = '6º ao 9º ANO - HABILIDADES - BNCC - Computação .xlsx'
ARQ_EM = 'COMPUTAÇÃO - ENSINO MÉDIO.xlsx'

EIXOS = {'PENSAMENTO COMPUTACIONAL': 'co-eixo-pensamento-computacional',
         'MUNDO DIGITAL': 'co-eixo-mundo-digital',
         'CULTURA DIGITAL': 'co-eixo-cultura-digital'}
EIXOS_NOME = {'co-eixo-pensamento-computacional': 'Pensamento Computacional',
              'co-eixo-mundo-digital': 'Mundo Digital',
              'co-eixo-cultura-digital': 'Cultura Digital'}

RE_HAB = re.compile(r'^\((E[IFM]\d{2}CO\d{2,3})\)\s*(.+)$', re.S)

# O anexo oficial imprime "(EF05CO011)" — único código com 3 dígitos de
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


def grade(caminho):
    """Matriz {(linha, coluna): valor} com células mescladas expandidas."""
    p = Planilha(caminho)
    celulas = {}
    for num, cels in p.linhas(p.abas[0]):
        for col, val in cels.items():
            celulas[(num, col)] = str(val)
    # expande merges: o valor da célula superior-esquerda vale para o range
    # (as células "engolidas" pelo merge existem no XML como vazias)
    z = zipfile.ZipFile(caminho)
    raiz = ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
    merges = raiz.find('m:mergeCells', NS)
    for m in (merges if merges is not None else []):
        c1, l1, c2, l2 = re.fullmatch(r'([A-Z]+)(\d+):([A-Z]+)(\d+)', m.get('ref')).groups()
        valor = celulas.get((int(l1), c1), '')
        if not str(valor).strip():
            continue
        for lin in range(int(l1), int(l2) + 1):
            for col in [chr(c) for c in range(ord(c1), ord(c2) + 1)]:
                if not str(celulas.get((lin, col), '')).strip():
                    celulas[(lin, col)] = valor
    linhas = sorted({l for l, _ in celulas})
    return celulas, linhas


def competencias_de(texto_l2):
    """Divide o bloco 'COMPETÊNCIAS 1. … 2. …' em itens numerados."""
    partes = re.split(r'(?:^|\n)\s*(\d+)\.\s+', texto_l2)
    itens = {}
    for i in range(1, len(partes) - 1, 2):
        itens[int(partes[i])] = limpa(partes[i + 1])
    if list(itens) != list(range(1, len(itens) + 1)):
        raise SystemExit(f'competências fora de sequência: {sorted(itens)}')
    return itens


def separa_codigo(celula, contexto):
    m = RE_HAB.match(celula.strip())
    if not m:
        raise SystemExit(f'célula sem código em {contexto}: {celula[:80]!r}')
    impresso, texto = m.group(1), limpa(m.group(2))
    codigo = CANONIZACOES.get(impresso, impresso)
    decodificar(codigo)  # gramática ou explosão
    return codigo, texto, impresso


def extrair_ei(pagina_por_codigo):
    celulas, linhas = grade(PE / ARQ_EI)
    objetivos = []
    for lin in linhas:
        b = celulas.get((lin, 'B'), '')
        if not b.strip().startswith('(EI'):
            continue
        codigo, texto, impresso = separa_codigo(b, f'EI L{lin}')
        eixo_bruto = limpa(celulas.get((lin, 'A'), ''))
        objetivos.append({
            'codigo': codigo, 'documento': 'computacao-2022', 'texto': texto,
            'eixo': EIXOS[eixo_bruto.upper()],
            'grupo_etario': 'ei-grupo-03',
            'vigencia': {'status': 'vigente', 'desde': DATA_VERSION, 'ate': None},
            'fonte': fonte(ARQ_EI, lin, pagina_por_codigo[codigo], impresso, codigo),
        })
    return objetivos


def extrair_ef(arquivo, col_objeto_pai, col_objeto, col_hab, objetos, pagina_por_codigo):
    celulas, linhas = grade(PE / arquivo)
    habilidades = []
    anos_secao = None
    for lin in linhas:
        a = limpa(celulas.get((lin, 'A'), ''))
        m = re.fullmatch(r'COMPUTAÇÃO - (\d)º ANO', a)
        if m:
            anos_secao = [int(m.group(1))]
            continue
        m = re.fullmatch(r'COMPUTAÇÃO / POR ETAPA - (\d)º ao (\d)º ANO', a)
        if m:
            anos_secao = list(range(int(m.group(1)), int(m.group(2)) + 1))
            continue
        cel_hab = celulas.get((lin, col_hab), '')
        if not cel_hab.strip().startswith('(EF'):
            continue
        codigo, texto, impresso = separa_codigo(cel_hab, f'{arquivo} L{lin}')
        ja = next((h for h in habilidades if h['codigo'] == codigo), None)
        if ja is not None:                     # linha de continuação (célula mesclada)
            if ja['texto'] != texto:
                raise SystemExit(f'{codigo}: repetido com texto diferente (L{lin})')
            continue
        dec = decodificar(codigo)
        if dec['anos'] != anos_secao:
            raise SystemExit(f'{codigo}: anos do código {dec["anos"]} ≠ seção {anos_secao} (L{lin})')

        eixo_bruto = limpa(celulas.get((lin, 'A'), ''))
        if eixo_bruto.upper() not in EIXOS:
            raise SystemExit(f'{codigo}: eixo não reconhecido {eixo_bruto!r} (L{lin})')

        nome_pai = limpa(celulas.get((lin, col_objeto_pai), '')) if col_objeto_pai else ''
        nome_obj = limpa(celulas.get((lin, col_objeto), ''))
        if not nome_obj and nome_pai:          # grupo sem sub-objeto: o pai é a folha
            nome_obj, nome_pai = nome_pai, ''
        if not nome_obj:
            raise SystemExit(f'{codigo}: sem objeto de conhecimento (L{lin})')

        chave_pai = objetos.registrar(nome_pai) if nome_pai else None
        chave_obj = objetos.registrar(nome_obj, chave_pai)

        habilidades.append({
            'codigo': codigo, 'documento': 'computacao-2022', 'texto': texto,
            'eixo': EIXOS[eixo_bruto.upper()],
            'objetos_conhecimento': [chave_obj],   # chave provisória; vira id em principal()
            'anos': dec['anos'],
            'vigencia': {'status': 'vigente', 'desde': DATA_VERSION, 'ate': None},
            'fonte': fonte(arquivo, lin, pagina_por_codigo[codigo], impresso, codigo),
        })
    return habilidades


class RegistroObjetos:
    """Identidade de objetos por slug COMPACTO (sem separadores): as células
    das planilhas quebram palavras no meio ("responsabilidad e"), gerando
    variantes do mesmo nome. A variante canônica é a mais frequente
    (desempate alfabético — determinístico); os nomes finais são conferidos
    contra o anexo pela verificação."""

    def __init__(self):
        self.variantes = {}   # chave compacta → {nome: contagem}
        self.pais = {}        # chave compacta → chave compacta do pai (ou None)

    @staticmethod
    def chave(nome):
        return slug(nome).replace('-', '')

    def registrar(self, nome, chave_pai=None):
        k = self.chave(nome)
        self.variantes.setdefault(k, {})
        self.variantes[k][nome] = self.variantes[k].get(nome, 0) + 1
        ja = self.pais.get(k)
        if ja is not None and chave_pai is not None and ja != chave_pai:
            raise SystemExit(f'objeto {k}: pais conflitantes {ja!r} × {chave_pai!r}')
        if chave_pai is not None:
            self.pais[k] = chave_pai
        else:
            self.pais.setdefault(k, None)
        return k

    def resolver(self):
        """Devolve ({chave: id}, [registros ordenados])."""
        nomes = {k: min(sorted(vs, key=lambda n: (-vs[n], n))[:1])
                 for k, vs in self.variantes.items()}
        ids = {k: f'co-obj-{slug(n)}' for k, n in nomes.items()}
        registros = [{'id': ids[k], 'documento': 'computacao-2022', 'nome': nomes[k],
                      'pai': ids[self.pais[k]] if self.pais[k] else None}
                     for k in sorted(ids, key=lambda k: ids[k])]
        return ids, registros


def extrair_em(competencias_em, pagina_por_codigo):
    celulas, linhas = grade(PE / ARQ_EM)
    por_prefixo = {limpa(t)[:60].lower(): n for n, t in competencias_em.items()}
    habilidades = []
    for lin in linhas:
        b = celulas.get((lin, 'B'), '')
        if not b.strip().startswith('(EM'):
            continue
        codigo, texto, impresso = separa_codigo(b, f'EM L{lin}')
        comp_bruta = limpa(celulas.get((lin, 'A'), ''))
        if not comp_bruta or comp_bruta.upper() == 'COMPETÊNCIA ESPECÍFICA':
            raise SystemExit(f'{codigo}: sem competência específica na coluna A (L{lin})')
        numero = por_prefixo.get(comp_bruta[:60].lower())
        if numero is None:
            raise SystemExit(f'{codigo}: competência não casa com a lista numerada: {comp_bruta[:80]!r}')
        habilidades.append({
            'codigo': codigo, 'documento': 'computacao-2022', 'texto': texto,
            'competencia': f'computacao-em-ce-{numero:02d}',
            'vigencia': {'status': 'vigente', 'desde': DATA_VERSION, 'ate': None},
            'fonte': fonte(ARQ_EM, lin, pagina_por_codigo[codigo], impresso, codigo),
        })
    return habilidades


def paginas_por_codigo():
    """Primeira página do anexo onde cada código aparece como marcador."""
    paginas = paginas_anexo()
    onde = {}
    for num, pag in enumerate(paginas, start=1):
        for cod in re.findall(r'\((E[IFM]\d{2}CO\d{2,3})\)', pag):
            onde.setdefault(CANONIZACOES.get(cod, cod), num)
    return onde


def principal():
    pagina_por_codigo = paginas_por_codigo()

    cel_ini, _ = grade(PE / ARQ_EF_INICIAIS)
    cel_fin, _ = grade(PE / ARQ_EF_FINAIS)
    cel_em, _ = grade(PE / ARQ_EM)
    comp_eb_a = competencias_de(cel_ini[(2, 'A')])
    comp_eb_b = competencias_de(cel_fin[(2, 'A')])
    if comp_eb_a != comp_eb_b:
        raise SystemExit('competências gerais divergem entre as planilhas de EF')
    comp_em = competencias_de(cel_em[(2, 'A')])

    competencias = (
        [{'id': f'computacao-cg-{n:02d}', 'documento': 'computacao-2022',
          'tipo': 'geral_computacao', 'numero': n, 'texto': t,
          'fonte': {'documento': 'computacao-2022', 'arquivo': ANEXO.name,
                    'proveniencia': 'competências gerais do complemento (cabeçalho das planilhas de EF, verificadas contra o anexo)'}}
         for n, t in comp_eb_a.items()] +
        [{'id': f'computacao-em-ce-{n:02d}', 'documento': 'computacao-2022',
          'tipo': 'especifica_em_computacao', 'numero': n, 'texto': t,
          'fonte': {'documento': 'computacao-2022', 'arquivo': ANEXO.name,
                    'proveniencia': 'competências específicas do EM (cabeçalho da planilha de EM, verificadas contra o anexo)'}}
         for n, t in comp_em.items()])

    objetos = RegistroObjetos()
    objetivos_ei = extrair_ei(pagina_por_codigo)
    habilidades_ef = (
        extrair_ef(ARQ_EF_INICIAIS, None, 'B', 'C', objetos, pagina_por_codigo) +
        extrair_ef(ARQ_EF_FINAIS, 'B', 'C', 'E', objetos, pagina_por_codigo))
    habilidades_ef.sort(key=lambda h: (h['anos'][0], len(h['anos']), h['codigo']))
    habilidades_em = extrair_em(comp_em, pagina_por_codigo)

    ids_obj, registros_obj = objetos.resolver()
    for h in habilidades_ef:
        h['objetos_conhecimento'] = [ids_obj[k] for k in h['objetos_conhecimento']]

    dados = {
        'eixos': [{'id': i, 'documento': 'computacao-2022', 'nome': n}
                  for i, n in EIXOS_NOME.items()],
        'objetos_conhecimento': registros_obj,
        'competencias': competencias,
        'objetivos_ei': objetivos_ei,
        'habilidades_ef': habilidades_ef,
        'habilidades_em': habilidades_em,
    }
    DATASET.mkdir(parents=True, exist_ok=True)
    (DATASET / 'computacao.json').write_text(json.dumps(dados, ensure_ascii=False, indent=2))
    print(f'computacao-2022: EI {len(objetivos_ei)} + EF {len(habilidades_ef)} + EM {len(habilidades_em)} '
          f'= {len(objetivos_ei) + len(habilidades_ef) + len(habilidades_em)} aprendizagens · '
          f'{len(registros_obj)} objetos · {len(competencias)} competências')


if __name__ == '__main__':
    principal()
