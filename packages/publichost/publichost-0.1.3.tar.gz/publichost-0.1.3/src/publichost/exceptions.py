# src/publichost/exceptions.py

class TunnelError(Exception):
    """Base exception for tunnel-related errors."""
    pass

class ConnectionError(TunnelError):
    """Raised when connection to service cannot be established."""
    pass

class ProxyError(TunnelError):
    """Raised when request proxying fails."""
    pass