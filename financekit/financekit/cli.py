"""Command-line entry point for FinanceKit."""

from . import __version__


def main() -> int:
    """Run the default FinanceKit CLI command."""
    print(f"FinanceKit {__version__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
