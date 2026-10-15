"""Infografik 'Programm Humanoide Roboter' (Querformat 3:2) nach Kundenentwurf.

Roboter: aus dem Entwurf, Real-ESRGAN x4 aufgewertet und freigestellt.
Alles andere (Texte, Karten, Linien, Logo, Produktfotos) ist neu als Vektor bzw.
mit den originalen EISELE-Produktfotos aufgebaut. Produktdaten laut EISELE-Flyer.

Aufruf: python3 make_infografik.py <robot_rgba.png> <inset.png> <produktbilder_dir> <flyer.pdf> <out.pdf>
"""
import sys

import pikepdf
from PIL import Image
from reportlab.pdfgen import canvas as rl
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

robot, inset, P, flyer, out = sys.argv[1:6]
K = 0.5625                                   # pt je Entwurfspixel (1536 x 1024 -> 864 x 576 pt)
PW, PH = 1536 * K, 1024 * K
LIB = '/usr/share/fonts/truetype/liberation'
pdfmetrics.registerFont(TTFont('H', f'{LIB}/LiberationSans-Regular.ttf'))
pdfmetrics.registerFont(TTFont('HB', f'{LIB}/LiberationSans-Bold.ttf'))


def hx(h, a=1.0):
    return Color(*(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)), alpha=a)


NAVY, TXT, MUTE = hx('#0B335E'), hx('#3E4A59'), hx('#6B7684')
ACC = hx('#1F6FD1')                          # Linien, Tags
BLUE, ORANGE, AIR, VAC = hx('#1F6FD1'), hx('#F07A1E'), hx('#33B5E5'), hx('#9AA5B4')
CARD_LINE, TILE = hx('#CFDCEA'), hx('#F1F3F5')
BG = hx('#F8F9FA')

tmp = out + '.overlay.pdf'
c = rl.Canvas(tmp, pagesize=(PW, PH), initialFontName='H', initialFontSize=8)
c.setTitle('Programm Humanoide Roboter – Infografik'); c.setAuthor('EISELE Marketing')


def X(x): return x * K
def Y(y): return PH - y * K


def text(x, y, s, font='H', size=11, col=TXT, anchor='l'):
    c.setFillColor(col); c.setFont(font, size * K)
    if anchor == 'r':
        c.drawRightString(X(x), Y(y), s)
    elif anchor == 'c':
        c.drawCentredString(X(x), Y(y), s)
    else:
        c.drawString(X(x), Y(y), s)


def card(x0, y0, x1, y1, title, sub):
    c.setFillColor(hx('#FFFFFF')); c.setStrokeColor(CARD_LINE); c.setLineWidth(1.1 * K)
    c.roundRect(X(x0), Y(y1), X(x1 - x0), X(y1 - y0), 7 * K, stroke=1, fill=1)
    text(x0 + 14, y0 + 22, title, 'HB', 14.5, NAVY)
    text(x0 + 14, y0 + 41, sub, 'H', 13.5, ACC)


def photo(name, cx, cy, r=34, fit=50):
    c.setFillColor(TILE); c.circle(X(cx), Y(cy), r * K, stroke=0, fill=1)
    im = Image.open(f'{P}/{name}.png'); iw, ih = im.size; s = fit / max(iw, ih)
    c.drawImage(f'{P}/{name}.png', X(cx - iw * s / 2), Y(cy + ih * s / 2), iw * s * K, ih * s * K, mask='auto')


def item(x, y, code, lines, bold_first=None):
    text(x, y, code, 'HB', 14.5, NAVY)
    for i, ln in enumerate(lines):
        text(x, y + 17 + i * 16, ln, 'H', 11.6, TXT if i == 0 else MUTE)


def leader(pts, end_marker=True, dot_start=False):
    for col, w in ((hx('#FFFFFF', 0.95), 6.0), (ACC, 2.0)):
        c.setStrokeColor(col); c.setLineWidth(w * K); c.setLineCap(1); c.setLineJoin(1)
        p = c.beginPath(); p.moveTo(X(pts[0][0]), Y(pts[0][1]))
        for q in pts[1:]:
            p.lineTo(X(q[0]), Y(q[1]))
        c.drawPath(p, stroke=1, fill=0)
    if end_marker:
        marker(*pts[-1])
    if dot_start:
        c.setFillColor(ACC); c.circle(X(pts[0][0]), Y(pts[0][1]), 3 * K, stroke=0, fill=1)


def marker(x, y, r=9.5):
    c.setFillColor(hx('#FFFFFF')); c.setStrokeColor(ACC); c.setLineWidth(2.6 * K)
    c.circle(X(x), Y(y), r * K, stroke=1, fill=1)
    c.setFillColor(ACC); c.circle(X(x), Y(y), r * 0.42 * K, stroke=0, fill=1)


def tag(x0, y0, x1, y1, s):
    c.setFillColor(ACC); c.roundRect(X(x0), Y(y1), X(x1 - x0), X(y1 - y0), 5 * K, stroke=0, fill=1)
    text((x0 + x1) / 2, y1 - 7.5, s, 'HB', 15, hx('#FFFFFF'), 'c')


# --------------------------------------------------------------- Hintergrund
c.setFillColor(hx('#FFFFFF')); c.rect(0, 0, PW, PH, stroke=0, fill=1)
c.saveState()
pth = c.beginPath(); pth.rect(0, 0, PW, PH); c.clipPath(pth, stroke=0)
c.radialGradient(X(745), Y(520), 620 * K, (hx('#EDF1F5'), hx('#F7F9FB'), hx('#FFFFFF')), (0, 0.5, 1), extend=True)
c.restoreState()

# --------------------------------------------------------------- Roboter
RX0, RW_, RH_ = 430, 630, 1024
c.drawImage(robot, X(RX0), Y(RH_), RW_ * K, RH_ * K, mask='auto')

# Detail Rumpf (Einschub)
c.setFillColor(hx('#FFFFFF')); c.setStrokeColor(CARD_LINE); c.setLineWidth(1.1 * K)
c.roundRect(X(551), Y(770), X(186), X(223), 7 * K, stroke=1, fill=1)
c.saveState(); p = c.beginPath(); p.roundRect(X(558), Y(702), X(172), X(146), 5 * K); c.clipPath(p, stroke=0)
c.drawImage(inset, X(558), Y(702), 172 * K, 146 * K); c.restoreState()
text(560, 722, 'Detail Rumpf', 'HB', 13, NAVY)
text(560, 740, 'Kühlplatte mit VT5528', 'H', 11.5, MUTE)
text(560, 756, '(Aluminium)', 'H', 11.5, MUTE)

# --------------------------------------------------------------- Kopfzeile
c.setFillColor(NAVY); c.rect(X(28), Y(98), 6 * K, 76 * K, stroke=0, fill=1)
text(60, 55, 'PROGRAMM', 'HB', 41, NAVY)
text(60, 95, 'HUMANOIDE ROBOTER', 'HB', 41, NAVY)
text(60, 142, 'EXTREM KLEINBAUEND.', 'HB', 29, NAVY)
text(60, 174, 'KOMPLETTER DURCHFLUSS.', 'HB', 29, NAVY)
text(60, 203, 'Flüssigkeitskühlung im humanoiden Roboter:', 'H', 16, TXT)
text(60, 224, 'EISELE verbindet Kühlwasser, Druckluft und Vakuum.', 'H', 16, TXT)

# --------------------------------------------------------------- Linke Karten
card(30, 246, 410, 388, 'SCHULTER / ARMMODUL', 'Kühlwasser')
photo('p_sa2113', 70, 330, 30, 46); photo('p_sa2113_2', 128, 330, 30, 46)
item(170, 306, 'SA2113-1 / -2', ['Schnellkupplung + Stecknippel, tropffrei', 'Modulschnittstelle im Kühlkreis', '0 – 10 bar · 0 bis +100 °C · M5 · NW 2,5'])

card(30, 402, 410, 676, 'HAND / WERKZEUG', 'Druckluft & Vakuum')
photo('p_863', 82, 482); item(150, 466, '863-4218', ['Push-In gerade, Programm 15', 'M3 · Schlauch AD3 · ca. 2 g'])
photo('p_887', 82, 560); item(150, 544, '887-4218', ['Push-In Winkel, schwenkbar', 'M3 · AD3 · ca. 9 g · −0,95 bis 15 bar', 'nicht für Dauerschwenkbewegungen'])
photo('p_529', 82, 636); item(150, 624, '529-5018G', ['Einschraubverschraubung gerade, P12', 'M5 · Schlauch AD3 · ca. 5 g'])

card(30, 690, 410, 958, 'IM UMFELD: PRÜFSTAND / FERTIGUNG', 'Druckluft / Vakuum')
photo('p_628d', 82, 772); item(150, 752, '628D / 686D', ['Drehanschluss gerade / Winkel', 'bis 800 U/min · −0,9 bis 16 bar', 'G1/4 · Schlauch AD8 bis AD12'])
photo('p_v0129', 82, 880); item(150, 862, 'V0129-1850-040601', ['Modulare Schwenkkupplung', 'Kanäle 1–4 in einem Bauteil', 'Daten auf Anfrage'])

# --------------------------------------------------------------- Rechte Karten
card(1052, 140, 1345, 292, 'RUMPF / RECHNER & ELEKTRONIK', 'Kühlwasser')
photo('p_vt5528', 1102, 232); item(1156, 206, 'VT5528-0202', ['Verschraubung P5500, Aluminium', 'Anschluss an Kühlplatten', 'G1/8 · Schlauch AD4 · ca. 4 g'])

card(1052, 350, 1240, 578, 'HÜFTE / KNIE', 'Kühlwasser')
photo('p_vt5528', 1104, 450)
item(1066, 512, 'VT5528-0202', ['Ein- und Auslauf', 'am Aktor-Kühlring', 'Dichtung FPM'])

# Legende
for i, (lab, col, dash) in enumerate((('Kühlwasser Vorlauf', BLUE, None), ('Kühlwasser Rücklauf', ORANGE, None),
                                       ('Druckluft', AIR, None), ('Vakuum', VAC, (4, 3)))):
    y = 200 + i * 29
    c.setStrokeColor(col); c.setLineWidth(4.5 * K); c.setLineCap(1)
    if dash:
        c.setDash(dash[0] * K, dash[1] * K); c.setLineCap(0)
    c.line(X(1362), Y(y), X(1390), Y(y)); c.setDash()
    text(1400, y + 4.5, lab, 'H', 12.5, TXT)

# Anwendungsbereiche
text(1262, 372, 'ANWENDUNGSBEREICHE', 'HB', 15, NAVY)
c.setStrokeColor(CARD_LINE); c.setLineWidth(1.2 * K); c.line(X(1262), Y(383), X(1505), Y(383))
AB = [('Modulschnittstelle Schulter / Arm', 'Tropffreies Trennen ohne Entleeren', 'SA2113'),
      ('Rechner / Elektronik im Rumpf', 'Kühlplatten für Elektronik', 'VT5528'),
      ('Hüfte / Knie', 'Aktor-Kühlkreise', 'VT5528'),
      ('Hand / Werkzeug', 'Greifer, Sauger, Werkzeugwechsel', '863 · 887 · 529'),
      ('Drehanschlüsse', 'Prüfstand und Fertigung', '628D · 686D')]
for i, (t1, t2, ref) in enumerate(AB):
    y = 412 + i * 61
    c.setFillColor(hx('#E7EEF7')); c.circle(X(1280), Y(y + 4), 17 * K, stroke=0, fill=1)
    text(1280, y + 9.5, str(i + 1), 'HB', 14, ACC, 'c')
    text(1310, y + 2, t1, 'HB', 12.8, NAVY)
    text(1310, y + 20, t2, 'H', 11.6, MUTE)
    text(1310, y + 36, ref, 'H', 10.5, ACC)

# Banner
c.setFillColor(NAVY)
p = c.beginPath(); p.moveTo(X(1130), Y(770)); p.lineTo(X(1536), Y(770)); p.lineTo(X(1536), Y(915)); p.lineTo(X(1056), Y(915)); p.close()
c.drawPath(p, stroke=0, fill=1)
text(1180, 812, 'KOMPAKTE LÖSUNGEN.', 'HB', 21, hx('#FFFFFF'))
text(1180, 840, 'TROPFFREI VERBUNDEN.', 'HB', 21, hx('#FFFFFF'))
text(1180, 874, 'EISELE – für die nächste Generation', 'H', 16, hx('#DCE6F2'))
text(1180, 896, 'humanoider Roboter.', 'H', 16, hx('#DCE6F2'))

# Fußzeile
text(32, 988, 'Konzeptdarstellung, KI-gestützte Visualisierung. Einbauorte beispielhaft. Daten laut EISELE-Datenblättern.', 'H', 11, MUTE)
text(1505, 988, 'www.eisele-connectors.com', 'HB', 12.5, NAVY, 'r')

# --------------------------------------------------------------- Linien + Tags am Roboter
# Geometrie deckungsgleich mit den Linien im Entwurf (überdeckt sie)
leader([(410, 268), (530, 268), (677, 216)], end_marker=False)
c.setFillColor(ACC); c.circle(X(677), Y(216), 4 * K, stroke=0, fill=1)
leader([(702, 192), (714, 229)])
tag(632, 168, 708, 200, 'SA2113')

leader([(926, 186), (812, 275)])
tag(930, 150, 1006, 182, 'VT5528')
leader([(1052, 225), (944, 225)])

leader([(384, 438), (430, 438), (463, 505)])
leader([(552, 523), (515, 555)])
tag(532, 498, 652, 530, '863 / 887 / 529')

leader([(1052, 438), (1040, 438), (1040, 448), (942, 507)], end_marker=False)
leader([(880, 522), (855, 554)])
leader([(855, 554), (890, 554), (895, 600)])
tag(856, 492, 944, 525, 'VT5528')
c.showPage(); c.save()

# --------------------------------------------------------------- Logo (Vektor aus dem Flyer)
pdf = pikepdf.open(tmp)
fl = pikepdf.open(flyer)
pg = fl.pages[0]
LX0, LY0, LX1, LY1 = 405, 30, 560, 86                  # Logo-Box im Flyer (pt, von oben)
FH = float(pg.MediaBox[3])
pg.MediaBox = pikepdf.Array([LX0, FH - LY1, LX1, FH - LY0])
pg.CropBox = pg.MediaBox
tw = 305 * K
th = tw * (LY1 - LY0) / (LX1 - LX0)
pdf.pages[0].add_overlay(pg, pikepdf.Rectangle(X(1200), Y(22) - th, X(1200) + tw, Y(22)))
pdf.save(out)
print('ok', out)
