# Athay · The Twentieth Issue (website edition)

A scrolling, animated version of the birthday magazine for Athay's 20th birthday (31 · 10 · 2026),
made with love by Ankan. Plain HTML, CSS and JavaScript: no build step, no libraries, no server code.

## What's inside

```
index.html        every word and photo, section by section (look for the ===== comments)
css/style.css     colours, fonts, frames and all animations
js/main.js        sparkles, counter, camera, 20 reasons, chat, envelope, hold-my-hand finale, lightbox
photos/           web-sized copies of the restored photos (originals were never touched)
photos/cut/       background-removed cut-outs
assets/fonts/     Bodoni Moda, Cormorant Garamond, Great Vibes, Pinyon Script, Cinzel, Montserrat, Tiro Bangla (OFL)
assets/art/       crown, cat, princess, teddy, flower frames… (SVG)
assets/music.m4a  the music-box birthday waltz (tools/make_music.py rebuilds it)
magazine.html     page-turning magazine reader; magazine/ holds its pages and the screen PDF
```

## Preview on your Mac

Double-clicking `index.html` works, but a tiny local server behaves exactly like the real site:

```bash
cd ~/Desktop/Anno/Birthday/Website && python3 -m http.server 8000
```

Then open http://localhost:8000 in Chrome or Safari (and on your phone, via your Mac's IP, if you like).

## Music

`assets/music.m4a` is an original music-box waltz composed for the site: a romantic intro, "Happy Birthday",
a love theme, and "Happy Birthday" again, about 1:41 on a loop. It fades in when she taps the wax seal,
pauses when she leaves the tab, and the gold button bottom-left turns it off and on.
To use your own song instead, save it as `assets/music.m4a` (or change `src` on the `<audio>` tag in `index.html`).
To regenerate the track: `python3 tools/make_music.py`.

## Editing

- Words: search `index.html` for the sentence and change it.
- A photo: change `src="photos/p035.jpg"`. `object-position:50% 30%` picks which part shows
  (first % = left/right, second % = up/down).
- The 20 reasons and the "Every moment" photo rows live at the top of `js/main.js`.

## Sections

Seal → Cover → Twenty years (live counter) → Editor's letter → Chapter One: The Cover Star, Little Athay,
Loved First, The Muse, Colours of Her, Grace, the Centrefold, Glow (live camera), Her Royal Softness →
Chapter Two: How it began, Date Night Diaries, 20 Reasons (flip cards), Just Us (photobooth) →
Chapter Three: The Little Things (love-language chat), Sealed with a Kiss, the Love Letter (envelope) →
Every Moment → Don't Let Go (press & hold the heart).

Everything respects "Reduce motion" on iPhone/Mac, and every photo opens full-screen with a tap.

Hosting: see HOSTING.md in the Birthday folder (one level up).
