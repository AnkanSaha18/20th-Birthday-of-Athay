"""Generates the decorative masks and the flower frame used by the magazine.
   python3 tools/make_assets.py"""
import numpy as np, math, random
from PIL import Image, ImageDraw, ImageFilter
from scipy.ndimage import gaussian_filter1d
OUT = 'assets/masks/'
rng = np.random.default_rng(7)

def edge(n, amp, smooth, jag):
    a = gaussian_filter1d(rng.normal(0, 1, n), smooth); a = a / (np.abs(a).max() + 1e-9) * amp
    return a + rng.uniform(0, jag, n)

def torn(w, h, name, m=26, amp=12, jag=6, smooth=18):
    """paper torn on all four sides: alpha mask"""
    top = m + edge(w, amp, smooth, jag); bot = h - m - edge(w, amp, smooth, jag)
    lef = m + edge(h, amp, smooth, jag); rig = w - m - edge(h, amp, smooth, jag)
    pts = [(x, top[x]) for x in range(w)] + [(rig[y], y) for y in range(h)] + \
          [(x, bot[x]) for x in range(w - 1, -1, -1)] + [(lef[y], y) for y in range(h - 1, -1, -1)]
    # clamp polygon to the inner box so corners stay clean
    pts = [(min(max(x, lef[int(min(max(y,0),h-1))]), rig[int(min(max(y,0),h-1))]), min(max(y, top[int(min(max(x,0),w-1))]), bot[int(min(max(x,0),w-1))])) for x, y in pts]
    im = Image.new('L', (w * 2, h * 2), 0)
    ImageDraw.Draw(im).polygon([(x * 2, y * 2) for x, y in pts], fill=255)
    im = im.resize((w, h), Image.LANCZOS)
    Image.merge('RGBA', (im, im, im, im)).save(OUT + name)

def deckle(w, h, name, m=40):
    """soft dreamy brush edge (ambient fade)"""
    im = Image.new('L', (w, h), 0); d = ImageDraw.Draw(im)
    d.rounded_rectangle((m, m, w - m, h - m), radius=m, fill=255)
    noise = (rng.random((h // 8, w // 8)) * 255).astype('uint8')
    nz = Image.fromarray(noise).resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(6))
    im = im.filter(ImageFilter.GaussianBlur(m * 0.6))
    a = np.asarray(im, float) / 255; n = np.asarray(nz, float) / 255
    a = np.clip((a - 0.25 * (1 - a) * n) * 1.15, 0, 1)
    g = (a * 255).astype('uint8'); g = Image.fromarray(g)
    Image.merge('RGBA', (g, g, g, g)).save(OUT + name)

torn(1000, 1250, 'torn_portrait.png'); torn(1250, 1000, 'torn_land.png'); torn(1100, 1100, 'torn_square.png')
deckle(1000, 1250, 'soft_portrait.png', 70); deckle(1250, 1000, 'soft_land.png', 70)

# ---------- flower wreath frame (SVG) ----------
GOLD = '#B08A3E'; BL1 = '#F4D5D3'; BL2 = '#E9B9B8'; IV = '#FFF9F2'
def rose(cx, cy, r, rot, col=BL1, col2=BL2):
    s = [f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({rot:.0f})">']
    for k in range(7):
        a = k * 2 * math.pi / 7
        px, py = math.cos(a) * r * .55, math.sin(a) * r * .55
        s.append(f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{r*.55:.1f}" ry="{r*.42:.1f}" transform="rotate({math.degrees(a):.0f} {px:.1f} {py:.1f})" fill="{col}" stroke="{GOLD}" stroke-width="{r*.05:.2f}"/>')
    s.append(f'<circle r="{r*.62:.1f}" fill="{col2}" stroke="{GOLD}" stroke-width="{r*.05:.2f}"/>')
    # inner cupped petals (three nested arcs) and a bud centre
    for k, (rr, rot) in enumerate([(.5, 20), (.36, 150), (.22, 280)]):
        a0 = math.radians(rot); a1 = a0 + math.radians(230)
        x0, y0, x1, y1 = math.cos(a0)*r*rr, math.sin(a0)*r*rr, math.cos(a1)*r*rr, math.sin(a1)*r*rr
        s.append(f'<path d="M{x0:.1f},{y0:.1f} A{r*rr:.1f},{r*rr:.1f} 0 1 1 {x1:.1f},{y1:.1f}" fill="{col if k%2 else col2}" fill-opacity=".9" stroke="{GOLD}" stroke-width="{r*.045:.2f}" stroke-linecap="round"/>')
    s.append(f'<ellipse rx="{r*.12:.1f}" ry="{r*.09:.1f}" fill="#D98E98" stroke="{GOLD}" stroke-width="{r*.035:.2f}"/>')
    s.append('</g>'); return ''.join(s)

def leaf(cx, cy, L, ang, fill='#F7EEDC'):
    return (f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({ang:.0f})"><path d="M0,0 C{L*.3:.1f},{-L*.32:.1f} {L*.75:.1f},{-L*.25:.1f} {L:.1f},0 C{L*.75:.1f},{L*.25:.1f} {L*.3:.1f},{L*.32:.1f} 0,0Z" '
            f'fill="{fill}" stroke="{GOLD}" stroke-width="1.6"/><path d="M0,0 L{L*.85:.1f},0" stroke="{GOLD}" stroke-width="1.1"/></g>')

def bud(cx, cy, r, ang):
    return (f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({ang:.0f})"><path d="M0,{-r} C{r*.9},{-r*.6} {r*.8},{r*.5} 0,{r} C{-r*.8},{r*.5} {-r*.9},{-r*.6} 0,{-r}Z" fill="{BL2}" stroke="{GOLD}" stroke-width="1.4"/>'
            f'<path d="M{-r*.6},{r*.4} Q0,{r*1.6} {r*.6},{r*.4}" fill="#F7EEDC" stroke="{GOLD}" stroke-width="1.4"/></g>')

def wreath(W, H, name, density=1.0, seed=3):
    random.seed(seed)
    cx, cy, rx, ry = W / 2, H / 2, W / 2 - 70, H / 2 - 70
    parts_back, parts_front = [], []
    # thin gold vine ring
    parts_back.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{GOLD}" stroke-width="3"/>')
    parts_back.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx-14}" ry="{ry-14}" fill="none" stroke="{GOLD}" stroke-width="1.2" stroke-dasharray="2 7" stroke-linecap="round"/>')
    n = int(90 * density)
    for i in range(n):
        t = i / n * 2 * math.pi
        x, y = cx + rx * math.cos(t), cy + ry * math.sin(t)
        tang = math.degrees(math.atan2(ry * math.cos(t), -rx * math.sin(t)))
        # leaves cluster: more at bottom-left and top-right
        w = 0.55 + 0.45 * math.cos(t - math.radians(135)) ** 2
        if random.random() < w:
            parts_back.append(leaf(x, y, random.uniform(34, 56), tang + random.choice([-50, 50, 130, -130]) + random.uniform(-20, 20)))
    # roses at two clusters + accents
    for t0, big in [(135, 1), (-45, 1), (250, .55), (20, .5), (95, .45), (190, .45)]:
        for j, off in enumerate([-17, 0, 17] if big == 1 else [0]):
            t = math.radians(t0 + off)
            x, y = cx + rx * math.cos(t), cy + ry * math.sin(t)
            r = (58 if j == 1 else 42) * (1 if big == 1 else 1) * (big if big < 1 else 1) + 4
            parts_front.append(rose(x, y, r, random.uniform(0, 360), BL1 if j != 1 else '#F9E3E1'))
        t = math.radians(t0 + 26); parts_front.append(bud(cx + rx * math.cos(t), cy + ry * math.sin(t), 13, t0 + 116))
        t = math.radians(t0 - 26); parts_front.append(bud(cx + rx * math.cos(t), cy + ry * math.sin(t), 11, t0 - 64))
    # gold pearls
    for i in range(40):
        t = random.uniform(0, 2 * math.pi); d = random.uniform(-30, 30)
        parts_front.append(f'<circle cx="{cx+(rx+d)*math.cos(t):.1f}" cy="{cy+(ry+d)*math.sin(t):.1f}" r="{random.uniform(2.5,5):.1f}" fill="#FFFDF8" stroke="{GOLD}" stroke-width="1.2"/>')
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{"".join(parts_back)}{"".join(parts_front)}</svg>'
    open('assets/art/' + name, 'w').write(svg)

wreath(700, 900, 'flower_frame_oval.svg')
wreath(800, 800, 'flower_frame_round.svg', seed=5)
print('assets done')
