ATHAY · THE TWENTIETH ISSUE  ·  Royal Ivory & Gold Edition  (Attempt 6 Revised)
=======================================================================
For Athay Saha's 20th birthday · 31 October 2026 · with love from Ankan Saha
8" x 11" trim, 20 pages (page 1 = front cover, page 20 = back cover with the last message).
Every page has 0.125" bleed on all sides (8.25" x 11.25") so nothing is lost when the printer trims.

PRINT_READY
  ATHAY_Birthday_Magazine_PRINT_8x11_with_bleed.pdf  -> give THIS to the print shop (600 dpi, TrimBox set)
  ATHAY_Birthday_Magazine_8x11_trimmed.pdf           -> exact 8 x 11 in (300 dpi) for screens / home printing
  JPG_600dpi/              4800 x 6600 px per page (8 x 11 in @ 600 dpi)
  JPG_300dpi/              2400 x 3300 px per page (8 x 11 in @ 300 dpi)
  JPG_600dpi_with_bleed/   4950 x 6750 px per page incl. bleed
  ATHAY_Birthday_Magazine_all_pages_preview.jpg   all 20 pages on one sheet

EDITABLE_SOURCE
  magazine.html      every word, photo and frame. Pages are marked  ===== PAGE 07 · THE MUSE =====
  styles.css         colours, fonts, frames (polaroid, film strip, camera, torn paper, stamp,
                     heart, arch, oval, flower frame, gold frame...), ambient glow
  photos/            restored copies of your photos (originals in "Images" were never touched);
                     photos/cutouts/ = background-removed versions; photo_index.csv maps names
  assets/art/        the illustrations (crowned cat, kitten on cushion, princess, teddy, crown,
                     bow, swans, butterfly, heel, rose, cake, flower frames) as editable SVG
  assets/fonts/      Bodoni Moda, Cormorant Garamond, Pinyon Script, Great Vibes, Cinzel,
                     Montserrat, Italiana, Tiro Bangla (all free / OFL)
  tools/             cutout.swift (Apple Vision background removal), make_assets.py, make_clips.py
  render.py          re-exports everything into Print_Ready

HOW TO EDIT
  Text:  open magazine.html in a text editor, change words between the tags, open the file
         in Google Chrome to see the result.
  Photo: change src="photos/p035.jpg"; object-position:50% 30% picks which part is visible
         (first % = left/right, second % = up/down). Boxes use left/top/width/height in px
         (96 px = 1 inch; page is 792 x 1080 px incl. bleed; keep text 60 px from the edges).
  New cut-out:  ./tools/cutout photos/pXXX.jpg photos/cutouts/pXXX.png

HOW TO EXPORT AGAIN (Terminal, inside Editable_Source)
  python3 render.py            everything (PDFs + 600/300 dpi JPGs + preview)
  python3 render.py proof      quick low-res check  ->  Print_Ready/proof/
  python3 render.py jpg 4 7    only pages 4 and 7
