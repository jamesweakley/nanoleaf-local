#!/usr/bin/env python3
"""
Simple example demonstrating basic Nanoleaf CoAP control.

This is a minimal example showing how to use the NanoleafCoAPClient.
"""
import os
import asyncio
import json
from nanoleaf_coap import NanoleafCoAPClient


async def main():
    # Get configuration from environment
    ipv6_address = os.getenv("NANOLEAF_IPV6")
    access_token = os.getenv("NANOLEAF_TOKEN")
    
    if not ipv6_address or not access_token:
        print("Please set NANOLEAF_IPV6 and NANOLEAF_TOKEN environment variables")
        return
    
    # Create and use the client
    async with NanoleafCoAPClient(ipv6_address, access_token) as client:
        # Get device information
        print("Getting device info...")
        info = await client.get("/api/v1/info")
        print(f"Device info: {json.dumps(info, indent=2)}\n")
        
        # Turn on the light
        print("Turning on the light...")
        payload = json.dumps({"on": {"value": True}})
        result = await client.put("/api/v1/state", payload)
        print(f"Result: {result}\n")
        
        # Wait a moment
        await asyncio.sleep(2)
        
        # Set brightness to 50%
        print("Setting brightness to 50%...")
        payload = json.dumps({"brightness": {"value": 50}})
        result = await client.put("/api/v1/state", payload)
        print(f"Result: {result}\n")
        
        # Wait a moment
        await asyncio.sleep(2)
        
        # Get current state
        print("Getting current state...")
        state = await client.get("/api/v1/state")
        print(f"Current state: {json.dumps(state, indent=2)}")


if __name__ == "__main__":
    asyncio.run(main())
