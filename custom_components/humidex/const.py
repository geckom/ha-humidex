"""Constants for the Humidex integration."""

from homeassistant.const import Platform

DOMAIN = "humidex"

PLATFORMS = [Platform.SENSOR]

DEFAULT_NAME = "Humidex"
DEFAULT_COMFORT_ICON = "mdi:gauge"

CONF_TEMPERATURE = "temperature"
CONF_HUMIDITY = "humidity"

COMFORT_NO_SIGNIFICANT = "no_significant_discomfort"
COMFORT_COMFORTABLE = "comfortable"
COMFORT_SOME_DISCOMFORT = "some_discomfort"
COMFORT_AVOID_EXERTION = "avoid_exertion"
COMFORT_DANGEROUS = "dangerous"
COMFORT_HEAT_STROKE = "heat_stroke_imminent"

COMFORT_LEVELS = [
    COMFORT_NO_SIGNIFICANT,
    COMFORT_COMFORTABLE,
    COMFORT_SOME_DISCOMFORT,
    COMFORT_AVOID_EXERTION,
    COMFORT_DANGEROUS,
    COMFORT_HEAT_STROKE,
]
