"""Tests for the aerosmart switch platform."""

import pytest

from homeassistant.components.switch import (
    DOMAIN as SWITCH_DOMAIN,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
)
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.core import HomeAssistant

from tests.common import MockConfigEntry


@pytest.mark.usefixtures(
    "entity_registry_enabled_by_default",
    "mock_modbus_unit_ventilation",
    "mock_modbus_unit_heat_pump",
)
async def test_turn_on(hass: HomeAssistant, mock_config_entry: MockConfigEntry) -> None:
    """Turning a boost-function switch on writes 1 to its register."""
    mock_config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    entity_id = "switch.aerosmart_funktion_heizung"
    await hass.services.async_call(
        SWITCH_DOMAIN,
        SERVICE_TURN_ON,
        {ATTR_ENTITY_ID: entity_id},
        blocking=True,
    )

    assert hass.states.get(entity_id).state == "on"


@pytest.mark.usefixtures(
    "entity_registry_enabled_by_default",
    "mock_modbus_unit_ventilation",
    "mock_modbus_unit_heat_pump",
)
async def test_turn_off(
    hass: HomeAssistant, mock_config_entry: MockConfigEntry
) -> None:
    """Turning a boost-function switch off writes 0 to its register."""
    mock_config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    entity_id = "switch.aerosmart_funktion_heizung"
    await hass.services.async_call(
        SWITCH_DOMAIN,
        SERVICE_TURN_OFF,
        {ATTR_ENTITY_ID: entity_id},
        blocking=True,
    )

    assert hass.states.get(entity_id).state == "off"
