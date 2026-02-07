"""OpenKarotz data coordinator for state management."""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import OpenKarotzAPI
from .const import (
    ATTR_ERROR_MESSAGE,
    ATTR_LAST_UPDATE,
)

_LOGGER = logging.getLogger(__name__)


class OpenKarotzCoordinator(DataUpdateCoordinator[Dict[str, Any]]):
    """Coordinator for OpenKarotz data updates."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: OpenKarotzAPI,
        update_interval: int = 30,
    ) -> None:
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="OpenKarotz",
            update_interval=timedelta(seconds=update_interval),
        )
        self.api = api
        self._device_info: Optional[Dict[str, Any]] = None
        self._device_state: Optional[Dict[str, Any]] = None
        self._led_state: Optional[Dict[str, Any]] = None
        self._tts_state: Optional[Dict[str, Any]] = None
        self._apps: Optional[Dict[str, Any]] = None

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch data from OpenKarotz API."""
        try:
            info_task = self.api.get_info()
            leds_task = self.api.get_leds()
            tts_task = self.api.get_tts()
            apps_task = self.api.get_apps()

            info, leds, tts, apps = await asyncio.gather(
                info_task,
                leds_task,
                tts_task,
                apps_task,
                return_exceptions=True,
            )

            errors = {}
            if isinstance(info, Exception):
                errors["info"] = str(info)
                info = {}
            if isinstance(leds, Exception):
                errors["leds"] = str(leds)
                leds = {}
            if isinstance(tts, Exception):
                errors["tts"] = str(tts)
                tts = {}
            if isinstance(apps, Exception):
                errors["apps"] = str(apps)
                apps = {}

            self._device_info = info
            self._device_state = info
            self._led_state = leds
            self._tts_state = tts
            self._apps = apps

            data = {
                "id": info.get("id", info.get("wlan_mac", "unknown")),
                "version": info.get("version", "unknown"),
                ATTR_LAST_UPDATE: datetime.now().isoformat(),
                ATTR_ERROR_MESSAGE: str(errors) if errors else None,
                "info": info,
                "state": info,
                "leds": leds,
                "tts": tts,
                "moods": apps,
            }

            if errors:
                _LOGGER.warning(f"OpenKarotz data update had errors: {errors}")

            return data

        except Exception as e:
            _LOGGER.error(f"Error updating OpenKarotz data: {e}")
            raise UpdateFailed(f"Error updating OpenKarotz data: {e}") from e

    @property
    def device_info(self) -> Dict[str, Any]:
        """Return device information."""
        if not self._device_info:
            return {}
        return {
            "name": self._device_info.get("name", "OpenKarotz"),
            "model": self._device_info.get("model", "Unknown"),
            "manufacturer": "OpenKarotz",
            "serial_number": self._device_info.get("serial", "Unknown"),
            "config_entry_id": self.config_entry.entry_id,
        }

    @property
    def device_state(self) -> Optional[Dict[str, Any]]:
        """Return current device state."""
        return self._device_state

    @property
    def leds_state(self) -> Optional[Dict[str, Any]]:
        """Return LED state."""
        return self._led_state

    @property
    def tts_state(self) -> Optional[Dict[str, Any]]:
        """Return TTS state."""
        return self._tts_state

    @property
    def apps(self) -> Optional[Dict[str, Any]]:
        """Return applications information."""
        return self._apps
