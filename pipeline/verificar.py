"""Verifica cada registro extraído contra o texto do PDF oficial.

Para cada habilidade: localiza o código no PDF (via pdftotext), compara o
texto da planilha com o texto do PDF (match estrito após normalização) e
grava a página PDF como `fonte.localizador_pdf`.

Saída: atualiza os JSONs em saida/ e gera saida/verificacao.json com o
resultado por registro (ok | divergente | nao_encontrado).
"""
import json
import re
import subprocess
import unicodedata
from pathlib import Path

AQUI = Path(__file__).parent
MEC = AQUI.parent / 'fontes'
SAIDA = AQUI / 'saida'
DATASET = AQUI.parent / 'dados' / 'bncc-2018'

# PDF canônico de verificação: BNCC completa homologada (601 p., três etapas,
# obtida em 09/jul/2026). Históricos no repo: BNCC-oficial.pdf (2017, EI+EF)
# e bncc_ensino_medio.pdf (rascunho pré-homologação do EM — nunca verificar
# contra ele; ver análise de fontes).
PDF_CANONICO = MEC / 'Base-Nacional-Comum-Curricular-BNCC.pdf'
PDF_POR_ETAPA = {'EF': PDF_CANONICO, 'EM': PDF_CANONICO}


def normalizar(t):
    """Normalização para comparação: espaços, hífens de quebra, aspas, unicode."""
    t = unicodedata.normalize('NFC', t)
    t = t.replace('­', '')                     # soft hyphen
    t = re.sub(r'-\s*\n\s*', '', t)                 # hifenização de quebra de linha
    t = t.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
    t = t.replace('ﬁ', 'fi').replace('ﬂ', 'fl')  # ligaduras tipograficas
    t = re.sub(r'[\s ]+', ' ', t)              # espaços (inclui nbsp)
    t = t.replace('–', '-').replace('—', '-')
    t = re.sub(r'\s*/\s*', '/', t)
    t = re.sub(r'(?<=[A-Za-zÀ-ú])- (?=[A-Za-zà-ú])', '-', t)  # 'fonema- grafema' -> 'fonema-grafema'  # 'leitura/ escuta' -> 'leitura/escuta' (quebra de linha na barra)
    return t.strip()


def paginas_pdf(pdf):
    """Texto do PDF por página (1-indexado)."""
    raw = subprocess.run(['pdftotext', '-enc', 'UTF-8', str(pdf), '-'],
                         capture_output=True, check=True).stdout.decode('utf-8')
    return raw.split('\f')


# Colunas laterais dos quadros que o pdftotext intercala no meio das células
# (observado nos quadros de LP do EM). Removidas só do lado do PDF.
INTERCALACOES = re.compile(
    r'(Competências específicas(?: \d+)*|Campos de atuação social|'
    r'Todos os campos de atuação social|campo jornalístico-midiático|'
    r'campo de atuação na vida pública|campo das práticas de estudo e pesquisa|'
    r'campo artístico(?:-literário)?|campo da vida pessoal)\s*', re.I)


def verificar(paginas, codigo, texto_planilha):
    alvo_original = normalizar(texto_planilha)
    marcador = f'({codigo})'
    primeira_divergencia = None
    for i, pag in enumerate(paginas, start=1):
        if marcador not in pag:
            continue
        alvo = alvo_original
        depois = normalizar(pag.split(marcador, 1)[1])
        # numeros soltos (1-2 digitos, listas '3, 7') vem da coluna de competencias
        # do quadro; removidos de AMBOS os lados para nao quebrar textos com numeros
        solto = re.compile(r'\b\d{1,2}(?:, ?\d{1,2})*\b ?')
        depois_limpo = re.sub(r'\s+', ' ', solto.sub('', INTERCALACOES.sub('', depois)))
        alvo_limpo = re.sub(r'\s+', ' ', solto.sub('', INTERCALACOES.sub('', alvo)))
        if depois.startswith(alvo) or depois_limpo.startswith(alvo_limpo):
            return {'status': 'ok', 'pagina_pdf': i}
        # fallback: hifenizacao/quebra ambigua (hifen de composto na quebra de
        # linha, palavra partida sem hifen) — compara sem espacos nem hifens,
        # mantendo todos os demais caracteres
        sem = lambda x: re.sub(r'[ \-]', '', x)
        if sem(depois_limpo).startswith(sem(alvo_limpo)):
            return {'status': 'ok', 'pagina_pdf': i, 'nota': 'quebras/hifenizacao ambiguas na comparacao'}
        depois = depois_limpo
        alvo = alvo_limpo
        # match parcial: acha o maior prefixo comum para diagnóstico
        comum = 0
        for a, b in zip(alvo, depois):
            if a != b:
                break
            comum += 1
        # o texto pode continuar na página seguinte
        if comum > len(alvo) * 0.5 and i < len(paginas):
            juntas = depois + ' ' + normalizar(paginas[i])
            if juntas.startswith(alvo):
                return {'status': 'ok', 'pagina_pdf': i, 'nota': 'texto atravessa páginas'}
        if primeira_divergencia is None:
            primeira_divergencia = {'status': 'divergente', 'pagina_pdf': i, 'prefixo_comum': comum,
                                    'trecho_planilha': alvo[comum:comum + 80], 'trecho_pdf': depois[comum:comum + 80]}
        # o mesmo codigo pode aparecer em outra pagina (ex.: exemplos do capitulo
        # de estrutura); segue procurando um match antes de reportar divergencia
    return primeira_divergencia or {'status': 'nao_encontrado'}


if __name__ == '__main__':
    paginas = paginas_pdf(PDF_CANONICO)
    print(f'{PDF_CANONICO.name}: {len(paginas)} páginas de texto extraídas')
    resultados = {}
    for arquivo, chave in (('ensino-fundamental.json', 'habilidades'),
                           ('ensino-medio.json', 'habilidades'),
                           ('educacao-infantil.json', 'objetivos')):
        dados = json.loads((DATASET / arquivo).read_text())
        for h in dados[chave]:
            r = verificar(paginas, h['codigo'], h['texto'])
            r['arquivo_pdf'] = PDF_CANONICO.name
            resultados[h['codigo']] = r
            if r['status'] == 'ok':
                h['fonte']['localizador_pdf'] = f"{PDF_CANONICO.name}, página PDF {r['pagina_pdf']}"
        (DATASET / arquivo).write_text(json.dumps(dados, ensure_ascii=False, indent=2))

    (DATASET / 'verificacao.json').write_text(json.dumps(resultados, ensure_ascii=False, indent=2))
    por_status = {}
    for r in resultados.values():
        por_status[r['status']] = por_status.get(r['status'], 0) + 1
    print('Resultado:', por_status)
    for cod, r in resultados.items():
        if r['status'] != 'ok':
            print(f'  {cod}: {r["status"]}', end='')
            if r['status'] == 'divergente':
                print(f" (pág {r['pagina_pdf']}, diverge após {r['prefixo_comum']} chars)\n    planilha: …{r['trecho_planilha']!r}\n    pdf:      …{r['trecho_pdf']!r}", end='')
            print()
