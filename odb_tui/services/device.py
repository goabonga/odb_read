"""OBD-II device detection service."""

import serial.tools.list_ports as list_ports


def detect_obd_device() -> tuple[str | None, str | None, str | None]:
    """Scan serial ports for a known OBD-II adapter.

    Returns a tuple of (device_path, vid_hex, pid_hex) or (None, None, None).
    """
    ports = list_ports.comports()
    for port in ports:
        vid = f"{port.vid:04x}" if port.vid else None
        pid = f"{port.pid:04x}" if port.pid else None
        if (
            (vid == "0403" and pid == "6015")
            or "vLinker" in (port.product or "")
            or "vgatemall" in (port.manufacturer or "")
        ):
            return port.device, vid, pid
    return None, None, None
