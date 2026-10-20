"""Neue Seite 1: Poster (oben, Navy) + Programmübersicht/VORTEILE/BAUWEISEN/Fußzeile
der bisherigen Seite 1 (unten, 1:1 als Vektor aus der korrigierten PDF).

Aufruf: python3 baue_seite1.py <seiten1-6_korr.pdf> <roboter_quelle.png> <produkte_dir> <logo_navy.pdf> <out.pdf>
Ausgabe: 6-seitige PDF (neue Seite 1 + bisherige Seiten 2–6).
"""
import io
import sys

import numpy as np
import pymupdf
from PIL import Image, ImageFilter

korr, robot_src, P, logo_pdf, out = sys.argv[1:6]
PW, PH = 595.28, 841.89
CUT = 425.2                                   # Oberkante grauer Übersichtsband (aus Quelldatei)
NAVY = (0x0b / 255, 0x33 / 255, 0x5e / 255)   # #0B335E, Flyer-Quelldatei (Footer-/Blockfarbe)
WHITE, SOFT, LINE, ACC = (1, 1, 1), (0.725, 0.796, 0.886), (0.498, 0.737, 1.0), (0.122, 0.435, 0.82)
BLUE, ORANGE, AIR = (0.184, 0.549, 1.0), (0.941, 0.478, 0.118), (0.902, 0.925, 0.957)
REG = 'fonts/texgyreheros-regular.otf'
BOLD = 'fonts/texgyreheros-bold.otf'

src = pymupdf.open(korr)
doc = pymupdf.open()
doc.insert_pdf(src)
p = doc[0]

# 1) Oberen Teil der alten Seite 1 entfernen (Titel, Headline, Bilder, Badge, Logo)
p.add_redact_annot(pymupdf.Rect(0, 0, PW, CUT - 0.3), fill=False)
p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_REMOVE,
                   graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED,
                   text=pymupdf.PDF_REDACT_TEXT_REMOVE)
p.insert_font(fontname='hr', fontfile=REG)
p.insert_font(fontname='hb', fontfile=BOLD)
F_R, F_B = pymupdf.Font(fontfile=REG), pymupdf.Font(fontfile=BOLD)

# 2) Poster-Hintergrund (Navy-Verlauf wie Roboterbild) – Grundfarbe aus dem Bildrand
im = Image.open(robot_src).convert('RGB')
arr = np.asarray(im).astype(np.float32)
edge = np.concatenate([arr[:40].reshape(-1, 3), arr[:, :40].reshape(-1, 3), arr[:, -40:].reshape(-1, 3)])
base = tuple((np.median(edge, 0) / 255).tolist())
p.draw_rect(pymupdf.Rect(0, 0, PW, CUT), color=None, fill=base, overlay=True)

# Roboterbild mit weicher Randausblendung (keine sichtbaren Bildkanten)
S = 0.31                                      # pt je Pixel der Entwurfsquelle 765 x 1024
OX, OY = 170.7, 112.0
w, h = im.size
k = w / 765.0                                 # Quellpixel je Entwurfspixel (x4-Version: 4)
# Bild unten an der Bandkante abschneiden (statt Abdeckfläche), damit die Übersicht sichtbar bleibt
h_keep = min(h, int((CUT - 0.5 - OY) / S * k))
rgba = im.crop((0, 0, w, h_keep)).convert('RGBA')
hh = h_keep
yy, xx = np.mgrid[0:hh, 0:w].astype(np.float32)
fx = np.clip(np.minimum(xx, w - 1 - xx) / (90.0 * k), 0, 1)
fy = np.clip(np.minimum(yy, hh - 1 - yy) / (90.0 * k), 0, 1)
a = (np.minimum(fx, fy) ** 1.5 * 255).astype(np.uint8)
del xx, yy, fx, fy
rgba.putalpha(Image.fromarray(a))
bio = io.BytesIO(); rgba.save(bio, 'PNG'); bio.seek(0)
img_rect = pymupdf.Rect(OX, OY, OX + w / k * S, OY + hh / k * S)
p.insert_image(img_rect, stream=bio.getvalue(), overlay=True)


def R(x, y):
    return OX + x * S, OY + y * S


def text(x, y, s, size, col, bold=False, align='l'):
    f = F_B if bold else F_R
    wd = f.text_length(s, fontsize=size)
    if align == 'c':
        x -= wd / 2
    elif align == 'r':
        x -= wd
    p.insert_text((x, y), s, fontname='hb' if bold else 'hr', fontsize=size, color=col, overlay=True)


def leader(pts):
    for col, wd in (((0.024, 0.086, 0.173), 3.0), (LINE, 0.9)):
        sh = p.new_shape()
        sh.draw_polyline([pymupdf.Point(*q) for q in pts])
        sh.finish(color=col, width=wd, lineCap=1, lineJoin=1, closePath=False)
        sh.commit(overlay=True)


def marker(x, y):
    p.draw_circle((x, y), 4.2, color=ACC, fill=WHITE, width=1.4, overlay=True)
    p.draw_circle((x, y), 1.7, color=None, fill=ACC, overlay=True)


def tile(name, cx, cy, r, label):
    p.draw_circle((cx, cy), r + 3.5, color=None, fill=(1, 1, 1), fill_opacity=0.10, overlay=True)
    p.draw_circle((cx, cy), r, color=LINE, fill=WHITE, width=0.7, overlay=True)
    pim = Image.open(f'{P}/{name}.png'); iw, ih = pim.size; s = (r * 1.45) / max(iw, ih)
    p.insert_image(pymupdf.Rect(cx - iw * s / 2, cy - ih * s / 2, cx + iw * s / 2, cy + ih * s / 2),
                   filename=f'{P}/{name}.png', overlay=True)
    text(cx, cy + r + 9.5, label, 6.6, WHITE, True, 'c')


# 3) Kopf
p.draw_rect(pymupdf.Rect(32, 36, 36, 98), color=None, fill=WHITE, overlay=True)
text(46, 60, 'PROGRAMM', 25, WHITE, True)
text(46, 89, 'HUMANOIDE ROBOTER', 25, WHITE, True)
text(46, 113, 'EXTREM KLEINBAUEND. AB M3 UND AD3.', 11.5, SOFT, True)
# Logo-Feld: Navy #0B335E (statt Weiß), Logo als Vektor
LX0, LY0, LX1, LY1 = 405, 30, 560, 86          # Logobox in der Quelldatei
TW = 112
TH = TW * (LY1 - LY0) / (LX1 - LX0)
fx0, fy0 = 563.3 - 126, 34
p.draw_rect(pymupdf.Rect(fx0, fy0, fx0 + 126, fy0 + TH + 14), color=None, fill=NAVY, overlay=True)
lg = pymupdf.open(logo_pdf)
p.show_pdf_page(pymupdf.Rect(fx0 + 7, fy0 + 7, fx0 + 7 + TW, fy0 + 7 + TH), lg, 0,
                clip=pymupdf.Rect(LX0, LY0, LX1, LY1), overlay=True)

# 4) Callouts (Einbauorte wie zuvor geprüft)
TX = 549
m = R(523, 350)
tile('p_vt5528', TX, 168, 17, 'VT5528-0202'); leader([(TX - 17, 168), (520, 168), m]); marker(*m)
m = R(528, 438)
tile('p_sa2113', TX, 225, 17, 'SA2113-1'); tile('p_sa2113_2', TX, 282, 17, 'SA2113-2')
leader([(TX - 17, 225), (520, 225), (520, 282), (TX - 17, 282)]); leader([(520, 253.5), m]); marker(*m)
mh, mk = R(568, 518), R(468, 700)
tile('p_vt5528', TX, 345, 17, 'VT5528-0202')
leader([(TX - 17, 345), (520, 345), mh]); leader([(520, 345), (520, 385), (mk[0] + 30, 385), mk]); marker(*mh); marker(*mk)
m = R(171, 426)
for i, (nm, lab) in enumerate((('p_863', '863-4218'), ('p_887', '887-4218'), ('p_529', '529-5018G'))):
    tile(nm, 62 + i * 50, 300, 17, lab)
leader([(62, 283), (62, 270), (162, 270), (162, 283)]); leader([(112, 283), (112, 270)]); leader([(112, 270), m]); marker(*m)

# Legende + Hinweis
for i, (lab, col) in enumerate((('Kühlwasser Vorlauf', BLUE), ('Kühlwasser Rücklauf', ORANGE), ('Druckluft / Vakuum', AIR))):
    yy_ = 352 + i * 12.5
    p.draw_line((46, yy_ - 2.5), (60, yy_ - 2.5), color=col, width=2.2, lineCap=1, overlay=True)
    text(66, yy_, lab, 7.0, SOFT)
text(46, 414, 'Konzeptdarstellung, KI-gestützte Visualisierung. Einbauorte beispielhaft.', 6.0, (0.6, 0.68, 0.78))

# 5) Seitenzahl-Format der Quelle beibehalten ("1 / 6" ist bereits gesetzt)

doc.save(out, garbage=3, deflate=True)
print('ok', out, len(doc), 'Seiten')
