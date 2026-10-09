"""The 30 original brainrots. Each builder returns a filled Grid.

Front = -y, up = +z, symmetry plane x = CX (72), depth centre y = CY (72).
"""
import math

import numpy as np

from parts import (BLACK, BLUSH, CHROME_DARK, EYE_WHITE, FLAME_O, FLAME_R, FLAME_Y, GLASS, GOLD,
                   GOLD_DARK, MOUTH, ORANGE_BEAK, PUPIL, RUBBER, SHINE, SILVER, SMOKE, TONGUE,
                   TOOTH, WATER, WHITE, WOOD, WOOD_LIGHT, YELLOW_BEAK, bird_foot, blush,
                   coil_along, cone_spikes, dot_eye, eye, glitch_bands, leg, open_mouth, smile,
                   sparkle)
from parts import (EMERALD, LENS_DARK, RUBY, SAPPHIRE, _shape_mask, beret, bow_tie, brows, cap, chef_hat,
                   crown, glow_eyes, goggles, gold_chain, halo, hard_hat, headphones, music_note, mustache,
                   party_hat, peaked_cap, scarf, shades, shower_cap, sneaker, straw_hat, top_hat, visor, zzz)
from vox import (CX, CY, PALETTE, Grid, Mat, _hash3, angular, bands, checker, hue_mats, speckle,
                 stripes)

ROSTER = []


def PAL_IDX(mat, shade=0):
    return PALETTE.get(mat, shade)


def mat_idx_arr(mat, X, Y_, Z):
    idx = mat.indices(X, Y_, Z)
    if np.ndim(idx) == 0:
        return np.full(X.shape, idx, np.uint16)
    return idx.astype(np.uint16)


HASH = _hash3

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
          "Pingouin-génie dont la tête est une ampoule allumée ; lunettes rondes et nœud papillon.")
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
    shades(g, C - 5, 46.2, 4.5, 4.5, Mat("nerd_frame", (30, 30, 36), rough=0.3), lens=None, rim=0.8, thick=0.8)
    bow_tie(g, (C, Y - 8.2, 28.5), 3.0, Mat("bowtie_red", (226, 36, 52), rough=0.4), Mat("bowtie_knot", (180, 20, 40), rough=0.4))
    return g


@brainrot(2, "Gommarello Ranocchio", "Common", "$8/s",
          "Grenouille-gomme bicolore, casquette à l'envers et dent en or.")
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
    cap(g, (C, Y + 3, 20.5), 6.2, Mat("cap_red", (232, 48, 60), rough=0.5),
        brim_mat=Mat("cap_dark", (40, 40, 52), rough=0.5), backwards=True)
    g.decal((C + 1.5, C + 3.5), (8.4, 9.8), lambda A, B: np.ones(A.shape, bool), GOLD, only=[pink, blue])
    return g


@brainrot(3, "Spugnetta Lumachina", "Common", "$12/s",
          "Escargot amoureux (yeux en cœur) dont la coquille est une éponge qui fait des bulles.")
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
    heart = Mat("heart_eye", (255, 40, 110), rough=0.2, emit=0.8)
    for cx in (C - 6.5, C + 6.5):
        g.decal((cx - 3, cx + 3), (39, 45), _shape_mask("heart", cx, 41.8, 2.3, 2.1), heart,
                only=[PUPIL, SHINE, EYE_WHITE])
    g.decal((C - 1.2, C + 1.2), (19.8, 22), lambda A, B: (A - C) ** 2 + (B - 21) ** 2 <= 1.4, TONGUE, only=[mint])
    return g


@brainrot(4, "Pomodorino Granchietto", "Common", "$18/s",
          "Crabe-tomate chef cuisinier : toque, moustache et sourcils froncés.")
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
    chef_hat(g, (C, Y + 2, 25.5), 5.6, 6, WHITE)
    mustache(g, C, 17, 5.2, Mat("mustache", (44, 30, 30), rough=0.6))
    brows(g, C - 5.5, 35.8, 2.4, Mat("crab_brow", (120, 30, 20), rough=0.5), tilt=0.5, ymax=Y - 10)
    return g


@brainrot(5, "Ombrellino Pipistrello", "Common", "$25/s",
          "Chauve-souris vampire en haut-de-forme, yeux rouges lumineux ; ses ailes sont un parapluie.")
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
    glow_eyes(g, C - 3.4, 31.5, 2.7, 1.9, Mat("bat_glow", (255, 40, 50), rough=0.2, emit=3.0), tilt=0.45)
    top_hat(g, (C, Y - 1, 38.3), 3.8, 6.5, Mat("tophat_black", (28, 26, 34), rough=0.35),
            Mat("tophat_band", (150, 50, 220), rough=0.35))
    return g


@brainrot(6, "Candelino Gufetto", "Common", "$35/s",
          "Bébé hibou en cire de bougie qui s'endort sur son bougeoir doré.")
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
    eye(g, C - 4.7, 19, r=3.8, iris=iris, pupil=0.42, lid=0.48, lid_mat=wax)
    g.cyl((C, Y - 10, 15.5), 1.9, 3.8, ORANGE_BEAK, axis="-y", r2=0.5)
    for z in (6.5, 10):
        for xc in (C - 3, C + 3):
            g.decal((xc - 2, xc + 2), (z - 1, z + 1),
                    lambda A, B, xc=xc, z=z: (np.abs(B - (z + np.abs(A - xc) * 0.6)) <= 0.5) & (np.abs(A - xc) <= 2),
                    vmark, only=[wax])
    g.ell((C - 10, Y + 1, 13), (2.3, 5, 8.5), wax, rot=(0, -10, 0), sym=True)
    bird_foot(g, C - 4, Y - 8.5, ORANGE_BEAK, z=3.2, toe=2.6, r=0.9)
    zmat = Mat("zzz_purple", (180, 140, 255), rough=0.3, emit=1.5)
    zzz(g, C + 13, Y - 4, 37, 1.6, zmat)
    zzz(g, C + 17, Y - 5, 43, 1.1, zmat)
    zzz(g, C + 20, Y - 6, 47.5, 0.8, zmat)
    return g


# ============================================================================
# RARE
# ============================================================================
@brainrot(7, "Ventilatore Pavone", "Rare", "$60/s",
          "Paon diva : roue-ventilateur, lunettes œil de chat et collier en or.")
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
    shades(g, C - 2.6, 40.8, 2.3, 1.7, Mat("diva_frame", (255, 255, 255), rough=0.25),
           lens=Mat("diva_lens", (120, 40, 140), rough=0.05), style="cat", rim=0.6, thick=0.7, ymax=Y - 9)
    gold_chain(g, (C, Y - 5.5, 30), 4.2, 4.2, drop=2.2, r=0.7, step=1.3)
    return g


@brainrot(8, "Lavatricino Polpetto", "Rare", "$90/s",
          "Pieuvre en bonnet de douche qui sort du hublot d'une machine à laver.")
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
    shower_cap(g, (C, Y - 10, 26), 8.2, Mat("shower_cap", (150, 205, 255), rough=0.4), WHITE)
    return g


@brainrot(9, "Microondino Riccio", "Rare", "$140/s",
          "Hérisson-micro-ondes debout en baskets, piquants brûlants comme des braises.")
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
    brows(g, C - 3.4, 33.6, 2.2, Mat("hedgehog_brow", (80, 50, 34), rough=0.6), tilt=0.5, ymax=Y - 9)
    g.lift(13)
    for s in (-1, 1):
        g.seg((C + s * 6.5, Y + 2, 17), (C + s * 7, Y + 2, 5), 2.3, skin)
    sneaker(g, C - 7, Y + 6, 0, 10, 3.6, 5.6, Mat("kick_cyan", (40, 200, 235), rough=0.4),
            Mat("kick_orange", (255, 140, 40), rough=0.4))
    return g


@brainrot(10, "Sveglia Coniglietta", "Rare", "$200/s",
          "Lapine-réveil en baskets roses et lunettes étoiles.")
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
    g.ell((C - 14.8, Y - 3, 19), (2.4, 2.7, 3.3), fur, sym=True)
    g.sphere((C, Y + 8, 15), 4.2, fur)
    sneaker(g, C - 6.5, Y + 2, 0, 9.5, 3.4, 5.2, Mat("kick_pink", (255, 110, 170), rough=0.4),
            Mat("kick_white", (255, 255, 255), rough=0.4))
    shades(g, C - 4.3, 25.6, 3.5, 3.5, Mat("star_frame", (255, 214, 40), rough=0.25, metal=0.6),
           lens=Mat("star_lens", (60, 20, 90), rough=0.05), style="star", rim=0.7)
    return g


@brainrot(11, "Pennellone Volpino", "Rare", "$300/s",
          "Renard artiste : béret, écharpe rayée et queue-pinceau trempée dans la peinture.")
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
    beret(g, (C - 1, Y - 2, 39.2), 5.4, Mat("beret_red", (200, 34, 56), rough=0.6))
    scarf(g, (C, Y - 1, 25.5), 8, 7, 1.6, Mat("scarf_teal", (30, 176, 176), rough=0.7), tail_dir=-1, tail_len=8,
          stripe=WHITE)
    g.front_ellipse(C + 5.6, 30, 1.3, 0.8, pb, only=[fw, fox])
    return g


@brainrot(12, "Innaffiatoio Elefantino", "Rare", "$450/s",
          "Bébé éléphant-arrosoir en chapeau de paille ; sa trompe est le bec verseur.")
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
    straw_hat(g, (C, Y - 9, 23.6), 5, Mat("straw", (240, 206, 120), rough=0.8, shades=2, amt=0.06, scale=1),
              Mat("hat_ribbon", (230, 60, 90), rough=0.5), flower=petal)
    return g


# ============================================================================
# EPIC
# ============================================================================
@brainrot(13, "Telefonino Fenicottero", "Epic", "$1.2K/s",
          "Flamant rose diva : corps en téléphone à cadran, cou en fil spiralé, lunettes cœur et perles.")
def telefonino_fenicottero():
    g = Grid()
    pink = Mat("flamingo_pink", (250, 130, 170), rough=0.5, shades=2, amt=0.05)
    phone = Mat("phone_pink", (244, 92, 142), rough=0.16)
    phone_d = Mat("phone_pink_d", (196, 58, 108), rough=0.2)
    dial = Mat("dial_white", (252, 248, 240), rough=0.3)
    cord = Mat("cord_pink", (232, 82, 132), rough=0.35)
    legm = Mat("flamingo_leg", (240, 112, 152), rough=0.5)

    g.seg((C - 3, Y + 1, 27), (C - 3, Y + 1, 2), 1.4, legm)
    g.sphere((C - 3, Y + 1, 14), 1.8, legm)
    bird_foot(g, C - 3, Y + 1, legm, z=0.8, toe=3.8, r=1.0, sym=False)
    g.tube([(C + 3, Y + 1, 27), (C + 5, Y - 2, 19), (C + 1.5, Y + 2, 16)], [1.4, 1.3, 1.1], legm)
    g.sphere((C + 5, Y - 2, 19), 1.8, legm)
    g.rbox((C, Y + 1, 30), (13, 10.5, 4.5), phone, n=5)
    g.rbox((C, Y + 1, 35.5), (10.5, 8.5, 3.5), phone, n=5)
    c = np.array([C, Y - 6.2, 34.0])
    R = np.array([[1, 0, 0], [0, 0.5, 0.866], [0, -0.866, 0.5]]).T
    g.cyl(tuple(c), 6.8, 1.8, dial, rot=(60, 0, 0))
    nrm = R[:, 2]
    u, v = np.array([1.0, 0, 0]), np.array([0, 0.5, 0.866])
    for k in range(10):
        a = math.radians(30 + k * 28)
        p = c + nrm * 1.8 + 4.6 * (math.cos(a) * u + math.sin(a) * v)
        g.sphere(tuple(p), 1.1, phone_d, mode="paint", only=[dial])
    g.sphere(tuple(c + nrm * 1.6), 1.8, phone)
    g.rbox((C, Y + 3, 41.5), (12.5, 2.8, 1.8), phone, n=4)
    g.ell((C - 11.5, Y + 3, 40.5), (3.4, 4, 2.8), phone, sym=True)
    g.box((C - 9, Y + 2, 38), (C - 8, Y + 4, 39.5), phone_d, sym=True)
    coil_along(g, [(C, Y + 4, 41), (C, Y + 7, 47), (C, Y + 4, 53), (C, Y - 1, 57)], 1.6, 11, 0.9, cord)
    g.sphere((C, Y - 2.5, 59), 4.6, pink)
    g.tube([(C, Y - 6.5, 59), (C, Y - 9.5, 57.5), (C, Y - 10.5, 54.5)], [1.9, 1.6, 1.2], WHITE)
    g.tube([(C, Y - 10, 56), (C, Y - 10.6, 54)], [1.6, 1.2], BLACK)
    eye(g, C - 2.6, 60, r=2.0, pupil=0.62)
    g.ell((C - 13.5, Y + 3, 31), (2.2, 6.5, 4.2), pink, rot=(0, -10, 0), sym=True)
    g.ell((C, Y + 12.5, 34), (5, 3, 2.6), pink, rot=(-25, 0, 0))
    shades(g, C - 2.4, 60.2, 2.1, 1.9, Mat("heart_frame", (255, 40, 140), rough=0.2),
           lens=Mat("heart_lens", (110, 10, 60), rough=0.05), style="heart", rim=0.6, thick=0.7, ymax=Y - 4)
    pearl = Mat("pearl", (250, 246, 240), rough=0.15, metal=0.2)
    gold_chain(g, (C, Y - 2.5, 55.2), 4.0, 4.0, drop=0.8, r=0.75, mat=pearl, alt=pearl, step=1.4)
    return g


@brainrot(14, "Jukeboxino Pappagallo", "Epic", "$1.8K/s",
          "Perroquet rockstar sorti d'un juke-box néon : aviateurs dorés et chaîne à note de musique.")
def jukeboxino_pappagallo():
    g = Grid()
    wood = Mat("juke_wood", (150, 74, 46), rough=0.32, shades=2, amt=0.05)
    red = Mat("parrot_red", (232, 40, 44), rough=0.45, shades=2, amt=0.05)
    yellow = Mat("parrot_yellow", (255, 206, 40), rough=0.45)
    blue = Mat("parrot_blue", (40, 110, 232), rough=0.45)
    glass = Mat("juke_glass", (44, 30, 70), rough=0.05)
    rec = Mat("record_black", (18, 18, 24), rough=0.2)
    label = Mat("record_label", (255, 90, 90), rough=0.4)
    panel = Mat("juke_panel", (255, 236, 196), rough=0.4)
    grille = Mat("juke_grille", (214, 176, 110), rough=0.3, metal=0.6)
    beak = Mat("macaw_beak", (240, 232, 214), rough=0.3)
    beak_d = Mat("macaw_beak_d", (40, 36, 40), rough=0.3)
    neon = hue_mats(8, sat=0.9, emit=2.4, prefix="neon")
    toe = Mat("parrot_feet", (120, 120, 130), rough=0.6)

    g.rbox((C, Y + 1, 15), (13.5, 9, 15), wood, n=8)
    g.cyl((C, Y - 8, 30), 13.5, 18, wood, axis="y", where=lambda X, Y_, Z: Z >= 29)
    g.torus((C, Y - 8.6, 30), 11.6, 1.5, angular((C, Y, 30), 16, neon, axis="y"), axis="y",
            where=lambda X, Y_, Z: Z >= 29)
    g.seg((C - 11.6, Y - 8.6, 3), (C - 11.6, Y - 8.6, 30), 1.4, neon[0], sym=False)
    g.seg((C + 11.6, Y - 8.6, 3), (C + 11.6, Y - 8.6, 30), 1.4, neon[4], sym=False)
    g.decal((C - 10, C + 10), (30, 41), lambda A, B: ((A - C) ** 2 + (B - 30) ** 2 <= 90) & (B >= 30), glass)
    for xx in (C - 5, C, C + 5):
        g.decal((xx - 3, xx + 3), (31, 37), lambda A, B, xx=xx: (A - xx) ** 2 + (B - 33.5) ** 2 <= 5.5, rec,
                only=[glass])
        g.decal((xx - 2, xx + 2), (32, 35), lambda A, B, xx=xx: (A - xx) ** 2 + (B - 33.5) ** 2 <= 1.2, label,
                only=[rec])
    g.decal((C - 8, C + 8), (19, 27), lambda A, B: np.ones(A.shape, bool), panel)
    for zz in (20.5, 23, 25.5):
        g.decal((C - 6, C + 6), (zz, zz), lambda A, B: (A - C) % 3 == 0, neon[int(zz) % 8], only=[panel])
    g.decal((C - 9, C + 9), (3, 15), lambda A, B: np.ones(A.shape, bool), stripes("z", 2, [grille, wood]))
    g.sphere((C, Y - 1, 48), 8.6, red)
    g.front_ellipse(C, 49, 6.2, 4.6, WHITE)
    eye(g, C - 3.5, 50, r=2.6, pupil=0.6)
    g.ell((C, Y - 9.5, 46), (3.4, 3.6, 4), beak)
    g.seg((C, Y - 12.2, 46.5), (C, Y - 12.6, 42.5), 1.5, beak, r1=0.7)
    g.ell((C, Y - 8.6, 42.5), (2.6, 2.6, 1.8), beak_d)
    g.ell((C, Y + 1, 57), (2, 4, 4), yellow, rot=(-30, 0, 0))
    g.ell((C, Y + 3.5, 58.5), (1.6, 4, 3.5), blue, rot=(-45, 0, 0))
    g.ell((C - 14.5, Y + 2, 26), (2.8, 7.5, 13), bands("z", [(0, blue), (21, yellow), (31, red)]),
          rot=(0, -12, 0), sym=True)
    g.ell((C, Y + 13, 9), (3, 2, 9.5), blue, rot=(35, 0, 0))
    g.ell((C + 3.5, Y + 12, 10), (2.5, 2, 8), red, rot=(30, 0, 15))
    bird_foot(g, C - 5, Y - 10, toe, z=0.8, toe=2.8, r=1.0)
    for (x, y, z, m) in ((C - 20, Y - 6, 44, neon[5]), (C + 19, Y - 4, 50, neon[2]), (C + 22, Y - 6, 38, neon[7])):
        g.sphere((x, y, z), 1.6, m)
        g.seg((x + 1.4, y, z), (x + 1.4, y, z + 5), 0.5, m)
        g.seg((x + 1.4, y, z + 5), (x + 3.2, y, z + 4), 0.5, m)
    shades(g, C - 3.6, 50.4, 2.9, 2.4, GOLD, style="aviator", rim=0.6, ymax=Y - 6)

    def note(u, v):
        return ((((u + 0.2) ** 2 + (v + 0.35) ** 2) <= 0.12) | ((np.abs(u - 0.12) <= 0.1) & (v >= -0.35) & (v <= 0.55))
                | ((u >= 0.12) & (u <= 0.45) & (np.abs(v - 0.5 + (u - 0.12) * 0.6) <= 0.1)))
    gold_chain(g, (C, Y - 1, 41.5), 8.6, 7.8, drop=6, r=0.9, medallion=GOLD, med_r=3.0, emblem=note,
               emblem_mat=Mat("medal_black", (30, 26, 34), rough=0.3))
    return g


@brainrot(15, "Aspirapolvere Formichiere", "Epic", "$2.5K/s",
          "Fourmilier-aspirateur tuné : lunettes de course, aileron et pots d'échappement enflammés.")
def aspirapolvere_formichiere():
    g = Grid()
    shell = Mat("vac_red", (234, 72, 58), rough=0.18)
    shell_d = Mat("vac_dark", (62, 62, 74), rough=0.4)
    bin_ = Mat("vac_bin", (176, 220, 242), rough=0.05, emit=0.12)
    dust = Mat("vac_dust", (150, 140, 130), rough=0.9)
    fur = Mat("anteater_fur", (146, 124, 106), rough=0.8, shades=3, amt=0.07)
    fur_d = Mat("anteater_dark", (50, 42, 44), rough=0.8)
    fur_w = Mat("anteater_white", (238, 232, 222), rough=0.7)
    hose_a = Mat("hose_a", (120, 124, 136), rough=0.4)
    hose_b = Mat("hose_b", (80, 84, 96), rough=0.4)

    g.seg((C, Y - 6, 13.5), (C, Y + 12, 13.5), 10.5, shell)
    g.seg((C, Y - 2, 18), (C, Y + 8, 18), 6.5, bin_, mode="paint", where=lambda X, Y_, Z: Z >= 21)
    g.seg((C, Y - 1, 18), (C, Y + 7, 18), 5.5, speckle(bin_, dust, 0.35, seed=4), mode="paint",
          where=lambda X, Y_, Z: (Z >= 21) & (Z <= 22.5))
    g.torus((C, Y + 3, 24), 5, 1.3, shell_d, axis="x", where=lambda X, Y_, Z: Z >= 24)
    for yy in (Y - 3, Y + 10):
        g.cyl((C - 12.5, yy, 5.5), 5.2, 2.6, RUBBER, axis="x", sym=True)
        g.cyl((C - 13, yy, 5.5), 2.3, 0.9, SILVER, axis="x", sym=True)

    def stripe(X, Y_, Z):
        return np.abs((Z - 13) + 0.9 * (Y_ - (Y - 4))) <= 2.4
    g.seg((C, Y - 6, 13.5), (C, Y + 12, 13.5), 10.6, fur_d, mode="paint", where=lambda X, Y_, Z: stripe(X, Y_, Z) & (Y_ < Y + 4))
    g.ell((C, Y - 15, 15.5), (6.8, 7.8, 6.8), fur)
    g.sphere((C - 5, Y - 13, 21), 2.1, fur, sym=True)
    eye(g, C - 3.6, 17.5, r=2.3, pupil=0.65)
    g.curve([(C, Y - 21, 14.5), (C, Y - 24, 13.5)], [3.3, 3.0], fur)
    g.curve([(C, Y - 24, 13.5), (C, Y - 29, 10.5), (C, Y - 33, 6.5), (C, Y - 36, 3.2)],
            [2.6, 2.4, 2.3, 2.3], stripes("y", 2, [hose_a, hose_b]))
    g.rbox((C, Y - 38, 1.8), (7, 2.6, 1.8), shell_d, n=4)
    g.box((C - 6, Y - 41, 0), (C + 6, Y - 41, 0), fur_w)
    g.seg((C - 6, Y - 9, 8), (C - 6.5, Y - 11, 2.5), 2.3, fur, sym=True)
    g.ell((C - 6.5, Y - 12.5, 1.6), (2.6, 3.4, 1.6), fur_d, sym=True)
    g.seg((C, Y + 21, 14), (C, Y + 25, 17), 3.5, fur)
    g.ell((C, Y + 29, 21), (3.8, 8.5, 10.5), fur, rot=(-35, 0, 0))
    for (x, y, z) in ((C - 3, Y - 44, 2), (C + 2, Y - 46, 3), (C + 4, Y - 43, 1), (C - 1, Y - 48, 4)):
        g.box((x, y, z), (x + 1, y + 1, z + 1), dust)
    g.curve([(C + 4, Y + 21, 4), (C + 10, Y + 25, 1), (C + 15, Y + 19, 1), (C + 18, Y + 23, 1)], 0.8, BLACK)
    g.box((C + 18, Y + 23, 0), (C + 20, Y + 25, 2), WHITE)
    goggles(g, C - 2.4, 20.6, 1.8, CHROME_DARK, Mat("goggle_lens", (255, 160, 40), rough=0.05, emit=0.8), BLACK,
            head_c=(C, Y - 15, 20.6), head_r=4.9)
    for s in (-1, 1):
        g.seg((C + s * 5, Y + 12, 22.5), (C + s * 5, Y + 15.5, 27), 0.8, shell_d)
        g.cyl((C + s * 6, Y + 19, 6.5), 1.7, 4.5, SILVER, axis="y")
        g.ell((C + s * 6, Y + 25, 6.5), (1.6, 2.6, 1.6), bands("y", [(0, FLAME_Y), (Y + 25.5, FLAME_O)]))
    g.rbox((C, Y + 16, 27.6), (9.5, 2.8, 0.9), shell_d, n=6)
    g.rbox((C, Y + 16, 27.6), (9.6, 2.9, 1.0), shell, n=6, mode="paint", where=lambda X, Y_, Z: np.abs(X - C) > 7)
    g.seg((C, Y - 6, 13.5), (C, Y + 12, 13.5), 10.7, WHITE, mode="paint",
          where=lambda X, Y_, Z: (np.abs(np.abs(X - C) - 2.4) <= 0.8) & (Z > 19))
    return g


@brainrot(16, "Cassettino Camaleonte", "Epic", "$3.6K/s",
          "Caméléon-cassette rétro avec bandeau années 80 ; sa queue est la bande magnétique.")
def cassettino_camaleonte():
    g = Grid()
    shell = Mat("cassette_shell", (38, 36, 48), rough=0.22)
    label = Mat("cassette_label", (255, 238, 204), rough=0.5)
    lo_ = Mat("label_orange", (255, 140, 40), rough=0.4)
    lp = Mat("label_pink", (255, 70, 140), rough=0.4)
    lc = Mat("label_cyan", (40, 200, 232), rough=0.4)
    win = Mat("cassette_window", (90, 84, 104), rough=0.05)
    reel = Mat("reel_white", (242, 242, 246), rough=0.3)
    tape = Mat("tape_brown", (112, 62, 40), rough=0.2)
    c1 = Mat("cham_green", (92, 212, 92), rough=0.45)
    c2 = Mat("cham_lime", (186, 224, 62), rough=0.45)
    c3 = Mat("cham_teal", (40, 192, 172), rough=0.45)
    cham = bands("x", [(0, c3), (C - 6, c1), (C + 6, c2)])
    leaf = Mat("branch_leaf", (60, 170, 70), rough=0.6)

    g.curve([(C - 24, Y - 1, 6), (C - 8, Y - 1, 4), (C + 8, Y - 1, 4.5), (C + 24, Y, 7)], 2.5, WOOD)
    for p in ((C - 25, Y - 2, 9), (C + 25, Y - 1, 10), (C + 20, Y + 1, 4)):
        g.ell(p, (3, 1.2, 2), leaf, rot=(0, 30, 0))
    g.rbox((C, Y, 22), (15.5, 3.6, 9.8), shell, n=10)
    g.decal((C - 13, C + 13), (23, 30.5), lambda A, B: np.ones(A.shape, bool), label)
    g.decal((C - 13, C + 13), (27, 29.5), lambda A, B: np.ones(A.shape, bool), stripes("z", 1, [lo_, lp, lc]),
            only=[label])
    g.decal((C - 8, C + 8), (15, 21), lambda A, B: np.ones(A.shape, bool), win)
    for xx in (C - 5.5, C + 5.5):
        g.decal((xx - 3, xx + 3), (15, 21), lambda A, B, xx=xx: (A - xx) ** 2 + (B - 18) ** 2 <= 8.5, reel,
                only=[win])
        g.decal((xx - 2, xx + 2), (16, 20), lambda A, B, xx=xx: (A - xx) ** 2 + (B - 18) ** 2 <= 1.6, shell,
                only=[reel])
    g.decal((C - 2, C + 2), (16, 20), lambda A, B: np.ones(A.shape, bool), tape, only=[win])
    for xx, zz in ((C - 14, 14), (C + 14, 14), (C - 14, 30), (C + 14, 30)):
        g.decal((xx, xx), (zz, zz), lambda A, B: np.ones(A.shape, bool), SILVER)
    g.ell((C, Y - 1, 37), (7.5, 7, 6.2), cham)
    g.cyl((C, Y + 1, 39.5), 4.4, 8, cham, r2=0.5, ry=3, rot=(-28, 0, 0))
    g.sphere((C - 7, Y - 2, 38.5), 3.6, cham, sym=True)
    g.front_ellipse(C - 7, 38.5, 1.9, 2.0, WHITE, only=[c3, c1, c2])
    g.front_ellipse(C - 7, 38.5, 1.0, 1.1, PUPIL)
    g.decal((Y - 4, Y), (36.5, 40.5), lambda A, B: ((A - (Y - 2)) ** 2 + (B - 38.5) ** 2 <= 3.6), WHITE,
            direction="+x")
    g.decal((Y - 4, Y), (36.5, 40.5), lambda A, B: ((A - (Y - 2)) ** 2 + (B - 38.5) ** 2 <= 1.1), PUPIL,
            direction="+x")
    smile(g, C, 34, 5.2, curve=1.6)
    blush(g, C - 4.5, 35.5, rx=1.4, rz=0.8)
    g.tube([(C - 13, Y - 1, 13), (C - 15, Y - 3, 9), (C - 14, Y - 3, 6.5)], [2, 1.8, 1.6], cham, sym=True)
    g.tube([(C - 15, Y - 1, 28), (C - 19, Y - 4, 25), (C - 20, Y - 6, 21)], [1.9, 1.7, 1.5], cham, sym=True)
    g.tube([(C + 15, Y, 16), (C + 19, Y, 14.5)], [2.4, 2.0], cham)
    pts = []
    for i in range(60):
        t = i / 59
        a = -math.pi / 2 + t * 3.2 * math.pi
        rr = 7 * (1 - t) + 1.2
        pts.append((C + 22 + rr * math.cos(a), Y + 0.5, 18 + rr * math.sin(a) + 3 * (1 - t)))
    g.tube([(C + 19, Y, 14.5)] + pts, 0.9, tape)
    g.torus((C, Y - 1, 42), 5.0, 1.0, stripes("z", 0.9, [Mat("sweat_pink", (255, 60, 150), rough=0.6), WHITE]))
    return g


@brainrot(17, "Frullatore Medusina", "Epic", "$5K/s",
          "Méduse fêtarde (chapeau pointu, yeux étoiles) posée sur un mixeur rempli de smoothie.")
def frullatore_medusina():
    g = Grid()
    base = Mat("blender_base", (60, 64, 82), rough=0.3, metal=0.3)
    jar = Mat("blender_glass", (200, 236, 250), rough=0.03, emit=0.15)
    smoothie = Mat("smoothie", (232, 112, 212), rough=0.2, emit=0.35, shades=2, amt=0.05)
    bell = Mat("jelly_bell", (222, 132, 242), rough=0.08, emit=0.7, shades=2, amt=0.05)
    spot = Mat("jelly_spot", (255, 214, 255), rough=0.1, emit=1.4)
    t1 = Mat("jelly_tentacle", (250, 160, 230), rough=0.2, emit=0.9)
    t2 = Mat("jelly_tentacle2", (170, 124, 255), rough=0.2, emit=0.9)
    bubble = Mat("smoothie_bubble", (255, 230, 250), rough=0.1, emit=0.8)
    btns = hue_mats(3, sat=0.8, emit=2.5, prefix="btn")

    g.rbox((C, Y, 6), (11, 11, 6), base, n=5)
    for i, xx in enumerate((C - 4, C, C + 4)):
        g.front_ellipse(xx, 6, 1.3, 1.3, btns[i])
    g.cyl((C, Y, 12), 8.8, 27, jar, r2=10.8)
    g.cyl((C, Y, 12), 9.3, 16, smoothie, r2=10.2, mode="paint")
    g.torus((C + 12.5, Y, 25), 5, 1.5, jar, axis="y", where=lambda X, Y_, Z: X >= C + 10.5)
    rng = np.random.default_rng(17)
    for _ in range(10):
        a = rng.uniform(math.pi * 1.1, math.pi * 1.9)
        z = rng.uniform(14, 26)
        rr = 9 + (z - 12) / 27 * 2
        g.sphere((C + rr * math.cos(a), Y + rr * math.sin(a), z), 0.9, bubble, mode="paint", only=[smoothie])
    g.ell((C, Y, 38), (13.5, 13.5, 11.5), bell, where=lambda X, Y_, Z: Z >= 37)
    for a in range(0, 360, 30):
        ar = math.radians(a)
        g.sphere((C + 13 * math.cos(ar), Y + 13 * math.sin(ar), 37.6), 1.9, bell)
    for _ in range(14):
        a = rng.uniform(0, 2 * math.pi)
        el = rng.uniform(0.35, 1.3)
        p = (C + 13.2 * math.cos(a) * math.cos(el), Y + 13.2 * math.sin(a) * math.cos(el), 38 + 11.3 * math.sin(el))
        g.sphere(p, rng.uniform(1.0, 1.7), spot, mode="paint", only=[bell])
    eye(g, C - 4.6, 43, r=3.3, pupil=0.6)
    open_mouth(g, C, 40, 2.2, 1.8, teeth=False, only=[bell])
    blush(g, C - 8, 40.5, rx=1.6, rz=0.9, only=[bell])
    for i, a in enumerate(range(15, 360, 36)):
        ar = math.radians(a)
        front = 240 <= a <= 300
        L = 1 if front else 5
        pts = []
        for k in range(L + 1):
            rr = 11.8 + 1.3 * math.sin(k * 1.4 + i)
            z = 37 - k * 5.4
            aa = ar + 0.12 * math.sin(k * 1.1 + i)
            pts.append((C + rr * math.cos(aa), Y + rr * math.sin(aa), z))
        g.tube(pts, list(np.linspace(1.2, 0.6, len(pts))), t1 if i % 2 else t2)
    party_hat(g, (C + 1, Y + 1, 48.6), 4.2, 9, [Mat("party_pink", (255, 70, 170), rough=0.4),
              Mat("party_yellow", (255, 220, 40), rough=0.4), Mat("party_cyan", (40, 210, 240), rough=0.4)],
              Mat("party_pom", (255, 255, 255), rough=0.5, emit=0.6))
    star = Mat("star_eye", (255, 236, 80), rough=0.2, emit=2.5)
    for cx in (C - 4.6, C + 4.6):
        g.decal((cx - 3, cx + 3), (40, 46), _shape_mask("star", cx, 43, 2.2, 2.2), star,
                only=[PUPIL, SHINE, EYE_WHITE])
    return g


@brainrot(18, "Semaforino Giraffino", "Epic", "$7.5K/s",
          "Girafe policière dont le cou est un feu tricolore ; casquette et sifflet.")
def semaforino_giraffino():
    g = Grid()
    gir = Mat("giraffe_yellow", (246, 202, 92), rough=0.6)
    spot = Mat("giraffe_spot", (178, 104, 48), rough=0.65)
    mane = Mat("giraffe_mane", (138, 78, 40), rough=0.7)
    muzzle = Mat("giraffe_muzzle", (252, 228, 164), rough=0.6)
    housing = Mat("tl_housing", (46, 54, 46), rough=0.35)
    visor = Mat("tl_visor", (30, 36, 30), rough=0.4)
    lights = [(57, Mat("tl_red", (255, 50, 50), rough=0.2, emit=3.0)),
              (48, Mat("tl_yellow", (255, 196, 40), rough=0.2, emit=3.0)),
              (39, Mat("tl_green", (40, 240, 110), rough=0.2, emit=3.0))]
    hoof = Mat("hoof", (72, 52, 42), rough=0.6)

    g.ell((C, Y + 6, 28), (9, 13.5, 8.5), gir)
    for yy in (Y - 2, Y + 14):
        g.seg((C - 5.5, yy, 25), (C - 5.5, yy, 3), 2.3, gir, sym=True)
        g.sphere((C - 5.5, yy, 13), 2.7, gir, sym=True)
        g.cyl((C - 5.5, yy, 0), 2.6, 3, hoof, sym=True)
    g.seg((C, Y + 19, 31), (C, Y + 22.5, 20), 0.9, gir)
    g.ell((C, Y + 23, 18.5), (1.6, 1.6, 2.6), mane)
    g.rbox((C, Y - 2, 48), (5, 5, 16.5), housing, n=8)
    for z, m in lights:
        g.sphere((C, Y - 6.6, z), 3.3, m)
        g.cyl((C, Y - 6.8, z), 4.3, 3.2, visor, axis="-y", where=lambda X, Y_, Z, z=z: Z >= z + 0.6)
        g.cyl((C, Y - 7.4, z), 3.5, 3.0, visor, axis="-y", mode="carve", where=lambda X, Y_, Z, z=z: Z >= z + 0.6)
    g.seg((C, Y + 3.4, 34), (C, Y + 3.4, 63), 1.5, mane)
    g.ell((C, Y - 3, 67.5), (5.6, 8.5, 4.6), gir)
    g.ell((C, Y - 9.5, 66.3), (4.4, 3.6, 3.6), muzzle)
    g.front_ellipse(C - 1.6, 66.8, 0.7, 0.7, mane, sym=True)
    smile(g, C, 64.3, 2.2, curve=0.9, only=[muzzle])
    g.ell((C - 6.5, Y - 1, 69.5), (2.8, 1.2, 1.4), gir, rot=(0, 0, -20), sym=True)
    eye(g, C - 3.4, 69.2, r=2.3, pupil=0.62)
    rng = np.random.default_rng(18)
    for _ in range(45):
        p = (C + rng.uniform(-9, 9), Y + 6 + rng.uniform(-13, 13), 28 + rng.uniform(-8, 8))
        g.sphere(p, rng.uniform(1.6, 2.6), spot, mode="paint", only=[gir],
                 where=lambda X, Y_, Z: Z > 20)
    for _ in range(10):
        p = (C + rng.uniform(-5, 5), Y - 3 + rng.uniform(-7, 7), 67.5 + rng.uniform(-3, 4))
        g.sphere(p, rng.uniform(1.0, 1.5), spot, mode="paint", only=[gir])
    peaked_cap(g, (C, Y - 2.5, 71.4), 4.4, Mat("police_navy", (34, 44, 92), rough=0.5),
               Mat("visor_black", (20, 20, 26), rough=0.15), GOLD,
               band_mat=checker(1, [Mat("police_white", (240, 240, 245), rough=0.5), Mat("police_navy2", (34, 44, 92), rough=0.5)]),
               h=3.0)
    g.cyl((C + 2.8, Y - 12.4, 64.6), 0.9, 2.6, SILVER, axis="-y")
    return g


# ============================================================================
# LEGENDARY
# ============================================================================
@brainrot(19, "Mongolfiera Balenotta", "Legendary", "$12K/s",
          "Baleine-montgolfière pilote : lunettes d'aviateur, nacelle en osier et nuages.")
def mongolfiera_balenotta():
    g = Grid()
    ga = Mat("balloon_red", (240, 84, 78), rough=0.5)
    gb = Mat("balloon_cream", (255, 236, 198), rough=0.5)
    gc = Mat("balloon_teal", (40, 182, 198), rough=0.5)
    belly = Mat("whale_belly", (252, 248, 240), rough=0.5)
    groove = Mat("whale_groove", (214, 204, 200), rough=0.5)
    wicker = Mat("wicker", (192, 138, 74), rough=0.85, shades=3, amt=0.1, scale=1)
    rim = Mat("wicker_rim", (130, 84, 44), rough=0.8)
    rope = Mat("rope", (222, 202, 152), rough=0.9)
    sand = Mat("sandbag", (214, 190, 140), rough=0.9)
    cloud = Mat("cloud", (250, 252, 255), rough=0.95, emit=0.1)

    gore = angular((C, Y, 46), 14, [ga, gb, gc, gb], axis="y", phase=0.02)
    g.ell((C, Y + 2, 46), (17.5, 22, 17), gore)
    g.seg((C, Y + 18, 48), (C, Y + 34, 52), 9.5, gore, r1=3)
    g.ell((C - 7.5, Y + 37, 53), (8.5, 4, 1.9), gc, rot=(0, 0, -22), sym=True)
    g.ell((C, Y - 2, 37), (13, 17, 9), stripes("z", 2.5, [belly, groove], widths=[3, 1]), mode="paint",
          where=lambda X, Y_, Z: Z <= 38)
    g.ell((C - 16.5, Y - 4, 38), (8, 4, 2), ga, rot=(0, -30, -20), sym=True)
    eye(g, C - 9, 46, r=3.5, pupil=0.58)
    smile(g, C, 39.5, 9, curve=3.2)
    blush(g, C - 12, 41.5, rx=2.2, rz=1.2)
    g.seg((C, Y - 8, 62), (C, Y - 8, 69), 1.5, WATER)
    for p, r in (((C - 3, Y - 8, 70), 1.7), ((C + 3, Y - 8, 70.5), 1.7), ((C, Y - 8, 72.5), 2.2),
                 ((C - 5, Y - 9, 67), 1.1), ((C + 5, Y - 7, 67.5), 1.1)):
        g.sphere(p, r, WATER)
    g.rbox((C, Y + 2, 6), (6.8, 6.8, 6), wicker, n=6)
    g.rbox((C, Y + 2, 11.5), (7.2, 7.2, 1.2), rim, n=6)
    for sx in (-1, 1):
        for sy in (-1, 1):
            g.seg((C + sx * 6, Y + 2 + sy * 6, 12), (C + sx * 9, Y + 2 + sy * 9, 31), 0.6, rope)
    g.cyl((C, Y + 2, 12), 2.2, 4, CHROME_DARK)
    g.ell((C, Y + 2, 19.5), (2, 2, 3.6), bands("z", [(0, FLAME_Y), (19.5, FLAME_O)]))
    g.seg((C - 7, Y - 2, 11), (C - 8, Y - 3, 7.5), 0.5, rope, sym=True)
    g.sphere((C - 8, Y - 3, 6.5), 1.9, sand, sym=True)
    for p, r in (((C - 13, Y + 6, 3), 4.5), ((C - 18, Y + 3, 3.5), 3.5), ((C - 9, Y - 4, 2.5), 3.2),
                 ((C + 13, Y - 1, 3.5), 4.5), ((C + 18, Y + 3, 3), 3.2), ((C + 9, Y + 10, 3), 3.6),
                 ((C - 2, Y + 12, 2.5), 3.4)):
        g.sphere(p, r, cloud)
    goggles(g, C - 5, 55, 2.6, Mat("goggle_leather", (126, 74, 40), rough=0.7),
            Mat("goggle_glass", (120, 220, 255), rough=0.05, emit=0.8), None)
    return g


@brainrot(20, "Escavatore Mammuttone", "Legendary", "$18K/s",
          "Mammouth chef de chantier sur chenilles : casque orange, trompe en bras de pelleteuse.")
def escavatore_mammuttone():
    g = Grid()
    fur = Mat("mammoth_fur", (130, 84, 52), rough=0.85, shades=3, amt=0.09, scale=1)
    fur_d = Mat("mammoth_fur_d", (92, 56, 34), rough=0.85)
    yel = Mat("cat_yellow", (250, 192, 30), rough=0.35)
    trk = Mat("track", (52, 52, 60), rough=0.7)
    trk_l = Mat("track_light", (92, 92, 100), rough=0.6)
    ivory = Mat("ivory", (250, 240, 214), rough=0.4)
    cabw = Mat("cab_window", (120, 200, 240), rough=0.05, emit=0.3)
    beacon = Mat("beacon", (255, 140, 30), rough=0.3, emit=3.0)
    stone = Mat("bucket_stone", (150, 150, 158), rough=0.9, shades=2, amt=0.1)

    def hazard(X, Y_, Z):
        a = PAL_IDX(yel)
        b = PAL_IDX(BLACK)
        return np.where(((X + Z) // 2) % 2 == 0, a, b).astype(np.uint16)

    g.rbox((C - 12.5, Y + 2, 5), (4.6, 16.5, 5), stripes("y", 2, [trk, trk_l]), n=6, sym=True)
    for yy in (Y - 10, Y - 3, Y + 4, Y + 11):
        g.cyl((C - 17.2, yy, 5), 3, 1.0, SILVER, axis="x", sym=True)
    g.cyl((C, Y + 2, 10), 11, 3, yel)
    g.ell((C, Y + 4, 25), (13.5, 15, 13), fur)
    g.rbox((C, Y + 11, 41), (6.6, 6, 5.5), yel, n=8)
    g.decal((C - 5, C + 5), (39, 44), lambda A, B: np.ones(A.shape, bool), cabw, direction="+z")
    g.decal((C - 5, C + 5), (39, 44.5), lambda A, B: np.ones(A.shape, bool), cabw)
    g.sphere((C, Y + 11, 47.5), 1.6, beacon)
    g.ell((C, Y - 10, 31), (10.5, 8.5, 10.5), fur)
    g.sphere((C, Y - 8, 41), 6, fur)
    g.ell((C - 10.5, Y - 7, 33), (2.2, 4, 5), fur_d, sym=True)
    eye(g, C - 4.4, 33.5, r=2.8, pupil=0.6, lid=0.18, lid_mat=fur)
    g.curve([(C - 5, Y - 16, 25), (C - 8.5, Y - 22, 21), (C - 10, Y - 27, 24), (C - 9, Y - 29, 29)],
            [2.3, 2.0, 1.6, 1.0], ivory, sym=True)
    g.seg((C, Y - 16, 29), (C, Y - 20, 33), 3.8, fur)
    g.seg((C, Y - 19, 32), (C, Y - 27, 47), 2.9, yel)
    g.sphere((C, Y - 27, 47), 3.3, CHROME_DARK)
    g.seg((C, Y - 27, 47), (C, Y - 36, 31), 2.3, yel)
    g.seg((C + 2.8, Y - 19, 28), (C + 2.8, Y - 26, 43), 0.9, SILVER, sym=True)
    g.sphere((C, Y - 36, 31), 2.6, CHROME_DARK)
    g.rbox((C, Y - 37, 25.5), (6.2, 4.2, 4.6), hazard, n=6)
    g.rbox((C, Y - 39.6, 27.2), (5.2, 3.2, 4.2), yel, n=6, mode="carve")
    for xx in np.arange(C - 5, C + 5.1, 2.5):
        g.box((xx, Y - 42, 21), (xx + 1, Y - 41, 22), SILVER)
    for p in ((C - 2, Y - 38, 23.5), (C + 2, Y - 39, 24), (C, Y - 37.5, 25)):
        g.sphere(p, 1.6, stone)
    hard_hat(g, (C, Y - 8, 44.2), 6.6, Mat("hardhat_orange", (255, 140, 24), rough=0.35))
    brows(g, C - 4.4, 36.9, 2.6, fur_d, tilt=0.5, ymax=Y - 14)
    return g


@brainrot(21, "Faro Pellicano", "Legendary", "$26K/s",
          "Pélican capitaine sur son phare rayé, lanterne allumée, poisson dans le bec.")
def faro_pellicano():
    g = Grid()
    red = Mat("lh_red", (226, 52, 52), rough=0.45)
    white = Mat("lh_white", (246, 244, 238), rough=0.45)
    gray = Mat("lh_gray", (70, 76, 92), rough=0.4)
    lamp = Mat("lh_lamp", (255, 238, 150), rough=0.1, emit=3.0)
    rock = Mat("rock", (122, 122, 134), rough=0.9, shades=3, amt=0.1, scale=2)
    pw = Mat("pelican_white", (250, 248, 244), rough=0.6, shades=2, amt=0.03)
    pouch = Mat("pelican_pouch", (255, 150, 92), rough=0.5)
    beak = Mat("pelican_beak", (255, 196, 70), rough=0.4)
    fish = Mat("fish_blue", (60, 140, 240), rough=0.3)
    door = Mat("lh_door", (92, 56, 40), rough=0.6)
    tipm = Mat("pelican_wingtip", (64, 64, 76), rough=0.6)
    win = Mat("lh_window", (60, 140, 200), rough=0.1, emit=0.6)

    for p, r in (((C - 11, Y + 3, 2), 6.5), ((C + 10, Y - 2, 1.5), 5.5), ((C + 2, Y + 11, 2), 6.5),
                 ((C - 5, Y - 9, 1), 4.5), ((C + 12, Y + 9, 1), 4)):
        g.sphere(p, r, rock, where=lambda X, Y_, Z: Z >= 0)
    g.cyl((C, Y, 2), 12.5, 44, stripes("z", 9, [red, white], offset=-2), r2=8.8)
    g.decal((C - 3, C + 3), (3, 11), lambda A, B: (B <= 8) | ((A - C) ** 2 + (B - 8) ** 2 <= 9), door)
    for zz in (19, 31):
        g.decal((C - 1, C + 1), (zz, zz + 2), lambda A, B: np.ones(A.shape, bool), win)
    g.cyl((C, Y, 46), 11.5, 2, gray)
    g.torus((C, Y, 50.5), 10.8, 0.7, gray)
    for a in range(0, 360, 30):
        ar = math.radians(a)
        g.seg((C + 10.8 * math.cos(ar), Y + 10.8 * math.sin(ar), 48), (C + 10.8 * math.cos(ar), Y + 10.8 * math.sin(ar), 50.5), 0.5, gray)
    g.cyl((C, Y, 48), 7, 8, angular((C, Y, 50), 16, [gray, lamp, lamp, lamp]))
    g.cyl((C, Y, 56), 8.4, 6, red, r2=2.5)
    g.sphere((C, Y, 67), 8, pw)
    eye(g, C - 3.6, 69.5, r=2.9, pupil=0.6)
    g.ell((C, Y - 17, 65), (3.2, 12.5, 2.0), beak, rot=(-6, 0, 0))
    g.sphere((C, Y - 29.5, 63.6), 1.7, Mat.of((230, 120, 40)))
    g.ell((C, Y - 15, 61), (3.9, 10, 4.3), pouch, rot=(-6, 0, 0))
    g.ell((C + 4.2, Y - 18, 61.5), (1.2, 3, 2.3), fish)
    g.ell((C + 5.3, Y - 18, 64.5), (1.0, 1.8, 2.0), fish)
    g.ell((C, Y + 7, 71), (2.2, 4, 2.2), pw, rot=(-40, 0, 0))
    g.ell((C - 12, Y + 2, 36), (3.2, 7.5, 12.5), pw, rot=(0, -10, 0), sym=True)
    g.ell((C - 12, Y + 2, 36), (3.5, 7.8, 12.8), tipm, rot=(0, -10, 0), mode="paint",
          where=lambda X, Y_, Z: Z <= 27, sym=True)
    g.ell((C - 5.5, Y - 13, 3.6), (3.4, 4.2, 1.1), pouch, sym=True)
    for p in ((C - 22, Y - 10, 40), (C + 21, Y - 6, 52), (C + 18, Y - 12, 30)):
        sparkle(g, p, 2, lamp)
    peaked_cap(g, (C, Y + 0.5, 73.6), 5.6, WHITE, Mat("visor_black", (20, 20, 26), rough=0.15), GOLD,
               band_mat=Mat("captain_navy", (30, 40, 80), rough=0.5), h=3.2)
    return g


@brainrot(22, "Discopalla Armadillo", "Legendary", "$40K/s",
          "Tatou boule disco : lunettes de star, chaîne en or et micro sur pied.")
def discopalla_armadillo():
    g = Grid()
    mirror = Mat("mirror_tile", (212, 216, 228), rough=0.06, metal=1.0, shades=3, amt=0.2, scale=3, seed=5)
    seam = Mat("mirror_seam", (92, 94, 108), rough=0.4, metal=1.0)
    glints = hue_mats(6, sat=0.7, emit=2.6, prefix="glint")
    skin = Mat("armadillo_skin", (228, 174, 152), rough=0.6)
    skin_d = Mat("armadillo_skin_d", (190, 130, 114), rough=0.6)
    frame = Mat("shades_pink", (255, 60, 172), rough=0.25)
    lens = Mat("shades_lens", (28, 18, 52), rough=0.05)
    nose = Mat("armadillo_nose", (150, 70, 90), rough=0.4)
    star = Mat("disco_star", (255, 250, 230), rough=0.1, emit=3.0)

    def tiles(X, Y_, Z):
        base = mat_idx_arr(mirror, X, Y_, Z)
        u = HASH(X // 3, Y_ // 3, Z // 3, 9)
        out = base.copy()
        for i, m in enumerate(glints):
            sel = (u >= i * 0.012) & (u < (i + 1) * 0.012)
            out[sel] = PAL_IDX(m)
        return out
    g.sphere((C, Y + 3, 29), 20.5, tiles)
    for k in range(-3, 4):
        g.sphere((C, Y + 3, 29), 21, seam, mode="paint",
                 where=lambda X, Y_, Z, k=k: np.abs((Y_ - (Y + 3)) * 0.55 + (Z - 29) - 7 * k) <= 0.55)
    g.ell((C, Y - 15, 16), (6.2, 6.8, 5.8), skin)
    g.cyl((C, Y - 20, 15), 2.7, 4.5, skin, axis="-y", r2=1.6)
    g.sphere((C, Y - 25, 15.6), 1.5, nose)
    g.ell((C - 4.2, Y - 13, 23), (1.9, 1.3, 4.2), skin, rot=(0, -22, 0), sym=True)
    g.ell((C - 4.2, Y - 14, 23), (1.0, 0.8, 3.0), skin_d, rot=(0, -22, 0), mode="paint", sym=True)
    for sx in (C - 3, C + 3):
        y0 = g.front_y(sx, 18)
        g.ell((sx, y0 - 0.6, 18), (2.8, 0.9, 2.3), frame)
        g.front_ellipse(sx, 18, 1.8, 1.4, lens, only=[frame])
    g.box((C - 1, g.front_y(C, 18) - 1, 18), (C + 1, g.front_y(C, 18), 18), frame)
    smile(g, C, 13, 2.2, curve=1.0, only=[skin])
    for yy in (Y - 10, Y + 15):
        g.ell((C - 7.5, yy, 3), (2.7, 3.6, 3), skin_d, sym=True)
    g.curve([(C, Y + 22, 14), (C, Y + 28, 7), (C + 3, Y + 31, 2.5)], [3, 2, 1],
            stripes("y", 2, [skin, skin_d]))
    for k in range(5):
        g.torus((C, Y + 3, 50.5 + k * 2.1), 1.3, 0.55, GOLD, axis="x" if k % 2 else "y")
    g.torus((C, Y + 3, 62), 2.4, 0.7, GOLD, axis="y")
    for p, s in (((C - 25, Y - 8, 40), 2), ((C + 25, Y - 4, 46), 2), ((C - 22, Y - 14, 18), 1),
                 ((C + 20, Y - 16, 22), 1), ((C + 4, Y - 22, 46), 2), ((C - 14, Y - 10, 55), 1)):
        sparkle(g, p, s, star)
    def star_emblem(u, v):
        th = np.arctan2(v, u) - math.pi / 2
        return np.sqrt(u * u + v * v) <= 0.45 + 0.4 * np.cos(5 * th) ** 2 * (np.cos(5 * th) > 0)
    gold_chain(g, (C, Y - 13.5, 11.8), 5.6, 5.6, drop=1.6, r=0.75, medallion=GOLD, med_r=2.2, emblem=star_emblem,
               emblem_mat=frame)
    g.cyl((C + 11, Y - 22, 0), 3, 0.8, CHROME_DARK)
    g.seg((C + 11, Y - 22, 0.5), (C + 11, Y - 22, 15), 0.6, SILVER)
    g.seg((C + 11, Y - 22, 15), (C + 9, Y - 23.5, 17), 0.6, SILVER)
    g.sphere((C + 8.6, Y - 24, 17.8), 1.9, Mat("mic_mesh", (60, 60, 70), rough=0.4, metal=0.6, shades=2, amt=0.2, scale=1))
    return g


@brainrot(23, "Arpa Cignetta", "Legendary", "$60K/s",
          "Cygne couronné dont le cou forme une harpe dorée aux cordes arc-en-ciel lumineuses.")
def arpa_cignetta():
    g = Grid()
    sw = Mat("swan_white", (250, 250, 248), rough=0.55, shades=2, amt=0.03)
    beak = Mat("swan_beak", (255, 122, 40), rough=0.4)
    pond = Mat("pond", (90, 182, 242), rough=0.05, emit=0.2)
    pond_l = Mat("pond_light", (200, 236, 255), rough=0.05, emit=0.35)
    strings = hue_mats(7, sat=0.45, emit=1.8, prefix="string")
    gem = Mat("swan_gem", (80, 200, 255), rough=0.05, emit=2.0)

    g.cyl((C, Y + 2, 0), 23, 1.5, pond)
    for R_ in (19, 13):
        g.torus((C, Y + 2, 1.5), R_, 0.7, pond_l)
    g.ell((C, Y + 4, 11), (11.5, 15.5, 9), sw)
    g.ell((C, Y + 18.5, 16.5), (6, 5, 4.2), sw, rot=(-35, 0, 0))
    g.ell((C - 10.5, Y + 6, 17), (3.2, 12, 7.5), sw, rot=(0, -32, 0), sym=True)
    for k in range(3):
        g.ell((C - 15 - k * 1.2, Y + 12 + k * 2.5, 21 + k * 1.5), (1.5, 3.2, 1.5), sw, rot=(0, -40, 0), sym=True)
    neck = [(C, Y - 8, 15), (C, Y - 11, 28), (C, Y - 10, 40), (C, Y - 8, 50), (C, Y - 10, 57), (C, Y - 14, 59)]
    g.curve(neck, [3.4, 3.0, 2.8, 2.6, 2.5, 2.5], sw)
    g.ell((C, Y - 15.5, 59.5), (3.4, 4.3, 3.4), sw)
    g.cyl((C, Y - 19, 58.5), 1.7, 4.8, beak, axis="-y", r2=0.9)
    g.sphere((C, Y - 19.5, 60.2), 1.1, BLACK)
    eye(g, C - 2.3, 60.6, r=1.8, pupil=0.7, shine=True)
    g.torus((C, Y - 15.5, 63.5), 2.2, 0.6, GOLD)
    for a in range(0, 360, 72):
        ar = math.radians(a)
        g.seg((C + 2.2 * math.cos(ar), Y - 15.5 + 2.2 * math.sin(ar), 63.5),
              (C + 2.4 * math.cos(ar), Y - 15.5 + 2.4 * math.sin(ar), 66), 0.5, GOLD)
    g.sphere((C, Y - 17.6, 64.3), 0.9, gem)
    bar = [(C, Y - 8.5, 50), (C, Y - 1, 53), (C, Y + 8, 47), (C, Y + 15, 35), (C, Y + 18, 22)]
    g.curve(bar, 1.7, GOLD)
    g.torus((C, Y - 1, 55.5), 2.2, 0.8, GOLD, axis="x")
    for k, yy in enumerate(range(Y - 4, Y + 16, 3)):
        zs = g.column_z(C, yy)
        low, high = zs[zs < 24], zs[zs > 25]
        if not len(low) or not len(high):
            continue
        g.seg((C, yy, low[-1] + 1), (C, yy, high[0] - 1), 0.5, strings[k % len(strings)])
    for p in ((C - 20, Y - 6, 30), (C + 18, Y - 10, 44), (C + 22, Y + 4, 24)):
        sparkle(g, p, 1, strings[3])
    for (x, y, z, k) in ((C - 17, Y - 8, 46, 0), (C + 15, Y - 12, 54, 2), (C + 19, Y - 2, 36, 4), (C - 20, Y + 2, 30, 5)):
        music_note(g, x, y, z, 1.4, strings[k])
    return g


# ============================================================================
# MYTHIC
# ============================================================================
@brainrot(24, "Vulcanetto Triceratopo", "Mythic", "$95K/s",
          "Tricératops volcanique : yeux de lave, piques d'obsidienne et éruption sur le dos.")
def vulcanetto_triceratopo():
    g = Grid()
    skin = Mat("trike_green", (76, 152, 118), rough=0.6, shades=3, amt=0.06)
    belly = Mat("trike_belly", (212, 224, 162), rough=0.6)
    frill = Mat("trike_frill", (250, 120, 52), rough=0.5)
    knob = Mat("trike_frill_knob", (255, 214, 82), rough=0.5)
    horn = Mat("trike_horn", (250, 238, 212), rough=0.4)
    beakm = Mat("trike_beak", (60, 92, 80), rough=0.5)
    rock = Mat("volcano_rock", (90, 70, 66), rough=0.9, shades=3, amt=0.12, scale=2)
    lava = Mat("lava", (255, 110, 30), rough=0.5, emit=3.0)
    lava_h = Mat("lava_hot", (255, 214, 84), rough=0.5, emit=4.0)

    g.ell((C, Y + 6, 21), (14.5, 19.5, 13.5), skin)
    g.ell((C, Y + 4, 16), (12, 16, 10), belly, mode="paint", where=lambda X, Y_, Z: Z <= 12)
    for yy in (Y - 4, Y + 16):
        g.seg((C - 9.5, yy, 14), (C - 10, yy, 4), 4.2, skin, sym=True)
        g.ell((C - 10, yy - 1, 2.3), (4.8, 5.4, 2.4), skin, sym=True)
        for dx in (-2.4, 0, 2.4):
            g.front_ellipse(C - 10 + dx, 1.8, 0.8, 0.9, horn, sym=True)
    g.tube([(C, Y + 23, 21), (C, Y + 31, 15), (C + 3, Y + 38, 9), (C + 7, Y + 41, 4)], [7, 5, 3, 1.2], skin)
    g.cyl((C, Y - 8, 28), 15.5, 2.8, frill, axis="y", where=lambda X, Y_, Z: Z >= 19)
    for a in range(0, 181, 18):
        ar = math.radians(a)
        g.sphere((C + 15.5 * math.cos(ar), Y - 6.8, 28 + 15.5 * math.sin(ar)), 2.3, knob)
    g.ell((C, Y - 15, 22), (9.8, 9.5, 9.2), skin)
    g.cyl((C, Y - 23, 18), 3.6, 5, beakm, axis="-y", r2=1.4)
    g.curve([(C - 4.6, Y - 21, 29), (C - 5.6, Y - 26, 33.5), (C - 6.2, Y - 30, 39.5)], [2.3, 1.7, 0.7], horn, sym=True)
    g.cyl((C, Y - 24, 21.5), 1.9, 4.2, horn, r2=0.4, rot=(55, 0, 0))
    smile(g, C - 4.5, 16.5, 1.8, curve=-0.8, only=[skin])
    smile(g, C + 4.5, 16.5, 1.8, curve=-0.8, only=[skin])
    blush(g, C - 7, 21, rx=1.6, rz=0.9, only=[skin])
    g.cyl((C, Y + 9, 30), 13, 21, rock, r2=5.2)
    g.cyl((C, Y + 9, 47), 4.4, 5, rock, mode="carve")
    g.cyl((C, Y + 9, 47), 4.5, 1.6, lava_h)
    for i, a in enumerate((230, 300, 20, 140)):
        ar = math.radians(a)
        pts = []
        for z in np.linspace(50.5, 31 + (i % 3) * 3, 8):
            rr = 13 - (z - 30) * (7.8 / 21) + 0.35
            aa = ar + 0.08 * math.sin(z * 0.7 + i)
            pts.append((C + rr * math.cos(aa), Y + 9 + rr * math.sin(aa), z))
        g.tube(pts, list(np.linspace(1.3, 0.9, len(pts))), lava)
    for p, r in (((C, Y + 9, 55.5), 3.6), ((C + 3, Y + 10, 59.5), 4.2), ((C - 2.5, Y + 8, 63.5), 3.2),
                 ((C + 1, Y + 9, 67.5), 2.4)):
        g.sphere(p, r, SMOKE)
    rng = np.random.default_rng(24)
    for _ in range(9):
        p = (C + rng.uniform(-11, 11), Y + 9 + rng.uniform(-8, 8), rng.uniform(52, 66))
        g.box(p, (p[0] + 1, p[1] + 1, p[2] + 1), lava_h if rng.random() < 0.5 else lava)
    glow_eyes(g, C - 5, 25, 2.6, 1.7, Mat("lava_eye", (255, 150, 30), rough=0.2, emit=3.5), tilt=0.55, ymax=Y - 18)
    obsidian = Mat("obsidian", (34, 28, 44), rough=0.2, shades=2, amt=0.12)
    pts = [(C, Y + 22 + k * 3.2, 33.5 - k * 2.6) for k in range(5)]
    cone_spikes(g, pts, obsidian, r=2.2, length=5, center=(C, Y + 20, 10), tip_mat=lava)
    for d in ("-x", "+x"):
        g.decal((Y - 8, Y + 22), (8, 26), lambda A, B: np.abs((B - 15) - 3.5 * np.sin((A - Y) * 0.45)) <= 0.45, lava,
                direction=d, only=[skin, belly])
    for s in (-1, 1):
        g.seg((C + s * 6.2, Y - 30, 39.5), (C + s * 5.7, Y - 27, 35.5), 0.9, lava_h)
    return g


@brainrot(25, "Disco Volante Axolotto", "Mythic", "$140K/s",
          "Axolotl extraterrestre à visière cyber et antennes, aux commandes d'une soucoupe volante.")
def disco_volante_axolotto():
    g = Grid()
    hull = Mat("ufo_hull", (198, 206, 222), rough=0.2, metal=1.0, shades=2, amt=0.05)
    hull_d = Mat("ufo_hull_d", (110, 118, 142), rough=0.25, metal=1.0)
    dome = Mat("ufo_dome", (150, 230, 255), rough=0.03, emit=0.35)
    beam = Mat("ufo_beam", (120, 255, 196), rough=0.5, emit=1.2)
    beam2 = Mat("ufo_beam2", (200, 255, 232), rough=0.5, emit=1.8)
    axo = Mat("axolotl_pink", (252, 166, 198), rough=0.4, shades=2, amt=0.04)
    axo_l = Mat("axolotl_light", (255, 214, 228), rough=0.4)
    gill = Mat("axolotl_gill", (236, 70, 152), rough=0.4, emit=0.5)
    gill_l = Mat("axolotl_gill_l", (255, 130, 200), rough=0.4, emit=0.8)
    lights = hue_mats(6, sat=0.8, emit=3.0, prefix="ufolight")

    g.cyl((C, Y, 0), 12, 18, stripes("z", 3, [beam, beam2]), r2=6)
    g.ell((C, Y, 22), (24.5, 24.5, 5.6), hull)
    g.torus((C, Y, 19), 14, 1.7, hull_d)
    for k in range(14):
        a = math.radians(k * 360 / 14)
        g.sphere((C + 23.5 * math.cos(a), Y + 23.5 * math.sin(a), 22), 1.8, lights[k % 6])
    g.torus((C, Y, 27), 11.5, 1.4, hull_d)
    g.sphere((C, Y + 2, 27), 12, dome, where=lambda X, Y_, Z: (Z >= 27) & (Y_ >= Y + 4))
    g.sphere((C, Y + 2, 27), 10.8, dome, mode="carve", where=lambda X, Y_, Z: (Z >= 27) & (Y_ >= Y + 4))
    g.ell((C, Y + 2, 31), (8, 8, 6), axo)
    g.ell((C, Y - 2, 39), (11.5, 9, 8.3), axo)
    g.ell((C, Y - 5, 35), (8, 6, 4), axo_l, mode="paint", where=lambda X, Y_, Z: Z <= 35)
    dot_eye(g, C - 6.5, 41.5, r=1.8)
    smile(g, C, 36, 7, curve=2.4)
    blush(g, C - 8, 37.8, rx=1.8, rz=1.0, only=[axo, axo_l])
    for s in (-1, 1):
        for k, (dz, ln, up) in enumerate(((5, 9.5, 7), (1, 11, 2.5), (-3.5, 9, -1.5))):
            base = (C + s * 10.5, Y - 1, 39 + dz)
            tip = (C + s * (10.5 + ln), Y, 39 + dz + up)
            g.seg(base, tip, 1.5, gill, r1=1.0)
            for t in np.linspace(0.25, 1.0, 5):
                p = (base[0] + (tip[0] - base[0]) * t, base[1] - 0.2, base[2] + (tip[2] - base[2]) * t + 1.3)
                g.sphere(p, 1.1, gill_l)
    g.seg((C - 7, Y - 6, 32), (C - 9.5, Y - 11.5, 28.5), 1.7, axo, sym=True)
    for dx in (-1.6, -0.5, 0.6, 1.7):
        g.sphere((C - 9.5 + dx, Y - 12.8, 28), 0.8, axo, sym=True)
    g.ell((C, Y + 12, 33), (1.6, 7, 4), axo, rot=(-10, 0, 0))
    g.ell((C, Y + 12, 33), (0.8, 7.5, 5.2), gill_l, rot=(-10, 0, 0))
    for p in ((C - 28, Y - 6, 40), (C + 27, Y - 2, 46), (C + 22, Y - 14, 12), (C - 20, Y - 12, 8)):
        sparkle(g, p, 2 if p[2] > 20 else 1, lights[1])
    visor(g, C - 10, C + 10, 39.8, 43.6, Mat("cyber_visor", (60, 240, 255), rough=0.1, emit=2.4), thick=1.0)
    for s in (-1, 1):
        g.seg((C + s * 3.5, Y - 1, 46.5), (C + s * 5.5, Y, 53), 0.5, SILVER)
        g.sphere((C + s * 5.5, Y, 53.8), 1.3, lights[2])
    return g


@brainrot(26, "Ghiacciolone Orso Polare", "Mythic", "$200K/s",
          "Ours polaire esquimau, lunettes de glace et écharpe, croqué sur un coin.")
def ghiacciolone_orso_polare():
    g = Grid()
    ice = Mat("ice_white", (242, 248, 255), rough=0.14, shades=2, amt=0.03)
    blue = Mat("ice_blue", (92, 172, 255), rough=0.08, emit=0.25)
    stick = Mat("popsicle_stick", (226, 192, 138), rough=0.75, shades=2, amt=0.05, scale=1)
    nose = Mat("bear_nose", (40, 42, 58), rough=0.2)
    muzzle = Mat("bear_muzzle", (255, 255, 255), rough=0.3)
    frost = Mat("frost", (220, 245, 255), rough=0.1, emit=0.7)

    g.cyl((C, Y, 0), 11, 1, blue)
    g.ell((C + 7, Y - 5, 0.5), (5, 3.5, 0.6), blue)
    g.rbox((C, Y, 14), (3.4, 1.7, 14), stick, n=6)
    g.rbox((C, Y, 44), (14.5, 7.5, 20.5), ice, n=5)
    g.sphere((C - 10.5, Y, 63.5), 5.2, ice, sym=True)
    g.front_ellipse(C - 10.5, 64.5, 2.5, 2.5, blue, sym=True)
    g.rbox((C, Y, 44), (15, 8, 21), blue, n=5, mode="paint", where=lambda X, Y_, Z: Z >= 57)
    g.sphere((C - 10.5, Y, 63.5), 5.6, blue, mode="paint", where=lambda X, Y_, Z: Z >= 64, sym=True)
    for x, zend in ((C - 9, 51), (C - 4, 54), (C + 1, 49), (C + 6, 53), (C + 10, 50)):
        g.decal((x - 2, x + 2), (zend - 2, 58),
                lambda A, B, x=x, zend=zend: ((np.abs(A - x) <= 1.2) & (B >= zend)) | ((A - x) ** 2 + (B - zend) ** 2 <= 2.6),
                blue)
    g.sphere((C + 14.5, Y - 3, 62), 6.8, ice, mode="carve")
    for k in range(4):
        a = math.radians(200 + k * 30)
        g.sphere((C + 14.5 + 6.8 * math.cos(a), Y - 3, 62 + 6.8 * math.sin(a)), 1.4, ice, mode="carve")
    g.ell((C, Y - 7.5, 41.5), (5.2, 2.8, 4.2), muzzle)
    g.ell((C, Y - 10, 43.5), (2.3, 1.2, 1.6), nose)
    dot_eye(g, C - 5.4, 48.5, r=1.9)
    smile(g, C, 39.4, 2.4, curve=1.0, only=[muzzle])
    blush(g, C - 8.5, 43.5, rx=2.0, rz=1.1, only=[ice])
    g.ell((C - 7, Y - 7.5, 28.5), (3.2, 2.4, 2.8), ice, sym=True)
    for x, y, ln in ((C - 10, Y - 6, 6), (C + 7, Y - 6, 8), (C + 12, Y + 5, 5), (C - 4, Y + 6, 7)):
        g.seg((x, y, 24.5), (x, y, 24.5 - ln), 1.3, ice)
        g.sphere((x, y, 24 - ln), 1.6, ice)
    for p, s in (((C - 22, Y - 6, 50), 2), ((C + 22, Y - 10, 40), 2), ((C - 19, Y - 12, 22), 1),
                 ((C + 18, Y + 2, 66), 1), ((C - 6, Y - 14, 66), 1)):
        sparkle(g, p, s, frost)
    shades(g, C - 5.4, 48.8, 3.6, 2.4, Mat("ice_frame", (40, 90, 210), rough=0.2, metal=0.5),
           lens=Mat("ice_lens", (150, 225, 255), rough=0.02, emit=0.5), style="square", rim=0.7)
    scarf_m = stripes("z", 1.4, [Mat("scarf_red", (226, 40, 60), rough=0.7), WHITE])
    g.rbox((C, Y, 34.5), (15.6, 8.6, 1.9), scarf_m, n=6)
    g.curve([(C + 9, Y - 8.5, 33.5), (C + 10.5, Y - 9.5, 29), (C + 11.5, Y - 9, 25)], [1.5, 1.4, 1.3], scarf_m)
    return g


@brainrot(27, "Razzo Gallinaccio", "Mythic", "$300K/s",
          "Poule-fusée au décollage : regard déterminé, écharpe de pilote, poussin au hublot.")
def razzo_gallinaccio():
    g = Grid()
    hen = Mat("hen_white", (250, 250, 246), rough=0.45, shades=2, amt=0.03)
    comb = Mat("hen_comb", (236, 46, 52), rough=0.4)
    fin = Mat("rocket_fin", (250, 96, 60), rough=0.3)
    fin2 = Mat("rocket_fin2", (255, 202, 60), rough=0.3)
    port = Mat("porthole", (130, 210, 250), rough=0.05, emit=0.3)
    chick = Mat("chick_yellow", (255, 220, 60), rough=0.5, emit=0.2)

    for p, r in (((C, Y, 4), 7.5), ((C - 9, Y + 2, 3.5), 6), ((C + 9, Y - 1, 3.5), 6), ((C - 4, Y - 9, 3), 5),
                 ((C + 5, Y + 9, 3.5), 5.5), ((C - 13, Y - 6, 2.5), 4), ((C + 14, Y + 6, 2.5), 4),
                 ((C + 2, Y - 13, 2), 3.5), ((C - 16, Y + 7, 2), 3)):
        g.sphere(p, r, SMOKE, where=lambda X, Y_, Z: Z >= 0)
    g.ell((C, Y, 16), (6.2, 6.2, 9.5), bands("z", [(0, FLAME_R), (11, FLAME_O), (17, FLAME_Y)]))
    g.cyl((C, Y, 26), 4.2, -5, CHROME_DARK, r2=6.4)
    g.seg((C, Y, 35), (C, Y, 55), 11.2, hen)
    g.seg((C, Y, 35), (C, Y, 55), 11.4, comb, mode="paint", where=lambda X, Y_, Z: (Z >= 30) & (Z <= 32))
    g.seg((C, Y, 35), (C, Y, 55), 11.4, comb, mode="paint", where=lambda X, Y_, Z: (Z >= 48) & (Z <= 48.9))
    g.torus((C, Y - 11, 41), 4.2, 1.1, SILVER, axis="y")
    g.cyl((C, Y - 11.6, 41), 3.4, 1.2, port, axis="y")
    g.front_ellipse(C, 40.5, 2.4, 2.4, chick, only=[port])
    g.front_ellipse(C - 1, 41.5, 0.5, 0.5, PUPIL, sym=True, only=[chick])
    g.front_ellipse(C, 40, 0.6, 0.5, ORANGE_BEAK, only=[chick])
    g.sphere((C, Y, 63), 9.4, hen)
    for p, r in (((C, Y - 1, 72.5), 2.7), ((C, Y + 2.5, 73.5), 2.9), ((C, Y + 5.5, 71.5), 2.4)):
        g.sphere(p, r, comb)
    g.cyl((C, Y - 9, 62), 2.5, 4.8, YELLOW_BEAK, axis="-y", r2=0.5)
    g.ell((C, Y - 8.5, 57.5), (1.6, 1.4, 2.7), comb)
    eye(g, C - 4.2, 65, r=3.0, pupil=0.6, look=(0.3, 0.3))
    g.ell((C - 12.5, Y + 1, 30), (3.2, 7.5, 11), bands("z", [(0, fin2), (27, fin)]), rot=(0, 25, 0), sym=True)
    g.ell((C, Y + 12.5, 30), (2, 7, 10), fin, rot=(25, 0, 0))
    g.seg((C - 6, Y - 5, 25), (C - 11, Y - 9, 4), 1.2, ORANGE_BEAK, sym=True)
    bird_foot(g, C - 11, Y - 9, ORANGE_BEAK, z=4, toe=3, r=0.9)
    brows(g, C - 4.2, 68.6, 2.6, Mat("hen_brow", (60, 40, 40), rough=0.6), tilt=0.5)
    scarf(g, (C, Y, 59.5), 10.9, 10.9, 1.4, Mat("pilot_scarf", (226, 46, 52), rough=0.7), tail_dir=1, tail_len=11)
    return g


# ============================================================================
# DIVINE
# ============================================================================
@brainrot(28, "Lampadario Fenicione", "Divine", "$650K/s",
          "Phénix divin aux yeux de lumière, auréole et anneaux de feu, perché sur un lustre de cristal.")
def lampadario_fenicione():
    g = Grid()
    pr = Mat("phoenix_red", (240, 70, 40), rough=0.4, emit=0.5, shades=2, amt=0.06)
    po = Mat("phoenix_orange", (255, 140, 30), rough=0.4, emit=1.1)
    py = Mat("phoenix_yellow", (255, 222, 72), rough=0.4, emit=1.9)
    crystal = Mat("crystal", (204, 242, 255), rough=0.02, emit=0.9)
    candle = Mat("candle_white", (252, 246, 236), rough=0.5)
    iris = Mat("phoenix_iris", (255, 200, 40), rough=0.2, emit=0.6)

    g.cyl((C, Y, 0), 9.5, 2, GOLD)
    g.seg((C, Y, 2), (C, Y, 31), 2, GOLD)
    g.sphere((C, Y, 8), 3.4, GOLD)
    g.sphere((C, Y, 15), 2.8, GOLD_DARK)
    g.torus((C, Y, 21), 16.5, 1.4, GOLD)
    for k in range(8):
        a = math.radians(k * 45 + 22.5)
        ca, sa = math.cos(a), math.sin(a)
        g.curve([(C + 2 * ca, Y + 2 * sa, 14), (C + 9 * ca, Y + 9 * sa, 13), (C + 16.5 * ca, Y + 16.5 * sa, 21)], 1.0, GOLD)
        x, y = C + 16.5 * ca, Y + 16.5 * sa
        g.cyl((x, y, 21.5), 1.5, 4.5, candle)
        g.ell((x, y, 28), (1.2, 1.2, 2), bands("z", [(0, FLAME_Y), (28.5, FLAME_O)]))
    for k in range(16):
        a = math.radians(k * 22.5)
        x, y = C + 16.5 * math.cos(a), Y + 16.5 * math.sin(a)
        g.seg((x, y, 20), (x, y, 16.5), 0.5, GOLD)
        g.ell((x, y, 14.5), (1.2, 1.2, 2.3), crystal)
    g.torus((C, Y, 31), 10.5, 1.2, GOLD)
    for k in range(10):
        a = math.radians(k * 36)
        x, y = C + 10.5 * math.cos(a), Y + 10.5 * math.sin(a)
        g.seg((x, y, 30), (x, y, 27.5), 0.5, GOLD)
        g.ell((x, y, 26), (1, 1, 1.9), crystal)
    g.cyl((C, Y, 31), 7.5, 2, GOLD)
    bird_foot(g, C - 3.5, Y - 2, GOLD, z=33.5, toe=2.6, r=0.9)
    g.ell((C, Y + 1, 44), (8.8, 9, 11.5), pr)
    g.ell((C, Y - 4, 42), (6, 5, 8), po, mode="paint")
    g.sphere((C, Y - 2, 59), 6.3, pr)
    for dx, dy, h in ((0, 0, 10), (-2.6, 2, 7.5), (2.6, 2, 7.5), (0, 4.5, 6.5)):
        g.ell((C + dx, Y - 1 + dy, 64.5 + h * 0.45), (1.7, 1.7, h * 0.62), py, rot=(-22, 0, 0))
    g.tube([(C, Y - 8, 59), (C, Y - 11, 57.5), (C, Y - 11.5, 55.5)], [1.8, 1.2, 0.6], GOLD)
    for s in (-1, 1):
        for k in range(7):
            a = 8 + k * 10
            ar = math.radians(a)
            ln = 13 + k * 2.6
            d = np.array([s * math.cos(ar), 0.12, math.sin(ar)])
            root = np.array([C + s * 7, Y + 2, 49.0])
            cen = root + d * ln / 2
            rot = (0, -a, 0) if s > 0 else (0, 180 + a, 0)
            mat = pr if k < 2 else (po if k < 5 else py)
            g.ell(tuple(cen), (ln / 2, 1.6, 2.8), mat, rot=rot)
            g.ell(tuple(root + d * (ln - 1.5)), (2.2, 1.4, 1.9), py, rot=rot)
    for s, mat in ((-1, po), (0, py), (1, po)):
        g.curve([(C + s * 2, Y + 8, 38), (C + s * 4, Y + 16, 30), (C + s * 9, Y + 22, 20), (C + s * 11, Y + 24, 10)],
                [2.3, 1.9, 1.4, 0.8], mat)
        g.ell((C + s * 11.5, Y + 24.5, 8), (1.4, 1.4, 2.5), py)
    rng = np.random.default_rng(28)
    for _ in range(14):
        p = (C + rng.uniform(-34, 34), Y + rng.uniform(-8, 10), rng.uniform(40, 80))
        g.box(p, (p[0], p[1], p[2]), py if rng.random() < 0.6 else po)
    glow_eyes(g, C - 3, 60.3, 2.2, 1.5, Mat("phoenix_eye", (255, 250, 200), rough=0.2, emit=4.0), tilt=0.4, ymax=Y - 5)
    aura = Mat("phoenix_aura", (255, 190, 60), rough=0.3, emit=2.5)
    g.torus((C, Y + 1, 46), 17, 0.6, aura, rot=(72, 0, 25))
    g.torus((C, Y + 1, 46), 17, 0.6, aura, rot=(72, 0, -35))
    halo(g, (C, Y - 1, 75), 4.5, 0.6, aura)
    return g


@brainrot(29, "Clessidra Serpentona", "Divine", "$900K/s",
          "Serpent émeraude couronné enroulé autour d'un sablier de sable magique lumineux.")
def clessidra_serpentona():
    g = Grid()
    sand = Mat("magic_sand", (255, 182, 52), rough=0.6, emit=1.6, shades=2, amt=0.06, scale=1)
    glass = Mat("hourglass_glass", (150, 216, 244), rough=0.03, emit=0.3)
    pillar = Mat("hourglass_wood", (122, 70, 42), rough=0.4)
    sn = Mat("serpent_green", (34, 170, 106), rough=0.35, shades=2, amt=0.05)
    sn_d = Mat("serpent_green_d", (20, 120, 76), rough=0.35)
    belly = Mat("serpent_belly", (250, 216, 92), rough=0.35)
    gem = Mat("ruby", (255, 30, 84), rough=0.05, emit=2.0)
    iris = Mat("snake_iris", (255, 212, 40), rough=0.2, emit=2.0)

    g.cyl((C, Y, 0), 15.5, 4, GOLD)
    g.cyl((C, Y, 74), 15.5, 4, GOLD)
    g.torus((C, Y, 4), 14.5, 1.1, GOLD_DARK)
    g.torus((C, Y, 74), 14.5, 1.1, GOLD_DARK)
    for a in (45, 135, 225, 315):
        ar = math.radians(a)
        x, y = C + 12.8 * math.cos(ar), Y + 12.8 * math.sin(ar)
        g.seg((x, y, 4), (x, y, 74), 1.7, pillar)
        g.sphere((x, y, 39), 2.6, GOLD)

    def hourglass(X, Y_, Z):
        d = np.sqrt((X - C) ** 2 + (Y_ - Y) ** 2)
        pile = Z <= 15 + np.maximum(0, 5 - d * 0.5)
        top = (Z >= 41) & (Z <= 50)
        stream = (d <= 1.0) & (Z > 15) & (Z < 41)
        sel = pile | top | stream
        return np.where(sel, PAL_IDX(sand), PAL_IDX(glass)).astype(np.uint16)
    g.ell((C, Y, 21), (10.8, 10.8, 17.5), hourglass, where=lambda X, Y_, Z: Z >= 4)
    g.ell((C, Y, 57), (10.8, 10.8, 17.5), hourglass, where=lambda X, Y_, Z: Z <= 74)
    g.seg((C, Y, 31), (C, Y, 47), 2.4, hourglass)
    turns = 2.25
    phase = -math.pi / 2 - 2 * math.pi * turns
    pts = g.helix((C, Y), 14.2, 9, 66, turns, 3.3, stripes("z", 3, [sn, sn_d], widths=[2, 1]), phase=phase)
    start = np.array(pts[0])
    g.seg(tuple(start), (start[0] + 3, start[1] - 2, 4.5), 3.3, sn, r1=1.0)
    g.seg(pts[-1], (C, Y - 15.5, 77), 3.3, sn)
    g.ell((C, Y - 17.5, 81.5), (5.6, 7.6, 4.4), sn)
    g.ell((C, Y - 18, 79), (3.8, 6, 2), belly, mode="paint", where=lambda X, Y_, Z: Z <= 79.5)
    eye(g, C - 3.3, 83, r=2.5, iris=iris, pupil=0.45, slit=True)
    g.seg((C, Y - 24.5, 79.5), (C, Y - 28.5, 79), 0.6, TONGUE)
    g.seg((C, Y - 28.5, 79), (C - 1.2, Y - 30, 78.5), 0.5, TONGUE)
    g.seg((C, Y - 28.5, 79), (C + 1.2, Y - 30, 78.5), 0.5, TONGUE)
    g.torus((C, Y - 16, 86), 3.2, 0.7, GOLD)
    for a in range(0, 360, 60):
        ar = math.radians(a)
        g.seg((C + 3.2 * math.cos(ar), Y - 16 + 3.2 * math.sin(ar), 86),
              (C + 3.4 * math.cos(ar), Y - 16 + 3.4 * math.sin(ar), 89.5), 0.6, GOLD)
    g.sphere((C, Y - 22.5, 84.5), 1.3, gem)
    rng = np.random.default_rng(29)
    for _ in range(16):
        p = (C + rng.uniform(-22, 22), Y + rng.uniform(-18, 10), rng.uniform(8, 80))
        if abs(p[0] - C) > 16 or p[1] < Y - 16:
            g.box(p, p, sand)
    gold_chain(g, (C, Y - 15.6, 76.5), 3.8, 3.8, drop=1.2, r=0.75, medallion=GOLD, med_r=1.8,
               emblem=lambda u, v: u * u + v * v <= 0.4, emblem_mat=EMERALD)
    return g


# ============================================================================
# SECRET
# ============================================================================
@brainrot(30, "Glitchino Gattivisore", "Secret", "$2.5M/s",
          "Chat-télé glitché : écran pixel, chaîne en or, couronne de pixels et corps qui buggue.")
def glitchino_gattivisore():
    g = Grid()
    fur = Mat("cat_black", (42, 40, 56), rough=0.6, shades=2, amt=0.08)
    fur_w = Mat("cat_white", (240, 240, 250), rough=0.6)
    ear_in = Mat("cat_ear_in", (255, 120, 190), rough=0.5)
    tv = Mat("crt_case", (96, 72, 146), rough=0.3)
    tv_d = Mat("crt_case_d", (62, 46, 100), rough=0.3)
    bezel = Mat("crt_bezel", (28, 24, 40), rough=0.3)
    scr_a = Mat("screen_dark", (14, 34, 44), rough=0.1, emit=0.8)
    scr_b = Mat("screen_noise", (70, 130, 150), rough=0.1, emit=1.0)
    face = Mat("screen_face", (200, 255, 248), rough=0.1, emit=4.0)
    cheek = Mat("screen_cheek", (255, 90, 190), rough=0.1, emit=3.0)
    mag = Mat("glitch_magenta", (255, 40, 200), rough=0.2, emit=2.5)
    cya = Mat("glitch_cyan", (40, 240, 255), rough=0.2, emit=2.5)
    yel = Mat("glitch_yellow", (255, 240, 60), rough=0.2, emit=2.5)
    static = speckle(scr_a, scr_b, 0.14, seed=30)

    g.ell((C, Y + 6, 22), (14.5, 15, 20.5), fur)
    g.ell((C, Y - 4, 24), (8, 6, 12.5), fur_w, mode="paint")
    g.ell((C - 11.5, Y + 10, 10), (5.2, 10, 9), fur, sym=True)
    g.seg((C - 5.5, Y - 5, 20), (C - 5.5, Y - 7, 3), 3.5, fur, sym=True)
    g.ell((C - 5.5, Y - 9, 2.2), (3.5, 4.2, 2.2), fur_w, sym=True)
    g.curve([(C + 8, Y + 19, 6), (C + 16, Y + 15, 3), (C + 22, Y + 5, 4), (C + 23, Y - 4, 10),
             (C + 21, Y - 8, 18), (C + 23, Y - 6, 27)], [3, 2.8, 2.6, 2.4, 2.2, 2.0], fur)
    for k, p in enumerate(((C + 24, Y - 6, 30), (C + 26, Y - 5, 33), (C + 24, Y - 7, 35))):
        g.box(p, (p[0] + 1, p[1] + 1, p[2] + 1), (mag, cya, fur)[k])
    g.rbox((C, Y + 2, 57), (18, 14, 14.5), tv, n=6)
    g.rbox((C, Y + 16, 57), (11.5, 7, 10), tv_d, n=4)
    g.decal((C - 16, C + 10), (45, 69), lambda A, B: np.ones(A.shape, bool), bezel)
    g.ell((C - 3, Y - 12, 57), (12.5, 1.8, 10), static)
    sx = C - 3
    for ex in (sx - 5, sx + 5):
        g.decal((ex - 3, ex + 3), (57, 64),
                lambda A, B, ex=ex: ((A - ex) / 1.9) ** 2 + ((B - 60.5) / 3.0) ** 2 <= 1.0, face,
                only=[scr_a, scr_b])
        g.decal((ex - 1, ex + 1), (61, 63), lambda A, B, ex=ex: (A <= ex) & (B >= 61.5), scr_a, only=[face])
    for mx_ in (sx - 1.8, sx + 1.8):
        g.decal((mx_ - 3, mx_ + 3), (51, 55),
                lambda A, B, mx_=mx_: (np.abs(B - (52.3 + 0.8 * (A - mx_) ** 2)) <= 0.75) & (np.abs(A - mx_) <= 1.9),
                face, only=[scr_a, scr_b])
    for cx_ in (sx - 9, sx + 9):
        g.decal((cx_ - 2, cx_ + 2), (55, 56), lambda A, B: np.ones(A.shape, bool), cheek, only=[scr_a, scr_b])
    for zz, m in ((62, GOLD), (54, SILVER)):
        g.cyl((C + 13.5, Y - 12.5, zz), 2.3, 1.6, m, axis="-y")
    g.cyl((C - 11.5, Y + 2, 70), 5.2, 10, fur, r2=0.5, ry=3.2, rot=(0, -15, 0), sym=True)
    g.cyl((C - 11.5, Y + 0.4, 70.5), 3.0, 7, ear_in, r2=0.3, ry=1.2, rot=(0, -15, 0), mode="paint", sym=True)
    g.sphere((C, Y + 4, 71), 3, tv_d)
    g.seg((C + 1.5, Y + 4, 72), (C + 10, Y + 7, 86), 0.7, SILVER)
    g.seg((C - 1.5, Y + 4, 72), (C - 8, Y + 8, 87), 0.7, SILVER)
    g.sphere((C + 10, Y + 7, 86.5), 1.4, SILVER)
    g.sphere((C - 8, Y + 8, 87.5), 1.4, SILVER)
    g.curve([(C, Y + 22, 50), (C + 4, Y + 27, 30), (C + 8, Y + 27, 4), (C + 14, Y + 22, 1)], 0.9, BLACK)
    g.box((C + 14, Y + 20, 0), (C + 16, Y + 22, 2), WHITE)
    glitch_bands(g, [(12, 13, -2), (30, 32, 3), (49, 50, -3), (66, 67, 2)], cya, mag)
    rng = np.random.default_rng(30)
    for _ in range(26):
        p = (C + rng.uniform(-30, 30), Y + rng.uniform(-20, 10), rng.uniform(5, 85))
        if abs(p[0] - C) < 20 and p[1] > Y - 14:
            continue
        s = rng.integers(0, 2)
        g.box(p, (p[0] + s, p[1] + s, p[2] + s), (mag, cya, yel)[rng.integers(0, 3)])
    gold_chain(g, (C, Y + 6, 40.5), 8.5, 8.5, drop=3.5, r=1.0, medallion=GOLD, med_r=3.2,
               emblem=lambda u, v: np.abs(u) + np.abs(v) <= 0.7, emblem_mat=cya)
    for k in range(20):
        a = 2 * math.pi * k / 20
        p = (C + 11 * math.cos(a), Y + 3 + 11 * math.sin(a), 92 + (k % 3) * 0.6)
        g.box(p, (p[0] + 1, p[1] + 1, p[2] + 1), (mag, cya, yel)[k % 3])
    return g
