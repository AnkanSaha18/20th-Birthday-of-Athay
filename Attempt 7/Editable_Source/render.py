"""
Export the magazine after editing magazine.html / styles.css / photos.

  python3 render.py              -> everything: print PDF (with bleed), trimmed PDF,
                                    600 dpi + 300 dpi JPGs, preview sheet
  python3 render.py proof        -> quick low-res check of all pages (exports/proof/)
  python3 render.py proof 4 7    -> quick check of pages 4 and 7 only
  python3 render.py jpg 4 7      -> re-export only pages 4 and 7 (600 + 300 dpi JPGs)

Needs:  pip3 install playwright pillow      (uses your installed Google Chrome)
"""
import sys, asyncio, pathlib
from playwright.async_api import async_playwright
from PIL import Image
from make_pdf import jpegs_to_pdf

Image.MAX_IMAGE_PIXELS = None
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / 'Print_Ready'
PAGES = 20
W, H = 792, 1080      # css px incl. bleed (8.25 x 11.25 in @ 96 px/in)
BLEED = 12            # css px = 0.125 in
NAME = 'ATHAY_Birthday_Magazine'


async def shoot(pages, scale, folder):
    folder.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        try:
            b = await p.chromium.launch(channel='chrome')
        except Exception:
            b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width': W, 'height': H}, device_scale_factor=scale)
        pg = await ctx.new_page()
        for n in pages:
            await pg.goto((HERE / 'magazine.html').as_uri() + f'?p={n}')
            await pg.evaluate("""async () => { await document.fonts.ready;
                await Promise.all([...document.images].map(i => i.decode().catch(() => {})));
                await new Promise(r => setTimeout(r, 500)); }""")
            await pg.screenshot(path=str(folder / f'page_{n:02d}.png'), clip={'x': 0, 'y': 0, 'width': W, 'height': H})
            print('rendered page', n, flush=True)
        await b.close()


def finish(pages, src):
    d600 = OUT / 'JPG_600dpi'; d300 = OUT / 'JPG_300dpi'; dB = OUT / 'JPG_600dpi_with_bleed'
    for d in (d600, d300, dB):
        d.mkdir(parents=True, exist_ok=True)
    for n in pages:
        im = Image.open(src / f'page_{n:02d}.png').convert('RGB')           # 4950 x 6750 px
        im.save(dB / f'{NAME}_Page_{n:02d}_bleed_600dpi.jpg', quality=95, dpi=(600, 600), subsampling=0)
        b = round(BLEED * im.width / W)
        t = im.crop((b, b, im.width - b, im.height - b))                    # 4800 x 6600 px = 8 x 11 in
        t.save(d600 / f'{NAME}_Page_{n:02d}_600dpi.jpg', quality=95, dpi=(600, 600), subsampling=0)
        t.resize((2400, 3300), Image.Resampling.LANCZOS).save(d300 / f'{NAME}_Page_{n:02d}_300dpi.jpg', quality=95, dpi=(300, 300), subsampling=0)
        (src / f'page_{n:02d}.png').unlink()


def pdfs():
    dB = OUT / 'JPG_600dpi_with_bleed'; d300 = OUT / 'JPG_300dpi'
    jpegs_to_pdf([str(dB / f'{NAME}_Page_{n:02d}_bleed_600dpi.jpg') for n in range(1, PAGES + 1)],
                 str(OUT / f'{NAME}_PRINT_8x11_with_bleed.pdf'), 600, 0.125,
                 title='ATHAY - The Twentieth Issue (print, 0.125 in bleed)')
    jpegs_to_pdf([str(d300 / f'{NAME}_Page_{n:02d}_300dpi.jpg') for n in range(1, PAGES + 1)],
                 str(OUT / f'{NAME}_8x11_trimmed.pdf'), 300, title='ATHAY - The Twentieth Issue')


def sheet(folder, pattern, out):
    tw, th, g = 400, 550, 24
    s = Image.new('RGB', (5 * tw + 6 * g, 4 * th + 5 * g), (226, 221, 213))
    for n in range(1, PAGES + 1):
        f = folder / pattern.format(n=n)
        if not f.exists():
            continue
        im = Image.open(f).convert('RGB').resize((tw, th), Image.Resampling.LANCZOS)
        i = n - 1
        s.paste(im, (g + (i % 5) * (tw + g), g + (i // 5) * (th + g)))
    s.save(out, quality=90)


if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'proof':
        pages = [int(x) for x in a[1:]] or list(range(1, PAGES + 1))
        asyncio.run(shoot(pages, 1.5, OUT / 'proof'))
        sheet(OUT / 'proof', 'page_{n:02d}.png', OUT / 'proof' / 'all_pages.jpg')
    elif a and a[0] == 'jpg':
        pages = [int(x) for x in a[1:]] or list(range(1, PAGES + 1))
        asyncio.run(shoot(pages, 600 / 96, OUT / '_raw')); finish(pages, OUT / '_raw')
    else:
        pages = list(range(1, PAGES + 1))
        asyncio.run(shoot(pages, 600 / 96, OUT / '_raw')); finish(pages, OUT / '_raw'); pdfs()
        sheet(OUT / 'JPG_300dpi', NAME + '_Page_{n:02d}_300dpi.jpg', OUT / f'{NAME}_all_pages_preview.jpg')
        print('done ->', OUT)
