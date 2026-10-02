"""Convierte citas y bibliografía del borrador en campos de Mendeley (CSL_CITATION y CSL_BIBLIOGRAPHY).

Cada cita lleva dentro los metadatos de su referencia en formato CSL-JSON, igual que las citas insertadas con el
complemento de Mendeley para Word. También genera un archivo RIS para importar las referencias a Mendeley.
"""
import json, re, uuid

SCHEMA = 'https://github.com/citation-style-language/schema/raw/master/csl-citation.json'


# ------------------------------------------------------------------ lectura de referencias
def _autores(txt):
    """Separa 'Apellido, I., Apellido, I., y Apellido, I.' en una lista de (apellido, iniciales)."""
    txt = txt.strip()
    if not re.search(r', [A-ZÁÉÍÓÚÑŁ]\.', txt):  # autor institucional
        return [{'literal': txt.rstrip('.')}]
    txt = txt.replace('… ', '')
    partes = [p.strip() for p in re.split(r', (?=[^,]*)', txt)]
    out, i = [], 0
    while i < len(partes):
        fam = re.sub(r'^y ', '', partes[i]).strip()
        giv = partes[i + 1].strip() if i + 1 < len(partes) else ''
        if giv.startswith('y '):  # caso sin iniciales
            giv = ''
            i += 1
        else:
            i += 2
        out.append({'family': fam, 'given': giv})
    return out


def leer_referencia(ref):
    m = re.match(r'^(.*?) \((\d{4}|s\.f\.)\)\. (.*)$', ref)
    if not m:
        raise ValueError('Referencia sin año: ' + ref[:80])
    autores, anio, resto = m.group(1), m.group(2), m.group(3)
    url = re.search(r'(https?://\S+)$', resto)
    url = url.group(1) if url else None
    cuerpo = resto[:resto.rfind(url)].strip() if url else resto
    item = {'author': _autores(autores), 'issued': {'date-parts': [[int(anio)]]} if anio.isdigit() else {}}
    if url and 'doi.org/' in url:
        item['DOI'] = url.split('doi.org/', 1)[1]
    elif url:
        item['URL'] = url
    tesis = re.search(r'^(.*?) \[(.*?), (.*?)\]\.?$', cuerpo)
    if tesis:
        item.update(type='thesis', title=tesis.group(1).strip(), genre=tesis.group(2), publisher=tesis.group(3))
        return item
    conf = re.search(r'^(.*?)\. En (.*?)(?: \(pp\. ([\d-]+)\))?\.(?: (.*?)\.)?$', cuerpo)
    revista = re.search(r'^(.*)\. ([^.]+?), (\d+)(?:\((\d+)\))?(?:, ([\w\d-]+))?\.$', cuerpo)
    if revista and not conf:
        item.update(type='article-journal', title=revista.group(1), **{'container-title': revista.group(2)})
        item['volume'] = revista.group(3)
        if revista.group(4): item['issue'] = revista.group(4)
        if revista.group(5): item['page'] = revista.group(5)
        return item
    if conf:
        item.update(type='paper-conference', title=conf.group(1), **{'container-title': conf.group(2)})
        if conf.group(3): item['page'] = conf.group(3)
        if conf.group(4): item['publisher'] = conf.group(4)
        return item
    partes = cuerpo.rstrip('.').split('. ')
    item.update(type='book' if len(partes) == 2 else 'article', title=partes[0])
    if len(partes) > 1:
        item['publisher'] = '. '.join(partes[1:])
    return item


def etiqueta(item):
    a = item['author']
    nom = lambda x: x.get('literal') or x['family']
    if len(a) == 1: return nom(a[0])
    if len(a) == 2: return f'{nom(a[0])} y {nom(a[1])}'
    return f'{nom(a[0])} et al.'


# ------------------------------------------------------------------ índice de citas
class Indice:
    def __init__(self, referencias):
        self.refs = []
        for r in referencias:
            it = leer_referencia(r)
            it['id'] = 'ITEM-' + str(uuid.uuid5(uuid.NAMESPACE_URL, r))
            anio = str(it['issued']['date-parts'][0][0]) if it['issued'] else 's.f.'
            et = etiqueta(it)
            variantes = {et}
            a0 = it['author'][0]
            if 'family' in a0 and a0['given']:  # forma con inicial para desambiguar apellidos repetidos
                ini = ' '.join(x for x in a0['given'].split() if x.endswith('.'))
                variantes.add(f'{ini} {et}')
            self.refs.append(dict(texto=r, item=it, anio=anio, etiquetas=variantes))

    def buscar(self, et, anio):
        c = [x for x in self.refs if x['anio'] == anio and et in x['etiquetas']]
        return c[0] if len(c) == 1 else None

    def regex_narrativa(self):
        ets = sorted({e for x in self.refs for e in x['etiquetas']}, key=len, reverse=True)
        return re.compile('(' + '|'.join(re.escape(e) for e in ets) + r') \((\d{4})\)')


PAREN = re.compile(r'\(((?:[^();]+?, \d{4})(?:; [^();]+?, \d{4})*)\)')
SECUNDARIA = re.compile(r'\(([^();]+?, \d{4}), como se citó en ([^();]+?), (\d{4})\)')


def citas_en(texto, idx, rx_nar):
    """Devuelve lista de (inicio, fin, [refs], texto_visible, prefijo) con las citas encontradas en el texto."""
    out, ocupado = [], []
    for m in SECUNDARIA.finditer(texto):
        r = idx.buscar(m.group(2), m.group(3))
        if r:
            out.append((m.start(), m.end(), [r], m.group(0), m.group(1) + ', como se citó en ')); ocupado.append((m.start(), m.end()))
    for m in PAREN.finditer(texto):
        if any(a <= m.start() < b for a, b in ocupado): continue
        partes = m.group(1).split('; ')
        refs = []
        for p in partes:
            et, anio = p.rsplit(', ', 1)
            refs.append(idx.buscar(et, anio))
        if all(refs):
            out.append((m.start(), m.end(), refs, m.group(0), None)); ocupado.append((m.start(), m.end()))
    for m in rx_nar.finditer(texto):
        if any(a <= m.start() < b for a, b in ocupado): continue
        r = idx.buscar(m.group(1), m.group(2))
        if r:
            out.append((m.start(), m.end(), [r], m.group(0), 'narrativa'))
    return sorted(out)


def instruccion(refs, visible, modo):
    items = []
    for r in refs:
        ci = {'id': r['item']['id'], 'itemData': {k: v for k, v in r['item'].items()}, 'uris': [], 'isTemporary': False}
        if modo and modo not in ('narrativa',):
            ci['prefix'] = modo
        items.append(ci)
    formateada = '(' + '; '.join(f"{etiqueta(r['item'])}, {r['anio']}" for r in refs) + ')'
    men = {'formattedCitation': formateada, 'plainTextFormattedCitation': formateada,
           'previouslyFormattedCitation': formateada}
    if visible != formateada:
        men['manualFormatting'] = visible
    datos = {'citationID': 'MENDELEY_CITATION_' + str(uuid.uuid4()), 'properties': {'noteIndex': 0},
             'citationItems': items, 'mendeley': men, 'schema': SCHEMA}
    return 'ADDIN CSL_CITATION ' + json.dumps(datos, ensure_ascii=False)


# ------------------------------------------------------------------ exportación RIS
TIPOS_RIS = {'article-journal': 'JOUR', 'thesis': 'THES', 'paper-conference': 'CONF', 'book': 'BOOK', 'article': 'GEN'}


def ris(indice):
    lineas = []
    for r in indice.refs:
        it = r['item']
        lineas.append('TY  - ' + TIPOS_RIS.get(it['type'], 'GEN'))
        for a in it['author']:
            lineas.append('AU  - ' + (a.get('literal') or f"{a['family']}, {a['given']}".rstrip(', ')))
        lineas.append('TI  - ' + it.get('title', ''))
        if it['issued']: lineas.append('PY  - ' + str(it['issued']['date-parts'][0][0]))
        for k, tag in (('container-title', 'T2'), ('volume', 'VL'), ('issue', 'IS'), ('publisher', 'PB'), ('genre', 'M3'),
                       ('DOI', 'DO'), ('URL', 'UR')):
            if it.get(k): lineas.append(f'{tag}  - {it[k]}')
        if it.get('page'):
            sp = it['page'].split('-')
            lineas.append('SP  - ' + sp[0])
            if len(sp) > 1: lineas.append('EP  - ' + sp[1])
        lineas.append('ER  - ')
        lineas.append('')
    return '\n'.join(lineas)


# ------------------------------------------------------------------ correcciones de tipo para casos especiales
OVERRIDES = {
    'Fang, X.': {'type': 'article-journal',
                 'title': 'Large language models (LLMs) on tabular data: Prediction, generation, and understanding. A survey',
                 'container-title': 'Transactions on Machine Learning Research', 'publisher': None},
    'Li, Y., Li, Z.': {'type': 'article-journal', 'container-title': 'Cureus', 'publisher': None},
}
_leer_base = leer_referencia


def leer_referencia(ref):
    it = _leer_base(ref)
    for k, v in OVERRIDES.items():
        if ref.startswith(k):
            for c, x in v.items():
                if x is None: it.pop(c, None)
                else: it[c] = x
    return it


def segmentos(ref, item):
    """Divide la referencia en tramos (texto, cursiva) según APA 7."""
    cursivas = []
    t = item.get('type')
    if t == 'article-journal' and item.get('container-title'):
        c = item['container-title']
        i = ref.find(c + ', ' + item['volume']) if item.get('volume') else ref.find(c + '.')
        if i >= 0:
            cursivas.append((i, i + len(c)))
            if item.get('volume'):
                j = i + len(c) + 2
                cursivas.append((j, j + len(item['volume'])))
    elif t == 'paper-conference' and item.get('container-title'):
        i = ref.find(' En ' + item['container-title'])
        if i >= 0: cursivas.append((i + 4, i + 4 + len(item['container-title'])))
    elif item.get('title'):
        i = ref.find(item['title'])
        if i >= 0: cursivas.append((i, i + len(item['title'])))
    out, pos = [], 0
    for a, b in sorted(cursivas):
        if a > pos: out.append((ref[pos:a], False))
        out.append((ref[a:b], True)); pos = b
    if pos < len(ref): out.append((ref[pos:], False))
    return out


# ------------------------------------------------------------------ formato Mendeley Cite (complemento de Word)
import base64, random, time
from lxml import etree

WNS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
W = '{%s}' % WNS
XMLNS = '{http://www.w3.org/XML/1998/namespace}'


def _item_mendeley(item):
    d = {k: v for k, v in item.items() if v not in (None, '', [])}
    d['author'] = [dict(a, **{'parse-names': False, 'dropping-particle': '', 'non-dropping-particle': ''})
                   if 'family' in a else a for a in item['author']]
    d['container-title-short'] = ''
    return d


def cita_json(refs, visible):
    formateada = '(' + '; '.join(f"{etiqueta(r['item'])}, {r['anio']}" for r in refs) + ')'
    manual = visible != formateada
    return {'citationID': 'MENDELEY_CITATION_' + str(uuid.uuid4()), 'properties': {'noteIndex': 0}, 'isEdited': False,
            'manualOverride': {'isManuallyOverridden': manual, 'citeprocText': formateada,
                               'manualOverrideText': visible if manual else ''},
            'citationItems': [{'id': r['item']['id'], 'itemData': _item_mendeley(r['item']), 'isTemporary': False}
                              for r in refs]}


def _sdt_inline(datos, run):
    sdt = etree.Element(W + 'sdt'); pr = etree.SubElement(sdt, W + 'sdtPr')
    rpr = run.find(W + 'rPr')
    if rpr is not None: pr.append(etree.fromstring(etree.tostring(rpr)))
    etree.SubElement(pr, W + 'tag').set(W + 'val', 'MENDELEY_CITATION_v3_' +
                                         base64.b64encode(json.dumps(datos, ensure_ascii=False).encode()).decode())
    etree.SubElement(pr, W + 'id').set(W + 'val', str(random.randint(-2**31, 2**31 - 1)))
    cont = etree.SubElement(sdt, W + 'sdtContent'); cont.append(run)
    return sdt


def _run(texto, rpr):
    r = etree.Element(W + 'r')
    if rpr is not None: r.append(etree.fromstring(etree.tostring(rpr)))
    t = etree.SubElement(r, W + 't'); t.text = texto; t.set(XMLNS + 'space', 'preserve')
    return r


def convertir_citas(body, indice, excluir):
    """Reemplaza las citas en texto plano por controles de contenido de Mendeley. Devuelve la lista de citas."""
    rx = indice.regex_narrativa(); todas = []
    for p in body.iter(W + 'p'):
        if p in excluir: continue
        for r in list(p.iter(W + 'r')):
            t = r.find(W + 't')
            if t is None or not t.text or r.getparent().tag == W + 'sdtContent': continue
            encontradas = citas_en(t.text, indice, rx)
            if not encontradas: continue
            rpr = r.find(W + 'rPr'); padre = r.getparent(); pos = padre.index(r); texto = t.text
            nuevos, ini = [], 0
            for a, b, refs, visible, modo in encontradas:
                if a > ini: nuevos.append(_run(texto[ini:a], rpr))
                datos = cita_json(refs, visible); todas.append(datos)
                nuevos.append(_sdt_inline(datos, _run(visible, rpr))); ini = b
            if ini < len(texto): nuevos.append(_run(texto[ini:], rpr))
            padre.remove(r)
            for k, n in enumerate(nuevos): padre.insert(pos + k, n)
    return todas


def bibliografia_sdt(parrafos):
    """Envuelve los párrafos de la bibliografía en el control de contenido de Mendeley."""
    sdt = etree.Element(W + 'sdt'); pr = etree.SubElement(sdt, W + 'sdtPr')
    etree.SubElement(pr, W + 'tag').set(W + 'val', 'MENDELEY_BIBLIOGRAPHY')
    etree.SubElement(pr, W + 'id').set(W + 'val', str(random.randint(-2**31, 2**31 - 1)))
    padre = parrafos[0].getparent(); pos = padre.index(parrafos[0])
    cont = etree.SubElement(sdt, W + 'sdtContent')
    for p in parrafos:
        padre.remove(p); cont.append(p)
    padre.insert(pos, sdt)
    return sdt


ESTILO = {'id': 'https://www.zotero.org/styles/apa-no-ampersand',
          'title': 'American Psychological Association 7th edition (no ampersand)', 'format': 'author-date',
          'defaultLocale': None, 'isLocaleCodeValid': True}


def webextension_xml(citas):
    from xml.sax.saxutils import quoteattr
    props = [('MENDELEY_BIBLIOGRAPHY_IS_DIRTY', 'false'),
             ('MENDELEY_BIBLIOGRAPHY_LAST_MODIFIED', str(int(time.time() * 1000))),
             ('MENDELEY_CITATIONS', json.dumps(citas, ensure_ascii=False)),
             ('MENDELEY_CITATIONS_LOCALE_CODE', '"es-ES"'),
             ('MENDELEY_CITATIONS_STYLE', json.dumps(ESTILO))]
    p = ''.join(f'<we:property name="{n}" value={quoteattr(v)}/>' for n, v in props)
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<we:webextension xmlns:we="http://schemas.microsoft.com/office/webextensions/webextension/2010/11" '
            'id="{996E50D1-05FE-4C21-A547-D8AA47C460BC}"><we:reference id="wa104382081" version="1.55.1.0" '
            'store="es-MX" storeType="OMEX"/><we:alternateReferences><we:reference id="wa104382081" version="1.55.1.0" '
            'store="wa104382081" storeType="OMEX"/></we:alternateReferences><we:properties>' + p +
            '</we:properties><we:bindings/><we:snapshot xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/'
            'relationships"/></we:webextension>')


TASKPANES = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<wetp:taskpanes xmlns:wetp="http://schemas.'
             'microsoft.com/office/webextensions/taskpanes/2010/11"><wetp:taskpane dockstate="right" visibility="0" '
             'width="438" row="2"><wetp:webextensionref xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/'
             'relationships" r:id="rId1"/></wetp:taskpane></wetp:taskpanes>')
TASKPANES_RELS = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.'
                  'openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.microsoft.'
                  'com/office/2011/relationships/webextension" Target="webextension1.xml"/></Relationships>')


def registrar_complemento(X, citas):
    """Escribe en el paquete .docx el registro del complemento Mendeley Cite con la lista de citas."""
    import os
    d = os.path.join(X, 'word', 'webextensions'); os.makedirs(os.path.join(d, '_rels'), exist_ok=True)
    open(os.path.join(d, 'webextension1.xml'), 'w', encoding='utf8').write(webextension_xml(citas))
    open(os.path.join(d, 'taskpanes.xml'), 'w', encoding='utf8').write(TASKPANES)
    open(os.path.join(d, '_rels', 'taskpanes.xml.rels'), 'w', encoding='utf8').write(TASKPANES_RELS)
    ct_p = os.path.join(X, '[Content_Types].xml'); ct = open(ct_p, encoding='utf8').read()
    if 'webextensiontaskpanes' not in ct:
        ct = ct.replace('</Types>', '<Override PartName="/word/webextensions/taskpanes.xml" ContentType="application/'
                        'vnd.ms-office.webextensiontaskpanes+xml"/><Override PartName="/word/webextensions/'
                        'webextension1.xml" ContentType="application/vnd.ms-office.webextension+xml"/></Types>')
        open(ct_p, 'w', encoding='utf8').write(ct)
    rel_p = os.path.join(X, '_rels', '.rels'); rel = open(rel_p, encoding='utf8').read()
    if 'webextensiontaskpanes' not in rel:
        rel = rel.replace('</Relationships>', '<Relationship Id="rIdMendeleyCite" Type="http://schemas.microsoft.com/'
                          'office/2011/relationships/webextensiontaskpanes" Target="word/webextensions/taskpanes.xml"/>'
                          '</Relationships>')
        open(rel_p, 'w', encoding='utf8').write(rel)
