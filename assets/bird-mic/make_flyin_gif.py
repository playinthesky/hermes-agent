"""Bird flies in from the distance, then offers the mic to the viewer.

Outputs a transparent-background animated GIF (and APNG) for Keynote.
"""
import math
from PIL import Image

SRC = "bird-mic.webp"
OUT_GIF = "bird-mic-flyin.gif"
OUT_APNG = "bird-mic-flyin.png"

CW, CH = 960, 720          # canvas
FPS_MS = 50                # 20 fps
BIRD_W_FINAL = 700         # final on-screen width of the bird

bird = Image.open(SRC).convert("RGBA")
AR = bird.height / bird.width

def ease_out_cubic(t):
    return 1 - (1 - t) ** 3

def smoothstep(t):
    return t * t * (3 - 2 * t)

frames = []

def add_frame(scale, cx, cy, rot=0.0):
    """scale: fraction of final size; (cx, cy): bird center on canvas."""
    w = max(8, int(BIRD_W_FINAL * scale))
    h = max(8, int(w * AR))
    spr = bird.resize((w, h), Image.LANCZOS)
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
    bob = math.sin(t * math.pi * 5) * 14 * scale  # wing-beat bobbing
    tilt = -10 * (1 - t) + math.sin(t * math.pi * 5) * 3 * (1 - t)
    add_frame(scale, x, y + bob, tilt)

# ---- Phase 2: offer the mic (anticipate, push toward viewer, settle) ----
for i in range(4):   # anticipation: pull back slightly
    t = (i + 1) / 4
    add_frame(1.0 - 0.05 * smoothstep(t), x1 - 12 * t, y1 + 4 * t, 2 * t)
for i in range(5):   # push: grow toward camera, lean into the handoff
    t = (i + 1) / 5
    e = ease_out_cubic(t)
    add_frame(0.95 + 0.22 * e, x1 - 12 + 30 * e, y1 + 4 - 10 * e, 2 - 5 * e)
for i in range(4):   # settle back a touch
    t = (i + 1) / 4
    e = smoothstep(t)
    add_frame(1.17 - 0.07 * e, x1 + 18 - 6 * e, y1 - 6 + 2 * e, -3 + 3 * e)

# ---- Phase 3: hold with a gentle idle bob ----
N3 = 22
for i in range(N3):
    t = i / N3
    bob = math.sin(t * math.pi * 2) * 5
    add_frame(1.10, x1 + 12, y1 - 4 + bob, 0)

# ---- Save GIF with one shared palette (no flicker) ----
palette_src = bird.resize((400, int(400 * AR)), Image.LANCZOS)
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
