# nanoleaf-local

An attempt to bypass the Matter protocol on Nanoleaf downlights and use CoAP over Thread instead.

This project provides a Python-based test rig for controlling Nanoleaf downlights using CoAP (Constrained Application Protocol) over a Thread network. This approach offers a more reliable alternative to the Matter protocol implementation.

## Background

Nanoleaf downlights support CoAP communication over Thread, as documented in the [nanoleaf-ltpdu](https://github.com/roysjosh/nanoleaf-ltpdu) repository. This project leverages that capability using Python's `aiocoap` library.

## Prerequisites

- Python 3.7 or higher
- A Thread network with a border gateway set up
- Nanoleaf downlights connected to the Thread network
- IPv6 address of your Nanoleaf device
- Access token for authentication

## Installation

1. Clone this repository:
```bash
git clone https://github.com/jamesweakley/nanoleaf-local.git
cd nanoleaf-local
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Set up environment variables with your Nanoleaf device details:

```bash
export NANOLEAF_IPV6='fe80::1234:5678:90ab:cdef'  # Your device's IPv6 address
export NANOLEAF_TOKEN='your-access-token-here'     # Your access token
```

## Usage

### Interactive Mode (Default)

Run the test rig in interactive mode to manually test commands:

```bash
python test_rig.py
```

or explicitly:

```bash
python test_rig.py interactive
```

Available commands in interactive mode:
- `info` - Get device information
- `state` - Get current device state
- `on` - Turn on the device
- `off` - Turn off the device
- `brightness` - Set brightness (0-100)
- `ct` - Set color temperature (Kelvin)
- `hue` - Set hue and saturation
- `get` - Send a custom GET request
- `put` - Send a custom PUT request
- `quit` - Exit

### Automated Test Mode

Run a comprehensive test suite:

```bash
python test_rig.py test
```

This will automatically test:
- Device information retrieval
- Power on/off
- Brightness control (25%, 50%, 100%)
- Color temperature adjustment (2700K, 6500K)

### Using as a Library

You can also import and use the `NanoleafCoAPClient` in your own scripts:

```python
import asyncio
from nanoleaf_coap import NanoleafCoAPClient

async def main():
    ipv6_address = "fe80::1234:5678:90ab:cdef"
    access_token = "your-token"
    
    async with NanoleafCoAPClient(ipv6_address, access_token) as client:
        # Get device info
        response = await client.get("/api/v1/info")
        print(response)
        
        # Turn on the light
        import json
        payload = json.dumps({"on": {"value": True}})
        response = await client.put("/api/v1/state", payload)
        print(response)

asyncio.run(main())
```

## API Reference

### NanoleafCoAPClient

The main client class for CoAP communication.

#### Methods

- `__init__(ipv6_address: str, access_token: str)` - Initialize the client
- `async get(path: str) -> dict` - Send a GET request
- `async put(path: str, payload: str = "") -> dict` - Send a PUT request
- `async post(path: str, payload: str = "") -> dict` - Send a POST request

Use the client as an async context manager:

```python
async with NanoleafCoAPClient(ipv6_address, access_token) as client:
    # Your code here
    pass
```

## Common API Endpoints

Based on the Nanoleaf LTPDU protocol:

- `/api/v1/info` - Get device information
- `/api/v1/state` - Get/set device state (power, brightness, color, etc.)

Example payloads for state updates:

```json
{"on": {"value": true}}
{"brightness": {"value": 75}}
{"ct": {"value": 4000}}
{"hue": {"value": 180}, "sat": {"value": 50}}
```

## Troubleshooting

- **Connection timeout**: Ensure your device is on the Thread network and the IPv6 address is correct
- **Authentication error**: Verify your access token is valid
- **Network unreachable**: Make sure your border gateway is functioning and your machine can reach the Thread network

## References

- [nanoleaf-ltpdu](https://github.com/roysjosh/nanoleaf-ltpdu) - Original documentation of the LTPDU protocol
- [aiocoap](https://aiocoap.readthedocs.io/) - Python CoAP library

## License

This project is provided as-is for educational and personal use.
