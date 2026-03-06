from unittest.mock import MagicMock, patch

from odb_tui.services.connection import OBDConnectionService


def _make_cmd(name: str, pid: int | None, desc: str) -> MagicMock:
    cmd = MagicMock()
    cmd.name = name
    cmd.pid = pid
    cmd.desc = desc
    return cmd


def test_discover_marks_supported_by_name():
    """Regression: supported commands must be detected by name, not object identity."""
    rpm_in_mode = _make_cmd("RPM", 0x0C, "Engine RPM")
    speed_in_mode = _make_cmd("SPEED", 0x0D, "Vehicle Speed")

    # Different object instances with the same name — simulates real python-obd behavior
    rpm_in_supported = _make_cmd("RPM", 0x0C, "Engine RPM")

    conn_mock = MagicMock()
    conn_mock.is_connected.return_value = True
    conn_mock.supported_commands = {rpm_in_supported}

    svc = OBDConnectionService()
    svc.connection = conn_mock

    mock_commands = MagicMock()
    mock_commands.__getitem__ = MagicMock(side_effect=lambda k: {1: [rpm_in_mode, speed_in_mode]}[k])
    mock_commands.ELM_VERSION = None
    mock_commands.ELM_VOLTAGE = None

    with patch("odb_tui.services.connection.obd.commands", mock_commands):
        result = svc.discover_supported_commands()

    mode_cmds = result.modes["Mode 01 — Live Data"]
    rpm_status = next(c for c in mode_cmds if c.name == "RPM")
    speed_status = next(c for c in mode_cmds if c.name == "SPEED")

    assert rpm_status.supported is True
    assert speed_status.supported is False
