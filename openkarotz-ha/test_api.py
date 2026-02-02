"""OpenKarotz API test script for validation."""

import asyncio
import sys
import os

# Add custom components to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'custom_components'))

from openkarotz.api import OpenKarotzAPI
from openkarotz.const import DEFAULT_HOST, DEFAULT_PORT


async def test_api():
    """Test OpenKarotz API connection."""
    print("Testing OpenKarotz API...")
    
    # Create API instance
    api = OpenKarotzAPI(DEFAULT_HOST, DEFAULT_PORT)
    
    # Test connection
    print(f"Connecting to {api.base_url}...")
    connected = await api.async_connect()
    
    if connected:
        print("✓ Successfully connected to OpenKarotz")
        
        # Test various API endpoints
        try:
            print("\nTesting API endpoints...")
            
            # Get device info
            print("Getting device info...")
            info = await api.get_info()
            print(f"✓ Device info: {info}")
            
            # Get device state
            print("Getting device state...")
            state = await api.get_state()
            print(f"✓ Device state: {state}")
            
            # Get LED state
            print("Getting LED state...")
            leds = await api.get_leds()
            print(f"✓ LED state: {leds}")
            
            # Get ears state
            print("Getting ears state...")
            ears = await api.get_ears()
            print(f"✓ Ears state: {ears}")
            
            # Get RFID state
            print("Getting RFID state...")
            rfid = await api.get_rfid()
            print(f"✓ RFID state: {rfid}")
            
            # Get TTS state
            print("Getting TTS state...")
            tts = await api.get_tts()
            print(f"✓ TTS state: {tts}")
            
            # Get pictures
            print("Getting pictures...")
            pictures = await api.get_pictures()
            print(f"✓ Pictures: {pictures}")
            
            # Get sounds
            print("Getting sounds...")
            sounds = await api.get_sounds()
            print(f"✓ Sounds: {sounds}")
            
            # Get apps
            print("Getting apps...")
            apps = await api.get_apps()
            print(f"✓ Apps: {apps}")
            
            print("\n✓ All API endpoints working correctly!")
            
        except Exception as e:
            print(f"\n✗ Error testing API endpoints: {e}")
            await api.async_disconnect()
            return False
    else:
        print("✗ Failed to connect to OpenKarotz")
        return False
    
    # Test service calls
    print("\nTesting service calls...")
    try:
        # Test LED set
        print("Setting LED...")
        led_response = await api.set_led(color="red", brightness=50)
        print(f"✓ LED set response: {led_response}")
        
        # Test volume set
        print("Setting volume...")
        volume_response = await api.set_volume(75)
        print(f"✓ Volume set response: {volume_response}")
        
        print("\n✓ All service calls working correctly!")
        
    except Exception as e:
        print(f"\n✗ Error testing service calls: {e}")
        await api.async_disconnect()
        return False
    
    # Clean up
    await api.async_disconnect()
    print("\n✓ All tests passed successfully!")
    return True


if __name__ == "__main__":
    success = asyncio.run(test_api())
    sys.exit(0 if success else 1)