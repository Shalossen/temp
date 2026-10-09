"""Small voxel modelling engine used to build the brainrot roster.

Coordinates: grid[x, y, z], z is up, the character's front faces -y.
Cell (i, j, k) has its centre at integer coordinates (i, j, k).
The symmetry plane is x = CX.
"""
import colorsys
import math

import numpy as np

N = 144          # grid size on every axis
CX = 72          # symmetry plane (x)
CY = 72          # default depth centre (y)


# --------------------------------------------------------------------------
# Materials and palette
# --------------------------------------------------------------------------

class Palette:
    """Global palette shared by every model (index 0 = empty)."""

    def __init__(self):
        self.entries = [None]   # (rgb, rough, metal, emit)
        self.keys = {}
        self.by_mat = {}

    def get(self, mat, shade=0):
        key = (mat.name, shade)
        if key not in self.keys:
            rgb = _shade(mat.rgb, shade * mat.amt)
            self.keys[key] = len(self.entries)
            self.entries.append((rgb, mat.rough, mat.metal, mat.emit))
            self.by_mat.setdefault(mat.name, []).append(self.keys[key])
        return self.keys[key]

    def indices_of(self, mats):
        out = []
        for m in mats:
            for s in m.shade_values():
                out.append(self.get(m, s))
        return out


PALETTE = Palette()


def _shade(rgb, f):
    if f == 0:
        return tuple(int(c) for c in rgb)
    h, l, s = colorsys.rgb_to_hls(*(c / 255 for c in rgb))
    l = min(1.0, max(0.0, l * (1 + f)))
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)))


def _hash3(X, Y, Z, seed=0):
    h = (X.astype(np.int64) * 73856093) ^ (Y.astype(np.int64) * 19349663) \
        ^ (Z.astype(np.int64) * 83492791) ^ (seed * 2654435761)
    h = h & 0xFFFFFFFF
    h = ((h ^ (h >> 16)) * 0x45d9f3b) & 0xFFFFFFFF
    h = ((h ^ (h >> 16)) * 0x45d9f3b) & 0xFFFFFFFF
    h = h ^ (h >> 16)
    return (h & 0xFFFF) / 65535.0


class Mat:
    _registry = {}

    def __init__(self, name, rgb, rough=0.6, metal=0.0, emit=0.0,
                 shades=1, amt=0.07, scale=2, seed=0):
        self.name = name
        self.rgb = tuple(rgb)
        self.rough = rough
        self.metal = metal
        self.emit = emit
        self.shades = shades
        self.amt = amt
        self.scale = scale
        self.seed = seed
        Mat._registry[name] = self

    @staticmethod
    def of(rgb, **kw):
        name = "c_%02x%02x%02x" % tuple(rgb)
        for k in sorted(kw):
            name += "_%s%s" % (k[0], kw[k])
        if name in Mat._registry:
            return Mat._registry[name]
        return Mat(name, rgb, **kw)

    def shade_values(self):
        if self.shades == 1:
            return [0]
        if self.shades == 2:
            return [0, -1]
        return [-1, 0, 1]

    def indices(self, X, Y, Z):
        if self.shades == 1:
            return PALETTE.get(self, 0)
        u = _hash3(X // self.scale, Y // self.scale, Z // self.scale, self.seed)
        vals = self.shade_values()
        if self.shades == 2:
            pick = np.where(u < 0.65, 0, 1)
        else:
            pick = np.where(u < 0.25, 0, np.where(u < 0.78, 1, 2))
        lut = np.array([PALETTE.get(self, s) for s in vals], np.uint16)
        return lut[pick]


def mat_indices(mat, X, Y, Z):
    if isinstance(mat, Mat):
        return mat.indices(X, Y, Z)
    return mat(X, Y, Z)


# --------------------------------------------------------------------------
# Patterns (callables returning palette indices)
# --------------------------------------------------------------------------

def _broadcast(idx, X):
    if np.isscalar(idx) or np.ndim(idx) == 0:
        return np.full(X.shape, idx, np.uint16)
    return idx


def stripes(axis, period, mats, offset=0.0, widths=None):
    """Bands along an axis ('x', 'y', 'z')."""
    ax = "xyz".index(axis)
    widths = widths or [1] * len(mats)
    total = float(sum(widths))
    edges = np.cumsum(widths) / total

    def f(X, Y, Z):
        c = (X, Y, Z)[ax]
        t = ((c + offset) / period) % 1.0
        k = np.searchsorted(edges, t, side="right")
        k = np.clip(k, 0, len(mats) - 1)
        out = np.zeros(X.shape, np.uint16)
        for i, m in enumerate(mats):
            sel = k == i
            if sel.any():
                out[sel] = _broadcast(mat_indices(m, X, Y, Z), X)[sel]
        return out
    return f


def bands(axis, stops):
    """Step gradient: stops = [(start_coord, mat), ...] sorted by coord."""
    ax = "xyz".index(axis)

    def f(X, Y, Z):
        c = (X, Y, Z)[ax]
        out = _broadcast(mat_indices(stops[0][1], X, Y, Z), X).copy()
        for start, m in stops[1:]:
            sel = c >= start
            if sel.any():
                out[sel] = _broadcast(mat_indices(m, X, Y, Z), X)[sel]
        return out
    return f


def angular(center, n, mats, axis="z", phase=0.0):
    """Pie slices around an axis through `center`."""
    def f(X, Y, Z):
        dx, dy, dz = X - center[0], Y - center[1], Z - center[2]
        if axis == "z":
            a = np.arctan2(dy, dx)
        elif axis == "y":
            a = np.arctan2(dz, dx)
        else:
            a = np.arctan2(dz, dy)
        k = np.floor(((a / (2 * math.pi)) + phase) * n).astype(int) % len(mats)
        out = np.zeros(X.shape, np.uint16)
        for i, m in enumerate(mats):
            sel = k == i
            if sel.any():
                out[sel] = _broadcast(mat_indices(m, X, Y, Z), X)[sel]
        return out
    return f


def checker(size, mats, offset=(0, 0, 0)):
    def f(X, Y, Z):
        k = ((X + offset[0]) // size + (Y + offset[1]) // size + (Z + offset[2]) // size) % len(mats)
        out = np.zeros(X.shape, np.uint16)
        for i, m in enumerate(mats):
            sel = k == i
            if sel.any():
                out[sel] = _broadcast(mat_indices(m, X, Y, Z), X)[sel]
        return out
    return f


def speckle(base, other, prob, seed=1, scale=1):
    def f(X, Y, Z):
        u = _hash3(X // scale, Y // scale, Z // scale, seed)
        out = _broadcast(mat_indices(base, X, Y, Z), X).copy()
        sel = u < prob
        if sel.any():
            out[sel] = _broadcast(mat_indices(other, X, Y, Z), X)[sel]
        return out
    return f


def hue_mats(n, sat=0.75, val=1.0, emit=0.0, rough=0.4, prefix="hue"):
    mats = []
    for i in range(n):
        r, g, b = colorsys.hsv_to_rgb(i / n, sat, val)
        mats.append(Mat("%s_%d_%d_%s" % (prefix, n, i, emit),
                        (int(r * 255), int(g * 255), int(b * 255)),
                        rough=rough, emit=emit))
    return mats


# --------------------------------------------------------------------------
# Geometry helpers
# --------------------------------------------------------------------------

def rotmat(rx=0.0, ry=0.0, rz=0.0):
    a, b, c = np.radians([rx, ry, rz])
    Rx = np.array([[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]])
    Ry = np.array([[math.cos(b), 0, math.sin(b)], [0, 1, 0], [-math.sin(b), 0, math.cos(b)]])
    Rz = np.array([[math.cos(c), -math.sin(c), 0], [math.sin(c), math.cos(c), 0], [0, 0, 1]])
    return Rz @ Ry @ Rx


AXIS_ROT = {
    "z": (0, 0, 0), "-z": (180, 0, 0),
    "-y": (90, 0, 0), "y": (-90, 0, 0),
    "x": (0, 90, 0), "-x": (0, -90, 0),
}


def _local(X, Y, Z, c, R):
    dx, dy, dz = X - c[0], Y - c[1], Z - c[2]
    lx = R[0, 0] * dx + R[1, 0] * dy + R[2, 0] * dz
    ly = R[0, 1] * dx + R[1, 1] * dy + R[2, 1] * dz
    lz = R[0, 2] * dx + R[1, 2] * dy + R[2, 2] * dz
    return lx, ly, lz


def mx(p):
    """Mirror a point across the symmetry plane."""
    return (2 * CX - p[0],) + tuple(p[1:])


def mrot(rot):
    return (rot[0], -rot[1], -rot[2])


# --------------------------------------------------------------------------
# Grid
# --------------------------------------------------------------------------

SCALE = 1.0      # resolution multiplier used by new Grids (set per model by build.py)


class Grid:
    """Voxel grid. Every coordinate passed to the API is in *design units*
    (the 144^3 design space); the grid itself stores design * scale voxels so
    a model can be rebuilt bigger and finer without touching its recipe."""

    def __init__(self, n=N, scale=None):
        self.s = float(SCALE if scale is None else scale)
        self.n = int(math.ceil(n * self.s))
        self.v = np.zeros((self.n, self.n, self.n), np.uint16)

    # ---- core -------------------------------------------------------------
    def _region(self, lo, hi):
        s = self.s
        lo = np.clip(np.floor(np.asarray(lo, float) * s).astype(int), 0, self.n - 1)
        hi = np.clip(np.ceil(np.asarray(hi, float) * s).astype(int), 0, self.n - 1)
        if np.any(hi < lo):
            return None
        sl = tuple(slice(l, h + 1) for l, h in zip(lo, hi))
        Xi, Yi, Zi = np.meshgrid(*(np.arange(l, h + 1) for l, h in zip(lo, hi)), indexing="ij")
        return sl, Xi / s, Yi / s, Zi / s

    def _run(self, lo, hi, maskfn, mat, mode="add", where=None, only=None):
        r = self._region(lo, hi)
        if r is None:
            return
        sl, X, Y, Z = r
        m = maskfn(X, Y, Z)
        if where is not None:
            m = m & where(X, Y, Z)
        sub = self.v[sl]
        if only is not None:
            only = only if isinstance(only, (list, tuple)) else [only]
            m = m & np.isin(sub, PALETTE.indices_of(only))
        if mode == "carve":
            sub[m] = 0
            return
        if mode == "paint":
            m = m & (sub > 0)
        elif mode == "fill":
            m = m & (sub == 0)
        if not m.any():
            return
        idx = mat_indices(mat, X, Y, Z)
        if np.isscalar(idx) or np.ndim(idx) == 0:
            sub[m] = idx
        else:
            sub[m] = idx[m]

    # ---- primitives -------------------------------------------------------
    def box(self, p0, p1, mat, sym=False, **kw):
        lo = np.minimum(p0, p1).astype(float)
        hi = np.maximum(p0, p1).astype(float)

        def f(X, Y, Z):
            return ((X > lo[0] - 0.5) & (X < hi[0] + 0.5) & (Y > lo[1] - 0.5) & (Y < hi[1] + 0.5)
                    & (Z > lo[2] - 0.5) & (Z < hi[2] + 0.5))
        self._run(lo - 1, hi + 1, f, mat, **kw)
        if sym:
            self.box(mx(p0), mx(p1), mat, **kw)

    def ell(self, c, r, mat, rot=(0, 0, 0), sym=False, **kw):
        r = np.asarray(r, float)
        R = rotmat(*rot)
        ext = np.abs(R) @ r
        c = np.asarray(c, float)

        def f(X, Y, Z):
            lx, ly, lz = _local(X, Y, Z, c, R)
            return (lx / r[0]) ** 2 + (ly / r[1]) ** 2 + (lz / r[2]) ** 2 <= 1.0
        self._run(c - ext - 1, c + ext + 1, f, mat, **kw)
        if sym:
            self.ell(mx(c), r, mat, rot=mrot(rot), **kw)

    def sphere(self, c, r, mat, **kw):
        self.ell(c, (r, r, r), mat, **kw)

    def rbox(self, c, h, mat, n=4, rot=(0, 0, 0), sym=False, **kw):
        """Superellipsoid: a box with rounded edges (bigger n = sharper)."""
        h = np.asarray(h, float)
        R = rotmat(*rot)
        ext = np.abs(R) @ h
        c = np.asarray(c, float)

        def f(X, Y, Z):
            lx, ly, lz = _local(X, Y, Z, c, R)
            return (np.abs(lx / h[0]) ** n + np.abs(ly / h[1]) ** n + np.abs(lz / h[2]) ** n) <= 1.0
        self._run(c - ext - 1, c + ext + 1, f, mat, **kw)
        if sym:
            self.rbox(mx(c), h, mat, n=n, rot=mrot(rot), **kw)

    def cyl(self, c, r, h, mat, axis="z", r2=None, ry=None, ry2=None, rot=None, sym=False, **kw):
        """Cylinder / cone frustum. `c` is the centre of the base disc; it
        extends `h` along the local +z axis (given by `axis` or `rot`)."""
        r2 = r if r2 is None else r2
        ry = r if ry is None else ry
        ry2 = (ry * r2 / r if r else r2) if ry2 is None else ry2
        rot_ = AXIS_ROT[axis] if rot is None else rot
        R = rotmat(*rot_)
        c = np.asarray(c, float)
        m = max(r, r2, ry, ry2, abs(h)) + 1

        def f(X, Y, Z):
            lx, ly, lz = _local(X, Y, Z, c, R)
            t = lz / h
            rr = np.maximum(r + (r2 - r) * t, 1e-6)
            rry = np.maximum(ry + (ry2 - ry) * t, 1e-6)
            return (t >= 0) & (t <= 1) & ((lx / rr) ** 2 + (ly / rry) ** 2 <= 1.0)
        self._run(c - m - abs(h), c + m + abs(h), f, mat, **kw)
        if sym:
            self.cyl(mx(c), r, h, mat, r2=r2, ry=ry, ry2=ry2, rot=mrot(rot_), **kw)

    def torus(self, c, R_, r, mat, axis="z", rot=None, arc=None, sym=False, **kw):
        """Ring in the local xy plane. `arc` = (a0, a1) degrees keeps a part."""
        rot_ = AXIS_ROT[axis] if rot is None else rot
        R = rotmat(*rot_)
        c = np.asarray(c, float)
        m = R_ + r + 1

        def f(X, Y, Z):
            lx, ly, lz = _local(X, Y, Z, c, R)
            q = np.sqrt(lx ** 2 + ly ** 2) - R_
            ok = q ** 2 + lz ** 2 <= r * r
            if arc is not None:
                a = np.degrees(np.arctan2(ly, lx)) % 360
                a0, a1 = arc[0] % 360, arc[1] % 360
                ok &= ((a >= a0) & (a <= a1)) if a0 <= a1 else ((a >= a0) | (a <= a1))
            return ok
        self._run(c - m, c + m, f, mat, **kw)
        if sym:
            self.torus(mx(c), R_, r, mat, rot=mrot(rot_), arc=arc, **kw)

    def seg(self, p0, p1, r0, mat, r1=None, sym=False, **kw):
        """Tapered capsule between two points."""
        r1 = r0 if r1 is None else r1
        p0 = np.asarray(p0, float)
        p1 = np.asarray(p1, float)
        d = p1 - p0
        L2 = float(d @ d) or 1e-9
        m = max(r0, r1) + 1

        def f(X, Y, Z):
            px, py, pz = X - p0[0], Y - p0[1], Z - p0[2]
            t = np.clip((px * d[0] + py * d[1] + pz * d[2]) / L2, 0, 1)
            qx, qy, qz = px - t * d[0], py - t * d[1], pz - t * d[2]
            rr = r0 + (r1 - r0) * t
            return qx * qx + qy * qy + qz * qz <= rr * rr
        self._run(np.minimum(p0, p1) - m, np.maximum(p0, p1) + m, f, mat, **kw)
        if sym:
            self.seg(mx(p0), mx(p1), r0, mat, r1=r1, **kw)

    def tube(self, pts, radii, mat, sym=False, **kw):
        if np.isscalar(radii):
            radii = [radii] * len(pts)
        for i in range(len(pts) - 1):
            self.seg(pts[i], pts[i + 1], radii[i], mat, r1=radii[i + 1], **kw)
        if sym:
            self.tube([mx(p) for p in pts], radii, mat, **kw)

    def curve(self, pts, radii, mat, steps=10, **kw):
        """Smooth tube through control points (Catmull-Rom)."""
        P = [np.asarray(p, float) for p in pts]
        if np.isscalar(radii):
            radii = [radii] * len(P)
        out_p, out_r = [], []
        for i in range(len(P) - 1):
            p0 = P[i - 1] if i > 0 else P[i]
            p1, p2 = P[i], P[i + 1]
            p3 = P[i + 2] if i + 2 < len(P) else P[i + 1]
            for s in range(steps):
                t = s / steps
                t2, t3 = t * t, t * t * t
                q = 0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2
                           + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)
                out_p.append(q)
                out_r.append(radii[i] + (radii[i + 1] - radii[i]) * t)
        out_p.append(P[-1])
        out_r.append(radii[-1])
        self.tube(out_p, out_r, mat, **kw)

    def helix(self, c, R_, z0, z1, turns, r, mat, phase=0.0, R1=None, **kw):
        R1 = R_ if R1 is None else R1
        n = max(8, int(turns * 24))
        pts = []
        for i in range(n + 1):
            t = i / n
            a = phase + 2 * math.pi * turns * t
            rr = R_ + (R1 - R_) * t
            pts.append((c[0] + rr * math.cos(a), c[1] + rr * math.sin(a), z0 + (z1 - z0) * t))
        self.tube(pts, r, mat, **kw)
        return pts

    # ---- surface tools ----------------------------------------------------
    def _gi(self, d):
        return int(np.clip(round(d * self.s), 0, self.n - 1))

    def front_y(self, x, z):
        col = np.nonzero(self.v[self._gi(x), :, self._gi(z)])[0]
        return col[0] / self.s if len(col) else None

    def top_z(self, x, y):
        col = np.nonzero(self.v[self._gi(x), self._gi(y), :])[0]
        return col[-1] / self.s if len(col) else None

    def column_z(self, x, y):
        """Design z of every filled cell in the column (x, y)."""
        return np.nonzero(self.v[self._gi(x), self._gi(y), :])[0] / self.s

    def decal(self, ar, br, fn, mat, direction="-y", depth=1, sym=False, only=None):
        """Paint the first filled voxels seen from a direction.
        ar/br: inclusive ranges on the two plane axes, design units
        ('-y'/'+y': x,z   '-x'/'+x': y,z   '+z'/'-z': x,y). fn(A, B) -> mask."""
        s = self.s
        a = np.arange(int(math.floor(ar[0] * s)), int(math.ceil(ar[1] * s)) + 1)
        b = np.arange(int(math.floor(br[0] * s)), int(math.ceil(br[1] * s)) + 1)
        a = a[(a >= 0) & (a < self.n)]
        b = b[(b >= 0) & (b < self.n)]
        if len(a) == 0 or len(b) == 0:
            return
        A, B = np.meshgrid(a, b, indexing="ij")
        m = fn(A / s, B / s)
        axis = {"-y": 1, "+y": 1, "-x": 0, "+x": 0, "+z": 2, "-z": 2}[direction]
        if axis == 1:
            filled = np.moveaxis(self.v[a[0]:a[-1] + 1, :, b[0]:b[-1] + 1] > 0, 1, 2)
        elif axis == 0:
            filled = np.moveaxis(self.v[:, a[0]:a[-1] + 1, b[0]:b[-1] + 1] > 0, 0, 2)
        else:
            filled = self.v[a[0]:a[-1] + 1, b[0]:b[-1] + 1, :] > 0
        rev = direction in ("+y", "+x", "+z")
        if rev:
            filled = filled[..., ::-1]
        has = filled.any(axis=2)
        first = filled.argmax(axis=2)
        if rev:
            first = self.n - 1 - first
        sel0 = m & has
        allowed = PALETTE.indices_of(only if isinstance(only, (list, tuple)) else [only]) if only else None
        for d in range(max(1, int(round(depth * s)))):
            st = first + (-d if rev else d)
            ai, bi, si = A[sel0], B[sel0], st[sel0]
            ok = (si >= 0) & (si < self.n)
            ai, bi, si = ai[ok], bi[ok], si[ok]
            if axis == 1:
                X, Y, Z = ai, si, bi
            elif axis == 0:
                X, Y, Z = si, ai, bi
            else:
                X, Y, Z = ai, bi, si
            cur = self.v[X, Y, Z]
            keep = cur > 0
            if allowed is not None:
                keep &= np.isin(cur, allowed)
            X, Y, Z = X[keep], Y[keep], Z[keep]
            if len(X) == 0:
                continue
            idx = mat_indices(mat, X / s, Y / s, Z / s)
            self.v[X, Y, Z] = idx
        if sym and axis in (1, 2):
            def fm(A2, B2):
                return fn(2 * CX - A2, B2)
            self.decal((2 * CX - ar[1], 2 * CX - ar[0]), br, fm, mat, direction, depth, False, only)

    def plate(self, ar, br, fn, mat, thick=1.0, sym=False, gap=0.0, ymax=None):
        """Stick a raised plate on the front surface (-y): for every (x, z)
        where fn is true, add voxels in front of the surface. Good for visors,
        glasses lenses, masks, badges."""
        s = self.s
        a = np.arange(int(math.floor(ar[0] * s)), int(math.ceil(ar[1] * s)) + 1)
        b = np.arange(int(math.floor(br[0] * s)), int(math.ceil(br[1] * s)) + 1)
        a = a[(a >= 0) & (a < self.n)]
        b = b[(b >= 0) & (b < self.n)]
        A, B = np.meshgrid(a, b, indexing="ij")
        m = fn(A / s, B / s)
        filled = np.moveaxis(self.v[a[0]:a[-1] + 1, :, b[0]:b[-1] + 1] > 0, 1, 2)
        has = filled.any(axis=2)
        first = filled.argmax(axis=2)
        sel = m & has
        if ymax is not None:
            sel &= first <= ymax * s
        t = max(1, int(round(thick * s)))
        g0 = int(round(gap * s))
        for k in range(1, t + 1):
            Y = first[sel] - g0 - k
            X, Z = A[sel], B[sel]
            ok = Y >= 0
            X, Y, Z = X[ok], Y[ok], Z[ok]
            idx = mat_indices(mat, X / s, Y / s, Z / s)
            self.v[X, Y, Z] = idx
        if sym:
            def fm(A2, B2):
                return fn(2 * CX - A2, B2)
            self.plate((2 * CX - ar[1], 2 * CX - ar[0]), br, fm, mat, thick, False, gap, ymax)

    def front_ellipse(self, x, z, rx, rz, mat, depth=1, sym=False, only=None, direction="-y"):
        self.decal((x - rx - 1, x + rx + 1), (z - rz - 1, z + rz + 1),
                   lambda A, B: ((A - x) / rx) ** 2 + ((B - z) / rz) ** 2 <= 1.0,
                   mat, direction=direction, depth=depth, sym=sym, only=only)

    def lift(self, dz):
        """Move everything up by dz design units (to put a body on legs)."""
        k = int(round(dz * self.s))
        self.v[:, :, k:] = self.v[:, :, :self.n - k].copy()
        self.v[:, :, :k] = 0

    def bbox(self):
        nz = np.nonzero(self.v)
        return [(int(a.min()), int(a.max())) for a in nz]

    def count(self):
        return int(np.count_nonzero(self.v))
