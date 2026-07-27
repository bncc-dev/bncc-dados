"""Validação do dataset completo + completude vs PDF + diff de base de regressão +
14 consultas do caso âncora + DECISOES.md consolidado.

Saídas: saida/relatorio-validacao.md e saida/DECISOES.md
"""
import csv
import json
import os
import re
import unicodedata
from collections import Counter
from pathlib import Path

from codigos import decodificar
from verificar import PDF_CANONICO, normalizar, paginas_pdf

AQUI = Path(__file__).parent
SAIDA = AQUI / 'saida'
DATASET = AQUI.parent / 'dados' / 'bncc-2018'
SAIDA.mkdir(exist_ok=True)
# Base de linhagem independente para diff de regressão (opcional).
# Aponte BNCC_BASE_REGRESSAO para um CSV com colunas `code` e `description`;
# sem a variável, o diff é pulado e a validação segue normalmente.
BASE_REGRESSAO = os.environ.get('BNCC_BASE_REGRESSAO')
PEI = Path(BASE_REGRESSAO) if BASE_REGRESSAO else None

ef = json.loads((DATASET / 'ensino-fundamental.json').read_text())
em = json.loads((DATASET / 'ensino-medio.json').read_text())
ei = json.loads((DATASET / 'educacao-infantil.json').read_text())
est = json.loads((DATASET / 'estrutura.json').read_text())
verif = json.loads((DATASET / 'verificacao.json').read_text())
dec_extracao = json.loads((SAIDA / 'decisoes-extracao.json').read_text())

checks = []
check = lambda nome, ok, det='': checks.append((nome, bool(ok), det))

# --------------------------------------------------------------- 1. gramática
todos = ([h['codigo'] for h in ef['habilidades']] + [h['codigo'] for h in em['habilidades']] +
         [o['codigo'] for o in ei['objetivos']])
erros_gram = []
for c in todos:
    try:
        decodificar(c)
    except ValueError as e:
        erros_gram.append(str(e))
check('1. Gramática: todos os códigos decodificam', not erros_gram, '; '.join(erros_gram[:3]))

# --------------------------------------------------------------- 2. contagens
GABARITO_EF = {'ef-comp-lp': 391, 'ef-comp-ar': 61, 'ef-comp-ef': 69, 'ef-comp-li': 88,
               'ef-comp-ma': 247, 'ef-comp-ci': 111, 'ef-comp-ge': 123, 'ef-comp-hi': 151, 'ef-comp-er': 63}
por_comp = Counter(h['componente'] for h in ef['habilidades'])
check('2. EF: 1.304 habilidades', len(ef['habilidades']) == 1304, f"{len(ef['habilidades'])}")
check('2. EF: contagem por componente', dict(por_comp) == GABARITO_EF)
por_area = Counter(h['area'] for h in em['habilidades'])
check('2. EM: 183 = LGG 28 + LP 54 + MAT 43 + CNT 26 + CHS 32',
      dict(por_area) == {'em-area-lgg': 82, 'em-area-mat': 43, 'em-area-cnt': 26, 'em-area-chs': 32}
      and sum(1 for h in em['habilidades'] if h['componente'] == 'em-comp-lp') == 54)
por_campo = Counter(o['campo_experiencias'] for o in ei['objetivos'])
check('2. EI: 93 objetivos (EO 20, CG 15, TS 9, EF 27, ET 22)',
      dict(por_campo) == {'ei-campo-eo': 20, 'ei-campo-cg': 15, 'ei-campo-ts': 9,
                          'ei-campo-ef': 27, 'ei-campo-et': 22}, f'{dict(por_campo)}')
check('2. Competências: 10 gerais + 105 específicas (84 EF + 21 EM)',
      len(est['competencias_gerais']) == 10 and len(est['competencias_especificas']) == 105)

# ------------------------------------------------- 3. integridade referencial
ctx_ef = {c['id'] for c in ef['contextos_organizacao']}
ctx_em = {c['id'] for c in em['contextos_organizacao']}
ces = {c['id'] for c in est['competencias_especificas']}
comps_est = {c['id'] for c in est['componentes_curriculares']}
ok_int = all(h['componente'] in comps_est for h in ef['habilidades'])
for h in ef['habilidades']:
    org = h['organizacao']
    refs = ([org.get('unidade_tematica')] + org.get('campos_atuacao', []) +
            [org.get('pratica_linguagem'), org.get('eixo')] + h['objetos_conhecimento'])
    ok_int &= all(r in ctx_ef for r in refs if r)
ok_int &= all(all(c in ces for c in h['competencias_especificas']) for h in em['habilidades'])
ok_int &= all(all(c in ctx_em for c in (h['campos_atuacao_social'] or [])) for h in em['habilidades'])
check('3. Integridade referencial (organização, objetos, competências)', ok_int)
tipos_org = Counter(h['organizacao']['tipo'] for h in ef['habilidades'])
check('3. Organização por layout: LP=campo_pratica, LI=eixo, demais=unidade_tematica',
      all((h['componente'] == 'ef-comp-lp') == (h['organizacao']['tipo'] == 'campo_pratica') and
          (h['componente'] == 'ef-comp-li') == (h['organizacao']['tipo'] == 'eixo')
          for h in ef['habilidades']), f'{dict(tipos_org)}')

# ------------------------------------------------------- 4. regras estruturais
lgg = [h for h in em['habilidades'] if h['area'] == 'em-area-lgg' and not h['componente']]
check('4. EM área: competência coerente com o dígito do código',
      all(h['competencias_especificas'] == [f"{h['area']}-ce-0{h['codigo'][7]}"]
          for h in em['habilidades'] if not h['componente']))
check('4. EM LP: 1..n competências da planilha',
      all(1 <= len(h['competencias_especificas']) <= 7 for h in em['habilidades'] if h['componente']))
check('4. Agrupamento: área/componente atribuídos = decodificação do código',
      all(f"ef-comp-{decodificar(h['codigo'])['componente'].lower()}" == h['componente']
          for h in ef['habilidades']) and
      all(f"em-area-{decodificar(h['codigo'])['area'].lower()}" == h['area'] for h in em['habilidades']))
check('4. Competência de componente só em área multi-componente',
      all(c.get('componente', '').split('-')[-1] not in ('ma', 'ci', 'er')
          for c in est['competencias_especificas'] if c['tipo'] == 'especifica_de_componente'))

# ------------------------------------------------------------- 5. duplicatas
check('5. Sem duplicatas', len(todos) == len(set(todos)))

# ---------------------------------------------------------- 6. alinhamentos EI
incompletos = [a['id'] for a in ei['alinhamentos'] if len(a['objetivos']) != 3]
check('6. Alinhamentos EI: 32; incompletos só onde o quadro oficial tem célula vazia',
      len(ei['alinhamentos']) == 32 and set(incompletos) == {'ei-align-eo-07', 'ei-align-et-07', 'ei-align-et-08'},
      f'incompletos: {incompletos}')

# ------------------------------------------------------------- 7. verificação
DIVERGENCIAS_CONHECIDAS = {
    'EM13LP35': 'planilha omite "de" ("a quantidade [de] texto e imagem") · PDF prevalece',
    'EF03MA05': 'planilha omite ", inclusive os convencionais," · PDF prevalece',
    'EF02MA06': 'camada de texto do PDF perde glifos na pág. 285 (dígitos e trecho final) · planilha prevalece, conferência visual feita',
    'EF07MA33': 'glifo π ausente da camada de texto do PDF · planilha prevalece',
}
vf = Counter(v['status'] for v in verif.values())
ruins = {k for k, v in verif.items() if v['status'] != 'ok'}
check('7. Verificação PDF: 1.576/1.580 ok; 4 divergências conhecidas e documentadas',
      ruins == set(DIVERGENCIAS_CONHECIDAS), f'{dict(vf)}; inesperadas: {sorted(ruins - set(DIVERGENCIAS_CONHECIDAS))}')

# ------------------------------------------------------- 8. vigência coerente
check('8. Vigência coerente', all(h['vigencia']['status'] == 'vigente'
                                  for h in ef['habilidades'] + em['habilidades'] + ei['objetivos']))

# ------------------------------------------------ 8b. marcos legais e perfis
ml = json.loads((DATASET / 'marcos-legais.json').read_text())
pf = json.loads((DATASET / 'perfis.json').read_text())
entidades_conhecidas = ({d['id'] for d in est['documento_curricular']} |
                        {e['id'] for e in est['etapas']} | {m['id'] for m in est['modalidades']} |
                        {a['id'] for a in est['areas_conhecimento']} | comps_est | ces)
rel_quebradas = [(m['id'], r['entidade']) for m in ml['marcos_legais']
                 for r in m['relaciona'] if r['entidade'] not in entidades_conhecidas]
check('8b. Marcos legais: 20 registros e relações apontando para entidades do dataset',
      len(ml['marcos_legais']) == 20 and not rel_quebradas, f'quebradas: {rel_quebradas[:5]}')
check('8b. Marcos legais: IDs únicos, URL oficial https no gov.br',
      len({m['id'] for m in ml['marcos_legais']}) == len(ml['marcos_legais'])
      and all(m['url_oficial'].startswith('https://') and '.gov.br/' in m['url_oficial']
              for m in ml['marcos_legais']))
PERFIS_MINIMOS = {'perfil-professor', 'perfil-aluno', 'perfil-gestor',
                  'perfil-responsavel', 'perfil-coordenador'}
check('8b. Perfis: vocabulário mínimo do plano presente',
      PERFIS_MINIMOS <= {p['id'] for p in pf['perfis']},
      f"faltam: {sorted(PERFIS_MINIMOS - {p['id'] for p in pf['perfis']})}")

# ------------------------------------------- 8c. Computação (computacao-2022)
CO_DIR = DATASET.parent / 'computacao-2022'
co = json.loads((CO_DIR / 'computacao.json').read_text())
verif_co = json.loads((CO_DIR / 'verificacao.json').read_text())
co_todas = co['objetivos_ei'] + co['habilidades_ef'] + co['habilidades_em']
cods_co = [h['codigo'] for h in co_todas]

check('8c. Documento curricular computacao-2022 na estrutura (complemento de bncc-2018)',
      any(d['id'] == 'computacao-2022' and d['tipo'] == 'complemento'
          and d['derivado_de'] == 'bncc-2018' for d in est['documento_curricular']))
check('8c. Computação: 141 aprendizagens (EI03 11 + EF 104 + EM 26)',
      (len(co['objetivos_ei']), len(co['habilidades_ef']), len(co['habilidades_em'])) == (11, 104, 26),
      f"{len(co['objetivos_ei'])}+{len(co['habilidades_ef'])}+{len(co['habilidades_em'])}")
pref_co = Counter(c[:4] for c in cods_co)
check('8c. Computação: contagem por prefixo de código',
      dict(pref_co) == {'EI03': 11, 'EF01': 7, 'EF02': 6, 'EF03': 9, 'EF04': 8, 'EF05': 11,
                        'EF06': 10, 'EF07': 11, 'EF08': 11, 'EF09': 10, 'EF15': 9, 'EF69': 12,
                        'EM13': 26}, f'{dict(pref_co)}')
erros_co = []
for c in cods_co:
    try:
        decodificar(c)
    except ValueError as e:
        erros_co.append(str(e))
check('8c. Computação: gramática — todos os códigos decodificam', not erros_co, '; '.join(erros_co[:3]))
grupos_co = {}
for c in cods_co:
    grupos_co.setdefault(c[:6], []).append(int(c[6:]))
check('8c. Computação: sem duplicatas e sequências contínuas (sem lacunas, ao contrário da BNCC 2018)',
      len(set(cods_co)) == len(cods_co) and
      all(sorted(ns) == list(range(1, len(ns) + 1)) for ns in grupos_co.values()))
eixos_co = {e['id'] for e in co['eixos']}
objs_co = {o['id'] for o in co['objetos_conhecimento']}
comps_co = {c['id'] for c in co['competencias']}
ok_co = all(o['eixo'] in eixos_co and o['grupo_etario'] == 'ei-grupo-03' for o in co['objetivos_ei'])
ok_co &= all(h['eixo'] in eixos_co and all(x in objs_co for x in h['objetos_conhecimento'])
             for h in co['habilidades_ef'])
ok_co &= all(h['competencia'] in comps_co for h in co['habilidades_em'])
ok_co &= all(o['pai'] in objs_co for o in co['objetos_conhecimento'] if o['pai'])
ok_co &= all(h['anos'] == decodificar(h['codigo'])['anos'] for h in co['habilidades_ef'])
check('8c. Computação: integridade referencial (eixo, objeto/pai, competência, anos=código)', ok_co)
vc = Counter(v['status'] for v in verif_co.values())
check('8c. Computação: verificação contra o anexo oficial — 141/141 idênticos',
      dict(vc) == {'ok': 141} and set(verif_co) == set(cods_co), f'{dict(vc)}')
from anexo_computacao import paginas_anexo
from extrair_computacao import CANONIZACOES
sweep_co = set()
for pag in paginas_anexo():
    for cod in re.findall(r'\((E[IFM]\d{2}CO\d{2,3})\)', pag):
        sweep_co.add(CANONIZACOES.get(cod, cod))
check('8c. Completude: varredura de códigos no anexo == dataset (141)',
      sweep_co == set(cods_co),
      f'faltam: {sorted(sweep_co - set(cods_co))[:5]} sobram: {sorted(set(cods_co) - sweep_co)[:5]}')

# ----------------------------------------------- 9. completude: varredura PDF
paginas = paginas_pdf(PDF_CANONICO)
texto_pdf = ' '.join(paginas)
sweep = set(re.findall(r'\((E[IFM]\d{2}[A-Z]{2,3}\d{2,3})\)', texto_pdf))
sweep = {c for c in sweep if not c.startswith('EM13') or re.fullmatch(r'EM13([A-Z]{3}\d{3}|LP\d{2})', c)}
extraidos = set(todos)
faltam = sorted(sweep - extraidos)
sobram = sorted(extraidos - sweep)
check('9. Completude: nenhum código do PDF fora do dataset', not faltam, f'faltam: {faltam[:10]}')
check('9. Completude: nenhum código do dataset fora do PDF', not sobram, f'sobram: {sobram[:10]}')

# ------------------------------------------------- diff base de regressão (tudo)
pei = {}
if PEI and PEI.exists():
    with open(PEI, encoding='utf-8') as fh:
        for row in csv.DictReader(fh):
            pei[row['code'].strip()] = re.sub(r'\s+', ' ', row['description']).strip()
nossos = {h['codigo']: h['texto'] for h in ef['habilidades'] + em['habilidades']}
if pei:
    pei_faltando = sorted(set(nossos) - set(pei))
    pei_extra = sorted(set(pei) - set(nossos))
    pei_texto_dif = [c for c in nossos if c in pei and normalizar(nossos[c]) != normalizar(pei[c])]
else:
    pei_faltando = pei_extra = pei_texto_dif = []
    print('aviso: base de regressão indisponível (BNCC_BASE_REGRESSAO); diff pulado')

# --------------------------------------------- consultas do caso âncora (14)
H_EF = ef['habilidades']
H_EM = em['habilidades']
ctx_nome = {c['id']: c['nome'] for c in ef['contextos_organizacao'] + em['contextos_organizacao']}
consultas = []

comps_6ano = sorted({h['componente'] for h in H_EF if 6 in h['anos']})
consultas.append(('C1: componentes disponíveis para aluno do 6º ano', f'{len(comps_6ano)}: {", ".join(c.split("-")[-1].upper() for c in comps_6ano)}'))
lp36 = [h for h in H_EF if h['componente'] == 'ef-comp-lp' and set(h['anos']) & {3, 4, 5, 6}]
consultas.append(('C2: habilidades de LP dos anos 3º–6º (flexibilização PEI)', f'{len(lp36)} habilidades'))
por_pratica = Counter(ctx_nome[h['organizacao']['pratica_linguagem']] for h in lp36)
consultas.append(('C3: agrupadas por prática de linguagem', ' · '.join(f'{k}: {v}' for k, v in por_pratica.most_common())))
h67 = next(h for h in H_EF if h['codigo'] == 'EF67LP08')
consultas.append(('C4: registro completo de EF67LP08',
                  f"anos {h67['anos']}, campos {[ctx_nome[c] for c in h67['organizacao']['campos_atuacao']]}, "
                  f"prática {ctx_nome[h67['organizacao']['pratica_linguagem']]}, {len(h67['objetos_conhecimento'])} objetos, "
                  f"fonte: {h67['fonte'].get('localizador_pdf', h67['fonte']['localizador'])}"))
consultas.append(('C5: decodificar código colado ("em13lgg103")', json.dumps(decodificar('em13lgg103'), ensure_ascii=False)))
fracoes = [h['codigo'] for h in H_EF if 'fraç' in h['texto'].lower() and h['componente'] == 'ef-comp-ma']
consultas.append(('C6: busca textual "frações" em Matemática', f'{len(fracoes)}: {", ".join(fracoes[:8])}…'))
alvo = next(h for h in H_EF if h['codigo'] == 'EF06MA07')
rel = [h['codigo'] for h in H_EF if set(h['objetos_conhecimento']) & set(alvo['objetos_conhecimento'])
       and max(h['anos']) < min(alvo['anos'])]
consultas.append(('C7: progressão de EF06MA07 via objetos em anos anteriores',
                  ', '.join(rel) or 'nenhuma por igualdade de slug · dedução exige curadoria (decisão nº 2 do schema)'))
al = next(a for a in ei['alinhamentos'] if a['id'] == 'ei-align-ts-01')
consultas.append(('C8: progressão EI entre faixas (campo TS)', ' → '.join(al['objetivos'])))
em_ex = next(h for h in H_EM if h['codigo'] == 'EM13LGG103')
lp_ex = next(h for h in H_EM if h['codigo'] == 'EM13LP02')
consultas.append(('C9: EM com competência (área e LP)',
                  f"LGG103 → {em_ex['competencias_especificas']}; LP02 → {lp_ex['competencias_especificas']}"))
eja = est['modalidades'][0]['segmentos']
consultas.append(('C10: EJA segmento → recorte', ' · '.join(f"{s['id']}→{s['corresponde_a']}" for s in eja)))
ma4 = [h['codigo'] for h in H_EF if h['componente'] == 'ef-comp-ma' and h['anos'] == [4]]
consultas.append(('C11: cobertura · habilidades de MA do 4º ano', f'{len(ma4)} habilidades'))
com_fonte = sum(1 for h in H_EF + H_EM if 'localizador_pdf' in h['fonte'])
consultas.append(('C12: fonte oficial citável', f'{com_fonte}/{len(H_EF) + len(H_EM)} com página do PDF homologado'))
vigentes = sum(1 for h in H_EF + H_EM if h['vigencia']['status'] == 'vigente')
consultas.append(('C13: filtro de vigência', f'{vigentes} vigentes; filtro operacional (nenhuma revogada no dado atual)'))
consultas.append(('C14: sugerir adaptação da habilidade', 'fora do dado de referência (inteligência do produto) · por desenho'))

# ------------------------------------------------------------- DECISOES.md
decisoes_md = ['# DECISOES.md · decisões de interpretação (rascunho do protótipo)', '',
               'Formato: contexto → decisão → fonte. Migram para o repositório de dados com a v1.0.', '']
entradas = [
    ('Rotação de linhas entre abas na planilha oficial do EM',
     'EM13CNT310 (aba Linguagens), EM13CHS606 (aba CNT) e EM13LGG105 (aba CHS) estão em abas trocadas. '
     'Realocados pela decodificação do código. A área/componente canônico é sempre o do código, nunca a aba.',
     'BNCC_Ensino_Medio.xlsx (23/06/2023) × decodificador'),
    ('EM13LP35 · divergência entre fontes oficiais',
     'Planilha omite "de" em "a quantidade de texto e imagem". Prevalece o PDF homologado (pág. PDF 520).',
     'planilha × Base-Nacional-Comum-Curricular-BNCC.pdf'),
    ('EF03MA05 · divergência entre fontes oficiais',
     'Planilha omite ", inclusive os convencionais,". Prevalece o PDF homologado (pág. PDF 289).',
     'planilha × PDF homologado'),
    ('EF02MA06 e EF07MA33 · limitações da camada de texto do PDF',
     'pdftotext perde glifos (dígitos/π) nas págs. 285 e 311. Prevalece a planilha; conferência visual registrada.',
     'PDF homologado (extração de texto)'),
    ('Alinhamento horizontal da EI reconstruído por posição sequencial',
     'Objetivos com o mesmo NN entre grupos etários são pareados (BNCC p. 26: "mesmo aspecto"). '
     'Células vazias do quadro oficial geram alinhamentos com 2 objetivos (eo-07, et-07, et-08). '
     'Heurística pendente de revisão pedagógica.',
     'PDF homologado, seção EI'),
    ('Objetos de conhecimento: dedup por slug não cria progressão entre anos',
     'Nomes de objetos variam entre anos; a travessia de progressão exige curadoria de equivalência (v1.x).',
     'consulta C7 do caso âncora'),
    ('Competências gerais idênticas nas planilhas de EF e EM',
     'Extraídas uma vez (cg-01..cg-10)' if 'Competências gerais divergem' not in ' '.join(dec_extracao)
     else 'DIVERGEM entre planilhas · decidir fonte', 'planilhas EF × EM'),
    ('Ano/Faixa da planilha vs código',
     'Quando divergem, prevalece o código (nenhum caso encontrado na extração atual).', 'extração'),
    ('EF05CO011 · código com 3 dígitos no anexo oficial de Computação',
     'O anexo ao Parecer CNE/CEB 2/2022 imprime "(EF05CO011)" — único código de Computação com sequência de 3 dígitos, '
     'vindo após o EF05CO10. Canonizado como EF05CO11 (gramática dos demais 140 códigos); a forma impressa fica '
     'registrada no localizador da fonte do registro.',
     'anexo ao Parecer CNE/CEB 2/2022, quadro do 5º ano'),
    ('Computação · estrutura via planilhas de Pernambuco, texto pelo anexo',
     'As células dos quadros do anexo são mescladas em múltiplos níveis e a camada de texto do PDF as embaralha. '
     'A estrutura (eixo, objeto, competência) vem das planilhas da Sec. de Educação de PE; variantes de nome geradas '
     'por quebra de linha nas células (ex.: "responsabilidad e") são unificadas pela forma mais frequente. '
     'TODOS os 141 textos e 78 itens de estrutura foram verificados caractere a caractere contra o anexo oficial, que sempre prevalece. '
     'Descritores de agrupamento, explicações e exemplos do anexo ficam para iteração futura do módulo.',
     'planilhas Sec. Educação PE × anexo ao Parecer CNE/CEB 2/2022'),
]
for titulo, corpo, fonte in entradas:
    decisoes_md += [f'## {titulo}', '', corpo, '', f'*Fonte: {fonte}*', '']
(SAIDA / 'DECISOES.md').write_text('\n'.join(decisoes_md))

# --------------------------------------------------------------- relatório
linhas = ['# Relatório de validação · dataset completo (bncc.dev, protótipo)', '',
          f'EF {len(H_EF)} + EM {len(H_EM)} + EI {len(ei["objetivos"])} = **{len(todos)} aprendizagens** · '
          f'{len(est["competencias_gerais"])} competências gerais · {len(est["competencias_especificas"])} específicas · '
          f'{len(ef["contextos_organizacao"]) + len(em["contextos_organizacao"])} contextos de organização · '
          f'{len(ml["marcos_legais"])} marcos legais · {len(pf["perfis"])} perfis · '
          f'**{len(co_todas)} aprendizagens de Computação** (computacao-2022)', '',
          '## Contratos', '']
linhas += [f"- {'✅' if ok else '❌'} {nome}" + (f' · {det}' if det and not ok else '') for nome, ok, det in checks]
linhas += ['', '## Verificação contra o PDF homologado', '',
           f'- `{dict(vf)}` · {vf["ok"]}/{len(verif)} com página registrada em `fonte.localizador_pdf`',
           '- Fila de divergências conhecidas (4):'] + \
          [f'  - **{k}**: {v}' for k, v in DIVERGENCIAS_CONHECIDAS.items()]
linhas += ['', '## Completude (varredura de códigos no PDF inteiro)', '',
           f'- Códigos no PDF: {len(sweep)} · extraídos: {len(extraidos)} · faltando: {faltam or "nenhum"} · sobrando: {sobram or "nenhum"}',
           '', '## Diff base de regressão (EF + EM completos)', '',
           f'- Faltam na base de regressão: {pei_faltando or "nenhum"}',
           f'- Extras na base de regressão: {pei_extra or "nenhum"}',
           f'- Textos divergentes: {len(pei_texto_dif)}' + (f' · {pei_texto_dif[:6]}' if pei_texto_dif else ''),
           '', '## As 14 consultas do caso âncora', '']
linhas += [f'- **{n}** → {r}' for n, r in consultas]
linhas += ['', '## Decisões de interpretação', '', f'Consolidadas em `saida/DECISOES.md` '
           f'({len(entradas)} entradas) + `decisoes-extracao.json` ({len(dec_extracao)} da extração).']
(SAIDA / 'relatorio-validacao.md').write_text('\n'.join(linhas) + '\n')

falhas = [n for n, ok, _ in checks if not ok]
print(f'Contratos: {len(checks) - len(falhas)}/{len(checks)} ok' + (f' | FALHAS: {falhas}' if falhas else ''))
print(f'Completude: sweep={len(sweep)} extraidos={len(extraidos)} faltam={faltam[:5]} sobram={sobram[:5]}')
print(f'regressao: faltam={pei_faltando} extras={pei_extra} texto_dif={pei_texto_dif[:5]}')
for n, r in consultas:
    print(f'  {n[:55]:55} → {str(r)[:90]}')

import sys
sys.exit(1 if falhas else 0)
