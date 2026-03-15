#!/usr/bin/env python3
"""Export the portfolio HTML as a single tall seamless PDF."""

import argparse
import os
import re
import sys
import tempfile

import fitz  # PyMuPDF
from PIL import Image
from weasyprint import CSS, HTML

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
DEFAULT_HTML = os.path.join(PROJECT_ROOT, "public", "index.html")
DEFAULT_OUTPUT = os.path.join(PROJECT_ROOT, "public", "renders", "render.pdf")
DPI = 300

# Inject zero margins so weasyprint renders edge-to-edge;
# the HTML's own .paper padding handles internal spacing.
PAGE_CSS = """
@page { size: letter; margin: 0; }

/* Override properties that weasyprint doesn't handle well */
.progressive-img { overflow: visible !important; }
.progressive-img img {
    aspect-ratio: auto !important;
    object-fit: contain !important;
}
"""


def main():
    parser = argparse.ArgumentParser(description="Export portfolio HTML as a tall seamless PDF.")
    parser.add_argument("input", nargs="?", default=DEFAULT_HTML, help="Path to HTML file")
    parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT, help="Output PDF path")
    args = parser.parse_args()

    html_path = os.path.abspath(args.input)
    output_path = os.path.abspath(args.output)

    if not os.path.exists(html_path):
        print(f"Error: HTML file not found: {html_path}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    base_url = os.path.join(PROJECT_ROOT, "public") + os.sep

    # Step 1: Render HTML to PDF with weasyprint
    print("Rendering HTML to PDF with weasyprint...")
    temp_pdf = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    temp_pdf.close()
    try:
        # Pre-process HTML to swap thumbnail src to full-res, since
        # weasyprint doesn't execute the progressive-img.js script.
        with open(html_path) as f:
            html_text = f.read()
        html_text = re.sub(
            r'(src="images/[^"]*)/thumbnails/([^"]*?)\.jpg"',
            r'\1/\2.png"',
            html_text,
        )
        html = HTML(string=html_text, base_url=base_url)
        html.write_pdf(temp_pdf.name, stylesheets=[CSS(string=PAGE_CSS)])

        # Step 2: Convert PDF pages to PIL images at 300 DPI
        print("Converting PDF pages to images...")
        doc = fitz.open(temp_pdf.name)
        zoom = DPI / 72  # PDF default is 72 DPI
        mat = fitz.Matrix(zoom, zoom)

        page_images = []
        for page in doc:
            pix = page.get_pixmap(matrix=mat)
            img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            page_images.append(img)
        doc.close()

        if not page_images:
            print("Error: no pages rendered", file=sys.stderr)
            sys.exit(1)

        print(f"Processing {len(page_images)} pages...")

        # Step 3: Stitch page images vertically
        width = page_images[0].width
        total_height = sum(img.height for img in page_images)
        result = Image.new("RGB", (width, total_height), (255, 255, 255))
        y_offset = 0
        for img in page_images:
            result.paste(img, (0, y_offset))
            y_offset += img.height

        # Step 4: Save as PDF at 300 DPI
        print(f"Saving to {output_path}")
        result.save(output_path, "PDF", resolution=DPI)

        for img in page_images:
            img.close()
        result.close()

    finally:
        os.unlink(temp_pdf.name)

    print("Done!")


if __name__ == "__main__":
    main()
