"""Konstruierte Vektor-Illustration des Phantom-Roboters (technischer Stil).
Koordinaten in Vorlagenpixeln (2339 x 3118 px), abgelesen aus der Rastervorlage.
draw_robot(c, K, PH, dx, dy, s) zeichnet in ein reportlab-Canvas.
"""
from reportlab.lib.colors import Color


def hx(h, a=1.0):
    return Color(*(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)), alpha=a)


SHELL_FILL = hx('#8FA6C8', 0.055)
SHELL_GLOW = hx('#7FA6D9', 0.10)
SHELL_LINE = hx('#B4CAE9', 0.92)
SEAM = hx('#8EA3C2', 0.45)
PART_A, PART_B = hx('#6E7A8C'), hx('#444E5D')
PART_LINE = hx('#A3AFC1')
PART_HI = hx('#C9D3E1', 0.55)
DARK, DARK_LINE = hx('#141C2A'), hx('#6A7C97')
BLUE, BLUE_HI = hx('#2F8CFF'), hx('#9CC8FF')
ORANGE, ORANGE_HI = hx('#FF7A2E'), hx('#FFC29A')
GREY, GREY_HI = hx('#D5D9DF'), hx('#FFFFFF')

# ---------------------------------------------------------------- Geometrie
HEAD = (1640, 700, 172, 208)                       # Ellipse cx, cy, rx, ry
CRANIUM = [(1640, 492), (1735, 508), (1798, 570), (1818, 680), (1802, 790), (1752, 865),
           (1690, 902), (1612, 904), (1540, 882), (1486, 828), (1462, 730), (1472, 625),
           (1520, 540), (1578, 503)]
FACE = [(1478, 650), (1510, 572), (1572, 538), (1628, 548), (1660, 610), (1668, 720),
        (1652, 818), (1612, 872), (1552, 880), (1500, 846), (1476, 760)]
VISOR = [(1478, 640), (1520, 560), (1600, 540), (1640, 590), (1650, 720),
         (1632, 850), (1590, 885), (1520, 870), (1478, 790)]
NECK = (1612, 890, 1712, 995)
TORSO = [(1445, 1000), (1560, 965), (1665, 960), (1770, 965), (1885, 1000),
         (1905, 1080), (1870, 1220), (1835, 1360), (1825, 1440), (1490, 1440),
         (1478, 1360), (1450, 1220), (1425, 1080)]
WAIST = (1468, 1440, 1846, 1660)
PELVIS = [(1468, 1665), (1842, 1665), (1858, 1765), (1832, 1905), (1478, 1905), (1452, 1765)]
LEG_L = (1460, 1880, 1650, 2300)
LEG_R = (1655, 1890, 1858, 2300)
ARM_L = [((1420, 1050), (1150, 1385), 74), ((1150, 1385), (790, 1560), 60)]
ARM_R = [((1985, 1070), (1995, 1545), 70), ((1995, 1545), (1945, 1975), 60)]
JOINTS = [(1420, 1050, 58), (1150, 1390, 54), (1985, 1075, 62), (1995, 1545, 56)]
HIP_PUCKS = [(1600, 1918, 84, 92), (1818, 1958, 84, 92)]
BOXES = [  # x0, y0, x1, y1, Radius
    (1552, 1150, 1755, 1330, 12),               # Verteiler (Einzelheit A)
    (1560, 1330, 1622, 1392, 8), (1612, 1356, 1712, 1408, 8),
    (1758, 1350, 1822, 1432, 8),
    (1540, 1440, 1842, 1600, 14),               # Pumpe / Akku
    (1958, 1225, 2026, 1352, 10), (1962, 1690, 2024, 1825, 10),
]
ARM_PARTS = [((1330, 1150), (1250, 1255), 34), ((1040, 1450), (930, 1505), 30)]
PORTS = [(1598, 1150), (1690, 1150)]           # Anschlussstutzen am Verteiler

# Leitungen: Bézierpfade (Liste aus Segmenten p0, c1, c2, p1)
TUBES = {
    'blue': [
        [((1610, 1138), (1606, 1100), (1612, 1060), (1625, 1000)), ((1625, 1000), (1635, 960), (1645, 930), (1650, 900))],
        [((1440, 1075), (1360, 1170), (1260, 1290), (1170, 1395))],
        [((1170, 1395), (1060, 1450), (950, 1500), (820, 1548))],
        [((1590, 1600), (1580, 1680), (1585, 1760), (1592, 1835))],
        [((1782, 1600), (1790, 1690), (1800, 1790), (1808, 1870))],
        [((2008, 1100), (2010, 1160), (2010, 1210), (2008, 1225))],
        [((1965, 1095), (1900, 1170), (1840, 1260), (1815, 1340))],
    ],
    'orange': [
        [((1690, 1138), (1690, 1060), (1770, 1050), (1785, 1120)), ((1785, 1120), (1800, 1200), (1790, 1290), (1790, 1350))],
        [((1790, 1432), (1792, 1440), (1795, 1445), (1800, 1450))],
        [((1418, 1060), (1340, 1160), (1250, 1270), (1155, 1380))],
        [((1612, 1600), (1605, 1680), (1606, 1760), (1612, 1835))],
        [((1760, 1600), (1768, 1690), (1780, 1790), (1790, 1875))],
        [((1950, 1090), (1885, 1170), (1825, 1260), (1800, 1350))],
    ],
    'grey': [
        [((1455, 1035), (1500, 1060), (1540, 1110), (1570, 1150))],
        [((1400, 1030), (1250, 1190), (1080, 1360), (900, 1500)), ((900, 1500), (860, 1530), (830, 1545), (800, 1555))],
        [((1965, 1080), (1960, 1300), (1972, 1600), (1958, 1975))],
        [((1720, 960), (1730, 1020), (1745, 1080), (1748, 1150))],
    ],
}
TUBE_W = {'blue': 3.4, 'orange': 3.4, 'grey': 2.2}   # in pt bei Maßstab 1


def draw_robot(c, K, PH, dx=0.0, dy=0.0, s=1.0, legs=True):
    """dx, dy: Versatz in pt (von oben); s: Vergrößerung."""
    u = 1.0 / (K * s)                    # pt -> lokale Pixeleinheit
    c.saveState()
    c.transform(K * s, 0, 0, -K * s, dx, PH - dy)
    c.setLineJoin(1); c.setLineCap(1)

    def path_poly(pts, close=True):
        p = c.beginPath(); p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        if close:
            p.close()
        return p

    def smooth_poly(pts):
        # geschlossene Catmull-Rom-Kurve -> Bézier
        p = c.beginPath(); n = len(pts)
        p.moveTo(*pts[0])
        for i in range(n):
            p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
            c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
            c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
            p.curveTo(*c1, *c2, *p2)
        p.close()
        return p

    def capsule(a, b, r):
        import math
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        nx, ny = -math.sin(ang), math.cos(ang)
        p = c.beginPath()
        p.moveTo(a[0] + nx * r, a[1] + ny * r)
        p.lineTo(b[0] + nx * r, b[1] + ny * r)
        deg = math.degrees(ang)
        p.arcTo(b[0] - r, b[1] - r, b[0] + r, b[1] + r, startAng=deg + 90, extent=-180)
        p.lineTo(a[0] - nx * r, a[1] - ny * r)
        p.arcTo(a[0] - r, a[1] - r, a[0] + r, a[1] + r, startAng=deg - 90, extent=-180)
        p.close()
        return p

    def shell(p):
        c.setFillColor(SHELL_FILL); c.drawPath(p, stroke=0, fill=1)
        c.setStrokeColor(SHELL_GLOW); c.setLineWidth(4.5 * u); c.drawPath(p, stroke=1, fill=0)
        c.setStrokeColor(SHELL_LINE); c.setLineWidth(0.7 * u); c.drawPath(p, stroke=1, fill=0)

    def part_rect(x0, y0, x1, y1, r):
        c.setFillColor(PART_B); c.setStrokeColor(PART_LINE); c.setLineWidth(0.5 * u)
        c.roundRect(x0, y0, x1 - x0, y1 - y0, r, stroke=1, fill=1)
        c.setFillColor(PART_A)
        c.roundRect(x0 + 2 * u, y0 + 2 * u, x1 - x0 - 4 * u, (y1 - y0) * 0.38, r * 0.8, stroke=0, fill=1)
        c.setStrokeColor(PART_HI); c.setLineWidth(0.45 * u)
        c.line(x0 + r, y0 + 3 * u, x1 - r, y0 + 3 * u)

    # ---- Hülle (hinten nach vorne)
    if legs:
        for (x0, y0, x1, y1) in (LEG_L, LEG_R):
            p = c.beginPath(); p.moveTo(x0, y1); p.lineTo(x0 + 6, y0 + 40)
            p.curveTo(x0 + 10, y0, x1 - 10, y0, x1 - 6, y0 + 40); p.lineTo(x1, y1)
            shell(p)
            # Bruchlinie (Darstellung abgebrochen)
            w = c.beginPath(); w.moveTo(x0 - 6, y1)
            q = (x1 - x0 + 12) / 4
            for k in range(4):
                xa = x0 - 6 + q * k
                w.curveTo(xa + q * 0.3, y1 - 14, xa + q * 0.7, y1 + 14, xa + q, y1)
            c.setStrokeColor(SHELL_LINE); c.setLineWidth(0.7 * u); c.drawPath(w, stroke=1, fill=0)
    pv = c.beginPath(); pv.moveTo(1490, 1665); pv.lineTo(1820, 1665)
    pv.curveTo(1842, 1665, 1852, 1680, 1855, 1700); pv.lineTo(1862, 1820)
    pv.curveTo(1864, 1880, 1840, 1905, 1800, 1905); pv.lineTo(1510, 1905)
    pv.curveTo(1470, 1905, 1446, 1880, 1448, 1820); pv.lineTo(1455, 1700)
    pv.curveTo(1458, 1680, 1468, 1665, 1490, 1665); pv.close()
    shell(pv)
    shell(path_poly([(WAIST[0], WAIST[1]), (WAIST[2], WAIST[1]), (WAIST[2] + 8, (WAIST[1] + WAIST[3]) / 2),
                     (WAIST[2], WAIST[3]), (WAIST[0], WAIST[3]), (WAIST[0] - 8, (WAIST[1] + WAIST[3]) / 2)]))
    shell(smooth_poly(TORSO))
    p = c.beginPath(); p.moveTo(1618, 885); p.lineTo(1706, 885)
    p.curveTo(1708, 930, 1716, 950, 1740, 968); p.lineTo(1586, 968); p.curveTo(1608, 950, 1616, 930, 1618, 885); p.close()
    c.setFillColor(SHELL_FILL); c.drawPath(p, stroke=0, fill=1)
    for side in ((1618, 885, 1616, 930, 1608, 950, 1586, 968), (1706, 885, 1708, 930, 1716, 950, 1740, 968)):
        q = c.beginPath(); q.moveTo(side[0], side[1]); q.curveTo(*side[2:])
        c.setStrokeColor(SHELL_GLOW); c.setLineWidth(4.5 * u); c.drawPath(q, stroke=1, fill=0)
        c.setStrokeColor(SHELL_LINE); c.setLineWidth(0.7 * u); c.drawPath(q, stroke=1, fill=0)
    for a, b, r in ARM_R:
        shell(capsule(a, b, r))
    for a, b, r in ARM_L:
        shell(capsule(a, b, r))
    shell(smooth_poly(CRANIUM))

    # Nähte / Segmentfugen der Hülle
    c.setStrokeColor(SEAM); c.setLineWidth(0.45 * u)
    c.saveState(); c.clipPath(smooth_poly(TORSO), stroke=0, fill=0)
    for y in (1180, 1330):
        c.line(1400, y, 1950, y)
    c.restoreState()
    c.line(1655, 1720, 1655, 1900)
    c.line(1472, 1550, 1842, 1550)

    # ---- Bauteile
    for a, b, r in ARM_PARTS:
        p = capsule(a, b, r)
        c.setFillColor(PART_B); c.setStrokeColor(PART_LINE); c.setLineWidth(0.5 * u); c.drawPath(p, stroke=1, fill=1)
    for bx in BOXES:
        part_rect(*bx)
    for (x, y) in PORTS:
        c.setFillColor(PART_A); c.setStrokeColor(PART_LINE); c.setLineWidth(0.5 * u)
        c.roundRect(x - 16, y - 26, 32, 28, 4, stroke=1, fill=1)
    for (x, y, rx, ry) in HIP_PUCKS:
        c.setFillColor(PART_B); c.setStrokeColor(PART_LINE); c.setLineWidth(0.5 * u)
        c.ellipse(x - rx, y - ry, x + rx, y + ry, stroke=1, fill=1)
        c.setFillColor(PART_A); c.ellipse(x - rx * 0.62, y - ry * 0.62, x + rx * 0.62, y + ry * 0.62, stroke=0, fill=1)
        c.setStrokeColor(PART_HI); c.setLineWidth(0.45 * u)
        c.ellipse(x - rx * 0.62, y - ry * 0.62, x + rx * 0.62, y + ry * 0.62, stroke=1, fill=0)
        c.setFillColor(PART_LINE); c.circle(x, y, 9, stroke=0, fill=1)

    # ---- Leitungen
    for key, col, hi in (('grey', GREY, GREY_HI), ('blue', BLUE, BLUE_HI), ('orange', ORANGE, ORANGE_HI)):
        for segs in TUBES[key]:
            p = c.beginPath(); p.moveTo(*segs[0][0])
            for (_, c1, c2, p1) in segs:
                p.curveTo(*c1, *c2, *p1)
            c.setStrokeColor(hx('#0A1220', 0.55)); c.setLineWidth((TUBE_W[key] + 1.4) * u); c.drawPath(p, stroke=1, fill=0)
            c.setStrokeColor(col); c.setLineWidth(TUBE_W[key] * u); c.drawPath(p, stroke=1, fill=0)
            c.setStrokeColor(hi); c.setLineWidth(TUBE_W[key] * u * 0.24); c.drawPath(p, stroke=1, fill=0)

    # ---- Gelenke (vor den Leitungen, Leitungen laufen hindurch)
    for (x, y, r) in JOINTS:
        c.setFillColor(PART_B); c.setStrokeColor(PART_LINE); c.setLineWidth(0.5 * u)
        c.circle(x, y, r, stroke=1, fill=1)
        c.setFillColor(PART_A); c.circle(x, y, r * 0.64, stroke=0, fill=1)
        c.setStrokeColor(PART_HI); c.setLineWidth(0.45 * u); c.circle(x, y, r * 0.64, stroke=1, fill=0)
        c.setFillColor(PART_LINE); c.circle(x, y, r * 0.16, stroke=0, fill=1)

    # ---- Kopf: Gesichtsscheibe, Sensor, Ohrmodul, Fugen, Halsringe
    _head_details(c, u, smooth_poly)
    _hand(c, u, (790, 1560), (530, 1700), flip=False)
    _hand(c, u, (1945, 1975), (1860, 2230), flip=True)
    c.restoreState()


def _rect_path(c, r):
    p = c.beginPath(); p.rect(r[0], r[1], r[2] - r[0], r[3] - r[1]); return p


def _head_details(c, u, smooth_poly):
    # Halsringe
    c.setStrokeColor(SEAM); c.setLineWidth(0.5 * u)
    for y in (912, 930, 948):
        c.line(1624, y, 1704, y)
    # Fugen am Schädel (hinter der Gesichtsscheibe)
    p = c.beginPath(); p.moveTo(1596, 498); p.curveTo(1690, 516, 1762, 600, 1774, 700)
    p.curveTo(1782, 790, 1752, 858, 1700, 896); c.drawPath(p, stroke=1, fill=0)
    p = c.beginPath(); p.moveTo(1560, 884); p.curveTo(1630, 862, 1705, 852, 1772, 842)
    c.drawPath(p, stroke=1, fill=0)
    # Ohrmodul (Gelenk-/Sensoreinheit), in 3/4-Ansicht
    c.setStrokeColor(SEAM); c.ellipse(1700, 625, 1790, 775, stroke=1, fill=0)
    c.setFillColor(PART_B); c.setStrokeColor(PART_LINE); c.setLineWidth(0.5 * u)
    c.ellipse(1714, 652, 1776, 750, stroke=1, fill=1)
    c.setFillColor(PART_A); c.ellipse(1726, 672, 1764, 730, stroke=0, fill=1)
    c.setStrokeColor(PART_HI); c.setLineWidth(0.4 * u); c.ellipse(1726, 672, 1764, 730, stroke=1, fill=0)
    c.setFillColor(PART_LINE); c.ellipse(1740, 693, 1750, 709, stroke=0, fill=1)
    # Gesichtsscheibe: dunkles Rauchglas mit weicher Spiegelung
    face = smooth_poly(FACE)
    c.setFillColor(DARK); c.setStrokeColor(DARK_LINE); c.setLineWidth(0.6 * u)
    c.drawPath(face, stroke=1, fill=1)
    c.saveState(); c.clipPath(smooth_poly(FACE), stroke=0, fill=0)
    r = c.beginPath(); r.moveTo(1488, 640); r.curveTo(1512, 575, 1570, 545, 1630, 560)
    r.curveTo(1600, 575, 1545, 600, 1505, 690); r.close()
    c.setFillColor(hx('#C9DAF2', 0.16)); c.drawPath(r, stroke=0, fill=1)
    r = c.beginPath(); r.moveTo(1640, 640); r.curveTo(1655, 700, 1650, 780, 1620, 840)
    r.curveTo(1632, 780, 1636, 700, 1625, 650); r.close()
    c.setFillColor(hx('#C9DAF2', 0.07)); c.drawPath(r, stroke=0, fill=1)
    c.restoreState()
    # Innenkante der Scheibe
    c.setStrokeColor(hx('#33425A')); c.setLineWidth(0.45 * u)
    p = c.beginPath(); p.moveTo(1500, 760); p.curveTo(1500, 840, 1560, 866, 1610, 856)
    c.drawPath(p, stroke=1, fill=0)
    # Stirnsensor
    c.setFillColor(PART_B); c.setStrokeColor(PART_LINE); c.setLineWidth(0.45 * u)
    c.circle(1612, 522, 9, stroke=1, fill=1)
    c.setFillColor(hx('#0E1522')); c.circle(1612, 522, 4.5, stroke=0, fill=1)


def _segment(c, u, l, w):
    """Ein Fingerglied entlang +x, mit Lichtkante und Gelenkpunkt am Ende."""
    c.setFillColor(DARK); c.setStrokeColor(DARK_LINE); c.setLineWidth(0.5 * u)
    c.roundRect(-w * 0.4, -w / 2, l + w * 0.4, w, w * 0.3, stroke=1, fill=1)
    c.setStrokeColor(hx('#53647F', 0.9)); c.setLineWidth(0.4 * u)
    c.line(w * 0.3, -w / 2 + 2.6, l - w * 0.45, -w / 2 + 2.6)
    c.setFillColor(DARK); c.setStrokeColor(DARK_LINE); c.setLineWidth(0.45 * u)
    c.circle(l, 0, w * 0.47, stroke=1, fill=1)
    c.setFillColor(hx('#3B4A62')); c.setStrokeColor(hx('#71839F')); c.setLineWidth(0.35 * u)
    c.circle(l, 0, w * 0.20, stroke=1, fill=1)


def _finger(c, u, base, spread, lens, widths, curls):
    c.saveState(); c.translate(*base); c.rotate(spread)
    for i, (l, w) in enumerate(zip(lens, widths)):
        if i == len(lens) - 1:
            # Endglied: ohne Gelenkpunkt, mit Fingerkuppe
            c.setFillColor(DARK); c.setStrokeColor(DARK_LINE); c.setLineWidth(0.5 * u)
            c.roundRect(-w * 0.4, -w / 2, l + w * 0.4, w, w / 2, stroke=1, fill=1)
            c.setStrokeColor(hx('#53647F', 0.9)); c.setLineWidth(0.4 * u)
            c.line(w * 0.35, -w / 2 + 2.6, l - w * 0.6, -w / 2 + 2.6)
            c.setStrokeColor(hx('#2E3B50')); c.line(l - w * 0.55, -w * 0.32, l - w * 0.55, w * 0.32)
        else:
            _segment(c, u, l, w)
            c.translate(l, 0); c.rotate(curls[i])
    c.restoreState()


def _hand(c, u, wrist, tip, flip):
    import math
    ang = math.atan2(tip[1] - wrist[1], tip[0] - wrist[0])
    Lh = math.hypot(tip[0] - wrist[0], tip[1] - wrist[1])
    sgn = -1 if flip else 1
    curl = (16, 20) if flip else (5, 7)
    c.saveState(); c.translate(*wrist); c.rotate(math.degrees(ang))
    P = Lh * 0.38                                   # Knöchellinie
    # Daumen (Ansatz an der Handwurzel)
    _finger(c, u, (Lh * 0.13, sgn * 22), sgn * 40, (Lh * 0.17, Lh * 0.11, Lh * 0.09), (28, 22, 19),
            (-sgn * 12, -sgn * 14))
    # Handgelenkmanschette
    c.setFillColor(DARK); c.setStrokeColor(DARK_LINE); c.setLineWidth(0.55 * u)
    c.roundRect(-18, -31, 46, 62, 10, stroke=1, fill=1)
    c.setStrokeColor(hx('#3A4A63')); c.setLineWidth(0.45 * u)
    for x in (-4, 10):
        c.line(x, -28, x, 28)
    # Handfläche: zur Knöchellinie hin breiter
    pm = c.beginPath(); pm.moveTo(26, -30); pm.lineTo(P - 6, -45)
    pm.curveTo(P + 8, -46, P + 12, -36, P + 12, -26); pm.lineTo(P + 12, 26)
    pm.curveTo(P + 12, 36, P + 8, 46, P - 6, 45); pm.lineTo(26, 30); pm.close()
    c.setFillColor(DARK); c.setStrokeColor(DARK_LINE); c.setLineWidth(0.55 * u)
    c.drawPath(pm, stroke=1, fill=1)
    c.setStrokeColor(hx('#3A4A63')); c.setLineWidth(0.45 * u)
    p = c.beginPath(); p.moveTo(34, sgn * 20); p.curveTo(P * 0.6, sgn * 8, P * 0.8, -sgn * 6, P - 4, -sgn * 30)
    c.drawPath(p, stroke=1, fill=0)                 # Ballenfuge
    c.setStrokeColor(hx('#53647F', 0.9)); c.setLineWidth(0.4 * u); c.line(32, -27, P - 8, -41)
    # Finger: Zeige-, Mittel-, Ring-, kleiner Finger
    for yk, sc, sp in ((-33 * sgn, 0.92, -3 * sgn), (-11 * sgn, 1.0, -1 * sgn), (11 * sgn, 0.95, 1 * sgn), (33 * sgn, 0.78, 3.5 * sgn)):
        _finger(c, u, (P + 6, yk), sp, (Lh * 0.19 * sc, Lh * 0.125 * sc, Lh * 0.10 * sc), (21, 19.5, 18),
                (curl[0] * sgn, curl[1] * sgn))
    # Knöchelgelenke
    for yk in (-33, -11, 11, 33):
        c.setFillColor(hx('#3B4A62')); c.setStrokeColor(hx('#71839F')); c.setLineWidth(0.4 * u)
        c.circle(P + 6, yk, 6.5, stroke=1, fill=1)
    c.restoreState()
