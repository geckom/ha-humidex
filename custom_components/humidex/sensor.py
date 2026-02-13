"""Humidex sensor platform."""

from __future__ import annotations

from collections.abc import Mapping
import logging
import math
from typing import Any

import voluptuous as vol

from homeassistant.components.sensor import (
    PLATFORM_SCHEMA,
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.const import (
    ATTR_UNIT_OF_MEASUREMENT,
    CONF_ICON,
    CONF_NAME,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event

from .const import (
    COMFORT_AVOID_EXERTION,
    COMFORT_COMFORTABLE,
    COMFORT_DANGEROUS,
    COMFORT_HEAT_STROKE,
    COMFORT_LEVELS,
    COMFORT_NO_SIGNIFICANT,
    COMFORT_SOME_DISCOMFORT,
    CONF_HUMIDITY,
    CONF_TEMPERATURE,
    DEFAULT_COMFORT_ICON,
    DEFAULT_NAME,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Required(CONF_TEMPERATURE): cv.entity_id,
        vol.Required(CONF_HUMIDITY): cv.entity_id,
        vol.Optional(CONF_ICON, default=DEFAULT_COMFORT_ICON): cv.icon,
    }
)


def _icon_for_comfort_level(level: str) -> str:
    if level in (COMFORT_NO_SIGNIFICANT, COMFORT_COMFORTABLE):
        return "mdi:gauge-empty"
    if level == COMFORT_SOME_DISCOMFORT:
        return "mdi:gauge-low"
    if level == COMFORT_AVOID_EXERTION:
        return "mdi:gauge"
    return "mdi:gauge-full"


def _to_celsius(value: float, unit: str | None, fallback_unit: UnitOfTemperature) -> float | None:
    normalized_unit = (unit or str(fallback_unit)).strip().lower()

    if normalized_unit in {"°c", "c", "celsius"}:
        return value
    if normalized_unit in {"°f", "f", "fahrenheit"}:
        return (value - 32.0) * (5.0 / 9.0)

    return None


def _calculate_humidex(temperature_c: float, humidity_pct: float) -> float:
    clamped_humidity = max(0.0, min(humidity_pct, 100.0))

    if clamped_humidity == 0.0:
        return temperature_c

    # Calculate dewpoint in Celsius.
    a = 17.27
    b = 237.7
    alpha = ((a * temperature_c) / (b + temperature_c)) + math.log(clamped_humidity / 100.0)
    dewpoint_c = (b * alpha) / (a - alpha)

    kelvin = 273.15
    temperature_k = temperature_c + kelvin
    dewpoint_k = dewpoint_c + kelvin

    vapor_pressure = 6.11 * math.exp(5417.7530 * ((1 / kelvin) - (1 / dewpoint_k)))
    humidex_c = temperature_k + (0.5555 * (vapor_pressure - 10.0)) - kelvin

    return max(humidex_c, temperature_c)


def _comfort_level_for_humidex(humidex_c: float) -> str:
    if humidex_c < 20:
        return COMFORT_NO_SIGNIFICANT
    if humidex_c < 30:
        return COMFORT_COMFORTABLE
    if humidex_c < 40:
        return COMFORT_SOME_DISCOMFORT
    if humidex_c < 46:
        return COMFORT_AVOID_EXERTION
    if humidex_c < 54:
        return COMFORT_DANGEROUS
    return COMFORT_HEAT_STROKE


def _normalized_base_name(entry_title: str) -> str:
    """Return a canonical base name ending with 'Humidex' exactly once."""
    base = entry_title.strip()
    if base.lower().endswith("humidex"):
        return f"{base[:-7].strip()} Humidex".strip()
    return f"{base} Humidex".strip()


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Humidex sensors from a config entry."""
    sensors = [
        HumidexScoreSensor(hass, entry),
        HumidexComfortSensor(hass, entry),
    ]
    async_add_entities(sensors)


async def async_setup_platform(
    hass: HomeAssistant,
    config: Mapping[str, Any],
    async_add_entities: AddEntitiesCallback,
    discovery_info: Mapping[str, Any] | None = None,
) -> None:
    """Import legacy YAML config into config entries."""
    _import_legacy_yaml_config(hass, config)


def setup_platform(
    hass: HomeAssistant,
    config: Mapping[str, Any],
    add_entities: AddEntitiesCallback,
    discovery_info: Mapping[str, Any] | None = None,
) -> None:
    """Import legacy YAML config into config entries from sync setup."""
    _import_legacy_yaml_config(hass, config)


def _import_legacy_yaml_config(hass: HomeAssistant, config: Mapping[str, Any]) -> None:
    """Queue a config flow import for legacy YAML."""
    _LOGGER.warning(
        "YAML configuration for humidex is deprecated and will be removed in a future release. "
        "Your config has been imported into the UI integration flow."
    )

    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": SOURCE_IMPORT},
            data={
                CONF_NAME: config.get(CONF_NAME, DEFAULT_NAME),
                CONF_TEMPERATURE: config[CONF_TEMPERATURE],
                CONF_HUMIDITY: config[CONF_HUMIDITY],
                CONF_ICON: config.get(CONF_ICON, DEFAULT_COMFORT_ICON),
            },
        )
    )


class HumidexBaseSensor(SensorEntity):
    """Base class for Humidex entities."""

    _attr_should_poll = False

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.hass = hass
        self._temperature_entity_id: str = entry.data[CONF_TEMPERATURE]
        self._humidity_entity_id: str = entry.data[CONF_HUMIDITY]
        self._comfort_icon: str = entry.data.get(CONF_ICON, DEFAULT_COMFORT_ICON)
        self._humidex_value: float | None = None
        self._comfort_level: str | None = None

    @property
    def available(self) -> bool:
        return self._humidex_value is not None and self._comfort_level is not None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        attributes: dict[str, Any] = {
            CONF_TEMPERATURE: self._temperature_entity_id,
            CONF_HUMIDITY: self._humidity_entity_id,
        }
        if self._humidex_value is not None:
            attributes["humidex"] = round(self._humidex_value, 2)
        if self._comfort_level is not None:
            attributes["comfort"] = self._comfort_level
        return attributes

    async def async_added_to_hass(self) -> None:
        """Set up listeners when entity is added to Home Assistant."""
        self.async_on_remove(
            async_track_state_change_event(
                self.hass,
                [self._temperature_entity_id, self._humidity_entity_id],
                self._async_source_state_changed,
            )
        )
        self._refresh_values()

    @callback
    def _async_source_state_changed(self, event) -> None:
        self._refresh_values()
        self.async_write_ha_state()

    @callback
    def _refresh_values(self) -> None:
        temp_state = self.hass.states.get(self._temperature_entity_id)
        humidity_state = self.hass.states.get(self._humidity_entity_id)

        if (
            temp_state is None
            or humidity_state is None
            or temp_state.state in (STATE_UNKNOWN, STATE_UNAVAILABLE)
            or humidity_state.state in (STATE_UNKNOWN, STATE_UNAVAILABLE)
        ):
            self._humidex_value = None
            self._comfort_level = None
            return

        try:
            temp_value = float(temp_state.state)
            humidity_pct = float(humidity_state.state)
        except ValueError:
            self._humidex_value = None
            self._comfort_level = None
            return

        temp_c = _to_celsius(
            temp_value,
            temp_state.attributes.get(ATTR_UNIT_OF_MEASUREMENT),
            self.hass.config.units.temperature_unit,
        )
        if temp_c is None:
            _LOGGER.debug(
                "Unsupported temperature unit '%s' on %s",
                temp_state.attributes.get(ATTR_UNIT_OF_MEASUREMENT),
                self._temperature_entity_id,
            )
            self._humidex_value = None
            self._comfort_level = None
            return

        self._humidex_value = _calculate_humidex(temp_c, humidity_pct)
        self._comfort_level = _comfort_level_for_humidex(self._humidex_value)


class HumidexScoreSensor(HumidexBaseSensor):
    """Numeric Humidex score sensor."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_suggested_display_precision = 1
    _attr_icon = "mdi:thermometer-lines"

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        super().__init__(hass, entry)
        base_name = _normalized_base_name(entry.title)
        self._attr_unique_id = f"{entry.entry_id}_humidex"
        self._attr_name = base_name

    @property
    def native_value(self) -> float | None:
        if self._humidex_value is None:
            return None
        return round(self._humidex_value, 1)


class HumidexComfortSensor(HumidexBaseSensor):
    """Comfort rating sensor derived from Humidex score."""

    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = COMFORT_LEVELS

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        super().__init__(hass, entry)
        base_name = _normalized_base_name(entry.title)
        self._attr_unique_id = f"{entry.entry_id}_comfort"
        self._attr_name = f"{base_name} Comfortable"

    @property
    def icon(self) -> str:
        if self._comfort_level is None:
            return self._comfort_icon
        return _icon_for_comfort_level(self._comfort_level)

    @property
    def native_value(self) -> str | None:
        return self._comfort_level

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        attributes = super().extra_state_attributes

        humidity_state = self.hass.states.get(self._humidity_entity_id)
        if humidity_state and humidity_state.state not in (STATE_UNKNOWN, STATE_UNAVAILABLE):
            try:
                attributes["humidity"] = float(humidity_state.state)
            except ValueError:
                pass

        return attributes
