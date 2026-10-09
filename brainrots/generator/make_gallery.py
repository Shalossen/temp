"""Assemble the web gallery (brainrots/web): thumbnails, GLBs, palettes and index.html."""
import json
import os
import shutil

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
WEB = os.path.join(ROOT, "web")


def main():
    roster = json.load(open(os.path.join(ROOT, "roster.json"), encoding="utf-8"))
    for sub in ("thumbs", "glb", "tex/mutations"):
        os.makedirs(os.path.join(WEB, sub), exist_ok=True)
    for r in roster:
        folder = os.path.join(ROOT, r["folder"])
        im = Image.open(os.path.join(folder, "preview.png")).convert("RGBA")
        im = im.crop(im.getbbox())
        side = max(im.size)
        sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        sq.alpha_composite(im, ((side - im.width) // 2, (side - im.height) // 2))
        sq.resize((360, 360), Image.LANCZOS).save(os.path.join(WEB, "thumbs", r["slug"] + ".webp"), quality=86)
        shutil.copy(os.path.join(folder, r["slug"] + ".glb"), os.path.join(WEB, "glb", r["slug"] + ".glb"))
    tex = os.path.join(ROOT, "textures")
    for f in os.listdir(tex):
        if f.endswith(".png"):
            shutil.copy(os.path.join(tex, f), os.path.join(WEB, "tex", f))
    for f in os.listdir(os.path.join(tex, "mutations")):
        shutil.copy(os.path.join(tex, "mutations", f), os.path.join(WEB, "tex", "mutations", f))
    html = open(os.path.join(HERE, "gallery_template.html"), encoding="utf-8").read()
    data = [{k: r[k] for k in ("num", "name", "slug", "rarity", "income", "concept", "triangles", "voxels",
                               "size_m", "folder")} for r in roster]
    html = html.replace("/*DATA*/[]", json.dumps(data, ensure_ascii=False))
    open(os.path.join(WEB, "index.html"), "w", encoding="utf-8").write(html)
    print("gallery written:", WEB)
    update_readme(roster)


RAR_FR = {"Common": "Commun", "Rare": "Rare", "Epic": "Épique", "Legendary": "Légendaire",
          "Mythic": "Mythique", "Divine": "Divin", "Secret": "Secret"}


def update_readme(roster):
    path = os.path.join(ROOT, "README.md")
    s = open(path, encoding="utf-8").read()
    rows = ["| # | Aperçu | Nom | Rareté | Revenu | Concept | Taille (m) | Triangles |",
            "|---|---|---|---|---|---|---|---|"]
    for r in roster:
        rows.append("| %02d | <img src=\"web/thumbs/%s.webp\" width=\"72\"> | **%s** | %s | %s | %s | %s × %s × %s | %s |" % (
            r["num"], r["slug"], r["name"], RAR_FR[r["rarity"]], r["income"], r["concept"],
            r["size_m"][0], r["size_m"][1], r["size_m"][2], format(r["triangles"], ",").replace(",", " ")))
    a = s.index("<!-- ROSTER_TABLE -->") + len("<!-- ROSTER_TABLE -->")
    b = s.index("<!-- /ROSTER_TABLE -->")
    s = s[:a] + "\n" + "\n".join(rows) + "\n" + s[b:]
    open(path, "w", encoding="utf-8").write(s)


if __name__ == "__main__":
    main()
