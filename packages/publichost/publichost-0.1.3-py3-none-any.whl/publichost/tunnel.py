# src/publichost/tunnel.py
import asyncio
import json
import logging
import re
import socket
import os
import websockets
from typing import Optional
from websockets.exceptions import WebSocketException
from .exceptions import ConnectionError, ProxyError, TunnelError
from .utils import generate_subdomain, RESERVED_WORDS
import threading

logger = logging.getLogger(__name__)

class Tunnel:
    """A tunnel that makes a local port accessible via a public URL."""

    SUBDOMAIN_PATTERN = re.compile(r'^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$')

    # Default production URLs
    DEFAULT_WS_URL = "wss://tunnel.publichost.dev"
    DEFAULT_PUBLIC_DOMAIN = "publichost.dev"
    
    def __init__(
        self, 
        port: int, 
        subdomain: Optional[str] = None,
        dev_mode: bool = False
    ):
        """
        Initialize a new tunnel.

        Args:
            port: Local port to tunnel
            subdomain: Optional custom subdomain to use
            dev_mode: Enable development mode (uses localhost)

        Raises:
            TunnelError: If the subdomain is invalid or reserved
            ConnectionError: If the tunnel service is unreachable
        """
        if not isinstance(port, int) or port < 1 or port > 65535:
            raise TunnelError("Port must be between 1 and 65535")

        self.port = port
        self.subdomain = self._validate_subdomain(subdomain) if subdomain else generate_subdomain()
        
        # Configure URLs based on environment
        self.ws_url = self._get_ws_url(dev_mode)
        self.public_url = self._get_public_url(dev_mode)
        
        # Start the tunnel in a separate thread
        self.tunnel_thread = threading.Thread(target=self._start_tunnel)
        self.tunnel_thread.daemon = True
        self.tunnel_thread.start()

    def _get_ws_url(self, dev_mode: bool) -> str:
        """Get WebSocket URL based on environment."""
        if dev_mode:
            return "ws://localhost:8765"
        return os.getenv("PUBLICHOST_WS_URL", self.DEFAULT_WS_URL)

    def _get_public_url(self, dev_mode: bool) -> str:
        """Get public URL based on environment."""
        domain = "localhost:8000" if dev_mode else os.getenv("PUBLICHOST_DOMAIN", self.DEFAULT_PUBLIC_DOMAIN)
        protocol = "http" if dev_mode else "https"
        return f"{protocol}://{self.subdomain}.{domain}"

    def _validate_subdomain(self, subdomain: str) -> str:
        """Validate and normalize a custom subdomain."""
        subdomain = subdomain.lower()

        if subdomain in RESERVED_WORDS:
            raise TunnelError(f"Subdomain '{subdomain}' is reserved")

        if not self.SUBDOMAIN_PATTERN.match(subdomain):
            raise TunnelError(
                "Subdomain must contain only letters, numbers, and hyphens, "
                "and must not start or end with a hyphen"
            )

        return subdomain

    def _start_tunnel(self) -> None:
        """Start the tunnel connection."""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self._connect())
            logger.info(f"Tunnel established at {self.public_url}")
            loop.run_forever()
        except (socket.gaierror, WebSocketException) as e:
            raise ConnectionError("Unable to reach tunnel service") from e
        except Exception as e:
            raise TunnelError(str(e))
        finally:
            loop.close()

    async def _connect(self) -> None:
        """Establish and maintain WebSocket connection."""
        async with websockets.connect(self.ws_url) as ws:
            await ws.send(json.dumps({
                "type": "register",
                "tunnel_id": self.subdomain,
                "local_port": self.port
            }))
            
            await asyncio.gather(
                self._handle_messages(ws),
                self._keep_alive(ws)
            )

    async def _keep_alive(self, ws: websockets.WebSocketClientProtocol) -> None:
        """Send periodic ping messages to keep connection alive."""
        while True:
            try:
                await asyncio.sleep(30)
                await ws.send(json.dumps({"type": "ping"}))
            except Exception:
                break

    async def _handle_messages(self, ws: websockets.WebSocketClientProtocol) -> None:
        """Process incoming WebSocket messages."""
        async for message in ws:
            try:
                data = json.loads(message)
                if data["type"] == "request":
                    response = await self._proxy_request(data)
                    await ws.send(json.dumps(response))
            except json.JSONDecodeError:
                logger.error("Invalid message format received")
            except Exception as e:
                logger.error(f"Error handling message: {str(e)}")

    async def _proxy_request(self, data: dict) -> dict:
        """Forward request to local server and return response."""
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
            except aiohttp.ClientError as e:
                return {
                    "type": "response",
                    "request_id": data["request_id"],
                    "status": 502,
                    "headers": {},
                    "content": f"Failed to reach local server on port {self.port}"
                }

    def __str__(self) -> str:
        """Return the public URL of the tunnel."""
        return self.public_url