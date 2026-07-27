"""Gera os derivados do dataset: derivados/bncc.sqlite e derivados/csv/*.csv.

Determinístico: mesma entrada → mesmos bytes nos CSVs e mesmo dump lógico
no SQLite. Nada aqui é editado à mão (ver derivados/README.md).
"""
import csv
import hashlib
import json
import sqlite3
from pathlib import Path

AQUI = Path(__file__).parent
DATASET = AQUI.parent / 'dados' / 'bncc-2018'
FONTES = AQUI.parent / 'fontes'
DERIVADOS = AQUI.parent / 'derivados'
CSV_DIR = DERIVADOS / 'csv'

ef = json.loads((DATASET / 'ensino-fundamental.json').read_text())
em = json.loads((DATASET / 'ensino-medio.json').read_text())
ei = json.loads((DATASET / 'educacao-infantil.json').read_text())
est = json.loads((DATASET / 'estrutura.json').read_text())
ml = json.loads((DATASET / 'marcos-legais.json').read_text())
pf = json.loads((DATASET / 'perfis.json').read_text())
co = json.loads((DATASET.parent / 'computacao-2022' / 'computacao.json').read_text())

DATA_VERSION = ef['habilidades'][0]['vigencia']['desde']
SEP = ' | '


def fonte_cols(f):
    f = f or {}
    return (f.get('documento'), f.get('arquivo'), f.get('proveniencia'),
            f.get('localizador'), f.get('localizador_pdf'))


FONTE_DDL = ('fonte_documento TEXT, fonte_arquivo TEXT, fonte_proveniencia TEXT, '
             'fonte_localizador TEXT, fonte_localizador_pdf TEXT')
VIG_DDL = 'vigencia_status TEXT NOT NULL, vigencia_desde TEXT NOT NULL, vigencia_ate TEXT'


def gerar_sqlite(caminho):
    caminho.unlink(missing_ok=True)
    db = sqlite3.connect(caminho)
    c = db.cursor()
    c.executescript(f'''
    CREATE TABLE meta (chave TEXT PRIMARY KEY, valor TEXT NOT NULL);
    CREATE TABLE documento_curricular (id TEXT PRIMARY KEY, nome TEXT, tipo TEXT, esfera TEXT, derivado_de TEXT);
    CREATE TABLE etapa (id TEXT PRIMARY KEY, nome TEXT);
    CREATE TABLE modalidade (id TEXT PRIMARY KEY, nome TEXT, transversal_a TEXT);
    CREATE TABLE modalidade_segmento (id TEXT PRIMARY KEY, modalidade TEXT REFERENCES modalidade(id), corresponde_a TEXT);
    CREATE TABLE area_conhecimento (id TEXT PRIMARY KEY, etapa TEXT REFERENCES etapa(id), nome TEXT, documento TEXT);
    CREATE TABLE componente_curricular (id TEXT PRIMARY KEY, etapa TEXT, nome TEXT, sigla_codigo TEXT,
        area TEXT REFERENCES area_conhecimento(id), tem_aprendizagens_proprias INTEGER,
        presenca_anos TEXT, destaque_legal TEXT, nota TEXT);
    CREATE TABLE recorte_temporal (id TEXT PRIMARY KEY, etapa TEXT, tipo TEXT, nome TEXT, faixa TEXT, numero INTEGER, segmento TEXT, nota TEXT);
    CREATE TABLE campo_experiencias (id TEXT PRIMARY KEY, nome TEXT, documento TEXT);
    CREATE TABLE direito_aprendizagem (id TEXT PRIMARY KEY, nome TEXT, documento TEXT);
    CREATE TABLE competencia_geral (id TEXT PRIMARY KEY, documento TEXT, numero INTEGER, texto TEXT, {FONTE_DDL});
    CREATE TABLE competencia_especifica (id TEXT PRIMARY KEY, documento TEXT, tipo TEXT, area TEXT, componente TEXT,
        numero INTEGER, texto TEXT, {FONTE_DDL});
    CREATE TABLE contexto_organizacao (id TEXT PRIMARY KEY, etapa TEXT, tipo TEXT, nome TEXT, componente TEXT, {FONTE_DDL});
    CREATE TABLE objetivo_ei (codigo TEXT PRIMARY KEY, documento TEXT, texto TEXT,
        campo_experiencias TEXT REFERENCES campo_experiencias(id), grupo_etario TEXT, alinhamento TEXT, {VIG_DDL}, {FONTE_DDL});
    CREATE TABLE habilidade_ef (codigo TEXT PRIMARY KEY, documento TEXT, texto TEXT,
        componente TEXT REFERENCES componente_curricular(id), organizacao_tipo TEXT,
        unidade_tematica TEXT, pratica_linguagem TEXT, eixo TEXT, {VIG_DDL}, {FONTE_DDL});
    CREATE TABLE habilidade_em (codigo TEXT PRIMARY KEY, documento TEXT, texto TEXT,
        area TEXT REFERENCES area_conhecimento(id), componente TEXT, {VIG_DDL}, {FONTE_DDL});
    CREATE TABLE alinhamento (id TEXT PRIMARY KEY, campo_experiencias TEXT, nota TEXT);
    CREATE TABLE alinhamento_objetivo (alinhamento TEXT REFERENCES alinhamento(id),
        objetivo TEXT REFERENCES objetivo_ei(codigo), PRIMARY KEY (alinhamento, objetivo));
    CREATE TABLE habilidade_ef_ano (codigo TEXT REFERENCES habilidade_ef(codigo), ano INTEGER, PRIMARY KEY (codigo, ano));
    CREATE TABLE habilidade_ef_objeto (codigo TEXT REFERENCES habilidade_ef(codigo),
        objeto TEXT REFERENCES contexto_organizacao(id), PRIMARY KEY (codigo, objeto));
    CREATE TABLE habilidade_ef_campo_atuacao (codigo TEXT REFERENCES habilidade_ef(codigo),
        campo_atuacao TEXT REFERENCES contexto_organizacao(id), PRIMARY KEY (codigo, campo_atuacao));
    CREATE TABLE habilidade_em_competencia (codigo TEXT REFERENCES habilidade_em(codigo),
        competencia TEXT REFERENCES competencia_especifica(id), PRIMARY KEY (codigo, competencia));
    CREATE TABLE habilidade_em_campo_atuacao (codigo TEXT REFERENCES habilidade_em(codigo),
        campo_atuacao TEXT REFERENCES contexto_organizacao(id), PRIMARY KEY (codigo, campo_atuacao));
    CREATE TABLE marco_legal (id TEXT PRIMARY KEY, tipo TEXT, titulo TEXT, ementa TEXT, url_oficial TEXT, nota TEXT);
    CREATE TABLE marco_legal_relacao (marco TEXT REFERENCES marco_legal(id),
        entidade TEXT, natureza TEXT, PRIMARY KEY (marco, entidade, natureza));
    CREATE TABLE perfil (id TEXT PRIMARY KEY, nome TEXT, descricao TEXT, sinonimos TEXT);
    CREATE TABLE eixo_computacao (id TEXT PRIMARY KEY, nome TEXT);
    CREATE TABLE objeto_computacao (id TEXT PRIMARY KEY, nome TEXT, pai TEXT REFERENCES objeto_computacao(id));
    CREATE TABLE competencia_computacao (id TEXT PRIMARY KEY, tipo TEXT, numero INTEGER, texto TEXT);
    CREATE TABLE aprendizagem_computacao (codigo TEXT PRIMARY KEY, documento TEXT, etapa TEXT, texto TEXT,
        eixo TEXT REFERENCES eixo_computacao(id), competencia TEXT REFERENCES competencia_computacao(id),
        grupo_etario TEXT, {VIG_DDL}, {FONTE_DDL});
    CREATE TABLE aprendizagem_computacao_ano (codigo TEXT REFERENCES aprendizagem_computacao(codigo),
        ano INTEGER, PRIMARY KEY (codigo, ano));
    CREATE TABLE aprendizagem_computacao_objeto (codigo TEXT REFERENCES aprendizagem_computacao(codigo),
        objeto TEXT REFERENCES objeto_computacao(id), PRIMARY KEY (codigo, objeto));
    CREATE INDEX idx_aco_eixo ON aprendizagem_computacao(eixo);
    CREATE INDEX idx_hef_componente ON habilidade_ef(componente);
    CREATE INDEX idx_hef_ano ON habilidade_ef_ano(ano);
    CREATE INDEX idx_hem_area ON habilidade_em(area);
    CREATE INDEX idx_oei_campo ON objetivo_ei(campo_experiencias);
    CREATE INDEX idx_ctx_tipo ON contexto_organizacao(tipo);
    ''')

    # NFC nos nomes: o macOS devolve NFD ao listar, o Linux devolve NFC — sem
    # normalizar, o meta diverge entre plataformas (CI reprova o dump lógico)
    import unicodedata
    checksums = SEP.join(
        f'{unicodedata.normalize("NFC", str(p.relative_to(FONTES)))}:{hashlib.sha256(p.read_bytes()).hexdigest()[:16]}'
        for p in sorted(FONTES.rglob('*'), key=lambda p: unicodedata.normalize('NFC', str(p)))
        if p.suffix in ('.pdf', '.xlsx'))
    c.executemany('INSERT INTO meta VALUES (?,?)', sorted({
        'data_version': DATA_VERSION, 'schema_version': 'schema-v1.0.0',
        'gerado_por': 'pipeline/derivar.py', 'fontes_sha256_16': checksums,
        'licenca_dados': 'CC BY 4.0', 'projeto': 'bncc.dev',
    }.items()))

    for d in est['documento_curricular']:
        c.execute('INSERT INTO documento_curricular VALUES (?,?,?,?,?)',
                  (d['id'], d['nome'], d['tipo'], d['esfera'], d['derivado_de']))
    for e in est['etapas']:
        c.execute('INSERT INTO etapa VALUES (?,?)', (e['id'], e['nome']))
    for m in est['modalidades']:
        c.execute('INSERT INTO modalidade VALUES (?,?,?)', (m['id'], m['nome'], SEP.join(m['transversal_a'])))
        for s in m['segmentos']:
            c.execute('INSERT INTO modalidade_segmento VALUES (?,?,?)', (s['id'], m['id'], s['corresponde_a']))
    for a in sorted(est['areas_conhecimento'], key=lambda x: x['id']):
        c.execute('INSERT INTO area_conhecimento VALUES (?,?,?,?)', (a['id'], a['etapa'], a['nome'], a.get('documento')))
    for k in sorted(est['componentes_curriculares'], key=lambda x: x['id']):
        pres = SEP.join(map(str, k['presenca']['anos'])) if k.get('presenca') else None
        c.execute('INSERT INTO componente_curricular VALUES (?,?,?,?,?,?,?,?,?)',
                  (k['id'], k['etapa'], k['nome'], k.get('sigla_codigo'), k['area'],
                   int(k['tem_aprendizagens_proprias']), pres, k.get('destaque_legal'), k.get('nota')))
    for r in sorted(est['recortes_temporais'], key=lambda x: x['id']):
        c.execute('INSERT INTO recorte_temporal VALUES (?,?,?,?,?,?,?,?)',
                  (r['id'], r['etapa'], r['tipo'], r.get('nome'), r.get('faixa'), r.get('numero'), r.get('segmento'), r.get('nota')))
    for x in est['campos_experiencias']:
        c.execute('INSERT INTO campo_experiencias VALUES (?,?,?)', (x['id'], x['nome'], x['documento']))
    for x in est['direitos_aprendizagem']:
        c.execute('INSERT INTO direito_aprendizagem VALUES (?,?,?)', (x['id'], x['nome'], x['documento']))
    for g in est['competencias_gerais']:
        c.execute('INSERT INTO competencia_geral VALUES (?,?,?,?,?,?,?,?,?)',
                  (g['id'], g['documento'], g['numero'], g['texto'], *fonte_cols(g.get('fonte'))))
    for s in sorted(est['competencias_especificas'], key=lambda x: x['id']):
        c.execute('INSERT INTO competencia_especifica VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
                  (s['id'], s['documento'], s['tipo'], s.get('area'), s.get('componente'),
                   s['numero'], s['texto'], *fonte_cols(s.get('fonte'))))
    for etapa, dados in (('EF', ef), ('EM', em)):
        for ctx in dados['contextos_organizacao']:
            c.execute('INSERT INTO contexto_organizacao VALUES (?,?,?,?,?,?,?,?,?,?)',
                      (ctx['id'], etapa, ctx['tipo'], ctx['nome'], ctx['componente'], *fonte_cols(ctx.get('fonte'))))

    for o in ei['objetivos']:
        v = o['vigencia']
        c.execute('INSERT INTO objetivo_ei VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                  (o['codigo'], o['documento'], o['texto'], o['campo_experiencias'], o['grupo_etario'],
                   o['alinhamento'], v['status'], v['desde'], v['ate'], *fonte_cols(o['fonte'])))
    for a in ei['alinhamentos']:
        c.execute('INSERT INTO alinhamento VALUES (?,?,?)', (a['id'], a['campo_experiencias'], a.get('nota')))
        for cod in a['objetivos']:
            c.execute('INSERT INTO alinhamento_objetivo VALUES (?,?)', (a['id'], cod))

    for h in ef['habilidades']:
        v, org = h['vigencia'], h['organizacao']
        c.execute('INSERT INTO habilidade_ef VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                  (h['codigo'], h['documento'], h['texto'], h['componente'], org['tipo'],
                   org.get('unidade_tematica'), org.get('pratica_linguagem'), org.get('eixo'),
                   v['status'], v['desde'], v['ate'], *fonte_cols(h['fonte'])))
        c.executemany('INSERT INTO habilidade_ef_ano VALUES (?,?)', [(h['codigo'], a) for a in h['anos']])
        c.executemany('INSERT INTO habilidade_ef_objeto VALUES (?,?)',
                      [(h['codigo'], o) for o in sorted(set(h['objetos_conhecimento']))])
        c.executemany('INSERT INTO habilidade_ef_campo_atuacao VALUES (?,?)',
                      [(h['codigo'], ca) for ca in sorted(set(org.get('campos_atuacao', [])))])

    for h in em['habilidades']:
        v = h['vigencia']
        c.execute('INSERT INTO habilidade_em VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',
                  (h['codigo'], h['documento'], h['texto'], h['area'], h['componente'],
                   v['status'], v['desde'], v['ate'], *fonte_cols(h['fonte'])))
        c.executemany('INSERT INTO habilidade_em_competencia VALUES (?,?)',
                      [(h['codigo'], ce) for ce in sorted(set(h['competencias_especificas']))])
        c.executemany('INSERT INTO habilidade_em_campo_atuacao VALUES (?,?)',
                      [(h['codigo'], ca) for ca in sorted(set(h['campos_atuacao_social'] or []))])

    for m in ml['marcos_legais']:
        c.execute('INSERT INTO marco_legal VALUES (?,?,?,?,?,?)',
                  (m['id'], m['tipo'], m['titulo'], m['ementa'], m['url_oficial'], m.get('nota')))
        c.executemany('INSERT INTO marco_legal_relacao VALUES (?,?,?)',
                      [(m['id'], r['entidade'], r['natureza']) for r in m['relaciona']])
    for p in pf['perfis']:
        c.execute('INSERT INTO perfil VALUES (?,?,?,?)',
                  (p['id'], p['nome'], p['descricao'], SEP.join(p['sinonimos'])))

    for e in co['eixos']:
        c.execute('INSERT INTO eixo_computacao VALUES (?,?)', (e['id'], e['nome']))
    for o in co['objetos_conhecimento']:
        c.execute('INSERT INTO objeto_computacao VALUES (?,?,?)', (o['id'], o['nome'], o['pai']))
    for k in co['competencias']:
        c.execute('INSERT INTO competencia_computacao VALUES (?,?,?,?)',
                  (k['id'], k['tipo'], k['numero'], k['texto']))
    for a in co['objetivos_ei'] + co['habilidades_ef'] + co['habilidades_em']:
        v = a['vigencia']
        c.execute('INSERT INTO aprendizagem_computacao VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                  (a['codigo'], a['documento'], a['codigo'][:2], a['texto'], a.get('eixo'),
                   a.get('competencia'), a.get('grupo_etario'),
                   v['status'], v['desde'], v['ate'], *fonte_cols(a['fonte'])))
        c.executemany('INSERT INTO aprendizagem_computacao_ano VALUES (?,?)',
                      [(a['codigo'], ano) for ano in a.get('anos', [])])
        c.executemany('INSERT INTO aprendizagem_computacao_objeto VALUES (?,?)',
                      [(a['codigo'], o) for o in sorted(set(a.get('objetos_conhecimento', [])))])

    db.commit()
    return db


def dump_logico(db):
    return '\n'.join(db.iterdump())


def gerar_csvs():
    CSV_DIR.mkdir(parents=True, exist_ok=True)

    def escrever(nome, colunas, linhas):
        with open(CSV_DIR / f'{nome}.csv', 'w', encoding='utf-8', newline='') as fh:
            w = csv.writer(fh, lineterminator='\n')
            w.writerow(colunas)
            w.writerows(linhas)

    escrever('habilidades-ef',
             ['codigo', 'componente', 'anos', 'organizacao_tipo', 'unidade_tematica', 'campos_atuacao',
              'pratica_linguagem', 'eixo', 'objetos_conhecimento', 'texto', 'vigencia_status', 'fonte_localizador', 'fonte_localizador_pdf'],
             [[h['codigo'], h['componente'], SEP.join(map(str, h['anos'])), h['organizacao']['tipo'],
               h['organizacao'].get('unidade_tematica') or '', SEP.join(h['organizacao'].get('campos_atuacao', [])),
               h['organizacao'].get('pratica_linguagem') or '', h['organizacao'].get('eixo') or '',
               SEP.join(h['objetos_conhecimento']), h['texto'], h['vigencia']['status'],
               h['fonte'].get('localizador', ''), h['fonte'].get('localizador_pdf', '')]
              for h in ef['habilidades']])

    escrever('habilidades-em',
             ['codigo', 'area', 'componente', 'competencias_especificas', 'campos_atuacao_social',
              'texto', 'vigencia_status', 'fonte_localizador', 'fonte_localizador_pdf'],
             [[h['codigo'], h['area'], h['componente'] or '', SEP.join(h['competencias_especificas']),
               SEP.join(h['campos_atuacao_social'] or []), h['texto'], h['vigencia']['status'],
               h['fonte'].get('localizador', ''), h['fonte'].get('localizador_pdf', '')]
              for h in em['habilidades']])

    escrever('objetivos-ei',
             ['codigo', 'campo_experiencias', 'grupo_etario', 'alinhamento', 'texto', 'vigencia_status', 'fonte_localizador'],
             [[o['codigo'], o['campo_experiencias'], o['grupo_etario'], o['alinhamento'], o['texto'],
               o['vigencia']['status'], o['fonte'].get('localizador', '')] for o in ei['objetivos']])

    escrever('alinhamentos', ['id', 'campo_experiencias', 'objetivos', 'nota'],
             [[a['id'], a['campo_experiencias'], SEP.join(a['objetivos']), a.get('nota', '')] for a in ei['alinhamentos']])

    escrever('competencias-gerais', ['id', 'numero', 'texto'],
             [[g['id'], g['numero'], g['texto']] for g in est['competencias_gerais']])

    escrever('competencias-especificas', ['id', 'tipo', 'area', 'componente', 'numero', 'texto'],
             [[s['id'], s['tipo'], s.get('area', ''), s.get('componente', ''), s['numero'], s['texto']]
              for s in sorted(est['competencias_especificas'], key=lambda x: x['id'])])

    escrever('contextos-organizacao', ['id', 'etapa', 'tipo', 'nome', 'componente'],
             [[c['id'], etapa, c['tipo'], c['nome'], c['componente']]
              for etapa, dados in (('EF', ef), ('EM', em)) for c in dados['contextos_organizacao']])

    escrever('componentes-curriculares',
             ['id', 'etapa', 'nome', 'sigla_codigo', 'area', 'tem_aprendizagens_proprias', 'presenca_anos', 'destaque_legal'],
             [[k['id'], k['etapa'], k['nome'], k.get('sigla_codigo') or '', k['area'],
               int(k['tem_aprendizagens_proprias']),
               SEP.join(map(str, k['presenca']['anos'])) if k.get('presenca') else '', k.get('destaque_legal', '')]
              for k in sorted(est['componentes_curriculares'], key=lambda x: x['id'])])

    escrever('areas-conhecimento', ['id', 'etapa', 'nome'],
             [[a['id'], a['etapa'], a['nome']] for a in sorted(est['areas_conhecimento'], key=lambda x: x['id'])])

    escrever('recortes-temporais', ['id', 'etapa', 'tipo', 'nome', 'faixa', 'numero', 'segmento'],
             [[r['id'], r['etapa'], r['tipo'], r.get('nome', ''), r.get('faixa', ''),
               r.get('numero', ''), r.get('segmento', '')]
              for r in sorted(est['recortes_temporais'], key=lambda x: x['id'])])

    escrever('marcos-legais', ['id', 'tipo', 'titulo', 'ementa', 'url_oficial', 'relaciona', 'nota'],
             [[m['id'], m['tipo'], m['titulo'], m['ementa'], m['url_oficial'],
               SEP.join(f"{r['entidade']}:{r['natureza']}" for r in m['relaciona']), m.get('nota', '')]
              for m in ml['marcos_legais']])

    escrever('perfis', ['id', 'nome', 'descricao', 'sinonimos'],
             [[p['id'], p['nome'], p['descricao'], SEP.join(p['sinonimos'])] for p in pf['perfis']])

    escrever('computacao',
             ['codigo', 'etapa', 'anos', 'grupo_etario', 'eixo', 'objetos_conhecimento', 'competencia',
              'texto', 'vigencia_status', 'fonte_localizador', 'fonte_localizador_pdf'],
             [[a['codigo'], a['codigo'][:2], SEP.join(map(str, a.get('anos', []))),
               a.get('grupo_etario', ''), a.get('eixo', ''),
               SEP.join(a.get('objetos_conhecimento', [])), a.get('competencia', ''),
               a['texto'], a['vigencia']['status'],
               a['fonte'].get('localizador', ''), a['fonte'].get('localizador_pdf', '')]
              for a in co['objetivos_ei'] + co['habilidades_ef'] + co['habilidades_em']])

    escrever('objetos-computacao', ['id', 'nome', 'pai'],
             [[o['id'], o['nome'], o['pai'] or ''] for o in co['objetos_conhecimento']])

    escrever('competencias-computacao', ['id', 'tipo', 'numero', 'texto'],
             [[k['id'], k['tipo'], k['numero'], k['texto']] for k in co['competencias']])


if __name__ == '__main__':
    DERIVADOS.mkdir(exist_ok=True)
    db = gerar_sqlite(DERIVADOS / 'bncc.sqlite')
    (DERIVADOS / 'bncc.sql').write_text(dump_logico(db) + '\n')
    db.close()
    gerar_csvs()
    n_csv = len(list(CSV_DIR.glob('*.csv')))
    tam = (DERIVADOS / 'bncc.sqlite').stat().st_size
    print(f'derivados: bncc.sqlite ({tam/1024:.0f} KB) + bncc.sql (dump lógico) + {n_csv} CSVs · data_version={DATA_VERSION}')
