"""Verifica o módulo de Computação contra o anexo oficial do Parecer
CNE/CEB 2/2022 (fonte canônica; as planilhas PE são só andaime).

Para cada uma das 141 aprendizagens: localiza o marcador "(CÓDIGO)" na
página registrada em fonte.localizador_pdf e exige que o texto extraído
apareça caractere a caractere logo após o marcador (normalização de
espaços/aspas/hifenização de quebra idêntica à do verificar.py). Nível
tolerante (ok_hifenizacao) aceita apenas diferenças de quebra de linha
dentro de palavras. Também confere que eixos, objetos de conhecimento e
competências existem no texto do anexo.

Saída: dados/computacao-2022/verificacao.json (status por registro).
"""
import json
import re
import sys
from pathlib import Path

from anexo_computacao import ANEXO, paginas_anexo
from extrair_computacao import CANONIZACOES
from verificar import normalizar

AQUI = Path(__file__).parent
DATASET = AQUI.parent / 'dados' / 'computacao-2022'

IMPRESSOS = {v: k for k, v in CANONIZACOES.items()}   # EF05CO11 → EF05CO011


def compacta(t):
    return re.sub(r'[\s\-–—·]+', '', normalizar(t))


def principal():
    dados = json.loads((DATASET / 'computacao.json').read_text())
    paginas = paginas_anexo()
    pag_norm = [normalizar(p) for p in paginas]
    pag_comp = [compacta(p) for p in paginas]
    doc_norm = normalizar(' '.join(paginas))
    doc_comp = compacta(' '.join(paginas))

    aprendizagens = dados['objetivos_ei'] + dados['habilidades_ef'] + dados['habilidades_em']
    resultado = {}
    contagem = {'ok': 0, 'ok_hifenizacao': 0, 'divergente': 0}
    for r in aprendizagens:
        pagina = int(re.search(r'(\d+)', r['fonte']['localizador_pdf']).group(1))
        impresso = IMPRESSOS.get(r['codigo'], r['codigo'])
        # a célula pode continuar na página seguinte
        janela_norm = ' '.join(pag_norm[pagina - 1:pagina + 1])
        janela_comp = ''.join(pag_comp[pagina - 1:pagina + 1])
        alvo = normalizar(f'({impresso}) {r["texto"]}')
        if alvo in janela_norm:
            status = 'ok'
        elif compacta(f'({impresso}){r["texto"]}') in janela_comp:
            status = 'ok_hifenizacao'
        else:
            status = 'divergente'
            i = janela_norm.find(f'({impresso})')
            trecho = janela_norm[i:i + len(alvo) + 40] if i >= 0 else '(marcador ausente)'
            print(f'DIVERGENTE {r["codigo"]}:\n  dataset: {alvo[:160]}\n  anexo:   {trecho[:160]}')
        contagem[status] += 1
        resultado[r['codigo']] = {'status': status, 'pagina_pdf': pagina, 'arquivo_pdf': ANEXO.name}

    # estruturas: nomes/textos precisam existir no anexo
    faltas = []
    for grupo, itens, campo in [('eixo', dados['eixos'], 'nome'),
                                ('objeto', dados['objetos_conhecimento'], 'nome'),
                                ('competência', dados['competencias'], 'texto')]:
        for item in itens:
            alvo = normalizar(item[campo])
            if alvo.lower() in doc_norm.lower():
                continue
            if compacta(item[campo]).lower() in doc_comp.lower():
                continue
            faltas.append((grupo, item['id'], item[campo][:70]))
    for g, i, t in faltas:
        print(f'ESTRUTURA AUSENTE NO ANEXO · {g} {i}: {t!r}')

    (DATASET / 'verificacao.json').write_text(json.dumps(resultado, ensure_ascii=False, indent=2))
    total = len(aprendizagens)
    print(f'verificação computacao-2022: {contagem["ok"]}/{total} ok · '
          f'{contagem["ok_hifenizacao"]} ok_hifenizacao · {contagem["divergente"]} divergentes · '
          f'estruturas ausentes: {len(faltas)}')
    sys.exit(1 if contagem['divergente'] or faltas else 0)


if __name__ == '__main__':
    principal()
