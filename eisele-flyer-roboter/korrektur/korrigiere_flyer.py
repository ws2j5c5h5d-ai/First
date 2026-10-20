"""Inhaltliche Korrekturen am Flyer 'Programm Humanoide Roboter' (Seiten 1–6).

Es gibt keine offenen Layoutdaten; korrigiert wird die PDF direkt:
Text wird per Redaction entfernt und mit der Originalschrift (TeX Gyre Heros)
an derselben Grundlinie neu gesetzt. Bilder, Farben und Layout bleiben.

Aufruf: python3 korrigiere_flyer.py <flyer.pdf> <out.pdf>
"""
import os
import sys

import pymupdf

src, out = sys.argv[1:3]
HERE = os.path.dirname(os.path.abspath(__file__))
REG = os.path.join(HERE, 'fonts', 'texgyreheros-regular.otf')
BOLD = os.path.join(HERE, 'fonts', 'texgyreheros-bold.otf')
F_REG, F_BOLD = pymupdf.Font(fontfile=REG), pymupdf.Font(fontfile=BOLD)
NAVY, BLUEGREY, WHITE = (0x0b / 255, 0x33 / 255, 0x5e / 255), (0x54 / 255, 0x6f / 255, 0x8e / 255), (1, 1, 1)

doc = pymupdf.open(src)
LOG = []


def spans(page):
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            for s in l['spans']:
                yield s


def find(page, text, near=None):
    hits = [s for s in spans(page) if s['text'].strip() == text]
    if near:
        hits.sort(key=lambda s: abs(s['bbox'][0] - near[0]) + abs(s['bbox'][1] - near[1]))
    if not hits:
        raise SystemExit(f'Nicht gefunden auf S.{page.number + 1}: {text!r}')
    return hits[0]


def color(s):
    c = s['color']
    return ((c >> 16 & 255) / 255, (c >> 8 & 255) / 255, (c & 255) / 255)


def bold(s):
    return 'Bold' in s['font']


PENDING = {}            # Seite -> Liste einzufügender Texte (nach den Redactions)


def put(page, x, y, text, size, col, is_bold=False, align='l', rotate=0):
    PENDING.setdefault(page.number, []).append((x, y, text, size, col, is_bold, align, rotate))


def width(text, size, is_bold):
    return (F_BOLD if is_bold else F_REG).text_length(text, fontsize=size)


def core(bb):
    r = pymupdf.Rect(bb); h = r.height
    return pymupdf.Rect(r.x0, r.y0 + 0.28 * h, r.x1, r.y1 - 0.22 * h)


def replace(pno, old, new, near=None, align='l', note=None):
    page = doc[pno - 1]
    s = find(page, old, near)
    page.add_redact_annot(core(s['bbox']), fill=False)
    if new:
        x, y = s['origin']
        if align == 'c':
            x = (s['bbox'][0] + s['bbox'][2]) / 2
        elif align == 'r':
            x = s['bbox'][2]
        put(page, x, y, new, s['size'], color(s), bold(s), align)
    LOG.append((pno, old, new if new else '(entfernt)', note))
    return s


# ------------------------------------------------------------------ Seite 1
p = doc[0]
replace(1, 'Aluminium, bleifrei', 'Werkstoffe: Messing, Edelstahl und Aluminium')
replace(1, 'Extrem kleinbauend für kompletten Durchfluss', 'Extrem kleinbauend: ab Gewinde M3, ab ca. 2 g (863-4218)')
replace(1, 'KOMPLETTER DURCHFLUSS.', 'AB M3 UND AD3.')
replace(1, 'Schlauch ab AD3', 'P12 ab AD3 · P5500 ab AD4', near=(253, 563))
replace(1, 'Modulare Schwenkkupplung', 'Schwenkkupplung')
replace(1, 'VT5528-0202 · 628D', 'VT5528-0202', align='c')
replace(1, '686D', '', near=(448, 775))
# Badge "ALUMINIUM BLEIFREI" (Vektorgrafik mit Text in Kurven) entfernen
badge = pymupdf.Rect(46, 112, 144, 210)
p.add_redact_annot(badge, fill=False)
LOG.append((1, 'Badge „ALUMINIUM BLEIFREI“ (Grafik)', '(entfernt)', 'enthielt „bleifrei“'))
# Zusatz in der Spalte DREHANSCHLÜSSE
s = find(p, 'max. 800 U/min')
put(p, s['origin'][0], s['origin'][1] + 8.6, 'Ergänzend: Prüfstand', 6.9, BLUEGREY)
put(p, s['origin'][0], s['origin'][1] + 16.4, 'und Fertigung', 6.9, BLUEGREY)
LOG.append((1, 'Programmübersicht, Spalte DREHANSCHLÜSSE', '+ „Ergänzend: Prüfstand und Fertigung“', None))
# Seitenzahl
put(p, 555.1, 819.0, '1 / 6', 7.39, NAVY, True, 'r')
LOG.append((1, '(keine Seitenzahl)', '„1 / 6“', 'Poster ausdrücklich ohne Zählung'))

# ------------------------------------------------------------------ Seite 2
replace(2, 'Modulare Schwenkkupplung', 'Schwenkkupplung')
replace(2, 'Vier nummerierte Kanäle (1–4) und mittige Bohrung', 'Mittige Bohrung')
replace(2, 'Sechs Innensechskantschrauben, vier nummerierte Kanäle (1–4)', '')
s_del = replace(2, 'Flanschseite mit sechs Innensechskantschrauben', '')
s_mv = find(doc[1], 'Technische Daten und Varianten auf Anfrage')
doc[1].add_redact_annot(core(s_mv['bbox']), fill=False)
put(doc[1], s_mv['origin'][0], s_del['origin'][1], 'Technische Daten und Varianten auf Anfrage', s_mv['size'], color(s_mv))
# leeren Aufzählungspunkt der untersten Zeile entfernen
doc[1].add_redact_annot(pymupdf.Rect(324.5, 774.5, 330.2, 779.5), fill=False)

# ------------------------------------------------------------------ Seite 3
replace(3, '101', '105', near=(517, 603), align='r')
replace(3, 'I (mm)', 'i (mm)', align='c')
fn = find(doc[2], 'Maß L1 laut Katalog-Maßzeichnung der jeweiligen Bauform, alle Maße in mm. Abbildungen der Versionen maßstäblich zueinander.')
star = find(doc[2], '*', near=(47, 628))
for sp in (fn, star):
    doc[2].add_redact_annot(core(sp['bbox']), fill=False)
for k, (t, b) in enumerate((('*', True), (fn['text'], False))):
    pass
FY = 626.6
put(doc[2], 47.1, FY, '*', 6.9, NAVY, True)
put(doc[2], 49.7, FY, fn['text'], 6.9, NAVY)
put(doc[2], 47.1, FY + 7.6, 'i = Länge Einschraubgewinde laut Maßblatt.', 6.9, NAVY)
put(doc[2], 47.1, FY + 15.2, 'Vor Inbetriebnahme Dokument „Hinweis für Artikelgruppe 628D / 686D / 688D“ beachten (www.eisele.eu).', 6.9, NAVY)
LOG.append((3, 'Fußnoten', '+ „i = Länge Einschraubgewinde laut Maßblatt.“', None))
LOG.append((3, 'Fußnoten', '+ „Vor Inbetriebnahme Dokument … 628D / 686D / 688D … beachten (www.eisele.eu).“', None))
# EIGENSCHAFTEN neu setzen (5 Punkte, kompakter Zeilenabstand)
p3 = doc[2]
old = ['Werkstoff: Messing vernickelt, blank, POM', 'Whitworth-Rohrgewinde, gekammerter O-Ring',
       'Dichtungen NBR, FPM', 'Steckanschluss mit Lösehülse, Schlauch AD8 bis AD12']
first = find(p3, old[0])
for t in old:
    sp = find(p3, t)
    p3.add_redact_annot(core(sp['bbox']), fill=False)
p3.add_redact_annot(pymupdf.Rect(324.5, 740, 330.2, 797), fill=False)          # alte Aufzählungspunkte
items = ['Werkstoff: Ms vernickelt / Ms blank / POM, Kugellager Edelstahl / Keramik',
         'Whitworth-Rohrgewinde, gekammerter O-Ring', 'Dichtungen NBR, FPM',
         'Steckanschluss mit Lösehülse, Schlauch AD8 bis AD12',
         'Auch mit Einschraubgewinde G3/8 erhältlich (628D-06xx, 686D-06xx).']
SZ, MAXW, LEAD, GAP = 7.6, 556 - 337, 8.8, 2.6
y = 735.0
BULLETS3 = []
for it in items:
    words, lines, cur = it.split(' '), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if width(t, SZ, False) <= MAXW:
            cur = t
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    BULLETS3.append(y)
    for k, ln in enumerate(lines):
        put(p3, 337.0, y, ln, SZ, NAVY)
        y += LEAD
    y += GAP
LOG.append((3, 'Werkstoff: Messing vernickelt, blank, POM', 'Werkstoff: Ms vernickelt / Ms blank / POM, Kugellager Edelstahl / Keramik', None))
LOG.append((3, 'EIGENSCHAFTEN', '+ „Auch mit Einschraubgewinde G3/8 erhältlich (628D-06xx, 686D-06xx).“', 'Block auf 8,0 pt verdichtet'))

# ------------------------------------------------------------------ Seite 4: Maßzeichnungen
p4 = doc[3]
K = 1.15 / (300 / 72)
def R(x0, y0, x1, y1):
    return pymupdf.Rect(36 + x0 * K, 379.2 + y0 * K, 36 + x1 * K, 379.2 + y1 * K)
LABELS = [  # (Box in Renderkoordinaten, neuer Text, Ankerpunkt, Ausrichtung, Drehung)
    ((290, 118, 333, 139), 'SW 8', (312, 133), 'c', 0),
    ((463, 30, 492, 230), 'Schlauch AD3', (482, 226), 'l', 90),
    ((482, 102, 516, 136), '', None, 'l', 0),
    ((38, 300, 59, 340), 'M5', (54, 321), 'c', 90),
    ((511, 296, 539, 346), 'Ø 8', (530, 321), 'c', 90),
    ((138, 456, 168, 476), '4,5', (152, 470), 'c', 0),
    ((331, 456, 362, 476), '8,5', (347, 470), 'c', 0),
    ((252, 523, 287, 542), '16,5', (270, 537), 'c', 0),
    ((1126, 176, 1175, 195), 'SW 13', (1150, 190), 'c', 0),
    ((1236, 181, 1284, 200), 'SW 10', (1260, 195), 'c', 0),
    ((1392, 28, 1416, 224), 'Schlauch AD4', (1411, 220), 'l', 90),
    ((1022, 288, 1050, 362), 'Ø 14,2', (1043, 324), 'c', 90),
    ((1060, 306, 1080, 342), 'G1/8', (1075, 324), 'c', 90),
    ((1420, 296, 1452, 352), 'Ø 11', (1441, 324), 'c', 90),
    ((1261, 396, 1318, 415), 'ca. 11,6', (1290, 410), 'c', 0),
    ((1124, 458, 1152, 477), '5,5', (1138, 472), 'c', 0),
    ((1258, 458, 1304, 477), 'ca. 13', (1281, 472), 'c', 0),
    ((1203, 501, 1260, 520), 'ca. 21,6', (1231, 515), 'c', 0),
]
for box, txt, anc, al, rot in LABELS:
    p4.add_redact_annot(R(*box), fill=False)
    if txt:
        ax, ay = 36 + anc[0] * K, 379.2 + anc[1] * K
        put(p4, ax, ay, txt, 7.0, NAVY, False, al, rot)
LOG.append((4, 'Beschriftungen Maßzeichnungen (ca. 3,5–4 pt, als Kurven)', 'neu gesetzt in 7 pt; „6-kt.“ → „SW“, Toleranzangaben und Bezug „A“ entfernt', None))

# ------------------------------------------------------------------ Seite 5
replace(5, 'PROGRAMM 15', 'P15', near=(47, 58))
# ------------------------------------------------------------------ Seite 6
replace(6, 'EDELSTAHL & ALUMINIUM', 'EDELSTAHL')

# ------------------------------------------------------------------ Anwenden + Text setzen
for page in doc:
    if page.number == 3:
        page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                              graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED,
                              text=pymupdf.PDF_REDACT_TEXT_REMOVE)
    elif page.number in (0, 1, 2):
        page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                              graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED,
                              text=pymupdf.PDF_REDACT_TEXT_REMOVE)
    else:
        page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                              graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
                              text=pymupdf.PDF_REDACT_TEXT_REMOVE)
    page.insert_font(fontname='hr', fontfile=REG)
    page.insert_font(fontname='hb', fontfile=BOLD)
    for x, y, text, size, col, is_bold, align, rot in PENDING.get(page.number, []):
        w = width(text, size, is_bold)
        if rot == 90:
            if align == 'c':
                y += w / 2
            page.insert_text((x, y), text, fontname='hb' if is_bold else 'hr', fontsize=size, color=col, rotate=90)
            continue
        if align == 'c':
            x -= w / 2
        elif align == 'r':
            x -= w
        page.insert_text((x, y), text, fontname='hb' if is_bold else 'hr', fontsize=size, color=col)

# Aufzählungspunkte Seite 3 neu (Quadrat wie Original)
for yb in BULLETS3:
    doc[2].draw_rect(pymupdf.Rect(325.5, yb - 4.4, 329.2, yb - 1.4), color=None, fill=NAVY)
# Seite 2: unterste Zeile AUSFÜHRUNG ist hochgerückt, Aufzählungspunkt steht schon dort
# Seite 4: Restkreis des Bezugszeichens „A“ mit Flächenfarbe abdecken
doc[3].draw_rect(pymupdf.Rect(170.8, 409.4, 176.5, 415.1), color=None, fill=(0.949, 0.9451, 0.9412))

doc.save(out, garbage=3, deflate=True)
with open(os.path.join(HERE, 'aenderungsliste.tsv'), 'w') as f:
    for row in LOG:
        f.write('\t'.join('' if v is None else str(v) for v in row) + '\n')
print('ok', out, len(LOG), 'Einträge')
