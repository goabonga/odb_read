"""Textual TUI application for OBD-II diagnostics."""

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Header, Static


class OBDReaderApp(App[None]):
    """Minimal Textual app rendering an OBD-II dashboard."""

    CSS = """
    Screen { background: black; color: green; }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        """Build the widget tree: header, main content, footer."""
        yield Header(show_clock=True)
        yield Static("OBD-II Reader", id="main")
        yield Footer()
