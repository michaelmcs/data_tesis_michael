"""Genera Borrador_Tesis_CareER-GPT_EPG_UNA.docx sobre la plantilla oficial ANEXO 004."""
import os, sys, shutil, subprocess, tempfile, zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join(AQUI, '..')
PLANTILLA = os.path.join(RAIZ, 'plantilla', 'ANEXO_004_-_BORRADOR_DE_TESIS_EPG_UNA_-_CUANTITATIVO.docx')
SALIDA = os.path.join(RAIZ, 'Borrador_Tesis_CareER-GPT_EPG_UNA.docx')

tmp = tempfile.mkdtemp(prefix='careergpt_')
try:
    with zipfile.ZipFile(PLANTILLA) as z:
        z.extractall(tmp)
    env = dict(os.environ, CAREER_X=tmp)
    subprocess.run([sys.executable, os.path.join(AQUI, 'construir.py')], cwd=AQUI, env=env, check=True)
    subprocess.run([sys.executable, os.path.join(AQUI, 'empaquetar.py'), tmp, SALIDA], check=True)
    print('Borrador generado en', os.path.abspath(SALIDA))
finally:
    shutil.rmtree(tmp, ignore_errors=True)
