"""Tafel 01 'Stille Zirkulation', technische Fassung.
Basis: das hochgeladene Raster (Roboter). Alles Grafische und jeder Text wird
als Vektor neu gesetzt: Zonenrahmen, Positionsnummern, Einzelheit A (2:1),
Medienlegende, Stückliste und Schriftfeld.

Aufruf: python3 make_tafel_technisch.py <raster.png> <robotermaske.png> <hintergrund.png> <fonts> <out.pdf>
"""
import io
import sys
import numpy as np
import cv2
from PIL import Image, ImageDraw
from reportlab.pdfgen import canvas as rl
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

src_p, mask_p, bg_p, fonts, out = sys.argv[1:6]
PW, PH = 842.04, 1122.48                 # Seitengröße wie Vorlage (pt)
src = np.array(Image.open(src_p).convert('RGB')).astype(np.float32)
H, W, _ = src.shape
K = PW / W                               # px -> pt

for name, f in (('Sans', 'InstrumentSans-Regular'), ('SansB', 'InstrumentSans-Bold'),
                ('Serif', 'InstrumentSerif-Italic'), ('Mono', 'GeistMono-Regular')):
    pdfmetrics.registerFont(TTFont(name, f'{fonts}/{f}.ttf'))

def hx(h):
    return tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))

INK, DIM, HAIR, LEAD = hx('#DCE2EA'), hx('#8A99AF'), hx('#3E5270'), hx('#AEBBCD')
BLUE, ORANGE, GREY = hx('#2F8CFF'), hx('#FF7A2E'), hx('#D5D9DF')

# --- Raster: Roboter auf neuem, sauberem Grund -------------------------------
m = np.array(Image.open(mask_p).convert('L')).astype(np.float32) / 255
halo = cv2.dilate((m > 0.5).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (61, 61))).astype(np.float32)
# Beinbereich unten weich auslaufen lassen (Vorlage blendet dort bereits aus)
ys, xs = np.where(m > 0.5)
leg_top = int(np.percentile(ys, 92))
halo[leg_top:min(H, ys.max() + 120), max(0, xs[ys > leg_top].min() - 30):xs[ys > leg_top].max() + 30] = 1
halo = cv2.GaussianBlur(halo, (0, 0), 22)
bg = np.array(Image.open(bg_p).convert('RGB')).astype(np.float32)
rng = np.random.default_rng(3)
bg += rng.normal(0, 0.6, bg.shape)        # Korn gegen Banding
comp = src * halo[..., None] + bg * (1 - halo[..., None])
comp_img = Image.fromarray(np.clip(comp, 0, 255).astype(np.uint8))
buf = io.BytesIO(); comp_img.save(buf, 'JPEG', quality=93, subsampling=0); buf.seek(0)

c = rl.Canvas(out, pagesize=(PW, PH))
c.setTitle('Tafel 01 – Stille Zirkulation'); c.setAuthor('EISELE Marketing')
c.drawImage(ImageReader(buf), 0, 0, PW, PH)

Y = lambda y: PH - y                      # Koordinaten von oben denken

def px(x, y):                             # Rasterpixel -> pt (von oben)
    return x * K, y * K

# --- Messpunktraster (12 pt), nicht im Roboterbereich ------------------------
c.setFillColorRGB(*hx('#22334D'))
for gy in np.arange(60, PH - 60, 12):
    for gx in np.arange(60, PW - 60, 12):
        if halo[min(H - 1, int(gy / K)), min(W - 1, int(gx / K))] > 0.03:
            continue
        c.circle(gx, Y(gy), 0.42, stroke=0, fill=1)

# --- Zeichnungsrahmen mit Zonen (A–H, 1–6) und Zentriermarken ---------------
O, I = 26, 38                             # Außen- und Innenrahmen
c.setStrokeColorRGB(*HAIR); c.setLineWidth(0.5)
c.rect(O, O, PW - 2 * O, PH - 2 * O); c.rect(I, I, PW - 2 * I, PH - 2 * I)
c.setFont('Mono', 5.6); c.setFillColorRGB(*DIM)
cols, rows = 6, 8
for i in range(1, cols):
    x = I + (PW - 2 * I) * i / cols
    for y0, y1 in ((O, I), (PH - I, PH - O)):
        c.line(x, y0, x, y1)
for i in range(cols):
    x = I + (PW - 2 * I) * (i + 0.5) / cols
    c.drawCentredString(x, Y(O + 8.2), str(i + 1)); c.drawCentredString(x, O + 3.8, str(i + 1))
for j in range(1, rows):
    y = I + (PH - 2 * I) * j / rows
    for x0, x1 in ((O, I), (PW - I, PW - O)):
        c.line(x0, y, x1, y)
for j in range(rows):
    y = Y(I + (PH - 2 * I) * (j + 0.5) / rows) - 2
    ch = 'ABCDEFGH'[j]
    c.drawCentredString((O + I) / 2, y, ch); c.drawCentredString(PW - (O + I) / 2, y, ch)
c.setStrokeColorRGB(*HAIR); c.setLineWidth(0.6)
for (x, y, dx, dy) in ((PW / 2, I, 0, 1), (PW / 2, PH - I, 0, -1), (I, PH / 2, 1, 0), (PW - I, PH / 2, -1, 0)):
    p = c.beginPath(); p.moveTo(x, y); p.lineTo(x + dx * 9 - dy * 4, y + dy * 9 - dx * 4)
    p.moveTo(x, y); p.lineTo(x + dx * 9 + dy * 4, y + dy * 9 + dx * 4); c.drawPath(p)

# --- Titel -------------------------------------------------------------------
LX = 62
c.setFillColorRGB(*DIM); c.setFont('Mono', 7); c.drawString(LX, Y(72), 'Tafel 01')
c.setFillColorRGB(*INK); c.setFont('Serif', 34); c.drawString(LX - 1, Y(106), 'Stille Zirkulation')
c.setFillColorRGB(*DIM); c.setFont('Sans', 9.5)
c.drawString(LX, Y(124), 'Fluidführung im humanoiden Roboter')

# --- Medienlegende links -------------------------------------------------------
c.setFont('Mono', 6.5); c.setFillColorRGB(*DIM); c.drawString(LX, Y(176), 'Medien')
for i, (lab, col) in enumerate((('Kühlwasser Vorlauf', BLUE), ('Kühlwasser Rücklauf', ORANGE),
                                 ('Druckluft / Vakuum', GREY))):
    y = 194 + i * 17
    c.setStrokeColorRGB(*col); c.setLineWidth(2); c.setLineCap(1); c.line(LX, Y(y), LX + 22, Y(y))
    c.setFillColorRGB(*INK); c.setFont('Sans', 8.5); c.drawString(LX + 32, Y(y) - 3, lab)
c.setLineCap(0)

# --- Positionsnummern ---------------------------------------------------------
POS = {  # Ankerpunkt am Bauteil (Rasterpixel), Balloon-Mitte (pt)
    1: ((1412, 1048), (452, 300)),        # Schulter / Modulschnittstelle
    2: ((1552, 1905), (470, 792)),        # Hüftaktor links
    3: ((772, 1565), (238, 488)),         # Handgelenk / Greifer
}

def balloon(n, anchor_px, b):
    ax, ay = px(*anchor_px); bx, by = b
    v = np.array([ax - bx, ay - by]); v = v / np.linalg.norm(v)
    c.setStrokeColorRGB(*LEAD); c.setLineWidth(0.55)
    c.line(bx + v[0] * 9, Y(by + v[1] * 9), ax, Y(ay))
    c.setFillColorRGB(*LEAD); c.circle(ax, Y(ay), 1.6, stroke=0, fill=1)
    c.circle(ax, Y(ay), 4.2, stroke=1, fill=0)
    c.setFillColorRGB(*hx('#0B1525')); c.setStrokeColorRGB(*LEAD); c.setLineWidth(0.7)
    c.circle(bx, Y(by), 9, stroke=1, fill=1)
    c.setFillColorRGB(*INK); c.setFont('SansB', 9); c.drawCentredString(bx, Y(by) - 3.2, str(n))

for n, (a, b) in POS.items():
    balloon(n, a, b)

# --- Einzelheit A (2:1): Verteiler im Torso -----------------------------------
SRC_C, SRC_R = (1690, 1200), 125         # Quelle im Raster (px)
DC, DR = (178, 760), 2 * SRC_R * K * 0.98 # Ziel (pt), Radius ~ 2:1
crop = comp_img.crop((SRC_C[0] - SRC_R, SRC_C[1] - SRC_R, SRC_C[0] + SRC_R, SRC_C[1] + SRC_R))
S = 4 * SRC_R
crop = crop.resize((S, S), Image.LANCZOS)
mk = Image.new('L', (S * 2, S * 2), 0); ImageDraw.Draw(mk).ellipse((0, 0, S * 2 - 1, S * 2 - 1), fill=255)
mk = mk.resize((S, S), Image.LANCZOS)
rgba = crop.convert('RGBA'); rgba.putalpha(mk)
b2 = io.BytesIO(); rgba.save(b2, 'PNG'); b2.seek(0)
c.drawImage(ImageReader(b2), DC[0] - DR, Y(DC[1] + DR), 2 * DR, 2 * DR, mask='auto')
c.setStrokeColorRGB(*LEAD); c.setLineWidth(0.7); c.circle(DC[0], Y(DC[1]), DR, stroke=1, fill=0)
# Quellkreis am Roboter, strichpunktiert
sx, sy = px(*SRC_C)
c.setDash([6, 2, 1, 2]); c.setLineWidth(0.6); c.circle(sx, Y(sy), SRC_R * K, stroke=1, fill=0); c.setDash()
c.setFillColorRGB(*INK); c.setFont('SansB', 10)
c.drawString(sx + SRC_R * K * 0.72 + 3, Y(sy - SRC_R * K * 0.72) - 2, 'A')
c.setFont('Sans', 8.5); c.drawString(DC[0] - DR, Y(DC[1] + DR + 16), 'Einzelheit A')
c.setFillColorRGB(*DIM); c.setFont('Mono', 6.5)
c.drawRightString(DC[0] + DR, Y(DC[1] + DR + 16), '2:1')

# --- Stückliste und Schriftfeld ------------------------------------------------
TY = 990                                  # Oberkante (pt von oben)
RH = 17
c.setStrokeColorRGB(*HAIR); c.setLineWidth(0.5)
# Stückliste
SL_X0, SL_X1 = I + 14, 530
cols_sl = (SL_X0, SL_X0 + 30, SL_X0 + 230, SL_X0 + 340, SL_X1)
heads = ('Pos.', 'Benennung', 'Artikel-Nr.', 'Medium')
rows_sl = (('1', 'Modulschnittstelle, tropffrei trennen', 'SA2113-1 / -2', 'Kühlwasser'),
           ('2', 'Aktorkühlung, Hüftantrieb', 'VT5528-0202', 'Kühlwasser'),
           ('3', 'Greifer', '863-4218 / 887-4218', 'Druckluft / Vakuum'))
n_r = len(rows_sl) + 1
c.rect(SL_X0, Y(TY + RH * n_r), SL_X1 - SL_X0, RH * n_r)
for i in range(1, n_r):
    c.line(SL_X0, Y(TY + RH * i), SL_X1, Y(TY + RH * i))
for x in cols_sl[1:-1]:
    c.line(x, Y(TY), x, Y(TY + RH * n_r))
c.setFont('Mono', 6.2); c.setFillColorRGB(*DIM)
for x, h in zip(cols_sl, heads):
    c.drawString(x + 5, Y(TY + 11.5), h)
for r, row in enumerate(rows_sl, 1):
    y = Y(TY + RH * r + 11.8)
    for k, (x, val) in enumerate(zip(cols_sl, row)):
        c.setFillColorRGB(*INK)
        c.setFont('Mono' if k == 2 else ('SansB' if k == 0 else 'Sans'), 7.4 if k == 2 else 8)
        c.drawString(x + 5, y, val)

# Schriftfeld
SF_X0, SF_X1 = 548, PW - I - 14
SF = [('Benennung', 'Fluidführung, humanoider Roboter', SF_X0, SF_X1),
      ('Darstellung', 'Konzept, nicht maßstäblich', SF_X0, SF_X0 + 150),
      ('Blatt', '1 / 1', SF_X0 + 150, SF_X1),
      ('Tafel', '01', SF_X0, SF_X0 + 75),
      ('Stand', '10 / 2026', SF_X0 + 75, SF_X0 + 150),
      ('Hinweis', 'Kein reales Modell', SF_X0 + 150, SF_X1)]
rows_y = (0, 1, 1, 2, 2, 2)
RH2 = RH * n_r / 3
c.rect(SF_X0, Y(TY + RH2 * 3), SF_X1 - SF_X0, RH2 * 3)
for i in (1, 2):
    c.line(SF_X0, Y(TY + RH2 * i), SF_X1, Y(TY + RH2 * i))
for (lab, val, x0, x1), r in zip(SF, rows_y):
    if x0 > SF_X0:
        c.line(x0, Y(TY + RH2 * r), x0, Y(TY + RH2 * (r + 1)))
    c.setFont('Mono', 5.4); c.setFillColorRGB(*DIM); c.drawString(x0 + 5, Y(TY + RH2 * r + 8), lab)
    c.setFont('Sans', 8); c.setFillColorRGB(*INK); c.drawString(x0 + 5, Y(TY + RH2 * r + 18.5), val)

c.showPage(); c.save()
print('ok', out)
