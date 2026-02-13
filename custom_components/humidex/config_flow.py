"""Config flow for the Humidex integration."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import voluptuous as vol

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_ICON, CONF_NAME
from homeassistant.helpers import selector

from .const import (
    CONF_HUMIDITY,
    CONF_TEMPERATURE,
    DEFAULT_COMFORT_ICON,
    DEFAULT_NAME,
    DOMAIN,
)


def _entry_unique_id(temperature: str, humidity: str) -> str:
    return f"{temperature}|{humidity}"


def _build_schema(user_input: Mapping[str, Any] | None = None) -> vol.Schema:
    data = user_input or {}

    return vol.Schema(
        {
            vol.Optional(CONF_NAME, default=data.get(CONF_NAME, DEFAULT_NAME)): selector.TextSelector(
                selector.TextSelectorConfig(type=selector.TextSelectorType.TEXT)
            ),
            vol.Required(
                CONF_TEMPERATURE,
                default=data.get(CONF_TEMPERATURE),
            ): selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain=["sensor"],
                    device_class=[SensorDeviceClass.TEMPERATURE],
                )
            ),
            vol.Required(
                CONF_HUMIDITY,
                default=data.get(CONF_HUMIDITY),
            ): selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain=["sensor"],
                    device_class=[SensorDeviceClass.HUMIDITY],
                )
            ),
            vol.Optional(CONF_ICON, default=data.get(CONF_ICON, DEFAULT_COMFORT_ICON)): selector.IconSelector(),
        }
    )


class HumidexConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Humidex."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        """Handle the initial step."""
        if user_input is not None:
            await self.async_set_unique_id(
                _entry_unique_id(user_input[CONF_TEMPERATURE], user_input[CONF_HUMIDITY])
            )
            self._abort_if_unique_id_configured()

            title = user_input.get(CONF_NAME) or DEFAULT_NAME
            data = {
                CONF_TEMPERATURE: user_input[CONF_TEMPERATURE],
                CONF_HUMIDITY: user_input[CONF_HUMIDITY],
                CONF_ICON: user_input.get(CONF_ICON, DEFAULT_COMFORT_ICON),
            }
            return self.async_create_entry(title=title, data=data)

        return self.async_show_form(step_id="user", data_schema=_build_schema())

    async def async_step_import(self, import_config: dict[str, Any]):
        """Import configuration from YAML."""
        await self.async_set_unique_id(
            _entry_unique_id(import_config[CONF_TEMPERATURE], import_config[CONF_HUMIDITY])
        )
        self._abort_if_unique_id_configured()

        title = import_config.get(CONF_NAME) or DEFAULT_NAME
        data = {
            CONF_TEMPERATURE: import_config[CONF_TEMPERATURE],
            CONF_HUMIDITY: import_config[CONF_HUMIDITY],
            CONF_ICON: import_config.get(CONF_ICON, DEFAULT_COMFORT_ICON),
        }
        return self.async_create_entry(title=title, data=data)

    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None):
        """Handle reconfiguration from the UI."""
        entry = self._get_reconfigure_entry()

        if user_input is not None:
            await self.async_set_unique_id(
                _entry_unique_id(user_input[CONF_TEMPERATURE], user_input[CONF_HUMIDITY])
            )
            self._abort_if_unique_id_mismatch(reason="already_configured")

            title = user_input.get(CONF_NAME) or DEFAULT_NAME
            data_updates = {
                CONF_TEMPERATURE: user_input[CONF_TEMPERATURE],
                CONF_HUMIDITY: user_input[CONF_HUMIDITY],
                CONF_ICON: user_input.get(CONF_ICON, DEFAULT_COMFORT_ICON),
            }

            self.hass.config_entries.async_update_entry(
                entry,
                title=title,
                data=data_updates,
                unique_id=self.unique_id,
            )
            await self.hass.config_entries.async_reload(entry.entry_id)
            return self.async_abort(reason="reconfigure_successful")

        current_values: dict[str, Any] = {
            CONF_NAME: entry.title,
            CONF_TEMPERATURE: entry.data[CONF_TEMPERATURE],
            CONF_HUMIDITY: entry.data[CONF_HUMIDITY],
            CONF_ICON: entry.data.get(CONF_ICON, DEFAULT_COMFORT_ICON),
        }

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=_build_schema(current_values),
        )
