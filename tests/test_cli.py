from click.testing import CliRunner

from makeqr.cli_app import make_app

runner = CliRunner()
app = make_app()


def test_unknown():
    result = runner.invoke(app, ["incorrect"])
    assert result.exit_code == 2, result.output  # noqa: PLR2004


def test_geo():
    result = runner.invoke(app, ["-qv", "geo", "-lat", "1.2", "-long", "4.5"])
    assert result.exit_code == 0, result.output
    assert "geo:1.2,4.5" in result.stdout, result.stdout


def test_link():
    result = runner.invoke(app, ["-qv", "link", "https://foo.bar"])
    assert result.exit_code == 0, result.output
    assert "https://foo.bar" in result.stdout, result.stdout


def test_mailto():
    result = runner.invoke(app, ["-qv", "mailto", "aaa@bbb.cc"])
    assert result.exit_code == 0, result.output
    assert "mailto:aaa@bbb.cc" in result.stdout, result.stdout


def test_sms():
    result = runner.invoke(app, ["-qv", "sms", "-r", "test"])
    assert result.exit_code == 0, result.output
    assert "sms:test" in result.stdout, result.stdout


def test_tel():
    result = runner.invoke(app, ["-qv", "tel", "test"])
    assert result.exit_code == 0, result.output
    assert "tel:test" in result.stdout, result.stdout


def test_wifi():
    result = runner.invoke(app, ["-qv", "wifi", "test"])
    assert result.exit_code == 0, result.output
    assert "WIFI:S:test;;" in result.stdout, result.stdout
