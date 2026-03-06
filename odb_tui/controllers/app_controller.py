"""Application controller orchestrating OBD services."""

from __future__ import annotations

from odb_tui.models.supported_commands import SupportedCommands
from odb_tui.models.vehicle import VehicleState
from odb_tui.services.connection import OBDConnectionService
from odb_tui.services.device import detect_obd_device
from odb_tui.services.update import UpdateService


class AppController:
    """Coordinate device detection and connection lifecycle."""

    def __init__(self) -> None:
        self.conn = OBDConnectionService()
        self.updater = UpdateService(self.conn)
        self.status = "DISCONNECTED"
        self.port = "-"
        self.vid = "-"
        self.pid = "-"
        self.supported_commands: SupportedCommands | None = None

    def connect(self) -> None:
        """Detect device, connect, and discover supported commands."""
        self.status = "CONNECTING..."
        device, vid, pid = detect_obd_device()
        if not device:
            self.status = "NO DEVICE"
            return
        self.port = device
        self.vid = vid or "-"
        self.pid = pid or "-"
        if self.conn.connect(device):
            self.status = "CONNECTED"
            self.supported_commands = self.conn.discover_supported_commands()
        else:
            self.status = "FAILED"

    def disconnect(self) -> None:
        """Disconnect and clear supported commands."""
        self.conn.disconnect()
        self.status = "DISCONNECTED"
        self.supported_commands = None

    def update_state(self, state: VehicleState) -> None:
        """Poll all OBD sensors and update state."""
        self.updater.update(state)
