"""Weißen Hintergrund von Webshop-Produktfotos entfernen (nur randverbundenes Weiß).

Aufruf: python3 freistellen.py <in.png> <out.png>
"""
import sys

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

src, out = sys.argv[1:3]
im = Image.open(src).convert('RGB')
a = np.asarray(im).astype(np.int16)
white = a.min(axis=2) > 245                         # nahezu weiß
lab, _ = ndimage.label(white)
edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
obj = ~np.isin(lab, list(edge))
# Glanzlichter am Umriss (reines Weiß) gehören zum Teil: Kontur schließen, Löcher füllen
yy, xx = np.mgrid[-15:16, -15:16]
obj = ndimage.binary_closing(obj, structure=(xx ** 2 + yy ** 2) <= 225, iterations=1, border_value=0)
obj = ndimage.binary_fill_holes(obj)
bg = ~obj
alpha = Image.fromarray(np.where(bg, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
rgba = im.convert('RGBA'); rgba.putalpha(alpha)
rgba = rgba.crop(rgba.getbbox())
rgba.save(out)
print(out, rgba.size)
