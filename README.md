*Please :star: this repo if you find it useful*

# Sensor of Humidex for Home Assistant

## Installation

### Install from HACS (recommended)

1. Use HACS after adding this `https://github.com/geckom/ha-humidex` as a custom repository. Skip to 7.
2. If no HACS, use the tool of choice to open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
3. If you do not have a `custom_components` directory (folder) there, you need to create it.
4. In the `custom_components` directory (folder) create a new folder called `humidex`.
5. Download _all_ the files from the `custom_components/humidex/` directory (folder) in this repository.
6. Place the files you downloaded in the new directory (folder) you created.
7. Update your configuration.yaml as per below.
8. Restart Home Assistant.

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

