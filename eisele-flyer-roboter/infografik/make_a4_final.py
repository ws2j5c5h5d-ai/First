"""A4 Navy, Phantom-Roboter (Bild 2, bereinigt + Real-ESRGAN) als vollflächiger Hintergrund,
dazu EISELE-Produktfotos an den Einbauorten (nur Artikelnummern) und Vektor-Logo.

Aufruf: python3 make_a4_phantom.py <hintergrund_x4.png> <produkte_dir> <flyer.pdf> <out.pdf>
"""
import sys

import pikepdf
from PIL import Image
from reportlab.pdfgen import canvas as rl
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

bgimg, P, flyer, out = sys.argv[1:5]
PW, PH = 595.28, 841.89
LIB = '/usr/share/fonts/truetype/liberation'
pdfmetrics.registerFont(TTFont('H', f'{LIB}/LiberationSans-Regular.ttf'))
pdfmetrics.registerFont(TTFont('HB', f'{LIB}/LiberationSans-Bold.ttf'))


def hx(h, a=1.0):
    return Color(*(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)), alpha=a)


WHITE, SOFT, DIM = hx('#FFFFFF'), hx('#B9CBE2'), hx('#8299B6')
LINE, ACC = hx('#7FBCFF'), hx('#1F6FD1')
BLUE, ORANGE, AIR = hx('#2F8CFF'), hx('#F07A1E'), hx('#E6ECF4')
Y = lambda y: PH - y

tmp = out + '.overlay.pdf'
c = rl.Canvas(tmp, pagesize=(PW, PH), initialFontName='H', initialFontSize=8)
c.setTitle('Programm Humanoide Roboter'); c.setAuthor('EISELE Marketing')

# ---------------------------------------------------------------- Bild (Entwurf 1112 x 1415 px)
S = 0.60                                      # pt je Pixel im Gemini-Bild (765 x 1024)
OX, OY = 80.0, 101.0                           # Lage des Entwurfs-Ursprungs auf der Seite (pt, von oben)
# Bild ist bereits auf die volle Seite erweitert (pad_page.py): Seite = Bild
c.setFillAlpha(1)
c.drawImage(bgimg, 0, 0, PW, PH)


def R(x, y):
    return OX + x * S, OY + y * S


# ---------------------------------------------------------------- Kopf
c.setFillColor(WHITE); c.rect(32, Y(98), 4, 62, stroke=0, fill=1)
c.setFont('HB', 25)
c.drawString(46, Y(60), 'PROGRAMM')
c.drawString(46, Y(89), 'HUMANOIDE ROBOTER')
c.setFillColor(SOFT); c.setFont('HB', 11.5)
c.drawString(46, Y(116), 'EXTREM KLEINBAUEND. AB M3 UND AD3.')
c.setFillColor(WHITE); c.roundRect(452, Y(84), 112, 50, 5, stroke=0, fill=1)


def leader(pts):
    for col, w in ((hx('#06162C', 0.85), 3.2), (LINE, 1.0)):
        c.setStrokeColor(col); c.setLineWidth(w); c.setLineCap(1); c.setLineJoin(1)
        pth = c.beginPath(); pth.moveTo(pts[0][0], Y(pts[0][1]))
        for q in pts[1:]:
            pth.lineTo(q[0], Y(q[1]))
        c.drawPath(pth, stroke=1, fill=0)


def marker(x, y):
    c.setFillColor(WHITE); c.setStrokeColor(ACC); c.setLineWidth(1.5); c.circle(x, Y(y), 4.6, stroke=1, fill=1)
    c.setFillColor(ACC); c.circle(x, Y(y), 1.9, stroke=0, fill=1)


def tile(name, cx, cy, r, label):
    c.setFillColor(hx('#FFFFFF', 0.10)); c.circle(cx, Y(cy), r + 4, stroke=0, fill=1)
    c.setFillColor(WHITE); c.setStrokeColor(LINE); c.setLineWidth(0.8); c.circle(cx, Y(cy), r, stroke=1, fill=1)
    pim = Image.open(f'{P}/{name}.png'); iw, ih = pim.size; s = (r * 1.45) / max(iw, ih)
    c.drawImage(f'{P}/{name}.png', cx - iw * s / 2, Y(cy) - ih * s / 2, iw * s, ih * s, mask='auto')
    c.setFillColor(WHITE); c.setFont('HB', 7.3)
    c.drawCentredString(cx, Y(cy + r + 11), label)


TX = 561
# Brust: VT5528 an den Anschlüssen des Kühlmoduls
m = R(523, 350)
tile('p_vt5528', TX, 205, 21, 'VT5528-0202'); leader([(TX - 21, 205), (531, 205), m]); marker(*m)
# Modulschnittstelle Rumpf/Becken: SA2113 (tropffrei trennen)
m = R(528, 438)
tile('p_sa2113', TX, 285, 21, 'SA2113-1'); tile('p_sa2113_2', TX, 357, 21, 'SA2113-2')
leader([(TX - 21, 285), (531, 285), (531, 357), (TX - 21, 357)]); leader([(531, 321), m]); marker(*m)
# Hüfte + Knie: VT5528 an den Aktor-Kühlringen
mh = R(568, 518); mk = R(468, 700)
tile('p_vt5528', TX, 455, 21, 'VT5528-0202')
leader([(TX - 21, 455), (531, 455), mh]); leader([(531, 455), (531, 520), mk]); marker(*mh); marker(*mk)
# Hand / Greifer
m = R(171, 426)
for i, (nm, lab) in enumerate((('p_863', '863-4218'), ('p_887', '887-4218'), ('p_529', '529-5018G'))):
    tile(nm, 50 + i * 58, 512, 21, lab)
leader([(50, 491), (50, 474), (166, 474), (166, 491)]); leader([(108, 491), (108, 474)]); leader([(108, 474), m]); marker(*m)

# Legende
for i, (lab, col) in enumerate((('Kühlwasser Vorlauf', BLUE), ('Kühlwasser Rücklauf', ORANGE), ('Druckluft / Vakuum', AIR))):
    yy = 600 + i * 15
    c.setStrokeColor(col); c.setLineWidth(2.4); c.setLineCap(1); c.line(46, Y(yy), 62, Y(yy))
    c.setFillColor(SOFT); c.setFont('H', 7.6); c.drawString(68, Y(yy) - 2.6, lab)

# ---------------------------------------------------------------- Umfeld-Leiste + Fuß
c.setFillColor(hx('#061A33', 0.88)); c.rect(0, Y(800), PW, 88, stroke=0, fill=1)
c.setStrokeColor(hx('#FFFFFF', 0.18)); c.setLineWidth(0.6); c.line(0, Y(712), PW, Y(712))
c.setFillColor(SOFT); c.setFont('HB', 8.5); c.drawString(46, Y(737), 'IM UMFELD')
c.setFillColor(DIM); c.setFont('H', 7.6); c.drawString(46, Y(749), 'Prüfstand und Fertigung')
for i, (nm, lab) in enumerate((('p_628d', '628D'), ('p_686d', '686D'), ('p_v0129', 'V0129-1850-040601'))):
    tile(nm, 228 + i * 112, 748, 22, lab)
c.setFillColor(hx('#05152A')); c.rect(0, 0, PW, PH - 800, stroke=0, fill=1)
c.setFillColor(WHITE); c.setFont('HB', 8.4); c.drawString(46, Y(823), 'www.eisele-connectors.com')
c.setFillColor(DIM); c.setFont('H', 6.2)
c.drawRightString(PW - 32, Y(818), 'Konzeptdarstellung, KI-gestützte Visualisierung. Einbauorte beispielhaft.')
c.drawRightString(PW - 32, Y(827), 'Abbildungen unverbindlich, Änderungen vorbehalten, für Irrtümer und Druckfehler keine Haftung – 10.26')
c.showPage(); c.save()

# ---------------------------------------------------------------- Logo (Vektor)
pdf = pikepdf.open(tmp)
fl = pikepdf.open(flyer); pg = fl.pages[0]
LX0, LY0, LX1, LY1 = 405, 30, 560, 86
FH = float(pg.MediaBox[3])
pg.MediaBox = pikepdf.Array([LX0, FH - LY1, LX1, FH - LY0]); pg.CropBox = pg.MediaBox
tw = 98; th = tw * (LY1 - LY0) / (LX1 - LX0)
x0 = 452 + (112 - tw) / 2; ytop = 34 + (50 - th) / 2
pdf.pages[0].add_overlay(pg, pikepdf.Rectangle(x0, PH - ytop - th, x0 + tw, PH - ytop))
pdf.save(out)
print('ok', out)
