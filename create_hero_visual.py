from PIL import Image, ImageDraw, ImageFilter
import math
import random


WIDTH = 1800
HEIGHT = 1120
random.seed(20260529)

rose = (246, 222, 227)
mint = (216, 235, 217)
paper = (255, 250, 244)
ink = (39, 51, 43)
moss = (57, 104, 77)
plum = (107, 63, 88)
gold = (194, 148, 78)

img = Image.new("RGB", (WIDTH, HEIGHT), rose)
px = img.load()

for y in range(HEIGHT):
    t = y / (HEIGHT - 1)
    for x in range(WIDTH):
        s = x / (WIDTH - 1)
        r = int(rose[0] * (1 - t) + mint[0] * t)
        g = int(rose[1] * (1 - t) + mint[1] * t)
        b = int(rose[2] * (1 - t) + mint[2] * t)
        r = int(r * (0.94 + 0.06 * s) + paper[0] * 0.05)
        g = int(g * (0.95 + 0.05 * (1 - s)) + paper[1] * 0.04)
        b = int(b * (0.96 + 0.04 * s) + paper[2] * 0.03)
        noise = random.randint(-4, 4)
        px[x, y] = (max(0, min(255, r + noise)), max(0, min(255, g + noise)), max(0, min(255, b + noise)))

overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

# Long paper-like planes and map lines create an academic/city-research mood
# without implying a portrait that was not provided.
draw.polygon(
    [(820, 120), (1710, 36), (1805, 986), (990, 1054)],
    fill=(255, 250, 244, 104),
)
draw.polygon(
    [(1030, 190), (1690, 130), (1760, 840), (1108, 920)],
    outline=(107, 63, 88, 46),
    width=3,
)

for i in range(22):
    x0 = 920 + i * 42 + random.randint(-20, 22)
    y0 = 155 + random.randint(-55, 80)
    x1 = x0 + random.randint(90, 300)
    y1 = min(990, y0 + random.randint(340, 780))
    draw.line([(x0, y0), (x1, y1)], fill=(57, 104, 77, 55), width=random.choice([2, 3, 4]))

for i in range(18):
    y = 230 + i * 42 + random.randint(-15, 18)
    draw.line([(890, y), (1760, y + random.randint(-90, 95))], fill=(107, 63, 88, 35), width=2)

for i in range(90):
    x = random.randint(950, 1740)
    y = random.randint(180, 950)
    radius = random.choice([3, 4, 5, 6])
    color = random.choice([(57, 104, 77, 115), (107, 63, 88, 112), (194, 148, 78, 130)])
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)

chart = []
for i in range(0, 760, 20):
    x = 930 + i
    y = 785 - 120 * math.sin(i / 95) - 0.22 * i + random.randint(-8, 8)
    chart.append((x, y))
draw.line(chart, fill=(107, 63, 88, 152), width=6, joint="curve")
for x, y in chart[::5]:
    draw.ellipse((x - 7, y - 7, x + 7, y + 7), fill=(255, 250, 244, 210), outline=(107, 63, 88, 165), width=3)

for i in range(7):
    x = 1070 + i * 86
    h = random.randint(120, 330)
    draw.rounded_rectangle((x, 860 - h, x + 34, 860), radius=5, fill=(57, 104, 77, 88))

for i in range(34):
    x0 = random.randint(0, 560)
    y0 = random.randint(80, 1040)
    length = random.randint(260, 560)
    color = random.choice([(255, 250, 244, 74), (57, 104, 77, 36), (107, 63, 88, 31)])
    draw.line([(x0, y0), (x0 + length, y0 + random.randint(-40, 58))], fill=color, width=random.choice([2, 3, 4]))

for i in range(13):
    x = random.randint(60, 660)
    y = random.randint(120, 940)
    w = random.randint(74, 190)
    h = random.randint(26, 82)
    draw.rounded_rectangle((x, y, x + w, y + h), radius=8, outline=(39, 51, 43, 31), width=2)

for i in range(9):
    x = 115 + i * 67
    y = 920 - i * random.randint(15, 25)
    draw.line([(x, 980), (x, y)], fill=(194, 148, 78, 91), width=10)
    draw.line([(x, y), (x + 46, y - random.randint(20, 54))], fill=(194, 148, 78, 91), width=10)

overlay = overlay.filter(ImageFilter.GaussianBlur(0.3))
img = Image.alpha_composite(img.convert("RGBA"), overlay)

vignette = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
vd = ImageDraw.Draw(vignette)
for i in range(160):
    alpha = int(82 * (i / 159) ** 2)
    vd.rectangle((i, i, WIDTH - i, HEIGHT - i), outline=(255, 250, 244, max(0, 24 - alpha // 6)), width=1)
    vd.rectangle((0, 0, WIDTH, HEIGHT), outline=(39, 51, 43, 0), width=1)
img = Image.alpha_composite(img, vignette)

img = img.convert("RGB")
img.save("assets/hero-research-landscape.png", quality=94)
