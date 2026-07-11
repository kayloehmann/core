"""Number platform for aerosmart (writable setpoints).

Every entity here is disabled by default: writability was inferred from the
source register's name, not a manufacturer specification, and must be
verified against the real unit before being relied on.
"""

from dataclasses import dataclass

from homeassistant.components.number import (
    NumberEntity,
    NumberEntityDescription,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .entity import AerosmartEntity
from .coordinator import AerosmartConfigEntry


@dataclass(frozen=True, kw_only=True)
class AerosmartNumberEntityDescription(NumberEntityDescription):
    """Describes an aerosmart number entity."""

    component: str
    attribute: str


NUMBER_DESCRIPTIONS: tuple[AerosmartNumberEntityDescription, ...] = (
    AerosmartNumberEntityDescription(
        key="boost_functions_ventilation_zeitspanne_function_heizung_plus",
        name="Zeitspanne Funktion HEIZUNG+",
        component="boost_functions_ventilation",
        attribute="zeitspanne_function_heizung_plus",
        entity_registry_enabled_default=False,
        native_unit_of_measurement="min",
    ),
    AerosmartNumberEntityDescription(
        key="boost_functions_ventilation_sollwert_erhoehung_function_heizung_plus",
        name="Sollwert-Erhöhung Funktion HEIZUNG+",
        component="boost_functions_ventilation",
        attribute="sollwert_erhoehung_function_heizung_plus",
        entity_registry_enabled_default=False,
        native_unit_of_measurement="K",
    ),
    AerosmartNumberEntityDescription(
        key="boost_functions_ventilation_zeitspanne_function_party",
        name="Zeitspanne Funktion PARTY",
        component="boost_functions_ventilation",
        attribute="zeitspanne_function_party",
        entity_registry_enabled_default=False,
        native_unit_of_measurement="min",
    ),
    AerosmartNumberEntityDescription(
        key="ventilation_erhoehung_luefterstufe_3",
        name="Erhöhung der Lüfterstufe 3 (R/W)",
        component="ventilation",
        attribute="erhoehung_luefterstufe_3",
        entity_registry_enabled_default=False,
        native_unit_of_measurement="%",
    ),
    AerosmartNumberEntityDescription(
        key="ventilation_soll_volumenstrom_luefterstufe2",
        name="Soll-Volumenstrom Lüfterstufe 2 (read/write)",
        component="ventilation",
        attribute="soll_volumenstrom_luefterstufe2",
        entity_registry_enabled_default=False,
        native_unit_of_measurement="m³/h",
    ),
    AerosmartNumberEntityDescription(
        key="room_temperature_temp_raumluft_soll",
        name="Temperatur Raumluft Soll",
        component="room_temperature",
        attribute="temp_raumluft_soll",
        entity_registry_enabled_default=False,
        native_unit_of_measurement="°C",
    ),
    AerosmartNumberEntityDescription(
        key="summer_bypass_sommerautomatik_schaltpunkt1",
        name="Sommerautomatik Schaltpunkt 1",
        component="summer_bypass",
        attribute="sommerautomatik_schaltpunkt1",
        entity_registry_enabled_default=False,
    ),
    AerosmartNumberEntityDescription(
        key="summer_bypass_sommerautomatik_schaltpunkt2",
        name="Sommerautomatik Schaltpunkt 2",
        component="summer_bypass",
        attribute="sommerautomatik_schaltpunkt2",
        entity_registry_enabled_default=False,
    ),
    AerosmartNumberEntityDescription(
        key="summer_bypass_sommerautomatik_schaltpunkt3",
        name="Sommerautomatik Schaltpunkt 3",
        component="summer_bypass",
        attribute="sommerautomatik_schaltpunkt3",
        entity_registry_enabled_default=False,
    ),
    AerosmartNumberEntityDescription(
        key="summer_bypass_sommerautomatik_schaltpunkt4",
        name="Sommerautomatik Schaltpunkt 4",
        component="summer_bypass",
        attribute="sommerautomatik_schaltpunkt4",
        entity_registry_enabled_default=False,
    ),
    AerosmartNumberEntityDescription(
        key="hot_water_heat_pump_wp_brauchwasser_soll_temp",
        name="Brauchwasser Solltemperatur",
        component="hot_water_heat_pump",
        attribute="wp_brauchwasser_soll_temp",
        entity_registry_enabled_default=False,
        native_unit_of_measurement="°C",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: AerosmartConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up aerosmart numbers."""
    coordinator = entry.runtime_data
    async_add_entities(
        AerosmartNumber(coordinator, description)
        for description in NUMBER_DESCRIPTIONS
    )


class AerosmartNumber(AerosmartEntity, NumberEntity):
    """A writable aerosmart setpoint."""

    entity_description: AerosmartNumberEntityDescription

    @property
    def native_value(self) -> float | int | None:
        """Return the register's current value."""
        return getattr(self._subsystem, self.entity_description.attribute)

    async def async_set_native_value(self, value: float) -> None:
        """Write the new setpoint and refresh."""
        await self._subsystem.write(self.entity_description.attribute, value)
        await self.coordinator.async_request_refresh()
