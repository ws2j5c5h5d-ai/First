"""Seite 1 des EISELE-Flyers mit dem bereinigten Roboterbild aus dem Kundenentwurf.

Aufruf: python3 make_flyer_v2.py <flyer.pdf> <robot_rgba.png> <produktbilder_dir> <out.pdf>
"""
import sys

import pikepdf
from PIL import Image, ImageFilter
from reportlab.pdfgen import canvas as rl
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

flyer, robot, imgdir, out = sys.argv[1:5]
PW, PH = 594.96, 841.92
LIB = '/usr/share/fonts/truetype/liberation'
pdfmetrics.registerFont(TTFont('H', f'{LIB}/LiberationSans-Regular.ttf'))
pdfmetrics.registerFont(TTFont('HB', f'{LIB}/LiberationSans-Bold.ttf'))


def hx(h, a=1.0):
    return Color(*(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)), alpha=a)


NAVY, GREY_T, MUTED = hx('#0B335E'), hx('#55606E'), hx('#8A94A3')
BLUE, ORANGE, AIRC = hx('#2F8CFF'), hx('#FF6A1F'), hx('#9AA6B5')
TILE, RULE = hx('#F2F1F0'), hx('#D9DEE4')
Y = lambda y: PH - y
BAND = 424.6

tmp = out + '.overlay.pdf'
c = rl.Canvas(tmp, pagesize=(PW, PH), initialFontName='H', initialFontSize=8)

# 1) Alten Titelbereich abdecken
c.setFillColor(hx('#FFFFFF')); c.rect(36, Y(BAND), PW - 36, BAND - 100, stroke=0, fill=1)

# 2) Roboter (Real-ESRGAN-aufgewertet, 2x der Originalauflösung)
im = Image.open(robot).convert('RGBA')
ORIG_W = 1210                             # Breite des Ausgangsbilds in px
S0 = 0.28                                 # pt pro Ausgangspixel
S = S0 * ORIG_W / im.width                # pt pro Pixel der aufgewerteten Datei
IX, IY = 266, BAND - im.height * S
c.drawImage(robot, IX, Y(BAND), im.width * S, im.height * S, mask='auto')


def P(cx, cy):
    return IX + cx * S0, IY + cy * S0


# 3) Linke Spalte
LX = 47.05
c.setFillColor(NAVY); c.setFont('HB', 19.6)
c.drawString(LX, Y(134), 'EXTREM KLEINBAUEND.')
c.drawString(LX, Y(154), 'KOMPLETTER DURCHFLUSS.')
c.setFillColor(GREY_T); c.setFont('H', 8.2)
c.drawString(LX, Y(171), 'Flüssigkeitskühlung im humanoiden Roboter:')
c.drawString(LX, Y(181), 'EISELE verbindet Kühlwasser, Druckluft und Vakuum.')

# Weg des Kühlwassers
fy = 199
x = LX; pos = []
for i, st in enumerate(['Pumpe', 'SA2113', 'VT5528', 'Aktor / Kühlplatte']):
    c.setFillColor(NAVY); c.setFont('HB', 6.9); c.drawString(x, Y(fy) - 2.4, st)
    w = pdfmetrics.stringWidth(st, 'HB', 6.9); pos.append((x, x + w)); x += w
    if i < 3:
        c.setStrokeColor(BLUE); c.setLineWidth(1.3); c.setLineCap(1); c.line(x + 4, Y(fy), x + 19, Y(fy))
        c.setFillColor(BLUE); p = c.beginPath(); p.moveTo(x + 21.5, Y(fy)); p.lineTo(x + 17, Y(fy) + 2.5)
        p.lineTo(x + 17, Y(fy) - 2.5); p.close(); c.drawPath(p, stroke=0, fill=1); x += 26
xa, xb = pos[0][0] + 9, pos[-1][1] - 30
c.setStrokeColor(ORANGE); c.setLineWidth(1.1); c.setDash(2.4, 2)
p = c.beginPath(); p.moveTo(xb, Y(fy + 4.5)); p.lineTo(xb, Y(fy + 11)); p.lineTo(xa, Y(fy + 11)); p.lineTo(xa, Y(fy + 6))
c.drawPath(p, stroke=1, fill=0); c.setDash()
c.setFillColor(ORANGE); p = c.beginPath(); p.moveTo(xa, Y(fy + 4.2)); p.lineTo(xa - 2.4, Y(fy + 8.4)); p.lineTo(xa + 2.4, Y(fy + 8.4)); p.close()
c.drawPath(p, stroke=0, fill=1)
c.setFont('H', 5.9); c.drawString(xb + 4, Y(fy + 13), 'Rücklauf')
c.setStrokeColor(RULE); c.setLineWidth(0.5); c.line(LX, Y(219), 262, Y(219))


def leader(pts, ax, ay):
    for col, wdt in ((hx('#FFFFFF', 0.9), 1.9), (NAVY, 0.6)):
        c.setStrokeColor(col); c.setLineWidth(wdt); c.setLineCap(1); c.setLineJoin(1)
        pth = c.beginPath(); pth.moveTo(*[pts[0][0], Y(pts[0][1])])
        for q in pts[1:] + [(ax, ay)]:
            pth.lineTo(q[0], Y(q[1]))
        c.drawPath(pth, stroke=1, fill=0)
    c.setFillColor(NAVY); c.circle(pts[0][0], Y(pts[0][1]), 1.3, stroke=0, fill=1)
    c.setFillColor(hx('#FFFFFF')); c.setStrokeColor(NAVY); c.setLineWidth(0.9)
    c.circle(ax, Y(ay), 3.3, stroke=1, fill=1)
    c.setFillColor(BLUE); c.circle(ax, Y(ay), 1.4, stroke=0, fill=1)


ROWS = [
    ('p_sa2113', 'SA2113-1 / SA2113-2', 'Tropffreie Kühlwasser-Modulschnittstelle',
     ['Schulter-/Armmodul oder Wartungsport · NW 2,5'], P(880, 380), [(262, 233), (300, 233), (372, 204), (470, 204)]),
    ('p_vt5528', 'VT5528-0202', 'Aluminium-Anschluss · G1/8 · Schlauch AD4',
     ['Für Kühlplatten an Aktor oder Elektronik'], P(585, 522), [(262, 274)]),
    ('p_887', '863-4218 · 887-4218 · 529-5018G', 'Push-In / Einschraubanschluss am Greifer',
     ['Druckluft und Vakuum (863 / 887) · M3 / M5 · AD3', '887 schwenkbar, nicht für Dauerschwenkbewegung'], P(95, 1062), [(262, 315), (272, 315)]),
]
for i, (img, code, l1, l2, (ax, ay), path) in enumerate(ROWS):
    cy = 240 + i * 41
    c.setFillColor(TILE); c.circle(LX + 17, Y(cy), 17, stroke=0, fill=1)
    pim = Image.open(f'{imgdir}/{img}.png'); iw, ih = pim.size; sc = 25 / max(iw, ih)
    c.drawImage(f'{imgdir}/{img}.png', LX + 17 - iw * sc / 2, Y(cy) - ih * sc / 2, iw * sc, ih * sc, mask='auto')
    tx = LX + 41
    c.setFillColor(NAVY); c.setFont('HB', 8.4); c.drawString(tx, Y(cy - 7.5), code)
    c.setFillColor(NAVY); c.setFont('H', 6.9); c.drawString(tx, Y(cy + 1.2), l1)
    c.setFillColor(GREY_T); c.setFont('H', 6.1)
    for k, t in enumerate(l2):
        c.drawString(tx, Y(cy + 9.4 + k * 7.4), t)
    leader(path, ax, ay)

# Legende
ly = 368
for lab, col, xx, dash in (('Kühlwasser Vorlauf', BLUE, LX, None), ('Rücklauf', ORANGE, LX + 78, None), ('Druckluft / Vakuum', AIRC, LX + 128, (1.2, 1.8))):
    c.setStrokeColor(col); c.setLineWidth(1.8); c.setLineCap(0)
    if dash:
        c.setDash(*dash)
    c.line(xx, Y(ly), xx + 11, Y(ly)); c.setDash()
    c.setFillColor(GREY_T); c.setFont('H', 6.1); c.drawString(xx + 15, Y(ly) - 2.1, lab)

# Im Umfeld (nicht im Roboterkörper)
c.setStrokeColor(RULE); c.setLineWidth(0.5); c.line(LX, Y(377), 262, Y(377))
c.setFillColor(NAVY); c.setFont('HB', 6.2); c.drawString(LX, Y(387), 'IM UMFELD DES ROBOTERS')
for j, (img, code, d1, d2) in enumerate((('p_v0129', 'V0129-1850-040601', '4-Kanal-Multikupplung für', 'Flansch- und Werkzeugwechsel'),
                                         (None, '628D / 686D', 'Drehanschlüsse für Dreh-', 'und Prüfstände, bis 800 U/min'))):
    bx = LX + j * 110
    c.setFillColor(TILE); c.circle(bx + 10, Y(403), 10, stroke=0, fill=1)
    if img:
        pim = Image.open(f'{imgdir}/{img}.png'); iw, ih = pim.size; sc = 15 / max(iw, ih)
        c.drawImage(f'{imgdir}/{img}.png', bx + 10 - iw * sc / 2, Y(403) - ih * sc / 2, iw * sc, ih * sc, mask='auto')
    else:
        pim = Image.open(f'{imgdir}/p_628d.png'); iw, ih = pim.size; sc = 15 / max(iw, ih)
        c.drawImage(f'{imgdir}/p_628d.png', bx + 10 - iw * sc / 2, Y(403) - ih * sc / 2, iw * sc, ih * sc, mask='auto')
    c.setFillColor(NAVY); c.setFont('HB', 6.6); c.drawString(bx + 24, Y(398.5), code)
    c.setFillColor(GREY_T); c.setFont('H', 5.7)
    c.drawString(bx + 24, Y(405.5), d1); c.drawString(bx + 24, Y(412), d2)
c.setFillColor(MUTED); c.setFont('H', 5.0)
c.drawString(LX, Y(420.5), 'Konzeptdarstellung, KI-gestützte Visualisierung. Einbauorte beispielhaft, keine Kundenreferenz.')
c.showPage(); c.save()

pdf = pikepdf.open(flyer)
ov = pikepdf.open(tmp)
pdf.pages[0].add_overlay(ov.pages[0])
pdf.docinfo['/Title'] = 'Programm Humanoide Roboter'
pdf.save(out)
print('ok', out)
