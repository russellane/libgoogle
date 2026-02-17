"""Connect to Google Service API's.

The `libgoogle` package provides a function to connect to a google
service (such as Calendar, Drive and Mail), and manage credentials
and access tokens under the `XDG` schema.
"""

import httplib2
import xdg
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore[import-untyped]
from googleapiclient.discovery import Resource, build  # type: ignore[import-untyped]
from loguru import logger

__all__ = ["connect", "set_debug"]


def connect(scope: str, version: str) -> Resource:
    """Connect to Google service identified by `scope` and `version`.

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
    """

    # Normalize `scope` to be abbreviated (without the prefix).
    scope_prefix = "https://www.googleapis.com/auth/"
    if scope.startswith(scope_prefix):
        scope = scope[len(scope_prefix) :]  # strip prefix

    # Path to user's credentials.
    credentials_dir = xdg.xdg_config_home() / "libgoogle"
    credentials_dir.mkdir(parents=True, exist_ok=True)
    credentials_file = credentials_dir / "credentials.json"
    if not credentials_file.exists():  # pragma: no cover
        raise FileNotFoundError(f"Can't find credentials: {str(credentials_file)!r}")

    # Path to access token.
    token_dir = xdg.xdg_cache_home() / "libgoogle"
    token_dir.mkdir(parents=True, exist_ok=True)
    token_file = token_dir / f"{scope}-token.json"

    # Check access token.
    scopes = [scope_prefix + scope]  # fully qualified
    creds = None
    if token_file.exists():
        logger.trace(f"Using access token {str(token_file)!r}")
        creds = Credentials.from_authorized_user_file(token_file, scopes)  # type: ignore[no-untyped-call]

    # Refresh access-token, or (re-)authorize user, as necessary.
    if not creds or not creds.valid:  # pragma: no cover
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            logger.debug(f"Signing in with {str(credentials_file)!r}")
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, scopes)
            creds = flow.run_local_server(port=0)

        # Save access token.
        with open(token_file, "w", encoding="utf-8") as fp:
            fp.write(creds.to_json())

    # Connect to service.
    service_name = scope.split(".")[0]
    logger.debug(f"Connecting to service={service_name!r} version={version!r}")

    service = build(
        service_name,
        version,
        credentials=creds,
        cache_discovery=False,
    )

    return service


def set_debug(flag: bool) -> None:
    """Turn on/off low-level `httplib2` debugging.

    Args:
        flag:   True to turn on debugging, False to turn off.
    """

    if flag:
        httplib2.debuglevel = 4  # type: ignore[misc]
    else:
        httplib2.debuglevel = 0  # type: ignore[misc]
