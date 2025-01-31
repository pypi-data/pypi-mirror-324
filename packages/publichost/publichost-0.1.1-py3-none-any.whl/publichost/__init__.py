# src/publichost/__init__.py
from .tunnel import Tunnel
from .exceptions import TunnelError, ConnectionError, ProxyError

__version__ = "0.1.0"
__all__ = ["Tunnel", "TunnelError", "ConnectionError", "ProxyError"]