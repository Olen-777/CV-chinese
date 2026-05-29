from PIL import Image, ImageDraw, ImageFilter
import math
import random


WIDTH = 1800
HEIGHT = 1120
random.seed(20260529)

paper = (255, 250, 244)
rose = (247, 224, 229)
mint = (218, 238, 219)
water = (198, 222, 226)
blue = (166, 199, 213)
lavender = (183, 167, 204)
leaf = (79, 129, 97)
deep_leaf = (48, 97, 78)
plum = (109, 64, 91)
gold = (194, 151, 82)


def lerp(a, b, t):
    return int(a * (1 - t) + b * t)


def mix(c1, c2, t):
    return tuple(lerp(c1[i], c2[i], t) for i in range(3))


img = Image.new("RGB", (WIDTH, HEIGHT), paper)
px = img.load()

for y in range(HEIGHT):
    v = y / (HEIGHT - 1)
    for x in range(WIDTH):
        u = x / (WIDTH - 1)
        base = mix(rose, mint, 0.45 + 0.4 * v)
        cool = mix(base, water, 0.2 + 0.18 * math.sin((u * 2.8 + v * 1.4) * math.pi))
        warm = mix(cool, paper, 0.18 + 0.2 * (1 - u))
        noise = random.randint(-4, 4)
        px[x, y] = tuple(max(0, min(255, channel + noise)) for channel in warm)

strokes = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
draw = ImageDraw.Draw(strokes, "RGBA")

# Broad water movement: short translucent strokes, intentionally soft and painterly.
stroke_palette = [
    (*blue, 68),
    (*mint, 74),
    (*lavender, 48),
    (*rose, 54),
    (245, 246, 228, 58),
    (126, 166, 158, 38),
]

for _ in range(820):
    x = random.randint(-80, WIDTH + 60)
    y = random.randint(70, HEIGHT - 40)
    length = random.randint(34, 220)
    angle = random.uniform(-0.2, 0.18)
    color = random.choice(stroke_palette)
    width = random.choice([5, 7, 9, 12, 15])
    x2 = x + int(length * math.cos(angle))
    y2 = y + int(length * math.sin(angle))
    draw.line((x, y, x2, y2), fill=color, width=width)
    r = width // 2
    draw.ellipse((x - r, y - r, x + r, y + r), fill=color)
    draw.ellipse((x2 - r, y2 - r, x2 + r, y2 + r), fill=color)

# A few softly reflected willow-like verticals, abstracted so they do not read as data lines.
for _ in range(28):
    x = random.randint(760, WIDTH + 140)
    y0 = random.randint(-80, 220)
    length = random.randint(360, 940)
    sway = random.randint(-55, 70)
    color = random.choice([(68, 111, 96, 36), (112, 98, 135, 28), (94, 139, 126, 30)])
    points = []
    for i in range(8):
        t = i / 7
        points.append((x + int(sway * math.sin(t * math.pi)) + random.randint(-12, 12), y0 + int(length * t)))
    draw.line(points, fill=color, width=random.choice([3, 4, 5]))


def lily_pad(cx, cy, scale, rotation, alpha=125):
    rx = int(72 * scale)
    ry = int(42 * scale)
    pad = Image.new("RGBA", (rx * 3, ry * 3), (0, 0, 0, 0))
    pd = ImageDraw.Draw(pad, "RGBA")
    ox = rx * 3 // 2
    oy = ry * 3 // 2
    body = random.choice([leaf, deep_leaf, (96, 147, 104), (111, 151, 118)])
    pd.ellipse((ox - rx, oy - ry, ox + rx, oy + ry), fill=(*body, alpha))
    pd.pieslice((ox - rx, oy - ry, ox + rx, oy + ry), start=308, end=26, fill=(0, 0, 0, 0))
    pd.arc((ox - rx + 10, oy - ry + 8, ox + rx - 16, oy + ry - 8), 192, 346, fill=(236, 241, 213, 52), width=2)
    for vein in range(5):
        a = rotation + random.uniform(-0.9, 0.8) + vein * 0.22
        pd.line((ox, oy, ox + int(rx * 0.75 * math.cos(a)), oy + int(ry * 0.8 * math.sin(a))), fill=(230, 241, 215, 34), width=2)
    pad = pad.rotate(math.degrees(rotation), resample=Image.Resampling.BICUBIC, expand=True)
    strokes.alpha_composite(pad, (int(cx - pad.width / 2), int(cy - pad.height / 2)))


def flower(cx, cy, scale, rotation=0):
    flower_layer = Image.new("RGBA", (220, 220), (0, 0, 0, 0))
    fd = ImageDraw.Draw(flower_layer, "RGBA")
    ox = oy = 110
    petal_count = 11
    for ring, alpha in [(0, 150), (1, 112)]:
        for i in range(petal_count):
            a = rotation + i * 2 * math.pi / petal_count + ring * 0.12
            px = ox + int(math.cos(a) * 20 * scale)
            py = oy + int(math.sin(a) * 13 * scale)
            w = int((16 + ring * 4) * scale)
            h = int((42 - ring * 4) * scale)
            petal = Image.new("RGBA", (w * 4, h * 4), (0, 0, 0, 0))
            pdraw = ImageDraw.Draw(petal, "RGBA")
            pdraw.ellipse((w, h // 2, w * 3, h * 3), fill=(255, 244, 247, alpha), outline=(197, 141, 168, 54), width=1)
            petal = petal.rotate(math.degrees(a) + 90, resample=Image.Resampling.BICUBIC, expand=True)
            flower_layer.alpha_composite(petal, (int(px - petal.width / 2), int(py - petal.height / 2)))
    fd.ellipse((ox - 9, oy - 7, ox + 10, oy + 8), fill=(*gold, 170))
    flower_layer = flower_layer.filter(ImageFilter.GaussianBlur(0.25))
    strokes.alpha_composite(flower_layer, (int(cx - 110), int(cy - 110)))


# Keep the left text area calm; concentrate lilies toward the right and lower field.
for _ in range(46):
    cx = random.randint(850, WIDTH - 70)
    cy = random.randint(250, HEIGHT - 80)
    lily_pad(cx, cy, random.uniform(0.42, 0.95), random.uniform(-0.5, 0.5), alpha=random.randint(78, 140))

for _ in range(16):
    cx = random.randint(900, WIDTH - 90)
    cy = random.randint(300, HEIGHT - 120)
    flower(cx, cy, random.uniform(0.55, 1.05), random.uniform(0, math.pi))

# Add a few distant pads on the center so the image feels continuous.
for _ in range(14):
    lily_pad(random.randint(560, 980), random.randint(300, HEIGHT - 120), random.uniform(0.26, 0.55), random.uniform(-0.4, 0.5), alpha=random.randint(45, 85))

strokes = strokes.filter(ImageFilter.GaussianBlur(0.22))
img = Image.alpha_composite(img.convert("RGBA"), strokes)

# Soft light veil at left for copy readability, integrated into the artwork itself.
veil = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
vd = ImageDraw.Draw(veil, "RGBA")
vd.rectangle((0, 0, 780, HEIGHT), fill=(255, 250, 244, 82))
for x in range(780, 1200):
    alpha = int(82 * (1 - (x - 780) / 420) ** 2)
    vd.line((x, 0, x, HEIGHT), fill=(255, 250, 244, alpha))
img = Image.alpha_composite(img, veil)

img = img.filter(ImageFilter.GaussianBlur(0.15)).convert("RGB")
img.save("assets/hero-water-lilies.png", quality=94)
