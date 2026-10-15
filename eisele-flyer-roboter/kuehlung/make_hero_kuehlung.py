"""Seite 1 des Flyers 'Programm Humanoide Roboter' mit Kühlkreis-Overlay.

Der reale Roboter-Render bleibt unverändert an seiner Stelle. Darüber liegt eine
Vektorebene: Kühlkreis (Vorlauf/Rücklauf) mit Flussrichtung, Druckluft/Vakuum,
gekühlte Aktoren, ein Einblick in den Torso (Pumpe, Verteiler) und vier
EISELE-Produkte mit Foto, Zweck und Daten aus dem Flyer.

Aufruf: python3 make_hero_kuehlung.py <flyer.pdf> <produktbilder_dir> <out.pdf>
"""
import sys
import numpy as np
import pikepdf
from reportlab.pdfgen import canvas as rl
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

flyer, imgdir, out = sys.argv[1:4]
PW, PH = 594.96, 841.92
LIB = '/usr/share/fonts/truetype/liberation'
pdfmetrics.registerFont(TTFont('H', f'{LIB}/LiberationSans-Regular.ttf'))
pdfmetrics.registerFont(TTFont('HB', f'{LIB}/LiberationSans-Bold.ttf'))


def hx(h, a=1.0):
    return Color(*(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)), alpha=a)


NAVY, GREY_T, LEADER = hx('#0B335E'), hx('#55606E'), hx('#7D8A9C')
BLUE, ORANGE, AIR = hx('#2F8CFF'), hx('#FF7A2E'), hx('#D9DEE6')
TILE = hx('#F2F1F0')

# Roboterbild: Platzierung laut Content-Stream (1156 x 1335 px)
RX0, RY0, RS = 309.0, 108.0, 0.24005


def R(px, py):
    """Bildpixel -> Seitenkoordinate (pt, von oben)."""
    return RX0 + px * RS, RY0 + py * RS


tmp = out + '.overlay.pdf'
c = rl.Canvas(tmp, pagesize=(PW, PH))
Y = lambda y: PH - y

# ---------------------------------------------------------------------------
# 1) Alten Heldbereich links (Badge, Headline, Produktfotos) abdecken
c.setFillColor(hx('#FFFFFF'))
p = c.beginPath()
p.moveTo(36, Y(100)); p.lineTo(306, Y(100)); p.lineTo(306, Y(322)); p.lineTo(472, Y(322))
p.lineTo(472, Y(424.6)); p.lineTo(36, Y(424.6)); p.close()
c.drawPath(p, stroke=0, fill=1)


# ---------------------------------------------------------------------------
def spline(pts, n=24):
    """Catmull-Rom durch Pixelpunkte -> dichte Liste in pt."""
    P = [R(*q) for q in pts]
    P = [P[0]] + P + [P[-1]]
    outp = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = map(np.array, (P[i - 1], P[i], P[i + 1], P[i + 2]))
        for t in np.linspace(0, 1, n, endpoint=False):
            t2, t3 = t * t, t * t * t
            q = 0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)
            outp.append(q)
    outp.append(np.array(P[-2]))
    return np.array(outp)


def offset(line, d):
    t = np.gradient(line, axis=0)
    t /= np.linalg.norm(t, axis=1, keepdims=True) + 1e-9
    nrm = np.stack([-t[:, 1], t[:, 0]], 1)
    return line + nrm * d


def stroke(line, col, w, alpha=1.0, dash=None):
    pth = c.beginPath(); pth.moveTo(line[0][0], Y(line[0][1]))
    for x, y in line[1:]:
        pth.lineTo(x, Y(y))
    c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=alpha)); c.setLineWidth(w)
    c.setLineCap(1); c.setLineJoin(1)
    if dash:
        c.setDash(*dash)
    c.drawPath(pth, stroke=1, fill=0)
    c.setDash()


def chevrons(line, col, every=30, size=1.7, reverse=False):
    seg = np.linalg.norm(np.diff(line, axis=0), axis=1)
    s = np.concatenate([[0], np.cumsum(seg)])
    c.setStrokeColor(hx('#FFFFFF', 0.95)); c.setLineWidth(0.6); c.setLineCap(1); c.setLineJoin(1)
    for d in np.arange(every * 0.6, s[-1] - 4, every):
        i = np.searchsorted(s, d) - 1
        i = max(0, min(i, len(line) - 2))
        t = line[i + 1] - line[i]; t = t / (np.linalg.norm(t) + 1e-9)
        if reverse:
            t = -t
        n = np.array([-t[1], t[0]])
        q = line[i] + (line[i + 1] - line[i]) * ((d - s[i]) / max(seg[i], 1e-9))
        a = q - t * size + n * size * 0.8
        b = q - t * size - n * size * 0.8
        pth = c.beginPath(); pth.moveTo(a[0], Y(a[1])); pth.lineTo(q[0], Y(q[1])); pth.lineTo(b[0], Y(b[1]))
        c.drawPath(pth, stroke=1, fill=0)


def coolant_pair(pts, sep=1.5, w=1.35):
    base = spline(pts)
    sup, ret = offset(base, -sep), offset(base, sep)
    for ln, col in ((sup, BLUE), (ret, ORANGE)):
        stroke(ln, col, w + 3.2, alpha=0.22)          # weicher Schein
    for ln, col in ((sup, BLUE), (ret, ORANGE)):
        stroke(ln, hx('#0A1424'), w + 0.9, alpha=0.65)  # dunkle Kontur
        stroke(ln, col, w)
    chevrons(sup, BLUE, reverse=False)                   # Vorlauf: weg von der Pumpe
    chevrons(ret, ORANGE, reverse=True)                  # Rücklauf: zur Pumpe


def air_line(pts):
    ln = spline(pts)
    stroke(ln, hx('#0A1424'), 1.7, alpha=0.6)
    stroke(ln, AIR, 0.9)
    stroke(ln, hx('#FFFFFF'), 0.9, dash=(1.2, 3.2))


def cooled_actuator(px, py, r_px):
    x, y = R(px, py); r = r_px * RS
    c.setStrokeColor(hx('#6FB6FF', 0.28)); c.setLineWidth(3.6); c.circle(x, Y(y), r, stroke=1, fill=0)
    c.setStrokeColor(hx('#A9D4FF', 0.95)); c.setLineWidth(0.7); c.circle(x, Y(y), r, stroke=1, fill=0)
    c.setStrokeColor(hx('#A9D4FF', 0.55)); c.setLineWidth(0.45); c.setDash(1.5, 1.8)
    c.circle(x, Y(y), r * 0.7, stroke=1, fill=0); c.setDash()


# ---------------------------------------------------------------------------
# 2) Kühlkreis auf dem Roboter
# Einblick in den Torso: Pumpe + Verteiler (dunkles Rauchglas)
wx0, wy0 = R(728, 432); wx1, wy1 = R(952, 640)
c.setFillColor(hx('#08182E', 0.86)); c.setStrokeColor(hx('#9CC3EE', 0.9)); c.setLineWidth(0.6)
c.roundRect(wx0, Y(wy1), wx1 - wx0, wy1 - wy0, 5, stroke=1, fill=1)
c.setStrokeColor(hx('#9CC3EE', 0.18)); c.setLineWidth(0.3)
for gx in np.arange(wx0 + 6, wx1 - 2, 6):
    c.line(gx, Y(wy0 + 2), gx, Y(wy1 - 2))
# Pumpe
px_, py_ = R(790, 575)
c.setFillColor(hx('#2A3B55')); c.setStrokeColor(hx('#B9D3F0')); c.setLineWidth(0.5)
c.circle(px_, Y(py_), 7.5, stroke=1, fill=1)
for k in range(6):
    a = k * np.pi / 3
    c.line(px_, Y(py_), px_ + 5.5 * np.cos(a + 0.5), Y(py_ + 5.5 * np.sin(a + 0.5)))
# Verteiler
mx0, my0 = R(838, 468); mx1, my1 = R(930, 600)
c.setFillColor(hx('#2A3B55')); c.roundRect(mx0, Y(my1), mx1 - mx0, my1 - my0, 2, stroke=1, fill=1)
for k in range(4):
    yy = my0 + 5 + k * (my1 - my0 - 10) / 3
    c.setFillColor(BLUE if k % 2 == 0 else ORANGE)
    c.circle(mx0 + 3.2, Y(yy), 1.4, stroke=0, fill=1); c.circle(mx1 - 3.2, Y(yy), 1.4, stroke=0, fill=1)
c.setFillColor(hx('#DCE8F7')); c.setFont('H', 4.6)
c.drawCentredString(px_, Y(py_ + 12.5), 'Pumpe')
# Pumpe -> Verteiler
stroke(np.array([[px_ + 7.5, py_ - 2], [mx0, py_ - 2]]), BLUE, 1.2)
stroke(np.array([[px_ + 7.5, py_ + 2.5], [mx0, py_ + 2.5]]), ORANGE, 1.2)

# Kreisläufe (Pixelkoordinaten im Roboterbild)
coolant_pair([(840, 488), (760, 468), (700, 440), (638, 392), (575, 470), (520, 560), (486, 632), (420, 664), (330, 694)])
coolant_pair([(930, 488), (975, 455), (1030, 405), (1062, 440), (1080, 560), (1098, 722)])
coolant_pair([(858, 600), (845, 660), (812, 760), (782, 860), (765, 958), (762, 1110), (760, 1300)])
coolant_pair([(905, 600), (918, 660), (925, 760), (928, 860), (930, 958), (930, 1110), (930, 1300)])
air_line([(728, 520), (700, 470), (660, 418), (600, 430), (548, 505), (500, 590), (440, 640), (340, 676), (250, 708), (175, 748), (120, 790)])

for (x, y, r) in ((636, 390, 44), (486, 634, 38), (1058, 400, 46), (1100, 724, 38), (765, 962, 50), (930, 962, 50)):
    cooled_actuator(x, y, r)

# ---------------------------------------------------------------------------
# 3) Linke Spalte: Headline, Legende, Produkte mit Zweck
LX = 47.05
c.setFillColor(NAVY); c.setFont('HB', 19.6)
c.drawString(LX, Y(132), 'EXTREM KLEINBAUEND.')
c.drawString(LX, Y(152), 'KOMPLETTER DURCHFLUSS.')
c.setFillColor(GREY_T); c.setFont('H', 8.2)
c.drawString(LX, Y(169), 'Flüssigkeitskühlung im humanoiden Roboter:')
c.drawString(LX, Y(179), 'EISELE verbindet Kühlwasser, Druckluft und Vakuum.')

ly = 196
for lab, col, xx in (('Vorlauf', BLUE, LX), ('Rücklauf', ORANGE, LX + 62), ('Druckluft / Vakuum', AIR, LX + 128)):
    if col is AIR:
        c.setStrokeColor(hx('#7D8A9C')); c.setLineWidth(1.6); c.setLineCap(1); c.setDash(1.2, 2.6)
    else:
        c.setStrokeColor(col); c.setLineWidth(1.8); c.setLineCap(1)
    c.line(xx, Y(ly), xx + 12, Y(ly)); c.setDash()
    c.setFillColor(GREY_T); c.setFont('H', 6.6); c.drawString(xx + 16, Y(ly) - 2.2, lab)
c.setStrokeColor(hx('#A9D4FF')); c.setLineWidth(0.7); c.circle(LX + 6, Y(ly + 11), 3.2, stroke=1, fill=0)
c.setFillColor(GREY_T); c.drawString(LX + 16, Y(ly + 11) - 2.2, 'Gekühlter Aktor (Kühlplatte)')

ROWS = [
    ('p_sa2113', 'SA2113-1 / -2', 'Schnellkupplung, tropffrei', 'Armmodul trennen ohne Medienverlust',
     'Kühlwasser · 0 bis 10 bar · bis +100 °C', [(636, 392)]),
    ('p_887', '863-4218 · 887-4218', 'Push-In, Programm 15', 'Druckluft und Vakuum zum Greifer',
     'M3 · Schlauch AD3 · ab ca. 2 g', [(196, 742)]),
    ('p_v0129', 'V0129-1850-040601', 'Modulare Schwenkkupplung', 'Vier Kanäle durch das Taillengelenk',
     'Kanäle 1–4 in einem Bauteil', 'waist'),
    ('p_vt5528', 'VT5528-0202', 'Verschraubung P5500, Aluminium', 'Kühlwasser an den Hüftaktor',
     'G1/8 · Schlauch AD4 · ca. 4 g', [(765, 962)]),
]
ry = 232
for i, (img, code, name, purpose, spec, anchor) in enumerate(ROWS):
    cy = ry + i * 47.5
    c.setFillColor(TILE); c.circle(LX + 20, Y(cy), 20, stroke=0, fill=1)
    from PIL import Image
    im = Image.open(f'{imgdir}/{img}.png'); iw, ih = im.size
    sc = 30 / max(iw, ih)
    c.drawImage(f'{imgdir}/{img}.png', LX + 20 - iw * sc / 2, Y(cy) - ih * sc / 2, iw * sc, ih * sc, mask='auto')
    tx = LX + 48
    c.setFillColor(NAVY); c.setFont('HB', 8.6); c.drawString(tx, Y(cy - 9), code)
    c.setFillColor(GREY_T); c.setFont('H', 6.6); c.drawString(tx, Y(cy - 0.5), name)
    c.setFillColor(NAVY); c.setFont('HB', 7); c.drawString(tx, Y(cy + 8), purpose)
    c.setFillColor(GREY_T); c.setFont('H', 6.3); c.drawString(tx, Y(cy + 16), spec)
    # Hinweislinie
    sx = 262
    if anchor == 'waist':
        ax, ay = R(735, 742)
        pts = [(sx, cy - 2), (452, cy - 2), (ax, ay)]
    else:
        ax, ay = R(*anchor[0])
        pts = [(sx, cy - 2), (ax, ay)]
    c.setStrokeColor(LEADER); c.setLineWidth(0.55); c.setLineCap(0)
    pth = c.beginPath(); pth.moveTo(pts[0][0], Y(pts[0][1]))
    for q in pts[1:]:
        pth.lineTo(q[0], Y(q[1]))
    c.drawPath(pth, stroke=1, fill=0)
    c.setFillColor(LEADER); c.circle(sx, Y(cy - 2), 1.1, stroke=0, fill=1)
    c.setFillColor(hx('#FFFFFF')); c.setStrokeColor(NAVY); c.setLineWidth(0.8)
    c.circle(ax, Y(ay), 3.0, stroke=1, fill=1)
    c.setFillColor(NAVY); c.circle(ax, Y(ay), 1.2, stroke=0, fill=1)

c.setFillColor(hx('#8A94A3')); c.setFont('H', 5.8)
c.drawString(LX, Y(418), 'Konzeptdarstellung, Einbauorte beispielhaft. Daten laut EISELE-Datenblättern.')
c.showPage(); c.save()

# ---------------------------------------------------------------------------
# 4) Auf Seite 1 des Original-Flyers legen
pdf = pikepdf.open(flyer)
ov = pikepdf.open(tmp)
pdf.pages[0].add_overlay(ov.pages[0])
pdf.save(out)
print('ok', out)
