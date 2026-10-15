"""Realitätsnaher Humanoid mit außen geführter Flüssigkeitskühlung (Blender/Cycles).

Aufruf: python robot_scene.py <out.png> <breite> <hoehe> <samples> [anker.json]
Schreibt zusätzlich die 2D-Bildkoordinaten der Produkt-Einbauorte als JSON.
"""
import json
import math
import sys

import bpy
import bmesh
from mathutils import Vector, Matrix, Euler
from bpy_extras.object_utils import world_to_camera_view

OUT, RW, RH, SAMPLES = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
ANCHOR_OUT = sys.argv[5] if len(sys.argv) > 5 else OUT.replace('.png', '_anker.json')

bpy.ops.wm.read_factory_settings(use_empty=True)
scn = bpy.context.scene


# ------------------------------------------------------------------ Materialien
def mat(name, color, rough=0.4, metal=0.0, coat=0.0, alpha=1.0, trans=0.0, emit=None):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*color, 1)
    b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    b.inputs['Coat Weight'].default_value = coat
    b.inputs['Coat Roughness'].default_value = 0.08
    if trans:
        b.inputs['Transmission Weight'].default_value = trans
        b.inputs['IOR'].default_value = 1.45
    if emit:
        b.inputs['Emission Color'].default_value = (*emit[0], 1)
        b.inputs['Emission Strength'].default_value = emit[1]
    return m


def srgb(h):
    def lin(v):
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    return tuple(lin(int(h[i:i + 2], 16)) for i in (1, 3, 5))


M_WHITE = mat('Verkleidung', srgb('#E9EBEE'), rough=0.32, coat=0.35)
M_GRAPH = mat('Graphit', srgb('#2A2E35'), rough=0.42, metal=0.35)
M_DARK = mat('Gelenk', srgb('#16191E'), rough=0.5, metal=0.2)
M_ALU = mat('Aluminium', srgb('#C9CDD3'), rough=0.22, metal=1.0)
M_STEEL = mat('Edelstahl', srgb('#B8BCC2'), rough=0.16, metal=1.0)
M_NICKEL = mat('Messing vernickelt', srgb('#D5D2CB'), rough=0.12, metal=1.0)
M_VISOR = mat('Visier', srgb('#07090C'), rough=0.04, coat=1.0)
M_BLUE = mat('Vorlauf', srgb('#0A6CFF'), rough=0.22, coat=0.6)
M_ORANGE = mat('Ruecklauf', srgb('#FF5A0A'), rough=0.22, coat=0.6)
M_AIR = mat('Druckluft', srgb('#E6EBF2'), rough=0.12, trans=0.55, coat=0.5)
M_ORING = mat('O-Ring', srgb('#1BA38B'), rough=0.5)
M_BAY = mat('Schacht', srgb('#0E1116'), rough=0.6)
M_LED = mat('LED', srgb('#0A0C10'), rough=0.3, emit=(srgb('#7CC4FF'), 6.0))


# ------------------------------------------------------------------ Bausteine
def link(ob, parent=None):
    bpy.context.collection.objects.link(ob) if ob.name not in bpy.context.collection.objects else None
    if parent:
        ob.parent = parent
    return ob


def empty(name, loc, parent=None, rot=(0, 0, 0)):
    e = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(e)
    e.location = loc
    e.rotation_euler = Euler(rot)
    if parent:
        e.parent = parent
    return e


def smooth(ob, sub=2, bevel=None, seg=3):
    if bevel:
        bv = ob.modifiers.new('bevel', 'BEVEL'); bv.width = bevel; bv.segments = seg; bv.limit_method = 'ANGLE'
    if sub:
        s = ob.modifiers.new('sub', 'SUBSURF'); s.levels = sub; s.render_levels = sub
    for p in ob.data.polygons:
        p.use_smooth = True
    return ob


def box(name, size, loc, m, parent=None, bevel=0.02, sub=2, taper=None, rot=(0, 0, 0), cast=0.0):
    """Abgerundeter Quader; taper=(sx, sy) skaliert die Oberseite."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x *= size[0]; v.co.y *= size[1]; v.co.z *= size[2]
        if taper and v.co.z > 0:
            v.co.x *= taper[0]; v.co.y *= taper[1]
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    ob.location = loc; ob.rotation_euler = Euler(rot)
    ob.data.materials.append(m)
    if parent:
        ob.parent = parent
    smooth(ob, sub, bevel)
    if cast:
        cm = ob.modifiers.new('cast', 'CAST'); cm.factor = cast; cm.cast_type = 'SPHERE'
    return ob


def cyl(name, r, depth, loc, m, parent=None, rot=(0, 0, 0), verts=48, bevel=0.004, sub=0, r2=None):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=verts, radius1=r, radius2=r2 if r2 else r, depth=depth)
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    ob.location = loc; ob.rotation_euler = Euler(rot)
    ob.data.materials.append(m)
    if parent:
        ob.parent = parent
    return smooth(ob, sub, bevel, 2)


def sphere(name, r, loc, m, parent=None, scale=(1, 1, 1)):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=64, v_segments=32, radius=r)
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    ob.location = loc; ob.scale = scale
    ob.data.materials.append(m)
    if parent:
        ob.parent = parent
    for p in ob.data.polygons:
        p.use_smooth = True
    return ob


def capsule(name, r_top, r_bot, length, m, parent, top=(0, 0, 0), flat=1.0):
    """Gliedverkleidung entlang -Z ab 'top' (lokal im Parent)."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=48, radius1=r_bot, radius2=r_top, depth=length)
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    ob.parent = parent
    ob.location = (top[0], top[1], top[2] - length / 2)
    ob.scale = (1, flat, 1)
    ob.data.materials.append(m)
    return smooth(ob, 2, min(r_top, r_bot) * 0.55, 4)


def bool_cut(target, cutter):
    mod = target.modifiers.new('cut', 'BOOLEAN')
    mod.operation = 'DIFFERENCE'; mod.object = cutter; mod.solver = 'EXACT'
    cutter.hide_render = True; cutter.hide_viewport = True
    # Boolean vor der Glättung anwenden
    target.modifiers.move(len(target.modifiers) - 1, 0)


def tube(name, pts, radius, m):
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '3D'; cu.bevel_depth = radius; cu.bevel_resolution = 6; cu.resolution_u = 24
    cu.use_fill_caps = True
    sp = cu.splines.new('NURBS')
    sp.points.add(len(pts) - 1)
    for p, q in zip(sp.points, pts):
        p.co = (q.x, q.y, q.z, 1)
    sp.use_endpoint_u = True; sp.order_u = 4
    ob = bpy.data.objects.new(name, cu)
    bpy.context.collection.objects.link(ob)
    ob.data.materials.append(m)
    return ob


def W(frame, p):
    """Lokaler Punkt eines Rahmens -> Weltkoordinate."""
    bpy.context.view_layer.update()
    return frame.matrix_world @ Vector(p)


def fitting(name, loc, direction, m=M_ALU, scale=1.0, oring=True):
    """Einschraubverschraubung (stilisiert VT5528-0202): Sechskant + Körper + O-Ring."""
    d = Vector(direction).normalized()
    rot = d.to_track_quat('Z', 'Y').to_euler()
    e = empty(name, loc, rot=rot)
    cyl(name + '_hex', 0.0105 * scale, 0.008 * scale, (0, 0, 0.004 * scale), m, e, verts=6, bevel=0.0012)
    cyl(name + '_body', 0.0085 * scale, 0.014 * scale, (0, 0, 0.015 * scale), m, e, bevel=0.001)
    cyl(name + '_nip', 0.0062 * scale, 0.010 * scale, (0, 0, 0.026 * scale), m, e, bevel=0.0008)
    if oring:
        cyl(name + '_or', 0.0095 * scale, 0.0025 * scale, (0, 0, -0.0012 * scale), M_ORING, e, bevel=0.0008)
    return e


def coupling(name, loc, direction, scale=1.0):
    """Tropffreie Schnellkupplung (stilisiert SA2113-1/-2), inline im Schlauch."""
    d = Vector(direction).normalized()
    rot = d.to_track_quat('Z', 'Y').to_euler()
    e = empty(name, loc, rot=rot)
    cyl(name + '_muffe', 0.0115 * scale, 0.030 * scale, (0, 0, -0.012 * scale), M_STEEL, e, bevel=0.0015)
    for k in range(5):
        cyl(name + f'_rill{k}', 0.0119 * scale, 0.0012 * scale, (0, 0, (-0.024 + k * 0.004) * scale), M_STEEL, e, bevel=0.0003)
    cyl(name + '_hex', 0.011 * scale, 0.007 * scale, (0, 0, 0.007 * scale), M_STEEL, e, verts=6, bevel=0.001)
    cyl(name + '_nippel', 0.0075 * scale, 0.022 * scale, (0, 0, 0.020 * scale), M_STEEL, e, bevel=0.001)
    cyl(name + '_or', 0.0085 * scale, 0.0022 * scale, (0, 0, 0.0115 * scale), M_ORING, e, bevel=0.0006)
    return e


# ------------------------------------------------------------------ Körper
root = empty('root', (0, 0, 0))

# Becken
pelvis = box('Becken', (0.27, 0.18, 0.13), (0, 0, 0.975), M_WHITE, root, bevel=0.04, sub=3, taper=(1.08, 1.0), cast=0.35)
box('Becken_unten', (0.22, 0.15, 0.06), (0, 0.0, 0.905), M_GRAPH, root, bevel=0.02)

# Taillen-Drehgelenk mit 4-Kanal-Schwenkkupplung (stilisiert V0129)
cyl('Taille', 0.115, 0.07, (0, 0, 1.075), M_DARK, root, bevel=0.01, sub=1)
swivel = cyl('Schwenkkupplung', 0.128, 0.034, (0, 0.0, 1.075), M_ALU, root, bevel=0.004, verts=96)
cyl('Schwenk_flansch', 0.136, 0.008, (0, 0.0, 1.094), M_ALU, root, bevel=0.002, verts=96)
for k, a in enumerate((-50, -18, 18, 50)):
    x = 0.128 * math.sin(math.radians(a)); y = -0.128 * math.cos(math.radians(a))
    cyl(f'Kanal{k}', 0.0075, 0.012, (x * 1.02, y * 1.02, 1.075), M_BAY, root, rot=(math.pi / 2, 0, -math.radians(a)), bevel=0.001)

# Torso mit offenem Wartungsschacht
torso = box('Torso', (0.30, 0.20, 0.36), (0, 0, 1.33), M_WHITE, root, bevel=0.06, sub=3, taper=(1.30, 1.12), cast=0.45)
box('Schacht', (0.175, 0.02, 0.16), (0, -0.16, 1.31), M_BAY, root, bevel=0.008, sub=2)
box('Schachtrahmen', (0.195, 0.024, 0.18), (0, -0.148, 1.31), M_GRAPH, root, bevel=0.01, sub=2)
box('Bauchsegment', (0.30, 0.20, 0.06), (0, 0, 1.125), M_GRAPH, root, bevel=0.02)
# Brustfugen

# Pumpe + Verteiler im Schacht
manifold = box('Verteiler', (0.085, 0.03, 0.095), (0.025, -0.178, 1.305), M_ALU, root, bevel=0.006, sub=1)
pump = cyl('Pumpe', 0.027, 0.04, (-0.05, -0.185, 1.30), M_GRAPH, root, rot=(math.pi / 2, 0, 0), bevel=0.004)
cyl('Pumpe_deckel', 0.02, 0.006, (-0.05, -0.207, 1.30), M_ALU, root, rot=(math.pi / 2, 0, 0), bevel=0.002)

# Hals + Kopf
cyl('Hals', 0.042, 0.09, (0, 0.0, 1.565), M_DARK, root, bevel=0.006)
for k in range(3):
    cyl(f'Halsring{k}', 0.046, 0.006, (0, 0, 1.535 + k * 0.022), M_GRAPH, root, bevel=0.002)
head = empty('Kopf', (0, 0.0, 1.70), root, rot=(0, 0, math.radians(-8)))
sphere('Schaedel', 0.1, (0, 0.012, 0), M_WHITE, head, scale=(0.95, 1.12, 1.22))
sphere('Visier', 0.1, (0, -0.055, -0.012), M_VISOR, head, scale=(0.74, 0.5, 0.66))
cyl('Ohr_L', 0.03, 0.022, (-0.094, 0.015, 0.0), M_GRAPH, head, rot=(0, math.pi / 2, 0), bevel=0.003)
cyl('Ohr_R', 0.03, 0.022, (0.094, 0.015, 0.0), M_GRAPH, head, rot=(0, math.pi / 2, 0), bevel=0.003)
cyl('Ohr_L_led', 0.011, 0.004, (-0.106, 0.015, 0.0), M_LED, head, rot=(0, math.pi / 2, 0), bevel=0.001)


# ------------------------------------------------------------------ Arme
def arm(side, sh_rot, el_rot, wr_rot):
    s = 1 if side == 'R' else -1      # +X = rechte Bildseite der Figur (fern), -X nah zur Kamera
    sh = empty(f'Schulter_{side}', (s * 0.262, 0.0, 1.45), root, rot=sh_rot)
    sphere(f'Schultergelenk_{side}', 0.062, (0, 0, 0), M_DARK, sh)
    cyl(f'Schulteraktor_{side}', 0.058, 0.05, (s * 0.035, 0, 0), M_GRAPH, sh, rot=(0, math.pi / 2, 0), bevel=0.005)
    sphere(f'Schulterkappe_{side}', 0.07, (s * 0.012, 0, 0.012), M_WHITE, sh, scale=(1.0, 1.0, 0.92))
    capsule(f'Oberarm_{side}', 0.058, 0.05, 0.25, M_WHITE, sh, top=(0, 0, -0.05))
    el = empty(f'Ellbogen_{side}', (0, 0, -0.315), sh, rot=el_rot)
    cyl(f'Ellbogenaktor_{side}', 0.047, 0.085, (0, 0, 0), M_DARK, el, rot=(0, math.pi / 2, 0), bevel=0.006)
    cyl(f'Kuehlplatte_E_{side}', 0.049, 0.012, (s * 0.034, 0, 0), M_ALU, el, rot=(0, math.pi / 2, 0), bevel=0.002)
    capsule(f'Unterarm_{side}', 0.048, 0.04, 0.215, M_WHITE, el, top=(0, 0, -0.04))
    wr = empty(f'Handgelenk_{side}', (0, 0, -0.275), el, rot=wr_rot)
    cyl(f'Handgelenkaktor_{side}', 0.032, 0.04, (0, 0, 0.01), M_DARK, wr, bevel=0.004)
    hand(side, wr, s)
    return sh, el, wr


def hand(side, wr, s):
    palm = box(f'Handflaeche_{side}', (0.075, 0.032, 0.085), (0, 0, -0.06), M_GRAPH, wr, bevel=0.012, taper=(0.92, 1.0))
    fingers = [(-0.027, 0.88), (-0.009, 1.0), (0.009, 0.95), (0.027, 0.8)]
    for i, (x, sc) in enumerate(fingers):
        f0 = empty(f'Finger{i}_{side}', (x * s, 0, -0.105), wr, rot=(math.radians(-14), 0, 0))
        f1 = empty(f'Finger{i}b_{side}', (0, 0, -0.036 * sc), f0, rot=(math.radians(-18), 0, 0))
        f2 = empty(f'Finger{i}c_{side}', (0, 0, -0.026 * sc), f1, rot=(math.radians(-16), 0, 0))
        for fr, ln, r in ((f0, 0.036 * sc, 0.0085), (f1, 0.026 * sc, 0.0078), (f2, 0.022 * sc, 0.0072)):
            capsule(f'Glied_{fr.name}', r, r * 0.95, ln, M_GRAPH, fr, top=(0, 0, 0.002))
            sphere(f'Knoechel_{fr.name}', r * 1.05, (0, 0, 0), M_DARK, fr)
    t0 = empty(f'Daumen_{side}', (s * 0.034, -0.012, -0.035), wr, rot=(math.radians(-30), math.radians(s * 35), 0))
    t1 = empty(f'Daumenb_{side}', (0, 0, -0.035), t0, rot=(math.radians(-15), 0, 0))
    for fr, ln, r in ((t0, 0.035, 0.0105), (t1, 0.03, 0.009)):
        capsule(f'Glied_{fr.name}', r, r * 0.95, ln, M_GRAPH, fr, top=(0, 0, 0.002))
        sphere(f'Knoechel_{fr.name}', r * 1.05, (0, 0, 0), M_DARK, fr)


# Nahe Seite (-X): Unterarm nach vorn angehoben, Handfläche nach oben
shL, elL, wrL = arm('L', (math.radians(-12), math.radians(11), 0), (math.radians(-42), 0, 0), (0, math.radians(-20), 0))
shR, elR, wrR = arm('R', (math.radians(4), math.radians(-9), 0), (math.radians(-16), 0, 0), (0, 0, 0))


# ------------------------------------------------------------------ Beine
def leg(side, hip_rot, knee_rot, ankle_rot):
    s = 1 if side == 'R' else -1
    hp = empty(f'Huefte_{side}', (s * 0.105, 0.0, 0.905), root, rot=hip_rot)
    cyl(f'Hueftaktor_{side}', 0.066, 0.1, (0, 0, 0), M_DARK, hp, rot=(0, math.pi / 2, 0), bevel=0.007)
    cyl(f'Kuehlplatte_H_{side}', 0.068, 0.014, (s * 0.052, 0, 0), M_ALU, hp, rot=(0, math.pi / 2, 0), bevel=0.002)
    capsule(f'Oberschenkel_{side}', 0.085, 0.066, 0.33, M_WHITE, hp, top=(0, 0, -0.045), flat=0.95)
    kn = empty(f'Knie_{side}', (0, 0, -0.42), hp, rot=knee_rot)
    cyl(f'Knieaktor_{side}', 0.058, 0.11, (0, 0, 0), M_DARK, kn, rot=(0, math.pi / 2, 0), bevel=0.007)
    cyl(f'Kuehlplatte_K_{side}', 0.06, 0.014, (s * 0.057, 0, 0), M_ALU, kn, rot=(0, math.pi / 2, 0), bevel=0.002)
    box(f'Kniescheibe_{side}', (0.07, 0.03, 0.07), (0, -0.05, 0.0), M_WHITE, kn, bevel=0.014)
    capsule(f'Unterschenkel_{side}', 0.066, 0.05, 0.33, M_WHITE, kn, top=(0, 0, -0.045), flat=0.95)
    an = empty(f'Knoechel_{side}', (0, 0, -0.415), kn, rot=ankle_rot)
    cyl(f'Sprunggelenk_{side}', 0.036, 0.075, (0, 0, 0), M_DARK, an, rot=(0, math.pi / 2, 0), bevel=0.005)
    box(f'Fuss_{side}', (0.095, 0.24, 0.055), (0, -0.045, -0.055), M_GRAPH, an, bevel=0.02, taper=(0.9, 0.85))
    box(f'Sohle_{side}', (0.096, 0.242, 0.012), (0, -0.045, -0.081), M_DARK, an, bevel=0.005)
    return hp, kn, an


hpL, knL, anL = leg('L', (math.radians(-3), 0, 0), (math.radians(6), 0, 0), (math.radians(-3), 0, 0))
hpR, knR, anR = leg('R', (math.radians(4), 0, 0), (math.radians(5), 0, 0), (math.radians(-9), 0, 0))

bpy.context.view_layer.update()

# ------------------------------------------------------------------ Kühlkreis
TR = 0.0055      # Schlauchradius (bewusst gut sichtbar)


def pair(name, frames_pts, sep_dir, sep=0.0125):
    """Vorlauf/Rücklauf als paralleles Schlauchpaar entlang derselben Route."""
    pts = [W(f, p) for f, p in frames_pts]
    d = Vector(sep_dir).normalized() * sep / 2
    tube(name + '_VL', [p - d for p in pts], TR, M_BLUE)
    tube(name + '_RL', [p + d for p in pts], TR, M_ORANGE)
    return pts


ANCH = {}

# Arm nah (-X): Verteiler -> Brust -> SA2113 am Moduluebergang -> Oberarm aussen -> Schlaufe -> Ellbogen-Kuehlplatte
arm_route = [
    (root, (-0.02, -0.196, 1.345)), (root, (-0.075, -0.18, 1.375)), (root, (-0.15, -0.15, 1.43)),
    (root, (-0.205, -0.10, 1.475)),
    (shL, (-0.045, -0.06, -0.04)), (shL, (-0.05, -0.058, -0.13)), (shL, (-0.05, -0.056, -0.23)),
    (shL, (-0.075, -0.03, -0.29)), (elL, (-0.07, 0.035, 0.045)), (elL, (-0.052, 0.0, 0.0)),
]
p = pair('Arm_L', arm_route, (0, 0, 1), sep=0.013)
coupling('SA2113_Arm_L', W(root, (-0.205, -0.10, 1.475)), W(shL, (-0.045, -0.06, -0.04)) - W(root, (-0.15, -0.15, 1.43)), scale=1.6)
fitting('VT5528_Ellbogen_L', W(elL, (-0.046, 0.0, 0.0)), Vector(W(elL, (-1, 0, 0))) - W(elL, (0, 0, 0)), scale=1.4)
ANCH['sa2113'] = W(root, (-0.205, -0.10, 1.475))
ANCH['vt5528'] = W(elL, (-0.048, 0.0, 0.0))

# Arm fern (+X)
pair('Arm_R', [
    (root, (0.06, -0.196, 1.345)), (root, (0.12, -0.175, 1.39)), (root, (0.19, -0.13, 1.46)),
    (shR, (0.045, -0.06, -0.04)), (shR, (0.05, -0.058, -0.15)), (shR, (0.05, -0.05, -0.27)),
    (elR, (0.055, -0.02, 0.03)), (elR, (0.052, 0.0, 0.0)),
], (0, 0, 1), sep=0.013)
fitting('VT5528_Ellbogen_R', W(elR, (0.046, 0.0, 0.0)), Vector(W(elR, (1, 0, 0))) - W(elR, (0, 0, 0)), scale=1.4)

# Beine: Verteiler -> durch die Schwenkkupplung -> Hueftaktor -> Oberschenkel -> Knieschlaufe -> Knieaktor
for side, hp, kn, s, xk in (('L', hpL, knL, -1, -0.025), ('R', hpR, knR, 1, 0.045)):
    route = [
        (root, (xk, -0.196, 1.255)), (root, (xk * 1.6, -0.17, 1.19)), (root, (s * 0.05, -0.12, 1.105)),
        (root, (s * 0.06, -0.128, 1.045)), (root, (s * 0.085, -0.12, 0.985)),
        (hp, (s * 0.05, -0.08, 0.01)), (hp, (s * 0.065, -0.07, -0.08)), (hp, (s * 0.07, -0.068, -0.2)),
        (hp, (s * 0.07, -0.07, -0.31)), (hp, (s * 0.088, -0.095, -0.37)), (kn, (s * 0.09, -0.05, 0.05)),
        (kn, (s * 0.068, 0.0, 0.0)),
    ]
    pair(f'Bein_{side}', route, (1, 0, 0), sep=0.0135)
    fitting(f'VT5528_Hueft_{side}', W(hp, (s * 0.061, -0.03, 0.0)), W(hp, (s, -0.4, 0)) - W(hp, (0, 0, 0)), scale=1.4, oring=True)
    fitting(f'VT5528_Knie_{side}', W(kn, (s * 0.064, 0.0, 0.0)), W(kn, (s, 0, 0)) - W(kn, (0, 0, 0)), scale=1.4)
ANCH['v0129'] = W(root, (-0.085, -0.1, 1.075))
ANCH['knie'] = W(knL, (-0.066, 0.0, 0.0))

# Verteiler-Anschlüsse im Schacht
for k, (x, z) in enumerate(((-0.02, 1.345), (0.06, 1.345), (-0.025, 1.255), (0.045, 1.255))):
    fitting(f'Verteiler_port{k}', (x, -0.193, z), (0, -1, 0), scale=0.85, oring=False)
tube('Pumpe_VL', [Vector((-0.05, -0.2, 1.327)), Vector((-0.03, -0.202, 1.333)), Vector((-0.017, -0.196, 1.34))], TR * 0.9, M_BLUE)
ANCH['pumpe'] = W(root, (-0.05, -0.21, 1.30))

# Druckluft/Vakuum zum Greifer (nah): Schulter hinten -> Arm aussen -> Push-In am Handgelenk
air = [W(root, (-0.17, 0.05, 1.47)), W(shL, (-0.06, 0.02, -0.03)), W(shL, (-0.058, 0.01, -0.2)),
       W(shL, (-0.07, 0.035, -0.30)), W(elL, (-0.05, 0.05, -0.02)), W(elL, (-0.045, 0.03, -0.12)),
       W(elL, (-0.04, 0.02, -0.22)), W(wrL, (-0.03, 0.0, 0.0))]
tube('Druckluft_L', air, TR * 0.75, M_AIR)
fitting('PushIn_863_4218', W(wrL, (-0.026, 0.0, -0.004)), W(wrL, (-1, 0, 0)) - W(wrL, (0, 0, 0)), m=M_NICKEL, scale=0.85, oring=False)
ANCH['pushin'] = W(wrL, (-0.028, 0.0, -0.004))

# ------------------------------------------------------------------ Licht, Kamera, Boden
world = bpy.data.worlds.new('Studio'); scn.world = world
world.use_nodes = True
bg = world.node_tree.nodes['Background']
bg.inputs['Color'].default_value = (*srgb('#DCDFE4'), 1); bg.inputs['Strength'].default_value = 0.3


def area(name, loc, target, size, power, color='#FFFFFF'):
    l = bpy.data.lights.new(name, 'AREA'); l.size = size; l.energy = power; l.color = srgb(color)
    o = bpy.data.objects.new(name, l); bpy.context.collection.objects.link(o)
    o.location = loc
    o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    return o


area('Key', (-2.2, -2.4, 3.0), (0, 0, 1.1), 2.4, 260)
area('Fill', (2.4, -2.6, 1.4), (0, 0, 1.0), 3.0, 70, '#EAF2FF')
area('Rim', (1.4, 2.2, 2.6), (0, 0, 1.3), 1.4, 260, '#DCEBFF')
area('Top', (0, 0, 3.4), (0, 0, 1.0), 2.0, 50)

floor = box('Boden', (8, 8, 0.01), (0, 0, -0.03), M_WHITE, None, bevel=0, sub=0)
floor.is_shadow_catcher = True
floor.visible_glossy = False

cam_d = bpy.data.cameras.new('Kamera'); cam_d.lens = 58
cam = bpy.data.objects.new('Kamera', cam_d); bpy.context.collection.objects.link(cam)
cam.location = (-1.48, -2.98, 1.05)
cam.rotation_euler = (Vector((0.02, 0, 0.93)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
scn.camera = cam

# ------------------------------------------------------------------ Render
scn.render.engine = 'CYCLES'
scn.cycles.device = 'CPU'
scn.cycles.samples = SAMPLES
scn.cycles.use_denoising = True
scn.cycles.max_bounces = 8
scn.render.film_transparent = True
scn.render.resolution_x = RW; scn.render.resolution_y = RH
scn.render.image_settings.file_format = 'PNG'; scn.render.image_settings.color_mode = 'RGBA'
scn.render.image_settings.color_depth = '16'
scn.view_settings.view_transform = 'AgX'
scn.view_settings.look = 'AgX - Punchy'
scn.render.filepath = OUT
scn.render.threads_mode = 'FIXED'; scn.render.threads = 4

bpy.context.view_layer.update()
dg = bpy.context.evaluated_depsgraph_get()
for nm in ('Torso', 'Becken'):
    ev = bpy.data.objects[nm].evaluated_get(dg)
    ys = [(ev.matrix_world @ v.co) for v in ev.to_mesh().vertices]
    print('BOUNDS', nm, 'ymin', min(v.y for v in ys if abs(v.z - 1.31) < 0.03) if nm == 'Torso' else min(v.y for v in ys))
anch2d = {}
for k, v in ANCH.items():
    co = world_to_camera_view(scn, cam, v)
    anch2d[k] = (co.x * RW, (1 - co.y) * RH)
json.dump(anch2d, open(ANCHOR_OUT, 'w'), indent=1)
bpy.ops.render.render(write_still=True)
print('fertig', OUT)
