"""Config flow for aerosmart."""

from typing import Any, override

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

# A named tuple, not an inline `except (A, B, C):` -- ruff's formatter has a
# bug where it strips the required parentheses from a multi-type except
# clause, producing invalid Python 2-style syntax. Referencing a module-level
# constant instead sidesteps it.
_CONNECT_ERRORS = (ConnectionNotReady, ModbusError, OSError, ValueError)

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

    @override
    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Pick a Modbus connection and both unit IDs."""
        return await self._async_step_connection(user_input, step_id="user")

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Change the Modbus connection and/or either unit ID of an existing entry."""
        return await self._async_step_connection(user_input, step_id="reconfigure")

    async def _async_step_connection(
        self, user_input: dict[str, Any] | None, *, step_id: str
    ) -> ConfigFlowResult:
        """Shared body for the initial and reconfigure steps.

        The unique ID is derived from exactly the fields this form lets the
        user change, so a reconfigure that doesn't touch any field recomputes
        the *same* unique ID as the entry being reconfigured -- checking that
        against ``_abort_if_unique_id_configured`` would always find itself
        and incorrectly abort. Only run the duplicate check when the
        recomputed unique ID actually differs from the reconfigured entry's
        current one.
        """
        errors: dict[str, str] = {}
        if user_input is not None:
            await self.async_set_unique_id(
                f"{user_input[CONF_CONNECTION]}"
                f"_{int(user_input[CONF_UNIT_VENTILATION])}"
                f"_{int(user_input[CONF_UNIT_HEAT_PUMP])}"
            )
            if step_id == "reconfigure":
                reconfigure_entry = self._get_reconfigure_entry()
                if self.unique_id != reconfigure_entry.unique_id:
                    self._abort_if_unique_id_configured()
            else:
                self._abort_if_unique_id_configured()

            if not await self._async_can_connect(user_input):
                errors["base"] = "cannot_connect"
            elif step_id == "reconfigure":
                return self.async_update_reload_and_abort(
                    self._get_reconfigure_entry(), data=user_input
                )
            else:
                return self.async_create_entry(title="aerosmart", data=user_input)

        schema = STEP_USER
        if step_id == "reconfigure":
            # Prefill with what the user just submitted (so a validation error
            # doesn't discard their input); fall back to the entry's current
            # data on the form's first display.
            suggested = user_input or self._get_reconfigure_entry().data
            schema = self.add_suggested_values_to_schema(schema, suggested)
        return self.async_show_form(step_id=step_id, data_schema=schema, errors=errors)

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
        except _CONNECT_ERRORS:
            return False
        return True
