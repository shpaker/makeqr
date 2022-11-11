from makeqr.cli_app import make_app


def main() -> None:
    app = make_app()
    app()  # pylint: disable=no-value-for-parameter


if __name__ == "__main__":
    main()
