"""Entfernt eingebrannte Doppel-Hinweislinien im aufgewerteten Roboter (Querinterpolation)."""
import sys
import numpy as np, cv2
from PIL import Image
src, out = sys.argv[1:3]
S, OX = 2, 430                                    # Roboter_HQ: 2x Entwurf, Ursprung x=430
im = np.array(Image.open(src).convert('RGBA')).astype(np.float32)
rgb = im[..., :3].copy()
SEGS = [((814, 272), (934, 180), 6.5)]            # Brust: Linie zum VT5528-Tag (Entwurfskoordinaten, halbe Breite)
for (ax, ay), (bx, by), w in SEGS:
    a = np.array([(ax - OX) * S, ay * S], np.float32); b = np.array([(bx - OX) * S, by * S], np.float32)
    L = float(np.linalg.norm(b - a)); d = (b - a) / L; n = np.array([-d[1], d[0]], np.float32); W = w * S
    ts = np.arange(10, L - 6, 0.5)
    cen = a[None] + d[None] * ts[:, None]
    def samp(P):
        return np.stack([cv2.remap(np.ascontiguousarray(rgb[..., c]), P[:, 0][None].astype(np.float32), P[:, 1][None].astype(np.float32), cv2.INTER_LINEAR)[0] for c in range(3)], -1)
    cl = samp(cen - n * (W + 2)); cr = samp(cen + n * (W + 2))
    for o in np.arange(-W, W + 0.01, 0.5):
        P = cen + n * o; t = (o + W + 2) / (2 * W + 4)
        val = cl * (1 - t) + cr * t
        xi = np.round(P[:, 0]).astype(int); yi = np.round(P[:, 1]).astype(int)
        im[yi, xi, :3] = val
Image.fromarray(np.clip(im, 0, 255).astype(np.uint8), 'RGBA').save(out)
print('ok')
