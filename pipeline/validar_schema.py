"""Valida os arquivos de dados contra os JSON Schemas (schema/).

Única dependência externa do projeto: jsonschema (só para validação; a
extração é stdlib puro). Instalação: pip install jsonschema

Inclui um autoteste negativo: corrompe registros em memória e confere que
o schema rejeita — prova de que a validação morde, não só passa.
"""
import copy
import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
except ImportError as e:
    sys.exit(f'erro ({e}): requer jsonschema>=4.18 — instale com `pip install --upgrade jsonschema`')

AQUI = Path(__file__).parent
SCHEMAS = AQUI.parent / 'schema'
DADOS = AQUI.parent / 'dados'
DATASET = DADOS / 'bncc-2018'

PARES = {
    'bncc-2018/estrutura.json': 'estrutura.schema.json',
    'bncc-2018/educacao-infantil.json': 'educacao-infantil.schema.json',
    'bncc-2018/ensino-fundamental.json': 'ensino-fundamental.schema.json',
    'bncc-2018/ensino-medio.json': 'ensino-medio.schema.json',
    'bncc-2018/marcos-legais.json': 'marcos-legais.schema.json',
    'bncc-2018/perfis.json': 'perfis.schema.json',
    'computacao-2022/computacao.json': 'computacao.schema.json',
}


def registro():
    """Registry com todos os schemas, resolvendo $refs entre arquivos."""
    recursos = []
    for arq in SCHEMAS.glob('*.json'):
        conteudo = json.loads(arq.read_text())
        recursos.append((conteudo['$id'], Resource.from_contents(conteudo)))
        # permite $ref relativo ("definicoes.json#/...") a partir de qualquer schema
        recursos.append((f'https://bncc.dev/schema/{arq.name}', Resource.from_contents(conteudo)))
    return Registry().with_resources(recursos)


def validar_arquivo(nome_dado, nome_schema, reg, dados=None):
    schema = json.loads((SCHEMAS / nome_schema).read_text())
    validador = Draft202012Validator(schema, registry=reg)
    if dados is None:
        dados = json.loads((DADOS / nome_dado).read_text())
    erros = sorted(validador.iter_errors(dados), key=lambda e: list(e.absolute_path))
    return erros


def autoteste_negativo(reg):
    """Registros corrompidos DEVEM falhar. Se passarem, o schema está frouxo."""
    casos = []
    ef = json.loads((DATASET / 'ensino-fundamental.json').read_text())

    caso = copy.deepcopy(ef)
    caso['habilidades'][0]['codigo'] = 'EF99XX01'          # ano e componente inválidos
    casos.append(('código EF inválido', 'ensino-fundamental.schema.json', caso))

    caso = copy.deepcopy(ef)
    caso['habilidades'][0]['campo_inventado'] = 'x'        # additionalProperties
    casos.append(('campo extra', 'ensino-fundamental.schema.json', caso))

    caso = copy.deepcopy(ef)
    lp = next(h for h in caso['habilidades'] if h['componente'] == 'ef-comp-lp')
    lp['organizacao'] = {'tipo': 'unidade_tematica', 'unidade_tematica': 'ef-comp-lp-ut-x'}
    casos.append(('LP com organização errada', 'ensino-fundamental.schema.json', caso))

    em = json.loads((DATASET / 'ensino-medio.json').read_text())
    caso = copy.deepcopy(em)
    area = next(h for h in caso['habilidades'] if h['componente'] is None)
    area['competencias_especificas'] = ['em-area-lgg-ce-01', 'em-area-lgg-ce-02']  # área deve ter 1
    casos.append(('habilidade de área com 2 competências', 'ensino-medio.schema.json', caso))

    ml = json.loads((DATASET / 'marcos-legais.json').read_text())
    caso = copy.deepcopy(ml)
    caso['marcos_legais'][0]['url_oficial'] = 'https://www.jusbrasil.com.br/lei'  # só fonte oficial gov.br
    casos.append(('marco legal com URL fora do gov.br', 'marcos-legais.schema.json', caso))

    co = json.loads((DADOS / 'computacao-2022' / 'computacao.json').read_text())
    caso = copy.deepcopy(co)
    caso['objetivos_ei'][0]['codigo'] = 'EI01CO01'         # anexo só define pré-escola (EI03)
    casos.append(('objetivo de Computação fora da pré-escola', 'computacao.schema.json', caso))

    caso = copy.deepcopy(co)
    caso['habilidades_ef'][0]['codigo'] = 'EF12CO01'       # bloco 12 não existe para CO
    casos.append(('habilidade CO com bloco inválido', 'computacao.schema.json', caso))

    falhas = []
    for nome, schema, dados in casos:
        if not validar_arquivo(None, schema, reg, dados=dados):
            falhas.append(nome)
    return falhas


if __name__ == '__main__':
    reg = registro()
    total_erros = 0
    for nome_dado, nome_schema in PARES.items():
        erros = validar_arquivo(nome_dado, nome_schema, reg)
        status = 'ok' if not erros else f'{len(erros)} ERROS'
        print(f'  {nome_dado:28} × {nome_schema:32} {status}')
        for e in erros[:5]:
            print(f'    - {"/".join(map(str, e.absolute_path))}: {e.message[:120]}')
        total_erros += len(erros)

    frouxos = autoteste_negativo(reg)
    if frouxos:
        print(f'  AUTOTESTE NEGATIVO FALHOU (schema frouxo): {frouxos}')
    else:
        print('  autoteste negativo: 7/7 corrupções rejeitadas')

    sys.exit(1 if total_erros or frouxos else 0)
