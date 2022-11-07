from makeqr.cli_app.app import make_app


def main() -> None:
    app = make_app()
    app()
