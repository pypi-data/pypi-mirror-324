# src/publichost/tunnel.py
import asyncio
import json
import logging
import string
import random
import websockets
from typing import Optional

logger = logging.getLogger(__name__)

class Tunnel:
    """
    A tunnel that makes a local port accessible via a public URL.
    
    Args:
        port (int): The local port to tunnel
        subdomain (str, optional): Custom subdomain to use
    """
    
    def __init__(
        self, 
        port: int,
        subdomain: Optional[str] = None
    ):
        self.port = port
        self.subdomain = subdomain or self._generate_subdomain()
        self.public_url = f"https://{self.subdomain}.publichost.dev"
        self.ws_url = "wss://tunnel.publichost.dev"
        self._start_tunnel()
        
    def _generate_subdomain(self, length: int = 5) -> str:
        """Generate a random subdomain."""
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))
    
    def _start_tunnel(self) -> None:
        """Start the tunnel connection."""
        try:
            asyncio.get_event_loop().run_until_complete(self._connect())
            logger.info(f"Tunnel established at {self.public_url}")
        except Exception as e:
            raise Exception(f"Failed to establish tunnel: {str(e)}")
    
    async def _connect(self) -> None:
        """Establish WebSocket connection with tunnel server."""
        async with websockets.connect(self.ws_url) as ws:
            # Register tunnel
            await ws.send(json.dumps({
                "type": "register",
                "tunnel_id": self.subdomain,
                "local_port": self.port
            }))
            
            # Handle tunnel traffic
            asyncio.create_task(self._handle_messages(ws))
            
            while True:
                try:
                    await asyncio.sleep(30)
                    await ws.send(json.dumps({"type": "ping"}))
                except websockets.exceptions.ConnectionClosed:
                    break
                except Exception as e:
                    logger.error(f"Error in tunnel connection: {str(e)}")
                    break
    
    async def _handle_messages(self, ws: websockets.WebSocketClientProtocol) -> None:
        """Handle incoming WebSocket messages."""
        async for message in ws:
            try:
                data = json.loads(message)
                if data["type"] == "request":
                    response = await self._proxy_request(data)
                    await ws.send(json.dumps(response))
            except Exception as e:
                logger.error(f"Error handling message: {str(e)}")
    
    async def _proxy_request(self, data: dict) -> dict:
        """Proxy request to local port and return response."""
        import aiohttp
        
        url = f"http://localhost:{self.port}{data['path']}"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(
                    method=data["method"],
                    url=url,
                    headers=data["headers"],
                    data=data.get("body", "")
                ) as response:
                    return {
                        "type": "response",
                        "request_id": data["request_id"],
                        "status": response.status,
                        "headers": dict(response.headers),
                        "content": await response.text()
                    }
            except Exception as e:
                return {
                    "type": "response",
                    "request_id": data["request_id"],
                    "status": 502,
                    "headers": {},
                    "content": f"Failed to proxy request: {str(e)}"
                }
    
    def __str__(self) -> str:
        return self.public_url