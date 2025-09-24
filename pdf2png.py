#!/usr/bin/env python3
"""Convert a scanned PDF into lossless per-page PNG images."""

import argparse
import sys
from pathlib import Path
from typing import Iterable

import pikepdf
from pikepdf import PdfImage
from PIL import Image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Convert each page of a scanned PDF into a lossless PNG file. "
            "The output files are named with a page number suffix."
        )
    )
    parser.add_argument(
        "pdf_path",
        type=Path,
        help="Path to the input PDF file (must be a scanned document).",
    )
    parser.add_argument(
        "output_dir",
        type=Path,
        help="Directory where PNG files will be written.",
    )
    parser.add_argument(
        "--prefix",
        help="Optional prefix for output filenames; defaults to the PDF stem.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing PNG files if they already exist.",
    )
    return parser.parse_args()


def get_largest_image(images: Iterable[PdfImage]) -> PdfImage:
    """Return the largest image (by pixel area) from a collection."""
    return max(images, key=lambda img: img.width * img.height)


def page_to_png(page: pikepdf.Page, output_path: Path) -> None:
    """Extract the primary scanned image from a page and save it as PNG."""
    pdf_images = []
    for raw_image in page.images.values():
        try:
            pdf_images.append(PdfImage(raw_image))
        except pikepdf.PdfError:
            continue

    if not pdf_images:
        raise RuntimeError("No extractable images found on page")

    largest = get_largest_image(pdf_images)
    pil_image: Image.Image = largest.as_pil_image()
    pil_image.save(output_path, format="PNG")


def convert_pdf(pdf_path: Path, output_dir: Path, prefix: str, overwrite: bool) -> None:
    with pikepdf.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        for index, page in enumerate(pdf.pages, start=1):
            page_number = f"{index:03d}"
            output_file = output_dir / f"{prefix}_page_{page_number}.png"

            if output_file.exists() and not overwrite:
                raise FileExistsError(
                    f"Output file {output_file} already exists. Use --overwrite to replace it."
                )

            try:
                page_to_png(page, output_file)
            except RuntimeError as exc:
                raise RuntimeError(f"Failed on page {index} of {total_pages}: {exc}") from exc


def main() -> None:
    args = parse_args()
    pdf_path: Path = args.pdf_path
    output_dir: Path = args.output_dir
    prefix: str = args.prefix or pdf_path.stem

    if not pdf_path.exists():
        sys.exit(f"Input PDF does not exist: {pdf_path}")
    if pdf_path.suffix.lower() != ".pdf":
        sys.exit("Input file must be a PDF")

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        sys.exit(f"Unable to create output directory {output_dir}: {exc}")

    try:
        convert_pdf(pdf_path, output_dir, prefix, overwrite=args.overwrite)
    except Exception as exc:
        sys.exit(str(exc))


if __name__ == "__main__":
    main()
