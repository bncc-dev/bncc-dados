"""Gera fontes/computacao-estrutura.json a partir das planilhas de apoio da
Secretaria de Educação de Pernambuco (decisão 13 do DECISOES.md).

As planilhas não são redistribuídas por este repositório: elas não trazem
licença explícita de redistribuição (decisões 11 e 13). Este script fica
público para documentar como o mapa foi produzido e para regenerá-lo por
quem tiver os arquivos. Uso:

    python3 gerar_mapa_computacao.py /caminho/para/secedu-pernambuco

Os quatro arquivos precisam ter os nomes e os SHA-256 registrados em
fontes/README.md. Sem argumento, procura em fontes/secedu-pernambuco/.

Estratégia (plano de 11/07/2026): as planilhas fornecem a ESTRUTURA
(células de eixo, objeto e competência preservadas, que a camada de texto
do PDF embaralha). Elas nunca são fonte de verdade: cada texto do mapa é
verificado caractere a caractere contra o anexo oficial por
verificar_computacao.py, e o PDF sempre prevalece.
"""
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from codigos import decodificar
from extrair import limpa, slug
from extrair_computacao import CANONIZACOES, EIXOS, MAPA
from xlsx import NS, Planilha

AQUI = Path(__file__).parent

ARQ_EI = 'COMPUTAÇÃO - EDUCAÇÃO INFANTIL .xlsx'
ARQ_EF_INICIAIS = '1º ao 5º ANO - HABILIDADES- BNCC - Computação.xlsx'
ARQ_EF_FINAIS = '6º ao 9º ANO - HABILIDADES - BNCC - Computação .xlsx'
ARQ_EM = 'COMPUTAÇÃO - ENSINO MÉDIO.xlsx'

# SHA-256 dos arquivos usados na geração (os mesmos de fontes/README.md).
SHA256 = {
    ARQ_EI: '1c3df76a1ead3e2df93ecef9eb931ace8b4756d3f203e66188c41e5b97c8e48d',
    ARQ_EF_INICIAIS: '78db18845598bb5efa3acf7e29ab6a2e12313c2913e1e4d7ab781070b40da53a',
    ARQ_EF_FINAIS: '202dab133d4b5b2ea3a0b49ce61792e40fa3cb82f2f45a4aadf892df30e4039c',
    ARQ_EM: '8b19f82ddd4b7ad140dd23120ff005647a8d1b7b9b56a10dc6d6e398dba6cdf9',
}

RE_HAB = re.compile(r'^\((E[IFM]\d{2}CO\d{2,3})\)\s*(.+)$', re.S)


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


def origem(codigo, impresso, arquivo, linha):
    """Campos de rastreio comuns a toda aprendizagem do mapa."""
    return {'impresso': impresso if impresso != codigo else None,
            'planilha': arquivo, 'linha': linha}


def extrair_ei(pe):
    celulas, linhas = grade(pe / ARQ_EI)
    objetivos = []
    for lin in linhas:
        b = celulas.get((lin, 'B'), '')
        if not b.strip().startswith('(EI'):
            continue
        codigo, texto, impresso = separa_codigo(b, f'EI L{lin}')
        eixo_bruto = limpa(celulas.get((lin, 'A'), ''))
        objetivos.append({'codigo': codigo, 'texto': texto, 'eixo': EIXOS[eixo_bruto.upper()],
                          **origem(codigo, impresso, ARQ_EI, lin)})
    return objetivos


def sem_continuacao(celula):
    """Nome de célula sem o marcador "(cont.)" com que o anexo (e as planilhas,
    que o copiam) sinaliza a continuação de um quadro na página seguinte
    ("COMPUTAÇÃO - 9º ANO (CONTINUAÇÃO)", PDF 58). Não é um objeto novo:
    "Segurança cibernética (cont.)" é "Segurança cibernética" (decisão 14)."""
    return re.sub(r'\s*\(cont\.\)\s*$', '', limpa(celula))


def extrair_ef(pe, arquivo, col_objeto_pai, col_objeto, col_hab, objetos):
    celulas, linhas = grade(pe / arquivo)
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

        nome_pai = sem_continuacao(celulas.get((lin, col_objeto_pai), '')) if col_objeto_pai else ''
        nome_obj = sem_continuacao(celulas.get((lin, col_objeto), ''))
        if not nome_obj and nome_pai:          # grupo sem sub-objeto: o pai é a folha
            nome_obj, nome_pai = nome_pai, ''
        if not nome_obj:
            raise SystemExit(f'{codigo}: sem objeto de conhecimento (L{lin})')

        chave_pai = objetos.registrar(nome_pai) if nome_pai else None
        chave_obj = objetos.registrar(nome_obj, chave_pai)

        habilidades.append({'codigo': codigo, 'texto': texto, 'eixo': EIXOS[eixo_bruto.upper()],
                            'objeto': chave_obj,   # chave provisória; vira nome em principal()
                            'anos': dec['anos'],
                            **origem(codigo, impresso, arquivo, lin)})
    return habilidades


class RegistroObjetos:
    """Identidade de objetos por slug COMPACTO (sem separadores): as células
    das planilhas quebram palavras no meio ("responsabilidad e"), gerando
    variantes do mesmo nome. A variante canônica é a mais frequente
    (desempate alfabético, determinístico); os nomes finais são conferidos
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
        """Devolve ({chave: nome canônico}, [{nome, pai}] ordenados pelo id final)."""
        nomes = {k: min(sorted(vs, key=lambda n: (-vs[n], n))[:1])
                 for k, vs in self.variantes.items()}
        registros = [{'nome': nomes[k], 'pai': nomes[self.pais[k]] if self.pais[k] else None}
                     for k in sorted(nomes, key=lambda k: slug(nomes[k]))]
        return nomes, registros


def extrair_em(pe, competencias_em):
    celulas, linhas = grade(pe / ARQ_EM)
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
        habilidades.append({'codigo': codigo, 'texto': texto, 'competencia_especifica': numero,
                            **origem(codigo, impresso, ARQ_EM, lin)})
    return habilidades


def confere_arquivos(pe):
    for arquivo, esperado in SHA256.items():
        caminho = pe / arquivo
        if not caminho.exists():
            raise SystemExit(f'planilha ausente: {caminho}')
        obtido = hashlib.sha256(caminho.read_bytes()).hexdigest()
        if obtido != esperado:
            raise SystemExit(f'SHA-256 divergente em {arquivo}: {obtido} (esperado {esperado})')


def principal():
    pe = Path(sys.argv[1]) if len(sys.argv) > 1 else AQUI.parent / 'fontes' / 'secedu-pernambuco'
    confere_arquivos(pe)

    cel_ini, _ = grade(pe / ARQ_EF_INICIAIS)
    cel_fin, _ = grade(pe / ARQ_EF_FINAIS)
    cel_em, _ = grade(pe / ARQ_EM)
    comp_eb_a = competencias_de(cel_ini[(2, 'A')])
    comp_eb_b = competencias_de(cel_fin[(2, 'A')])
    if comp_eb_a != comp_eb_b:
        raise SystemExit('competências gerais divergem entre as planilhas de EF')
    comp_em = competencias_de(cel_em[(2, 'A')])

    objetos = RegistroObjetos()
    objetivos_ei = extrair_ei(pe)
    habilidades_ef = (
        extrair_ef(pe, ARQ_EF_INICIAIS, None, 'B', 'C', objetos) +
        extrair_ef(pe, ARQ_EF_FINAIS, 'B', 'C', 'E', objetos))
    habilidades_ef.sort(key=lambda h: (h['anos'][0], len(h['anos']), h['codigo']))
    habilidades_em = extrair_em(pe, comp_em)

    nomes_obj, registros_obj = objetos.resolver()
    for h in habilidades_ef:
        h['objeto'] = nomes_obj[h['objeto']]
        del h['anos']                         # o extrator decodifica do código

    mapa = {
        'sobre': ('Mapa de estrutura do complemento de Computação (anexo ao Parecer CNE/CEB 2/2022). '
                  'Gerado por pipeline/gerar_mapa_computacao.py a partir das planilhas de apoio da '
                  'Secretaria de Educação de Pernambuco, que não são redistribuídas (fontes/README.md, '
                  'DECISOES.md 13). Os textos e nomes são verificados caractere a caractere contra o '
                  'anexo oficial por pipeline/verificar_computacao.py. Não editar à mão.'),
        'planilhas_origem': [{'arquivo': a, 'sha256': s} for a, s in SHA256.items()],
        'competencias_gerais': [{'numero': n, 'texto': t} for n, t in comp_eb_a.items()],
        'competencias_especificas_em': [{'numero': n, 'texto': t} for n, t in comp_em.items()],
        'objetos_conhecimento': registros_obj,
        'objetivos_ei': objetivos_ei,
        'habilidades_ef': habilidades_ef,
        'habilidades_em': habilidades_em,
    }
    MAPA.write_text(json.dumps(mapa, ensure_ascii=False, indent=2) + '\n')
    print(f'mapa computacao-2022: EI {len(objetivos_ei)} + EF {len(habilidades_ef)} + EM {len(habilidades_em)} '
          f'= {len(objetivos_ei) + len(habilidades_ef) + len(habilidades_em)} aprendizagens · '
          f'{len(registros_obj)} objetos · {len(comp_eb_a) + len(comp_em)} competências → {MAPA.name}')


if __name__ == '__main__':
    principal()
