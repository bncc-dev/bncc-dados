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
except ImportError:
    sys.exit('erro: instale a dependência de validação com `pip install jsonschema`')

AQUI = Path(__file__).parent
SCHEMAS = AQUI.parent / 'schema'
DATASET = AQUI.parent / 'dados' / 'bncc-2018'

PARES = {
    'estrutura.json': 'estrutura.schema.json',
    'educacao-infantil.json': 'educacao-infantil.schema.json',
    'ensino-fundamental.json': 'ensino-fundamental.schema.json',
    'ensino-medio.json': 'ensino-medio.schema.json',
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
        dados = json.loads((DATASET / nome_dado).read_text())
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
        print('  autoteste negativo: 4/4 corrupções rejeitadas')

    sys.exit(1 if total_erros or frouxos else 0)
