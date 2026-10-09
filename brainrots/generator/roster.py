"""The 30 original brainrots. Each builder returns a filled Grid.

Front = -y, up = +z, symmetry plane x = CX (72), depth centre y = CY (72).
"""
import math

import numpy as np

from parts import (BLACK, BLUSH, CHROME_DARK, EYE_WHITE, FLAME_O, FLAME_R, FLAME_Y, GLASS, GOLD,
                   GOLD_DARK, MOUTH, ORANGE_BEAK, PUPIL, RUBBER, SHINE, SILVER, SMOKE, TONGUE,
                   TOOTH, WATER, WHITE, WOOD, WOOD_LIGHT, YELLOW_BEAK, bird_foot, blush,
                   cone_spikes, dot_eye, eye, leg, open_mouth, smile, sparkle)
from vox import (CX, CY, Grid, Mat, angular, bands, checker, hue_mats, speckle, stripes)

ROSTER = []

RARITIES = {
    "Common": (150, 160, 170),
    "Rare": (60, 140, 255),
    "Epic": (170, 70, 255),
    "Legendary": (255, 170, 30),
    "Mythic": (255, 60, 90),
    "Divine": (255, 230, 120),
    "Secret": (20, 20, 20),
}


def brainrot(num, name, rarity, income, concept):
    def deco(fn):
        ROSTER.append(dict(num=num, name=name, rarity=rarity, income=income,
                           concept=concept, build=fn))
        return fn
    return deco


C = CX
Y = CY


# ============================================================================
# COMMON
# ============================================================================
@brainrot(1, "Lampadino Pinguino", "Common", "$5/s",
          "Pingouin dont la tête est une ampoule allumée, vissée à la place du cou.")
def lampadino_pinguino():
    g = Grid()
    navy = Mat("peng_navy", (44, 52, 84), rough=0.55, shades=2, amt=0.05)
    cream = Mat("peng_cream", (250, 246, 232), rough=0.55)
    bulb = Mat("bulb_glow", (255, 222, 96), rough=0.12, emit=0.45)
    fil = Mat("bulb_filament", (255, 160, 60), rough=0.2, emit=3.0)
    thread = Mat("bulb_thread", (176, 182, 196), rough=0.25, metal=1.0)
    thread_d = Mat("bulb_thread_d", (118, 124, 140), rough=0.3, metal=1.0)
    feet = Mat("peng_feet", (255, 150, 40), rough=0.5)

    g.ell((C, Y, 16), (13, 11, 15), navy)
    g.ell((C, Y - 4.5, 14), (10, 7.5, 12), cream, mode="paint")
    g.ell((C - 13, Y + 1, 16), (2.6, 6, 9.5), navy, rot=(0, -20, 0), sym=True)
    g.rbox((C - 5.5, Y - 7, 1.7), (3.8, 5, 1.7), feet, n=3, sym=True)
    g.cyl((C, Y, 27), 8.2, 2, navy)
    g.cyl((C, Y, 28), 7, 6, stripes("z", 2, [thread, thread_d]))
    g.cyl((C, Y, 33), 7.5, 6, bulb, r2=10.5)
    g.sphere((C, Y, 47), 13.5, bulb)
    g.decal((C - 6, C + 6), (52, 57), lambda A, B: np.abs(B - (54.5 + 1.8 * np.sin((A - C) * 1.1))) <= 0.7,
            fil, only=[bulb])
    eye(g, C - 5, 46, r=4.0, look=(0.6, -0.2), pupil=0.58)
    g.cyl((C, Y - 12.5, 40.5), 2.6, 5.5, feet, axis="-y", r2=0.8)
    blush(g, C - 9.5, 41.5, rx=2.4, rz=1.3, only=[bulb])
    smile(g, C, 37.5, 2.5, curve=1.2, only=[bulb])
    g.decal((C + 6, C + 10), (49, 56), lambda A, B: ((A - (C + 8)) / 1.2) ** 2 + ((B - 52.5) / 2.6) ** 2 <= 1,
            SHINE, only=[bulb])
    return g


@brainrot(2, "Gommarello Ranocchio", "Common", "$8/s",
          "Grenouille-gomme bicolore (rose et bleue), un coin déjà usé.")
def gommarello_ranocchio():
    g = Grid()
    pink = Mat("eraser_pink", (246, 120, 150), rough=0.85)
    blue = Mat("eraser_blue", (72, 132, 232), rough=0.85)
    frog = Mat("frog_green", (110, 205, 80), rough=0.6, shades=2, amt=0.05)
    belly = Mat("frog_belly", (215, 240, 150), rough=0.6)

    g.rbox((C, Y, 11), (15, 10.5, 10), bands("x", [(0, pink), (C + 4, blue)]), n=6)
    g.sphere((C - 15, Y - 10, 21), 4.5, pink, mode="carve")     # worn corner
    g.sphere((C - 7.5, Y - 3, 21), 5.5, frog, sym=True)
    eye(g, C - 7.5, 22.5, r=3.9, look=(0.6, 0.0), pupil=0.56)
    smile(g, C, 10, 10, curve=3.8, thick=1)
    blush(g, C - 11, 12.5, rx=2.0, rz=1.0)
    g.seg((C - 9, Y - 8, 5), (C - 11, Y - 11, 1.2), 2.3, frog, sym=True)
    for k in (-1.7, 0, 1.7):
        g.ell((C - 11 + k, Y - 13.5, 0.9), (1.0, 1.8, 0.9), frog, sym=True)
    g.ell((C - 14.5, Y + 5, 5), (3.6, 7, 4.6), frog, rot=(0, 0, -12), sym=True)
    g.ell((C - 16, Y - 1, 1.2), (3.2, 4.6, 1.2), frog, sym=True)
    g.ell((C - 14.5, Y + 4, 6), (2.6, 5.5, 3), belly, mode="paint", sym=True)
    rng = np.random.default_rng(2)
    for _ in range(9):
        x = C + rng.uniform(-22, 22)
        y = Y - 14 + rng.uniform(-6, 4)
        g.box((x, y, 0), (x + rng.integers(0, 2), y + rng.integers(0, 2), rng.integers(0, 2)),
              pink if rng.random() < 0.6 else blue)
    return g


@brainrot(3, "Spugnetta Lumachina", "Common", "$12/s",
          "Escargot menthe dont la coquille est une éponge de cuisine qui fait des bulles.")
def spugnetta_lumachina():
    g = Grid()
    mint = Mat("snail_mint", (140, 222, 192), rough=0.45, shades=2, amt=0.04)
    sponge = Mat("sponge_yellow", (252, 214, 72), rough=0.9, shades=3, amt=0.07, scale=1)
    scrub = Mat("sponge_scrub", (60, 162, 82), rough=0.95, shades=3, amt=0.1, scale=1)
    hole = Mat("sponge_hole", (196, 146, 36), rough=0.9)
    bubble = Mat("bubble", (214, 240, 255), rough=0.03, emit=0.45)
    foam = Mat("foam", (250, 252, 255), rough=0.8, emit=0.1)

    g.tube([(C, Y - 9, 4.5), (C, Y + 6, 4), (C, Y + 22, 2.4)], [6.2, 5.8, 2.0], mint)
    g.curve([(C, Y - 7, 5), (C, Y - 11, 13), (C, Y - 12, 21)], [6.2, 6.2, 6.5], mint)
    g.ell((C, Y - 12, 25), (8, 7.2, 7.2), mint)
    g.curve([(C - 3, Y - 13, 29), (C - 5, Y - 14, 35), (C - 6.5, Y - 15, 39)], [1.7, 1.5, 1.5], mint, sym=True)
    g.sphere((C - 6.5, Y - 15, 41.5), 3.9, mint, sym=True)
    eye(g, C - 6.5, 41.8, r=3.3, look=(0.5, 0.2), pupil=0.55)
    smile(g, C, 22.5, 3.2, curve=1.5)
    blush(g, C - 5, 24, rx=1.8, rz=1.0)
    # sponge shell
    g.rbox((C, Y + 7, 15.5), (9, 10.5, 10.5), sponge, n=5)
    g.rbox((C, Y + 7, 15.5), (9.6, 11.1, 11.1), scrub, n=5, mode="paint", where=lambda X, Y_, Z: Z >= 22)
    rng = np.random.default_rng(3)
    for _ in range(60):
        face = rng.integers(0, 3)
        if face == 0:
            p = (C + rng.choice([-9, 9]), Y + 7 + rng.uniform(-9, 9), rng.uniform(7, 21))
        elif face == 1:
            p = (C + rng.uniform(-7, 7), Y + 17.5, rng.uniform(7, 21))
        else:
            p = (C + rng.uniform(-7, 7), Y - 3.5, rng.uniform(9, 21))
        r = rng.uniform(1.0, 1.6)
        g.sphere(p, r + 0.7, hole, mode="paint", only=[sponge])
        g.sphere(p, r, sponge, mode="carve")
    for p, r in (((C - 4, Y + 4, 27.5), 2.2), ((C + 1, Y + 8, 28), 2.8), ((C + 5, Y + 12, 27.3), 2.0),
                 ((C - 2, Y + 13, 27.2), 1.8)):
        g.sphere(p, r, foam)
    for p, r in (((C + 13, Y - 4, 31), 3.0), ((C + 16, Y - 7, 39), 2.0), ((C - 14, Y + 2, 34), 2.4),
                 ((C + 9, Y + 4, 38), 1.5)):
        g.sphere(p, r, bubble)
    return g


@brainrot(4, "Pomodorino Granchietto", "Common", "$18/s",
          "Crabe-tomate cerise : pinces de crabe, yeux sur pédoncules, feuilles vertes sur la tête.")
def pomodorino_granchietto():
    g = Grid()
    red = Mat("tomato_red", (234, 54, 44), rough=0.3, shades=2, amt=0.05, scale=3)
    leaf = Mat("tomato_leaf", (72, 168, 62), rough=0.6, shades=2, amt=0.06)
    crab = Mat("crab_orange", (246, 112, 62), rough=0.5)
    crab_l = Mat("crab_light", (255, 190, 140), rough=0.5)

    g.ell((C, Y, 15), (14.5, 12.5, 11), red)
    for k in range(5):
        a = math.radians(k * 72 + 18)
        g.ell((C + 5 * math.cos(a), Y + 5 * math.sin(a), 26), (5, 2, 1.1), leaf, rot=(0, 0, k * 72 + 18))
    g.curve([(C, Y, 25), (C, Y, 29), (C + 1.5, Y, 31)], [1.4, 1.2, 1.0], leaf)
    g.seg((C - 4, Y - 8, 23), (C - 5.5, Y - 10, 31), 1.4, crab, sym=True)
    g.sphere((C - 5.5, Y - 10.5, 33), 3.5, crab, sym=True)
    eye(g, C - 5.5, 33.3, r=3.0, look=(0.5, 0.0), pupil=0.56)
    g.tube([(C - 12, Y - 4, 13), (C - 17, Y - 9, 15), (C - 20, Y - 13, 19)], [2.3, 2.1, 2.1], crab, sym=True)
    g.ell((C - 21, Y - 16, 22), (4.6, 5.2, 4.6), crab, sym=True)
    g.ell((C - 21, Y - 16, 22), (4.6, 5.2, 4.6), crab_l, mode="paint", where=lambda X, Y_, Z: Z <= 20, sym=True)
    g.rbox((C - 21, Y - 20.5, 22.5), (5.5, 3.5, 1.0), crab, n=3, mode="carve", sym=True)
    for k in range(3):
        yy = Y - 2 + k * 5
        g.tube([(C - 12, yy, 9), (C - 17, yy + 1, 7), (C - 19.5, yy + 2, 0.8)], [1.5, 1.3, 1.0], crab, sym=True)
    open_mouth(g, C, 13, 3.6, 3.0, teeth=False, only=[red])
    blush(g, C - 9, 14.5, rx=2.0, rz=1.1, only=[red])
    return g


@brainrot(5, "Ombrellino Pipistrello", "Common", "$25/s",
          "Chauve-souris dont les ailes sont un parapluie rayé ; la poignée sert de queue.")
def ombrellino_pipistrello():
    g = Grid()
    fur = Mat("bat_fur", (96, 72, 126), rough=0.7, shades=2, amt=0.06)
    face = Mat("bat_face", (190, 160, 210), rough=0.7)
    ca = Mat("umb_teal", (40, 192, 204), rough=0.45)
    cb = Mat("umb_yellow", (252, 214, 70), rough=0.45)
    rib = Mat("umb_rib", (56, 48, 70), rough=0.5)
    handle = Mat("umb_handle", (176, 74, 40), rough=0.35)
    ear_in = Mat("bat_ear_in", (240, 150, 190), rough=0.6)

    g.ell((C, Y, 17), (8, 7, 9.5), fur)
    g.ell((C, Y - 1, 31), (9, 8, 8), fur)
    g.front_ellipse(C, 30, 6.5, 5, face)
    g.cyl((C - 5.5, Y, 36), 3.2, 9, fur, r2=0.5, rot=(0, -22, 0), sym=True)
    g.cyl((C - 5.6, Y - 1.4, 37), 1.8, 6.5, ear_in, r2=0.3, rot=(0, -22, 0), mode="paint", sym=True)
    eye(g, C - 3.4, 31.5, r=3.0, pupil=0.6)
    smile(g, C, 27.5, 2.6, curve=1.1, only=[face])
    for sx in (C - 1.2, C + 1.2):
        y0 = g.front_y(sx, 26.5)
        if y0 is not None:
            g.box((sx, y0 - 1, 25), (sx, y0, 26), TOOTH)
    # umbrella wings
    for s in (-1, 1):
        root = (C + s * 6, Y + 2, 24)
        pat = angular(root, 8, [ca, cb], axis="y", phase=0.03)
        g.ell((C + s * 18, Y + 2, 25), (14, 1.8, 10.5), pat, rot=(0, s * -12, 0))
        for k in range(5):
            x = C + s * (8 + k * 5.5)
            g.sphere((x, Y + 2, 15.5 - abs(k - 2) * 0.6), 2.7, fur, mode="carve")
        for a in (-60, -25, 10, 45):
            ar = math.radians(a)
            tip = (root[0] + s * 22 * math.cos(ar), Y + 0.6, root[2] + 22 * math.sin(ar) * 0.62)
            g.seg((root[0], Y + 0.6, root[2]), tip, 0.7, rib)
            g.sphere(tip, 1.1, rib)
    g.curve([(C, Y + 6, 12), (C, Y + 11, 8), (C, Y + 12, 3), (C, Y + 15, 1.5), (C, Y + 17.5, 3.5)],
            [1.5, 1.5, 1.5, 1.5, 1.5], handle)
    g.seg((C - 3, Y, 9), (C - 3.5, Y - 1, 2.5), 1.5, fur, sym=True)
    g.ell((C - 3.5, Y - 2.5, 1.4), (2.1, 3, 1.4), rib, sym=True)
    return g


@brainrot(6, "Candelino Gufetto", "Common", "$35/s",
          "Bébé hibou en cire de bougie, flamme sur la tête, posé sur un bougeoir doré.")
def candelino_gufetto():
    g = Grid()
    wax = Mat("wax", (250, 238, 214), rough=0.45, shades=2, amt=0.03)
    drip = Mat("wax_drip", (255, 248, 232), rough=0.3)
    ring = Mat("owl_ring", (238, 208, 166), rough=0.5)
    iris = Mat("owl_iris", (255, 186, 36), rough=0.2)
    vmark = Mat("owl_v", (214, 186, 150), rough=0.5)

    g.cyl((C, Y, 0), 14.5, 2.5, GOLD)
    g.torus((C, Y, 2.5), 13.3, 1.3, GOLD)
    g.torus((C + 15.5, Y, 3.5), 3.6, 1.0, GOLD, axis="y")
    g.cyl((C, Y, 2.5), 10, 27, wax)
    g.cyl((C, Y, 27.5), 7.5, 3, wax, mode="carve")
    g.torus((C, Y, 29), 8.8, 1.7, wax)
    for a, ln in ((200, 9), (232, 5), (305, 4), (338, 11), (20, 7), (62, 12), (118, 8), (160, 13)):
        ar = math.radians(a)
        x, y = C + 10.1 * math.cos(ar), Y + 10.1 * math.sin(ar)
        g.seg((x, y, 29.5), (x, y, 29.5 - ln), 1.6, drip, r1=1.9)
    g.cyl((C, Y, 27.5), 0.8, 4.5, BLACK)
    g.ell((C, Y, 38), (4.6, 4.6, 7.8), bands("z", [(0, FLAME_Y), (39, FLAME_O), (43.5, FLAME_R)]))
    g.cyl((C - 7, Y - 1, 29.5), 2.8, 6, wax, r2=0.4, rot=(0, -28, 0), sym=True)
    g.front_ellipse(C - 4.7, 19, 4.8, 5, ring, sym=True)
    eye(g, C - 4.7, 19, r=3.8, iris=iris, pupil=0.42)
    g.cyl((C, Y - 10, 15.5), 1.9, 3.8, ORANGE_BEAK, axis="-y", r2=0.5)
    for z in (6.5, 10):
        for xc in (C - 3, C + 3):
            g.decal((xc - 2, xc + 2), (z - 1, z + 1),
                    lambda A, B, xc=xc, z=z: (np.abs(B - (z + np.abs(A - xc) * 0.6)) <= 0.5) & (np.abs(A - xc) <= 2),
                    vmark, only=[wax])
    g.ell((C - 10, Y + 1, 13), (2.3, 5, 8.5), wax, rot=(0, -10, 0), sym=True)
    bird_foot(g, C - 4, Y - 8.5, ORANGE_BEAK, z=3.2, toe=2.6, r=0.9)
    return g


# ============================================================================
# RARE
# ============================================================================
@brainrot(7, "Ventilatore Pavone", "Rare", "$60/s",
          "Paon bleu dont la roue de plumes est un ventilateur de bureau.")
def ventilatore_pavone():
    g = Grid()
    blue = Mat("peacock_blue", (32, 92, 214), rough=0.4, shades=2, amt=0.06)
    teal = Mat("peacock_teal", (22, 164, 176), rough=0.4)
    blade = Mat("fan_blade", (44, 182, 134), rough=0.35, shades=2, amt=0.05, scale=3)
    spot_d = Mat("feather_eye", (42, 40, 150), rough=0.3)
    spot_g = Mat("feather_gold", (242, 192, 52), rough=0.3, metal=0.4)
    leg_m = Mat("peacock_leg", (150, 140, 150), rough=0.6)

    fy, fz = Y + 11, 30
    g.cyl((C, fy + 3, 0), 9, 2.5, SILVER)
    g.seg((C, fy + 3, 2), (C, fy + 3, fz - 6), 1.8, SILVER)
    g.ell((C, fy + 4, fz), (5.5, 5, 5.5), CHROME_DARK)
    for k in range(5):
        a = 90 + k * 72
        ar = math.radians(a)
        cx, cz = C + 10.5 * math.cos(ar), fz + 10.5 * math.sin(ar)
        g.ell((cx, fy, cz), (8.5, 1.4, 4.8), blade, rot=(0, -a, 0))
        sx, sz = C + 14 * math.cos(ar), fz + 14 * math.sin(ar)
        g.decal((sx - 4, sx + 4), (sz - 4, sz + 4), lambda A, B, sx=sx, sz=sz: (A - sx) ** 2 + (B - sz) ** 2 <= 7.5,
                spot_g, only=[blade])
        g.decal((sx - 3, sx + 3), (sz - 3, sz + 3), lambda A, B, sx=sx, sz=sz: (A - sx) ** 2 + (B - sz) ** 2 <= 2.6,
                spot_d, only=[spot_g])
    g.sphere((C, fy - 1.5, fz), 3.2, SILVER)
    g.torus((C, fy - 2, fz), 20, 1.0, SILVER, axis="y")
    for a in range(0, 360, 30):
        ar = math.radians(a)
        g.seg((C + 3 * math.cos(ar), fy - 2.5, fz + 3 * math.sin(ar)),
              (C + 20 * math.cos(ar), fy - 2, fz + 20 * math.sin(ar)), 0.6, SILVER)
    g.ell((C, Y - 2, 16), (7.5, 8, 10), blue)
    g.front_ellipse(C, 17, 4.5, 6.5, teal)
    g.ell((C - 7.5, Y - 1, 16), (2.2, 6, 7.5), teal, rot=(0, -8, 0), sym=True)
    g.curve([(C, Y - 4, 23), (C, Y - 6, 31), (C, Y - 7, 37)], [4.6, 3.6, 3.3], blue)
    g.sphere((C, Y - 7.5, 40), 5, blue)
    for dx in (-2.4, 0, 2.4):
        g.seg((C + dx, Y - 7, 44), (C + dx * 1.8, Y - 7, 50), 0.6, teal)
        g.sphere((C + dx * 1.8, Y - 7, 50.5), 1.3, teal)
    eye(g, C - 2.5, 40.5, r=2.4, pupil=0.62)
    g.cyl((C, Y - 12, 38.5), 1.4, 3.2, YELLOW_BEAK, axis="-y", r2=0.3)
    g.seg((C - 3, Y - 1, 7), (C - 3, Y - 2, 1), 0.9, leg_m, sym=True)
    bird_foot(g, C - 3, Y - 2, leg_m, z=0.8, toe=2.8, r=0.8)
    return g


@brainrot(8, "Lavatricino Polpetto", "Rare", "$90/s",
          "Pieuvre qui sort du hublot d'une machine à laver, une chaussette dans un tentacule.")
def lavatricino_polpetto():
    g = Grid()
    body = Mat("washer_white", (238, 240, 246), rough=0.35)
    panel = Mat("washer_panel", (200, 208, 222), rough=0.4)
    inside = Mat("washer_inside", (66, 74, 90), rough=0.5)
    octo = Mat("octo_purple", (192, 92, 204), rough=0.45, shades=2, amt=0.05)
    octo_l = Mat("octo_light", (244, 176, 240), rough=0.45)
    screen = Mat("washer_screen", (90, 240, 220), rough=0.2, emit=2.0)
    sock_r = Mat("sock_red", (236, 64, 70), rough=0.8)
    bubble = Mat("bubble", (214, 240, 255), rough=0.03, emit=0.45)
    foam = Mat("foam", (250, 252, 255), rough=0.8, emit=0.1)

    g.rbox((C, Y + 2, 20), (14, 12, 18), body, n=8)
    g.rbox((C, Y + 2, 20), (14.3, 12.3, 18.3), panel, n=8, mode="paint", where=lambda X, Y_, Z: Z >= 33)
    g.decal((C - 11, C - 3), (33.5, 36), lambda A, B: np.ones(A.shape, bool), screen)
    g.cyl((C + 8, Y - 10, 34.7), 2.2, 1.6, SILVER, axis="-y")
    for xx in (C - 11, C + 11):
        for yy in (Y - 7, Y + 11):
            g.box((xx - 1, yy - 1, 0), (xx + 1, yy + 1, 2), RUBBER)
    g.cyl((C, Y - 11, 18), 9.2, 8, inside, axis="y", mode="paint")
    g.cyl((C, Y - 11, 18), 8.2, 6, inside, axis="y", mode="carve")
    g.ell((C, Y - 10, 20), (8.6, 8, 8.4), octo)
    eye(g, C - 3.6, 22, r=3.4, pupil=0.6, look=(0, 0.3))
    open_mouth(g, C, 16.5, 2.2, 2.0, teeth=False, only=[octo])
    blush(g, C - 6.5, 17.5, rx=1.6, rz=0.9, only=[octo])
    # open door on its hinge
    g.torus((C - 9.5, Y - 19.5, 18), 8.5, 1.9, SILVER, axis="x")
    g.cyl((C - 10.2, Y - 19.5, 18), 7, 1.4, GLASS, axis="x")
    tent = bands("z", [(0, octo_l), (2.2, octo)])
    for i, (x0, x1, x2) in enumerate(((-6, -11, -17), (-3, -5, -8), (-0.5, 0, 1), (3, 5, 8), (6, 11, 17))):
        g.curve([(C + x0, Y - 14, 13), (C + x0 * 1.1, Y - 17, 7), (C + x1, Y - 19, 2),
                 (C + x2, Y - 23 - (i % 2) * 3, 1.3), (C + x2 * 1.08, Y - 25 - (i % 2) * 3, 3.2)],
                [2.6, 2.3, 1.9, 1.3, 0.9], tent)
    g.curve([(C + 7, Y - 11, 22), (C + 12, Y - 14, 28), (C + 16, Y - 13, 34)], [2.4, 1.8, 1.4], octo)
    g.tube([(C + 16, Y - 13, 34), (C + 16.5, Y - 13, 28), (C + 19, Y - 13, 27)], [1.7, 1.7, 1.8],
           stripes("z", 2, [sock_r, WHITE]))
    for p, r in (((C - 5, Y - 12, 26), 2.0), ((C + 2, Y - 13, 27), 2.5), ((C - 1, Y - 12, 28.5), 1.6)):
        g.sphere(p, r, foam)
    for p, r in (((C - 15, Y - 6, 30), 2.4), ((C - 18, Y - 9, 37), 1.6), ((C + 18, Y - 4, 40), 1.8)):
        g.sphere(p, r, bubble)
    return g


@brainrot(9, "Microondino Riccio", "Rare", "$140/s",
          "Hérisson dont le corps est un micro-ondes allumé ; ses piquants brillent comme des braises.")
def microondino_riccio():
    g = Grid()
    case = Mat("micro_case", (232, 236, 242), rough=0.35)
    window = Mat("micro_window", (38, 42, 52), rough=0.08)
    glow = Mat("micro_glow", (255, 176, 80), rough=0.3, emit=1.6)
    btn = Mat("micro_btn", (176, 184, 198), rough=0.4)
    disp = Mat("micro_display", (110, 255, 140), rough=0.2, emit=2.5)
    skin = Mat("hedgehog_skin", (234, 192, 150), rough=0.6)
    spine = Mat("hedgehog_spine", (122, 84, 58), rough=0.7, shades=2, amt=0.08)
    tip = Mat("spine_tip", (255, 140, 60), rough=0.5, emit=1.2)

    g.rbox((C, Y + 2, 14), (16, 11, 11), case, n=10)
    g.decal((C - 12, C + 5), (7, 21), lambda A, B: np.ones(A.shape, bool), window)
    g.decal((C - 10, C + 3), (9, 19), lambda A, B: ((A - (C - 3.5)) / 6.5) ** 2 + ((B - 14) / 5) ** 2 <= 1, glow,
            only=[window])
    g.decal((C + 8, C + 14), (18, 20), lambda A, B: np.ones(A.shape, bool), disp)
    for zz in (9, 12, 15):
        for xx in (C + 9, C + 12):
            g.decal((xx, xx + 1), (zz, zz + 1), lambda A, B: np.ones(A.shape, bool), btn)
    for xx, yy in ((C - 11, Y - 6), (C - 11, Y + 10)):
        g.ell((xx, yy, 1.6), (2.6, 3.2, 1.8), skin, sym=True)
    pts = []
    for xx in np.arange(C - 14, C + 14.1, 4.6):
        for yy in np.arange(Y - 2, Y + 12.1, 4.6):
            pts.append((xx, yy, 25))
    for xx in np.arange(C - 13, C + 13.1, 5.2):
        for zz in (8, 14, 20):
            pts.append((xx, Y + 13, zz))
    cone_spikes(g, pts, spine, r=2.0, length=7.0, center=(C, Y + 2, 4), tip_mat=tip)
    g.ell((C, Y - 6, 28), (8, 7, 6.5), skin)
    for xx in np.arange(C - 6, C + 6.1, 4):
        cone_spikes(g, [(xx, Y - 3, 33)], spine, r=1.8, length=6, center=(C, Y + 4, 20), tip_mat=tip)
    g.cyl((C, Y - 12, 27.5), 3.2, 4, skin, axis="-y", r2=1.9)
    g.sphere((C, Y - 16, 28), 1.7, BLACK)
    eye(g, C - 3.4, 30.5, r=2.5, pupil=0.62)
    g.sphere((C - 6.5, Y - 4, 33), 1.9, skin, sym=True)
    smile(g, C, 25.5, 2.4, curve=0.9, only=[skin])
    return g


@brainrot(10, "Sveglia Coniglietta", "Rare", "$200/s",
          "Lapine-réveil : cadran pour visage, cloches dorées et longues oreilles.")
def sveglia_coniglietta():
    g = Grid()
    case = Mat("clock_case", (250, 140, 178), rough=0.3, metal=0.2)
    face = Mat("clock_face", (255, 252, 240), rough=0.4)
    tick = Mat("clock_tick", (64, 52, 76), rough=0.5)
    fur = Mat("bunny_white", (250, 248, 252), rough=0.7, shades=2, amt=0.03)
    pink = Mat("bunny_pink", (255, 168, 190), rough=0.6)

    g.cyl((C, Y - 5, 23), 14, 11, case, axis="y")
    g.cyl((C, Y - 6, 23), 11.6, 1.6, face, axis="y")
    g.torus((C, Y - 6, 23), 12.4, 1.5, GOLD, axis="y")
    for k in range(12):
        a = math.radians(k * 30)
        tx, tz = C + 9.6 * math.sin(a), 23 + 9.6 * math.cos(a)
        rr = 0.9 if k % 3 == 0 else 0.5
        g.decal((tx - 1, tx + 1), (tz - 1, tz + 1), lambda A, B, tx=tx, tz=tz, rr=rr: (A - tx) ** 2 + (B - tz) ** 2 <= rr * rr + 0.3,
                tick, only=[face])
    for s in (-1, 1):
        g.sphere((C + s * 8, Y, 37), 5.8, GOLD, where=lambda X, Y_, Z: Z >= 35.5)
        g.torus((C + s * 8, Y, 35.6), 5.6, 0.9, GOLD_DARK)
    g.seg((C, Y, 36), (C, Y, 42.5), 0.8, GOLD)
    g.sphere((C, Y, 43.5), 1.6, GOLD)
    g.ell((C - 4.5, Y + 2.5, 50), (3, 2.2, 10), fur, rot=(0, -14, 0), sym=True)
    g.ell((C - 4.5, Y + 0.6, 50), (1.6, 1.2, 7.5), pink, rot=(0, -14, 0), mode="paint", sym=True)
    eye(g, C - 4.3, 25.5, r=3.0, pupil=0.6)
    g.front_ellipse(C, 21, 1.5, 1.0, pink)
    smile(g, C - 1.3, 19.2, 1.3, curve=0.8, only=[face])
    smile(g, C + 1.3, 19.2, 1.3, curve=0.8, only=[face])
    g.decal((C - 1, C + 1), (16.5, 18), lambda A, B: np.ones(A.shape, bool), Mat.of((235, 235, 225)), only=[face])
    for zz in (20.5, 22):
        g.decal((C - 11, C - 6.5), (zz, zz), lambda A, B: np.ones(A.shape, bool), tick, sym=True, only=[face])
    blush(g, C - 7, 19.5, rx=1.8, rz=1.0, only=[face])
    g.seg((C - 6, Y, 10), (C - 6.5, Y - 3, 4), 1.6, GOLD, sym=True)
    g.ell((C - 6.5, Y - 6, 2.5), (3.8, 6.5, 2.5), fur, sym=True)
    g.ell((C - 14.8, Y - 3, 19), (2.4, 2.7, 3.3), fur, sym=True)
    g.sphere((C, Y + 8, 15), 4.2, fur)
    return g


@brainrot(11, "Pennellone Volpino", "Rare", "$300/s",
          "Renard malin dont la queue est un gros pinceau trempé dans la peinture bleue.")
def pennellone_volpino():
    g = Grid()
    fox = Mat("fox_orange", (242, 122, 42), rough=0.6, shades=3, amt=0.05)
    fw = Mat("fox_white", (252, 246, 236), rough=0.6)
    fd = Mat("fox_dark", (60, 40, 42), rough=0.6)
    handle = Mat("brush_handle", (230, 62, 72), rough=0.25)
    pb = Mat("paint_blue", (40, 122, 255), rough=0.12, emit=0.2)
    py = Mat("paint_yellow", (255, 214, 40), rough=0.12)
    pp = Mat("paint_pink", (255, 82, 162), rough=0.12)

    g.ell((C, Y + 2, 14), (9.5, 10, 13), fox)
    g.ell((C, Y - 4, 15), (6, 5, 9), fw, mode="paint")
    g.ell((C - 8, Y + 4, 6), (4.2, 7, 6), fox, sym=True)
    g.seg((C - 4, Y - 5, 12), (C - 4, Y - 7, 2.6), 2.6, fox, sym=True)
    g.ell((C - 4, Y - 8.5, 1.6), (2.7, 3.3, 1.6), fd, sym=True)
    g.ell((C, Y - 3, 32), (9.5, 8, 8), fox)
    g.ell((C - 5, Y - 8, 29.5), (4, 3, 3), fw, mode="paint", sym=True)
    g.ell((C, Y - 11, 29.5), (3.8, 4.6, 3), fw)
    g.sphere((C, Y - 15.4, 30.6), 1.6, BLACK)
    g.cyl((C - 5.5, Y - 2, 38), 3.9, 9.5, fox, r2=0.3, ry=2.2, rot=(0, -18, 0), sym=True)
    g.cyl((C - 5.5, Y - 2, 38), 4.2, 9.5, fd, r2=0.4, ry=2.5, rot=(0, -18, 0), mode="paint",
          where=lambda X, Y_, Z: Z >= 44, sym=True)
    g.cyl((C - 5.5, Y - 3.4, 38.5), 2.2, 6.5, fw, r2=0.2, ry=1, rot=(0, -18, 0), mode="paint", sym=True)
    eye(g, C - 4, 33.2, r=2.9, pupil=0.6, lid=0.28, lid_mat=fox, lid_tilt=0.25, look=(0.5, 0))
    smile(g, C, 27.3, 2.4, curve=1.0, only=[fw])
    g.seg((C + 4, Y + 10, 8), (C + 12, Y + 18, 18), 1.9, handle)
    g.seg((C + 12, Y + 18, 18), (C + 14, Y + 20, 21), 2.7, SILVER)
    g.ell((C + 16, Y + 21, 28), (5, 5, 8.5), fox, rot=(-10, 25, 0))
    g.ell((C + 17.8, Y + 22, 34), (4.4, 4.4, 4), pb, mode="paint")
    for dx, ln in ((-1.5, 5), (2, 7), (0.5, 3)):
        g.seg((C + 18 + dx, Y + 19.5, 32), (C + 18 + dx, Y + 19.5, 32 - ln), 0.9, pb)
    for (x, y, r, m) in ((C - 10, Y - 13, 3.2, pb), (C + 9, Y - 14, 2.6, py), (C + 2, Y - 18, 1.9, pp),
                         (C + 19, Y + 14, 2.4, pb)):
        g.cyl((x, y, 0), r, 1, m)
    return g


@brainrot(12, "Innaffiatoio Elefantino", "Rare", "$450/s",
          "Bébé éléphant-arrosoir : sa trompe est le bec verseur, une fleur pousse sur son dos.")
def innaffiatoio_elefantino():
    g = Grid()
    can = Mat("can_green", (70, 182, 122), rough=0.3, metal=0.5)
    can_d = Mat("can_green_dark", (48, 140, 96), rough=0.3, metal=0.5)
    ele = Mat("ele_blue", (150, 176, 232), rough=0.55, shades=2, amt=0.04)
    ear_in = Mat("ele_ear_pink", (250, 170, 192), rough=0.6)
    stem = Mat("flower_stem", (60, 160, 70), rough=0.6)
    petal = Mat("flower_petal", (255, 120, 170), rough=0.5)
    center = Mat("flower_center", (255, 214, 60), rough=0.5)

    g.cyl((C, Y + 4, 4), 11.5, 19, can)
    for zz in (6, 19):
        g.cyl((C, Y + 4, zz), 11.8, 1.2, can_d, mode="paint")
    g.cyl((C, Y + 4, 20.5), 9.5, 3, can, mode="carve")
    g.torus((C, Y + 4, 23), 10.4, 1.5, can_d)
    g.torus((C, Y + 9, 23), 8, 1.5, can_d, axis="x", where=lambda X, Y_, Z: Z >= 23)
    for yy in (Y - 2, Y + 10):
        g.seg((C - 6.5, yy, 5), (C - 6.5, yy, 2.6), 3.4, ele, sym=True)
        g.ell((C - 6.5, yy - 0.5, 2.2), (3.8, 3.8, 2.2), ele, sym=True)
    g.sphere((C, Y - 9, 16.5), 8.2, ele)
    g.ell((C - 10.5, Y - 7, 17.5), (6.8, 1.7, 7.8), ele, rot=(0, 0, 28), sym=True)
    g.ell((C - 10.5, Y - 8.6, 17.5), (5.2, 0.9, 6.2), ear_in, rot=(0, 0, 28), mode="paint", sym=True)
    eye(g, C - 3.9, 19, r=2.7, pupil=0.6)
    g.curve([(C, Y - 15, 13.5), (C, Y - 20, 12.5), (C, Y - 24, 15.5), (C, Y - 27, 20.5)],
            [3.3, 2.7, 2.3, 2.1], ele)
    g.cyl((C, Y - 27.3, 20.5), 3.8, 2, SILVER, rot=(31, 0, 0))
    for p, r in (((C, Y - 30, 25), 1.2), ((C - 2.5, Y - 32, 23.5), 1.0), ((C + 2.5, Y - 33, 22.5), 1.1),
                 ((C - 1, Y - 35, 18.5), 1.0), ((C + 3, Y - 36, 15), 0.9), ((C - 3.5, Y - 36, 13), 1.1),
                 ((C + 0.5, Y - 38, 9), 1.0)):
        g.sphere(p, r, WATER)
    blush(g, C - 5.6, 14.5, rx=1.7, rz=1.0, only=[ele])
    smile(g, C - 4.5, 12.6, 1.6, curve=-0.8, only=[ele])
    g.seg((C + 3, Y + 4, 20), (C + 4, Y + 3, 30), 0.8, stem)
    g.ell((C + 1.5, Y + 3.5, 25), (2.5, 0.8, 1.2), stem, rot=(0, -25, 0))
    for k in range(5):
        a = math.radians(k * 72 + 90)
        g.sphere((C + 4 + 2.4 * math.cos(a), Y + 2.5, 31 + 2.4 * math.sin(a)), 1.8, petal)
    g.sphere((C + 4, Y + 1.8, 31), 1.4, center)
    return g
