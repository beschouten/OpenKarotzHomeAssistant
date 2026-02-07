"""Integration tests for OpenKarotz light entity."""

import asyncio
import sys
sys.path.insert(0, '.')

from unittest.mock import AsyncMock, MagicMock, patch

from custom_components.openkarotz.light import OpenKarotzLight, PREDEFINED_COLORS
from custom_components.openkarotz.coordinator import OpenKarotzCoordinator
from custom_components.openkarotz.const import DOMAIN


async def test_light_entity_turn_on():
    """Test light entity turn on functionality."""
    print("\n=== Testing Light Entity Turn On ===\n")

    # Create mock coordinator
    coordinator = MagicMock(spec=OpenKarotzCoordinator)
    coordinator.api = AsyncMock()
    coordinator.api.set_led = AsyncMock(return_value={"status": "ok"})

    # Mock LED state
    coordinator.leds_state = {"enabled": True, "brightness": 50, "rgb_value": "FF0000"}
    coordinator.data = {
        "info": {"id": "test_device_123"},
        "leds": {"enabled": True, "brightness": 50, "rgb_value": "FF0000"}
    }

    # Create light entity
    led_data = {"id": 1, "name": "Main LED"}
    light = OpenKarotzLight(coordinator, led_data)

    # Test turn on with brightness
    print("Test 1: Turn on with brightness=75")
    await light.async_turn_on(brightness=75)
    coordinator.api.set_led.assert_called_with(brightness=75)
    print("  SUCCESS: Brightness set to 75")

    # Reset mock
    coordinator.api.set_led.reset_mock()

    # Test turn on with color
    print("\nTest 2: Turn on with color (red)")
    await light.async_turn_on(color=(255, 0, 0))
    coordinator.api.set_led.assert_called_with(rgb_value="ff0000")
    print("  SUCCESS: Color set to red (FF0000)")

    # Reset mock
    coordinator.api.set_led.reset_mock()

    # Test turn on with color temperature
    print("\nTest 3: Turn on with color_temperature=3500")
    await light.async_turn_on(color_temperature=3500)
    coordinator.api.set_led.assert_called_with(color_temperature=3500)
    print("  SUCCESS: Color temperature set to 3500K")

    # Reset mock
    coordinator.api.set_led.reset_mock()

    # Test turn on without parameters (should set brightness to 100)
    print("\nTest 4: Turn on without parameters")
    await light.async_turn_on()
    coordinator.api.set_led.assert_called_with(brightness=100)
    print("  SUCCESS: Brightness set to 100 (default)")


async def test_light_entity_turn_off():
    """Test light entity turn off functionality."""
    print("\n=== Testing Light Entity Turn Off ===\n")

    # Create mock coordinator
    coordinator = MagicMock(spec=OpenKarotzCoordinator)
    coordinator.api = AsyncMock()
    coordinator.api.set_led = AsyncMock(return_value={"status": "ok"})

    # Mock LED state
    coordinator.leds_state = {"enabled": True, "brightness": 100, "rgb_value": "FFFFFF"}
    coordinator.data = {
        "info": {"id": "test_device_123"},
        "leds": {"enabled": True, "brightness": 100, "rgb_value": "FFFFFF"}
    }

    # Create light entity
    led_data = {"id": 1, "name": "Main LED"}
    light = OpenKarotzLight(coordinator, led_data)

    # Test turn off
    print("Test: Turn off light")
    await light.async_turn_off()
    coordinator.api.set_led.assert_called_with(brightness=0)
    print("  SUCCESS: Brightness set to 0 (off)")


async def test_light_entity_color_change():
    """Test light entity color change functionality."""
    print("\n=== Testing Light Entity Color Change ===\n")

    # Create mock coordinator
    coordinator = MagicMock(spec=OpenKarotzCoordinator)
    coordinator.api = AsyncMock()
    coordinator.api.set_led = AsyncMock(return_value={"status": "ok"})

    # Mock LED state
    coordinator.leds_state = {"enabled": True, "brightness": 100, "rgb_value": "FFFFFF"}
    coordinator.data = {
        "info": {"id": "test_device_123"},
        "leds": {"enabled": True, "brightness": 100, "rgb_value": "FFFFFF"}
    }

    # Create light entity
    led_data = {"id": 1, "name": "Main LED"}
    light = OpenKarotzLight(coordinator, led_data)

    # Test predefined colors
    print("Test 1: Change to blue using predefined color")
    await light.async_turn_on(color=(0, 0, 255))
    coordinator.api.set_led.assert_called_with(rgb_value="0000ff")
    print("  SUCCESS: Color set to blue (0000FF)")

    # Reset mock
    coordinator.api.set_led.reset_mock()

    print("\nTest 2: Change to green using predefined color")
    await light.async_turn_on(color=(0, 255, 0))
    coordinator.api.set_led.assert_called_with(rgb_value="00ff00")
    print("  SUCCESS: Color set to green (00FF00)")

    # Reset mock
    coordinator.api.set_led.reset_mock()

    print("\nTest 3: Change to yellow using predefined color")
    await light.async_turn_on(color=(255, 255, 0))
    coordinator.api.set_led.assert_called_with(rgb_value="ffff00")
    print("  SUCCESS: Color set to yellow (FFFF00)")


async def test_light_entity_properties():
    """Test light entity properties."""
    print("\n=== Testing Light Entity Properties ===\n")

    # Create mock coordinator
    coordinator = MagicMock(spec=OpenKarotzCoordinator)
    coordinator.api = AsyncMock()
    coordinator.api.set_led = AsyncMock(return_value={"status": "ok"})

    # Mock LED state
    coordinator.leds_state = {"enabled": True, "brightness": 75, "rgb_value": "FF0000"}
    coordinator.data = {
        "info": {"id": "test_device_123"},
        "leds": {"enabled": True, "brightness": 75, "rgb_value": "FF0000"}
    }

    # Create light entity
    led_data = {"id": 1, "name": "Main LED"}
    light = OpenKarotzLight(coordinator, led_data)

    # Test is_on property
    print("Test 1: is_on property")
    assert light.is_on is True, "Light should be on"
    print("  SUCCESS: is_on = True")

    # Test brightness property
    print("\nTest 2: brightness property")
    assert light.brightness == 75, "Brightness should be 75"
    print("  SUCCESS: brightness = 75")

    # Test color property
    print("\nTest 3: color property")
    color = light.color
    assert color == (255, 0, 0), f"Color should be (255, 0, 0), got {color}"
    print("  SUCCESS: color = (255, 0, 0)")

    # Test color_mode property
    print("\nTest 4: color_mode property")
    color_mode = light.color_mode
    assert color_mode == "rgb", f"Color mode should be 'rgb', got {color_mode}"
    print("  SUCCESS: color_mode = 'rgb'")

    # Test supported_color_modes property
    print("\nTest 5: supported_color_modes property")
    modes = light.supported_color_modes
    assert "rgb" in modes, "RGB mode should be supported"
    print(f"  SUCCESS: supported_color_modes = {modes}")


async def test_light_entity_with_color_temperature():
    """Test light entity with color temperature."""
    print("\n=== Testing Light Entity with Color Temperature ===\n")

    # Create mock coordinator
    coordinator = MagicMock(spec=OpenKarotzCoordinator)
    coordinator.api = AsyncMock()
    coordinator.api.set_led = AsyncMock(return_value={"status": "ok"})

    # Mock LED state with color temperature
    coordinator.leds_state = {"enabled": True, "brightness": 50, "color_temperature": 3000}
    coordinator.data = {
        "info": {"id": "test_device_123"},
        "leds": {"enabled": True, "brightness": 50, "color_temperature": 3000}
    }

    # Create light entity
    led_data = {"id": 1, "name": "Main LED"}
    light = OpenKarotzLight(coordinator, led_data)

    # Test color_temperature property
    print("Test 1: color_temperature property")
    assert light.color_temperature == 3000, "Color temperature should be 3000"
    print("  SUCCESS: color_temperature = 3000K")

    # Test color_mode property with color temperature
    print("\nTest 2: color_mode property with color temperature")
    color_mode = light.color_mode
    assert color_mode == "color_temperature", f"Color mode should be 'color_temperature', got {color_mode}"
    print("  SUCCESS: color_mode = 'color_temperature'")


async def main():
    """Run all light integration tests."""
    print("=" * 60)
    print("OpenKarotz Light Entity Integration Tests")
    print("=" * 60)

    try:
        await test_light_entity_turn_on()
        await test_light_entity_turn_off()
        await test_light_entity_color_change()
        await test_light_entity_properties()
        await test_light_entity_with_color_temperature()

        print("\n" + "=" * 60)
        print("ALL LIGHT INTEGRATION TESTS PASSED!")
        print("=" * 60)
        print("\nSummary:")
        print("  [OK] Light entity turn on works correctly")
        print("  [OK] Light entity turn off works correctly")
        print("  [OK] Light entity color change works correctly")
        print("  [OK] Light entity properties work correctly")
        print("  [OK] Light entity color temperature works correctly")
        print("\nLight entity is ready for production use.")
        print("=" * 60)

    except Exception as e:
        print(f"\n[FAIL] Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    asyncio.run(main())