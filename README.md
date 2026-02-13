# Humidex for Home Assistant

Custom integration that creates two sensors from a temperature source and humidity source:
- Numeric humidex score
- Comfort rating (`Comfortable`, `Some discomfort`, etc.)

## Installation

### HACS (recommended)
1. Add `https://github.com/geckom/ha-humidex` as a custom repository in HACS.
2. Install the integration.
3. Restart Home Assistant.
4. Go to `Settings -> Devices & services -> Add Integration`.
5. Search for `Humidex` and complete setup.

### Manual
1. Copy `custom_components/humidex` into your Home Assistant `custom_components` directory.
2. Restart Home Assistant.
3. Add the integration from `Settings -> Devices & services`.

## GUI Setup

The integration setup form asks for:
- `Temperature entity` (supports Celsius and Fahrenheit source values)
- `Humidity entity`
- Optional display name
- Optional comfort icon override

After setup, two entities are created:
- `<Name> Humidex` (numeric score, exposed as temperature)
- `<Name> Comfort` (comfort rating enum)

## YAML Migration

Legacy YAML configuration is still accepted temporarily and automatically imported into a UI config entry:

```yaml
sensor:
  - platform: humidex
    name: Study
    temperature: sensor.study_air_temperature
    humidity: sensor.study_humidity
    icon: mdi:gauge
```

When Home Assistant starts, this YAML entry is imported into the integration UI flow. YAML support is deprecated and should be removed from `configuration.yaml` after import.

## Troubleshooting

```yaml
logger:
  default: info
  logs:
    custom_components.humidex: debug
```

## Icon assets

- HACS assets are included at repo root: `icon.png` and `logo.png`.
- Home Assistant integration icons in the UI are sourced from the `home-assistant/brands` repository. Matching assets are included in `.github/brands/humidex/` for submission.
