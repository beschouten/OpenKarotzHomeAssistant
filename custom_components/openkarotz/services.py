"""OpenKarotz services."""

import logging
import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall

from .const import DOMAIN, SERVICE_NAMES, SERVICE_DATA_SCHEMAS

_LOGGER = logging.getLogger(__name__)


async def handle_set_led(hass: HomeAssistant, service_data: dict) -> bool:
    """Handle set LED service.

    Args:
        hass: Home Assistant instance
        service_data: Service call data

    Returns:
        True if successful, False otherwise
    """
    try:
        entry_id = service_data.get("config_entry_id")
        if not entry_id:
            _LOGGER.error("config_entry_id is required for set_led service")
            return False

        entry_data = hass.data[DOMAIN].get(entry_id)
        if not entry_data:
            _LOGGER.error(f"OpenKarotz entry {entry_id} not found")
            return False

        api = entry_data.get("api")
        if not api:
            _LOGGER.error("API not found for OpenKarotz entry")
            return False

        await api.set_led(
            color=service_data.get("color"),
            brightness=service_data.get("brightness"),
            color_temperature=service_data.get("color_temperature"),
            preset=service_data.get("preset"),
            rgb_value=service_data.get("rgb_value"),
        )
        return True
    except Exception as e:
        _LOGGER.error(f"Error setting LED: {e}")
        return False


async def handle_play_tts(hass: HomeAssistant, service_data: dict) -> bool:
    """Handle play TTS service.

    Args:
        hass: Home Assistant instance
        service_data: Service call data

    Returns:
        True if successful, False otherwise
    """
    try:
        entry_id = service_data.get("config_entry_id")
        if not entry_id:
            _LOGGER.error("config_entry_id is required for play_tts service")
            return False

        entry_data = hass.data[DOMAIN].get(entry_id)
        if not entry_data:
            _LOGGER.error(f"OpenKarotz entry {entry_id} not found")
            return False

        api = entry_data.get("api")
        if not api:
            _LOGGER.error("API not found for OpenKarotz entry")
            return False

        await api.play_tts(
            text=service_data.get("text"),
            voice=service_data.get("voice"),
            category=service_data.get("category"),
        )
        return True
    except Exception as e:
        _LOGGER.error(f"Error playing TTS: {e}")
        return False


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up OpenKarotz services."""

    async def handle_set_led_wrapper(service: ServiceCall) -> None:
        """Handle set LED service wrapper."""
        success = await handle_set_led(hass, service.data)
        if not success:
            _LOGGER.error("set_led service failed")

    async def handle_play_tts_wrapper(service: ServiceCall) -> None:
        """Handle play TTS service wrapper."""
        success = await handle_play_tts(hass, service.data)
        if not success:
            _LOGGER.error("play_tts service failed")

    hass.services.async_register(
        DOMAIN,
        SERVICE_NAMES["SET_LED"],
        handle_set_led_wrapper,
        schema=vol.Schema(SERVICE_DATA_SCHEMAS["set_led"]),
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_NAMES["PLAY_TTS"],
        handle_play_tts_wrapper,
        schema=vol.Schema(SERVICE_DATA_SCHEMAS["play_tts"]),
    )

    _LOGGER.info("OpenKarotz services registered")
