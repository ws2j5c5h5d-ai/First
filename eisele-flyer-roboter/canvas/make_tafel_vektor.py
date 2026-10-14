"""Tafel 01 'Stille Zirkulation', Vektorfassung.
Der Roboter wird aus der Rastervorlage nachgezeichnet (Silhouette, Hüllkanten,
Bauteile, Leitungen, dunkle Teile) und vollständig als Vektor gesetzt.
Hintergrund, Raster, Rahmen, Einzelheit A und alle Texte sind ebenfalls Vektor.

Aufruf: python3 make_tafel_vektor.py <vorlage.png> <silhouette.png> <fonts> <out.pdf>
"""
import sys
import numpy as np
import cv2
from PIL import Image
from scipy import ndimage as ndi
from reportlab.pdfgen import canvas as rl
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

src_p, sil_p, fonts, out = sys.argv[1:5]
PW, PH = 842.04, 1122.48
im = np.array(Image.open(src_p).convert('RGB'))
H, W, _ = im.shape
K = PW / W

for name, f in (('Sans', 'InstrumentSans-Regular'), ('SansB', 'InstrumentSans-Bold'),
                ('Serif', 'InstrumentSerif-Italic'), ('Mono', 'GeistMono-Regular')):
    pdfmetrics.registerFont(TTFont(name, f'{fonts}/{f}.ttf'))

def hx(h, a=1.0):
    return Color(*(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)), alpha=a)

INK, DIM, HAIR, LEAD = hx('#DCE2EA'), hx('#8A99AF'), hx('#3E5270'), hx('#AEBBCD')
BLUE, ORANGE, GREY = hx('#2F8CFF'), hx('#FF7A2E'), hx('#D5D9DF')

sys.path.insert(0, __import__('os').path.dirname(__file__))
from robot_vektor import draw_robot
# ============ 2) Zeichnen =====================================================
c = rl.Canvas(out, pagesize=(PW, PH))
c.setTitle('Tafel 01 – Stille Zirkulation'); c.setAuthor('EISELE Marketing')
Y = lambda y: PH - y

# Hintergrund: Vektor-Radialverlauf
c.setFillColor(hx('#070D17')); c.rect(0, 0, PW, PH, stroke=0, fill=1)
CX, CY = 1700 * K, 1350 * K
c.saveState()
p = c.beginPath(); p.rect(0, 0, PW, PH); c.clipPath(p, stroke=0)
c.radialGradient(CX, Y(CY), 640, (hx('#15294A'), hx('#0C1728'), hx('#070D17')), (0, 0.55, 1), extend=True)
c.restoreState()

def robot(dx=0, dy=0, s=1.0):
    draw_robot(c, K, PH, dx, dy, s)


# Messpunktraster (nicht auf der Figur)
sil = np.array(Image.open(sil_p).convert('L')) > 127
sil_d = cv2.dilate(sil.astype(np.uint8), np.ones((41, 41), np.uint8)) > 0
c.setFillColor(hx('#22334D'))
for gy in np.arange(60, PH - 60, 12):
    for gx in np.arange(60, PW - 60, 12):
        if sil_d[min(H - 1, int(gy / K)), min(W - 1, int(gx / K))]:
            continue
        c.circle(gx, Y(gy), 0.42, stroke=0, fill=1)

robot()

# ---------- Rahmen mit Zonen ----------
O, I = 26, 38
c.setStrokeColor(HAIR); c.setLineWidth(0.5)
c.rect(O, O, PW - 2 * O, PH - 2 * O, stroke=1, fill=0); c.rect(I, I, PW - 2 * I, PH - 2 * I, stroke=1, fill=0)
c.setFont('Mono', 5.6); c.setFillColor(DIM)
for i in range(1, 6):
    x = I + (PW - 2 * I) * i / 6
    c.line(x, O, x, I); c.line(x, PH - I, x, PH - O)
for i in range(6):
    x = I + (PW - 2 * I) * (i + 0.5) / 6
    c.drawCentredString(x, Y(O + 8.2), str(i + 1)); c.drawCentredString(x, O + 3.8, str(i + 1))
for j in range(1, 8):
    y = I + (PH - 2 * I) * j / 8
    c.line(O, y, I, y); c.line(PW - I, y, PW - O, y)
for j in range(8):
    y = Y(I + (PH - 2 * I) * (j + 0.5) / 8) - 2
    c.drawCentredString((O + I) / 2, y, 'ABCDEFGH'[j]); c.drawCentredString(PW - (O + I) / 2, y, 'ABCDEFGH'[j])
c.setLineWidth(0.6)
for (x, y, dx, dy) in ((PW / 2, I, 0, 1), (PW / 2, PH - I, 0, -1), (I, PH / 2, 1, 0), (PW - I, PH / 2, -1, 0)):
    p = c.beginPath(); p.moveTo(x - dy * 4 + dx * 9, y - dx * 4 + dy * 9); p.lineTo(x, y)
    p.lineTo(x + dy * 4 + dx * 9, y + dx * 4 + dy * 9); c.drawPath(p, stroke=1, fill=0)

# ---------- Titel ----------
LX = 62
c.setFillColor(DIM); c.setFont('Mono', 7); c.drawString(LX, Y(72), 'Tafel 01')
c.setFillColor(INK); c.setFont('Serif', 34); c.drawString(LX - 1, Y(106), 'Stille Zirkulation')
c.setFillColor(DIM); c.setFont('Sans', 9.5)
c.drawString(LX, Y(124), 'Kühlung und Pneumatik im humanoiden Roboter, tropffrei verbunden')

# ---------- Medienlegende ----------
c.setFont('Mono', 6.5); c.setFillColor(DIM); c.drawString(LX, Y(176), 'Medien')
c.setLineCap(1)
for i, (lab, col) in enumerate((('Kühlwasser Vorlauf', BLUE), ('Kühlwasser Rücklauf', ORANGE), ('Druckluft / Vakuum', GREY))):
    y = 194 + i * 17
    c.setStrokeColor(col); c.setLineWidth(2.2); c.line(LX, Y(y), LX + 22, Y(y))
    c.setFillColor(INK); c.setFont('Sans', 8.5); c.drawString(LX + 32, Y(y) - 3, lab)
c.setLineCap(0)

# ---------- Positionsnummern ----------
POS = {1: ((1420, 1050), (452, 300)), 2: ((1600, 1918), (470, 792)), 3: ((772, 1565), (238, 488))}
for n, ((ax, ay), (bx, by)) in POS.items():
    ax, ay = ax * K, ay * K
    v = np.array([ax - bx, ay - by]); v /= np.linalg.norm(v)
    c.setStrokeColor(LEAD); c.setLineWidth(0.55)
    c.line(bx + v[0] * 9, Y(by + v[1] * 9), ax, Y(ay))
    c.setFillColor(LEAD); c.circle(ax, Y(ay), 1.6, stroke=0, fill=1)
    c.circle(ax, Y(ay), 4.2, stroke=1, fill=0)
    c.setFillColor(hx('#0B1525')); c.setLineWidth(0.7); c.circle(bx, Y(by), 9, stroke=1, fill=1)
    c.setFillColor(INK); c.setFont('SansB', 9); c.drawCentredString(bx, Y(by) - 3.2, str(n))

# ---------- Einzelheit A (2:1), echte Vektorvergrößerung ----------
SC = (1655 * K, 1190 * K); SR = 118 * K            # Quelle (pt)
DC, DR = (182, 812), 2 * SR
c.saveState()
p = c.beginPath(); p.circle(DC[0], Y(DC[1]), DR); c.clipPath(p, stroke=0)
c.setFillColor(hx('#0B1626')); c.rect(DC[0] - DR, Y(DC[1] + DR), 2 * DR, 2 * DR, stroke=0, fill=1)
robot(dx=DC[0] - 2 * SC[0], dy=DC[1] - 2 * SC[1], s=2.0)
c.restoreState()
c.setStrokeColor(LEAD); c.setLineWidth(0.7); c.circle(DC[0], Y(DC[1]), DR, stroke=1, fill=0)
c.setDash([6, 2, 1, 2]); c.setLineWidth(0.6); c.circle(SC[0], Y(SC[1]), SR, stroke=1, fill=0); c.setDash()
c.setFillColor(INK); c.setFont('SansB', 10); c.drawString(SC[0] + SR * 0.72 + 3, Y(SC[1] - SR * 0.72) - 2, 'A')
c.setFont('Sans', 8.5); c.drawString(DC[0] - DR, Y(DC[1] + DR + 16), 'Einzelheit A, Verteiler im Torso')
c.setFillColor(DIM); c.setFont('Mono', 6.5); c.drawRightString(DC[0] + DR, Y(DC[1] + DR + 16), '2:1')

# ---------- Stückliste ----------
TY, RH = 990, 17
c.setStrokeColor(HAIR); c.setLineWidth(0.5)
X0, X1 = I + 14, 530
cols = (X0, X0 + 30, X0 + 230, X0 + 340, X1)
rows = (('1', 'Modulschnittstelle, tropffrei trennen', 'SA2113-1 / -2', 'Kühlwasser'),
        ('2', 'Aktorkühlung, Hüftantrieb', 'VT5528-0202', 'Kühlwasser'),
        ('3', 'Greifer', '863-4218 / 887-4218', 'Druckluft / Vakuum'))
n_r = len(rows) + 1
c.rect(X0, Y(TY + RH * n_r), X1 - X0, RH * n_r, stroke=1, fill=0)
for i in range(1, n_r):
    c.line(X0, Y(TY + RH * i), X1, Y(TY + RH * i))
for x in cols[1:-1]:
    c.line(x, Y(TY), x, Y(TY + RH * n_r))
c.setFont('Mono', 6.2); c.setFillColor(DIM)
for x, h in zip(cols, ('Pos.', 'Benennung', 'Artikel-Nr.', 'Medium')):
    c.drawString(x + 5, Y(TY + 11.5), h)
for r, row in enumerate(rows, 1):
    for k, (x, val) in enumerate(zip(cols, row)):
        c.setFillColor(INK)
        c.setFont('Mono' if k == 2 else ('SansB' if k == 0 else 'Sans'), 7.4 if k == 2 else 8)
        c.drawString(x + 5, Y(TY + RH * r + 11.8), val)

# ---------- Schriftfeld ----------
S0, S1 = 548, PW - I - 14
RH2 = RH * n_r / 3
cells = [('Benennung', 'Fluidführung, humanoider Roboter', S0, S1, 0),
         ('Darstellung', 'Konzept, nicht maßstäblich', S0, S0 + 150, 1),
         ('Tafel', '01', S0 + 150, S1, 1),
         ('Web', 'eisele-connectors.com', S0, S0 + 150, 2),
         ('Stand', '10 / 2026', S0 + 150, S1, 2)]
c.rect(S0, Y(TY + RH2 * 3), S1 - S0, RH2 * 3, stroke=1, fill=0)
for i in (1, 2):
    c.line(S0, Y(TY + RH2 * i), S1, Y(TY + RH2 * i))
for lab, val, x0, x1, r in cells:
    if x0 > S0:
        c.line(x0, Y(TY + RH2 * r), x0, Y(TY + RH2 * (r + 1)))
    c.setFont('Mono', 5.4); c.setFillColor(DIM); c.drawString(x0 + 5, Y(TY + RH2 * r + 8), lab)
    c.setFont('Sans', 8); c.setFillColor(INK); c.drawString(x0 + 5, Y(TY + RH2 * r + 18.5), val)
c.setFont('Mono', 5.4); c.setFillColor(DIM)
c.drawRightString(S1, Y(TY + RH2 * 3 + 9), 'Konzeptdarstellung, kein reales Robotermodell')

c.showPage(); c.save()
print('ok', out)
