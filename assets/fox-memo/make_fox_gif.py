"""Fox walks in, scribbles a memo, and an exclamation mark pops above its head.

Layers cut from the still image:
  - bulb: the exclamation balloon + rays (a separate alpha component)
  - hand: pen + writing paw, rotated around the pen tip for a scribble motion
  - body: everything else; the hole behind the hand is inpainted
Outputs a transparent-background GIF and APNG for Keynote.
"""
import math
from PIL import Image, ImageChops, ImageDraw, ImageFilter
import numpy as np
from collections import deque

SRC = "fox.webp"
OUT_GIF = "fox-memo.gif"
OUT_APNG = "fox-memo.apng.png"

CW, CH = 960, 720
FPS_MS = 50

src = Image.open(SRC).convert("RGBA")
W, H = src.size

# ---- bulb = alpha components above the head ----
a = np.asarray(src.getchannel("A"))
s4 = 4
small = (a[::s4, ::s4] > 10).astype(np.uint8)
h, w = small.shape
lab = np.zeros((h, w), dtype=np.int32)
cur = 0
for y in range(h):
    for x in range(w):
        if small[y, x] and not lab[y, x]:
            cur += 1
            q = deque([(y, x)]); lab[y, x] = cur
            while q:
                cy, cx = q.popleft()
                for dy, dx in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
                    ny, nx = cy+dy, cx+dx
                    if 0 <= ny < h and 0 <= nx < w and small[ny, nx] and not lab[ny, nx]:
                        lab[ny, nx] = cur; q.append((ny, nx))
# bulb components: everything whose bbox lies in the top quarter
bulb_small = np.zeros((h, w), dtype=np.uint8)
for c in range(1, cur + 1):
    ys, xs = np.where(lab == c)
    if ys.max() * s4 < 560:
        bulb_small[lab == c] = 255
bulb_mask = Image.fromarray(bulb_small).resize((W, H), Image.NEAREST)
bulb_mask = bulb_mask.filter(ImageFilter.MaxFilter(9))  # dilate to keep outlines

bulb = src.copy()
bulb.putalpha(ImageChops.multiply(src.getchannel("A"), bulb_mask))
char = src.copy()
char.putalpha(ImageChops.multiply(char.getchannel("A"), ImageChops.invert(bulb_mask)))
BULB_ANCHOR = (712, 500)   # bottom of the balloon tail

# ---- hand = pen + writing paw ----
HAND_POLY = [
    (590, 1170), (710, 1185), (722, 1250), (722, 1320), (770, 1395),
    (778, 1445), (700, 1470), (640, 1465), (560, 1480), (478, 1470),
    (438, 1438), (460, 1388), (500, 1330), (545, 1265), (562, 1215),
]
PEN_PIVOT = (475, 1435)    # pen tip stays planted on the pad

hand_mask = Image.new("L", (W, H), 0)
ImageDraw.Draw(hand_mask).polygon(HAND_POLY, fill=255)
hand_mask = hand_mask.filter(ImageFilter.GaussianBlur(2))

hand = char.copy()
hand.putalpha(ImageChops.multiply(char.getchannel("A"), hand_mask))

hole_mask = hand_mask.point(lambda v: 255 if v > 210 else 0).filter(ImageFilter.MinFilter(5))
body = char.copy()
body.putalpha(ImageChops.multiply(body.getchannel("A"), ImageChops.invert(hole_mask)))

# ---- inpaint the hole behind the hand (iterative premultiplied blur fill) ----
def box_blur(arr, r):
    out = arr.astype(np.float64)
    for axis in (0, 1):
        c = np.cumsum(out, axis=axis)
        if axis == 0:
            pad = np.zeros((1,) + c.shape[1:]); c = np.concatenate([pad, c], axis=0)
            n = c.shape[0] - 1
            hi = np.clip(np.arange(n) + r + 1, 0, n)
            lo = np.clip(np.arange(n) - r, 0, n)
            out = (c[hi] - c[lo]) / (hi - lo)[:, None, None][:, :, :out.shape[2]] if out.ndim == 3 else (c[hi] - c[lo]) / (hi - lo)[:, None]
        else:
            c = np.concatenate([np.zeros((c.shape[0], 1) + c.shape[2:]), c], axis=1)
            n = c.shape[1] - 1
            hi = np.clip(np.arange(n) + r + 1, 0, n)
            lo = np.clip(np.arange(n) - r, 0, n)
            div = (hi - lo)[None, :, None] if out.ndim == 3 else (hi - lo)[None, :]
            out = (c[:, hi] - c[:, lo]) / div
    return out

body_arr = np.asarray(body).astype(np.float64)
fill_region = (np.asarray(hole_mask) > 0) & (np.asarray(src.getchannel("A")) > 100)
work = body_arr.copy()
work[..., :3] *= work[..., 3:4] / 255.0          # premultiply
for _ in range(12):
    bl = box_blur(work, 14)
    alpha = bl[..., 3:4]
    need = fill_region & (work[..., 3] < 250)
    unpremul = np.where(alpha > 1, bl[..., :3] / np.maximum(alpha / 255.0, 1e-3), 0)
    filled = np.where(alpha[..., 0] > 1, 255.0, 0.0)
    work[need, :3] = (unpremul[need] * (filled[need] / 255.0)[:, None])
    work[need, 3] = filled[need]
work[..., :3] = np.where(work[..., 3:4] > 1, work[..., :3] / (work[..., 3:4] / 255.0), 0)
body_inpainted = Image.fromarray(np.clip(work, 0, 255).astype(np.uint8))

# ---- pose compositor ----
_cache = {}

def pose(hand_deg=0.0, bulb_scale=0.0, bulb_dy=0.0):
    key = (round(hand_deg * 2) / 2, round(bulb_scale * 20) / 20, round(bulb_dy / 3) * 3)
    if key not in _cache:
        f = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        f.alpha_composite(body_inpainted)
        hr = hand.rotate(-key[0], center=PEN_PIVOT, resample=Image.BICUBIC)
        f.alpha_composite(hr)
        bs = key[1]
        if bs > 0.02:
            bw, bh = max(4, int(W * bs)), max(4, int(H * bs))
            bl = bulb.resize((bw, bh), Image.LANCZOS)
            ox = int(BULB_ANCHOR[0] * (1 - bs))
            oy = int(BULB_ANCHOR[1] * (1 - bs) + key[2])
            f.alpha_composite(bl, (ox, oy))
        _cache[key] = f
    return _cache[key]

# ---- animation ----
FOX_H = 640            # display height of the full source frame
FOX_W = int(W * FOX_H / H)
GROUND = 668           # feet line on canvas

def ease_out_cubic(t):
    return 1 - (1 - t) ** 3

def smoothstep(t):
    return t * t * (3 - 2 * t)

frames = []

def add_frame(cx, y_off=0.0, rot=0.0, hand_deg=0.0, bulb_scale=0.0, bulb_dy=0.0):
    spr = pose(hand_deg, bulb_scale, bulb_dy).resize((FOX_W, FOX_H), Image.LANCZOS)
    if abs(rot) > 0.1:
        spr = spr.rotate(rot, resample=Image.BICUBIC, expand=True)
    canvas = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    canvas.alpha_composite(spr, (int(cx - spr.width / 2), int(GROUND - spr.height + y_off)))
    frames.append(canvas)

X_END = 480

# Phase 1: walk in from the left with a bouncy step
N1 = 30
for i in range(N1):
    t = i / (N1 - 1)
    x = -260 + (X_END + 260) * (0.15 * t + 0.85 * smoothstep(t))
    step = 2 * math.pi * 4 * t
    hop = -13 * abs(math.sin(step / 2)) * (1 if t < 0.92 else (1 - t) / 0.08 * 0 + 1)
    rock = 4.5 * math.sin(step / 2) * (1 - 0.5 * t)
    lean = -5 * (1 - smoothstep(t))
    add_frame(x, hop, rock + lean)

# settle
for i in range(4):
    t = (i + 1) / 4
    add_frame(X_END, -3 * (1 - t), 0)

# Phase 2: scribble on the memo pad
N2 = 26
for i in range(N2):
    t = i / N2
    wig = 5.0 * math.sin(2 * math.pi * 4.2 * t) * (0.75 + 0.25 * math.sin(2 * math.pi * 0.9 * t + 1))
    nod = 1.5 * math.sin(2 * math.pi * 2.1 * t)
    add_frame(X_END, nod, 0, hand_deg=wig)

# Phase 3: the idea lands — exclamation pops with a little hop
POP = [0.35, 0.7, 1.0, 1.18, 0.95, 1.05, 1.0]
for k, bs in enumerate(POP):
    hop = -10 if k in (1, 2) else (-5 if k == 3 else 0)
    add_frame(X_END, hop, 0, hand_deg=0, bulb_scale=bs)

# Phase 4: hold — bulb floats, body idles
N4 = 20
for i in range(N4):
    t = i / N4
    float_dy = 6 * math.sin(2 * math.pi * t)
    bob = 2.5 * math.sin(2 * math.pi * t + math.pi / 3)
    add_frame(X_END, bob, 0, hand_deg=0, bulb_scale=1.0, bulb_dy=float_dy)

# ---- save GIF (shared palette) and APNG ----
pal_rgb = Image.new("RGB", src.size, (255, 255, 255))
pal_rgb.paste(src, mask=src.getchannel("A"))
global_pal = pal_rgb.resize((500, 711)).quantize(colors=255)

pframes = []
for f in frames:
    alpha = f.getchannel("A")
    rgb = Image.new("RGB", f.size, (255, 255, 255))
    rgb.paste(f, mask=alpha)
    p = rgb.quantize(colors=255, palette=global_pal, dither=Image.NONE)
    p.paste(255, alpha.point(lambda v: 255 if v < 128 else 0))
    pframes.append(p)

pframes[0].save(OUT_GIF, save_all=True, append_images=pframes[1:],
                duration=FPS_MS, loop=0, transparency=255, disposal=2, optimize=False)
frames[0].save(OUT_APNG, save_all=True, append_images=frames[1:],
               duration=FPS_MS, loop=0, default_image=False)

import os
print("GIF :", os.path.getsize(OUT_GIF) // 1024, "KB,", len(frames), "frames")
print("APNG:", os.path.getsize(OUT_APNG) // 1024, "KB")
