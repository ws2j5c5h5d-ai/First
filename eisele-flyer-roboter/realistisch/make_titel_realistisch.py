"""Titelseite: realistischer Humanoid (Cycles-Render) + Kühlkreislauf + EISELE-Produkte.

Aufruf: python3 make_titel_realistisch.py <render.png> <anker.json> <produktbilder_dir> <out.pdf>
"""
import json
import sys

from PIL import Image
from reportlab.pdfgen import canvas as rl
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

render, anchors, imgdir, out = sys.argv[1:5]
PW, PH = 595.28, 841.89
LIB = '/usr/share/fonts/truetype/liberation'
pdfmetrics.registerFont(TTFont('H', f'{LIB}/LiberationSans-Regular.ttf'))
pdfmetrics.registerFont(TTFont('HB', f'{LIB}/LiberationSans-Bold.ttf'))


def hx(h, a=1.0):
    return Color(*(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)), alpha=a)


WHITE, SOFT, DIMT = hx('#FFFFFF'), hx('#C3CEDC'), hx('#8193AB')
BLUE, ORANGE, AIR = hx('#2F8CFF'), hx('#FF6A1F'), hx('#DCE3EC')
LINE = hx('#9FB2CB')
Y = lambda y: PH - y

c = rl.Canvas(out, pagesize=(PW, PH))
c.setTitle('Programm Humanoide Roboter – Kühlkreislauf'); c.setAuthor('EISELE Marketing')

# ---------------------------------------------------------------- Hintergrund
c.saveState()
p = c.beginPath(); p.rect(0, 0, PW, PH); c.clipPath(p, stroke=0)
c.radialGradient(330, Y(380), 640, (hx('#1C4778'), hx('#0C2747'), hx('#06142A')), (0, 0.5, 1), extend=True)
c.restoreState()

# ---------------------------------------------------------------- Roboter
S = 584 / 2550                       # pt pro Renderpixel
IX, IY = 134, 110                    # linke obere Ecke des Renders (pt, von oben)
im = Image.open(render)
im8 = im.convert('RGBA')
tmp = out.replace('.pdf', '_robot8.png'); im8.save(tmp)
c.drawImage(tmp, IX, Y(IY + 2550 * S), 1700 * S, 2550 * S, mask='auto')
A = {k: (IX + x * S, IY + y * S) for k, (x, y) in json.load(open(anchors)).items()}

# ---------------------------------------------------------------- Kopfzeile
LX = 40
c.setFillColor(WHITE); c.setFont('HB', 23)
c.drawString(LX, Y(62), 'PROGRAMM')
c.drawString(LX, Y(88), 'HUMANOIDE ROBOTER')
c.setFillColor(SOFT); c.setFont('H', 9.5)
c.drawString(LX, Y(108), 'Flüssigkeitskühlung, Druckluft und Vakuum: tropffrei verbunden.')
c.setStrokeColor(hx('#FFFFFF', 0.85)); c.setLineWidth(3); c.line(28, Y(40), 28, Y(92))


# ---------------------------------------------------------------- Markierungen am Roboter
def tag(num, key, side, ty, title, sub, img=None):
    ax, ay = A[key]
    tx = 40 if side == 'L' else 452
    tw = 150 if side == 'L' else 112
    # Hinweislinie mit Knick
    ex = tx + tw + 6 if side == 'L' else tx - 6
    kx = ax - 18 if side == 'L' else ax + 18
    c.setStrokeColor(LINE); c.setLineWidth(0.6)
    pth = c.beginPath(); pth.moveTo(ex, Y(ty)); pth.lineTo(kx, Y(ty)); pth.lineTo(ax, Y(ay))
    c.drawPath(pth, stroke=1, fill=0)
    c.setFillColor(WHITE); c.circle(ax, Y(ay), 2.4, stroke=0, fill=1)
    c.setStrokeColor(WHITE); c.setLineWidth(0.7); c.circle(ax, Y(ay), 5.2, stroke=1, fill=0)
    # Nummer
    nx = tx if side == 'L' else tx
    if num == '':
        c.setStrokeColor(WHITE); c.setLineWidth(1); c.circle(nx + 7, Y(ty), 6, stroke=1, fill=0)
    else:
        c.setFillColor(WHITE); c.circle(nx + 7, Y(ty), 7, stroke=0, fill=1)
        c.setFillColor(hx('#0B2545')); c.setFont('HB', 8); c.drawCentredString(nx + 7, Y(ty) - 2.8, str(num))
    c.setFillColor(WHITE); c.setFont('HB', 8.6); c.drawString(nx + 19, Y(ty) - 0.5, title)
    c.setFillColor(SOFT); c.setFont('H', 6.9)
    for i, line in enumerate(sub):
        c.drawString(nx + 19, Y(ty + 10 + i * 8.6), line)


tag(1, 'sa2113', 'L', 232, 'SA2113-1 / -2', ['Tropffreie Schnellkupplung', 'Armmodul tauschen ohne Medienverlust'])
tag(2, 'vt5528', 'L', 322, 'VT5528-0202', ['Einschraubverschraubung, Aluminium', 'Kühlwasser an die Aktor-Kühlplatte'])
tag(3, 'pushin', 'L', 418, '863-4218 · 887-4218', ['Push-In M3, Schlauch AD3', 'Druckluft / Vakuum zum Greifer'])
tag(2, 'knie', 'L', 560, 'VT5528-0202', ['Gleiches Teil am Knieaktor', 'G1/8 · AD4 · ca. 4 g'])
tag(4, 'v0129', 'R', 404, 'V0129-1850-040601', ['Schwenkkupplung, 4 Kanäle', 'Medien durch die Taille'])
tag('', 'pumpe', 'R', 300, 'Pumpe + Verteiler', ['Kühlmodul im Brustraum', 'Start und Ende des Kreislaufs'])

# ---------------------------------------------------------------- Kreislauf-Leiste
BY = 694
c.setFillColor(hx('#FFFFFF', 0.06)); c.roundRect(28, Y(BY + 104), PW - 56, 104, 8, stroke=0, fill=1)
c.setFillColor(SOFT); c.setFont('HB', 7.2); c.drawString(42, Y(BY + 13), 'Der Weg des Kühlwassers')
nodes = [('Pumpe + Verteiler', 'Kühlmodul im Torso', None), ('SA2113', 'Modul tropffrei trennen', 'p_sa2113'),
         ('VT5528', 'Anschluss Kühlplatte', 'p_vt5528'), ('Aktor', 'gibt Wärme ab', None)]
xs = [112, 240, 368, 496]
cy = BY + 40
for i, (x, (t1, t2, img)) in enumerate(zip(xs, nodes)):
    c.setFillColor(hx('#F2F1F0') if img else hx('#FFFFFF', 0.10))
    c.circle(x, Y(cy), 17, stroke=0, fill=1)
    if img:
        pim = Image.open(f'{imgdir}/{img}.png'); iw, ih = pim.size; sc = 25 / max(iw, ih)
        c.drawImage(f'{imgdir}/{img}.png', x - iw * sc / 2, Y(cy) - ih * sc / 2, iw * sc, ih * sc, mask='auto')
    else:
        c.setStrokeColor(WHITE); c.setLineWidth(0.8)
        if i == 0:
            c.circle(x, Y(cy), 8, stroke=1, fill=0)
            for k in range(3):
                c.line(x, Y(cy), x + 7 * [1, -0.5, -0.5][k], Y(cy) + 7 * [0, 0.87, -0.87][k])
        else:
            c.setStrokeColor(ORANGE); c.setLineWidth(1.2)
            for k in range(3):
                c.line(x - 6 + k * 6, Y(cy + 7), x - 6 + k * 6, Y(cy - 7))
    c.setFillColor(WHITE); c.setFont('HB', 7.4); c.drawCentredString(x, Y(cy + 27), t1)
    c.setFillColor(SOFT); c.setFont('H', 6.4); c.drawCentredString(x, Y(cy + 35.5), t2)
# Vorlauf-Pfeile zwischen den Knoten, Rücklauf als Bogen zurück
c.setLineCap(1)
for i in range(len(xs) - 1):
    a, b = xs[i] + 21, xs[i + 1] - 21
    col = BLUE
    c.setStrokeColor(col); c.setLineWidth(1.6); c.line(a, Y(cy), b, Y(cy))
    c.setFillColor(col)
    pth = c.beginPath(); pth.moveTo(b, Y(cy)); pth.lineTo(b - 5, Y(cy) + 3); pth.lineTo(b - 5, Y(cy) - 3); pth.close()
    c.drawPath(pth, stroke=0, fill=1)
c.setStrokeColor(ORANGE); c.setLineWidth(1.2); c.setDash(3, 2.5)
RY2 = cy + 52
pth = c.beginPath(); pth.moveTo(xs[-1] + 19, Y(cy)); pth.curveTo(xs[-1] + 52, Y(cy), xs[-1] + 52, Y(RY2), xs[-1], Y(RY2))
pth.lineTo(xs[0], Y(RY2)); pth.curveTo(xs[0] - 52, Y(RY2), xs[0] - 52, Y(cy), xs[0] - 19, Y(cy))
c.drawPath(pth, stroke=1, fill=0); c.setDash()
c.setFillColor(ORANGE)
pth = c.beginPath(); pth.moveTo(xs[0] - 18.5, Y(cy)); pth.lineTo(xs[0] - 24, Y(cy) + 3); pth.lineTo(xs[0] - 24, Y(cy) - 3); pth.close()
c.drawPath(pth, stroke=0, fill=1)
c.setFillColor(hx('#0E2440')); c.rect((xs[0] + xs[-1]) / 2 - 40, Y(RY2) - 4, 80, 8, stroke=0, fill=1)
c.setFillColor(ORANGE); c.setFont('H', 6.4); c.drawCentredString((xs[0] + xs[-1]) / 2, Y(RY2) - 2.2, 'Rücklauf zur Pumpe')

# ---------------------------------------------------------------- Legende + Fuß
FY = 812
for lab, col, x in (('Kühlwasser Vorlauf', BLUE, 40), ('Kühlwasser Rücklauf', ORANGE, 140), ('Druckluft / Vakuum', AIR, 248)):
    c.setStrokeColor(col); c.setLineWidth(2); c.line(x, Y(FY), x + 14, Y(FY))
    c.setFillColor(SOFT); c.setFont('H', 6.8); c.drawString(x + 19, Y(FY) - 2.3, lab)
c.setFillColor(DIMT); c.setFont('H', 5.9)
c.drawString(40, Y(FY + 13), 'Konzeptdarstellung, kein reales Robotermodell. Einbauorte beispielhaft, Bauteile zur Lesbarkeit vergrößert.')
c.setFillColor(WHITE); c.setFont('HB', 7.4); c.drawRightString(PW - 40, Y(FY), 'www.eisele-connectors.com')
c.setFillColor(DIMT); c.setFont('H', 6.2); c.drawRightString(PW - 40, Y(FY + 13), 'EISELE · Member of HENN Connector Group')

c.showPage(); c.save()
print('ok', out)
