"""OpenKarotz README and documentation."""

# OpenKarotz Home Assistant Integration

A comprehensive Home Assistant integration for OpenKarotz devices, enabling seamless control and monitoring through the Home Assistant Community Store (HACS).

## Features

 - **Device Information**: Monitor device status, memory usage, and uptime
 - **LED Control**: Full RGB color control, brightness adjustment, and color temperature
 - **Audio Player**: Playback control, volume management, and media management
 - **RFID Detection**: Real-time RFID card detection and event handling
 - **Text-to-Speech**: Voice synthesis with customizable categories
 - **Sound Effects**: Play various sound categories with volume control
 - **Picture Display**: Display pictures with customizable duration
 - **Ear Movement Control**: Control ear movement with position adjustment, mode selection, and reset functionality
 - **Service Integration**: Full API access through Home Assistant services

## Installation

### Via HACS (Recommended)

1. Install Home Assistant Community Store (HACS)
2. Go to HACS → Integrations
3. Search for "OpenKarotz"
4. Click "Install"
5. Follow the setup wizard

### Manual Installation

1. Download this repository
2. Place the `custom_components/openkarotz` directory in your Home Assistant `custom_components` folder
3. Restart Home Assistant
4. Go to Settings → Devices & Services → Add Integration → OpenKarotz

## Configuration

### Basic Setup

Enter your OpenKarotz device IP address and port:

- **Host**: The IP address of your OpenKarotz device (default: 192.168.1.201)
- **Port**: The device port number (default: 80)

### Configuration Example

```yaml
openkarotz:
  host: 192.168.1.201
  port: 80
```

## Entities

### Sensors

- **Device Name**: Name of the OpenKarotz device
- **Device State**: Current state of the device
- **Memory Usage**: Memory usage percentage
- **Device Uptime**: Device uptime in seconds

### Lights

- **LED Light**: Full RGB color control with brightness and color temperature

### Media Player

- **Audio Player**: Complete audio playback control with volume management

### Binary Sensors

- **RFID Detection**: Real-time RFID card detection status

### Switches

- **Enable Device**: Enable or disable the OpenKarotz device

### Ear Movement Entities

- **Ear Position**: Current ear position
- **Ear Mode**: Current ear movement mode
- **Ear Reset**: Ear reset control

## Services

### Set LED
Set LED color, brightness, or preset.

**Service Data Attributes:**
- `color`: Color name (e.g., "red", "blue")
- `brightness`: Brightness level (0-100)
- `color_temperature`: Color temperature in Kelvin
- `preset`: Preset color scheme name
- `rgb_value`: RGB color value (e.g., "FF0000")

### Play Audio
Play audio from specified source.

**Service Data Attributes:**
- `source`: Audio source identifier
- `category`: Audio category (e.g., "alarm", "notification")
- `volume`: Audio volume (0-100)

### Stop Audio
Stop audio playback.

**Service Data Attributes:**
- `source`: Audio source to stop (optional)

### Set Volume
Set audio volume level.

**Service Data Attributes:**
- `volume`: Volume level (0-100)

### Play TTS
Play text-to-speech.

**Service Data Attributes:**
- `text`: Text to speak
- `voice`: Voice identifier
- `category`: TTS category (e.g., "notification")

### Play Sound
Play a sound effect.

**Service Data Attributes:**
- `sound`: Sound identifier
- `volume`: Volume level (0-100)

### Display Picture
Display a picture on the device.

**Service Data Attributes:**
- `picture`: Picture identifier
- `duration`: Display duration in seconds

### Move Ears
Control ear movement to specific position.

**Service Data Attributes:**
- `position`: Ear position (0-100)
- `duration`: Movement duration in seconds
- `sync`: Synchronize both ears (boolean)

### Ear Mode
Set ear movement mode.

**Service Data Attributes:**
- `mode`: Movement mode ("idle", "scan", "reactive")

### Ear Reset
Reset ears to default position.

**Service Data Attributes:**
- No attributes required

## Configuration Examples

### Automation Examples

#### Turn on LED when device starts
```yaml
automation:
  - alias: "Turn on LED on startup"
    trigger:
      - platform: state
        entity_id: sensor.device_state
        to: "running"
    action:
      - service: openkarotz.set_led
        data:
          color: "blue"
          brightness: 100
```

#### Play TTS when RFID detected
```yaml
automation:
  - alias: "Play TTS on RFID"
    trigger:
      - platform: state
        entity_id: binary_sensor.rfid_detection
        to: "on"
    action:
      - service: openkarotz.play_tts
        data:
          text: "RFID card detected"
          category: "notification"
```

#### Move ears when device starts
```yaml
automation:
  - alias: "Move ears on startup"
    trigger:
      - platform: state
        entity_id: sensor.device_state
        to: "running"
    action:
      - service: openkarotz.move_ears
        data:
          position: 50
          duration: 2
          sync: true
```

#### Set ear mode for scanning
```yaml
automation:
  - alias: "Set scanning mode"
    trigger:
      - platform: state
        entity_id: binary_sensor.rfid_detection
        to: "on"
    action:
      - service: openkarotz.ears_mode
        data:
          mode: "reactive"
```

#### Reset ears after RFID scan
```yaml
automation:
  - alias: "Reset ears after scan"
    trigger:
      - platform: state
        entity_id: binary_sensor.rfid_detection
        to: "off"
    action:
      - service: openkarotz.ears_reset
        data: {}
```

## Troubleshooting

### Connection Issues

- Ensure OpenKarotz device is accessible from Home Assistant
- Check IP address and port configuration
- Verify network connectivity
- Check device logs for errors

### Entity Not Appearing

- Wait for data synchronization (default: 30 seconds)
- Check connection status in device info
- Restart Home Assistant
- Verify device is responding to API requests

### API Errors

- Check device API documentation
- Verify API endpoints are accessible
- Review integration logs for detailed error messages
- Ensure proper authentication if required

## Development

### Project Structure

```
openkarotz-ha/
├── custom_components/
│   └── openkarotz/
│       ├── __init__.py
│       ├── config_flow.py
│       ├── coordinator.py
│       ├── api.py
│       │   └── Includes: move_ears(), ears_mode(), ears_reset(), get_pictures(), get_sounds(), get_apps()
│       ├── sensors.py
│       ├── lights.py
│       ├── media_player.py
│       ├── binary_sensor.py
│       ├── switch.py
│       ├── ear_movement.py
│       ├── services.py
│       ├── const.py
│       ├── manifest.json
│       └── translations/
│           └── en.json
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_ear_movement.py
├── README.md
└── requirements.txt
```

### Requirements

- Home Assistant >= 2026.1.0
- Python 3.9+

### Testing

Run automated tests:
```bash
pytest tests/
```

## Changelog

### Version 1.1.0
- Added ear movement control (move_ears, ears_mode, ears_reset)
- Added play_sound and display_picture services
- Added get_pictures, get_sounds, get_apps API methods
- Added comprehensive tests for ear movement API
- Fixed HACS installation issues
- All code validated with pytest

## Contributing

Contributions are welcome! Please read the contributing guidelines and submit pull requests.

## License

This project is provided as-is for educational and personal use.

## Support

For issues, questions, or contributions, please visit the GitHub repository or contact the maintainers.

## Credits

- Home Assistant: https://www.home-assistant.io
- OpenKarotz: https://github.com/beschouten/OpenKarotz

## API Documentation

The OpenKarotz API is based on the OpenKarotz Websources Installer project by rofra:
- **Repository**: https://github.com/rofra/karotz-openkarotz-websources-installer
- **API Pattern**: All endpoints follow the `/cgi-bin/` pattern

### Key API Methods

| Endpoint | Function | Parameters |
|----------|----------|------------|
| `/cgi-bin/status` | Device status | - |
| `/cgi-bin/ears` | Ear movement | left, right positions (0-16) |
| `/cgi-bin/ears_mode` | Set ear mode | disabled=0/1 |
| `/cgi-bin/ears_reset` | Reset ears | - |
| `/cgi-bin/leds` | LED control | RGB, brightness |
| `/cgi-bin/tts` | Text-to-speech | text, voice, category |
| `/cgi-bin/sound` | Play sound | sound identifier, volume |
| `/cgi-bin/sound_list` | List sounds | - |
| `/cgi-bin/pictures` | Display pictures | picture, duration |
| `/cgi-bin/rfid` | RFID detection | - |

For detailed API documentation, visit the [OpenKarotz API Documentation](https://github.com/rofra/karotz-openkarotz-websources-installer).