from pathlib import Path
import pytest
from unittest import mock

from PIL import Image, ImageChops

from pdf2png import convert_pdf, get_largest_image


def create_sample_pdf(pdf_path: Path, size=(32, 32), append_images=None) -> Image.Image:
    """Create a sample PDF from PIL images."""
    image = Image.new("RGB", size, color="white")
    save_kwargs = {"format": "PDF"}
    if append_images:
        save_kwargs["append_images"] = append_images
    image.save(pdf_path, **save_kwargs)
    return image


def test_get_largest_image():
    """Test get_largest_image function with multiple images."""
    class MockImage:
        def __init__(self, width, height):
            self.width = width
            self.height = height

    images = [
        MockImage(10, 10),
        MockImage(20, 30),
        MockImage(40, 20),  # 800 px area
        MockImage(15, 15),  # 225 px area
    ]
    largest = get_largest_image(images)
    assert largest is images[2]  # 40x20


def test_convert_pdf_outputs_named_png_single_page(tmp_path) -> None:
    """Test successful conversion of a single-page PDF."""
    pdf_path = tmp_path / "sample.pdf"
    baseline = create_sample_pdf(pdf_path)

    output_dir = tmp_path / "out"
    output_dir.mkdir()

    convert_pdf(pdf_path, output_dir, prefix="sample", overwrite=False)

    output_file = output_dir / "sample_page_001.png"
    assert output_file.exists()

    with Image.open(output_file) as png:
        assert png.size == (32, 32)

        diff = ImageChops.difference(png.convert("RGB"), baseline)
        assert diff.getbbox() is None


def test_convert_pdf_outputs_named_png_multiple_pages(tmp_path) -> None:
    """Test successful conversion of a multi-page PDF."""
    pdf_path = tmp_path / "multi.pdf"
    img1 = Image.new("RGB", (32, 32), color="red")
    img2 = Image.new("RGB", (64, 64), color="blue")
    img3 = Image.new("RGB", (16, 16), color="green")
    img1.save(pdf_path, "PDF", append_images=[img2, img3])

    output_dir = tmp_path / "out"
    output_dir.mkdir()

    convert_pdf(pdf_path, output_dir, prefix="multi", overwrite=False)

    for page_num in range(1, 4):
        output_file = output_dir / f"multi_page_{page_num:03d}.png"
        assert output_file.exists()
        with Image.open(output_file) as png:
            if page_num == 1:
                assert png.size == (32, 32)
            elif page_num == 2:
                assert png.size == (64, 64)
            elif page_num == 3:
                assert png.size == (16, 16)


def test_convert_pdf_overwrite_existing_file_raises(tmp_path) -> None:
    """Test that convert_pdf raises FileExistsError when output exists and overwrite=False."""
    pdf_path = tmp_path / "sample.pdf"
    create_sample_pdf(pdf_path)

    output_dir = tmp_path / "out"
    output_dir.mkdir()

    convert_pdf(pdf_path, output_dir, prefix="sample", overwrite=False)

    # Try to convert again without overwrite
    with pytest.raises(FileExistsError, match="Output file .* already exists"):
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

    with mock.patch('pdf2png.page_to_png', side_effect=RuntimeError("No extractable images found on page")):
        with pytest.raises(RuntimeError, match=r"Failed on page 1 of 1: No extractable images found on page"):
            convert_pdf(pdf_path, output_dir, prefix="sample", overwrite=False)


def test_main_invalid_pdf_path(tmp_path) -> None:
    """Test main exits with error for non-existent PDF."""
    pdf_path = tmp_path / "nonexist.pdf"
    out_dir = tmp_path / "out"

    with mock.patch('sys.argv', ['pdf2png.py', str(pdf_path), str(out_dir)]):
        with mock.patch('sys.exit') as mock_exit:
            mock_exit.side_effect = SystemExit
            with pytest.raises(SystemExit):
                from pdf2png import main
                main()
            mock_exit.assert_called_once_with(f"Input PDF does not exist: {pdf_path}")


def test_main_not_pdf_extension(tmp_path) -> None:
    """Test main exits with error for non-PDF extension."""
    txt_path = tmp_path / "file.txt"
    txt_path.write_text("not a pdf")
    out_dir = tmp_path / "out"

    with mock.patch('sys.argv', ['pdf2png.py', str(txt_path), str(out_dir)]):
        with mock.patch('sys.exit') as mock_exit:
            mock_exit.side_effect = SystemExit
            with pytest.raises(SystemExit):
                from pdf2png import main
                main()
            mock_exit.assert_called_once_with("Input file must be a PDF")


def test_main_mkdir_failure(tmp_path) -> None:
    """Test main exits with error when mkdir fails."""
    pdf_path = tmp_path / "sample.pdf"
    create_sample_pdf(pdf_path)
    out_dir = tmp_path / "out"

    with mock.patch('sys.argv', ['pdf2png.py', str(pdf_path), str(out_dir)]):
        with mock.patch('pathlib.Path.mkdir', side_effect=OSError("Permission denied")):
            with mock.patch('sys.exit') as mock_exit:
                mock_exit.side_effect = SystemExit
                with pytest.raises(SystemExit):
                    from pdf2png import main
                    main()
                call_arg = mock_exit.call_args[0][0]
                assert "Unable to create output directory" in call_arg and "Permission denied" in call_arg
