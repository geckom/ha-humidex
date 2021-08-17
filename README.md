*Please :star: this repo if you find it useful*

# Sensor of Humidex for Home Assistant

## Installation

### Install from HACS (recommended)

1. Have [HACS][hacs] installed, this will allow you to easily manage and track updates.
1. Search for "Temperature Feels Like".
1. Click Install below the found integration.

... then if you want to use `configuration.yaml` to configure sensor...
1. Add `humidex` sensor to your `configuration.yaml` file. See configuration examples below.
1. Restart Home Assistant

### Manual installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `humidex`.
1. Download file `humidex.zip` from the [latest release section][releases-latest] in this repository.
1. Extract _all_ files from this archive you downloaded in the directory (folder) you created.
1. Restart Home Assistant

... then if you want to use `configuration.yaml` to configure sensor...
1. Add `humidex` sensor to your `configuration.yaml` file. See configuration examples below.
1. Restart Home Assistant

### Configuration Examples

```yaml
# Example configuration.yaml entry
sensor:
  - platform: humidex
    temperature: sensor.study_air_temperature
    humidity: sensor.study_humidity
```

<p align="center">* * *</p>
I put a lot of work into making this repo and component available and updated to inspire and help others! I will be glad to receive thanks from you — it will give me new strength and add enthusiasm:

### Configuration Variables

**temperature:**\
  _(entity) (Required)_\
  Temperature provider entity ID. This can be celcius or fahreheit.

**humidity:**\
  _(entity) (Required)_\
  Humidity provider entity ID.

> **_Note_**:\
> Temperature and humidity values are both required for calculations.

## Track updates

You can automatically track new versions of this component and update it by [HACS][hacs].

## Troubleshooting

To enable debug logs use this configuration:
```yaml
# Example configuration.yaml entry
logger:
  default: info
  logs:
    custom_components.humidex: debug
```
... then restart HA.

## Contributions are welcome!

This is an active open-source project. We are always open to people who want to
use the code or contribute to it.

We have set up a separate document containing our
[contribution guidelines](CONTRIBUTING.md).

Thank you for being involved! :heart_eyes:

***

