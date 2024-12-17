## libgoogle

Connect to Google services.

The `libgoogle` package provides a function to connect to a google
service (such as Calendar, Drive and Mail), and manage credentials
and access tokens.


### function connect_to_google

Connect to Google service identified by `scope`.

Args:
    scope:          (valid examples):
                    "https://www.googleapis.com/auth/gmail"
                    "https://www.googleapis.com/auth/gmail.readonly"
                    "gmail"
                    "gmail.readonly"
                    "drive.metadata.readonly"
                    "photoslibrary.readonly"

    version:        "v1", "v3", etc.

Files:
    credentials:    XDG_CONFIG_HOME / libgoogle / credentials.json
                    Must exist, or raises FileNotFoundError.

    token:          XDG_CACHE_HOME / libgoogle / {scope}-token.json


### function set_debug

Turn on/off low-level httplib2 debugging.

### function use_cache

Use cache or not.

