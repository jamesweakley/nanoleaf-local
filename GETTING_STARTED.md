# Getting Started with Nanoleaf CoAP Test Rig

This guide will help you quickly get started with controlling your Nanoleaf downlights via CoAP over Thread.

## Prerequisites Checklist

Before you begin, ensure you have:

- [ ] Python 3.7 or higher installed
- [ ] pip (Python package manager) installed
- [ ] A Thread network with a border gateway configured
- [ ] Nanoleaf downlights connected to your Thread network
- [ ] The IPv6 address of your Nanoleaf device
- [ ] An access token for authentication

## Quick Start (5 minutes)

### Step 1: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/jamesweakley/nanoleaf-local.git
cd nanoleaf-local

# Run the setup script
./setup.sh
```

### Step 2: Configure Environment

Set your device credentials as environment variables:

```bash
export NANOLEAF_IPV6='fe80::1234:5678:90ab:cdef'  # Replace with your device's IPv6
export NANOLEAF_TOKEN='your-access-token-here'     # Replace with your token
```

**Tip:** Add these to your `~/.bashrc` or `~/.zshrc` to persist them across sessions.

### Step 3: Test the Connection

Run a simple example to verify everything works:

```bash
python3 example.py
```

You should see output showing device information and the light being controlled.

## Finding Your Device Information

### Finding the IPv6 Address

The IPv6 address of your Nanoleaf device can typically be found:

1. Through your Thread border router's interface
2. Using network scanning tools like `nmap` for IPv6
3. From your device's setup interface or app

The address will be in IPv6 format, typically starting with `fe80::` for link-local addresses.

### Getting an Access Token

The access token is device-specific. Methods to obtain it may include:

1. Check the Nanoleaf app or configuration interface
2. Refer to Nanoleaf's documentation for your specific device model
3. Use the device's pairing or setup mode

## Usage Modes

### 1. Simple Example (Best for First-Time Users)

Run the basic example script:

```bash
python3 example.py
```

This demonstrates:
- Connecting to the device
- Getting device information
- Turning on the light
- Setting brightness
- Getting device state

### 2. Interactive Mode (Best for Testing)

Run the interactive test rig:

```bash
python3 test_rig.py interactive
```

or simply:

```bash
python3 test_rig.py
```

This gives you a menu-driven interface where you can:
- Query device information
- Toggle power
- Adjust brightness, color temperature, hue, and saturation
- Send custom CoAP requests

### 3. Automated Test Mode (Best for Verification)

Run the automated test suite:

```bash
python3 test_rig.py test
```

This runs through a comprehensive set of tests including:
- Power on/off cycles
- Brightness adjustments (25%, 50%, 100%)
- Color temperature changes
- State queries

## Using as a Python Library

Integrate the CoAP client into your own Python scripts:

```python
import asyncio
import json
from nanoleaf_coap import NanoleafCoAPClient

async def control_lights():
    # Your device credentials
    ipv6 = "fe80::1234:5678:90ab:cdef"
    token = "your-token-here"
    
    # Create client and control lights
    async with NanoleafCoAPClient(ipv6, token) as client:
        # Turn on and set to warm white at 75% brightness
        payload = json.dumps({
            "on": {"value": True},
            "brightness": {"value": 75},
            "ct": {"value": 2700}
        })
        result = await client.put("/api/v1/state", payload)
        print(f"Light control result: {result}")

# Run it
asyncio.run(control_lights())
```

## Common Issues and Solutions

### "Connection timeout" or "Network unreachable"

**Causes:**
- Device is not on the Thread network
- IPv6 address is incorrect
- Border gateway is not functioning

**Solutions:**
- Verify the device is powered on and connected to Thread
- Double-check the IPv6 address
- Ensure your computer can reach the Thread network through the border gateway
- Try pinging the IPv6 address: `ping6 fe80::your:device:address`

### "Authentication error" or "Unauthorized"

**Cause:**
- Access token is invalid or expired

**Solution:**
- Verify your access token is correct
- Regenerate the access token if needed
- Ensure the token matches the specific device

### "Module not found" errors

**Cause:**
- aiocoap not installed

**Solution:**
```bash
pip3 install -r requirements.txt
```

### Import errors with aiocoap

**Cause:**
- Python version incompatibility

**Solution:**
- Ensure you're using Python 3.7 or higher: `python3 --version`
- Try upgrading pip: `pip3 install --upgrade pip`
- Reinstall aiocoap: `pip3 install --upgrade aiocoap`

## Next Steps

Once you have basic connectivity working:

1. **Explore the API**: Check out `API_REFERENCE.md` for detailed endpoint documentation
2. **Customize**: Modify `example.py` or create your own scripts
3. **Automate**: Use the library in home automation scripts
4. **Integrate**: Combine with other systems (Home Assistant, Node-RED, etc.)

## Additional Resources

- [API_REFERENCE.md](API_REFERENCE.md) - Complete API documentation
- [README.md](README.md) - Project overview and detailed usage
- [nanoleaf-ltpdu](https://github.com/roysjosh/nanoleaf-ltpdu) - Original LTPDU protocol documentation
- [aiocoap docs](https://aiocoap.readthedocs.io/) - Python CoAP library documentation

## Getting Help

If you encounter issues:

1. Run the import test to verify basic functionality: `python3 test_import.py`
2. Check that environment variables are set: `echo $NANOLEAF_IPV6 $NANOLEAF_TOKEN`
3. Review the troubleshooting section in `README.md`
4. Check the issue tracker on GitHub

## Contributing

Found a bug or have an improvement? Contributions are welcome!

---

Happy lighting! 💡
