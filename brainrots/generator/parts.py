"""Shared materials and reusable body parts (eyes, mouths, limbs...)."""
import math

import numpy as np

from vox import CX, Mat, mx

# ---- shared materials ------------------------------------------------------
EYE_WHITE = Mat("eye_white", (250, 250, 252), rough=0.25)
PUPIL = Mat("pupil", (22, 20, 30), rough=0.15)
SHINE = Mat("shine", (255, 255, 255), rough=0.1, emit=0.8)
MOUTH = Mat("mouth", (74, 22, 36), rough=0.7)
TONGUE = Mat("tongue", (236, 96, 122), rough=0.5)
TOOTH = Mat("tooth", (252, 250, 240), rough=0.35)
BLUSH = Mat("blush", (255, 128, 150), rough=0.7)
BLACK = Mat("black", (30, 30, 36), rough=0.6)
WHITE = Mat("white", (244, 244, 238), rough=0.55)
GOLD = Mat("gold", (246, 190, 58), rough=0.22, metal=1.0)
GOLD_DARK = Mat("gold_dark", (196, 136, 34), rough=0.3, metal=1.0)
SILVER = Mat("silver", (204, 210, 222), rough=0.22, metal=1.0)
CHROME_DARK = Mat("chrome_dark", (120, 126, 140), rough=0.3, metal=1.0)
RUBBER = Mat("rubber", (46, 46, 54), rough=0.85)
WOOD = Mat("wood", (168, 112, 64), rough=0.75, shades=3, amt=0.08, scale=1)
WOOD_LIGHT = Mat("wood_light", (226, 190, 136), rough=0.7, shades=2, amt=0.06, scale=1)
ORANGE_BEAK = Mat("beak_orange", (250, 150, 40), rough=0.45)
YELLOW_BEAK = Mat("beak_yellow", (252, 206, 64), rough=0.45)
GLASS = Mat("glass", (196, 232, 246), rough=0.05, emit=0.12)
WATER = Mat("water", (120, 200, 250), rough=0.05, emit=0.25)
FLAME_Y = Mat("flame_yellow", (255, 236, 120), rough=0.5, emit=4.0)
FLAME_O = Mat("flame_orange", (255, 150, 40), rough=0.5, emit=3.5)
FLAME_R = Mat("flame_red", (240, 70, 30), rough=0.5, emit=3.0)
SMOKE = Mat("smoke", (226, 226, 232), rough=0.95, shades=2, amt=0.05, scale=2)


# ---- face ------------------------------------------------------------------
def eye(g, x, z, r=3.0, sym=True, look=(0.0, 0.0), pupil=0.5, iris=None,
        white=EYE_WHITE, pupil_mat=PUPIL, bulge=0.45, depth_r=None,
        lid=None, lid_mat=None, lid_tilt=0.0, shine=True, tall=1.12, y=None,
        slit=False):
    """Cartoon eye glued on the front surface at (x, z).

    lid: fraction of the eye height covered from the top (0..1) using lid_mat,
    lid_tilt > 0 makes the lid lower towards the middle (angry look)."""
    sides = [x, 2 * CX - x] if sym else [x]
    for i, sx in enumerate(sides):
        y0 = g.front_y(sx, z) if y is None else y
        if y0 is None:
            y0 = 40
        ry = depth_r if depth_r is not None else r * 0.75
        cy = y0 + r * bulge
        g.ell((sx, cy, z), (r, ry, r * tall), white)
        px, pz = sx + look[0], z + look[1]
        rng_x = (sx - r - 1, sx + r + 1)
        rng_z = (z - r * tall - 1, z + r * tall + 1)
        if iris is not None:
            ir = r * min(0.85, pupil * 1.55)
            g.decal(rng_x, rng_z, lambda A, B: ((A - px) / ir) ** 2 + ((B - pz) / (ir * 1.1)) ** 2 <= 1,
                    iris, only=[white])
        pr = r * pupil
        if slit:
            g.decal(rng_x, rng_z, lambda A, B: ((A - px) / max(0.6, pr * 0.32)) ** 2 + ((B - pz) / (pr * 1.25)) ** 2 <= 1,
                    pupil_mat, only=[white] + ([iris] if iris else []))
        else:
            g.decal(rng_x, rng_z, lambda A, B: ((A - px) / pr) ** 2 + ((B - pz) / (pr * 1.15)) ** 2 <= 1,
                    pupil_mat, only=[white] + ([iris] if iris else []))
        if shine:
            sr = max(0.75, r * 0.2)
            hx, hz = px - pr * 0.45, pz + pr * 0.5
            g.decal(rng_x, rng_z, lambda A, B: (A - hx) ** 2 + (B - hz) ** 2 <= sr * sr,
                    SHINE, only=[pupil_mat] + ([iris] if iris else []))
        if lid is not None:
            sgn = 1 if sx <= CX else -1
            ztop = z + r * tall
            zcut = ztop - 2 * r * tall * lid

            def lidf(A, B, sx=sx, zcut=zcut, sgn=sgn):
                return B >= zcut - lid_tilt * (A - sx) * sgn
            g.decal(rng_x, rng_z, lidf, lid_mat, only=[white, pupil_mat, SHINE] + ([iris] if iris else []), depth=2)


def dot_eye(g, x, z, r=1.6, sym=True, mat=PUPIL, shine=True, y=None):
    """Small glossy bead eye."""
    sides = [x, 2 * CX - x] if sym else [x]
    for sx in sides:
        y0 = g.front_y(sx, z) if y is None else y
        if y0 is None:
            continue
        g.ell((sx, y0 + r * 0.3, z), (r, r * 0.8, r * 1.15), mat)
        if shine:
            g.decal((sx - r - 1, sx + r + 1), (z - r - 1, z + r + 1),
                    lambda A, B, sx=sx: (A - (sx - r * 0.35)) ** 2 + (B - (z + r * 0.4)) ** 2 <= 0.6,
                    SHINE, only=[mat])


def smile(g, x, z, w, mat=MOUTH, curve=None, thick=1, depth=1, only=None):
    curve = w * 0.38 if curve is None else curve

    def f(A, B):
        t = (A - x) / max(w, 1e-6)
        zc = z + curve * t * t
        return (np.abs(t) <= 1.0) & (B >= zc - thick / 2.0 - 0.01) & (B <= zc + thick / 2.0 + 0.01)
    g.decal((x - w - 1, x + w + 1), (z - 1 - thick, z + abs(curve) + 1 + thick), f, mat, depth=depth, only=only)


def open_mouth(g, x, z, w, h, teeth=True, tongue=True, only=None, fangs=False):
    """Big D-shaped open mouth (flat top at z, round bottom)."""
    def mouth(A, B):
        return (B <= z) & (((A - x) / w) ** 2 + ((B - z) / h) ** 2 <= 1.0)
    g.decal((x - w - 1, x + w + 1), (z - h - 1, z + 1), mouth, MOUTH, depth=2, only=only)
    if tongue:
        g.decal((x - w, x + w), (z - h, z),
                lambda A, B: mouth(A, B) & (((A - x) / (w * 0.6)) ** 2 + ((B - (z - h)) / (h * 0.55)) ** 2 <= 1.0),
                TONGUE, depth=1, only=[MOUTH])
    if teeth:
        tw = max(1, int(w * 0.28))
        g.decal((x - w, x + w), (z - 1, z),
                lambda A, B: mouth(A, B) & (B >= z - 1) & (np.abs(A - x) <= tw) & (np.abs(A - x) >= 0.5 if tw > 1 else True),
                TOOTH, depth=1, only=[MOUTH])
    if fangs:
        for sx in (x - w * 0.55, x + w * 0.55):
            g.decal((sx - 1, sx + 1), (z - 2, z),
                    lambda A, B, sx=sx: (np.abs(A - sx) <= 0.6) & (B >= z - 2) & mouth(A, B),
                    TOOTH, depth=1, only=[MOUTH])


def blush(g, x, z, rx=2.2, rz=1.2, sym=True, only=None):
    g.front_ellipse(x, z, rx, rz, BLUSH, sym=sym, only=only)


# ---- limbs -----------------------------------------------------------------
def leg(g, x, y, z_top, mat, r=2.5, foot_mat=None, foot=(3.0, 4.0, 1.6), sym=True, z_bottom=0.0):
    foot_mat = foot_mat or mat
    g.seg((x, y, z_top), (x, y, z_bottom + foot[2]), r, mat, sym=sym)
    g.ell((x, y - foot[1] * 0.35, z_bottom + foot[2]), foot, foot_mat, sym=sym)


def bird_foot(g, x, y, mat, z=0.8, toe=4.0, r=0.9, sym=True):
    for ang in (-35, 0, 35):
        a = math.radians(ang)
        tip = (x + toe * math.sin(a), y - toe * math.cos(a), z)
        g.seg((x, y, z), tip, r, mat, sym=sym)
    g.seg((x, y, z), (x, y + toe * 0.5, z), r, mat, sym=sym)


def sparkle(g, c, s, mat):
    """Floating 3D plus-shaped star."""
    x, y, z = c
    g.box((x - s, y, z), (x + s, y, z), mat)
    g.box((x, y, z - s), (x, y, z + s), mat)
    g.box((x, y - s, z), (x, y + s, z), mat)
    if s >= 2:
        g.box((x - 1, y - 1, z - 1), (x + 1, y + 1, z + 1), mat)


def cone_spikes(g, pts, mat, r=2.0, length=6.0, center=(CX, 72, 20), tip_mat=None):
    """Spikes pointing away from `center`, starting at each point."""
    c = np.asarray(center, float)
    for p in pts:
        p = np.asarray(p, float)
        d = p - c
        n = np.linalg.norm(d) or 1.0
        tip = p + d / n * length
        g.seg(p, tip, r, mat, r1=0.35)
        if tip_mat is not None:
            g.seg(p + d / n * length * 0.65, tip, r * 0.4, tip_mat, r1=0.35)


def coil_along(g, ctrl, coil_r, turns, wire_r, mat, steps=240):
    """Telephone-cord coil following a Catmull-Rom centre line."""
    P = [np.asarray(p, float) for p in ctrl]
    pts = []
    for i in range(len(P) - 1):
        p0 = P[i - 1] if i > 0 else P[i]
        p1, p2 = P[i], P[i + 1]
        p3 = P[i + 2] if i + 2 < len(P) else P[i + 1]
        for s in range(20):
            t = s / 20
            pts.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    pts.append(P[-1])
    pts = np.array(pts)
    seg_len = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    cum = np.concatenate([[0], np.cumsum(seg_len)])
    total = cum[-1]
    out = []
    for k in range(steps + 1):
        d = total * k / steps
        i = min(np.searchsorted(cum, d) - 1, len(pts) - 2)
        i = max(i, 0)
        f = (d - cum[i]) / max(seg_len[i], 1e-9)
        c = pts[i] + (pts[i + 1] - pts[i]) * f
        tng = pts[i + 1] - pts[i]
        tng /= np.linalg.norm(tng) or 1
        n1 = np.cross(tng, [1.0, 0, 0])
        if np.linalg.norm(n1) < 1e-3:
            n1 = np.cross(tng, [0, 1.0, 0])
        n1 /= np.linalg.norm(n1)
        n2 = np.cross(tng, n1)
        a = 2 * math.pi * turns * k / steps
        out.append(c + coil_r * (math.cos(a) * n1 + math.sin(a) * n2))
    g.tube(out, wire_r, mat)


def glitch_bands(g, bands_, edge_a, edge_b):
    """Shift horizontal slabs sideways and colour their edges (RGB split look).
    bands_: list of (z0, z1, shift_x) in design units."""
    from vox import PALETTE
    ia = PALETTE.get(edge_a)
    ib = PALETTE.get(edge_b)
    s = g.s
    for z0, z1, sh in bands_:
        k0, k1 = int(round(z0 * s)), int(round((z1 + 1) * s))
        slab = np.roll(g.v[:, :, k0:k1].copy(), int(round(sh * s)), axis=0)
        filled = slab > 0
        right = filled & ~np.roll(filled, -1, axis=0)
        left = filled & ~np.roll(filled, 1, axis=0)
        slab[right] = ia
        slab[left] = ib
        g.v[:, :, k0:k1] = slab


# ============================================================================
# Style kit: accessories that give each brainrot an attitude
# ============================================================================
RUBY = Mat("ruby_gem", (255, 34, 86), rough=0.05, emit=1.8)
SAPPHIRE = Mat("sapphire_gem", (50, 140, 255), rough=0.05, emit=1.8)
EMERALD = Mat("emerald_gem", (40, 230, 130), rough=0.05, emit=1.8)
LENS_DARK = Mat("lens_dark", (24, 20, 40), rough=0.04, metal=0.3)
LENS_SHINE = Mat("lens_shine", (210, 230, 255), rough=0.05, emit=0.9)
SOLE = Mat("sneaker_sole", (248, 248, 244), rough=0.5)
LACE = Mat("sneaker_lace", (255, 255, 255), rough=0.6)


def _shape_mask(style, cx, z, rx, rz):
    def f(A, B):
        x = (A - cx) / rx
        y = (B - z) / rz
        if style == "aviator":
            yy = np.where(y > 0, y * 1.15, y * 0.8)
            return x * x + yy * yy <= 1.0
        if style == "heart":
            x2, y2 = x * 1.05, y * 1.1 + 0.15
            return (x2 * x2 + y2 * y2 - 1) ** 3 - x2 * x2 * y2 ** 3 <= 0
        if style == "star":
            th = np.arctan2(y, x) - math.pi / 2
            rr = np.sqrt(x * x + y * y)
            return rr <= 0.52 + 0.48 * np.cos(5 * th) ** 2 * (np.cos(5 * th) > 0) + 0.12
        if style == "cat":
            yy = y - 0.35 * x * (1 if cx < CX else -1)
            return x * x + (yy * 1.25) ** 2 <= 1.0
        if style == "square":
            return (np.abs(x) <= 1.0) & (np.abs(y) <= 1.0)
        return x * x + y * y <= 1.0
    return f


def shades(g, x, z, rx, rz, frame, lens=LENS_DARK, style="round", rim=0.7, thick=0.9, bridge=True, shine=True,
           ymax=None):
    """Sunglasses glued on the face (symmetric around CX). x = left lens centre.
    lens=None gives see-through glasses (frame only)."""
    for cx in (x, 2 * CX - x):
        outer = _shape_mask(style, cx, z, rx + rim, rz + rim)
        inner = _shape_mask(style, cx, z, rx, rz)
        rng = ((cx - rx - rim - 1, cx + rx + rim + 1), (z - rz - rim - 1, z + rz + rim + 1))
        g.plate(rng[0], rng[1], lambda A, B, o=outer, i=inner: o(A, B) & ~i(A, B), frame, thick=thick + 0.3,
                ymax=ymax)
        if lens is None:
            continue
        g.plate(rng[0], rng[1], inner, lens, thick=thick, ymax=ymax)
        if shine:
            g.decal(rng[0], rng[1],
                    lambda A, B, i=inner, cx=cx: i(A, B) & (np.abs((A - cx) + (B - z) - rx * 0.35) <= 0.45),
                    LENS_SHINE, only=[lens])
    if bridge:
        y0 = g.front_y(CX, z + rz * 0.35)
        if y0 is not None:
            g.seg((x + rx, y0 - thick, z + rz * 0.35), (2 * CX - x - rx, y0 - thick, z + rz * 0.35), 0.55, frame)


def visor(g, x0, x1, z0, z1, mat, thick=1.0, slit=None):
    """One-piece band across the face (cyber visor / mask)."""
    g.plate((x0, x1), (z0, z1), lambda A, B: (A >= x0) & (A <= x1) & (B >= z0) & (B <= z1), mat, thick=thick)
    if slit is not None:
        zm = (z0 + z1) / 2
        g.decal((x0, x1), (z0, z1), lambda A, B: np.abs(B - zm) <= 0.5, slit, only=[mat])


def glow_eyes(g, x, z, rx, rz, mat, tilt=0.5, thick=0.6, ymax=None):
    """Emissive slanted eyes without pupils (menacing / powerful look)."""
    for cx in (x, 2 * CX - x):
        sgn = 1 if cx < CX else -1

        def f(A, B, cx=cx, sgn=sgn):
            ell = ((A - cx) / rx) ** 2 + ((B - z) / rz) ** 2 <= 1.0
            return ell & (B <= z + rz * 0.35 + tilt * (A - cx) * sgn)
        g.plate((cx - rx - 1, cx + rx + 1), (z - rz - 1, z + rz + 1), f, mat, thick=thick, ymax=ymax)


def brows(g, x, z, w, mat, tilt=0.45, thick=0.8, h=0.7, ymax=None):
    """Angry/confident eyebrows (tilt > 0: inner end lower)."""
    for cx in (x, 2 * CX - x):
        sgn = 1 if cx < CX else -1

        def f(A, B, cx=cx, sgn=sgn):
            zc = z + tilt * (A - cx) * -sgn
            return (np.abs(A - cx) <= w) & (np.abs(B - zc) <= h)
        g.plate((cx - w - 1, cx + w + 1), (z - w - 2, z + w + 2), f, mat, thick=thick, ymax=ymax)


def mustache(g, x, z, w, mat, thick=0.9):
    def f(A, B):
        t = (A - x) / w
        zc = z - 0.9 * np.abs(t) + 1.3 * np.maximum(0, np.abs(t) - 0.75) * 3
        return (np.abs(t) <= 1.05) & (B >= zc - 0.9) & (B <= zc + 0.9 - 0.6 * np.abs(t))
    g.plate((x - w - 2, x + w + 2), (z - w, z + 3), f, mat, thick=thick)


def gold_chain(g, c, rx, ry, drop=3.0, r=0.85, mat=None, alt=None, medallion=None, med_r=2.6,
               emblem=None, emblem_mat=None, step=1.5):
    """Bead chain around a neck; drops lower at the front, optional medallion."""
    mat = mat or GOLD
    alt = alt or GOLD_DARK
    cx, cy, cz = c
    n = max(16, int(2 * math.pi * max(rx, ry) / step))
    for k in range(n):
        t = 2 * math.pi * k / n
        y = cy + ry * math.sin(t)
        z = cz - drop * max(0.0, -math.sin(t)) ** 1.5
        g.sphere((cx + rx * math.cos(t), y, z), r, mat if k % 2 else alt)
    if medallion is not None:
        mz = cz - drop - med_r * 0.9
        my = cy - ry - 0.4
        g.cyl((cx, my + 0.6, mz), med_r, 1.2, medallion, axis="-y")
        g.sphere((cx, my, cz - drop + 0.2), r * 1.1, mat)
        if emblem is not None:
            g.decal((cx - med_r, cx + med_r), (mz - med_r, mz + med_r),
                    lambda A, B: emblem((A - cx) / med_r, (B - mz) / med_r), emblem_mat, only=[medallion])


def crown(g, c, r, h=3.0, mat=None, gem=None, points=5, band=1.2):
    mat = mat or GOLD
    gem = gem or RUBY
    cx, cy, cz = c
    g.cyl((cx, cy, cz), r, band * 1.6, mat)
    g.cyl((cx, cy, cz + 0.3), r - 0.9, band * 1.6, mat, mode="carve")
    for k in range(points):
        a = math.radians(k * 360 / points - 90)
        px, py = cx + (r - 0.4) * math.cos(a), cy + (r - 0.4) * math.sin(a)
        g.cyl((px, py, cz + band * 1.5), 1.1, h, mat, r2=0.35)
        g.sphere((px, py, cz + band * 1.5 + h + 0.3), 0.7, mat)
    g.sphere((cx, cy - r + 0.2, cz + band * 0.8), 0.9, gem)


def cap(g, c, r, mat, brim_mat=None, backwards=False, button=None, logo=None):
    """Baseball cap sitting on a head whose top is around c."""
    brim_mat = brim_mat or mat
    cx, cy, cz = c
    g.sphere((cx, cy, cz), r, mat, where=lambda X, Y_, Z: Z >= cz)
    dirn = 1 if backwards else -1
    g.ell((cx, cy + dirn * (r + 2.2), cz + 0.3), (r * 0.8, 3.6, 0.7), brim_mat)
    g.sphere((cx, cy, cz + r), 0.9, button or brim_mat)
    if logo is not None and not backwards:
        g.decal((cx - 2, cx + 2), (cz + r * 0.25, cz + r * 0.7),
                lambda A, B: (np.abs(A - cx) <= 1.6) & (B >= cz + r * 0.3) & (B <= cz + r * 0.65), logo)


def top_hat(g, c, r, h, mat, band_mat, brim=1.6):
    cx, cy, cz = c
    g.cyl((cx, cy, cz), r * brim, 0.8, mat)
    g.cyl((cx, cy, cz + 0.5), r, h, mat)
    g.cyl((cx, cy, cz + 0.8), r + 0.25, 1.4, band_mat)


def chef_hat(g, c, r, h, mat):
    cx, cy, cz = c
    g.cyl((cx, cy, cz), r, h, mat)
    for a in range(0, 360, 60):
        ar = math.radians(a)
        g.sphere((cx + r * 0.7 * math.cos(ar), cy + r * 0.7 * math.sin(ar), cz + h + 1.2), r * 0.55, mat)
    g.sphere((cx, cy, cz + h + 2.2), r * 0.7, mat)


def hard_hat(g, c, r, mat):
    cx, cy, cz = c
    g.sphere((cx, cy, cz), r, mat, where=lambda X, Y_, Z: Z >= cz)
    g.ell((cx, cy - 0.8, cz + 0.2), (r + 1.6, r + 2.4, 0.7), mat)
    g.seg((cx, cy - r + 0.5, cz + r * 0.4), (cx, cy + r - 0.5, cz + r * 0.4), 0.9, mat)
    g.seg((cx, cy - r * 0.7, cz + r * 0.75), (cx, cy + r * 0.7, cz + r * 0.75), 1.1, mat)


def peaked_cap(g, c, r, mat, visor_mat, badge_mat, band_mat=None, h=3.0):
    """Police / captain style cap with a flat crown and a glossy visor."""
    cx, cy, cz = c
    g.cyl((cx, cy, cz), r, h * 0.6, band_mat or mat)
    g.ell((cx, cy + 0.6, cz + h * 0.6 + 0.6), (r + 1.4, r + 1.6, h * 0.45), mat)
    g.ell((cx, cy - r - 0.8, cz + 0.2), (r * 0.85, 2.6, 0.6), visor_mat, rot=(-12, 0, 0))
    g.decal((cx - 1.6, cx + 1.6), (cz + 0.2, cz + h), lambda A, B: (A - cx) ** 2 + (B - (cz + h * 0.55)) ** 2 <= 1.6,
            badge_mat)


def beret(g, c, r, mat, tilt=14):
    cx, cy, cz = c
    g.ell((cx + 1, cy, cz + 0.6), (r * 1.15, r * 1.1, r * 0.38), mat, rot=(0, tilt, 0))
    g.seg((cx + 1.5, cy, cz + r * 0.4), (cx + 1.8, cy, cz + r * 0.4 + 1.6), 0.5, mat)


def straw_hat(g, c, r, mat, ribbon, flower=None):
    cx, cy, cz = c
    g.cyl((cx, cy, cz), r * 2.0, 0.8, mat)
    g.sphere((cx, cy, cz + 0.5), r, mat, where=lambda X, Y_, Z: Z >= cz + 0.5)
    g.cyl((cx, cy, cz + 0.7), r + 0.2, 1.4, ribbon)
    if flower is not None:
        for a in range(0, 360, 72):
            ar = math.radians(a)
            g.sphere((cx + r + 0.3, cy - 1.5 + 1.2 * math.cos(ar), cz + 1.5 + 1.2 * math.sin(ar)), 0.9, flower)


def party_hat(g, c, r, h, mats, pom):
    cx, cy, cz = c
    from vox import stripes as _stripes
    g.cyl((cx, cy, cz), r, h, _stripes("z", 2.2, mats), r2=0.4)
    g.sphere((cx, cy, cz + h + 0.6), 1.4, pom)


def shower_cap(g, c, r, mat, frill):
    cx, cy, cz = c
    g.ell((cx, cy, cz + r * 0.25), (r + 0.6, r + 0.6, r * 0.75), mat, where=lambda X, Y_, Z: Z >= cz - 0.5)
    for a in range(0, 360, 20):
        ar = math.radians(a)
        g.sphere((cx + (r + 0.6) * math.cos(ar), cy + (r + 0.6) * math.sin(ar), cz - 0.4), 1.0, frill)


def headphones(g, c, half_w, mat_band, mat_cup, led=None, cup_r=3.2, band_r=0.9, band_h=None):
    cx, cy, cz = c
    band_h = half_w if band_h is None else band_h
    g.torus((cx, cy, cz), half_w + 0.6, band_r, mat_band, axis="y", where=lambda X, Y_, Z: Z >= cz)
    for s in (-1, 1):
        g.cyl((cx + s * (half_w - 0.4), cy, cz), cup_r, 2.4, mat_cup, rot=(0, s * 90, 0))
        if led is not None:
            g.torus((cx + s * (half_w + 2.1), cy, cz), cup_r * 0.6, 0.45, led, axis="x")


def goggles(g, x, z, r, frame, lens, strap, head_c=None, head_r=None):
    for cx in (x, 2 * CX - x):
        y0 = g.front_y(cx, z)
        if y0 is None:
            continue
        g.cyl((cx, y0 + 0.6, z), r + 0.6, 1.8, frame, axis="-y")
        g.cyl((cx, y0 - 1.3, z), r - 0.2, 0.4, lens, axis="-y")
    if head_c is not None:
        g.torus(head_c, head_r, 0.75, strap)


def bow_tie(g, c, s, mat, knot):
    cx, cy, cz = c
    g.ell((cx - s, cy, cz), (s, 0.9, s * 0.65), mat, rot=(0, 0, 0))
    g.ell((cx + s, cy, cz), (s, 0.9, s * 0.65), mat)
    g.sphere((cx, cy - 0.3, cz), s * 0.42, knot)


def scarf(g, c, rx, ry, r, mat, tail_dir=1, tail_len=8, stripe=None):
    cx, cy, cz = c
    from vox import stripes as _stripes
    m = _stripes("z", 1.6, [mat, stripe]) if stripe else mat
    g.torus((cx, cy, cz), max(rx, ry), r, m, rot=(0, 0, 0))
    tx = cx + tail_dir * rx * 0.55
    g.curve([(tx, cy - ry - 0.5, cz - 0.5), (tx + tail_dir * 1.5, cy - ry - 1.5, cz - tail_len * 0.5),
             (tx + tail_dir * 2.5, cy - ry - 1.0, cz - tail_len)], [r * 0.9, r * 0.85, r * 0.8], m)


def sneaker(g, x, y, z, L, W, H, main, accent, sole=None, lace=None, sym=True):
    """Chunky cartoon sneaker, toe pointing to -y. (x, y, z) = heel-bottom centre."""
    sole = sole or SOLE
    lace = lace or LACE
    g.rbox((x, y - L * 0.45, z + H * 0.16), (W, L * 0.62, H * 0.17), sole, n=4, sym=sym)
    g.rbox((x, y - L * 0.3, z + H * 0.52), (W * 0.9, L * 0.5, H * 0.38), main, n=4, sym=sym)
    g.ell((x, y - L * 0.78, z + H * 0.42), (W * 0.88, L * 0.32, H * 0.32), main, sym=sym)
    g.ell((x, y - L * 0.95, z + H * 0.28), (W * 0.8, L * 0.16, H * 0.16), sole, sym=sym)
    g.decal((y - L, y), (z + H * 0.3, z + H * 0.85),
            lambda A, B: np.abs((B - (z + H * 0.55)) - 0.45 * np.sin((A - y) * 0.9)) <= H * 0.08,
            accent, direction="-x", only=[main])
    for k in range(3):
        yy = y - L * (0.55 + k * 0.14)
        g.seg((x - W * 0.45, yy, z + H * 0.86 - k * 0.6), (x + W * 0.45, yy, z + H * 0.86 - k * 0.6), 0.45, lace,
              sym=sym)


def halo(g, c, R, r, mat):
    g.torus(c, R, r, mat)


def zzz(g, x, y, z, s, mat):
    g.seg((x - s, y, z + s), (x + s, y, z + s), 0.55, mat)
    g.seg((x + s, y, z + s), (x - s, y, z - s), 0.55, mat)
    g.seg((x - s, y, z - s), (x + s, y, z - s), 0.55, mat)


def music_note(g, x, y, z, s, mat):
    g.ell((x, y, z), (s * 0.75, s * 0.5, s * 0.55), mat, rot=(0, -20, 0))
    g.seg((x + s * 0.65, y, z), (x + s * 0.65, y, z + s * 2.6), 0.45, mat)
    g.seg((x + s * 0.65, y, z + s * 2.6), (x + s * 1.7, y, z + s * 2.0), 0.45, mat)
