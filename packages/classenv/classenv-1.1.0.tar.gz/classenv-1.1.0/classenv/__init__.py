"""
Use a decorator to specify environment variables with automatic type parsing!
"""
__version__ = "1.1.0"
from classenv.decorator import environment
from classenv.models import ParsedConfig, RawConfig
from classenv.types import JSON, Base64, Base85


__all__ = (
    "environment",
    "ParsedConfig",
    "RawConfig",
    "JSON",
    "Base64",
    "Base85",
)
