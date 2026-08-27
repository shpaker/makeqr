import pytest
from pydantic import ValidationError

from makeqr.constants import OtpAlgorithm, OtpType
from makeqr.models import QROtpModel


def test_totp_defaults() -> None:
    data = QROtpModel(label="alice@example.com", secret="JBSWY3DPEHPK3PXP")
    assert data.qr_data == "otpauth://totp/alice%40example.com?secret=JBSWY3DPEHPK3PXP"


def test_totp_with_issuer() -> None:
    data = QROtpModel(label="alice@example.com", secret="JBSWY3DPEHPK3PXP", issuer="Example")
    assert data.qr_data == "otpauth://totp/Example%3Aalice%40example.com?secret=JBSWY3DPEHPK3PXP&issuer=Example"


def test_totp_with_every_parameter() -> None:
    data = QROtpModel(
        label="alice@example.com",
        secret="JBSWY3DPEHPK3PXP",
        issuer="Example",
        algorithm=OtpAlgorithm.SHA256,
        digits=8,
        period=60,
    )
    assert data.qr_data == (
        "otpauth://totp/Example%3Aalice%40example.com"
        "?secret=JBSWY3DPEHPK3PXP&issuer=Example&algorithm=SHA256&digits=8&period=60"
    )


def test_hotp_with_zero_counter() -> None:
    data = QROtpModel(type=OtpType.HOTP, label="alice@example.com", secret="JBSWY3DPEHPK3PXP", counter=0)
    assert data.qr_data == "otpauth://hotp/alice%40example.com?secret=JBSWY3DPEHPK3PXP&counter=0"


def test_hotp_requires_counter() -> None:
    with pytest.raises(ValidationError, match="counter is required"):
        QROtpModel(type=OtpType.HOTP, label="a", secret="S")


def test_totp_rejects_counter() -> None:
    with pytest.raises(ValidationError, match="only valid when type is hotp"):
        QROtpModel(label="a", secret="S", counter=1)


def test_hotp_rejects_period() -> None:
    with pytest.raises(ValidationError, match="only valid when type is totp"):
        QROtpModel(type=OtpType.HOTP, label="a", secret="S", counter=1, period=30)


def test_secret_is_masked_in_dumps() -> None:
    data = QROtpModel(label="alice@example.com", secret="JBSWY3DPEHPK3PXP")
    assert "JBSWY3DPEHPK3PXP" not in data.model_dump_json()
