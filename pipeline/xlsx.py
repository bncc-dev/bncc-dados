"""Leitor mínimo de xlsx com stdlib (sem openpyxl/pandas no ambiente do protótipo).

Suficiente para as planilhas oficiais do MEC: strings compartilhadas, strings
inline e valores numéricos. Não trata fórmulas nem datas (não existem nelas).
"""
import re
import zipfile
from xml.etree import ElementTree as ET

NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


def _col_letra(ref):
    return re.match(r'([A-Z]+)', ref).group(1)


class Planilha:
    def __init__(self, caminho):
        self.caminho = caminho
        self._zip = zipfile.ZipFile(caminho)
        wb = ET.fromstring(self._zip.read('xl/workbook.xml'))
        self.abas = [s.get('name') for s in wb.findall('.//m:sheet', NS)]
        self._shared = []
        if 'xl/sharedStrings.xml' in self._zip.namelist():
            ss = ET.fromstring(self._zip.read('xl/sharedStrings.xml'))
            for si in ss.findall('m:si', NS):
                self._shared.append(''.join(t.text or '' for t in si.findall('.//m:t', NS)))

    def linhas(self, aba):
        """Itera (numero_linha, {coluna: valor}) da aba (nome exato)."""
        idx = self.abas.index(aba) + 1
        raiz = ET.fromstring(self._zip.read(f'xl/worksheets/sheet{idx}.xml'))
        for row in raiz.findall('.//m:row', NS):
            celulas = {}
            for c in row.findall('m:c', NS):
                v = c.find('m:v', NS)
                if v is None:
                    inline = c.find('m:is', NS)
                    valor = ''.join(t.text or '' for t in inline.findall('.//m:t', NS)) if inline is not None else ''
                elif c.get('t') == 's':
                    valor = self._shared[int(v.text)]
                else:
                    valor = v.text or ''
                celulas[_col_letra(c.get('r'))] = valor
            yield int(row.get('r')), celulas
