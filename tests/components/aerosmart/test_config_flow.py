"""Tests for the aerosmart config flow."""

from unittest.mock import AsyncMock

import pytest

from homeassistant import config_entries
from homeassistant.components.aerosmart.const import (
    CONF_CONNECTION,
    CONF_UNIT_HEAT_PUMP,
    CONF_UNIT_VENTILATION,
    DOMAIN,
)
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from tests.common import MockConfigEntry


@pytest.mark.usefixtures("mock_modbus_unit_ventilation", "mock_modbus_unit_heat_pump")
async def test_full_flow(
    hass: HomeAssistant,
    connection_entry: MockConfigEntry,
    mock_setup_entry: AsyncMock,
) -> None:
    """A valid connection and both unit IDs create an entry."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_CONNECTION: connection_entry.entry_id,
            CONF_UNIT_VENTILATION: 1,
            CONF_UNIT_HEAT_PUMP: 2,
        },
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "aerosmart"
    assert result["data"] == {
        CONF_CONNECTION: connection_entry.entry_id,
        CONF_UNIT_VENTILATION: 1,
        CONF_UNIT_HEAT_PUMP: 2,
    }
    mock_setup_entry.assert_called_once()


async def test_cannot_connect(
    hass: HomeAssistant, connection_entry: MockConfigEntry
) -> None:
    """An unreachable unit shows a form error instead of aborting."""
    await connection_entry.runtime_data.close()

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_CONNECTION: connection_entry.entry_id,
            CONF_UNIT_VENTILATION: 1,
            CONF_UNIT_HEAT_PUMP: 2,
        },
    )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "cannot_connect"}
