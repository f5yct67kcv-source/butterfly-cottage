# Butterfly Cottage

Website for Butterfly Cottage, a self-catering cottage in the grounds of Garden
Park Guest House, Grantown-on-Spey.

Plain HTML, CSS and a little JavaScript. No framework, no build step for the
site itself: open `index.html` in a browser and it works. Only the photos are
generated, see below.

## Structure

```
index.html            English, the source language
de/  nl/  it/         German, Dutch, Italian
assets/site.css       all styling
assets/site.js        theme toggle, mobile menu, gallery lightbox, video
assets/photos/        the images the site serves (generated)
assets/img/           the camera originals the photos are cut from
assets/logo.svg       wordmark, used as a CSS mask so it takes the text colour
assets/favicon.svg    the butterfly on its own
grantown/             the interactive Highland map and its 24 destination photos
logo/                 brand source files (PDF, traced SVG)
build_images.py       regenerates everything in assets/photos/
apply_edits.py        a one-off content edit from an earlier round, kept as a
                      record; its paths point at a sandbox and it will not run
```

## The four languages

English is the source. When the content changes, all four files change. The
three translations follow two rules the owner asked for: Swiss spelling with
`ss` instead of `ß`, and no dashes or colons in running text.

Each page carries its own `hreflang` block and language switcher. If a page is
added or a URL changes, both have to be updated in all four files.

## Photos

`build_images.py` reads `assets/img/` and writes `assets/photos/`. It needs
Pillow:

```bash
pip3 install Pillow
python3 build_images.py
```

It produces a WebP and a JPEG fallback of every photo in two sizes, and writes
`assets/photos/sizes.json` with the real output dimensions so the HTML can
carry accurate `width`/`height`.

The hero is a special case. A single wide photo cannot serve both a desktop
band and a phone, so `HERO_CROPS` cuts the same 4:3 original twice, once wide
and once square, and the HTML picks per screen with `<picture media=...>`. The
crop boxes are pixel coordinates on the orientation-corrected original; change
them there, not in the HTML.

WebP quality is 74. At 80 the leafy autumn photos were barely smaller than
their JPEGs.

## The map

`grantown/grantown-map.html` is the interactive Highland map. It is maintained
separately in the GardenParkMap repository and copied in here; edits belong
upstream, not in this file. It needs `grantown/media/`, which holds the 24
destination photos. Leaflet and the fonts come from a CDN, everything else is
in the file.

## Deployment

Any static host works, the site has no server side. Copy the whole folder up.

The English page belongs at `/en/`, not at the root: its canonical URL and the
`hreflang` entries say `/en/`, and the live domain already redirects `/` there.

The preview at <https://f5yct67kcv-source.github.io/butterfly-cottage/> serves
the English page from the root, which is why the map's own back link points at
the old site there. On the real domain that link resolves correctly.
