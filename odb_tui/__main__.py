"""CLI entry point for odb-tui."""

import argparse

from odb_tui import __version__
from odb_tui.app import OBDReaderApp


def main() -> None:
    """Parse CLI arguments and launch the Textual TUI app."""
    parser = argparse.ArgumentParser(
        description=f"OBD-II diagnostic TUI v{__version__}",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.parse_args()
    OBDReaderApp().run()


if __name__ == "__main__":
    main()
