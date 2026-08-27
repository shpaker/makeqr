from datetime import UTC, datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from makeqr.models import QREventModel


def test_naive_event() -> None:
    data = QREventModel(
        summary="Standup",
        start=datetime(2026, 9, 1, 12, 0),
        end=datetime(2026, 9, 1, 12, 15),
    )
    assert data.qr_data == (
        "BEGIN:VEVENT\r\nSUMMARY:Standup\r\nDTSTART:20260901T120000\r\nDTEND:20260901T121500\r\nEND:VEVENT"
    )


def test_aware_event_is_converted_to_utc() -> None:
    tz = timezone(timedelta(hours=3))
    data = QREventModel(summary="Standup", start=datetime(2026, 9, 1, 15, 0, tzinfo=tz))
    assert "DTSTART:20260901T120000Z" in data.qr_data


def test_start_accepts_iso_strings() -> None:
    data = QREventModel(summary="x", start="2026-09-01T12:00:00")
    assert "DTSTART:20260901T120000" in data.qr_data


def test_optional_lines_are_omitted() -> None:
    data = QREventModel(summary="x", start=datetime(2026, 9, 1, 12, 0))
    assert "DTEND:" not in data.qr_data
    assert "LOCATION:" not in data.qr_data
    assert "DESCRIPTION:" not in data.qr_data


def test_text_fields_are_escaped() -> None:
    data = QREventModel(
        summary="a,b;c",
        start=datetime(2026, 9, 1, 12, 0),
        location="Room 1;2",
        description="x\ny",
    )
    assert r"SUMMARY:a\,b\;c" in data.qr_data
    assert r"LOCATION:Room 1\;2" in data.qr_data
    assert r"DESCRIPTION:x\ny" in data.qr_data


def test_end_before_start_is_rejected() -> None:
    with pytest.raises(ValidationError, match="end must be after"):
        QREventModel(summary="x", start=datetime(2026, 9, 1, 12, 0), end=datetime(2026, 9, 1, 11, 0))


def test_end_equal_to_start_is_rejected() -> None:
    with pytest.raises(ValidationError, match="end must be after"):
        QREventModel(summary="x", start=datetime(2026, 9, 1, 12, 0), end=datetime(2026, 9, 1, 12, 0))


def test_mixed_naive_and_aware_is_rejected() -> None:
    with pytest.raises(ValidationError, match="both"):
        QREventModel(summary="x", start=datetime(2026, 9, 1, 12, 0), end=datetime(2026, 9, 1, 13, 0, tzinfo=UTC))
