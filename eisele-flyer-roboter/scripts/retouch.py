"""Retusche der Phantom-Roboterfigur (EISELE Flyer Titel).
Eingabe: RGB-Bild + Alphamaske aus der Digital-PDF. Ausgabe: RGBA-PNG.
Alle Zielwerte entsprechen der Analyse (Legendenfarben, Fresnel 15/55 %, usw.).
"""
import sys
import numpy as np
import cv2
from PIL import Image
from scipy import ndimage as ndi

src_rgb, src_a, out = sys.argv[1], sys.argv[2], sys.argv[3]
rgb = np.array(Image.open(src_rgb).convert('RGB')).astype(np.float32) / 255
A = np.array(Image.open(src_a).convert('L')).astype(np.float32) / 255
H, W = A.shape

def hexf(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], np.float32) / 255

BLUE, ORANGE, GREY = hexf('#2F8CFF'), hexf('#FF7A2E'), hexf('#D5D9DF')
SHELL, INNER, RIM = hexf('#9AA3B0'), hexf('#5A626E'), hexf('#7FA6D9')
VISOR, HAND = hexf('#1A2333'), hexf('#363C46')

hsv = cv2.cvtColor((rgb * 255).astype(np.uint8), cv2.COLOR_RGB2HSV_FULL).astype(np.float32)
hue = hsv[..., 0] / 255 * 360
sat = hsv[..., 1] / 255
val = hsv[..., 2] / 255
L = rgb @ np.array([0.2126, 0.7152, 0.0722], np.float32)

body = A > 0.04
opaque = A > 0.95
yy, xx = np.mgrid[0:H, 0:W]

# --- Leitungen erkennen ---------------------------------------------------
blue_raw = (hue > 185) & (hue < 225) & (sat > 0.22) & (val > 0.25)
orange_raw = (hue > 15) & (hue < 50) & (sat > 0.22) & (val > 0.3)
# Blaue Kompositing-Säume (blaue Kante in teiltransparenten Zonen) sind keine Leitung
fringe = blue_raw & (A < 0.6)
blue_m = blue_raw & ~fringe
orange_m = orange_raw & (A > 0.5)

def clean(m, min_px=25):
    m = ndi.binary_opening(m, iterations=1) | (m & ndi.binary_erosion(ndi.binary_dilation(m, iterations=2), iterations=1))
    lab, n = ndi.label(m)
    sizes = ndi.sum(m, lab, range(1, n + 1))
    keep = np.isin(lab, np.where(sizes >= min_px)[0] + 1)
    return keep

blue_m, orange_m = clean(blue_m), clean(orange_m)
# Druckluftleitung: helle, dünne, unbunte Linie entlang des rechten Arms und der Schulter
bright = (L > 0.70) & (sat < 0.12) & opaque
tophat = cv2.morphologyEx((L * 255).astype(np.uint8), cv2.MORPH_TOPHAT,
                          cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))) / 255
grey_m = bright & (tophat > 0.10)
grey_m = clean(grey_m, 60)
blob = cv2.morphologyEx(grey_m.astype(np.uint8), cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))) > 0
grey_m &= ~ndi.binary_dilation(blob, iterations=2)
# Nur dünne, lange Komponenten sind Schläuche (keine Glanzkanten an Scheiben/Visier)
lab, n = ndi.label(grey_m)
dt = ndi.distance_transform_edt(grey_m)
keep = []
for i, sl in enumerate(ndi.find_objects(lab), 1):
    comp = lab[sl] == i
    area = comp.sum()
    thick = dt[sl][comp].max()
    length = max(sl[0].stop - sl[0].start, sl[1].stop - sl[1].start)
    if thick <= 5 and length >= 55 and sl[0].start > 300:
        keep.append(i)
grey_m = np.isin(lab, keep)
lines = blue_m | orange_m | grey_m

# --- Zonen ---------------------------------------------------------------
head = (yy < 300) & (xx > 680) & (xx < 960)
dark = opaque & (L < 0.33) & ~lines
lab, n = ndi.label(dark)
sizes = ndi.sum(dark, lab, range(1, n + 1))
dark = np.isin(lab, np.where(sizes > 400)[0] + 1)
dark_any = (L < 0.33) & (A > 0.5) & head
lab_v, nv = ndi.label(dark_any)
if nv:
    sz = ndi.sum(dark_any, lab_v, range(1, nv + 1)); dark_any = lab_v == (np.argmax(sz) + 1)
visor = ndi.binary_fill_holes(ndi.binary_closing(dark_any, iterations=12)) & head & (A > 0.3)
visor = ndi.binary_dilation(visor, iterations=2) & body & head & ~(shell_tmp := np.zeros_like(visor))
hands = dark & ~head & (yy > 300)
hands = ndi.binary_fill_holes(ndi.binary_closing(hands, iterations=4)) & opaque & ~lines
neck = dark & (yy >= 250) & (yy < 360) & (xx > 780) & (xx < 920)
hands &= ~neck
inner = opaque & ~lines & ~visor & ~hands & ~neck
shell = body & ~opaque

# --- 1) Entrauschen (Glühwürmchen und Körnung) ------------------------------
u8 = (rgb * 255).astype(np.uint8)
den = cv2.fastNlMeansDenoisingColored(u8, None, 9, 9, 7, 21).astype(np.float32) / 255
med = cv2.medianBlur(u8, 5).astype(np.float32) / 255
# Ausreißer (Sparkles) gegen Median ersetzen, Rest mit NLM glätten
spark = (np.abs(rgb - med).max(-1) > 0.10) & ~lines
base = np.where(spark[..., None], med, den)
base = np.where(lines[..., None], rgb, base)
# Alpha-Rauschen in der Hülle ebenfalls glätten
A_s = cv2.GaussianBlur(A, (0, 0), 0.8)
A = np.where(shell, A_s, A)

Lb = base @ np.array([0.2126, 0.7152, 0.0722], np.float32)
outc = base.copy()

# --- 2) Hülle: kühler, Fresnel-Alpha ------------------------------------------
# Abstand zum Silhouettenrand des Körpers (inkl. Innenkanten der Teilformen)
sil = cv2.GaussianBlur(body.astype(np.float32), (0, 0), 1.0) > 0.5
d_out = ndi.distance_transform_edt(sil)
# Innenkanten: Teilflächen der Hülle über Helligkeitssprünge
shell_edges = cv2.Canny((cv2.GaussianBlur(Lb, (0, 0), 2.0) * 255).astype(np.uint8), 12, 30) > 0
shell_edges &= shell
d_in = ndi.distance_transform_edt(~shell_edges)
d = d_out
fres = np.exp(-d / 12.0)                       # 1 am Rand, 0 innen
a_shell = 0.15 + (0.55 - 0.15) * fres         # Mitte 15 %, Rand 55 %
shade = np.clip(Lb / max(np.median(Lb[shell]), 1e-3), 0.6, 1.6)
shell_col = SHELL[None, None, :] * shade[..., None] * 0.92 + 0.22 * fres[..., None]
outc = np.where(shell[..., None], shell_col, outc)
A_new = np.where(shell, a_shell, A)

# Blaue Säume entfernen (entsättigen auf Hüllenfarbe)
outc = np.where(fringe[..., None], SHELL[None, None, :] * shade[..., None], outc)

# --- 3) Innenteile abdunkeln: satiniertes Alu #4A515C -----------------------
li = Lb[inner]
li_med = np.median(li) if li.size else 0.5
ishade = np.clip(Lb / li_med, 0.55, 1.5) ** 0.85
outc = np.where(inner[..., None], INNER[None, None, :] * ishade[..., None], outc)

# --- 4) Visier: matt, ohne Glanzfleck -----------------------------------------
vy = np.clip((yy - 60) / 230.0, 0, 1)
vx = np.clip((xx - 700) / 160.0, 0, 1)
vis_col = VISOR[None, None, :] * (1.45 - 0.55 * vy - 0.15 * vx)[..., None]
vis_col = vis_col + 0.06 * np.exp(-((xx - 735) / 18.0) ** 2)[..., None] * (1 - vy)[..., None]
vsoft = np.clip(cv2.GaussianBlur(visor.astype(np.float32), (0, 0), 2.0) * 1.3, 0, 1)
outc = outc * (1 - vsoft[..., None]) + vis_col * vsoft[..., None]
# --- 5) Hände und Hals: dunkel eloxiert #2A2F37 --------------------------------
hshade = np.clip(Lb / max(np.median(Lb[hands]) if hands.any() else 0.25, 1e-3), 0.6, 2.2) ** 0.45
hcol = HAND[None, None, :] * hshade[..., None]
outc = np.where((hands | neck)[..., None], hcol, outc)

# --- 6) Leitungen: Legendenfarben, ungefiltert, heller Kern, dezenter Halo ----
def paint(mask, col, outc, A_new):
    if not mask.any():
        return outc, A_new
    soft = cv2.GaussianBlur(mask.astype(np.float32), (0, 0), 0.6)
    soft = np.clip(soft * 1.6, 0, 1)
    dist = ndi.distance_transform_edt(mask)
    core = np.clip((dist - 1.5) / 2.0, 0, 1)                   # Mitte der Linie
    lv = np.clip(Lb / max(np.median(Lb[mask]), 1e-3), 0.75, 1.15)
    c = col[None, None, :] * lv[..., None]
    c = c + (1 - c) * 0.20 * core[..., None]                   # +20 % Helligkeit im Kern
    outc = outc * (1 - soft[..., None]) + c * soft[..., None]
    A_new = np.maximum(A_new, soft)
    return outc, A_new

for m, c in ((grey_m, GREY), (blue_m, BLUE), (orange_m, ORANGE)):
    outc, A_new = paint(m, c, outc, A_new)

def halo(mask, col, outc, A_new, strength=0.18, sigma=3.0):
    h = cv2.GaussianBlur(mask.astype(np.float32), (0, 0), sigma)
    h = np.clip(h * 2.2, 0, 1) * strength * (~mask)
    outc = outc * (1 - h[..., None]) + col[None, None, :] * h[..., None]
    A_new = np.where(body, np.clip(A_new + h * 0.5, 0, 1), A_new)
    return outc, A_new

outc, A_new = halo(blue_m, BLUE, outc, A_new)
outc, A_new = halo(orange_m, ORANGE, outc, A_new)

# --- 7) Kantenlicht von rechts hinten (#7FA6D9) ----------------------------------
sm = cv2.GaussianBlur(sil.astype(np.float32), (0, 0), 3.0)
gx = cv2.Sobel(sm, cv2.CV_32F, 1, 0, ksize=5)
gy = cv2.Sobel(sm, cv2.CV_32F, 0, 1, ksize=5)
nrm = np.sqrt(gx ** 2 + gy ** 2) + 1e-6
nx, ny = -gx / nrm, -gy / nrm                       # Außennormale
facing = np.clip(nx * 0.93 + (-ny) * 0.37, 0, 1)    # Licht von rechts, leicht oben
band = np.exp(-np.maximum(d_out - 1, 0) / 2.5) * sil  # ca. 1–1,5 pt Breite
rim = band * facing ** 1.5 * 0.75
outc = outc * (1 - rim[..., None]) + RIM[None, None, :] * rim[..., None]
A_new = np.clip(A_new + rim * 0.35, 0, 1)
# Weiche Key-Light-Kante oben links (sehr schwach)
key = band * np.clip(-nx * 0.6 + (-ny) * 0.8, 0, 1) ** 2 * 0.25
outc = outc + (1 - outc) * key[..., None] * 0.6

# --- 8) Beine unten ausblenden (ca. 8 mm = 95 px) --------------------------------
fade = np.clip((H - 1 - yy) / 95.0, 0, 1)
fade = fade * fade * (3 - 2 * fade)
A_new = A_new * fade

A_new = np.where(body | (A_new > 0.01), A_new, 0)
outc = np.clip(outc, 0, 1)
res = np.dstack([outc, np.clip(A_new, 0, 1)])
Image.fromarray((res * 255 + 0.5).astype(np.uint8), 'RGBA').save(out)

# Diagnose
for name, m in (('blue', blue_m), ('orange', orange_m), ('grey', grey_m), ('fringe', fringe),
                ('visor', visor), ('hands', hands), ('inner', inner), ('shell', shell), ('spark', spark)):
    print(f'{name:7s} {int(m.sum()):7d}')
dbg = np.zeros((H, W, 3), np.uint8)
dbg[shell] = (60, 60, 60); dbg[inner] = (140, 140, 140); dbg[visor] = (255, 0, 255)
dbg[hands | neck] = (0, 255, 0); dbg[grey_m] = (255, 255, 255); dbg[blue_m] = (0, 120, 255)
dbg[orange_m] = (255, 120, 0); dbg[fringe] = (255, 0, 0)
Image.fromarray(dbg).save(out.replace('.png', '_masks.png'))
