"""Convert scanned PDFs to lossless per-page PNG images."""

from .__main__ import main
from .converter import convert_pdf, get_largest_image

__version__ = "0.1.0"

__all__ = ["convert_pdf", "get_largest_image", "main"]
