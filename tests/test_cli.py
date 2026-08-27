from pathlib import Path

from click.testing import CliRunner

from makeqr import __version__
from makeqr.cli import make_app

runner = CliRunner()
app = make_app()


def test_unknown_command() -> None:
    result = runner.invoke(app, ["incorrect"])
    assert result.exit_code == 2, result.output


def test_version() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0, result.output
    assert result.stdout.strip() == __version__


def test_help_lists_every_command() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0, result.output
    commands = ("event", "geo", "link", "mailto", "mecard", "otp", "sms", "tel", "text", "vcard", "wifi")
    for command in commands:
        assert command in result.stdout


def test_event() -> None:
    result = runner.invoke(app, ["-qv", "event", "-s", "Standup", "-st", "2026-09-01T12:00:00"])
    assert result.exit_code == 0, result.output
    assert "DTSTART:20260901T120000" in result.stdout


def test_geo() -> None:
    result = runner.invoke(app, ["-qv", "geo", "-lat", "1.2", "-long", "4.5"])
    assert result.exit_code == 0, result.output
    assert "geo:1.2,4.5" in result.stdout


def test_link() -> None:
    result = runner.invoke(app, ["-qv", "link", "https://foo.bar"])
    assert result.exit_code == 0, result.output
    assert "https://foo.bar" in result.stdout


def test_link_without_scheme() -> None:
    result = runner.invoke(app, ["-qv", "link", "foo.bar"])
    assert result.exit_code == 0, result.output
    assert "https://foo.bar" in result.stdout


def test_mailto() -> None:
    result = runner.invoke(app, ["-qv", "mailto", "aaa@bbb.cc"])
    assert result.exit_code == 0, result.output
    assert "mailto:aaa@bbb.cc" in result.stdout


def test_mailto_cc_is_repeatable_and_distinct_from_bcc() -> None:
    result = runner.invoke(
        app,
        ["-qv", "mailto", "--cc", "a@b.cc", "--cc", "c@d.ee", "--bcc", "e@f.gg", "to@to.tt"],
    )
    assert result.exit_code == 0, result.output
    assert "cc=a%40b.cc%2Cc%40d.ee" in result.stdout
    assert "bcc=e%40f.gg" in result.stdout


def test_mailto_help_has_no_none_flag() -> None:
    result = runner.invoke(app, ["mailto", "--help"])
    assert result.exit_code == 0, result.output
    assert "-None" not in result.stdout


def test_mecard() -> None:
    result = runner.invoke(app, ["-qv", "mecard", "-f", "John", "Doe"])
    assert result.exit_code == 0, result.output
    assert "MECARD:N:Doe,John;;" in result.stdout


def test_otp() -> None:
    result = runner.invoke(app, ["-qv", "otp", "-l", "alice@example.com", "-s", "JBSWY3DPEHPK3PXP", "-i", "Example"])
    assert result.exit_code == 0, result.output
    assert "otpauth://totp/Example%3Aalice%40example.com" in result.stdout


def test_otp_secret_is_never_printed() -> None:
    result = runner.invoke(app, ["-qv", "otp", "-l", "alice@example.com", "-s", "JBSWY3DPEHPK3PXP"])
    assert result.exit_code == 0, result.output
    assert "JBSWY3DPEHPK3PXP" not in result.stdout


def test_sms() -> None:
    result = runner.invoke(app, ["-qv", "sms", "-r", "test"])
    assert result.exit_code == 0, result.output
    assert "sms:test" in result.stdout


def test_tel() -> None:
    result = runner.invoke(app, ["-qv", "tel", "test"])
    assert result.exit_code == 0, result.output
    assert "tel:test" in result.stdout


def test_text() -> None:
    result = runner.invoke(app, ["-qv", "text", "hello"])
    assert result.exit_code == 0, result.output
    assert "Encoded: hello" in result.stdout


def test_vcard() -> None:
    result = runner.invoke(app, ["-qv", "vcard", "-f", "John", "-t", "+111", "-t", "+222", "Doe"])
    assert result.exit_code == 0, result.output
    assert "N:Doe;John" in result.stdout
    assert "TEL:+222" in result.stdout


def test_vcard_option_names_use_dashes() -> None:
    result = runner.invoke(app, ["vcard", "--help"])
    assert result.exit_code == 0, result.output
    assert "--first-name" in result.stdout
    assert "--first_name" not in result.stdout


def test_wifi() -> None:
    result = runner.invoke(app, ["-qv", "wifi", "test"])
    assert result.exit_code == 0, result.output
    assert "WIFI:S:test;T:nopass;;" in result.stdout


def test_wifi_hidden_is_a_flag() -> None:
    result = runner.invoke(app, ["-qv", "wifi", "--hidden", "test"])
    assert result.exit_code == 0, result.output
    assert "H:true" in result.stdout


def test_wifi_password_is_never_printed() -> None:
    result = runner.invoke(app, ["-qv", "wifi", "-s", "wpa", "-p", "TopSecret", "HomeWiFi"])
    assert result.exit_code == 0, result.output
    assert "TopSecret" not in result.stdout
    assert "T:WPA" in result.stdout


def test_validation_error_exits_nonzero() -> None:
    result = runner.invoke(app, ["-q", "mailto", "not-an-email"])
    assert result.exit_code == 1, result.output


def test_quiet_suppresses_the_matrix() -> None:
    result = runner.invoke(app, ["-q", "text", "hello"])
    assert "██" not in result.stdout


def test_quite_is_still_accepted() -> None:
    result = runner.invoke(app, ["--quite", "text", "hello"])
    assert result.exit_code == 0, result.output
    assert "██" not in result.stdout


def test_matrix_is_printed_by_default() -> None:
    result = runner.invoke(app, ["text", "hello"])
    assert result.exit_code == 0, result.output
    assert "██" in result.stdout


def test_output_writes_a_file(tmp_path: Path) -> None:
    target = tmp_path / "code.png"
    result = runner.invoke(app, ["-q", "-o", str(target), "text", "hello"])
    assert result.exit_code == 0, result.output
    assert target.read_bytes().startswith(b"\x89PNG")


def test_output_with_an_odd_extension_keeps_the_original_file(tmp_path: Path) -> None:
    target = tmp_path / "notes.txt"
    target.write_text("IMPORTANT USER DATA")
    result = runner.invoke(app, ["-q", "-o", str(target), "text", "hello"])
    assert result.exit_code == 0, result.output
    assert target.read_text() == "IMPORTANT USER DATA"
    assert (tmp_path / "notes.txt.png").read_bytes().startswith(b"\x89PNG")


def test_box_size_scales_the_image(tmp_path: Path) -> None:
    small = tmp_path / "small.png"
    large = tmp_path / "large.png"
    runner.invoke(app, ["-q", "-s", "2", "-o", str(small), "text", "hello"])
    runner.invoke(app, ["-q", "-s", "10", "-o", str(large), "text", "hello"])
    assert large.stat().st_size > small.stat().st_size
