#!/usr/bin/env python3
"""Render the 8 modulize promo scenes (1280x720 PNGs)."""
import os, math, random
from PIL import Image, ImageDraw, ImageFont

OUT = "/home/theneovimmer/Documents/Modulize/assets/promo/scenes"
os.makedirs(OUT, exist_ok=True)

W, H = 1280, 720
BG = (10, 10, 10)
PANEL = (20, 20, 20)
LINE = (38, 38, 38)
WHITE = (250, 250, 250)
GREY = (163, 163, 163)
FAINT = (115, 115, 115)
GREEN = (74, 222, 128)
RED = (248, 113, 113)
GOLD = (252, 211, 77)

# fonts: Noto Sans family + monospace fallback
def font(size, bold=False, mono=False):
    candidates = []
    if mono:
        candidates = ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
                      "/usr/share/fonts/noto/NotoMono-Regular.ttf",
                      "/usr/share/fonts/noto/NotoMono-Bold.ttf" if bold else "/usr/share/fonts/noto/NotoMono-Regular.ttf"]
    if bold:
        candidates += ["/usr/share/fonts/noto/NotoSans-Bold.ttf",
                       "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"]
    else:
        candidates += ["/usr/share/fonts/noto/NotoSans-Regular.ttf",
                       "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def new_canvas():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    for x in range(0, W, 34):
        for y in range(0, H, 34):
            d.point((x, y), fill=(22, 22, 22))
    return img, d

def centered(d, y, text, fnt, fill=WHITE):
    tw = d.textlength(text, font=fnt)
    d.text(((W - tw) / 2, y), text, font=fnt, fill=fill)

def top_label(d, text):
    centered(d, 44, text, font(24, True), FAINT)

def mark(draw, cx, cy, scale):
    # three lines merging right (the modulize mark)
    draw.line([(cx-70*scale, cy-30*scale), (cx-10*scale, cy-6*scale), (cx+80*scale, cy)], fill=WHITE, width=int(8*scale))
    draw.line([(cx-70*scale, cy), (cx+80*scale, cy)], fill=WHITE, width=int(8*scale))
    draw.line([(cx-70*scale, cy+30*scale), (cx-10*scale, cy+6*scale), (cx+80*scale, cy)], fill=WHITE, width=int(8*scale))

def save(img, name):
    path = os.path.join(OUT, name)
    img.save(path)
    print("wrote", path)

random.seed(7)

# 1 — The mess
img, d = new_canvas()
top_label(d, "THE MESS")
draw = ImageDraw.Draw(img)
# knot: random web center-right
pts = [(640 + random.randint(-320, 320), 390 + random.randint(-170, 170)) for _ in range(46)]
for i in range(len(pts)-1):
    draw.line([pts[i], pts[i+1]], fill=(90, 90, 90), width=2)
for p in pts:
    if random.random() < 0.3:
        draw.ellipse([p[0]-5, p[1]-5, p[0]+5, p[1]+5], fill=RED)
labels = ["if (special case)", "TODO", "workaround", "sleep(100ms)", "duplicated", "if provider == 'x'"]
lx, ly = 120, 470
for i, l in enumerate(labels):
    x = lx + (i % 3) * 360
    y = ly + (i // 3) * 60
    draw.rounded_rectangle([x, y, x + 300, y + 44], 10, fill=(30, 18, 18), outline=(70, 35, 35))
    draw.text((x+16, y+10), l, font=font(20, False, True), fill=RED)
centered(d, 100, "One feature. Five folders by layer.", font(40, True))
save(img, "01-mess.png")

# 2 — Phase 0 safety net
img, d = new_canvas()
top_label(d, "PHASE 0 — THE SAFETY NET")
d.rounded_rectangle([190, 150, 1090, 560], 18, fill=PANEL, outline=LINE, width=2)
d.text((240, 185), "$ git status — clean", font=font(30, False, True), fill=WHITE)
d.text((240, 265), "$ npm test → 212 passing", font=font(30, False, True), fill=WHITE)
d.text((240, 345), "$ git stash — checkpoint", font=font(30, False, True), fill=WHITE)
for i, y in enumerate([190, 270, 350]):
    d.ellipse([1010, y, 1050, y+40], outline=GREEN, width=3)
    d.line([(1018, y+20), (1028, y+30), (1044, y+10)], fill=GREEN, width=4)
centered(d, 610, "Before a single file is touched.", font(34, True), GREY)
save(img, "02-safety-net.png")

# 3 — Phase 2 mapping
img, d = new_canvas()
top_label(d, "PHASE 2 — MAP")
nodes = [(340, 230), (640, 180), (940, 230), (340, 420), (640, 470), (940, 420)]
edges = [(0,1),(1,2),(0,3),(1,4),(2,5),(3,4),(4,5),(0,4)]
for a,b in edges:
    d.line([nodes[a], nodes[b]], fill=(80, 80, 80), width=3)
for i,(x,y) in enumerate(nodes):
    fill = GOLD if i in (1,4) else (30, 30, 30)
    d.ellipse([x-42, y-42, x+42, y+42], fill=fill, outline=(60,60,60), width=2)
for s in range(3):
    x = 200 + s*400
    d.line([(x, 300), (x+300, 300)], fill=(252, 211, 77), width=2)
d.rounded_rectangle([490, 580, 790, 636], 10, fill=(30, 28, 14), outline=(80, 75, 40))
centered(d, 594, "import graph · skeleton", font(22, False, True), GOLD)
save(img, "03-map.png")

# 4 — Phase 3 list
img, d = new_canvas()
top_label(d, "PHASE 3 — LIST EVERY PROBLEM")
rows = [("HIDDEN LINK", "duplicated money formatting × 3", RED),
        ("HIDDEN LINK", "checkout → payments/stripe.ts direct", RED),
        ("NEEDLESS LINK", "the 100ms sleep hoping for focus", GOLD),
        ("NEEDLESS LINK", "stable code importing a volatile SDK", GOLD),
        ("SURPLUS", "wrapper functions that only forward calls", (96, 165, 250)),
        ("SURPLUS", "unused exports + dead feature flags", (96, 165, 250)),
        ("SPECIAL CASE", "if (provider == 'paypal') …", (192, 132, 252)),
        ("SPECIAL CASE", "try { } catch { /* swallow */ }", (192, 132, 252))]
y = 140
for tag, txt, col in rows:
    d.rounded_rectangle([210, y, 1070, y+54], 12, fill=PANEL, outline=LINE, width=1)
    d.rectangle([210, y, 224, y+54], fill=col)
    d.text((250, y+14), tag, font=font(19, True), fill=col)
    d.text((520, y+14), txt, font=font(22, False, True), fill=WHITE)
    y += 70
save(img, "04-list.png")

# 5 — Phase 4 redesign
img, d = new_canvas()
top_label(d, "PHASE 4 — REDESIGN FROM FIRST PRINCIPLES")
# before: knot (left)
pts = [(330 + random.randint(-140, 140), 410 + random.randint(-140, 140)) for _ in range(22)]
for i in range(len(pts)-1):
    d.line([pts[i], pts[i+1]], fill=(90, 90, 90), width=2)
centered(d, 600, "", font(1))
# sweep line
d.line([(600, 130), (600, 600)], fill=WHITE, width=4)
# after: clean modules (right)
for i in range(4):
    y = 200 + i*90
    d.rounded_rectangle([740, y, 1120, y+62], 10, fill=(16, 24, 18), outline=(34, 80, 50), width=2)
    d.rectangle([740, y, 754, y+62], fill=GREEN)
d.text((210, 600), "the knot", font=font(22), fill=FAINT)
d.text((770, 600), "one change · one place", font=font(22), fill=GREEN)
save(img, "05-redesign.png")

# 6 — Phase 5 fix
img, d = new_canvas()
top_label(d, "PHASE 5 — FIX")
d.rounded_rectangle([240, 140, 1040, 330], 16, fill=PANEL, outline=LINE, width=2)
d.text((290, 170), "refactor: single registry", font=font(28, False, True), fill=WHITE)
d.text((290, 215), "for every action + undo", font=font(28, False, True), fill=WHITE)
d.text((290, 268), "suite: green between commits", font=font(22, False, True), fill=GREEN)
# counter
d.rounded_rectangle([415, 400, 865, 520], 16, fill=(16, 24, 18), outline=(34, 80, 50), width=2)
centered(d, 418, "files touched", font(20), FAINT)
centered(d, 446, "5  →  1", font(52, True), GREEN)
save(img, "06-fix.png")

# 7 — Phase 6 loop
img, d = new_canvas()
top_label(d, "PHASE 6 — VERIFY & LOOP")
d.rounded_rectangle([290, 150, 990, 470], 18, fill=PANEL, outline=LINE, width=2)
rows = [("fresh-eyes sweep", "nothing worth fixing"),
        ("import audit", "no reverse edges"),
        ("one-place check", "2 changes traced"),
        ("suite vs baseline", "same or better")]
y = 185
for a, b in rows:
    d.text((340, y), a, font=font(26, True), fill=WHITE)
    d.text((700, y), b, font=font(26, False, True), fill=GREY)
    d.line([(1018, y+4), (1028, y+14), (1044, y-6)], fill=GREEN, width=4)
    y += 70
centered(d, 540, "special cases: 17  →  2  (each one justified)", font(30, True), GOLD)
save(img, "07-verify.png")

# 8 — Close
img, d = new_canvas()
mark(d, 210, 360, 1.5)
d.text((380, 220), "modulize", font=font(130, True), fill=WHITE)
d.text((386, 380), "Say goodbye to messy code.", font=font(40), fill=GREY)
d.rounded_rectangle([386, 480, 1105, 562], 14, fill=(20, 20, 20), outline=LINE, width=2)
d.text((416, 504), "$ npx skills add TheNeovimmer/modulize", font=font(26, False, True), fill=WHITE)
d.text((386, 600), "/modulize  ·  MIT  ·  TheNeovimmer", font=font(24), fill=FAINT)
save(img, "08-close.png")

print("done — 8 scenes")
