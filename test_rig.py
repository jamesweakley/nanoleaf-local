#!/usr/bin/env python3
"""
Test rig for Nanoleaf CoAP communication over Thread.

This script provides an interactive way to test various CoAP commands
with Nanoleaf downlights.
"""
import os
import sys
import asyncio
import json
from typing import Optional
from nanoleaf_coap import NanoleafCoAPClient


async def test_basic_info(client: NanoleafCoAPClient):
    """Test basic device information retrieval."""
    print("\n=== Test: Basic Device Info ===")
    response = await client.get("/api/v1/info")
    print(json.dumps(response, indent=2))
    return response


async def test_state(client: NanoleafCoAPClient):
    """Test getting device state."""
    print("\n=== Test: Device State ===")
    response = await client.get("/api/v1/state")
    print(json.dumps(response, indent=2))
    return response


async def test_power_on(client: NanoleafCoAPClient):
    """Test turning on the device."""
    print("\n=== Test: Power On ===")
    payload = json.dumps({"on": {"value": True}})
    response = await client.put("/api/v1/state", payload)
    print(json.dumps(response, indent=2))
    return response


async def test_power_off(client: NanoleafCoAPClient):
    """Test turning off the device."""
    print("\n=== Test: Power Off ===")
    payload = json.dumps({"on": {"value": False}})
    response = await client.put("/api/v1/state", payload)
    print(json.dumps(response, indent=2))
    return response


async def test_brightness(client: NanoleafCoAPClient, brightness: int):
    """Test setting brightness."""
    print(f"\n=== Test: Set Brightness to {brightness}% ===")
    payload = json.dumps({"brightness": {"value": brightness}})
    response = await client.put("/api/v1/state", payload)
    print(json.dumps(response, indent=2))
    return response


async def test_color_temperature(client: NanoleafCoAPClient, temp: int):
    """Test setting color temperature."""
    print(f"\n=== Test: Set Color Temperature to {temp}K ===")
    payload = json.dumps({"ct": {"value": temp}})
    response = await client.put("/api/v1/state", payload)
    print(json.dumps(response, indent=2))
    return response


async def test_hue_saturation(client: NanoleafCoAPClient, hue: int, sat: int):
    """Test setting hue and saturation."""
    print(f"\n=== Test: Set Hue to {hue}, Saturation to {sat} ===")
    payload = json.dumps({"hue": {"value": hue}, "sat": {"value": sat}})
    response = await client.put("/api/v1/state", payload)
    print(json.dumps(response, indent=2))
    return response


async def run_all_tests(client: NanoleafCoAPClient):
    """Run a comprehensive test suite."""
    print("\n" + "="*60)
    print("Running Comprehensive Test Suite")
    print("="*60)
    
    # Basic info tests
    await test_basic_info(client)
    await asyncio.sleep(1)
    
    await test_state(client)
    await asyncio.sleep(1)
    
    # Power tests
    await test_power_on(client)
    await asyncio.sleep(2)
    
    await test_power_off(client)
    await asyncio.sleep(2)
    
    await test_power_on(client)
    await asyncio.sleep(2)
    
    # Brightness tests
    await test_brightness(client, 25)
    await asyncio.sleep(2)
    
    await test_brightness(client, 50)
    await asyncio.sleep(2)
    
    await test_brightness(client, 100)
    await asyncio.sleep(2)
    
    # Color temperature test (if supported)
    await test_color_temperature(client, 2700)
    await asyncio.sleep(2)
    
    await test_color_temperature(client, 6500)
    await asyncio.sleep(2)
    
    print("\n" + "="*60)
    print("Test Suite Complete")
    print("="*60)


async def interactive_mode(client: NanoleafCoAPClient):
    """Run in interactive mode."""
    
    def get_validated_int(prompt: str, min_val: int, max_val: int) -> Optional[int]:
        """Get a validated integer input from user."""
        try:
            value = int(input(prompt))
            if not min_val <= value <= max_val:
                print(f"Error: Value must be between {min_val} and {max_val}")
                return None
            return value
        except ValueError:
            print("Error: Please enter a valid integer")
            return None
    
    print("\n" + "="*60)
    print("Interactive Mode")
    print("="*60)
    print("\nAvailable commands:")
    print("  1. info       - Get device information")
    print("  2. state      - Get device state")
    print("  3. on         - Turn on the device")
    print("  4. off        - Turn off the device")
    print("  5. brightness - Set brightness (0-100)")
    print("  6. ct         - Set color temperature (2700-6500K)")
    print("  7. hue        - Set hue (0-360) and saturation (0-100)")
    print("  8. get        - Custom GET request")
    print("  9. put        - Custom PUT request")
    print("  0. quit       - Exit interactive mode")
    print("="*60)
    
    while True:
        try:
            command = input("\nEnter command: ").strip().lower()
            
            if command == "quit" or command == "0":
                break
            elif command == "info" or command == "1":
                await test_basic_info(client)
            elif command == "state" or command == "2":
                await test_state(client)
            elif command == "on" or command == "3":
                await test_power_on(client)
            elif command == "off" or command == "4":
                await test_power_off(client)
            elif command == "brightness" or command == "5":
                brightness = get_validated_int("Enter brightness (0-100): ", 0, 100)
                if brightness is not None:
                    await test_brightness(client, brightness)
            elif command == "ct" or command == "6":
                temp = get_validated_int("Enter color temperature (2700-6500K): ", 2700, 6500)
                if temp is not None:
                    await test_color_temperature(client, temp)
            elif command == "hue" or command == "7":
                hue = get_validated_int("Enter hue (0-360): ", 0, 360)
                if hue is not None:
                    sat = get_validated_int("Enter saturation (0-100): ", 0, 100)
                    if sat is not None:
                        await test_hue_saturation(client, hue, sat)
            elif command == "get" or command == "8":
                path = input("Enter path (e.g., /api/v1/info): ")
                response = await client.get(path)
                print(json.dumps(response, indent=2))
            elif command == "put" or command == "9":
                path = input("Enter path: ")
                payload = input("Enter payload (JSON): ")
                response = await client.put(path, payload)
                print(json.dumps(response, indent=2))
            else:
                print("Unknown command. Try again.")
                
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


async def main():
    """Main entry point for the test rig."""
    # Get configuration from environment variables
    ipv6_address = os.getenv("NANOLEAF_IPV6")
    access_token = os.getenv("NANOLEAF_TOKEN")
    
    if not ipv6_address or not access_token:
        print("Error: Please set NANOLEAF_IPV6 and NANOLEAF_TOKEN environment variables")
        print("\nExample:")
        print("  export NANOLEAF_IPV6='fe80::1234:5678:90ab:cdef'")
        print("  export NANOLEAF_TOKEN='your-access-token-here'")
        print("\nThen run:")
        print("  python test_rig.py [test|interactive]")
        sys.exit(1)
    
    mode = sys.argv[1] if len(sys.argv) > 1 else "interactive"
    
    print(f"Connecting to Nanoleaf device at [{ipv6_address}]...")
    print(f"Mode: {mode}")
    
    async with NanoleafCoAPClient(ipv6_address, access_token) as client:
        if mode == "test":
            await run_all_tests(client)
        elif mode == "interactive":
            await interactive_mode(client)
        else:
            print(f"Unknown mode: {mode}")
            print("Usage: python test_rig.py [test|interactive]")
            sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
