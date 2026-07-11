"""Constants for the aerosmart integration."""

from datetime import timedelta
from typing import Final

DOMAIN: Final = "aerosmart"

CONF_CONNECTION: Final = "connection_entry_id"
CONF_UNIT_VENTILATION: Final = "unit_ventilation"
CONF_UNIT_HEAT_PUMP: Final = "unit_heat_pump"

# The installation this library was transcribed from uses unit 1 for the
# ventilation controller and unit 2 for the heat pump; both are configurable
# in case another installation differs.
DEFAULT_UNIT_VENTILATION: Final = 1
DEFAULT_UNIT_HEAT_PUMP: Final = 2

# A ventilation/heat-pump controller changes slowly; poll conservatively.
SCAN_INTERVAL: Final = timedelta(seconds=30)

# The real unit sits behind a slow RS232-to-Modbus-TCP gateway: back-to-back
# requests with no pacing at all made it return responses under stale/mismatched
# transaction IDs (live-tested against the real hardware). 300ms between
# requests eliminated that entirely; unset (0) leaves pacing to pymodbus, which
# is not enough for this gateway.
MESSAGE_SPACING_SECONDS: Final = 0.3
