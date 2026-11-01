"""
Build a PDF from finished page JPGs WITHOUT re-compressing them (the JPEG
data is embedded byte-for-byte, so the PDF is exactly as sharp as the JPGs).

  python3 make_pdf.py OUT.pdf DPI [TRIM_INCHES] page1.jpg page2.jpg ...

TRIM_INCHES (optional, e.g. 0.125) sets a TrimBox that far inside every edge
(used for the print file with bleed).  Only needs Pillow.
"""
import sys
from PIL import Image


def jpegs_to_pdf(files, out, dpi, trim_in=0.0, title='ATHAY — The Birthday Issue', author='Ankan Saha'):
    objs = []                                   # list of bytes, object n = index+1

    def add(b):
        objs.append(b)
        return len(objs)

    def esc(s):
        return s.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')

    catalog = add(b'')                          # placeholders, filled later
    pages = add(b'')
    kids = []
    for f in files:
        with Image.open(f) as im:
            w, h = im.size
            cs = {'RGB': '/DeviceRGB', 'L': '/DeviceGray', 'CMYK': '/DeviceCMYK'}[im.mode]
        data = open(f, 'rb').read()
        img = add(b'<< /Type /XObject /Subtype /Image /Width %d /Height %d /ColorSpace %s /BitsPerComponent 8 '
                  b'/Filter /DCTDecode /Length %d >>\nstream\n' % (w, h, cs.encode(), len(data)) + data + b'\nendstream')
        pw, ph = w * 72.0 / dpi, h * 72.0 / dpi
        content = b'q %.4f 0 0 %.4f 0 0 cm /Im0 Do Q' % (pw, ph)
        cobj = add(b'<< /Length %d >>\nstream\n' % len(content) + content + b'\nendstream')
        t = trim_in * 72.0
        boxes = b''
        if t:
            boxes = b' /BleedBox [0 0 %.4f %.4f] /TrimBox [%.4f %.4f %.4f %.4f]' % (pw, ph, t, t, pw - t, ph - t)
        kids.append(add(b'<< /Type /Page /Parent %d 0 R /MediaBox [0 0 %.4f %.4f]%s /Resources << /XObject << /Im0 %d 0 R >> >> /Contents %d 0 R >>'
                        % (pages, pw, ph, boxes, img, cobj)))
    objs[pages - 1] = b'<< /Type /Pages /Count %d /Kids [%s] >>' % (len(kids), b' '.join(b'%d 0 R' % k for k in kids))
    objs[catalog - 1] = b'<< /Type /Catalog /Pages %d 0 R >>' % pages
    info = add(('<< /Title (%s) /Author (%s) /Producer (ATHAY magazine) >>' % (esc(title), esc(author))).encode('latin-1', 'replace'))

    with open(out, 'wb') as fh:
        fh.write(b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n')
        offs = []
        for i, b in enumerate(objs, 1):
            offs.append(fh.tell())
            fh.write(b'%d 0 obj\n' % i + b + b'\nendobj\n')
        x = fh.tell()
        fh.write(b'xref\n0 %d\n0000000000 65535 f \n' % (len(objs) + 1))
        for o in offs:
            fh.write(b'%010d 00000 n \n' % o)
        fh.write(b'trailer\n<< /Size %d /Root %d 0 R /Info %d 0 R >>\nstartxref\n%d\n%%%%EOF\n' % (len(objs) + 1, catalog, info, x))


if __name__ == '__main__':
    out, dpi = sys.argv[1], float(sys.argv[2])
    rest = sys.argv[3:]
    trim = 0.0
    if rest and not rest[0].lower().endswith(('.jpg', '.jpeg')):
        trim = float(rest[0]); rest = rest[1:]
    jpegs_to_pdf(rest, out, dpi, trim)
    print('wrote', out, len(rest), 'pages')
