"""Diagnostics support for aerosmart."""

from typing import Any

from homeassistant.core import HomeAssistant

from .binary_sensor import BINARY_SENSOR_DESCRIPTIONS
from .coordinator import AerosmartConfigEntry
from .number import NUMBER_DESCRIPTIONS
from .select import SELECT_DESCRIPTIONS
from .sensor import SENSOR_DESCRIPTIONS
from .switch import SWITCH_DESCRIPTIONS

_ALL_DESCRIPTIONS = (
    SENSOR_DESCRIPTIONS
    + BINARY_SENSOR_DESCRIPTIONS
    + NUMBER_DESCRIPTIONS
    + SELECT_DESCRIPTIONS
    + SWITCH_DESCRIPTIONS
)


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: AerosmartConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry.

    Reads every known register the same way its entity would -- via the
    description's ``component``/``attribute`` pair -- instead of introspecting
    ``aerosmart_modbus`` internals, so this stays correct regardless of how
    that library stores field values.
    """
    coordinator = entry.runtime_data
    device = coordinator.data

    registers: dict[str, Any] = {}
    for description in _ALL_DESCRIPTIONS:
        subsystem = getattr(device, description.component)
        registers[description.key] = getattr(subsystem, description.attribute)

    return {
        "entry_data": {
            "connection_entry_id": entry.data["connection_entry_id"],
            "unit_ventilation": entry.data["unit_ventilation"],
            "unit_heat_pump": entry.data["unit_heat_pump"],
        },
        "last_update_success": coordinator.last_update_success,
        "registers": registers,
    }
