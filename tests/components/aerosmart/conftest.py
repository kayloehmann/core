"""Fixtures for the aerosmart tests.

The ``mock_modbus_connection`` fixture comes from the ``modbus_connection``
library's pytest plugin (registered as a ``pytest11`` entry point). Seeding
both units' stores drives the real ``aerosmart_modbus`` library exactly as the
two physical Modbus units would.
"""

from collections.abc import Generator
from unittest.mock import AsyncMock, patch

from modbus_connection.mock import MockModbusConnection, MockModbusUnit
import pytest

from homeassistant.components.aerosmart.const import (
    CONF_CONNECTION,
    CONF_UNIT_HEAT_PUMP,
    CONF_UNIT_VENTILATION,
    DOMAIN,
)
from homeassistant.components.modbus_connection.const import (
    CONNECTION_TCP,
    DOMAIN as MODBUS_CONNECTION_DOMAIN,
)
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_TYPE
from homeassistant.core import HomeAssistant

from tests.common import MockConfigEntry

UNIT_VENTILATION = 1
UNIT_HEAT_PUMP = 2

# uint32 fields span 2 registers, big word order: [high_word, low_word].
VENTILATION_HOLDING: dict[int, list[int]] = {
    1174: [0, 3],  # general.wochentag
    202: [0, 123],  # outside_temperature.temp_aussenluft (scale 0.001 -> 0.123)
}
HEAT_PUMP_HOLDING: dict[int, list[int]] = {
    1044: [0, 1],  # heat_pump.waermepumpe
    212: [0, 45000],  # hot_water_heat_pump.warmwasser_speicher_oben (-> 45.0)
}


@pytest.fixture
def mock_modbus_unit_ventilation(
    mock_modbus_connection: MockModbusConnection,
) -> MockModbusUnit:
    """A seeded aerosmart ventilation unit (Modbus unit 1)."""
    unit = mock_modbus_connection.for_unit(UNIT_VENTILATION)
    for address, words in VENTILATION_HOLDING.items():
        unit.holding[address] = words
    return unit


@pytest.fixture
def mock_modbus_unit_heat_pump(
    mock_modbus_connection: MockModbusConnection,
) -> MockModbusUnit:
    """A seeded aerosmart heat pump unit (Modbus unit 2)."""
    unit = mock_modbus_connection.for_unit(UNIT_HEAT_PUMP)
    for address, words in HEAT_PUMP_HOLDING.items():
        unit.holding[address] = words
    return unit


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock]:
    """Prevent the created entry from actually setting up during flow tests."""
    with patch(
        "homeassistant.components.aerosmart.async_setup_entry",
        return_value=True,
    ) as mock_setup_entry:
        yield mock_setup_entry


@pytest.fixture
def mock_connect(
    mock_modbus_connection: MockModbusConnection,
) -> Generator[AsyncMock]:
    """Patch the modbus_connection backend to return the mock connection."""
    connect = AsyncMock(return_value=mock_modbus_connection)
    with (
        patch("homeassistant.components.modbus_connection.connect_tcp", connect),
        patch("homeassistant.components.modbus_connection.connect_serial", connect),
    ):
        yield connect


@pytest.fixture
async def connection_entry(
    hass: HomeAssistant,
    mock_connect: AsyncMock,
) -> MockConfigEntry:
    """Set up a loaded modbus_connection entry backed by the seeded mock."""
    entry = MockConfigEntry(
        domain=MODBUS_CONNECTION_DOMAIN,
        title="1.2.3.4:502",
        data={CONF_TYPE: CONNECTION_TCP, CONF_HOST: "1.2.3.4", CONF_PORT: 502},
    )
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    return entry


@pytest.fixture
def mock_config_entry(
    connection_entry: MockConfigEntry,
    mock_modbus_unit_ventilation: MockModbusUnit,
    mock_modbus_unit_heat_pump: MockModbusUnit,
) -> MockConfigEntry:
    """An aerosmart config entry pointing at ``connection_entry``."""
    return MockConfigEntry(
        domain=DOMAIN,
        title="aerosmart",
        unique_id=f"{connection_entry.entry_id}_{UNIT_VENTILATION}_{UNIT_HEAT_PUMP}",
        data={
            CONF_CONNECTION: connection_entry.entry_id,
            CONF_UNIT_VENTILATION: UNIT_VENTILATION,
            CONF_UNIT_HEAT_PUMP: UNIT_HEAT_PUMP,
        },
    )
