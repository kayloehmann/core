"""Tests for the aerosmart number platform."""

import pytest

from homeassistant.components.number import (
    ATTR_VALUE,
    DOMAIN as NUMBER_DOMAIN,
    SERVICE_SET_VALUE,
)
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.core import HomeAssistant

from tests.common import MockConfigEntry


@pytest.mark.usefixtures(
    "entity_registry_enabled_by_default",
    "mock_modbus_unit_ventilation",
    "mock_modbus_unit_heat_pump",
)
async def test_set_native_value(
    hass: HomeAssistant, mock_config_entry: MockConfigEntry
) -> None:
    """Writing a setpoint updates the register and refreshes the entity."""
    mock_config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    entity_id = "number.aerosmart_brauchwasser_solltemperatur"
    await hass.services.async_call(
        NUMBER_DOMAIN,
        SERVICE_SET_VALUE,
        {ATTR_ENTITY_ID: entity_id, ATTR_VALUE: 52.0},
        blocking=True,
    )

    state = hass.states.get(entity_id)
    assert state is not None
    assert state.state == "52.0"
