"""A4-Hochformat, Navy: Roboter (KI-aufgewertet) + EISELE-Produktfotos an den Einbauorten.
Keine Beschreibungstexte, nur Artikelnummern.

Aufruf: python3 make_a4_navy.py <robot_rgba.png> <produkte_dir> <flyer.pdf> <out.pdf>
"""
import sys

import pikepdf
from PIL import Image
from reportlab.pdfgen import canvas as rl
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

robot, P, flyer, out = sys.argv[1:5]
PW, PH = 595.28, 841.89
LIB = '/usr/share/fonts/truetype/liberation'
pdfmetrics.registerFont(TTFont('H', f'{LIB}/LiberationSans-Regular.ttf'))
pdfmetrics.registerFont(TTFont('HB', f'{LIB}/LiberationSans-Bold.ttf'))


def hx(h, a=1.0):
    return Color(*(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)), alpha=a)


WHITE, SOFT, DIM = hx('#FFFFFF'), hx('#B9CBE2'), hx('#7F95B3')
LINE, ACC = hx('#6FB2FF'), hx('#1F6FD1')
BLUE, ORANGE = hx('#2F8CFF'), hx('#F07A1E')
Y = lambda y: PH - y

tmp = out + '.overlay.pdf'
c = rl.Canvas(tmp, pagesize=(PW, PH), initialFontName='H', initialFontSize=8)
c.setTitle('Programm Humanoide Roboter'); c.setAuthor('EISELE Marketing')

# ---------------------------------------------------------------- Hintergrund
c.saveState(); p = c.beginPath(); p.rect(0, 0, PW, PH); c.clipPath(p, stroke=0)
c.linearGradient(0, PH, 0, 0, (hx('#0D3563'), hx('#0A2A50'), hx('#071C38')), (0, 0.55, 1), extend=True)
c.radialGradient(300, Y(380), 330, (hx('#24578F'), hx('#103866'), hx('#0A2A50'), hx('#08213F')), (0, 0.5, 0.8, 1), extend=True)
c.restoreState()
# feines Punktraster als technische Textur
c.setFillColor(hx('#FFFFFF', 0.05))
for gy in range(150, 700, 14):
    for gx in range(20, 580, 14):
        c.circle(gx, Y(gy), 0.45, stroke=0, fill=1)

# ---------------------------------------------------------------- Roboter
S = 0.548                                   # pt je Entwurfspixel
RX, RY = 120, 148
im = Image.open(robot)
c.setFillAlpha(1); c.setStrokeAlpha(1)
c.drawImage(robot, RX, Y(RY + 1024 * S), 630 * S, 1024 * S, mask='auto')


def R(x, y):
    return RX + (x - 430) * S, RY + y * S


# Bodenausblendung der Beine in den Fußbereich
for k in range(40):                         # Ausblendung per Alpha-Stufen
    y0 = 652 + k * 1.5
    c.setFillColor(hx('#071C38', min(1.0, (k + 1) / 40) ** 1.6)); c.rect(0, Y(y0 + 1.5), PW, 1.6, stroke=0, fill=1)
c.setFillColor(hx('#071C38')); c.rect(0, Y(712), PW, 2, stroke=0, fill=1)

# ---------------------------------------------------------------- Kopf
c.setFillColor(LINE); c.rect(32, Y(98), 4, 62, stroke=0, fill=1)
c.setFillColor(WHITE); c.setFont('HB', 25)
c.drawString(46, Y(60), 'PROGRAMM')
c.drawString(46, Y(89), 'HUMANOIDE ROBOTER')
c.setFillColor(SOFT); c.setFont('HB', 11.5)
c.drawString(46, Y(116), 'EXTREM KLEINBAUEND. KOMPLETTER DURCHFLUSS.')
# Logo-Fläche (Logo wird unten als Vektor eingesetzt)
c.setFillColor(WHITE); c.roundRect(405, Y(98), 158, 64, 6, stroke=0, fill=1)


# ---------------------------------------------------------------- Produkt-Callouts
def leader(pts):
    for col, w in ((hx('#071C38', 0.85), 3.4), (LINE, 1.1)):
        c.setStrokeColor(col); c.setLineWidth(w); c.setLineCap(1); c.setLineJoin(1)
        pth = c.beginPath(); pth.moveTo(*[pts[0][0], Y(pts[0][1])])
        for q in pts[1:]:
            pth.lineTo(q[0], Y(q[1]))
        c.drawPath(pth, stroke=1, fill=0)


def marker(x, y):
    c.setFillColor(WHITE); c.setStrokeColor(ACC); c.setLineWidth(1.6); c.circle(x, Y(y), 5.4, stroke=1, fill=1)
    c.setFillColor(ACC); c.circle(x, Y(y), 2.2, stroke=0, fill=1)


def tile(name, cx, cy, r, label, label_side='below'):
    c.setFillColor(hx('#FFFFFF', 0.10)); c.circle(cx, Y(cy), r + 4, stroke=0, fill=1)
    c.setFillColor(WHITE); c.setStrokeColor(LINE); c.setLineWidth(0.8); c.circle(cx, Y(cy), r, stroke=1, fill=1)
    pim = Image.open(f'{P}/{name}.png'); iw, ih = pim.size; s = (r * 1.45) / max(iw, ih)
    c.drawImage(f'{P}/{name}.png', cx - iw * s / 2, Y(cy) - ih * s / 2, iw * s, ih * s, mask='auto')
    c.setFillColor(WHITE); c.setFont('HB', 7.6)
    c.drawCentredString(cx, Y(cy + r + 12), label)


# Schulter: SA2113
mx, my = R(714, 229)
tile('p_sa2113', 62, 210, 27, 'SA2113-1'); tile('p_sa2113_2', 62, 290, 27, 'SA2113-2')
leader([(89, 210), (110, 210), (mx, my)]); leader([(89, 290), (110, 290), (110, 210)])
marker(mx, my)

# Hand / Werkzeug: 863, 887, 529
h1 = R(463, 505); h2 = R(515, 555)
for i, (nm, lab) in enumerate((('p_863', '863-4218'), ('p_887', '887-4218'), ('p_529', '529-5018G'))):
    cy = 405 + i * 82
    tile(nm, 50, cy, 25, lab)
leader([(75, 405), (95, 405), h1]); leader([(75, 487), (100, 487), (h2[0] - 6, h2[1] + 20), h2])
leader([(75, 569), (100, 569), (100, 487)])
marker(*h1); marker(*h2)

# Rumpf: VT5528
cx_, cy_ = R(812, 275)
tile('p_vt5528', 532, 255, 28, 'VT5528-0202')
leader([(504, 255), (480, 255), (cx_, cy_)]); marker(cx_, cy_)

# Hüfte: VT5528 (verdeckt den Tag aus dem Entwurf)
t0 = R(856, 492); t1 = R(944, 525)
hp1 = R(855, 554); hp2 = R(895, 600)
tile('p_vt5528', 532, 440, 28, 'VT5528-0202')
leader([(504, 440), (480, 440), (t1[0] - 2, (t0[1] + t1[1]) / 2)])
c.setFillColor(ACC); c.roundRect(t0[0] - 1, Y(t1[1] + 1), t1[0] - t0[0] + 2, t1[1] - t0[1] + 2, 3, stroke=0, fill=1)
c.setFillColor(WHITE); c.setFont('HB', 8.2); c.drawCentredString((t0[0] + t1[0]) / 2, Y(t1[1]) + 4.2, 'VT5528')
marker(*hp1); marker(*hp2)

# Legende
ly = 612
for lab, col, x in (('Kühlwasser Vorlauf', BLUE, 430), ('Kühlwasser Rücklauf', ORANGE, 430)):
    yy = ly if col is BLUE else ly + 15
    c.setStrokeColor(col); c.setLineWidth(2.4); c.setLineCap(1); c.line(x, Y(yy), x + 16, Y(yy))
    c.setFillColor(SOFT); c.setFont('H', 7.6); c.drawString(x + 22, Y(yy) - 2.6, lab)

# ---------------------------------------------------------------- Umfeld-Leiste
c.setFillColor(hx('#FFFFFF', 0.06)); c.rect(0, Y(800), PW, 88, stroke=0, fill=1)
c.setStrokeColor(hx('#FFFFFF', 0.18)); c.setLineWidth(0.6); c.line(0, Y(712), PW, Y(712))
c.setFillColor(SOFT); c.setFont('HB', 8.5); c.drawString(46, Y(737), 'IM UMFELD')
c.setFillColor(DIM); c.setFont('H', 7.6); c.drawString(46, Y(749), 'Prüfstand und Fertigung')
for i, (nm, lab) in enumerate((('p_628d', '628D'), ('p_686d', '686D'), ('p_v0129', 'V0129-1850-040601'))):
    tile(nm, 228 + i * 112, 748, 22, lab)

# Fuß
c.setFillColor(WHITE); c.setFont('HB', 8.4); c.drawString(46, Y(823), 'www.eisele-connectors.com')
c.setFillColor(DIM); c.setFont('H', 6.2)
c.drawRightString(PW - 32, Y(823), 'Konzeptdarstellung, KI-gestützte Visualisierung. Einbauorte beispielhaft.')
c.showPage(); c.save()

# ---------------------------------------------------------------- Logo als Vektor
pdf = pikepdf.open(tmp)
fl = pikepdf.open(flyer); pg = fl.pages[0]
LX0, LY0, LX1, LY1 = 405, 30, 560, 86
FH = float(pg.MediaBox[3])
pg.MediaBox = pikepdf.Array([LX0, FH - LY1, LX1, FH - LY0]); pg.CropBox = pg.MediaBox
tw = 138; th = tw * (LY1 - LY0) / (LX1 - LX0)
x0 = 405 + (158 - tw) / 2; ytop = 34 + (64 - th) / 2
pdf.pages[0].add_overlay(pg, pikepdf.Rectangle(x0, PH - ytop - th, x0 + tw, PH - ytop))
pdf.save(out)
print('ok', out)
