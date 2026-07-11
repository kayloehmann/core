"""Binary sensor platform for aerosmart."""

from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .entity import AerosmartEntity
from .coordinator import AerosmartConfigEntry


@dataclass(frozen=True, kw_only=True)
class AerosmartBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes an aerosmart binary_sensor entity.

    The underlying register is a plain holding register, not a native Modbus
    coil -- ``is_on`` treats any non-zero value as True. This is a naming
    heuristic against an unverified register map, not a confirmed
    manufacturer specification.
    """

    component: str
    attribute: str


BINARY_SENSOR_DESCRIPTIONS: tuple[AerosmartBinarySensorEntityDescription, ...] = (
    AerosmartBinarySensorEntityDescription(
        key="general_relaykontakt_ext_lu",
        name="Relaiskontakt: EXT (LU)",
        component="general",
        attribute="relaykontakt_ext_lu",
    ),
    AerosmartBinarySensorEntityDescription(
        key="outside_temperature_aussenluftfuehler_vorhanden",
        name="Außenluftfühler vorhanden?",
        component="outside_temperature",
        attribute="aussenluftfuehler_vorhanden",
    ),
    AerosmartBinarySensorEntityDescription(
        key="outside_temperature_stoerung_temperaturfuehler_aussenluft",
        name="Störung: Temperaturfühler Außenluft",
        component="outside_temperature",
        attribute="stoerung_temperaturfuehler_aussenluft",
    ),
    AerosmartBinarySensorEntityDescription(
        key="outside_temperature_stoerung_temperaturfuehler_sole_aussenluft",
        name="Störung: Temperaturfühler Sole Außenluft",
        component="outside_temperature",
        attribute="stoerung_temperaturfuehler_sole_aussenluft",
    ),
    AerosmartBinarySensorEntityDescription(
        key="fire_alarm_brandmeldealarm",
        name="Brandmeldealarm",
        component="fire_alarm",
        attribute="brandmeldealarm",
    ),
    AerosmartBinarySensorEntityDescription(
        key="fire_alarm_brandmeldealarm_vorhanden",
        name="Brandmeldeanlage vorhanden?",
        component="fire_alarm",
        attribute="brandmeldealarm_vorhanden",
    ),
    AerosmartBinarySensorEntityDescription(
        key="fire_alarm_kontakt_brandmeldealarm",
        name="Kontakt: Brandmeldealarm",
        component="fire_alarm",
        attribute="kontakt_brandmeldealarm",
    ),
    AerosmartBinarySensorEntityDescription(
        key="carbon_dioxide_co2_sensor_available",
        name="CO2-Sensor vorhanden?",
        component="carbon_dioxide",
        attribute="co2_sensor_available",
    ),
    AerosmartBinarySensorEntityDescription(
        key="carbon_dioxide_stoerung_co2_sensor",
        name="Störung: CO2 Sensor",
        component="carbon_dioxide",
        attribute="stoerung_co2_sensor",
    ),
    AerosmartBinarySensorEntityDescription(
        key="utility_lockout_evu_vorhanden",
        name="EVU Anlage vorhanden?",
        component="utility_lockout",
        attribute="evu_vorhanden",
    ),
    AerosmartBinarySensorEntityDescription(
        key="utility_lockout_evu_sperre_brauchwasser_aktiv",
        name="EVU-Sperre Brauchwasser aktiv?",
        component="utility_lockout",
        attribute="evu_sperre_brauchwasser_aktiv",
    ),
    AerosmartBinarySensorEntityDescription(
        key="utility_lockout_evu_sperre_elektroheizstab_aktiv",
        name="EVU-Sperre Elektroheizstab aktiv?",
        component="utility_lockout",
        attribute="evu_sperre_elektroheizstab_aktiv",
    ),
    AerosmartBinarySensorEntityDescription(
        key="utility_lockout_evu_sperre_raumheizung_aktiv",
        name="EVU-Sperre Raumheizung aktiv?",
        component="utility_lockout",
        attribute="evu_sperre_raumheizung_aktiv",
    ),
    AerosmartBinarySensorEntityDescription(
        key="fine_dust_filter_feinstaubfilter_vorhanden",
        name="Feinstaubfilter vorhanden?",
        component="fine_dust_filter",
        attribute="feinstaubfilter_vorhanden",
    ),
    AerosmartBinarySensorEntityDescription(
        key="fine_dust_filter_feinstaubfilter_wechseln",
        name="Feinstaubfilter wechseln?",
        component="fine_dust_filter",
        attribute="feinstaubfilter_wechseln",
    ),
    AerosmartBinarySensorEntityDescription(
        key="coarse_dust_filter_grobstaubfilter_vorhanden",
        name="grobstaubfilter_vorhanden",
        component="coarse_dust_filter",
        attribute="grobstaubfilter_vorhanden",
    ),
    AerosmartBinarySensorEntityDescription(
        key="coarse_dust_filter_grobstaubfilter_wechseln",
        name="Grobstaubfilter wechseln?",
        component="coarse_dust_filter",
        attribute="grobstaubfilter_wechseln",
    ),
    AerosmartBinarySensorEntityDescription(
        key="cooling_kuehlung_vorhanden",
        name="Kühlung vorhanden?",
        component="cooling",
        attribute="kuehlung_vorhanden",
    ),
    AerosmartBinarySensorEntityDescription(
        key="ventilation_anforderung_abtauen",
        name="Anforderung: Abtauen (read)",
        component="ventilation",
        attribute="anforderung_abtauen",
    ),
    AerosmartBinarySensorEntityDescription(
        key="ventilation_anforderung_beschattung",
        name="Anforderung: Beschattung (read)",
        component="ventilation",
        attribute="anforderung_beschattung",
    ),
    AerosmartBinarySensorEntityDescription(
        key="ventilation_anforderung_st3_ext",
        name="Anforderung: LST3_EXT (read)",
        component="ventilation",
        attribute="anforderung_st3_ext",
    ),
    AerosmartBinarySensorEntityDescription(
        key="ventilation_stoerung_teilnehmer_nicht_erreichbar",
        name="Störung: Teilnehmer nicht erreichbar!",
        component="ventilation",
        attribute="stoerung_teilnehmer_nicht_erreichbar",
    ),
    AerosmartBinarySensorEntityDescription(
        key="ventilation_stoerung_temperaturfuehler_verdampferregister",
        name="Störung: Temperaturfühler Verdampferregister",
        component="ventilation",
        attribute="stoerung_temperaturfuehler_verdampferregister",
    ),
    AerosmartBinarySensorEntityDescription(
        key="ventilation_stoerung_waermepumpe_hochdruck",
        name="Störung: Wärmepumpe Hochdruck",
        component="ventilation",
        attribute="stoerung_waermepumpe_hochdruck",
    ),
    AerosmartBinarySensorEntityDescription(
        key="ventilation_stoerung_waermepumpe_niederdruck",
        name="Störung: Wärmepumpe Niederdruck",
        component="ventilation",
        attribute="stoerung_waermepumpe_niederdruck",
    ),
    AerosmartBinarySensorEntityDescription(
        key="ventilation_stoerung_wert_nicht_zulaessig",
        name="Störung: Wert nicht zulässig",
        component="ventilation",
        attribute="stoerung_wert_nicht_zulaessig",
    ),
    AerosmartBinarySensorEntityDescription(
        key="room_temperature_stoerung_temperaturfuehler_raum",
        name="Störung: Temperaturfühler Raum",
        component="room_temperature",
        attribute="stoerung_temperaturfuehler_raum",
    ),
    AerosmartBinarySensorEntityDescription(
        key="room_temperature_timeout_soll_temp_raum",
        name="Time-Out: Solltemperatur Raum",
        component="room_temperature",
        attribute="timeout_soll_temp_raum",
    ),
    AerosmartBinarySensorEntityDescription(
        key="room_temperature_timeout_temp_fuehler_raum",
        name="Time-Out: Temperaturfühler Raum",
        component="room_temperature",
        attribute="timeout_temp_fuehler_raum",
    ),
    AerosmartBinarySensorEntityDescription(
        key="room_temperature_anforderung_raum_heizstufe_1",
        name="Anforderung: Raum-Heizstufe 1 (read)",
        component="room_temperature",
        attribute="anforderung_raum_heizstufe_1",
    ),
    AerosmartBinarySensorEntityDescription(
        key="room_temperature_anforderung_raum_heizstufe_2",
        name="Anforderung: Raum-Heizstufe 2 (read)",
        component="room_temperature",
        attribute="anforderung_raum_heizstufe_2",
    ),
    AerosmartBinarySensorEntityDescription(
        key="summer_bypass_anforderung_sommerautomatik",
        name="Anforderung: Sommerautomatik (read)",
        component="summer_bypass",
        attribute="anforderung_sommerautomatik",
    ),
    AerosmartBinarySensorEntityDescription(
        key="summer_bypass_function_sommerautomatik",
        name="Funktion „Sommerautomatik“",
        component="summer_bypass",
        attribute="function_sommerautomatik",
    ),
    AerosmartBinarySensorEntityDescription(
        key="aggregate_fault_stoerung_summenstoerung",
        name="Störung: Summenstörung",
        component="aggregate_fault",
        attribute="stoerung_summenstoerung",
    ),
    AerosmartBinarySensorEntityDescription(
        key="aggregate_fault_stoerung_summenstoerung2",
        name="Störung: Summenstörung 2",
        component="aggregate_fault",
        attribute="stoerung_summenstoerung2",
    ),
    AerosmartBinarySensorEntityDescription(
        key="fans_anforderung_ventilatoren_durch_waermepumpe",
        name="Anforderung der Ventilatoren durch Wärmepumpe (read)",
        component="fans",
        attribute="anforderung_ventilatoren_durch_waermepumpe",
    ),
    AerosmartBinarySensorEntityDescription(
        key="fans_anforderung_ventilatoren_durch_zonenregelung",
        name="Anforderung der Ventilatoren durch Zonenregelung (read)",
        component="fans",
        attribute="anforderung_ventilatoren_durch_zonenregelung",
    ),
    AerosmartBinarySensorEntityDescription(
        key="fans_stoerung_zuluftventilator",
        name="Störung: Zuluftventilator",
        component="fans",
        attribute="stoerung_zuluftventilator",
    ),
    AerosmartBinarySensorEntityDescription(
        key="fans_stoerung_abluftventilator",
        name="Störung: Abluftventilator",
        component="fans",
        attribute="stoerung_abluftventilator",
    ),
    AerosmartBinarySensorEntityDescription(
        key="heat_pump_wp_kontakt_evu",
        name="Kontakt (EVU)",
        component="heat_pump",
        attribute="wp_kontakt_evu",
    ),
    AerosmartBinarySensorEntityDescription(
        key="heat_pump_wp_relaiskontakt_ext",
        name="Relaiskontakt: EXT (WP)",
        component="heat_pump",
        attribute="wp_relaiskontakt_ext",
    ),
    AerosmartBinarySensorEntityDescription(
        key="hot_water_ventilation_anforderung_disbalance_boilerueberwaermung",
        name="Anforderung Disbalance (Boilerüberwärmung) (read)",
        component="hot_water_ventilation",
        attribute="anforderung_disbalance_boilerueberwaermung",
    ),
    AerosmartBinarySensorEntityDescription(
        key="hot_water_ventilation_stoerung_elektroheizstab",
        name="Störung: Boilerfühler Elektroheizstab",
        component="hot_water_ventilation",
        attribute="stoerung_elektroheizstab",
    ),
    AerosmartBinarySensorEntityDescription(
        key="hot_water_ventilation_stoerung_boilerfuehler_waermepumpe",
        name="Störung: Boilerfühler Wärmepumpe",
        component="hot_water_ventilation",
        attribute="stoerung_boilerfuehler_waermepumpe",
    ),
    AerosmartBinarySensorEntityDescription(
        key="hot_water_ventilation_stoerung_boiler_uebertemperatur",
        name="Störung: Boilerübertemperatur",
        component="hot_water_ventilation",
        attribute="stoerung_boiler_uebertemperatur",
    ),
    AerosmartBinarySensorEntityDescription(
        key="hot_water_ventilation_anforderung_brauchwasserheizung_elektroheizstab",
        name="Anforderung: Brauchwasserheizung Elektoheizstab (read)",
        component="hot_water_ventilation",
        attribute="anforderung_brauchwasserheizung_elektroheizstab",
    ),
    AerosmartBinarySensorEntityDescription(
        key="hot_water_ventilation_anforderung_brauchwasserheizung_waermepumpe",
        name="Anforderung: Brauchwasserheizung Wärmepumpe (read)",
        component="hot_water_ventilation",
        attribute="anforderung_brauchwasserheizung_waermepumpe",
    ),
    AerosmartBinarySensorEntityDescription(
        key="hot_water_heat_pump_wp_elektroheizstab_vorhanden",
        name="Elektroheizstab vorhanden?",
        component="hot_water_heat_pump",
        attribute="wp_elektroheizstab_vorhanden",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: AerosmartConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up aerosmart binary sensors."""
    coordinator = entry.runtime_data
    async_add_entities(
        AerosmartBinarySensor(coordinator, description)
        for description in BINARY_SENSOR_DESCRIPTIONS
    )


class AerosmartBinarySensor(AerosmartEntity, BinarySensorEntity):
    """An aerosmart binary_sensor entity backed by a single register."""

    entity_description: AerosmartBinarySensorEntityDescription

    @property
    def is_on(self) -> bool | None:
        """Return True if the register's value is non-zero."""
        value = getattr(self._subsystem, self.entity_description.attribute)
        return None if value is None else bool(value)
