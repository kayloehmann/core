"""The aerosmart integration.

aerosmart is a Modbus device. This integration does not own its connection: it
borrows two ``ModbusUnit`` handles (ventilation + heat pump) from a
``modbus_connection`` config entry chosen in the config flow, and hands them to
the ``aerosmart_modbus`` library. The ``modbus_connection`` entry owns the
connection lifecycle; this integration reloads when the connection drops so it
re-borrows on the rebuilt connection.
"""

from aerosmart_modbus import AerosmartDevice

from homeassistant.components.modbus_connection import async_get_unit
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import (
    CONF_CONNECTION,
    CONF_UNIT_HEAT_PUMP,
    CONF_UNIT_VENTILATION,
    MESSAGE_SPACING_SECONDS,
)
from .coordinator import AerosmartConfigEntry, AerosmartCoordinator

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.NUMBER,
    Platform.SWITCH,
    Platform.SELECT,
]


async def async_setup_entry(hass: HomeAssistant, entry: AerosmartConfigEntry) -> bool:
    """Set up aerosmart from a config entry.

    ``async_get_unit`` raises ``ConnectionNotReady`` (a ``ConfigEntryNotReady``)
    if the shared connection is missing or not loaded; letting it propagate gives
    Home Assistant's setup retry.
    """
    unit_ventilation = async_get_unit(
        hass, entry.data[CONF_CONNECTION], entry.data[CONF_UNIT_VENTILATION]
    )
    unit_heat_pump = async_get_unit(
        hass, entry.data[CONF_CONNECTION], entry.data[CONF_UNIT_HEAT_PUMP]
    )
    unit_ventilation.set_message_spacing(MESSAGE_SPACING_SECONDS)
    unit_heat_pump.set_message_spacing(MESSAGE_SPACING_SECONDS)
    device = AerosmartDevice(unit_ventilation, unit_heat_pump)
    coordinator = AerosmartCoordinator(hass, entry, device)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    # Both units are bound to modbus_connection's current connection. When that
    # connection drops, modbus_connection rebuilds it; reload so we re-borrow
    # fresh units on the rebuilt connection instead of holding dead ones.
    entry.async_on_unload(
        unit_ventilation.on_connection_lost(
            lambda: hass.config_entries.async_schedule_reload(entry.entry_id)
        )
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: AerosmartConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
