"""Feinschliff am 6-seitigen Flyer (nach korrigiere_flyer.py und baue_seite1.py).

Keine neuen Aussagen und keine Werte: Texte werden nur entfernt, umbrochen, verschoben
oder in der Größe angepasst; Maßzahlen kommen 1:1 aus den bestehenden Zeichnungen.

Aufruf: python3 feinschliff.py <in_6S.pdf> <out.pdf>
"""
import os
import sys

import pymupdf

src_path, out = sys.argv[1:3]
HERE = os.path.dirname(os.path.abspath(__file__))
REG = os.path.join(HERE, 'fonts', 'texgyreheros-regular.otf')
BOLD = os.path.join(HERE, 'fonts', 'texgyreheros-bold.otf')
F = {False: pymupdf.Font(fontfile=REG), True: pymupdf.Font(fontfile=BOLD)}
NAVY = (0x0b / 255, 0x33 / 255, 0x5e / 255)
GREY = (0.949, 0.9451, 0.9412)                 # Flächenfarbe der grauen Bänder (Quelldatei)
HENN_RED = (1.0, 0.0, 0.0)                     # #FF0000 aus HENN_connector_group_logo_aus_Praesentation1.svg
LW = 0.27                                      # Linienstärke der Maßlinien (Quelldatei S. 4)

src = pymupdf.open(src_path)                   # unveränderte Vorlage zum Auslesen
doc = pymupdf.open(src_path)
LOG = []
PENDING = {}                                   # Seite -> einzufügende Texte (nach allen Redactions)
RED = {}                                       # Seite -> [(Rect, Modus)]
AFTER = {}                                     # Seite -> Zeichenfunktionen (nach Redactions, vor Text)


def spans(page):
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            for s in l['spans']:
                if s['text'].strip():
                    yield s


def find(pno, text, near=None):
    hits = [s for s in spans(src[pno - 1]) if s['text'].strip() == text]
    if near:
        hits.sort(key=lambda s: abs(s['bbox'][0] - near[0]) + abs(s['bbox'][1] - near[1]))
    if not hits:
        raise SystemExit(f'Nicht gefunden auf S.{pno}: {text!r}')
    return hits[0]


def col(s):
    c = s['color']
    return ((c >> 16 & 255) / 255, (c >> 8 & 255) / 255, (c & 255) / 255)


def core(bb):
    r = pymupdf.Rect(bb); h = r.height
    return pymupdf.Rect(r.x0, r.y0 + 0.28 * h, r.x1, r.y1 - 0.22 * h)


def redact(pno, rect, mode='text'):
    """mode: 'text' = nur Text; 'art' = Text + vollständig bedeckte Vektorgrafik;
    'artonly' = nur bedeckte Vektorgrafik; 'img' = Text + Bilder."""
    RED.setdefault(pno, []).append((pymupdf.Rect(rect), mode))


def put(pno, x, y, text, size, color=NAVY, bold=False, align='l', rotate=0):
    PENDING.setdefault(pno, []).append((x, y, text, size, color, bold, align, rotate))


def after(pno, fn):
    AFTER.setdefault(pno, []).append(fn)


def move_span(pno, s, dx=0.0, dy=0.0, size=None, text=None):
    redact(pno, core(s['bbox']))
    put(pno, s['origin'][0] + dx, s['origin'][1] + dy, text or s['text'].strip() if text is None else text,
        size or s['size'], col(s), 'Bold' in s['font'])


def copy_paths(pno_src, region, matrix, fill=None, keep=lambda d: True):
    """Vektorpfade aus der Vorlage (vollständig in region) transformiert neu zeichnen."""
    region = pymupdf.Rect(region)
    ds = [d for d in src[pno_src - 1].get_drawings() if region.contains(d['rect']) and keep(d)]

    def draw(page):
        for d in ds:
            sh = page.new_shape()
            for it in d['items']:
                if it[0] == 'l':
                    sh.draw_line(it[1] * matrix, it[2] * matrix)
                elif it[0] == 'c':
                    sh.draw_bezier(it[1] * matrix, it[2] * matrix, it[3] * matrix, it[4] * matrix)
                elif it[0] == 're':
                    sh.draw_rect(pymupdf.Rect(it[1]) * matrix)
                elif it[0] == 'qu':
                    sh.draw_quad(pymupdf.Quad(it[1]) * matrix)
            lc = d.get('lineCap') or (0,)
            sh.finish(fill=(fill if (fill and d.get('fill')) else d.get('fill')), color=d.get('color'),
                      width=(d.get('width') or 0) * (matrix.a if d.get('color') else 1),
                      lineCap=max(lc) if isinstance(lc, (tuple, list)) else lc,
                      lineJoin=int(d.get('lineJoin') or 0), dashes=d.get('dashes'),
                      even_odd=bool(d.get('even_odd')), closePath=bool(d.get('closePath')),
                      fill_opacity=d.get('fill_opacity') or 1, stroke_opacity=d.get('stroke_opacity') or 1)
            sh.commit()
    return draw, ds


def dim_h(page, x0, x1, y):
    """Horizontale Maßlinie mit zwei Pfeilen (Geometrie wie Quelldatei: 3,2 x 0,9 pt)."""
    page.draw_line((x0, y), (x1, y), color=NAVY, width=LW)
    for tip, sgn in ((x0, 1), (x1, -1)):
        page.draw_polyline([(tip, y), (tip + sgn * 3.2, y - 0.45), (tip + sgn * 3.2, y + 0.45), (tip, y)],
                           color=NAVY, fill=NAVY, width=LW, closePath=True)


# ================================================================== SEITE 1
s = find(1, 'NEU')
redact(1, pymupdf.Rect(86.0, 516.4, 109.8, 527.0), 'art')              # Badge (Fläche + Text)
LOG.append((1, 'Badge „NEU“ neben „NEUHEIT“', '(entfernt)'))

a, b = find(1, 'V0129-'), find(1, '1850-040601')
ref = find(1, '628D · 686D')
num = 'V0129-1850-040601'
DIV = 142.5                                   # Spaltentrennlinie (Quelldatei)
size = int(min(ref['size'], (DIV - 47.1 - 5.0) / F[True].text_length(num, 1)) * 10) / 10
for sp in (a, b):
    redact(1, core(sp['bbox']))
put(1, ref['origin'][0] - 103.1, ref['origin'][1], num, size, col(ref), True)
sk = find(1, 'Schwenkkupplung', near=(47, 569))
gw = find(1, 'Gerade und Winkel')
move_span(1, sk, dy=gw['origin'][1] - sk['origin'][1])
LOG.append((1, 'Spaltenkopf „V0129-/1850-040601“ zweizeilig, 15,5 pt', f'„V0129-1850-040601“ einzeilig, {size:.1f} pt; „Schwenkkupplung“ auf Höhe der Nachbarspalten'))

# BAUWEISEN: zwei Gruppen gleichmäßig über die Blockbreite verteilen
X0, X1 = 324.8, 555.1
for name, icon_box, texts, cx_new in (
        ('GERADE', (330, 705, 392, 740), ['GERADE', '863-4218 · 529-5018G', 'VT5528-0202'], X0 + (X1 - X0) / 4),
        ('WINKEL', (436, 706, 486, 745), ['WINKEL', '887-4218 schwenkbar'], X0 + 3 * (X1 - X0) / 4)):
    sps = [find(1, t, near=(340 if name == 'GERADE' else 440, 760)) for t in texts]
    cx_old = (sps[0]['bbox'][0] + sps[0]['bbox'][2]) / 2
    dx = cx_new - cx_old
    for sp in sps:
        move_span(1, sp, dx=dx)
    redact(1, icon_box, 'artonly')
    fn, _ = copy_paths(1, icon_box, pymupdf.Matrix(1, 0, 0, 1, dx, 0))
    after(1, fn)
LOG.append((1, 'BAUWEISEN: Gruppen GERADE/WINKEL links gedrängt, rechts Leerfläche', 'Gruppen auf 1/4 und 3/4 der Blockbreite verteilt (Inhalt unverändert)'))

# ================================================================== SEITE 2
t_neu = find(2, 'NEUHEIT', near=(47, 31))
t_sk = find(2, 'SCHWENKKUPPLUNG', near=(47, 59))
redact(2, core(t_neu['bbox']))
move_span(2, t_sk, dy=t_neu['origin'][1] - t_sk['origin'][1])
put(2, t_sk['origin'][0], t_sk['origin'][1], 'V0129-1850-040601', t_sk['size'], col(t_sk), True)
LOG.append((2, 'Titel „NEUHEIT / SCHWENKKUPPLUNG“', 'Titel zweizeilig „SCHWENKKUPPLUNG / V0129-1850-040601“'))
# Abbildung „Flanschseite“ oben rechts + Bildunterschrift entfernen
redact(2, pymupdf.Rect(400, 135, 541, 256), 'img')
for t in ('Flanschseite', 'V0129-1850-040601 · Ansicht von hinten'):
    redact(2, core(find(2, t, near=(466, 259))['bbox']))
LOG.append((2, 'Abbildung „Flanschseite“ oben rechts mit Bildunterschrift', '(entfernt; Ansicht bleibt unter ANSICHTEN & DETAILS)'))
# Hauptfoto vergrößern
info = [i for i in src[1].get_image_info(xrefs=True) if abs(i['bbox'][0] - 181.5) < 1][0]
old = pymupdf.Rect(info['bbox'])
redact(2, pymupdf.Rect(old.x0 + 8, old.y0 + 8, old.x1 - 8, old.y1 - 8), 'img')
NH = 194.0
new = pymupdf.Rect(190.0, 100.0, 190.0 + NH * old.width / old.height, 100.0 + NH)
after(2, lambda pg: pg.insert_image(new, xref=info['xref']))
c1, c2 = find(2, 'V0129-1850-040601', near=(180, 259)), find(2, 'Schwenkkupplung', near=(180, 276))
fl = find(2, 'Flanschseite', near=(466, 259)); fl2 = find(2, 'V0129-1850-040601 · Ansicht von hinten')
for c, ref_ in ((c1, fl), (c2, fl2)):
    redact(2, core(c['bbox']))
    put(2, ref_['bbox'][2], ref_['origin'][1], c['text'].strip(), c['size'], col(c), 'Bold' in c['font'], 'r')
LOG.append((2, f'Produktfoto {old.width:.0f} × {old.height:.0f} pt, Bildunterschrift links darunter',
            f'Produktfoto {new.width:.0f} × {new.height:.0f} pt (×{new.height / old.height:.2f}), Bildunterschrift rechtsbündig unten'))
# „Mittige Bohrung“ unter „Stirnseite“ entfernen
redact(2, core(find(2, 'Mittige Bohrung', near=(47, 566))['bbox']))
LOG.append((2, '„Mittige Bohrung“ unter Abbildung „Stirnseite“', '(entfernt; steht im Block SCHWENKKUPPLUNG)'))
# MUSTER & DATEN ANFRAGEN: höher, größer, als Karte mit QR-Code
h1 = find(2, 'MUSTER & DATEN ANFRAGEN')
t1 = find(2, 'Technische Daten, Varianten und Anschlussgrößen erhalten Sie auf Anfrage.')
t2 = find(2, 'info@eisele.eu · Tel. +49 (0)7151-1719-0')
redact(2, pymupdf.Rect(40, 582.5, 562, 641), 'art')                    # Trennlinie, Texte, QR
CARD = pymupdf.Rect(47.1, 571.0, 555.6, 643.0)
QR_OLD = pymupdf.Rect(508.5, 592.5, 555.6, 639.6)
QS = 62.0 / QR_OLD.width
QR_NEW = pymupdf.Rect(CARD.x1 - 7 - 62.0, CARD.y0 + 5, CARD.x1 - 7, CARD.y0 + 5 + 62.0 * QR_OLD.height / QR_OLD.width)
qr_m = pymupdf.Matrix(QS, 0, 0, QS, QR_NEW.x0 - QR_OLD.x0 * QS, QR_NEW.y0 - QR_OLD.y0 * QS)
qr_draw, qr_ds = copy_paths(2, QR_OLD, qr_m)


def card(pg):
    pg.draw_rect(CARD, color=None, fill=(1, 1, 1))
    pg.draw_rect(pymupdf.Rect(CARD.x0, CARD.y0, CARD.x0 + 4, CARD.y1), color=None, fill=NAVY)
    qr_draw(pg)


after(2, card)
TX = CARD.x0 + 14
put(2, TX, 593.0, h1['text'].strip(), 12.5, col(h1), True)
put(2, TX, 609.5, t1['text'].strip(), 8.6, col(t1), False)
put(2, TX, 622.5, t2['text'].strip(), 8.6, col(t2), True)
LOG.append((2, 'Block MUSTER & DATEN ANFRAGEN: ab y 594, Titel 10,5 pt, Text 8 pt, QR 47 pt',
            'weiße Karte mit Navy-Kante ab y 571, Titel 12,5 pt, Text 8,6 pt, QR 62 pt'))

# ================================================================== SEITE 3
EIG = [('Werkstoff: Ms vernickelt / Ms blank / POM, Kugellager Edelstahl', 'Werkstoff: Ms vernickelt / Ms blank / POM,'),
       ('/ Keramik', 'Kugellager Edelstahl/Keramik'),
       ('Steckanschluss mit Lösehülse, Schlauch AD8 bis AD12', 'Schlauch AD8 bis AD12'),
       ('Auch mit Einschraubgewinde G3/8 erhältlich (628D-06xx,', 'Auch mit Einschraubgewinde G3/8 erhältlich'),
       ('686D-06xx).', '(628D-06xx, 686D-06xx).')]
for old_t, new_t in EIG:
    sp = find(3, old_t)
    redact(3, core(sp['bbox']))
    put(3, sp['origin'][0], sp['origin'][1], new_t, sp['size'], col(sp))
LOG.append((3, 'Steckanschluss mit Lösehülse, Schlauch AD8 bis AD12', 'Schlauch AD8 bis AD12'))
LOG.append((3, '„… Kugellager Edelstahl“ / „/ Keramik“ (Wortrest allein)', '„… POM,“ / „Kugellager Edelstahl/Keramik“'))
LOG.append((3, '„… erhältlich (628D-06xx,“ / „686D-06xx).“', '„… erhältlich“ / „(628D-06xx, 686D-06xx).“'))

# ================================================================== SEITE 4
fn4 = find(4, 'Programme P12 und P5500 mit metrischem und zölligem Gewinde. Länge = Gesamtlänge laut Maßblatt.')
put(4, 47.1, fn4['origin'][1] + 7.6, 'Nennmaße, Toleranzen siehe Maßblatt.', fn4['size'], col(fn4))
LOG.append((4, '(keine)', 'Fußnote „Nennmaße, Toleranzen siehe Maßblatt.“'))
# VT5528-0202: Maßketten nach unten ziehen, damit Maßzahlen frei von Linien stehen
for t in ('ca. 11,6', '5,5', 'ca. 13', 'ca. 21,6'):
    redact(4, find(4, t, near=(360, 500))['bbox'])
Y116, Y13, Y216 = 501.5, 515.0, 528.5


def vt_dims(pg):
    pg.draw_rect(pymupdf.Rect(336.0, 492.6, 416.0, 526.0), color=None, fill=GREY)
    for x, y0, y1 in ((341.2, 492.0, Y216 + 1.2), (359.0, 492.0, Y13 + 1.2), (368.7, 492.0, Y13 + 1.2),
                      (373.6, 492.0, Y116 + 1.2), (411.1, 492.0, Y216 + 1.2)):
        pg.draw_line((x, y0), (x, y1), color=NAVY, width=LW)
    dim_h(pg, 373.6, 411.1, Y116)
    dim_h(pg, 341.2, 359.0, Y13)
    dim_h(pg, 368.7, 411.1, Y13)
    dim_h(pg, 341.2, 411.1, Y216)


after(4, vt_dims)
for t, x0, x1, y in (('ca. 11,6', 373.6, 411.1, Y116), ('5,5', 341.2, 359.0, Y13),
                     ('ca. 13', 368.7, 411.1, Y13), ('ca. 21,6', 341.2, 411.1, Y216)):
    put(4, (x0 + x1) / 2, y - 1.6, t, 7.0, NAVY, False, 'c')
LOG.append((4, 'VT5528-0202: „ca. 11,6“ auf Kontur/Hilfslinie, Maßlinien 1,4 pt unter dem Bauteil',
            'Maßlinien auf y 501,5 / 515 / 528,5 gezogen, Hilfslinien verlängert; Maßzahlen unverändert'))

# ================================================================== SEITEN 5 und 6: Maßzeichnungen
K = 72 / 400                                    # Zoom-Pixel (400 dpi) -> pt
LABEL_BOXES = {}


def labels(pno, origin, items, shift=0.0):
    ox, oy = origin
    boxes = []
    for box, txt, anc, al, rot in items:
        r = pymupdf.Rect(ox + box[0] * K, oy + box[1] * K, ox + box[2] * K, oy + box[3] * K)
        boxes.append(r)
        LABEL_BOXES.setdefault(pno, []).append(r)
        redact(pno, r, 'artonly')
        if txt:
            put(pno, ox + anc[0] * K, oy + anc[1] * K + shift - (0.8 if rot == 0 else 0), txt, 7.0, NAVY, False, al, rot)
    return boxes


labels(5, (36, 375), [   # 863-4218
    ((165, 283, 250, 306), '6-kt. 1,5', (248, 304), 'r', 0),
    ((938, 68, 974, 374), 'Schlauch AD3', (961, 366), 'l', 90),
    ((60, 448, 84, 492), 'Ø 6', (81, 470), 'c', 90),
    ((136, 453, 156, 487), 'M3', (153, 470), 'c', 90),
    ((994, 432, 1021, 500), 'Ø 5,8', (1017, 466), 'c', 90),
    ((260, 662, 282, 686), '3', (270, 683), 'c', 0),
    ((624, 662, 706, 686), 'ca. 11,5', (664, 683), 'c', 0),
    ((516, 740, 598, 764), 'ca. 16,7', (556, 761), 'c', 0)])
W6 = F[False].text_length('6-kt. 1,5', fontsize=7.0)
after(5, lambda pg: pg.draw_line((36 + 248 * K - W6, 375 + 308 * K), (36 + 172 * K, 375 + 308 * K), color=NAVY, width=0.3))
D887 = 3.5                                     # Zeichnung 887 etwas tiefer: Abstand Maß ≈18,8 zur Überschrift
b887 = labels(5, (300, 375), [  # 887-4218
    ((568, 66, 632, 88), '≈18,8', (600, 86), 'c', 0),
    ((636, 152, 696, 172), '≈14,3', (666, 171), 'c', 0),
    ((680, 217, 742, 237), '≈11,3', (711, 236), 'c', 0),
    ((186, 180, 258, 213), 'SW 10', (255, 211), 'r', 0),
    ((638, 620, 694, 656), 'SW 8', (693, 645), 'r', 0),
    ((958, 183, 984, 238), '', None, 'l', 0),
    ((936, 262, 964, 452), 'Schlauch AD3', (975, 436), 'l', 90),
    ((1040, 475, 1064, 532), 'Ø 5,8', (1061, 505), 'c', 90),
    ((112, 588, 134, 632), '16,9', (131, 610), 'c', 90),
    ((186, 614, 204, 634), '8', (203, 625), 'c', 90),
    ((186, 748, 204, 765), '1', (203, 757), 'c', 90),
    ((186, 808, 204, 827), '3', (203, 818), 'c', 90),
    ((435, 902, 470, 923), 'M3', (452, 922), 'c', 0),
    ((435, 970, 472, 991), 'Ø 6', (453, 991), 'c', 0)], shift=D887)
R887 = pymupdf.Rect(305, 386, 560, 560)
redact(5, R887, 'artonly')
after(5, copy_paths(5, R887, pymupdf.Matrix(1, 0, 0, 1, 0, D887), keep=lambda d: not any(b.contains((d['rect'].tl + d['rect'].br) / 2) and d['rect'].width < 6 and d['rect'].height < 6 for b in b887))[0])
LOG.append((5, 'Maßzeichnungen 863-4218 / 887-4218: Beschriftung ca. 3,5–4 pt (Kurven), Toleranzen ±0,07 / ±0,1',
            'neu gesetzt in 7 pt, Toleranzen entfernt; „für Schlauch mit Außen-Ø 3“ bzw. „für Schlauch mit AD“ + „3“ → „Schlauch AD3“ (wie S. 4)'))
labels(6, (36, 330), [   # SA2113-1
    ((526, 100, 1040, 130), 'Schiebemuffe beim Verbinden in Pfeilrichtung schieben', (782, 139), 'c', 0),
    ((836, 278, 902, 310), 'SW 10', (898, 308), 'r', 0),
    ((58, 492, 87, 552), 'Ø 11', (84, 522), 'c', 90),
    ((1150, 503, 1176, 542), 'M5', (1173, 522), 'c', 90),
    ((1218, 503, 1243, 542), 'Ø 9', (1240, 522), 'c', 90),
    ((1014, 673, 1052, 695), '4,5', (1033, 693), 'c', 0),
    ((999, 765, 1037, 787), '5,5', (1018, 786), 'c', 0),
    ((622, 854, 672, 876), '30,3', (646, 875), 'c', 0),
    ((98, 660, 133, 918), '', None, 'l', 0)])
# „für Stecknippel SA2113-2“: in 7 pt zu lang für die Senkrechte -> waagerecht am oberen Ende der Bezugslinie
after(6, lambda pg: pg.draw_line((36 + 130 * K, 330 + 390 * K), (36 + 130 * K, 379.5), color=NAVY, width=0.3))
put(6, 61.6, 382.0, 'für Stecknippel', 7.0)
put(6, 61.6, 390.3, 'SA2113-2', 7.0)
labels(6, (300, 330), [  # SA2113-2
    ((26, 98, 61, 338), '', None, 'l', 0),
    ((751, 193, 812, 224), 'SW 10', (810, 221), 'r', 0),
    ((1136, 440, 1158, 478), 'M5', (1157, 458), 'c', 90),
    ((1188, 437, 1210, 480), 'Ø 9', (1209, 458), 'c', 90),
    ((1001, 624, 1039, 645), '4,5', (1020, 643), 'c', 0),
    ((986, 757, 1024, 778), '5,5', (1005, 777), 'c', 0),
    ((254, 757, 302, 778), '12,1', (277, 777), 'c', 0),
    ((568, 867, 616, 888), '33,1', (591, 887), 'c', 0)])
put(6, 312.6, 356.0, 'für Kupplung', 7.0)
put(6, 312.6, 364.4, 'SA2113-1', 7.0)
LOG.append((6, 'Maßzeichnungen SA2113-1 / SA2113-2: Beschriftung ca. 3,5 pt (Kurven), Bezugstexte senkrecht',
            'neu gesetzt in 7 pt; „für Stecknippel SA2113-2“ / „für Kupplung SA2113-1“ waagerecht zweizeilig am Ende der Bezugslinie'))

# ================================================================== SEITE 5: Benennung P15 + Fußnote
bx = find(5, 'PROGRAMM 15')
redact(5, core(bx['bbox'])); put(5, bx['origin'][0], bx['origin'][1], 'PROGRAMM P15', bx['size'], col(bx), True)
LOG.append((5, 'PROGRAMM 15', 'PROGRAMM P15'))
fn5 = find(5, 'Programm 15 mit metrischem und zölligem Gewinde. Länge = Gesamtlänge laut Maßblatt.')
st5 = find(5, '*', near=(47, 631))
FY5 = fn5['origin'][1] - 7.6
for sp in (fn5, st5):
    redact(5, core(sp['bbox']))
put(5, 47.1, FY5, '*', fn5['size'], col(fn5), True)
put(5, 49.7, FY5, ' P15 mit metrischem und zölligem Gewinde. Länge = Gesamtlänge laut Maßblatt.', fn5['size'], col(fn5))
put(5, 47.1, FY5 + 7.6, 'Nennmaße, Toleranzen siehe Maßblatt.', fn5['size'], col(fn5))
LOG.append((5, '* Programm 15 mit metrischem und zölligem Gewinde. …', '* P15 mit metrischem und zölligem Gewinde. …'))
LOG.append((5, '(keine)', 'Fußnote „Nennmaße, Toleranzen siehe Maßblatt.“'))

# ================================================================== SEITE 6: Tabelle 6 pt höher, Fußnote darunter
DY = -6.0
TAB = pymupdf.Rect(40, 497.5, 560, 572.5)
for sp in [s for s in spans(src[5]) if TAB.contains(pymupdf.Rect(s['bbox']))]:
    move_span(6, sp, dy=DY)
rules = [d['rect'] for d in src[5].get_drawings() if d['type'] == 'f' and TAB.contains(d['rect']) and d['rect'].height < 1.5]
redact(6, TAB, 'artonly')


def tab6(pg):
    pg.draw_rect(pymupdf.Rect(58.4, 476.0, 60.5, 495.0), color=None, fill=GREY)  # Bezugslinie kürzen (Abstand Tabellenkopf)
    pg.draw_rect(pymupdf.Rect(0, 573.8, 595.5, 577.2), color=None, fill=GREY)   # Band um 3,4 pt verlängert
    for r in rules:
        pg.draw_rect(r + (0, DY, 0, DY), color=None, fill=NAVY)


after(6, tab6)
put(6, 47.1, 573.4, 'Nennmaße, Toleranzen siehe Maßblatt.', 6.9, NAVY)
LOG.append((6, '(keine)', 'Fußnote „Nennmaße, Toleranzen siehe Maßblatt.“ unter der Tabelle (Tabelle 6 pt höher, graues Band 3,4 pt länger)'))

# ================================================================== SEITE 6: Footer-Logo, „HENN Connector Group“ rot
HENN = pymupdf.Rect(466.0, 799.0, 557.0, 810.0)
henn_draw, henn_ds = copy_paths(6, HENN, pymupdf.Matrix(1, 1), fill=HENN_RED)
assert len(henn_ds) == 17, len(henn_ds)       # 17 Teilflächen wie im Logo auf Seite 1
redact(6, HENN, 'artonly')
after(6, henn_draw)
LOG.append((6, 'Footer-Logo: „HENN Connector Group“ weiß', '„HENN Connector Group“ #FF0000 (EISELE und „Member of“ weiß, Vektor, Geometrie unverändert)'))

# ================================================================== anwenden
MODES = {'text': (pymupdf.PDF_REDACT_IMAGE_NONE, pymupdf.PDF_REDACT_LINE_ART_NONE, pymupdf.PDF_REDACT_TEXT_REMOVE),
         'art': (pymupdf.PDF_REDACT_IMAGE_NONE, pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED, pymupdf.PDF_REDACT_TEXT_REMOVE),
         'artonly': (pymupdf.PDF_REDACT_IMAGE_NONE, pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED, pymupdf.PDF_REDACT_TEXT_NONE),
         'img': (pymupdf.PDF_REDACT_IMAGE_REMOVE, pymupdf.PDF_REDACT_LINE_ART_NONE, pymupdf.PDF_REDACT_TEXT_REMOVE)}
for pno in range(1, len(doc) + 1):
    page = doc[pno - 1]
    for mode in ('text', 'img', 'art', 'artonly'):
        rs = [r for r, m in RED.get(pno, []) if m == mode]
        if not rs:
            continue
        for r in rs:
            page.add_redact_annot(r, fill=False)
        im, ga, tx = MODES[mode]
        page.apply_redactions(images=im, graphics=ga, text=tx)
    for fn in AFTER.get(pno, []):
        fn(page)
    # Reste alter Kurvenbeschriftung, die die Redaction nicht erfasst (Querstrich im „Ø“):
    # innerhalb der Beschriftungsfelder liegen keine Zeichnungslinien, daher mit Bandfarbe abdecken
    for b in LABEL_BOXES.get(pno, []):
        for dr in page.get_drawings():
            r = dr['rect']
            if r.width < 6 and r.height < 6 and b.contains((r.tl + r.br) / 2):
                page.draw_rect(r + (-0.4, -0.4, 0.4, 0.4), color=None, fill=GREY)
    page.insert_font(fontname='hr', fontfile=REG)
    page.insert_font(fontname='hb', fontfile=BOLD)
    for x, y, text, size, color, bold, align, rot in PENDING.get(pno, []):
        w = F[bold].text_length(text, fontsize=size)
        if rot == 90:
            if align == 'c':
                y += w / 2
            page.insert_text((x, y), text, fontname='hb' if bold else 'hr', fontsize=size, color=color, rotate=90)
            continue
        if align == 'c':
            x -= w / 2
        elif align == 'r':
            x -= w
        page.insert_text((x, y), text, fontname='hb' if bold else 'hr', fontsize=size, color=color)

# ================================================================== Produktfotos aus dem Webshop (S. 4, 5)
import io as _io
from PIL import Image as _Image
PROD = os.path.join(HERE, '..', 'infografik', 'produkte')
for pno, near, name in ((4, (394, 123), 'p_vt5528'), (5, (199, 123), 'p_863'), (5, (405, 121), 'p_887')):
    page = doc[pno - 1]
    info = min(page.get_image_info(xrefs=True), key=lambda i: abs(i['bbox'][0] - near[0]) + abs(i['bbox'][1] - near[1]))
    r = pymupdf.Rect(info['bbox'])
    ph = _Image.open(os.path.join(PROD, name + '.png')).convert('RGBA')
    W = int(max(ph.width, ph.height * r.width / r.height) * 1.06)
    H = int(W * r.height / r.width)
    canvas = _Image.new('RGBA', (W, H), (255, 255, 255, 0))
    canvas.alpha_composite(ph, ((W - ph.width) // 2, (H - ph.height) // 2))
    buf = _io.BytesIO(); canvas.save(buf, 'PNG')
    page.replace_image(info['xref'], stream=buf.getvalue())
    LOG.append((pno, f'Produktfoto {name[2:].upper()} (Flyer-Rendering)', 'Produktfoto aus dem EISELE-Webshop (freigestellt)'))

doc.save(out, garbage=3, deflate=True)
with open(os.path.join(HERE, 'aenderungsliste_feinschliff.tsv'), 'w') as f:
    for row in LOG:
        f.write('\t'.join(str(v) for v in row) + '\n')
print('ok', out, len(doc), 'Seiten,', len(LOG), 'Einträge')
