"""PDF to PNG conversion utilities."""

from pathlib import Path
from typing import Iterable, cast

import pikepdf
from pikepdf import PdfImage, Stream
from PIL import Image


def get_largest_image(images: Iterable[PdfImage]) -> PdfImage:
    """Return the largest image (by pixel area) from a collection.

    Args:
        images: An iterable collection of PdfImage objects.

    Returns:
        The PdfImage with the maximum width * height.
    """
    return max(images, key=lambda img: img.width * img.height)


def page_to_png(page: pikepdf.Page, output_path: Path) -> None:
    """Extract the primary scanned image from a page and save it as PNG.

    Iterates through all images in the PDF page, extracts them as PdfImage
    objects, and skips any that fail to load. If no valid images are found,
    raises a RuntimeError. Otherwise, selects the largest by area and saves it
    as a lossless PNG file.

    Args:
        page: The pikepdf.Page object from which to extract images.
        output_path: Path where the output PNG file will be written.

    Raises:
        RuntimeError: If no extractable images are found on the page.
    """
    pdf_images = []
    for raw_image in page.images.values():
        try:
            pdf_images.append(PdfImage(cast(Stream, raw_image)))
        except pikepdf.PdfError:
            continue

    if not pdf_images:
        raise RuntimeError("No extractable images found on page")

    largest = get_largest_image(pdf_images)
    pil_image: Image.Image = largest.as_pil_image()
    # Use PNG with no lossy transformations so pixel data remains untouched.
    pil_image.save(output_path, format="PNG", compress_level=0, optimize=False)


def convert_pdf(pdf_path: Path, output_dir: Path, prefix: str, overwrite: bool) -> None:
    """Convert each page of the PDF to a separate PNG file.

    For each page in the PDF, extracts the largest image and saves it as a PNG
    file with a numbered suffix (e.g., prefix_page_001.png).

    Args:
        pdf_path: Path to the input PDF file.
        output_dir: Directory where PNG files will be saved.
        prefix: String prefix for output filenames.
        overwrite: If True, overwrite existing PNG files; otherwise raise an error.

    Raises:
        FileExistsError: If a PNG file already exists and overwrite is False.
        RuntimeError: If a page contains no extractable images.
    """
    with pikepdf.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        for index, page in enumerate(pdf.pages, start=1):
            page_number = f"{index:03d}"
            output_file = output_dir / f"{prefix}_page_{page_number}.png"

            if output_file.exists() and not overwrite:
                raise FileExistsError(
                    f"Output file {output_file} already exists. Use --overwrite."
                )

            try:
                page_to_png(page, output_file)
            except RuntimeError as exc:
                raise RuntimeError(
                    f"Failed on page {index} of {total_pages}: {exc}"
                ) from exc
