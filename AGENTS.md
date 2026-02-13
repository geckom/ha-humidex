# AGENTS

This repository contains a Home Assistant custom integration (`humidex`) with HACS distribution.

## Project Goals
- Provide a modern config-entry integration for Humidex.
- Create two entities per config entry:
  - `<Name> Humidex` (numeric humidex value)
  - `<Name> Humidex Comfort` (comfort classification)
- Support temperature sources in Celsius and Fahrenheit.
- Maintain temporary YAML import/migration support.

## Repository Structure
- `custom_components/humidex/`: integration source code
- `custom_components/humidex/translations/`: localization files
- `hacs.json`: HACS metadata
- `icon.png`, `logo.png`: HACS assets
- `.github/brands/humidex/`: assets for Home Assistant brands submission

## Development Rules
- Follow Home Assistant developer conventions first.
- Keep config flow UI-first; avoid introducing new YAML-only features.
- Preserve backwards compatibility for YAML import unless removal is explicitly planned.
- Ensure all Python modules/functions/classes have clear docstrings.
- Use stable `unique_id` behavior for config entries and entities.

## Validation Checklist
- `python3 -m compileall custom_components/humidex`
- Validate JSON files are well-formed:
  - `custom_components/humidex/manifest.json`
  - `custom_components/humidex/strings.json`
  - `custom_components/humidex/translations/en.json`
  - `hacs.json`
- Confirm setup flow filters selectors to:
  - Temperature sensors only for temperature input
  - Humidity sensors only for humidity input

## Release Notes Expectations
When behavior changes, update:
- `README.md` usage and migration notes
- `info.md` summary for HACS
- integration version in `custom_components/humidex/manifest.json`
