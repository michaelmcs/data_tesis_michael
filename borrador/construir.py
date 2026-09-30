import copy, re, os, shutil, zipfile
from lxml import etree
from PIL import Image
from contenido2 import *

X = os.environ['CAREER_X']
WNS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
W = '{%s}' % WNS
MNS = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
M_ = '{%s}' % MNS
RNS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
XMLNS = '{http://www.w3.org/XML/1998/namespace}'

tree = etree.parse(X + '/word/document.xml'); root = tree.getroot(); body = root.find(W + 'body')

# ------------------------------------------------------------------ utilidades
def txt(el): return ''.join(el.itertext()).strip()
def sty(el):
    p = el if el.tag == W + 'p' else el.find('.//' + W + 'p')
    if p is None: return None
    s = p.find(W + 'pPr/' + W + 'pStyle'); return s.get(W + 'val') if s is not None else '-'
def blocks(): return list(body)
def protegido(b):
    return b.find('.//' + W + 'sectPr') is not None or b.find('.//' + W + "br[@{%s}type='page']" % WNS) is not None
def buscar(texto, estilo=None, desde=None, exacto=True):
    bs = blocks(); ini = bs.index(desde) + 1 if desde is not None else 0
    for b in bs[ini:]:
        ps = [b] if b.tag == W + 'p' else list(b.iter(W + 'p'))
        if b.tag == W + 'tbl': continue
        for p in ps:
            t = txt(p)
            if (t == texto if exacto else t.startswith(texto)) and (estilo is None or sty(p) == estilo):
                return b
    raise ValueError(f'No encontrado: {texto}')
def eliminar_entre(a, b):
    bs = blocks(); i, j = bs.index(a), bs.index(b)
    for el in bs[i + 1:j]:
        if not protegido(el): body.remove(el)
def insertar_despues(ref, nuevos):
    for el in nuevos:
        ref.addnext(el); ref = el
    return ref
def ppr_de(b):
    p = b if b.tag == W + 'p' else b.find('.//' + W + 'p')
    pp = p.find(W + 'pPr'); return copy.deepcopy(pp) if pp is not None else None

def run(t, b=False, i=False, sz=None):
    r = etree.Element(W + 'r')
    if b or i or sz:
        rp = etree.SubElement(r, W + 'rPr')
        if b: etree.SubElement(rp, W + 'b')
        if i: etree.SubElement(rp, W + 'i')
        if sz: etree.SubElement(rp, W + 'sz').set(W + 'val', str(sz)); etree.SubElement(rp, W + 'szCs').set(W + 'val', str(sz))
    tt = etree.SubElement(r, W + 't'); tt.text = t; tt.set(XMLNS + 'space', 'preserve'); return r
def par(estilo=None, partes=None, ppr=None, jc=None, ind=None):
    p = etree.Element(W + 'p')
    if ppr is not None:
        pp = copy.deepcopy(ppr); rp = pp.find(W + 'rPr')
        if rp is not None: pp.remove(rp)
        p.append(pp)
    elif estilo or jc or ind is not None:
        pp = etree.SubElement(p, W + 'pPr')
        if estilo: etree.SubElement(pp, W + 'pStyle').set(W + 'val', estilo)
        if ind is not None: etree.SubElement(pp, W + 'ind').set(W + 'left', str(ind))
        if jc: etree.SubElement(pp, W + 'jc').set(W + 'val', jc)
    if isinstance(partes, str): partes = [(partes, {})]
    for t, f in (partes or []): p.append(run(t, **f))
    return p

NIV = {'L12': ('TITTBFGL1L2', 'NotasL1L2', 0), 'L3': ('TITTBFGL3', 'NotasL3', 709), 'L4': ('TITTBFGL4L5', 'NotasL4L5', 1418)}
cont = {'Tabla': 0, 'Figura': 0}
def titulo(tipo, texto, nivel):
    cont[tipo] += 1
    p = par(NIV[nivel][0]); p.append(run(f'{tipo} '))
    fs = etree.SubElement(p, W + 'fldSimple'); fs.set(W + 'instr', f' SEQ {tipo} \\* ARABIC ')
    r = etree.SubElement(fs, W + 'r'); etree.SubElement(etree.SubElement(r, W + 'rPr'), W + 'noProof')
    etree.SubElement(r, W + 't').text = str(cont[tipo])
    p.append(run(' ')); br = etree.SubElement(p, W + 'r'); etree.SubElement(br, W + 'br')
    r2 = etree.SubElement(p, W + 'r'); rp = etree.SubElement(r2, W + 'rPr')
    etree.SubElement(rp, W + 'b').set(W + 'val', '0'); etree.SubElement(rp, W + 'i')
    t2 = etree.SubElement(r2, W + 't'); t2.text = texto
    return p
def nota(texto, nivel):
    return par(NIV[nivel][1], [('Nota.', {'i': True}), (' ' + texto, {})])

def celda(contenido, ancho, enc=False, ultima=False, primera=False, sz=None, izq=True):
    tc = etree.Element(W + 'tc'); pr = etree.SubElement(tc, W + 'tcPr')
    w = etree.SubElement(pr, W + 'tcW'); w.set(W + 'w', str(ancho)); w.set(W + 'type', 'dxa')
    bd = etree.SubElement(pr, W + 'tcBorders')
    for lado, cond in (('top', enc or primera), ('bottom', enc or ultima)):
        if cond:
            e = etree.SubElement(bd, W + lado)
            for k, v in (('val', 'single'), ('sz', '4'), ('space', '0'), ('color', 'auto')): e.set(W + k, v)
    etree.SubElement(pr, W + 'vAlign').set(W + 'val', 'center')
    lineas = contenido if isinstance(contenido, list) else [contenido]
    for k, ln in enumerate(lineas):
        p = etree.SubElement(tc, W + 'p'); pp = etree.SubElement(p, W + 'pPr')
        etree.SubElement(pp, W + 'pStyle').set(W + 'val', 'CONTTBFB')
        if sz:  # espaciado simple en tablas de texto denso
            sp = etree.SubElement(pp, W + 'spacing'); sp.set(W + 'after', '0'); sp.set(W + 'line', '240'); sp.set(W + 'lineRule', 'auto')
        etree.SubElement(pp, W + 'jc').set(W + 'val', 'center' if (enc or not izq) else 'left')
        negrita = enc or (isinstance(contenido, list) and ln.endswith(':'))
        p.append(run(ln, b=negrita, sz=sz))
    return tc
def tabla(enc, filas, nivel, anchos=None, sz=None, izq_todo=False, ancho_total=8503):
    ind = NIV[nivel][2]; total = ancho_total - ind
    nc = len(enc)
    if anchos is None:
        primero = int(total * (0.34 if nc >= 4 else 0.45)); resto = (total - primero) // (nc - 1)
        anchos = [primero] + [resto] * (nc - 1)
    if sz is None: sz = 18 if nc >= 5 else None
    t = etree.Element(W + 'tbl'); tp = etree.SubElement(t, W + 'tblPr')
    etree.SubElement(tp, W + 'tblStyle').set(W + 'val', 'Tablaconcuadrcula')
    tw = etree.SubElement(tp, W + 'tblW'); tw.set(W + 'w', str(sum(anchos))); tw.set(W + 'type', 'dxa')
    if ind:
        ti = etree.SubElement(tp, W + 'tblInd'); ti.set(W + 'w', str(ind)); ti.set(W + 'type', 'dxa')
    bd = etree.SubElement(tp, W + 'tblBorders')
    for lado in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        e = etree.SubElement(bd, W + lado)
        for k, v in (('val', 'none'), ('sz', '0'), ('space', '0'), ('color', 'auto')): e.set(W + k, v)
    etree.SubElement(tp, W + 'tblLayout').set(W + 'type', 'fixed')
    g = etree.SubElement(t, W + 'tblGrid')
    for a in anchos: etree.SubElement(g, W + 'gridCol').set(W + 'w', str(a))
    tr = etree.SubElement(t, W + 'tr'); trp = etree.SubElement(tr, W + 'trPr'); etree.SubElement(trp, W + 'tblHeader')
    for c, a in zip(enc, anchos): tr.append(celda(c, a, enc=True, sz=sz))
    for k, f in enumerate(filas):
        tr = etree.SubElement(t, W + 'tr'); etree.SubElement(etree.SubElement(tr, W + 'trPr'), W + 'cantSplit')
        for j, (c, a) in enumerate(zip(f, anchos)):
            tr.append(celda(c, a, ultima=(k == len(filas) - 1), sz=sz, izq=(j == 0 or izq_todo)))
    return t

# ---------------- ecuaciones OMML
def mr(t):
    r = etree.Element(M_ + 'r'); rp = etree.SubElement(r, W + 'rPr'); rf = etree.SubElement(rp, W + 'rFonts')
    rf.set(W + 'ascii', 'Cambria Math'); rf.set(W + 'hAnsi', 'Cambria Math'); tt = etree.SubElement(r, M_ + 't'); tt.text = t; tt.set(XMLNS + 'space', 'preserve'); return r
def mfrac(num, den):
    f = etree.Element(M_ + 'f'); fp = etree.SubElement(f, M_ + 'fPr'); cp = etree.SubElement(fp, M_ + 'ctrlPr')
    rf = etree.SubElement(etree.SubElement(cp, W + 'rPr'), W + 'rFonts'); rf.set(W + 'ascii', 'Cambria Math'); rf.set(W + 'hAnsi', 'Cambria Math')
    n_ = etree.SubElement(f, M_ + 'num'); d_ = etree.SubElement(f, M_ + 'den')
    for x in num: n_.append(x)
    for x in den: d_.append(x)
    return f
def msup(base, exp):
    s = etree.Element(M_ + 'sSup'); e = etree.SubElement(s, M_ + 'e'); e.append(mr(base))
    sp = etree.SubElement(s, M_ + 'sup'); sp.append(mr(exp)); return s
def _om(tokens):
    """Convierte una lista de tokens en elementos OMML."""
    if isinstance(tokens, str): tokens = [tokens]
    out = []
    for t in tokens:
        if isinstance(t, str): out.append(mr(t)); continue
        k = t[0]
        if k == 'f': out.append(mfrac(_om(t[1]), _om(t[2])))
        elif k in ('sub', 'sup'):
            el = etree.Element(M_ + ('sSub' if k == 'sub' else 'sSup')); e = etree.SubElement(el, M_ + 'e')
            for x in _om(t[1]): e.append(x)
            s_ = etree.SubElement(el, M_ + k)
            for x in _om(t[2]): s_.append(x)
            out.append(el)
        elif k == 'nary':
            el = etree.Element(M_ + 'nary'); pr = etree.SubElement(el, M_ + 'naryPr')
            etree.SubElement(pr, M_ + 'chr').set(M_ + 'val', t[1])
            if not t[3]: etree.SubElement(pr, M_ + 'supHide').set(M_ + 'val', '1')
            sb = etree.SubElement(el, M_ + 'sub')
            for x in _om(t[2]): sb.append(x)
            sp = etree.SubElement(el, M_ + 'sup')
            for x in _om(t[3] or []): sp.append(x)
            e = etree.SubElement(el, M_ + 'e')
            for x in _om(t[4]): e.append(x)
            out.append(el)
        elif k == 'rad':
            el = etree.Element(M_ + 'rad'); pr = etree.SubElement(el, M_ + 'radPr')
            etree.SubElement(pr, M_ + 'degHide').set(M_ + 'val', '1'); etree.SubElement(el, M_ + 'deg')
            e = etree.SubElement(el, M_ + 'e')
            for x in _om(t[1]): e.append(x)
            out.append(el)
    return out
def f(a, b): return ('f', a, b)
def sb(a, b): return ('sub', a, b)
def sp(a, b): return ('sup', a, b)
def nary(ch, a, b, e): return ('nary', ch, a, b, e)
EQS = {
 'F1': ['F1=2×', f(['Precisión×Sensibilidad'], ['Precisión+Sensibilidad'])],
 'ROUGE': ['ROUGE‑L=', f(['(1+', sp('β', '2'), ')R·P'], ['R+', sp('β', '2'), 'P'])],
 'LORA': ['h=', sb('W', '0'), 'x+ΔWx=', sb('W', '0'), 'x+', f(['α'], ['r']), 'BAx'],
 'PARAM': ['Parámetros entrenables=r(d+k)≪d×k'],
 'ATTN': ['Atención(Q,K,V)=softmax', '(', f(['Q', sp('K', '⊤')], [('rad', [sb('d', 'k')])]), ')', 'V'],
 'CE': ['ℒ(θ)=−', f(['1'], ['T']), nary('∑', 't=1', 'T', ['log ', sb('P', 'θ'), '(', sb('y', 't'), '∣', sb('y', '<t'), ',x)'])],
 'XGB1': ['ℒ=', nary('∑', 'i=1', 'n', ['l(', sb('y', 'i'), ',', sb('ŷ', 'i'), ')']), '+', nary('∑', 'k=1', 'K', ['Ω(', sb('f', 'k'), ')'])],
 'XGB2': ['Ω(f)=γT+', f(['1'], ['2']), 'λ', sp('‖w‖', '2')],
 'TFN': ['TFN=', f(['FN'], ['FN+VP'])],
 'AUC': ['AUC=P(', sp('ŝ', '+'), '>', sp('ŝ', '−'), ')'],
 'CLIFF': ['δ=', f(['#(', sb('x', 'i'), '>', sb('y', 'j'), ')−#(', sb('x', 'i'), '<', sb('y', 'j'), ')'], [sb('n', '1'), sb('n', '2')])],
 'CRAMER': ['V=', ('rad', [f([sp('χ', '2')], ['n(k−1)'])])],
 'BRIER': ['BS=', f(['1'], ['N']), nary('∑', 'i=1', 'N', [sp(['(', sb('p', 'i'), '−', sb('y', 'i'), ')'], '2')])],
 'BERTR': [sb('R', 'BERT'), '=', f(['1'], ['|x|']), nary('∑', [sb('x', 'i'), '∈x'], None, [sb('max', [sb('x̂', 'j'), '∈x̂']), ' ', sp(sb('x', 'i'), '⊤'), sb('x̂', 'j')])],
 'BERTF': [sb('F', 'BERT'), '=2', f([sb('P', 'BERT'), '·', sb('R', 'BERT')], [sb('P', 'BERT'), '+', sb('R', 'BERT')])],
 'DCG': ['DCG@k=', nary('∑', 'i=1', 'k', [f([sb('rel', 'i')], [sb('log', '2'), '(i+1)'])])],
 'NDCG': ['NDCG@k=', f(['DCG@k'], ['IDCG@k'])],
 'MRR': ['MRR=', f(['1'], ['|Q|']), nary('∑', 'q=1', '|Q|', [f(['1'], [sb('rank', 'q')])])],
}
def ecuacion(clave, ind):
    p = etree.Element(W + 'p'); pp = etree.SubElement(p, W + 'pPr')
    etree.SubElement(pp, W + 'ind').set(W + 'left', str(ind)); etree.SubElement(pp, W + 'jc').set(W + 'val', 'center')
    omp = etree.SubElement(p, M_ + 'oMathPara'); om = etree.SubElement(omp, M_ + 'oMath')
    for x in _om(EQS[clave]): om.append(x)
    return p

# ---------------- figuras
rels = etree.parse(X + '/word/_rels/document.xml.rels'); rr = rels.getroot()
RELNS = '{http://schemas.openxmlformats.org/package/2006/relationships}'
ids = [int(re.sub(r'\D', '', r.get('Id'))) for r in rr]
nid = [max(ids) + 1]; docpr = [5000]
def figura(archivo, nivel):
    os.makedirs(X + '/word/media', exist_ok=True)
    destino = f'careergpt_{archivo}'; shutil.copy(S + archivo, X + '/word/media/' + destino)
    rid = f'rId{nid[0]}'; nid[0] += 1
    rel = etree.SubElement(rr, RELNS + 'Relationship'); rel.set('Id', rid)
    rel.set('Type', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image'); rel.set('Target', 'media/' + destino)
    ind = NIV[nivel][2]; ancho_in = (8503 - ind) / 1440 - 0.1
    wpx, hpx = Image.open(S + archivo).size; cx = int(ancho_in * 914400); cy = int(cx * hpx / wpx)
    docpr[0] += 1
    xml = f'''<w:p xmlns:w="{WNS}" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture" xmlns:r="{RNS}"><w:pPr><w:pStyle w:val="CONTTBFB"/><w:ind w:left="{ind}"/></w:pPr><w:r><w:rPr><w:noProof/></w:rPr><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/><wp:effectExtent l="0" t="0" r="0" b="0"/><wp:docPr id="{docpr[0]}" name="Figura {docpr[0]}"/><wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr><a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic><pic:nvPicPr><pic:cNvPr id="{docpr[0]}" name="{destino}"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'''
    return etree.fromstring(xml)

def fijar_texto(b, texto):
    """Reemplaza el texto de un bloque (párrafo o control de contenido) conservando su formato."""
    sdt_pr = b.find(W + 'sdtPr') if b.tag == W + 'sdt' else None
    if sdt_pr is not None:
        sh = sdt_pr.find(W + 'showingPlcHdr')
        if sh is not None: sdt_pr.remove(sh)
    p = b if b.tag == W + 'p' else b.find('.//' + W + 'p')
    runs = p.findall('.//' + W + 'r')
    rpr = copy.deepcopy(runs[0].find(W + 'rPr')) if runs and runs[0].find(W + 'rPr') is not None else None
    if rpr is not None:
        for e in rpr.findall(W + 'rStyle'): rpr.remove(e)
    for el in list(p):
        if el.tag != W + 'pPr': p.remove(el)
    r = etree.SubElement(p, W + 'r')
    if rpr is not None: r.append(rpr)
    t = etree.SubElement(r, W + 't'); t.text = texto; t.set(XMLNS + 'space', 'preserve')

def items(lista, estilo, nivel, ind):
    out = []
    for it in lista:
        if isinstance(it, str): out.append(par(estilo, it))
        elif it[0] == 'eq': out.append(ecuacion(it[1], ind))
        elif it[0] == 'fig': out += [titulo('Figura', it[2], nivel), figura(it[1], nivel), nota(it[3], nivel)]
    return out

# =================================================================== CARÁTULA
fijar_texto(buscar('MAESTRÍA EN ….'), 'MAESTRÍA EN INFORMÁTICA')
fijar_texto(buscar('TÍTULO DEL BORRADOR DE TESIS'), TITULO)
fijar_texto(buscar('MAESTRO EN …….'), 'MAESTRO EN INFORMÁTICA')
fijar_texto(buscar('[CON MENCIÓN EN …]'), 'CON MENCIÓN EN GERENCIA DE TECNOLOGÍAS DE INFORMACIÓN Y COMUNICACIONES')
for b in [x for x in blocks() if txt(x) == 'Nombre(s) y Apellido(s) del Autor.']:
    fijar_texto(b, 'Michael Newton Cutipa Santi')

# =================================================================== ACRÓNIMOS
tacr = [b for b in blocks() if b.tag == W + 'tbl'][0]
filas = tacr.findall(W + 'tr'); modelo = copy.deepcopy(filas[0])
for f in filas: tacr.remove(f)
for sig, sig_txt in ACRONIMOS:
    f = copy.deepcopy(modelo); tcs = f.findall(W + 'tc')
    for tc, val in zip(tcs, [sig, ':', sig_txt]):
        p = tc.find(W + 'p')
        for el in list(p):
            if el.tag != W + 'pPr': p.remove(el)
        p.append(run(val))
    tacr.append(f)

# =================================================================== RESUMEN Y ABSTRACT
b_res = buscar('RESUMEN', 'TITLE01'); b_abs = buscar('ABSTRACT', 'TITLE01'); b_int = buscar('INTRODUCCIÓN', 'TITLE01')
pp_res = ppr_de(buscar('El resumen debe contener', exacto=False)); pp_kw = ppr_de(buscar('Palabras clave: Palabra 1', exacto=False))
eliminar_entre(b_res, b_abs)
insertar_despues(b_res, [par(ppr=pp_res, partes=RESUMEN),
                         par(ppr=pp_kw, partes=[('Palabras clave:', {'b': True}), (PALABRAS.split(':', 1)[1], {})])])
pp_ab = ppr_de(buscar('Aquí va el abstract', exacto=False)); pp_kwe = ppr_de(buscar('Keywords: Keyword 1', exacto=False))
eliminar_entre(b_abs, b_int)
insertar_despues(b_abs, [par(ppr=pp_ab, partes=ABSTRACT),
                         par(ppr=pp_kwe, partes=[('Keywords:', {'b': True}), (KEYWORDS.split(':', 1)[1], {})])])

# =================================================================== INTRODUCCIÓN
pp_in = ppr_de(buscar('Se elabora considerando', exacto=False))
b_c1 = buscar('CAPÍTULO I', 'TITLE01')
eliminar_entre(b_int, b_c1)
insertar_despues(b_int, [par(ppr=pp_in, partes=x) for x in INTRO])

# =================================================================== CAPÍTULO I
b_mt = buscar('Marco teórico', 'Ttulo2'); b_an = buscar('Antecedentes', 'Ttulo2')
eliminar_entre(b_mt, b_an)
nuevos = []
for tit, pars in MARCO:
    nuevos.append(par('Ttulo3', tit)); nuevos += items(pars, 'NORML3', 'L3', 709)
insertar_despues(b_mt, nuevos)
b_int_ = buscar('Internacionales', 'Ttulo3'); b_nac = buscar('Nacionales', 'Ttulo3'); b_loc = buscar('Locales', 'Ttulo3')
b_c2 = buscar('CAPÍTULO II', 'TITLE01')
eliminar_entre(b_an, b_int_)
insertar_despues(b_an, [par('NORML12', 'Se presentan los estudios previos que sustentan la investigación, organizados '
                        'según su ámbito internacional, nacional y local.')])
eliminar_entre(b_int_, b_nac); insertar_despues(b_int_, [par('NORML3', x) for x in ANT_INT])
eliminar_entre(b_nac, b_loc); insertar_despues(b_nac, [par('NORML3', x) for x in ANT_NAC])
eliminar_entre(b_loc, b_c2); insertar_despues(b_loc, [par('NORML3', x) for x in ANT_LOC])

# =================================================================== CAPÍTULO II
b_pp = buscar('PLANTEAMIENTO DEL PROBLEMA', 'Ttulo1'); b_id = buscar('Identificación del problema', 'Ttulo2')
eliminar_entre(b_pp, b_id)
b_en = buscar('Enunciados del problema', 'Ttulo2'); eliminar_entre(b_id, b_en)
insertar_despues(b_id, [par('NORML12', x) for x in IDENT])
b_pg = buscar('Problema general', 'Ttulo3'); eliminar_entre(b_en, b_pg); insertar_despues(b_en, [par('NORML12', ENUNC)])
b_pes = buscar('Problemas específicos', 'Ttulo3')
pp_pg = ppr_de(buscar('Problema general.', 'proobjhip')); eliminar_entre(b_pg, b_pes); insertar_despues(b_pg, [par(ppr=pp_pg, partes=PG)])
b_ju = buscar('Justificación', 'Ttulo2')
protos = [ppr_de(b) for b in blocks()[blocks().index(b_pes) + 1:blocks().index(b_ju)] if sty(b) == 'proobjhip']
eliminar_entre(b_pes, b_ju); insertar_despues(b_pes, [par(ppr=protos[min(k, len(protos) - 1)], partes=x) for k, x in enumerate(PE)])
b_ob = buscar('Objetivos', 'Ttulo2'); eliminar_entre(b_ju, b_ob); insertar_despues(b_ju, [par('NORML12', x) for x in JUST])
b_og = buscar('Objetivo general', 'Ttulo3'); eliminar_entre(b_ob, b_og); insertar_despues(b_ob, [par('NORML12', OBJ_INTRO)])
b_oes = buscar('Objetivos específicos', 'Ttulo3'); eliminar_entre(b_og, b_oes); insertar_despues(b_og, [par('NORML3', OG)])
b_hi = buscar('Hipótesis', 'Ttulo2')
protos = [ppr_de(b) for b in blocks()[blocks().index(b_oes) + 1:blocks().index(b_hi)] if sty(b) == 'proobjhip']
eliminar_entre(b_oes, b_hi); insertar_despues(b_oes, [par(ppr=protos[min(k, len(protos) - 1)], partes=x) for k, x in enumerate(OE)])
b_hg = buscar('Hipótesis general', 'Ttulo3'); b_hes = buscar('Hipótesis específicas', 'Ttulo3')
eliminar_entre(b_hg, b_hes); insertar_despues(b_hg, [par('NORML3', HG)])
b_c3 = buscar('CAPÍTULO III', 'TITLE01')
protos = [ppr_de(b) for b in blocks()[blocks().index(b_hes) + 1:blocks().index(b_c3)] if sty(b) == 'proobjhip']
eliminar_entre(b_hes, b_c3); insertar_despues(b_hes, [par(ppr=protos[min(k, len(protos) - 1)], partes=x) for k, x in enumerate(HE)])

# =================================================================== CAPÍTULO III
b_lu = buscar('Lugar de estudio', 'Ttulo2'); b_po = buscar('Población', 'Ttulo2'); b_mu = buscar('Muestra', 'Ttulo2')
b_me = buscar('Método de investigación', 'Ttulo2'); b_de = buscar('Descripción detallada de métodos por objetivos específicos', 'Ttulo2')
b_c4 = buscar('CAPÍTULO IV', 'TITLE01')
eliminar_entre(b_lu, b_po); insertar_despues(b_lu, [par('NORML12', x) for x in LUGAR])
eliminar_entre(b_po, b_mu)
excl_hist = P['postulaciones'] - P['con_historial']; excl_aus = P['con_historial'] - P['analizables']
t1 = [['Postulaciones registradas, 2021-I a 2025-II', n(P['postulaciones']), '100.0'],
      ['Excluidas por no contar con historial escolar emparejable', n(excl_hist), f'{excl_hist/P["postulaciones"]*100:.1f}'],
      ['Excluidas por ausencia al examen', n(excl_aus), f'{excl_aus/P["postulaciones"]*100:.1f}'],
      ['Conjunto analítico', n(P['analizables']), f'{P["analizables"]/P["postulaciones"]*100:.1f}']]
insertar_despues(b_po, [par('NORML12', x) for x in POBL] + [
    titulo('Tabla', 'Conformación del conjunto analítico de postulaciones, Universidad Nacional del Altiplano, 2021-I a 2025-II', 'L12'),
    tabla(['Etapa', 'Postulaciones', 'Porcentaje'], t1, 'L12', anchos=[5103, 1700, 1700]),
    nota(f'El conjunto analítico corresponde a {n(P["personas_analizables"])} personas. Elaboración propia con datos de la '
         'Oficina de Admisión de la UNAP y del SIAGIE.', 'L12')])
eliminar_entre(b_mu, b_me); insertar_despues(b_mu, [par('NORML12', x) for x in MUESTRA])
eliminar_entre(b_me, b_de); insertar_despues(b_me, items(METODO, 'NORML12', 'L12', 0))
eliminar_entre(b_de, b_c4)
nuevos = [par('NORML12', 'La metodología se describe por objetivo específico, considerando la descripción de las '
              'variables, el uso de materiales, equipos e insumos, y la prueba estadística inferencial aplicada.')]
for t3, subs in METODOS:
    nuevos.append(par('Ttulo3', t3))
    for t4, its in subs:
        nuevos.append(par('Ttulo4', t4))
        nuevos += items(its, 'NORML4L5', 'L4', 1440)
insertar_despues(b_de, nuevos)

# =================================================================== CAPÍTULO IV
b_re = buscar('Resultados', 'Ttulo2'); b_di = buscar('Discusión', 'Ttulo2')
eliminar_entre(b_re, b_di)
nuevos = [par('NORML12', RES_INTRO)]
import re as _re
for it in RES:
    k = it[0]
    if k == 'h3': nuevos.append(par('Ttulo3', it[1]))
    elif k == 'h4': nuevos.append(par('Ttulo4', it[1]))
    elif k == 'p3': nuevos.append(par('NORML3', it[1]))
    elif k == 'p4': nuevos.append(par('NORML4L5', it[1]))
    elif k in ('tbl3', 'tbl4'):
        nv = 'L3' if k == 'tbl3' else 'L4'
        nuevos += [titulo('Tabla', it[1], nv), tabla(it[2], it[3], nv), nota(it[4], nv)]
    elif k == 'fig4':
        nuevos += [titulo('Figura', it[1], 'L4'), figura(it[2], 'L4'), nota(it[3], 'L4')]
    elif k == 'rank':
        probs = _re.findall(r'([A-ZÁÉÍÓÚÑ:,\s]+?) (\d+\.\d) %', EJ['instruction'].split('Probabilidades estimadas de ingreso:')[1])
        filas = [[str(i + 1), p_.strip(), f'{float(v):.1f}'] for i, (p_, v) in enumerate(probs)]
        nuevos += [titulo('Tabla', 'Rankeo de programas estimado para un postulante ilustrativo del área de '
                          + EJ['area'].capitalize().replace('Biomédicas', 'Biomédicas'), 'L4'),
                   tabla(['Posición', 'Programa de estudios', 'Probabilidad de ingreso (%)'], filas, 'L4', anchos=[1300, 3585, 2200]),
                   nota('Postulante de un colegio ' + EJ['area_colegio'].lower() + ', seleccionado del corpus. Probabilidades '
                        'estimadas por el modelo XGBoost final y calibradas mediante regresión isotónica.', 'L4')]
    elif k == 'par':
        nuevos += [titulo('Tabla', 'Ejemplo de par de instrucción y respuesta del corpus CareER-Dataset', 'L3'),
                   tabla(['Componente', 'Contenido'], [['Instrucción', EJ['instruction']], ['Respuesta de referencia', EJ['output']]],
                         'L3', anchos=[1794, 6000], sz=20, izq_todo=True),
                   nota('Par correspondiente a la partición de entrenamiento. Elaboración propia.', 'L3')]
insertar_despues(b_re, nuevos)

b_con = buscar('CONCLUSIONES', 'TITLE01'); eliminar_entre(b_di, b_con)
insertar_despues(b_di, [par('NORML12', x) for x in DISC])

# =================================================================== CONCLUSIONES Y RECOMENDACIONES
pp_c = ppr_de(buscar('Aquí va la primera conclusión', 'CONCLUT1', exacto=False))
b_rec = buscar('RECOMENDACIONES', 'TITLE01'); eliminar_entre(b_con, b_rec)
insertar_despues(b_con, [par(ppr=pp_c, partes=x) for x in CONCL])
pp_r = ppr_de(buscar('Aquí va la primera recomendación', 'RECOMENT1', exacto=False))
b_bib = buscar('BIBLIOGRAFÍA', 'TITLE01'); eliminar_entre(b_rec, b_bib)
insertar_despues(b_rec, [par(ppr=pp_r, partes=x) for x in RECOM])

# =================================================================== BIBLIOGRAFÍA
pp_b = ppr_de(buscar('Las citas deben realizarse', 'BIBLIOGRAFIA', exacto=False))
b_anx = buscar('ANEXOS', 'TITLE01'); eliminar_entre(b_bib, b_anx)
insertar_despues(b_bib, [par(ppr=pp_b, partes=x) for x in BIB])

# =================================================================== ANEXOS
b_a1 = buscar('Anexo 1. Matriz de consistencia', exacto=False, desde=b_anx)
eliminar_entre(b_anx, b_a1)
b_a2 = [b for b in blocks()[blocks().index(b_a1)+1:] if 'Título del anexo 2' in txt(b)][0]
eliminar_entre(b_a1, b_a2)
filas_m = [[c for c in fila] for fila in MATRIZ]
sec_final = root.find(W + 'body/' + W + 'sectPr')
def salto_seccion(horizontal):
    sp = copy.deepcopy(sec_final)
    if horizontal:
        for e in sp.findall(W + 'pgNumType'): sp.remove(e)
        pz = sp.find(W + 'pgSz'); pz.set(W + 'w', '16838'); pz.set(W + 'h', '11906'); pz.set(W + 'orient', 'landscape')
    p = etree.Element(W + 'p'); pp = etree.SubElement(p, W + 'pPr'); pp.append(sp); return p
b_a1.addprevious(salto_seccion(False))
anch = [2239] * 5 + [2240]
insertar_despues(b_a1, [tabla(MATRIZ_HDR, filas_m, 'L12', anchos=anch, sz=18, izq_todo=True, ancho_total=13435), salto_seccion(True)])
pn = sec_final.find(W + 'pgNumType')
if pn is not None: sec_final.remove(pn)
ts = list(b_a2.iter(W + 't')); full = ''.join(t.text or '' for t in ts)
k = full.find('Título del anexo 2')
if k >= 0:
    pos = 0; hecho = False
    for t in ts:
        s0, s1 = pos, pos + len(t.text or ''); pos = s1
        if s1 <= k: continue
        if not hecho:
            t.text = (t.text or '')[:max(0, k - s0)] + 'Base de datos y código de procesamiento'; hecho = True
        else:
            t.text = ''
# el cambio de sección ya inicia página nueva: se quitan saltos de página sobrantes antes del Anexo 2
for el in blocks()[blocks().index(b_a1) + 1:blocks().index(b_a2)]:
    if el.tag == W + 'p' and el.find('.//' + W + 'sectPr') is None and el.find('.//' + W + "br[@{%s}type='page']" % WNS) is not None:
        body.remove(el)
fin = blocks()[blocks().index(b_a2) + 1:]
for el in fin:
    if el.tag == W + 'sectPr' or protegido(el): continue
    body.remove(el)
insertar_despues(b_a2, [
    par('NORML12', 'Las bases de datos anonimizadas de admisión y del SIAGIE, el corpus CareER-Dataset en formato JSONL y los '
        'programas de procesamiento en Python se encuentran disponibles para su validación en el siguiente enlace: '
        '[insertar enlace del repositorio].'),
    par('NORML12', 'Los programas comprenden: preprocesamiento y emparejamiento de las bases, cálculo de resultados y pruebas '
        'estadísticas, búsqueda de hiperparámetros del modelo tabular, y construcción del corpus de instrucción y respuesta.')])

# =================================================================== guardado
tree.write(X + '/word/document.xml', xml_declaration=True, encoding='UTF-8', standalone=True)
rels.write(X + '/word/_rels/document.xml.rels', xml_declaration=True, encoding='UTF-8', standalone=True)
ct = open(X + '/[Content_Types].xml', encoding='utf8').read()
if 'Extension="png"' not in ct:
    ct = ct.replace('<Default Extension="xml"', '<Default Extension="png" ContentType="image/png"/><Default Extension="xml"')
    open(X + '/[Content_Types].xml', 'w', encoding='utf8').write(ct)
print('Tablas:', cont['Tabla'], '| Figuras:', cont['Figura'])
