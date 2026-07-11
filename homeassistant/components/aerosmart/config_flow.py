"""Config flow for aerosmart."""

from typing import Any

from aerosmart_modbus import AerosmartDevice
from modbus_connection import ModbusError
import voluptuous as vol

from homeassistant.components.modbus_connection import (
    ConnectionNotReady,
    async_get_unit,
)
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.selector import (
    ConfigEntrySelector,
    ConfigEntrySelectorConfig,
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
)

from .const import (
    CONF_CONNECTION,
    CONF_UNIT_HEAT_PUMP,
    CONF_UNIT_VENTILATION,
    DEFAULT_UNIT_HEAT_PUMP,
    DEFAULT_UNIT_VENTILATION,
    DOMAIN,
)

STEP_USER = vol.Schema(
    {
        vol.Required(CONF_CONNECTION): ConfigEntrySelector(
            ConfigEntrySelectorConfig(integration="modbus_connection")
        ),
        vol.Required(
            CONF_UNIT_VENTILATION, default=DEFAULT_UNIT_VENTILATION
        ): NumberSelector(
            NumberSelectorConfig(min=1, max=255, step=1, mode=NumberSelectorMode.BOX)
        ),
        vol.Required(
            CONF_UNIT_HEAT_PUMP, default=DEFAULT_UNIT_HEAT_PUMP
        ): NumberSelector(
            NumberSelectorConfig(min=1, max=255, step=1, mode=NumberSelectorMode.BOX)
        ),
    }
)


class AerosmartConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for aerosmart."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Pick a Modbus connection and both unit IDs."""
        errors: dict[str, str] = {}
        if user_input is not None:
            await self.async_set_unique_id(
                f"{user_input[CONF_CONNECTION]}"
                f"_{int(user_input[CONF_UNIT_VENTILATION])}"
                f"_{int(user_input[CONF_UNIT_HEAT_PUMP])}"
            )
            self._abort_if_unique_id_configured()
            if not await self._async_can_connect(user_input):
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(title="aerosmart", data=user_input)
        return self.async_show_form(
            step_id="user", data_schema=STEP_USER, errors=errors
        )

    async def _async_can_connect(self, data: dict[str, Any]) -> bool:
        """Probe both units by reading the general sub-system once."""
        try:
            unit_ventilation = async_get_unit(
                self.hass, data[CONF_CONNECTION], int(data[CONF_UNIT_VENTILATION])
            )
            unit_heat_pump = async_get_unit(
                self.hass, data[CONF_CONNECTION], int(data[CONF_UNIT_HEAT_PUMP])
            )
            device = AerosmartDevice(unit_ventilation, unit_heat_pump)
            await device.general.async_update()
        except (ConnectionNotReady, ModbusError, OSError, ValueError):
            return False
        return True
