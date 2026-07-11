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
