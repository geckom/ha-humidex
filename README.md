# Humidex for Home Assistant

A Home Assistant custom integration that calculates humidex from temperature + relative humidity and exposes two entities:
- `<Name> Humidex` (numeric humidex score)
- `<Name> Humidex Comfort` (comfort rating enum)

## Features
- UI-first setup with config flow
- Reconfigure support from the integration UI
- Temperature source support for Celsius and Fahrenheit
- Automatic legacy YAML import into config entries
- Comfort sensor states support localization via Home Assistant translations
- HACS-ready packaging (`hacs.json`, `icon.png`, `logo.png`)
- Minimum Home Assistant version: `2024.8.0`

## Installation

### HACS (recommended)
1. In HACS, add `https://github.com/geckom/ha-humidex` as a custom repository.
2. Install `Humidex`.
3. Restart Home Assistant.
4. Go to `Settings -> Devices & services -> Add Integration`.
5. Search for `Humidex` and complete setup.

### Manual
1. Copy `custom_components/humidex` into your Home Assistant `custom_components` folder.
2. Restart Home Assistant.
3. Add `Humidex` from `Settings -> Devices & services`.

## GUI Setup

The setup form requires:
- `Temperature entity` (filtered to temperature-class sensors)
- `Humidity entity` (filtered to humidity-class sensors)

Optional fields:
- `Name`
- `Comfort icon`

## YAML Migration

Legacy YAML is still accepted temporarily and is imported automatically into a config entry.

```yaml
sensor:
  - platform: humidex
    name: Study
    temperature: sensor.study_air_temperature
    humidity: sensor.study_humidity
    icon: mdi:gauge
```

After import, remove the YAML block from `configuration.yaml`.

## Troubleshooting

```yaml
logger:
  default: info
  logs:
    custom_components.humidex: debug
```

## HACS Compatibility

This repository includes the standard assets and metadata HACS expects:
- `hacs.json`
- `custom_components/humidex/manifest.json`
- `icon.png`
- `logo.png`

## Integration Icon Note

Home Assistant integration tile icons shown in the core UI are sourced from the `home-assistant/brands` repository. Matching assets for submission are included in:
- `.github/brands/humidex/icon.png`
- `.github/brands/humidex/logo.png`
