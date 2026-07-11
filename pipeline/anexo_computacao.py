"""Acesso ao anexo do Parecer CNE/CEB 2/2022 (BNCC Computação).

O PDF oficial tem tabela xref fora do padrão e o poppler não o lê
diretamente (nota em fontes/README.md). A normalização com Ghostscript
gera uma cópia legível em pipeline/saida/ — a fonte arquivada permanece
intocada. O texto normalizado serve à extração (páginas por código) e à
verificação caractere a caractere.
"""
import subprocess
from pathlib import Path

AQUI = Path(__file__).parent
ANEXO = AQUI.parent / 'fontes' / 'anexo-ao-parecer-cneceb-no-2-2022-bncc-computacao.pdf'
NORMALIZADO = AQUI / 'saida' / 'anexo-computacao-normalizado.pdf'


def normalizar_pdf():
    """Gera (se preciso) a cópia normalizada do anexo e devolve o caminho."""
    NORMALIZADO.parent.mkdir(exist_ok=True)
    if not NORMALIZADO.exists() or NORMALIZADO.stat().st_mtime < ANEXO.stat().st_mtime:
        subprocess.run(['gs', '-q', '-dNOPAUSE', '-dBATCH', '-sDEVICE=pdfwrite',
                        f'-sOutputFile={NORMALIZADO}', str(ANEXO)], check=True)
    return NORMALIZADO


def paginas_anexo():
    """Lista de textos, um por página do anexo (75)."""
    pdf = normalizar_pdf()
    raw = subprocess.run(['pdftotext', '-enc', 'UTF-8', str(pdf), '-'],
                         capture_output=True, check=True).stdout.decode('utf-8')
    return raw.split('\f')
