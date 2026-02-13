"""Constants for the Humidex integration."""

from homeassistant.const import Platform

DOMAIN = "humidex"

PLATFORMS = [Platform.SENSOR]

DEFAULT_NAME = "Humidex"
DEFAULT_COMFORT_ICON = "mdi:gauge"

CONF_TEMPERATURE = "temperature"
CONF_HUMIDITY = "humidity"

COMFORT_NO_SIGNIFICANT = "No significant discomfort"
COMFORT_COMFORTABLE = "Comfortable"
COMFORT_SOME_DISCOMFORT = "Some discomfort"
COMFORT_AVOID_EXERTION = "Avoid exertion"
COMFORT_DANGEROUS = "Dangerous"
COMFORT_HEAT_STROKE = "Heat stroke imminent"

COMFORT_LEVELS = [
    COMFORT_NO_SIGNIFICANT,
    COMFORT_COMFORTABLE,
    COMFORT_SOME_DISCOMFORT,
    COMFORT_AVOID_EXERTION,
    COMFORT_DANGEROUS,
    COMFORT_HEAT_STROKE,
]
