"""Tests for the aerosmart config-entry setup."""

from unittest.mock import patch

from modbus_connection.mock import MockModbusConnection

from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant

from tests.common import MockConfigEntry


async def test_setup_entry_creates_entities(
    hass: HomeAssistant, mock_config_entry: MockConfigEntry
) -> None:
    """The entry loads and produces entities across every platform."""
    mock_config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    assert mock_config_entry.state is ConfigEntryState.LOADED

    wochentag = hass.states.get("sensor.aerosmart_wochentag")
    assert wochentag is not None
    assert wochentag.state == "3"

    outside_temp = hass.states.get("sensor.aerosmart_temperatur_aussenluft")
    assert outside_temp is not None
    assert outside_temp.state == "0.123"


async def test_reloads_on_connection_lost(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_modbus_connection: MockModbusConnection,
) -> None:
    """Losing the shared connection reloads the entry to re-borrow units."""
    mock_config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    with patch.object(hass.config_entries, "async_schedule_reload") as schedule_reload:
        mock_modbus_connection.simulate_connection_lost()
        await hass.async_block_till_done()

    # modbus_connection also reloads itself to rebuild the dropped connection,
    # so aerosmart's own reload is one call among others, not the only one.
    schedule_reload.assert_any_call(mock_config_entry.entry_id)


async def test_coordinator_update_failure(
    hass: HomeAssistant,
    connection_entry: MockConfigEntry,
    mock_config_entry: MockConfigEntry,
) -> None:
    """A Modbus error during a periodic refresh marks the update failed."""
    mock_config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    await connection_entry.runtime_data.close()
    coordinator = mock_config_entry.runtime_data
    await coordinator.async_refresh()

    assert coordinator.last_update_success is False
