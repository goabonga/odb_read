from unittest.mock import MagicMock

from odb_tui.models.vehicle import VehicleState
from odb_tui.services.update import UpdateService


def _make_quantity(value: float) -> MagicMock:
    q = MagicMock()
    q.magnitude = value
    return q


def test_update_fills_numeric_fields():
    conn = MagicMock()
    conn.is_connected = True

    def fake_query(cmd: str) -> MagicMock | None:
        if cmd == "RPM":
            return _make_quantity(3000.0)
        if cmd == "SPEED":
            return _make_quantity(60.0)
        return None

    conn.query = fake_query

    svc = UpdateService(conn)
    state = VehicleState()
    svc.update(state)

    assert state.rpm == 3000.0
    assert state.speed == 60.0


def test_update_skips_null_responses():
    conn = MagicMock()
    conn.is_connected = True
    conn.query = MagicMock(return_value=None)

    svc = UpdateService(conn)
    state = VehicleState()
    svc.update(state)

    assert state.rpm is None
    assert state.speed is None


def test_update_computes_net_boost():
    conn = MagicMock()
    conn.is_connected = True

    def fake_query(cmd: str) -> MagicMock | None:
        if cmd == "INTAKE_PRESSURE":
            return _make_quantity(200.0)
        if cmd == "BAROMETRIC_PRESSURE":
            return _make_quantity(101.0)
        return None

    conn.query = fake_query

    svc = UpdateService(conn)
    state = VehicleState()
    svc.update(state)

    assert state.intake_press == 200.0
    assert state.baro == 101.0
    assert state.net_boost == 99.0


def test_update_handles_dtc_list():
    conn = MagicMock()
    conn.is_connected = True

    dtcs = [("P0300", "Random misfire"), ("P0420", "Catalyst efficiency")]

    def fake_query(cmd: str) -> list[tuple[str, str]] | None:
        if cmd == "GET_DTC":
            return dtcs
        return None

    conn.query = fake_query

    svc = UpdateService(conn)
    state = VehicleState()
    svc.update(state)

    assert state.dtc_list == [("P0300", "Random misfire"), ("P0420", "Catalyst efficiency")]


def test_update_handles_status_raw():
    conn = MagicMock()
    conn.is_connected = True

    status_obj = MagicMock()
    status_obj.MIL = True
    status_obj.DTC_count = 2

    def fake_query(cmd: str) -> MagicMock | None:
        if cmd == "STATUS":
            return status_obj
        return None

    conn.query = fake_query

    svc = UpdateService(conn)
    state = VehicleState()
    svc.update(state)

    assert state.status_raw is status_obj


def test_update_not_connected():
    conn = MagicMock()
    conn.is_connected = False

    svc = UpdateService(conn)
    state = VehicleState()
    state.rpm = 1500.0
    svc.update(state)

    assert state.rpm == 1500.0
