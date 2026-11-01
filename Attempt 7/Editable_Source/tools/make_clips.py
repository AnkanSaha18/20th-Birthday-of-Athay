"""Writes assets/clips.html: SVG clip-path shapes (heart, blobs, torn paper,
stamp, scallop) in 0..1 units. They are pasted into magazine.html."""
import numpy as np, math
from scipy.ndimage import gaussian_filter1d
rng = np.random.default_rng(11)
def f(v): return f'{v:.4f}'
def torn(seed, amp=.012, jag=.006, m=.018, n=260):
    r = np.random.default_rng(seed)
    def e(k):
        a = gaussian_filter1d(r.normal(0, 1, k), 6); a = a / np.abs(a).max() * amp
        return a + r.uniform(0, jag, k)
    t, b, l, rr = e(n), e(n), e(n), e(n); xs = np.linspace(m, 1 - m, n)
    pts = [(x, m + t[i]) for i, x in enumerate(xs)] + [(1 - m - rr[i], y) for i, y in enumerate(xs)] + \
          [(x, 1 - m - b[i]) for i, x in enumerate(xs[::-1])] + [(m + l[i], y) for i, y in enumerate(xs[::-1])]
    return 'M' + ' L'.join(f'{f(x)},{f(y)}' for x, y in pts) + 'Z'
def stamp(n=16, r=.022):
    # perforated edge: rectangle with semicircle bites
    d = 'M0,0 '
    seg = 1 / n
    for i in range(n): d += f'L{f(i*seg+seg/2-r)},0 A{r},{r} 0 0 0 {f(i*seg+seg/2+r)},0 '
    d += 'L1,0 '
    for i in range(n): d += f'L1,{f(i*seg+seg/2-r)} A{r},{r} 0 0 0 1,{f(i*seg+seg/2+r)} '
    d += 'L1,1 '
    for i in range(n): x = 1 - (i*seg+seg/2); d += f'L{f(x+r)},1 A{r},{r} 0 0 0 {f(x-r)},1 '
    d += 'L0,1 '
    for i in range(n): y = 1 - (i*seg+seg/2); d += f'L0,{f(y+r)} A{r},{r} 0 0 0 0,{f(y-r)} '
    return d + 'Z'
def scallop(n=28):
    pts = []
    for k in range(720):
        t = k / 720 * 2 * math.pi
        rad = .47 + .03 * abs(math.cos(n / 2 * t))
        pts.append((.5 + rad * math.cos(t), .5 + rad * math.sin(t)))
    return 'M' + ' L'.join(f'{f(x)},{f(y)}' for x, y in pts) + 'Z'
def blob(seed):
    r = np.random.default_rng(seed); k = np.arange(1, 4); ph = r.uniform(0, 6.3, 3); am = r.uniform(.02, .05, 3)
    pts = []
    for i in range(360):
        t = i / 360 * 2 * math.pi; rad = .44 + sum(am[j] * math.sin(k[j] * t + ph[j]) for j in range(3))
        pts.append((.5 + rad * math.cos(t), .5 + rad * math.sin(t)))
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    sx = 1 / (max(xs) - min(xs)); sy = 1 / (max(ys) - min(ys))
    pts = [((x - min(xs)) * sx, (y - min(ys)) * sy) for x, y in pts]
    return 'M' + ' L'.join(f'{f(x)},{f(y)}' for x, y in pts) + 'Z'
heart = 'M0.5,0.18 C0.5,0.05 0.32,-0.02 0.18,0.04 C0.02,0.11 -0.03,0.32 0.06,0.5 C0.15,0.68 0.36,0.82 0.5,0.98 C0.64,0.82 0.85,0.68 0.94,0.5 C1.03,0.32 0.98,0.11 0.82,0.04 C0.68,-0.02 0.5,0.05 0.5,0.18Z'
clips = {'c-heart': heart, 'c-blob1': blob(3), 'c-blob2': blob(8), 'c-torn1': torn(1), 'c-torn2': torn(2),
         'c-stamp': stamp(), 'c-scallop': scallop()}
s = '<svg width="0" height="0" style="position:absolute"><defs>\n' + '\n'.join(
    f'<clipPath id="{k}" clipPathUnits="objectBoundingBox"><path d="{v}"/></clipPath>' for k, v in clips.items()) + '\n</defs></svg>'
open('assets/clips.html', 'w').write(s); print(len(s))
