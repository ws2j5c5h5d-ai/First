"""Erweitert das (x4) Roboterbild per Randwiederholung auf das volle A4-Seitenformat."""
import sys
import numpy as np, cv2
from PIL import Image
src, out = sys.argv[1:3]
SC = 4; S = 0.476; OX, OY = 10.5, 59.0; PW, PH = 595.28, 841.89
im = np.array(Image.open(src).convert('RGB'))
px = SC / S                                       # Bildpixel je pt
l, t = int(round(OX * px)), int(round(OY * px))
W, H = int(round(PW * px)), int(round(PH * px))
r, b = W - l - im.shape[1], H - t - im.shape[0]
pad = cv2.copyMakeBorder(im, t, b, l, r, cv2.BORDER_REPLICATE)
# Randwiederholung leicht glätten, damit keine Streifen entstehen
mask = np.ones(pad.shape[:2], np.float32); mask[t:t + im.shape[0], l:l + im.shape[1]] = 0
bl = cv2.GaussianBlur(pad, (0, 0), 40)
m = cv2.GaussianBlur(mask, (0, 0), 30)[..., None]
outim = (pad * (1 - m) + bl * m).astype(np.uint8)
img = Image.fromarray(outim).resize((2480, 3508), Image.LANCZOS)   # 300 dpi A4
img.save(out, optimize=True)
print('ok', outim.shape, 'dpi', round(px * 72))
