"""Command-line interface for PDF to PNG conversion."""

import argparse
import sys
from pathlib import Path

from .converter import convert_pdf


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


def main() -> None:
    """Main entry point for the CLI application.

    Parses command-line arguments, validates inputs, and initiates PDF conversion.
    """
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
