"""Integration tests for OpenKarotz services with example data."""

import asyncio
import sys
sys.path.insert(0, '.')

from unittest.mock import AsyncMock, MagicMock, patch

from custom_components.openkarotz import services
from custom_components.openkarotz.const import DOMAIN


async def test_set_led_service_integration():
    """Test set_led service with example data."""
    print("\n=== Testing set_led Service Integration ===\n")

    # Create mock hass with data
    hass = MagicMock()
    hass.data = {
        DOMAIN: {
            "abc123": {
                "api": AsyncMock(),
                "coordinator": MagicMock(),
            }
        }
    }
    hass.services = MagicMock()

    # Example service call data
    service_data = {
        "config_entry_id": "abc123",
        "color": "red",
        "brightness": 75,
        "color_temperature": 3500,
        "preset": "relax",
        "rgb_value": "FF0000",
    }

    # Mock the API response
    expected_response = {
        "status": "ok",
        "message": "LED settings updated successfully",
    }
    hass.data[DOMAIN]["abc123"]["api"].set_led = AsyncMock(return_value=expected_response)

    # Execute the service handler
    success = await services.handle_set_led(hass, service_data)

    # Verify the API was called with correct parameters
    api = hass.data[DOMAIN]["abc123"]["api"]
    api.set_led.assert_called_once_with(
        color="red",
        brightness=75,
        color_temperature=3500,
        preset="relax",
        rgb_value="FF0000",
    )

    print("SUCCESS: set_led service called successfully")
    print(f"  - Color: red")
    print(f"  - Brightness: 75")
    print(f"  - Color Temperature: 3500K")
    print(f"  - Preset: relax")
    print(f"  - RGB Value: FF0000")
    print(f"  - API Response: {expected_response}")
    print(f"  - Return value: {success}")
    assert success is True, "Service should return True on success"


async def test_play_tts_service_integration():
    """Test play_tts service with example data."""
    print("\n=== Testing play_tts Service Integration ===\n")

    # Create mock hass with data
    hass = MagicMock()
    hass.data = {
        DOMAIN: {
            "def456": {
                "api": AsyncMock(),
                "coordinator": MagicMock(),
            }
        }
    }
    hass.services = MagicMock()

    # Example service call data
    service_data = {
        "config_entry_id": "def456",
        "text": "Hello, this is a test message from OpenKarotz integration",
        "voice": "default",
        "category": "notification",
    }

    # Mock the API response
    expected_response = {
        "status": "ok",
        "message": "TTS playback started",
    }
    hass.data[DOMAIN]["def456"]["api"].play_tts = AsyncMock(return_value=expected_response)

    # Execute the service handler
    success = await services.handle_play_tts(hass, service_data)

    # Verify the API was called with correct parameters
    api = hass.data[DOMAIN]["def456"]["api"]
    api.play_tts.assert_called_once_with(
        text="Hello, this is a test message from OpenKarotz integration",
        voice="default",
        category="notification",
    )

    print("SUCCESS: play_tts service called successfully")
    print(f"  - Text: Hello, this is a test message from OpenKarotz integration")
    print(f"  - Voice: default")
    print(f"  - Category: notification")
    print(f"  - API Response: {expected_response}")
    print(f"  - Return value: {success}")
    assert success is True, "Service should return True on success"


async def test_set_led_service_error_handling():
    """Test set_led service error handling."""
    print("\n=== Testing set_led Service Error Handling ===\n")

    # Create mock hass with data
    hass = MagicMock()
    hass.data = {
        DOMAIN: {
            "ghi789": {
                "api": AsyncMock(),
                "coordinator": MagicMock(),
            }
        }
    }
    hass.services = MagicMock()

    # Test 1: Missing config_entry_id
    print("Test 1: Missing config_entry_id")
    service_data = {
        "color": "blue",
        "brightness": 50,
    }

    success = await services.handle_set_led(hass, service_data)
    print(f"  SUCCESS: No exception raised, returned: {success}")
    assert success is False, "Should return False for missing entry_id"

    # Test 2: Invalid config_entry_id
    print("\nTest 2: Invalid config_entry_id")
    service_data = {
        "config_entry_id": "nonexistent",
        "color": "green",
    }

    success = await services.handle_set_led(hass, service_data)
    print(f"  SUCCESS: No exception raised, returned: {success}")
    assert success is False, "Should return False for invalid entry_id"

    # Test 3: API Error
    print("\nTest 3: API Error handling")
    service_data = {
        "config_entry_id": "ghi789",
        "color": "yellow",
    }

    api = hass.data[DOMAIN]["ghi789"]["api"]
    api.set_led = AsyncMock(side_effect=Exception("Connection timeout"))

    success = await services.handle_set_led(hass, service_data)
    print(f"  SUCCESS: No exception raised, returned: {success}")
    assert success is False, "Should return False for API error"


async def test_play_tts_service_error_handling():
    """Test play_tts service error handling."""
    print("\n=== Testing play_tts Service Error Handling ===\n")

    # Create mock hass with data
    hass = MagicMock()
    hass.data = {
        DOMAIN: {
            "jkl012": {
                "api": AsyncMock(),
                "coordinator": MagicMock(),
            }
        }
    }
    hass.services = MagicMock()

    # Test 1: Missing config_entry_id
    print("Test 1: Missing config_entry_id")
    service_data = {
        "text": "Test message",
    }

    success = await services.handle_play_tts(hass, service_data)
    print(f"  SUCCESS: No exception raised, returned: {success}")
    assert success is False, "Should return False for missing entry_id"

    # Test 2: Invalid config_entry_id
    print("\nTest 2: Invalid config_entry_id")
    service_data = {
        "config_entry_id": "nonexistent",
        "text": "Test message",
    }

    success = await services.handle_play_tts(hass, service_data)
    print(f"  SUCCESS: No exception raised, returned: {success}")
    assert success is False, "Should return False for invalid entry_id"

    # Test 3: API Error
    print("\nTest 3: API Error handling")
    service_data = {
        "config_entry_id": "jkl012",
        "text": "Test message",
    }

    api = hass.data[DOMAIN]["jkl012"]["api"]
    api.play_tts = AsyncMock(side_effect=Exception("API unavailable"))

    success = await services.handle_play_tts(hass, service_data)
    print(f"  SUCCESS: No exception raised, returned: {success}")
    assert success is False, "Should return False for API error"


async def test_set_led_service_minimal():
    """Test set_led service with minimal data."""
    print("\n=== Testing set_led Service with Minimal Data ===\n")

    # Create mock hass with data
    hass = MagicMock()
    hass.data = {
        DOMAIN: {
            "mno345": {
                "api": AsyncMock(),
                "coordinator": MagicMock(),
            }
        }
    }
    hass.services = MagicMock()

    # Example: Only brightness
    print("Test: Only brightness specified")
    service_data = {
        "config_entry_id": "mno345",
        "brightness": 100,
    }

    api = hass.data[DOMAIN]["mno345"]["api"]
    api.set_led = AsyncMock(return_value={"status": "ok"})

    success = await services.handle_set_led(hass, service_data)

    api.set_led.assert_called_once_with(
        color=None,
        brightness=100,
        color_temperature=None,
        preset=None,
        rgb_value=None,
    )
    print(f"  SUCCESS: Service called with only brightness parameter, returned: {success}")
    assert success is True, "Should return True on success"

    # Example: Only color
    print("\nTest: Only color specified")
    service_data = {
        "config_entry_id": "mno345",
        "color": "purple",
    }

    api.set_led = AsyncMock(return_value={"status": "ok"})

    success = await services.handle_set_led(hass, service_data)

    api.set_led.assert_called_once_with(
        color="purple",
        brightness=None,
        color_temperature=None,
        preset=None,
        rgb_value=None,
    )
    print(f"  SUCCESS: Service called with only color parameter, returned: {success}")
    assert success is True, "Should return True on success"


async def test_play_tts_service_minimal():
    """Test play_tts service with minimal data."""
    print("\n=== Testing play_tts Service with Minimal Data ===\n")

    # Create mock hass with data
    hass = MagicMock()
    hass.data = {
        DOMAIN: {
            "pqr678": {
                "api": AsyncMock(),
                "coordinator": MagicMock(),
            }
        }
    }
    hass.services = MagicMock()

    # Example: Only text (required field)
    print("Test: Only text specified (required)")
    service_data = {
        "config_entry_id": "pqr678",
        "text": "Quick test",
    }

    api = hass.data[DOMAIN]["pqr678"]["api"]
    api.play_tts = AsyncMock(return_value={"status": "ok"})

    success = await services.handle_play_tts(hass, service_data)

    api.play_tts.assert_called_once_with(
        text="Quick test",
        voice=None,
        category=None,
    )
    print(f"  SUCCESS: Service called with only text parameter, returned: {success}")
    assert success is True, "Should return True on success"


async def main():
    """Run all integration tests."""
    print("=" * 60)
    print("OpenKarotz Services Integration Tests")
    print("=" * 60)

    try:
        await test_set_led_service_integration()
        await test_play_tts_service_integration()
        await test_set_led_service_error_handling()
        await test_play_tts_service_error_handling()
        await test_set_led_service_minimal()
        await test_play_tts_service_minimal()

        print("\n" + "=" * 60)
        print("ALL INTEGRATION TESTS PASSED!")
        print("=" * 60)
        print("\nSummary:")
        print("  [OK] set_led service works correctly")
        print("  [OK] play_tts service works correctly")
        print("  [OK] Error handling works correctly")
        print("  [OK] Minimal data scenarios work correctly")
        print("\nAll services are ready for production use.")
        print("=" * 60)

    except Exception as e:
        print(f"\n[FAIL] Test failed with error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())