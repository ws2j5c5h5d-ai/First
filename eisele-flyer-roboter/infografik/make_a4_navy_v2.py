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
S = 0.45                                    # pt je Pixel im Entwurf (Ausschnitt 1180 x 1024 ab x=270)
RX, RY = 10, 160
OX = 270
c.setFillAlpha(1); c.setStrokeAlpha(1)
c.drawImage(robot, RX, Y(RY + 1024 * S), 1180 * S, 1024 * S, mask='auto')


def R(x, y):
    return RX + (x - OX) * S, RY + y * S


BOT = RY + 1024 * S                         # Unterkante; Ausblendung ist im PNG-Alpha enthalten

# ---------------------------------------------------------------- Kopf
c.setFillColor(LINE); c.rect(32, Y(98), 4, 62, stroke=0, fill=1)
c.setFillColor(WHITE); c.setFont('HB', 25)
c.drawString(46, Y(60), 'PROGRAMM')
c.drawString(46, Y(89), 'HUMANOIDE ROBOTER')
c.setFillColor(SOFT); c.setFont('HB', 11.5)
c.drawString(46, Y(116), 'EXTREM KLEINBAUEND. KOMPLETTER DURCHFLUSS.')
c.setFillColor(WHITE); c.roundRect(405, Y(98), 158, 64, 6, stroke=0, fill=1)


def leader(pts):
    for col, w in ((hx('#071C38', 0.85), 3.4), (LINE, 1.1)):
        c.setStrokeColor(col); c.setLineWidth(w); c.setLineCap(1); c.setLineJoin(1)
        pth = c.beginPath(); pth.moveTo(*[pts[0][0], Y(pts[0][1])])
        for q in pts[1:]:
            pth.lineTo(q[0], Y(q[1]))
        c.drawPath(pth, stroke=1, fill=0)


def marker(x, y):
    c.setFillColor(WHITE); c.setStrokeColor(ACC); c.setLineWidth(1.6); c.circle(x, Y(y), 5.0, stroke=1, fill=1)
    c.setFillColor(ACC); c.circle(x, Y(y), 2.0, stroke=0, fill=1)


def tile(name, cx, cy, r, label):
    c.setFillColor(hx('#FFFFFF', 0.10)); c.circle(cx, Y(cy), r + 4, stroke=0, fill=1)
    c.setFillColor(WHITE); c.setStrokeColor(LINE); c.setLineWidth(0.8); c.circle(cx, Y(cy), r, stroke=1, fill=1)
    pim = Image.open(f'{P}/{name}.png'); iw, ih = pim.size; s = (r * 1.45) / max(iw, ih)
    c.drawImage(f'{P}/{name}.png', cx - iw * s / 2, Y(cy) - ih * s / 2, iw * s, ih * s, mask='auto')
    c.setFillColor(WHITE); c.setFont('HB', 7.4)
    c.drawCentredString(cx, Y(cy + r + 11), label)


TX = 561                                     # rechte Spalte
# Schulter: SA2113 (Inline-Kupplung im Armabgang)
m = R(1205, 345)
tile('p_sa2113', TX, 250, 22, 'SA2113-1'); tile('p_sa2113_2', TX, 326, 22, 'SA2113-2')
leader([(TX - 22, 250), (527, 250), (527, 326), (TX - 22, 326)]); leader([(527, 288), m]); marker(*m)
# Rumpf: VT5528 an der Kühlplatte
m = R(1012, 468)
tile('p_vt5528', TX, 420, 22, 'VT5528-0202'); leader([(TX - 22, 420), (527, 420), m]); marker(*m)
# Taille: VT5528 am unteren Modul
m = R(985, 676)
tile('p_vt5528', TX, 500, 22, 'VT5528-0202'); leader([(TX - 22, 500), (527, 500), m]); marker(*m)
# Hand / Werkzeug: 863, 887, 529 unter der Hand
m1 = R(458, 612)
for i, (nm, lab) in enumerate((('p_863', '863-4218'), ('p_887', '887-4218'), ('p_529', '529-5018G'))):
    tile(nm, 48 + i * 58, 545, 22, lab)
leader([(48, 523), (48, 505), (164, 505), (164, 523)]); leader([(106, 523), (106, 505)]); leader([(106, 505), m1]); marker(*m1)

# Legende
ly = 655
for lab, col, x in (('Kühlwasser Vorlauf', BLUE, 46), ('Kühlwasser Rücklauf', ORANGE, 46)):
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
