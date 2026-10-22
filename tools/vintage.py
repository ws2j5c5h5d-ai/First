"""Vintage-Zeitungslook (vergilbtes Zeitungspapier, Ende 1970er) und A3-Druckversion.
python3 tools/vintage.py <eingabe.png> <ausgabe-ohne-endung> [seed]
Ergebnis: <ausgabe>.pdf (A3, 300 dpi) und <ausgabe>_vorschau.jpg"""
import sys
import numpy as np
from PIL import Image, ImageFilter

A3 = (3508, 4961)                      # 297 x 420 mm bei 300 dpi
src, out = sys.argv[1], sys.argv[2]
rng = np.random.default_rng(int(sys.argv[3]) if len(sys.argv) > 3 else 1979)

def blurred_noise(shape, sigma, small=8):
    h, w = shape
    n = rng.random((h // small + 2, w // small + 2)).astype(np.float32)
    im = Image.fromarray((n * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(sigma / small))
    im = im.resize((w, h), Image.BICUBIC)
    a = np.asarray(im, np.float32) / 255
    return (a - a.min()) / (np.ptp(a) + 1e-6)

W, H = A3
# Inhalt auf A3 einpassen, umlaufend ca. 7 mm Rand
page = Image.open(src).convert('L')
m = 85
s = min((W - 2 * m) / page.width, (H - 2 * m) / page.height)
page = page.resize((round(page.width * s), round(page.height * s)), Image.LANCZOS)
canvas = Image.new('L', A3, 255)
canvas.paste(page, ((W - page.width) // 2, (H - page.height) // 2))
# leichtes Verlaufen der Druckfarbe
canvas = canvas.filter(ImageFilter.GaussianBlur(0.9))
ink = 1 - np.asarray(canvas, np.float32) / 255           # 0 = Papier, 1 = volle Farbe

# Papier: Grundton, Wolkigkeit, Fasern, dunklere Ränder
y, x = np.mgrid[0:H, 0:W].astype(np.float32)
cloud = blurred_noise((H, W), 260)
fine = rng.normal(0, 1, (H, W)).astype(np.float32)
edge = np.minimum.reduce([x, W - x, y, H - y]) / 420
vign = np.clip(1 - edge, 0, 1) ** 2
tone = 0.55 * cloud + 0.9 * vign                         # 0 = hell, >1 = stark vergilbt
paper = np.stack([
    238 - 14 * tone + 2.2 * fine,
    228 - 22 * tone + 2.2 * fine,
    200 - 38 * tone + 2.2 * fine], -1)

# Stockflecken (Foxing)
for _ in range(rng.integers(10, 18)):
    cx, cy, r = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(15, 70)
    d = np.exp(-(((x - cx) ** 2 + (y - cy) ** 2) / (2 * r * r)))
    paper -= d[..., None] * np.array([18, 26, 34]) * rng.uniform(0.4, 1)
# Knickfalte in der Mitte
fold = np.exp(-((y - H / 2) ** 2) / (2 * 6 ** 2))
paper -= fold[..., None] * np.array([14, 16, 20])
paper += np.exp(-((y - H / 2 - 9) ** 2) / (2 * 5 ** 2))[..., None] * 6

# Druckfarbe: nicht ganz schwarz, ungleichmäßig, leicht durchgedruckt
inkcol = np.array([38, 34, 30], np.float32)
uneven = 0.86 + 0.14 * blurred_noise((H, W), 40, 4)
grain = np.clip(1 - 0.18 * rng.random((H, W)).astype(np.float32), 0, 1)
a = np.clip(ink * uneven * grain * 0.97, 0, 1)[..., None]
img = paper * (1 - a) + inkcol * a
img = np.clip(img, 0, 255).astype(np.uint8)
res = Image.fromarray(img, 'RGB')
res.save(out + '.pdf', 'PDF', resolution=300, quality=90)
res.resize((W // 4, H // 4), Image.LANCZOS).save(out + '_vorschau.jpg', quality=88)
print(out, 'ok')
