"""Eingebrannte Hinweislinien, Marker und Text vom Roboter entfernen und freistellen."""
import sys
import numpy as np, cv2
from PIL import Image
from scipy import ndimage as ndi
src, out = sys.argv[1:3]
im = np.array(Image.open(src).convert('RGB'))
X0, Y0, X1, Y1 = 790, 0, 2000, 1096
im = im[Y0:Y1, X0:X1].copy()
f = im.astype(np.float32)
R, G, B = f[..., 0], f[..., 1], f[..., 2]
V = f.max(-1) / 255
navy = (B > R + 22) & (B > G + 8) & (V < 0.62)
thick = cv2.morphologyEx(navy.astype(np.uint8), cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))) > 0
thick = ndi.binary_dilation(thick, iterations=2)
lines = navy & ~thick
lab, n = ndi.label(lines, structure=np.ones((3, 3)))
sz = ndi.sum(lines, lab, range(1, n + 1))
lines = np.isin(lab, np.where(sz > 25)[0] + 1)
mask = ndi.binary_dilation(lines, iterations=2)
# Marker-Ringe: nur Ring-/Punktpixel (kräftiges Blau oder Weiß) im Umkreis ersetzen
yy, xx = np.mgrid[0:im.shape[0], 0:im.shape[1]]
for (cx, cy) in ((1610, 360), (1373, 530), (885, 1065)):
    d = np.hypot(xx - (cx - X0), yy - (cy - Y0))
    ring = (d < 16) & (((B > R + 45) & (V > 0.45)) | (f.min(-1) > 215))
    mask |= ndi.binary_dilation(ring, iterations=2) & (d < 19)
# Text über dem Unterarm: nur graublaue Textpixel
tr = np.zeros_like(mask); tr[960 - Y0:998 - Y0, 836 - X0:964 - X0] = True
txt = tr & (f.mean(-1) > 52) & (f.mean(-1) < 225) & (B >= R + 3)
mask |= ndi.binary_dilation(txt, iterations=2) & tr
cleaned = cv2.inpaint(im, mask.astype(np.uint8), 4, cv2.INPAINT_TELEA)
# Rechte Brustverschraubung vom linken Zwilling klonen (gleiche Bauform, 35 px versetzt)
sx0, sy0, sx1, sy1 = 541, 500, 575, 557
patch = cleaned[sy0:sy1, sx0:sx1].astype(np.float32)
dx = 31
tgt = cleaned[sy0:sy1, sx0 + dx:sx1 + dx].astype(np.float32)
h, w = patch.shape[:2]
fy = np.minimum(np.arange(h), np.arange(h)[::-1]) / 6.0
fx = np.minimum(np.arange(w), np.arange(w)[::-1]) / 6.0
feather = np.clip(np.minimum.outer(fy, fx), 0, 1)[..., None]
cleaned[sy0:sy1, sx0 + dx:sx1 + dx] = (patch * feather + tgt * (1 - feather)).astype(np.uint8)
Image.fromarray(mask.astype(np.uint8) * 255).save(out.replace('.png', '_mask.png'))
# Freistellen
mn = cleaned.astype(np.float32).min(-1)
fg = mn < 244
lab, n = ndi.label(fg)
sz = ndi.sum(fg, lab, range(1, n + 1))
fg = lab == (np.argmax(sz) + 1)
fg = ndi.binary_fill_holes(cv2.morphologyEx(fg.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8)) > 0)
soft = np.clip((252 - mn) / 22, 0, 1)
edge = ndi.binary_dilation(fg, iterations=2) & ~ndi.binary_erosion(fg, iterations=2)
alpha = np.where(ndi.binary_erosion(fg, iterations=2), 1.0, np.where(edge, soft, 0.0))
alpha = cv2.GaussianBlur(alpha.astype(np.float32), (0, 0), 0.6)
alpha[-3:, :] = np.where(fg[-3:, :], 1.0, alpha[-3:, :])
rgba = np.dstack([cleaned, (alpha * 255).astype(np.uint8)])
Image.fromarray(rgba, 'RGBA').save(out)
ys, xs = np.where(alpha > 0.5)
print('bbox', xs.min(), ys.min(), xs.max(), ys.max(), 'size', rgba.shape, 'removed px', int(mask.sum()))
