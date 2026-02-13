{% if prerelease %}
### NB: This is a beta version
{% endif %}

_Create humidex and comfort sensors from temperature and humidity entities._

## Features
- Supports Celsius and Fahrenheit temperature sources
- Creates numeric humidex score sensor
- Creates comfort rating sensor
- UI configuration flow
- Automatic import of legacy YAML entries

{% if not installed %}
## Installation
1. Click install.
2. Restart Home Assistant.
3. Go to `Settings -> Devices & services`.
4. Click `Add Integration` and search for `Humidex`.
{% endif %}
