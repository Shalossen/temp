"""Voxel -> mesh (greedy meshing), palette textures and MagicaVoxel export."""
import math
import struct

import numpy as np
from PIL import Image

EMIT_MAX = 4.0   # emissive texture is scaled by emit / EMIT_MAX


def crop(v):
    nz = np.nonzero(v)
    lo = [int(a.min()) for a in nz]
    hi = [int(a.max()) + 1 for a in nz]
    return v[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]].copy(), lo


def _greedy2d(mask):
    """Merge equal non-zero cells of a 2D array into rectangles."""
    A, B = mask.shape
    done = np.zeros_like(mask, dtype=bool)
    rects = []
    for i in range(A):
        row = mask[i]
        if not row.any():
            continue
        j = 0
        while j < B:
            val = row[j]
            if val == 0 or done[i, j]:
                j += 1
                continue
            w = 1
            while j + w < B and row[j + w] == val and not done[i, j + w]:
                w += 1
            h = 1
            while i + h < A:
                seg = mask[i + h, j:j + w]
                if np.all(seg == val) and not done[i + h, j:j + w].any():
                    h += 1
                else:
                    break
            done[i:i + h, j:j + w] = True
            rects.append((i, j, h, w, int(val)))
            j += w
    return rects


def greedy_mesh(v):
    """Returns (verts Nx3 float, quads Mx4 int, quad_pal M int) in voxel units
    (voxel (i,j,k) spans [i,i+1]x[j,j+1]x[k,k+1])."""
    pad = np.pad(v, 1)
    verts = {}
    vlist = []
    quads = []
    pals = []

    def vid(p):
        key = (int(p[0]), int(p[1]), int(p[2]))
        if key not in verts:
            verts[key] = len(vlist)
            vlist.append(key)
        return verts[key]

    for d in range(3):
        a_ax, b_ax = [ax for ax in range(3) if ax != d]
        natural = {0: 1, 1: -1, 2: 1}[d]   # sign of e_a x e_b along d
        for sign in (-1, 1):
            for k in range(v.shape[d]):
                cur = np.take(pad, k + 1, axis=d)
                nb = np.take(pad, k + 1 + sign, axis=d)
                m = np.where((cur > 0) & (nb == 0), cur, 0)[1:-1, 1:-1]
                if not m.any():
                    continue
                plane = k + (1 if sign > 0 else 0)
                for (i, j, h, w, val) in _greedy2d(m):
                    corners = [(i, j), (i + h, j), (i + h, j + w), (i, j + w)]
                    if natural != sign:
                        corners = corners[::-1]
                    q = []
                    for (a, b) in corners:
                        p = [0, 0, 0]
                        p[d] = plane
                        p[a_ax] = a
                        p[b_ax] = b
                        q.append(vid(p))
                    quads.append(q)
                    pals.append(val)
    return np.array(vlist, float), np.array(quads, int), np.array(pals, int)


# ---- palette textures ------------------------------------------------------
def palette_size(n_entries):
    side = 1
    while side * side < n_entries:
        side *= 2
    return max(side, 8)


def palette_uv(idx, side):
    px, py = idx % side, idx // side
    return ((px + 0.5) / side, 1.0 - (py + 0.5) / side)


def write_palette_textures(entries, side, out_dir, suffix="", transform=None):
    """entries: list (index 0 = None) of (rgb, rough, metal, emit)."""
    base = Image.new("RGB", (side, side), (255, 0, 255))
    orm = Image.new("RGB", (side, side), (255, 200, 0))
    emi = Image.new("RGB", (side, side), (0, 0, 0))
    for i, e in enumerate(entries):
        if e is None:
            continue
        rgb, rough, metal, emit = transform(e) if transform else e
        p = (i % side, i // side)
        base.putpixel(p, tuple(int(c) for c in rgb))
        orm.putpixel(p, (255, int(round(rough * 255)), int(round(metal * 255))))
        k = min(1.0, emit / EMIT_MAX)
        emi.putpixel(p, tuple(int(round(c * k)) for c in rgb))
    paths = {}
    for name, img in (("BaseColor", base), ("ORM", orm), ("Emissive", emi)):
        path = "%s/T_Brainrot_%s%s.png" % (out_dir, name, suffix)
        img.save(path)
        paths[name] = path
    return paths


# ---- MagicaVoxel -----------------------------------------------------------
def _chunk(cid, content, children=b""):
    return cid + struct.pack("<ii", len(content), len(children)) + content + children


def _dict(d):
    out = struct.pack("<i", len(d))
    for k, v in d.items():
        kb, vb = k.encode(), v.encode()
        out += struct.pack("<i", len(kb)) + kb + struct.pack("<i", len(vb)) + vb
    return out


def write_vox(path, v, entries):
    """v: cropped uint16 array of global palette indices."""
    sx, sy, sz = v.shape
    assert max(v.shape) <= 256, "vox dims > 256"
    used = sorted(int(u) for u in np.unique(v) if u)
    assert len(used) <= 255, "more than 255 colours"
    local = {g: i + 1 for i, g in enumerate(used)}
    xs, ys, zs = np.nonzero(v)
    data = bytearray()
    for x, y, z in zip(xs, ys, zs):
        # MagicaVoxel views from -y, so its y grows away from the viewer like ours
        data += struct.pack("<BBBB", x, y, z, local[int(v[x, y, z])])
    size = _chunk(b"SIZE", struct.pack("<iii", sx, sy, sz))
    xyzi = _chunk(b"XYZI", struct.pack("<i", len(xs)) + bytes(data))
    rgba = bytearray()
    for i in range(256):
        if i < len(used):
            rgb = entries[used[i]][0]
            rgba += struct.pack("<BBBB", rgb[0], rgb[1], rgb[2], 255)
        else:
            rgba += struct.pack("<BBBB", 0, 0, 0, 255)
    rgba_c = _chunk(b"RGBA", bytes(rgba))
    matl = b""
    for g, li in local.items():
        rgb, rough, metal, emit = entries[g]
        if emit >= 0.5:
            props = {"_type": "_emit", "_emit": "%.3f" % min(1.0, emit / EMIT_MAX), "_flux": "1"}
        elif metal > 0.5:
            props = {"_type": "_metal", "_metal": "%.2f" % metal, "_rough": "%.2f" % rough}
        else:
            continue
        matl += _chunk(b"MATL", struct.pack("<i", li) + _dict(props))
    children = size + xyzi + rgba_c + matl
    with open(path, "wb") as f:
        f.write(b"VOX " + struct.pack("<i", 150))
        f.write(_chunk(b"MAIN", b"", children))


# ---- mutations -------------------------------------------------------------
def _lum(rgb):
    r, g, b = (c / 255.0 for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _lerp(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


def mut_gold(e):
    rgb, rough, metal, emit = e
    t = min(1.0, _lum(rgb) ** 0.75 * 1.15)
    return (_lerp((92, 52, 8), (255, 222, 110), t), 0.22, 1.0, emit * 0.5)


def mut_diamond(e):
    rgb, rough, metal, emit = e
    t = min(1.0, _lum(rgb) ** 0.7 * 1.1)
    return (_lerp((70, 150, 215), (238, 252, 255), t), 0.04, 0.0, max(emit, 0.35))


def mut_void(e):
    rgb, rough, metal, emit = e
    l = _lum(rgb)
    col = _lerp((10, 4, 26), (128, 64, 220), min(1.0, l ** 1.6 * 1.3))
    return (col, 0.35, 0.0, 2.5 if l > 0.72 or emit > 0.5 else 0.0)


def mut_lava(e):
    rgb, rough, metal, emit = e
    l = _lum(rgb)
    if l > 0.55 or emit > 0.5:
        return (_lerp((255, 90, 20), (255, 210, 80), min(1.0, (l - 0.55) * 2.5)), 0.5, 0.0, 3.5)
    return (_lerp((28, 20, 22), (92, 60, 52), l / 0.55), 0.85, 0.0, 0.0)


def mut_neon(e):
    import colorsys
    rgb, rough, metal, emit = e
    h, l, s = colorsys.rgb_to_hls(*(c / 255.0 for c in rgb))
    r, g, b = colorsys.hls_to_rgb(h, 0.55, min(1.0, s * 1.6 + 0.35))
    return ((r * 255, g * 255, b * 255), 0.3, 0.0, max(emit, 1.2))


def mut_candy(e):
    import colorsys
    rgb, rough, metal, emit = e
    h, l, s = colorsys.rgb_to_hls(*(c / 255.0 for c in rgb))
    r, g, b = colorsys.hls_to_rgb((h + 0.08) % 1.0, 0.72 + 0.2 * l, 0.75)
    return ((r * 255, g * 255, b * 255), 0.25, 0.0, emit)


def mut_noir(e):
    rgb, rough, metal, emit = e
    l = _lum(rgb)
    v = 255 * (0.03 if l < 0.42 else 0.97)
    return ((v, v, v), rough, 0.0, emit if l >= 0.42 else 0.0)


MUTATIONS = {
    "Gold": mut_gold,
    "Diamond": mut_diamond,
    "Void": mut_void,
    "Lava": mut_lava,
    "Neon": mut_neon,
    "Candy": mut_candy,
    "BlackWhite": mut_noir,
}
