"""Tests for OpenKarotz services."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from custom_components.openkarotz import services
from custom_components.openkarotz.const import DOMAIN


class TestOpenKarotzServices:
    """Test cases for OpenKarotz services."""

    @pytest.fixture
    def mock_hass(self):
        """Create a mock Home Assistant instance."""
        hass = MagicMock()
        hass.data = {
            DOMAIN: {
                "test_entry_id": {
                    "api": AsyncMock(),
                    "coordinator": MagicMock(),
                }
            }
        }
        hass.services = MagicMock()
        return hass

    @pytest.fixture
    def mock_service_call_set_led(self):
        """Create a mock service call for set_led."""
        service_call = MagicMock()
        service_call.data = {
            "config_entry_id": "test_entry_id",
            "color": "red",
            "brightness": 50,
            "color_temperature": 3000,
            "preset": "happy",
            "rgb_value": "FF0000",
        }
        return service_call

    @pytest.fixture
    def mock_service_call_play_tts(self):
        """Create a mock service call for play_tts."""
        service_call = MagicMock()
        service_call.data = {
            "config_entry_id": "test_entry_id",
            "text": "Hello, this is a test",
            "voice": "default",
            "category": "notification",
        }
        return service_call

    @pytest.fixture
    def mock_service_call_missing_entry_id(self):
        """Create a mock service call with missing entry_id."""
        service_call = MagicMock()
        service_call.data = {
            "color": "blue",
            "brightness": 75,
        }
        return service_call

    @pytest.mark.asyncio
    async def test_handle_set_led_success(self, mock_hass, mock_service_call_set_led):
        """Test successful set_led service call."""
        # Setup
        api_mock = mock_hass.data[DOMAIN]["test_entry_id"]["api"]
        api_mock.set_led = AsyncMock(return_value={"status": "ok"})

        # Execute
        await services.handle_set_led(mock_service_call_set_led)

        # Verify
        api_mock.set_led.assert_called_once_with(
            color="red",
            brightness=50,
            color_temperature=3000,
            preset="happy",
            rgb_value="FF0000",
        )

    @pytest.mark.asyncio
    async def test_handle_set_led_missing_entry_id(
        self, mock_hass, mock_service_call_missing_entry_id
    ):
        """Test set_led service call with missing entry_id."""
        # Setup
        api_mock = mock_hass.data[DOMAIN]["test_entry_id"]["api"]
        api_mock.set_led = AsyncMock()

        # Execute
        await services.handle_set_led(mock_service_call_missing_entry_id)

        # Verify - API should not be called
        api_mock.set_led.assert_not_called()

    @pytest.mark.asyncio
    async def test_handle_set_led_entry_not_found(self, mock_hass):
        """Test set_led service call with invalid entry_id."""
        # Setup
        service_call = MagicMock()
        service_call.data = {
            "config_entry_id": "invalid_entry_id",
            "color": "green",
        }

        # Execute
        await services.handle_set_led(service_call)

        # Verify - no exception should be raised

    @pytest.mark.asyncio
    async def test_handle_set_led_api_error(self, mock_hass, mock_service_call_set_led):
        """Test set_led service call with API error."""
        # Setup
        api_mock = mock_hass.data[DOMAIN]["test_entry_id"]["api"]
        api_mock.set_led = AsyncMock(side_effect=Exception("API Error"))

        # Execute - should not raise exception
        await services.handle_set_led(mock_service_call_set_led)

        # Verify - error should be logged (handled internally)

    @pytest.mark.asyncio
    async def test_handle_play_tts_success(self, mock_hass, mock_service_call_play_tts):
        """Test successful play_tts service call."""
        # Setup
        api_mock = mock_hass.data[DOMAIN]["test_entry_id"]["api"]
        api_mock.play_tts = AsyncMock(return_value={"status": "ok"})

        # Execute
        await services.handle_play_tts(mock_service_call_play_tts)

        # Verify
        api_mock.play_tts.assert_called_once_with(
            text="Hello, this is a test",
            voice="default",
            category="notification",
        )

    @pytest.mark.asyncio
    async def test_handle_play_tts_missing_entry_id(self, mock_hass):
        """Test play_tts service call with missing entry_id."""
        # Setup
        service_call = MagicMock()
        service_call.data = {
            "text": "Test message",
        }

        # Execute
        await services.handle_play_tts(service_call)

        # Verify - no exception should be raised

    @pytest.mark.asyncio
    async def test_handle_play_tts_entry_not_found(self, mock_hass):
        """Test play_tts service call with invalid entry_id."""
        # Setup
        service_call = MagicMock()
        service_call.data = {
            "config_entry_id": "invalid_entry_id",
            "text": "Test message",
        }

        # Execute
        await services.handle_play_tts(service_call)

        # Verify - no exception should be raised

    @pytest.mark.asyncio
    async def test_handle_play_tts_api_error(self, mock_hass, mock_service_call_play_tts):
        """Test play_tts service call with API error."""
        # Setup
        api_mock = mock_hass.data[DOMAIN]["test_entry_id"]["api"]
        api_mock.play_tts = AsyncMock(side_effect=Exception("API Error"))

        # Execute - should not raise exception
        await services.handle_play_tts(mock_service_call_play_tts)

        # Verify - error should be logged (handled internally)

    def test_async_setup_services(self, mock_hass):
        """Test async_setup_services function."""
        # Execute
        services.async_setup_services(mock_hass)

        # Verify services are registered
        assert mock_hass.services.async_register.called

    @pytest.mark.asyncio
    async def test_handle_set_led_minimal_data(self, mock_hass):
        """Test set_led service call with minimal data."""
        # Setup
        service_call = MagicMock()
        service_call.data = {
            "config_entry_id": "test_entry_id",
            "brightness": 100,
        }

        api_mock = mock_hass.data[DOMAIN]["test_entry_id"]["api"]
        api_mock.set_led = AsyncMock(return_value={"status": "ok"})

        # Execute
        await services.handle_set_led(service_call)

        # Verify
        api_mock.set_led.assert_called_once_with(
            color=None,
            brightness=100,
            color_temperature=None,
            preset=None,
            rgb_value=None,
        )

    @pytest.mark.asyncio
    async def test_handle_set_led_only_color(self, mock_hass):
        """Test set_led service call with only color."""
        # Setup
        service_call = MagicMock()
        service_call.data = {
            "config_entry_id": "test_entry_id",
            "color": "blue",
        }

        api_mock = mock_hass.data[DOMAIN]["test_entry_id"]["api"]
        api_mock.set_led = AsyncMock(return_value={"status": "ok"})

        # Execute
        await services.handle_set_led(service_call)

        # Verify
        api_mock.set_led.assert_called_once_with(
            color="blue",
            brightness=None,
            color_temperature=None,
            preset=None,
            rgb_value=None,
        )

    @pytest.mark.asyncio
    async def test_handle_set_led_only_rgb(self, mock_hass):
        """Test set_led service call with only RGB value."""
        # Setup
        service_call = MagicMock()
        service_call.data = {
            "config_entry_id": "test_entry_id",
            "rgb_value": "00FF00",
        }

        api_mock = mock_hass.data[DOMAIN]["test_entry_id"]["api"]
        api_mock.set_led = AsyncMock(return_value={"status": "ok"})

        # Execute
        await services.handle_set_led(service_call)

        # Verify
        api_mock.set_led.assert_called_once_with(
            color=None,
            brightness=None,
            color_temperature=None,
            preset=None,
            rgb_value="00FF00",
        )

    @pytest.mark.asyncio
    async def test_handle_play_tts_minimal_data(self, mock_hass):
        """Test play_tts service call with minimal data."""
        # Setup
        service_call = MagicMock()
        service_call.data = {
            "config_entry_id": "test_entry_id",
            "text": "Test",
        }

        api_mock = mock_hass.data[DOMAIN]["test_entry_id"]["api"]
        api_mock.play_tts = AsyncMock(return_value={"status": "ok"})

        # Execute
        await services.handle_play_tts(service_call)

        # Verify
        api_mock.play_tts.assert_called_once_with(
            text="Test",
            voice=None,
            category=None,
        )

    @pytest.mark.asyncio
    async def test_handle_play_tts_with_voice_only(self, mock_hass):
        """Test play_tts service call with voice."""
        # Setup
        service_call = MagicMock()
        service_call.data = {
            "config_entry_id": "test_entry_id",
            "text": "Test",
            "voice": "en-US",
        }

        api_mock = mock_hass.data[DOMAIN]["test_entry_id"]["api"]
        api_mock.play_tts = AsyncMock(return_value={"status": "ok"})

        # Execute
        await services.handle_play_tts(service_call)

        # Verify
        api_mock.play_tts.assert_called_once_with(
            text="Test",
            voice="en-US",
            category=None,
        )