"""Freistellen eines KI-Roboterbildes (x4 aufgewertet) vor weißem Hintergrund, ohne Tag-Masken.
Aufruf: matte_robot.py <robot_x4.png> <out_rgba.png>   (Ausschnitt ab x=430 im Entwurf)"""
import sys
import numpy as np, cv2
from PIL import Image
from scipy import ndimage as ndi
src, out = sys.argv[1:3]
S, OX = 4, 430
im = np.array(Image.open(src).convert('RGB'))
f = im.astype(np.float32)
H, W = im.shape[:2]
mn = f.min(-1)
fg = mn < 236
fg = cv2.morphologyEx(fg.astype(np.uint8), cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))) > 0
lab, n = ndi.label(fg); sz = ndi.sum(fg, lab, range(1, n + 1))
mean_mn = ndi.mean(mn, lab, range(1, n + 1))
keep = np.where((sz > max(40000, 0.004 * sz.max())) & (np.array(mean_mn) < 170))[0] + 1   # helle Hintergrundflächen verwerfen
fg = np.isin(lab, keep)   # alle großen Teile (Arm, Hand) behalten
print('Teile', len(keep))
fg = ndi.binary_fill_holes(cv2.morphologyEx(fg.astype(np.uint8), cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21))) > 0)
inner = ndi.binary_erosion(fg, iterations=5)
band = ndi.binary_dilation(fg, iterations=5) & ~inner
soft = np.clip((248 - mn) / 30, 0, 1)
alpha = np.where(inner, 1.0, np.where(band, soft, 0.0)).astype(np.float32)
alpha = cv2.GaussianBlur(alpha, (0, 0), 1.2)
alpha[-6:] = np.where(fg[-6:], 1.0, alpha[-6:])
# weißen Saum aus halbtransparenten Kanten herausrechnen
a3 = np.clip(alpha, 0.06, 1)[..., None]
bgc = 249.0
dec = np.clip((f - bgc * (1 - a3)) / a3, 0, 255)
f2 = np.where(((alpha > 0.02) & (alpha < 0.98))[..., None], dec, im.astype(np.float32))
rgba = np.dstack([f2.astype(np.uint8), (alpha * 255).astype(np.uint8)])
img = Image.fromarray(rgba, 'RGBA').resize((W // 2, H // 2), Image.LANCZOS)   # 2x Entwurf = ca. 340 dpi bei 864 pt Breite
img.save(out)
print('ok', img.size)
