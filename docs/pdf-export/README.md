# PDF Export

Exports the portfolio HTML as a single tall seamless PDF using weasyprint for HTML→PDF rendering, PyMuPDF for page rasterization, and Pillow for stitching.

## Dependencies

```bash
pip install weasyprint PyMuPDF Pillow
```

## Usage

```bash
python3 main.py                          # defaults: ../../public/index.html → renders/Andrew Cromar's Portfolio.pdf
python3 main.py path/to/page.html -o out.pdf
```

## How it works

1. **Thumbnail → full-res swap** — The HTML uses thumbnail JPGs that get swapped to full-res PNGs by `progressive-img.js` at runtime. Since weasyprint doesn't execute JavaScript, `main.py` does a regex replacement on the HTML to rewrite `images/*/thumbnails/*.jpg` paths to `images/*/*.png` before rendering.

2. **CSS overrides** — `photo-collage.css` sets `aspect-ratio: 4/3` and `object-fit: cover` with `overflow: hidden`, which crops 16:9 images. The script injects `!important` overrides to use `aspect-ratio: auto`, `object-fit: contain`, and `overflow: visible` so images render fully.

3. **Stitching** — Weasyprint renders to a multi-page letter-size PDF. PyMuPDF rasterizes each page at 300 DPI, then Pillow stitches them vertically into a single tall image saved as a one-page PDF.
