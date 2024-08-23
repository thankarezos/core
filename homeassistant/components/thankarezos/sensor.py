"""Platform for sensor integration."""

# This file shows the setup for the sensors associated with the cover.
# They are setup in the same way with the call to the async_setup_entry function
# via HA from the module __init__. Each sensor has a device_class, this tells HA how
# to display it in the UI (for know types). The unit_of_measurement property tells HA
# what the unit is, so it can display the correct range. For predefined types (such as
# battery), the unit_of_measurement should match what's expected.

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import HubConfigEntry
from .const import DOMAIN


# See cover.py for more details.
# Note how both entities for each roller sensor (battry and illuminance) are added at
# the same time to the same list. This way only a single async_add_devices call is
# required.
async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: HubConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add sensors for passed config_entry in HA."""
    hub = config_entry.runtime_data

    new_devices = [TemperatureSensor(thermostat) for thermostat in hub.thermostats]
    if new_devices:
        async_add_entities(new_devices)


class SensorBase(Entity):
    """Base representation of a Sensor."""

    should_poll = False

    def __init__(self, device):
        """Initialize the sensor."""
        self._device = device

    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return {"identifiers": {(DOMAIN, self._device.thermostat_id)}}

    @property
    def available(self) -> bool:
        """Return True if the device is available."""
        return self._device.online and self._device.hub.online

    async def async_added_to_hass(self):
        """Run when this Entity has been added to HA."""
        self._device.register_callback(self.async_write_ha_state)

    async def async_will_remove_from_hass(self):
        """Entity being removed from HA."""
        self._device.remove_callback(self.async_write_ha_state)


class TemperatureSensor(SensorBase):
    """Representation of a Temperature Sensor."""

    device_class = SensorDeviceClass.TEMPERATURE
    _attr_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, thermostat):
        """Initialize the sensor."""
        super().__init__(thermostat)
        self._attr_unique_id = f"{self._device.thermostat_id}_temperature"
        self._attr_name = f"{self._device.name} Temperature"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._device.current_temperature
