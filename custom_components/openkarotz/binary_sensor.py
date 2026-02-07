"""OpenKarotz binary sensors."""

import logging

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
) -> None:
    """Set up OpenKarotz binary sensors."""
    async_add_entities([])


