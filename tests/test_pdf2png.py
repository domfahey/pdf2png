from pathlib import Path

from PIL import Image

from pdf2png import convert_pdf


def create_sample_pdf(pdf_path: Path) -> None:
    image = Image.new("RGB", (32, 32), color="white")
    image.save(pdf_path, "PDF")


def test_convert_pdf_outputs_named_png(tmp_path) -> None:
    pdf_path = tmp_path / "sample.pdf"
    create_sample_pdf(pdf_path)

    output_dir = tmp_path / "out"
    output_dir.mkdir()

    convert_pdf(pdf_path, output_dir, prefix="sample", overwrite=False)

    output_file = output_dir / "sample_page_001.png"
    assert output_file.exists()

    with Image.open(output_file) as png:
        assert png.size == (32, 32)
