"""The esp-thermostat integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from . import hub

# For your initial PR, limit it to 1 platform.
PLATFORMS = [Platform.SENSOR]


type HubConfigEntry = ConfigEntry[hub.Hub]


async def async_setup_entry(hass: HomeAssistant, entry: HubConfigEntry) -> bool:
    """Set up esp-thermostat from a config entry."""

    entry.runtime_data = hub.Hub(hass, entry.data["host"])

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
