"""Baut den realistischen Humanoid (Flyer-Variante) in Seite 1 des EISELE-Flyers ein.

Aufruf: python3 make_flyer_seite1.py <flyer.pdf> <render.png> <anker.json> <produktbilder_dir> <out.pdf>
"""
import json
import sys

import pikepdf
from PIL import Image
from reportlab.pdfgen import canvas as rl
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

flyer, render, anchors, imgdir, out = sys.argv[1:6]
PW, PH = 594.96, 841.92
LIB = '/usr/share/fonts/truetype/liberation'
pdfmetrics.registerFont(TTFont('H', f'{LIB}/LiberationSans-Regular.ttf'))
pdfmetrics.registerFont(TTFont('HB', f'{LIB}/LiberationSans-Bold.ttf'))


def hx(h, a=1.0):
    return Color(*(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)), alpha=a)


NAVY, GREY_T, LEADER = hx('#0B335E'), hx('#55606E'), hx('#7D8A9C')
BLUE, ORANGE = hx('#2F8CFF'), hx('#FF6A1F')
TILE = hx('#F2F1F0')
Y = lambda y: PH - y
BAND = 424.6                          # Oberkante des grauen Bandes (Programmübersicht)

tmp = out + '.overlay.pdf'
c = rl.Canvas(tmp, pagesize=(PW, PH), initialFontName='H', initialFontSize=8)

# 1) Alten Titelbereich (Badge, Headline, Produktfotos, Roboter) abdecken
c.setFillColor(hx('#FFFFFF')); c.rect(36, Y(BAND), PW - 36, BAND - 100, stroke=0, fill=1)

# 2) Roboter-Render
im = Image.open(render)
RWpx, RHpx = im.size
S = 340 / RHpx
IX, IY = 302, BAND - RHpx * S
im8 = out + '.robot8.png'; im.convert('RGBA').save(im8)
c.drawImage(im8, IX, Y(BAND), RWpx * S, RHpx * S, mask='auto')
A = {k: (IX + x * S, IY + y * S) for k, (x, y) in json.load(open(anchors)).items()}

# 3) Linke Spalte
LX = 47.05
c.setFillColor(NAVY); c.setFont('HB', 19.6)
c.drawString(LX, Y(132), 'EXTREM KLEINBAUEND.')
c.drawString(LX, Y(152), 'KOMPLETTER DURCHFLUSS.')
c.setFillColor(GREY_T); c.setFont('H', 8.2)
c.drawString(LX, Y(169), 'Flüssigkeitskühlung im humanoiden Roboter:')
c.drawString(LX, Y(179), 'EISELE verbindet Kühlwasser, Druckluft und Vakuum.')

# Weg des Kühlwassers als kompakte Zeile
fy = 197
steps = ['Pumpe', 'SA2113', 'VT5528', 'Aktor']
x = LX
c.setFont('HB', 6.8)
pos = []
for i, st in enumerate(steps):
    w = pdfmetrics.stringWidth(st, 'HB', 6.8)
    c.setFillColor(NAVY); c.drawString(x, Y(fy) - 2.3, st)
    pos.append((x, x + w))
    x += w
    if i < len(steps) - 1:
        c.setStrokeColor(BLUE); c.setLineWidth(1.3); c.setLineCap(1)
        c.line(x + 4, Y(fy), x + 20, Y(fy))
        c.setFillColor(BLUE); p = c.beginPath(); p.moveTo(x + 22, Y(fy)); p.lineTo(x + 18, Y(fy) + 2.4)
        p.lineTo(x + 18, Y(fy) - 2.4); p.close(); c.drawPath(p, stroke=0, fill=1)
        x += 26
# Rücklauf-Bogen unter der Zeile
c.setStrokeColor(ORANGE); c.setLineWidth(1.1); c.setDash(2.4, 2)
p = c.beginPath(); p.moveTo(pos[-1][1] - 8, Y(fy + 4)); p.curveTo(pos[-1][1] - 8, Y(fy + 11), pos[-1][1] - 8, Y(fy + 11), pos[-1][1] - 20, Y(fy + 11))
p.lineTo(pos[0][0] + 14, Y(fy + 11)); p.curveTo(pos[0][0] + 8, Y(fy + 11), pos[0][0] + 8, Y(fy + 11), pos[0][0] + 8, Y(fy + 5))
c.drawPath(p, stroke=1, fill=0); c.setDash()
c.setFillColor(ORANGE); p = c.beginPath(); p.moveTo(pos[0][0] + 8, Y(fy + 4)); p.lineTo(pos[0][0] + 5.6, Y(fy + 8))
p.lineTo(pos[0][0] + 10.4, Y(fy + 8)); p.close(); c.drawPath(p, stroke=0, fill=1)
c.setFillColor(ORANGE); c.setFont('H', 5.8); c.drawString(x + 8, Y(fy + 13), 'Rücklauf')

ROWS = [
    ('p_sa2113', 'SA2113-1 / -2', 'Schnellkupplung, tropffrei', 'Armmodul tauschen ohne Medienverlust',
     'Kühlwasser · 0 bis 10 bar · bis +100 °C', 'sa2113'),
    ('p_vt5528', 'VT5528-0202', 'Verschraubung P5500, Aluminium', 'Kühlwasser an die Aktor-Kühlplatte',
     'G1/8 · Schlauch AD4 · ca. 4 g', 'vt5528'),
    ('p_v0129', 'V0129-1850-040601', 'Modulare Schwenkkupplung', 'Vier Kanäle durch das Taillengelenk',
     'Kanäle 1–4 in einem Bauteil', 'v0129'),
    ('p_887', '863-4218 · 887-4218', 'Push-In, Programm 15', 'Druckluft und Vakuum zum Greifer',
     'M3 · Schlauch AD3 · ab ca. 2 g', 'pushin'),
]
for i, (img, code, name, purpose, spec, key) in enumerate(ROWS):
    cy = 240 + i * 45.5
    c.setFillColor(TILE); c.circle(LX + 19, Y(cy), 19, stroke=0, fill=1)
    pim = Image.open(f'{imgdir}/{img}.png'); iw, ih = pim.size
    sc = 28 / max(iw, ih)
    c.drawImage(f'{imgdir}/{img}.png', LX + 19 - iw * sc / 2, Y(cy) - ih * sc / 2, iw * sc, ih * sc, mask='auto')
    tx = LX + 46
    c.setFillColor(NAVY); c.setFont('HB', 8.4); c.drawString(tx, Y(cy - 9), code)
    c.setFillColor(GREY_T); c.setFont('H', 6.4); c.drawString(tx, Y(cy - 0.8), name)
    c.setFillColor(NAVY); c.setFont('HB', 6.9); c.drawString(tx, Y(cy + 7.4), purpose)
    c.setFillColor(GREY_T); c.setFont('H', 6.1); c.drawString(tx, Y(cy + 15), spec)
    ax, ay = A[key]
    sx = 262
    c.setStrokeColor(LEADER); c.setLineWidth(0.55); c.setLineCap(0)
    c.line(sx, Y(cy - 2), ax, Y(ay))
    c.setFillColor(LEADER); c.circle(sx, Y(cy - 2), 1.1, stroke=0, fill=1)
    c.setFillColor(hx('#FFFFFF')); c.setStrokeColor(NAVY); c.setLineWidth(0.8)
    c.circle(ax, Y(ay), 3.0, stroke=1, fill=1)
    c.setFillColor(NAVY); c.circle(ax, Y(ay), 1.2, stroke=0, fill=1)

# Legende + Hinweis
ly = 409
for lab, col, xx in (('Kühlwasser Vorlauf', BLUE, LX), ('Kühlwasser Rücklauf', ORANGE, LX + 84), ('Druckluft / Vakuum', hx('#B9C3CF'), LX + 172)):
    c.setStrokeColor(col); c.setLineWidth(1.8); c.setLineCap(1); c.line(xx, Y(ly), xx + 11, Y(ly))
    c.setFillColor(GREY_T); c.setFont('H', 6.2); c.drawString(xx + 15, Y(ly) - 2.1, lab)
c.setFillColor(hx('#8A94A3')); c.setFont('H', 5.4)
c.drawString(LX, Y(419), 'Konzeptdarstellung, kein reales Robotermodell. Einbauorte beispielhaft, Bauteile vergrößert.')
c.showPage(); c.save()

pdf = pikepdf.open(flyer)
ov = pikepdf.open(tmp)
pdf.pages[0].add_overlay(ov.pages[0])
pdf.docinfo['/Title'] = 'Programm Humanoide Roboter'
pdf.save(out)
print('ok', out)
