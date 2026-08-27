from pathlib import Path

import pytest

from makeqr import MakeQR, QRTextModel
from makeqr.constants import ErrorCorrectionLevel

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def test_accepts_a_plain_string() -> None:
    assert MakeQR("plain string").data == "plain string"


def test_accepts_a_model_and_stores_its_payload() -> None:
    assert MakeQR(QRTextModel(text="hello")).data == "hello"


def test_matrix_is_square_and_boolean() -> None:
    matrix = MakeQR(QRTextModel(text="x"), border=1).matrix
    assert len({len(row) for row in matrix}) == 1
    assert len(matrix) == len(matrix[0])
    assert all(isinstance(cell, bool) for row in matrix for cell in row)


def test_border_widens_the_quiet_zone() -> None:
    narrow = MakeQR(QRTextModel(text="x"), border=1).matrix
    wide = MakeQR(QRTextModel(text="x"), border=4).matrix
    assert len(wide) == len(narrow) + 6


def test_higher_error_correction_needs_more_modules() -> None:
    payload = "x" * 100
    low = MakeQR(payload, error_correction=ErrorCorrectionLevel.LOW).matrix
    high = MakeQR(payload, error_correction=ErrorCorrectionLevel.HIGH).matrix
    assert len(high) > len(low)


def test_error_correction_accepts_a_string() -> None:
    assert MakeQR("x", error_correction="high").matrix == MakeQR("x", error_correction=ErrorCorrectionLevel.HIGH).matrix


def test_unknown_error_correction_is_rejected() -> None:
    with pytest.raises(ValueError, match="nonsense"):
        MakeQR("x", error_correction="nonsense")


def test_make_image_data_returns_a_png() -> None:
    assert MakeQR(QRTextModel(text="x")).make_image_data().startswith(PNG_MAGIC)


def test_make_image_data_honours_the_format() -> None:
    data = MakeQR(QRTextModel(text="x")).make_image_data("JPEG")
    assert data.startswith(b"\xff\xd8")


def test_save_writes_a_png(tmp_path: Path) -> None:
    target = tmp_path / "code.png"
    MakeQR(QRTextModel(text="x")).save(target)
    assert target.read_bytes().startswith(PNG_MAGIC)


def test_save_rejects_an_unknown_extension_without_creating_a_file(tmp_path: Path) -> None:
    target = tmp_path / "code.unknown"
    with pytest.raises(ValueError, match="unknown file extension"):
        MakeQR(QRTextModel(text="x")).save(target)
    assert not target.exists()


def test_save_rejects_a_missing_extension(tmp_path: Path) -> None:
    target = tmp_path / "code"
    with pytest.raises(ValueError, match="no file extension"):
        MakeQR(QRTextModel(text="x")).save(target)
    assert not target.exists()


def test_a_failed_save_leaves_an_existing_file_intact(tmp_path: Path) -> None:
    target = tmp_path / "notes.txt"
    target.write_text("IMPORTANT USER DATA")
    with pytest.raises(ValueError, match="unknown file extension"):
        MakeQR(QRTextModel(text="x")).save(target)
    assert target.read_text() == "IMPORTANT USER DATA"


def test_save_leaves_no_temporary_files_behind(tmp_path: Path) -> None:
    MakeQR(QRTextModel(text="x")).save(tmp_path / "code.png")
    assert [path.name for path in tmp_path.iterdir()] == ["code.png"]


def test_reassigning_data_rebuilds_the_code() -> None:
    qr = MakeQR(QRTextModel(text="x"))
    short = qr.matrix
    qr.data = "y" * 200
    assert len(qr.matrix) > len(short)
    assert qr.data == "y" * 200
