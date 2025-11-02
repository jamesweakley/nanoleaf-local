"""
Nanoleaf CoAP client for controlling Nanoleaf downlights over Thread.

Based on the LTPDU protocol documented at:
https://github.com/roysjosh/nanoleaf-ltpdu
"""
import os
import asyncio
from typing import Optional
import aiocoap
from aiocoap import Context, Message, Code


class NanoleafCoAPClient:
    """Client for controlling Nanoleaf devices via CoAP over Thread."""
    
    def __init__(self, ipv6_address: str, access_token: str):
        """
        Initialize the Nanoleaf CoAP client.
        
        Args:
            ipv6_address: The IPv6 address of the Nanoleaf device
            access_token: The access token for authentication
        """
        self.ipv6_address = ipv6_address
        self.access_token = access_token
        self.context: Optional[Context] = None
        
    async def __aenter__(self):
        """Async context manager entry."""
        self.context = await Context.create_client_context()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.context:
            await self.context.shutdown()
            
    def _build_uri(self, path: str) -> str:
        """
        Build a CoAP URI for the device.
        
        Args:
            path: The path component of the URI
            
        Returns:
            Complete CoAP URI
        """
        # For IPv6 addresses, we need to wrap them in brackets
        return f"coap://[{self.ipv6_address}]{path}"
    
    async def get(self, path: str) -> dict:
        """
        Send a GET request to the device.
        
        Args:
            path: The API path to query
            
        Returns:
            Response payload as dict
        """
        if not self.context:
            raise RuntimeError("Client context not initialized. Use async with statement.")
            
        uri = self._build_uri(path)
        request = Message(code=Code.GET, uri=uri)
        
        # Add access token as a URI query parameter
        request.opt.uri_query = (f"auth={self.access_token}",)
        
        try:
            response = await self.context.request(request).response
            return {
                "status": "success",
                "code": response.code,
                "payload": response.payload.decode('utf-8') if response.payload else ""
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def put(self, path: str, payload: str = "") -> dict:
        """
        Send a PUT request to the device.
        
        Args:
            path: The API path to update
            payload: The payload to send
            
        Returns:
            Response payload as dict
        """
        if not self.context:
            raise RuntimeError("Client context not initialized. Use async with statement.")
            
        uri = self._build_uri(path)
        request = Message(code=Code.PUT, uri=uri, payload=payload.encode('utf-8'))
        
        # Add access token as a URI query parameter
        request.opt.uri_query = (f"auth={self.access_token}",)
        
        try:
            response = await self.context.request(request).response
            return {
                "status": "success",
                "code": response.code,
                "payload": response.payload.decode('utf-8') if response.payload else ""
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def post(self, path: str, payload: str = "") -> dict:
        """
        Send a POST request to the device.
        
        Args:
            path: The API path
            payload: The payload to send
            
        Returns:
            Response payload as dict
        """
        if not self.context:
            raise RuntimeError("Client context not initialized. Use async with statement.")
            
        uri = self._build_uri(path)
        request = Message(code=Code.POST, uri=uri, payload=payload.encode('utf-8'))
        
        # Add access token as a URI query parameter
        request.opt.uri_query = (f"auth={self.access_token}",)
        
        try:
            response = await self.context.request(request).response
            return {
                "status": "success",
                "code": response.code,
                "payload": response.payload.decode('utf-8') if response.payload else ""
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }


async def main():
    """Example usage of the Nanoleaf CoAP client."""
    # Get configuration from environment variables
    ipv6_address = os.getenv("NANOLEAF_IPV6")
    access_token = os.getenv("NANOLEAF_TOKEN")
    
    if not ipv6_address or not access_token:
        print("Error: Please set NANOLEAF_IPV6 and NANOLEAF_TOKEN environment variables")
        print("Example:")
        print("  export NANOLEAF_IPV6='fe80::1234:5678:90ab:cdef'")
        print("  export NANOLEAF_TOKEN='your-access-token-here'")
        return
    
    print(f"Connecting to Nanoleaf device at [{ipv6_address}]...")
    
    async with NanoleafCoAPClient(ipv6_address, access_token) as client:
        # Example: Get device info
        print("\n--- Getting device info ---")
        response = await client.get("/api/v1/info")
        print(f"Response: {response}")
        
        # Example: Get state
        print("\n--- Getting device state ---")
        response = await client.get("/api/v1/state")
        print(f"Response: {response}")


if __name__ == "__main__":
    asyncio.run(main())
