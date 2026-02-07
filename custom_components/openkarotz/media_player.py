"""OpenKarotz media player.""" 

from homeassistant.config_entries import ConfigEntry 
from homeassistant.core import HomeAssistant 
from homeassistant.helpers.entity_platform import AddEntitiesCallback 


async def async_setup_entry( 
    hass: HomeAssistant, 
    entry: ConfigEntry, 
    async_add_entities: AddEntitiesCallback, 
) -> None: 
    """Set up OpenKarotz media players.""" 
    async_add_entities([])