# src/publichost/exceptions.py
class TunnelError(Exception):
    """Base exception for tunnel-related errors."""
    pass

# src/publichost/__init__.py
from .tunnel import Tunnel
from .exceptions import TunnelError

__version__ = "0.1.0"
__all__ = ["Tunnel", "TunnelError"]