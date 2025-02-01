from ansitoolkit.core.constants import AnsiDeviceStatus
from ansitoolkit.core.generator import ansi_device_status_sequence


class DeviceStatus:
    DEVICE_STATUS_REPORT = ansi_device_status_sequence(AnsiDeviceStatus.DEVICE_STATUS_REPORT)
    TERMINAL_OK = ansi_device_status_sequence(AnsiDeviceStatus.TERMINAL_OK)
    TERMINAL_MALFUNCTION = ansi_device_status_sequence(AnsiDeviceStatus.TERMINAL_MALFUNCTION)
    CURSOR_POSITION_REPORT = ansi_device_status_sequence(AnsiDeviceStatus.CURSOR_POSITION_REPORT)
    QUERY_DEVICE_ATTRIBUTES = ansi_device_status_sequence(AnsiDeviceStatus.QUERY_DEVICE_ATTRIBUTES)
