"""Service to poll OBD commands and populate VehicleState."""

from __future__ import annotations

from typing import Any

from odb_tui.models.vehicle import VehicleState
from odb_tui.services.connection import OBDConnectionService

NUMERIC_MAP: dict[str, str] = {
    "RPM": "rpm",
    "ENGINE_LOAD": "engine_load",
    "ABSOLUTE_LOAD": "abs_load",
    "COOLANT_TEMP": "coolant_temp",
    "OIL_TEMP": "oil_temp",
    "INTAKE_TEMP": "intake_temp",
    "AMBIANT_TEMP": "ambient_temp",
    "MAF": "maf",
    "CONTROL_MODULE_VOLTAGE": "voltage",
    "TIMING_ADVANCE": "timing",
    "RUN_TIME": "run_time",
    "FUEL_RAIL_PRESSURE_DIRECT": "fuel_rail",
    "FUEL_RATE": "fuel_rate",
    "FUEL_LEVEL": "fuel_level",
    "FUEL_INJECT_TIMING": "fuel_inject",
    "COMMANDED_EQUIV_RATIO": "equiv_ratio",
    "SHORT_FUEL_TRIM_1": "short_ft1",
    "LONG_FUEL_TRIM_1": "long_ft1",
    "INTAKE_PRESSURE": "intake_press",
    "BAROMETRIC_PRESSURE": "baro",
    "THROTTLE_POS": "throttle",
    "THROTTLE_POS_B": "throttle_b",
    "THROTTLE_ACTUATOR": "throttle_act",
    "ACCELERATOR_POS_D": "accel_d",
    "ACCELERATOR_POS_E": "accel_e",
    "RELATIVE_ACCEL_POS": "rel_accel",
    "O2_S1_WR_CURRENT": "o2_s1_wr",
    "O2_S2_WR_CURRENT": "o2_s2_wr",
    "COMMANDED_EGR": "egr_cmd",
    "EGR_ERROR": "egr_err",
    "SPEED": "speed",
    "DISTANCE_W_MIL": "dist_mil",
    "RUN_TIME_MIL": "run_time_mil",
    "WARMUPS_SINCE_DTC_CLEAR": "warmups",
    "DISTANCE_SINCE_DTC_CLEAR": "dist_dtc",
    "TIME_SINCE_DTC_CLEARED": "time_dtc",
}

PASSTHROUGH_MAP: dict[str, str] = {
    "STATUS": "status_raw",
    "OBD_COMPLIANCE": "obd_comp",
    "FUEL_TYPE": "fuel_type",
    "FUEL_STATUS": "fuel_status",
    "O2_SENSORS": "o2_sensors",
    "CALIBRATION_ID": "cal_id",
    "CVN": "cvn",
}

DTC_MAP: dict[str, str] = {
    "GET_DTC": "dtc_list",
    "GET_CURRENT_DTC": "current_dtc_list",
}


def _extract_float(raw: Any) -> float:
    if hasattr(raw, "magnitude"):
        return float(raw.magnitude)
    return float(raw)


class UpdateService:
    """Poll OBD commands and fill VehicleState fields."""

    def __init__(self, conn: OBDConnectionService) -> None:
        self.conn = conn

    def update(self, state: VehicleState) -> None:
        """Query all mapped commands and update state in-place."""
        if not self.conn.is_connected:
            return

        for cmd_name, field in NUMERIC_MAP.items():
            raw = self.conn.query(cmd_name)
            if raw is not None:
                setattr(state, field, _extract_float(raw))

        for cmd_name, field in PASSTHROUGH_MAP.items():
            raw = self.conn.query(cmd_name)
            if raw is not None:
                setattr(state, field, raw)

        for cmd_name, field in DTC_MAP.items():
            raw = self.conn.query(cmd_name)
            if raw is not None:
                setattr(state, field, list(raw))

        # Computed: net boost
        if state.intake_press is not None and state.baro is not None:
            state.net_boost = state.intake_press - state.baro
