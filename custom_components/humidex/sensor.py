from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (CONF_NAME, ATTR_ICON)
from homeassistant.helpers.entity import Entity

import homeassistant.helpers.config_validation as cv
from homeassistant.util.temperature import convert as convert_temperature

from homeassistant.const import (
        ATTR_UNIT_OF_MEASUREMENT,
        TEMP_CELSIUS,
)

import voluptuous as vol
import math

DOMAIN = 'humidex'

DEFAULT_NAME = 'Humidex'

CONF_TEMPERATURE = 'temperature'
CONF_HUMIDITY = 'humidity'


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_TEMPERATURE): cv.entity_id,
    vol.Required(CONF_HUMIDITY): cv.entity_id ,
    vol.Optional(ATTR_ICON, default='mdi:wifi-strength-outline'): cv.string
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    name = config.get(CONF_NAME)
    temp = config.get(CONF_TEMPERATURE)
    humid = config.get(CONF_HUMIDITY)
    icon = config.get(ATTR_ICON)

    add_devices([HumidexSensor(hass, name, temp, humid, icon)])




class HumidexSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass, name, temp, humid, icon):
        """Initialize the sensor."""
        self._hass = hass
        self._name = name
        self._temp = temp
        self._humid = humid
        self._icon = icon
        self._state = None
        self._humidex = None
        self._attributes = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return self._icon

    @property
    def device_state_attributes(self):
        """Return the state attributes of the monitored installation."""
        if self._attributes is not None:
            return self._attributes

    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        temperature = self._hass.states.get(self._temp)
        humidity = self._hass.states.get(self._humid)
    
        if temperature and humidity and temperature.state != 'unknown' and humidity.state != 'unknown':
            
            # Setup varaibles
            temp = float(temperature.state)
            humid = float(humidity.state)

            # Calculate kelvin from celcius or fahrenheit
            entity_unit = temperature.attributes.get(ATTR_UNIT_OF_MEASUREMENT)
            temp = convert_temperature(
                float(temp), entity_unit, TEMP_CELSIUS
            )

            # Calculate dewpoint
            A = 17.27
            B = 237.7
            alpha = ((A * temp) / (B + temp)) + math.log(humid/100.0)
            d = (B * alpha) / (A - alpha)

            # Calculate humidex
            kelvin = 273.15
            temperature = temp + kelvin
            dewpoint = d+kelvin
            # Calculate vapor pressure in mbar.
            e = 6.11 * math.exp(5417.7530 * ((1 / kelvin) - (1 / dewpoint)))
            # Calculate saturation vapor pressure
            es = 6.11 * math.exp(5417.7530 * ((1 / kelvin) - (1 / temperature)))
            humidity = e / es
            h = 0.5555 * (e - 10.0)
            humidex = temperature + h - kelvin
            self._attributes = {}
            self._attributes.update({"humidex": humidex})

            if humidex < temp:
                humidex = temp
            
            if humidex < 20:
                self._state = 'No significant'
                self._icon = 'mdi:gauge-empty'
            elif humidex < 30:
                self._state = 'Comfortable'
                self._icon = 'mdi:gauge-empty'
            elif humidex < 40:
                self._state = 'Some discomfort'
                self._icon = 'mdi:gauge-low'
            elif humidex < 46:
                self._state = 'Avoid exertion'
                self._icon = 'mdi:gauge'
            elif humidex < 54:
                self._state = 'Dangerous'
                self._icon = 'mdi:gauge-full'
            else:
                self._state = 'Heat stroke imminent'
                self._icon = 'mdi:gauge-full'
            #self._state = humidex
