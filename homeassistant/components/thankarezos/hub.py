"""A demonstration 'hub' that connects several devices."""

import asyncio
from collections.abc import Callable
import random

from homeassistant.core import HomeAssistant


class Hub:
    """Dummy hub for Hello World example."""

    manufacturer = "Demonstration Corp"

    def __init__(self, hass: HomeAssistant, host: str) -> None:
        """Init dummy hub."""
        self._host = host
        self._hass = hass
        self._name = host
        self._id = host.lower()
        self.thermostats = [
            Thermostat(f"{self._id}_1", f"{self._name} Thermostat 1", self),
            Thermostat(f"{self._id}_2", f"{self._name} Thermostat 2", self),
            Thermostat(f"{self._id}_3", f"{self._name} Thermostat 3", self),
        ]
        self.online = True

    @property
    def hub_id(self) -> str:
        """ID for dummy hub."""
        return self._id

    async def test_connection(self) -> bool:
        """Test connectivity to the Dummy hub is OK."""
        await asyncio.sleep(1)
        return True


class Thermostat:
    """Dummy thermostat (device for HA) example."""

    def __init__(self, thermostat_id: str, name: str, hub: Hub) -> None:
        """Initialize dummy thermostat."""
        self._id = thermostat_id
        self.hub = hub
        self.name = name
        self._callbacks: set[Callable[[], None]] = set()
        self._loop = asyncio.get_event_loop()
        self._target_temperature = 22  # Default target temperature in Celsius
        self._current_temperature = 22  # Current temperature in Celsius

        # Some static information about this device
        self.firmware_version = f"1.0.{random.randint(1, 9)}"
        self.model = "Test Thermostat"

    @property
    def thermostat_id(self) -> str:
        """Return ID for thermostat."""
        return self._id

    @property
    def current_temperature(self):
        """Return current temperature."""
        return self._current_temperature

    @property
    def target_temperature(self):
        """Return target temperature."""
        return self._target_temperature

    async def set_temperature(self, temperature: int) -> None:
        """Set thermostat to the given temperature."""
        self._target_temperature = temperature

        # Simulate a delay and then update the current temperature
        await self.publish_updates()
        self._loop.create_task(self.delayed_update())

    async def delayed_update(self) -> None:
        """Simulate temperature change delay."""
        await asyncio.sleep(random.randint(1, 5))
        self._current_temperature = self._target_temperature
        await self.publish_updates()

    def register_callback(self, callback: Callable[[], None]) -> None:
        """Register callback, called when temperature changes."""
        self._callbacks.add(callback)

    def remove_callback(self, callback: Callable[[], None]) -> None:
        """Remove previously registered callback."""
        self._callbacks.discard(callback)

    async def publish_updates(self) -> None:
        """Call all registered callbacks."""
        for callback in self._callbacks:
            callback()

    @property
    def online(self) -> bool:
        """Thermostat is online."""
        return random.random() > 0.1
