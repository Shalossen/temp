"""Build every brainrot: .vox, .glb, .fbx, palette textures and preview renders.

Usage (from this folder):
    python3 build.py                 # everything
    python3 build.py --only 1,2      # some models
    python3 build.py --no-render     # skip Cycles previews
"""
import argparse
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import numpy as np  # noqa: E402

from meshing import MUTATIONS, crop, greedy_mesh, palette_size, write_palette_textures, write_vox  # noqa: E402
from roster import ROSTER  # noqa: E402
from vox import CX, PALETTE  # noqa: E402

ROOT = os.path.abspath(os.path.join(HERE, ".."))


def slug(name):
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--no-render", action="store_true")
    ap.add_argument("--samples", type=int, default=48)
    ap.add_argument("--res", type=int, default=900)
    ap.add_argument("--mutations", default="", help="model numbers to render in every mutation")
    args = ap.parse_args()
    only = {int(s) for s in args.only.split(",") if s}

    # 1) build all voxel grids first (the palette must be complete before UVs)
    built = []
    for item in sorted(ROSTER, key=lambda r: r["num"]):
        t = time.time()
        g = item["build"]()
        v, lo = crop(g.v)
        built.append((item, v, lo))
        print("built %2d %-28s %s voxels=%d (%.1fs)" % (item["num"], item["name"], v.shape,
                                                        int(np.count_nonzero(v)), time.time() - t))
    entries = PALETTE.entries
    side = palette_size(len(entries))
    print("palette entries:", len(entries) - 1, "texture:", side)

    tex_dir = os.path.join(ROOT, "textures")
    os.makedirs(os.path.join(tex_dir, "mutations"), exist_ok=True)
    tex = write_palette_textures(entries, side, tex_dir)
    mut_tex = {}
    for name, fn in MUTATIONS.items():
        mut_tex[name] = write_palette_textures(entries, side, os.path.join(tex_dir, "mutations"),
                                               suffix="_" + name, transform=fn)

    import blender_io as B  # bpy import is slow, do it once
    B.reset_scene()
    material = B.make_material(tex)
    cam = None if args.no_render else B.setup_render_scene(res=args.res, samples=args.samples)

    meta = []
    for item, v, lo in built:
        if only and item["num"] not in only:
            continue
        s = slug(item["name"])
        out = os.path.join(ROOT, "models", "%02d_%s" % (item["num"], s))
        os.makedirs(out, exist_ok=True)
        t = time.time()
        write_vox(os.path.join(out, "%s.vox" % s), v, entries)
        verts, quads, pals = greedy_mesh(v)
        # pivot: centre of the symmetry plane in x, centre of depth in y, ground in z
        origin = (CX - lo[0] + 0.5, v.shape[1] / 2.0, 0.0)
        obj = B.build_object("SM_Brainrot_%s" % s, verts, quads, pals, entries, side, material, origin)
        B.export(obj, os.path.join(out, "%s.glb" % s), os.path.join(out, "%s.fbx" % s))
        tris = len(quads) * 2
        dims_m = [round(d * B.VOXEL_M, 2) for d in v.shape]
        print("exported %2d %-28s tris=%d size=%sm (%.1fs)" % (item["num"], item["name"], tris, dims_m, time.time() - t))
        if cam is not None:
            t = time.time()
            B.frame_camera(cam, obj)
            B.render(os.path.join(out, "preview.png"))
            print("rendered (%.1fs)" % (time.time() - t))
            if str(item["num"]) in args.mutations.split(","):
                for mname, paths in mut_tex.items():
                    B.swap_textures(material, paths)
                    B.render(os.path.join(out, "mutation_%s.png" % mname))
                B.swap_textures(material, tex)
        obj.hide_render = True
        meta.append(dict(num=item["num"], name=item["name"], slug=s, rarity=item["rarity"],
                         income=item["income"], concept=item["concept"], triangles=tris,
                         voxels=int(np.count_nonzero(v)), size_m=dims_m,
                         folder="models/%02d_%s" % (item["num"], s)))

    if not only:
        with open(os.path.join(ROOT, "roster.json"), "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
