"""Tests for the aerosmart select platform."""

import pytest

from homeassistant.components.select import (
    ATTR_OPTION,
    DOMAIN as SELECT_DOMAIN,
    SERVICE_SELECT_OPTION,
)
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.core import HomeAssistant

from tests.common import MockConfigEntry


@pytest.mark.usefixtures(
    "entity_registry_enabled_by_default",
    "mock_modbus_unit_ventilation",
    "mock_modbus_unit_heat_pump",
)
async def test_select_option(
    hass: HomeAssistant, mock_config_entry: MockConfigEntry
) -> None:
    """Selecting a Betriebsart option writes its underlying enum code."""
    mock_config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    entity_id = "select.aerosmart_betriebsart"
    await hass.services.async_call(
        SELECT_DOMAIN,
        SERVICE_SELECT_OPTION,
        {ATTR_ENTITY_ID: entity_id, ATTR_OPTION: "Party"},
        blocking=True,
    )

    state = hass.states.get(entity_id)
    assert state is not None
    assert state.state == "Party"
