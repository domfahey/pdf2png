from pathlib import Path
from dataclasses import dataclass
from unittest import mock

import pytest
from PIL import Image, ImageChops

from pdf2png import convert_pdf, get_largest_image


# Test data structures
@dataclass
class MockImage:
    """Mock image object for testing."""
    width: int
    height: int


@dataclass
class SamplePDF:
    """PDF test fixture data."""
    path: Path
    baseline_image: Image.Image


# Configuration
SAMPLE_SIZE = (32, 32)
OUTPUT_DIR_NAME = "out"


# Pytest fixtures
@pytest.fixture
def sample_pdf(tmp_path: Path) -> SamplePDF:
    """Create a basic single-page PDF for testing."""
    pdf_path = tmp_path / "sample.pdf"
    baseline = Image.new("RGB", SAMPLE_SIZE, color="white")
    baseline.save(pdf_path, "PDF")
    return SamplePDF(pdf_path, baseline)


@pytest.fixture
def output_dir(tmp_path: Path) -> Path:
    """Create a temporary output directory."""
    out_dir = tmp_path / OUTPUT_DIR_NAME
    out_dir.mkdir()
    return out_dir


@pytest.fixture
def multi_page_pdf(tmp_path: Path) -> tuple[Path, dict[int, tuple[int, int]]]:
    """Create a multi-page PDF with known page sizes."""
    pdf_path = tmp_path / "multi.pdf"
    pages = [
        Image.new("RGB", (32, 32), color="red"),
        Image.new("RGB", (64, 64), color="blue"),
        Image.new("RGB", (16, 16), color="green"),
    ]
    expected_sizes = {1: (32, 32), 2: (64, 64), 3: (16, 16)}

    pages[0].save(pdf_path, "PDF", append_images=pages[1:])

    return pdf_path, expected_sizes


def create_sample_pdf(pdf_path: Path, size=SAMPLE_SIZE, append_images=None) -> Image.Image:
    """Create a sample PDF from PIL images."""
    image = Image.new("RGB", size or SAMPLE_SIZE, color="white")
    save_kwargs = {"format": "PDF"}
    if append_images:
        save_kwargs["append_images"] = append_images
    image.save(pdf_path, **save_kwargs)
    return image


def test_get_largest_image():
    """Test get_largest_image function selects the largest by pixel area."""

    images = [
        MockImage(10, 10),  # 100 px
        MockImage(20, 30),  # 600 px
        MockImage(40, 20),  # 800 px (largest)
        MockImage(15, 15),  # 225 px
    ]
    largest = get_largest_image(images)
    assert largest is images[2]
    assert largest.width == 40
    assert largest.height == 20


def test_convert_pdf_outputs_named_png_single_page(sample_pdf: SamplePDF, output_dir: Path) -> None:
    """Test successful conversion of a single-page PDF."""
    convert_pdf(sample_pdf.path, output_dir, prefix="sample", overwrite=False)

    output_file = output_dir / "sample_page_001.png"
    assert output_file.exists()

    with Image.open(output_file) as png:
        assert png.size == SAMPLE_SIZE

        diff = ImageChops.difference(png.convert("RGB"), sample_pdf.baseline_image)
        assert diff.getbbox() is None


def test_convert_pdf_outputs_named_png_multiple_pages(multi_page_pdf: tuple[Path, dict[int, tuple[int, int]]], output_dir: Path) -> None:
    """Test successful conversion of a multi-page PDF."""
    pdf_path, expected_sizes = multi_page_pdf

    convert_pdf(pdf_path, output_dir, prefix="multi", overwrite=False)

    for page_num, expected_size in expected_sizes.items():
        output_file = output_dir / f"multi_page_{page_num:03d}.png"
        assert output_file.exists()
        with Image.open(output_file) as png:
            assert png.size == expected_size


def test_convert_pdf_overwrite_existing_file_raises(tmp_path) -> None:
    """Test that convert_pdf raises FileExistsError when output exists."""
    pdf_path = tmp_path / "sample.pdf"
    create_sample_pdf(pdf_path)

    output_dir = tmp_path / "out"
    output_dir.mkdir()

    convert_pdf(pdf_path, output_dir, prefix="sample", overwrite=False)

    # Try to convert again without overwrite
    with pytest.raises(FileExistsError, match=r"Output file .* already exists"):
        convert_pdf(pdf_path, output_dir, prefix="sample", overwrite=False)


def test_convert_pdf_overwrite_existing_file_succeeds(tmp_path) -> None:
    """Test that convert_pdf overwrites when overwrite=True."""
    pdf_path = tmp_path / "sample.pdf"
    create_sample_pdf(pdf_path)

    output_dir = tmp_path / "out"
    output_dir.mkdir()

    convert_pdf(pdf_path, output_dir, prefix="sample", overwrite=False)
    output_file = output_dir / "sample_page_001.png"
    mtime1 = output_file.stat().st_mtime

    # Wait a bit to ensure mtime changes
    import time

    time.sleep(0.01)

    convert_pdf(pdf_path, output_dir, prefix="sample", overwrite=True)

    mtime2 = output_file.stat().st_mtime
    assert mtime1 < mtime2


def test_convert_pdf_invalid_pdf_path(tmp_path) -> None:
    """Test that convert_pdf raises error for non-existent PDF."""
    pdf_path = tmp_path / "nonexistent.pdf"
    output_dir = tmp_path / "out"
    output_dir.mkdir()

    with pytest.raises(FileNotFoundError):
        convert_pdf(pdf_path, output_dir, prefix="invalid", overwrite=False)


def test_convert_pdf_page_processing_error(tmp_path) -> None:
    """Test that convert_pdf re-raises errors from page processing."""
    pdf_path = tmp_path / "sample.pdf"
    create_sample_pdf(pdf_path)

    output_dir = tmp_path / "out"
    output_dir.mkdir()

    with (
        mock.patch(
            "pdf2png.converter.page_to_png",
            side_effect=RuntimeError("No extractable images found on page"),
        ),
        pytest.raises(
            RuntimeError,
            match=r"Failed on page 1 of 1: No extractable images found on page",
        ),
    ):
        convert_pdf(pdf_path, output_dir, prefix="sample", overwrite=False)


@pytest.mark.parametrize(
    "invalid_path,expected_message",
    [
        ("nonexistent.pdf", lambda path: f"Input PDF does not exist: {path}"),
        ("file.txt", lambda _: "Input file must be a PDF"),
    ],
)
def test_main_invalid_inputs(tmp_path, invalid_path, expected_message):
    """Test main exits with error for invalid input files."""
    input_path = tmp_path / invalid_path
    if invalid_path == "file.txt":
        input_path.write_text("not a pdf")
    out_dir = tmp_path / "out"

    with (
        mock.patch("sys.argv", ["pdf2png.py", str(input_path), str(out_dir)]),
        mock.patch("sys.exit") as mock_exit,
    ):
        mock_exit.side_effect = SystemExit
        with pytest.raises(SystemExit):
            from pdf2png import main

            main()
        expected = expected_message(input_path) if callable(expected_message) else expected_message
        mock_exit.assert_called_once_with(expected)


def test_main_mkdir_failure(tmp_path) -> None:
    """Test main exits with error when mkdir fails."""
    pdf_path = tmp_path / "sample.pdf"
    create_sample_pdf(pdf_path)
    out_dir = tmp_path / "out"

    with mock.patch("sys.argv", ["pdf2png.py", str(pdf_path), str(out_dir)]):
        with mock.patch("pathlib.Path.mkdir", side_effect=OSError("Permission denied")):
            with mock.patch("sys.exit") as mock_exit:
                mock_exit.side_effect = SystemExit
                with pytest.raises(SystemExit):
                    from pdf2png import main

                    main()
                call_arg = mock_exit.call_args[0][0]
                assert (
                    "Unable to create output directory" in call_arg
                    and "Permission denied" in call_arg
                )
