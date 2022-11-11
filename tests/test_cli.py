# from click.testing import CliRunner
#
# from makeqr.cli_app import make_app
#
# runner = CliRunner()
# app = make_app()
#
#
# def test_unknown():
#     result = runner.invoke(app, ["incorrect"])
#     assert result.exit_code == 2, result.stderr()
#
#
# def test_geo():
#     result = runner.invoke(app, ["geo", "1.2", "4.5"])
#     assert result.exit_code == 0, result.stderr()
#     assert "geo:1.2,4.5" in result.stdout, result.stdout
#
#
# def test_link():
#     result = runner.invoke(app, ["link", "https://foo.bar"])
#     assert result.exit_code == 0, result.stderr()
#     assert "https://foo.bar" in result.stdout, result.stdout
#
#
# def test_mailto():
#     result = runner.invoke(app, ["mailto", "aaa@bbb.cc"])
#     assert result.exit_code == 0, result.stderr()
#     assert "mailto:aaa@bbb.cc" in result.stdout, result.stdout
#
#
# def test_sms():
#     result = runner.invoke(app, ["sms", "test"])
#     assert result.exit_code == 0, result.stderr()
#     assert "sms:test" in result.stdout, result.stdout
#
#
# def test_tel():
#     result = runner.invoke(app, ["tel", "test"])
#     assert result.exit_code == 0, result.stderr()
#     assert "tel:test" in result.stdout, result.stdout
#
#
# def test_wifi():
#     result = runner.invoke(app, ["wifi", "test"])
#     assert result.exit_code == 0, result.stderr()
#     assert "WIFI:S:test;;" in result.stdout, result.stdout
