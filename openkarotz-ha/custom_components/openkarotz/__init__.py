"""OpenKarotz Home Assistant Integration."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api import OpenKarotzAPI
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up OpenKarotz from a config entry."""
    _LOGGER.info(f"Setting up OpenKarotz integration: {entry.entry_id}")

    host = entry.data.get("host", "192.168.1.201")
    port = entry.data.get("port", 80)

    api = OpenKarotzAPI(host, port)

    # Test connection
    try:
        await api.async_connect()
    except Exception as e:
        _LOGGER.error(f"Failed to connect to OpenKarotz: {e}")
        return False

    # Create coordinator
    from .coordinator import OpenKarotzCoordinator
    coordinator = OpenKarotzCoordinator(hass, api)

    # Store API instance and coordinator in hass data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "api": api,
        "coordinator": coordinator,
    }

    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, [Platform.SENSOR, Platform.LIGHT, Platform.MEDIA_PLAYER, Platform.BINARY_SENSOR, Platform.Switch, Platform.TEXT_SENSOR, Platform.PICTURE])

    # Set up services
    from .services import async_setup_services
    await async_setup_services(hass)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload OpenKarotz config entry."""
    _LOGGER.info(f"Unloading OpenKarotz integration: {entry.entry_id}")

    # Close API connection
    if entry.entry_id in hass.data.get(DOMAIN, {}):
        api = hass.data[DOMAIN][entry.entry_id].get("api")
        if api:
            await api.async_disconnect()
        del hass.data[DOMAIN][entry.entry_id]

    # Unload platforms
    unload_ok = await hass.config_entries.async_unload_platforms(entry, [Platform.SENSOR, Platform.LIGHT, Platform.MEDIA_PLAYER, Platform.BINARY_SENSOR, Platform.Switch, Platform.TEXT_SENSOR, Platform.PICTURE])

    return unload_ok


async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Migrate old config entry to new format."""
    _LOGGER.info(f"Migrating configuration entry: {config_entry.entry_id} from version {config_entry.version}")

    if config_entry.version <= 1:
        # Migration logic for version 1 to 2
        new_data = {**config_entry.data}
        # Add any new default values or migrate old data
        config_entry.version = 2

    return True