"""Tafel 'Stille Zirkulation': nur die Roboterfigur, als ruhige Beobachtungstafel.
Aufruf: python3 make_canvas.py <robot_rgba.png> <fonts_dir> <out_prefix>
"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

robot_path, fonts, out = sys.argv[1:4]
S = 2                                  # Supersampling
W, H = 1800, 2250                      # Ausgabe 4:5
w, h = W * S, H * S

NAVY_IN, NAVY_OUT = (19, 36, 59), (7, 13, 23)
DOT, HAIR, INK, INK_DIM = (31, 47, 71), (58, 78, 106), (196, 204, 216), (120, 136, 158)
BLUE, ORANGE, GREY = (47, 140, 255), (255, 122, 46), (213, 217, 223)

# --- Figur und Position ----------------------------------------------------
robot = Image.open(robot_path).convert('RGBA')
rw, rh = robot.size
RX, RY = 452, 372                      # obere linke Ecke der Figur (1x)
CX, CY = RX + 850, RY + 620            # Torso: Zentrum des Lichts

# --- Grund: radialer Lichtabfall --------------------------------------------
yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
r = np.sqrt(((xx - CX * S) / (1.05 * w)) ** 2 + ((yy - CY * S) / (0.95 * h)) ** 2)
t = np.clip(r / 0.62, 0, 1) ** 1.35
bg = np.empty((h, w, 3), np.float32)
for i in range(3):
    bg[..., i] = NAVY_IN[i] * (1 - t) + NAVY_OUT[i] * t
# feines Korn gegen Banding im Verlauf
rng = np.random.default_rng(7)
bg += rng.normal(0, 0.55, bg.shape)
canvas = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8), 'RGB').convert('RGBA')
d = ImageDraw.Draw(canvas)

# --- Raster aus Messpunkten (30 px), zum Rand hin leiser --------------------
M = 90                                  # Innenrand des Rasters
step = 30
for gy in range(M, H - M + 1, step):
    for gx in range(M, W - M + 1, step):
        rr = np.hypot((gx - CX) / W, (gy - CY) / H)
        k = max(0.0, 1 - rr / 0.75)
        a = int(40 + 120 * k)
        rad = 0.85 * S
        d.ellipse([gx * S - rad, gy * S - rad, gx * S + rad, gy * S + rad], fill=DOT + (a,))

# --- Registermarken an den vier Ecken des Rasters ---------------------------
def cross(x, y, L=14):
    d.line([(x - L) * S, y * S, (x + L) * S, y * S], fill=HAIR + (255,), width=S)
    d.line([x * S, (y - L) * S, x * S, (y + L) * S], fill=HAIR + (255,), width=S)
for x, y in ((M, M), (W - M, M), (M, H - M), (W - M, H - M)):
    cross(x, y)

# --- Vertikale Skala links, auf Höhe der Figur --------------------------------
SX = 150
top, bot = RY + 30, RY + rh - 120
d.line([SX * S, top * S, SX * S, bot * S], fill=HAIR + (255,), width=S)
for i, y in enumerate(range(top, bot + 1, 30)):
    L = 16 if i % 5 == 0 else 7
    d.line([SX * S, y * S, (SX + L) * S, y * S], fill=HAIR + (255,), width=S)

# --- Figur ---------------------------------------------------------------
big = robot.resize((rw * S, rh * S), Image.LANCZOS)
canvas.alpha_composite(big, (RX * S, RY * S))
d = ImageDraw.Draw(canvas)

# --- Typografie ------------------------------------------------------------
f_title = ImageFont.truetype(f'{fonts}/InstrumentSerif-Italic.ttf', 64 * S)
f_label = ImageFont.truetype(f'{fonts}/Jura-Light.ttf', 23 * S)
f_mono = ImageFont.truetype(f'{fonts}/GeistMono-Regular.ttf', 14 * S)

def text(x, y, s, f, fill):
    d.text((x * S, y * S), s, font=f, fill=fill + (255,))

text(SX, 160, 'Tafel 01', f_mono, INK_DIM)
text(SX - 3, 186, 'Stille Zirkulation', f_title, INK)

# Legende: drei Adern, je eine Linie in Leitungsstärke
LY = 1930
rows = (('Kühlwasser Vorlauf', BLUE), ('Kühlwasser Rücklauf', ORANGE), ('Druckluft / Vakuum', GREY))
for i, (lab, col) in enumerate(rows):
    y = LY + i * 46
    d.rounded_rectangle([SX * S, (y - 1.5) * S, (SX + 56) * S, (y + 1.5) * S], radius=1.5 * S, fill=col + (255,))
    text(SX + 76, y - 15, lab, f_label, INK)

# Wärmeband: von kalt nach warm, mit Teilstrichen
BX0, BX1, BY = 1080, 1650, LY
for x in range(BX0 * S, BX1 * S):
    k = (x - BX0 * S) / ((BX1 - BX0) * S)
    c = tuple(int(BLUE[j] * (1 - k) + ORANGE[j] * k) for j in range(3))
    d.line([x, (BY - 1.5) * S, x, (BY + 1.5) * S], fill=c + (255,))
for i in range(0, 11):
    x = BX0 + (BX1 - BX0) * i / 10
    L = 10 if i in (0, 5, 10) else 5
    d.line([x * S, (BY + 8) * S, x * S, (BY + 8 + L) * S], fill=HAIR + (255,), width=S)
text(BX0, BY + 28, 'kalt', f_mono, INK_DIM)
wb = d.textbbox((0, 0), 'warm', font=f_mono)
text(BX1 - (wb[2] - wb[0]) / S, BY + 28, 'warm', f_mono, INK_DIM)

cap = 'Konzeptdarstellung, kein reales Robotermodell'
cb = d.textbbox((0, 0), cap, font=f_mono)
text(BX1 - (cb[2] - cb[0]) / S, LY + 2 * 46 - 9, cap, f_mono, INK_DIM)

final = canvas.convert('RGB').resize((W, H), Image.LANCZOS)
final.save(f'{out}.png', dpi=(300, 300))
final.save(f'{out}.pdf', resolution=300)
print('ok', final.size)
