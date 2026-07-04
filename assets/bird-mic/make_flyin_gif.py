"""Bird flies in from the distance flapping its wing, then offers the mic.

The wing is cut out of the still image and rotated around the shoulder to
create a real flapping motion; the body (drawn on top) hides the seam.
Outputs a transparent-background animated GIF (and APNG) for Keynote.
"""
import math
from PIL import Image, ImageChops, ImageDraw, ImageFilter

SRC = "bird-mic.webp"
OUT_GIF = "bird-mic-flyin.gif"
OUT_APNG = "bird-mic-flyin.apng.png"

CW, CH = 960, 720          # canvas
FPS_MS = 50                # 20 fps
BIRD_W_FINAL = 700         # final on-screen width of the bird

src = Image.open(SRC).convert("RGBA")
W, H = src.size
AR = H / W

# ---- split the wing from the body ----
# generous wing polygon (includes a junction band into the body fluff)
WING_POLY = [
    (1000, 545), (900, 560), (800, 610), (700, 625), (600, 595),
    (500, 460), (300, 400), (100, 395), (-50, 460),
    (-50, 780), (60, 950), (160, 1080), (300, 1170),
    (480, 1180), (650, 1160), (820, 1080), (950, 950),
    (1020, 800), (1030, 650),
]
# same polygon with the junction edge pulled ~45px toward the wing, so the
# body keeps a static band of fluff that covers the rotation seam
WING_ONLY_POLY = [
    (955, 585), (880, 600), (790, 650), (700, 665), (600, 635),
    (500, 460), (300, 400), (100, 395), (-50, 460),
    (-50, 780), (60, 950), (160, 1080), (300, 1170),
    (480, 1180), (640, 1120), (780, 1040), (905, 915),
    (975, 790), (985, 655),
]
PIVOT = (960, 640)         # wing shoulder

wing_mask = Image.new("L", (W, H), 0)
ImageDraw.Draw(wing_mask).polygon(WING_POLY, fill=255)
wing_mask = wing_mask.filter(ImageFilter.GaussianBlur(12))

only_mask = Image.new("L", (W, H), 0)
ImageDraw.Draw(only_mask).polygon(WING_ONLY_POLY, fill=255)
only_mask = only_mask.filter(ImageFilter.GaussianBlur(8))

wing = Image.new("RGBA", (W, H), (0, 0, 0, 0))
wing.paste(src, mask=wing_mask)

body = src.copy()
body.putalpha(ImageChops.multiply(body.getchannel("A"), ImageChops.invert(only_mask)))

_pose_cache = {}

def bird_pose(theta):
    """Full-res bird with the wing rotated by theta degrees (positive = up)."""
    key = round(theta * 2) / 2
    if key not in _pose_cache:
        wr = wing.rotate(-key, center=PIVOT, resample=Image.BICUBIC)
        frame = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        frame.alpha_composite(wr)
        frame.alpha_composite(body)
        _pose_cache[key] = frame
    return _pose_cache[key]

def ease_out_cubic(t):
    return 1 - (1 - t) ** 3

def smoothstep(t):
    return t * t * (3 - 2 * t)

frames = []

def add_frame(scale, cx, cy, rot=0.0, flap=0.0):
    """scale: fraction of final size; (cx, cy): bird center; flap: wing deg."""
    w = max(8, int(BIRD_W_FINAL * scale))
    h = max(8, int(w * AR))
    spr = bird_pose(flap).resize((w, h), Image.LANCZOS)
    if abs(rot) > 0.1:
        spr = spr.rotate(rot, resample=Image.BICUBIC, expand=True)
    canvas = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    canvas.alpha_composite(spr, (int(cx - spr.width / 2), int(cy - spr.height / 2)))
    frames.append(canvas)

# ---- Phase 1: fly in from far away (upper-left, tiny -> center, full) ----
N1 = 34
x0, y0 = CW * 0.10, CH * 0.20
x1, y1 = CW * 0.50, CH * 0.52
s0, s1 = 0.05, 1.0
for i in range(N1):
    t = i / (N1 - 1)
    pt = ease_out_cubic(t)                       # position eases out
    scale = s0 * (s1 / s0) ** smoothstep(t)      # exponential growth = approach
    x = x0 + (x1 - x0) * pt
    y = y0 + (y1 - y0) * pt
    bob = math.sin(t * math.pi * 5) * 14 * scale     # wing-beat bobbing
    flap = -10 + 16 * math.sin(t * math.pi * 5 + math.pi / 2)
    tilt = -10 * (1 - t) + math.sin(t * math.pi * 5) * 3 * (1 - t)
    add_frame(scale, x, y + bob, tilt, flap)

# ---- Phase 2: offer the mic (anticipate, push toward viewer, settle) ----
flap_arrive = -10 + 16 * math.sin(math.pi * 5 + math.pi / 2)
for i in range(4):   # anticipation: pull back slightly, wing rises
    t = (i + 1) / 4
    f = flap_arrive + (6 - flap_arrive) * smoothstep(t)
    add_frame(1.0 - 0.05 * smoothstep(t), x1 - 12 * t, y1 + 4 * t, 2 * t, f)
for i in range(5):   # push: grow toward camera, wing sweeps down
    t = (i + 1) / 5
    e = ease_out_cubic(t)
    f = 6 + (-20 - 6) * e
    add_frame(0.95 + 0.22 * e, x1 - 12 + 30 * e, y1 + 4 - 10 * e, 2 - 5 * e, f)
for i in range(4):   # settle back a touch
    t = (i + 1) / 4
    e = smoothstep(t)
    f = -20 + (-8 + 20) * e
    add_frame(1.17 - 0.07 * e, x1 + 18 - 6 * e, y1 - 6 + 2 * e, -3 + 3 * e, f)

# ---- Phase 3: hold with a gentle hover flap ----
N3 = 22
for i in range(N3):
    t = i / N3
    bob = math.sin(t * math.pi * 2) * 5
    flap = -8 + 10 * math.sin(t * math.pi * 4 + math.pi / 2)
    add_frame(1.10, x1 + 12, y1 - 4 + bob, 0, flap)

# ---- Save GIF with one shared palette (no flicker) ----
palette_src = src.resize((400, int(400 * AR)), Image.LANCZOS)
pal_rgb = Image.new("RGB", palette_src.size, (255, 255, 255))
pal_rgb.paste(palette_src, mask=palette_src.getchannel("A"))
global_pal = pal_rgb.quantize(colors=255)

pframes = []
for f in frames:
    alpha = f.getchannel("A")
    rgb = Image.new("RGB", f.size, (255, 255, 255))
    rgb.paste(f, mask=alpha)
    p = rgb.quantize(colors=255, palette=global_pal, dither=Image.NONE)
    mask = alpha.point(lambda a: 255 if a < 128 else 0)
    p.paste(255, mask)          # index 255 = transparent
    pframes.append(p)

pframes[0].save(
    OUT_GIF, save_all=True, append_images=pframes[1:],
    duration=FPS_MS, loop=0, transparency=255, disposal=2, optimize=False,
)

# ---- APNG: full 8-bit alpha, much cleaner in Keynote ----
frames[0].save(
    OUT_APNG, save_all=True, append_images=frames[1:],
    duration=FPS_MS, loop=0, default_image=False,
)

import os
print("GIF :", os.path.getsize(OUT_GIF) // 1024, "KB,", len(frames), "frames")
print("APNG:", os.path.getsize(OUT_APNG) // 1024, "KB")
