"""Verifica cada registro extraído contra o texto do PDF oficial.

Para cada aprendizagem: localiza o código no PDF (via pdftotext), compara o
texto da planilha com o texto do PDF (match estrito após normalização) e
grava a página PDF como `fonte.localizador_pdf`. Para cada competência
(10 gerais e 105 específicas): procura o texto inteiro no PDF e grava a
página da mesma forma.

Saída: atualiza os JSONs em dados/bncc-2018/ e gera
dados/bncc-2018/verificacao.json com o resultado por registro
(ok | divergente | requer_conferencia_visual | nao_encontrado), chaveado
pelo código da aprendizagem ou pelo id da competência.
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

# PDF canônico de verificação: BNCC completa homologada (600 p., três etapas,
# obtida em 09/jul/2026). Históricos no repo: BNCC-oficial.pdf (2017, EI+EF)
# e bncc_ensino_medio.pdf (rascunho pré-homologação do EM — nunca verificar
# contra ele; ver análise de fontes).
PDF_CANONICO = MEC / 'Base-Nacional-Comum-Curricular-BNCC.pdf'
PDF_POR_ETAPA = {'EF': PDF_CANONICO, 'EM': PDF_CANONICO}

# Capítulo "Estrutura" do PDF (páginas PDF 25 a 36, impressas 23 a 34): traz
# exemplos ilustrativos de quadros ("Como é possível observar no exemplo
# apresentado…") que repetem, palavra por palavra, objetivos da EI (PDF 28) e
# habilidades de Ciências do 1º ano (PDF 31). A página de verificação deve
# ser a do quadro normativo da etapa, não a do exemplo (decisão 14).
PAGINAS_CAPITULO_ESTRUTURA = range(25, 37)


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
    paginas = raw.split('\f')
    if paginas and not paginas[-1].strip():   # o pdftotext fecha a última página com \f
        paginas.pop()
    return paginas


# Colunas laterais dos quadros que o pdftotext intercala no meio das células
# (observado nos quadros de LP do EM). Removidas só do lado do PDF.
INTERCALACOES = re.compile(
    r'(Competências específicas(?: \d+)*|Campos de atuação social|'
    r'Todos os campos de atuação social|campo jornalístico-midiático|'
    r'campo de atuação na vida pública|campo das práticas de estudo e pesquisa|'
    r'campo artístico(?:-literário)?|campo da vida pessoal)\s*', re.I)


# Exceções com conferência visual registrada: casos em que a camada de texto
# do PDF diverge do dataset, mas a página IMPRESSA confere com o dado.
# Cada entrada exige a página conferida e a referência da conferência.
# (Auditoria independente de 10/08/2026 + conferência visual das páginas
# renderizadas em 10/08/2026; ver DECISOES.md.)
CONFERIDOS_VISUALMENTE = {
    'EF07MA33': {'pagina_pdf': 311, 'motivo': 'camada de texto do PDF perde o glifo π; página impressa confere com o dataset (decisão nº 4)'},
    'EF04GE08': {'pagina_pdf': 379, 'motivo': 'hífen repetido na quebra de linha ("matérias- -primas") na camada de texto; página impressa imprime "matérias-primas" e confere com o dataset'},
    'EF03LP11': {'pagina_pdf': 121, 'motivo': 'hífen de quebra de linha em "gráfico-visuais" na camada de texto; página impressa confere com o dataset'},
    'EF69LP48': {'pagina_pdf': 161, 'motivo': 'hífen de quebra de linha em "gráfico-espacial" na camada de texto; página impressa confere com o dataset'},
}

CODIGO_QUALQUER = re.compile(r'\((?:EI\d{2}[A-Z]{2}\d{2,3}|EF\d{2}[A-Z]{2,3}\d{2,3}|EM13[A-Z]{2,3}\d{2,3})\)')


def continuacao_no_pdf(resto):
    """O PDF continua a frase depois de onde o texto do dataset terminou?

    `resto` é o que sobra no PDF após o match do texto completo do dataset.
    Corta no próximo código (a região seguinte pertence a outra habilidade) e
    considera continuação se o resto começa em minúscula ou pontuação — i.e.,
    a mesma frase segue. Cabeçalhos/títulos (maiúsculas) e lixo de layout não
    contam como continuação.
    """
    m = CODIGO_QUALQUER.search(resto)
    resto = resto[:m.start()] if m else resto
    resto = resto.strip()
    if not resto:
        return None
    if resto[0].islower() or resto[0] in '.,;:)»…':
        return resto[:80]
    return None


def verificar(paginas, codigo, texto_planilha):
    alvo_original = normalizar(texto_planilha)
    marcador = f'({codigo})'
    primeira_divergencia = None
    for i, pag in enumerate(paginas, start=1):
        if marcador not in pag or i in PAGINAS_CAPITULO_ESTRUTURA:
            continue
        alvo = alvo_original
        depois = normalizar(pag.split(marcador, 1)[1])
        # numeros soltos (1-2 digitos, listas '3, 7') vem da coluna de competencias
        # do quadro; removidos de AMBOS os lados para nao quebrar textos com numeros
        solto = re.compile(r'\b\d{1,2}(?:, ?\d{1,2})*\b ?')
        depois_limpo = re.sub(r'\s+', ' ', solto.sub('', INTERCALACOES.sub('', depois)))
        alvo_limpo = re.sub(r'\s+', ' ', solto.sub('', INTERCALACOES.sub('', alvo)))
        if depois.startswith(alvo) or depois_limpo.startswith(alvo_limpo):
            resto = depois[len(alvo):] if depois.startswith(alvo) else depois_limpo[len(alvo_limpo):]
            cont = continuacao_no_pdf(resto)
            if cont is not None:
                return {'status': 'divergente', 'pagina_pdf': i,
                        'nota': 'o PDF continua depois do fim do texto do dataset (truncamento)',
                        'continuacao_pdf': cont}
            return {'status': 'ok', 'pagina_pdf': i}
        # fallback: hifenizacao/quebra ambigua (hifen de composto na quebra de
        # linha, palavra partida sem hifen) — compara sem espacos nem hifens,
        # mantendo todos os demais caracteres. Match por essa via NUNCA vira
        # "ok" sozinho: hifenizacao ambigua ja mascarou texto corrompido
        # (EF03LP20, auditoria de 10/08/2026); exige conferencia visual.
        sem = lambda x: re.sub(r'[ \-]', '', x)
        if sem(depois_limpo).startswith(sem(alvo_limpo)):
            return {'status': 'requer_conferencia_visual', 'pagina_pdf': i,
                    'nota': 'match apenas ignorando espacos e hifens; conferir a pagina impressa'}
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
                cont = continuacao_no_pdf(juntas[len(alvo):])
                if cont is not None:
                    return {'status': 'divergente', 'pagina_pdf': i,
                            'nota': 'o PDF continua depois do fim do texto do dataset (truncamento)',
                            'continuacao_pdf': cont}
                return {'status': 'ok', 'pagina_pdf': i, 'nota': 'texto atravessa páginas'}
        if primeira_divergencia is None:
            primeira_divergencia = {'status': 'divergente', 'pagina_pdf': i, 'prefixo_comum': comum,
                                    'trecho_planilha': alvo[comum:comum + 80], 'trecho_pdf': depois[comum:comum + 80]}
        # o mesmo codigo pode aparecer em outra pagina (ex.: exemplos do capitulo
        # de estrutura); segue procurando um match antes de reportar divergencia
    return primeira_divergencia or {'status': 'nao_encontrado'}


def verificar_competencia(paginas, texto):
    """Localiza o texto inteiro de uma competência no PDF.

    Competências não têm marcador de código; o texto normalizado é procurado
    em cada página e, como as colunas dos quadros podem partir o texto entre
    páginas, também no par página + seguinte. Fora do capítulo "Estrutura".
    """
    alvo = normalizar(texto)
    norm = [normalizar(p) for p in paginas]
    for i in range(1, len(paginas) + 1):
        if i in PAGINAS_CAPITULO_ESTRUTURA:
            continue
        if alvo in norm[i - 1]:
            return {'status': 'ok', 'pagina_pdf': i}
        if i < len(paginas) and alvo not in norm[i] and alvo in f'{norm[i - 1]} {norm[i]}':
            return {'status': 'ok', 'pagina_pdf': i, 'nota': 'texto atravessa páginas'}
    return {'status': 'nao_encontrado', 'trecho_planilha': alvo[:80]}


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
            exc = CONFERIDOS_VISUALMENTE.get(h['codigo'])
            if exc and r['status'] != 'ok' and r.get('pagina_pdf') == exc['pagina_pdf']:
                r = {'status': 'ok', 'pagina_pdf': exc['pagina_pdf'],
                     'nota': f"conferência visual registrada: {exc['motivo']}"}
            r['arquivo_pdf'] = PDF_CANONICO.name
            resultados[h['codigo']] = r
            if r['status'] == 'ok':
                h['fonte']['localizador_pdf'] = f"{PDF_CANONICO.name}, página PDF {r['pagina_pdf']}"
        (DATASET / arquivo).write_text(json.dumps(dados, ensure_ascii=False, indent=2))

    est = json.loads((DATASET / 'estrutura.json').read_text())
    for c in est['competencias_gerais'] + est['competencias_especificas']:
        r = verificar_competencia(paginas, c['texto'])
        r['arquivo_pdf'] = PDF_CANONICO.name
        resultados[c['id']] = r
        if r['status'] == 'ok':
            c['fonte']['localizador_pdf'] = f"{PDF_CANONICO.name}, página PDF {r['pagina_pdf']}"
    (DATASET / 'estrutura.json').write_text(json.dumps(est, ensure_ascii=False, indent=2))

    (DATASET / 'verificacao.json').write_text(json.dumps(resultados, ensure_ascii=False, indent=2))
    por_status = {}
    for r in resultados.values():
        por_status[r['status']] = por_status.get(r['status'], 0) + 1
    print('Resultado:', por_status)
    for cod, r in resultados.items():
        if r['status'] != 'ok':
            print(f'  {cod}: {r["status"]}', end='')
            if r['status'] == 'divergente' and 'continuacao_pdf' in r:
                print(f" (pág {r['pagina_pdf']}, truncamento)\n    pdf continua: …{r['continuacao_pdf']!r}", end='')
            elif r['status'] == 'divergente':
                print(f" (pág {r['pagina_pdf']}, diverge após {r['prefixo_comum']} chars)\n    planilha: …{r['trecho_planilha']!r}\n    pdf:      …{r['trecho_pdf']!r}", end='')
            print()
