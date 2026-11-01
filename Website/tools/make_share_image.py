"""Builds the link-preview image (assets/og-image.jpg) and the icons. macOS fonts. Run from Website/."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

F = '/System/Library/Fonts/Supplemental/'
didot = lambda s: ImageFont.truetype(F + 'Didot.ttc', s)
snell = lambda s: ImageFont.truetype(F + 'SnellRoundhand.ttc', s, index=1)
NIGHT, GOLD, GOLDHI, IVORY = (20, 24, 43), (214, 175, 96), (243, 221, 160), (245, 236, 220)

W, H = 1200, 630
img = Image.new('RGB', (W, H), NIGHT)
glow = Image.new('L', (W, H), 0)
ImageDraw.Draw(glow).ellipse((380, -200, 1300, 700), fill=110)
img = Image.composite(Image.new('RGB', (W, H), (52, 58, 100)), img, glow.filter(ImageFilter.GaussianBlur(160)))
cov = ImageOps.fit(Image.open('photos/cover.jpg'), (430, 630), centering=(0.5, 0.3))
fade = Image.linear_gradient('L').rotate(-90).resize((430, 630)).point(lambda v: 255 if v > 90 else int(v * 255 / 90))
img.paste(cov, (0, 0), fade)
d = ImageDraw.Draw(img)

def ctext(y, txt, font, fill, x0=470, x1=1160):
    d.text((x0 + (x1 - x0 - d.textlength(txt, font=font)) / 2, y), txt, font=font, fill=fill)

ctext(70, 'T H E   T W E N T I E T H   I S S U E', didot(22), GOLD)
ctext(124, '20th Birthday of', didot(74), IVORY)
ctext(205, 'Athay', snell(150), GOLDHI)
d.line((715, 415, 915, 415), fill=GOLD, width=2)
ctext(440, '“No matter what happens,', didot(34), IVORY)
ctext(484, 'please don’t let go of my hand.”', didot(34), IVORY)
ctext(556, 'with love, Ankan  ·  31 · 10 · 2026', didot(22), GOLD)
img.save('assets/og-image.jpg', quality=88)

def icon(sz):
    im = Image.new('RGBA', (sz * 4, sz * 4), (0, 0, 0, 0))
    dd = ImageDraw.Draw(im)
    dd.ellipse((0, 0, sz * 4 - 1, sz * 4 - 1), fill=NIGHT + (255,), outline=GOLD + (255,), width=max(4, sz // 8))
    f = snell(int(sz * 3.1)); bb = dd.textbbox((0, 0), 'A', font=f)
    dd.text(((sz * 4 - (bb[2] - bb[0])) / 2 - bb[0], (sz * 4 - (bb[3] - bb[1])) / 2 - bb[1]), 'A', font=f, fill=GOLDHI + (255,))
    return im.resize((sz, sz), Image.LANCZOS)

icon(32).save('assets/favicon-32.png')
icon(180).save('assets/apple-touch-icon.png')
icon(512).save('assets/icon-512.png')
icon(48).save('favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])
