# Nanoleaf CoAP API Reference

This document provides a reference for the CoAP API endpoints available on Nanoleaf downlights, based on the [nanoleaf-ltpdu](https://github.com/roysjosh/nanoleaf-ltpdu) protocol.

## Base URI

```
coap://[IPv6_ADDRESS]
```

## Authentication

All requests require authentication via a query parameter:

```
?auth=YOUR_ACCESS_TOKEN
```

## Common Endpoints

### Get Device Information

```
GET /api/v1/info
```

Returns information about the device including firmware version, model, etc.

**Example Response:**
```json
{
  "name": "Nanoleaf Light",
  "serialNo": "...",
  "manufacturer": "Nanoleaf",
  "firmwareVersion": "...",
  "model": "..."
}
```

### Get Device State

```
GET /api/v1/state
```

Returns the current state of the device including power, brightness, color, etc.

**Example Response:**
```json
{
  "on": {"value": true},
  "brightness": {"value": 75},
  "hue": {"value": 180},
  "sat": {"value": 50},
  "ct": {"value": 4000}
}
```

### Update Device State

```
PUT /api/v1/state
Content-Type: application/json
```

Update one or more state properties.

**Example Payloads:**

Turn on/off:
```json
{"on": {"value": true}}
{"on": {"value": false}}
```

Set brightness (0-100):
```json
{"brightness": {"value": 75}}
```

Set color temperature in Kelvin (typically 2700-6500):
```json
{"ct": {"value": 4000}}
```

Set hue (0-360) and saturation (0-100):
```json
{"hue": {"value": 180}, "sat": {"value": 50}}
```

Combine multiple properties:
```json
{
  "on": {"value": true},
  "brightness": {"value": 80},
  "ct": {"value": 3500}
}
```

With transition time (in deciseconds, i.e., 10 = 1 second):
```json
{
  "brightness": {"value": 100, "duration": 20}
}
```

## Property Ranges

| Property | Type | Range | Description |
|----------|------|-------|-------------|
| on | boolean | true/false | Power state |
| brightness | integer | 0-100 | Brightness percentage |
| hue | integer | 0-360 | Hue in degrees |
| sat | integer | 0-100 | Saturation percentage |
| ct | integer | 2700-6500 | Color temperature in Kelvin |
| duration | integer | 0-65535 | Transition time in deciseconds |

## Error Responses

The device may return error codes for invalid requests:

- **2.05 Content** - Success (GET)
- **2.04 Changed** - Success (PUT)
- **4.00 Bad Request** - Invalid request format
- **4.01 Unauthorized** - Invalid or missing authentication
- **4.04 Not Found** - Endpoint does not exist
- **4.05 Method Not Allowed** - HTTP method not supported

## Usage Examples

### Python (using nanoleaf_coap.py)

```python
import asyncio
import json
from nanoleaf_coap import NanoleafCoAPClient

async def example():
    async with NanoleafCoAPClient("fe80::1234", "token") as client:
        # Get info
        info = await client.get("/api/v1/info")
        
        # Turn on and set brightness
        payload = json.dumps({
            "on": {"value": True},
            "brightness": {"value": 75}
        })
        result = await client.put("/api/v1/state", payload)

asyncio.run(example())
```

## Notes

- The device must be on the same Thread network as your client
- IPv6 addresses should be wrapped in square brackets: `[fe80::1234]`
- CoAP uses UDP as the transport protocol
- Requests may timeout if the device is unreachable or sleeping
- Some properties may not be available on all device models

## Resources

- [aiocoap Documentation](https://aiocoap.readthedocs.io/)
- [CoAP Specification (RFC 7252)](https://tools.ietf.org/html/rfc7252)
- [nanoleaf-ltpdu Repository](https://github.com/roysjosh/nanoleaf-ltpdu)
