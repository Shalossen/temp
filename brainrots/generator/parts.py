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
    bands_: list of (z0, z1, shift_x)."""
    from vox import PALETTE
    ia = PALETTE.get(edge_a)
    ib = PALETTE.get(edge_b)
    for z0, z1, sh in bands_:
        slab = g.v[:, :, z0:z1 + 1].copy()
        slab = np.roll(slab, sh, axis=0)
        filled = slab > 0
        right = filled & ~np.roll(filled, -1, axis=0)
        left = filled & ~np.roll(filled, 1, axis=0)
        slab[right] = ia
        slab[left] = ib
        g.v[:, :, z0:z1 + 1] = slab
