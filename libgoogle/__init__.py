"""Connect to Google services.

The `libgoogle` package provides a function to connect to a google
service (such as Calendar, Drive and Mail), and manage credentials
and access tokens under the `xdg` schema.
"""

from libgoogle.libgoogle import connect_to_google, set_debug, use_cache

__all__ = ["connect_to_google", "set_debug", "use_cache"]
