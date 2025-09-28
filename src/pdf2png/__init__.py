"""Convert scanned PDFs to lossless per-page PNG images."""

from .cli import main
from .converter import convert_pdf, get_largest_image

__version__ = "0.1.0"

__all__ = ["main", "convert_pdf", "get_largest_image"]
