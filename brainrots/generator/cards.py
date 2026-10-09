"""Game-style cards for every brainrot + a roster sheet and a mutation strip.

Run after build.py:  python3 cards.py [--mutations 14]
"""
import argparse
import json
import math
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
FONT = os.path.join(HERE, "fonts", "LilitaOne-Regular.ttf")

RARITY_STYLE = {
    "Common": ((120, 130, 140), (200, 208, 214), (255, 255, 255)),
    "Rare": ((20, 70, 190), (90, 170, 255), (255, 255, 255)),
    "Epic": ((80, 20, 150), (190, 110, 255), (255, 255, 255)),
    "Legendary": ((190, 90, 0), (255, 200, 60), (255, 255, 255)),
    "Mythic": ((150, 0, 40), (255, 80, 110), (255, 255, 255)),
    "Divine": ((150, 110, 10), (255, 240, 160), (255, 255, 255)),
    "Secret": ((8, 8, 12), (60, 30, 90), (255, 255, 255)),
}
W, H = 900, 1150


def font(size):
    return ImageFont.truetype(FONT, size)


def outlined(draw, xy, text, fnt, fill, stroke=(20, 20, 28), width=6, anchor="mm"):
    draw.text(xy, text, font=fnt, fill=fill, stroke_width=width, stroke_fill=stroke, anchor=anchor)


def background(rarity):
    dark, light, _ = RARITY_STYLE[rarity]
    img = Image.new("RGB", (W, H), dark)
    px = img.load()
    cx, cy = W / 2, H * 0.45
    maxd = math.hypot(W, H) * 0.6
    for y in range(H):
        for x in range(W):
            t = min(1.0, math.hypot(x - cx, y - cy) / maxd)
            t = t ** 1.2
            px[x, y] = tuple(int(light[i] * (1 - t) + dark[i] * t) for i in range(3))
    d = ImageDraw.Draw(img, "RGBA")
    if rarity in ("Divine", "Legendary", "Mythic"):
        for k in range(24):
            a0 = k * 15
            if k % 2:
                continue
            pts = [(cx, cy)]
            for a in (a0, a0 + 7.5):
                r = math.radians(a)
                pts.append((cx + 1400 * math.cos(r), cy + 1400 * math.sin(r)))
            d.polygon(pts, fill=(255, 255, 255, 28))
    if rarity == "Secret":
        import random
        rnd = random.Random(7)
        for _ in range(140):
            x, y = rnd.randrange(W), rnd.randrange(H)
            s = rnd.choice((6, 10, 16))
            col = rnd.choice(((255, 40, 200, 120), (40, 240, 255, 120), (255, 240, 60, 90)))
            d.rectangle((x, y, x + s, y + s), fill=col)
        for _ in range(10):
            y = rnd.randrange(H)
            d.rectangle((0, y, W, y + rnd.choice((2, 4))), fill=(40, 240, 255, 60))
    return img


def make_card(item, preview_path, out_path):
    rarity = item["rarity"]
    img = background(rarity).convert("RGBA")
    d = ImageDraw.Draw(img)
    # frame
    d.rounded_rectangle((10, 10, W - 10, H - 10), radius=46, outline=(255, 255, 255), width=8)
    # model + soft shadow already in the render
    model = Image.open(preview_path).convert("RGBA")
    bbox = model.getbbox()
    if bbox:
        model = model.crop(bbox)
    scale = min((W - 120) / model.width, 700 / model.height)
    model = model.resize((int(model.width * scale), int(model.height * scale)), Image.LANCZOS)
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gx = (W - model.width) // 2
    gy = 170 + (700 - model.height) // 2
    alpha = model.split()[3].point(lambda a: 255 if a > 40 else 0)
    halo = Image.new("RGBA", model.size, (255, 255, 255, 150))
    halo.putalpha(alpha)
    glow.alpha_composite(halo, (gx, gy))
    glow = glow.filter(ImageFilter.GaussianBlur(14))
    img.alpha_composite(glow)
    img.alpha_composite(model, (gx, gy))
    # rarity pill
    rtxt = rarity.upper()
    f_r = font(64)
    tw = d.textlength(rtxt, font=f_r)
    dark, light, _ = RARITY_STYLE[rarity]
    pill = (W / 2 - tw / 2 - 40, 48, W / 2 + tw / 2 + 40, 140)
    d.rounded_rectangle(pill, radius=46, fill=dark + (255,), outline=(255, 255, 255), width=5)
    rcol = (255, 236, 120) if rarity == "Divine" else ((40, 240, 255) if rarity == "Secret" else (255, 255, 255))
    outlined(d, (W / 2, 96), rtxt, f_r, rcol, width=5)
    d.text((44, 40), "#%02d" % item["num"], font=font(52), fill=(255, 255, 255), stroke_width=5,
           stroke_fill=(20, 20, 28))
    # name (two lines if needed)
    words = item["name"].split()
    lines = [item["name"]] if len(item["name"]) <= 16 else [" ".join(words[:len(words) // 2 or 1]),
                                                             " ".join(words[len(words) // 2 or 1:])]
    f_n = font(84 if len(lines) == 1 else 76)
    y = 930 if len(lines) == 1 else 900
    for ln in lines:
        outlined(d, (W / 2, y), ln, f_n, (255, 255, 255), width=8)
        y += 84
    outlined(d, (W / 2, H - 70), item["income"], font(72), (90, 255, 110), width=7)
    img.convert("RGB").save(out_path, quality=92)


def roster_sheet(cards, out_path, cols=6):
    cw, ch = 300, int(300 * H / W)
    rows = math.ceil(len(cards) / cols)
    head = 170
    sheet = Image.new("RGB", (cols * cw + 40, rows * ch + head + 30), (24, 22, 38))
    d = ImageDraw.Draw(sheet)
    outlined(d, (sheet.width / 2, 80), "30 BRAINROTS ORIGINAUX", font(96), (255, 255, 255), width=8)
    for i, p in enumerate(cards):
        c = Image.open(p).resize((cw - 10, ch - 10), Image.LANCZOS)
        sheet.paste(c, (20 + (i % cols) * cw + 5, head + (i // cols) * ch + 5))
    sheet.save(out_path, quality=90)


def mutation_strip(folder, item, out_path):
    names = ["Normal", "Gold", "Diamond", "Void", "Lava", "Neon", "Candy", "BlackWhite"]
    tiles = []
    for n in names:
        p = os.path.join(folder, "preview.png" if n == "Normal" else "mutation_%s.png" % n)
        if os.path.exists(p):
            tiles.append((n, Image.open(p).convert("RGBA")))
    tw = 420
    strip = Image.new("RGB", (tw * len(tiles), tw + 150), (24, 22, 38))
    d = ImageDraw.Draw(strip)
    for i, (n, im) in enumerate(tiles):
        bbox = im.getbbox()
        im = im.crop(bbox)
        s = min((tw - 40) / im.width, (tw - 40) / im.height)
        im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        bg = Image.new("RGBA", (tw, tw), (48, 44, 70, 255))
        bg.alpha_composite(im, ((tw - im.width) // 2, (tw - im.height) // 2))
        strip.paste(bg.convert("RGB"), (i * tw, 120))
        outlined(d, (i * tw + tw / 2, 70), n, font(56), (255, 255, 255), width=6)
    outlined(d, (strip.width / 2, tw + 135), "", font(10), (255, 255, 255))
    strip.save(out_path, quality=90)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutations", default="")
    args = ap.parse_args()
    roster = json.load(open(os.path.join(ROOT, "roster.json"), encoding="utf-8"))
    out_dir = os.path.join(ROOT, "previews")
    os.makedirs(os.path.join(out_dir, "cards"), exist_ok=True)
    cards = []
    for item in roster:
        folder = os.path.join(ROOT, item["folder"])
        out = os.path.join(out_dir, "cards", "%02d_%s.jpg" % (item["num"], item["slug"]))
        make_card(item, os.path.join(folder, "preview.png"), out)
        cards.append(out)
        print("card", out)
    roster_sheet(cards, os.path.join(out_dir, "roster_sheet.jpg"))
    for n in [int(s) for s in args.mutations.split(",") if s]:
        item = next(r for r in roster if r["num"] == n)
        mutation_strip(os.path.join(ROOT, item["folder"]), item,
                       os.path.join(out_dir, "mutations_%02d_%s.jpg" % (n, item["slug"])))


if __name__ == "__main__":
    main()
